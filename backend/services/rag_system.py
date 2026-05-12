import os
import json
from typing import List, Optional
import openai
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from config import OPENAI_API_KEY, CHROMA_DB_PATH, EMBEDDING_MODEL

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

class RAGSystem:
    """Retrieval-Augmented Generation system for property documents"""
    
    def __init__(self):
        """Initialize RAG system"""
        self.embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize or load Chroma DB
        try:
            self.vectordb = Chroma(
                persist_directory=CHROMA_DB_PATH,
                embedding_function=self.embedding_model
            )
        except:
            self.vectordb = None
        
        self.llm = OpenAI(
            openai_api_key=OPENAI_API_KEY,
            temperature=0.7,
            max_tokens=500
        )
    
    def index_document(self, file_path: str, document_type: str = "general") -> bool:
        """Index a document to the vector store"""
        try:
            # Read document
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                document_text = f.read()
            
            # Split text
            chunks = self.text_splitter.split_text(document_text)
            
            if not chunks:
                return False
            
            # Add to vector store
            if self.vectordb is None:
                self.vectordb = Chroma(
                    persist_directory=CHROMA_DB_PATH,
                    embedding_function=self.embedding_model
                )
            
            # Add documents with metadata
            metadatas = [
                {
                    "source": file_path,
                    "type": document_type,
                    "chunk": i
                }
                for i in range(len(chunks))
            ]
            
            self.vectordb.add_texts(texts=chunks, metadatas=metadatas)
            self.vectordb.persist()
            
            return True
        except Exception as e:
            print(f"Error indexing document: {e}")
            return False
    
    def query(self, question: str, property_context: Optional[dict] = None) -> str:
        """Query the RAG system"""
        try:
            if self.vectordb is None:
                return "No documents indexed yet. Please upload property documents first."
            
            # Retrieve relevant documents
            retriever = self.vectordb.as_retriever(search_kwargs={"k": 5})
            
            # Create QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )
            
            # Build context-aware question
            context_str = ""
            if property_context:
                context_str = f"Property Context: {json.dumps(property_context, indent=2)}\n\n"
            
            full_question = f"{context_str}Question: {question}"
            
            # Get response
            result = qa_chain({"query": full_question})
            
            return result.get("result", "Unable to find an answer.")
        except Exception as e:
            print(f"Error querying RAG: {e}")
            return f"Error: {str(e)}"
    
    def get_property_summary(self, document_path: str) -> str:
        """Generate a summary of a property document"""
        try:
            with open(document_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()[:5000]  # Limit to 5000 chars
            
            prompt = f"""Please provide a concise summary of the following property document:

{text}

Summary:"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a real estate document expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def extract_key_information(self, document_path: str) -> dict:
        """Extract key information from a property document"""
        try:
            with open(document_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()[:5000]
            
            prompt = f"""Extract key information from this property document in JSON format:
{{
    "property_type": "",
    "location": "",
    "price": "",
    "bedrooms": "",
    "bathrooms": "",
    "area": "",
    "key_features": [],
    "amenities": []
}}

Document:
{text}

JSON:"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract data and return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            
            result = response['choices'][0]['message']['content']
            return json.loads(result)
        except Exception as e:
            return {"error": str(e)}
    
    def compare_properties(self, property_ids: List[int], criteria: Optional[List[str]] = None) -> str:
        """Compare multiple properties"""
        context = f"Compare the following property IDs: {', '.join(map(str, property_ids))}"
        if criteria:
            context += f"\nComparison criteria: {', '.join(criteria)}"
        
        question = f"{context}\nProvide a detailed comparison."
        
        return self.query(question)
    
    def get_area_insights(self, area: str) -> str:
        """Get insights about a specific area"""
        question = f"""Provide detailed insights about the real estate market in {area}, including:
        - Market trends
        - Average property prices
        - Popular property types
        - Investment potential
        - Nearby amenities
        - Transportation connectivity"""
        
        return self.query(question)

# Initialize global RAG system
rag_system = RAGSystem()
