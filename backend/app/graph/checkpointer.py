from langgraph.checkpoint.postgres import PostgresSaver
from app.config.settings import DATABASE_URL


def get_checkpointer():
    checkpointer = PostgresSaver.from_conn_string(
        DATABASE_URL
    )

    return checkpointer