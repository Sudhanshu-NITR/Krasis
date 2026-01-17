from pinecone_text.sparse import BM25Encoder
from typing import List

class PineconeBM25Encoder:
    """
    Uses Pinecone Text's BM25 encoder to produce sparse vectors.
    """

    def __init__(self):
        self.encoder = BM25Encoder()

    def fit(self, texts: List[str]):
        """
        Fit BM25 stats on the corpus.
        """
        self.encoder.fit(texts)

    def encode(self, text: str):
        return self.encoder.encode_documents([text])[0]
    
    def encode_documents(self, texts: List[str]):
        return self.encoder.encode_documents(texts)
    
    