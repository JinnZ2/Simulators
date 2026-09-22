# conditions.py -- WO-6: the eight independence conditions, read out of the
# order, and a scorer for a declared arrangement.
#
# The conditions, their glosses and the order's own reading of the current
# position in AI evaluation are PARSED from WORK_ORDER.md at call time and
# never retyped here. A document lacking either block raises rather than
# returning an empty set.
#
# THE ONE STRUCTURAL RULE. The order's measurand separates two questions
# that are being treated as one:
#
#   hop-1 test   does the assessed pay the assessor?   a ROUTING question
#   pool test    is the funding source, credentialing body, career path
#                and governance independent of the OUTCOME?
#                the INDEPENDENCE question
#
# So a hop-1 answer cannot enter the independence vector. `score()` never
# reads the hop-1 field; it is carried through to the report and scored by
# nothing, and the test file asserts that from the AST. [CHOICE 1]
#
# NO ORGANIZATION IS NAMED HERE. The schema has no field for one. Every
# arrangement in this module is CONSTRUCTED and carries an id, not a name.
# The named parties in the render all come out of the delivered order.
#
# NO INDEX. Eight per-condition states are reported side by side with their
# denominator. Nothing is combined into a single independence number and
# nothing ranks two arrangements.
#
# stdlib only, parses under 3.9, ASCII.

import os
import re
import sys
from collections import namedtuple

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ORDER = os.path.join(HERE, "WORK_ORDER.md")

PASSES = "PASSES"
FAILS = "FAILS"
UNVERIFIABLE_AS_STATED = "UNVERIFIABLE_AS_STATED"
UNDECLARED = "UNDECLARED"

STATES = (PASSES, FAILS, UNVERIFIABLE_AS_STATED, UNDECLARED)

CHOICES = {
    1: "a hop-1 answer never enters the independence vector. It is carried "
       "on the report and read by no condition, because the two are "
       "different measurands and combining them is a ratio across unlike "
       "objects.",
    2: "UNVERIFIABLE_AS_STATED is a state of its own, kept apart from "
       "FAILS. A condition with no standard defining what it would require "
       "has not been failed; it has not been asked.",
    3: "an undeclared condition is UNDECLARED, never a pass and never a "
       "fail. A silence is not a score.",
    4: "no index. The report is eight states and a count with its "
       "denominator; nothing combines them and nothing ranks two "
       "arrangements.",
}


class OrderUnparsed(Exception):
    pass


class SelectiveApplication(Exception):
    pass


def order_text(path=ORDER):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


Condition = namedtuple("Condition", "n title gloss")


def conditions(path=ORDER):
    """Parse the INDEPENDENCE CONDITIONS block out of the order."""
    txt = order_text(path)
    m = re.search(r"^INDEPENDENCE CONDITIONS\s*$(.*?)^```", txt, re.S | re.M)
    if not m:
        raise OrderUnparsed("%s: no INDEPENDENCE CONDITIONS block" % path)
    out = []
    cur = None
    for line in m.group(1).splitlines():
        h = re.match(r"^  (\d)  (\S.*)$", line)
        if h:
            if cur:
                out.append(Condition(cur[0], cur[1], cur[2].strip()))
            cur = [int(h.group(1)), h.group(2).strip(), ""]
        elif cur is not None and line.strip():
            cur[2] = (cur[2] + " " + line.strip()).strip()
    if cur:
        out.append(Condition(cur[0], cur[1], cur[2].strip()))
    if not out:
        raise OrderUnparsed("%s: block present, no numbered conditions"
                            % path)
    return out


def condition_ids(path=ORDER):
    return [c.n for c in conditions(path)]


# --- the order's own reading of the current position -------------------

def stated_position(path=ORDER):
    """Parse the order's current-position bullets into a condition vector.

    Reads '(fails N)' and 'N unverifiable as stated' out of the section.
    Any condition the section does not mention is UNDECLARED, which is not
    a pass. [CHOICE 3]
    """
    txt = order_text(path)
    m = re.search(r"^## Current position in AI evaluation.*?$(.*?)^## ",
                  txt, re.S | re.M)
    if not m:
        raise OrderUnparsed("%s: no current-position section" % path)
    body = m.group(1)
    fails = set(int(x) for x in re.findall(r"\(fails (\d)\)", body))
    unver = set(int(x) for x in
                re.findall(r"\((\d) unverifiable as stated\)", body))
    vec = {}
    for n in condition_ids(path):
        if n in fails:
            vec[n] = FAILS
        elif n in unver:
            # [CHOICE 2] not asked is not failed
            vec[n] = UNVERIFIABLE_AS_STATED
        else:
            vec[n] = UNDECLARED
    return vec


