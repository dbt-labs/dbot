import os

import tiktoken
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class VectorStore:
    def __init__(self, name: str, docs_loc: str) -> None:
        embedder = OpenAIEmbeddings(client=OPENAI_API_KEY)
        # Check if a directory exists and if not create it
        if not os.path.exists(f"./{name}"):
            os.makedirs(f"./{name}")
        if os.listdir(f"./{name}") == []:
            self.create_db(name, docs_loc, embedder)
        else:
            self.database = Chroma(
                persist_directory=f"./{name}", embedding_function=embedder
            )
            print("🔮 Loaded database of embeddings")

    def create_db(self, name: str, docs_path: str, embedder: OpenAIEmbeddings):
        loader = DirectoryLoader(
            docs_path, glob="**/*.md"
        )  # Why doesn't recursive=True work?
        docs = loader.load()
        self.database = Chroma.from_documents(
            documents=docs,
            embedding=embedder,
            name=name,
            persist_directory=f"./{name}",
        )
        print("🔮 New database of embeddings created")
        self.add_docs_in_subdirs(path=docs_path)

    def add_docs_in_subdirs(self, path: str):
        for root, dir_names, file_names in os.walk(path):
            for f in file_names:
                item_path = os.path.join(root, f)
                if f.endswith(".md"):
                    loader = UnstructuredMarkdownLoader(item_path)
                    doc = loader.load()
                    if (self.num_tokens_from_string(doc[0].page_content)) > 8191:
                        # doc = truncate_document(doc)
                        continue
                    self.database.add_documents(doc)
                    print(f"📝 Docs in {item_path} directory added to database")

    def num_tokens_from_string(
        self, string: str, encoding_name: str = "cl100k_base"
    ) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    # def truncate_document(self, document: tuple, max_tokens: int = 8191):
    #     """Truncates a document to a maximum number of tokens."""
    #     document_content = document[0].page_content
    #     document_tokens = self.num_tokens_from_string(document_content, "cl100k_base")
    #     if document_tokens > max_tokens:
    #         truncated_document = document_content[:max_tokens]
    #     else:
    #         truncated_document = document_content
    #     return truncated_document

    def get_similar_documents(self, question: str):
        results = self.database.similarity_search_with_score(question)
        return results

    def rank_and_truncate_documents(self, question: str, max_tokens: int = 3000):
        SEPARATOR = "\n* "
        SEPARATOR_LEN = 3
        results = self.get_similar_documents(question)
        chosen_sections = ""
        chosen_sections_len = 0

        for result in results:
            result_content = result[0].page_content.replace("\n", " ")
            if (
                chosen_sections_len
                + self.num_tokens_from_string(result_content)
                + SEPARATOR_LEN
                > max_tokens
            ):
                break

            chosen_sections += SEPARATOR + result_content

            chosen_sections_len += SEPARATOR_LEN + self.num_tokens_from_string(
                result_content
            )
        return chosen_sections
