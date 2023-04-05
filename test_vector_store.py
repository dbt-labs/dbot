from langchain.docstore.document import Document

from vector_store import VectorStore


def test_vector_store_returns_list_of_similar_documents_with_scores():
    vector_store = VectorStore(name="dbt-docs", docs_loc="./test-docs")

    results = vector_store.get_similar_documents("What is dbt?")

    assert type(results) == list
    assert all(isinstance(document[0], Document) for document in results)
    assert all(isinstance(document[1], float) for document in results)
