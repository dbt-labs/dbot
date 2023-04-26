import pytest

from question_answerer import QuestionAnswerer


# def test_question_answerer_returns_a_string():
#     qa = QuestionAnswerer("./test-docs")

#     answer = qa.answer_question("What is dbt?")

#     assert type(answer) == str


# def test_question_answerer_refuses_non_strings_as_input():
#     qa = QuestionAnswerer("./test-docs")

#     with pytest.raises(TypeError):
#         qa.answer_question(42)  # type: ignore
