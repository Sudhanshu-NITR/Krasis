from typing import List, Optional
import time

from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_core.documents import Document
from langchain_community.retrievers import PineconeHybridSearchRetriever

from app.retrieval.encoder import QuickSparseEncoder
from app.retrieval.embeddings import GeminiEmbeddingClient
from app.config.settings import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME as DEFAULT_INDEX_NAME,
    EMBEDDING_DIM,
)


class PineconeVectorStore:
    """
    Memory-efficient Hybrid Pinecone Store for Krasis:
    - Uses Gemini for Dense (semantic) embeddings.
    - Uses Pinecone Inference API for Sparse (keyword) embeddings (Zero RAM impact).
    - Supports incremental updates for LangChain/Stripe/Next.js docs.
    """

    def __init__(self, index_name: str = DEFAULT_INDEX_NAME, namespace: str = "langchain_docs"):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = index_name
        self.namespace = namespace

        # Ensure index exists with 'dotproduct' metric (required for hybrid)
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=EMBEDDING_DIM,
                metric="dotproduct", 
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        self.index = self.pc.Index(name=self.index_name)
        self.embeddings = GeminiEmbeddingClient()
        
        # Lightweight wrapper for the sparse API (no local model loaded)
        self.sparse_encoder = QuickSparseEncoder(self.pc)

    # ----------------------------
    # Incremental Logic Helpers
    # ----------------------------
    def delete_by_source_url(self, source_url: str):
        try:
            self.index.delete(
                filter={"source_url": {"$eq": source_url}},
                namespace=self.namespace,
            )
        except Exception as e:
            if "Namespace not found" not in str(e):
                raise

    def get_document_last_ingested(self, source_url: str) -> Optional[float]:
        try:
            # Query using a zero vector to find the latest timestamp for a URL
            dummy_vector = [0.0] * EMBEDDING_DIM
            result = self.index.query(
                vector=dummy_vector,
                top_k=1,
                filter={"source_url": {"$eq": source_url}},
                namespace=self.namespace,
                include_metadata=True
            )
            if result.matches:
                return result.matches[0].metadata.get("ingested_at")
            return None
        except Exception:
            return None

    # ----------------------------
    # Upsert Logic (Memory Efficient)
    # ----------------------------
    def upsert_documents(self, docs: List[Document]):
        if not docs:
            return

        texts = [doc.page_content for doc in docs]
        
        # 1. Get Dense Vectors (Gemini)
        dense_vectors = self.embeddings.embed_documents(texts)
        
        # 2. Get Sparse Vectors (Pinecone API - Zero local RAM usage)
        sparse_res = self.pc.inference.embed(
            model="pinecone-sparse-english-v0",
            inputs=texts,
            parameters={"input_type": "passage", "truncate": "END"}
        )

        now_ts = time.time()
        vectors = []

        for i, (doc, dense, sparse) in enumerate(zip(docs, dense_vectors, sparse_res)):
            metadata = doc.metadata.copy()
            metadata["text"] = doc.page_content  # Required for Retriever context
            metadata["ingested_at"] = now_ts

            vectors.append({
                "id": f"{doc.metadata.get('doc_id', 'unknown')}::chunk_{i}",
                "values": dense,
                "sparse_values": {"indices": sparse.sparse_indices, "values": sparse.sparse_values}, # Native hybrid support
                "metadata": metadata,
            })

        # Upsert in batches to Pinecone
        self.index.upsert(vectors=vectors, namespace=self.namespace)

    # ----------------------------
    # Hybrid Retriever
    # ----------------------------
    def get_hybrid_retriever(self, top_k: int = 5, alpha: float = 0.5):
        """
        Returns a retriever that combines semantic (Gemini) and keyword (Pinecone) search.
        alpha=1.0 is pure semantic, alpha=0.0 is pure keyword.
        """
        return PineconeHybridSearchRetriever(
            embeddings=self.embeddings.embeddings,
            sparse_encoder=self.sparse_encoder,
            index=self.index,
            namespace=self.namespace,
            text_key="text",
            top_k=top_k,
            alpha=alpha,
        )