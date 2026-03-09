from langgraph.checkpoint.memory import InMemorySaver

def get_checkpointer():
    checkpointer = MemorySaver()

    return checkpointer
