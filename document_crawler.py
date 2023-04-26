import hashlib
from abc import abstractmethod
from typing import List

from langchain.docstore.document import Document


class DocumentCrawler:
    @abstractmethod
    def crawl_and_make_docs(self) -> List[Document]:
        pass

    @abstractmethod
    def split_file_into_docs(self) -> List[Document]:
        pass

    @abstractmethod
    def hash_string(self, string: str) -> str:
        """Creates an md5 hash from a string."""
        return hashlib.md5(string.encode()).hexdigest()

    @abstractmethod
    def make_source_link(self, source: str) -> str:
        """Creates a link to the source file from the Document source property."""
        pass
