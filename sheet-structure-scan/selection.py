#!/usr/bin/env python3
"""
selection -- work order 7 S1. The eligibility screen, and the reject log.

NAMED `selection`, NOT `select`. The obvious name collides with a stdlib
module: `import select` resolves to the standard library from anywhere
whose sys.path does not put this directory first, so the collision is
silent and intermittent -- it worked when run as a script and failed the
first time it was imported. Caught by running it, not by reading it.

WHAT S1b ASKS FOR AND WHAT EXISTED. Criterion (b) is "provenance prose
classified RETROSPECTIVE under the amended WO4 test". No such test was
in the code: SSS_043 drew the retrospective/prospective distinction in
PROSE, from two workbooks, and nothing implemented it. `RETROSPECTIVE`
and `PROSPECTIVE` appear zero times in this folder before this file.
So the screen's second criterion named an instrument that did not exist
-- the MF_017 / CW_015 / DL_004 / GC_012 shape, sixth instance here --
and building it is most of this order's work.

THE TRAP THE CLASSIFIER HAS TO AVOID. The easy implementation of (b) is
"does any prose cell yield a resolvable relationship", which is (c). Two
criteria computing one quantity is a weld: the screen would look like
two independent gates and be one. So (b) reads STANCE -- who the sentence
is addressed to and what tense it is in -- and (c) reads RESOLVABILITY,
and `independence()` reports whether they have ever been observed
disagreeing. On the two workbooks in hand they have not, which is a
statement about n=2 and is printed as one.

WHAT THIS FILE DOES NOT DO. It does not go looking for candidates. The
publisher hosts are refused by this environment's allowlist (probe in
the reject log, with timestamps), and trawling third-party repositories
on a reachable host is outside this session's scope. Candidates are
handed to it; it screens them and records why each was rejected.

CC0. stdlib only. Parses under Python 3.9.
"""

import json
import os
import re
import sys

import scan4
import sheetmodel

_HERE = os.path.dirname(os.path.abspath(__file__))
from sheetmodel import CONSTANT_NUMBER, CONSTANT_DATE, CONSTANT_TEXT, DERIVED

RETROSPECTIVE = "RETROSPECTIVE"
PROSPECTIVE = "PROSPECTIVE"
NEITHER = "NEITHER"
UNDETERMINED = "UNDETERMINED"

# ---- S1b. The stance test, built here because it did not exist. -------
#
# RETROSPECTIVE prose describes how a value ALREADY IN THE FILE was
# produced. PROSPECTIVE prose tells a filer what to write. The markers
# are about address and tense, deliberately NOT about whether operands
# resolve -- that is criterion (c) and welding them would make the screen
# one gate wearing two names.

# Second person, imperative, and the empty-prompt shape. A colon at the
# end of a short noun phrase is the strongest single marker of a form
# field and is handled separately below.
_PROSPECTIVE_MARKERS = [
    r"\bplease\b", r"\byou (?:used|use|may|should|will|must|can)\b",
    r"\byour\b", r"\benter\b", r"\bfill in\b", r"\bcomplete the\b",
    r"\bdescribe\b", r"\bdescription of\b", r"\bprovide\b",
    r"\breport the\b", r"\bindicate\b", r"\bspecify\b", r"\bselect\b",
    r"\battach\b", r"\bsubmit\b", r"\bis required to be\b",
    r"\bif applicable\b", r"\bas appropriate\b", r"\bleave blank\b",
]
# Descriptive of an existing value's origin.
_RETROSPECTIVE_MARKERS = [
    r"\baverage of\b", r"\bmean of\b", r"\bsum of\b", r"\btotal of\b",
    r"\bcalculated as\b", r"\bcalculated from\b", r"\bderived from\b",
    r"\bbased on\b", r"\btaken from\b", r"\bsourced from\b",
    r"\bassumed to be\b", r"\bwas (?:computed|calculated|taken|derived)\b",
    r"\bthese (?:values|factors|figures) (?:are|were)\b",
    r"\bupper quartile\b", r"\blower quartile\b", r"\bmedian of\b",
    r"\bweighted by\b", r"\bexcludes?\b.*\bfrom the (?:average|mean)\b",
]
_PROSPECTIVE_RE = [re.compile(p, re.I) for p in _PROSPECTIVE_MARKERS]
_RETROSPECTIVE_RE = [re.compile(p, re.I) for p in _RETROSPECTIVE_MARKERS]

