#!/usr/bin/env python3
"""assembly_audit.py -- checks on the constraint-assembly drop.

Added, not delivered. assemble.py is the drop as received and is not
modified. Findings are recorded in AUDIT_NOTES.md as CA_001..CA_007.

    python3 assembly_audit.py

The drop is one file: a scorer with a selftest, no cases/, no README and
no claim table. Nothing here invents a case.

stdlib only, deterministic. CC0.
"""

import contextlib
import io
import os

import assemble as A

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BAR = "=" * 70


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def probe(comps, rejected=None):
    return A.score({"case": "p", "components": comps,
                    "rejected": rejected if rejected is not None
                    else [{"option": "x", "ruled_out_by": "r"}]})


print("constraint-assembly -- audit of the delivered drop")
print("delivered: assemble.py")
print("not delivered: cases/, README.md, CLAIM_TABLE.md")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = A.selftest()
print("selftest: %s, rc=%d" % (buf.getvalue().strip().splitlines()[-1], rc))

# ------------------------------------------------------------------ CA_001
head(1, "CA_001", "the reversal, and where it sits against the sibling folders")
print("""
    Constraints are not what limits the option set. They are what makes
    composition computable. A term that will not move can be leaned on; a
    soft term cannot, because there is no way to know when the pieces add
    up. So the parts inventory is not domains -- it is domains with hard
    laws in them. More hard constraints, more composition available.

That is an argument with a mechanism in it, not a slogan. The mechanism is
decidability: composition needs a stopping rule, and a term that holds
regardless of use supplies one. A term that moves under load does not, so
a plan resting on it has no assembly guarantee -- which is why `soft` is a
recorded class rather than an excluded one.

It also runs opposite to the two nearest folders in this drop family, on
the same object.

  generation-capacity   the option space was REDUCED upstream, and the
                        party cannot generate what is missing
  presented-binary      the option set was CLOSED at presentation, and
                        the reduction is performed rather than found
  constraint-assembly   the option is CONSTRUCTED out of parts that
                        individually do not do the job

The first two measure an option space that is smaller than it looks. This
measures one being made larger, from components, under a fixed budget --
and it names constraints as the enabling term in that operation rather
than the limiting one.

The three are not in tension. They are three positions on one quantity,
and only this one treats hard laws as the parts inventory.
""".strip())

# ------------------------------------------------------------------ CA_002
head(2, "CA_002", "the nearest-neighbour discriminator is built in and fail-closed")
print("""
    A case with no rejections is a case of selection, not assembly, and is
    recorded as such.

Selection from presented alternatives is the thing assembly is most likely
to be mistaken for, and `selection_not_assembly` is a readout rather than
a caveat. The selftest exercises it.

`composition_present` is the second guard, and it fails closed:
""".strip())
print()
print("  %-32s %-12s %-9s %s" % ("used components", "composition", "unknown",
                                 "single_sufficient"))
print("  " + "-" * 70)
for label, vals in (("both explicitly insufficient", [False, False]),
                    ("one unrecorded", [None, False]),
                    ("one sufficient alone", [True, False])):
    s = probe([{"name": str(i), "constraint_class": A.INVARIANT,
                "sufficient_alone": v, "used": True}
               for i, v in enumerate(vals)])
    print("  %-32s %-12s %-9s %s" % (
        label, s["composition_present"], s["sufficiency_unknown"],
        s["single_sufficient_component"]))
print("""
An unrecorded sufficiency blocks composition and is reported separately.
The claim is not made when the evidence for it is missing, and the reason
is visible -- which is the opposite direction from closure-cost CC_003,
where an omitted field reads as the informative state.

Running tally of that repair across this drop family:
""".strip())
print()
for cid, where, how in [
    ("PB_004", "frame_sim option_gain", "found -- merged"),
    ("PB_012", "binary_audit handoff()", "found -- merged"),
    ("GC_004", "MECHANISM_10 R3", "found -- merged"),
    ("MD_002", "moral-decomposer reduces_to", "found -- merged"),
    ("CC_002", "closure.py rules_out", "found -- merged"),
    ("GC_010", "SUBCASE_10A S1", "designed in -- specified"),
    ("DL_008", "anchor.py routing states", "designed in -- implemented"),
    ("CC_001", "closure.py knowledge_state", "designed in -- vocabulary"),
    ("CA_002", "assemble.py sufficiency", "designed in -- fail-closed"),
]:
    print("  %-8s %-30s %s" % (cid, where, how))

# ------------------------------------------------------------------ CA_003
head(3, "CA_003", "the reversal's own quantity is recordable and unreported")
comps = [
    {"name": "used-1", "constraint_class": A.INVARIANT,
     "sufficient_alone": False, "used": True},
    {"name": "used-2", "constraint_class": A.CONSUMABLE,
     "sufficient_alone": False, "used": True},
    {"name": "avail-1", "constraint_class": A.INVARIANT,
     "sufficient_alone": False, "used": False},
    {"name": "avail-2", "constraint_class": A.INVARIANT,
     "sufficient_alone": False, "used": False},
    {"name": "avail-3", "constraint_class": A.CONSUMABLE,
     "sufficient_alone": False, "used": False},
]
s = probe(comps)
print("""
The headline claim is about the INVENTORY: "more hard constraints, more
composition available". That is a statement about what was available to
compose from, not about what ended up in the composition.

`score()` filters to used components on its first line and every readout
downstream derives from that list. A case recording five components, three
of them available and not used:
""".strip())
print()
print("  components in the file       %d   (2 used, 3 available and unused)" % len(comps))
print("  components_used              %d" % s["components_used"])
print("  invariant_count              %d   (used only)" % s["invariant_count"])
print("  consumable_count             %d   (used only)" % s["consumable_count"])
print("  fields counting the unused   %s" % (
    [k for k in s if "avail" in k or "inventory" in k] or "none"))
