# AUDIT_NOTES — category-weld

Added, not delivered. [`README.md`](README.md),
[`MECHANISM_09.md`](MECHANISM_09.md), [`CLAIM_TABLE.md`](CLAIM_TABLE.md)
and both files under [`welds/`](welds/) are the drop as received and are
not modified. Everything in this file, and everything it points at, is
audit content.

Run it:

    python3 weld_audit.py

## File status

| file | status |
|------|--------|
| `MECHANISM_09.md` | delivered, verbatim |
| `README.md` | delivered, verbatim |
| `CLAIM_TABLE.md` | delivered, verbatim |
| `welds/rural.json` | delivered, verbatim |
| `welds/capital.json` | delivered, verbatim |
| `weld.py` | **named in README, did not arrive — reconstructed** |
| `test_weld.py` | **named in README, did not arrive — reconstructed** |
| `weld_audit.py` | added |
| `AUDIT_NOTES.md` | added |
| `samples/` | added |

Same situation as `measurement-fork/widen.py` and `validate.py`:
reconstructed from documented call sites, with `[CHOICE]` at every point
the delivered prose did not fix the arithmetic. Nine such marks in
`weld.py`.

## Claims

Refutation protocol as in the delivered table: a break is a measurement.
Update the claim, never retune the scorer to preserve a claim.

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| CW_001 | `CLAIM_TABLE.md`'s statement that `max_spread` and `bias` are "verified against synthetic fixtures in `test_weld.py`" cannot be checked from the delivery, because neither `weld.py` nor `test_weld.py` arrived | the delivered files turning up and matching the reconstruction's arithmetic | UNVERIFIED |
| CW_002 | `MECHANISM_09.md`'s test condition 2 is refuted on the literal reading (English) and holds on the record reading; the seed files are written under the second and the doc states the first | showing the seed terms' hidden components are carried as separately reportable fields in their own records | SUPPORTED |
| CW_003 | The two-part test has one part instrumented: all three readouts measure condition 1, and condition 2 has no readout anywhere in the drop | a readout in the drop that returns whether the record carries a separate handle | SUPPORTED |
| CW_004 | `max_spread`, defined as a ratio, diverges at the paradigm weld — the tracked component unmoved — so it is unbounded where the phenomenon is cleanest and undefined at the limit | a ratio formulation that stays bounded as the tracked component's relative change goes to zero | SUPPORTED |
| CW_005 | On the set as delivered the only live readout returns the same value for both seed terms | a third term whose `n_cases` differs, or either seed term acquiring a quantified case | SUPPORTED |
| CW_006 | `bias` over one observation is 1.0 by construction, and the delivery is one paired figure away from that being the first bias anyone reads | a floor stated in the delivered spec, or a bias formulation that is not sign-consistency | SUPPORTED |
| CW_007 | 2 of 8 named cases carry a readings block, 1 carries a usable pair, 0 carry the two a spread needs | any case in `welds/` acquiring two paired components | SUPPORTED |
| CW_008 | C1 survives a structural check against the eight, and the survival runs through CW_002: on the English reading of condition 2, PROXY SUBSTITUTION absorbs both seed terms and C1 falls | a weld case where the hidden component IS separately named in the record and displaced anyway — that is proxy substitution, not a weld | SUPPORTED |
| CW_009 | C5 compares two rates and neither has a denominator; the generation rule under it is checkable on one term at a time and does not need the comparison | a stated denominator for "prone", or a run of the one-term test | SUPPORTED |

## 1 — CW_001, the verification claim

`README.md` lists `weld.py` and `test_weld.py` under Files.
`CLAIM_TABLE.md` says the two unquantified readouts "are implemented and
verified against synthetic fixtures in `test_weld.py`". Neither file is in
the drop, so that statement is the one thing in the folder that cannot be
checked from the folder.

Not a defect in the argument — a gap in the delivery, and marked as
`UNVERIFIED` rather than as a negative verdict, per the `claim-audits/`
convention.

