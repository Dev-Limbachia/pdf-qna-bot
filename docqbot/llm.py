# llm.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Initialize Groq client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"  # Important for Groq
)

def query_local_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="gemma2-9b-it",  # You asked for this model
            messages=[
                {"role": "system", "content": "You are a helpful document assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"