print("""
The schema lets a case record what was available and not used -- `used` is
a per-component boolean, so the inventory is expressible -- and no readout
counts it. The quantity the reversal turns on is the one that does not
reach the table.

This is not the usual missing-field shape (MF_017, CW_015, DL_004, GC_012),
where a stated rule has no schema slot. Here the slot exists and the
readout does not, which is cheaper still: `hard_constraints_available`
over all components rather than over used ones is one line, and it is the
number that would let the claim be checked across cases -- does a case with
a larger hard-law inventory compose more.

Without it, `invariant_count` reads as an inventory measure and is a
composition measure. Two cases with identical used-counts and very
different available-counts are indistinguishable in the table.
""".strip())

# ------------------------------------------------------------------ CA_004
head(4, "CA_004", "rejections_all_grounded, the narrow version of the usual shape")
print()
print("  %-32s %5s %14s %s" % ("case", "rej", "all_grounded", "selection"))
print("  " + "-" * 66)
for label, rej in (("2 rejections, both grounded",
                    [{"option": "x", "ruled_out_by": "r"},
                     {"option": "y", "ruled_out_by": "r"}]),
                   ("2 rejections, one ungrounded",
                    [{"option": "x", "ruled_out_by": "r"}, {"option": "y"}]),
                   ("0 rejections (selection)", [])):
    sc = A.score({"case": "p", "components": [], "rejected": rej})
    print("  %-32s %5d %14s %s" % (
        label, sc["rejected_count"], sc["rejections_all_grounded"],
        sc["selection_not_assembly"]))
print("""
    "rejections_all_grounded": len(rejected) > 0 and len(grounded) == len(rejected)

Rows 2 and 3 return the same value for different reasons: a data-quality
failure in an assembly case, and a case with nothing to ground.

This is the narrow version of the shape rather than the usual one, and it
is worth saying so. `selection_not_assembly` sits beside it and separates
them, the table prints both columns, and the footer states the rule -- "A
case with rej 0 is selection, not assembly." A reader has what they need.

What is left is that the column alone reads `no` for a case with nothing
to ground, so the field is not safe to quote on its own. Returning None
when `rejected` is empty would cost nothing and is what `budget_consumed`
does one folder over.
""".strip())

# ------------------------------------------------------------------ CA_005
head(5, "CA_005", "the argument guard, second consecutive tool")
print()
print("  %-36s %s" % ("tool", "bounds-checked lookup after a flag"))
print("  " + "-" * 72)
for path in ("domain-ledger/ledger.py", "domain-ledger/anchor.py",
             "closure-cost/closure.py", "constraint-assembly/assemble.py"):
    src = open(os.path.join(ROOT, path), encoding="utf-8").read()
    print("  %-36s %s" % (path, "if len(a) > i + 1 else None" in src))
print("""
  measured: assemble.py --case  ->  IndexError, rc 1

CC_004 recorded this for closure.py. It recurs unchanged in the next tool,
and in both files `--new` IS guarded with exactly the expression the two
`domain-ledger` tools use throughout. Same author, same pattern available
in the same function, applied to one flag of two.
""".strip())

# ------------------------------------------------------------------ CA_006
head(6, "CA_006", "the diagnostic budget is shared with closure-cost, and said so")
print("""
    DIAGNOSTIC QUARANTINE. Where a cause is unknown at the time of action,
    whether the diagnostic was deferred is recorded separately from the
    assembly. Establishing what class of event this is spends the same
    budget the assembly needs. Deferral is a recorded property, not a
    virtue.

closure-cost's central readout is `diagnostic_spend` -- time spent
establishing what class of event this is, over time available before
action had to be taken. This folder records whether that spend was
DEFERRED, on the same budget.

So the two folders measure one quantity from opposite ends:

  closure-cost          the categorisation stall, as a fraction of the
                        budget consumed
  constraint-assembly   whether the operator declined to spend it, and
                        assembled without knowing the cause

That pairing is stated by the author rather than inferred here, and it is
the first time in this drop family that two folders name the same budget.
closure-cost's README says the same thing from its side: "the observed
case that generated it is a category-stall avoided, not one suffered."

"Deferral is a recorded property, not a virtue" is consistent with the
module's own "No scoring of the operator", and it is the harder version --
deferring the diagnostic is the behaviour the shape predicts, and it is
still not scored.
""".strip())

# ------------------------------------------------------------------ CA_007
head(7, "CA_007", "an empty corpus prints a clean report -- fourth tool")
print()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    A.table([])
print("  rows printed  : 0")
print("  lines printed : %d" % len(buf.getvalue().strip().splitlines()))
print("  exit code     : 0")
print()
for path, refuses in (("category-weld/weld.py", True),
                      ("presented-binary/binary_audit.py", True),
                      ("generation-capacity/capacity.py", True),
                      ("domain-ledger/ledger.py", False),
                      ("domain-ledger/anchor.py", False),
                      ("closure-cost/closure.py", False),
                      ("constraint-assembly/assemble.py", False)):
    print("    %-40s refuses on empty: %s" % (path, refuses))
print("""
Three refuse, four print. The split is by drop age, and the newer half is
now the larger one. DL_005 and CC_006 stand; this is the fourth instance
and adds nothing new except the count.

Unlike closure.py, this table's footer does not state a corpus condition.
It states a reading rule -- "A case with rej 0 is selection, not
assembly" -- which is the right footer for a populated run and says
nothing about an empty one.
""".strip())

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as CA_001..CA_007")
print(BAR)
