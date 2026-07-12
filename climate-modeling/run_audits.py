"""Entry point: run every registered audit and print a report card."""

import json
import sys
from audits.audit_registry import BUILT_AUDITS, FRONTIER_AUDITS, ALL_AUDITS


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
