from question_answerer import QuestionAnswerer

qa = QuestionAnswerer()


def test_should_return_string_as_answer():
    answer = qa.answer_question("What is dbt?")
    assert type(answer) == str
