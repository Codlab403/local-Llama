"""Simple migration runner for backend SQLite metadata DB.
This will apply SQL files found in the migrations/ directory in lexical order.
It is intentionally minimal and safe for local dev. For production use a proper migration tool.
"""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).parent
DB_PATH = ROOT.parent / "data" / "metadata.db"
MIGRATIONS_DIR = ROOT


def applied_migrations_table_exists(conn: sqlite3.Connection) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='applied_migrations'")
    return cur.fetchone() is not None


def ensure_applied_table(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS applied_migrations (
        id TEXT PRIMARY KEY,
        applied_at TEXT
    )
    """
    )
    conn.commit()


def get_applied(conn: sqlite3.Connection) -> set:
    cur = conn.cursor()
    cur.execute("SELECT id FROM applied_migrations")
    rows = cur.fetchall()
    return set(r[0] for r in rows)


def apply_migration(conn: sqlite3.Connection, path: Path):
    sql = path.read_text(encoding="utf-8")
    cur = conn.cursor()
    try:
        # Split into statements and apply carefully. This avoids running ALTERs when base table missing.
        stmts = [s.strip() for s in sql.split(';') if s.strip()]
        for s in stmts:
            low = s.lower()
            if low.startswith('alter table') and 'add column' in low:
                # parse column name
                # naive parse: ALTER TABLE ingest_tasks ADD COLUMN col_name TYPE
                parts = s.split()
                try:
                    col_idx = parts.index('COLUMN') + 1
                    col_name = parts[col_idx].strip()
                except Exception:
                    # fallback: execute safely
                    cur.execute(s)
                    continue
                # check if column exists
                cur.execute("PRAGMA table_info('ingest_tasks')")
                cols = [r[1] for r in cur.fetchall()]
                if col_name in cols:
                    print(f"skipping column {col_name} (already exists)")
                    continue
                else:
                    cur.execute(s)
            else:
                cur.execute(s)
        cur.execute("INSERT INTO applied_migrations (id, applied_at) VALUES (?, datetime('now'))", (path.name,))
        conn.commit()
        print(f"applied {path.name}")
    except Exception as e:
        conn.rollback()
        print(f"failed applying {path.name}: {e}")
        raise


def run():
    # If the app's meta module is available, use its DB_PATH so we migrate the same DB
    try:
        import importlib

        meta_mod = importlib.import_module("backend.src.db.meta")
        # use the DB_PATH used by the application
        app_db = Path(str(meta_mod.DB_PATH))
        db_path_to_use = app_db
    except Exception:
        db_path_to_use = DB_PATH

    db_path_to_use.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path_to_use))
    # Ensure base table exists. If backend.src.db.meta is importable, call its init_db helper to ensure schema
    try:
        meta_mod.init_db()
    except Exception:
        # fallback: create a minimal ingest_tasks table if it doesn't exist in this DB
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
        conn.commit()
    ensure_applied_table(conn)
    applied = get_applied(conn)
    sqls = sorted(p for p in MIGRATIONS_DIR.iterdir() if p.suffix == ".sql")
    for sql in sqls:
        if sql.name in applied:
            continue
        # Guard: only run ALTER if column does not exist
        if "ALTER TABLE ingest_tasks ADD COLUMN last_error" in sql.read_text():
            # Check if column exists
            cur = conn.cursor()
            cur.execute("PRAGMA table_info('ingest_tasks')")
            cols = [r[1] for r in cur.fetchall()]
            if "last_error" in cols and "last_error_at" in cols:
                print(f"skipping {sql.name} - columns already exist")
                cur.execute("INSERT INTO applied_migrations (id, applied_at) VALUES (?, datetime('now'))", (sql.name,))
                conn.commit()
                continue
        apply_migration(conn, sql)
    conn.close()


if __name__ == "__main__":
    run()
