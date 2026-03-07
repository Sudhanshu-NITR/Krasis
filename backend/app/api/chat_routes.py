from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

from src.core.chat import get_assistant

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    doc_mode: str = "langchain"


@router.post("/ask")
async def ask_docs(request: ChatRequest):
    """
    Standard endpoint that returns the full response at once.
    """
    assistant = get_assistant(request.doc_mode)

    result = assistant.ask(request.query)

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

            for chunk in assistant.chain.stream(request.query):
                yield f"data: {json.dumps({'token': chunk})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")