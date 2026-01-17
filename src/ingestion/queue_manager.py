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
        if self._queue.empty():
            print("[*] Queue empty.")
            return

        print("\n--- STARTING BATCH ---")
        while not self._queue.empty():
            url = self._queue.get()

            print(f"    Processing: {url}")

            raw = self.loader.load(url)
            if not raw:
                self._queue.task_done()
                continue

            docs = self.splitter.split(
                raw["content"],
                source_url=raw["source_url"],
                doc_id=raw["doc_id"],
            )

            print(f"    → Generated {len(docs)} chunks")

            # TODO: persist docs to vector store here

            self._queue.task_done()

        print("--- BATCH COMPLETE ---\n")