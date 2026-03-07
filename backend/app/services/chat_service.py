from app.llms.google_genai import get_google_genai_llm
from app.retrieval.vector_store import PineconeVectorStore
from app.chain.rag_chain import create_rag_chain

class DocAssistant:
    def __init__(self, namespace="langchain_docs"):
        print(f"Initializing DocAssistant for namespace: {namespace}...")
        self.llm = get_google_genai_llm()

        self.vector_store = PineconeVectorStore(namespace=namespace)
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
        
# Global singleton instance cache mapping source_name to an assistant
_assistant_instances = {}

def get_assistant(source_name="langchain"):
    """
    Lazy load the DocAssistant singleton dictionary via config mapping.
    """
    global _assistant_instances
    if source_name not in _assistant_instances:
        from app.config.settings import get_config
        cfg = get_config(source_name)
        _assistant_instances[source_name] = DocAssistant(namespace=cfg.pinecone_namespace)
    return _assistant_instances[source_name]

# Removed global instantiation to save memory on import
# assistant = DocAssistant()