from ..state import ChatState
from app.llms.google_genai import get_google_genai_llm

llm = get_google_genai_llm()

def chat_node(state: ChatState):
    # Take user query from state
    messages = state['messages']

    # send to llm
    response = llm.invoke(messages)

    # response store state
    return {'messages': [response]}