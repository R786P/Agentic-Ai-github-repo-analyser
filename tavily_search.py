from tavily import TavilyClient
import os

# Initialize Tavily client
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search_tool(query: str) -> str:
    try:
        response = tavily.search(query=query, search_depth="basic")
        return response.get("results", [{}])[0].get("content", "No relevant info found.")
    except Exception as e:
        return f"Search failed: {str(e)}"
