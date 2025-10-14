from langgraph.graph import StateGraph, END

# Import agents
from research_agents.planner import plan_research
from research_agents.search import run_search
from research_agents.synthesizer import synthesize_results
from research_agents.writer import compose_report
from research_agents.reviewer import review_report
from research_agents.delivery import deliver_report

# Create a graph with dict state
graph = StateGraph(dict)

# Add nodes
graph.add_node("planner", plan_research)
graph.add_node("search", run_search)
graph.add_node("synthesizer", synthesize_results)
graph.add_node("writer", compose_report)
graph.add_node("reviewer", review_report)
graph.add_node("delivery", deliver_report)

# Connect nodes
graph.add_edge("planner", "search")
graph.add_edge("search", "synthesizer")
graph.add_edge("synthesizer", "writer")
graph.add_edge("writer", "reviewer")
graph.add_edge("reviewer", "delivery")

# Define entry and end
graph.set_entry_point("planner")
graph.add_edge("delivery", END)

# Compile runnable app
research_graph = graph.compile()
