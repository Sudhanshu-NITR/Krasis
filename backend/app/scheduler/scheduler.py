import os
import schedule
import time
from config.settings import get_config, CHECK_INTERVAL_HOURS
from src.ingestion.monitor import SitemapMonitor
from src.ingestion.sqlite_queue import SQLiteQueue

SOURCES = ["langchain", "stripe"]

def run_ingestion_cycle():
    print(f"[*] Starting ingestion cycle for sources: {SOURCES}")
    
    for source in SOURCES:
        try:
            cfg = get_config(source)
            print(f"[*] Processing source: {source} (Sitemap: {cfg.sitemap_url})")
            
            monitor = SitemapMonitor(
                sitemap_url=cfg.sitemap_url,
                db_path=cfg.state_db_path,
                source=source
            )

            # 1. Check for changes (this populates the queue)
            monitor.fetch_and_diff()
            print(f"[*] Completed for {source}.")
            
        except Exception as e:
            print(f"[!] Error processing {source}: {e}")

    print("[*] Ingestion cycle complete.")

def start_scheduler():
    if os.getenv("ENV", "DEV") == "DEV":
        print("[*] Running initial ingestion cycle for development...")
        run_ingestion_cycle()

    # Schedule
    schedule.every(CHECK_INTERVAL_HOURS).hours.do(run_ingestion_cycle)

    print(f"[*] Scheduler active. Running every {CHECK_INTERVAL_HOURS} hours.")
    while True:
        schedule.run_pending()
        time.sleep(1)