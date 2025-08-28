import os, sqlite3, threading, json

_DB_LOCK = threading.Lock()
_DB_PATH = os.path.join(os.path.dirname(__file__), 'orchestrator.db')

_SCHEMA = [
    "CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, formation TEXT, description TEXT, assigned_to TEXT, status TEXT, results_json TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
    "CREATE INDEX IF NOT EXISTS idx_tasks_formation ON tasks(formation)"
]

def init_db():
    with _DB_LOCK:
        conn = sqlite3.connect(_DB_PATH)
        cur = conn.cursor()
        for stmt in _SCHEMA:
            cur.execute(stmt)
        conn.commit()
        conn.close()


def save_task(task, formation):
    with _DB_LOCK:
        conn = sqlite3.connect(_DB_PATH)
        cur = conn.cursor()
        cur.execute("REPLACE INTO tasks (id, formation, description, assigned_to, status, results_json) VALUES (?,?,?,?,?,?)",
                    (task.id, formation, task.description, task.assigned_to, task.status, json.dumps(task.results)))
        conn.commit()
        conn.close()


def load_tasks(formation):
    with _DB_LOCK:
        conn = sqlite3.connect(_DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, description, assigned_to, status, results_json FROM tasks WHERE formation=? ORDER BY created_at", (formation,))
        rows = cur.fetchall()
        conn.close()
    tasks = []
    for r in rows:
        tasks.append({
            'id': r[0],
            'description': r[1],
            'assigned_to': r[2],
            'status': r[3],
            'results': json.loads(r[4]) if r[4] else {}
        })
    return tasks
