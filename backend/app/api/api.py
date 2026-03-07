from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.chat_routes import router as chat_router
from app.ingestion.queues.queue_factory import get_queue

app = FastAPI(title="Krasis Intelligent Docs API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)


@app.get("/")
async def root():
    """
    Root endpoint showing available routes.
    """
    routes = []

    for route in app.routes:
        if hasattr(route, "methods"):
            routes.append({
                "path": route.path,
                "methods": list(route.methods - {"HEAD", "OPTIONS"})
            })

    return {
        "name": "Krasis Intelligent Docs API",
        "status": "running",
        "docs": "/docs",
        "routes": routes
    }


@app.get("/health")
async def health_check():
    return {"status": "online", "model": "gemini-2.5-flash"}


@app.get("/queue/status")
async def get_queue_status():
    queue = get_queue()
    return queue.get_stats()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)