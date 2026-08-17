# AUDIT_NOTES — category-weld

Added, not delivered. [`README.md`](README.md),
[`MECHANISM_09.md`](MECHANISM_09.md), [`CLAIM_TABLE.md`](CLAIM_TABLE.md),
[`weld.py`](weld.py), [`test_weld.py`](test_weld.py) and both files under
[`welds/`](welds/) are the drop as received and are not modified.
Everything in this file, and everything it points at, is audit content.

    python3 weld_audit.py

## File status

| file | status |
|------|--------|
| `MECHANISM_09.md` | delivered, drop 1, verbatim |
| `README.md` | delivered, drop 1, verbatim |
| `CLAIM_TABLE.md` | delivered, drop 1, verbatim |
| `welds/rural.json` | delivered, drop 1, verbatim |
| `welds/capital.json` | delivered, drop 1, verbatim (re-delivered byte-identical ×3) |
| `welds/hierarchy.json` | delivered, drop 3, verbatim — third term, first to carry an `open` list |
| `weld.py` | delivered, verbatim — **drop 3 version**, six lines added so `detail()` renders a term's `open` list |
| `test_weld.py` | delivered, drop 2, verbatim |
| `reconstruction/weld.py` | superseded reconstruction, kept as the comparison object |
| `reconstruction/test_weld.py` | superseded reconstruction |
| `weld_audit.py` | added |
| `AUDIT_NOTES.md` | added |
| `samples/` | added |

Drop 1 named `weld.py` and `test_weld.py` under Files and shipped neither,
so both were reconstructed from the four documented call sites with
`[CHOICE]` at nine points the prose left the arithmetic open. Drop 2
delivered them. The reconstruction is kept because one of those nine
choices was wrong in a way that produced a finding, and the disagreement
is the most useful thing in the folder.

## Claims

Refutation protocol as in the delivered table: a break is a measurement.
Update the claim, never retune the scorer to preserve a claim.

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| CW_001 | `CLAIM_TABLE.md`'s statement that `max_spread` and `bias` are "verified against synthetic fixtures in `test_weld.py`" holds — the fixtures exist, run, and check hand-computed values | a fixture failing, or the assertions not covering the two named readouts | **CLOSED — verified**, see CW_013 for what the fixtures do not reach |
| CW_002 | `MECHANISM_09.md`'s test condition 2 is refuted on the literal reading (English) and holds on the record reading; the seed files are written under the second and the doc states the first | showing the seed terms' hidden components are carried as separately reportable fields in their own records | SUPPORTED |
| CW_003 | The two-part test has one part instrumented: all four score fields measure condition 1, and condition 2 has no readout anywhere in the drop | a readout in the drop that returns whether the record carries a separate handle | SUPPORTED |
| CW_004 | ~~`max_spread`, defined as a ratio, diverges at the paradigm weld~~ | the delivered `rel_change` being multiplicative, so an unmoved component is 1.0 and the spread converges | **REFUTED** — by the delivered file, against this audit |
| CW_005 | On the set as delivered the only live readout returns the same value for both seed terms | a third term whose `n_cases` differs, or either seed term acquiring a quantified case | SUPPORTED |
| CW_006 | `bias` over one resolvable direction is 1.0 by construction and the delivered file has no floor | a floor in the delivered spec, or a bias formulation that is not sign-consistency | SUPPORTED, demonstration instance **corrected** |
| CW_007 | 2 of 8 named cases carry a readings block, 1 carries a usable ratio, 0 carry the two a spread needs | any case in `welds/` acquiring two usable components | SUPPORTED |
| CW_008 | C1 survives a structural check against the eight, and the survival runs through CW_002 | a weld case where the hidden component IS separately named in the record and displaced anyway — that is proxy substitution, not a weld | SUPPORTED |
| CW_009 | C5 compares two rates and neither has a denominator; the generation rule under it is checkable one term at a time | a stated denominator for "prone", or a run of the one-term test | SUPPORTED |
| CW_010 | `max_spread` is undefined at total collapse: `rel_change` rejects `after <= 0`, so a component reaching zero is dropped and its case falls out as unquantified | a stated rule for what a component reaching zero scores | SUPPORTED |
| CW_011 | `case_direction`'s docstring is inverted against its body; `test_weld.py`'s comments side with the body | reading the sign convention the other way and finding the docstring consistent | SUPPORTED |
| CW_012 | The `--new` template carries a placeholder divergence with an empty id, which `score()` counts, so a blank file scores on the only live readout | `n_cases` counting only cases that have been named | SUPPORTED |
| CW_013 | The delivered fixtures reach 2 of `rel_change`'s 6 exit branches, and the unreached set includes the branch that decides CW_010 | a fixture exercising the `after <= 0` branch | SUPPORTED |
| CW_014 | A third term arrives. `n_cases` now returns two distinct values over three terms, separating `hierarchy` from the other two and still not separating `capital` from `rural` — the pair `CW_005` was stated about | either seed term acquiring a different case count | SUPPORTED — CW_005 stands, reach unchanged |
| CW_015 | The new `open` field carries a pre-registration guard (fix the read-vs-imposed criterion before any series is run), and `TEMPLATE` has no `open` key, so `--new` never prompts for it | `open` appearing in `TEMPLATE` | SUPPORTED |
| CW_016 | `hierarchy`'s `naturalness-argument` case states C4's directional-weld point structurally — support and application land on different components of one term with no handle marking the switch — and names the folder's first concrete data source (fire-service credential requirements, documented and dated) | a handle in general use that marks the switch | SUPPORTED, unmeasured |
| CW_017 | `tracked_by_label` is declared a judgment call in `hierarchy`'s own `open` list, with the competing candidate and its condition named; nothing in the schema records the choice or its alternative, so two terms with the same structure and different label choices are indistinguishable to the scorer | a field carrying the choice and its reason | SUPPORTED |

