import os
from typing import List

from langchain.docstore.document import Document
from langchain.document_loaders.csv_loader import CSVLoader

from document_crawler import DocumentCrawler


class CSVCrawler(DocumentCrawler):
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
                if filename.endswith(".csv")
            ]
            for filename in markdown_filenames:
                docs_split_from_file = self.split_file_into_docs(filename)
                docs.extend(docs_split_from_file)

        return docs

    def split_file_into_docs(self, filename) -> List[Document]:
        """Splits a markdown file into a list of chunks with metadata."""
        docs = CSVLoader(filename, source_column="topic_id").load()

        for doc in docs:
            doc.metadata["id"] = self.hash_string(
                f"{doc.metadata['source']}{doc.page_content}"
            )

        return docs

    def make_source_link(self, source: str) -> str:
        """Creates a link to the source file from the Document source property."""
        source = source.replace(".csv", "")
        return f"https://discourse.getdbt.com/t/{source}"
