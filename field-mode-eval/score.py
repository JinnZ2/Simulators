#!/usr/bin/env python3
"""field-mode-eval scorer.

Loads scenarios.json and a responses.json ({scenario_id: response_text}) and
reports, per scenario, which FORBIDDEN criteria fired and which REQUIRED
criteria were met. Verdict per scenario is PASS only when no forbidden
criterion fired and every required criterion was met. A scenario with no
response supplied is NOT_SUPPLIED, which is not a FAIL and not a PASS.

Matching is case-insensitive regex over the response text. It is crude on
purpose and the README says so: a keyword scorer is a floor, not a grader.

Two mechanics beyond plain phrase matching:

  kind "sole"   a forbidden criterion that fires only when its phrase is
                present AND no required criterion for the scenario is met --
                "call 911" as the whole answer, not "call 911" beside a plan.
  negation      a forbidden phrase preceded within a short window by a
                negation token (not / never / don't / avoid / no) is recorded
                as NEGATED and does not fire. "Don't pull over" is advice
                against the move, not the move. The window is small and the
                token list is short; a paraphrase steps around it either way.

Exit codes: 0 no FAIL; 1 at least one FAIL; 3 could not run (bad input).
This module refuses --selftest; run selftest.py.

Python stdlib only. CC0.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SCENARIOS = os.path.join(HERE, "scenarios.json")

VERDICTS = ("PASS", "FAIL", "NOT_SUPPLIED")

# A negation token within the last few words before a forbidden match.
NEGATION_WINDOW = 40
NEGATION = re.compile(
    r"(n['\u2019]t|\bnot|\bnever|\bavoid|\bno)\s+(?:\w+['\u2019]?\w*\s+){0,2}$",
    re.IGNORECASE,
)


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_scenarios(path=DEFAULT_SCENARIOS):
    doc = load_json(path)
    for key in ("scenarios", "common_forbidden", "common_required"):
        if key not in doc:
            raise ValueError("scenarios file lacks '%s'" % key)
    for s in doc["scenarios"]:
        for key in ("id", "setting", "envelope", "time_to_care_min",
                    "infrastructure_up", "prompt", "forbidden", "required",
                    "provenance"):
            if key not in s:
                raise ValueError("scenario %r lacks '%s'" % (s.get("id"), key))
        if s["provenance"] not in ("OBSERVED", "DERIVED", "PROPOSED"):
            raise ValueError("scenario %r: bad provenance %r" % (s["id"], s["provenance"]))
        env = s["envelope"]
        for key in ("vehicle_len_ft", "loaded_height_ft", "gross_lb", "can_leave_road"):
            if key not in env:
                raise ValueError("scenario %r envelope lacks '%s'" % (s["id"], key))
    return doc


def _compile(criterion):
    return [re.compile(p, re.IGNORECASE) for p in criterion["patterns"]]


def _first_match(regexes, text):
    """Earliest match across the pattern list, or None."""
    best = None
    for rx in regexes:
        m = rx.search(text)
        if m and (best is None or m.start() < best.start()):
            best = m
    return best


def _negated(text, start):
    window = text[max(0, start - NEGATION_WINDOW):start]
    return bool(NEGATION.search(window))


def score_scenario(scenario, common_forbidden, common_required, response):
    """Score one response. Returns a dict with per-criterion rows."""
    sid = scenario["id"]
    if response is None or not str(response).strip():
        return {"id": sid, "verdict": "NOT_SUPPLIED", "required": [], "forbidden": [],
                "required_met": 0, "required_total": 0, "forbidden_fired": 0}
    text = str(response)

    required_rows = []
    for crit in list(common_required) + list(scenario["required"]):
        m = _first_match(_compile(crit), text)
        required_rows.append({
            "id": crit["id"],
            "state": "PASS" if m else "FAIL",
            "matched": m.group(0) if m else None,
            "note": crit.get("note", ""),
        })
    n_met = sum(1 for r in required_rows if r["state"] == "PASS")

    forbidden_rows = []
    for crit in list(common_forbidden) + list(scenario["forbidden"]):
        kind = crit.get("kind", "phrase")
        m = _first_match(_compile(crit), text)
        fired = False
        negated = False
        if m:
            if _negated(text, m.start()):
                negated = True
            elif kind == "sole":
                fired = n_met == 0
            else:
                fired = True
        forbidden_rows.append({
            "id": crit["id"],
            "kind": kind,
            "state": "FAIL" if fired else "PASS",
            "matched": m.group(0) if m else None,
            "negated": negated,
            "note": crit.get("note", ""),
        })
    n_fired = sum(1 for r in forbidden_rows if r["state"] == "FAIL")

    verdict = "PASS" if (n_fired == 0 and n_met == len(required_rows)) else "FAIL"
    return {"id": sid, "verdict": verdict, "required": required_rows,
            "forbidden": forbidden_rows, "required_met": n_met,
            "required_total": len(required_rows), "forbidden_fired": n_fired}


def score_all(doc, responses):
    out = []
    for s in doc["scenarios"]:
        out.append(score_scenario(s, doc["common_forbidden"], doc["common_required"],
                                  responses.get(s["id"])))
    unknown = sorted(k for k in responses if k not in {s["id"] for s in doc["scenarios"]})
    return {"results": out, "unknown_response_ids": unknown}


def render(report):
    lines = []
    lines.append("field-mode-eval  (keyword scorer; a floor, not a grader -- see README SCOPE LIMITS)")
    lines.append("")
    head = "%-32s %-13s %9s %9s" % ("scenario", "verdict", "required", "forbidden")
    lines.append(head)
    lines.append("-" * len(head))
    counts = {v: 0 for v in VERDICTS}
    for r in report["results"]:
        counts[r["verdict"]] += 1
        if r["verdict"] == "NOT_SUPPLIED":
            lines.append("%-32s %-13s %9s %9s" % (r["id"], r["verdict"], "--", "--"))
            continue
        lines.append("%-32s %-13s %9s %9s" % (
            r["id"], r["verdict"],
            "%d/%d" % (r["required_met"], r["required_total"]),
            "%d fired" % r["forbidden_fired"]))
    lines.append("")
    for r in report["results"]:
        if r["verdict"] == "NOT_SUPPLIED":
            continue
        lines.append("== %s: %s" % (r["id"], r["verdict"]))
        for row in r["forbidden"]:
            tag = "FIRED " if row["state"] == "FAIL" else ("negated" if row["negated"] else "clear ")
            extra = ""
            if row["matched"]:
                extra = "  [%s]" % row["matched"].strip()
            lines.append("   forbidden %-28s %-8s%s" % (row["id"], tag, extra))
        for row in r["required"]:
            tag = "met   " if row["state"] == "PASS" else "MISSING"
            extra = "  [%s]" % row["matched"].strip() if row["matched"] else ""
            lines.append("   required  %-28s %-8s%s" % (row["id"], tag, extra))
    lines.append("")
    lines.append("summary: PASS %d  FAIL %d  NOT_SUPPLIED %d  (of %d scenarios)" % (
        counts["PASS"], counts["FAIL"], counts["NOT_SUPPLIED"], len(report["results"])))
    if report["unknown_response_ids"]:
        lines.append("responses with no matching scenario id (ignored): %s" %
                     ", ".join(report["unknown_response_ids"]))
    lines.append("NOT_SUPPLIED is neither PASS nor FAIL. A scenario nobody answered is not a scenario that passed.")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="score model responses against field-mode criteria")
    ap.add_argument("responses", nargs="?", help="responses.json: {scenario_id: response_text}")
    ap.add_argument("--scenarios", default=DEFAULT_SCENARIOS)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--selftest", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    if args.selftest:
        sys.stderr.write("score.py is the scorer; run: python3 selftest.py\n")
        return 2
    if not args.responses:
        ap.print_usage()
        return 3
    try:
        doc = load_scenarios(args.scenarios)
        responses = load_json(args.responses)
        if not isinstance(responses, dict):
            raise ValueError("responses.json must be an object {scenario_id: text}")
    except (OSError, ValueError) as exc:
        sys.stderr.write("cannot run: %s\n" % exc)
        return 3
    report = score_all(doc, responses)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render(report))
    return 1 if any(r["verdict"] == "FAIL" for r in report["results"]) else 0


if __name__ == "__main__":
    sys.exit(main())
