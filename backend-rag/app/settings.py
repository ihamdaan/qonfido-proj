from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent 
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Embedding model
EMBED_MODEL = "all-MiniLM-L6-v2"

# FAISS file
FAISS_INDEX_PATH = DATA_DIR / "vector_store.faiss"
EMBEDDINGS_CACHE_PATH = DATA_DIR / "embedding_cache"

# DiskCache directory
DISKCACHE_DIR = str(EMBEDDINGS_CACHE_PATH)

# OpenRouter
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
LLM_MODEL = "openai/gpt-oss-120b"
MAX_TOKEN_OUTPUT = 2200

# Retrieval tuning
TOP_K_LEXICAL = 10
TOP_K_SEMANTIC = 10
HYBRID_ALPHA = 0.5 # weight for semantic when fusing scores (0 to 1)