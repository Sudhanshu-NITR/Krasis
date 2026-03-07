import os
import time
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, Any

class PostgresQueue:
    def __init__(self, db_url: str, table: str = "ingestion_queue"):
        self.db_url = db_url
        self.table = table
        self._init_table()

    def _get_conn(self, max_retries=5):
        for attempt in range(max_retries):
            try:
                conn = psycopg2.connect(self.db_url)
                conn.autocommit = False # We manage transactions manually
                return conn
            except psycopg2.OperationalError:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)

    def _init_table(self):
        """
        Initialize the table if it doesn't exist.
        Notes:
        - Uses SERIAL for auto-increment ID
        - Uses JSONB for metadata (more efficient querying if needed later)
        - timestamptz is better practice, but we'll stick to REAL/DOUBLE for compatibility with existing logic if possible, 
          OR better yet, use standard Postgres timestamps and cast. 
          Actually, sticking to REAL (epoch) is easiest to match the SQLite logic 1:1 without refactoring the worker.
        """
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL UNIQUE,
            doc_id TEXT,
            lastmod TEXT,
            metadata_json JSONB,
            status TEXT NOT NULL DEFAULT 'pending',
            priority INTEGER NOT NULL DEFAULT 0,
            attempts INTEGER NOT NULL DEFAULT 0,
            last_error TEXT,
            next_try_at DOUBLE PRECISION DEFAULT 0,
            created_at DOUBLE PRECISION NOT NULL,
            processing_started_at DOUBLE PRECISION
        );
        CREATE INDEX IF NOT EXISTS idx_{self.table}_status_next_try ON {self.table}(status, next_try_at);
        """
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(create_sql)
            conn.commit()

    def enqueue_or_update(self, url: str, lastmod: Optional[str] = None, doc_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, priority: int = 0):
        now = time.time()
        meta_json = json.dumps(metadata or {})
        
        sql = f"""
        INSERT INTO {self.table} (url, doc_id, lastmod, metadata_json, priority, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT(url) DO UPDATE SET
            lastmod = EXCLUDED.lastmod,
            metadata_json = EXCLUDED.metadata_json,
            priority = GREATEST({self.table}.priority, EXCLUDED.priority),
            status = CASE 
                WHEN {self.table}.status IN ('failed', 'succeeded') THEN 'pending' -- Retry failed/succeeded items if re-queued
                ELSE {self.table}.status 
            END,
            attempts = CASE
                WHEN {self.table}.status IN ('failed', 'succeeded') THEN 0
                ELSE {self.table}.attempts
            END,
            next_try_at = CASE 
                WHEN {self.table}.status IN ('failed', 'succeeded') THEN 0 
                ELSE {self.table}.next_try_at 
            END
        """
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (url, doc_id, lastmod, meta_json, priority, now))
            conn.commit()

    def dequeue(self) -> Optional[Dict]:
        """
        Atomically selects a pending item and marks it as processing using FOR UPDATE SKIP LOCKED.
        This is the gold standard for Postgres queues.
        """
        now = time.time()
        sql = f"""
        UPDATE {self.table}
        SET status = 'processing', processing_started_at = %s
        WHERE id = (
            SELECT id
            FROM {self.table}
            WHERE status = 'pending' AND next_try_at <= %s
            ORDER BY priority DESC, created_at ASC
            FOR UPDATE SKIP LOCKED
            LIMIT 1
        )
        RETURNING id, url, doc_id, lastmod, metadata_json, status, priority, attempts, last_error, next_try_at, created_at, processing_started_at;
        """
        
        conn = self._get_conn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, (now, now))
                row = cur.fetchone()
            conn.commit()
            
            if row:
                # Convert RealDictRow to dict and handle JSONB automatically
                return dict(row)
            return None
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def ack_success(self, id: int):
        sql = f"UPDATE {self.table} SET status='succeeded', processing_started_at=NULL WHERE id = %s"
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (id,))
            conn.commit()

    def ack_failure(self, id: int, error: str, backoff_seconds: Optional[int] = None):
        now = time.time()
        # We need to fetch attempts first to calculate backoff if not provided
        # Or we can do it all in one query if we want to be fancy, but let's be explicit
        
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                if backoff_seconds is None:
                    cur.execute(f"SELECT attempts FROM {self.table} WHERE id = %s", (id,))
                    row = cur.fetchone()
                    attempts = (row[0] if row else 0) + 1
                    backoff_seconds = min(60 * (2 ** attempts), 60 * 60 * 6)
                else:
                    # Increment attempts anyway
                    cur.execute(f"SELECT attempts FROM {self.table} WHERE id = %s", (id,))
                    row = cur.fetchone()
                    attempts = (row[0] if row else 0) + 1
                
                next_try_at = now + backoff_seconds
                
                cur.execute(
                    f"UPDATE {self.table} SET status='pending', attempts=%s, last_error=%s, next_try_at=%s, processing_started_at=NULL WHERE id = %s",
                    (attempts, error, next_try_at, id)
                )
            conn.commit()
        finally:
            conn.close()

    def requeue_front(self, id: int):
        now = time.time()
        sql = f"""
        UPDATE {self.table} 
        SET status='pending', priority = priority + 10, attempts=0, processing_started_at=NULL, next_try_at = %s 
        WHERE id = %s
        """
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (now, id))
            conn.commit()

    def count_pending(self) -> int:
        now = time.time()
        sql = f"SELECT COUNT(*) FROM {self.table} WHERE status = 'pending' AND next_try_at <= %s"
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (now,))
                return cur.fetchone()[0]

    def get_stats(self) -> Dict[str, int]:
        sql = f"SELECT status, COUNT(*) FROM {self.table} GROUP BY status"
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
        return {row[0]: row[1] for row in rows}
