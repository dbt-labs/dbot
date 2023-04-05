# import modal

from question_answerer import QuestionAnswerer

# stub = modal.Stub(name="question_answerer")


qa = QuestionAnswerer()


# @stub.function
def answer_question(question: str):
    answer = qa.answer_question(question)
    print(answer)


if __name__ == "__main__":
    question = input("Ask a question: ")
    answer_question(question)
