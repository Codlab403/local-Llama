from ..db import meta
from ..embeddings import adapter
from ..storage import fs_store
from ..vectorstore import get_default_store
import uuid
from typing import List
import datetime
import math


MAX_ATTEMPTS = 3


def _chunk_text(text: str, chunk_size: int = 200, overlap: int = 50):
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i : i + chunk_size]
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def process_task(task_id: str):
    task = meta.get_task(task_id)
    if not task:
        return
    meta.update_task_status(task_id, "indexing")
    upload_path = task.get("upload_path")
    if not upload_path:
        # fallback: try to find the file in the default uploads directory by filename
        filename = task.get("filename")
        if not filename:
            attempts = meta.increment_attempts(task_id)
            if attempts >= MAX_ATTEMPTS:
                meta.update_task_status(task_id, "error")
                meta.set_last_error(task_id, "missing filename for upload and unable to resolve path")
            else:
                # schedule next retry using exponential backoff (UTC aware)
                delay = int(math.pow(2, attempts))
                next_ts = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=delay)).isoformat()
                meta.set_next_retry(task_id, next_ts)
                meta.update_task_status(task_id, "queued")
            return
        try:
            candidate = fs_store.BASE_UPLOAD_DIR / filename
            if not candidate.exists():
                attempts = meta.increment_attempts(task_id)
                if attempts >= MAX_ATTEMPTS:
                    meta.update_task_status(task_id, "error")
                    meta.set_last_error(task_id, f"upload file not found: {candidate}")
                else:
                    delay = int(math.pow(2, attempts))
                    next_ts = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=delay)).isoformat()
                    meta.set_next_retry(task_id, next_ts)
                    meta.update_task_status(task_id, "queued")
                return
            upload_path = str(candidate)
        except Exception:
            attempts = meta.increment_attempts(task_id)
            if attempts >= MAX_ATTEMPTS:
                meta.update_task_status(task_id, "error")
                meta.set_last_error(task_id, "exception while resolving upload path")
            else:
                delay = int(math.pow(2, attempts))
                next_ts = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=delay)).isoformat()
                meta.set_next_retry(task_id, next_ts)
                meta.update_task_status(task_id, "queued")
            return

    try:
        with open(upload_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception as e:
        # increment attempts and possibly requeue with backoff; record final error message when exhausted
        attempts = meta.increment_attempts(task_id)
        if attempts >= MAX_ATTEMPTS:
            meta.update_task_status(task_id, "error")
            meta.set_last_error(task_id, str(e))
        else:
            delay = int(math.pow(2, attempts))
            next_ts = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=delay)).isoformat()
            meta.set_next_retry(task_id, next_ts)
            meta.update_task_status(task_id, "queued")
        return

    chunks = _chunk_text(text)
    store = get_default_store()
    for idx, chunk in enumerate(chunks, start=1):
        emb = adapter.embed_text(chunk)
        node_id = f"{task_id}-{idx}"
        metadata = {"doc_id": task_id, "page": idx, "snippet": chunk[:200]}
        store.add(node_id, emb, metadata)

    meta.update_task_status(task_id, "ready")


def poll_and_process_once() -> List[str]:
    """Find queued tasks and attempt to process them once.

    Returns list of processed task_ids.
    """
    conn = meta.get_conn()
    cur = conn.cursor()
    # only select tasks whose next_retry_at is NULL or <= now
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cur.execute(
        "SELECT task_id FROM ingest_tasks WHERE status = 'queued' AND (next_retry_at IS NULL OR next_retry_at <= ?)",
        (now_iso,),
    )
    rows = cur.fetchall()
    conn.close()
    processed = []
    for (tid,) in rows:
        process_task(tid)
        processed.append(tid)
    return processed
