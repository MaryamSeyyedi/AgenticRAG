from typing import Dict, Any

from src.test.graph.chains.generation import generation_chain
from src.test.graph.state import GraphState

def generate(state: GraphState):
    print("__generate__")
    question = state["question"]
    documents = state["documents"]
    
    generation = generation_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}
    