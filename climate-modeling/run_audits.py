"""Entry point: run every registered audit and print a report card.

Also exports `AUDIT_REGISTRY` (name -> audit instance) and
`run_single_audit(name, model_instance=None)` — the interface the AI-patching
loop in `meta_experiments.py` calls to run one audit on a specific model."""

import json
import sys
from audits.audit_registry import BUILT_AUDITS, FRONTIER_AUDITS, ALL_AUDITS


AUDIT_REGISTRY = {type(a).__name__: a for a in ALL_AUDITS}


def run_single_audit(audit_name, model_instance=None):
    """Run one named audit and return a normalised result dict.

    If `model_instance` is given, temporarily replaces the audit's
    `generate_audited_model` so the caller-supplied model is what's audited
    (this is how the AI-patching loop tests each round's patched model).
    """
    if audit_name not in AUDIT_REGISTRY:
        raise KeyError(f"unknown audit '{audit_name}'. "
                       f"Known: {sorted(AUDIT_REGISTRY)}")
    audit = AUDIT_REGISTRY[audit_name]
    original = audit.generate_audited_model
    try:
        if model_instance is not None:
            audit.generate_audited_model = lambda: model_instance
        try:
            raw = audit.run()
        except NotImplementedError as e:
            raw = {"audit_name": audit_name, "failure_detected": None,
                   "metrics": {"status": "FRONTIER_STUB", "reason": str(e)},
                   "true_final": None, "audited_final": None}
    finally:
        audit.generate_audited_model = original
    # normalise into the schema the patching loop expects
    fd = raw.get("failure_detected")
    passed = fd is False
    status = "STUB" if fd is None else ("PASS" if passed else "FAIL")
    return {
        "name": audit_name,
        "status": status,
        "passed": passed,
        "failure_detected": fd,
        "metrics": raw.get("metrics", {}),
        "true_final": raw.get("true_final"),
        "audited_final": raw.get("audited_final"),
    }


def _fmt(value):
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "PASS" if not value else "FAIL"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def run_all(report_path="samples/audit_report.json"):
    print("=" * 72)
    print(f"CLIMATE MODELING AUDIT SUITE — {len(BUILT_AUDITS)} built, "
          f"{len(FRONTIER_AUDITS)} frontier stubs")
    print("=" * 72)
    results = []
    print(f"\n{'audit':<32} {'verdict':<10} {'metric':<30}")
    print("-" * 72)
    for audit in ALL_AUDITS:
        try:
            r = audit.run()
        except NotImplementedError as e:
            r = {"audit_name": audit.name, "failure_detected": None,
                 "metrics": {"status": "FRONTIER_STUB", "reason": str(e)},
                 "true_final": None, "audited_final": None}
        results.append(r)
        fd = r.get("failure_detected")
        verdict = "STUB" if fd is None else ("FAIL" if fd else "PASS")
        first_metric = next(iter(r.get("metrics", {}).items()), ("", ""))
        detail = f"{first_metric[0]}={_fmt(first_metric[1])}" if first_metric[0] else ""
        print(f"{r['audit_name']:<32} {verdict:<10} {detail:<30}")

    n_built_fail = sum(1 for r in results if r.get("failure_detected") is True)
    n_built_pass = sum(1 for r in results if r.get("failure_detected") is False)
    n_stub = sum(1 for r in results if r.get("failure_detected") is None)
    print("\n" + "=" * 72)
    print(f"SUMMARY: {n_built_pass} pass, {n_built_fail} fail, {n_stub} stub")
    print("=" * 72)

    if report_path:
        try:
            with open(report_path, "w") as f:
                json.dump(results, f, indent=2, default=str)
            print(f"report saved -> {report_path}")
        except OSError as e:
            print(f"could not save report ({e})", file=sys.stderr)

    return results


if __name__ == "__main__":
    run_all()
