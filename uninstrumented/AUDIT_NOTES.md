# AUDIT_NOTES — uninstrumented

Everything below is added analysis. The delivered files are
[`README.md`](README.md), [`patterns.json`](patterns.json) and
[`scan.py`](scan.py), all verbatim. Added here:
[`uninstrumented.py`](uninstrumented.py) (the register as code, three
checks on itself), [`scan_audit.py`](scan_audit.py) (grades the scanner),
[`case_010_audit.py`](case_010_audit.py),
[`case_011_audit.py`](case_011_audit.py) and
[`case_012_audit.py`](case_012_audit.py) and
[`case_013_audit.py`](case_013_audit.py) and
[`case_014_audit.py`](case_014_audit.py) and
[`case_015_audit.py`](case_015_audit.py) (checks on the six delivered
cases) and [`CLAIM_TABLE.md`](CLAIM_TABLE.md). `cases/case-010.md`
through `cases/case-015.md` are delivered, verbatim.

The delivered README supersedes what follows on two points, and both are
carried into the claim table rather than silently corrected:

- **Eight mechanisms, not seven.** `PROXY SUBSTITUTION` — *enforceable
  measure displaces the target* — is now in the canonical list. The
  register as coded still holds seven entries, so `PROXY SUBSTITUTION` is
  a mechanism with no entry: the first mechanism to arrive from the
  scanner side rather than from a case.
- **`scan.py` is delivered**, so the reconstructed one is gone and
  `../declared-frame/v2/` imports this one rather than holding a copy.

---

CC0-1.0. Cases where a quantity exists and the instrument's constitution
prevents it from appearing.

Not a gap log. A gap is an oversight. These are exclusions built into the
apparatus before the first reading is taken.

Every entry is a QUESTION until something measures it. Nothing here is a
position under defense. Test fit, extend, or report where it breaks.

## Entry structure

```
QUANTITY       what would be measured
EXCLUDED BY    what in the instrument's constitution prevents it
VISIBLE AS     how the absence currently reads
WOULD MEASURE  the design, if one exists yet
CONFIDENCE     gradient, stated separately from the shape
```

## Exclusion mechanisms

```
MODALITY            apparatus in the wrong channel
STORAGE             medium cannot hold the shape
SCALAR DEMAND       function collapsed to a number
BUDGET BOUNDARY     closed budget compared to open
AUTHORED REFERENCE  reference produced by the measured party
AUDIT ASYMMETRY     guard fires on one side only
SCORED AS WASTE     component read as cost by the instrument's own
                    accounting
```

Sort by mechanism, not by field. That is what lets a case from evolutionary
biology sit next to one from survey methodology and be recognizably the same
failure.

## The register

| mechanism | quantity | visible as | worked in this repo |
| --- | --- | --- | --- |
| MODALITY | capability in a non-human configuration | absence of capability | — |
| STORAGE | calibration between one body and one environment | *"no literature exists"* | `../inverseminar/`, `../anchor-interval/` `ANC_011` |
| SCALAR DEMAND | response as a function over situations | middling score, indistinguishable from flat moderate | — |
| BUDGET BOUNDARY | efficiency under a closed budget | the tree is inefficient at photosynthesis | `../declared-frame/` `DF_005`, `DF_007` |
| AUTHORED REFERENCE | model drift | a number attributed to the model | `../anchor-interval/moving_reference.py` |
| SCORED AS WASTE | practice rate during the stable interval | expenditure with zero return | `../measurement-fork/` K14–K16 |
| AUDIT ASYMMETRY | reliability of an account | neutrality | — |

Full entries with `WOULD MEASURE` and `CONFIDENCE` in
[`uninstrumented.py`](uninstrumented.py); run it.

## Three checks on the register itself

`uninstrumented.py` does not only print the register. It tests it.

### 1 — the mechanism sort is untested, not confirmed

The stated reason for sorting by mechanism rather than by field is that it
groups cases from different fields. At **7 entries, 7 fields, 7 mechanisms**
the two partitions are identical, so nothing yet demonstrates the grouping.

It buys nothing until a second entry lands under an existing mechanism from
a different field. Nearest candidate already in the repo: `MODALITY` holds
animal cognition, and `../reasoning-dial/` `RD_009`'s G-STATE gap — a
self-report from a miscalibrated observer is the quantity in question — is a
different field with arguably the same shape.

### 2 — the mechanisms are not mutually exclusive

**4 of 7** entries have a second mechanism with a claim on them.

```
MODALITY            capability in a non-human configuration
  also SCALAR_DEMAND   the tasks are scored on a human-derived scale,
                       so a different competence integrates to a low
                       number rather than to no number

AUTHORED_REFERENCE  model drift
  also AUDIT_ASYMMETRY the contemporary benchmark is not checked against
                       the fixed one, only the reverse

SCORED_AS_WASTE     practice rate during the stable interval
  also BUDGET_BOUNDARY the return falls outside the sampling window --
                       a boundary placed in time rather than in space

AUDIT_ASYMMETRY     reliability of an account
  also AUTHORED_REF.   the corpus that sets what counts as a normal
                       account was produced by the side that goes
                       unaudited
```

Not a defect to fix by tightening definitions. The filing decides which
comparison case an entry sits next to, which is the register's whole
function — so the filing is a **choice** and should be visible as one.
Minimal repair: carry `excluded_by` as a primary plus a list, sort under
all of them, and accept that an entry appears more than once.

### 3 — a known-null corpus, and nothing files that should not

Every delivered entry states high confidence on the exclusion. A list that
only ever admits entries is `CONSTANT_FIRES` in the `../null-harness/`
sense, and *"not a gap log"* is a rule the structure does not enforce.

Null corpus: the six instruments graded in `../instrument-epistemology/`.
Real apparatus, real transduction chains, three of them graded *mostly
assumed*.

```
broadband seismometer network      0.800   well grounded        no
satellite thermal IR radiometer    0.504   partially grounded   no
airborne LiDAR biomass             0.514   partially grounded   no
camera trap array                  0.293   mostly assumed       no
IRMS + isotopic mixing model       0.275   mostly assumed       no
eDNA metabarcoding assay           0.165   mostly assumed       no

false entries: 0 of 6
```

The line holds exactly where the doc puts it:

```
weak grounding          the quantity is reached, badly
constitutive exclusion  the quantity cannot appear at all,
                        and the apparatus is why
```

eDNA at 0.165 is the hardest case and it stays out — every step of its chain
is named in its own blindness map, which is what a reached-but-badly
quantity looks like. An excluded one has no blindness map, because the
exclusion happens before the map is drawn.

