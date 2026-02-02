import os
from dotenv import load_dotenv

load_dotenv()

# Target Documentation
SITEMAP_URL = os.getenv("SITEMAP_URL", "https://docs.langchain.com/sitemap.xml")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATE_DB_PATH = os.path.join(DATA_DIR, "state", "sitemap_state.db")

# Scheduling
CHECK_INTERVAL_HOURS = 24

# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "langchain-hybrid-search")
PINECONE_NAMESPACE = "langchain_docs"
EMBEDDING_DIM = 3072

# Gemini (dense embeddings)
GOOGLE_API_KEY_EMBEDDINGS = os.getenv("GOOGLE_API_KEY_EMBEDDINGS")
GOOGLE_API_KEY_GENERATIVE = os.getenv("GOOGLE_API_KEY_EMBEDDINGS")
GEMINI_EMBED_MODEL = "models/gemini-embedding-001"
CHAT_MODEL_NAME = "gemini-2.5-flash"