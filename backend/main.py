import threading
import uvicorn
from src.orchestration.scheduler import start_scheduler
from src.ingestion.worker import run_worker
from api.api import app

def run_api():
    print("[*] Starting API Server at http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

def run_scheduler_thread():
    print("[*] Starting Scheduler...")
    start_scheduler()

def run_worker_thread():
    print("[*] Starting Background Worker...")
    run_worker()

if __name__ == "__main__":
    # Create threads for all services (API, Scheduler, Worker)
    api_thread = threading.Thread(target=run_api, daemon=True)
    scheduler_thread = threading.Thread(target=run_scheduler_thread, daemon=True)
    worker_thread = threading.Thread(target=run_worker_thread, daemon=True)

    api_thread.start()
    scheduler_thread.start()
    worker_thread.start()

    # Keep main thread alive
    try:
        api_thread.join()
        scheduler_thread.join()
        worker_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down...")