**What this does not establish:** that the register has a reachable fire
branch on a case someone would bring. The null corpus is six cases chosen
because they are well documented, not because they sit near the boundary.
The near-boundary test is a quantity a field believes it measures and does
not, and none of the seven entries is currently contested by anyone.

## Related

- `../instrument-epistemology/` — supplies the null corpus, and its
  blindness-map idea is what section 3's boundary rests on.
- `../null-harness/` — `CONSTANT_FIRES`; section 3 is that invariant applied
  to a classifier whose entries are all positive.
- `../measurement-fork/` — `SCORED_AS_WASTE` is K14–K16 there;
  `BUDGET_BOUNDARY` is K18.
- `../declared-frame/` — `BUDGET_BOUNDARY` is `DF_005` and `DF_007`.
- `../anchor-interval/` — `AUTHORED_REFERENCE` is `moving_reference.py`;
  `STORAGE` is `ANC_011`.
- `../inverseminar/` — the `WOULD MEASURE` for `STORAGE`.

CC0.

---

## Case 010 — the near-boundary case the schema will not take

`cases/case-010.md`, delivered verbatim. Checks in
[`case_010_audit.py`](case_010_audit.py); claims `UNI_013..019`.

Three firsts in one entry: it declines to name its mechanism and says why,
it states a confidence below the ceiling, and it carries a live external
occasion with a DOI. Each of those touches something the register had
already recorded as open.

### UNI_013 — the central move is not constructible

    entry(excluded_by='UNASSIGNED')             -> ValueError
    entry(excluded_by='PROTOCOL_ORTHOGONALITY') -> ValueError
    entry(excluded_by=None)                     -> ValueError

> Argument for leaving it unassigned: assigning the bin before the
> measurement exists closes a variable that has not been read out.

That is this register's own discipline turned on this register's schema,
and the schema has no slot for it. `entry()` validates `excluded_by`
against the closed eight-tuple, so an entry with the mechanism deliberately
open cannot be built — and neither can one filed under the new bin the drop
proposes (`PROTOCOL ORTHOGONALITY`).

Fifth instance of a familiar shape (`MF_017`, `CW_015`, `DL_004`,
`GC_012`, `CA_003`) with one difference that matters: those are missing
**fields**, a stated rule with nowhere to put it. Here the vocabulary is
closed **on purpose** and the closure is the design. Case 010 is the first
delivery to argue the closure is premature for a particular case, and the
schema can only obey that argument or be edited — it cannot record it.

Cheap repair, and deliberately not a ninth mechanism: `UNASSIGNED` as a
legal `excluded_by`, with `candidates=[...]` for the bins under
consideration and a required `why_open`. Filed entries keep the closed
vocabulary; unfiled ones become a state the sort can count instead of an
absence living in a Markdown file beside the register.

### UNI_014 — the first confidence below the ceiling

Eight of eight existing entries open with "high". Case 010: *"not above
~40%. Not sufficient to act on. Stated as a gradient, not a commitment."*

`UNI_004` graded the confidence field `CONSTANT_FIRES` and the check is
still in `check_null()`. It no longer holds — the field carries information
for the first time and a sort by it now means something.

It does **not** close `UNI_006`, which is about admission rather than about
the field. The register has still never turned an entry away, and a
low-confidence entry that is admitted is an admitted entry. The
discriminating test is a case the register **refuses**, and there is not
one.

### UNI_015 / UNI_016 — the occasion, checked

Six stated details, six confirmed: author, journal, volume and issue, DOI,
the Ag-synDNA-on-quasi-2D-perovskite stack, sub-0.1 V operation,
forming-free switching. Nothing embellished, and the citation is exact.

First literature claim in this drop family that was **checkable at all** —
`ANC_010`, `CD_009`, `RD_015` and `HO_005` are all UNVERIFIED because their
markers point outside the delivery. A DOI is checkable.

Two of the four "not located in open sources" items turn out to be
locatable:

    FOUND   cycle count           1000 cycles
    FOUND   retention duration    > 4e3 s, both HRS and LRS
    STILL   temperature range
    STILL   variability distributions

**And the correction cuts in the entry's favour.** Endurance is a cycle
count; retention is a duration. Both are scalars, and both are produced the
way the entry says — cycle with everything else at setpoint, or hold with
everything else at setpoint. SCALAR DEMAND was offered as a hypothesis
about how the suite is built; the two metrics that turned up are instances
of it.

Worth a second look by anyone extending this: `> 4e3 s` is a little over an
hour, where retention is normally quoted at 1e4 s or extrapolated to years.
That is a measurement window rather than a lifetime — again a single-axis
scalar with its own holding-fixed.

### UNI_017 — the field-wide falsifier partially fires

> coupled-perturbation protocols are already standard in the memristor
> qualification literature

Not none. **THB** (temperature-humidity-bias) applies three variables at
once; **TB**, temperature cycling and radiation testing are established;
IEEE **P1817** and JEDEC **JC-42.4** are named standardisation efforts
covering temperature cycling, humidity and EMI. So the sub-question's
"if none across the field" branch does not obtain, and the exclusion is not
field-wide in the strong sense.

**The entry survives narrowed, and the narrowing is precise.** THB and its
relatives hold several variables simultaneously at *constant elevated
setpoints* — 85 °C / 85 % RH is a corner of a factorial, aimed at package
and moisture-ingress reliability. ARM B specifies something else:
co-varying **drift**, non-square waveform, at **matched integrated dose**,
compared on *distribution shape, not total load*. A corner test asks
whether the device survives a harsh place; ARM B asks whether the joint
trajectory matters at equal dose. No protocol answering the second was
located.

The edit that follows: say "co-varying drift at matched integrated dose"
wherever the entry says "co-varying", and cite THB rather than treating
combined stress as absent.

### UNI_018 — the falsifier that could not be checked

The supplement question is UNVERIFIED. The publisher's page and every news
mirror located are blocked by this environment's egress proxy; search
returned metrics, not methods. Recorded as a gap, not a fault — and it is
the cheapest of the three falsifiers for anyone with institutional access,
and the only one that would close the case outright rather than narrow it.

### UNI_019 — the case the register was waiting for, and the comparator

`check_null()` ends by naming what it does not establish:

> the near-boundary test is a quantity a field believes it measures and
> does not, and none of the delivered entries is currently contested by
> anyone.

Case 010 is that case. Device stability is a quantity the field believes it
measures — there are standards bodies for it — and the entry claims a
component of it is unreachable by the suite as constituted. It arrives with
a paper, a DOI, and a confidence low enough to be wrong.

**And it cannot file.** The near-boundary case the register was waiting for
is the one the schema will not take.

