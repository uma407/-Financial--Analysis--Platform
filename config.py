"""
Configuration file for the Financial Analysis Platform
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Model Configuration
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"  # Can be changed to gpt-4, claude, gemini, etc.

# Vector Store Configuration
VECTOR_STORE_TYPE = "chroma"  # Options: "chroma" or "faiss"
CHROMA_PERSIST_DIR = "./chroma_db"
FAISS_INDEX_PATH = "./faiss_index"

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_CHUNKS = 5

# Portfolio Configuration
RISK_FREE_RATE = 0.02  # 2% annual risk-free rate
MAX_PORTFOLIO_WEIGHT = 0.25  # Maximum 25% allocation to single asset

# Data Paths
DATA_DIR = "./data"
SAMPLE_FINANCIAL_DATA = os.path.join(DATA_DIR, "financial_statements.csv")
SAMPLE_PORTFOLIO_DATA = os.path.join(DATA_DIR, "portfolio_data.csv")
