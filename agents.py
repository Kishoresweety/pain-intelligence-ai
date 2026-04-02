import os
from openai import OpenAI
import json

client = OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY")
def call_llm(prompt):
    response = client.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']


def understanding_agent(text, memory):
    prompt = f"""
    Similar past complaints:
    {memory}

    Analyze this complaint:
    "{text}"

    Return JSON:
    {{
      "intent": "",
      "category": "",
      "emotion": "",
      "keywords": []
    }}
    """
    return json.loads(call_llm(prompt))


def root_cause_agent(text, context):
    prompt = f"""
    Complaint: {text}
    Context: {context}

    What is the root cause?
    """
    return call_llm(prompt)


def solution_agent(text, cause):
    prompt = f"""
    Complaint: {text}
    Cause: {cause}

    Give:
    - Fix
    - Workaround
    - Prevention
    """
    return call_llm(prompt)


def insight_agent(texts):
    prompt = f"""
    Complaints:
    {texts}

    Return:
    - Top issues
    - Most common category
    - Urgency level
    """
    return call_llm(prompt)
