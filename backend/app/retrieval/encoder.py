from typing import List

class QuickSparseEncoder:
    def __init__(self, pc, model_name="pinecone-sparse-english-v0"):
        self.pc = pc
        self.model_name = model_name
        
    def encode_queries(self, queries: str):
        if isinstance(queries, str):
            queries = [queries]
        res = self.pc.inference.embed(
            model=self.model_name,
            inputs=queries,
            parameters={"input_type": "query"}
        )
        return {"indices": res[0].sparse_indices, "values": res[0].sparse_values}
        
    def encode_documents(self, texts: List[str]):
        res = self.pc.inference.embed(
            model=self.model_name,
            inputs=texts,
            parameters={"input_type": "passage", "truncate": "END"}
        )
        return [{"indices": r.sparse_indices, "values": r.sparse_values} for r in res]
