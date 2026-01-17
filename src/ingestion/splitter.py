from typing import List

from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_classic.schema import Document

class MarkdownDocsSplitter:
    """
    Markdown splitter for LangChain Docs
    """

    HEADERS_TO_SPLIT_ON = [
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3"),
        ("####", "h4"),
    ]

    def __init__(self):
        self.splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.HEADERS_TO_SPLIT_ON,
            strip_headers=False,
        )

    def split(
        self,
        markdown: str,
        *,
        source_url: str,
        doc_id: str,
    ) -> List[Document]:
        docs = self.splitter.split_text(markdown)

        for doc in docs:
            doc.metadata.update({
                "doc_id": doc_id,
                "source_url": source_url,
                "source_type": "markdown",
                "doc_site": "langchain",
            })

        return docs