import schedule
import time
from config.settings import SITEMAP_URL, CHECK_INTERVAL_HOURS
from src.ingestion.monitor import SitemapMonitor
from src.ingestion.queue_manager import IngestionQueue

def run_ingestion_cycle():
    print(f"[*] Starting ingestion cycle...")
    monitor = SitemapMonitor(SITEMAP_URL)

    queue = IngestionQueue()

    # 1. Check for changes
    new_urls = monitor.fetch_and_diff()

    # 2. Process
    if new_urls:
        queue.add(new_urls)
        queue.process()
    else:
        print("[*] No changes found.")

def start_scheduler():
    # TODO: for development run once immidiately, change for production
    run_ingestion_cycle()

    # Schedule
    schedule.every(CHECK_INTERVAL_HOURS).hours.do(run_ingestion_cycle)

    print(f"[*] Scheduler active. Running every {CHECK_INTERVAL_HOURS} hours.")
    while True:
        schedule.run_pending()
        time.sleep(1)