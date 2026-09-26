from src.test.graph.chains.answer_grader import answer_grader
from src.test.graph.chains.hallucination_grader import hallucination_grader
from src.test.graph.chains.router import RouteQuery, question_router
from src.test.graph.consts import GENERATE, GRADE_DOCUMENTS, RETRIEVE, WEBSEARCH
from src.test.graph.nodes import generate, grade_documents, retrieve, web_search
from src.test.graph.state import GraphState

from langgraph.graph import StateGraph, END


def decide_to_generate(state):
    print("__Asses graded documents__")
    
    if state["web_search"]:
        return WEBSEARCH
    else:
        return GENERATE
    
    
def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    print("__Check hallucination__")
    
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]
    
    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )
    
    hallucination_grade = score.binary_score
    if hallucination_grade:
        score = answer_grader.invoke({"question": question, "generation": generation})
        answer_grade = score.binary_score
        if answer_grade:
            return "useful"
        else:
            return "not useful"
        
    else:
        return "not supported"
    

def route_question(state: GraphState) -> str:
    print("__Route Question__")
    question = state["question"]
    source: RouteQuery = question_router.invoke({"question": question})
    if source.datasource == WEBSEARCH:
        return WEBSEARCH
    else:
        return RETRIEVE
    
    


workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)

workflow.set_conditional_entry_point(route_question, {
    WEBSEARCH: WEBSEARCH,
    RETRIEVE: RETRIEVE
})
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS, decide_to_generate, {
        WEBSEARCH: WEBSEARCH
        GENERATE: GENERATE
    }
)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {
        "not supported": GENERATE,
        "useful": END,
        "not useful": WEBSEARCH,
    },
)
workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, END)


app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")