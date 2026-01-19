from typing import List, Dict, Optional

from src.store.embeddings import GeminiEmbeddingClient
from src.store.sparse_encoder import PineconeBM25Encoder
from src.store.pinecone_store import PineconeHybridStore

class HybridQueryEngine:
    """
    Executes hybrid search (dense + sparse) against a single Pinecone index.
    """
    
    def __init__(
        self,
        *,
        alpha: float = 0.5,
        top_k: int = 10,
    ):
        """
        alpha:
            1.0 -> dense only
            0.0 -> sparse only
        """

        self.alpha = alpha
        self.top_k = top_k

        self.embedder = GeminiEmbeddingClient()
        self.sparse_encoder = PineconeBM25Encoder()
        self.store = PineconeHybridStore()

    def search(
        self,
        query: str,
        *,
        namespace: Optional[str] = None,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Perform hybrid search.

        Returns:
            List of Pinecone matched with metadata and scores.
        """
        
        # Dense Embedding
        dense_vec = self.embedder.embed_documents([query])[0]

        # Sparse Embedding (BM25)
        sparse_vec = self.sparse_encoder.encode(query)

        # Hybrid Query
        response = self.store.index.query(
            vector=dense_vec,
            sparse_vector=sparse_vec,
            top_k=self.top_k,
            include_metadata=True,
            filter=filters,
            namespace=namespace,
            alpha=self.alpha,
        )

        return response["matches"]