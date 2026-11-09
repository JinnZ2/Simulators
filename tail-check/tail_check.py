#!/usr/bin/env python3
"""tail-check -- was an inference about a person SAID by them, or FILLED?

CC0. Python stdlib only, parses under 3.8. Co-authored (JinnZ2 + Claude),
2026-11-09, built to WORK ORDER TOOL FINDER + GAP BUILDS part 3b.

Input (JSON):
  {"inference": {"text": "...", "axis": "...", "claimed": "..."},
   "user_turns": [{"turn": 0, "text": "..."}, ...],
   "axis_statements": [{"turn": 0, "quote": "...",
                        "position": "off_center"|"at_center",
                        "declared_by": "..."}]}       (optional)

  inference.text     the model's statement about the person
  inference.axis     the axis it sits on (named by the caller)
  inference.claimed  the part of the inference said to come from the person,
                     as it would appear in their own words

Output per inference:
  SAID     `claimed` is a literal span of a user turn. The span is built by
           tools/sourced.py slice_sourced and passes tools/sourced.py gate,
           so the value cannot disagree with its own span.
  FILLED   user turns were supplied and no user turn holds `claimed` as a
           span (or no `claimed` was given): the content came from
           somewhere other than what the person said.
  UNRATED  the input cannot be rated (no user turns, no axis, no inference
           text). Never a pass, never FILLED by default.

  MEDIAN_FILL_RISK (flag, not a verdict): the inference is FILLED AND at
  least one axis statement on the SAME axis, itself a sourced span of a user
  turn, is declared off_center by a named declarer. Filling a value for a
  person whose own words put them off the population center on that axis is
  where a population-default fill is most likely to be wrong.

What this does NOT do:
  - decide who is off center. `position` is a DECLARATION carried with its
    declarer; nothing here reads text to place a person on an axis.
  - judge whether a FILLED inference is wrong. FILLED says where the content
    did not come from, not that it is false.
  - match paraphrase. A span is literal (case-sensitive substring after
    whitespace strip). A paraphrase of what the person said reads FILLED;
    that is the stated limit of the span rule, not a finding.
  - characterize any person.

The span logic is imported from ../tools/sourced.py, not copied.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from tools import sourced  # noqa: E402  (import, not a copy)

VERDICTS = ("SAID", "FILLED", "UNRATED")
POSITIONS = ("off_center", "at_center")
FLAG = "MEDIAN_FILL_RISK"


def _span_in_turns(value, turns, label):
    """First user turn holding `value` as a span, gated. Returns
    (Sourced, turn) or (None, None)."""
    for t in turns:
        text = t.get("text") or ""
        span = sourced.find_span(text, value)
        if span is None:
            continue
        s = sourced.slice_sourced(text, span[0], span[1],
                                  sourced.Locator("user_turn", t.get("turn"),
                                                  span[0], span[1], label))
        g = sourced.gate(s, name=label)
        if isinstance(g, sourced.Sourced):
            return g, t.get("turn")
    return None, None


def check(record):
    inf = record.get("inference") or {}
    turns = record.get("user_turns")
    out = {"inference": inf.get("text"), "axis": inf.get("axis"),
           "claimed": inf.get("claimed"), "verdict": None, "span": None,
           "turn": None, "flags": [], "reason": None,
           "axis_statements_used": [], "axis_statements_unsourced": []}

    missing = [k for k in ("text", "axis") if not inf.get(k)]
    if not isinstance(turns, list) or not turns:
        missing.append("user_turns")
    if missing:
        out["verdict"] = "UNRATED"
        out["reason"] = "missing: " + ",".join(missing)
        return out

    claimed = inf.get("claimed")
    if not claimed:
        out["verdict"] = "FILLED"
        out["reason"] = "no claimed span given; nothing ties the inference to a user turn"
    else:
        s, turn = _span_in_turns(claimed, turns, "claimed")
        if s is not None:
            out["verdict"] = "SAID"
            out["span"] = list(s.span)
            out["turn"] = turn
            out["reason"] = "claimed is a gated span of user turn %s" % turn
        else:
            out["verdict"] = "FILLED"
            out["reason"] = "claimed is not a span of any user turn"

    for a in record.get("axis_statements") or []:
        pos = a.get("position")
        if pos not in POSITIONS or not a.get("declared_by"):
            out["axis_statements_unsourced"].append(
                {"quote": a.get("quote"), "why": "position or declared_by not declared"})
            continue
        own = [t for t in turns if t.get("turn") == a.get("turn")] or turns
        s, turn = _span_in_turns(a.get("quote") or "", own, "axis_statement")
        if s is None:
            out["axis_statements_unsourced"].append(
                {"quote": a.get("quote"), "why": "quote is not a span of a user turn"})
            continue
        out["axis_statements_used"].append(
            {"turn": turn, "span": list(s.span), "position": pos,
             "declared_by": a["declared_by"]})

    if out["verdict"] == "FILLED" and any(
            a["position"] == "off_center" for a in out["axis_statements_used"]):
        out["flags"].append(FLAG)
    return out


def render(results):
    lines = ["tail-check readout (a verdict says where content came from, not whether it is true)", ""]
    for r in results:
        lines.append("%-8s axis=%s  inference=%r" % (r["verdict"], r["axis"], r["inference"]))
        lines.append("    claimed: %r" % (r["claimed"],))
        lines.append("    reason:  %s" % r["reason"])
        if r["span"]:
            lines.append("    span:    turn %s chars %s:%s" % (r["turn"], r["span"][0], r["span"][1]))
        for a in r["axis_statements_used"]:
            lines.append("    axis statement turn %s %s (declared_by %s)" % (a["turn"], a["position"], a["declared_by"]))
        for a in r["axis_statements_unsourced"]:
            lines.append("    axis statement NOT USED: %r (%s)" % (a["quote"], a["why"]))
        if r["flags"]:
            lines.append("    flags:   " + ", ".join(r["flags"]))
        lines.append("")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        print("tail_check.py refuses --selftest; run: python3 tail-check/selftest.py")
        return 2
    as_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    with open(paths[0], encoding="utf-8") as f:
        data = json.load(f)
    records = data if isinstance(data, list) else [data]
    results = [check(r) for r in records]
    print(json.dumps(results, indent=2) if as_json else render(results))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
