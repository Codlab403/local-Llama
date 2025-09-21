from pathlib import Path
import sqlite3
import uuid
import datetime


DB_PATH = Path("C:/Users/Tcyber/Documents/PROJECTS/LlamaInde-Chatbot/data/metadata.db")


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS ingest_tasks (
        task_id TEXT PRIMARY KEY,
        filename TEXT,
        upload_path TEXT,
        status TEXT,
        created_at TEXT
    )
    """
    )
    # Ensure migration: add missing columns on older DBs.
    try:
        cur.execute("PRAGMA table_info('ingest_tasks')")
        cols = [r[1] for r in cur.fetchall()]
        if "upload_path" not in cols:
            cur.execute("ALTER TABLE ingest_tasks ADD COLUMN upload_path TEXT")
        if "attempts" not in cols:
            cur.execute("ALTER TABLE ingest_tasks ADD COLUMN attempts INTEGER DEFAULT 0")
        if "next_retry_at" not in cols:
            cur.execute("ALTER TABLE ingest_tasks ADD COLUMN next_retry_at TEXT")
        if "last_error" not in cols:
            cur.execute("ALTER TABLE ingest_tasks ADD COLUMN last_error TEXT")
        if "last_error_at" not in cols:
            cur.execute("ALTER TABLE ingest_tasks ADD COLUMN last_error_at TEXT")
    except Exception:
        # best-effort migration; ignore failures to avoid blocking startup in tests
        pass
    conn.commit()
    conn.close()


def create_task(filename: str, upload_path: str | None = None) -> str:
    task_id = str(uuid.uuid4())
    conn = get_conn()
    cur = conn.cursor()
    # Use timezone-aware UTC ISO timestamps for created_at so consumers can parse reliably
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        cur.execute(
            "INSERT INTO ingest_tasks (task_id, filename, upload_path, status, created_at, attempts, next_retry_at, last_error) VALUES (?, ?, ?, ?, ?, 0, NULL, NULL)",
            (task_id, filename, upload_path, "queued", created_at),
        )
    except sqlite3.OperationalError:
        # older schema without upload_path; fall back to original insert
        cur.execute(
            "INSERT INTO ingest_tasks (task_id, filename, status, created_at, attempts, next_retry_at, last_error) VALUES (?, ?, ?, ?, 0, NULL, NULL)",
            (task_id, filename, "queued", created_at),
        )
    conn.commit()
    conn.close()
    return task_id


def update_task_status(task_id: str, status: str) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE ingest_tasks SET status = ? WHERE task_id = ?", (status, task_id))
    conn.commit()
    conn.close()


def get_attempts(task_id: str) -> int:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT attempts FROM ingest_tasks WHERE task_id = ?", (task_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return 0
        return int(row[0] or 0)
    except sqlite3.OperationalError:
        conn.close()
        return 0


def set_next_retry(task_id: str, iso_timestamp: str | None) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE ingest_tasks SET next_retry_at = ? WHERE task_id = ?", (iso_timestamp, task_id))
    conn.commit()
    conn.close()


def get_next_retry(task_id: str) -> str | None:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT next_retry_at FROM ingest_tasks WHERE task_id = ?", (task_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return row[0]
    except sqlite3.OperationalError:
        conn.close()
        return None


def increment_attempts(task_id: str) -> int:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE ingest_tasks SET attempts = COALESCE(attempts,0) + 1 WHERE task_id = ?", (task_id,))
        conn.commit()
        cur.execute("SELECT attempts FROM ingest_tasks WHERE task_id = ?", (task_id,))
        row = cur.fetchone()
        conn.close()
        return int(row[0] or 0) if row else 0
    except sqlite3.OperationalError:
        conn.close()
        return 0


def set_last_error(task_id: str, message: str | None) -> None:
    conn = get_conn()
    cur = conn.cursor()
    # write the error message and a UTC timestamp for when it occurred
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat() if message is not None else None
    cur.execute("UPDATE ingest_tasks SET last_error = ?, last_error_at = ? WHERE task_id = ?", (message, ts, task_id))
    conn.commit()
    conn.close()


def get_last_error(task_id: str) -> str | None:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT last_error FROM ingest_tasks WHERE task_id = ?", (task_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return row[0]
    except sqlite3.OperationalError:
        conn.close()
        return None


def get_last_error_at(task_id: str) -> str | None:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT last_error_at FROM ingest_tasks WHERE task_id = ?", (task_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return row[0]
    except sqlite3.OperationalError:
        conn.close()
        return None


def get_task(task_id: str):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT task_id, filename, upload_path, status, created_at, attempts, next_retry_at, last_error, last_error_at FROM ingest_tasks WHERE task_id = ?",
            (task_id,),
        )
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return {
            "task_id": row[0],
            "filename": row[1],
            "upload_path": row[2],
            "status": row[3],
            "created_at": row[4],
            "attempts": row[5],
            "next_retry_at": row[6],
            "last_error": row[7],
            "last_error_at": row[8],
        }
    except sqlite3.OperationalError:
        # older schema without upload_path
        cur.execute("SELECT task_id, filename, status, created_at FROM ingest_tasks WHERE task_id = ?", (task_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return {"task_id": row[0], "filename": row[1], "upload_path": None, "status": row[2], "created_at": row[3], "attempts": 0, "next_retry_at": None, "last_error": None}
