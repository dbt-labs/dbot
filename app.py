from fastapi import FastAPI

from question_answerer import QuestionAnswerer

qa = QuestionAnswerer()
app = FastAPI()


@app.get("/answer")
def get_answer(question: str = "What is dbt?"):
    return {"answer": qa.answer_question(question)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
