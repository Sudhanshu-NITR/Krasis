from typing import List
from langchain_classic.schema import Document

from src.store.embeddings import GeminiEmbeddingClient
from src.store.sparse_encoder import PineconeBM25Encoder
from src.store.pinecone_store import PineconeHybridStore

class VectorStore:
    """
    Pinecone hybrid vector store (dense + sparse).
    """

    def __init__(self):
        self.embedder = GeminiEmbeddingClient()
        self.sparse_encoder = PineconeBM25Encoder()
        self.hybrid_store = PineconeHybridStore()

    def upsert(self, docs: List[Document]):
        # Extract texts + IDs
        texts = [doc.page_content for doc in docs] 
        doc_ids = [doc.metadata["doc_id"] for doc in docs]

        # Fit sparse BM25 stats
        self.sparse_encoder.fit(texts)

        # Compute embeddings
        dense_vecs = self.embedder.embed_documents(texts)
        sparse_vecs = self.sparse_encoder.encode_documents(texts)

        # Prepare upsert payload
        upsert_batch = []
        for doc, dense, sparse in zip(docs, dense_vecs, sparse_vecs):
            upsert_batch.append({
                "id": doc.metadata["doc_id"],
                "values": dense,
                "sparse_values": sparse,
                "metadata": doc.metadata,
            })

        # Upsert into Pinecone
        self.hybrid_store.upsert(upsert_batch)

        print(f"[VectorStore] Upserted {len(upsert_batch)} hybrid vectors.")