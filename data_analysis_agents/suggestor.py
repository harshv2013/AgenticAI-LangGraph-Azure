# data_analysis_agents/suggestor.py
from services.azure_client import chat_completion

def suggest(state):
    insights = state.get("insights") or []
    prompt = f"Given these insights: {insights}\nSuggest 3 follow-up analytical questions a user could ask about this dataset."
    try:
        text = chat_completion(
            messages=[
                {"role":"system","content":"You are a helpful analyst that suggests follow-ups."},
                {"role":"user","content":prompt}
            ],
            max_tokens=200
        )
        # return as plain text; you could parse into list
        return {"suggestions": text}
    except Exception as e:
        return {"suggestions": f"⚠️ Suggestor error: {e}"}
