from openai import AzureOpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent / ".env"

load_dotenv(dotenv_path=env_path)

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=(
        f"https://{os.getenv('OPENAI_SERVICE')}"
        ".openai.azure.com/"
    )
)

deployment_name = os.getenv(
    "OPENAI_CHAT_MODEL"
)