The reconstruction is faithful to the four documented call sites and the
three readout descriptions, and it makes nine arithmetic decisions the
prose does not fix. Three of them turn out to be load-bearing:

- the relative-change denominator (`abs(before)`, and `before == 0`
  undefined rather than infinite)
- what a "ratio between relative-changes" is (§4)
- whether `bias` has a floor (§6)

## 2 — CW_002, one word

`MECHANISM_09.md`'s test:

> 2. The language provides no separate handle for the components that
>    diverged.

Read as a statement about English, the drop's own files refute it. Every
component in both seed files has an English name and a unit — "ownership
distribution", "independent operators per 1000 acres"; "authority over
what gets built and toward what objective", "share of decisions
determined". English has handles for all nine.

Read as a statement about the **record** — the census category, the
statistic, the accounting line — it holds, and it is the reading the seed
files are actually written under. `tracked_by_label` is a field about what
the record reads off, not about what English can say.

The doc states the first reading. One word — *record* for *language* —
separates a condition refuted by the drop's own files from a live one.

This is not cosmetic. §8 shows the distinction between CATEGORY WELD and
the register's existing PROXY SUBSTITUTION runs through exactly this
choice.

## 3 — CW_003, one part of the test instrumented

Two conditions, three readouts, and all three readouts are about condition
1:

    n_cases      how many divergences can be named        -> condition 1
    max_spread   how far components moved apart           -> condition 1
    bias         whether they moved apart consistently    -> condition 1
    (none)       whether the record carries a handle      -> condition 2

So a term with real divergence cases and perfectly good separate handles
in the record scores exactly like a weld. By the doc's own test that term
is "a summary, not a weld", and nothing in the drop can tell them apart.

The missing readout has a shape, and it is cheap: components for which the
record has an independently reportable field, over total components. It
would also make the drop's own two-condition test runnable instead of
stated.

## 4 — CW_004, the statistic diverges where the phenomenon is cleanest

`max_spread` is "largest ratio between component relative-changes in any
one case". The paradigm weld, in `rural.json`'s own words:

> Density stays low so the label holds; ownership distribution and
> functional diversity have collapsed.

The tracked component does not move. Measured, holding the hidden
component at −0.5 and walking the label toward unmoved:

    label after   label rel      max_spread
    50.00         -0.5000              1.0
    90.00         -0.1000              5.0
    99.00         -0.0100             50.0
    99.90         -0.0010            500.0
    99.99         -0.0001           5000.0
    100.00        +0.0000               --

Smallest where the weld is weakest, unbounded where it is strongest,
undefined at the ideal case. Consequences: the number is not comparable
across terms, and `max()` over cases selects whichever case came closest
to a perfect weld rather than whichever divergence was largest — which is
not what "largest ratio" is being read as.

A difference of relative changes is bounded, defined at the limit, and
orders cases the same way away from it. That is a change to the readout
and not to a claim, so it is recorded here and **not applied** —
`weld.py` implements the ratio the doc specifies, and returns `None` with
a stated reason at the singular point rather than `inf`.

## 5 — CW_005, the live readout does not discriminate

    term         comp  cases  quant max_spread   bias
    capital         5      4      0         --     --
    rural           4      4      0         --     --

Both seed terms return 4. The other two readouts return `--`. The scorer
assigns the two terms an identical score and the number it agrees on is
the count of paragraphs someone wrote.

This is the drop's own C3 shown from its own data rather than argued. It
does not close C3 — C3's stated falsifier needs a populated set and there
is none — but it moves it from asserted to demonstrated on a set of size
two.

## 6 — CW_006, bias fires before it has seen anything

`bias` is |Σ sign| / count. On one observation that is |±1| / 1 = 1.0
whatever the datum is — the value `MECHANISM_09.md` reads as "one
component is systematically standing behind another", returned by a
statistic that has watched one component move once. `null-harness/` calls
this `CONSTANT_FIRES`.

The guard is load-bearing on the next datum this folder expects.
`capital / socialized-downside` has `risk_bearing` quantified and
`revenue_claim` null. Fill `revenue_claim` and `capital` has exactly one
quantified case, hence exactly one directional observation:

    with the guard      bias = --      (1 observation, minimum 2)
    without the guard   bias = 1.000   on 1 observation

