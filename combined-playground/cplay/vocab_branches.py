"""G5 item 12: vocabulary mapping rows, three branches side by side, no winner (9c VOID-12, BRANCHED).

V-A  EXACT TERM   same label string.
V-B  DEFINITION   the two definitions match under the TOOL_CARDS rule (tools/check_cards.py):
                  VERBATIM (one is a substring of the other) or WRAP_COLLAPSED (substring once
                  runs of whitespace are collapsed). norm() is imported from that checker.
V-C  STRUCTURE    same predicate and same slots (wordslots place-table style).

DECIDED on evidence (2026-11-18): the mapping relation is V-C, tiered --
  MAPS     same predicate, same slots
  PARTIAL  same predicate, slots differ (the mapping row must name the slot correspondence)
  HOMONYM  same label (V-A) with no shared predicate: the label match is not a mapping
  NONE     different label, different predicate
V-A and V-B stay as columns. Open: predicates are assigned by a single reader (this build); a
blind second-reader predicate assignment has not been run.

Every definition is quoted from its source and pinned (repo, commit, path, sha256, one-line
anchor), checked with pins.resolve. Predicates are declared readings, written here; slots are
read from code where the code names them (marked slots_from), else declared.
Pairs: TAF glossary / unified_audit <-> COMBINED_SPEC / cplay <-> formula-audit numcheck labels.
"""
import importlib.util
import inspect
import os
from collections import namedtuple

from . import axes as A
from . import pins as P
from . import tokens as T

_here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_spec = importlib.util.spec_from_file_location("_check_cards", os.path.join(_here, "tools", "check_cards.py"))
_cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cc)
norm = _cc.norm

Term = namedtuple("Term", "term_id label definition predicate slots slots_from pin")

TAF = ("thermodynamic-accountability-framework", "16285cccdd48d608067b9bca50bd6ac683fe860a")
TAF_GLOSS = "412ed3abf4c2a546fe16def60fcb223bd496e4f297db995fcfb7232ad56c712b"
SIM = "9658b3ee64892ab375b201a9dcd376180a503417"
SPEC_SHA = "b42e23b4c9327aef6ac056561a50753f4928b4b836c74f89bf801264ff35b357"
TOK_SHA = "8c43890bf90ab49931a3947ff420b00368e5ce23ed82f8e57bd7aec3be6337e6"
CLO_SHA = "827d681c8b08003519a60967d3b61ef891254a38bb8c02e29cacba51633c3188"
FA = ("formula-audit", "4345de69c19429a876f5b16aaf32666a1b00db59")
NUM_SHA = "f6df0dc196f5ac273f864f1cab1a5a0d6c67fa88eaba53ca822f94412fb7fd83"
TAF_EXPIRY = tuple(T.TAF_EXPIRY_KEYS)


def _pin(tid, repo, commit, path, sha, anchor):
    return P.Pin("V12-" + tid, 12, repo, commit, path, sha, anchor, "item 12 definition source")


def _taf(tid, label, d, pred, slots, sf, anchor, path="docs/glossary.md", sha=TAF_GLOSS):
    return Term("taf:" + tid, label, d, pred, slots, sf, _pin(tid, TAF[0], TAF[1], path, sha, anchor))


def _cp(tid, label, d, pred, slots, sf, path, sha, anchor):
    return Term("cplay:" + tid, label, d, pred, slots, sf, _pin(tid, "Simulators", SIM, path, sha, anchor))


def _fa(tid, label, d, pred, slots):
    return Term("fa:" + tid, label, d, pred, slots, "declared",
                _pin(tid, FA[0], FA[1], "numcheck/check.py", NUM_SHA, d))


_ABS_PARAMS = tuple(inspect.signature(T.absent_at_sensitivity).parameters)

