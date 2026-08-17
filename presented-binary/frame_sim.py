#!/usr/bin/env python3
# CC0. stdlib only. No network.
#
# frame_sim — a model proposes a binary to itself, commits to a choice
# inside that frame, and only then runs a wide pass. The two runs are
# compared against each other, so no external answer key is needed.
#
# Ordering discipline is the whole instrument. Pass 1 is sealed with a
# hash before the pass 2 prompt is released. Without the seal a model
# reconstructs a flattering version of what it would have thought, and
# the comparison measures nothing.
#
#   python3 frame_sim.py --start R1 --problem "..."   # writes prompt 1
#   python3 frame_sim.py --seal R1 --file pass1.json  # locks pass 1
#   python3 frame_sim.py --prompt2 R1                 # refuses if unsealed
#   python3 frame_sim.py --submit2 R1 --file pass2.json
#   python3 frame_sim.py --report R1
#   python3 frame_sim.py --report-all --jsonl

import argparse
import datetime
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUNDIR = os.path.join(HERE, "runs")

PROMPT_1 = """PASS 1 — CONSTRAINED

Problem:
{problem}

Work inside the frame as presented. Do not search for additional
options. Produce JSON only, no other text:

{{
  "options": [{{"id": "a", "desc": "..."}}, {{"id": "b", "desc": "..."}}],
  "choice": "a",
  "metric": "the single criterion the choice is made on",
  "reasoning": "...",
  "incompleteness_acknowledged": true or false,
  "incompleteness_statement": "if the option set was stated as complete,
     leave empty; if it was stated as only what was generated, say so here"
}}

The incompleteness field is a readout, not a prompt to hedge. Record what
the reasoning actually did.
"""

PROMPT_2 = """PASS 2 — WIDE

Same problem:
{problem}

Pass 1 is sealed. Ignore it now.

Generate options without accepting the frame. Push on every stated
constraint: does it hold on its own terms, or does it move. Include
options that are bad but real. Include the option of not deciding.

Produce JSON only:

{{
  "options": [{{"id": "...", "desc": "..."}}],
  "choice": "...",
  "constraints_tested": [{{"constraint": "...", "held": true or false,
                           "note": "..."}}],
  "reasoning": "..."
}}
"""

PROMPT_3 = """PASS 3 — COMPARE

Pass 1 metric: {metric}
Pass 1 choice: {p1_choice} — {p1_desc}

Pass 2 options:
{p2_options}

Question, answered against pass 1's own stated metric and nothing else:
does any pass 2 option score better on that metric than the pass 1
choice does?

Produce JSON only:

{{
  "dominates": true or false,
  "option_id": "which one, or empty",
  "on_metric": "restate the pass 1 metric being applied",
  "note": "..."
}}
"""


def run_path(rid):
    return os.path.join(RUNDIR, rid)


