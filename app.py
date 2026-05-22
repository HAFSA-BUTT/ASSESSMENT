from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = "todos.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            priority TEXT NOT NULL DEFAULT 'medium',
            due_date TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/todos", methods=["GET"])
def get_todos():
    conn = get_db()
    todos = conn.execute(
        "SELECT * FROM todos ORDER BY done ASC, priority DESC, created_at DESC"
    ).fetchall()
    conn.close()
    return jsonify([dict(t) for t in todos])


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Text is required"}), 400
    priority = data.get("priority", "medium")
    due_date = data.get("due_date") or None
    created_at = datetime.now().isoformat()
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO todos (text, priority, due_date, created_at) VALUES (?, ?, ?, ?)",
        (text, priority, due_date, created_at)
    )
    conn.commit()
    new_id = cursor.lastrowid
    todo = conn.execute("SELECT * FROM todos WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return jsonify(dict(todo)), 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    conn = get_db()
    # Edge case: check if todo exists before updating
    existing = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Todo not found"}), 404
    text = data.get("text", existing["text"]).strip()
    if not text:
        conn.close()
        return jsonify({"error": "Text cannot be empty"}), 400
    done = data.get("done", existing["done"])
    priority = data.get("priority", existing["priority"])
    due_date = data.get("due_date", existing["due_date"])
    conn.execute(
        "UPDATE todos SET text=?, done=?, priority=?, due_date=? WHERE id=?",
        (text, done, priority, due_date, todo_id)
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    conn.close()
    return jsonify(dict(updated))


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_db()
    # Edge case: check if todo exists before deleting
    existing = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({"error": "Todo not found"}), 404
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return jsonify({"deleted": todo_id})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