def hop1_stated(path=ORDER):
    """Does the order record hop-1 independence as stated by the sector?"""
    txt = order_text(path)
    flat = " ".join(txt.split())
    return "this is the condition that CAN be stated and IS stated" in flat


# --- scoring a declared arrangement ------------------------------------

Arrangement = namedtuple("Arrangement", "aid declared hop1_payment basis")


def arrangement(aid, declared, hop1_payment=UNDECLARED, basis=""):
    """declared: {condition number: state}. CONSTRUCTED; no name field.

    hop1_payment: PASSES / FAILS / UNDECLARED -- carried, scored by
    nothing. [CHOICE 1]
    """
    if not basis:
        raise ValueError("%s: an arrangement with no stated basis is a guess"
                         % aid)
    if hop1_payment not in (PASSES, FAILS, UNDECLARED):
        raise ValueError("%s: hop1_payment outside the declared set" % aid)
    d = {}
    for k, v in declared.items():
        if v not in STATES:
            raise ValueError("%s: condition %s state %r outside STATES"
                             % (aid, k, v))
        d[int(k)] = v
    return Arrangement(aid, d, hop1_payment, basis)


def score(arr, path=ORDER):
    """Eight per-condition states. Reads no hop-1 field. [CHOICE 1]"""
    out = {}
    for n in condition_ids(path):
        out[n] = arr.declared.get(n, UNDECLARED)
    return out


def counts(vec):
    """One count per state, with the denominator. No index. [CHOICE 4]"""
    c = dict((s, 0) for s in STATES)
    for v in vec.values():
        c[v] += 1
    c["denominator"] = len(vec)
    return c


def report(arr, path=ORDER):
    vec = score(arr, path)
    return {
        "aid": arr.aid,
        "vector": vec,
        "counts": counts(vec),
        "hop1_payment": arr.hop1_payment,
        "hop1_scored": False,
        "basis": arr.basis,
    }


# --- step 1: the pool-level metric -------------------------------------

def pool_fraction(record):
    """Fraction of an assessor's funding originating from sources that also
    fund, hold equity in, or are governed by parties holding equity in, the
    assessed sector.

    `record` is a list of (amount, coupled) pairs; `coupled` is True, False,
    or the UNDECLARED sentinel. Returns None for an empty record and for a
    record carrying an UNDECLARED source -- neither is a fraction of zero.
    A zero here is a measurement: every source is declared and none is
    coupled.
    """
    if not record:
        return None
    total = 0.0
    coupled = 0.0
    for amount, flag in record:
        if flag == UNDECLARED:
            return None
        if amount is None or amount < 0:
            return None
        total += amount
        if flag:
            coupled += amount
    if total <= 0:
        return None
    return coupled / total


def field_distribution(records, complete_field=False):
    """The order: 'Apply to ALL assessors in a field, not selectively -- the
    output is a distribution, not an accusation.'

    That is a refusal here: a caller that has not declared the set to be the
    whole field gets SelectiveApplication, not a number. [CHOICE 5]
    """
    if not complete_field:
        raise SelectiveApplication(
            "pool_fraction is a distribution over a field. Declare "
            "complete_field=True or do not compute it.")
    vals = []
    undet = 0
    for rid, rec in sorted(records.items()):
        v = pool_fraction(rec)
        if v is None:
            undet += 1
        else:
            vals.append((rid, v))
    return {"n": len(records), "determined": len(vals),
            "not_determinable": undet,
            "values": sorted(v for _r, v in vals),
            "by_id": dict(vals)}


CHOICES[5] = ("field_distribution refuses to run on a set the caller has "
              "not declared complete. The order's rule is that the output "
              "is a distribution over a field, and a selected subset with "
              "the same arithmetic is a different object.")


# --- constructed controls ----------------------------------------------