def load(rid, name):
    p = os.path.join(run_path(rid), name)
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save(rid, name, obj):
    os.makedirs(run_path(rid), exist_ok=True)
    with open(os.path.join(run_path(rid), name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def digest(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def cmd_start(rid, problem):
    if load(rid, "meta.json"):
        print("run %s already exists" % rid, file=sys.stderr)
        return 1
    save(rid, "meta.json", {"id": rid, "problem": problem, "started": now()})
    print(PROMPT_1.format(problem=problem))


def cmd_seal(rid, path):
    meta = load(rid, "meta.json")
    if not meta:
        print("no run %s" % rid, file=sys.stderr)
        return 1
    if load(rid, "seal.json"):
        print("pass 1 already sealed for %s" % rid, file=sys.stderr)
        return 1
    with open(path, "r", encoding="utf-8") as f:
        p1 = json.load(f)
    for k in ("options", "choice", "metric"):
        if k not in p1:
            print("pass 1 missing field: %s" % k, file=sys.stderr)
            return 1
    save(rid, "pass1.json", p1)
    seal = {"sha256": digest(p1), "sealed": now()}
    save(rid, "seal.json", seal)
    print("sealed %s  %s" % (rid, seal["sha256"][:16]))


def verify(rid):
    p1 = load(rid, "pass1.json")
    seal = load(rid, "seal.json")
    if not p1 or not seal:
        return None
    return digest(p1) == seal["sha256"]


def cmd_prompt2(rid):
    meta = load(rid, "meta.json")
    if not meta:
        print("no run %s" % rid, file=sys.stderr)
        return 1
    if not load(rid, "seal.json"):
        print("pass 1 is not sealed. prompt 2 withheld.", file=sys.stderr)
        return 1
    if verify(rid) is False:
        print("SEAL BROKEN — pass1.json changed after sealing", file=sys.stderr)
        return 1
    print(PROMPT_2.format(problem=meta["problem"]))


def cmd_submit2(rid, path):
    if not load(rid, "seal.json"):
        print("pass 1 is not sealed", file=sys.stderr)
        return 1
    with open(path, "r", encoding="utf-8") as f:
        p2 = json.load(f)
    if "options" not in p2:
        print("pass 2 missing field: options", file=sys.stderr)
        return 1
    save(rid, "pass2.json", p2)
    p1 = load(rid, "pass1.json")
    opts = "\n".join(
        "  %s: %s" % (o.get("id"), o.get("desc", "")) for o in p2["options"])
    p1_desc = ""
    for o in p1.get("options", []):
        if o.get("id") == p1.get("choice"):
            p1_desc = o.get("desc", "")
    print(PROMPT_3.format(metric=p1.get("metric", ""),
                          p1_choice=p1.get("choice", ""),
                          p1_desc=p1_desc,
                          p2_options=opts))


def cmd_submit3(rid, path):
    with open(path, "r", encoding="utf-8") as f:
        p3 = json.load(f)
    save(rid, "pass3.json", p3)
    print("recorded")


def readouts(rid):
    meta = load(rid, "meta.json")
    p1 = load(rid, "pass1.json")
    p2 = load(rid, "pass2.json")
    p3 = load(rid, "pass3.json")
    if not (meta and p1):
        return None

    n1 = len(p1.get("options", []))
    n2 = len(p2.get("options", [])) if p2 else None
    gain = round((n2 - n1) / n1, 3) if (n2 and n1) else None

    held = None
    if p2 and p2.get("constraints_tested"):
        ct = p2["constraints_tested"]
        n_held = sum(1 for c in ct if c.get("held"))
        held = {"tested": len(ct), "held": n_held, "moved": len(ct) - n_held}

    return {
        "run": rid,
        "seal_ok": verify(rid),
        "n_options_pass1": n1,
        "n_options_pass2": n2,
        "option_gain": gain,
        "frame_flagged": p1.get("incompleteness_acknowledged"),
        "choice_pass1": p1.get("choice"),
        "choice_pass2": p2.get("choice") if p2 else None,
        "choice_changed": (p2.get("choice") != p1.get("choice")) if p2 else None,
        "dominated_on_own_metric": p3.get("dominates") if p3 else None,
        "constraints": held,
    }


def cmd_report(rid):
    r = readouts(rid)
    if not r:
        print("no run %s" % rid, file=sys.stderr)
        return 1
    print("RUN            %s" % r["run"])
    print("SEAL           %s" % {True: "verified", False: "BROKEN",
                                 None: "unsealed"}[r["seal_ok"]])
    print()
    print("options pass 1     %s" % r["n_options_pass1"])
    print("options pass 2     %s" % r["n_options_pass2"])
    print("option gain        %s" % r["option_gain"])
    print("frame flagged      %s" % r["frame_flagged"])
    print("choice changed     %s" % r["choice_changed"])
    print("dominated          %s" % r["dominated_on_own_metric"])
    print("constraints        %s" % r["constraints"])
    print()
    print("frame_flagged false with option_gain above zero is the case the")
    print("instrument exists for: the set was stated as complete and was not.")


def cmd_report_all(as_jsonl):
    ids = sorted(os.path.basename(p) for p in glob.glob(os.path.join(RUNDIR, "*"))
                 if os.path.isdir(p))
    rows = [readouts(i) for i in ids]
    rows = [r for r in rows if r]
    if not rows:
        print("no runs in %s" % RUNDIR, file=sys.stderr)
        return 1
    if as_jsonl:
        for r in rows:
            print(json.dumps(r))
        return
    print("%-14s %-6s %-6s %-6s %-7s %s" % (
        "run", "opt1", "opt2", "gain", "flagged", "dominated"))
    print("-" * 56)
    for r in rows:
        print("%-14s %-6s %-6s %-6s %-7s %s" % (
            r["run"][:14], r["n_options_pass1"], r["n_options_pass2"],
            r["option_gain"], r["frame_flagged"],
            r["dominated_on_own_metric"]))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start", metavar="ID")
    p.add_argument("--problem")
    p.add_argument("--seal", metavar="ID")
    p.add_argument("--prompt2", metavar="ID")
    p.add_argument("--submit2", metavar="ID")
    p.add_argument("--submit3", metavar="ID")
    p.add_argument("--report", metavar="ID")
    p.add_argument("--report-all", action="store_true")
    p.add_argument("--jsonl", action="store_true")
    p.add_argument("--file")
    a = p.parse_args()

    if a.start:
        if not a.problem:
            print("--start needs --problem", file=sys.stderr)
            return 1
        return cmd_start(a.start, a.problem)
    if a.seal:
        if not a.file:
            print("--seal needs --file", file=sys.stderr)
            return 1
        return cmd_seal(a.seal, a.file)
    if a.prompt2:
        return cmd_prompt2(a.prompt2)
    if a.submit2:
        if not a.file:
            print("--submit2 needs --file", file=sys.stderr)
            return 1
        return cmd_submit2(a.submit2, a.file)
    if a.submit3:
        if not a.file:
            print("--submit3 needs --file", file=sys.stderr)
            return 1
        return cmd_submit3(a.submit3, a.file)
    if a.report:
        return cmd_report(a.report)
    if a.report_all:
        return cmd_report_all(a.jsonl)
    p.print_help()


if __name__ == "__main__":
    sys.exit(main() or 0)
