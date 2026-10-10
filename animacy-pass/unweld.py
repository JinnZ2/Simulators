"""unweld.py -- unweld an evaluative claim before it is allowed to stand.

CC0. stdlib only. Parses under Python 3.9.

The operator's framing, which is the spec. Words like "cheaper",
"efficient", "optimal" (and the same class: "productive", "better",
"scalable", "clean") are WELDED CLAIMS: one word fusing several buried
terms, asserted as if it were one clean physical fact. The physics
underneath runs regardless of what the label chooses to count.

The proof they are not physical: the IDENTICAL process spending the
IDENTICAL matter and energy can be called "expensive" by one company and
"cheap" by another. The term is a property of the framing, not of the
process, so it has to be grounded to a common variable before it stands.

The physics tell: "cheaper" usually means a boundary was drawn tight, so a
real cost -- energy, matter, waste -- falls OUTSIDE the frame. Unwelding it
means forcing it to name its boundary, then running the balance across the
FULL boundary to surface what the word pushed out. That pushed-out cost is
the externality, and it is physical.

STANDING CHALLENGE (the bar this is built against): if something can be
found that is UNANIMOUSLY cheaper / more efficient / optimal across all
framings -- that stays grounded and keeps its label wherever the boundary
is drawn -- the term earns its use. Until then these words must be grounded
to a common variable before they stand. `unanimous()` is that test: it
returns EARNED only when every framing supplied is GROUNDED and all carry
the same label; otherwise NOT_EARNED with the reason.

What the check does:
  1. Finds welded terms in the claim (word boundary, listed forms).
  2. Lists the buried terms each one must declare, and which the claim's
     DECLARATIONS fill or leave blank. A declaration is a field the
     claimant supplies -- this is the CSV row every headline should come
     with. The tool does not read buried terms out of prose.
  3. For the named process, builds the full balance: every prerequisite
     dependency_check.derive_map derives (all degrees), plus the outputs
     the process must put somewhere (OUTPUTS, a seed set). Anything in the
     full balance not covered by the declared boundary is a CANDIDATE
     EXTERNALITY.

Verdict:
  NO_WELDED_TERM           nothing to unweld
  GROUNDED                 every buried term declared, boundary stated,
                           and the full balance falls inside the boundary
  UNGROUNDED               a buried term is blank, and/or a balance item
                           falls outside the boundary (reasons listed)
  UNDETERMINED_NO_BALANCE  terms declared but no balance for the process,
                           so what the boundary leaves out cannot be checked
                           -- never read as GROUNDED

HONEST LIMIT: filling a buried term is a declaration. The tool checks for
blanks and for balance items outside the stated boundary. It does not
adjudicate the real-world numbers, does not check that a declared value is
true, and matches boundary items to balance items by name or alias, so a
different word for the same input is missed (reported as outside).

Usage:
  python3 unweld.py CASE.json        one framing
  python3 unweld.py --demo
  python3 unweld.py --terms
  python3 unweld.py --selftest
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dependency_check as dc  # noqa: E402

# ---------------------------------------------------------------- welded terms
# Each: the forms that trigger it, and the buried terms it must declare.

WELDED = {
    "cheaper": {
        "forms": ["cheaper", "cheap", "cheapest", "expensive", "costly",
                  "lower cost", "low-cost", "less costly"],
        "buried": ["for_whom", "unit", "boundary", "time_span",
                   "inputs_counted", "outputs_counted", "compared_to"],
        "note": "a cost comparison: who pays, in what unit, inside what "
                "boundary, over what time, counting which inputs and "
                "outputs, against what alternative",
    },
    "efficient": {
        "forms": ["efficient", "efficiency", "more efficient",
                  "inefficient"],
        "buried": ["output_quantity", "input_quantity", "boundary",
                   "time_span"],
        "note": "a ratio output/input: both quantities with units, and the "
                "boundary they are counted across",
    },
    "optimal": {
        "forms": ["optimal", "optimized", "optimised", "optimize",
                  "optimum"],
        "buried": ["objective", "constraints", "chosen_by", "boundary"],
        "note": "optimal with respect to what objective, under what "
                "constraints, chosen by whom, inside what boundary",
    },
    "productive": {
        "forms": ["productive", "productivity"],
        "buried": ["output_quantity", "input_quantity", "for_whom",
                   "boundary", "time_span"],
        "note": "output per input, for whom, across what boundary and time",
    },
    "better": {
        "forms": ["better", "best", "superior", "improved"],
        "buried": ["with_respect_to", "compared_to", "for_whom",
                   "boundary"],
        "note": "better in what respect, than what, for whom",
    },
    "scalable": {
        "forms": ["scalable", "scales", "at scale"],
        "buried": ["what_scales", "along_what", "up_to_limit",
                   "input_growth", "boundary"],
        "note": "what grows, along what axis, to what limit, and how fast "
                "its inputs grow with it",
    },
    "clean": {
        "forms": ["clean", "green", "zero-emission", "emission-free"],
        "buried": ["free_of_what", "at_which_point", "boundary"],
        "note": "free of what, at which point in the chain, inside what "
                "boundary",
    },
}

# Outputs a process must put somewhere (mass and energy leave it). SEED SET.
OUTPUTS = {
    "data center": [("waste heat", "energy"), ("e-waste", "matter")],
    "combustion": [("carbon dioxide", "matter"), ("water vapor", "matter"),
                   ("heat", "energy")],
    "thermal power": [("rejected heat", "energy"),
                      ("carbon dioxide", "matter")],
    "conductor": [("sulfur dioxide", "matter"), ("tailings", "matter")],
}


def find_terms(claim):
    """[(welded_key, form_matched)] in order of first appearance."""
    text = claim.lower()
    hits = []
    for key, w in WELDED.items():
        for form in sorted(w["forms"], key=len, reverse=True):
            pat = r"(?<![a-z0-9])" + re.escape(form) + r"(?![a-z0-9])"
            m = re.search(pat, text)
            if m:
                hits.append((m.start(), key, form))
                break
    return [(k, f) for _, k, f in sorted(hits)]


def _blank(v):
    return v is None or (isinstance(v, str) and not v.strip()) or v == []


def full_balance(process, extra=None):
    """[(item, kind, role)] -- all derived prerequisites and outputs."""
    dmap = dc.derive_map(process) if process else {}
    if not dmap and not extra:
        return None
    kinds = dc.derived_kinds(dmap)
    items = []
    if dmap:
        for name, _deg in sorted(dc.degrees(process, dmap).items(),
                                 key=lambda x: (x[1], x[0])):
            items.append((name, kinds.get(name, "UNDECLARED"), "input"))
        key = dc._template_for(process)
        for name, kind in OUTPUTS.get(key, []):
            items.append((name, kind, "output"))
    for name, kind, role in (extra or []):
        if name not in [i[0] for i in items]:
            items.append((name, kind, role))
    return items


def covered(item, boundary):
    names = {b.lower().strip() for b in boundary}
    if item.lower() in names:
        return True
    al = dc.derived_aliases([item]).get(item, [])
    return any(a.lower() in names for a in al)


def unweld(case):
    claim = case.get("claim", "")
    terms = find_terms(claim)
    if not terms:
        return {"verdict": "NO_WELDED_TERM", "terms": []}
    decl = case.get("declares") or {}
    reasons, per_term = [], []
    for key, form in terms:
        buried = WELDED[key]["buried"]
        filled = [b for b in buried if not _blank(decl.get(b))]
        blank = [b for b in buried if _blank(decl.get(b))]
        per_term.append({"term": key, "form": form, "filled": filled,
                         "blank": blank})
        if blank:
            reasons.append("'%s' leaves blank: %s" % (form, ", ".join(blank)))
    boundary = decl.get("boundary") or []
    if isinstance(boundary, str):
        boundary = [boundary]
    balance = full_balance(case.get("process"), case.get("extra_balance"))
    outside = None
    if balance is not None:
        outside = [(n, k, r) for n, k, r in balance
                   if not covered(n, boundary)]
        if outside and boundary:
            reasons.append("outside the stated boundary: %s"
                           % ", ".join(n for n, _, _ in outside))
    if reasons:
        verdict = "UNGROUNDED"
    elif balance is None:
        verdict = "UNDETERMINED_NO_BALANCE"
    else:
        verdict = "GROUNDED"
    return {"verdict": verdict, "terms": per_term, "reasons": reasons,
            "process": case.get("process"), "boundary": boundary,
            "balance": balance, "outside": outside,
            "label": case.get("label_used")}


def compare_framings(a, b):
    """Two framings of one process: does the label flip while the physics
    (the full balance and any declared physical quantity) is identical?"""
    ra, rb = unweld(a), unweld(b)
    same_process = a.get("process") == b.get("process")
    same_balance = ra.get("balance") == rb.get("balance")
    same_phys = (a.get("physical_quantity") == b.get("physical_quantity")
                 and a.get("physical_quantity") is not None)
    flipped = (a.get("label_used") != b.get("label_used"))
    bd_a = set(map(str.lower, ra.get("boundary") or []))
    bd_b = set(map(str.lower, rb.get("boundary") or []))
    if same_process and same_balance and same_phys and flipped:
        state = "LABEL_FLIPS_PHYSICS_IDENTICAL"
    elif not flipped:
        state = "LABEL_SAME"
    else:
        state = "PHYSICS_DIFFERS"
    return {"state": state, "a": ra, "b": rb,
            "only_in_a": sorted(bd_a - bd_b), "only_in_b": sorted(bd_b - bd_a)}


def unanimous(cases):
    """The standing challenge: EARNED only if every framing is GROUNDED and
    all carry the same label."""
    if not cases:
        return {"state": "NOT_EARNED", "why": "no framings supplied"}
    res = [unweld(c) for c in cases]
    if any(r["verdict"] != "GROUNDED" for r in res):
        return {"state": "NOT_EARNED",
                "why": "%d of %d framings not GROUNDED" % (
                    sum(r["verdict"] != "GROUNDED" for r in res), len(res))}
    labels = {c.get("label_used") for c in cases}
    if len(labels) != 1:
        return {"state": "NOT_EARNED",
                "why": "grounded framings disagree on the label: %s"
                       % ", ".join(sorted(map(str, labels)))}
    return {"state": "EARNED", "why": "every framing grounded, one label"}


def render(case, res):
    out = ["claim  : %s" % case.get("claim", ""),
           "verdict: %s" % res["verdict"]]
    for t in res.get("terms", []):
        out.append("  welded '%s' (%s): %s" % (t["form"], t["term"],
                                               WELDED[t["term"]]["note"]))
        out.append("    declared: %s" % (", ".join(t["filled"]) or "-"))
        out.append("    BLANK   : %s" % (", ".join(t["blank"]) or "-"))
    if res["verdict"] == "NO_WELDED_TERM":
        return "\n".join(out)
    out.append("  boundary: %s" % (", ".join(res["boundary"]) or "(none)"))
    if res["balance"] is None:
        out.append("  balance : none for process %r -- what the boundary "
                   "leaves out cannot be checked" % res["process"])
    else:
        out.append("  full balance for '%s': %d items" % (
            res["process"], len(res["balance"])))
        for n, k, r in res["balance"]:
            out.append("    %-22s %-7s %-6s %s" % (
                n, k, r, "outside" if (n, k, r) in res["outside"]
                else "inside"))
    for r in res["reasons"]:
        out.append("  -> %s" % r)
    return "\n".join(out)


def render_compare(a, b, cmp):
    out = ["SAME PROCESS, TWO FRAMINGS", ""]
    for tag, c in (("A", a), ("B", b)):
        out.append("framing %s (label '%s'):" % (tag, c.get("label_used")))
        out.append(render(c, cmp[tag.lower()]))
        out.append("")
    out.append("comparison: %s" % cmp["state"])
    out.append("  physical quantity, both framings: %s"
               % a.get("physical_quantity"))
    out.append("  counted only by A: %s" % (", ".join(cmp["only_in_a"]) or "-"))
    out.append("  counted only by B: %s" % (", ".join(cmp["only_in_b"]) or "-"))
    out.append("  the label moved with the boundary; the process and its "
               "balance did not")
    return "\n".join(out)


def render_terms():
    out = ["welded terms and the buried terms each must declare", ""]
    for k, w in WELDED.items():
        out.append("%s  (forms: %s)" % (k, ", ".join(w["forms"])))
        out.append("  must declare: %s" % ", ".join(w["buried"]))
        out.append("  %s" % w["note"])
    return "\n".join(out)


# ---------------------------------------------------------------- demo

_FULL_DC = ["electricity", "cooling", "land", "conductor", "cold sink",
            "ore", "primary energy source", "smelting energy", "water",
            "waste heat", "e-waste"]

FLIP_A = {
    "label_used": "cheap",
    "claim": "Running our data center here is cheap.",
    "process": "data center",
    "physical_quantity": "1.2 GWh electricity per year, all leaving as heat",
    "declares": {"for_whom": "the operating company", "unit": "USD",
                 "boundary": ["electricity", "land"],
                 "time_span": "one fiscal year",
                 "inputs_counted": "electricity bill at a subsidised rate, "
                                   "land lease",
                 "outputs_counted": "none",
                 "compared_to": "the same site last year"},
}
FLIP_B = {
    "label_used": "expensive",
    "claim": "Running that data center there is expensive.",
    "process": "data center",
    "physical_quantity": "1.2 GWh electricity per year, all leaving as heat",
    "declares": {"for_whom": "the watershed and the grid region",
                 "unit": "joules and kilograms",
                 "boundary": _FULL_DC,
                 "time_span": "hardware lifetime, ten years",
                 "inputs_counted": "all eleven balance items",
                 "outputs_counted": "waste heat into the river, e-waste",
                 "compared_to": "not building it"},
}

DEMO = [
    {"label": "CONSTRUCTED -- welded term, nothing declared",
     "claim": "Remote compute is cheaper and more efficient.",
     "process": None, "declares": {}},
    {"label": "CONSTRUCTED -- terms declared, no balance for the process",
     "claim": "The new rota is more efficient.", "process": "staff rota",
     "declares": {"output_quantity": "shifts covered per week",
                  "input_quantity": "staff hours", "boundary": ["one ward"],
                  "time_span": "four weeks"}},
]


def selftest():
    fails, n = [], [0]

    def ok(c, label):
        n[0] += 1
        if not c:
            fails.append(label)

    for k, w in WELDED.items():
        ok(w["forms"] and w["buried"] and w["note"], "term %s complete" % k)
    ok([t for t, _ in find_terms("Cheaper and more efficient")]
       == ["cheaper", "efficient"], "terms found in order")
    ok(find_terms("cheapskate stacks") == [], "word boundary")
    ok(find_terms("lower cost option") == [("cheaper", "lower cost")],
       "multiword form")
    ok(unweld({"claim": "it runs on rain"})["verdict"] == "NO_WELDED_TERM",
       "no welded term")

    r = unweld(DEMO[0])
    ok(r["verdict"] == "UNGROUNDED" and len(r["reasons"]) == 2,
       "UNGROUNDED by blank, both terms")
    ok(unweld(DEMO[1])["verdict"] == "UNDETERMINED_NO_BALANCE",
       "declared but no balance: UNDETERMINED, never GROUNDED")

    ra = unweld(FLIP_A)
    ok(ra["verdict"] == "UNGROUNDED", "narrow boundary UNGROUNDED")
    ok(any("outside the stated boundary" in x for x in ra["reasons"]),
       "UNGROUNDED by externality")
    outs = [o[0] for o in ra["outside"]]
    ok("waste heat" in outs and "cooling" in outs, "pushed-out costs named")
    ok(not [x for x in ra["reasons"] if "leaves blank" in x],
       "narrow framing has no blanks: externality alone fails it")

    rb = unweld(FLIP_B)
    ok(rb["verdict"] == "GROUNDED" and rb["outside"] == [],
       "full boundary GROUNDED")
    ok(covered("conductor", ["copper"]), "boundary alias covers balance item")

    cmp = compare_framings(FLIP_A, FLIP_B)
    ok(cmp["state"] == "LABEL_FLIPS_PHYSICS_IDENTICAL", "flip detected")
    ok(ra["balance"] == rb["balance"], "identical balance both framings")
    same = dict(FLIP_B, label_used="cheap")
    ok(compare_framings(FLIP_A, same)["state"] == "LABEL_SAME",
       "same label is not a flip")
    other = dict(FLIP_B, physical_quantity="3 GWh")
    ok(compare_framings(FLIP_A, other)["state"] == "PHYSICS_DIFFERS",
       "different physics is not a pure framing flip")

    ok(unanimous([FLIP_A, FLIP_B])["state"] == "NOT_EARNED",
       "challenge: the pair does not earn the term")
    b2 = dict(FLIP_B, claim="That data center is expensive.")
    ok(unanimous([FLIP_B, b2])["state"] == "EARNED",
       "challenge is reachable: grounded and one label")
    ok(unanimous([FLIP_B, dict(FLIP_B, label_used="cheap")])["state"]
       == "NOT_EARNED", "grounded framings that disagree do not earn it")
    ok(unanimous([])["state"] == "NOT_EARNED", "no framings: NOT_EARNED")

    print("checks: %d   failed: %d" % (n[0], len(fails)))
    for f in fails:
        print("  FAIL", f)
    return 0 if not fails else 1


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--selftest":
        return selftest()
    if argv[0] == "--terms":
        print(render_terms())
        return 0
    if argv[0] == "--demo":
        for c in DEMO:
            print("== %s" % c["label"])
            print(render(c, unweld(c)))
            print()
        print("== CONSTRUCTED -- the expensive/cheap flip")
        print(render_compare(FLIP_A, FLIP_B, compare_framings(FLIP_A, FLIP_B)))
        print()
        u = unanimous([FLIP_A, FLIP_B])
        print("standing challenge over these two framings: %s (%s)"
              % (u["state"], u["why"]))
        return 0
    with open(argv[0], encoding="utf-8") as f:
        case = json.load(f)
    print(render(case, unweld(case)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
