"""WO-6 step 4, the disclosure-field audit.

A conflict-of-interest instrument is a list of FIELDS. Each field DECLARES
which of the eight conditions it gives a place to record (coding is
declared, never inferred from the field's name: a word list deciding what
a field covers is T1-1). The audit reports, per instrument, which
conditions have at least one field and which have none. The order's
expected null is money only, condition 2.

The five non-financial couplings the order lists are parsed from the
order; a coupling with no field is UNMEASURED and is never ABSENT, which
is the order's own 'read as ABSENT rather than unmeasured' stated as a
schema rule.

Every instrument here is CONSTRUCTED: real COI instruments sit behind
hosts that refuse CONNECT. Library module: refuses --selftest.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = os.path.join(HERE, "WORK_ORDER.md")
MONEY_ONLY = (2,)


def couplings(text=None):
    """The non-financial couplings with no disclosure field, parsed."""
    text = text if text is not None else open(ORDER, encoding="utf-8").read()
    m = re.search(r"They have no fields for:\n\n((?:- .*\n)+)", text)
    if not m:
        raise ValueError("non-financial couplings block not found")
    return [l[2:].strip() for l in m.group(1).splitlines() if l.startswith("- ")]


def audit(instrument):
    """instrument: {"id":..., "source":..., "fields":[{"name":..., "covers":[cond ids] | "UNCODED"}]}"""
    if not isinstance(instrument, dict) or not isinstance(instrument.get("fields"), list):
        return {"state": "MALFORMED"}
    covered = {c: [] for c in range(1, 9)}
    uncoded = []
    for f in instrument["fields"]:
        cov = f.get("covers", "UNCODED")
        if cov == "UNCODED":
            uncoded.append(f.get("name"))
            continue
        if not isinstance(cov, list) or any(c not in range(1, 9) for c in cov):
            return {"state": "MALFORMED", "why": "field %r covers %r" % (f.get("name"), cov)}
        for c in cov:
            covered[c].append(f.get("name"))
    has = [c for c in range(1, 9) if covered[c]]
    if uncoded and not has:
        verdict = "NOT_EVALUABLE"          # nothing coded: no reading either way
    elif tuple(has) == MONEY_ONLY:
        verdict = "MONEY_ONLY"
    elif not has:
        verdict = "NO_CONDITION_FIELD"
    else:
        verdict = "BEYOND_MONEY"
    return {"state": verdict, "has_field": has, "no_field": [c for c in range(1, 9) if not covered[c]],
            "fields_by_condition": covered, "uncoded_fields": uncoded, "n_fields": len(instrument["fields"])}


def coupling_readout(instrument):
    """The five non-financial couplings against the instrument's fields:
    each is COVERED (a field declares it) or UNMEASURED. Never ABSENT."""
    declared = set()
    for f in instrument.get("fields", []):
        for c in f.get("couplings", []):
            declared.add(c)
    return {c: ("COVERED" if c in declared else "UNMEASURED") for c in couplings()}


def constructed():
    return [
        {"id": "I-money", "source": "CONSTRUCTED",
         "fields": [{"name": "payments received from assessed party", "covers": [2]},
                    {"name": "equity held in assessed party", "covers": [2]},
                    {"name": "consulting income, past 3 years", "covers": [2]}]},
        {"id": "I-money-plus", "source": "CONSTRUCTED",
         "fields": [{"name": "payments received", "covers": [2]},
                    {"name": "board memberships", "covers": [2], "couplings": ["overlapping boards and advisory positions"]},
                    {"name": "engagement basis (mandated / invited)", "covers": [3]},
                    {"name": "publication terms", "covers": [4]}]},
        {"id": "I-uncoded", "source": "CONSTRUCTED",
         "fields": [{"name": "other interests (free text)", "covers": "UNCODED"}]},
        {"id": "I-empty", "source": "CONSTRUCTED", "fields": []},
    ]


def render(instruments=None):
    instruments = instruments or constructed()
    lines = ["disclosure_audit -- WO-6 step 4, which conditions a COI instrument has a field for",
             "  coverage is DECLARED per field, never read from the field's name; every instrument CONSTRUCTED",
             "  expected null (the order): money only = condition 2"]
    for ins in instruments:
        a = audit(ins)
        lines.append("  %-14s %-19s fields %d  has_field %s  no_field %s  uncoded %s"
                     % (ins["id"], a["state"], a.get("n_fields", 0), a.get("has_field"), a.get("no_field"), a.get("uncoded_fields")))
    ro = coupling_readout(instruments[0])
    lines.append("  non-financial couplings against %s:" % instruments[0]["id"])
    for c, s in ro.items():
        lines.append("      %-11s %s" % (s, c))
    lines.append("  reading: a coupling with no field is UNMEASURED; the instrument cannot return ABSENT for it,")
    lines.append("           because the field that would carry the negative does not exist. No real instrument read.")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("disclosure_audit.py is a library; run python3 selftest.py\n")
        return 2
    ins = None
    if "--instruments" in argv:
        ins = json.load(open(argv[argv.index("--instruments") + 1]))
    print(render(ins))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
