import os
import re
from typing import List

from langchain.docstore.document import Document

from document_crawler import DocumentCrawler


class MarkdownCrawler(DocumentCrawler):
    """Crawls a filepath and subdirs for markdown files and splits them into chunks."""

    def __init__(self, sources_path: str) -> None:
        self.sources_path = sources_path

    def crawl_and_make_docs(self) -> List[Document]:
        """Crawls all dirs and subdirs in a filepath for markdown files to chunk"""
        docs = []
        for dirpath, dirnames, filenames in os.walk(self.sources_path):
            markdown_filenames = [
                f"{dirpath}/{filename}"
                for filename in filenames
                if filename.endswith(".md")
            ]
            for filename in markdown_filenames:
                docs_split_from_file = self.split_file_into_docs(filename)
                docs.extend(docs_split_from_file)

        return docs

    def split_file_into_docs(self, filename) -> List[Document]:
        """Splits a markdown file into a list of chunks with metadata."""
        docs: List[Document] = []
        with open(filename, "r") as f:
            markdown = f.read()
            chunks = re.findall(
                # make header and content in the same group
                r"^#{2,}\s+(.*?)\n(.*?)(?=\n#{2,}|\Z)",
                markdown,
                flags=re.DOTALL | re.MULTILINE,
            )
            for chunk in chunks:
                docs.append(
                    Document(
                        page_content=f"{chunk[0]}{chunk[1]}",
                        metadata={
                            "id": self.hash_string(f"{filename}{chunk[0]}{chunk[1]}"),
                            "source": filename,
                        },
                    )
                )

        return docs
