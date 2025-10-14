from langgraph.graph import StateGraph, END
from data_analysis_agents.ingest import ingest_data
from data_analysis_agents.analyzer import analyze_data
from data_analysis_agents.visualizer import visualize_data
from data_analysis_agents.insight_writer import write_insights
from data_analysis_agents.report_builder import build_report

graph = StateGraph(dict)

graph.add_node("ingest", ingest_data)
graph.add_node("analyzer", analyze_data)
graph.add_node("visualizer", visualize_data)
graph.add_node("insight_writer", write_insights)
graph.add_node("report", build_report)

graph.set_entry_point("ingest")
graph.add_edge("ingest", "analyzer")
graph.add_edge("analyzer", "visualizer")
graph.add_edge("visualizer", "insight_writer")
graph.add_edge("insight_writer", "report")
graph.add_edge("report", END)

data_analysis_graph = graph.compile()
