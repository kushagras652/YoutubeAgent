from typing import TypedDict,Optional,List
from langchain_core.documents import Document

class GraphState(TypedDict):
    user_input:str
    intent:Optional[str]

    retrieved_docs:Optional[List]
    answer:Optional[str]
    quiz:Optional[str]
    summary:Optional[str]