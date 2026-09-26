from typing import Dict, Any

from src.test.ingestion import retriever
from src.test.graph.state import GraphState



def retriever(state: GraphState) -> Dict[str, Any]:
    print("__Retrieve__")
    question = state["question"]
    
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}