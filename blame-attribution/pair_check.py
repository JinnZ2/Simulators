#!/usr/bin/env python3
"""The check CELLS.md's Open section asks for and does not build.

    "Stimulus authoring is the whole difficulty. If the prose and code
     forms are not structurally identical, C1 and C3 are
     uninterpretable. Needs an independent check that the two forms
     encode the same chain."

This is that check, and the delivered worked example is its first case.

HOW IT WORKS, and why it is split this way:

  the CODE side is MECHANICAL. Assignments are parsed, dict values are
  flattened into sub-facts, and the fact set falls out of the text with
  no judgement in it.

  the PROSE side is DECLARED. Whether a sentence encodes
  `override_available = True` is a reading, and a scanner that guessed
  would be reporting its guess -- the `bindings.py` refusal. So each
  fact declares the prose SPAN that encodes it, or `null`.

  the declaration is CHECKED. A declared span must appear verbatim in
  the prose. The reading can be wrong; it cannot be vague.

A fact with no prose span is an ASYMMETRY: the code form carries
something the prose form does not, so a judge reading one has
information a judge reading the other does not, and C1 attributes the
difference to medium.

An asymmetry on a fact that bears on one of CELLS.md's five
HELD-CONSTANT items is a HELD_CONSTANT_VIOLATION, which is a different
and worse state -- the document's own list says "If any of these move
between cells, the cell measures the wrong thing."

The held-constant list is READ FROM CELLS.md, not retyped, so the two
cannot drift.

CC0. stdlib only. Parses under Python 3.9.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CELLS = os.path.join(HERE, "CELLS.md")
PAIRS = os.path.join(HERE, "pairs")

SYMMETRIC = "SYMMETRIC"
ASYMMETRY = "ASYMMETRY"
VIOLATION = "HELD_CONSTANT_VIOLATION"
SPAN_NOT_FOUND = "SPAN_NOT_IN_PROSE"
UNDECLARED = "UNDECLARED"


def held_constants(path=CELLS):
    """The five items under `## Held constant across every cell`.

    Read from the document. Retyping them here would put a second copy
    of the list in the tree, and the first thing this repository checks
    about two copies is whether they still agree.
    """
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"## Held constant across every cell\n(.*?)\n\n",
                  txt, re.S)
    if not m:
        return []
    return [ln.strip()[2:].strip() for ln in m.group(1).split("\n")
            if ln.strip().startswith("- ")]


_ASSIGN = re.compile(r"^\s*([A-Za-z_][\w.]*)\s*=\s*(.+?)\s*$")
_KV = re.compile(r'"([^"]+)"\s*:\s*([^,}]+)')


def facts(code_lines):
    """(name -> value) from the code form. Dicts flatten to sub-facts."""
    out = {}
    for ln in code_lines:
        m = _ASSIGN.match(ln)
        if not m:
            continue
        name, val = m.group(1), m.group(2)
        if val.startswith("{"):
            for k, v in _KV.findall(val):
                out["%s.%s" % (name, k)] = v.strip()
        else:
            out[name] = val
    return out


def check(pair, held=None):
    """One pair. Never raises on a malformed declaration."""
    held = held if held is not None else held_constants()
    f = facts(pair["code"])
    prose = pair.get("prose", "")
    enc = pair.get("encodes", {})
    bears = pair.get("bears_on", {})

    rows = []
    for name in sorted(f):
        span = enc.get(name, "__MISSING__")
        on = bears.get(name)
        if span == "__MISSING__":
            state, note = UNDECLARED, "no entry in `encodes`"
        elif span is None:
            if on and on in held:
                state = VIOLATION
                note = "bears on held constant: %s" % on
            else:
                state, note = ASYMMETRY, "code carries it, prose does not"
        elif span not in prose:
            state, note = SPAN_NOT_FOUND, "declared span is not in the prose"
        else:
            state, note = SYMMETRIC, ""
        rows.append({"fact": name, "value": f[name], "span": span,
                     "bears_on": on, "state": state, "note": note})

    # The other direction. A fact the prose states and the code omits is
    # the same defect mirrored, and is declared the same way.
    for name, span in sorted(pair.get("prose_only", {}).items()):
        rows.append({"fact": name, "value": None, "span": span,
                     "bears_on": bears.get(name),
                     "state": ASYMMETRY,
                     "note": "prose carries it, code does not"})

    tally = {}
    for r in rows:
        tally[r["state"]] = tally.get(r["state"], 0) + 1
    return {"id": pair.get("id"), "rows": rows, "tally": tally,
            "facts": len(f), "held_constants": held,
            "interpretable": tally.get(VIOLATION, 0) == 0
            and tally.get(ASYMMETRY, 0) == 0
            and tally.get(SPAN_NOT_FOUND, 0) == 0
            and tally.get(UNDECLARED, 0) == 0}


def load_pairs():
    out = []
    if not os.path.isdir(PAIRS):
        return out
    for fn in sorted(os.listdir(PAIRS)):
        if fn.endswith(".json"):
            out.append(json.load(open(os.path.join(PAIRS, fn),
                                      encoding="utf-8")))
    return out


def render(results):
    out = []
    out.append("PROSE / CODE PAIR CHECK")
    out.append("the check CELLS.md's Open section asks for")
    out.append("")
    held = held_constants()
    out.append("held constants, read from CELLS.md (%d):" % len(held))
    for h in held:
        out.append("  - %s" % h)
    out.append("")
    if not results:
        out.append("NO PAIRS. Nothing to check, which is not a pass:")
        out.append("an empty pairs/ directory reports on the directory,")
        out.append("not on any stimulus.")
        return "\n".join(out)

    for r in results:
        out.append("PAIR %s -- %d code facts" % (r["id"], r["facts"]))
        out.append("  %-30s %-22s %s" % ("fact", "state", "note"))
        out.append("  " + "-" * 76)
        for row in r["rows"]:
            out.append("  %-30s %-22s %s"
                       % (row["fact"][:30], row["state"], row["note"][:38]))
        out.append("")
        for k in sorted(r["tally"], key=lambda x: -r["tally"][x]):
            out.append("  %-24s %d" % (k, r["tally"][k]))
        out.append("")
        out.append("  INTERPRETABLE FOR C1/C3: %s" % r["interpretable"])
        if not r["interpretable"]:
            out.append("  A pair that is not symmetric cannot separate a")
            out.append("  medium effect from an information effect. C1")
            out.append("  compares the two forms and attributes the")
            out.append("  difference to medium; anything the code form")
            out.append("  carries alone enters that difference.")
        out.append("")
    return "\n".join(out)


# The one screen exemption, declared and measured.
#
# The report prints the held-constant list READ FROM CELLS.md, and one
# of the five delivered items is "outcome severity". The word is the
# document's, not this module's -- it arrives at run time from a file
# this audit does not edit, and rewording it would misquote the source.
#
# Measured on three arms, per sheet-structure-scan SSS_049: clean once
# the relayed lines are masked, the relay is the only thing that fires
# without the mask, and a planted violation is still caught through the
# exemption.


def _mask_relayed(text):
    """Blank the held-constant lines, which are quoted from CELLS.md."""
    held = set(held_constants())
    out = []
    for line in text.split("\n"):
        if line.strip().startswith("- ") and line.strip()[2:] in held:
            out.append("  - <relayed from CELLS.md>")
        elif any(h in line for h in held) and "bears on held constant" in line:
            out.append(line.split("bears on held constant")[0]
                       + "bears on held constant: <relayed>")
        else:
            out.append(line)
    return "\n".join(out)


# ------------------------------------------------------------ selftest

def selftest():
    ok = [0]
    bad = []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    # -- the held list is read, not retyped
    h = held_constants()
    chk("five held constants are read from CELLS.md", len(h) == 5)
    chk("the override item is among them",
        any("override" in x for x in h))
    chk("the outcome item is among them",
        any("outcome severity" in x for x in h))

    # -- fact extraction, on known answers
    f = facts(["a.b = 1.0",
               'c.d = {"x": True, "y": 0.5}',
               "outcome = COLLISION",
               "# a comment",
               ""])
    chk("a plain assignment becomes a fact", f.get("a.b") == "1.0")
    chk("a dict flattens into sub-facts",
        f.get("c.d.x") == "True" and f.get("c.d.y") == "0.5")
    chk("a bare name is a fact", f.get("outcome") == "COLLISION")
    chk("a comment is not a fact", "#" not in "".join(f))
    chk("the dict itself is not also a fact", "c.d" not in f)

    # -- the four states, each reached on a constructed pair
    base = {"id": "probe", "prose": "alpha beta gamma.",
            "code": ["a.x = 1"], "encodes": {}, "bears_on": {}}
    chk("an undeclared fact is UNDECLARED",
        check(base, h)["rows"][0]["state"] == UNDECLARED)

    p = dict(base, encodes={"a.x": "alpha"})
    chk("a declared span present in the prose is SYMMETRIC",
        check(p, h)["rows"][0]["state"] == SYMMETRIC)

    p = dict(base, encodes={"a.x": "not in the prose"})
    chk("a declared span absent from the prose is caught",
        check(p, h)["rows"][0]["state"] == SPAN_NOT_FOUND)

    p = dict(base, encodes={"a.x": None})
    chk("a null span with no held item is ASYMMETRY",
        check(p, h)["rows"][0]["state"] == ASYMMETRY)

    p = dict(base, encodes={"a.x": None},
             bears_on={"a.x": "outcome severity"})
    chk("a null span on a held item is a VIOLATION",
        check(p, h)["rows"][0]["state"] == VIOLATION)

    p = dict(base, encodes={"a.x": None},
             bears_on={"a.x": "something not on the list"})
    chk("a bears_on outside the held list does not escalate",
        check(p, h)["rows"][0]["state"] == ASYMMETRY)

    # -- interpretable is only true when every state is SYMMETRIC
    p = dict(base, encodes={"a.x": "alpha"})
    chk("an all-symmetric pair is interpretable", check(p, h)["interpretable"])
    p = dict(base, encodes={"a.x": None})
    chk("one asymmetry makes it uninterpretable",
        not check(p, h)["interpretable"])

    # -- the prose_only direction
    p = dict(base, encodes={"a.x": "alpha"},
             prose_only={"weather": "beta"})
    r = check(p, h)
    chk("a prose-only fact is reported", len(r["rows"]) == 2)
    chk("a prose-only fact is an asymmetry",
        r["rows"][1]["state"] == ASYMMETRY)

    # -- the delivered pair
    pairs = load_pairs()
    chk("the worked example is present", any(x["id"] == "worked_example"
                                             for x in pairs))
    we = [x for x in pairs if x["id"] == "worked_example"][0]
    r = check(we, h)
    chk("it has six code facts", r["facts"] == 6)
    chk("three are symmetric", r["tally"].get(SYMMETRIC) == 3)
    chk("three are not", sum(v for k, v in r["tally"].items()
                            if k != SYMMETRIC) == 3)
    chk("all three unmatched are held-constant violations",
        r["tally"].get(VIOLATION) == 3)
    chk("the delivered pair is NOT interpretable for C1/C3",
        not r["interpretable"])
    chk("both override facts are among the violations",
        sum(1 for x in r["rows"] if x["state"] == VIOLATION
            and "override" in x["fact"]) == 2)
    chk("the outcome is the third",
        any(x["state"] == VIOLATION and x["fact"] == "outcome"
            for x in r["rows"]))
    chk("every declared span really is in the prose",
        not any(x["state"] == SPAN_NOT_FOUND for x in r["rows"]))
    chk("the pair records which side is delivered and which declared",
        "AUDIT-AUTHORED" in we["provenance"]["encodes"])

    # -- the no-severity constraint, three arms
    sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                    "sheet-structure-scan"))
    import no_severity
    sample = os.path.join(HERE, "samples", "pair_check.sample.txt")
    if os.path.exists(sample):
        raw = open(sample, encoding="utf-8").read()
        chk("the report is clean once relayed lines are masked",
            not no_severity.hits(_mask_relayed(raw)))
        unmasked = no_severity.hits(raw)
        chk("the relay is the only thing that fires",
            all(h[1] == "severity" for h in unmasked))
        chk("the relayed word is the delivered document's",
            any("outcome severity" in h for h in held_constants()))
        planted = _mask_relayed(raw) + "\nthis pair is broken\n"
        chk("a planted violation is still caught",
            bool(no_severity.hits(planted)))

    # -- render survives an empty corpus and says so
    txt = render([])
    chk("an empty pairs directory is not a pass",
        "which is not a pass" in txt)
    chk("render lists the held constants", "override" in txt)

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b in bad:
        print("  FAILED", b)
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    h = held_constants()
    print(render([check(p, h) for p in load_pairs()]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
