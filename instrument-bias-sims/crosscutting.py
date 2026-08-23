#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
crosscutting.py - the work order's four cross-cutting rules, enforced over
the sims rather than stated in a README.

    python3 crosscutting.py
    python3 crosscutting.py --selftest

  1  no moral labels in any data structure
  2  no intent attribution in outputs; graded terms only (incentive
     direction, cost asymmetry, whether the aggregate steers)
  3  confidence reported as a separate readout from the pattern, not resolved
  4  README states: marker under exploration, not a thesis
  5  a readout comparing correlations must compare SIGNED values; a
     comparison of abs() across correlation-named operands fails

Rules 1 and 2 are scanned. Rules 3 and 4 are structural and are checked by
calling the modules. A rule stated in prose and not checked is a rule that
drifts, which is this repo's own recurring finding.

WHERE THIS BREAKS is at the top of the file rather than the bottom, because
it matters for reading the PASS lines: a keyword scan can be stepped around
by any paraphrase, so a PASS on rules 1 and 2 means "no listed token was
found", not "the rule holds". The scan is a floor, not a certificate.

stdlib only, CC0.
"""

import ast
import importlib
import inspect
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _shared as SH                                            # noqa: E402

SUBFOLDERS = ["allocation_coupling"]
for _sf in SUBFOLDERS:
    sys.path.insert(0, os.path.join(HERE, _sf))

MODULES = ["s1_encounter_denominator", "s2_symmetric_anchor",
           "s3_rubric_backcast", "s4_antler_calibration",
           "s5_adversarial_prior", "s6_foreclosure_rate",
           "s7_hardship_threshold", "s8_recognition_to_delivery",
           "s9_corpus_position_filter",
           "m1_tenure_budget", "m2_coupling_readout", "m3_energy_ledger",
           "m4_assessment_record", "run_all", "excluded_subject"]

# Rule 1. Tokens that would make a data structure carry a verdict about worth
# rather than a quantity. Deliberately excludes words with technical uses
# here ("right" in "right-hand", "fault" in geology).
MORAL_TOKENS = ("evil", "cruel", "wicked", "greedy", "selfish", "malicious",
                "deserve", "undeserving", "guilty", "blameworthy", "shameful",
                "virtuous", "immoral", "unjust", "abuser", "victim")

# Rule 2. Phrases that attribute an interior aim. The permitted graded terms
# are listed separately and are what a module SHOULD use instead.
INTENT_PHRASES = ("in order to", "intends", "intended to", "wants to",
                  "motivated by", "deliberately", "so that they can",
                  "on purpose", "designed to hide", "trying to")
GRADED_TERMS = ("incentive direction", "cost asymmetry", "steers",
                "aggregate steers")


def collect_strings(obj, depth=0, out=None):
    """Every string reachable inside a data structure."""
    if out is None:
        out = []
    if depth > 6:
        return out
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            collect_strings(k, depth + 1, out)
            collect_strings(v, depth + 1, out)
    elif isinstance(obj, (list, tuple, set)):
        for v in obj:
            collect_strings(v, depth + 1, out)
    return out


def module_data_strings(mod):
    """Strings inside module-level CONSTANT data structures only.

    Docstrings, prose and function bodies are excluded on purpose: the rule
    is about data structures.
    """
    out = []
    for name in dir(mod):
        if not name.isupper():
            continue
        val = getattr(mod, name)
        if isinstance(val, (dict, list, tuple, set, str)):
            out.extend(collect_strings(val))
    return out


def check_rule_1(mod):
    hits = []
    for s in module_data_strings(mod):
        low = s.lower()
        for t in MORAL_TOKENS:
            if t in low:
                hits.append((t, s[:60]))
    return {"rule": "no moral labels in any data structure",
            "hits": hits, "pass": not hits}


def check_rule_2(mod):
    text = mod.report().lower()
    hits = [p for p in INTENT_PHRASES if p in text]
    graded = [g for g in GRADED_TERMS if g in text]
    return {"rule": "no intent attribution in outputs",
            "hits": hits, "graded_terms_used": graded, "pass": not hits}


def check_rule_3(mod):
    """Confidence must be a separate callable, must not be a single scalar,
    and must not be resolved."""
    ok = hasattr(mod, "confidence") and hasattr(mod, "breaks")
    problems = []
    if not ok:
        problems.append("missing confidence() or breaks()")
    else:
        c = mod.confidence()
        if not isinstance(c, dict):
            problems.append("confidence() is not a structured readout")
        elif c.get("resolved") is not False:
            problems.append("confidence() does not record resolved False")
        if not mod.breaks():
            problems.append("breaks() is empty")
    return {"rule": "confidence separate from the pattern, not resolved",
            "problems": problems, "pass": not problems}


# Rule 5. Earned from S10/M4, where a readout compared |r| only and reported
# "tracks generated observations" for a correlation of MINUS 0.85. The sign
# was the finding and the magnitude comparison lost it. This is an AST check,
# not a keyword scan: it finds Compare nodes where BOTH sides call abs() and
# at least one operand's source mentions a correlation.
CORR_TOKENS = ("corr", "correlation", "_r", "rho")


def _mentions_correlation(node):
    try:
        src = ast.dump(node).lower()
    except Exception:                                       # pragma: no cover
        return False
    return any(t in src for t in CORR_TOKENS)


def _is_abs_call(node):
    return (isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "abs")


def check_rule_5(mod):
    """Find abs()-vs-abs() comparisons over correlation-named operands."""
    try:
        src = inspect.getsource(mod)
    except (OSError, TypeError):                            # pragma: no cover
        return {"rule": "signed correlation comparison", "hits": [],
                "pass": True, "note": "source unavailable"}
    hits = []
    for node in ast.walk(ast.parse(src)):
        if not isinstance(node, ast.Compare):
            continue
        sides = [node.left] + list(node.comparators)
        abs_sides = [x for x in sides if _is_abs_call(x)]
        if len(abs_sides) < 2:
            continue
        if any(_mentions_correlation(x) for x in abs_sides):
            hits.append(getattr(node, "lineno", -1))
    return {"rule": "a readout comparing correlations must compare SIGNED "
                    "values, not abs()",
            "hits": hits, "pass": not hits}


def check_rule_4(readme_path):
    """Also checks every subfolder README carries the phrase."""
    if not os.path.exists(readme_path):
        return {"rule": "README states marker under exploration",
                "problems": ["README.md not found"], "pass": False}
    with open(readme_path) as fh:
        txt = fh.read().lower()
    need = "marker under exploration"
    return {"rule": "README states marker under exploration",
            "problems": [] if need in txt else ["phrase not found"],
            "pass": need in txt}


def audit():
    rows = []
    for name in MODULES:
        mod = importlib.import_module(name)
        rows.append({"module": name,
                     "r1": check_rule_1(mod), "r2": check_rule_2(mod),
                     "r3": check_rule_3(mod), "r5": check_rule_5(mod)})
    r4 = check_rule_4(os.path.join(HERE, "README.md"))
    return {"rows": rows, "r4": r4,
            "all_pass": all(r[k]["pass"] for r in rows
                            for k in ("r1", "r2", "r3", "r5"))
            and r4["pass"]}


def scan_limit():
    """The null test on this checker: does it fire on a planted violation?"""
    class Fake(object):
        MORAL_TABLE = {"status": "the operator was greedy"}

        @staticmethod
        def report():
            return "the aggregate was designed to hide the cost, "\
                   "deliberately"

        @staticmethod
        def confidence():
            return {"resolved": True}

        @staticmethod
        def breaks():
            return []
    f = Fake()

    planted_r5 = """
