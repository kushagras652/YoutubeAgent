from langgraph.graph import StateGraph,END
from graph.state import GraphState
from graph.router import IntentRouter
from qa.rag_qa import RAGQAAgent
from quiz.quiz_agent import QuizAgent
from summary.summary_agent import SummaryAgent

def build_graph(vector_store):

    router=IntentRouter()
    qa_agent=RAGQAAgent()
    quiz_agent=QuizAgent()
    summary_agent=SummaryAgent()

    def route_node(state:GraphState):
        return router.route(state)
    
    def qa_node(state:GraphState):
        docs=vector_store.search(state['user_input'],top_k=4)
        answer=qa_agent.answer(state['user_input'],docs)
        return {'answer':answer}
    
    def summary_node(state:GraphState):
        docs=vector_store.search('key topics in the video',top_k=6)
        summary=summary_agent.summarize(docs)
        return {'summary':summary}
    
    def quiz_node(state:GraphState):
        docs=vector_store.search(state['user_input'],top_k=6)
        quiz=quiz_agent.generate_quiz(docs)
        return {'quiz':quiz}
    
    graph=StateGraph(GraphState)

    graph.add_node('router',route_node)
    graph.add_node('qa',qa_node)
    graph.add_node('quiz',quiz_node)
    graph.add_node('summary',summary_node)

    graph.set_entry_point('router')

    graph.add_conditional_edges(
        "router",
        lambda state:state['intent'],
        {
            'question_answering':'qa',
            'quiz_generation':'quiz',
            'summary_generation':'summary'
        }
    )

    graph.add_edge('qa',END)
    graph.add_edge('quiz',END)
    graph.add_edge('summary',END)

    return graph.compile()