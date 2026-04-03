import os
from openai import OpenAI
from groq import Groq

# Clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- CHAT ----------------
def call_ai(prompt):
    provider = os.getenv("AI_PROVIDER", "groq")  # default groq

    # 🔹 Try Groq first
    if provider == "groq":
        try:
            response = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print("⚠️ Groq failed, switching to OpenAI:", e)

    # 🔹 Fallback to OpenAI
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ---------------- EMBEDDING ----------------
def get_embedding(text):
    provider = os.getenv("AI_PROVIDER", "openai")

    # Groq DOES NOT support embeddings → always use OpenAI
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
def smart_response(memory):
    if memory and memory[0]['score'] > 0.85:
        return memory[0]['solution']
        
    return response.data[0].embedding
