# app.py
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict
import os
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Create uploads folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def process_excel_data(file_path, similarity_threshold, sort_by):
    """Process Excel file and return grouped results"""
    try:
        # Read Excel file
        data1 = pd.read_excel(file_path)
        
        # Check if required columns exist
        if "DESCRIPTION" not in data1.columns or "Sales Value" not in data1.columns:
            return {"error": "Excel file must contain 'DESCRIPTION' and 'Sales Value' columns!"}
        
        data = data1[["DESCRIPTION", "Sales Value"]].copy()
        
        # Preprocess descriptions
        data['processed_description'] = data['DESCRIPTION'].apply(preprocess_text)
        
        # TF-IDF Vectorization
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(data['processed_description'])
        
        # Calculate cosine similarity
        cosine_sim_matrix = cosine_similarity(tfidf_matrix)
        
        # Find similar pairs
        similar_pairs = []
        for i in range(cosine_sim_matrix.shape[0]):
            for j in range(i + 1, cosine_sim_matrix.shape[1]):
                if cosine_sim_matrix[i, j] > similarity_threshold:
                    similar_pairs.append((i, j))
        
        # Group similar items using DFS
        graph = defaultdict(list)
        for i, j in similar_pairs:
            graph[i].append(j)
            graph[j].append(i)
        
        visited = set()
        groups = []
        
        def dfs(node, current_group):
            visited.add(node)
            current_group.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, current_group)
        
        for i in range(data.shape[0]):
            if i not in visited:
                current_group = []
                dfs(i, current_group)
                groups.append(current_group)
        
        group_labels = np.zeros(data.shape[0], dtype=int)
        for i, group in enumerate(groups):
            for index in group:
                group_labels[index] = i
        
        data['group_label'] = group_labels
        
        # Calculate group statistics
        group_counts = data.groupby('group_label').size()
        group_sales_values = data.groupby('group_label')['Sales Value'].sum()
        
        # Sort based on user selection
        if sort_by == "sales":
            sorted_groups = group_sales_values.sort_values(ascending=False)
        else:
            sorted_groups = group_counts.sort_values(ascending=False)
        
        # Prepare results
        results = []
        for group_label in sorted_groups.index:
            count = group_counts[group_label]
            total_sales = group_sales_values[group_label]
            
            group_data = data[data['group_label'] == group_label]
            products = []
            for index, row in group_data.iterrows():
                products.append({
                    'description': row['DESCRIPTION'],
                    'sales_value': float(row['Sales Value'])
                })
            
            results.append({
                'group_number': int(group_label) + 1,
                'count': int(count),
                'total_sales': float(total_sales),
                'products': products
            })
        
        return {
            'success': True,
            'total_products': len(data),
            'similar_pairs': len(similar_pairs),
            'total_groups': len(groups),
            'threshold': similarity_threshold,
            'sort_by': 'Total Sales Value' if sort_by == 'sales' else 'Count',
            'groups': results,
            'processed_data': data
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload .xlsx or .xls file'}), 400
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get parameters
        threshold = float(request.form.get('threshold', 0.5))
        sort_by = request.form.get('sort_by', 'sales')
        
        # Process data
        result = process_excel_data(filepath, threshold, sort_by)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        if 'error' in result:
            return jsonify(result), 400
        
        # Store processed data in session for export (in production, use database or cache)
        if 'processed_data' in result:
            # Save to temp file for export
            export_path = os.path.join(app.config['UPLOAD_FOLDER'], f'result_{filename}')
            result['processed_data'].to_excel(export_path, index=False)
            result['export_filename'] = f'result_{filename}'
            del result['processed_data']  # Remove from JSON response
        
        return jsonify(result)
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing file: {error_details}")
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/export/<filename>')
def export(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return send_file(filepath, as_attachment=True, download_name=f'grouped_{filename}')
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Use gunicorn in production, flask dev server locally only
    if os.environ.get('RENDER'):
        # On Render, gunicorn will handle this
        pass
    else:
        # Local development only
        app.run(debug=False, host='0.0.0.0', port=port)
