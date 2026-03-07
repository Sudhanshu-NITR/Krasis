from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from src.core.prompts import get_prompt_template

def format_docs(docs):
    """
    Formats retrieved documents into a string while preserving source metadata.
    This helps the LLM cite specific documentation URLs.
    """
    return "\n\n".join(
        f"--- DOCUMENT START ---\n"
        f"Content: {doc.page_content}\n"
        f"Source URL: {doc.metadata.get('source_url', doc.metadata.get('url', 'No link available'))}\n"
        f"--- DOCUMENT END ---"
        for doc in docs
    )

def create_rag_chain(retriever, llm):
    """
    Constructs a hybrid search RAG chain.
    """

    prompt = get_prompt_template()

    # Step 1: Prepare the context and question in parallel
    context_and_question = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough(),
        # "chat_history": 
    })

    # Step 2: Combine into the final chain
    main_chain = context_and_question | prompt | llm | StrOutputParser()

    return main_chain