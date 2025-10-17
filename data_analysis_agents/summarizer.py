# data_analysis_agents/summarizer.py
from services.azure_client import chat_completion

def summarize(state):
    """
    state includes 'insights' list and maybe 'parsed' raw.
    Returns {'summary': '...'}
    """
    insights = state.get("insights") or []
    raw = state.get("parsed") or {}
    prompt = f"Write a concise executive summary (3-6 bullets) of these analysis insights:\n\n{insights}\n\nAlso mention any errors seen: {raw.get('error') or raw.get('raw_stdout','')[:1000]}"
    try:
        text = chat_completion(
            messages=[
                {"role":"system","content":"You are a concise analyst."},
                {"role":"user","content":prompt}
            ],
            max_tokens=300
        )
        return {"summary": text}
    except Exception as e:
        return {"summary": f"⚠️ Summarizer error: {e}"}

