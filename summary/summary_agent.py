from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage,HumanMessage

class SummaryAgent:
    def __init__(self):
        self.llm=ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0
        )

    def summarize(self,docs):
        context="\n\n".join([doc.page_content for doc,_ in docs])

        messages=[
            SystemMessage(
                content="Summarize the following video content clearly and concisely."
            ),
            HumanMessage(content=context)
        ]

        return self.llm.invoke(messages).content.strip()