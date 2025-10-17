# from langgraph.graph import StateGraph, END
# from data_analysis_agents.ingest import ingest_data
# from data_analysis_agents.analyzer import analyze_data
# from data_analysis_agents.visualizer import visualize_data
# from data_analysis_agents.insight_writer import write_insights
# from data_analysis_agents.report_builder import build_report

# graph = StateGraph(dict)

# graph.add_node("ingest", ingest_data)
# graph.add_node("analyzer", analyze_data)
# graph.add_node("visualizer", visualize_data)
# graph.add_node("insight_writer", write_insights)
# graph.add_node("report", build_report)

# graph.set_entry_point("ingest")
# graph.add_edge("ingest", "analyzer")
# graph.add_edge("analyzer", "visualizer")
# graph.add_edge("visualizer", "insight_writer")
# graph.add_edge("insight_writer", "report")
# graph.add_edge("report", END)

# data_analysis_graph = graph.compile()




# # workflows/data_analysis_graph.py
# from langgraph.graph import StateGraph, END
# from data_analysis_agents.ingest import ingest
# from data_analysis_agents.intent import detect_intent
# from data_analysis_agents.codegen import generate_code
# from data_analysis_agents.executor import execute_code
# from data_analysis_agents.summarizer import summarize
# from data_analysis_agents.suggestor import suggest
# from data_analysis_agents.report_builder import build_report

# # Graph uses a dict state
# graph = StateGraph(dict)

# graph.add_node("ingest", ingest)
# graph.add_node("intent", detect_intent)
# graph.add_node("codegen", generate_code)
# graph.add_node("executor", execute_code)
# graph.add_node("summarizer", summarize)
# graph.add_node("suggestor", suggest)
# graph.add_node("report", build_report)

# # Flow:
# graph.add_edge("ingest", "intent")

# # If intent says code_run or viz: generate code -> execute -> summarizer -> suggestor -> report
# graph.add_edge("intent", "codegen")
# graph.add_edge("codegen", "executor")
# graph.add_edge("executor", "summarizer")
# graph.add_edge("summarizer", "suggestor")
# graph.add_edge("suggestor", "report")
# graph.add_edge("report", END)

# graph.set_entry_point("ingest")

# data_analysis_graph = graph.compile()



# workflows/data_analysis_graph.py
from langgraph.graph import StateGraph, END
from data_analysis_agents.ingest import ingest
from data_analysis_agents.intent import detect_intent
from data_analysis_agents.codegen import generate_code
from data_analysis_agents.executor import execute_code
from data_analysis_agents.summarizer import summarize
from data_analysis_agents.suggestor import suggest
from data_analysis_agents.report_builder import build_report


# -------------------------------
# 🧩 Utility: Flatten node outputs
# -------------------------------
def flatten_state(state, node_output):
    """
    LangGraph passes each node's output as {node_name: node_output}.
    This merges key fields like file_path, df, etc., to the global state.
    """
    if not isinstance(node_output, dict):
        return state

    # Promote important fields
    if "file_path" in node_output:
        state["file_path"] = node_output["file_path"]
    if "df" in node_output:
        state["df"] = node_output["df"]
    if "status" in node_output:
        state["status"] = node_output["status"]

    # Merge the node output itself
    state.update(node_output)
    return state


# -------------------------------
# 🧠 Node wrapper functions
# -------------------------------
def ingest_node(state):
    output = ingest(state)
    return flatten_state(state, output)

def intent_node(state):
    output = detect_intent(state)
    return flatten_state(state, output)

def codegen_node(state):
    output = generate_code(state)
    return flatten_state(state, output)

def executor_node(state):
    output = execute_code(state)
    return flatten_state(state, output)

def summarizer_node(state):
    output = summarize(state)
    return flatten_state(state, output)

def suggestor_node(state):
    output = suggest(state)
    return flatten_state(state, output)

def report_node(state):
    output = build_report(state)
    return flatten_state(state, output)


# -------------------------------
# 🧠 Graph definition
# -------------------------------
graph = StateGraph(dict)

graph.add_node("ingest", ingest_node)
graph.add_node("intent", intent_node)
graph.add_node("codegen", codegen_node)
graph.add_node("executor", executor_node)
graph.add_node("summarizer", summarizer_node)
graph.add_node("suggestor", suggestor_node)
graph.add_node("report", report_node)

# Flow definition
graph.add_edge("ingest", "intent")
graph.add_edge("intent", "codegen")
graph.add_edge("codegen", "executor")
graph.add_edge("executor", "summarizer")
graph.add_edge("summarizer", "suggestor")
graph.add_edge("suggestor", "report")
graph.add_edge("report", END)

graph.set_entry_point("ingest")

data_analysis_graph = graph.compile()
