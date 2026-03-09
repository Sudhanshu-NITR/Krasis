from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import json

from langchain_core.messages import HumanMessage, AIMessage
from app.services.chat_service import get_assistant

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    doc_mode: str = "langchain"
    chat_history: Optional[List[Dict[str, str]]] = []
    config: Optional[Dict[str, Any]] = None 


def format_history(chat_history: List[Dict[str, str]]):
    formatted_history = []
    for msg in chat_history:
        if msg.get("role") == "user":
            formatted_history.append(HumanMessage(content=msg.get("content", "")))
        elif msg.get("role") == "assistant" and msg.get("content"):
            formatted_history.append(AIMessage(content=msg.get("content", "")))

    return formatted_history


@router.post("/ask")
async def ask_docs(request: ChatRequest):
    """
    Standard endpoint that returns the full response at once.
    """
    assistant = get_assistant(request.doc_mode)

    config = request.config

    # Convert frontend dictionaries into LangChain objects
    formatted_history = format_history(request.chat_history)
    
    # Package into a dictionary payload
    payload = {
        "question": request.query,
        "chat_history": formatted_history
    }

    result = assistant.ask(payload, config)

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result


@router.post("/ask/stream")
async def ask_docs_stream(request: ChatRequest):
    """
    Streaming endpoint for a real-time UI experience.
    """
    assistant = get_assistant(request.doc_mode)

    config = request.config

    # Convert frontend dictionaries into LangChain objects
    formatted_history = format_history(request.chat_history)
    
    # Package the query and history into a dictionary payload
    payload = {
        "question": request.query,
        "chat_history": formatted_history
    }

    return StreamingResponse(assistant.ask_stream(payload, config=config), media_type="text/event-stream")