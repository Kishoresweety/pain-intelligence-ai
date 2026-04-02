from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from agents import *
from memory import retrieve_semantic_memory, store_semantic_memory

app = Flask(__name__)
CORS(app)

# ---------------- DB INIT ----------------
def init_db():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        category TEXT,
        emotion TEXT,
        cause TEXT,
        solution TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS semantic_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        embedding TEXT,
        category TEXT,
        solution TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    text = request.json['text']

    # 🔍 Retrieve semantic memory
    memory = retrieve_semantic_memory(text)

    # 🧠 Agents
    understanding = understanding_agent(text, memory)
    cause = root_cause_agent(text, understanding)
    solution = solution_agent(text, cause)

    # 💾 Store memory
    store_semantic_memory(text, understanding['category'], solution)

    # 💾 Save complaint
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO complaints (text, category, emotion, cause, solution)
        VALUES (?, ?, ?, ?, ?)
    """, (
        text,
        understanding.get('category'),
        understanding.get('emotion'),
        cause,
        solution
    ))
    conn.commit()
    conn.close()

    return jsonify({
        "understanding": understanding,
        "cause": cause,
        "solution": solution,
        "memory_used": memory
    })


@app.route('/insights')
def insights():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("SELECT text FROM complaints")
    rows = c.fetchall()
    conn.close()

    texts = [r[0] for r in rows]

    insights = insight_agent(texts)

    return jsonify({"insights": insights})


@app.route('/patterns')
def patterns():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()

    c.execute("""
        SELECT category, COUNT(*) as count
        FROM complaints
        GROUP BY category
        ORDER BY count DESC
        LIMIT 5
    """)

    rows = c.fetchall()
    conn.close()

    return jsonify(rows)


@app.route('/all')
def all_data():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("SELECT * FROM complaints ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()

    return jsonify(rows)


# ---------------- RUN ----------------
import os
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
