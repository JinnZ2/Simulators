# effective-redundancy-audit

A system claims N-fold redundancy and fails anyway, all N channels down
together. The protocol's claim: the channels were never N — they shared
a node the redundancy diagram cannot draw, because the shared node is a
**process, an input, a decision, or a budget**, not a component. Six
such classes (authorization, information, discretion, maintenance,
envelope, verification), coded yes/no per case, give `N_eff` — the
channels that survive failure of every shared node.

`SOURCE_DROP.md` is delivered verbatim, and it **ships real code**
(Section 4). `effective_redundancy.py` is that code, landed verbatim and
not edited; `worked_example.py` is the Section 5 example, verbatim but
for the import line.

    python3 effective-redundancy-audit/effective_redundancy.py  # the module
    python3 effective-redundancy-audit/worked_example.py        # the delivered run
    python3 effective-redundancy-audit/audit.py                 # what holds
    python3 effective-redundancy-audit/selftest_er.py           # the checks

## The study is not run here — and the third reason is a refusal

To run the coding study you need the investigation reports, two blind
coders, and cases coded from those reports. All three are unavailable:

    www.csb.gov  www.ntsb.gov  www.iaea.org  www.fema.gov  www.gao.gov
    -> every one 000 (allowlist egress)

and there are no two human coders. **The third block is not a
limitation, it is a refusal:** coding a real disaster's shared-node
structure is a claim about a real event. A fabricated `Case` for
Fukushima or Katrina asserting *N_eff = 1, that is why it failed* would
be a fabricated finding about a real disaster. So the audit runs the
author's one delivered coding (Kerr County) and codes no case of its
own — the selftest asserts it constructs zero `Case` objects.

So **H1 vs H0 is UNVERIFIED here.** What is checkable is the delivered
instrument.

## The finding: the protocol's primary guard is not computed

Section 3.2: *"Report the kappa first, always."* Section 3.4 makes a low
kappa one of the two *honest* theory-killers — if two coders can't agree
which node was shared, the six classes are narrative, not structure.

The delivered `report()` prints the 2×2, the counterexamples, the Fisher
p, and the nominal averages — **and not the kappa.** And it cannot be
given it: the `Case` dataclass holds one coding, with no field for a
second coder, so the two-coder blind protocol has **no representation in
the shipped code.** `cohen_kappa` is defined and never called, over data
that could not feed it.

The function is correct (perfect agreement → 1.0), so the omission is in
the wiring and the data model, not the math — the instrument's own
primary honesty number is the one it does not produce.

## Why that is load-bearing — the recursion bites

Section 7: *"Mode F is the audit itself ... the checker is a shared
node."* This instrument is coded by humans against one reading of one
report, so by its own Mode F it *is* a shared node — one coder's
judgment is the measurement. Its only defense against that judgment
being narrative rather than structure is inter-coder agreement, i.e.
kappa. That defense is exactly the number the delivered code omits. As
shipped, the tool cannot detect the failure mode the protocol
foregrounds as the honest one.

## What holds up

**Fisher is correct** — the one piece of statistics the code runs is
right, verified against two independent references (`[[3,1],[1,3]]` →
0.4857, `[[8,2],[1,5]]` → 0.03497). **The worked example reproduces the
stated coding** (Kerr 2025 → N_eff=1, 2026 → N_eff=2), with one hedged
prose/code discrepancy (N_nominal ~4 vs 3, the code excluding sirens
that *did not exist*).

**The seed set is self-forbidden and degenerate.** Section 6 says *DO
NOT TEST ON THESE* (circular), and Section 3.1 says *DO NOT sample on
disasters*. The seeds are 5 failed / 1 held, so the 2×2 held column has
n=1 and no test has power — provable from the delivered outcome labels
alone, no channel coding.

**A latent edge:** `contingency` tests `n_eff == 1` exactly, so a
zero-channel failed case lands in the *failed with real redundancy* cell
— a false counterexample from malformed input the code does not guard.

## Files

| file | what |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim, not edited |
| `effective_redundancy.py` | the Section 4 code, landed verbatim |
| `worked_example.py` | the Section 5 example, verbatim but for the import |
| `audit.py` | what holds without running the study, each demonstrated |
| `selftest_er.py` | the checks; run it, it prints its own count |
| `CLAIM_TABLE.md` | `ERA_001..ERA_008` with REFUTATION_PROTOCOL |
| `samples/` | pinned runs |

The delivered files are landed verbatim and carry no `--selftest`
handling; `audit.py` refuses `--selftest` rather than exiting 0. No
`no_severity` exemptions — every screen hit was reworded.

## Scope

Nothing here bears on whether N_eff separates failed systems from ones
that held — the whole study, needing exposure-sampled cases coded blind
from reports this environment cannot reach and this audit will not
fabricate. What is established is about the instrument: its arithmetic
is sound, and it omits its own primary guard.

CC0. Stdlib only, parses under 3.9, phone-buildable.
