from langchain_core.tools import tool
from app.helpers.format_docs_helper import format_docs

def get_retrieval_tool(retriever):
    """
    Factory function to create a LangChain tool injected with the Pinecone retriever.
    The tool takes a search query and returns the relevant formatted documents.
    """
    @tool
    def search_documentation(query: str) -> str:
        """
        Use this tool to search the documentation whenever a user asks a technical question 
        or you need more context to provide an accurate answer.
        """
        print(f"Retrieving documents for query: {query}")
        
        # Pull documents from Pinecone
        docs = retriever.invoke(query)
        
        # Format retrieved documents as a raw string
        formatted_docs = format_docs(docs)
        
        return formatted_docs

    return search_documentation