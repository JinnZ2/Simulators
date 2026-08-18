#!/usr/bin/env python3
"""
CONSTRAINT ASSEMBLY
Records cases where sufficiency was composed from parts that individually do
not do the job. Stdlib only.

WHAT THIS IS NOT. Not option selection among presented alternatives. Not
recognition of a workable candidate from experience. The operation here is
CONSTRUCTION of an option that did not exist in the environment, out of
components each of which is insufficient alone, under a fixed budget.

THE REVERSAL THIS ENCODES. Constraints are not what limits the option set.
They are what makes composition computable. A term that will not move can be
leaned on; a soft term cannot, because there is no way to know when the pieces
add up. So the parts inventory is not domains — it is domains with hard laws
in them. More hard constraints, more composition available.

TWO CONSTRAINT CLASSES, and they behave differently enough that merging them
loses the failure mode.

  invariant    holds regardless of use. Cannot be spent. Momentum on a
               grade increases whether the engine runs or not. Load-bearing
               without limit, and available for the whole event.

  consumable   finite, and availability is destroyed by spending. Air in a
               system with no compressor running. Partial use can be worse
               than none: applying brakes without enough air to fully stop
               leaves zero air, zero brakes, and the slope still working.
               A consumable is a resource and a hazard in the same term.

  soft         does not hold under load. Recorded so that reliance on one
               is visible, not to score anybody. A plan built on a soft
               term has no assembly guarantee.

The distinction that matters operationally: an invariant is encountered, a
consumable is SPENT. Failure on a consumable is usually spending it, not
running into it.

REJECTED CANDIDATES ARE THE DATA. A composed solution is only visible as
composition if the options that were rejected are recorded with the reason.
Each rejection names which constraint ruled it out. A case with no rejections
is a case of selection, not assembly, and is recorded as such.

DIAGNOSTIC QUARANTINE. Where a cause is unknown at the time of action,
whether the diagnostic was deferred is recorded separately from the assembly.
Establishing what class of event this is spends the same budget the assembly
needs. Deferral is a recorded property, not a virtue.

No verdict. No scoring of the operator. Every readout is a property of the
recorded case.

Usage:
  assemble.py                 table over cases/
  assemble.py --case NAME     detail
  assemble.py --new NAME      skeleton
  assemble.py --jsonl
  assemble.py --selftest
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CASEDIR = os.path.join(HERE, "cases")

INVARIANT = "invariant"
CONSUMABLE = "consumable"
SOFT = "soft"
CLASSES = (INVARIANT, CONSUMABLE, SOFT)


def load(path=CASEDIR):
    out = []
    if not os.path.isdir(path):
        return out
    for f in sorted(os.listdir(path)):
        if f.endswith(".json"):
            with open(os.path.join(path, f), encoding="utf-8") as fh:
                out.append(json.load(fh))
    return out


def score(c):
    comps = c.get("components", []) or []
    used = [x for x in comps if x.get("used")]
    classes = [x.get("constraint_class") for x in used]

    # sufficiency: a component is insufficient alone if the record says so.
    # composition is present when every used component is insufficient alone
    # and there are at least two of them. one sufficient component means the
    # case is not an assembly.
    alone = [x.get("sufficient_alone") for x in used]
    any_sufficient = any(a is True for a in alone)
    all_insufficient = len(used) >= 2 and all(a is False for a in alone)
    unknown_sufficiency = any(a is None for a in alone)

    rejected = c.get("rejected", []) or []
    grounded = [r for r in rejected if r.get("ruled_out_by")]

    consumables = [x for x in used if x.get("constraint_class") == CONSUMABLE]
    spent_partial = [x for x in consumables
                     if x.get("partial_use_destroys") is True]

    softs = [x for x in used if x.get("constraint_class") == SOFT]

    diag = c.get("diagnostic", {}) or {}

    return {
        "case": c.get("case"),
        "components_used": len(used),
        "class_mix": {k: classes.count(k) for k in CLASSES if k in classes},
        "invariant_count": classes.count(INVARIANT),
        "consumable_count": classes.count(CONSUMABLE),
        "soft_count": len(softs),
        "composition_present": all_insufficient and not any_sufficient,
        "single_sufficient_component": any_sufficient,
        "sufficiency_unknown": unknown_sufficiency,
        "rejected_count": len(rejected),
        "rejections_grounded": len(grounded),
        "rejections_all_grounded": len(rejected) > 0
        and len(grounded) == len(rejected),
        "selection_not_assembly": len(rejected) == 0,
        "consumables_destroyable_by_partial_use": len(spent_partial),
        "relies_on_soft_term": len(softs) > 0,
        "diagnostic_known_at_action": diag.get("cause_known"),
        "diagnostic_deferred": diag.get("deferred"),
        "budget_terms": c.get("budget_terms", []),
        "source_class": c.get("source_class"),
        "open": c.get("open", []),
    }


def fmt(x):
    if x is None:
        return "--"
    if x is True:
        return "yes"
    if x is False:
        return "no"
    return str(x)


def wrap(t, w, ind=""):
    words, lines, cur = str(t).split(), [], ""
    for word in words:
        if len(cur) + len(word) + 1 > w:
            lines.append(ind + cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    if cur:
        lines.append(ind + cur)
    return lines


def table(scores):
    hdr = (f"{'case':<24}{'used':>6}{'inv':>5}{'cons':>6}{'soft':>6}"
           f"{'comp':>6}{'rej':>5}{'grnd':>6}")
    print(hdr)
    print("-" * len(hdr))
    for s in scores:
        print(f"{str(s['case'])[:24]:<24}{s['components_used']:>6}"
              f"{s['invariant_count']:>5}{s['consumable_count']:>6}"
              f"{s['soft_count']:>6}{fmt(s['composition_present']):>6}"
              f"{s['rejected_count']:>5}"
              f"{fmt(s['rejections_all_grounded']):>6}")
    print()
    print("used  components used in the assembled solution")
    print("inv   invariant terms. hold regardless of use, cannot be spent")
    print("cons  consumable terms. finite, destroyed by spending")
    print("soft  terms that do not hold under load")
    print("comp  every used component insufficient alone, two or more")
    print("rej   options rejected, with the constraint that ruled each out")
    print("grnd  every rejection names a constraint")
    print()
    print("A case with rej 0 is selection, not assembly.")


def detail(s):
    print("CASE  %s" % s["case"])
    print()
    print("COMPONENTS USED   %d   %s" % (s["components_used"], s["class_mix"]))
    print("  composition present        %s" % fmt(s["composition_present"]))
    if s["single_sufficient_component"]:
        print("  one component sufficient alone — not an assembly")
    if s["sufficiency_unknown"]:
        print("  sufficiency unrecorded for at least one component")
    print()
    print("CONSTRAINT CLASSES")
    print("  invariant                  %d" % s["invariant_count"])
    print("  consumable                 %d" % s["consumable_count"])
    print("  destroyable by partial use %d"
          % s["consumables_destroyable_by_partial_use"])
    if s["relies_on_soft_term"]:
        print("  RELIES ON A SOFT TERM      %d" % s["soft_count"])
        print("    no assembly guarantee from a term that moves under load")
    print()
    print("REJECTED OPTIONS  %d   all grounded: %s"
          % (s["rejected_count"], fmt(s["rejections_all_grounded"])))
    if s["selection_not_assembly"]:
        print("  no rejections recorded — selection, not assembly")
    print()
    print("DIAGNOSTIC")
    print("  cause known at action      %s" % fmt(s["diagnostic_known_at_action"]))
    print("  deferred                   %s" % fmt(s["diagnostic_deferred"]))
    print()
    if s["budget_terms"]:
        print("BUDGET TERMS  %s" % ", ".join(s["budget_terms"]))
        print()
    print("SOURCE  %s" % s["source_class"])
    print()
    for o in s["open"]:
        print("OPEN")
        for line in wrap(o, 58, "    "):
            print(line)
        print()


SKELETON = {
    "case": "",
    "components": [
        {"name": "", "constraint_class": INVARIANT, "law": "",
         "sufficient_alone": False, "used": True,
         "partial_use_destroys": None}
    ],
    "rejected": [{"option": "", "ruled_out_by": ""}],
    "budget_terms": [],
    "diagnostic": {"cause_known": None, "deferred": None, "note": ""},
    "source_class": "",
    "open": []
}


def selftest():
    a = score({
        "case": "a",
        "components": [
            {"name": "i", "constraint_class": INVARIANT,
             "sufficient_alone": False, "used": True},
            {"name": "c", "constraint_class": CONSUMABLE,
             "sufficient_alone": False, "used": True,
             "partial_use_destroys": True},
        ],
        "rejected": [{"option": "x", "ruled_out_by": "r"},
                     {"option": "y", "ruled_out_by": "r"}],
        "diagnostic": {"cause_known": False, "deferred": True}})
    b = score({
        "case": "b",
        "components": [
            {"name": "s", "constraint_class": SOFT,
             "sufficient_alone": True, "used": True}],
        "rejected": []})
    c = score({
        "case": "c",
        "components": [
            {"name": "u", "constraint_class": INVARIANT,
             "sufficient_alone": None, "used": True},
            {"name": "v", "constraint_class": INVARIANT,
             "sufficient_alone": False, "used": True}],
        "rejected": [{"option": "z"}]})
    empty = score({"case": "e"})
    checks = [
        ("composition detected", a["composition_present"] is True),
        ("single sufficient blocks composition",
         b["composition_present"] is False),
        ("single sufficient flagged", b["single_sufficient_component"]),
        ("unknown sufficiency blocks composition",
         c["composition_present"] is False),
        ("unknown sufficiency flagged", c["sufficiency_unknown"] is True),
        ("class counts split", a["invariant_count"] == 1
         and a["consumable_count"] == 1),
        ("soft counted separately", b["soft_count"] == 1),
        ("soft reliance flagged", b["relies_on_soft_term"] is True),
        ("partial-use destruction counted",
         a["consumables_destroyable_by_partial_use"] == 1),
        ("grounded rejections", a["rejections_all_grounded"] is True),
        ("ungrounded rejection caught",
         c["rejections_all_grounded"] is False),
        ("no rejections is selection", b["selection_not_assembly"] is True),
        ("rejections present not selection",
         a["selection_not_assembly"] is False),
        ("diagnostic fields carried",
         a["diagnostic_known_at_action"] is False
         and a["diagnostic_deferred"] is True),
        ("diagnostic none when unstated",
         c["diagnostic_known_at_action"] is None),
        ("empty case no crash", empty["components_used"] == 0),
        ("empty composition false", empty["composition_present"] is False),
        ("no verdict field", not any(
            k in a for k in ("verdict", "correct", "score", "quality"))),
    ]
    ok = 0
    for n, r in checks:
        print(("PASS" if r else "FAIL"), n)
        ok += bool(r)
    print("\n%d/%d" % (ok, len(checks)))
    return 0 if ok == len(checks) else 1


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if "--new" in a:
        i = a.index("--new")
        sk = json.loads(json.dumps(SKELETON))
        sk["case"] = a[i + 1] if len(a) > i + 1 else "unnamed"
        print(json.dumps(sk, indent=2))
        return
    scores = [score(x) for x in load()]
    if "--jsonl" in a:
        for s in scores:
            print(json.dumps(s))
        return
    if "--case" in a:
        want = a[a.index("--case") + 1]
        for s in scores:
            if s["case"] == want:
                detail(s)
                return
        print("no case named %s" % want, file=sys.stderr)
        sys.exit(1)
    table(scores)


if __name__ == "__main__":
    main()
