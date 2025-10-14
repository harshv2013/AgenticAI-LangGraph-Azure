# services/tavily_client.py
import os
from tavily import TavilyClient

from dotenv import load_dotenv
load_dotenv(override=True)

# Load API Key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("Missing TAVILY_API_KEY in environment variables.")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
