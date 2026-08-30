# effective-redundancy-audit — CLAIM_TABLE

`ERA_001..ERA_008`. Claims about the delivered `SOURCE_DROP.md` — a test
protocol that **ships real code** (Section 4, landed verbatim as
`effective_redundancy.py`), plus a worked example (Section 5) and seed
cases (Section 6).

**The study is not run here.** Three things block it, the third
load-bearing: the public investigation reports the protocol names
(CSB, NTSB, IAEA, FEMA, GAO) refuse CONNECT; the design requires two
human coders, blind; and **coding a real disaster's shared-node
structure is a claim about a real event** — constructing a `Case` for
Fukushima and asserting *N_eff=1, that is why it failed* would be a
fabricated finding about a real disaster. Only the author's one
delivered coding (Kerr County) is run — reproduction, not new coding.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `ERA_001` | The study cannot be run here (reports blocked, no coders, no fabrication of real-disaster codings), so H1 vs H0 is UNVERIFIED; only the delivered Kerr County example is executed. | SUPPORTED |
| `ERA_002` | **The finding: the delivered `report()` does not compute the kappa the protocol says to report first, and the `Case` model cannot hold the two codings kappa needs.** | SUPPORTED |
| `ERA_003` | That omission is load-bearing by the protocol's own Section 7 recursion: the instrument's only defense against being narrative-not-structure is the check it does not compute. | SUPPORTED |
| `ERA_004` | The honest positive: `fisher_exact_2sided` is numerically correct, verified against two independent references. | SUPPORTED |
| `ERA_005` | The worked example reproduces the stated coding (Kerr 2025 N_eff=1, 2026 N_eff=2); one prose/code discrepancy (N_nominal ~4 vs 3). | SUPPORTED |
| `ERA_006` | The seed set is self-forbidden (Section 6) and degenerate: 5 failed / 1 held, so no 2×2 test has power — provable from the delivered outcome labels alone. | SUPPORTED |
| `ERA_007` | A latent edge: `contingency` tests `n_eff == 1` exactly, so a zero-channel failed case lands in the "failed with real redundancy" cell. | SUPPORTED |
| `ERA_008` | Whether N_eff separates failed from held is the whole study and is UNVERIFIED — it needs exposure-sampled cases coded blind from public reports. | UNVERIFIED |

---

## ERA_001 — not runnable here, and the third reason is the load-bearing one

The protocol is a coding study. To run it you need the investigation
reports, two blind coders, and a set of cases coded from those reports.
All three are unavailable here:

    www.csb.gov   000      www.ntsb.gov  000     www.iaea.org  000
    www.fema.gov  000      www.gao.gov   000

— egress is an allowlist. There are no two human coders. And **the third
block is not a limitation, it is a refusal**: coding a real disaster's
shared-node structure is a claim about a real event. A fabricated `Case`
for Fukushima or Katrina asserting *N_eff = 1, that is why it failed*
reads as a finding about a real disaster with real dead people. This is
the `PB_001` / `CW_004` rule at its sharpest, and the same line held in
`columbia-chain-cascade` and `household-scope-audit`.

So the audit runs the author's **one delivered coding** (Kerr County,
Section 5) — reproduction of the author's own work — and codes no case
of its own. The selftest asserts `audit.py` constructs zero `Case`
objects.

**Falsifier:** reachable reports and available coders. Then the study
runs and this is about one environment.

## ERA_002 — the protocol's primary guard is not computed

Section 3.2: *"Compute Cohen's kappa on the 6 mode flags across all
cases ... Report the kappa first, always."* Section 3.4 makes a low
kappa one of the two *"honest"* theory-killers: *"coders disagree on
modes → categories aren't real."*

The delivered `report()` prints the 2×2, the counterexamples, the Fisher
p, and the nominal averages — and **not the kappa.** Asserted against
the delivered AST: `report()` calls `contingency` and
`fisher_exact_2sided`, and does not call `cohen_kappa`.

And it *cannot* be given the kappa without changing the data model. The
`Case` dataclass holds one coding — `modes_present` and `channels` — with
no field for a second coder. The two-coder blind protocol that Section
3.2 makes the guard against invented patterns has **no representation in
the shipped code.** `cohen_kappa` is defined and never called, over data
that could not feed it.

The function itself is correct (perfect agreement → 1.0), so the
omission is in the wiring and the data model, not the math. This is the
same shape as `report-typing` `RT_005` / `household-scope-audit`: the
instrument's own primary honesty number is the one it does not produce.

