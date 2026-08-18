#!/usr/bin/env python3
"""closure_audit.py -- checks on the closure-cost drop.

Added, not delivered. closure.py is the drop as received and is not
modified. Findings are recorded in AUDIT_NOTES.md as CC_001..CC_006.

    python3 closure_audit.py

The drop is one file: a scorer with a selftest, no cases/ directory, no
README and no claim table. Nothing here invents a case.

stdlib only, deterministic. CC0.
"""

import contextlib
import io
import os

import json

import closure as C

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BAR = "=" * 70


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


print("closure-cost -- audit of the delivered drop")
print("delivered: closure.py")
print("delivered drop 2: README.md, CLAIM_TABLE.md (C1-C5), 3 cases")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = C.selftest()
print("selftest: %s, rc=%d" % (buf.getvalue().strip().splitlines()[-1], rc))

# ------------------------------------------------------------------ CC_001
head(1, "CC_001", "the vocabulary carries a named rival hypothesis")
print("""
The shape: response failure tracks whether a variable was carried as live,
not whether the event was severe and not whether information was
available. The delay when it fires is categorisation, not reaction.

Two things in the docstring are unusual enough to record before anything
else.

A NAMED RIVAL, IN THE SCHEMA.

    Missing procedure is the obvious competing account of non-response. It
    is not independent: nobody acquires a protocol for an event they have
    closed. So procedure absence can be a downstream readout of the closed
    prior rather than an alternative to it. That collapse is not
    automatic. It is asserted per case, with the ground stated, and the
    field records which.

`procedure_gap.collapsed_into_closure` plus `procedure_gap.ground` carry
it. This is the first folder in the drop family to hold its competing
explanation as a schema field rather than as prose, and the first to state
that the rival is not independent of the shape -- which is the harder
admission, because a non-independent rival cannot be ruled out by finding
the shape.

FOUR-VALUED KNOWLEDGE STATE.

    not_taught              never delivered
    taught_not_retained     delivered, did not attach
    retained_not_executed   present, not run under load
    not_separable           the record cannot tell them apart

Three failures with different signatures and different remedies, plus an
explicit state for the record being unable to separate them -- and the
docstring says why: "Most disaster self-report cannot separate them, and
the field says so rather than guessing."

That is the sixth instance of one repair across this drop family and the
third designed in rather than found:
""".strip())
print()
for cid, where, what in [
    ("PB_004", "frame_sim option_gain", "0 options found == never ran"),
    ("PB_012", "binary_audit handoff()", "above ceiling == never checked"),
    ("GC_004", "MECHANISM_10 R3", "not cited == no corpus searched"),
    ("MD_002", "moral-decomposer reduces_to", "irreducible == routed elsewhere"),
    ("GC_010", "SUBCASE_10A S1", "absent vs zero -- specified"),
    ("DL_008", "anchor.py routing states", "unrouted vs absent -- implemented"),
    ("CC_001", "closure.py knowledge_state", "three failures vs not_separable"),
]:
    print("  %-8s %-30s %s" % (cid, where, what))
print()
print("""
`knowledge_separable` reports it, and `detail()` prints "The record cannot
separate the three failures" when it fires. Sections 2 and 3 are about the
two places in the same file where the discipline is not applied.
""".strip())

# ------------------------------------------------------------------ CC_002
head(2, "CC_002", "the discriminator collapses unknown with checked-and-absent")
print("""
    rules_out = bool(avail in (PRESENT, PRESENT_LOCAL) and var == CLOSED)

`availability_rules_out_procedure_gap` is the field that decides between
the shape and its rival. The docstring says so: "If the information was
absent, procedure gap stands on its own. If the information was present
... then availability is ruled out and the procedure gap needs a different
explanation."

`AVAILABILITY` includes `None` as a legal value, meaning not recorded.
Measured:
""".strip())
print()
print("  %-38s %-24s %s" % ("state", "information_availability", "rules_out"))
print("  " + "-" * 74)
for label, avail in (("checked, information was absent", C.ABSENT),
                     ("never recorded (None is legal)", None),
                     ("checked, information present", C.PRESENT),
                     ("checked, local memorialised instance", C.PRESENT_LOCAL)):
    s = C.score({"case": "p", "variable_state": C.CLOSED,
                 "information_availability": avail})
    print("  %-38s %-24s %s" % (
        label, str(avail), s["availability_rules_out_procedure_gap"]))
