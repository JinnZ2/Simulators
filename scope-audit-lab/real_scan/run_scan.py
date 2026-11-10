#!/usr/bin/env python3
"""SAL-WO3: the first real-data scan, run as pre-registered in
PREREGISTRATION.md (committed before this script existed).

Series: commits per calendar day in this repository's own history, at the
pinned commit, zero days included. Procedures: the delivered lab 0.3,
unmodified. Records are written to stream.jsonl in the lab's own record
format; nothing is interpreted.

    python3 run_scan.py            build the series, run, write stream.jsonl, print the reading
    python3 run_scan.py --check    rebuild and compare to the committed stream (no write)
"""
import json
import math
import statistics
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent / "lab_0_3"
sys.path.insert(0, str(LAB))
sys.path.insert(0, str(HERE.parent))

from scope_audit_lab.transitions import Case, scan_transitions  # noqa: E402
from scope_audit_lab.experiments import (threshold_sweep, order_permutation_probe,  # noqa: E402
                                         coupling_scan, make_experiment_record)
import null_expectation as ne  # noqa: E402

PIN_PREFIX = "5e75eb6"
PIN_FULL = "5e75eb6e74a74046049af9bc01fc94d42f0bcd9b"
STREAM = HERE / "stream.jsonl"
SERIES = HERE / "series.json"


def git(*args):
    return subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True, check=True).stdout


def build_series():
    if git("rev-parse", "--is-shallow-repository").strip() != "false":
        raise SystemExit("shallow clone: history incomplete, run `git fetch --unshallow` first")
    full = git("rev-parse", PIN_PREFIX).strip()
    if full != PIN_FULL:
        raise SystemExit(f"pin resolves to {full}, pre-registration says {PIN_FULL}")
    days = git("log", "--format=%cs", PIN_FULL).split()
    counts = {}
    for d in days:
        counts[d] = counts.get(d, 0) + 1
    first, last = date.fromisoformat(min(counts)), date.fromisoformat(max(counts))
    series = []
    d = first
    while d <= last:
        series.append({"day": d.isoformat(), "commits": counts.get(d.isoformat(), 0),
                       "weekday": d.isoweekday()})
        d += timedelta(days=1)
    return {"pin": PIN_FULL, "commits": len(days), "series": series}


def cases(series):
    return [Case(f"day_{s['day']}", float(i), float(s["commits"]), "day_index", "commits",
                 ("real: git history, commit date per day",)) for i, s in enumerate(series)]


def run(data):
    s = data["series"]
    cs = cases(s)
    scan = scan_transitions(cs, threshold=10.0, threshold_kind="absolute",
                            scan_label="real_daily_commits_t10")
    sweep = threshold_sweep(cs, thresholds=[5.0, 10.0, 20.0, 40.0], sweep_label="real_sweep")
    perm = order_permutation_probe(cs, n_permutations=25, threshold=10.0, seed=3,
                                   probe_label="real_permute")
    couple = coupling_scan([{"case_id": c.case_id, "factor_a": c.factor_value,
                             "factor_b": float(x["weekday"]), "output": c.output_value}
                            for c, x in zip(cs, s)],
                           threshold=10.0, factor_a_label="day_index",
                           factor_b_label="iso_weekday", output_label="commits",
                           coupling_label="real_couple")
    vals = [x["commits"] for x in s]
    mu, sd = statistics.fmean(vals), statistics.pstdev(vals)
    exp, state = ne.from_generator("normal", {"mean": mu, "sd": sd}, 10.0, len(vals))
    return scan, sweep, perm, couple, (mu, sd, exp, state)


def records(results):
    scan, sweep, perm, couple, _ = results
    out = [{"schema_version": "0.2", "record_type": "transition_scan",
            "record_id": "transition_scan_real_t10", "created_utc": None, "payload": scan}]
    for i, p in enumerate((sweep, perm, couple)):
        r = make_experiment_record(p).to_dict()
        r["record_id"] = f"experiment_real_{i}"
        r["created_utc"] = None
        out.append(r)
    return out