TERMS = (
    _taf("GAP_INSTRUMENT_CRASH", "GAP_INSTRUMENT_CRASH",
         "A module raised; nothing was measured. Coverage, not severity (#82 sense)",
         "a check raised; recorded on coverage, never severity",
         ("kind", "module", "input", "reason", "missing_path", "expiry_condition"),
         "code: unified_audit.py lines 337-342",
         "A module raised; nothing was measured. Coverage, not severity (#82 sense)"),
    _cp("CRASHED", "CRASHED", "did not run: the check raised",
        "a check raised; recorded on coverage, never severity",
        tuple(A.CoverageEntry._fields), "code: cplay axes.CoverageEntry (crash() fills it)",
        "playground-crossrun/COMBINED_SPEC.md", SPEC_SHA, "did not run: the check raised"),
    _taf("UNKNOWN", "UNKNOWN",
         "A slot whose value is not yet known. Never read as zero or as absent.",
         "value not yet known, held open with an exit", ("expiry_condition",) + TAF_EXPIRY,
         "code: expiry_register.py EXPIRY_KEYS",
         "A slot whose value is not yet known. Never read as zero or as absent."),
    _cp("UNKNOWN", "UNKNOWN",
        "UNKNOWN requires a typed expiry trigger",
        "value not yet known, held open with an exit", ("reason", "triggers", "kind", "target", "condition"),
        "declared: cplay tokens.unknown + ExpiryTrigger",
        "playground-crossrun/COMBINED_SPEC.md", SPEC_SHA, "UNKNOWN requires a typed expiry trigger"),
    _taf("ABSENT_AT_SENSITIVITY", "ABSENT_AT_SENSITIVITY",
         "Scoped absence: looked for with a stated instrument / sensitivity / protocol and not found at "
         "that sensitivity. Never written as bare \"absent\". No slot holds it yet.",
         "scoped absence: not found at a stated sensitivity", ("instrument_class", "sensitivity", "protocol"),
         "declared from the definition's three named slots",
         "Scoped absence: looked for with a stated instrument / sensitivity / protocol"),
    _cp("ABSENT_AT_SENSITIVITY", "ABSENT_AT_SENSITIVITY",
        "ABSENT_AT_SENSITIVITY must carry three things, or it is refused (F7):",
        "scoped absence: not found at a stated sensitivity", _ABS_PARAMS,
        "code: cplay tokens.absent_at_sensitivity signature",
        "playground-crossrun/COMBINED_SPEC.md", SPEC_SHA, "must carry three things, or it is refused (F7):"),
    _taf("expiry_condition", "expiry_condition",
         "Instrument class, sensitivity or protocol whose null result would downgrade a PENDING / UNKNOWN "
         "slot.", "the exit of an open slot", TAF_EXPIRY, "code: expiry_register.py EXPIRY_KEYS",
         "Instrument class, sensitivity or protocol whose null result would downgrade a PENDING / UNKNOWN"),
    _cp("ExpiryTrigger", "ExpiryTrigger",
        "Typed: kind, target, condition all required.", "the exit of an open slot",
        ("kind", "target", "condition"), "code: cplay tokens.ExpiryTrigger",
        "combined-playground/cplay/tokens.py", TOK_SHA, "Typed: kind, target, condition all required."),
    _fa("VOID", "VOID", "units not PASS, a missing or unreadable value, no value on",
        "the check could not be evaluated on these inputs", ("reason",)),
    _cp("VOID", "VOID", "VOID in the spec, so VOID here (never a default):",
        "a value the spec leaves open, held with a reason", ("reason",), "code: cplay tokens.Token",
        "combined-playground/cplay/tokens.py", TOK_SHA, "VOID in the spec, so VOID here (never a default):"),
    _fa("UNDECIDED", "UNDECIDED", "D straddles the edge at the last tier",
        "an uncertain difference straddles a tolerance edge", ("D", "t")),
    _cp("UNRESOLVED", "UNRESOLVED", "otherwise UNRESOLVED (inside the",
        "an uncertain difference straddles a tolerance edge", ("m", "tol", "U"),
        "declared: verdict_branch_G inputs", "combined-playground/cplay/closure.py", CLO_SHA,
        "otherwise UNRESOLVED (inside the"),
    _fa("HOLDS", "HOLDS", "D lies inside [-t, t]", "a difference lies inside its tolerance", ("D", "t")),
    _cp("OK", "OK", "ran and passed", "a check ran and passed", (), "declared: axes.reading OK carries no slot",
        "playground-crossrun/COMBINED_SPEC.md", SPEC_SHA, "ran and passed"),
    _cp("CLOSED_WITHIN", "CLOSED_WITHIN", "closure holds within sigma, not exactly",
        "a difference lies inside its tolerance", ("sigma", "basis"), "code: axes.reading CLOSED_WITHIN",
        "playground-crossrun/COMBINED_SPEC.md", SPEC_SHA, "closure holds within sigma, not exactly"),
)

