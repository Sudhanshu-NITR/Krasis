from typing import List, Optional, Dict
import os
import time

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_core.documents import Document
from src.store.embeddings import GeminiEmbeddingClient
from langchain_community.retrievers import PineconeHybridSearchRetriever
from pinecone_text.sparse import BM25Encoder

from config.settings import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME as DEFAULT_INDEX_NAME, # Rename for clarity
    EMBEDDING_DIM,
    PINECONE_NAMESPACE as DEFAULT_NAMESPACE, # Rename for clarity
)

# Global singleton for BM25 Encoder to save memory on 512MB instances
_SHARED_BM25_ENCODER = None

def get_shared_bm25_encoder():
    global _SHARED_BM25_ENCODER
    if _SHARED_BM25_ENCODER is None:
        # Cache BM25 encoder to avoid re-downloading default corpus on every restart
        bm25_file = "data/bm25_values.json"
        # Ensure data directory exists
        os.makedirs(os.path.dirname(bm25_file), exist_ok=True)
        
        encoder = BM25Encoder()
        if os.path.exists(bm25_file):
            print(f"[*] Loading BM25 encoder from {bm25_file}...")
            encoder.load(bm25_file)
        else:
            print("[*] Downloading default BM25 encoder (this may take a while)...")
            encoder = encoder.default()
            encoder.dump(bm25_file)
            print(f"[*] BM25 encoder saved to {bm25_file}")
        
        _SHARED_BM25_ENCODER = encoder
    return _SHARED_BM25_ENCODER

class PineconeVectorStore:
    """
    Unified Pinecone store:
    - owns the index
    - handles ingestion (delete + upsert)
    - exposes LangChain hybrid retriever
    """

    def __init__(self, index_name: str = DEFAULT_INDEX_NAME, namespace: str = DEFAULT_NAMESPACE):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = index_name
        self.namespace = namespace

        # Only check/create index if we suspect it's needed (or catch errors during ops)
        # Checking list_indexes() on every init adds startup latency
        # But for robustness we'll keep it for now, unless it times out.
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=EMBEDDING_DIM,
                metric="dotproduct",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                ),
            )

        self.index = self.pc.Index(name=self.index_name)
        self.embeddings = GeminiEmbeddingClient()
        
        # Lazy load BM25 only when creating retriever or upserting
        self._bm25_encoder = None

    @property
    def bm25_encoder(self):
        if self._bm25_encoder is None:
            self._bm25_encoder = get_shared_bm25_encoder()
        return self._bm25_encoder

    def delete_by_source_url(self, source_url: str):
        try:
            self.index.delete(
                filter={"source_url": {"$eq": source_url}},
                namespace=self.namespace,
            )
        except Exception as e:
            # First-time namespace creation case → safe to ignore
            if "Namespace not found" not in str(e):
                raise

    def get_document_last_ingested(self, source_url: str) -> Optional[float]:
        """
        Check if a document exists by fetching 1 vector with the source_url filter.
        Returns the 'last_ingested_at' timestamp from metadata if found, else None.
        """
        try:
            # We generate a dummy vector of 0s to query because Pinecone doesn't support metadata-only queries efficiently
            # without a vector. However, a better way for just checking existence is `query` with top_k=1
            # and a filter.
            
            dummy_vector = [0.0] * EMBEDDING_DIM
            
            result = self.index.query(
                vector=dummy_vector,
                top_k=1,
                filter={"source_url": {"$eq": source_url}},
                namespace=self.namespace,
                include_metadata=True
            )
            
            if result.matches:
                metadata = result.matches[0].metadata
                # Check for ingested timestamp in metadata (we need to ensure we save this during upsert!)
                return metadata.get("ingested_at")
            
            return None
            
        except Exception:
            # If namespace doesn't exist or other error, assume not ingested
            return None

    def upsert_documents(self, docs: List[Document]):
        texts = [doc.page_content for doc in docs]
        
        dense_vectors = self.embeddings.embed_documents(texts)
        # Use property to lazy load shared encoder
        sparse_vectors = self.bm25_encoder.encode_documents(texts)

        # Add ingestion timestamp to all docs
        now_ts = time.time()
        
        vectors = []
        for i, (doc, dense, sparse) in enumerate(zip(docs, dense_vectors, sparse_vectors)):
            metadata = doc.metadata.copy()
            metadata["context"] = doc.page_content
            metadata["ingested_at"] = now_ts # Save timestamp for future checks!
            
            vectors.append({
                "id": f"{doc.metadata.get('doc_id', 'unknown')}::chunk_{i}",
                "values": dense,
                "sparse_values": sparse, 
                "metadata": metadata,
            })

        self.index.upsert(vectors=vectors, namespace=self.namespace)

    def get_hybrid_retriever(self, top_k: int = 5) -> PineconeHybridSearchRetriever:
        return PineconeHybridSearchRetriever(
            embeddings=self.embeddings.embeddings,
            sparse_encoder=self.bm25_encoder, # Triggers lazy load property
            index=self.index,
            namespace=self.namespace,
            top_k=top_k,
        )
