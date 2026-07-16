#!/usr/bin/env python3
"""
run_all.py — top-level runner for fragility-cascade/.

Runs every module's __main__ demo in a subprocess (isolated imports,
bounded wall time), records exit code + duration + first & last non-empty
stdout line, prints a report card, and writes a machine-readable report
to samples/run_all_report.json.

Skips modules that are interactive by design (explorer.py) and this file
itself. Pass --json PATH to override the report location.

Usage:
    python3 run_all.py                  # default (samples/run_all_report.json)
    python3 run_all.py --timeout 30     # relax per-module wall-time cap
    python3 run_all.py --json /tmp/x.json

The tool is deliberately dumb: it does NOT check numbers against
CLAIM_TABLE. It just tells you which modules run, which crash, which
time out, and how long each takes — the smallest artifact that pins
today's audit state so tomorrow's can be diffed against it.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
import time
from datetime import datetime

# Modules that are interactive or otherwise not eligible for automated demo.
SKIP = frozenset({
    "run_all.py",           # this file
})

# Modules with a non-interactive smoke path invoked via extra CLI args.
SMOKE_ARGS = {
    "explorer.py": ["--smoke"],   # bypasses the interactive menu
}


def module_files(root: str) -> list:
    files = sorted(glob.glob(os.path.join(root, "*.py")))
    return [f for f in files if os.path.basename(f) not in SKIP]


def _first_last(text: str) -> tuple:
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ("", "")
    return (lines[0][:120], lines[-1][:120])


def run_one(path: str, timeout: float) -> dict:
    """Run one module's __main__. Return a normalised result dict."""
    started = time.perf_counter()
    verdict = "OK"
    exit_code = 0
    stdout = ""
    stderr = ""
    extra = SMOKE_ARGS.get(os.path.basename(path), [])
    try:
        proc = subprocess.run(
            [sys.executable, path, *extra],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.path.dirname(path) or ".",
        )
        exit_code = proc.returncode
        stdout = proc.stdout
        stderr = proc.stderr
        if exit_code != 0:
            verdict = "ERROR"
    except subprocess.TimeoutExpired as e:
        verdict = "TIMEOUT"
        exit_code = -1
        stdout = e.stdout.decode(errors="replace") if e.stdout else ""
        stderr = e.stderr.decode(errors="replace") if e.stderr else ""
    dt = time.perf_counter() - started

    first, last = _first_last(stdout)
    # if we crashed, the failure lives in stderr
    err_first, err_last = _first_last(stderr)
    return {
        "module": os.path.basename(path),
        "verdict": verdict,
        "exit_code": exit_code,
        "seconds": round(dt, 3),
        "stdout_first": first,
        "stdout_last": last,
        "stderr_first": err_first,
        "stderr_last": err_last,
    }


def _table_row(r: dict) -> str:
    mod = r["module"][:38]
    verdict = r["verdict"]
    secs = f"{r['seconds']:.2f}s"
    last = r["stdout_last"] if r["verdict"] != "ERROR" else r["stderr_last"]
    last = (last or "")[:60]
    return f"  {mod:<38} {verdict:<8} {secs:>7}  {last}"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    p.add_argument("--timeout", type=float, default=15.0,
                   help="per-module wall-time cap in seconds (default 15)")
    p.add_argument("--json", default=None,
                   help="path to write the JSON report "
                        "(default: <root>/samples/run_all_report.json)")
    p.add_argument("--root", default=os.path.dirname(os.path.abspath(__file__)),
                   help="directory of modules to run")
    args = p.parse_args(argv)
    if args.json is None:
        args.json = os.path.join(args.root, "samples", "run_all_report.json")

    files = module_files(args.root)
    print("=" * 78)
    print(f"fragility-cascade — run_all  ({len(files)} modules, timeout {args.timeout:.0f}s)")
    print("=" * 78)
    header = f"  {'module':<38} {'verdict':<8} {'wall':>7}  last stdout line"
    print(header)
    print("  " + "-" * (len(header) - 2))

    results = []
    for path in files:
        r = run_one(path, timeout=args.timeout)
        results.append(r)
        print(_table_row(r))

    counts = {"OK": 0, "ERROR": 0, "TIMEOUT": 0}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print("\n" + "=" * 78)
    print(f"SUMMARY: {counts['OK']} OK, {counts['ERROR']} error, {counts['TIMEOUT']} timeout, "
          f"{len(SKIP) - 1} skipped ({', '.join(sorted(SKIP - {'run_all.py'}))})")
    print("=" * 78)

    report = {
        "run_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "timeout_seconds": args.timeout,
        "n_modules": len(results),
        "skipped": sorted(SKIP - {"run_all.py"}),
        "counts": counts,
        "results": results,
    }
    try:
        os.makedirs(os.path.dirname(args.json) or ".", exist_ok=True)
        with open(args.json, "w") as f:
            json.dump(report, f, indent=2)
        print(f"report -> {args.json}")
    except OSError as e:
        print(f"could not write report ({e})", file=sys.stderr)

    # exit code = number of non-OK modules, capped at 255
    return min(counts["ERROR"] + counts["TIMEOUT"], 255)


if __name__ == "__main__":
    sys.exit(main())
