from src.llms.google_genai import get_google_genai_llm
from src.store.vector_store import PineconeVectorStore
from src.core.rag_chain import create_rag_chain

class DocAssistant:
    def __init__(self):
        self.llm = get_google_genai_llm()

        self.vector_store = PineconeVectorStore()
        self.retriever = self.vector_store.get_hybrid_retriever()

        self.chain = create_rag_chain(self.retriever, self.llm)

    def ask(self, query: str):
        """
        The main entry point for queries.
        """
        try:
            response = self.chain.invoke(query)
            return {
                "status": "success",
                "answer": response
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
        
assistant = DocAssistant()