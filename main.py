import asyncio
import os
from workflows.general_manager_graph import general_manager_graph

async def run_manager(prompt=None, file_path=None):
    """
    Runs the unified general manager that routes to:
    - research_graph (for text prompts)
    - data_analysis_graph (for CSV files)
    - realtime_graph (for live queries)
    """
    state = {"input": prompt, "file_path": file_path}
    final_output = None

    async for update in general_manager_graph.astream(state):
        node = list(update.keys())[0]
        data = update[node]

        # 🧠 Research Workflow
        if node == "executor" and isinstance(data, dict):
            if "report" in data.get("result", {}):
                final_output = data["result"]["report"]
            elif "message" in data.get("result", {}):
                final_output = data["result"]["message"]

            # 📊 Data Analysis (with charts)
            charts = data["result"].get("charts", {})
            if charts:
                print("\n📊 Charts generated:")
                for k, v in charts.items():
                    print(f" - {k}: {v}")
                    if os.path.exists(v):
                        print(f"✅ Saved: {os.path.abspath(v)}")

        print(update)

    # Print or return final outcome
    if final_output:
        print("\n\n=== FINAL OUTPUT ===\n")
        print(final_output)
    else:
        print("\n⚠️ No final report or message generated.")


if __name__ == "__main__":
    # 🧠 Research Workflow
    # asyncio.run(run_manager(prompt="Impact of AI on healthcare"))

    # 📊 Data Analysis
    # asyncio.run(run_manager(file_path="sales_data.csv"))

    # 🌍 Realtime
    # asyncio.run(run_manager(prompt="What's the weather in Delhi?"))
    # asyncio.run(run_manager(prompt="aaj ka mausam kaisa hai in Gorakhpur"))
    asyncio.run(run_manager(prompt="What is new framework of Agentic AI in October 2025"))

    

    