## 1 — CW_001, closed by delivery

Drop 1's `CLAIM_TABLE.md` said `max_spread` and `bias` "are implemented
and verified against synthetic fixtures in `test_weld.py`" while shipping
neither file. That was recorded `UNVERIFIED` — a gap, not a defect — with
the falsifier "the delivered files turning up".

They turned up. The statement holds: `test_weld.py` builds a synthetic
term with three quantified cases and one unquantified one and checks
`n_cases`, `n_quantified`, `n_unquantified`, `max_spread` and `bias`
against hand-computed values. Six assertions, all pass.

True and partial — §4 measures how partial.

## 2 — CW_004 is REFUTED, and this audit is what it refutes

The first pass read "largest ratio between component relative-changes" as
an **additive** relative change, `(after − before) / |before|`. On that
reading an unmoved component is 0, and a ratio taken against it diverges.
The paradigm weld — the tracked component holding while the hidden one
collapses — is exactly an unmoved tracked component, so `max_spread` ran
to infinity precisely where the mechanism is cleanest. That was CW_004.

The delivered `rel_change` is **multiplicative**: `after / before`. An
unmoved component is 1.0.

    label after      delivered   reconstruction
    50.00                1.000            1.000
    90.00                1.800            5.000
    99.00                1.980           50.000
    99.90                1.998          500.000
    99.99                2.000         5000.000
    100.00               2.000               --

The delivered statistic converges to 2.000. There is no divergence, and
CW_004 was a property of a `[CHOICE]` this audit made, not of the
mechanism.

The delivered choice is also better for a reason worth stating: a ratio of
multipliers is dimensionless *and* its identity element sits at "did not
move", which is where the tracked component is expected to sit. An
additive relative change puts the statistic's zero there instead. Putting
a singular point where the data is expected to be is the defect the first
pass introduced and then reported as a finding.

What survives is the shape, relocated — §3.

## 3 — CW_010, the same shape in the right place

`rel_change` guards with `if a <= 0 or b < 0: return None`. A component
that reaches exactly zero has no ratio, is dropped from the case, and if
it was one of two quantified components the whole case leaves `max_spread`
and `bias` as unquantified.

    hidden after       max_spread   components read
    10.00                    10.0                 2
    1.00                    100.0                 2
    0.10                   1000.0                 2
    0.01                  10000.0                 2
    0.00                       --                 1

