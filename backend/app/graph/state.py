from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class ChatState(TypedDict):
    """
    ChatState of the Chatbot
    """
    messages: Annotated[list[BaseMessage], add_messages]