# A label ending in a colon with nothing after it is a form field. This
# is the LGO shape ("Description of computational method:") and it is
# the marker with the fewest false friends.
_FORM_FIELD = re.compile(r"^[^:]{3,80}:\s*$")


def classify_stance(text):
    """RETROSPECTIVE / PROSPECTIVE / NEITHER for one prose cell.

    NEITHER is a real answer, not a failure: most prose in a workbook is
    a heading or a definition and is addressed to nobody about nothing.
    Counting it as prospective would make every workbook prospective.
    """
    t = (text or "").strip()
    if not t:
        return NEITHER
    r = sum(1 for p in _RETROSPECTIVE_RE if p.search(t))
    p_ = sum(1 for p in _PROSPECTIVE_RE if p.search(t))
    if _FORM_FIELD.match(t):
        p_ += 2
    if r and r >= p_:
        return RETROSPECTIVE
    if p_:
        return PROSPECTIVE
    return NEITHER


def stance_of_workbook(wb, min_retro=1):
    """A workbook's stance, plus the counts it rests on.

    A workbook is RETROSPECTIVE if any provenance prose cell is. One is
    enough by construction: the question the scan asks is whether the
    file states a relationship about its own values, and one such
    statement is a testable relationship. The threshold is named so it
    can be argued with.
    """
    sheets = scan4.provenance_sheets(wb)
    counts = {RETROSPECTIVE: 0, PROSPECTIVE: 0, NEITHER: 0}
    examples = {}
    for sh, _why in sheets:
        for c in scan4.prose_cells(wb, sh):
            s = classify_stance(str(c.value))
            counts[s] += 1
            examples.setdefault(s, (c.ref(), str(c.value)[:90]))
    if not sheets:
        return UNDETERMINED, counts, examples, sheets
    if counts[RETROSPECTIVE] >= min_retro:
        return RETROSPECTIVE, counts, examples, sheets
    if counts[PROSPECTIVE]:
        return PROSPECTIVE, counts, examples, sheets
    return NEITHER, counts, examples, sheets


# ---- S1a. Ships values rather than being a blank template. ------------

def ships_values(wb):
    """(bool, detail). A template's numeric cells are formulas over
    empty inputs; a data-shipping workbook holds numbers of its own.

    Counted on CONSTANT_NUMBER, not on DERIVED: a formula is a
    relationship, and a workbook of formulas over nothing is exactly the
    blank template this criterion exists to exclude. Both UNFCCC and LGO
    are unfilled by their INPUT cells (SSS_026), and they differ here --
    UNFCCC ships 789 reference constants, LGO ships zero.
    """
    n_num = sum(1 for c in wb.cells.values()
                if c.kind in (CONSTANT_NUMBER, CONSTANT_DATE))
    n_der = sum(1 for c in wb.cells.values() if c.kind == DERIVED)
    return n_num > 0, {"constant_numbers": n_num, "derived": n_der,
                       "cells": len(wb.cells)}


# ---- S1c. At least one relationship whose operands resolve. -----------

def resolvable_relationships(wb, tolerance=scan4.DEFAULT_TOLERANCE):
    """(count, detail). Uses scan 4's own extractor, unchanged.

    Deliberately the SAME machinery the scan will run, so a file that
    passes this screen cannot then produce zero testable relationships
    -- which is exactly what happened to WO6's candidate after it was
    already chosen (SSS_042).
    """
    res = scan4.scan(wb, tolerance)
    testable = [r for r in res["rows"] if r["bin"] != scan4.NOT_TESTABLE]
    return len(testable), {"prose_cells": res["prose_cells"],
                           "not_arithmetic": res["not_arithmetic"],
                           "rows": len(res["rows"]),
                           "testable": len(testable)}


