from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
# Document
# Standard LangChain data structure
# Wraps:
# page_content → actual text
# metadata → extra info (IDs, timestamps, source, etc.)
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

class LangChainVectorStore:
    # __init__ is a constructor automatically runs whne an object of LangChainVectorStore() is created
    def __init__(self):
        # why self makes it accissible to other methods
        self.embeddings=OpenAIEmbeddings(model='text-embedding-3-small')
        self.vectorstore=None

    def build_from_chunks(self,chunks:list[dict]):
        documents=[]

        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk['text'],
                    metadata={
                        "chunk_id":chunk['chunk_id'],
                        "start_char":chunk['start_char'],
                        'end_char':chunk['end_char']
                    }
                )
            )
        # here in this line Document.page_content is sent to OpenAI and gets embeddings then FIASS indexes those vectors
        self.vectorstore=FAISS.from_documents(
            documents,
            self.embeddings
        )

    def search(self,query:str,top_k:int =5):
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        
        return self.vectorstore.similarity_search_with_score(
            query,
            k=top_k
        )