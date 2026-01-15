import requests
import json
import os
import xml.etree.ElementTree as ET
from config.settings import STATE_FILE_PATH

class SitemapMonitor:
    def __init__(self, url):
        self.url = url
        self.state_file = STATE_FILE_PATH
        self._ensure_state_dir()
        self.previous_state = self._load_state()

    def _ensure_state_dir(self):
        dir_path = os.path.dirname(self.state_file)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)


    def _load_state(self):
        """Loads the last known state of urls and timestamps."""
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                return json.load(f)
        return {}
    
    def _save_state(self, current_state):
        """Persists the current state to disk."""
        with open(self.state_file, 'w') as f:
            json.dump(current_state, f ,indent=4)

    def fetch_and_diff(self):
        print(f"[*] Fetching sitemap from {self.url}...")

        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"[!] Error fetching Sitemap: {e}")
            return []

        root = ET.fromstring(response.content)

        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        current_state = {}
        updates_needed = []

        urls = root.findall("ns:url", ns)
        print(f"[*] Analyzing {len(urls)} URLs for updates...")

        for url in urls:
            loc = url.find("ns:loc", ns).text

            lastmod_tag = url.find("ns:lastmod", ns)
            lastmod = lastmod_tag.text if lastmod_tag is not None else "N/A"

            current_state[loc] = lastmod

            if loc not in self.previous_state:
                print(f"    [+] New URL found: {loc}")
                updates_needed.append(loc)
            elif self.previous_state[loc] != lastmod:
                print(f"    [~] Modified URL found: {loc}")
                updates_needed.append(loc)

        self._save_state(current_state)
        self.previous_state = current_state

        return updates_needed


loader = SitemapMonitor('https://docs.langchain.com/sitemap.xml')

loader.fetch_and_diff()