#!/usr/bin/env python3
"""SAL-WO1: the closed-form null expectation for a thresholded adjacent-delta scan.

The lab's null_baseline_scan runs the transition engine on seeded noise and
records how many candidate regions it flags. For an absolute threshold that
count has a closed form, so it is a known answer rather than a figure:

    adjacent pairs           n - 1
    P(|X_i+1 - X_i| > th)    uniform(w):  (1 - th/w)^2   for 0 <= th <= w, else 0
                             normal(sd):  erfc(th / (2 sd))
    expected flags           (n - 1) * P

The expectation is exact. The SPREAD across replications is not binomial,
because adjacent pairs share a case and are dependent; this module states
the mean only and does not supply a variance it has not derived.

States kept apart:
    a number                the expectation exists and was computed
    NOT_DERIVED  (reason)   the scan's kind has no closed form here (relative
                            thresholds: a ratio of noise values)
    None                    the inputs carry no denominator (fewer than two
                            cases, or a non-positive width or sd)

    python3 null_expectation.py              read the lab's shipped null record
    python3 null_expectation.py RECORD.jsonl read the first null record in a file

The module refuses --selftest; checks live in test_null_expectation.py.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_STREAM = HERE / "lab_0_3" / "experiments_demo.jsonl"


def p_exceed_uniform(width, threshold):
    """P(|U1 - U2| > threshold) for two independent uniforms of the given width."""
    if width is None or width <= 0 or threshold < 0:
        return None
    if threshold >= width:
        return 0.0
    return (1 - threshold / width) ** 2


def p_exceed_normal(sd, threshold):
    """P(|X1 - X2| > threshold) for two independent N(mu, sd^2); the
    difference is N(0, 2 sd^2), so the tail is erfc(th / (2 sd))."""
    if sd is None or sd <= 0 or threshold < 0:
        return None
    return math.erfc(threshold / (2 * sd))


def expected_flags(n_cases, p):
    if n_cases is None or n_cases < 2 or p is None:
        return None
    return (n_cases - 1) * p


def from_generator(distribution, parameters, threshold, n_cases, threshold_kind="absolute"):
    """Expectation for a lab-style generator description. Returns
    (value_or_None, state) where state is 'COMPUTED', 'NOT_DERIVED: ...'
    or 'NO_DENOMINATOR'."""
    if threshold_kind != "absolute":
        return None, "NOT_DERIVED: relative threshold is a ratio of noise values; no closed form here"
    if distribution == "uniform":
        p = p_exceed_uniform(parameters.get("high", 0) - parameters.get("low", 0), threshold)
    elif distribution == "normal":
        p = p_exceed_normal(parameters.get("sd"), threshold)
    else:
        return None, f"NOT_DERIVED: unknown distribution {distribution!r}"
    e = expected_flags(n_cases, p)
    return (e, "COMPUTED") if e is not None else (None, "NO_DENOMINATOR")


def read_null_record(record):
    """Expectation beside the recorded counts of one null_baseline_scan record."""
    p = record.get("payload", record)
    g = p["generator"]
    sc = p["scan_config"]
    s = p["recorded_summary"]
    e, state = from_generator(g["distribution"], g["parameters"], sc["threshold"],
                              s["cases_per_replication"], sc["threshold_kind"])
    return {
        "distribution": g["distribution"],
        "parameters": g["parameters"],
        "threshold": sc["threshold"],
        "n_cases": s["cases_per_replication"],
        "replications": s["replications"],
        "recorded_mean": s["mean_candidate_regions"],
        "recorded_range": (s["min_candidate_regions"], s["max_candidate_regions"]),
        "expected": e,
        "state": state,
        "gap": None if e is None else s["mean_candidate_regions"] - e,
    }


def first_null_record(path):
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("payload", r).get("experiment_kind") == "null_baseline_scan":
            return r
    return None


def render(path=DEFAULT_STREAM):
    r = first_null_record(path)
    if r is None:
        return f"no null_baseline_scan record in {path}"
    x = read_null_record(r)
    lines = [
        "scope-audit-lab / null_expectation.py",
        "=" * 60,
        f"stream: {Path(path).name}",
        f"generator: {x['distribution']} {x['parameters']}",
        f"threshold {x['threshold']:g} (absolute), {x['n_cases']} cases, {x['replications']} replications",
        f"recorded: mean {x['recorded_mean']:.2f}, range {x['recorded_range'][0]}..{x['recorded_range'][1]}",
    ]
    if x["expected"] is None:
        lines.append(f"expected: {x['state']}")
    else:
        lines += [
            f"expected: (n-1) * P = {x['expected']:.4f}   [{x['state']}]",
            f"recorded - expected: {x['gap']:+.4f}",
            "reading: the null count is a property of the generator's width against",
            "the threshold. A real scan's count is read against this expectation,",
            "not against zero and not against the demo figure.",
        ]
    lines.append("spread across replications: not derived (adjacent pairs are dependent)")
    return "\n".join(lines)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("null_expectation.py is a library; run: python3 test_null_expectation.py")
        sys.exit(2)
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    print(render(args[0] if args else DEFAULT_STREAM))
