import requests
import time
import hashlib
from typing import Dict, Optional


HEADERS = {
    "User-Agent": "doc-assistant-bot/0.1 (+https://github.com/Sudhanshu-NITR/Krasis)"
}
TIMEOUT = 10

class MarkdownLoader:
    """
    Fetches markdown documentation.
    Designed for sites that serve raw markdown via .md extension (e.g. LangChain, Stripe).
    """

    def load(self, url: str) -> Optional[Dict]:
        md_url = self._to_markdown_url(url)

        try:
            resp = requests.get(md_url, headers=HEADERS, timeout=TIMEOUT)
            resp.raise_for_status()
        except Exception as e:
            print(f"[MarkdownLoader] Failed to fetch {md_url}: {e}")
            return None

        raw_md = resp.text
        content = self.strip_after_footer(raw_md)

        return {
            "doc_id": self._stable_id(md_url),
            "source_url": url,
            "resolved_url": md_url,
            "content": content,
            "content_length": len(content),
            "source_type": "markdown",
            "fetched_at": time.time(),
        }

    @staticmethod
    def _to_markdown_url(url: str) -> str:
        # Assumes /foo/bar -> /foo/bar.md strategy works for both
        return url.rstrip("/") + ".md"

    @staticmethod
    def _stable_id(url: str) -> str:
        return hashlib.sha256(url.encode()).hexdigest()
    
    @staticmethod
    def strip_after_footer(md: str) -> str:
        """
        Removes footer content.
        Currently checks for LangChain's '***' divider. 
        TODO: Make this configurable per source if Stripe uses different unexpected footers.
        """
        if "***" in md:
            return md.split("***", 1)[0].strip()
        return md.strip()

if __name__ == "__main__": 
    loader = MarkdownLoader() 
    test_url = "https://docs.langchain.com/oss/python/integrations/document_loaders" 
    data = loader.load(test_url)
    if data:
        # print(f"\nSuccessfully loaded {len(data['content'])} chars from {data['source']}") 
        print(data['content'])  