import psycopg2
from typing import Optional
import time

class PostgresState:
    """
    PostgreSQL-backed state store.
    """
    
    def __init__(self, db_url: str, table: str = "sitemap_urls"):
        self.db_url = db_url
        self.table = table
        self._init_db()

    def _get_conn(self):
        return psycopg2.connect(self.db_url)

    def _init_db(self):
        # Note: using DOUBLE PRECISION for timestamps to match SQLite implementation
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            url TEXT PRIMARY KEY,
            lastmod TEXT,
            last_seen_at DOUBLE PRECISION,
            last_ingested_at DOUBLE PRECISION,
            status TEXT
        );
        """
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(create_sql)
            conn.commit()

    def get_lastmod(self, url: str) -> Optional[str]:
        sql = f"SELECT lastmod FROM {self.table} WHERE url = %s"
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (url,))
                row = cur.fetchone()
        return row[0] if row else None

    def upsert(self, url: str, lastmod: str):
        now = time.time()
        sql = f"""
        INSERT INTO {self.table} (url, lastmod, last_seen_at, status)
        VALUES (%s, %s, %s, 'pending')
        ON CONFLICT (url) DO UPDATE SET
            lastmod = EXCLUDED.lastmod,
            last_seen_at = EXCLUDED.last_seen_at;
        """
        # Note: status is not updated on conflict to preserve 'ingested' unless explicitly reset?
        # The SQLite version does NOT update 'status' on conflict, so we match that behavior.
        # It only updates lastmod and last_seen_at.
        
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (url, lastmod, now))
            conn.commit()

    def mark_ingested(self, url: str):
        now = time.time()
        sql = f"UPDATE {self.table} SET last_ingested_at = %s, status = 'ingested' WHERE url = %s"
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (now, url))
            conn.commit()

    def mark_failed(self, url: str):
        sql = f"UPDATE {self.table} SET status = 'failed' WHERE url = %s"
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (url,))
            conn.commit()

    def get_last_ingested_at(self, url: str) -> Optional[float]:
        sql = f"SELECT last_ingested_at FROM {self.table} WHERE url = %s"
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (url,))
                row = cur.fetchone()
        return row[0] if row else None
