"""End-to-end CLI tests via subprocess."""
import json
import os
import subprocess
import sys

CMD = [sys.executable, "-m", "fourd_municipal_engine.cli"]

SAMPLE_TEXT = (
    "We are thrilled to announce the critical realignment of our workforce. "
    "The optimization of resources was executed immediately!"
)

ORDINANCE_TEXT = (
    "Purpose: to reduce traffic congestion near intersections.\n"
    "\n"
    "Section 1. Pursuant to Section 8.2, the applicant shall pay a fee of "
    "$150.00 and $0.25 per square foot. The city shall reduce congestion by "
    "10% no later than June 30, 2027 and issue an annual report."
)


def _run(args):
    # The subprocess needs the package on its path. Without this the
    # tests pass only where `pip install -e .` has been run and fail on
    # a bare checkout -- which is every other test directory's baseline
    # in this repository, and the state a reported count is taken in.
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env = dict(os.environ)
    env["PYTHONPATH"] = root + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        CMD + args, capture_output=True, text=True, timeout=60, env=env
    )


def test_cli_human_report_corporate_pr():
    proc = _run([SAMPLE_TEXT, "--genre", "corporate_pr"])
    assert proc.returncode == 0, proc.stderr
    assert "4D Language Lens Report" in proc.stdout
    assert "Corporate PR" in proc.stdout
    assert "Manipulation index:" in proc.stdout
    assert "Trace:" in proc.stdout


def test_cli_json_deep_analysis():
    proc = _run(
        [
            ORDINANCE_TEXT,
            "--genre",
            "legal_contract",
            "--citation",
            "Section 8.2",
            "--deep-analysis",
            "--json",
        ]
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["genre"] == "legal_contract"
    sig = payload["lens_signature"]
    assert 0.0 <= sig["manipulation_index"] <= 1.0
    assert sig["trace"]

    translation = payload["translation"]
    assert translation["section_citation"] == "Section 8.2"
    assert "must" in translation["plain_english_summary"]
    assert translation["fees"]
    assert translation["root_causes"]
    assert translation["stated_intent"]
    assert translation["interconnected_regulations"]
    assert translation["audit_metrics"]
    assert 0.0 < translation["auditability_score"] <= 1.0
    assert translation["lens_signature"]["manipulation_index"] == sig[
        "manipulation_index"
    ]


def test_cli_deep_analysis_human_report():
    proc = _run([ORDINANCE_TEXT, "--deep-analysis", "--citation", "Section 8.2"])
    assert proc.returncode == 0, proc.stderr
    assert "Deep Analysis" in proc.stdout
    assert "Section 8.2" in proc.stdout
    assert "Auditability score:" in proc.stdout


def test_cli_requires_input():
    proc = _run([])
    assert proc.returncode != 0
