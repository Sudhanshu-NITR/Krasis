import schedule
import time
from config.settings import SITEMAP_URL, CHECK_INTERVAL_HOURS
from src.ingestion.monitor import SitemapMonitor
from src.ingestion.sqlite_queue import SQLiteQueue

def run_ingestion_cycle():
    print(f"[*] Starting ingestion cycle...")
    monitor = SitemapMonitor(SITEMAP_URL)

    # 1. Check for changes (this populates the queue)
    monitor.fetch_and_diff()
    print("[*] Ingestion cycle complete. Tasks enqueued (if any).")

def start_scheduler():
    # TODO: for development run once immidiately, change for production
    run_ingestion_cycle()

    # Schedule
    schedule.every(CHECK_INTERVAL_HOURS).hours.do(run_ingestion_cycle)

    print(f"[*] Scheduler active. Running every {CHECK_INTERVAL_HOURS} hours.")
    while True:
        schedule.run_pending()
        time.sleep(1)