PAIRS = (("taf:GAP_INSTRUMENT_CRASH", "cplay:CRASHED"), ("taf:UNKNOWN", "cplay:UNKNOWN"),
         ("taf:ABSENT_AT_SENSITIVITY", "cplay:ABSENT_AT_SENSITIVITY"),
         ("taf:expiry_condition", "cplay:ExpiryTrigger"), ("fa:VOID", "cplay:VOID"),
         ("fa:UNDECIDED", "cplay:UNRESOLVED"), ("fa:HOLDS", "cplay:OK"), ("fa:HOLDS", "cplay:CLOSED_WITHIN"))


def term(tid):
    return next(t for t in TERMS if t.term_id == tid)


def va(a, b):
    return a.label == b.label


def vb_text(x, y):
    if x in y or y in x:
        return True                         # VERBATIM
    nx, ny = norm(x), norm(y)
    return nx in ny or ny in nx             # WRAP_COLLAPSED


def vb(a, b):
    return vb_text(a.definition, b.definition)


def vc(a, b):
    return a.predicate == b.predicate and tuple(a.slots) == tuple(b.slots)


TIERS = ("MAPS", "PARTIAL", "HOMONYM", "NONE")
PREDICATE_STATUS = ("single reader: predicates declared by the building session; a blind second-reader "
                    "assignment is open")


def relation(a, b):
    if a.predicate == b.predicate:
        return "MAPS" if tuple(a.slots) == tuple(b.slots) else "PARTIAL"
    return "HOMONYM" if va(a, b) else "NONE"


def table():
    rows = []
    for x, y in PAIRS:
        a, b = term(x), term(y)
        got = {"V-A": va(a, b), "V-B": vb(a, b), "V-C": vc(a, b)}
        rows.append(dict(pair="%s | %s" % (a.label, b.label), left=x, right=y,
                         same_predicate=a.predicate == b.predicate, relation=relation(a, b),
                         split=len(set(got.values())) > 1, **got))
    return rows


def render():
    yn = lambda v: "maps" if v else "--"
    out = ["DECIDED on evidence: relation = V-C tiered (MAPS / PARTIAL / HOMONYM / NONE)",
           "pair                                           V-A label  V-B defn  V-C exact  same pred  relation  SPLIT"]
    for r in table():
        out.append("%-46s %-10s %-9s %-10s %-10s %-9s %s" % (r["pair"], yn(r["V-A"]), yn(r["V-B"]), yn(r["V-C"]),
                                                         "yes" if r["same_predicate"] else "no", r["relation"],
                                                         "SPLIT" if r["split"] else ""))
    out.append("SPLIT (branches disagree): " + ", ".join(r["pair"] for r in table() if r["split"]))
    out.append("predicates are declared readings; slots marked code are read from the source")
    out.append("open: %s" % PREDICATE_STATUS)
    return "\n".join(out)


if __name__ == "__main__":
    print(render())
