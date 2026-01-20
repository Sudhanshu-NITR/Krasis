from typing import List

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_classic.schema import Document
from src.store.embeddings import GeminiEmbeddingClient
from langchain_community.retrievers import PineconeHybridSearchRetriever

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
        dense_vectors = self.embeddings.embed_documents(
            texts
        )

        print("Hi")

        vectors = []
        for i, (doc, dense) in enumerate(zip(docs, dense_vectors)):
            vectors.append({
                "id": f"{doc.metadata['doc_id']}::chunk_{i}",
                "values": dense,
                "metadata": doc.metadata,
            })

        self.index.upsert(vectors=vectors, namespace=PINECONE_NAMESPACE)


    def get_hybrid_retriever(self, top_k: int = 5) -> PineconeHybridSearchRetriever:
        return PineconeHybridSearchRetriever(
            index=self.index,
            sparse_encoder="bm25",
            embedding_function=self.embeddings.embeddings,
            namespace=PINECONE_NAMESPACE,
            top_k=top_k,
        )
