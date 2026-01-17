from queue import Queue
import time

class IngestionQueue:
    """
    A simple FIFO queue for managing ingestion tasks.

    This class abstracts queue behavior so the rest of the application
    does not depend on a specific queue implementation.
    """

    def __init__(self):
        """
        Initialize the ingestion queue.
        """
        self._queue = Queue()

    def add(self, items):
        """
        Add one or more items to the ingestion queue
        """
        if not items:
            return 
        
        for item in items:
            self._queue.put(item)
        print(f"[*] Added {len(items)} items to queue.")

    def process(self):
        """
        Process all items currently in the queue.
        """
        if self._queue.empty():
            print("[*] Queue Empty.")

        print("\n--- STARTING BATCH ---")
        while not self._queue.empty():
            url = self._queue.get()

            # TODO: Call src.ingestion.loaders.process_url(urk) here
            print(f"    Processing: {url}")
            time.sleep(0.1) 
            
            self._queue.task_done()
        print("--- BATCH COMPLETE ---\n")