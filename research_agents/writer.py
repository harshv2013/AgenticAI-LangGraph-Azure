import os
from services.azure_client import chat_completion


def compose_report(state: dict) -> dict:
    user_prompt = state["user_prompt"]
    summary = state["synthesis"]["summary"]

    # Fallback: simple report if no API key
    if not os.getenv("OPENAI_API_KEY"):
        report = f"# Research Report\n\nTopic: {user_prompt}\n\n{summary}\n"
        state["report"] = report
        return state

    # LLM-powered report
    messages = [
        {"role": "system", "content": "You are a research assistant. Write a clear, factual, well-structured research report."},
        {"role": "user", "content": f"Topic: {user_prompt}\n\nHere are the synthesized notes:\n{summary}\n\nWrite a structured report with sections and analysis."}
    ]

    report = chat_completion(messages, max_tokens=800)
    state["report"] = report
    return state