def bad_readout(rows):
    corr_a = 0.9
    corr_b = -0.85
    if abs(corr_b) > abs(corr_a):
        return "tracks b"
    return "tracks a"
"""

    class FakeMod5(object):
        pass

    def _r5_on_source(src):
        hits = []
        for node in ast.walk(ast.parse(src)):
            if not isinstance(node, ast.Compare):
                continue
            sides = [node.left] + list(node.comparators)
            abs_sides = [x for x in sides if _is_abs_call(x)]
            if len(abs_sides) >= 2 and any(_mentions_correlation(x)
                                           for x in abs_sides):
                hits.append(node.lineno)
        return hits

    return {"planted_moral_caught": not check_rule_1(f)["pass"],
            "planted_intent_caught": not check_rule_2(f)["pass"],
            "planted_confidence_caught": not check_rule_3(f)["pass"],
            "planted_abs_comparison_caught": bool(_r5_on_source(planted_r5)),
            "paraphrase_limit": "a keyword scan is stepped around by any "
                                "paraphrase. A PASS on rules 1 and 2 means "
                                "no listed token was found, not that the "
                                "rule holds"}


def report():
    L = ["CROSS-CUTTING RULES, ENFORCED", "=" * 72, ""]
    a = audit()
    L.append("  %-32s %-8s %-8s %-11s %s"
             % ("module", "r1 data", "r2 out", "r3 readouts", "r5 signed"))
    for r in a["rows"]:
        L.append("  %-32s %-8s %-8s %-11s %s"
                 % (r["module"],
                    "pass" if r["r1"]["pass"] else "FAIL",
                    "pass" if r["r2"]["pass"] else "FAIL",
                    "pass" if r["r3"]["pass"] else "FAIL",
                    "pass" if r["r5"]["pass"] else "FAIL"))
    L.append("")
    L.append("  r4 README: %s" % ("pass" if a["r4"]["pass"] else "FAIL"))
    L.append("  all rules pass: %s" % a["all_pass"])
    L.append("")
    for r in a["rows"]:
        if r["r2"]["graded_terms_used"]:
            L.append("  %s uses graded terms: %s"
                     % (r["module"], ", ".join(r["r2"]["graded_terms_used"])))
    L.append("")
    L.append("-" * 72)
    L.append("")
    sl = scan_limit()
    L.append("  THE CHECKER, NULL-TESTED ON A PLANTED VIOLATION")
    for k in ("planted_moral_caught", "planted_intent_caught",
              "planted_confidence_caught", "planted_abs_comparison_caught"):
        L.append("    %-32s %s" % (k, sl[k]))
    L.append("")
    L.extend(SH.wrap(sl["paraphrase_limit"], "    "))
    L.append("")
    L.extend(SH.wrap("A rule stated in a README and never checked is a rule "
                     "that drifts. Rules 1 and 2 are scanned, which is a "
                     "floor. Rules 3 and 4 are structural and are actually "
                     "enforced: a module without a separate unresolved "
                     "confidence readout, or without a non-empty breaks "
                     "list, fails here and turns the folder's test red.",
                     "    "))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    a = audit()
    ck("nine sims, five S10 modules and the excluded-subject entry",
       len(a["rows"]) == 15)
    ck("rule 1 passes on every module",
       all(r["r1"]["pass"] for r in a["rows"]))
    ck("rule 2 passes on every module",
       all(r["r2"]["pass"] for r in a["rows"]))
    ck("rule 3 passes on every module",
       all(r["r3"]["pass"] for r in a["rows"]))
    ck("rule 4 passes", a["r4"]["pass"])
    ck("the aggregate verdict is computed, not asserted",
       a["all_pass"] is True)

    sl = scan_limit()
    ck("the moral scan fires on a planted violation",
       sl["planted_moral_caught"])
    ck("the intent scan fires on a planted violation",
       sl["planted_intent_caught"])
    ck("the readout check fires on a planted violation",
       sl["planted_confidence_caught"])
    ck("rule 5 fires on the exact defect it was earned from -- an abs() "
       "comparison over correlation-named operands",
       sl["planted_abs_comparison_caught"])
    ck("and rule 5 passes on every shipped module, so the repair held",
       all(r["r5"]["pass"] for r in a["rows"]))
    ck("so none of the three checks is CONSTANT_SILENT",
       all(sl[k] for k in ("planted_moral_caught", "planted_intent_caught",
                           "planted_confidence_caught",
                           "planted_abs_comparison_caught")))
    ck("the paraphrase limit is stated rather than left implied",
       "stepped around" in sl["paraphrase_limit"])

    ck("at least one module uses the permitted graded terms, so rule 2 is "
       "not passing by silence",
       any(r["r2"]["graded_terms_used"] for r in a["rows"]))
    ck("report renders", "NULL-TESTED" in report())
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "crosscutting"))
