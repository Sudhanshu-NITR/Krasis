from queue import Queue
import time

class IngestionQueue:
    def __init__(self):
        self._queue = Queue()

    def add(self, items):
        if not items:
            return 
        
        for item in items:
            self._queue.put(item)
        print(f"[*] Added {len(items)} items to queue.")

    def process(self):
        if self._queue.empty():
            print("[*] Queue Empty.")

        print("\n--- STARTING BATCH ---")
        while not self._queue():
            url = self._queue.get()

            # TODO: Call src.ingestion.loaders.process_url(urk) here
            print(f"    Processing: {url}")
            time.sleep(0.1) 
            
            self._queue.task_done()
        print("--- BATCH COMPLETE ---\n")