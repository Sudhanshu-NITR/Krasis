def process_url(url: str, loader, splitter, store):    
    raw = loader.load(url)
    if not raw:
        return 
    
    store.delete_by_source_url(url)

    docs = splitter.split(
        raw["content"],
        source_url=raw["source_url"],
        doc_id=raw["doc_id"]
    )

    store.upsert_documents(docs)