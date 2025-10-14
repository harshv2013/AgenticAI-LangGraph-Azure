import os
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv(override=True)

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def run_search(inputs):
    queries = inputs["queries"]
    results = []
    for q in queries:
        response = client.search(q)
        results.append({
            "query": q,
            "snippet": response["results"][0]["content"] if response["results"] else "No result"
        })
    return {"queries": queries, "user_prompt": inputs["user_prompt"], "results": results}
