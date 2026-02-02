import time
from src.ingestion.sqlite_queue import SQLiteQueue
from src.ingestion.pipeline import process_url  # reuse existing processing code
from src.ingestion.sitemap_state import SitemapState
from config.settings import STATE_DB_PATH

QUEUE_POLL_SECONDS = 2  # base polling interval
RATE_LIMIT_SECONDS = 1  # naive per-embed delay; make configurable

def run_worker():
    print("[worker] starting...")
    queue = SQLiteQueue(db_path=STATE_DB_PATH, table="ingestion_queue")
    state = SitemapState(db_path=STATE_DB_PATH, table="langchain_sitemap_urls")
    
    while True:
        item = queue.dequeue()
        if not item:
            time.sleep(QUEUE_POLL_SECONDS)
            continue

        item_id = item["id"]
        url = item["url"]
        print(f"[worker] processing {url} (id={item_id})")

        try:
            process_url(url)  # this upserts into vector store
            queue.ack_success(item_id)
            state.mark_ingested(url)
            # TODO: apply rate limit / quota accounting here
            time.sleep(RATE_LIMIT_SECONDS)
        except Exception as e:
            err = str(e)
            print(f"[worker] error for {url}: {err}")
            
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                print(f"\n[worker] Hit rate limit/quota. Sleeping for 1 hour before next attempt...")
                # Requeue this item to the front so it's tried first after waking up
                queue.requeue_front(item_id)
                # Sleep for 1 hour
                time.sleep(3600)
            else:
                # For general errors use exponential backoff:
                queue.ack_failure(item_id, err)


if __name__ == "__main__":
    run_worker()
