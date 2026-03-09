from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import json

from langchain_core.messages import HumanMessage, AIMessage
from app.services.chat_service import get_assistant

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    doc_mode: str = "langchain"
    chat_history: Optional[List[Dict[str, str]]] = []

@router.post("/ask")
async def ask_docs(request: ChatRequest):
    """
    Standard endpoint that returns the full response at once.
    """
    assistant = get_assistant(request.doc_mode)

    # Convert frontend dictionaries into LangChain objects
    formatted_history = []
    for msg in request.chat_history:
        if msg.get("role") == "user":
            formatted_history.append(HumanMessage(content=msg.get("content", "")))
        elif msg.get("role") == "assistant" and msg.get("content"):
            formatted_history.append(AIMessage(content=msg.get("content", "")))
            
    # Package into a dictionary payload
    payload = {
        "question": request.query,
        "chat_history": formatted_history
    }

    result = assistant.ask(payload)

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result


@router.post("/ask/stream")
async def ask_docs_stream(request: ChatRequest):
    """
    Streaming endpoint for a real-time UI experience.
    """

    async def generate():
        try:
            assistant = get_assistant(request.doc_mode)

            # Convert frontend dictionaries into LangChain objects
            formatted_history = []
            for msg in request.chat_history:
                if msg.get("role") == "user":
                    formatted_history.append(HumanMessage(content=msg.get("content", "")))
                elif msg.get("role") == "assistant" and msg.get("content"):
                    formatted_history.append(AIMessage(content=msg.get("content", "")))

            # Package the query and history into a dictionary payload
            payload = {
                "question": request.query,
                "chat_history": formatted_history
            }

            # Stream using the payload
            for chunk in assistant.chain.stream(payload):
                yield f"data: {json.dumps({'token': chunk})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")