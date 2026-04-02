import sqlite3
import json
from embedding import get_embedding
from similarity import cosine_similarity


def retrieve_semantic_memory(text):
    query_embedding = get_embedding(text)

    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("SELECT text, embedding, category, solution FROM semantic_memory")
    rows = c.fetchall()
    conn.close()

    matches = []

    for row in rows:
        emb = json.loads(row[1])
        score = cosine_similarity(query_embedding, emb)

        if score > 0.75:
            matches.append({
                "text": row[0],
                "category": row[2],
                "solution": row[3],
                "score": score
            })

    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[:3]


def store_semantic_memory(text, category, solution):
    embedding = get_embedding(text)

    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()

    c.execute("""
        INSERT INTO semantic_memory (text, embedding, category, solution)
        VALUES (?, ?, ?, ?)
    """, (
        text,
        json.dumps(embedding),
        category,
        solution
    ))

    conn.commit()
    conn.close()
