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
        for i, (doc, dense, sparse) in enumerate(zip(docs, dense_vecs, sparse_vecs)):
            upsert_batch.append({
                "id": f"{doc.metadata['doc_id']}::chunk_{i}",
                "values": dense,
                "sparse_values": sparse,
                "metadata": doc.metadata,
            })

        # Upsert into Pinecone
        self.hybrid_store.upsert(upsert_batch)

        print(f"[VectorStore] Upserted {len(upsert_batch)} hybrid vectors.")

    def delete_by_source_url(self, source_url: str):
        """
        Delete all vectors belonging to a specific source URL.
        """
        self.hybrid_store.index.delete(
            filter={
                "source_url": {"$eq": source_url}
            }
        )
        print(f"[VectorStore] Deleted vectors for source_url={source_url}")