**Falsifier:** a `report()` that computes kappa, or a `Case` that holds
two codings. Neither is in the delivered file.

## ERA_003 — the recursion makes the omission load-bearing

Section 7: *"Mode F is the audit itself. The instrument that certifies
redundancy is validated against one standard. So the checker is a shared
node."*

This instrument is coded by humans against one reading of one report, so
by its own Mode F it **is** a shared node — one coder's judgment is the
measurement. The protocol's only defense against that judgment being
narrative rather than structure is inter-coder agreement, i.e. kappa
(Section 3.4 threat 3). That defense is exactly the number `ERA_002`
shows the delivered code omits.

So the recursion bites in the code, not just the prose: as shipped, the
tool cannot detect the failure mode the protocol foregrounds as the
honest one. The fix is not cosmetic — it requires the two-coder data
model the shipped `Case` lacks.

**Falsifier:** a reading on which the coding is reproducible without
being checked. The protocol itself rejects that (Section 3.2).

## ERA_004 — the honest positive: Fisher is correct

The one piece of statistics the delivered code actually runs is right.
`fisher_exact_2sided` verified against two independently known values:

    tea-tasting [[3,1],[1,3]]     -> 0.48571   (ref 0.4857)
    asymmetric  [[8,2],[1,5]]     -> 0.03497   (ref 0.03497)

The hypergeometric PMF, the extremity sum with the float-tie tolerance,
and the margin handling are all correct, including the degenerate
all-failed table (returns p = 1). The method's statistics are sound; the
gap is the missing guard, not the arithmetic.

**Falsifier:** a 2×2 where `fisher_exact_2sided` disagrees with the
hypergeometric. The references match to 4 decimals.

## ERA_005 — the worked example reproduces the stated coding

A known-answer check on the delivered code, using the delivered data:

    Kerr County 2025   N_eff = 1   (prose: 1, failed)   match
    Kerr County 2026   N_eff = 2   (prose: 2, held)     match

The teaching move — weather radio escapes Mode C but collapses on a
shared reception dependency, so N_eff = 1 not 2 — reproduces exactly.

One discrepancy: the prose says *N_nominal ~4* for 2025 (counting
sirens, which *"did not exist"*), while the code counts channels and
gives **3**. The *"~"* hedges it, and the code is the more defensible
count — a channel that did not exist is not a nominal channel.

**Falsifier:** the code producing a different N_eff than the prose
states. It does not.

## ERA_006 — the seed set is self-forbidden and degenerate

Section 6: *"DO NOT TEST ON THESE. These built the hypothesis. Testing
on them is circular."* And independently, Section 3.1: *"DO NOT sample on
disasters ... sampling only failures conditions on the outcome."*

The seed set is a set of disasters, and its outcomes — transcribed from
the delivered table as **labels only, no channel coding** — are **5
failed, 1 held.** With one held case the 2×2 held column has n = 1, so
cells c and d cannot both be populated and no test has power, regardless
of how the channels are coded. The degeneracy is provable from the
delivered outcome labels alone.

So the seed set demonstrates the coding format and nothing about H1, and
the protocol says so. This audit codes none of the six.

**Falsifier:** a seed set balanced on exposure with several held cases.
The delivered one is not.

## ERA_007 — a latent zero-channel edge

`contingency` classifies on `x.n_eff == 1` exactly. A case with no
channels has `n_eff = 0`, so it is *not* collapsed, and a failed
zero-channel case lands in cell **b** — *"failed WITH real redundancy"* —
a false counterexample that would count against H1.

Minor: a zero-channel case is malformed input. But the exact-equality
test has no channels-nonempty guard, so a data-entry slip becomes a
counterexample rather than an error.

**Falsifier:** an input guard rejecting zero-channel cases. The
delivered code has none.

## ERA_008 — the study's own question is untouched

Whether N_eff separates failed from held (H1) or does not (H0) is the
entire point of the protocol, and nothing here bears on it. It requires
8–15 **exposure-sampled** cases — failed and held, same hazard — coded
blind by two coders from public reports. Reports unreachable, coders
absent, and no case fabricated here.

The protocol's own verdict conditions (Section 3.4: b large, c large,
kappa low, N_nominal also separates) are all untouched in either
direction. What is established is about the instrument — its arithmetic
is sound, and it omits its own primary guard — not about the claim.

**Falsifier:** run the study. That is the whole point of the document,
and this is what a text-only environment can say about the tool before
anyone does.
