from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver 
from app.config.settings.config import DATABASE_URL

connection_pool = ConnectionPool(conninfo=DATABASE_URL, max_size=20)

def get_checkpointer():
    """
    Returns a PostgresSaver checkpointer using a connection pool.
    """
    checkpointer = PostgresSaver(connection_pool)

    # Automatically creates all necessary checkpoint tables if they don't exist
    checkpointer.setup()

    return checkpointer