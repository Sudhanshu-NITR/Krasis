from app.graph.nodes.chat_node import chat_node
from langgraph.graph import StateGraph
from .checkpointer import get_checkpointer
from .state import ChatState

def create_graph():
    # Get the checkpointer
    checkpointer = get_checkpointer()

    # Define the Graph
    graph = StateGraph(ChatState)

    # Add nodes
    graph = add_node('chat_node', chat_node)
    
    # Set entry point
    graph.set_entry_point('chat_node')

    # Add edges
    graph.add_edge('chat_node', END)

    # Compile the graph
    chatbot = graph.compile(checkpointer=checkpointer)

    return chatbot