# workflows/general_manager_graph.py
from langgraph.graph import StateGraph, END
from workflows.research_graph import research_graph
from workflows.data_analysis_graph import data_analysis_graph
from workflows.realtime_graph import realtime_graph
from services.router_llm import llm_route_classifier

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] : %(message)s",
)

def route_request(state):
    """LLM-based router to decide workflow dynamically."""
    user_input = state.get("input", "")
    file_path = state.get("file_path")

    # 🧮 File uploads are still deterministic
    if file_path:
        return {"route": "analysis", "graph": data_analysis_graph, "file_path": file_path}

    # 🤖 LLM-based intent classification
    route = llm_route_classifier(user_input)
    print(f"🧭 LLM Router → Chose workflow: {route}")

    if route == "realtime":
        return {"route": "realtime", "graph": realtime_graph, "input": user_input}
    elif route == "analysis":
        return {"route": "analysis", "graph": data_analysis_graph, "file_path": file_path}
    else:
        return {"route": "research", "graph": research_graph, "input": user_input}


async def execute_subgraph(input_value: dict):
    """Invoke the selected subgraph asynchronously and collect results."""
    graph = input_value.get("graph")
    if not graph:
        raise ValueError("No graph provided for execution.")

    # Prepare state
    if input_value.get("file_path"):
        state_data = {"file_path": input_value["file_path"]}
    elif input_value.get("input"):
        state_data = input_value["input"]
    else:
        raise ValueError("No valid input provided for graph execution.")

    final_state = {}
    print("\n--- Executing Subgraph ---\n")

    # ✅ Use async streaming (works for LangGraph astream)
    async for event in graph.astream(state_data):
        node = list(event.keys())[0]
        node_output = event[node]

        print(f"[{node.upper()}] → {list(node_output.keys())}")
        final_state.update(node_output)

    print("\n--- Subgraph Execution Complete ---\n")

    # ✅ Normalize return structure
    normalized = {
        "status": final_state.get("status"),
        "report": final_state.get("report"),
        "message": final_state.get("message"),
        "summary": final_state.get("summary"),
        "charts": final_state.get("charts", {}),
    }

    # ✅ Log charts if present
    if normalized["charts"]:
        print("\nGenerated Charts:")
        for name, path in normalized["charts"].items():
            print(f" - {name}: {path}")

    return {"result": normalized}

# --- General Manager Graph ---
graph = StateGraph(dict)
graph.add_node("router", route_request)
graph.add_node("executor", execute_subgraph)  # this is now async
graph.add_edge("router", "executor")
graph.add_edge("executor", END)
graph.set_entry_point("router")

general_manager_graph = graph.compile()
