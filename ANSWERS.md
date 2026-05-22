# ANSWERS.md

## 1. How to Run

Requirements: Python 3.8+

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

A `todos.db` SQLite file is created automatically on first run. All data persists between restarts.

---

## 2. Stack Choice

**Why Flask + SQLite?**

Flask is lightweight and has no boilerplate — a full REST API fits in one file. SQLite is built into Python's standard library, requires zero configuration, and stores all data in a single `todos.db` file. Together, they let me focus on features rather than infrastructure.

**A worse choice:** Django + PostgreSQL. Django is excellent for large apps but brings significant overhead (migrations, ORM, settings files, admin scaffolding) for a simple mini-app. PostgreSQL adds a server process dependency that makes "run on a fresh machine" much harder. SQLite gives true persistence with a single file and no server required.

---

## 3. One Real Edge Case

**File:** `app.py`, lines 44–47 (update route) and lines 60–63 (delete route)

Before updating or deleting a todo, the code checks whether the ID actually exists:

```python
existing = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
if not existing:
    conn.close()
    return jsonify({"error": "Todo not found"}), 404
```

**Without this handling:** SQLite's `UPDATE` and `DELETE` statements silently succeed even when no rows match — they return `rowcount = 0` but raise no error. The API would return a 200 OK response to the client for a completely non-existent ID, making it impossible for the frontend to know whether the operation actually did anything. With the check, the client receives a proper 404 and can handle it correctly (e.g., refresh the list if it's stale).

---

## 4. AI Usage

- **Tool:** Claude (claude.ai)
- **What I asked:** Scaffold a Flask REST API with SQLite for a todo app with priority and due date fields.
- **What it gave:** A working skeleton with routes for GET, POST, PUT, DELETE.
- **What I changed:** The original AI output used `conn.execute()` without checking whether a row existed before UPDATE/DELETE. I added the existence check (see edge case above) because returning 200 on a no-op is incorrect REST behaviour — a missing resource should return 404. I also changed the ordering of todos in the GET query (sorting by `done ASC, priority DESC`) to surface active high-priority items at the top, which the AI output did not include.

---

## 5. Honest Gap

**The gap:** There is no user authentication. Anyone who can reach `localhost:5000` can create, edit, or delete all todos. The app assumes a single user on a personal machine.

**What I'd do with another day:** Add a simple session-based login with a username and password stored as a bcrypt hash. Each todo would get a `user_id` foreign key, and all queries would filter by the logged-in user. This would make the app safe to deploy on a shared or networked machine.
