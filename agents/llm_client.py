import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt: str, system: str = "You are a helpful assistant.", temperature: float = 0.1, max_tokens: int = 1000) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=30
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM Error: {e}")
        return None