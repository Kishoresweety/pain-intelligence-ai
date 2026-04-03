from ai_router import get_embedding
'''
import os

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


import os
from openai import OpenAI

client = OpenAI()

client.api_key = os.getenv("OPENAI_API_KEY")
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response['data'][0]['embedding']
'''