print("""
Rows 1 and 2 are different states and return the same value. "We looked and
the information was not there, so the procedure gap stands on its own" and
"nobody recorded whether the information was there" are the measurement and
its absence, and `bool()` merges them into False.

What makes this the sharp one rather than a routine instance: the same
function keeps the distinction two lines away, and the selftest asserts it.
""".strip())
e = C.score({"case": "e"})
print()
print("  budget_consumed on an unfilled case : %r" % e["budget_consumed"])
print("    selftest check: \"budget flag none not false\"")
print("  rules_out       on an unfilled case : %r" % e["availability_rules_out_procedure_gap"])
print("    no selftest check for the unrecorded case")
print("""
`budget_consumed` is `None if spend is None else spend >= 1.0` -- correct,
deliberate, and pinned. `rules_out` is `bool(...)` -- and it is the field
that adjudicates the rival the whole design is built around.

Same repair, same file, one applied and one not. A three-valued return
(None / False / True) needs no new vocabulary: `None` when availability was
not recorded, `False` when it was recorded absent.
""".strip())

# ------------------------------------------------------------------ CC_003
head(3, "CC_003", "knowledge_separable fails open on an omitted field")
print("""
    "knowledge_separable": c.get("knowledge_state") != NOT_SEPARABLE
""".strip())
print()
print("  %-24s %-20s %s" % ("case", "knowledge_state", "separable"))
print("  " + "-" * 56)
for label, ks in (("states not_separable", C.NOT_SEPARABLE),
                  ("states not_taught", C.NOT_TAUGHT),
                  ("omits the field", "__OMIT__")):
    c = {"case": "p"}
    if ks != "__OMIT__":
        c["knowledge_state"] = ks
    s = C.score(c)
    print("  %-24s %-20s %s" % (label, str(s["knowledge_state"]),
                                s["knowledge_separable"]))
print("""
A case that omits `knowledge_state` reads as SEPARABLE -- the informative
state. The default runs toward the claim rather than away from it, which
is the opposite of what presented-binary's `binary_audit` does with every
one of its eleven checks (PB_008: every default runs toward `absent`).

`SKELETON` defaults the field to `not_separable`, so anything from `--new`
is safe. A hand-written case is not, and the selftest covers the stated
values and not the omitted one.

Small fix, same shape as section 2: compare against the vocabulary rather
than against one member of it -- separable only when the value is one of
the three named failures.
""".strip())

# ------------------------------------------------------------------ CC_004
head(4, "CC_004", "argument handling regresses against both sibling tools")
print()
print("  %-32s %s" % ("tool", "bounds-checked lookup after a flag"))
print("  " + "-" * 68)
for path in ("domain-ledger/ledger.py", "domain-ledger/anchor.py",
             "closure-cost/closure.py"):
    src = open(os.path.join(ROOT, path), encoding="utf-8").read()
    print("  %-32s %s" % (path, "if len(a) > i + 1 else None" in src))
print()
print("  measured exit codes:")
print("    closure.py --case            IndexError, rc 1")
print("    closure.py --case unknown    'no case named unknown', rc 1")
print("    closure.py --branch unknown  empty table, rc 0")
print("""
Both sibling tools in this family guard the lookup after a flag;
closure.py does not, so `--case` with no argument raises IndexError
instead of a message. `--new` in the same file IS guarded, so the pattern
is known to the author and applied once of three times.

The second asymmetry is between the two lookups. An unknown case name
errors on stderr with rc 1; an unknown branch name prints an empty table
and exits 0. A typo in a branch name is indistinguishable from a branch
with no cases in it -- which is the same shape as section 2 one layer out,
at the CLI.
""".strip())

# ------------------------------------------------------------------ CC_005
head(5, "CC_005", "the instrument branch is mechanism 6 with a rate on it")
print("""
    instrument   a reliable intermediary exists and becomes the reading.
                 The underlying quantity stops being sampled directly.
                 Failure clusters where the intermediary has been correct
                 for a long time, which is the inverse of how reliability
                 is usually scored.

`uninstrumented/`'s sixth mechanism, PROXY SUBSTITUTION, is "an
enforceable measure displaces the target it stood in for" -- the register's
worked entry being hours-since-last-drive standing in for fitness to drive.
That is the first sentence here.

The second sentence is not in the register. PROXY SUBSTITUTION as filed
has no time term: it says the displacement happened, not that the risk
accumulates with the proxy's track record. `signal.years_correct` is that
term, and the claim on it is directional -- a longer correct record is a
larger exposure, because reliance grew with it and direct sampling stopped.

That is a real addition to an existing mechanism rather than a new
mechanism, and it is checkable in principle without any new vocabulary:
across recorded instrument failures, is time-since-last-direct-sample
correlated with response delay. The field exists; no case does.
""".strip())

