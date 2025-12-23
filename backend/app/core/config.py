
import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv('PORT', '8000'))
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./dev.db')

# Auth
SECRET_KEY = os.getenv('SECRET_KEY', 'CHANGE_ME')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))

# RAG
RAG_STORE = os.getenv('RAG_STORE', 'local')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
RAG_STORE_PATH = os.getenv('RAG_STORE_PATH', 'rag_store.json')

# Pinecone
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', '')
PINECONE_INDEX = os.getenv('PINECONE_INDEX', 'products-index')
PINECONE_CLOUD = os.getenv('PINECONE_CLOUD', 'aws')
PINECONE_REGION = os.getenv('PINECONE_REGION', 'us-east-1')
