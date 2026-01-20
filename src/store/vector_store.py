from typing import List

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_classic.schema import Document
from src.store.embeddings import GeminiEmbeddingClient
from langchain_community.retrievers import PineconeHybridSearchRetriever
from pinecone_text.sparse import BM25Encoder

from config.settings import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    EMBEDDING_DIM,
    PINECONE_NAMESPACE, 
)

class PineconeVectorStore:
    """
    Unified Pinecone store:
    - owns the index
    - handles ingestion (delete + upsert)
    - exposes LangChain hybrid retriever
    """

    def __init__(self):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)

        if PINECONE_INDEX_NAME not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=EMBEDDING_DIM,
                metric="dotproduct",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                ),
            )

        self.index = self.pc.Index(name=PINECONE_INDEX_NAME)

        self.embeddings = GeminiEmbeddingClient()
        self.bm25_encoder = BM25Encoder().default()

    
    def delete_by_source_url(self, source_url: str):
        try:
            self.index.delete(
                filter={"source_url": {"$eq": source_url}},
                namespace=PINECONE_NAMESPACE,
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

        self.index.upsert(vectors=vectors, namespace=PINECONE_NAMESPACE)

    def get_hybrid_retriever(self, top_k: int = 5) -> PineconeHybridSearchRetriever:
        return PineconeHybridSearchRetriever(
            embeddings=self.embeddings.embeddings,
            sparse_encoder=self.bm25_encoder,
            index=self.index,
            namespace=PINECONE_NAMESPACE,
            top_k=top_k,
        )
