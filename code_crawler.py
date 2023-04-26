import os
from typing import List, Tuple

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

from document_crawler import DocumentCrawler


class CodeCrawler(DocumentCrawler):
    def __init__(self, sources_path: str) -> None:
        self.sources_path: str = sources_path
        self.file_types: Tuple = (".py", ".sql")

    def crawl_and_make_docs(self) -> List[Document]:
        """Crawls all dirs and subdirs in a filepath for markdown files to chunk"""
        docs = []
        for dirpath, dirnames, filenames in os.walk(self.sources_path):
            filtered_filenames = [
                f"{dirpath}/{filename}"
                for filename in filenames
                if filename.endswith(self.file_types)
            ]
            for filename in filtered_filenames:
                docs_split_from_file = self.split_file_into_docs(filename)
                docs.extend(docs_split_from_file)

        return docs

    def split_file_into_docs(self, filename) -> List[Document]:
        """Splits code files into a list of chunks with metadata."""
        docs: List[Document] = []
        with open(filename, "r") as f:
            code = f.read()

            text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
            chunks = text_splitter.split_text(code)
            for chunk in chunks:
                docs.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "id": self.hash_string(f"{filename}{chunk}"),
                            "source": filename,
                        },
                    )
                )

        return docs

    def make_source_link(self, source: str) -> str:
        """Creates a link to the source file from the Document source property."""
        return f"https://github.com/dbt-labs/jaffle-shop-template/blob/main/{source}"
