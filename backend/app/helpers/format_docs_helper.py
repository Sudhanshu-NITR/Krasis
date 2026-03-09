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
