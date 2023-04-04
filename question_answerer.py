import os

from dotenv import load_dotenv
from langchain import OpenAI, PromptTemplate

from vector_store import VectorStore

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

template = """
 Answer the question as truthfully as possible using the provided context, 
 and if the answer is not contained within the text below, say "I don't know."
 \n
 \n
 Context:
 \n
 {context}
 \n
 \n
 Question:
 \n
 {question}
"""


class QuestionAnswerer:
    def __init__(self):
        self.llm = OpenAI(client=OPENAI_API_KEY, temperature=0.8)
        self.db = VectorStore(name="dbt-docs", docs_loc="./docs")

    def answer_question(self) -> str:
        prompt = PromptTemplate(
            input_variables=["context", "question"], template=template
        )
        question = input("Ask a question: ")
        context = self.db.rank_and_truncate_documents(question)
        answer = self.llm(prompt.format(question=question, context=context))
        print(answer)
