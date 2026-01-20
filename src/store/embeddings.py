from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.settings import GOOGLE_API_KEY, GEMINI_EMBED_MODEL

class GeminiEmbeddingClient:
    """
    Gemini Embeddings for dense semantic vectors
    """

    def __init__(
        self,
        model: str = GEMINI_EMBED_MODEL,
        api_key: str = GOOGLE_API_KEY,
    ):
        """
        Args:
            model: embedding model name, e.g. "models/gemini-embedding-001"
            api_key: your Google API key for Gemini
        """
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=model,
            google_api_key=api_key,
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of document texts in batches.
        """

        return self.embeddings.embed_documents(
            texts,
            task_type="RETRIEVAL_DOCUMENT",
        )

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.
        """
        return self.embeddings.embed_query(
            text,
            task_type="RETRIEVAL_QUERY",
        )
    

if __name__ == "__main__":
    print("🔍 Testing GeminiEmbeddingClient...\n")

    client = GeminiEmbeddingClient()

    # ---- Test 1: embed_query ----
    query = "What is machine learning?"
    print("Embedding query:", query)

    try:
        query_embedding = client.embed_query(query)
        print("✅ Query embedding successful")
        print("Vector length:", len(query_embedding))
        print("First 10 values:", query_embedding[:10])
    except Exception as e:
        print("❌ Query embedding failed")
        raise e

    print("\n" + "-" * 50 + "\n")

    # ---- Test 2: embed_documents ----
    documents = [
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with many layers.",
        "Embeddings convert text into numerical vectors."
    ]

    print("Embedding documents:")
    for i, doc in enumerate(documents, 1):
        print(f"{i}. {doc}")

    try:
        doc_embeddings = client.embed_documents(documents)
        print("\n✅ Document embedding successful")
        print("Number of embeddings:", len(doc_embeddings))
        print("Vector length (doc 1):", len(doc_embeddings[0]))
        print("First 10 values (doc 1):", doc_embeddings[0][:10])
    except Exception as e:
        print("❌ Document embedding failed")
        raise e

    print("\n🎉 All embedding tests passed successfully!")