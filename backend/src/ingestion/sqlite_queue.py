import sqlite3
import time
import json
from typing import Optional, Dict, Any

DEFAULT_DB = "data/sitemap_state.db"

class SQLiteQueue:
    def __init__(self, db_path: str = DEFAULT_DB, table: str = "ingestion_queue"):
        import os
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.table = table
        self.conn = sqlite3.connect(self.db_path, timeout=30, isolation_level=None)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.row_factory = sqlite3.Row
        self._init_table()

    def _init_table(self):
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            doc_id TEXT,
            lastmod TEXT,
            metadata_json TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            priority INTEGER NOT NULL DEFAULT 0,
            attempts INTEGER NOT NULL DEFAULT 0,
            last_error TEXT,
            next_try_at REAL DEFAULT 0,
            created_at REAL NOT NULL,
            processing_started_at REAL
        );
        """
        self.conn.execute(create_sql)
        self.conn.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{self.table}_url ON {self.table}(url);")
        self.conn.commit()

    def enqueue_or_update(self, url: str, lastmod: Optional[str] = None, doc_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, priority: int = 0):
        now = time.time()
        meta_json  = json.dumps(metadata or {})
        # Upsert by URL: if exists, update lastmod/priority, otherwise insert.
        sql = f"""
        INSERT INTO {self.table} (url, doc_id, lastmod, metadata_json, priority, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            lastmod = excluded.lastmod,
            metadata_json = excluded.metadata_json,
            priority = MAX({self.table}.priority, excluded.priority)
        """
        self.conn.execute(sql, (url, doc_id, lastmod, meta_json, priority, now))
        self.conn.commit()


    def _atomic_select_and_mark_processing(self):
        """
        Atomically select a pending item ready to be processed and mark it as 'processing'.
        We use a BEGIN IMMEDIATE transaction to reduce race conditions.
        """

        cur = self.conn.cursor()

        try:
            cur.execute("BEGIN IMMEDIATE")
            now = time.time()
            row = cur.execute(
                f"""
                SELECT id FROM {self.table}
                WHERE status = 'pending' AND next_try_at <= ?
                ORDER BY priority DESC, created_at ASC
                LIMIT 1
                """,
                (now,)
            ).fetchone()

            if not row:
                cur.execute("COMMIT")
                return None
            
            item_id = row["id"]
            cur.execute(
                f"UPDATE {self.table} SET status='processing', processing_started_at=? WHERE id=? AND status='pending'",
                (now, item_id)
            )
            cur.execute("COMMIT")
            return item_id
        
        except Exception:
            cur.execute("ROLLBACK")
            raise

    def dequeue(self) -> Optional[Dict]:
        item_id = self._atomic_select_and_mark_processing()

        if not item_id:
            return None
        row = self.conn.execute(f"SELECT * FROM {self.table} WHERE id = ?", (item_id,)).fetchone()
        if not row:
            return None
        return dict(row)
    
    def ack_success(self, id: int):
        now = time.time()
        self.conn.execute(f"UPDATE {self.table} SET status='succeeded', processing_started_at=NULL WHERE id = ?", (id,))
        self.conn.commit()

    def ack_failure(self, id: int, error: str, backoff_seconds: Optional[int] = None):
        # increment attempts & set next_try_at based on backoff
        now = time.time()
        row = self.conn.execute(f"SELECT attempts FROM {self.table} WHERE id = ?", (id,)).fetchone()
        attempts = (row["attempts"] if row else 0) + 1
        if backoff_seconds is None:
            backoff_seconds = min(60 * (2 ** attempts), 60 * 60 * 6)  # exponential up to 6 hours
        next_try_at = now + backoff_seconds
        self.conn.execute(
            f"UPDATE {self.table} SET status='pending', attempts=?, last_error=?, next_try_at=?, processing_started_at=NULL WHERE id = ?",
            (attempts, error, next_try_at, id)
        )
        self.conn.commit()

    def requeue_front(self, id: int):
        # bump priority and set next_try_at to now
        now = time.time()
        self.conn.execute(f"UPDATE {self.table} SET priority = priority + 10, next_try_at = ? WHERE id = ?", (now, id))
        self.conn.commit()

    def count_pending(self) -> int:
        now = time.time()
        row = self.conn.execute(f"SELECT COUNT(1) as c FROM {self.table} WHERE status = 'pending' AND next_try_at <= ?", (now,)).fetchone()
        return row["c"]