# ---- the screen -------------------------------------------------------

PRIOR_BODIES = ("UNFCCC", "The Climate Registry")
PRIOR_DATES = ("2021-05-25", "2016-05-02")


def screen(path, body=None, min_retro=1, tolerance=scan4.DEFAULT_TOLERANCE):
    """Every criterion, in order, with every result recorded.

    The screen does NOT stop at the first failure. S1 says to record the
    reject reason, and one reason is less informative than all of them:
    a file that fails only (e) is a different candidate from one that
    fails (a), (b) and (c), and a first-failure log cannot tell them
    apart.
    """
    out = {"path": os.path.basename(path), "criteria": {}, "notes": []}
    try:
        wb = sheetmodel.read(path)
    except Exception as e:
        # NO SHORT-CIRCUIT. The screen used to return here, recording one
        # criterion and none of the other five -- which SSS_053 described
        # as "records every criterion rather than stopping at the first
        # failure", true of a criterion failure and false of a reader
        # failure. Every criterion is now emitted with pass=None, which
        # is neither a pass nor a fail: the criterion was not evaluated,
        # and reporting it as failed would say the file lacks something
        # nobody looked for.
        out["criteria"]["read"] = {"pass": False, "why": str(e)[:160]}
        for k in ("a_ships_values", "b_retrospective", "c_resolvable"):
            out["criteria"][k] = {
                "pass": None,
                "why": "NOT EVALUATED: this criterion takes a reader that "
                       "opened the file, and none did"}
        # (d) and (e) do not take a reader. (d) does take container
        # dates, which the reader supplies, so it is unevaluated too;
        # (e) is recorded from the caller and is evaluable regardless.
        out["criteria"]["d_date_separated"] = {
            "pass": None,
            "why": "NOT EVALUATED: container dates come from the reader"}
        known = body in PRIOR_BODIES if body else None
        out["criteria"]["e_different_body"] = {
            "pass": (body is not None and not known),
            "stated_body": body,
            "why": "" if (body and not known) else
                   ("authoring body not stated; recorded, not computed"
                    if body is None else
                    "same authoring body as a prior file: %s" % body)}
        out["shape_note"] = (
            "This screen is WORKBOOK-shaped. Criterion (a) reads cells and "
            "(c) reads a relationship whose operands resolve inside the "
            "file; for a prose document both are category mismatches "
            "rather than failures, so a 'not eligible' verdict is about the "
            "screen's fit, not about the file's contents.")
        out["eligible"] = False
        return out
    out["reader"] = wb.reader
    out["capabilities"] = dict(getattr(wb, "capabilities", {}))
    fd = getattr(wb, "file_dates", {}) or {}
    out["file_dates"] = fd

    ok_a, det_a = ships_values(wb)
    out["criteria"]["a_ships_values"] = {
        "pass": ok_a, "detail": det_a,
        "why": "" if ok_a else "no constant numbers: every numeric cell "
                               "is a formula over empty inputs"}

    stance, counts, examples, sheets = stance_of_workbook(wb, min_retro)
    out["criteria"]["b_retrospective"] = {
        "pass": stance == RETROSPECTIVE, "stance": stance,
        "detail": {"counts": counts,
                   "provenance_sheets": [s for s, _ in sheets]},
        "example": examples.get(stance, ("-", "-")),
        "why": "" if stance == RETROSPECTIVE else
               ("no provenance sheet located" if stance == UNDETERMINED
                else "prose is %s: it addresses a filer rather than "
                     "describing a value the file carries" % stance)}

    n_rel, det_c = resolvable_relationships(wb, tolerance)
    out["criteria"]["c_resolvable"] = {
        "pass": n_rel > 0, "detail": det_c,
        "why": "" if n_rel else "no stated relationship whose operands "
                                "resolve inside the file"}

    same_date = [d for d in (fd.get("created"), fd.get("modified"))
                 if d in PRIOR_DATES]
    out["criteria"]["d_date_separated"] = {
        "pass": not same_date and bool(fd),
        "detail": {"dates": fd, "collides_with_prior": same_date},
        "why": "" if fd and not same_date else
               ("the container records no date" if not fd else
                "shares a date with a prior file: %s" % ", ".join(same_date))}

    # (e) is not a property of the bytes. It is recorded, never computed,
    # and a screen that guessed it from an organisation string would be reading
    # a metadata field nobody verified.
    known = body in PRIOR_BODIES if body else None
    out["criteria"]["e_different_body"] = {
        "pass": (body is not None and not known),
        "stated_body": body,
        "why": "" if (body and not known) else
               ("authoring body not stated; this criterion is recorded, "
                "not computed" if body is None else
                "same authoring body as a prior file: %s" % body)}

    ts = threshold_sensitivity(wb)
    out["threshold"] = ts
    out["threshold_flips"] = ts["flips"]

    out["eligible"] = all(v.get("pass") for v in out["criteria"].values())
    return out