`MIN_BIAS_OBS = 2` is a `[CHOICE]`; the delivered spec names the range
0..1 and no floor. Without one, the first term anyone quantifies reports
maximal directional work on its first pair of numbers.

## 7 — CW_007, one retrieved pair away

    term       case                                 keys   paired
    capital    intermediated-title                     0        0
    capital    socialized-downside                     2        1
    capital    subsidy-without-behaviour-change        0        0
    capital    input-supply-uncompensated              0        0
    rural      industrial-consolidation                2        0
    rural      no-alternate-check                      0        0
    rural      employment-concentration                0        0
    rural      service-withdrawal                      0        0

The delivered `CLAIM_TABLE.md` says "no paired before/after readings
attached", which is accurate. The sharper statement is that the state is
not empty: two cases have a readings block, one has a usable number, and
zero have the two a spread needs.

`capital / socialized-downside` is one retrieved pair short — and its own
note says the divergence between those exact two components "is the
entire structure". `rural / industrial-consolidation` names two components
and leaves all four values null.

## 8 — CW_008, C1 against the eight

C1's falsifier is "showing any of the eight already covers the two seed
terms without adding a mechanism". The one that gets closest is PROXY
SUBSTITUTION: density is enforceable and stands where ownership
distribution is not read.

The separation is in what each mechanism requires to exist.

**PROXY SUBSTITUTION needs two named things and a substitution.** "Fitness
to drive" is a phrase; "hours since last drive" was written into a rule in
its place. The register entry can name the target it lost.

**CATEGORY WELD is the case where there is no second name to point at.**
One word, components never separately carried, no substitution event to
date, no displaced target to name.

SCALAR DEMAND is the other near miss and it is a different collapse: one
quantity's variation over a domain flattened to a scalar, against N
quantities flattened to one handle. Both lose a dimension. They lose
different ones.

C1 survives. What the check also shows: the survival runs through §2. On
the English reading of condition 2 the hidden components ARE named, which
makes them named targets, which makes both seed terms proxy substitution,
and C1 falls. The record reading is what keeps the ninth mechanism
distinct from the sixth.

## 9 — CW_009, C5 has no denominator

C5: "Language models are more prone to welds than to retrieval errors."

Two rates, no denominator on either — prone per term encountered, per
query, per output? And the stated falsifier ("a model separating
components on a term whose corpus never separates them, without external
tooling") requires establishing that a corpus never separates them, which
requires the corpus.

The generation rule underneath is separately statable and does not need
the comparison: a representation that summarises contexts of occurrence
has no gradient pulling apart components the contexts never separate. That
is testable one term at a time — hand a model a divergence case for a
welded term and score whether the components are held apart without being
handed the decomposition.

Recorded as a claim that should be split, not as a claim that is wrong.

## Relation to the rest of the repo

- `uninstrumented/` — this is a proposed ninth mechanism for that
  register. It arrives with two cases, which `UNI_007` records that
  `PROXY SUBSTITUTION` did not. It does **not** move `UNI_002` (does
  sorting by mechanism cut across field?): both seed terms are policy /
  economics, so a ninth mechanism holding two same-field cases adds
  nothing to that check.
- `null-harness/` — §6 is `CONSTANT_FIRES` on a consistency statistic;
  §3 is a classifier with one of its two conditions unmeasured.
- `measurement-fork/` — same reconstruct-from-call-sites situation as
  `widen.py` and `validate.py`; `MF_017`'s shape recurs in §3 (a stated
  rule with no field in the schema to express it).
- `reasoning-gate/` — §4 is a `G-FIT` question: the statistic is not
  blind, but it is unbounded at the point of interest, which is a
  different way for a statistic to fail to discriminate.
- `criteria-drift/` — `CD_002` found every drift primitive returning a
  non-negative distance where the verdict needed a sign. §4 is the mirror:
  a readout with a fine sign and an unbounded magnitude.
