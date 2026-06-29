from fastapi import FastAPI
from pydantic import BaseModel
from openai import AzureOpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=f"https://{os.getenv('OPENAI_SERVICE')}.openai.azure.com/"
)

deployment_name = os.getenv("OPENAI_CHAT_MODEL")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    return {
        "reply": response.choices[0].message.content
    }