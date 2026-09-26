from typing import Dict, Any

from src.test.graph.chains.retrieval_grader import retrieval_grader
from src.test.graph.state import GraphState


def grade_documents(state: GraphState) -> Dict[str, Any]:
    print("__Check document relevance to the question__")
    
    question = state["question"]
    documents = state["documents"]
    
    filtered_docs = []
    web_search = False
    
    for doc in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": document}
        )
        
        grade = score.binary_score
        
        if grade.lower == "yes":
            filtered_docs.append(doc)
        else:
            web_search = True
            continue
        
    return {"documents": filtered_docs, "question": question, "web_search": web_search}