#!/usr/bin/env python3
"""P1 -- DEPENDENCY RECORDS. Records, not prose.

The order's move, stated as one operation: any outcome -> its
preconditions. For a result, enumerate what it REQUIRED that is absent
from its own argument -- instruments, calibration chains, inherited
methods, materials, infrastructure -- and give each entry a SOURCE.

The schema carries the order's rule as a REFUSAL rather than a flag:

    a requirement with no source does not enter the record.

`Requirement` raises `SourceMissing` on construction. That is the one
place the order is unambiguous ("Each entry needs a SOURCE"), and an
admitted-but-flagged entry is a record that can be cited with the flag
dropped. What cannot be enforced is whether the source SAYS what the
entry says it says; that is a reading, it is not checked here, and it is
where this part is weakest.

Two fields per entry are kept apart and neither is derived from the
other:

    kind                 INSTRUMENT / CALIBRATION / METHOD / MATERIAL /
                         INFRASTRUCTURE; a closed set, and an entry
                         outside it is refused rather than filed under
                         a nearest neighbour.
    absent_from_argument True when the published argument does not
                         state the requirement. DECLARED per entry, not
                         inferred: deciding from the text whether an
                         argument states a precondition is a reading,
                         and a word list doing it would be the failure
                         this whole folder is about.

The readout is `unstated_fraction` -- absent_from_argument over total.
An empty record returns None, never 0.0: zero would read as an argument
that stated every precondition it has, which is the one conclusion an
empty record cannot support.

PIPELINE: NOT RUN. The order names open-access methods sections as the
source. This environment's egress is an allowlist that refuses every
publisher and preprint host, so no methods section has been read and
none is paraphrased from memory. What ships is the schema, the move,
and one CONSTRUCTED record labelled as such in its own field.

    python3 p1_records.py                         # ships one record
    python3 p1_records.py --record FILE.json
    python3 p1_records.py --template

Refuses --selftest; checks live in test_proof.py.
"""

import json
import sys

import scope

KINDS = ("INSTRUMENT", "CALIBRATION", "METHOD", "MATERIAL",
         "INFRASTRUCTURE")

PROVENANCE = ("CONSTRUCTED", "READ")


class SourceMissing(ValueError):
    """Raised when a requirement is offered with no source."""


class KindError(ValueError):
    """Raised on a kind outside the closed set."""


class Requirement(object):
    """One precondition of one outcome.

    Refuses at construction rather than at report time, so a sourceless
    entry cannot sit in a record waiting to be counted.
    """

    __slots__ = ("kind", "statement", "source", "absent_from_argument")

    def __init__(self, kind, statement, source, absent_from_argument):
        if kind not in KINDS:
            raise KindError(
                "kind %r is outside the closed set %s" % (kind, KINDS))
        if not isinstance(statement, str) or not statement.strip():
            raise ValueError("statement must be non-empty")
        if not isinstance(source, str) or not source.strip():
            raise SourceMissing(
                "requirement %r has no source; the order requires one and"
                " the record does not admit it" % (statement,))
        if not isinstance(absent_from_argument, bool):
            raise ValueError(
                "absent_from_argument is declared per entry as a bool;"
                " %r is not one" % (absent_from_argument,))
        self.kind = kind
        self.statement = statement
        self.source = source
        self.absent_from_argument = absent_from_argument

    def as_dict(self):
        return {"kind": self.kind, "statement": self.statement,
                "source": self.source,
                "absent_from_argument": self.absent_from_argument}


class Record(object):
    """An outcome and its preconditions."""

    def __init__(self, outcome, provenance, requirements, scope_coding=None,
                 note=""):
        if provenance not in PROVENANCE:
            raise ValueError("provenance must be one of %s" % (PROVENANCE,))
        self.outcome = outcome
        self.provenance = provenance
        self.requirements = list(requirements)
        self.scope_coding = scope_coding
        self.note = note

    def preconditions(self):
        """THE REUSABLE MOVE: outcome -> preconditions, grouped by kind.

        Kinds with no entry appear with an empty list rather than being
        dropped, so a kind nobody looked for is visible as a zero
        instead of being absent from the report.
        """
        out = {}
        for kind in KINDS:
            out[kind] = [r.as_dict() for r in self.requirements
                         if r.kind == kind]
        return out

    def unstated_fraction(self):
        if not self.requirements:
            return None
        n = sum(1 for r in self.requirements if r.absent_from_argument)
        return float(n) / float(len(self.requirements))


def from_json(obj):
    reqs = [Requirement(r.get("kind"), r.get("statement", ""),
                        r.get("source", ""),
                        r.get("absent_from_argument"))
            for r in obj.get("requirements", [])]
    return Record(obj.get("outcome", ""), obj.get("provenance", "CONSTRUCTED"),
                  reqs, obj.get("scope"), obj.get("note", ""))