Total collapse is the mechanism's maximal divergence, and `rural.json`'s
own `employment-concentration` note describes it literally: "One packing
facility closure **zeroes** regional employment at once."

This is a real guard, not an oversight — `max/min` with `min = 0` is a
division by zero, and the guard is what stops it. What the guard answers
by silence is what a component reaching zero should score. A count that
hits zero is not missing data; it is the reading, and it is the reading
the term is least able to carry.

## 4 — CW_013, the fixtures reach two branches of six

`rel_change` has six exit points. Counted against every reading in
`test_weld.py`'s fixture:

    B1 empty/absent reading         reached
    B2 before or after is null      not reached
    B3 non-numeric                  not reached
    B4 before == 0                  not reached
    B5 after <= 0 or before < 0     not reached
    B6 usable, returns a ratio      reached

B5 is the branch that decides §3. So the verification claim in §1 is true
of the arithmetic that runs on ordinary data and silent on the arithmetic
that runs at the mechanism's limit case. A fixture for it is two lines,
and adding one would force the zero question to be answered rather than
guarded.

B4 is the mirror: a component that *starts* at zero — growth from nothing,
the first enterprise type in a region — has no ratio either.

## 5 — CW_011, one word

    """+1 if the untracked component fell relative to the tracked one,
       -1 if it rose relative, 0 if not resolvable."""
    ...
    d = math.log(far[1] / ratios[tracked])
    return -1 if d < 0 else 1

`far < tracked` means the untracked component fell relative to the tracked
one, which makes `d < 0`, which returns **−1**. The docstring says +1.
Measured:

    untracked fell   -> case_direction = -1
    untracked rose   -> case_direction = +1

`test_weld.py`'s own comments side with the body: *"# a holds, b falls
10x -> spread 10, direction -1 (b hidden below a)"*.

Blast radius is small — `bias` takes `|sum(dirs)|`, so the convention
cancels and no number in the drop moves. It matters to a reader deciding
which side of a weld is being hidden, which is what the paragraph under
the function says the sign is for. The body is right; the docstring is
backwards.

## 6 — CW_006 stands, its demonstration corrected

`bias` is `|Σ sign| / count` with no floor in the delivered file, so one
resolvable direction reads **1.000** — the value `MECHANISM_09.md` glosses
as "one component is systematically standing behind another", returned by
a statistic that has watched one component move once. `null-harness/`
calls this `CONSTANT_FIRES`. The claim stands.

**Correction.** The first pass demonstrated it on `capital /
socialized-downside` with `revenue_claim` filled in. That instance does
not hold against the delivered code: `case_direction` returns 0 when the
**tracked** component is unquantified, and `ownership_title` has no
readings in that case, so `bias` stays `None` there.

    capital with revenue_claim filled:  bias = --   max_spread = 6.768

The delivered code is stricter than the reconstruction and immune to that
particular reading. The floor is still absent, and still reachable by any
case in which the tracked component *is* measured — the likelier case,
since the tracked component is by definition the one the record already
carries.

## 7 — CW_012, the template scores

`README.md` documents `python3 weld.py --new employed > welds/employed.json`.
`TEMPLATE` carries a placeholder divergence with `"id": ""`, and `score()`
counts `len(divergences)`, so:

    blank template -> n_cases = 1, placeholder id = ''

`n_cases` is the only readout returning a number for either seed term, so
a file with nothing in it scores on the folder's only live measurement.
`MECHANISM_09.md` defines the readout as "how many divergence cases can be
**named**"; a case with no id has not been named. Filtering on a non-empty
id is faithful to that sentence rather than a patch to it.

## 8 — CW_002, one word

`MECHANISM_09.md`'s test:

> 2. The language provides no separate handle for the components that
>    diverged.

Read as a statement about English, the drop's own files refute it. All
nine components across the two seed terms carry an English name and a
unit — "ownership distribution", "independent operators per 1000 acres";
"authority over what gets built and toward what objective", "share of
decisions determined".