def threshold_sensitivity(wb):
    """How the stance verdict moves with the rule, on one workbook.

    `min_retro=1` (any retrospective sentence) is a [CHOICE] and it is
    load-bearing: on the UNFCCC calculator the counts are RETRO 4 /
    PROSP 9, so a MAJORITY rule calls it PROSPECTIVE -- and that is the
    file carrying 23 testable relationships. A rule that rejects it at
    criterion (b) would reject the only workbook this repository has
    that criterion (c) accepts.

    So the threshold is calibrated by a case rather than stipulated, and
    the case is stated. It also settles the independence question one
    way: under the any-rule (b) and (c) agree on both workbooks; under a
    majority rule they DISAGREE on UNFCCC, which is the off-diagonal
    cell. Whether the two criteria are independent is therefore a
    property of a threshold, not of the criteria.
    """
    _st, counts, _ex, sheets = stance_of_workbook(wb, 1)
    r, p_ = counts[RETROSPECTIVE], counts[PROSPECTIVE]
    return {"counts": counts,
            "any_rule": (RETROSPECTIVE if r else
                         (PROSPECTIVE if p_ else NEITHER)),
            "majority_rule": (RETROSPECTIVE if r > p_ else
                              (PROSPECTIVE if p_ else NEITHER)),
            "flips": (r > 0) and (r <= p_),
            "provenance_sheets": len(sheets)}


def independence(results):
    """Have (b) and (c) ever been observed disagreeing?

    If they never have, the screen has two names for one gate and the
    reject log cannot tell which criterion is doing the work. This is
    the MD_008 shape -- three quantities set by one hand, never observed
    varying independently -- and it is reported rather than assumed away.
    """
    cells = {}
    for r in results:
        b = r["criteria"].get("b_retrospective", {}).get("pass")
        c = r["criteria"].get("c_resolvable", {}).get("pass")
        if b is None or c is None:
            continue
        cells[(bool(b), bool(c))] = cells.get((bool(b), bool(c)), 0) + 1
    off = sum(n for k, n in cells.items() if k[0] != k[1])
    return {"cells": cells, "off_diagonal": off,
             "independent_observed": off > 0,
             "n": sum(cells.values())}


# ---- frozen parameter snapshot (S2) -----------------------------------

FROZEN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "frozen_wo6.json")


def parameter_state():
    """The values S2 freezes, read from where they live."""
    pats = {}
    pp = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "patterns.json")
    if os.path.exists(pp):
        d = json.load(open(pp))
        pats = {k: len(v) if isinstance(v, list) else v
                for k, v in sorted(d.items()) if not k.startswith("_")}
    return {
        "PROVENANCE_WORDS": list(scan4.PROVENANCE_WORDS),
        "DEFAULT_TOLERANCE": scan4.DEFAULT_TOLERANCE,
        "PROSE_MIN_CHARS": scan4.PROSE_MIN_CHARS,
        "patterns_json_counts": pats,
    }


