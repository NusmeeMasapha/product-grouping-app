import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict

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