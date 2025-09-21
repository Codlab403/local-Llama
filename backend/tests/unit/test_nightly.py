from backend.src.eval import nightly


def test_register_job_and_sample():
    res = nightly.register_job(nightly.sample_evaluation, schedule="@daily")
    assert isinstance(res, dict)
    assert res["name"] == "sample_evaluation"
    out = nightly.sample_evaluation()
    assert out.get("ok") is True
from backend.src.eval.nightly import run_nightly_evaluation


def test_run_nightly_evaluation_returns_report():
    report = run_nightly_evaluation()
    assert isinstance(report, dict)
    assert "evaluated" in report and "metrics" in report
