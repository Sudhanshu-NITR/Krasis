from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import uvicorn
from src.core.chat import assistant
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Krasis Intelligen Docs API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

@app.get("/health")
async def health_check():
    return {"status": "online", "model": "gemini-2.5-flash"}

@app.post("/ask")
async def ask_docs(request: ChatRequest):
    """
    Standard endpoint that returns the full response at once.
    """
    print(request.query)
    result = assistant.ask(request.query)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result
    
@app.post("/ask/stream")
async def ask_docs_stream(request: ChatRequest):
    """
    Streaming endpoint for a real-time UI experience.
    """
    async def generate():
        try:
            for chunk in assistant.chain.stream(request.query):
                # We yield the chunk as a server-sent event (SSE)
                yield f"data: {json.dumps({'token': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)