from langchain_core.tools import tool
from functools import partial
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition    
from .nodes.chat_node import chat_node
from .tools.retrieval_tool import get_retrieval_tool
from .checkpointer import get_checkpointer
from .state import ChatState

def create_graph(retriever, llm):
    # Get the checkpointer
    checkpointer = get_checkpointer()

    # Create the specialized tool instance
    retrieval_tool = get_retrieval_tool(retriever)
    tools = [retrieval_tool]

    # Define the Graph
    graph = StateGraph(ChatState)

    # Add nodes
    # We pass the tools to the chat_node so the LLM is aware of them
    graph.add_node('chat_node', partial(chat_node, llm=llm, tools=tools))
    
    # Pre-built ToolNode to execute any tool calls returned by the LLM
    graph.add_node('tools', ToolNode(tools))
    
    # Set entry point
    graph.set_entry_point('chat_node')

    # Add edges
    # If the LLM returns a tool_call, route to 'tools', otherwise route to END
    graph.add_conditional_edges('chat_node', tools_condition)
    
    # After a tool executes, return the result back to the chat_node
    graph.add_edge('tools', 'chat_node')

    # Compile the graph
    chatbot = graph.compile(checkpointer=checkpointer)

    return chatbot