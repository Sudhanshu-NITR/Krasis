from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.settings import GOOGLE_API_KEY, GEMINI_EMBED_MODEL

class GeminiEmbeddingClient:
    """
    Gemini Embeddings for dense semantic vectors
    """

    def __init__(
        self,
        model: str = GEMINI_EMBED_MODEL,
        api_key: str = GOOGLE_API_KEY,
    ):
        """
        Args:
            model: embedding model name, e.g. "models/gemini-embedding-001"
            api_key: your Google API key for Gemini
        """
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=model,
            google_api_key=api_key,
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of document texts in batches.
        """

        return self.embeddings.embed_documents(
            texts,
            task_type="RETRIEVAL_DOCUMENT",
        )

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.
        """
        return self.embeddings.embed_query(
            text,
            task_type="RETRIEVAL_QUERY",
        )