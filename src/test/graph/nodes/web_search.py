from typing import Dict, Any

from src.test.graph.state import GraphState
from langchain_core.documents import Document
from langchain_tavily import TavilySearch

web_search_tool = TavilySearch(max_results=5)

def web_search(state: GraphState) -> Dict[str, Any]:
    print("__Web search__")
    
    question = state["question"]
    documents = state["documents"] if "documents" in state else None
    
    tavily_results = web_search_tool.invoke({"query": question})["results"]
    joined_tavily_result = "\n".join([
        tavily_result["content"] for tavily_result in tavily_results
    ])
    
    web_results = Document(page_content=joined_tavily_result)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
return {"documents": documents, "question": question}


if __name__ == "__main__":
    web_search(state={"question": "agent memory", "documents": None})