TEMPLATE = {
    "outcome": "the result as its authors state it",
    "provenance": "READ",
    "note": "where the methods section was read",
    "requirements": [
        {"kind": "INSTRUMENT", "statement": "", "source": "",
         "absent_from_argument": True},
    ],
    "scope": {"C1": None, "C2": None, "C3": None, "C4": None},
}

DEMO = {
    "outcome": ("a reported mass difference between two samples, stated "
                "to four significant figures"),
    "provenance": "CONSTRUCTED",
    "note": ("CONSTRUCTED. Written here to show the move and the "
             "refusal. No methods section was read: every host the "
             "order's pipeline names refuses CONNECT in this "
             "environment. Each source field below points at this file, "
             "which is what a source field looks like when the thing it "
             "would point at was not reachable."),
    "requirements": [
        {"kind": "INSTRUMENT",
         "statement": "a balance resolving below the reported difference",
         "source": "constructed: p1_records.py DEMO",
         "absent_from_argument": True},
        {"kind": "CALIBRATION",
         "statement": ("a mass standard the reporting laboratory does not "
                       "own, traceable to a definition it did not set"),
         "source": "constructed: p1_records.py DEMO",
         "absent_from_argument": True},
        {"kind": "METHOD",
         "statement": ("a weighing procedure inherited rather than derived "
                       "in the paper, including the buoyancy correction"),
         "source": "constructed: p1_records.py DEMO",
         "absent_from_argument": True},
        {"kind": "MATERIAL",
         "statement": "reference samples prepared by a third party",
         "source": "constructed: p1_records.py DEMO",
         "absent_from_argument": True},
        {"kind": "INFRASTRUCTURE",
         "statement": ("a temperature-stable room, mains power, and a "
                       "numeric library implementing IEEE-754"),
         "source": "constructed: p1_records.py DEMO",
         "absent_from_argument": True},
        {"kind": "METHOD",
         "statement": ("the statistical test named in the paper's own "
                       "results section"),
         "source": "constructed: p1_records.py DEMO",
         "absent_from_argument": False},
    ],
    "scope": {"C1": False, "C2": False, "C3": True, "C4": False},
}


def render(record):
    lines = []
    lines.append("P1 DEPENDENCY RECORDS")
    lines.append("")
    lines.append("  outcome:    %s" % record.outcome)
    lines.append("  provenance: %s" % record.provenance)
    if record.note:
        lines.append("  note:       %s" % record.note)
    lines.append("")
    pre = record.preconditions()
    for kind in KINDS:
        rows = pre[kind]
        lines.append("  %s (%d)" % (kind, len(rows)))
        if not rows:
            lines.append("      -- none recorded; a kind nobody looked for")
            lines.append("         reads as a zero here, not as an absence")
        for r in rows:
            mark = "absent from argument" if r["absent_from_argument"] \
                else "stated in argument"
            lines.append("      %s" % r["statement"])
            lines.append("          source: %s" % r["source"])
            lines.append("          %s" % mark)
        lines.append("")
    frac = record.unstated_fraction()
    lines.append("  unstated_fraction: %s"
                 % ("--  (empty record; no reading, not a zero)"
                    if frac is None else "%.4f" % frac))
    lines.append("")
    lines.append("  The move: outcome -> preconditions. It is reusable")
    lines.append("  because it asks what the result REQUIRED, not whether")
    lines.append("  the result is right. A requirement with no source does")
    lines.append("  not enter the record at all.")
    lines.append("")
    lines.append("  PIPELINE: NOT RUN. Open-access methods sections are the")
    lines.append("  order's source and no host serving them is reachable")
    lines.append("  from this environment. Nothing here is a statement")
    lines.append("  about any published result.")
    lines.append("")
    if record.scope_coding:
        sr = scope.code(record.scope_coding)
        lines.append("  scope coding (C1-C4): %s" % sr["verdict"])
        lines.append("  %s" % sr["reading"])
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "p1_records.py does not carry its own checks.\n"
            "Run: python3 test_proof.py\n")
        return 2
    if "--choices" in argv:
        sys.stdout.write(
            "p1_records.py declares no [CHOICE]: the kind set, the source\n"
            "rule and the absent_from_argument field are the order's.\n")
        return 0
    if "--template" in argv:
        sys.stdout.write(json.dumps(TEMPLATE, indent=1, sort_keys=True) + "\n")
        return 0
    obj = DEMO
    for i, a in enumerate(argv):
        if a == "--record" and i + 1 < len(argv):
            with open(argv[i + 1], "r", encoding="utf-8") as fh:
                obj = json.load(fh)
    sys.stdout.write(render(from_json(obj)) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