# ------------------------------------------------------------------ CC_006
head(6, "CC_006", "an empty corpus prints a clean report -- third tool")
print()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    C.table([])
out = buf.getvalue().strip().splitlines()
print("  rows printed  : 0")
print("  lines printed : %d" % len(out))
print("  exit code     : 0")
print()
print("  siblings on the same state:")
for path, refuses in (("category-weld/weld.py", True),
                      ("presented-binary/binary_audit.py", True),
                      ("generation-capacity/capacity.py", True),
                      ("domain-ledger/ledger.py", False),
                      ("domain-ledger/anchor.py", False),
                      ("closure-cost/closure.py", False)):
    print("    %-38s refuses on empty: %s" % (path, refuses))
print("""
Three tools refuse, three print. The split is by drop family rather than
by design intent -- the three that refuse are the older ones.

closure.py does better than the other two on one point: its table footer
states the corpus condition rather than only the column meanings.

    No case here quantifies the mechanism. These are properties of the
    records, and the records were not built to ask this.

That sentence is true of an empty run and of a full one, and it is the
honest framing for a folder whose readouts are all properties of records
that were written for another purpose. DL_005 stands for all three: the
line prints over zero cases and reads the same.
""".strip())

# ------------------------------------------------------------------ CC_007
head(7, "CC_007", "the tool refuses to fill its central field, and names the mechanism")
CASES = [json.load(open(os.path.join(HERE, "cases", f), encoding="utf-8"))
         for f in sorted(os.listdir(os.path.join(HERE, "cases")))
         if f.endswith(".json")]
S = [C.score(c) for c in CASES]
print("""
README, WHAT THE TOOL DOES NOT DO:

    It does not estimate diagnostic spend where the source lacks the
    numbers. Hawaii's 38 minutes is the duration of the ERROR, not of
    anyone's decision, and substituting it would be PROXY SUBSTITUTION.

`diagnostic_spend` is the readout the folder exists for. A 38-minute
number is sitting in every account of the incident, it would fill the
cell, and the author names why it must not: it measures a different
quantity, and putting it there would be `uninstrumented/`'s sixth
mechanism -- an enforceable measure displacing the target it stood in for.

The refusal is specific rather than blanket. The denominator IS filled:
""".strip())
h = next(c for c in CASES if c["case"] == "hawaii-missile-alert")
print()
print("  hawaii latency.budget_seconds     %s" % h["latency"]["budget_seconds"])
print("  hawaii latency.diagnostic_seconds %s" % h["latency"]["diagnostic_seconds"])
print("  resulting diagnostic_spend        %s" % C.fmt(
    C.score(h)["diagnostic_spend"]))
print("""
Budget is flight time under a real threat, which is a property of the
physics and is knowable. The numerator is a per-respondent
time-to-first-protective-action distribution, which nobody published. One
half filled, one half refused, and the note says which and why.

That is the strongest single move in the drop. Elsewhere in this repo the
register's mechanisms are used to diagnose an instrument after the fact;
here one is used ahead of time as a reason not to produce a number.
""".strip())

# ------------------------------------------------------------------ CC_008
head(8, "CC_008", "the schema has a mixed branch and the mixed case is not coded mixed")
from collections import Counter
b = Counter(s["branch"] for s in S)
print()
for br in C.BRANCHES:
    print("  %-12s %d" % (br, b.get(br, 0)))
print("""
closure.py's docstring states the rule:

    A case that mixes them is recorded as mixed rather than forced into
    one.

The corpus contains exactly one case that mixes them, and it is coded
`event`. From hawaii-missile-alert's own signal note:

    A second signal was relied on in the opposite direction: some
    discounted the alert because air-raid sirens were not sounding,
    treating silence on a different instrument as evidence of no threat.
    That fragment is an instrument-branch reading sitting inside an
    event-branch case.

And from its open list, and from C4's status in the claim table, in the
same words: whether it should be split out is unsettled.

So the rule and the open question point different ways. The docstring says
record it mixed; the case holds the decision open between splitting it
into a separate instrument case and leaving it. Those are both reasonable
and neither is what the stated rule prescribes.

Related to DL_011 and distinct from it. There, `absent_established` was
unused because no link had been investigated far enough to earn it -- the
state was unearned. Here the state is earned, acknowledged twice in the
delivery, and a different value is recorded.
""".strip())

