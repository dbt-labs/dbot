import os

from dotenv import load_dotenv

from vector_store import VectorStore

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


template = """
 Answer the question as truthfully as possible using the provided context, and assume 
 that the question is about dbt, analytics engineering, or data. Prefer code snippets 
 over prose where possible and relevant. 
 If the answer is not contained within the text below, say "I don't know."\n
 \n
 Context:\n
 {context} \n
 \n
 Question: In dbt \n
  {question}
"""


class QuestionAnswerer:
    def __init__(self):
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        from langchain import OpenAI

        self.llm = OpenAI(client=OPENAI_API_KEY, temperature=0)
        self.vector_store = VectorStore(
            name="qa-db", sources_path="./context-sources", reindex=True
        )

    def answer_question(self, question: str):
        """Use the LLM to answer a question using the vector store as context."""
        if not isinstance(question, str):
            raise TypeError("Question must be a string")

        from langchain import PromptTemplate

        prompt = PromptTemplate(
            input_variables=["context", "question"], template=template
        )

        chosen_sections = self.vector_store.choose_relevant_documents(question)
        context = chosen_sections["content"]
        sources = chosen_sections["source_links"]
        question = prompt.format(question=question, context=context)

        answer = self.llm(question)
        answer_with_sources = self.append_source_links(sources, answer)

        return answer_with_sources

    def append_source_links(self, source_links: list, answer: str) -> str:
        """Appends source links to the end of an answer."""
        answer += "\n\nSources:"
        for link in source_links:
            answer += f"\n{link}"
        return answer
