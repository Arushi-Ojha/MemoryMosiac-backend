import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print("DEBUG - OPENROUTER_API_KEY:", OPENROUTER_API_KEY)

async def generate_beautiful_story(description: str) -> str:
    headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "Memory Mosaic AI Journal"
}


    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a poetic AI journal assistant."},
            {"role": "user", "content": f"Turn this journal input into a beautiful story:\n\n{description}"}
        ]
    }

    print("DEBUG - Headers:", headers)
    print("DEBUG - Payload:", payload)

    async with httpx.AsyncClient() as client:
        response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
