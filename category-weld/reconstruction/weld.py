#!/usr/bin/env python3
"""weld.py -- scorer for CATEGORY WELD terms. SUPERSEDED.

The real weld.py arrived in a second drop and sits at the folder root.
This file is the reconstruction written before it, kept because the
delivered-vs-reconstructed comparison is what closes CW_001 and refutes
CW_004. Do not use it to score a term.

The one arithmetic choice that mattered: this file reads "ratio between
component relative-changes" ADDITIVELY, (after - before) / abs(before),
which puts the statistic's zero at "did not move" -- the tracked
component's expected state -- so the ratio diverges at the paradigm weld.
The delivered file reads it MULTIPLICATIVELY, after / before, where an
unmoved component is 1.0 and the spread converges. The delivered reading
is the better one and CW_004, which the divergence produced, is refuted.
See AUDIT_NOTES.md sections 2 and 3.

RECONSTRUCTED. The first drop named this file and test_weld.py in
README.md ("weld.py scorer" / "test_weld.py synthetic fixtures for the
arithmetic") and neither arrived. Everything here is built backwards from
the four documented call sites:

    python3 weld.py                  # readouts for every term
    python3 weld.py --term capital   # components and cases for one term
    python3 weld.py --jsonl          # one score object per line
    python3 weld.py --new employed    > welds/employed.json

and from the three readouts named in MECHANISM_09.md:

    n_cases      how many divergence cases can be named
    max_spread   largest ratio between component relative-changes in one case
    bias         how consistently the divergence runs one direction, 0..1

The prose names the readouts. It does not fix the arithmetic. Every point
where the arithmetic had to be decided rather than read off is marked
[CHOICE] at the decision. A different reconstruction that satisfies the
same prose will return different numbers.

stdlib only. CC0.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# term files live one level up, alongside the delivered scorer
WELDS = os.path.join(os.path.dirname(HERE), "welds")

# [CHOICE] bias over a single observation is |+-1| / 1 == 1.0 whatever the
# data says -- a value the statistic returns before it has seen anything to
# be consistent WITH. Below this count bias is None with a reason, rather
# than a number that always reads as maximal directional work.
MIN_BIAS_OBS = 2

# [CHOICE] a relative change is (after - before) / abs(before). abs() in the
# denominator so that the SIGN of the returned change is the direction the
# component moved, not the direction times the sign of its baseline.
# before == 0 has no relative change and is reported as unquantified.


def relative_change(before, after):
    """Signed relative change, or None where it is not defined."""
    if before is None or after is None:
        return None
    if before == 0:
        return None  # [CHOICE] not 0.0, not inf -- undefined, and said so
    return (after - before) / abs(before)


def quantified(case):
    """{component_id: relative_change} for components with a usable pair."""
    out = {}
    for cid, r in (case.get("readings") or {}).items():
        rc = relative_change(r.get("before"), r.get("after"))
        if rc is not None:
            out[cid] = rc
    return out


def case_spread(case):
    """Largest ratio between component relative-changes in this one case.

    [CHOICE] "ratio between relative-changes" is read as a ratio of
    MAGNITUDES: max(|r|) / min(|r|) over the quantified components, so a
    component that barely moved while another collapsed gives a large
    number regardless of which way either went. Direction is bias's job.

    [CHOICE] a zero denominator (one component exactly unmoved) is returned
    as None rather than inf. An unmoved component alongside a moved one is
    the mechanism's own headline case, so it wants its own readout, not a
    float that poisons every max() downstream.
    """
    q = quantified(case)
    if len(q) < 2:
        return None, "fewer than two quantified components"
    mags = sorted(abs(v) for v in q.values())
    if mags[0] == 0:
        return None, "a quantified component is exactly unmoved"
    return mags[-1] / mags[0], None


def case_directions(term, case):
    """Signed divergences for this case, as (sign, note) observations.

    The term is read off `tracked_by_label`. The divergence that matters is
    the hidden component moving relative to the one carrying the label, so
    each observation is sign(r_other - r_tracked).

    [CHOICE] where the tracked component is not quantified in a case, the
    first quantified component in declared order stands in as reference and
    the observation is flagged. Without the fallback the only case in the
    delivered data with any readings at all contributes nothing, because
    the component the term is read off is the one nobody measured.
    """
    q = quantified(case)
    if len(q) < 2:
        return []
    tracked = term.get("tracked_by_label")
    order = [c["id"] for c in term.get("components", [])]
    substituted = False
    if tracked not in q:
        ref = next((c for c in order if c in q), None)
        substituted = True
    else:
        ref = tracked
    if ref is None:
        return []
    out = []
    for cid, rc in q.items():
        if cid == ref:
            continue
        d = rc - q[ref]
        if d == 0:
            continue  # [CHOICE] exact ties carry no direction, excluded
        out.append((1 if d > 0 else -1, "reference substituted" if substituted else ""))
    return out


def named_cases(term):
    """Divergence cases that have actually been named.

    [CHOICE] n_cases is defined in MECHANISM_09.md as "how many divergence
    cases can be NAMED", and the documented workflow is
    `weld.py --new employed > welds/employed.json`, which writes a
    placeholder case with an empty id. Counting placeholders would let a
    blank template score on the only live readout in the folder. A case
    with no id has not been named.
    """
    return [c for c in term.get("divergences", []) if (c.get("id") or "").strip()]


def score(term):
    cases = named_cases(term)
    spreads = []
    unspreadable = []
    for c in cases:
        s, why = case_spread(c)
        if s is None:
            unspreadable.append((c.get("id"), why))
        else:
            spreads.append((c.get("id"), s))

    obs = []
    for c in cases:
        obs.extend(case_directions(term, c))

    if len(obs) >= MIN_BIAS_OBS:
        signs = [s for s, _ in obs]
        bias = abs(sum(signs)) / len(signs)
        bias_note = ""
    else:
        bias = None
        bias_note = "%d directional observation(s), minimum %d" % (
            len(obs),
            MIN_BIAS_OBS,
        )

    return {
        "term": term.get("term"),
        "domain": term.get("domain"),
        "tracked_by_label": term.get("tracked_by_label"),
        "n_components": len(term.get("components", [])),
        "n_cases": len(cases),
        "n_cases_with_readings": sum(
            1 for c in cases if (c.get("readings") or {})
        ),
        "n_cases_quantified": len(spreads),
        "max_spread": max((s for _, s in spreads), default=None),
        "max_spread_case": max(spreads, key=lambda t: t[1])[0] if spreads else None,
        "bias": bias,
        "bias_n_obs": len(obs),
        "bias_note": bias_note,
        "unspreadable": unspreadable,
    }


def fmt(v, spec="%.3f"):
    return "--" if v is None else spec % v


def load_all(path=WELDS):
    terms = []
    for name in sorted(os.listdir(path)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(path, name), encoding="utf-8") as fh:
            terms.append(json.load(fh))
    return terms


def print_table(terms):
    print("CATEGORY WELD -- %d term(s)" % len(terms))
    print()
    print("  %-10s %5s %5s %5s  %10s  %6s" % (
        "term", "comp", "case", "quan", "max_spread", "bias"))
    print("  " + "-" * 50)
    for t in terms:
        s = score(t)
        print("  %-10s %5d %5d %5d  %10s  %6s" % (
            s["term"], s["n_components"], s["n_cases"],
            s["n_cases_quantified"], fmt(s["max_spread"]), fmt(s["bias"])))
    print()
    print("  quan = cases with two or more components carrying a usable")
    print("  before/after pair. max_spread and bias read only those.")
    print()
    for t in terms:
        s = score(t)
        if s["bias"] is None and s["bias_note"]:
            print("  %s: bias withheld -- %s" % (s["term"], s["bias_note"]))
        for cid, why in s["unspreadable"]:
            print("  %s / %s: no spread -- %s" % (s["term"], cid, why))


def print_term(term):
    s = score(term)
    print("%s -- %s" % (term["term"], term.get("domain", "")))
    print("read off: %s" % term.get("tracked_by_label"))
    if term.get("note"):
        print()
        print("  " + term["note"])
    print()
    print("COMPONENTS")
    for c in term.get("components", []):
        mark = "*" if c["id"] == term.get("tracked_by_label") else " "
        print("  %s %-18s %s" % (mark, c["id"], c.get("name", "")))
        print("      unit: %s" % c.get("unit", ""))
    print()
    print("DIVERGENCE CASES")
    for c in named_cases(term):
        q = quantified(c)
        sp, why = case_spread(c)
        tag = "quantified" if sp is not None else (
            "readings present, %s" % why if (c.get("readings") or {}) else "named only")
        print("  [%s] %s" % (tag, c.get("id")))
        for line in wrap(c.get("note", ""), 66):
            print("      " + line)
        for cid, rc in sorted(q.items()):
            print("      %-18s rel change %+.4f" % (cid, rc))
        if sp is not None:
            print("      spread %.3f" % sp)
        print()
    print("READOUTS")
    print("  n_cases      %d" % s["n_cases"])
    print("  max_spread   %s" % fmt(s["max_spread"]))
    print("  bias         %s%s" % (
        fmt(s["bias"]), "  (%s)" % s["bias_note"] if s["bias_note"] else ""))


def wrap(text, width):
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


TEMPLATE = {
    "term": None,
    "domain": "",
    "tracked_by_label": "",
    "note": "",
    "components": [
        {"id": "", "name": "", "unit": ""},
    ],
    "divergences": [
        {
            "id": "",
            "note": "",
            "readings": {
                "": {"before": None, "after": None, "unit": "", "source": ""}
            },
        }
    ],
}


def new_term(name):
    t = dict(TEMPLATE)
    t["term"] = name
    return json.dumps(t, indent=2) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="score CATEGORY WELD terms")
    ap.add_argument("--term", help="components and cases for one term")
    ap.add_argument("--jsonl", action="store_true", help="one score object per line")
    ap.add_argument("--new", metavar="TERM", help="emit a blank term file")
    ap.add_argument("--welds", default=WELDS, help="directory of term files")
    a = ap.parse_args(argv)

    if a.new:
        sys.stdout.write(new_term(a.new))
        return 0

    terms = load_all(a.welds)

    if a.term:
        hit = next((t for t in terms if t.get("term") == a.term), None)
        if hit is None:
            print("no term %r in %s" % (a.term, a.welds), file=sys.stderr)
            return 1
        print_term(hit)
        return 0

    if a.jsonl:
        for t in terms:
            print(json.dumps(score(t), sort_keys=True))
        return 0

    print_table(terms)
    return 0


if __name__ == "__main__":
    sys.exit(main())
