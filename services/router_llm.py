# services/router_llm.py
from services.azure_client import azure_client, AZURE_OPENAI_DEPLOYMENT_NAME
import json

def llm_route_classifier(user_input: str):
    """
    Uses LLM to classify the request dynamically into one of:
      - research
      - realtime
      - analysis
    The LLM decides based purely on semantic context, not keywords.
    """

    prompt = f"""
    You are a routing decision model.
    Read the user input carefully and classify it into ONE of the following routes:

    - research → when the user asks for explanations, reasoning, conceptual info, or summaries.
    - realtime → when the user is asking for current, live, or time-sensitive data (e.g., today's weather, live scores, current events).
    - analysis → when the user wants data processing, file-based operations, or statistical/analytical computation.

    User input: "{user_input}"

    Respond ONLY in valid JSON:
    {{
        "route": "<research | realtime | analysis>"
    }}
    """

    try:
        response = azure_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You classify user intent for routing. Respond only in JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=30,
        )

        text = response.choices[0].message.content.strip()
        result = json.loads(text)
        return result.get("route", "research")

    except Exception as e:
        print(f"⚠️ Router LLM error: {e}")
        return "research"
