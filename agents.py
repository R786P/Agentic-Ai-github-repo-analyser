from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from tools.tavily_search import tavily_search_tool

class AgentState(TypedDict):
    repo_url: str
    analysis_mode: str
    messages: Annotated[list, operator.add]
    result: str

def github_fetch_node(state: AgentState):
    repo_url = state["repo_url"]
    # In real use, call GitHub API here
    messages = [f"Fetched metadata for {repo_url}. Mode: {state['analysis_mode']}"]
    return {"messages": messages}

def reasoning_node(state: AgentState):
    mode = state["analysis_mode"]
    if mode == "codebase_summary":
        task = "Summarize codebase structure, main languages, and key files."
    elif mode == "security_check":
        task = "Check for known security issues or deprecated dependencies."
    else:
        task = "Analyze top contributors and recent activity trends."
    
    context = tavily_search_tool(f"{state['repo_url']} {task}")
    result = f"Insight ({mode}): {context[:500]}..."
    return {"result": result}

def should_continue(state: AgentState):
    return "reasoning" if len(state["messages"]) == 1 else END

workflow = StateGraph(AgentState)
workflow.add_node("fetch", github_fetch_node)
workflow.add_node("reasoning", reasoning_node)
workflow.set_entry_point("fetch")
workflow.add_edge("fetch", "reasoning")
workflow.add_conditional_edges("reasoning", should_continue)

app_graph = workflow.compile()

def run_analysis_agent(repo_url: str, analysis_mode: str) -> str:
    inputs = {"repo_url": repo_url, "analysis_mode": analysis_mode, "messages": []}
    result = app_graph.invoke(inputs)
    return result.get("result", "No result generated.")
