"""Nightly evaluation job skeleton.

Provides a register_job function that can be wired into a scheduler.
"""
from typing import Callable, Optional


def register_job(job_func: Callable, schedule: Optional[str] = "@daily") -> dict:
    """Register a job with a simple metadata contract.

    Args:
        job_func: callable to execute
        schedule: cron-like schedule string (informational)

    Returns:
        dict describing registration
    """
    # In future, integrate with background scheduler (APScheduler / RQ / Celery)
    return {"name": getattr(job_func, "__name__", "job"), "schedule": schedule}


def sample_evaluation():
    """A tiny placeholder evaluation function."""
    # Example: compute recall@k against a small gold set
    return {"ok": True}
"""Nightly evaluation skeleton for Local-first RAG.

This module provides a simple entrypoint that can be scheduled (e.g., via
cron, Windows Task Scheduler, or a job runner) to run nightly evaluations
against a small gold Q/A set.

The implementation is intentionally minimal and returns a report dict that
can later be wired into observability or GitHub Actions.
"""
from typing import Dict, Any
import logging

logger = logging.getLogger("llamainde.eval")


def run_nightly_evaluation() -> Dict[str, Any]:
    """Run a small evaluation and return a report.

    For now this is a stub that returns an empty/placeholder report. Replace
    or extend this with retrieval, generation, and metrics calculation.
    """
    logger.info("Starting nightly evaluation (stub)")
    report: Dict[str, Any] = {"evaluated": 0, "metrics": {}}
    logger.info("Finished nightly evaluation")
    return report


if __name__ == "__main__":
    print(run_nightly_evaluation())
