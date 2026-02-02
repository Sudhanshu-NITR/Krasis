import time
import argparse
from src.ingestion.sqlite_queue import SQLiteQueue
from src.ingestion.pipeline import process_url
from src.ingestion.sitemap_state import SitemapState
from config.settings import get_config, PINECONE_INDEX_NAME

# Loaders
from src.ingestion.loader import MarkdownLoader
from src.ingestion.splitter import MarkdownDocsSplitter
from src.store.vector_store import PineconeVectorStore

QUEUE_POLL_SECONDS = 2
RATE_LIMIT_SECONDS = 5  # increased to avoid hitting Gemini Free Tier (100 RPM) 

def run_worker(source_name: str = "langchain"):
    print(f"[worker] starting for source: {source_name}...")
    
    try:
        cfg = get_config(source_name)
    except ValueError as e:
        print(f"[worker] Error loading config: {e}")
        return

    # 1. Instantiate Dependencies
    # Use generic MarkdownLoader for both LangChain and Stripe
    loader = MarkdownLoader()
    
    splitter = MarkdownDocsSplitter()
    
    store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        namespace=cfg.pinecone_namespace
    )

    # 2. Instantiate State Managers with source-specific DB
    queue = SQLiteQueue(db_path=cfg.state_db_path, table="ingestion_queue")
    state = SitemapState(db_path=cfg.state_db_path, table="sitemap_urls")

    while True:
        item = queue.dequeue()
        if not item:
            time.sleep(QUEUE_POLL_SECONDS)
            continue

        item_id = item["id"]
        url = item["url"]
        print(f"[worker] processing {url} (id={item_id})")

        try:
            # Pass dependencies to pipeline
            process_url(url, loader, splitter, store)
            
            queue.ack_success(item_id)
            state.mark_ingested(url)
            # TODO: apply rate limit / quota accounting here
            time.sleep(RATE_LIMIT_SECONDS)
        except Exception as e:
            err = str(e)
            print(f"[worker] error for {url}: {err}")
            
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                print(f"\n[worker] Hit rate limit/quota. Sleeping for 1 hour before next attempt...")
                queue.requeue_front(item_id)
                time.sleep(3600)
            else:
                queue.ack_failure(item_id, err)


if __name__ == "__main__":
    # Allow running manually with a specific source
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="langchain", help="Source name (e.g., langchain, stripe)")
    args = parser.parse_args()
    
    run_worker(args.source)