def freeze(path=FROZEN):
    json.dump(parameter_state(), open(path, "w"), indent=2, sort_keys=True)
    return path


def frozen_check(path=FROZEN):
    """(bool, differences). S2 asks for these frozen at their WO6 values
    BEFORE the candidate is chosen, which is a claim anyone can check
    only if the values are written down. They are."""
    if not os.path.exists(path):
        return None, ["no snapshot on disk"]
    was = json.load(open(path))
    now = parameter_state()
    diffs = []
    for k in sorted(set(was) | set(now)):
        if was.get(k) != now.get(k):
            diffs.append("%s: %r -> %r" % (k, was.get(k), now.get(k)))
    return (not diffs), diffs


# ---- render -----------------------------------------------------------

CRITERIA_TEXT = {
    "a_ships_values": "(a) ships values in its own cells",
    "b_retrospective": "(b) provenance prose is RETROSPECTIVE",
    "c_resolvable": "(c) >=1 relationship whose operands resolve",
    "d_date_separated": "(d) file date separated from both priors",
    "e_different_body": "(e) different authoring body",
    "read": "reader could open the file",
}


def render(results, probe=None):
    L = ["work order 7 -- eligibility screen and reject log",
         "candidates screened: %d" % len(results),
         ""]
    ok, diffs = frozen_check()
    L += ["S2, parameters frozen at their WO6 values: %s"
          % ("unchanged" if ok else
             ("NO SNAPSHOT" if ok is None else "CHANGED")),
          ""]
    for d in diffs:
        L.append("  %s" % d)
    if diffs:
        L.append("")

    for r in results:
        L.append("%s -- %s" % (r["path"],
                               "ELIGIBLE" if r.get("eligible") else
                               "not eligible"))
        for k, v in r["criteria"].items():
            mark = ("pass" if v.get("pass") is True else
                    ("----" if v.get("pass") is False else "n/e "))
            L.append("  %-4s %-46s %s"
                     % (mark, CRITERIA_TEXT.get(k, k), v.get("why", "")))
        if r.get("shape_note"):
            L += ["", "       %s" % r["shape_note"].replace(
                ". ", ".\n       "), ""]
        b = r["criteria"].get("b_retrospective", {})
        if b.get("detail"):
            c = b["detail"]["counts"]
            L.append("       prose stance: RETRO %d  PROSP %d  NEITHER %d"
                     % (c[RETROSPECTIVE], c[PROSPECTIVE], c[NEITHER]))
            ex = b.get("example", ("-", "-"))
            L.append("       example (%s): %s | %s" % (b.get("stance"),
                                                       ex[0], ex[1]))
        L.append("")

    flips = [r for r in results if r.get("threshold_flips")]
    if flips:
        L += ["The stance threshold is a [CHOICE] and it moves the verdict.",
              "min_retro = 1 (any retrospective sentence) is what these",
              "results use. Under a MAJORITY rule the following candidates",
              "change stance, and one of them is the file that carries every",
              "testable relationship this repository has found:",
              ""]
        L.append(table(["candidate", "RETRO", "PROSP", "any rule",
                        "majority rule"],
                       [[r["path"][:44], r["threshold"]["counts"][
                           RETROSPECTIVE],
                         r["threshold"]["counts"][PROSPECTIVE],
                         r["threshold"]["any_rule"],
                         r["threshold"]["majority_rule"]] for r in flips]))
        L += ["",
              "The threshold is therefore calibrated by a case rather than",
              "stipulated: a rule that rejects that file at (b) rejects the",
              "only workbook (c) accepts.",
              ""]

    ind = independence(results)
    L += ["Criteria (b) and (c): have they been observed disagreeing?", ""]
    L.append(table(["b passes", "c passes", "candidates"],
                   [[str(k[0]), str(k[1]), n]
                    for k, n in sorted(ind["cells"].items())]))
    L += ["",
          "off-diagonal candidates: %d of %d"
          % (ind["off_diagonal"], ind["n"]),
          ""]
    if not ind["independent_observed"]:
        L += ["Not under the rule these results use. Two ways they would",
              "separate, and one is already in this table: under a MAJORITY",
              "stance rule the UNFCCC calculator is (b) PROSPECTIVE and (c)",
              "resolvable, which is the off-diagonal cell -- so whether the",
              "criteria are independent is a property of the threshold. The",
              "other is a retrospective note whose operands sit OUTSIDE the",
              "file, and no candidate here is one.",
              ""]
    if probe:
        L += ["Candidate sources, reachability probe:", ""]
        L.append(table(["host", "CONNECT"], probe))
        L += ["",
              "000 is a refused CONNECT. The publisher hosts are not",
              "reachable from this session, so S1's search over published",
              "workbooks was not run here and no candidate was rejected on",
              "its contents that this log does not show.",
              ""]
    return "\n".join(L)


