# data_analysis_agents/intent.py
def detect_intent(state):
    """
    state contains:
      - 'question' (string) optional
      - 'df' (pandas.DataFrame) from ingest
    Returns: {"intent": "summary"|"viz"|"code_run"|"explore", "question": "..."}
    """
    question = ""
    if isinstance(state, dict):
        question = state.get("question", "") or state.get("input", "")
    else:
        question = str(state or "")

    q_lower = question.lower().strip()

    # Simple heuristics — you can replace this with an LLM classifier if you want
    if not q_lower:
        return {"intent": "explore", "question": question}

    if any(w in q_lower for w in ["plot", "chart", "show", "visual", "bar", "line", "scatter"]):
        return {"intent": "viz", "question": question}

    if any(w in q_lower for w in ["run code", "execute code", "python", "script"]):
        return {"intent": "code_run", "question": question}

    # default to summary/analysis
    return {"intent": "summary", "question": question}
