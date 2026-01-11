from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,SystemMessage
from dotenv import load_dotenv

load_dotenv()

class RAGQAAgent:
    def __init__(self):
        self.llm=ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0 
        )

        self.system_prompt="""
You are a teaching assistant answering questions strictly
based on the provided video transcript excerpts.

Rules:
- Use ONLY the given context.
- If the answer is not present, say:
  "This was not explained in the video."
- Do NOT use outside knowledge.
- Be clear and concise.
"""

    def answer(self,question:str,retrieved_docs:list)->str:
        context="\n\n".join(
            [doc.page_content for doc,_ in retrieved_docs]
        )

        messages=[
            SystemMessage(content=self.system_prompt),
            HumanMessage(
                content=f"""
Context from Video:
{context}

Question:
{question}
"""
            )
        ]

        response=self.llm.invoke(messages)
        return response.content.strip()
    