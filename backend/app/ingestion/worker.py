from datetime import datetime
import time
import argparse
from app.ingestion.queues.queue_factory import get_queue, get_state_store
from app.ingestion.pipeline import process_url
from app.config.settings import get_config, PINECONE_INDEX_NAME

# Loaders
from app.ingestion.loader import MarkdownLoader
from app.ingestion.splitter import MarkdownDocsSplitter
from app.retrieval.vector_store import PineconeVectorStore

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
    loader = MarkdownLoader()
    
    splitter = MarkdownDocsSplitter(doc_site=source_name)
    
    store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        namespace=cfg.pinecone_namespace
    )

    # 2. Instantiate Queue (Factory handles Postgres vs SQLite)
    queue = get_queue()
    
    # 3. Instantiate State Store (Factory handles Postgres vs SQLite)
    state = get_state_store(source_name)


    while True:
        item = queue.dequeue()
        if not item:
            time.sleep(QUEUE_POLL_SECONDS)
            continue

        item_id = item["id"]
        url = item["url"]
        print(f"[worker] processing {url} (id={item_id})")

        try:
            # Check if Pinecone already has this URL up-to-date
            # This handles the case where local/postgres state is wiped but Pinecone is still full
            last_ingested_ts = store.get_document_last_ingested(url)
            sitemap_lastmod = item.get("lastmod")

            skip_processing = False
            
            if last_ingested_ts and sitemap_lastmod and sitemap_lastmod != "N/A":
                try:
                    # Parse sitemap timestamp
                    sitemap_ts = datetime.fromisoformat(sitemap_lastmod.replace("Z", "")).timestamp()
                    
                    # If ingested AFTER the last modification of the proper page
                    if last_ingested_ts >= sitemap_ts:
                        print(f"  -> Skipping (already in Vector Store): {url}")
                        skip_processing = True
                except Exception:
                    pass
            
            if not skip_processing:
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