Read as a statement about the **record** — the census category, the
statistic, the accounting line — it holds, and it is the reading the seed
files are actually written under. `tracked_by_label` is a field about what
the record reads off, not about what English can say.

One word — *record* for *language* — separates a condition refuted by the
drop's own files from a live one. §10 shows the choice is load-bearing.

## 9 — CW_003, one part of the test instrumented

Two conditions, four score fields, all four about condition 1:

    n_cases        how many divergences are named          -> condition 1
    n_quantified   how many carry paired readings          -> condition 1
    max_spread     how far components moved apart          -> condition 1
    bias           whether they moved apart consistently   -> condition 1
    (none)         whether the record carries a handle     -> condition 2

A term with real divergence cases and perfectly good separate handles in
the record scores exactly like a weld. By the doc's own test that term is
"a summary, not a weld", and nothing in the drop can tell them apart. The
missing readout has a shape and it is cheap: components for which the
record has an independently reportable field, over total components.

## 10 — CW_005, CW_007, CW_008, CW_009

**CW_005.** Both seed terms return `n_cases = 4`, `n_quantified = 0`, and
`--` for both live readouts. The scorer assigns them an identical score
and the number it agrees on is the count of paragraphs someone wrote.
This is the drop's own C3 shown from its own data. It does not close C3 —
that falsifier needs a populated set and there is none — but it moves it
from asserted to demonstrated on a set of size two.

**CW_007.** Two of eight named cases carry a readings block, one carries a
usable ratio, zero carry the two a spread needs. The distance to the first
number is now measurable rather than described: filling `capital /
socialized-downside`'s one missing pair returns `max_spread = 6.768`, the
folder's first non-`--` readout — in the case whose own note says the
divergence between those two components "is the entire structure".

**CW_008.** C1's falsifier is "showing any of the eight already covers the
two seed terms". The nearest competitor is `PROXY SUBSTITUTION`, which
requires two named things and a substitution: "fitness to drive" is a
phrase and "hours since last drive" was written into a rule in its place,
so the register entry can name the target it lost. A weld is the case with
no second name to point at — one word, components never separately
carried, no substitution event and no displaced target. `SCALAR DEMAND` is
the other near miss and is a different collapse: one quantity's variation
over a domain flattened to a scalar, against N quantities flattened to one
handle. C1 survives — and the survival runs through §8, because on the
English reading of condition 2 the hidden components become named targets,
`PROXY SUBSTITUTION` absorbs both seed terms, and C1 falls.

**CW_009.** C5 compares two rates and neither has a denominator — prone
per term encountered, per query, per output? Its stated falsifier needs a
corpus shown never to separate the components, which needs the corpus. The
generation rule underneath is separately statable and needs no comparison:
a representation summarising contexts of occurrence has no gradient
pulling apart components the contexts never separate. That is testable one
term at a time — hand a model a divergence case for a welded term and
score whether the components are held apart without being handed the
decomposition. Split the claim, don't discard it.

## 11 — CW_014, a third term

    term           comps   cases    open   domain
    capital            5       4       0   economics / corporate ownership
    hierarchy          5       5       3   governance / organizational theory / naturalness arguments
    rural              4       4       0   policy / agricultural statistics / census

`CW_005` said the only live readout returns the same value for both seed
terms. Over three terms it returns two distinct values, so it separates
`hierarchy` from the other two — and still does not separate `capital`
from `rural`, which is the pair the claim was stated about. The claim
stands and its reach has not grown: one value distinguishes one term.

The domain spread does change. The two seeds were policy/economics;
`hierarchy`'s five divergence cases sit in animal behaviour, volunteer
fire service, credentialed fire service, surgical teams, and a rhetorical
argument. **Cross-field at the case level**, while the domain label stays
adjacent to the first two.

It does not move `uninstrumented/` `UNI_002`, which asks whether sorting
the REGISTER by mechanism cuts across field. CATEGORY WELD is still not a
filed entry there.

