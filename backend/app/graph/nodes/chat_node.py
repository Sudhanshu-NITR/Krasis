from ..state import ChatState
from app.llms.google_genai import get_google_genai_llm

def chat_node(state: ChatState, llm, tools=None):
    # Take user query from state
    messages = state['messages']

    # Bind tools to the LLM if any are provided
    if tools:
        llm_with_tools = llm.bind_tools(tools)

    # send to llm
    response = llm_with_tools.invoke(messages)

    # response store state
    return {'messages': [response]}