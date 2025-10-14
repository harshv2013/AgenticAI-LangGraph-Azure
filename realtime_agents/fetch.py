# realtime_agents/fetch.py
import logging
from services.tavily_client import tavily_client


def fetch(state: dict):
    """
    Uses Tavily to fetch real-time data for weather, price, stock, or news.
    """
    query_text = state.get("query", "")
    intent = state.get("intent", "general")

    try:
        # Perform a real-time search using Tavily
        result = tavily_client.search(query=query_text, max_results=3)

        # Combine summary + sources
        summaries = []
        sources = []
        for r in result.get("results", []):
            title = r.get("title", "Untitled")
            url = r.get("url", "")
            content = r.get("content", "")
            summaries.append(f"🔹 {title}: {content[:200]}...")
            if url:
                sources.append(f"- [{title}]({url})")

        combined_summary = "\n".join(summaries)
        combined_sources = "\n".join(sources)

        return {
            "source": "tavily",
            "data": {
                "intent": intent,
                "query": query_text,
                "summary": combined_summary[:2000],  # limit size
                "links": combined_sources,           # ✅ Added link list
            },
        }

    except Exception as e:
        print(f"⚠️ Tavily fetch error: {e}")
        return {
            "source": "tavily",
            "data": {"intent": intent, "error": str(e)},
        }
