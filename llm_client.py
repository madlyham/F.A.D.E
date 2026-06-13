import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# --- 1. GROQ CLIENT ---
groq_client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# === THE FIRING FUNCTIONS ===

def query_groq(prompt, model="llama-3.3-70b-versatile"):
    try:
        res = groq_client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e: return f"[ERROR] Groq: {e}"

def query_gemini(prompt, model="gemini-3.5-flash"):
    # Talking directly to Google's raw REST API for maximum stability
    api_key = os.environ.get("GEMINI_API_KEY")
    
    clean_model = model.replace("models/", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model}:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        data = response.json()
        if "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"[ERROR] Gemini format mismatch: {data}"
    except Exception as e: 
        return f"[ERROR] Gemini Connection: {e}"