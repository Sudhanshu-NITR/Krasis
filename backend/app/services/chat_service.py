import json
from app.llms.google_genai import get_google_genai_llm
from app.retrieval.vector_store import PineconeVectorStore
from app.chain.rag_chain import create_rag_chain
from app.graph.graph import create_graph
from langchain_core.messages import HumanMessage

class DocAssistant:
    """
    A service class that orchestrates the Retrieval-Augmented Generation (RAG) pipeline 
    using LangChain. It initializes the LLM, connects to the Pinecone vector store, 
    and sets up the necessary retrievers and chains for querying documents.
    """
    def __init__(self, namespace="langchain_docs"):
        print(f"Initializing DocAssistant for namespace: {namespace}...")
        self.llm = get_google_genai_llm()

        self.vector_store = PineconeVectorStore(namespace=namespace)
        self.retriever = self.vector_store.get_hybrid_retriever()

        self.chain = create_rag_chain(self.retriever, self.llm)

    def ask(self, payload: dict):
        """
        The main entry point for queries.
        """
        try:
            response = self.chain.invoke(payload)
            return {
                "status": "success",
                "answer": response
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def ask_stream(self, payload: dict):
        """
        A generator for streaming queries.
        """
        try:
            for chunk in self.chain.stream(payload):
                yield f"data: {json.dumps({'token': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"


class DocAssistant_v2:
    """
    A service class that orchestrates the Retrieval-Augmented Generation (RAG) pipeline 
    using LangChain. It initializes the LLM, connects to the Pinecone vector store, 
    and sets up the necessary retrievers and chains for querying documents.
    """
    def __init__(self, namespace="langchain_docs"):
        print(f"Initializing DocAssistant for namespace: {namespace}...")
        self.llm = get_google_genai_llm()

        self.vector_store = PineconeVectorStore(namespace=namespace)
        self.retriever = self.vector_store.get_hybrid_retriever()

        self.graph = create_graph(self.retriever, self.llm)

    def ask(self, payload: dict, config: dict = None):
        """
        The main entry point for queries.
        """
        try:
            response = self.graph.invoke({'messages': [HumanMessage(content=payload["question"])]}, config=config)
            return {
                "status": "success",
                "answer": response['messages'][-1].content
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def ask_stream(self, payload: dict, config: dict = None):
        """
        A generator for streaming queries.
        """
        try:
            for chunk, metadata in self.graph.stream({
                'messages': [HumanMessage(content=payload["question"])]}, 
                config=config,
                stream_mode='messages'
            ):
                yield f"data: {json.dumps({'token': chunk.content})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"



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
        _assistant_instances[source_name] = DocAssistant_v2(namespace=cfg.pinecone_namespace)
    return _assistant_instances[source_name]