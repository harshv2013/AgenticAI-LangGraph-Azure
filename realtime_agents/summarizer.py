# realtime_agents/summarizer.py
from services.azure_client import azure_client,AZURE_OPENAI_DEPLOYMENT_NAME

def summarizer(data: dict):
    try:
        content = str(data)
        response = azure_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,  # ✅ use your .env deployment
            messages=[
                {"role": "system", "content": "You are a concise real-time data summarization assistant."},
                {"role": "user", "content": f"Summarize this realtime data: {content}"}
            ]
        )
        summary = response.choices[0].message.content
        return {"summary": summary}

    except Exception as e:
        return {"summary": f"⚠️ Azure OpenAI error: {e}"}

