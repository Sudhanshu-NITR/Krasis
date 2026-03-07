import os
import threading
import logging
import uvicorn
from app.scheduler.scheduler import start_scheduler
from app.ingestion.worker import run_worker
from app.api.api import app

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def run_scheduler_thread():
    logger.info("Starting Scheduler...")
    try:
        start_scheduler()
    except Exception as e:
        logger.error(f"Scheduler failed: {e}")

def run_worker_thread():
    logger.info("Starting Background Worker...")
    try:
        run_worker()
    except Exception as e:
        logger.error(f"Worker failed: {e}")

if __name__ == "__main__":
    logger.info("Starting backend services...")

    scheduler_thread = threading.Thread(target=run_scheduler_thread, daemon=True)
    worker_thread = threading.Thread(target=run_worker_thread, daemon=True)

    scheduler_thread.start()
    worker_thread.start()

    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting API Server at http://0.0.0.0:{port}")
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")