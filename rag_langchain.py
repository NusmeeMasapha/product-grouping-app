from langchain_anthropic import ChatAnthropic
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
import os

class AdvancedRAG:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('CLAUDE_API_KEY')
        
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY is required")
        
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            anthropic_api_key=self.api_key,
            max_tokens=4000,
            temperature=0.7
        )
        
        print("Loading embeddings model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        self.vectorstore = None
        self.qa_chain = None
        self.data_loaded = False
        
    def get_relevant_context(self, question: str, k: int = 3) -> str:
        """Retrieve relevant context for the question"""
        if not self.vectorstore:
            return "No data available."
            
        docs = self.vectorstore.similarity_search(question, k=k)
        return "\n\n".join(doc.page_content for doc in docs)
    
    def ask(self, question: str) -> str:
        """Process a question and return an answer"""
        if not self.data_loaded:
            raise ValueError("No data loaded. Please load data first.")
            
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Please load data first.")
            
        try:
            result = self.qa_chain.invoke({
                "question": question,
                "context": self.get_relevant_context(question)
            })
            return str(result)
        except Exception as e:
            raise Exception(f"Error processing question: {str(e)}")

    def load_data(self, groups_data, total_products, similar_pairs):
        """Load and index data into vector store"""
        print(f"Loading {len(groups_data)} groups into RAG system...")
        
        documents = []
        
        summary_text = f"""ข้อมูลภาพรวม:
        - สินค้าทั้งหมด: {total_products} รายการ
        - จำนวนกลุ่มสินค้า: {len(groups_data)} กลุ่ม
        - คู่สินค้าที่คล้ายกัน: {similar_pairs} คู่

        กลุ่มที่มียอดขายสูงสุด 5 อันดับ:
        """
        
        top_5 = sorted(groups_data, key=lambda x: x['total_sales'], reverse=True)[:5]
        for i, group in enumerate(top_5, 1):
            summary_text += f"{i}. กลุ่มที่ {group['group_number']}: {group['total_sales']:,.2f} บาท ({group['count']} รายการ)\n"
        
        documents.append(Document(
            page_content=summary_text,
            metadata={'type': 'summary', 'group_number': 0}
        ))
        
        for group in groups_data:
            group_text = f"""กลุ่มสินค้าที่ {group['group_number']}

ข้อมูลกลุ่ม:
- จำนวนสินค้าในกลุ่ม: {group['count']} รายการ
- ยอดขายรวมของกลุ่ม: {group['total_sales']:,.2f} บาท
- ยอดขายเฉลี่ยต่อสินค้า: {group['total_sales']/group['count']:,.2f} บาท

รายการสินค้าในกลุ่ม:
"""
            
            for idx, product in enumerate(group['products'], 1):
                group_text += f"{idx}. {product['description']}\n"
                group_text += f"   - ยอดขาย: {product['sales_value']:,.2f} บาท\n"
                group_text += f"   - คิดเป็น {(product['sales_value']/group['total_sales']*100):.1f}% ของกลุ่ม\n"
            
            documents.append(Document(
                page_content=group_text,
                metadata={
                    'type': 'group',
                    'group_number': group['group_number'],
                    'total_sales': group['total_sales'],
                    'count': group['count']
                }
            ))
            
            for product in group['products']:
                product_text = f"""สินค้า: {product['description']}
ยอดขาย: {product['sales_value']:,.2f} บาท
กลุ่ม: กลุ่มที่ {group['group_number']}
"""
                documents.append(Document(
                    page_content=product_text,
                    metadata={
                        'type': 'product',
                        'group_number': group['group_number'],
                        'description': product['description'],
                        'sales_value': product['sales_value']
                    }
                ))
        
        print(f"Created {len(documents)} documents")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        splits = text_splitter.split_documents(documents)
        print(f"Split into {len(splits)} chunks")
        
        print("Creating vector store...")
        self.vectorstore = FAISS.from_documents(splits, self.embeddings)
        print("Vector store created successfully!")
        
        prompt_template = """คุณเป็น Data Analyst ผู้เชี่ยวชาญด้านการวิเคราะห์ข้อมูลการขายสินค้า

        ใช้ข้อมูลต่อไปนี้ในการตอบคำถาม:

        {context}

        คำถาม: {question}

        คำตอบ (ตอบเป็นภาษาไทย ชัดเจน มีตัวเลขประกอบ และให้คำแนะนำเชิงธุรกิจด้วย):"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create retriever
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}  # ดึงข้อมูล 5 chunks ที่เกี่ยวข้องที่สุด
        )
        
        # สร้าง chain แบบ LCEL (LangChain Expression Language)
        self.qa_chain = (
            {
                "context": retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)),
                "question": RunnablePassthrough()
            }
            | PROMPT
            | self.llm
            | StrOutputParser()
        )
        
        self.data_loaded = True
        print("RAG system ready!")
    
    def query(self, question):
        """Query with RAG"""
        if not self.data_loaded:
            return {
                "success": False,
                "error": "No data loaded. Please process data first."
            }
        
        try:
            print(f"Processing query: {question}")
            answer = self.qa_chain.invoke(question)
            
            # Get the relevant documents that were used
            retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5}
            )
            docs = retriever.get_relevant_documents(question)
            sources = []
            for doc in docs:
                sources.append({
                    'content': doc.page_content[:200] + "...",  # First 200 chars
                    'metadata': doc.metadata
                })
            
            return {
                "success": True,
                "answer": answer,
                "sources": sources,
                "model": "claude-sonnet-4 + FAISS"
            }
            
        except Exception as e:
            import traceback
            print(f"Error in query: {traceback.format_exc()}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_insights(self):
        """Get automatic insights"""
        if not self.data_loaded:
            return {
                "success": False,
                "error": "No data loaded"
            }
        
        insights_query = """วิเคราะห์ข้อมูลการขายและให้ insights ดังนี้:

1. กลุ่มสินค้าที่มียอดขายสูงสุด 3 อันดับ พร้อมเหตุผล
2. แนวโน้มที่น่าสนใจจากข้อมูล
3. คำแนะนำทางธุรกิจ:
   - สินค้าที่ควรมัดรวมกัน (Bundle)
   - โปรโมชั่นที่แนะนำ
   - สินค้าที่ควรเพิ่ม stock
4. จุดที่ควรปรับปรุงหรือข้อควรระวัง

กรุณาให้ insights ที่เป็นประโยชน์ มีตัวเลขประกอบ และสามารถนำไปปฏิบัติได้จริง"""

        return self.query(insights_query)
    
    def search_similar(self, query, k=5):
        """Search similar products/groups"""
        if not self.vectorstore:
            return {
                "success": False,
                "error": "No data loaded"
            }
        
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            results = []
            
            for doc in docs:
                results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata
                })
            
            return {
                "success": True,
                "results": results
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def compare_groups(self, group1, group2):
        """Compare two groups"""
        query = f"เปรียบเทียบกลุ่มที่ {group1} กับกลุ่มที่ {group2} ในแง่ของยอดขาย จำนวนสินค้า และลักษณะสินค้าในกลุ่ม"
        return self.query(query)
    
    def filter_by_keywords(self, keywords, sort_by='count', order='desc'):
        """Filter groups by keywords"""
        if not self.data_loaded:
            return {
                "success": False,
                "error": "No data loaded"
            }
        
        try:
            # Convert keywords to list if it's a string
            if isinstance(keywords, str):
                keywords = [k.strip() for k in keywords.split(',')]
            
            # Search for documents matching keywords
            if not self.vectorstore:
                return {
                    "success": False,
                    "error": "Vector store not initialized"
                }
            
            # Combine keywords into a search query
            search_query = " ".join(keywords)
            docs = self.vectorstore.similarity_search(search_query, k=20)
            
            # Filter for group documents only
            matching_groups = []
            seen_groups = set()
            
            for doc in docs:
                if doc.metadata.get('type') == 'group':
                    group_num = doc.metadata.get('group_number')
                    if group_num not in seen_groups:
                        seen_groups.add(group_num)
                        matching_groups.append({
                            'group_number': group_num,
                            'count': doc.metadata.get('count', 0),
                            'total_sales': doc.metadata.get('total_sales', 0),
                            'content': doc.page_content
                        })
            
            # Sort results
            if sort_by == 'sales':
                matching_groups.sort(key=lambda x: x['total_sales'], reverse=(order == 'desc'))
            else:  # sort by count
                matching_groups.sort(key=lambda x: x['count'], reverse=(order == 'desc'))
            
            return {
                "success": True,
                "groups": matching_groups,
                "total": len(matching_groups),
                "keywords": keywords
            }
            
        except Exception as e:
            import traceback
            print(f"Error in filter_by_keywords: {traceback.format_exc()}")
            return {
                "success": False,
                "error": str(e)
            }