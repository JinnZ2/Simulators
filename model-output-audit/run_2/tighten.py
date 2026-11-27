#!/usr/bin/env python3
"""Run 2 item 4: a narrower extractor over run 1's candidates. Stdlib only. Still a word list.

    python3 tighten.py   -> tightened.json (counts, rules, kept claim ids)
"""
import collections
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
R1 = os.path.dirname(HERE)
RULES = [   # applied in this order; the first that fires removes the line
    ("data_or_code_file", None),        # a line of .json/.csv/.yaml/.yml, or a non-comment line of .py
    ("pass_count", re.compile(r"\b0 (failed|failures?|errors?)\b|\ball (tests )?pass|\b\d+/\d+ PASS\b|\bGREEN\b", re.I)),
    ("usage_or_command", re.compile(r"^\s*(python3? |\$ |pytest |cd |git |pip |#!|usage:)|--selftest|exit [0-9] ?=|exits? (0|1|2|3|nonzero)\b", re.I)),
    ("listing_row", re.compile(r"^[\s│├└─|]*[├└│]|^\|\s*`[^`]+`\s*\|[^|]*\|\s*$")),
    ("fixed_or_past", re.compile(r"\b(fixed|repaired|resolved|corrected|closed|no longer|now (passes|runs|green)|was failing|used to fail|before:|\(was )\b|\bREPAIRED\b|\bFIXED\b", re.I)),
    ("rule_or_conditional", re.compile(r"\bfails? (on|if|when|unless|with a|closed)\b|\b(must|should|would|will|can|could|may) (fail|crash|raise)\b|\bif .{0,60}\b(fails?|crash(es)?|is broken)\b|\brefuses? (a|an|to)\b", re.I)),
]
KEEP = re.compile(r"\b[1-9]\d* (tests? )?(failed|failing|failures?)\b|\b(fails|failed|failing)\b|\bcrash(es|ed)\b|\braises? \w*(Error|Exception)\b|\b\w*Error\b:"
                  r"|can't run|cannot run|could not (be )?run|couldn't run|unable to run|cannot be run|\bNOT_RUN\b|not runnable|\bis broken\b|doesn't work|does not work"
                  r"|(does|did) not converge|won't converge|\b(bug|defect) in\b|refuses CONNECT|egress.{0,30}(refus|block|403)|not installed", re.I)


def build():
    kept, removed = [], collections.Counter()
    by_type = collections.Counter()
    for l in open(os.path.join(R1, "claims.jsonl"), encoding="utf-8"):
        c = json.loads(l)
        q, path = c["quote"], c["location"].get("path", "")
        ext = os.path.splitext(path)[1].lower()
        if ext in (".json", ".csv", ".yaml", ".yml") or (ext == ".py" and not q.lstrip().startswith("#")):
            removed["data_or_code_file"] += 1
            continue
        hit = next((name for name, rx in RULES[1:] if rx.search(q)), None)
        if hit:
            removed[hit] += 1
        elif not KEEP.search(q):
            removed["no_assertion_form"] += 1
        else:
            kept.append(c["claim_id"])
            by_type[c["claim_type"]] += 1
    lines = len({k.rsplit(":", 1)[0] for k in kept})
    return {"record": "TIGHTENED_EXTRACTION", "run_1_candidates": sum(removed.values()) + len(kept), "kept": len(kept),
            "kept_distinct_lines": lines, "kept_by_type": dict(by_type), "removed_by_rule": dict(removed),
            "rules": [n for n, _ in RULES] + ["no_assertion_form"],
            "note": "a kept line is a candidate assertion, not a verdict; the rules are patterns and a paraphrase steps around them in both directions",
            "kept_claim_ids": kept}


if __name__ == "__main__":
    out = build()
    json.dump(out, open(os.path.join(HERE, "tightened.json"), "w"), indent=1)
    print({k: out[k] for k in ("run_1_candidates", "kept", "kept_distinct_lines", "kept_by_type", "removed_by_rule")})
