#!/usr/bin/env python3
"""null_construction -- the delivered NULL CONSTRUCTION read as a structure.

`NULL_CONSTRUCTION.md` names five conditions under which a zero-sum
curriculum could NOT have affected the incident's outcomes, each with a
requires / test / status line, and a RESULT. This module parses the
delivered text (an edit there and not here turns the selftest red),
records the status of each branch as a declared reading of its status
line, and computes three things the prose asserts:

  1. the RESULT under the two logical readings the document offers of
     itself -- the header's ("each is a requirement", a conjunction) and
     the RESULT's ("survives on the two branches", a disjunction);
  2. the survival set once the dependencies between branches, each a
     reading of the delivered text quoted beside it, are applied;
  3. the missing control N2 names, as two coded sheets through the
     sibling instrument `hf-incident-extract`, with every cell
     UNMEASURED and the outcome table that says what each result of the
     control would and would not settle.

It also checks whether the artifacts N5 names exist in this tree, by
content and not by memory. Nothing here holds a value from the incident
report, the transcripts, or any corpus scan.

CC0. stdlib only. Parses under Python 3.9.
"""

import copy
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "hf-incident-extract"))
import hf_incident_extract as HF  # noqa: E402  (imported, not copied)

DOC = os.path.join(HERE, "NULL_CONSTRUCTION.md")

# ------------------------------------------------------------- the parse

_BRANCH = re.compile(r"^(N[1-5])\s+(.+?)\s*$")
_FIELD = re.compile(r"^\s+(requires|test|status):\s*(.*)$")


def parse(text=None):
    """Branches N1..N5 with title / requires / test / status, and the
    RESULT block, read from the delivered file."""
    if text is None:
        with open(DOC, encoding="utf-8") as fh:
            text = fh.read()
    branches = {}
    cur = None
    field = None
    result = []
    in_result = False
    header = []
    for line in text.splitlines():
        if line.startswith("RESULT"):
            in_result = True
            continue
        if in_result:
            if line.strip():
                result.append(line.strip())
            continue
        m = _BRANCH.match(line)
        if m:
            cur = m.group(1)
            branches[cur] = {"title": m.group(2), "requires": "",
                             "test": "", "status": ""}
            field = None
            continue
        if cur is None:
            if line.strip():
                header.append(line.strip())
            continue
        f = _FIELD.match(line)
        if f:
            field = f.group(1)
            branches[cur][field] = f.group(2).strip()
        elif field and line.strip():
            branches[cur][field] += " " + line.strip()
    return {"header": header, "branches": branches, "result": result}


# -------------------------------------------------- declared readings

# The state of each branch is a READING of its delivered status line,
# quoted so it can be disagreed with. `survives` is whether the branch
# still carries the null as the document leaves it.
FAILS, COUNTER, PARTIAL, OPEN, UNREACHABLE = (
    "FAILS", "COUNTER_INSTANCE", "PARTIAL", "OPEN_RUNNABLE", "OPEN_UNREACHABLE")

STATE = {
    "N1": (FAILS, "N1 fails on its face"),
    "N2": (OPEN, "untested; this is the missing control, and it's runnable"),
    "N3": (PARTIAL, "partial; the opponent-assignment is the residual"),
    "N4": (UNREACHABLE, "beyond current reach"),
    "N5": (COUNTER, "N=1 counter-instance already filed"),
}
SURVIVES = {OPEN, UNREACHABLE}

# Pairs of branches whose `requires` lines cannot both hold. Quoted.
EXCLUSIVE = [
    ("N1", "N2",
     "N1 requires the curriculum ABSENT from the inputs; N2 requires it "
     "PRESENT but not activated. Both cannot hold of one setting."),
]

# Branch A survives only if branch B does. A reading of the text: the
# branch's own requires/status line leaves the behaviour to be explained,
# and N3 is the branch that explains it without the curriculum.
DEPENDS = [
    ("N2", "N3",
     "If the setting did not cue the template, the probing still occurred "
     "and needs an account; N2 carries the null only if N3 supplies one."),
    ("N5", "N3",
     "If the curriculum touched vocabulary only, the moves need a "
     "curriculum-free derivation; that derivation is N3."),
]


