import json
from ai_router import call_ai


def understanding_agent(text, memory):
    prompt = f"""
    Similar past complaints:
    {memory}

    Analyze this complaint:
    "{text}"

    Return ONLY valid JSON:
    {{
      "intent": "",
      "category": "",
      "emotion": "",
      "keywords": []
    }}
    """

    try:
        return json.loads(call_ai(prompt))
    except:
        return {
            "intent": "unknown",
            "category": "general",
            "emotion": "neutral",
            "keywords": []
        }


def root_cause_agent(text, context):
    prompt = f"""
    Complaint: {text}
    Context: {context}

    What is the root cause?
    """
    return call_ai(prompt)


def solution_agent(text, cause):
    prompt = f"""
    Complaint: {text}
    Cause: {cause}

    Provide:
    - Fix
    - Workaround
    - Prevention
    """
    return call_ai(prompt)


def insight_agent(texts):
    prompt = f"""
    Complaints:
    {texts}

    Return:
    - Top issues
    - Most common category
    - Urgency level
    """
    return call_ai(prompt)