The strongest part of the design is the **comparator**: *organic scaffold
replaced by a synthetic periodic scaffold of matched spacing and matched Ag
loading.* That is a known-null in `../null-harness/` terms, and without it
the reported result — hybrid beats DNA-alone and beats perovskite-alone —
cannot be decomposed, because the hybrid differs from each of those in more
than one way at once. Matched spacing and matched Ag loading is what
isolates *organic* from *periodic scaffold with silver in it*.

The three-way discriminator names its own discard branch — *"if the margin
narrows under ARM B, the coupling reading is wrong in sign and should be
discarded"* — so it is not `CONSTANT_SILENT`, and the flat branch is stated
as a real outcome with a name (*"the organic layer is functioning as a
geometric ruler"*) rather than as a failure to find something, which is the
distinction `UNI_005` turns on.

What it does not carry is a **power calculation**. `delta(A, B)` is a
difference of differences across two device populations, and nothing states
how many devices or what margin would be resolvable against
device-to-device variability — which is one of the two items still not
located. That is a `G-RES` pair waiting to be declared: variability spread
against the margin being claimed.

---

## Case 011 — the second case the schema cannot hold, refused differently

`cases/case-011.md`, delivered verbatim. Checks in
[`case_011_audit.py`](case_011_audit.py); claims `UNI_020..026`.

### UNI_020 — two cases, two different refusals by one schema

| case | what it declines | schema field that refuses it |
|------|------------------|------------------------------|
| 010 | to name its mechanism | `excluded_by` is a closed vocabulary |
| 011 | to be one quantity | `quantity`, `excluded_by`, `would_measure` are each scalar |

Case 011 carries five sub-questions; four have their own WOULD MEASURE and
one its own EXCLUDED BY. (Q4's WOULD MEASURE is the word "unclear" — a
filled field, not an empty one: it records that the instrument is not
obvious, which is different from not having looked.)

Stated plainly: **the schema fits the eight entries written to fit it, and
neither of the two real cases delivered to it since.** That is `UNI_002`'s
open question reached from a different direction — a schema tested only
against its own examples is not yet tested.

The `UNI_013` repair does not cover this. An `UNASSIGNED` sentinel gives an
unfiled entry a state; a cluster needs **sub-entries** — a parent with
`questions=[...]`, each carrying its own `excluded_by` (possibly
`UNASSIGNED`) and its own `would_measure`. Q1 and Q3 below both *narrow
without closing*, which is precisely the state a scalar entry cannot
record.

### UNI_021 — a reasoned refusal, stored as an omission

    entry(confidence='')   -> accepted, stored as ''
    entry(confidence=None) -> accepted, stored as None

> Not stated. This is a cluster of open questions, and a scalar over a
> cluster would not carry usable information.

Three states now exist in the wild — `high` (8 of 8 original entries), a
gradient (`~40%`, Case 010), and deliberately absent with the reason given
(Case 011). The schema can tell apart two.

Eleventh instance of the absent-versus-known-negative repair in this drop
family, and it lands in the one field the register singles out as *recorded
verbatim and not adjudicated*. Case 010 made the field non-constant
(`UNI_014`); Case 011 shows it needs three states rather than a wider range
of one.

### UNI_022 — Q5, and the only defence a document has

> Do not fill this in with an approximation. It is left open on purpose.

This is the register's own thesis turned on the register's own vocabulary.
`uninstrumented` exists because forcing a quantity through an apparatus
that cannot represent it is the operation that removes it. Q5 says the same
about forcing an observation into the eight bins before it has a shape, and
refuses.

It is also the cheapest instruction in the drop to violate. Every
downstream reader is under pressure to produce a name, and "political and
ownership structure of the affected area" sits close enough to several
existing mechanisms that a plausible bin is easy to supply. A direct
instruction is the only defence available to a document — and there is no
schema slot behind it, so `note` would file the open axis as a remark and
nothing in any sort would show the cluster has an unnamed member.

### UNI_023 — the occasion

Five of six exact: authors, journal, 12 Aug 2026, DOI, the title verbatim,
16 events, and the stated implication about sequences. Second consecutive
occasion in this register that checks out (`UNI_015` was the first).

One drift, inherited rather than introduced: the entry says *"within
roughly 18 months"* where coverage describes the sequence as spanning late
1341 to 1343, about two years. The entry is quoting the paper's own title
window. It matters because **Q2 nominates 1342–1343 as its corpus**, and a
reconstruction starting at 1342 drops the first inter-event interval —
which is the one that establishes the arrival rate Q2's whole hypothesis
turns on.

### UNI_024 — Q1 narrows: hazard antecedent yes, system antecedent no

Q1 bundles three things in one sentence, and they do not have the same
status:

> A second event arrives into **saturated ground**, **unrepaired works**,
> and **spent response capacity**.

| term | status |
|------|--------|
| saturated ground | **instrumented, and dramatic** — antecedent moisture is standard in flood frequency analysis; saturated soil turns a 7-year rainfall into a 100-year flood, dry soil turns a 200-year rainfall into a 15-year flood |
| compound / sequence hazard | an active quantified field, with published flooded-area figures by return period |
| unrepaired works, spent response capacity | no design-standard variable located |

So the entry's own mechanism — *the second event is not the first one
scaled up* — is already measured on the catchment side, and measured to
matter more than the rainfall return period does.

The sharper statement worth taking from Q1: **the field instruments the
antecedent state of the hazard and not the antecedent state of the
system.** Catchment wetness carries forward between events; the condition
of the works, and of the people who operate them, does not.

Same shape as `UNI_017` one case earlier — the strong reading of the
falsifier fires, the narrow one survives, and the edit is to split the
sentence.

### UNI_025 — Q3 narrows along the boundary of whoever keeps the record

| pathway | status |
|---------|--------|
| residents decide | **attributed** — FEMA HMGP acquisitions are required to be voluntary; the owner agrees to sell and eminent domain is excluded |
| state declines to fund works | **attributed** — state and local governments decide which properties to acquire under federal restriction, and that selection is recorded |
| insurer withdraws coverage | not located |
| lender declines to finance rebuild | not located |

The split is not random: **the two pathways with attribution are the two
inside the institution that keeps the record, and the two without are the
two outside it.** An insurer's withdrawal and a lender's refusal are
decisions by parties the program does not administer, so they cannot appear
in its record whatever anyone intends — and the site still ends up
unoccupied, logged the same way. A boundary result, not an oversight, and
the register's own subject.

The entry's own cross-link is instanced by the same fact. **"Voluntary" is
a truthful attribution of the final step**, and the option set that step
ranges over is generated elsewhere — which properties the administering
authority chose to fund, under federal restriction. That is
`../generation-capacity/MECHANISM_10.md` exactly: the choice is real, the
record is honest, and the generation happened upstream on a clock the
choosing party has no access to.

### UNI_026 — the cross-links

    rate-mismatch-polytope     ABSENT
    generation-capacity        resolves
    rural-conflation case      resolves
    Case 010                   resolves

The rural link is not only present but accurately characterised: `rural` is
tracked by `density` — a headcount per area — with `self_support` among the
welded components, which is exactly *"counts headcount, not what is
holding"*.

`rate-mismatch-polytope` does not exist anywhere in the tree; the two
apparent hits under `../declared-frame/` are the unrelated phrase "separate
mismatch line". Seventh instance of a reference naming an absent artifact
(`CW_001`, `PB_001`, `GC_009`, `PB_015`, `MD_001`, `DL_014`), three of
which landed a drop later.

Worth naming the kin that do exist, because **Q2's hypothesis is already
modelled twice here in a different vocabulary**.
`../rigidification-sensor/simulator.py` runs exactly Q2's comparison —
variance suppressed faster than it regenerates, with `locked_at` recording
the tick where the cost of reversal passes the cost of continuation — and
`../sustained-activation-gate/` holds the restore-versus-coupling
trade-off. Q2's *"same total water across 40 years versus across 4 years"*
is a repair rate against an arrival rate, which is that crossing.

---

## Case 012 — the first entry whose confidence can be checked

`cases/case-012.md`, delivered verbatim. Checks in
[`case_012_audit.py`](case_012_audit.py); claims `UNI_027..033`.

Third consecutive case the schema cannot hold. It is also the first where
the stated confidence is not a string to be recorded but a claim that can
be settled, and settling it is the first section.

### UNI_027 — Q1 is arithmetic, and it holds

The entry rates Q1 "high — arithmetic, not hypothesis". That is checkable,
so it is checked rather than recorded.

Let class *i* deliver `n_i` loads of value `v_i` each at freight cost `f_i`
each. The published aggregate is total freight over total value, and it
rearranges:

    F / V  =  Σ n_i f_i / Σ n_i v_i  =  Σ ( n_i v_i / V ) · ( f_i / v_i )

The aggregate **is** a mean of the per-class ratios, weighted by each
class's share of total **value**. Not a summary of freight burden across
classes — a summary tilted toward whichever class carries the dollars.

| illustrative class | value/load | freight | ratio | $ weight |
|---|---|---|---|---|
| electronics, dry van | 500,000 | 2,000 | 0.40% | 87.11% |
| produce, reefer | 45,000 | 3,200 | 7.11% | 7.84% |
| structural steel, flatbed | 20,000 | 2,500 | 12.50% | 3.48% |
| transformer, oversize | 180,000 | 14,000 | 7.78% | 1.57% |

    aggregate F/V                    =  1.463%
    same, as the weighted mean above =  1.463%   (identity exact)
    worst class's own ratio          = 12.500%
    understatement factor            =    8.5x

The numbers are illustrative and are not data. What they show is the
mechanism, and the mechanism is exact: **Q1 is right in a stronger sense
than it claims for itself.** It does not need any freight figure to be
correct. Any mix in which value-density varies across classes produces the
effect, and it is largest exactly where the entry says the interesting
classes are.

This makes Case 012 the first entry whose confidence field is adjudicable
rather than merely recorded (`UNI_014`, `UNI_021`) — and it adjudicates in
the entry's favour.

### UNI_028 — a fourth confidence state

> Q1: high — arithmetic, not hypothesis.
> Q2, Q3, Q4 as causal chains: not stated. Each needs Q1's data to exist
> before a gradient means anything.

| state | first seen |
|---|---|
| `high`, one string | 8 of 8 original entries |
| one gradient (~40%) | Case 010 |
| deliberately absent, with the reason | Case 011 |
| **split across sub-questions** | Case 012 |

`entry()` takes one string. Three cases, three distinct failures of that
one field: too coarse (`UNI_014`), cannot record a reasoned absence
(`UNI_021`), cannot record a split (here). The `UNI_020` sub-entry repair
reaches a second field, and for the same reason — the questions close at
different times, on different evidence.

### UNI_029 — a negative-provenance record

No precedent in this register, no slot in the schema, and the strongest
methodological move in the drop.

Every prior literature finding in this drop family runs the other
direction. `ANC_010`, `CD_009`, `RD_015` and `HO_005` are citation markers
that pointed outside the delivery, caught afterwards by an auditor and
marked UNVERIFIED. Case 012 marks the numbers **before** anyone builds on
them — names them, names where they circulate, states that no
peer-reviewed origin was located, and says why the note exists: *"recorded
so the next reader does not mistake them for literature."*

An entry carrying its own do-not-use list does the auditor's job at the
point where it is cheap: at authoring time, by the person who knows which
numbers were tempting. Doing it afterwards is what costs.

Checked, not assumed — none of `4.75`, `5.25` or the jet-fuel claim
appears anywhere in the entry's reasoning outside the note itself. The
jet-fuel item is filed the same way: attributed to a source class ("at
least one large 3PL"), marked unverified, listed as a check rather than as
a finding.

### UNI_030 / UNI_031 — one occasion verifies, one figure does not

The pass-through result checks out in full: ~50% immediate, ~100% within a
week, carriers unable to absorb it on thin margins in a competitive
market — including the mechanism the entry attributes it to. Third
consecutive occasion in this register that verifies, after `UNI_015` and
`UNI_023`.

The rate figure does not.

| | |
|---|---|
| entry states | flatbed roughly **$0.70–$1.20/mile** above dry van, 2026 spot data |
| located | **$0.48/mile** (March 2026, stated directly) |
| located | early-2026 averages: dry van $2.47, flatbed $2.95 → **$0.48** independently |
| located | late July 2026: flatbed $3.72, reefer $3.39, no matched dry van figure |

The stated range sits above everything located, and two independent routes
give the same $0.48. No matched-date pair was found for late 2026, when
flatbed alone is quoted much higher, so the range may hold at some date or
on some lanes — but not in the 2026 spot data the entry cites.

**It does not touch Q1.** Q1 is the identity above and holds for any mix
with varying value-density; the premium is one input to the numerator Q1's
WOULD MEASURE asks for, and it appears to be about half the stated size.
A magnitude correction, not a structural one.

### UNI_032 — Q4 splits three ways

**The falsifier partially fires.** BLS publishes which item categories use
hedonic quality adjustment and publishes the share: excluding shelter,
approximately **2.9% of the CPI**. The adjusted set is enumerable and
weighted, which is most of what Q4 asks for.

**The asymmetry is confirmed by that same list.** Personal computers,
televisions, consumer audio, VCRs, camcorders, DVD players, apparel,
microwave ovens, refrigerators, college textbooks, broadband for PPI —
the high-value-density consumer set, exactly as predicted. Neither food
nor electricity appears, so *"a calorie has no new features. A
kilowatt-hour has no new features"* is borne out by which categories the
method is actually applied to.

**The magnitude constrains the mechanism.** Q4's test is that "the
aggregate can be held level by hedonic credit accruing to deniable-quality
goods while substrate goods degrade in real terms". At ~2.9% ex-shelter
that channel has a published upper bound on its leverage, and the bound is
small. The claim is now quantitative, and the number is against it.

**And there is a denominator switch.** Q4 is about **GDP real output**
(BEA, via deflators); the located share is the **CPI** (BLS). Related, not
the same aggregate — so the bound applies to one and leaves the other
unchecked. That is `../measurement-fork/`'s VOID RATIO shape arriving
inside a falsifier rather than inside a result.

Not checked: whether "the quality dimensions come largely from the
producer's own account of what improved". BLS hedonic models use product
characteristics data whose provenance was not established here.

### UNI_033 — Q3's halves have opposite status

**The non-linearity is open, with the sharpest falsifier in the drop.** It
fails "if reefer loads past viability are in practice rerouted or
downgraded at a rate that smooths the discontinuity" — a specific industry
practice that either happens at a measurable rate or does not, and either
answer is informative. A reachable negative, so not `CONSTANT_SILENT`.

The methodological line under it is stronger than the claim and stands
alone: *"Smooth elasticity models do not generate discontinuities — the
functional form is wrong before any parameter is estimated."* That is
`../climate-modeling/`'s cascade-speed result in a third domain, and this
repo already holds it twice (`PhaseChangeAudit`, and
`../sustained-activation-gate/`'s double well).

**The accounting claim is true by construction and needs no search.**
Household food purchases are final consumption expenditure — they enter
GDP on the output side, as C. Labour is a *primary* input rather than a
produced one, so it has no row in the intermediate input-output matrix,
and the calories that sustain it are intermediate consumption of no
industry. The entry's sentence —

> The one input without which no other input can be produced is recorded
> as a consumption category

— is a correct description of the framework, not a contested reading of
it.

That inverts this register's usual pattern. The half carrying "WOULD
MEASURE: unclear, flagged as needing an instrument" is the **established**
half; the half with a clean falsifier is the one still open. The
instrument is missing not because the fact is uncertain but because the
framework has no slot for the quantity — which is this register's own
subject, and makes Q3 the entry's best candidate for a filed mechanism if
one had to be chosen today.

---

## Case 013 — the case that does not know if it is one case

`cases/case-013.md`, delivered verbatim. Checks in
[`case_013_audit.py`](case_013_audit.py); claims `UNI_034..041`.

The simulations in §5 are stdlib, seeded, and reproduce by running the
script — the first time in this register that a delivered entry's
load-bearing technical claim could be settled by running something rather
than by searching.

### UNI_034 — a fourth refusal, about the record rather than a field

| case | declines | schema field |
|---|---|---|
| 010 | to name its mechanism | `excluded_by`, closed vocabulary |
| 011 | to be one quantity | `quantity`, scalar |
| 012 | to carry one confidence | `confidence`, one string |
| **013** | **to be one entry, or two** | **the entry itself** |

`entry()` returns one dict, and the `UNI_020` sub-entry repair does not
reach this — sub-entries let a cluster hold several questions under one
parent, which presumes the parent is one thing.

The drop anticipates the pressure a filename applies and says so directly:
the one-or-two question "should not be resolved to get a cleaner
filename". Honored — landed as `case-013.md`, the register's own
numbering, which takes no position. A name drawn from either half would
have.

### UNI_035 — provenance inside an entry

`[stated by Kavik]`, attached to Q4. First provenance tag inside a
register entry, and it is at sub-question granularity rather than entry
granularity — which is the right level here, because Q4 is the half the
SPLIT IS OPEN section says may leave as its own case, and it would leave
with the attribution attached.

`../held-open-uncertainty/OPEN_QUESTIONS.md` does this per entry
(`HO_001`). `entry()` has nine fields; none carries who said it, and 0 of
8 existing entries carry an attribution.

### UNI_036 / UNI_037 — the anchor, and what it does not say

Located, all dated:

    5-digit SATCAT exhausted 2026-07-11 with the addition of Saramago
    official USSF SATCAT now at 100365; new objects get 100000+
    Alpha-5: alphanumeric first character, called a STOPGAP by its
      publisher, capacity 339,999, letters I and O omitted to avoid
      confusion with the digits 1 and 0
    9-digit catalogue numbers in GP/OMM formats, introduced 2020
    legacy fixed-width TLE/3LE still in use alongside both

Three coexisting representations is the "parallel schemes, reconciliation
routines between them" the entry names — running now, documented. And the
overflow is **six weeks old**, so Q1's "per year since the overflow"
denominator starts essentially now rather than being reconstructed. That
is a better measurement position than the entry claims for itself.

Two details the entry does not extract. Alpha-5 gives up capacity (I and
O) to prevent a legibility failure it introduced. And it is a stopgap with
a stated ceiling — so **the compensation layer is itself a fixed-width
scheme with a design-time population assumption**, which is Q2's asymmetry
recurring one level up rather than resolving.

**The correction.** The entry says high number blocks are opened "and
objects recategorised", and treats that as the event that moves the key.
What was located is narrower: new objects get 100000+, and Alpha-5 changes
the **encoding** of numbers ≥100000 so they fit five characters. Neither
renumbers an existing object. If existing numbers do not move, the
analysed key does not move for the existing population — Q3's own
falsifier, met from a direction the entry does not consider.

Reassignments *do* occur, for a different reason: corrections when
tracking data reveals merged or split objects from refined sensor
observations. That is a physical-resolution event, not an overflow event.
**Two distinct sources of key movement, and the entry attributes to
overflow what is documented for resolution.** Q1's measurement would have
to separate them, because only one is caused by the design-time omission
the case is about.

The falsifier's other half also partly fires: the COSPAR International
Designator (launch year, launch number, piece letter) is published
alongside the NORAD number and does not overflow on a fixed field width,
so a population analysed by COSPAR ID is stable against the overflow
source. It is not stable against the resolution source — a split adds a
piece letter.

### UNI_038 — Q3's transfer, simulated

Citation checks out: Adam Pintar and Samuel Stavis, NIST, August 2026, the
"dimming effect" in nanoparticle sizing with a correction that reverses
it. The entry's one-line characterisation is accurate.

The transfer is checkable by simulation, so it was simulated. Three
regimes, because a catalog number is used in more than one way and those
are not the same statistics.

| regime | mechanism | measured attenuation |
|---|---|---|
| 1 — continuous X, random additive error (the NIST case) | classical errors-in-variables | ratio = reliability ratio, matched to 3 dp (0.998 / 0.797 / 0.500 / 0.198) |
| 2 — grouping key, records mis-attached (the join case) | non-differential misclassification | exactly `1−2p` (1.02 / 0.78 / 0.52 / 0.18) |
| 3 — subset moved to a distant block (the overflow case) | variance inflation | 0.099 / 0.010 / 0.021 — down to **1%** of the true slope |

**All three flatten toward zero.** Q3's direction claim survives in every
regime tested — including regime 3, which was built expecting it to fail.
An order-preserving remap looked like it could bias either way; it does
not, because moving a subset into a distant block inflates `var(X)` far
more than it adds covariance. Recorded because the expectation was wrong
and the simulation is what settled it.

What does not transfer is the **mechanism**. Three distinct derivations
with one shared direction. "Structurally the same as the NIST dimming
effect" is true of the direction and of nothing else — and the catalog
cases are *worse* than the nanoparticle case (1% versus 50%), which
strengthens Q3 rather than weakening it.

One caution the entry omits: regime 3 assumes the key is used as a numeric
covariate, and regressing an outcome on a catalog number is rarely
meaningful. **The strongest form of Q3 is regime 2** — mis-joins across
reconciled schemes — because that is the operation the compensation layer
performs constantly.

### UNI_039 — the Case 010 cross-link corrects UNI_019

Case 013 says Case 010 "reads it as a geometric constraint on silver
placement; that reading may be incomplete", because the sequence is the
address.

**It lands, and it corrects a finding recorded in this file.** `UNI_019`
called Case 010's comparator the load-bearing element and a known-null in
`../null-harness/` terms, because matched spacing and matched Ag loading
isolate *organic* from *periodic scaffold with silver in it*. That holds
on the organic-versus-inorganic axis and was too generous on a second axis
the comparator does not control.

A periodic scaffold has one spacing repeated and its positions are
interchangeable. A sequence-addressed scaffold has positions
distinguishable from one another — that is what "the structure is the
address" means. If the DNA layer's contribution depends on
distinguishability rather than on pitch, matched pitch is not a matched
control: the comparator differs from the hybrid in the dimension under
test.

The consequence is a specific **false negative**. Case 010's flat branch
reads *"the organic layer is functioning as a geometric ruler and any
periodic scaffold of matched pitch substitutes"*. Under the addressing
reading, a flat margin is also what you get when addressing is everything
and the comparator cannot express it — so the branch meant to say
"geometry was enough" fires in both cases.

Repair is one arm: a comparator with matched pitch **and** aperiodic,
position-distinguishable structure — same spacing statistics, same Ag
loading, sequence scrambled. That separates pitch from addressing, which
the delivered two-arm design cannot.

The entry's "do not collapse them" is right for the reason it gives:
evidence propagates both ways. This finding is an instance — a claim in
Case 013 changed the reading of a claim about Case 010.

### UNI_040 — Q4's comparison class, narrowed

Its falsifier — "fails if object-carried identification schemes turn out
to have their own bounded capacity under a different name" — does not
fail, and the class does not survive as stated either.

A DNA sequence of length L over four letters addresses 4^L states, which
is bounded, so "no block to overflow" is not literally true. The statable
version is that **capacity scales with the object rather than being fixed
by a register**: one more base multiplies capacity by four at the cost of
one base, where widening a fixed counter rewrites every consumer of the
field — which is exactly the compensation load Q1 is about.

The middle term was already in the anchor's own records and goes
unmentioned. The COSPAR designator is **compositional** — launch year,
launch number within the year, piece letter — so its year field is
open-ended and capacity grows with time rather than being drawn from a
fixed pool. It sits between the sequential counter and the
sequence-as-address family, in the same records as the counter. That is
the cheapest next step for Q4: the comparison class does not have to be
reached for across substrates, because a partial instance is published
alongside the anchor.

### UNI_041 — cross-links and a fifth confidence state

    Case 010        resolves
    Case 011        resolves
    Case 012        resolves
    Mechanism 11    resolves

First drop in this sequence with **no dangling reference**;
`rate-mismatch-polytope` (`UNI_026`, `DD_008`) is not cited here.

Confidence is a fifth state of one string field: an absence with a stated
**unlock condition** — "Q3 alone could take a gradient once Q1's data
exists" — which is a dependency between sub-questions rather than a value.

| state | first seen |
|---|---|
| `high` | the eight originals |
| a gradient | Case 010 |
| a reasoned absence | Case 011 |
| a split across sub-questions | Case 012 |
| an absence with an unlock condition | Case 013 |

`entry()` stores a string and cannot tell any of the five from an omission
(`UNI_021`).

---

## Case 014 — the entry whose EXCLUDED BY says nothing excludes it

`cases/case-014.md`, delivered verbatim. Checks in
[`case_014_audit.py`](case_014_audit.py); claims `UNI_042..049`.

### UNI_042 — the founding binary is two-valued and three states have arrived

The README's opening rule:

> Not a gap log. A gap is an oversight. These are exclusions built into
> the apparatus before the first reading is taken.

Q1's EXCLUDED BY, in full: *"nothing prevents it. It has not been
assembled."*

By that rule it is a gap. But the entry does not leave it there, and the
next paragraph is the one that matters — the checking apparatus exists in
a neighbouring field and is closed on its own inputs; *"the target moved;
the instrument did not follow."*

| state | the README has a name for it |
|---|---|
| an oversight | gap |
| built into the apparatus before the first reading | exclusion |
| **the apparatus exists, works, and points elsewhere** | **no** |

Case 013's Q4 named the same state one drop earlier — *"there, a record is
destroyed. Here the record is intact and unread"* — and Case 014's own
cross-links point at it. Delivered twice now, against a two-valued
distinction.

Whether it belongs in this register is a real question and it is the
register's own: admitting it widens the subject from *what an instrument
cannot see* to *what an existing instrument is not pointed at*. Those are
different objects with different remedies — the first needs a new
instrument, the second needs someone to turn one.

### UNI_043 — a second absent artifact, and a pattern

    wiki-style references in this entry : tool-off-metrology, cited 2x
    ../tool-off-metrology exists        : False
    also reached for in case-011.md Q4  : True

Two distinct named-but-absent artifacts now, each load-bearing across two
drops:

    rate-mismatch-polytope   Case 011 Q2, Mechanism 11 sub-q 4   UNI_026, DD_008
    tool-off-metrology       Case 011 Q4, Case 014 Q4 + links    UNI_043

Worth naming separately from either instance. A forward reference cited
once is a note to self; two references, each cited by two drops for two
different arguments, is a set of folders this drop family keeps needing
and has not written. And both are the same object from different ends: **a
rate or a baseline that the measurement destroys.**

The `[[...]]` syntax is new — prior cases name cross-links in prose, and
nothing in the repo resolves that form, so it reads as a link and behaves
as text.

### UNI_044 / UNI_046 — what the citations do and do not carry

The occasion verifies four for four: Fellers & Storm, *JEPLMC*, reminder
users impaired when reminders are removed, attributed to desirable
difficulties — and the load-bearing detail, *"falling below the baseline
levels of performance observed for participants who never used
reminders."* The entry's "below the no-reminder baseline, not merely level
with it" is exact, and that is the difference between a tool that does not
help you learn and one that leaves you worse than not having used it.

Fifth consecutive verifying occasion in this register.

The critique literature verifies too. Pobiner (2016) is exactly
*"Accepting, understanding, teaching, and learning (human) evolution:
Obstacles and opportunities"*, AJPA; the acquired-traits-are-heritable
misconception is documented there, which is what the entry uses it for.
Kelemen's "promiscuous teleology" is a conceptual default all peoples
share, tamped down by enculturation.

**One attribution runs broader than what was located.** "Not the product
of parental explanation, religiosity, or storybook convention" is a
three-item rule-out; the located framing is universality plus
enculturation. Compatible, not identical — and the distinction is
load-bearing for the use the entry makes of it, since "a default reading
mode, which is why it survives in people who would disavow it" needs the
rule-out. A universally *taught* thing is also universal.

### UNI_045 — Q1's corpus already exists

Q1: *"EXCLUDED BY: nothing prevents it. It has not been assembled."*

The second sentence is the expensive one and it is less true than it
looks. A meta-analysis of cognitive offloading exists — *"Meta-analytic
investigations of the effect of cognitive offloading on memory-based task
performance and interindividual variability"* — and a meta-analysis ships
an enumerated included-studies list with stated inclusion criteria.

**That list is the denominator Q1 needs**, built for a different question
by people with no stake in this one, which is better provenance for a
denominator than building it to fit the audit. Q1's cost drops from
"define a corpus and defend the definition" to "run three-way scoring over
a published list."

The caveat travels with it: a meta-analysis on memory-based *performance*
selects for studies reporting a performance effect, which is not the same
population as "instances where offloading is described in evolutionary
terms". A starting corpus with a statable bias, not the frame Q1 would
ideally draw.

Same shape as `DD_005` on Mechanism 11's R2, and concrete rather than
structural.

### UNI_047 — Q2 has two claims and one falsifier

| | |
|---|---|
| claim A | the reference population is smuggled — unstated rather than misstated |
| claim B | this error has **no name** in the sources, unlike the pinnacle error |
| falsifier | "fails if reference populations are stated in the sources and the generalization is explicit rather than smuggled" |

The falsifier tests A. B — the one the entry leans on ("only one is
documented", "the one with no name in the sources found") — has none.

On the corpus reached: the evolution-education literature studies
populations of **learners** (religiosity, education, age, political
affiliation as predictors of acceptance), not the implicit reference
population of the narrative being taught. So B is consistent with what was
located.

Named as the cheapest next check and **not searched here**: the
history-of-science and decolonial-paleoanthropology literature, where a
critique of Eurocentric framing in human-origins narratives plausibly
exists under a different name. B is a negative about a literature, and a
negative about a literature is only as good as the search behind it —
`UNI_006`'s rule applied to a claim instead of to a register.

### UNI_048 — the attribution tag at scale

| q | attributed | instrument |
|---|---|---|
| Q1 — is a transmission channel ever specified | — | stated, independent, runnable |
| Q2 — the reference population | yes | stated, depends on Q1 |
| Q3 — are the channels separable | yes | "unclear" |
| Q4 — coupling value as a function of difference | yes | "no instrument proposed" |

Three tags, up from one in Case 013 (`UNI_035`). The distribution is the
finding: **the single untagged question is the one with an independent
runnable instrument and a stated high confidence**, and instrumentability
falls off across the tagged ones.

Not a criticism of the tagged questions — a description of what the tag
does. It marks the parts of the entry that are somebody's position rather
than a procedure, inside a document whose reading protocol says it holds
markers and not positions. The tag is how those two coexist, and it is
doing real work. `entry()` still has no field for it.

### UNI_049 — third instance of the withheld slot, and Q3's sentence

    ../uninstrumented/cases/case-011.md         Q5
    ../derivation-discarded/MECHANISM_11.md     sub-question 4
    cases/case-014.md                           Q3

`DD_007` recorded this as "a recurring device" at two instances. At three
it is a construct with a stable form, and still no schema slot anywhere in
the family.

Q3 adds what the prior two did not:

> the non-separability may be the finding rather than the obstacle. If the
> channels are not separable in the system, any study isolating one is
> measuring an artifact of its own isolation, and the isolation is a
> property of the instrument.

That is `uninstrumented`'s own thesis stated in general form, by an entry,
about a domain — and stated as a **conditional with the condition named**,
not as an assertion. It also supplies its own falsifier's shape from the
other side: a design that separates the channels "without assuming their
independence" is exactly a design whose isolation is not a property of the
instrument.

The NOT CLAIMED HERE section belongs beside it. *"No intent. The drift
direction is arguable from evidence; a party steering it is not, and the
case does not require one."* That pre-empts the reading that would convert
Q4 into a claim about somebody's plan, by naming what the argument does
**not** need — the same discipline `../rigidification-sensor/` states
about itself ("names no actor, motive, or plan by construction"), arriving
in a one-page case.

---

## Case 015 — the label that outranked a century of observation

`cases/case-015.md`, delivered verbatim. Checks in
[`case_015_audit.py`](case_015_audit.py); claims `UNI_050..057`.

### UNI_051 — Q1's mechanism is refuted, and its conclusion strengthened

Q1 opens: *"Aerobe / anaerobe is a two-state classification."*

It is five-state, and has been as long as the textbook categories have
existed:

| # | category | |
|---|---|---|
| 1 | obligate aerobe | requires O₂, survives atmospheric |
| 2 | facultative anaerobe | uses O₂ if present, otherwise not |
| 3 | microaerophile | requires O₂ at ~1–10%, harmed at 21% |
| 4 | **aerotolerant anaerobe** | **survives O₂, does not use it for growth** |
| 5 | obligate anaerobe | does not survive normal atmospheric O₂ |

Category 4 is named for exactly the phenomenon the 2026 paper reports.

**And that makes the entry's conclusion stronger.** If the vocabulary had
been binary, the label holding would be partly a tooling failure — nowhere
to file the result. With five categories and one named for the finding,
the label held **despite** an available slot. Worse failure, better
evidence for the mechanism the case proposes.

A second published figure cuts the same way: the obligate-anaerobe
category's own documented range reaches **8% oxygen** — *"some obligate
anaerobes can survive in up to 8% oxygen, while others cannot survive
unless the oxygen concentration is less than 0.5%."* The measured growth
limit, between 5% and 8%, sits **inside** the range already published for
the category it was assigned to. Only the 21% aerotolerance exceeds it.

So the finding is not "an organism was outside its category by two orders
of magnitude". It is closer to: *an organism sat at the documented top of
its own category, and in a neighbouring category on a second axis, and
neither was checked for a century.*

### UNI_052 — the falsifier partly fires, and the refinement beats the claim

The standard assay is a **thioglycollate broth tube**, and the categories
"can be distinguished experimentally using thioglycollate broth tubes,
where position in the tube reflects the organism's oxygen preference."

A thioglycollate tube *is* an oxygen gradient. So "standard anaerobic
culture reproduces the binary, not the gradient" is not right about the
protocol.

What the assay does not do is **quantify**. It returns a position, which
maps to a category *name*. It never returns a concentration. The sharper
exclusion, and a better statement of the entry's own case:

> the numeric threshold attached to the label was never measured by the
> assay that assigns the label

A number like 0.05% cannot come out of reading a band's depth in a tube.
It has to come from somewhere else, attach to the category name, and then
travel with every organism the assay assigns that name — an assay which
could not have produced it. **The sensor platform matters because it
quantifies, not because it is a gradient**; the gradient was already
there.

### UNI_053 / UNI_054 — the title, and what it settles

The VISIBLE AS claim verifies verbatim: **"Oxygen induces mutation in a
strict anaerobe, *Prevotella melaninogenica*"** (2008) — eighteen years
before the 2026 paper. The study measured decreased survival, increased
oxidative DNA damage and raised mutation frequency under oxygen exposure.

An oxygen-response measurement on the organism, published, with the label
retained in the title of the paper doing the measuring. The proposed
mechanism instanced in five words.

Q3 asks whether the binding constraint was the instrument or the category
and leaves it open. The 2008 paper lands on the **category** branch —
oxygen experiments ran 18 years before the sensor and the classification
survived them. It does **not** settle the instrument branch: its readout
was mutation frequency and survival, not growth across intermediate
concentrations, and a study of that design cannot produce a growth-limit
number however carefully run.

**The branches are not exclusive, and the 2008 paper shows both
operating.** Q3's either/or is what needs editing; the question underneath
— how many other cases sit in this state — is unaffected, and the joint
reading makes it worse, since it needs both a missing quantifier and a
holding label rather than either alone.

### UNI_055 — the headline number was not located

    threshold 0.05%  ->  5% is 100x   8% is 160x   (2.0 orders at 5%)
    threshold 0.50%  ->  5% is  10x   8% is  16x   (1.0 orders at 5%)

At 0.05% the arithmetic is exact: two orders of magnitude on the nose.

The 0.05% figure itself was **not located**. What was located is the
category description giving **0.5%** as the low end — an order of
magnitude above, which would halve the exponent and turn "a wrong number
that stood for approximately 100 years" into a smaller wrong number.

The entry may well be quoting a Prevotella-specific threshold from the
source paper, which is a different quantity from the category's general
low end. Recorded as NOT LOCATED rather than as wrong — but it is the one
number the headline claim depends on, and the neighbouring published
figure differs from it by exactly the amount that matters. Cheapest check
for anyone with the paper: the threshold the source attributes to the
historical classification.

### UNI_056 — a fourth state, and the first that names an operation

| state | named where |
|---|---|
| an oversight | README: *gap* |
| built into the apparatus before the first reading | README: *exclusion* |
| apparatus exists, works, points elsewhere | Case 013 Q4, Case 014 Q1 (`UNI_042`) |
| **observation made, recorded, re-explained by the label** | **Case 015** |

`UNI_042` recorded three states against a two-valued founding
distinction. This is a fourth, and it differs in kind from the third: not
*nobody looked*, but **somebody looked, published it in the same field,
and the category converted it into a methods problem**.

> Once an organism is inside the category, an observation of it in oxygen
> does not read as evidence against the category — it reads as
> contamination, a handling error, or a bad sample.

Strongest candidate for an actual new mechanism to come through this drop
family, and the reason is structural. The other candidates name an
**absence** — capacity removed, derivation discarded, a quantity with no
register. This one names an **operation** that runs on data that did
arrive. Subject, verb, object, and the object is evidence that exists.

It also has the best-instanced anchor of the four (`UNI_053`).

### UNI_050 / UNI_057 — the occasion, and the links

Everything in OCCASION checks: five authors, DOI, bioRxiv ID, Michigan,
the source's own "100-year-old classification", the bracketed 5–8% limit
(correct as an inference — growth at 2% and 5%, 8% the next level tested),
robust aerotolerance at 21%.

One drift, small and pointed: the preprint says *"Lung **Commensal**"*,
the Journal of Bacteriology version says *"lung **symbiont**"*. The entry
cites the JB DOI and uses the preprint's word — a categorical relabeling
inside the paper whose subject is a categorical relabeling that took a
century. Nothing turns on it, except that the entry's QUANTITY line says
"oxygen tolerance of a commensal organism" and the published version no
longer uses that word.

Also located and stronger than the entry claims: P. melaninogenica is
reported at **more than 10%** of microbial populations in both healthy and
diseased lungs, which sharpens the contradiction the paper names.

Four of four cross-links resolve — second drop with no dangling reference,
after Case 013 (`UNI_041`). The `presented-binary` link is accurate to
that folder, with the twist `UNI_051` supplies: the option space was not
in fact constrained to two, so the alternatives were present, documented,
and not reached for.

Confidence is split across the cluster again — "Q2 is high as an audit.
Q1's magnitude unknown until the denominator is pulled" — which is Case
012's state (`UNI_028`) on its second appearance. Five states of the one
string field are in the wild; `entry()` stores a string (`UNI_021`).