# ------------------------------------------------------------------ CC_009
head(9, "CC_009", "CC_002 instanced: the instrument case needs a third value")
d = next(c for c in CASES if c["case"] == "dash-warning-light")
sd = C.score(d)
print()
print("  dash-warning-light")
print("    variable_state           %s" % sd["variable_state"])
print("    information_availability %s" % sd["information_availability"])
print("    rules_out                %s" % sd["availability_rules_out_procedure_gap"])
print("    procedure_gap collapsed  %r" % sd["procedure_gap_collapsed"])
print("    ground                   %s" % sd["collapse_ground"])
print("""
CC_002 recorded that `availability_rules_out_procedure_gap` merges
"checked, information absent" with "never recorded". The instrument case
adds a third state the same boolean cannot hold: NOT APPLICABLE.

The procedure-gap rival is an event-branch object. On the instrument
branch the missing quantity is direct sampling, not procedure, and the
case says so in the field the readout carries:

    Not applicable on this branch. Procedure is not the missing quantity;
    direct sampling is.

`collapsed_into_closure` correctly reads `None` here. `rules_out` reads
`False` -- the same value an event case returns when the information was
checked and found absent, which is a substantive finding on that branch.

So the field now needs three distinctions, not two: applicable and ruled
out, applicable and not ruled out, not applicable. The information is in
the record and prints in `detail()`; the derived boolean is the only place
it collapses. Same shape as DL_003 and DL_012 -- the per-item text
survives and the scalar merges.
""".strip())

# ------------------------------------------------------------------ CC_010
head(10, "CC_010", "two circularities, both disclosed before use")
print("""
DISCLOSED WEAKNESSES, first item:

    `variable_state` is inferred, never measured. Nothing in any source
    recorded a prior probability before the event. In Hawaii it is
    inferred from the procedure-knowledge finding, which is the same
    evidence C3 uses -- so C3 and the coding of that case are not
    independent.

Checkable, and it holds: hawaii's `variable_state: closed` and its
`procedure_gap.ground` both rest on the survey finding about never having
heard a recommendation, and C3's status cites that same case.
""".strip())
print()
print("  hawaii variable_state       %s   (inferred, per the disclosure)" %
      C.score(h)["variable_state"])
print("  hawaii procedure_gap ground rests on the same survey finding")
print("  C3 status                   'supported in one direction by the Hawaii case'")
print("""
C5's status discloses a second one, about a series not yet used:

    The rail-crossing data is the nearest available series and the
    exposure denominator there is modelled per warning-device category,
    which is circular for this purpose.

A denominator modelled per device category cannot test a claim about which
device categories fail, and the claim table says so before the series is
touched. That is the `generation-capacity` GC_003 shape -- a denominator
that does not survive the question being asked of it -- caught in advance
rather than in audit.

Both disclosures cost the drop something. C3's support is one case whose
coding is not independent of it, and C5's nearest data is unusable as
constituted. Neither is softened.

What is left unmeasured: `signal.years_correct` is the rate term that
distinguishes the instrument branch and makes C5 invert standard scoring.
""".strip())
print()
for s in S:
    print("  %-22s branch=%-11s years_correct=%s" % (
        s["case"], s["branch"], C.fmt(s["signal_reliability_record"])))
print("""
0 of 3, including the one case on the branch it defines. The case names
where the number would come from -- "the rail-crossing signal is the same
branch with better data available. It is a separate case file and is not
yet written" -- which is a statement of intent, not a verification claim
about a file that should exist. Different shape from CW_001 / PB_001 /
GC_009, and worth keeping apart from them.
""".strip())

# ------------------------------------------------------------------ CC_003 update
head(11, "CC_003", "not tripped by the delivered corpus, which is the point")
print()
for s in S:
    print("  %-22s knowledge_state=%-16s separable=%s" % (
        s["case"], s["knowledge_state"], s["knowledge_separable"]))
print("""
All three cases state `not_separable` explicitly, so the fail-open default
CC_003 records is never exercised by the delivered data. The README says
this is "the honest state of the published record rather than a gap in the
transcription", and the table confirms it.

That is exactly why the defect survives. A default that runs toward the
informative state is invisible on data written by someone who knows the
schema, and fires on the first case written by someone who does not --
which, for a folder whose README invites others to add cases, is the
population it will meet.
""".strip())


print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as CC_001..CC_010")
print(BAR)
