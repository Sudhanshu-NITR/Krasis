from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from typing import List, Dict
from config.settings import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    EMBEDDING_DIM,
)

class PineconeHybridStore:
    """
    Single Pinecone index for hybrid storage (dense + sparse).
    """

    def __init__(self):
        pc = Pinecone(api_key=PINECONE_API_KEY)

        # Create if not exist — single hybrid index
        if PINECONE_INDEX_NAME not in pc.list_indexes().names():
            pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=EMBEDDING_DIM, # dimensionality of dense model
                metric="dotproduct", # sparse values supported only for dotproduct
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        self.index = pc.Index(PINECONE_INDEX_NAME)

    def upsert(self, vectors: List[Dict]):
        """
        Each vector dict must be:
            {
                "id": str,
                "values": dense_vector,
                "sparse_values": sparse_vector,
                "metadata": { ... }
            }
        """

        self.index.upsert(vectors=vectors)