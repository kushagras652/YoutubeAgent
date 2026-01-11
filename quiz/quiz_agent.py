from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage,HumanMessage
from dotenv import load_dotenv

load_dotenv()

class QuizAgent:
    def __init__(self):
        self.llm=ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0
        )

        self.system_prompt="""
You are an educational quiz generator.

Rules:
- Generate questions ONLY from the given video context.
- Do NOT introduce outside knowledge.
- If context is insufficient, generate fewer questions.
- Always include correct answers and explanations.
- Be clear, precise, and educational.
"""
    def generate_quiz(
            self,
            retrieved_docs:list,
            num_questions: int=5,
            difficulty:str ="medium"
    )->str:
        context="\n\n".join(
            [doc.page_content for doc,_ in retrieved_docs]
        )

        prompt=f"""
Context from video:
{context}

Task:
Create {num_questions} quiz questions based on the video.

Difficulty: {difficulty}

Format:
1. Question
   A. Option
   B. Option
   C. Option
   D. Option
   Correct Answer:
   Explanation:

Only use information present in the context.
"""
        messages=[
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]

        response=self.llm.invoke(messages)
        return response.content.strip()