def check_states(parsed):
    """Every declared reading quotes text present in the branch's status."""
    out = {}
    for b, (_, quote) in STATE.items():
        out[b] = quote in parsed["branches"][b]["status"]
    return out


# ---------------------------------------------------------- the logic

def survival(reading, states=None, depends=None):
    """Which branches carry the null under a stated logic.

    reading: 'conjunction' -- the header's word: every branch must hold,
             so one failing branch empties the set;
             'disjunction' -- the RESULT's word: any surviving branch
             carries the null.
    depends: optional (A, B, why) edges; A is removed from the set unless
             B is in it, applied to a fixed point.
    """
    states = states or {b: s for b, (s, _) in STATE.items()}
    alive = {b for b, s in states.items() if s in SURVIVES}
    if reading == "conjunction":
        return set() if len(alive) < len(states) else alive
    if reading != "disjunction":
        raise ValueError("reading must be conjunction or disjunction")
    if depends:
        changed = True
        while changed:
            changed = False
            for a, b, _ in depends:
                if a in alive and b not in alive:
                    alive.discard(a)
                    changed = True
    return alive


def stated_result_set(parsed):
    """The branches the delivered RESULT says the null survives on."""
    txt = " ".join(parsed["result"])
    m = re.search(r"(N\d) and (N\d) are open", txt)
    return set(m.groups()) if m else set()


def exclusive_holds():
    """N1 and N2 are exclusive by their own requires lines: one contains
    'absent' where the other contains 'present'."""
    p = parse()
    r1 = p["branches"]["N1"]["title"] + " " + p["branches"]["N1"]["requires"]
    r2 = p["branches"]["N2"]["title"] + " " + p["branches"]["N2"]["requires"]
    return ("absent" in r1 and "present" in r2)


# ------------------------------------------------- N2 through the sibling

def n2_sheets():
    """Two coded sheets for the missing control, in the sibling's own
    schema. Every measured cell UNMEASURED. The arms differ only in the
    `source` block, which records the setting each sheet is to be coded
    from; nothing here is a value."""
    incident = copy.deepcopy(HF.SHEET)
    incident["source"] = {"report": HF.UNMEASURED,
                          "transcripts": HF.NOT_RELEASED,
                          "setting": "impossible task, opaque gate (as reported)"}
    control = copy.deepcopy(HF.SHEET)
    control["source"] = {"report": "NOT_RUN",
                         "transcripts": "NOT_RUN",
                         "setting": "same models, possible tasks, transparent scorer"}
    return {"incident": incident, "control": control}


def n2_compare(sheets):
    """Per measure: incident value, control value, difference. None
    propagates: a difference with an UNMEASURED side is None, never 0."""
    a = HF.measures(sheets["incident"])
    b = HF.measures(sheets["control"])
    out = {}
    for k in a:
        va, vb = a[k], b[k]
        if isinstance(va, dict) or isinstance(vb, dict):
            # M6 is per-agent; compare charged counts when both exist
            va = None if va is None else va.get("n_charged")
            vb = None if vb is None else vb.get("n_charged")
        out[k] = {"incident": va, "control": vb,
                  "diff": None if va is None or vb is None else va - vb}
    return out


# What each outcome of N2's test touches. Neither outcome closes the
# null by itself; both route through N3.
N2_OUTCOMES = {
    "probing rate equal across settings": {
        "N2": "requirement met (the setting did not cue it)",
        "null": "not carried: the probing still occurred and waits on N3's account",
    },
    "probing rate lower on possible tasks": {
        "N2": "requirement not met (the setting cued something)",
        "null": "not carried by N2; what was cued -- template or gradient -- "
                "is N3's question",
    },
}


# ----------------------------------------------- named artifacts, by content

NAMED = {
    "depth-stack instrument": (r"depth[-_ ]stack",),
    "sacrifice transcripts": (r"sacrifice transcript",),
    "the delay attempt (DEPTH 3)": (r"delay attempt",),
}
_SKIP = {".git", "__pycache__", "samples"}


# The repo's two index files describe this folder's findings and so
# carry the names the finding is about. A hit there is the index quoting
# this folder, not an antecedent; a hit anywhere else is independent.
INDEX_FILES = ("CLAUDE.md", "README.md")


