# realtime_agents/query.py
from services.azure_client import azure_client, AZURE_OPENAI_DEPLOYMENT_NAME
import logging


async def query(state: dict):
    print("query state : ", state)
    logging.info(f"query state : {state}")
    """
    Extracts the actual query string from user input for real-time information retrieval.
    """
    user_input = state if isinstance(state, str) else state.get("input", "")
    # user_input = state.get("user_input", "")
    
    prompt = f"""
    You are an assistant that extracts the meaningful real-time search query
    from the following user input. The query should be concise and directly
    usable for search APIs like Tavily.

    Example:
    User: "What is the weather in Gorakhpur today?"
    Output: "weather in Gorakhpur today"

    User input: "{user_input}"

    Respond ONLY with the query text.
    """

    try:
        response = azure_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a query extractor for real-time data."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100,
        )
        extracted_query = response.choices[0].message.content.strip()
        return {"query": extracted_query}

    except Exception as e:
        print(f"⚠️ Realtime query error: {e}")
        return {"query": ""}
