import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

# Target Documentation (Legacy/Default)
SITEMAP_URL = os.getenv("SITEMAP_URL", "https://docs.langchain.com/sitemap.xml")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATE_DB_PATH = os.path.join(DATA_DIR, "state", "sitemap_state.db") # Legacy default

# Scheduling
CHECK_INTERVAL_HOURS = 24

# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "langchain-hybrid-search")
PINECONE_NAMESPACE = "langchain_docs" # Legacy default
EMBEDDING_DIM = 3072

# Gemini (dense embeddings)
GOOGLE_API_KEY_EMBEDDINGS = os.getenv("GOOGLE_API_KEY_EMBEDDINGS")
GOOGLE_API_KEY_GENERATIVE = os.getenv("GOOGLE_API_KEY_GENERATIVE")
GEMINI_EMBED_MODEL = "models/gemini-embedding-001"
CHAT_MODEL_NAME = "gemini-2.5-flash"

@dataclass
class DataSourceConfig:
    name: str
    sitemap_url: str
    state_db_path: str
    pinecone_namespace: str

def get_config(source_name: str) -> DataSourceConfig:
    state_dir = os.path.join(DATA_DIR, "state")
    os.makedirs(state_dir, exist_ok=True)
    
    configs = {
        "langchain": DataSourceConfig(
            name="langchain",
            sitemap_url=os.getenv("SITEMAP_URL", "https://docs.langchain.com/sitemap.xml"),
            state_db_path=os.path.join(state_dir, "langchain_state.db"),
            pinecone_namespace="langchain_docs"
        ),
        "stripe": DataSourceConfig(
            name="stripe",
            sitemap_url="https://docs.stripe.com/sitemap.xml", # Placeholder
            state_db_path=os.path.join(state_dir, "stripe_state.db"),
            pinecone_namespace="stripe_docs"
        )
    }
    
    if source_name not in configs:
        raise ValueError(f"Unknown source: {source_name}")
        
    return configs[source_name]