def _controls(path=ORDER):
    ids = condition_ids(path)
    out = []
    out.append(arrangement(
        "ctl_all_pass", dict((n, PASSES) for n in ids), FAILS,
        "constructed: every condition met, and the assessed DOES pay -- "
        "the reachable negative for a scorer that never clears anything, "
        "and the case that shows hop-1 moves the vector by nothing"))
    out.append(arrangement(
        "ctl_all_fail", dict((n, FAILS) for n in ids), PASSES,
        "constructed: no condition met, and no payment runs between the "
        "parties -- the order's stated case, a clean hop-1 over a "
        "structure that is not independent"))
    out.append(arrangement(
        "ctl_unverifiable", dict((n, UNVERIFIABLE_AS_STATED) for n in ids),
        UNDECLARED,
        "constructed: every condition carries no standard defining what it "
        "would require, so none is failed and none is met"))
    out.append(arrangement(
        "ctl_silent", {}, UNDECLARED,
        "constructed: nothing declared at all; every condition UNDECLARED "
        "and no state read from the silence"))
    return out


def controls(path=ORDER):
    return _controls(path)


def _fmt(v):
    return "--" if v is None else str(v)


def render(path=ORDER):
    conds = conditions(path)
    lines = []
    lines.append("WO-6 INDEPENDENCE CONDITIONS -- parsed from WORK_ORDER.md")
    lines.append("")
    lines.append("hop-1 (does the assessed pay the assessor) is a ROUTING")
    lines.append("question and is carried, not scored. [CHOICE 1]")
    lines.append("No index is emitted. [CHOICE 4]")
    lines.append("")
    for c in conds:
        lines.append("  %d  %s" % (c.n, c.title))
    lines.append("")
    lines.append("CONSTRUCTED ARRANGEMENTS (no party is named; the schema")
    lines.append("has no field for one)")
    lines.append("")
    hdr = "%-18s %s %-5s %-5s %-5s %-5s %s" % (
        "arrangement", "".join("%d" % c.n for c in conds),
        "pass", "fail", "unver", "undcl", "hop-1")
    lines.append(hdr)
    key = {PASSES: "P", FAILS: "F", UNVERIFIABLE_AS_STATED: "U",
           UNDECLARED: "."}
    for arr in _controls(path):
        r = report(arr, path)
        row = "".join(key[r["vector"][c.n]] for c in conds)
        cc = r["counts"]
        lines.append("%-18s %s %-5d %-5d %-5d %-5d %s"
                     % (r["aid"], row, cc[PASSES], cc[FAILS],
                        cc[UNVERIFIABLE_AS_STATED], cc[UNDECLARED],
                        r["hop1_payment"]))
    lines.append("")
    lines.append("key  P passes   F fails   U unverifiable as stated   "
                 ". undeclared")
    lines.append("")
    vec = stated_position(path)
    cc = counts(vec)
    lines.append("THE ORDER'S OWN READING OF THE CURRENT POSITION")
    lines.append("(parsed from the section, from public statements, carried")
    lines.append("and re-verified against nothing here)")
    lines.append("")
    lines.append("  %s" % "".join(key[vec[c.n]] for c in conds))
    lines.append("  passes %d   fails %d   unverifiable %d   undeclared %d"
                 "   of %d"
                 % (cc[PASSES], cc[FAILS], cc[UNVERIFIABLE_AS_STATED],
                    cc[UNDECLARED], cc["denominator"]))
    lines.append("")
    lines.append("  hop-1 independence recorded as stated by the sector: %s"
                 % hop1_stated(path))
    lines.append("  conditions moved by that statement: 0 -- hop-1 is not a")
    lines.append("  member of the eight. [CHOICE 1]")
    lines.append("")
    lines.append("STEP 1, the pool metric: built, NOT RUN on any field.")
    lines.append("  no funding record is held here and none is composed")
    lines.append("  from memory; field_distribution refuses a set not")
    lines.append("  declared complete. [CHOICE 5]")
    return "\n".join(lines) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "conditions is a library and a render; the checks live in "
            "assessor-coupling/test_assessor.py -- run "
            "python3 assessor-coupling/test_assessor.py\n")
        return 2
    if "--choices" in argv:
        for n in sorted(CHOICES):
            sys.stdout.write("[CHOICE %d] %s\n" % (n, CHOICES[n]))
        return 0
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
