from typing import List

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
        
        # Cache BM25 encoder to avoid re-downloading default corpus on every restart
        import os
        bm25_file = "data/bm25_values.json"
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(bm25_file), exist_ok=True)

        self.bm25_encoder = BM25Encoder()
        if os.path.exists(bm25_file):
            print(f"[*] Loading BM25 encoder from {bm25_file}...")
            self.bm25_encoder.load(bm25_file)
        else:
            print("[*] Downloading default BM25 encoder (this may take a while)...")
            self.bm25_encoder = self.bm25_encoder.default()
            self.bm25_encoder.dump(bm25_file)
            print(f"[*] BM25 encoder saved to {bm25_file}")

    
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

    def upsert_documents(self, docs: List[Document]):
        texts = [doc.page_content for doc in docs]
        
        dense_vectors = self.embeddings.embed_documents(texts)
        sparse_vectors = self.bm25_encoder.encode_documents(texts)

        vectors = []
        for i, (doc, dense, sparse) in enumerate(zip(docs, dense_vectors, sparse_vectors)):
            metadata = doc.metadata.copy()
            metadata["context"] = doc.page_content
            
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
            sparse_encoder=self.bm25_encoder,
            index=self.index,
            namespace=self.namespace,
            top_k=top_k,
        )
