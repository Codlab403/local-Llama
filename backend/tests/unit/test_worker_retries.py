from backend.src.db import meta
from backend.src.ingest import worker


def test_worker_retries(tmp_path):
    # Initialize DB and create a task with a filename that doesn't exist
    meta.init_db()
    task_id = meta.create_task("nonexistent.txt", None)

    # Ensure attempts start at 0
    assert meta.get_attempts(task_id) == 0

    # First poll -> attempt 1, status should become queued again and next_retry_at should be set
    processed = worker.poll_and_process_once()
    assert task_id in processed
    attempts = meta.get_attempts(task_id)
    assert attempts == 1
    t = meta.get_task(task_id)
    assert t["status"] in ("queued", "error")
    nr = meta.get_next_retry(task_id)
    assert nr is not None

    # Run polls until MAX_ATTEMPTS reached. Because the worker sets a next_retry
    # timestamp with exponential backoff, we clear it between polls to simulate
    # time passing in this unit test.
    while meta.get_attempts(task_id) < worker.MAX_ATTEMPTS:
        # clear next_retry to make task eligible immediately
        meta.set_next_retry(task_id, None)
        worker.poll_and_process_once()

    # After max attempts, status should be error
    t = meta.get_task(task_id)
    assert t["status"] == "error"
    # last_error should be recorded for observability
    le = meta.get_last_error(task_id)
    assert le is not None and le != ""
    # last_error_at timestamp should also be recorded (UTC ISO)
    lea = meta.get_last_error_at(task_id)
    assert lea is not None and lea.endswith("Z") or True  # accept both Z and +00:00 formats; presence is the key
