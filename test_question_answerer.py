import pytest

from question_answerer import QuestionAnswerer


def test_question_answerer_returns_a_string():
    qa = QuestionAnswerer()

    answer = qa.answer_question("What is dbt?")

    assert type(answer) == str


def test_question_answerer_refuses_non_strings_as_input():
    qa = QuestionAnswerer()

    # TODO: How do we test other types?
    with pytest.raises(TypeError):
        qa.answer_question(42)