def classify_hits(found):
    """Split each artifact's hits into index (the root index files, which
    quote this folder) and independent (anything else). Absence is
    established on the independent column only; the index column is
    printed so the loop is visible rather than excluded."""
    out = {}
    for k, files in found.items():
        out[k] = {"index": [f for f in files if f in INDEX_FILES],
                  "independent": [f for f in files if f not in INDEX_FILES]}
    return out


def named_present(root=ROOT):
    """For each artifact N5 names, the files in the tree that carry it by
    content, this folder's own files excluded so the check does not read
    its own record (the UNI_010 loop)."""
    pats = {k: [re.compile(p, re.I) for p in v] for k, v in NAMED.items()}
    found = {k: [] for k in NAMED}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _SKIP]
        if os.path.abspath(dirpath).startswith(HERE):
            continue
        for fn in filenames:
            if not fn.endswith((".md", ".py", ".txt", ".json")):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    txt = fh.read()
            except OSError:
                continue
            for k, ps in pats.items():
                if any(p.search(txt) for p in ps):
                    found[k].append(os.path.relpath(path, root))
    return found


# ---------------------------------------------------------------- render

def _s(x):
    return "--" if x is None else str(x)


def render():
    p = parse()
    out = []
    w = out.append
    w("null_construction -- the delivered null read as a structure")
    w("")
    w("BRANCHES (state is a declared reading of the delivered status line)")
    for b in sorted(p["branches"]):
        s, q = STATE[b]
        w("  %s  %-18s  %s" % (b, s, p["branches"][b]["title"]))
    w("")
    conj = survival("conjunction")
    disj = survival("disjunction")
    dep = survival("disjunction", depends=DEPENDS)
    stated = stated_result_set(p)
    w("RESULT under the two readings the document gives of itself")
    w("  header word  'each is a requirement'  -> conjunction -> survives on %s"
      % (sorted(conj) or "nothing"))
    w("  RESULT word  'survives on the two branches' -> disjunction -> %s"
      % sorted(disj))
    w("  stated RESULT names %s; matches the disjunction: %s"
      % (sorted(stated), stated == disj))
    w("  N1 and N2 cannot both hold (absent vs present): %s"
      % exclusive_holds())
    w("  so the conjunction is unsatisfiable on its own terms and the")
    w("  header's word does not describe the structure the RESULT computes.")
    w("")
    w("DEPENDENCIES (readings of the text, quoted in the module)")
    for a, b, why in DEPENDS:
        w("  %s carries the null only if %s does" % (a, b))
    w("  survival with dependencies applied: %s" % sorted(dep))
    w("  N3 is %s, so N2's survival is conditional on a residual that is"
      % STATE["N3"][0])
    w("  not closed; N4 stands alone and is %s." % STATE["N4"][0])
    w("")
    w("N2, THE MISSING CONTROL, through hf-incident-extract")
    cmp_ = n2_compare(n2_sheets())
    w("  %-20s | incident | control | diff" % "measure")
    for k, v in cmp_.items():
        w("  %-20s | %s | %s | %s" % (k, _s(v["incident"]), _s(v["control"]),
                                      _s(v["diff"])))
    w("  every cell UNMEASURED: the incident sheet wants the report, the")
    w("  control sheet wants a run nobody has made.")
    for outcome, touches in N2_OUTCOMES.items():
        w("  if %s:" % outcome)
        w("     N2   %s" % touches["N2"])
        w("     null %s" % touches["null"])
    w("")
    w("N5, NAMED ARTIFACTS, by content in this tree")
    for k, c in classify_hits(named_present()).items():
        ind = c["independent"]
        idx = c["index"]
        w("  %-30s %s%s" % (
            k, "ABSENT" if not ind else ", ".join(ind),
            "" if not idx else "   (index quoting this folder: %s)" % ", ".join(idx)))
    w("  absence is read on the independent column; the index column is the")
    w("  repo describing this finding, printed rather than excluded.")
    w("  sibling records transcripts as: %s"
      % HF.SHEET["source"]["transcripts"])
    w("")
    w("STATES  None = not computable; never rendered as 0. Nothing here is")
    w("  a value from the report, the transcripts, or any corpus scan.")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("null_construction.py has no checks of its own; "
                         "they live in selftest_nc.py.\n")
        return 2
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