def reading(data, results):
    scan, sweep, perm, couple, (mu, sd, exp, state) = results
    s = data["series"]
    n_reg = len(scan["candidate_regions"])
    given = {tuple(sorted(r["between"])) for r in scan["candidate_regions"]}
    perm_only = [a for a in perm["region_appearances"]
                 if tuple(sorted(a["between_pair_unordered"])) not in given]
    cr = couple["coincidence_record"]
    zero_days = sum(1 for x in s if x["commits"] == 0)
    perm_counts = [sc["candidate_region_count"] for sc in perm["scans"]
                   if sc["order_kind"] == "seeded_permutation"]
    perm_mean = statistics.fmean(perm_counts)
    perm_lo, perm_hi = min(perm_counts), max(perm_counts)
    lines = [
        "scope-audit-lab / real_scan / run_scan.py", "=" * 64,
        f"series: {len(s)} days, {data['commits']} commits at pin {data['pin'][:12]}, "
        f"{zero_days} zero days (measured)",
        f"mean {mu:.2f} commits/day, sd {sd:.2f}, max {max(x['commits'] for x in s)}",
        "",
        f"1. scan at threshold 10: {n_reg} candidate regions over {len(s) - 1} adjacent pairs",
        f"2. sweep 5/10/20/40: " + ", ".join(str(t["candidate_region_count"]) for t in sweep["per_threshold"]),
        f"3. permutation probe: {len(perm['region_appearances'])} distinct pairs over 26 scans; "
        f"{len(perm_only)} never occur in the given order",
        f"4. coupling (day index vs weekday): coincident {len(cr['coincident_pairs'])}, "
        f"A-only {len(cr['factor_a_only_pairs'])}, B-only {len(cr['factor_b_only_pairs'])}",
        f"5. null (independent normal days, the series' own mean and sd): expected {exp:.2f}  [{state}]",
        "",
        "against the pre-registration:",
        f"   P1 coupling A-only = B-only = 0: "
        f"{'HELD' if not cr['factor_a_only_pairs'] and not cr['factor_b_only_pairs'] else 'FAILED'}",
        f"   P2 observed differs from null: observed {n_reg}, expected {exp:.2f}, "
        f"difference {n_reg - exp:+.2f}. P2 stated no tolerance, so any difference holds it;",
        "      as written it could only fail on an exact tie, which makes it close to unfalsifiable.",
        f"   P3 permutation flags pairs absent from the given order: "
        f"{'HELD' if perm_only else 'FAILED'} ({len(perm_only)})",
        "",
        "NOT PRE-REGISTERED (added after the run, labelled as such):",
        f"   shuffled-order null from the probe's 25 permutations (same days, order destroyed):",
        f"   mean {perm_mean:.1f}, range {perm_lo}..{perm_hi}; the real order gives {n_reg},",
        f"   below all {len(perm_counts)} shuffles. The normal null's {exp:.1f} mostly measures that",
        "   generator's misfit to zero-heavy counts (it also admits negative days); the order-only",
        f"   part of the gap is {n_reg - perm_mean:+.1f}: active days come in runs.",
        "",
        "interpretation: unassigned. A candidate region is a day-to-day change of",
        "more than 10 commits. Nothing here reads the repository's activity as",
        "anything beyond that.",
    ]
    return "\n".join(lines)


def main():
    data = build_series()
    results = run(data)
    recs = records(results)
    body = "\n".join(json.dumps(r, sort_keys=True) for r in recs) + "\n"
    if "--check" in sys.argv[1:]:
        same = STREAM.read_text(encoding="utf-8") == body and \
            json.loads(SERIES.read_text(encoding="utf-8")) == data
        print("stream and series reproduce:", same)
        sys.exit(0 if same else 1)
    if "--selftest" in sys.argv[1:]:
        print("run_scan.py is a run; use --check to reproduce the committed stream")
        sys.exit(2)
    SERIES.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    STREAM.write_text(body, encoding="utf-8")
    print(reading(data, results))


if __name__ == "__main__":
    main()
