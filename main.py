# import asyncio
# import os
# from workflows.general_manager_graph import general_manager_graph

# async def run_manager(prompt=None, file_path=None):
#     """
#     Runs the unified general manager that routes to:
#     - research_graph (for text prompts)
#     - data_analysis_graph (for CSV files)
#     - realtime_graph (for live queries)
#     """
#     state = {"input": prompt, "file_path": file_path}
#     final_output = None

#     async for update in general_manager_graph.astream(state):
#         node = list(update.keys())[0]
#         data = update[node]

#         # 🧠 Research Workflow
#         if node == "executor" and isinstance(data, dict):
#             if "report" in data.get("result", {}):
#                 final_output = data["result"]["report"]
#             elif "message" in data.get("result", {}):
#                 final_output = data["result"]["message"]

#             # 📊 Data Analysis (with charts)
#             charts = data["result"].get("charts", {})
#             if charts:
#                 print("\n📊 Charts generated:")
#                 for k, v in charts.items():
#                     print(f" - {k}: {v}")
#                     if os.path.exists(v):
#                         print(f"✅ Saved: {os.path.abspath(v)}")

#         print(update)

#     # Print or return final outcome
#     if final_output:
#         print("\n\n=== FINAL OUTPUT ===\n")
#         print(final_output)
#     else:
#         print("\n⚠️ No final report or message generated.")


# if __name__ == "__main__":
#     # 🧠 Research Workflow
#     # asyncio.run(run_manager(prompt="Impact of AI on healthcare"))

#     # 📊 Data Analysis
#     # asyncio.run(run_manager(file_path="sales_data.csv"))

#     # 🌍 Realtime
#     # asyncio.run(run_manager(prompt="What's the weather in Delhi?"))
#     # asyncio.run(run_manager(prompt="aaj ka mausam kaisa hai in Gorakhpur"))
#     asyncio.run(run_manager(prompt="What is new framework of Agentic AI in October 2025"))

    

    


# # quick test runner (add to your main.py or a new test file)
# import asyncio
# from workflows.data_analysis_graph import data_analysis_graph

# async def run_analysis(file_path, question=""):
#     state = {"file_path": file_path, "question": question}
#     # stream results for debugging
#     async for st in data_analysis_graph.astream(state):
#         print(st)

# if __name__ == "__main__":
#     asyncio.run(run_analysis("sales_data.csv", "Show me revenue over time and a scatter of revenue vs profit"))


import asyncio
import os
import sys
import inspect
from workflows.general_manager_graph import general_manager_graph
from workflows.data_analysis_graph import data_analysis_graph

# Optional: add colorized logging for clarity
def log(stage: str, msg: str):
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m",
    }
    color = colors.get(stage.upper(), colors["INFO"])
    print(f"{color}[{stage.upper()}] {msg}{colors['RESET']}")


async def run_manager(prompt=None, file_path=None):
    """
    Runs unified manager routing between:
    - research_graph  (text prompt)
    - data_analysis_graph (CSV)
    - realtime_graph  (live lookup)
    """

    # Decide which workflow to use
    if file_path and os.path.exists(file_path):
        log("INFO", f"📊 Detected CSV file → routing to data_analysis_graph")
        graph = data_analysis_graph
        state = {"file_path": file_path, "question": prompt or ""}
    else:
        log("INFO", f"🧠 Detected text query → routing to general_manager_graph")
        graph = general_manager_graph
        state = {"input": prompt, "file_path": None}

    final_output = None
    charts = {}

    # Run selected graph asynchronously
    async for update in graph.astream(state):
        node = list(update.keys())[0]
        data = update[node]

        # --- Debug Print Node Transitions ---
        log("INFO", f"➡️  Node completed: {node}")

        # --- Handle Data Analysis Outputs ---
        if graph is data_analysis_graph:
            if node == "executor" and isinstance(data, dict):
                charts = data.get("charts", {})
                if charts:
                    log("SUCCESS", f"Generated {len(charts)} chart(s):")
                    for k, v in charts.items():
                        log("INFO", f"   {k}: {os.path.abspath(v)}")

            elif node == "report" and isinstance(data, dict):
                report_text = data.get("report") or data.get("summary")
                if report_text:
                    final_output = report_text

        # --- Handle Research / General Outputs ---
        elif graph is general_manager_graph:
            if node == "executor" and isinstance(data, dict):
                result = data.get("result", {})
                final_output = (
                    result.get("report")
                    or result.get("message")
                    or result.get("summary")
                )

        # Print each update if you want full trace
        # print(update)

    # --- Final Output Display ---
    print("\n" + "=" * 70)
    if final_output:
        log("SUCCESS", "🎯 FINAL OUTPUT:")
        print(final_output)
    else:
        log("WARNING", "⚠️ No final report or message generated.")

    if charts:
        print("\n📊 Charts saved at:")
        for name, path in charts.items():
            print(f" - {name}: {path}")


if __name__ == "__main__":
    # Example use cases

    # 🧠 Research Workflow
    # asyncio.run(run_manager(prompt="Impact of AI on healthcare"))

    # 📊 Data Analysis
    asyncio.run(run_manager(file_path="sales_data.csv", prompt="Show me revenue over time and a scatter of revenue vs profit"))

    # 🌍 Realtime Query
    # asyncio.run(run_manager(prompt="What’s the weather in Delhi?"))
