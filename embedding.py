import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
def get_embedding(text):
    response = openai.Embedding.create(
        model="text-embedding-3-small",
        input=text
    )
    return response['data'][0]['embedding']
