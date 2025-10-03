import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load env variables
load_dotenv()

# Initialize client
azure_client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
    api_version=os.getenv("OPENAI_API_VERSION"),
)

DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")


def chat_completion(messages, max_tokens=500):
    """Wrapper to call Azure OpenAI Chat Completion"""
    response = azure_client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=messages,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
