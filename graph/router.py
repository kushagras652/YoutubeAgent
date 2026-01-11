from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage,HumanMessage

class IntentRouter:
    def __init__(self):
        self.llm=ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0 
        )

        self.system_prompt="""
Classify the user's intent into one of the following categories:
 - question_answering
 -quiz_generation
 -summary_generation

 Respond with ONLY the intent label.
"""

    def route(self,state):
        messages=[
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=state['user_input'])
        ]

        intent=self.llm.invoke(messages).content.strip()
        return {'intent':intent}