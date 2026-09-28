# SPDX-License-Identifier: CC0-1.0
"""question_space.py -- FWO-9. Per conversion point, the class of question that
stops being askable there. Records where the door is; estimates no loss.

    python3 question_space.py            the column over every conversion point known to FWO-5/6/8/13
    python3 question_space.py --choices  every [CHOICE n] in force
    python3 test_single_channel.py       the checks; this module refuses --selftest

The conversion points are IMPORTED: FWO-5's six (dependency_chain_audit.CONVERSION_POINTS)
plus the tax step FWO-13 registers as its own row type (tax_step.TAX_STEP).  The
classes are the order's five candidates, PROPOSED, with the fifth carried from the
operator's material (OBSERVED).  Every cell is a DECLARED list of classes or the
string UNKNOWN; nothing here derives a cell from text, and nothing here computes a
quantity of questions lost -- the test walks the AST for any function whose name
carries loss / estimate / count and for any arithmetic over a cell.

KEY-HOLDER STATUS
    EXPECTED E9.2 was committed before this file.  The declarations below are this
    session's; rule 2 (external SOURCE) is not met and any hold is scored with that
    said.  fail_fixture() is a column in which `credential` closes nothing, so E9.2
    can be shown to fail.

Stdlib only. Parses under Python 3.8. No network. CC0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import dependency_chain_audit as D  # noqa: E402
import tax_step as T                 # noqa: E402

UNKNOWN = "UNKNOWN"

# id, class, provenance
CLASSES = (
    ("Q1", "instrument needing no funder", "PROPOSED"),
    ("Q2", "result with no product downstream", "PROPOSED"),
    ("Q3", "timescale longer than any grant or contract cycle", "PROPOSED"),
    ("Q4", "question whose answer would reduce demand for the funder's output", "PROPOSED"),
    ("Q5", "question arising only from a constraint the funded population does not live under",
     "OBSERVED (carried from the operator's material: what gets experimented on is set by which "
     "constraints the person has actually run)"),
)
CLASS_IDS = tuple(c[0] for c in CLASSES)
POINTS = tuple(D.CONVERSION_POINTS) + (T.TAX_STEP,)

CHOICES = {
    1: "the conversion points are FWO-5's six plus FWO-13's tax_step, imported; no point is defined here",
    2: "a cell is a declared list of class ids or UNKNOWN; an empty list means 'declared: closes none', kept apart from UNKNOWN",
    3: "no cell derives from text and no number of questions is emitted; the column records where the door is",
}


class ColumnError(ValueError):
    """A declaration the schema refuses; the message names the field."""


def declare(point, classes, basis):
    """One cell. classes is a list of class ids, or the string UNKNOWN."""
    if point not in POINTS:
        raise ColumnError("conversion point %r not in %s" % (point, POINTS))
    if not isinstance(basis, str) or not basis.strip():
        raise ColumnError("basis is required on every cell")
    if classes == UNKNOWN:
        return {"point": point, "closes": UNKNOWN, "basis": basis}
    if not isinstance(classes, (list, tuple)):
        raise ColumnError("classes is a list of ids or UNKNOWN")
    bad = [c for c in classes if c not in CLASS_IDS]
    if bad:
        raise ColumnError("unknown class id(s) %s; the vocabulary is %s" % (bad, CLASS_IDS))
    if len(set(classes)) != len(classes):
        raise ColumnError("a class id appears twice under %r" % point)
    return {"point": point, "closes": sorted(classes), "basis": basis}


def column(cells):
    """Every point, once; a point with no cell is refused (an absence is declared, not implied)."""
    by = {}
    for c in cells:
        if "loss" in c or "estimate" in c:
            raise ColumnError("a cell carries a loss estimate; the tool records where the door is [CHOICE 3]")
        if c["point"] in by:
            raise ColumnError("point %r declared twice" % c["point"])
        by[c["point"]] = c
    missing = [p for p in POINTS if p not in by]
    if missing:
        raise ColumnError("no cell for %s" % missing)
    return [by[p] for p in POINTS]


# ------------------------------------------------------- the declared column ---
# PROPOSED; this session's readings, with the basis in place.

def demo_column():
    return column([
        declare("account", ["Q1"],
                "a question needing an instrument with no funder is not askable where the unit of account is "
                "what the instrument is bought in; the other classes are not closed at the account step itself"),
        declare("settlement", ["Q1", "Q3"],
                "settlement in the dominant token is where a funder becomes necessary and where the cycle it "
                "funds on sets the longest answerable timescale"),
        declare("input_purchase", ["Q2"],
                "an input bought against a line item has to lead to the deliverable the line was opened for; a "
                "result with nothing downstream has no line"),
        declare("credential", ["Q5", "Q4"],
                "the credential selects for a population that lived under the credentialing constraints; a "
                "question from a constraint that population did not run has no one credentialed to ask it, and "
                "a question reducing demand for the credential's issuer is not on the syllabus"),
        declare("publication", ["Q2", "Q5", "Q4"],
                "a venue takes a product; a result with none is not a submission; the venue's reviewers are the "
                "funded population; a result reducing demand for the venue's field is refereed by that field"),
        declare("tax", ["Q1"],
                "the tax step converts a non-monetary route into a monetary obligation, so an instrument that "
                "needed no funder acquires one at the tax step"),
        declare(T.TAX_STEP, UNKNOWN,
                "the tax step's own row type is registered in FWO-13 with two OBSERVED appearances and one "
                "candidate; which question classes it closes beyond 'tax' above is not declared here"),
    ])


def fail_fixture():
    """CONSTRUCTED: a column in which `credential` closes nothing, so E9.2 fails on it."""
    cells = demo_column()
    out = []
    for c in cells:
        if c["point"] == "credential":
            out.append(declare("credential", [], "CONSTRUCTED fail fixture: declared to close none"))
        else:
            out.append(c)
    return column(out)


def check_expectations(cells):
    by = dict((c["point"], c["closes"]) for c in cells)

    def has(p, q):
        return by[p] != UNKNOWN and q in by[p]
    rows = [
        ("E9.2 Q5 attaches to credential and publication", has("credential", "Q5") and has("publication", "Q5")),
        ("E9.2 tax closes Q1", has("tax", "Q1")),
        ("E9.2 input_purchase closes Q2", has("input_purchase", "Q2")),
    ]
    return [(l, "MATCH" if v else "MISMATCH") for l, v in rows]


def render(out=None):
    out = out or sys.stdout
    w = out.write
    w("question_space -- FWO-9; per conversion point, the classes of question that stop being askable there\n")
    w("records where the door is; no quantity of questions is estimated [CHOICE 3]; every cell this session's declaration\n\n")
    w("classes:\n")
    for cid, text, prov in CLASSES:
        w("   %s  %-84s %s\n" % (cid, text, prov))
    w("\n%-16s %-16s %s\n" % ("point", "closes", "basis"))
    for c in demo_column():
        closes = c["closes"] if c["closes"] == UNKNOWN else (",".join(c["closes"]) or "none (declared)")
        w("%-16s %-16s %s\n" % (c["point"], closes, c["basis"]))
    w("\n")
    for l, v in check_expectations(demo_column()):
        w("expected %-60s %s\n" % (l, v))
    w("fail fixture (CONSTRUCTED): %s\n" % check_expectations(fail_fixture())[0][1])
    w("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_single_channel.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
