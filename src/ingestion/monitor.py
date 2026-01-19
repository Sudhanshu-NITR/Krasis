import requests
import xml.etree.ElementTree as ET
from datetime import datetime

from config.settings import STATE_DB_PATH
from src.ingestion.sitemap_state import SitemapState
from src.ingestion.sqlite_queue import SQLiteQueue


class SitemapMonitor:
    """
    Monitors a sitemap and enqueues new or modified URLs
    into the persistent ingestion queue.
    """

    def __init__(self, sitemap_url: str):
        self.sitemap_url = sitemap_url

        self.state = SitemapState(
            db_path=STATE_DB_PATH,
            table="langchain_sitemap_urls"
        )

        self.queue = SQLiteQueue(
            db_path=STATE_DB_PATH,
            table="ingestion_queue"
        )

    def fetch_and_diff(self):
        print(f"[*] Fetching sitemap from {self.sitemap_url}...")

        try:
            response = requests.get(self.sitemap_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"[!] Error fetching sitemap: {e}")
            return

        root = ET.fromstring(response.content)
        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        urls = root.findall("ns:url", ns)
        print(f"[*] Analyzing {len(urls)} URLs for updates...")

        for url_node in urls:
            loc = url_node.find("ns:loc", ns).text

            lastmod_tag = url_node.find("ns:lastmod", ns)
            lastmod = lastmod_tag.text if lastmod_tag is not None else "N/A"

            previous_lastmod = self.state.get_lastmod(loc)

            last_ingested_at = self.state.get_last_ingested_at(loc)

            # If already ingested AFTER lastmod → skip
            if last_ingested_at and lastmod != "N/A":
                try:
                    lastmod_ts = datetime.fromisoformat(lastmod.replace("Z", "")).timestamp()
                    if last_ingested_at > lastmod_ts:
                        continue  # ignore this URL
                except Exception:
                    pass

            # NEW URL or UPDATED URL → enqueue
            if previous_lastmod is None:
                print(f"    [+] New URL: {loc}")
                self.queue.enqueue_or_update(
                    url=loc,
                    lastmod=lastmod,
                    priority=1
                )

            elif previous_lastmod != lastmod:
                print(f"    [~] Modified URL: {loc}")
                self.queue.enqueue_or_update(
                    url=loc,
                    lastmod=lastmod,
                    priority=2  # higher priority for updates
                )

            # Always update sitemap state
            self.state.upsert(loc, lastmod)


if __name__ == "__main__":
    loader = SitemapMonitor('https://docs.langchain.com/sitemap.xml')
    loader.fetch_and_diff()