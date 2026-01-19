from src.ingestion.loader import MarkdownLoader
from src.ingestion.splitter import MarkdownDocsSplitter
from src.store.vector_store import VectorStore

loader = MarkdownLoader()
splitter = MarkdownDocsSplitter()
store = VectorStore()

def process_url(url: str):
    raw = loader.load(url)
    if not raw:
        return 
    
    store.delete_by_source_url(url)
    
    docs = splitter.split(
        raw["content"],
        source_url=raw["source_url"],
        doc_id=raw["doc_id"]
    )

    store.upsert(docs)