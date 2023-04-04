from langchain.docstore.document import Document

from question_answerer import QuestionAnswerer
from vector_store import VectorStore

qa = QuestionAnswerer()
embeddings = VectorStore(name="dbt-docs", docs_loc="./docs")


def test_should_return_string_as_answer():
    answer = qa.answer_question()
    assert type(answer) == str


def test_vector_store_returns_list_of_similar_results():
    results = embeddings.get_similar_documents("What is dbt?")
    assert type(results) == list


def test_vector_store_returns_Documents_for_similar_results():
    results = embeddings.get_similar_documents("What is dbt?")
    assert all(isinstance(document[0], Document) for document in results)


# test that vector store returns a vector store
# test that vector store returns a vector store with the right number of vectors
# test that vector store creates a new vector store if one doesn't exist


# Important considerations:
# test edge cases
# think about what the unit of abstraction is
