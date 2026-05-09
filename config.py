import os
from dotenv import load_dotenv

load_dotenv()

# LLM
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
LLM_MODEL = "mistralai/mistral-7b-instruct"

# Embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 3

# DuckDB
DUCKDB_PATH = "data/knowledge_base.duckdb"

# Documents
DOCUMENTS_DIR = "documents"
