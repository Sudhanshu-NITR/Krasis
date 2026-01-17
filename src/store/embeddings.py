from typing import List
import google.generativeai as genai
from config.settings import GEMINI_API_KEY, GEMINI_EMBED_MODEL

genai.configure(api_key=GEMINI_API_KEY)

class GeminiEmbeddingClient:
    """
    Gemini Embeddings for dense semantic vectors
    """

    def __init__(self, model: str = GEMINI_EMBED_MODEL):
        self,model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            resp = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document",  # optimized for retrieval
            )
            embeddings.append(resp["embedding"])
        return embeddings