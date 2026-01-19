import time
from src.ingestion.sqlite_queue import SQLiteQueue
from src.ingestion.pipeline import process_url  # reuse existing processing code
from src.ingestion.sitemap_state import SitemapState
from config.settings import STATE_DB_PATH

QUEUE_POLL_SECONDS = 2  # base polling interval
RATE_LIMIT_SECONDS = 60  # naive per-embed delay; make configurable

queue = SQLiteQueue(db_path=STATE_DB_PATH, table="ingestion_queue")
state = SitemapState(db_path=STATE_DB_PATH, table="langchain_sitemap_urls")

def run_worker():
    print("[worker] starting...")
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
            # TODO: If it's a quota error you may want to requeue_front
            # For general errors use exponential backoff:
            queue.ack_failure(item_id, err)
