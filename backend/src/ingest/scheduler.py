import threading
import time
import random
from typing import Callable

from . import worker


class Scheduler:
    def __init__(self, interval: float = 5.0):
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread = None

    def _loop(self):
        while not self._stop_event.is_set():
            try:
                worker.poll_and_process_once()
            except Exception:
                # swallow errors to keep scheduler alive
                pass
            # add a small jitter to avoid tight loops
            time.sleep(self.interval + random.random())

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self, timeout: float = 5.0):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=timeout)


_default_scheduler: Scheduler | None = None


def get_default_scheduler() -> Scheduler:
    global _default_scheduler
    if _default_scheduler is None:
        _default_scheduler = Scheduler()
    return _default_scheduler