def table(head, rows):
    cols = [len(str(h)) for h in head]
    for r in rows:
        for i, c in enumerate(r):
            cols[i] = max(cols[i], len(str(c)))
    out = ["  ".join(str(h).ljust(cols[i]) for i, h in enumerate(head)),
           "  ".join("-" * c for c in cols)]
    for r in rows:
        out.append("  ".join(str(c).ljust(cols[i]) for i, c in enumerate(r)))
    return "\n".join(out)


# ---- selftest ---------------------------------------------------------

def _selftest():
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-58s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("selection selftest")

    # ---- the stance classifier, on the two sentences that motivated it.
    # Known answers assigned by hand in SSS_043, before this code existed.
    ck("the UNFCCC sentence reads retrospective",
       classify_stance("Bonaire, Sint Eustatius and Saba, Bouvet Island: "
                       "Average of  American Samoa, Antigua and Barbuda"),
       RETROSPECTIVE)
    ck("the LGO sentence reads prospective",
       classify_stance("Description of computational method:"), PROSPECTIVE)
    ck("a second LGO sentence reads prospective",
       classify_stance("Please report the methods you used to convert the "
                       "activity data disclosed in Section 3."), PROSPECTIVE)

    # ---- NEITHER is a real answer. A classifier with two values calls
    # every heading in every workbook prospective.
    ck("a heading is neither", classify_stance("SCOPE 1 STATIONARY "
                                               "COMBUSTION"), NEITHER)
    ck("a definition is neither",
       classify_stance("Buildings and Other Facilities includes stationary "
                       "and fugitive emissions as well as Scope 2."),
       NEITHER)
    ck("an empty cell is neither", classify_stance(""), NEITHER)

    # ---- the trap: (b) must not be (c) in disguise. A retrospective
    # sentence whose operands are OUTSIDE the file is retro and
    # unresolvable, and that is the case that separates the criteria.
    ck("a retrospective note over external operands is still retro",
       classify_stance("Emission factors taken from the 2019 IEA world "
                       "energy balances."), RETROSPECTIVE)
    ck("and a form field over in-file names is still prospective",
       classify_stance("Enter the average of your four quarterly totals:"),
       PROSPECTIVE)

    # ---- ties go to retrospective, and that is a stated choice: a
    # sentence carrying both is describing a value AND asking for one,
    # and the describing half is what the scan can test.
    ck("a sentence with both markers resolves retrospective",
       classify_stance("Please note: these factors are based on the 2020 "
                       "grid mix."), RETROSPECTIVE)

    # ---- independence readout, both branches reachable.
    def R(b, c):
        return {"path": "x", "criteria": {"b_retrospective": {"pass": b},
                                          "c_resolvable": {"pass": c}}}
    ck("agreeing candidates report no independence",
       independence([R(True, True), R(False, False)])["independent_observed"],
       False)
    ck("one disagreeing candidate reports it",
       independence([R(True, True), R(True, False)])["independent_observed"],
       True)
    ck("and the off-diagonal is counted, not just flagged",
       independence([R(True, False), R(False, True)])["off_diagonal"], 2)

    # ---- NO SHORT-CIRCUIT, including on a reader failure. The order
    # says all criteria recorded per file; the screen used to return
    # after one. Three states now: pass, fail, and not-evaluated, and
    # the third is not a fail -- reporting it as one would say the file
    # lacks something nobody looked for.
    unreadable = screen(os.path.join(_HERE, "selection.py"))
    ck("a file no reader opens still records every criterion",
       sorted(unreadable["criteria"]), sorted(CRITERIA_TEXT))
    ck("and the reader-dependent ones read not-evaluated, not failed",
       [unreadable["criteria"][k]["pass"]
        for k in ("a_ships_values", "b_retrospective", "c_resolvable",
                  "d_date_separated")], [None, None, None, None])
    ck("the read criterion itself is a fail, not a not-evaluated",
       unreadable["criteria"]["read"]["pass"], False)
    ck("(e) is still evaluated, since it takes no reader",
       screen(os.path.join(_HERE, "selection.py"),
              body="Someone Else")["criteria"]["e_different_body"]["pass"],
       True)
    ck("not-evaluated is not eligible either", unreadable["eligible"], False)
    ck("and the shape note says the verdict is about fit, not contents",
       "category mismatches" in unreadable.get("shape_note", ""), True)
    ck("independence skips a candidate with unevaluated criteria",
       independence([unreadable])["n"], 0)

    # ---- the screen records every criterion, not the first failure.
    # ---- the threshold is a choice and it moves the verdict. Both
    # branches asserted on constructed counts, so the readout is not
    # trusted from the two real files alone.
    class _WB(object):
        def __init__(self, n_r, n_p):
            self.n_r, self.n_p = n_r, n_p

    def _fake(n_r, n_p):
        import types
        w = types.SimpleNamespace()
        w._counts = {RETROSPECTIVE: n_r, PROSPECTIVE: n_p, NEITHER: 0}
        return w

    saved = globals()["stance_of_workbook"]
    globals()["stance_of_workbook"] = (
        lambda wb, m=1: (RETROSPECTIVE, wb._counts, {}, [("s", "w")]))
    try:
        ck("4 retro against 9 prospective flips with the rule",
           (threshold_sensitivity(_fake(4, 9))["any_rule"],
            threshold_sensitivity(_fake(4, 9))["majority_rule"]),
           (RETROSPECTIVE, PROSPECTIVE))
        ck("and the flip is reported, not left to be noticed",
           threshold_sensitivity(_fake(4, 9))["flips"], True)
        ck("a clear majority does not flip",
           threshold_sensitivity(_fake(9, 4))["flips"], False)
        ck("and neither does a zero", threshold_sensitivity(
            _fake(0, 32))["flips"], False)
    finally:
        globals()["stance_of_workbook"] = saved

    ck("criteria are all recorded", sorted(CRITERIA_TEXT), sorted(
        ["a_ships_values", "b_retrospective", "c_resolvable",
         "d_date_separated", "e_different_body", "read"]))

    # ---- (e) is recorded, never computed.
    # Composed from tokens so the check does not match the line that
    # defines it -- UNI_010, and the second time in two orders (MP_009).
    src = open(os.path.abspath(__file__)).read()
    banned = [chr(80) + "ID 4", "comp" + "any", "auth" + "or_name"]
    ck("no identity metadata is read anywhere in this module",
       [w for w in banned if w in src], [])

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


USAGE = """usage:
  selection.py screen BOOK [BOOK2 ...] [--body NAME] [--probe]
  selection.py freeze
  selection.py --selftest"""


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if not argv or argv[0] not in ("screen", "freeze"):
        print(USAGE)
        return 2
    if argv[0] == "freeze":
        print("frozen -> %s" % freeze())
        return 0
    paths = [a for a in argv[1:] if not a.startswith("-")]
    body = None
    if "--body" in argv:
        i = argv.index("--body")
        body = argv[i + 1] if i + 1 < len(argv) else None
        paths = [p for p in paths if p != body]
    if not paths:
        print(USAGE)
        return 2
    results = [screen(p, body=body) for p in paths]
    print(render(results))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
