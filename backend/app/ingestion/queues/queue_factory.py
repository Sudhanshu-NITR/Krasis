import os
from .sqlite_queue import SQLiteQueue
from .postgres_queue import PostgresQueue
from .sitemap_state import SitemapState
from .postgres_state import PostgresState

def get_queue():
    """
    Factory function to return the appropriate queue implementation.
    Checks for `DATABASE_URL` environment variable.
    """
    db_url = os.environ.get("DATABASE_URL")
    
    if db_url and db_url.startswith("postgres"):
        return PostgresQueue(db_url)
    
    # Fallback to SQLite
    return SQLiteQueue()

def get_state_store(source_name: str = "langchain"):
    """
    Factory function for SitemapState.
    """
    db_url = os.environ.get("DATABASE_URL")
    
    if db_url and db_url.startswith("postgres"):
        # For Postgres, we can share tables or use prefixes if needed.
        # Ideally, we put all sources in one table with a 'source' column,
        # but to keep migration simple and match existing 1:1 table structure:
        table_name = f"sitemap_urls_{source_name}"
        return PostgresState(db_url, table=table_name)

    # Fallback to SQLite (local file per source)
    db_path = f"data/state/{source_name}.db"
    return SitemapState(db_path, "sitemap_urls")
