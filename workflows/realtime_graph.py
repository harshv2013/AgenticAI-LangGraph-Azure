# workflows/realtime_graph.py
from langgraph.graph import StateGraph, END
from realtime_agents.query import query
from realtime_agents.fetch import fetch
from realtime_agents.summarizer import summarizer
from realtime_agents.delivery import delivery

graph = StateGraph(dict)

graph.add_node("query", query)
graph.add_node("fetch", fetch)
graph.add_node("summarizer", summarizer)
graph.add_node("delivery", delivery)

graph.add_edge("query", "fetch")
graph.add_edge("fetch", "summarizer")
graph.add_edge("summarizer", "delivery")
graph.add_edge("delivery", END)

graph.set_entry_point("query")

realtime_graph = graph.compile()
