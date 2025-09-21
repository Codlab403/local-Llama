import time

from backend.src.db import meta
from backend.src.ingest import scheduler


def test_scheduler_processes_queued_task():
    meta.init_db()
    task_id = meta.create_task("nonexistent2.txt", None)
    sched = scheduler.Scheduler(interval=0.1)
    try:
        sched.start()
        # wait a short time for scheduler to process
        time.sleep(0.6)
    finally:
        sched.stop()

    attempts = meta.get_attempts(task_id)
    assert attempts > 0