## 12 — CW_015, the OPEN field and its guard

`weld.py` gains six lines: `detail()` renders a top-level `open` list. One
of `hierarchy`'s three items is a methodological guard stated before any
data exists:

> The read-vs-imposed criterion must be fixed BEFORE any series is run.
> Sorting cases into 'not really hierarchy' after seeing the cut rate
> makes the finding true by construction.

That is the failure the term is most exposed to, named by the author, in
the file, ahead of the measurement. If `cut_rate` comes back high only in
cases sorted as hierarchy *after* the rate was seen, the finding is
circular — and that is undetectable from the finished series. Only fixing
the criterion first prevents it.

Same shape as `reasoning-gate/` `G-PRE` and
`photoperiod-claim-harness/`'s `MechanismEdit` protocol, reached here from
a third direction, and the first weld term to carry it.

The gap: `TEMPLATE` has no `open` key, so `--new` never emits one. A field
carrying a pre-registration guard is the field a new term most needs
prompting for. Same shape as `measurement-fork/` `MF_017` — a stated rule
with no schema slot — one folder over and much cheaper to close.

## 13 — CW_016, the naturalness case

`hierarchy`'s fifth divergence is not components diverging in the field.
It is the weld being *used*:

> The claim 'hierarchy is natural' is supported by pointing at nested
> containment and at environment-ordered dominance, then applied to
> imposed orderings with standing. Both supports sit in components where
> cut_rate is zero. The application sits in the component where cut_rate
> is unbounded. No separate handle in English marks the switch.

C4 says `bias` separates directional welds from imprecise ones with no
input about intent. This case makes the same structural point one level
up — support and application land on different components of one term,
and the term carries no handle marking the move.

Stated, not measured: `cut_rate` has zero collected series. What it would
take is what the `open` list also says — the fire service, volunteer
through present, credential requirements documented and dated. **That is
the first concrete data source named anywhere in this folder.**

## 14 — CW_017, a declared judgment call

> `tracked_by_label` is a judgment call here as elsewhere.
> `nested_containment` is the reading because it is what is pointed at in
> naturalness arguments; `imposed_ordering` has a competing case if the
> domain is taken as organizational practice rather than the naturalness
> claim.

`tracked_by_label` is load-bearing: `case_direction()` returns 0 when the
tracked component is unquantified, and `bias` is computed entirely
relative to it. A different tracked component can flip the sign of every
case direction in a term.

Declaring the choice, naming the alternative, and stating the condition
under which the alternative wins is more than the other two terms do, and
is the right handling for a quantity with no procedure behind it.

What is not in the schema is a field for it. It lives in `open` as prose
on one term; `weld.py` reads `tracked_by_label` and nothing reads the
reason, so two terms with the same structure and different label choices
are indistinguishable to the scorer — the same declaration-not-a-check
shape as `generation-capacity/` `GC_003`'s `scored_against`.

## Relation to the rest of the repo

- `uninstrumented/` — this is a proposed ninth mechanism for that
  register. It arrives with two cases, which `UNI_007` records that
  `PROXY SUBSTITUTION` did not. It does **not** move `UNI_002` (does
  sorting by mechanism cut across field?): both seed terms are policy /
  economics.
- `null-harness/` — §6 is `CONSTANT_FIRES` on a consistency statistic;
  §4 is the same known-null-first discipline applied to a fixture set
  rather than to a gate.
- `measurement-fork/` — §2 is the reconstruct-from-call-sites risk
  arriving with a bill. `MF_001` marked reconstructions with `[CHOICE]`
  precisely so a later delivery could adjudicate them; this is the first
  time one did, and it went against the audit.
- `aperiodic-order-sim-stack/` — §2 has the same shape as `AOS_006`: an
  audit finding that turned out to be an artifact of the instrument the
  auditor chose, corrected from the same paragraph's own numbers.
- `criteria-drift/` — `CD_002` found drift primitives returning unsigned
  distances where a sign was needed; §5 is the mirror, a sign convention
  that is right in the body and backwards in the documentation.
