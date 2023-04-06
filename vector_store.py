import os

import tiktoken
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from markdown_splitter import MarkdownSplitter

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class VectorStore:
    def __init__(self, name: str, docs_loc: str) -> None:
        embedder = OpenAIEmbeddings(client=OPENAI_API_KEY)
        self.initialize_db(name, docs_loc, embedder)

    def initialize_db(self, name: str, docs_loc: str, embedder: OpenAIEmbeddings):
        """Initialize a new vector store or load an existing one."""
        if not os.path.exists(f"./{name}"):
            os.makedirs(f"./{name}")
        self.database = Chroma(
            persist_directory=f"./{name}", embedding_function=embedder
        )
        if os.listdir(f"./{name}") == []:
            print(f"🔮 Initialized new vector store {name}")
            self.add_docs(name, docs_loc, embedder)
            print(f"✅ Added embeddings for all docs in {docs_loc} to vector store")
        else:
            print(f"🔮 Loaded existing vector store {name}")

    def add_docs(self, name: str, docs_path: str, embedder: OpenAIEmbeddings):
        """Add all docs in a directory to the vector store."""
        for root, dir_names, file_names in os.walk(docs_path):
            for f in file_names:
                item_path = os.path.join(root, f)
                if f.endswith(".md"):
                    markdown_splitter = MarkdownSplitter()
                    docs = markdown_splitter.create_documents(item_path)
                    for doc in docs:
                        self.database.add_documents([doc])
                        print(
                            f"🌱 Added {doc.metadata['source']}#{doc.metadata['slug']}"
                        )
            print(f"🕸️ Embeddings for docs in {root} directory added to vector store")

    def num_tokens_from_string(
        self, string: str, encoding_name: str = "cl100k_base"
    ) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def get_similar_documents(self, question: str):
        """Returns a list of documents similar to a question with a similarity score."""
        results = self.database.similarity_search_with_score(question)
        return results

    def format_source_links(self, source: str) -> str:
        """Formats a file path into a  source link on the dbt docs site."""
        return source.replace("./docs", "https://docs.getdbt.com").replace(".md", "")

    def choose_relevant_documents(self, question: str, max_tokens: int = 3000):
        """Chooses relevant documents to answer a question within a max_tokens limit."""
        SEPARATOR = "\n* "
        SEPARATOR_LEN = 3
        results = self.get_similar_documents(question)
        chosen_sections = {
            "content": "",
            "source_links": [],
            "length": 0,
        }

        for result in sorted(results, key=lambda x: x[1], reverse=True):
            result_data = result[0]
            result_content = result_data.page_content.replace("\n", " ")
            result_source = result_data.metadata["source"]
            result_source_link = self.format_source_links(result_source)
            result_slug = result_data.metadata["slug"]

            if (
                chosen_sections["length"]
                + self.num_tokens_from_string(result_content)
                + SEPARATOR_LEN
                > max_tokens
            ):
                break

            chosen_sections["content"] += SEPARATOR + result_content

            chosen_sections["source_links"].append(
                f"{result_source_link}#{result_slug}"
            )

            chosen_sections["length"] += SEPARATOR_LEN + self.num_tokens_from_string(
                result_content
            )

        return chosen_sections
        return chosen_sections
