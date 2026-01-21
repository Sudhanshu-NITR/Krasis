import re
from typing import List
from langchain_classic.schema import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter


CODE_BLOCK_PATTERN = re.compile(r"```[\s\S]*?```", re.MULTILINE)


class CodeAwareMarkdownSplitter:
    HEADERS_TO_SPLIT_ON = [
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3"),
        ("####", "h4"),
    ]

    def __init__(self):
        self.header_splitter = MarkdownHeaderTextSplitter(
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
        docs = self.header_splitter.split_text(markdown)

        final_docs = []
        for doc in docs:
            contains_code = bool(CODE_BLOCK_PATTERN.search(doc.page_content))

            doc.metadata.update({
                "doc_id": doc_id,
                "source_url": source_url,
                "source_type": "markdown",
                "doc_site": "langchain",
                "contains_code": contains_code,
            })

            final_docs.append(doc)

        return final_docs
