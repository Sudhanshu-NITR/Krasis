import os
import sqlite3
import time
from typing import Optional

class SitemapState:
    """
    SQLite-backed state store for sitemap URLs.
    One table per documentation source (e.g. langchain_sitemap_urls).
    """

    def __init__(self, db_path: str, table: str):
        # print("db_path:", db_path, type(db_path))
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.table = table
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self.conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            url TEXT PRIMARY KEY,
            lastmod TEXT,
            last_seen_at REAL,
            last_ingested_at REAL,
            status TEXT
        )
        """)
        self.conn.commit()

    def get_lastmod(self, url: str) -> Optional[str]:
        cur = self.conn.execute(
            f"SELECT lastmod FROM {self.table} WHERE url = ?",
            (url,)
        )

        row = cur.fetchone()
        return row["lastmod"] if row else None
    
    def upsert(self, url: str, lastmod: str):
        now = time.time()

        self.conn.execute(f"""
            INSERT INTO {self.table} (
            url, lastmod, last_seen_at, status
            )
            VALUES (?, ?, ?, 'pending')
            ON CONFLICT(url) DO UPDATE SET
                lastmod = excluded.lastmod,
                last_seen_at = excluded.last_seen_at
        """, (url, lastmod, now))

        self.conn.commit()

    def mark_ingested(self, url: str):
        self.conn.execute(f"""
            UPDATE {self.table}
            SET last_ingested_at = ?, status = 'ingested'
            WHERE url = ?
        """, (time.time(), url))

        self.conn.commit()

    def mark_failed(self, url: str):
        self.conn.execute(f"""
            UPDATE {self.table}
            SET status = 'failed'
            WHERE url = ?
        """, (url,))

        self.conn.commit()

    def get_last_ingested_at(self, url: str):
        cur = self.conn.execute(
            f"SELECT last_ingested_at FROM {self.table} WHERE url = ?",
            (url,)
        )
        row = cur.fetchone()
        return row["last_ingested_at"] if row else None
