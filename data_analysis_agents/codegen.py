# data_analysis_agents/codegen.py
import json
from services.azure_client import chat_completion  # ✅ use your Azure client wrapper

def generate_code(state):
    """
    Generate Python data analysis code for the given dataset.
    Works with Azure OpenAI and supports flexible state formats.
    """

    # 🧠 Extract intent safely
    intent_value = state.get("intent")
    if isinstance(intent_value, dict):
        intent = intent_value.get("intent", "")
        question = intent_value.get("question", "")
    else:
        intent = intent_value or ""
        question = state.get("question", "")

    # 🧾 Get dataset path from ingest or state root
    file_path = None
    if "ingest" in state and isinstance(state["ingest"], dict):
        file_path = state["ingest"].get("file_path")
    elif state.get("file_path"):
        file_path = state["file_path"]

    if not file_path:
        print("⚠️ Warning: No file_path found in state; defaulting to None.")
        file_path = "None"

    # 🪄 Build code generation prompt
    prompt = f"""
You are a Python data analysis agent.

Dataset path: {file_path}

User Intent: {intent}
User Question: {question}

Generate a **complete Python script** that:
1. Loads the dataset from this path.
2. Performs analysis and visualization including:
   - Histogram (first numeric column)
   - Revenue over time (if 'Date'/'Time' and 'Revenue' columns exist)
   - Profit by Region (if 'Region' and 'Profit' columns exist)
   - Revenue vs Profit scatter
3. Collects insights and chart filenames into a dict named `results`:
   {{
       "insights": [],
       "charts": [],
       "errors": []
   }}
4. Prints the JSON at the end using:
   print(json.dumps(results, indent=2))
5. Always include the matplotlib backend fix:
   matplotlib.use("Agg")
6. End the code cleanly — no incomplete try/except blocks.
"""

    # 🧠 Call Azure OpenAI via your helper
    messages = [{"role": "user", "content": prompt}]
    code = chat_completion(messages, max_tokens=2048).strip()

    # ✅ Pass forward both code + file path for executor
    return {"code": code, "file_path": file_path}
