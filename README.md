# Taskr — Persistent Todo Web App

A Flask-based todo app with SQLite persistence. Create, view, update, and delete tasks — they survive restarts.

## How to Run

**Requirements:** Python 3.8+

```bash
# 1. Clone / download the repo
# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in browser
http://127.0.0.1:5000
```

That's it. A `todos.db` SQLite file is created automatically on first run.

## Features

- ✅ Create, read, update, delete todos
- 🔴 Priority levels (High / Medium / Low)
- 📅 Due dates with overdue highlighting
- 🔍 Filter by status, priority, or overdue
- 💾 Persistent storage via SQLite (survives restarts)

## Stack

- **Backend:** Python + Flask
- **Database:** SQLite (via built-in `sqlite3`)
- **Frontend:** Plain HTML/CSS/JS (no frameworks)
