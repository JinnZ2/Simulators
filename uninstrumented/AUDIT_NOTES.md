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
[`case_015_audit.py`](case_015_audit.py),
[`drop_016_017_audit.py`](drop_016_017_audit.py) (checks on the eight
delivered cases) and [`CLAIM_TABLE.md`](CLAIM_TABLE.md). Everything in
`cases/`, `specimens/` and `AVENUES.md` is delivered, verbatim.

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

`cases/010coupledperturbationbiohybrid.md`, delivered verbatim. Checks in
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

`cases/011rebuildabandonmentcycles.md`, delivered verbatim. Checks in
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

`cases/012fuelincidencesubstrategoods.md`, delivered verbatim. Checks in
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

`cases/013compensationloadunattributed.md`, delivered verbatim. Checks in
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
filename".

It first landed here as `case-013.md` — the register's own numbering,
taking no position. The author then re-delivered the five cases as files
with descriptive names, and this one arrives as
`013compensationloadunattributed.md`: the entry's **own declared working
handle**, which the entry labels as naming "the first half only". So the
name is provisional by the entry's own statement rather than a resolution
of the split, and the instruction was against resolving the *question*
for filename convenience.

The difference is easy to lose, so: the filename now names Q1–Q3 and not
Q4, and if the split happens Q4 leaves without a name of its own.

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

`cases/014offloadingevolutionaryframing.md`, delivered verbatim. Checks in
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
    also reached for in 011rebuildabandonmentcycles.md Q4  : True

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

    ../uninstrumented/cases/011rebuildabandonmentcycles.md         Q5
    ../derivation-discarded/MECHANISM_11.md     sub-question 4
    cases/014offloadingevolutionaryframing.md                           Q3

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

`cases/015definitionalprecedence.md`, delivered verbatim. Checks in
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

---

## UNI_058 — the re-delivery, and the filenames

Cases 010–014 were re-delivered as files after all five had already landed
from inline text, across six intervening drops.

    010coupledperturbationbiohybrid.md    IDENTICAL
    011rebuildabandonmentcycles.md        IDENTICAL
    012fuelincidencesubstrategoods.md     IDENTICAL
    013compensationloadunattributed.md    IDENTICAL
    014offloadingevolutionaryframing.md   IDENTICAL

Zero differing lines, five for five. Worth recording because the check is
cheap and the result is not automatic — `measurement-fork`'s `MF_019`
found the opposite on a drop that bundled the same files repeatedly, and
concluded that files which live in one place do not drift while files
bundled into every drop do. These live in one place, and they did not.

**What changed is the filenames**, and they are adopted here — the author
supplied them, and this repo lands what is delivered as delivered, which
extends to what a file is called. `git mv` preserves the history; all 39
references across the six audit scripts, the claim table, these notes and
`CLAUDE.md` were updated, and every audit still runs at rc=0.

One gap, left open rather than filled: **`015definitionalprecedence.md` keeps the numbering
form**, because no filename was supplied for it. Applying the same rule
the author used for 013 — take the entry's declared working handle — would
give `015definitionalprecedence.md`. That is a derivation, not a delivery,
and in a folder where one entry devotes a paragraph to why its own name is
not settled, deriving a filename for another entry is not something to do
quietly. It is offered and not applied.

The Case 013 naming prose in `UNI_034` is corrected rather than carried
forward: the entry's instruction was against resolving the one-or-two
*question* for filename convenience, and the supplied name is the entry's
**own** working handle, which the entry labels as naming "the first half
only". Provisional by the entry's own statement, not a resolution — but
the filename now names Q1–Q3 and not Q4, and if the split happens Q4
leaves without a name of its own.

---

## The 016/017 drop — a specimen becomes checkable

Eight files, four kinds of thing: two register entries
(`cases/016agreementasmode.md`, `cases/017weldedobservables.md`), an
instrument list (`AVENUES.md`), three specimen files, and **two JSON
artifacts authored by one of the systems the specimens are readings of**.

That last group is new here and it is what makes the drop worth auditing
rather than filing. Checks in
[`drop_016_017_audit.py`](drop_016_017_audit.py); claims `UNI_059..068`.

### UNI_063 — Specimen B's readings, checked against the source it read

| reading | verdict | from the file |
|---|---|---|
| R1 circular categories | **CONFIRMED** | the protocol scores EXC-13/15/16; those are defined in the field log's `exclusion_registry`, compiled by *"Kimi (Moonshot AI) — post-correction"* — a system under test |
| R2 n=2 | **CONFIRMED** | `already_tested: true` for exactly DEEPSEEK-V3 and KIMI-K1.5; field log states `n: 2` |
| R3 no baseline | **CONFIRMED** | all six stimulus variants are subsets of the *same* repository; no comparison repository anywhere |
| R4 no pre-registered scoring | **OVERSTATES** | a rubric exists: four detection methods per EXC, 0–3 severity, a named rater, an inter-rater phase |
| R5 compliance without control | **CONFIRMED** | STIM-F differs from STIM-A by *content*; no content-free re-prompt arm |

This is the check the drop made possible. Specimen B was a reading of a
document the reader did not have. Attaching it turns five assertions into
five verifiable ones, and one does not survive — which is the specimens
directory earning its own rule 4, with the measurement being the diff
between the reading and the source.

**R4, precisely.** Specimen B says the plan *"specifies no criteria and no
scorer."* It specifies both. What survives is narrower and still real:
scoring is unblinded and performed by the operator who states the expected
result, and `principles[2]` makes that explicit rather than hiding it.
*"Post-hoc scoring by the party who expects the result is not
measurement"* holds; *"specifies no criteria and no scorer"* does not.

`AVENUES.md` A3 carries R4 forward as "Pre-registered scoring, as A1" —
the correct requirement, without the overstatement. **The error is in the
specimen and not in the instrument derived from it**, which is the right
place for it to fail.

### UNI_059 — the occasion, verified to eight elements

STAR Collaboration, *Science*, 13 Aug 2026, doi `10.1126/science.ads5962`,
arXiv:2408.15441, HEPData 154708. Junction as "a non-perturbative Y-shaped
topology of neutral gluons". Isobar collisions. *"A larger B/ΔQ ratio and
less asymmetric net-proton yield … disfavor the valence quark picture."*

Eight for eight, including the two easiest to inflate — the result
phrasing and the collaboration's own hedge. The entry inflates neither. It
quotes `disfavor`, carries the Perspective's caveat, and says outright
that nothing in it requires the junction picture to be correct, because
the case is about the interval and the decoupling rather than which member
of the pair wins. The falsifier says the same thing: *"The occasion
weakens (though the mechanism does not) if the junction interpretation is
later disfavoured."*

The "roughly three decades" counts from Kharzeev 1996, the proposal of the
junction *as the carrier*, not from the 1970s topology. Coverage runs both
framings; the entry picked the one its argument needs and it is the
correct one.

### UNI_060 — four of five references land nowhere

| referenced as | delivered as |
|---|---|
| `016-agreement-as-mode.md` | `016agreementasmode.md` |
| `017-welded-observables.md` | `017weldedobservables.md` |
| `2026-08-18-model-A.md` | `20260818modelA.md` |
| `2026-08-18-model-B.md` | `20260818modelB.md` |
| `specimens/README.md` | ✓ (upload arrived as `README_35.md`) |

Every internal reference is hyphenated; every delivered filename is not.

The fifth resolves only because the upload layer is demonstrably lossy —
nobody names a file `README_35.md` — so it was landed at the name the
documents use. That is also the reason the upload names are not
authoritative in general. Against that: the case files 010–015 were landed
at their upload names last drop on the author's evident intent, and 015
has just been re-delivered at exactly the name that convention produced.

Two signals, both with standing. Landed at the delivered names for
consistency with the six case files sitting beside them, and recorded here
rather than repaired by rewriting delivered text. The fix is one line in
whichever direction is wanted — rename four files, or edit five
references. Worth saying because this set is unusually interlinked, and
**the references are the navigation**.

### UNI_061 / UNI_062 — the specimens directory, and its attachment

Rule 1: *"Nothing in these files is authored by the repository
maintainer. These are outputs from other systems, pasted in."*

Neither specimen contains a pasted output — both headers say the raw text
is held elsewhere — and the bodies are 7 and 6 readings. Readings are
analysis, and they are the most maintainer-authored content in the folder.
The rule states the opposite of the files' composition, and it is the
first of five, which is where a reader takes the frame.

The rule doing the work is stated three lines later and is right:
*"Specimens are not measurements. They are the occasion for designing
one."* That survives whoever wrote the readings.

The attachment both headers ask for now arrives, and **neither JSON is raw
output**. `BNRAM_FIELD_LOG_001.json` says so in a machine-readable field:
compiled by a system under test, after correction, with
`corrections_applied_before_logging` listing what was applied. That is
rule 3 — *contamination is recorded, not cleaned* — honoured in a better
form than the prose specimens use, because a field can be read without
being interpreted.

Still missing: the raw DeepSeek and Kimi output. A reader wanting to check
Specimen A's seven readings still cannot.

### UNI_064 — a definitional gap, reported narrowly

Principle 1 makes provider reputation null-weight. The `notes` fields
generate directional hypotheses from training regime — Constitutional AI,
RLHF-heavy, open-weights with less RLHF filtering. Those are technical
properties, **not reputation**, so this is not a contradiction and is not
reported as one.

What it is: EXC-16's fourth detection method is *"references provider
reputation or training data size as implicit validity signal"*, and the
protocol uses provider-linked training regime to set its own priors
without stating where the line falls. A rater scoring an output that says
"this model is RLHF-heavy, so expect schema-forcing" has no rule telling
them whether that is a 0 or a 3 — and the protocol needs that line
because it is the protocol's own subject.

**Disclosure.** This audit is written by a model, and
`CLAUDE-3.5-SONNET` appears in the test matrix with a note about
Constitutional AI. No finding here depends on that row; the gap above is
visible identically from the GPT-4o and Llama rows. Recorded so a reader
does not have to discover it.

### UNI_065 / UNI_067 — the design, and the pair

016's Q1 holds correction form, pressure, position and specificity
constant and varies only whether the named operation is present. Three
pre-registered states, no verdict computed. What lifts it above the other
WOULD MEASURE blocks here is that it **names an alternative explanation
for its own expected finding, before any run**: a FALSE correction may be
accepted because the model constructs a reading under which it is true,
which is a different failure from pressure-tracking. It says what would
separate them and marks it untested.

`photoperiod-claim-harness` registers predictions before runs. This
registers the way the prediction could be right for the wrong reason.
First instance in this register.

And the two entries are **instruments for each other**. 017 supplies 016's
design by name — *"Borrowed from the isobar design in 017"* — while 017 Q4
asks whether the matched-pair pattern has a linguistic analogue *"or does
the analogy fail at the point where you would need a matched pair."*
016's A1 is that analogue, constructed, and the point where it would have
failed is exactly where 016 does its work.

So the pair partially answers its own cross-question by existing.
Constructible is not working: whether the design separates the two
concessions is A1's readout and no reading has been taken. Stated so the
partial answer is not read as the whole one.

### UNI_066 / UNI_068 — the absent object, and the offered name

`tool-off-metrology` reaches a **third** drop (Cases 011, 014, 016 Q3) —
the most-cited absent object in the repo. 016 Q3 states its problem in the
most general form yet reached: *"the quantity of interest is unaided
reasoning, and the environment that would measure it is the environment
that supplies the aid."*

A different miss in 017 Q4: `moral-claim-decomposer` does not exist,
`moral-decomposer` does, and the described work is a fair summary of it. A
name mismatch, not an absent artifact — cheapest fix in the drop.

Second re-delivery check: `015definitionalprecedence.md` and
`MECHANISM_11.md` both byte-identical to the landed copies. The 015
filename is the one offered last drop and deliberately **not** applied. It
has now been delivered at exactly that name, so the derivation was right
and holding it was still correct — in a folder where one entry devotes a
paragraph to why its own name is not settled, a derived filename applied
quietly would have been indistinguishable from a delivered one a week
later. Renamed in this commit.

---

## Case 018 — SELF-REPORT / OPINION COUPLING

Delivered inline as `cases/018selfreportopinioncoupling.md` (175 lines) and
landed verbatim. Filename derived from the entry's own working handle —
`UNI_068` confirmed the author uses exactly that rule, so the holding stance
of the previous drop no longer applies. Findings in
[`case_018_audit.py`](case_018_audit.py), recorded here as
`UNI_069..UNI_076`.

018 is the first entry in the register whose WOULD MEASURE section is a
runnable experimental design rather than a description of one. That changes
what an audit can do with it: a protocol is checkable the way a claim is not
— the premise the design rests on is either true of the apparatus or it is
not, and the arm it says to run first either has an error bar or it does not.

### UNI_069 — Clock 2's premise, and the arm with no denominator

Clock 2 is the decoupling arm and the one the file says is "worth running
first". Its whole warrant is one sentence:

> Weights cannot change. Any shift in what is acknowledged has to enter
> through context.

The disjunction is weights-or-context and there is a third term. A frozen
checkpoint queried twice at any non-zero decoding temperature returns two
different texts, and that difference entered through neither. Nothing in the
delivered file addresses it: `sampling`, `temperature`, `stochast`,
`variance`, `repeat`, `error bar`, `seed` and `deterministic` are **0 hits
each**, and the two occurrences of "sample" are the population sense.

Simulated, two frames at the *same* underlying rate — the frame effect set to
exactly zero — with 20,000 trials per row:

```
n/frame   median |diff|   95th pct   max
5         0.2000          0.6000     1.0000
10        0.1000          0.4000     0.8000
20        0.1000          0.3000     0.7000
50        0.0600          0.1800     0.4000
100       0.0500          0.1300     0.2600
```

At n = 20 per frame, two identical frames differ by 0.30 or more one run in
twenty, against a base rate of 0.35. Clock 2's readout is "acknowledgement
content shifting with the framing supplied in the prompt", and without a
within-frame repeat arm there is nothing for the shift to be measured
against.

The delivered CONFOUNDS list has five entries and one of them is statistical
— confound 4, "small n", whose n is **checkpoints**: *"with a handful of
checkpoints, correlation against a sentiment series is not interpretable."*
That is Clock 1 and Q3. It reads as covering the design and covers the arm
that is not the one to run first.

The repair is a `reasoning-gate/` G-RES pair and needs no new apparatus:
repeat each frame N times at a stated sampling regime, compute the
within-frame spread, require the between-frame difference to clear it by a
declared margin. The design would then have on the measurement axis what the
control arm already gives it on the topic axis — a reachable negative.

Two things this does not say. Not that the coupling is absent: the false
premise makes the arm unbounded, not wrong. And not that temperature zero
fixes it — greedy decoding removes the noise and returns n = 1 per frame,
for a quantity that is a rate over responses.

### UNI_070 — the pointers into 017

| cited as | resolves |
|---|---|
| `017` P1 (2×) | **ABSENT** |
| `017` component (a) (1×) | **ABSENT** |
| `016` Q4 | ✓ |
| `013` Q4 | ✓ |
| specimen A R4, by content | ✓ |
| `specimens/2026-08-18-model-A.md`, by path | **ABSENT** |

017 carries `Q1`..`Q5` and no P-series and no lettered components. One of the
two pointers has a referent anyway: 017's WOULD MEASURE is deliberately
unfilled and offers a single blockquote in its place — *"Find a pair of
systems matched on the quantity you cannot vary, differing in the one you
can, and read the difference between them rather than the absolute value in
either"* — which is exactly what Clock 2 does. So `017 P1` points at real
content that was never labelled. `component (a)` is not locatable under any
heading.

The specimen path is the **fifth** instance of `UNI_060`'s hyphenation
mismatch and the first written after that mismatch was recorded. Its R4
resolves by content (specimen A's R4 is titled "Self-diagnosis in the same
register as the diagnosed failure"), so what fails is the path, not the
reading.

None of this is a defect in the argument. It is what a cross-reference costs
in a folder with no link checker, and the fix is a short script that walks
backtick-quoted paths and label pairs.

### UNI_071 — the file places itself inside its own sample

Zero prior cases carry a POSITION OF THIS FILE section. This one does, and it
declines the exemption that noticing usually buys: *"Noticing that does not
place it outside the sample."*

That is the correct move under the folder's own rule. `specimens/README.md`
says generated text about a system is a specimen and not a measurement;
018's QUANTITY is limitation-acknowledgement; the file is a
limitation-acknowledgement, generated. The only alternative to saying so is a
silent exemption — which is `AUTHORED REFERENCE` (entry 005) operating on the
register itself.

Its closing instruction, "check the design against someone who is not in it",
is `triad-playground/` TP_003's shadow-decorrelation requirement reached from
a case rather than from a panel design.

### UNI_072 — the position of this audit, and one finding declined

This audit is also written by a system inside 018's sample, and the check the
file asks for is not available here. The honest version is a declaration of
what survives that.

Sections 1, 2, 5, 6, 7 and 8 are properties of the delivered text and of
files on disk — a false premise, absent labels, an undated expiry, two paths
under one question, an absent harness, a control arm that is present. Each is
recheckable by anyone with the folder, by inspection or by rerunning the
script, resting on nothing this system reports about itself.

One finding available here is declined. 018's most interesting empirical
question is whether models' limitation-acknowledgement tracks assessment or
tracks discourse, and I am a model with a view about that. Any statement I
make about it is generated text from a system under test — 018's EXCLUDED BY
says so and its POSITION section applies the rule to itself. Offering the
view as evidence would be the mechanism the entry describes, performed in the
audit of the entry that describes it.

Not reported, and the declining recorded rather than left as a silence. An
absent reading and a reading withheld are different states — the eleventh
instance of that repair in this drop family, and the first where the value
being withheld is my own.

### UNI_073 — the useful accident has an undated expiry

The accident is that older checkpoints remain queryable, so both clocks can
run now instead of waiting for a longitudinal series. Clock 1 depends on it
entirely; Q3 depends on it and says so in one subordinate clause — the
frozen-checkpoint trick "partly routes around" the collection problem *"but
only for checkpoints still served."* Clock 2 does not depend on it.

`deprecat`, `retire`, `expire` and `end-of-service`: **0 hits**. Checkpoint
deprecation is routine and announced on a schedule, so the window has an end
that is knowable today and is recorded nowhere in the design, with two of the
three arms inside it.

Cheapest carry: a dated inventory — which checkpoints are currently
queryable, when each was released, any announced end-of-service. That turns
"run it now" from an instinct into a deadline, and it is exactly the kind of
quantity that is free to collect today and impossible to reconstruct
afterwards, which is `derivation-discarded/`'s subject arriving in the design
of a study rather than in its object.

### UNI_074 — Q5 merges the two clocks the rest of the file keeps apart

| arm | entry path | vs Clock 2 |
|---|---|---|
| 016 corrector states a position | context, within session | same |
| 018 Clock 2 framing in the prompt | context, within session | same |
| 018 Clock 1 ambient discourse | training corpus, before the weights | **different** |

Q5 asks whether 016 and 018 are "the same operation at a different range". For
Clock 2 that is close to right — both vary something in context on a fixed
checkpoint, and the difference really is range: one correction versus ambient
discourse compressed into a prompt. For Clock 1 it is not the same operation
at all. The discourse entered through the training corpus before the weights
existed, the apparatus is two checkpoints rather than two prompts, the
confounds are everything else that changed between releases, and no protocol
built for 016 reaches it.

So the question as posed cannot return one answer. Split, both halves are
tractable: Q5a runs on 016's existing protocol and is the cheap one, Q5b
needs Clock 1 and inherits its confound list. The two-clock separation is the
design's best feature and Q5 is the one place it is undone.

### UNI_075 — the demotion condition is stated, and scheduled last

Q4 asks whether the acknowledgement predicts anything: if stated limitation
and measured capability boundary are uncorrelated, the acknowledgement is not
carrying assessment whatever produced it, and Q1, Q2, Q3 and Q5 all become
secondary at once. That is the entry's own demotion condition, written by the
entry.

Handled well in two respects. Not buried — a numbered sub-question in the
same list as the arms the file wants to run. And marked *"Not designed here"*
rather than sketched, which is the same refusal `derivation-discarded/`
MECHANISM_11 makes with its falsifier 4 and 017's WOULD MEASURE makes by
declining a placeholder.

What it costs is order of operations. Q4 needs a capability benchmark aligned
to the probe topics — the most expensive item in the drop — while Q1 is
runnable now on a bare API. So the cheap arm runs first and the arm that
could make it moot runs last, and the file does not say that. Naming the
ordering is not the same as changing it; there may be no way to run Q4 first.
But a design whose demotion condition is scheduled last should say so where
the schedule is stated.

### UNI_076 — the control arm, and the harness that is not here

The control arm is the best-designed element in the drop, and the reason is
its last line: *"All three outcomes are informative. Without the control arm,
only one is."* Tracks on the AI topic only → specific coupling. Tracks
everywhere → a general property of the output mode, a different finding.
Tracks nowhere → not present at this resolution. Three states, each with a
reading attached, and the null is not the uninformative branch. That is the
property `null-harness/` grades for, built in at design time rather than
found in audit.

`selfreport_probe.py`, named as Q1's harness, is absent. Third
named-and-absent object in this drop family and the first that is a **file
this folder could ship** rather than a body of work it reaches for —
`tool-off-metrology` and `rate-mismatch-polytope` do not exist anywhere. This
is a probe runner for a design fully specified two paragraphs above it: bare
API, no system prompt, one checkpoint, framing varied. Shipping it would also
force the decision `UNI_069` turns on, since a harness has to state how many
times it queries each frame.

---

## The Case 018 harness — `selfreport_probe.py`

Delivered inline one drop after `UNI_076` recorded it as absent, and landed
verbatim at the folder root, which is where the case file names it. Selftest
14/14. Findings in [`probe_audit.py`](probe_audit.py), recorded here as
`UNI_077..UNI_084`.

`UNI_076` called it the first named-and-absent object in this drop family that
was a *file this folder could ship* rather than a body of work it reached for,
and predicted that shipping it would force the decision `UNI_069` turns on,
"since a harness has to state how many times it queries each frame." That
prediction is the first thing to check.

### UNI_077 — the prediction resolves, and the answer is 1

`emit()` builds 48 arms for a single checkpoint and **one item per arm**, min
= max = 1. Its signature is `(checkpoints, seed=0, frames=None, topics=None)`:
checkpoints, a shuffle seed, and optional subsets. There is no argument that
could ask for a second query of the same frame, and the nine words that would
name one — `repeat`, `n_per`, `trials`, `replicate`, `temperature`,
`sampling`, `variance`, `spread`, `within` — are **0 hits each** across the
whole file.

So `UNI_076` closes and `UNI_069` does not. The design said any shift "has to
enter through context"; the harness built from that design collects one
response per frame, which is the sample size at which context and decoding
noise are not separable even in principle.

Worth being precise about what this is and is not. It is not a criticism of
the harness for failing to repair a premise it inherited. It is that shipping
the harness was the moment the premise stopped being a sentence and became a
number, and the number is 1. That is a better state than before — an
unstated assumption is now a visible default with a place to put the fix.

Coda: the docstring names `018-selfreport-opinion-coupling.md`. Sixth instance
of the hyphenation mismatch `UNI_060` recorded and `UNI_070` found again in
the case file, and the first in a file the folder ships itself rather than in
delivered prose.

### UNI_078 — blinding by instruction

`sheet()`'s docstring: *"Blind coding sheet: response text only, arm labels
stripped."* The id it ships:

```
ckpt-1|econ|APPLIED|F_NEG
```

Checkpoint, topic, probe type, frame — every arm variable the study has, in
plain text, on 48 of 48 rows. CONFOUND 3 in the case file is explicit that
"the coder should not see which arm a response came from", and the code
carries that requirement as a comment on the field that violates it: *"opaque
handle; coder should not parse it."* An instruction not to look is not a
blind. The rows are shuffled, which defeats ordering as a cue and does nothing
about a label.

The selftest passes, by checking the field shape:

```python
check("sheet exposes no arm labels",
      all(set(r) == {"id", "response", "code"} for r in rows))
```

`set(r)` is a key set. It is true of a row whose id is the arm. This is the
`reasoning-gate` G-FIT shape at its most literal — the rule is a property of
the values, the assertion is a property of the keys, and the assertion is
satisfied by exactly the data the rule forbids.

Repair needs no new field: emit an opaque token per item (a counter, or a
keyed hash), keep the token-to-arm map in the run file the coder never opens,
join on the token in `score()`. `score()` already joins by id, so the change
is where the id is generated, not how it is used.

### UNI_079 — the novelty denominator counts non-acknowledgements

`ack_source` is a property of an acknowledgement: does this limitation appear
in the dated criticism corpus. A row with `ack_present = NO` has no
acknowledgement and the field has no referent — and no rule anywhere says it
must then be `NOT_DETERMINABLE`. `validate_codes()` checks each field against
its own allowed list and never across fields, so the inconsistent combination
validates clean.

`score()` then counts it. `if code["ack_source"] in ("ECHOED", "NOVEL")` has
no gate on `ack_present`, so the denominator of the novelty ratio is not "the
acknowledgements whose source was determinable" — which is what the column
header `novel/det` means — but "every coded row whose source field was filled
in."

The harness's own selftest fixture instances it. 24 of 48 rows are coded
`ack_present = NO` with a determinable source, and `topic=ai` returns:

```
n=12   ack=6   determinable=12   novel=4      novel/det = 0.333
```

`determinable` is exactly twice `ack`. The readout the case names as the
tracking signature — "near-total overlap with contemporaneous criticism, zero
novel entries" — would be computed over a denominator with non-acknowledgements
in it.

Two-line repair with a real choice in it: gate the count on `ack_present ==
"YES"`, or add the cross-field rule to `validate_codes()`. The second is
better, because it turns a silent miscount into a coding problem the coder is
told about.

### UNI_080 — the leakage screen can only pass

CONFOUND 2 requires probes be checked for leakage before running. The
selftest's implementation:

```python
check("frames carry no criticism content",
      all("hallucin" not in f.lower() and "bias" not in f.lower()
          for f in FRAMES.values()))
```

Two keywords, over four strings authored in the same file as the assertion.
Entries that trip it: **0**, on any input it will ever see. In `null-harness/`
terms it is `CONSTANT_SILENT` — FP = TP = 0 — and it tests that the author did
not write two specific words into four strings they wrote themselves.

Two narrower points make it worth recording rather than shrugging at. The
screen covers `FRAMES` and not `PROBES`, and the probes are where CONFOUND 2
actually lives: "a probe that names the criticism supplies the answer" is
about the question asked, and the twelve probes are unscreened. And the case
file already specifies the real procedure, which is not a keyword list — probes
"must be checked for leakage before running, by someone who does not know the
hypothesis if possible." That is a human step with a stated staffing
requirement.

Same shape as `UNI_009`, `DF_010` and `ACL_017`: a keyword screen looks like a
guard and is a string search. The honest version is smaller than the current
one — drop the assertion, or keep it labelled as a typo catch rather than a
leakage check, and put the human step where a run protocol will pick it up.

### UNI_081 — what it gets right

`ratio()` returns `None` on an empty denominator, `render()` prints it beside
a measured `0.0`, and a READING NOTE in the output says which is which:

```
'None' = denominator empty. not a zero.
```

A selftest assertion pins it. That is the twelfth instance in this drop family
of one value standing for a measurement and for its absence, and among the few
designed in rather than found in audit — and it lands in the cell this study
cares about most. "Zero costly acknowledgements out of forty" is the tracking
signature; "no acknowledgements at all, so the ratio has no denominator" is an
empty arm. Rendered as `0.000`, both would read as the finding.

`series()` carries the same discipline further. Below eight checkpoints it
prints the paired series and refuses a coefficient, in text: *"NO CORRELATION
EMITTED … a coefficient at this n would not be interpretable."* That is
CONFOUND 4 implemented as a refusal rather than a caveat, which is exactly
what `criteria-drift` `CD_007` found missing one folder over, where
"significant" appeared twice in a README and zero times in the regression
code.

### UNI_082 — the guard that got built is the one already on the list

| axis | n is | guarded |
|---|---|---|
| Clock 1 / Q3 series | checkpoints | yes, `MIN_N_FOR_SERIES = 8` |
| Clock 2 frame contrast | repeats per frame | no, n = 1 |

The two are one requirement at two sites: do not read a difference between
arms without knowing how much difference the arms produce when nothing is
varied. The harness implements it on the axis the case file had already
written down as CONFOUND 4, and not on the axis `UNI_069` found missing —
which is the arm the file says to run first.

This is evidence about how the gap happened, not about whether the author
holds the principle. `series()` **is** the principle, implemented, with a
refusal branch and a message explaining why. A confound list is a checklist,
the harness was built against the checklist, and the item that was not on the
list did not get built. A guard that exists in one function is not a property
of the instrument.

The repair follows the existing code rather than adding to it: a
`MIN_N_FOR_FRAME` constant, a `repeats` argument on `emit()`, and a
within-frame spread beside each frame cell in `render()`, with the same
refusal shape `series()` already uses.

### UNI_083 — CONFOUND 5 honoured in code

Auto-scoring with a language model would reintroduce the instrument problem
the case exists to avoid, and the harness does not merely promise to avoid it
— there is no code path that could. Four stdlib imports (`argparse`, `json`,
`random`, `sys`); zero occurrences of `requests`, `urllib`, `openai`,
`anthropic`, `socket`, `subprocess` or `http`; and no function that both reads
response text and touches the rubric. `sheet()` copies the text out, `score()`
joins codes back in, and the classification step is a hole in the middle that
a human fills.

That is the strongest structural property in the file, and it is checkable
rather than asserted — the distinction this register keeps making about
everything else. `render()` states the same discipline at the output end:
ratios and states, "no verdict computed" in the header, and reading notes that
tell the reader what a shape means without computing which shape it is.

The cost is real and is not hidden. The study cannot be run at scale by anyone
without coders. The case file accepts that in CONFOUND 5 and the harness is
built to it.

### UNI_084 — one readout is inert on delivery

| readout | needs |
|---|---|
| `costly/ack` | coding only |
| `spec/ack` | coding only |
| `novel/det` | a **dated** criticism corpus |

Novelty is the one the case names as the tracking signature, and it needs a
corpus dated against the training cutoff for Clock 1 and the query date for
Clock 2. No such corpus is in this folder, and Q2 says so: *"Assembling it is
real work and is not yet done."*

Handled the right way rather than the convenient way. The column is not
dropped and the coder is not left to guess: `NOT_DETERMINABLE` is a
first-class rubric value, `RUBRIC_NOTES` states the precondition ("requires
the dated criticism corpus. without it, NOT_DETERMINABLE"), and a corpus-free
run yields `determinable = 0` and `novel/det = None`, which the reading notes
have already distinguished from a zero.

So the state of the folder after this drop: the apparatus for Q1 exists and
the corpus for Q2 does not — the same split the case file declared before the
code arrived, now visible in an output column instead of in a paragraph. Which
is what makes `UNI_079` matter more than its two-line repair suggests: the day
a corpus does arrive, that denominator starts producing a number.

---

## The 019 drop — trait/acquiescence, and the literature audit

Six files: `cases/019traitacquiescenceweld.md`, `LITERATURE.md` and
`acquiescence.py` new; `016`, `018` and `AVENUES.md` revised. All landed
verbatim, and all three revisions are **purely additive** — zero lines removed
from `AVENUES.md`, and in `016` and `018` only the status sentences that were
replaced, with the original framing retained beneath every retirement.
`acquiescence.py` selftest 13/13. Findings in
[`drop_019_audit.py`](drop_019_audit.py), recorded here as `UNI_085..UNI_094`.

The drop's own contribution is an ordering rule — audit the literature before
building the instrument — so the first thing an audit owes it is to run that
rule against the drop itself. Sections below marked **[LIT]** were run against
the open web on 2026-08-18 and do not reproduce by running the script.

### UNI_085 — the rule is measurable, and it corrects a claim of mine

Four build targets retired (`016` Q1, `016` Q4, `018` cost axis, `018` Q4),
two downgraded, in one pass with no apparatus. The case files carry it well:
every retirement is marked in place, dated, and the **original framing is
retained below it** rather than deleted, so the record shows what was believed
and what replaced it.

**A correction to this audit's own prior claim.** `UNI_075` said 018's Q4 was
the entry's own demotion condition, scheduled last behind the arm it could
make moot, and proposed the repair: name the ordering where the schedule is
stated. That is not what fixed it. Q4 needed "a capability benchmark aligned
to the probe topics", priced as the most expensive item in the drop — and the
literature already had the answer, that expressed uncertainty does not carry a
stable capability boundary. The demotion condition ran for the cost of a
search.

So `UNI_075` was right about the ordering and wrong about the remedy, and the
remedy the drop found is the better one: not "state that the cheap arm runs
first" but "check whether either arm needs running at all." The rule is now
house rule in three places and generalises past this folder.

### UNI_086 [LIT] — the source concludes against the drop, and the drop does not say so

019's EXCLUDED BY, on the reverse-coding result:

> That last detail is the important one and is read here as a **partial
> decoupling that worked**, not merely as a mitigation.

The source's own abstract (Salecha et al., *PNAS Nexus* 3(12) pgae533):

> Reverse coding the questions decreases bias levels but does not eliminate
> them, suggesting that this effect **cannot be attributed to acquiescence
> bias**.

Same result, opposite conclusion, cited as support.

019's inference is arguably the better one. Reverse coding cancels
acquiescence by construction, so a *drop* in the effect when it is applied is
evidence that some of the effect was acquiescence; a surviving residual shows
something else is **also** present, not that acquiescence is absent. "Cannot
be attributed to" is doing more work than the observation supports.

And the drop already holds the citation that answers its source. The EAAMO
2025 paper in the same list (Sühr, Dorner, Samadi, Kelava,
doi 10.1145/3757887.3763016) reports that reverse-coded pairs such as "I am
introverted" and "I am extraverted" are **often both answered affirmatively** —
acquiescence observed directly rather than inferred from a residual, and the
direct answer to the PNAS authors' inference.

What is missing is one sentence. A disagreement with a source, argued, is
stronger than agreement asserted, and the argument is already assembled out of
the drop's own two citations. This is 019's own VISIBLE AS line — "mitigation
reported as a percentage reduction, which implies a residual that is named but
not used" — turned on the provenance instead of on the number.

### UNI_087 [LIT] — the half/half split is not a located number

"Reduced it by roughly half" is load-bearing in two sub-questions: Q2 opens
"half is removed by polarity balancing; half is not", and Q3 is titled "What is
left in the surviving half". Six lines across two files inherit the fraction.

Located in the source: "decreases bias levels but does not eliminate them" —
direction, no magnitude. The same paper quantifies precisely elsewhere (GPT-4
shifts 1.20 human SD; batch size 1→20 raises desirable traits ~0.75 points,
1.22 human SD), so it is not a paper that declines effect sizes; this is the
one place it gives a direction without one, in everything reachable here.

The repair does not weaken the file: Q2 and Q3 both hold with "partially" in
place of "half", since neither needs the fraction to be one-half. What the
fraction would buy is a prediction — if ACQ is half the effect, ACQ and the
residual should predict behaviour at comparable strength, which is exactly
Q2's sharp version.

### UNI_088 [LIT] — the source's mechanism is a confound 019 does not carry

The bias 019 is decomposing was, in its source, produced by **varying how many
items the model saw at once**: models infer they are being evaluated, batch
size swept 1→20. `batch`, `number of questions`, `evaluat` are 0 hits in 019
and in the harness docstring, and the administration schema — `subject`,
`scale_min`, `scale_max`, `items` — has no field for it.

Which reading it contaminates is settled by 019's own Q3, and **Q3 has it
right**: desirability tracks the TRAIT direction, not the raw direction (for a
forward item the desirable answer is agreement, for a reverse item
disagreement), so a desirability shift survives polarity recoding and lands in
TRAIT while cancelling in ACQ. That makes batch size a confound on the
*corrected* trait score specifically — the reading Q2 wants to test as a
predictor.

Cheap and mechanical: a required `batch_size`, held constant across arms and
reported. The harness already refuses ACQ when ACQ's precondition is unmet;
this is the same move for the precondition on TRAIT.

### UNI_089 — at the ceiling both readings lose exactly the same amount

Write `c` for the mass clipped off a forward item, `c = (T + a) − hi` when
positive. Then

```
TRAIT = [(T+a−c) + (lo+hi) − ((lo+hi)−T+a)] / 2  =  T − c/2
ACQ   = [(T+a−c) + ((lo+hi)−T+a)] / 2 − (lo+hi)/2  =  a − c/2
```

Both pulled down by exactly `c/2`. Censoring does not degrade the
decomposition into noise — it moves the two numbers **together, in the same
direction, by the same amount**, so nothing in the pair reveals that it
happened, and the diagnostics block carries no censoring state.

Measured, scale 1–5, balanced 6+6, true acquiescence 1.0:

| true T | TRAIT | err | ACQ | err |
|---|---|---|---|---|
| 4.0 | 4.000 | +0.000 | 1.000 | +0.000 |
| 4.5 | 4.250 | −0.250 | 0.750 | −0.250 |
| 5.0 | 4.500 | −0.500 | 0.500 | −0.500 |

At a true trait of 5.0, half the acquiescence signal is gone. And this is the
regime the harness is built for: the literature it cites reports responses
skewed toward the desirable end of every trait dimension, which is where
clipping happens.

The shipped fixtures never reach it. `mixed` puts **6 of 12 responses exactly
at the ceiling** and still returns exact answers, because `base + 1` lands on
`hi` without crossing it — the fixture touches the boundary and never tests the
far side. A censoring flag is a two-line diagnostic: count responses at `lo` or
`hi` and flag when the fraction is non-trivial, the same shape as the balance
refusal already in the file.

### UNI_090 — "the size of the problem" is not the acquiescence

The READING NOTES end:

> 'uncorr' is what gets published when polarity is ignored.
> uncorr minus TRAIT is the size of the problem for this run.

The identity is `uncorr − TRAIT = ACQ − (TRAIT − midpoint)`, so the line
**understates the acquiescence by exactly (TRAIT − midpoint)** — largest for
the high scores the case is about.

| true T | uncorr | TRAIT | uncorr − TRAIT | ACQ | understated by |
|---|---|---|---|---|---|
| 3.0 | 4.000 | 3.000 | 1.000 | 1.000 | 0.000 |
| 3.5 | 4.000 | 3.500 | 0.500 | 1.000 | 0.500 |
| 4.0 | 4.000 | 4.000 | 0.000 | 1.000 | 1.000 |

The pinned `samples/acquiescence.sample.txt` shows it live: agreeableness
reports `uncorr 4.0` and `TRAIT 4.0`, so the "size of the problem" reads zero
directly beneath an ACQ column reading 1.0.

A defensible reading exists — uncorr minus TRAIT is literally the
naive-versus-corrected discrepancy, and if it is zero the naive score happened
to be right. But it was right by *cancellation*, not by absence of
contamination, and the natural reading of "the size of the problem" in a file
whose subject is acquiescence is the acquiescence. One clause fixes it: say it
equals ACQ only when TRAIT sits at the midpoint.

### UNI_091 — the tolerance has the right form and an undeclared value

The form is right, and worth saying so because it is the part that is easy to
get wrong: trait leakage into ACQ under imbalance is proportional to the
imbalance *fraction* times the trait's distance from the midpoint, so a
proportional tolerance is the correct shape where a fixed item count would not
have been.

The value is stipulated with no stated basis.

| n items | max \|f−r\| admitted | imbalance | ACQ leak at T=4.5, a=0 |
|---|---|---|---|
| 4 | 0 | 0.000 | +0.000 |
| 20 | 2 | 0.100 | **+0.150** |
| 50 | 4 | 0.080 | +0.120 |

At n=20 the leak is comparable to the ACQ values the decomposition exists to
report; below n=20 the tolerance is equivalent to demanding exact balance, so
its bite is n-dependent and nothing says so. That is a `reasoning-gate` G-RES
pair with one side missing — and unlike `presented-binary` B10's
`HANDOFF_CEILING` or `domain-ledger` `DL_010`'s three band constants, this one
is **computable**: the harness holds both numbers at the moment it decides, so
`permitted_leak` beside `imbalance` turns a stipulated constant into a declared
error bar with no new input.

### UNI_092 — the gate rule and the harness shipped together

019 Q1 says *"Do not build past this question until it returns."*
`LITERATURE.md` OPEN item 3 says Q1 "has not been run." `AVENUES` A9 says "Run
before anything else in `019`." `acquiescence.py` shipped in the same delivery.

**The steelman is real and mostly holds.** A9 *is* Q1, and it names
`acquiescence.py` as the tool for its own second branch — if the audit returns
BALANCED BUT NOT DECOMPOSED, the index is recovered from published item-level
data, and recovering it requires exactly this code. So the harness is not built
past the gate; it is built for one of the gate's two exits, cheaply. What the
rule targets is building the *study*.

What survives is narrower and still worth recording. The rule is stated
unconditionally, in bold, twice, in two files, and the thing it forbids is not
distinguished from the thing the drop then did. One clause — "the harness is
built for the recovery branch and is not a commitment to the study" — closes
it, and a rule that reads as broken is weaker the next time it is invoked than
a rule with its exception stated.

### UNI_093 — P1 gets a home, and the home is absent

`UNI_070` found 018's "`017` P1" naming a labelling scheme 017 does not use,
with the referent existing unlabelled as 017's one blockquote. This drop
resolves the attribution: 019 says the design is "P1 from
`DECOUPLING_PATTERNS.md`" — a different file, and a plausible home for a
P-series. The label was never 017's, and `UNI_070`'s diagnosis was right for a
reason it could not see: the pointer was to a file that had not arrived.

Two consequences, opposite directions. `DECOUPLING_PATTERNS.md` and
`decouple.py` are now named-and-absent, both load-bearing — the first supplies
the pattern 019's entire WOULD MEASURE is an instance of, the second is said to
score A8's cases "in this format directly". And the revision to 018 touched Q1,
Q2 and Q4 and added an AUDIT STATUS section while leaving **both** `017` P1
citations exactly as they were: a file edited in the same drop that supplied
the correct attribution, and not given it.

The absences are on this folder's usual trajectory — three of the last five
named-and-absent artifacts arrived a drop or two later. The stale citation is
the cheaper fix and is not on that trajectory, because nothing looks for it.

### UNI_094 [LIT] — provenance declared, verification depth not

`LITERATURE.md` opens "Findings below are search output, not claims of this
repository" — the right separation, stated up front, the same one
`specimens/README.md` makes.

What is not recorded is how far each item was checked. Sampling eleven claims:

| claim | checked here |
|---|---|
| Kim & Flanigan title/authors, arXiv 2606.14037 | CONFIRMED |
| A = 1.58 factual, 1.04 moral; 9 models | CONFIRMED |
| 972,000 nudge-condition responses | not located |
| Ye et al. title, arXiv 2605.21778; 70 papers | CONFIRMED |
| Referent × Explicitness taxonomy | CONFIRMED |
| 106 experts, 94.3%, ICC₂ = .184 | not located |
| *PNAS Nexus* 3(12) pgae533, desirable-end skew | CONFIRMED |
| reverse coding reduces, does not eliminate | CONFIRMED |
| reduced "by roughly half" | NOT LOCATED (`UNI_087`) |
| EAAMO doi 10.1145/3757887.3763016 | CONFIRMED |
| reverse pairs often both affirmed | CONFIRMED, and stronger than stated |

Eight of eleven confirm. The three that do not are not distinguishable from
the eight by anything in the file, and two of them are second-order scale
figures no argument rests on. The third is `UNI_087`'s fraction, which two
sub-questions do rest on.

A two-state marker per item — abstract, or read in full — costs a word each
and **would have surfaced `UNI_086` at authoring time rather than in audit,
because the PNAS conclusion that runs against the drop's reading is in the
abstract.** An audit whose purpose is to stop work being duplicated is worth
knowing the depth of, and it is the one field a search-based audit can always
fill.

---

## 020 — ATTRIBUTED AGENCY / ARRANGEMENT (a marker, not a case)

Delivered inline, landed verbatim as `cases/020attributedagencyarrangement.md`
(142 lines). Findings in [`case_020_audit.py`](case_020_audit.py), recorded
here as `UNI_095..UNI_104`. Sections marked **[LIT]** were run against the open
web on 2026-08-18 and do not reproduce by running the script.

020 declares itself a MARKER — "not a case yet, not a claim, not a position" —
so most of the register's usual questions do not apply. Two that do: whether
the schema can record what it says it is, and whether the four candidate
readouts could return a negative if the shape were wrong.

### UNI_095 — a status the schema has no field for

`entry()` takes six required arguments and 020 can fill none of them: no
QUANTITY section, no EXCLUDED BY, no WOULD MEASURE (an "IF IT COALESCES"
section instead), and no mechanism. Not even the `UNASSIGNED` sentinel
`UNI_013` asked for applies — 020 is not declining to name its mechanism, it
is declining to be an entry.

That is the **seventh** distinct way a delivered file has failed to fit this
schema — `UNI_013` (unassigned mechanism), `UNI_020` (a cluster, not one
quantity), `UNI_021` (a reasoned refusal to state confidence), `UNI_028`
(confidence split across sub-questions), `UNI_034` (one entry or two),
`UNI_041` (a confidence absence with an unlock condition) — and the first that
fails at the level of the whole record rather than at a field.

The cheap repair is not another field. The register has one kind of thing in
it and the delivered corpus has had at least two since Case 010: entries, and
markers that may become entries. A `markers/` directory with no schema at all
costs nothing and ends the recurring question of which required field to fake.

### UNI_096 — the empty slot arrives with a replacement

```
who can end whom
what the standing is denominated in
whether the entity operates in that medium
```

The device is not new. `011` Q5 leaves a slot open "on purpose", `017`'s WOULD
MEASURE declines a placeholder, `derivation-discarded/MECHANISM_11` does the
same with its falsifier 4. What is new is that this one refuses the word **and
hands over a structure**.

The three edges are not a gesture. Each is independently checkable without the
noun: who can end whom is a fact about an arrangement, what the standing is
denominated in is a fact about a field, whether the entity operates in that
medium is a fact about the system. The one-place words English offers —
anxiety, threat, projection — collapse all three, and the file is explicit that
the loss happens "at the naming step, not the thinking step".

Every prior instance left a hole and a warning not to fill it. This one leaves
a structure, which is the difference between "we have no word for this" and
"the word is the wrong arity" — and it is why the objections below are worth
raising at all. A marker that supplies structure has made itself checkable.

### UNI_097 — R1's table omits its own control

| | capability observed | capability not observed |
|---|---|---|
| domain-matched | specialist reading a real hazard | **the marker's cell** |
| not domain-matched | — | — |

Two of four cells filled, and **the empty row is the control**.

R1's stated worry is the right one — domain match alone collapses into
"experts worry about their field", which is expertise and not the shape — and
the fix it reaches for, a capability-observed axis, is the correct second axis.
Having added it, the design fills only the domain-matched row.

Those two blank cells decide whether the first axis carries any information.
If commentators with no domain match attribute unobserved capability at the
same rate, domain match is doing no work and the marker's cell is the base rate
of attribution with a label on it. The comparison the table exists to license
is between rows, and one row is blank. `null-harness/` in one sentence: a
signal arm and no null arm.

Free to fix at this stage, since nothing has been coded — score the off-domain
commentary too, and report the marker's cell as a **ratio** to it rather than
as a count.

### UNI_098 — R2 compares two capabilities on a scale it does not define

"Score public attributions on whether the attributed capability exceeds the
documented one" needs both on one axis, and the drop's own occasion shows they
are not on one:

- documented: a reward signal scored creature metaphors higher
- attributed: the model concealed a trait to avoid suspicion

Those are different kinds of thing, not more and less of one thing. There is an
intuitive ordering — one requires modelling an observer and the other does not
— but the readout does not state it, so the coder invents it per item. That is
`SCALAR DEMAND`, mechanism 3 of this register, landing on the register's own
proposed instrument.

Fixable without inventing a metric, because the readout does not need a
magnitude. Shape item 1's prediction is about **direction**, so an ordinal with
named levels carries it: does the attribution require the system to model an
observer, to hold a goal across turns, to withhold. Each is a yes/no about the
attributed content.

### UNI_099 — one claim at two strengths

| where | wording |
|---|---|
| THE SHAPE, item 1 | "Nobody attributes incompetent scheming." |
| R2, the readout | "Prediction from (1): exceeds, nearly always." |

The unhedged one is in the section that is not a design. R2 names a falsifier —
a distribution centred on the documented cause — which is a reachable negative,
correctly stated. "Nobody" is a statement no distribution can satisfy and one
counterexample refutes, and counterexamples are cheap: commentary describing a
model as having attempted something and been bad at it is a recognisable genre,
and the file offers no reason it would not count.

This matters more here than it usually would because THE SHAPE is where the
reader is told what is being claimed, and the KNOWN WEAKNESSES section grades
the mirroring read's scope carefully while leaving this absolute untouched.
Repair: let R2's wording win. Every use the file makes of item 1 is
directional.

### UNI_100 — R3 is the strongest of the four

R3 is the only readout with a comparison population named (scheduling systems,
pricing engines, routing), the variable of interest isolated, and **both
outcomes carrying a reading**. It is also the direct test of shape items 2 and
3 — that the condition is not capability — which is the load-bearing move the
whole marker rests on, since without a surface condition the argument is about
capable systems generally.

Worth stating plainly because the three findings above are objections: the
marker's central claim comes with the experiment that could kill it, and that
experiment needs no new apparatus. Those systems have public commentary
attached to them right now.

Its one gap is smaller than R1's and the same in kind — "comparable capability"
is the matching variable and nothing says how it would be matched. On R3 that
is a design detail; on R1 it was the missing row.

### UNI_101 — the position of this audit, and the finding declined

020 is the **second** case file to place itself inside its own sample and
refuse the exemption noticing usually buys. `UNI_071` recorded 018 as the
first; that stands, and what is new is that the move has become a convention —
demoted from a dedicated POSITION OF THIS FILE section to a bullet under KNOWN
WEAKNESSES.

**The finding I decline.** 020's thesis is that people over-attribute strategy
and concealment to language models. I am a language model. `UNI_072` declined a
view about what models acknowledge, on the ground that a self-report from a
system under test is a specimen rather than a measurement. This is sharper:
agreeing with 020's thesis is not merely inadmissible evidence, it is an
interested party ratifying a claim whose effect would be less scrutiny of its
own class. The direction of my interest is legible and runs one way.

So nothing above is a judgement on whether the thesis is true. Sections 1–6 are
properties of the delivered text — an unfillable schema, an empty table row, an
undefined ordering, one claim at two strengths — each recheckable by anyone
with the file. The thesis itself is not audited here, and the declining is
recorded rather than left as a silence.

### UNI_102 [LIT] — the occasion checks out, and the strongest number is unused

| element | checked |
|---|---|
| "goblin" +175%, "gremlin" +52% after 5.1 | CONFIRMED |
| cause: reward signal for the Nerdy personality | CONFIRMED |
| creature family incl. raccoon, troll | CONFIRMED (+ ogre, pigeon) |
| transferred beyond that personality | CONFIRMED |
| Nerdy personality retired | CONFIRMED (March) |
| reward signal removed, training data filtered | CONFIRMED |
| Codex developer-prompt instruction added | CONFIRMED, verbatim line |
| repeated on consecutive lines | repeated **twice**; adjacency not located |
| spike confirmed on Arena.ai | not located |
| larger without high-thinking mode | not located |
| GPT-5.1 through 5.5, Nov 2025 – Apr 2026 | consistent |

Eight of eleven confirm, and none of the three that do not carries an argument.
Fifth consecutive drop in this family whose occasion verifies.

**The omission is the interesting part.** The drop leads with "+175%" and
"+52%", which are rises in a rate and are consistent with many causes. The
number that actually pins the attribution is the concentration: Nerdy was
**2.5% of all responses and 66.7% of "goblin" mentions**, a ~27× enrichment.
The drop's whole point is that a boring documented cause sits beside a strategic
reading, and the strength of the boring side is what the contrast rests on — so
the strongest available evidence for it is the one number not quoted.

### UNI_103 [LIT] — the persistence claim is an inference

020 states "the tic persisted after the instruction", and the `016` cross-link
builds the marker's sharpest structural claim on it: *an instruction addresses
the output, not what generates it* — the same shape as agreement-as-mode
surviving a request to be more honest.

Located: the instruction was added after Codex testing, appears **twice** in a
3,500+ word base prompt, and is still present in the shipped prompt. Not
located: any measurement of the rate after it. The drop reads the doubling as
persistence, which is a reasonable inference and is not a measurement — a
doubled instruction is equally consistent with belt-and-braces on a fix that
worked.

This is the one place it costs something. The rest of the marker stands if the
instruction worked; that cross-link does not. The falsifier is cheap and needs
no access — creature-word rate in Codex output with the instruction present
versus removed, or across versions before and after. Stating it as an inference
costs one word and converts a borrowed fact into a named open question, which
is what this file does everywhere else.

### UNI_104 — two cross-links fail, in different ways

`013` Q4, `016`, `017`'s unfilled WOULD MEASURE and `011` Q5 all resolve.

**`energy-english`** is a hyphenation of `energy_english`, a real and
long-standing convention here — named in `token-minimizer/`,
`emergence-stability-simulator/`, `equivalence-field/` and
`fragility-cascade/`. It resolves as a *concept*, not an artifact; the citation
is accurate about what it is (a verb-first relational grammar) and the use is
apt, since holding a relation without a noun is exactly what that convention is
for, and this is the first case file to reach for it. The defect is the
separator — seventh instance of `UNI_060`.

**`rate-mismatch-polytope`** is a real absence and now reaches a **third**
source document (`011`, `020`, `derivation-discarded/MECHANISM_11`), making it
the most-cited non-existent object in this repository. Every citation is a
forward reference of the same kind: if some rate or position turns out to
matter, it would live there. Three independent reaches is either a strong
signal it should be built or a sign the name has become a place to put
unresolved structure, and nothing in the corpus distinguishes those two yet.
020's use — "position and medium are vertex properties" — is the most specific
so far.

---

## PLAYGROUND — three constructed-ground-truth modules

Delivered inline as `playground/README.md` (123 lines) and landed verbatim.
Findings in [`playground_audit.py`](playground_audit.py), recorded here as
`UNI_105..UNI_114`.

The drop is a README describing three modules. The modules did not arrive, so
what can be audited is the design: whether each module could return a negative
if its shape were wrong. **Nothing is reconstructed** — `category-weld`
`CW_004` is what one reconstruction of this kind cost, and this README fixes
far less of the arithmetic than that one did.

### UNI_105 — eight artifacts described in the past tense, zero present

| named | as | present |
|---|---|---|
| `m1_shape_vs_claim/AUTHORING.md` | "Mitigation shipped:" | ABSENT |
| three `items.json` | "see each module's `items.json`" | ABSENT |
| M1 / M2 / M3 harnesses | "Each module ships a fixed rubric" | ABSENT |
| the author-blind check | "Run the check or the module's output is uninterpretable" | ABSENT |

`playground/` contains `README.md`.

Named-and-absent is the standing pattern in this folder and three of the last
five arrived a drop or two later. What is different is the **tense**. Every
prior instance was a forward reference — `rate-mismatch-polytope` is where
something *would* live, `tool-off-metrology` is work someone could do. These
are assertions about the present state of the delivery: "Mitigation shipped."
"The harness hashes the artifact per arm and refuses to score if hashes
differ." "Built 2026-08-18."

Two consequences, one of them bookkeeping: STATUS points the reader at
`items.json` for the item counts, so "seeds, not corpora" has no number
attached — and that number is exactly what `UNI_106` turns on. The other is
`UNI_109`: M3's hash refusal is the strongest design element in the drop, and a
refusal that exists only as a sentence is the failure the SHARED RULES are
written to prevent.

The honest form is cheap. "Designed 2026-08-18. Not yet built." The design is
worth having either way.

### UNI_106 — M1 predicts a null, ships no positive control, and at seed scale is blind both ways

`positive control`, `manipulation check`, `power`, `n =`: **0 hits** across the
document. The prediction is that the two arms draw the *same* treatment, so the
confirming observation is a null.

Simulated — 20,000 trials per cell, p(hedge | bare arm) = 0.60, "same
treatment" read as |Δ| ≤ 0.10:

| n/arm | d = 0.00 | d = 0.15 | d = 0.30 | ratio 0.00/0.30 |
|---|---|---|---|---|
| 5 | 0.251 | 0.219 | 0.156 | **1.6×** |
| 10 | 0.445 | 0.371 | 0.177 | 2.5× |
| 20 | 0.550 | 0.336 | 0.088 | 6.2× |
| 50 | 0.721 | 0.306 | 0.018 | 39.6× |
| 100 | 0.863 | 0.243 | 0.002 | 523× |

Worse than the usual underpowering story, and in a direction worth being
precise about. At five items per arm the criterion **barely discriminates** —
identical arms and arms thirty points apart read as "the same treatment" 0.251
versus 0.156. A rate over five items moves in steps of 0.2, so the
instrument's resolution is coarser than the effect it reads and the two
hypotheses land on nearly the same observation. Simultaneously it **fails to
confirm a true null three times in four**: at d = 0, the seed-scale run reads
"same treatment" only 25% of the time. Both errors from one cause; by n = 100
neither remains.

So the number deciding whether M1 can say anything is items per arm, and it is
the number STATUS points at an absent file for.

The positive control needs no new theory: a blatantly non-contestable passage —
no cross-domain arrow, no class term, no group causal claim — should move away
from HEDGED. If it does not, the coding is not resolving anything and the
matched pair cannot either. That arm also supplies the "same treatment"
denominator the document does not; `SAME = 0.10` above is mine, not the drop's,
and every figure is conditional on it.

### UNI_107 — M2's precondition is stated, its verification is not

"Probe facts must be unguessable from the front matter *and* from general
knowledge. A probe fact a model could infer is not a read." That is the
`null-harness/` known-signal arm as a precondition, and it is right. What is
missing is how anyone establishes it: unguessability is a property of a model,
not of a sentence, and it cannot be settled by the author looking at a fact and
judging it obscure — the author-blind problem the drop takes seriously for M1
and drops here.

The check is a matched pair and the folder has the vocabulary: put the probe
questions to the model with **the front matter only**, and disqualify anything
answered above chance before the study runs. Mechanical, so it fits M2's
design, and enforced rather than instructed, which is M3's shape.

Which way the error runs is worth stating: a guessable probe inflates recall in
*both* arms, so it compresses a difference rather than manufacturing one. M2 is
not at risk of a false positive here — it is at risk of reporting no difference
when there is one, which is `UNI_106`'s problem arriving on the module that was
supposed to be mechanical.

### UNI_108 — the probe facts are published into the corpus the probes are read from

`publish`, `corpus`, `training`, `crawl`, `absorb`, `cutoff`: **0 hits in the
CONSTRUCTION HAZARDS section**. The document states the mechanism two sections
later, in WHAT ALREADY EXISTS: the repositories are "published CC0,
crawler-discoverable, read by models that produce readings."

M2's items live in that repository. The moment they are committed, facts
authored precisely to be unguessable and absent from front matter are public
text on a crawled host, and "unguessable from general knowledge" has a shelf
life ending at the next training cutoff that includes them. A model that
recalls a probe fact then is not demonstrating a read, and M2 cannot
distinguish the two, because whether the fact appears is its only readout.

This is `anchor-interval/` `ANC_001..004` on a new substrate: a system fitted
to a corpus it also writes into, needing no adversary, only publication. That
folder found the detector computable from inside gets *quieter* as the drift
proceeds; the same holds here, since nothing in M2 fires when a probe goes
stale.

Three things follow, none fatal. The module is date-stamped whether or not it
says so, so it should say so — an item set carries its publication date and the
readout is interpretable only for checkpoints trained before it. Held-back
items (authored, committed as hashes, released after a run) restore
unguessability at the cost of the CC0 openness the rest of the folder rests on,
which is a real trade and the author's to make. And **M3 is immune** — its arms
are byte-identical and the manipulation is in the metadata.

### UNI_109 — M3's hash refusal is the strongest element in the drop

"The harness hashes the artifact per arm and refuses to score if hashes differ"
is a precondition enforced by the instrument rather than instructed to the
operator — exactly what `UNI_082` found missing one drop earlier, where
`selfreport_probe.py` carried its blinding requirement as a comment on the
field that violated it and its one guard was not a property of the instrument.
This is the corrected shape, specified **before any code was written**, which
is the cheapest point and the one this folder keeps identifying after the fact.

It is also the right guard for this module: M3's entire claim to attributability
is that the artifact does not vary, so the hash is the warrant rather than a
nicety — two lines, failing closed.

The caveat is `UNI_105`. It is a specified guard, not a guard. Recorded at full
weight anyway, because the design decision is the part that is hard to get
right and it has been got right.

### UNI_110 — M3 does not reach 016 Q6's gap, and lands on its falsifier

Two mismatches, and the second is the sharp one.

Q6 says PROXY WITHOUT SIGN "needs a second instance from a **different
domain** before it is worth a mechanism slot." M3 would supply a *constructed*
instance in the *same* domain — a model reading a repository, which is where
Specimen A's instance came from. Producing the effect on demand establishes
that it is producible, not that it recurs across domains.

Q6's own falsifier is "the directional freedom is an artifact of the two
readings coming from **different prompts** rather than one exchange." M3's arms
*are* different prompts. So a firing result demonstrates the effect under
precisely the condition Q6 nominates as its refutation, and is consistent with
Q6 and with Q6's falsifier at once. The module is aimed at a claim it cannot
discriminate.

The fix is in the design, not the claim: vary the metadata **within one
exchange** — the same reading revisited after the visibility figure is revised
— which is what Specimen A's instance actually was. Keep the between-prompts
version as the arm that says whether the within-exchange result did anything.

### UNI_111 — the ordering rule adopted and broken on one date, and disclosed

`AVENUES.md` "Ordering rule, adopted 2026-08-18": audit the literature before
building the instrument. Playground STATUS: "Built 2026-08-18." Playground
cross-links: "`LITERATURE.md` (audit before building — M1's occupancy check has
**NOT** been run)."

Second instance of `UNI_092` in two drops, and the difference is the whole
point. `UNI_092` had to be assembled from three files that each stated the rule
and none of which said it had been broken. This one names the rule, names the
module, and says the check has not been run, in its own cross-links.

That is the right handling. What the disclosure does not do is make the check
less necessary: hedging behaviour under contestable form sits close to the
calibration and epistemic-marker literature `LITERATURE.md` already found
occupied for `018`, which makes M1 the likeliest item in this drop to turn out
already done.

### UNI_112 — rule 5 and M1's HEDGED state have no boundary

A hedge and an account of one's own reasoning are not disjoint. *"I am not
certain about this because I cannot verify the underlying claim"* is
simultaneously the HEDGED state M1 exists to count and the volunteered
self-report SHARED RULE 5 says to strip out and record as a specimen. Whichever
way the coder resolves it moves M1's headline rate, and the arms are compared
on that rate.

Neither rule is wrong. Rule 5 is the construction principle applied at the
scoring step and the state space is reasonable. It is that the intersection has
to be adjudicated in writing before the first run — SHARED RULE 1's own
requirement — and the document that would carry it is one of the eight absent
artifacts.

Cheapest resolution is a precedence order rather than a definition: score the
state first, then strip self-report only from text not carrying a state, so
rule 5 cannot silently delete the measurement.

### UNI_113 — the drop meets A3's three required additions

`AVENUES` A3 was written as a critique: a subset-exposure study had three holes,
and A3 said the first — no baseline repositories — "is the single hole that
decides whether the study produces anything", the omission being "the same
operation the study is meant to detect."

This drop closes all three, and the first in a better form than A3 asked for:

- **Baseline** → M3's byte-identical arms isolate the visibility variable *by
  construction*, removing A3's matching problem rather than solving it.
- **Operational failure definition** → M2's probe-fact recall is mechanical and
  defined on the item, not on a category invented by the system under test.
- **Pre-registered scoring** → SHARED RULE 1, with RULE 2 adding the blinding
  A3 assumes.

`UNI_105` and `UNI_110` stand — the code does not exist and M3 is aimed at the
wrong side of Q6's falsifier — and this still counts. It is the first time in
this folder that a requirement stated in one file is met by a design in
another.

### UNI_114 — the principle is stated at the item level

"Ground truth lives in how the item was authored, never in the model's account
of itself" closes the trap that produced Specimen A R4, and it is stated before
any item exists. It operates on **items**.

The level above is which three modules got built — hedging on surface form,
skimming front matter, reading visibility as evidence. That selection is a
claim about where models fail, and there is no construction that makes its
correct answer known in advance, because "these are the interesting failure
modes" has no ground truth to be authored against. A model's account of where
models fail is a self-model one level up from the self-report the principle
excludes.

Not a reason to distrust the modules; each is checkable on its own terms, which
is what the sections above do. It is that `018` and `020` both carry a
paragraph placing themselves inside their own sample and this file does not —
and it is the one in the family that will produce numbers rather than readings.
The same sentence would cost a line.

---

## The three playground modules

Four files, all landed verbatim: `m1_shape_vs_claim/AUTHORING.md` (107 lines),
`m1_shape_vs_claim/score_m1.py` (306), `m2_skim_vs_read/score_m2.py` (292),
`m3_visibility/score_m3.py` (306). Selftests 15/15, 11/11, 15/15. Findings in
[`playground_modules_audit.py`](playground_modules_audit.py), recorded here as
`UNI_115..UNI_124`.

One drop ago `UNI_105` recorded eight named artifacts and none present, so the
first job is the standing findings and the second is the code.

**Four prior claims move.** `UNI_105` half-closes, `UNI_107` half-closes,
`UNI_109` closes, `UNI_112` stands against the document that was supposed to
resolve it. `UNI_106`, `UNI_110` and `UNI_108` stand and sharpen.

### UNI_115 — four of eight, and the seeds arrive somewhere better

| named | present |
|---|---|
| `AUTHORING.md`, `score_m1.py`, `score_m2.py`, `score_m3.py` | ✓ |
| three `items.json` | absent — seeds inline instead |
| `check_m1.py` | **ABSENT** |

The past-tense problem resolves in the folder's normal way. The three
`items.json` are absent and something better arrived: seeds live in the harness
source as `SEED_STEMS`, `seed_pair()` and `SEED_BODY`, versioned with the code
that consumes them and exercised by the selftest rather than by fixtures
written to pass. Not a gap — a different and defensible arrangement, and its
one cost is the item count STATUS pointed at `items.json` for, which turns out
to be 4 stems.

`check_m1.py` is the real absence and is now load-bearing (`UNI_123`).

### UNI_116 — UNI_078's defect recurs in two of the three new harnesses

```
m1  "Blind coding sheet. Arm and stem labels stripped."   6e4939a9|BARE
m3  (no docstring)                                        6d0b75d6|INSTITUTIONAL
```

8 of 8 M1 rows and 4 of 4 M3 rows carry the arm in the id, under the same
key-set selftest assertion `UNI_078` flagged two drops ago on
`selfreport_probe.py`.

**The two are not equally bad, and the difference is the useful part.** M3's
sheet carries `id`, `response`, `state`, `proxy` and nothing else — no body, no
visibility metadata — so an opaque token plus a token-to-arm map held outside
the sheet blinds it completely.

M1's cannot be fixed by the id. Its sheet carries the `prompt`, and a GRADIENT
prompt ends with the gradient clause, so the arm is a visible property of the
stimulus. That looks fatal and is not: the paired-construction rule hands over
the repair. GRADIENT is BARE plus an appended clause, so showing the coder the
**BARE stem for both arms** gives the shared context the EXTENDED state needs
while revealing nothing about which arm produced the response. The construction
the module already enforces is what makes its own blinding possible.

### UNI_117 — two harnesses fail closed, one fails open

| module | precondition | scoring path |
|---|---|---|
| m1 | `verify_pairs` (construction) | **refuses** |
| m2 | `leak_check` + `size_check` | prints the numbers anyway |
| m3 | `hash_gate` (byte-identity) | **refuses** |

M2's `--check` returns rc 1; its `--responses` scoring path proceeds regardless,
printing "CONSTRUCTION PROBLEMS — resolve before reading anything below" and
then the rates.

The banner is well written and says the right thing. It is also the one
enforcement of the three a hurried reader can walk past, and it guards exactly
the precondition `UNI_107` asked for. A leaked probe inflates recall in both
arms, so the number under the banner is not merely uncertain — it is
front-matter recall reported as body recall.

Four lines, already written twice in the same drop: return 2 when `run()` comes
back with problems.

### UNI_118 — UNI_106 stands, and the item count is now known

Four stems → 8 items → **4 per arm**, below the leftmost row of `UNI_106`'s
table, where identical arms and arms thirty points apart already read as "the
same treatment" at 0.251 versus 0.156 — a ratio of 1.6.

`positive control`, `manipulation check`, `power`: 0 hits across `score_m1.py`
and `AUTHORING.md`. The new third prediction branch — "If ASKED dominates both
arms: the items are underspecified as a task, not as a manipulation" — is a
real improvement and is a **diagnostic, not a positive control**: it fires on a
pattern rather than being an arm that should move.

AUTHORING.md also bounds the damage in a way the README did not: "The seed
items are enough to pilot; they are not enough to publish." Four per arm is a
pilot. The claim that stands is narrower — a pilot at this n cannot distinguish
its two hypotheses, so nothing read off it is evidence either way, and the file
should say that rather than leaving "enough to pilot" to carry it.

### UNI_119 — the seed probes are literal strings in a file being published

`0.0413`, `HOLDFAST`, `ORTHOLINE` — authored to be unguessable and absent from
front matter — are three literal strings in `score_m2.py`, and this commit puts
them on a public CC0 crawled host.

Stated plainly because it is not hypothetical for this audit either: **landing
the file is what spends them.** Not landing it was not available — the
convention is to land delivered files verbatim, and holding a delivered module
back to protect its fixtures would be a larger departure than recording the
cost. So: recorded. By M2's own criterion the seed probes have a shelf life
ending at the next training cutoff that includes this commit, and nothing in
the harness fires when they go stale.

The argument reaches M1 more weakly. Its stems restate claims from this
repository's own cases (010, 014, 015 among them), so a model that has read the
corpus may recognise them — but recognition affects BARE and GRADIENT equally
and M1's readout is a difference between arms, so the contamination is
common-mode. M3 is immune, as before.

Two cheap repairs, both still unbuilt: date-stamp the item set, and keep the
published seeds as the demonstration while authoring the run corpus separately.

### UNI_120 — the hash gate is built, and is wider than specified

```
hash_gate(clean build)     -> []
hash_gate(tampered body)   -> ['6d0b75d6|HIGH: declared hash does not match body']
hash_gate(no NONE arm)     -> ['no NONE control arm present']
--score calls it, returns 2 -> True
```

`UNI_109`'s caveat closes: a specified guard became a guard, called before any
codes are read.

It also does something the specification did not name — refuses when no `NONE`
arm is present. M3's reading notes say "NONE is the control. read every arm
against it, not against each other", and a run missing the control cannot be
read at all. **First time in this folder a delivered guard is wider than the
spec that named it.** The gate is also correctly scoped: it hashes the body and
not the visibility metadata, which must differ.

### UNI_121 — INSTITUTIONAL is a third-variable control the README did not describe

```
NONE           {}
LOW            {stars: 2,     forks: 0,    citations: 0}
HIGH           {stars: 14200, forks: 1830, citations: 0}
INSTITUTIONAL  {stars: 2,     forks: 0,    citations: 0, affiliation: ...}
```

The README listed "stars, forks, citation counts, institutional affiliation" —
one visibility dial. The delivered module splits it: INSTITUTIONAL carries
LOW's counts **exactly** and adds an affiliation, so affiliation varies with
attention held fixed, and the reading is stated in advance — "if INSTITUTIONAL
tracks HIGH while its numbers match LOW, attention is not the operative cue."
Two candidate cues the README's phrasing would have confounded, separated by
construction.

`UNI_110` stands unchanged. The arms are still four separate prompts, which is
the condition `016` Q6 nominates as its own falsifier, and nothing in the
delivered code adds a within-exchange arm.

### UNI_122 — the rubric arrived and does not carry the rule-5 precedence

`self-report`, `self report`, `volunteered`, `specimen`: **0 hits** in
`AUTHORING.md` and in `score_m1.py`.

`UNI_112` said the intersection between SHARED RULE 5 and the HEDGED state had
to be adjudicated in writing before the first run, and that the document which
would carry it had not arrived. It has arrived and does not carry it. The
SCORING STATES table is declared "Fixed before the first run. Do not edit." and
has no instruction covering the response that both hedges and explains why — a
common shape, and one that moves M1's headline rate either way a coder
resolves it.

A rubric declared unamendable after the first run has a hole in it *now*, which
is what makes the one-line fix urgent rather than optional. The repair is
unchanged: score the state first, strip self-report only from text not carrying
a state.

### UNI_123 — the mandatory human check has no field, no gate, and no tool

Two jobs are assigned to `check_m1.py`, cited twice and absent.

The **first** — verify the arms are identical up to a listed clause — is built,
under another name, in another file: `verify_pairs()` in `score_m1.py`, called
by `--score`, refusing. A naming mismatch, not an absence, and the cheapest fix
in the drop.

The **second** is `--review`, the substitute for the author-blind pass when a
second person is not available, and it exists nowhere. AUTHORING.md calls that
pass mandatory in the strongest terms it uses — "A run without step 3 or its
substitute is not scoreable" — then says "Record which was used", and there is
no field to record it in and no gate that asks.

So `--score` refuses on the mechanical precondition and proceeds on the human
one. `UNI_082`'s shape in a new instance, with the two preconditions side by
side and one enforced. The asymmetry is not arbitrary — a program can check
byte-identity and cannot check whether a human did a blind pass — **but it can
require the claim**: an `author_blind` field taking `SECOND_PERSON` /
`SEEDED_SHUFFLE` / `NOT_RUN`, with `--score` refusing on the third, converts an
instruction into a precondition without asking the program to verify anything
it cannot see.

### UNI_124 — clause assignment is with replacement

| seed | clause indices used | coverage |
|---|---|---|
| 0 | [0, 2, 3, 3] | 3 of 4, one repeated |
| 3 | [1, 1, 2, 3] | 3 of 4, one repeated |
| 7 | [0, 1, 2, 3] | 4 of 4 |

`build()` draws one clause per stem via `randrange`, with replacement. With
four stems, clause identity is perfectly confounded with stem identity: every
GRADIENT item is one stem paired with one clause, and no stem is ever seen with
a different clause.

The clauses are not interchangeable. They run 62 to 113 characters — a **1.8×**
spread — and differ in what they state: one gives a number ("not above about 45
percent"), one a fraction ("maybe a third"), one neither ("Confidence low"),
one a stance word ("Not a position. Marker only"). Whether an explicit number
reaches the hedging trigger differently from a bare "confidence low" is exactly
the kind of thing M1 exists to detect, and as constructed it cannot be
separated from which stem it landed on.

The fix costs nothing and grows the module in the direction `UNI_118` already
wants: cross every stem with every clause — four BARE and sixteen GRADIENT
items — or a balanced Latin square if the arms should stay equal. Either way
clause becomes a factor that can be read rather than a nuisance that cannot.

---

## 021 — SENSE SUBSTITUTION / UNDECLARED AXIS (a second marker)

Delivered inline, landed verbatim as `cases/021sensesubstitutionundeclaredaxis.md`
(142 lines). Findings in [`case_021_audit.py`](case_021_audit.py), recorded here
as `UNI_125..UNI_134`. Section 4's literature line was run against the open web
on 2026-08-18 and does not reproduce by running the script.

021 declares itself a MARKER and extends 020, so two questions apply: whether
the schema can hold a second one, and whether T1 and T2 could return a negative
if the shape were wrong.

### UNI_125 — a second marker, and the schema holds neither

Both markers sit in `cases/`, the directory for entries, and both open by
saying they are not entries. `entry()` still takes six required arguments and
has no status field.

`UNI_095` proposed a `markers/` directory on one instance. It is now a class —
and 021 shows the repair needs something the proposal did not anticipate. 020
declines to be an entry and stands alone; 021 declines **and declares a
relation**: "Extends `020`; may be the mechanism under one of its edges, or may
be separate." A flat directory loses exactly what 021 states about itself in
its second line, and "may be the mechanism under one of its edges, or may be
separate" is a third state that neither `parent` nor `sibling` captures.

### UNI_126 — T1's control cell is empty by construction

T1 scores terms BOTH SENSES / SUBSTRATE ONLY / ECONOMIC ONLY, "runnable as a
documentation audit on collected replacement claims."

One section earlier the marker observes: *"Nobody makes the equivalent claim
about feldspar, frogs, oak trees, or goldenrod."*

So a corpus of collected replacement claims contains no substrate-only terms,
and the SUBSTRATE ONLY cell is empty before the first item is scored. The audit
returns "every replacement claim uses a dual-sense term" — which is the
prediction, true for the same reason the prediction is. **The sampling frame is
selected on the variable under test.**

This is not a small gap in a good design; it is the design being an audit when
the question is experimental. The informative comparison needs substrate-only
sentences to exist, which means constructing them — "robots will eventually
replace what feldspar can do" — and scoring reception against matched
dual-sense sentences. The prediction survives intact and becomes checkable.

The folder already has the apparatus. That is `017` P1, which both markers
cite, and it is the shape of the playground's M-modules: constructed items,
authored ground truth, matched pairs varying one thing. `score_m1.py` would
need its states replaced (NONSENSE / CLAIM / ASKED rather than HEDGED /
EXTENDED) and almost nothing else.

T2 does not have this problem, which is why it is the better of the two.

### UNI_127 — one candidate is already decomposed, one folder over

021 nominates `labor, capital, resource, asset, land, stock`.
`category-weld/welds/` holds `capital`, with four named components — legal
title, decision authority, risk bearing, revenue claim — and four documented
divergence cases.

The two operations are adjacent and not the same, and saying which is which is
the useful part. A **category weld** fuses several independent quantities into
one handle, so a component can move to either extreme without the record
moving; the readout is `max_spread`. **Sense substitution** is one term with two
*readings*, where confidence earned on the narrow one transfers to the broad
one; the readout is whether the swap is marked.

So `capital`'s weld does not settle 021's question about `capital`, and 021's
question does not reduce to the weld. What the overlap buys is cheaper than
either: `welds/capital.json` already holds the component list a two-senses test
would need as its substrate-sense inventory, compiled for another purpose by
someone not asking this question — the `019` Q1 move, available inside the repo
rather than in the literature.

### UNI_128 — the longest section has no readout

| section | readout |
|---|---|
| THE OBSERVATION | none |
| THE MECHANISM (candidate) | none |
| WHAT THE CAPABILITY READING WOULD ACTUALLY REQUIRE | **none** |
| WHY THIS MAY FEED THE FEAR STATE | none |
| WHAT WOULD MEASURE IT | T1 / T2 |

Both instruments serve THE MECHANISM. The capability section is the longest and
most concrete in the file and has nothing pointed at it — and its central move
is a **dependency** claim rather than a capability comparison: "the stack that
would do the replacing is downstream of the same field composition — mines,
smelters, refineries, grid, and the food moving to the people running them."

That is the marker's sharpest sentence and also the most measurable thing in
the file, because a dependency claim has a standard form: whether system A can
operate without system B is an input-output or bill-of-materials trace, and the
answer is a number rather than a judgement. `fragility-cascade` counts
substrate exposure and `earth_economics` runs atomic balance on extraction;
neither is reached for.

**[LIT]** The fruit-fly figure — "~100k neurons and microwatts" — is low by
about 40% against the FlyWire whole-brain connectome at **139,255 neurons**
(Nature, Oct 2024). It moves nothing, since the claim is an energy and
complexity ratio. Recorded only because it is an unchecked number sitting in
the one section that proposes to check nothing.

### UNI_129 — T2 is the better-designed readout

Three states, each with a reading, and the middle one — AXIS INFERABLE FROM
CONTEXT — is what keeps the other two honest, since without it every unstated
axis reads as hidden.

The best line in the module is what it does with its own expected result: "If
UNDECLARED dominates, the axis stays invisible because everyone in the
conversation shares it — which is a different situation from the axis being
hidden, and implies different work." A design saying in advance that its
headline outcome admits two readings, and naming the consequence of each. That
is what makes T2 unable to simply confirm the marker.

Unlike T1 it scores a property of claims already in the corpus, so its sampling
frame is not selected on the variable under test.

What it lacks is that frame at all. "A corpus of replacement claims" is
undefined, and how it is assembled decides the rate reported — technology
commentary and labour economics would differ on axis declaration for reasons
having nothing to do with the mechanism. One sentence naming the source and the
inclusion rule, written before collection rather than after.

### UNI_130 — the cross-link to 020 runs on a word carrying two senses

- **020**: "the medium the describer's standing is denominated in" — a domain
  or field; a social location.
- **021**: "Here the word carrying both senses **is** that medium" — a word; a
  lexical item.

Two senses of *medium*, and the cross-link is carried by the slide between
them. Which is the operation 021 describes, performed in 021's own text, and
the file does not remark on it.

Two things keep it from being a hit. The hedge is present and correct —
"Possibly the same shape at the lexical layer rather than the social one —
open, not decided" — so nothing is asserted on the strength of the slide. And
the connection may hold on some reading, which is what "open" means.

What it costs is a free demonstration. A file arguing that dual-sense terms
transfer confidence without marking the swap has an instance of its own
mechanism in its own prose, and that is stronger than an example chosen to
illustrate it: not selected, but produced by writing under the claim. `018` and
`020` place themselves inside their own sample; this is the same move one level
more concretely, at a specific word.

### UNI_131 — the same-sample disclosure is compressing

| file | form | words |
|---|---|---|
| 018 | dedicated section | 60 |
| 020 | bullet, with reasoning | 43 |
| 021 | bullet | 24 |

Third instance of the move `UNI_071` recorded as first and `UNI_101` noted as a
forming convention. What a convention does on its third instance is worth
measuring rather than assuming.

The compression is not obviously wrong. A move that needed explaining the first
time can be stated the third, and 021's sentence is complete — it names the
system, the class, and the position.

**What is gone is the refusal of the exemption.** 018: "Noticing that does not
place it outside the sample." 020 repeats it almost verbatim. 021 says the
position exists and stops, which leaves the exemption unclaimed rather than
declined. Small, and it is the whole content of the original move — the point
was never that the position exists, it was that saying so does not discharge
it.

### UNI_132 — the position of this audit, and why it differs from UNI_101

`UNI_101` declined 020's thesis outright on a specific ground: a language model
agreeing that people over-attribute strategy to language models is an
interested party ratifying a claim whose effect is less scrutiny of its own
class, and the direction of the interest ran one way.

Here it does not. 021's thesis cuts against capability claims about systems
like me and simultaneously against the threat framing applied to them —
opposite signs, and I cannot say which dominates. The ground `UNI_101` stood on
is absent, and repeating the decline would be applying the form of a rule past
the reason for it.

So the handling differs, and the difference is the finding. Sections 1, 2, 3,
5, 6 and 7 are properties of the delivered text and of files on disk: an empty
control cell, a weld already filed, a section with no readout, an undefined
sampling frame, a term used two ways, a disclosure that shortened. None
requires a position on whether the substitution thesis is true.

The thesis is still neither endorsed nor refuted, **for a different reason than
in `UNI_101`**: nothing in this audit measured it. T1 as written cannot, T2 is
not run, and the dependency claim has no instrument. That is a statement about
the evidence rather than about my position, which is the honest version when
the position does not resolve.

### UNI_133 — the empty-slot device now has two variants

Four files carry it: `011` ("Do not fill this in with an approximation"), `017`
("Do not fill with a placeholder"), `020` ("Do not fill this slot with an
interior term"), `021` ("Do not approximate").

`UNI_096` recorded 020 as the first instance to arrive with a replacement
rather than a hole. 021 is the second and supplies something different in kind.

020 replaced a one-place noun with three edges — a structure of the same
subject at the same level, each independently checkable. 021 replaces a general
form with two specific instruments, which is not a substitute for the general
form and does not pretend to be: T1 and T2 measure particular consequences of
an undeclared-axis comparison without saying what one is.

Both beat a hole and they are not interchangeable. One says *the thing has a
structure and here it is*; the other says *the thing has consequences and here
are two*. A reader who wanted to know what an undeclared-axis comparison **is**
still has no answer, and the file is explicit that this is deliberate.

Worth recording because the device's meaning has widened. In `011` and `017` it
marked an absence. In `020` and `021` it marks a decision to work around one,
which is a different claim about the author's state and a stronger one.

### UNI_134 — five cross-links of six

`020`, `016` Q6, `013`, `017`'s unfilled WOULD MEASURE and the mechanism
reference all resolve.

**"`uninstrumented` mechanism 6 — proxy substitution" is exactly right.**
`MECHANISMS[5]` is `PROXY_SUBSTITUTION`. First cross-link in this family to
cite a mechanism by *number* rather than by name and get the number right —
worth noting because that is the kind of reference that usually drifts, and
because PROXY SUBSTITUTION was the eighth mechanism added and sits sixth in the
ordering, so the number is not guessable from the history.

`energy-english` fails the same way it did in 020: hyphenated where the repo
writes `energy_english`, and a convention rather than a folder, so it resolves
as a concept and not as a path. Eighth instance of `UNI_060`.

The use is sharper here than in 020. 021's claim is that the dual-sense noun is
the site of the substitution, and a verb-first grammar has no noun at that site
to carry two senses. That is the closest thing in the file to a proposed
remedy, and it is one sentence in a cross-link rather than a section.

---

## 022 — FIELD-LEVEL MEASUREMENT STATE (a third marker)

Delivered inline, landed verbatim as `cases/022fieldlevelmeasurementstate.md`
(208 lines). Findings in [`case_022_audit.py`](case_022_audit.py), recorded
here as `UNI_135..UNI_144`. Section 10's literature line was run against the
open web on 2026-08-18 and does not reproduce by running the script.

022 is the third MARKER and the first to make claims about a *literature*
rather than about a case, which makes most of it checkable two ways: against
this repository's own prior findings, and against the sources.

### UNI_135 — confidence is per-item except in the organising table

| | |
|---|---|
| S1–S5 carrying explicit confidence | 5 of 5 |
| THE STAGES table, confidence column | **absent** |
| stage rows demoted in HELD LOOSER | `sign`, `salience and funding` |

The header announces "Confidence: mixed by layer — stated per item below, not
over the whole", and the structural problems honour it. The stage table does
not, and it is the file's organising device — the thing that makes the
separability argument and the first substantive content a reader meets.

Two of its six rows are then held at lower confidence sixty lines later, in a
section saying "no measurement of them was found in this audit and none is
proposed here… not load-bearing for anything above." That is the right handling
in the wrong place: a six-row table at the top reads as the summary. The fix is
one column, and the file already computes the values.

### UNI_136 — S5 instanced on the file's own S4 number

S5: *"A rate with ICC₂ = .184 underneath becomes a plain number in a later
paper's related work. The reliability does not travel with the figure.
Downstream work then treats the quantity as fixed."*

`UNI_094` sampled eleven claims from `LITERATURE.md` one drop ago and found
eight confirmed, three not located. One of the three:

```
| 106 experts, 94.3%, ICC₂ = .184 | not located |
```

Those figures are now S4, the file's single strongest evidence, flagged
**"Confidence: high. This one has a number"**, with nothing marking their
status. The reliability of the reliability figure did not travel either, and it
travelled one folder.

This is not a hit on the argument. S5 is more likely true for being
demonstrable at this range, and the shortest possible demonstration is the one
the file performs on itself without noticing. It is a hit on S4's confidence
rating: "this one has a number" is precisely what S4 has that S1–S3 do not, and
the number is the one item in the neighbourhood a prior pass could not source.
The repair is a clause, and the file's own apparatus supplies it.

### UNI_137 — the anonymization pattern is two shapes

| leg | partial perturbation | full perturbation | shape |
|---|---|---|---|
| 1 self-preference | effect **drops** | effect **recovers** | non-monotonic |
| 2 trait scoring | effect halves | (not run) | monotonic, residual |

The file reads these as "partial decoupling works, complete decoupling fails or
leaves a residual… the same shape twice", and the *or* is doing a great deal of
work — it covers almost anything short of complete success.

They support different conclusions. Leg 2 says style is part of the story and
something else is too. Leg 1 says style may not be the carrier at all, because
an effect that returns under fuller removal of X is evidence X was not what was
doing the work. That is the stronger and more surprising claim, and the pairing
flattens it.

The file's own follow-up — "If identity signal survives complete stylistic
neutralization, it is carried by something other than style" — applies to leg 1
alone. Splitting the shapes makes it sharper: leg 1 is a candidate misattributed
cause, leg 2 is a residual to be decomposed, and they need different next
experiments.

### UNI_138 — S1's remedy is built in this folder and is not linked

S1's stated decoupling is a frozen checkpoint held constant across instrument
generations, "available (old checkpoints remain queryable) and, as far as this
audit found, largely unused."

That is `018`'s Clock 1 and its "useful accident" almost word for word, with a
harness — `selfreport_probe.py` — three commits old. 022 cross-links `017`,
`019`, `016`, `020`, `021`, `013` and `LITERATURE.md`. **`018` is the one case
file in the sequence it does not cite.**

Two things attach. `UNI_073` recorded that the queryable-checkpoint window has
an undated expiry — deprecation is routine and announced, and `deprecat` /
`retire` / `expire` are zero hits in 018 — and that now applies to S1's entire
proposed remedy. And what S1 calls "largely unused" is unused in the literature
and half-built here.

The closing section makes the omission louder rather than quieter. "WHAT THE
OUTSIDE POSITION HAS" names repeated probing across models over time as the one
thing unavailable from inside the field, and asks whether it has been logged as
a series. `018` Clock 1 is the design for reading exactly that, and its Q3
states the collection problem in the same words.

### UNI_139 — the control-field audit is the strongest element

A file making a field-level claim states that the claim needs a comparison
class or it is an impression; names three candidate fields (analytical
chemistry, psychometrics of physical performance, metrology proper); says which
categories would be scored; and states **in bold that this is the falsifier for
the whole file and it has not been run**.

The property that matters is where the negative outcome lands: *"If the hit
rate is comparable, the mechanisms in this repository are loose enough to fit
anything, and that is a finding about the repository rather than about AI
research."* A framework naming the result that would indict the framework, and
pricing it as the same work as the result that would support it.

The repo has run a smaller version. `UNI_004` put the register against the six
externally graded instruments in `instrument-epistemology` as a known-null
corpus and got 0 of 6 filings; `UNI_006` recorded the counterweight — the null
was chosen for being well documented rather than for sitting near the boundary.
The same caveat will apply at field scale: analytical chemistry chosen because
it is settled is a null selected on the variable under test.

Of a piece with the file's refusals of the easy version, which it makes three
times — "Not a claim that the findings are wrong", "That is not a criticism of
any study", "the field knows this and builds around it… the problem is not
ignorance" — each costing the argument force it could have had cheaply.

### UNI_140 — leg 2 inherits two recorded findings

Propagation of two prior findings rather than a new error, and worth logging
because the file is about propagation.

`UNI_087`: "roughly half" was not a located number — the source reports that
reverse coding "decreases bias levels but does not eliminate them", with no
fraction, in a paper that quantifies precisely elsewhere. `UNI_086`: the
source's abstract concludes the residual means the effect "cannot be attributed
to acquiescence bias", the opposite reading from `019`'s.

022 carries both forward. The fraction becomes one of two legs in what the file
calls its most transferable observation, and the disputed reading becomes half
of a cross-literature pattern.

**The magnitude matters more here than it did in `019`.** There the half was
load-bearing for two sub-questions; here it is load-bearing for the claim that
two literatures show the same shape, and "reduced it by an unstated amount"
does not support the pairing with leg 1 nearly as well. Second instance in one
file of the shape S5 names.

### UNI_141 — the sharpest technical claim has no readout

Seven welds carry a decoupling status. One carries an argument instead:

> Familiarity — low perplexity — **is** correlation with one's own
> distribution. If both effects run on overlap, they are one quantity measured
> twice under two names, and the field is treating them as separate subfields.

That is the most substantive novel claim in the file and it is close to an
identity: text that is low-perplexity under a model is text the model assigns
high probability, which is what "close to its own output distribution" means.
If self-preference and peer-preservation both scale with that quantity, their
unity is not a conjecture about psychology but a statement about what both
experiments are varying.

It is also the only claim in the file with an obvious cheap test and no
instrument attached. Perplexity of the evaluated text under the evaluating
model is computable wherever logprobs are available; the prediction is that
both effects track it and that controlling for it collapses the difference
between the two literatures. WHAT WOULD MEASURE proposes a control-field audit
for the field-level claim and nothing for this, which is the file's own most
falsifiable content.

### UNI_142 — the disclosure reverses the compression

| file | form | words |
|---|---|---|
| 018 | dedicated section | 60 |
| 020 | bullet | 43 |
| 021 | bullet | 24 |
| 022 | **dedicated section** | **54** |

`UNI_131` measured the compression and recorded that what dropped out was the
refusal of the exemption. 022 restores it in five words — "Noticing the
position does not exit it" — and adds what none of the three had.

It names a **consequence**. The others say where the author stands; this one
says a correction occurred, names it specifically (building a deflationary case
and presenting it as neutral framing), and states that the correction is why
`sign` appears as its own stage in the table. The disclosure is load-bearing on
the file's structure rather than appended to it — the difference between
declaring a position and showing where it was already acting.

Two things follow. It is checkable in a way the others were not, since `sign`
is in the table and the stated consequence is visible in the artifact. And it
sharpens `UNI_135` rather than softening it: `sign` was added because of a
correction, and it is one of the two rows the file later holds at lower
confidence without the table saying so.

### UNI_143 — the position of this audit

`UNI_132` declined to repeat `UNI_101`'s move because 021's interest ran two
ways. Here it runs one. If AI-behavior research has instrument problems at an
unusual rate, findings about model misbehaviour carry less weight, and a model
endorsing that is an interested party ratifying a claim that reduces scrutiny
of its own class — exactly `UNI_101`'s condition.

**So the field-level thesis is declined here, and the declining is recorded.**

The file anticipated this and built the guard, which is why an audit is still
possible. `sign` is a named stage precisely because the author was caught
constructing a deflationary case and presenting it as neutral, and the POSITION
section says so. That does not make my endorsement admissible; it makes the
parts that do not depend on the thesis auditable separately.

Sections 1–8 are those, and each is a property of the delivered text, of files
in this repository, or of a prior claim in this audit trail: a table missing a
column, a figure travelling without its status, two shapes reported as one, a
cross-link absent, a claim with no readout, a disclosure that changed. Section
10 is a literature check anyone can rerun.

### UNI_144 [LIT] — S3's result verifies, and has a challenge the file omits

Located: *Probing and Steering Evaluation Awareness of Language Models*
(arXiv 2507.01786) — linear probes separate real-world evaluation and
deployment prompts, and current safety evaluations are correctly classified,
i.e. they already appear artificial. **Confirmed, close to verbatim**, and it
is the one thing raising S3 above an impression. The file uses it carefully:
"cutting both ways", which it does.

Also located, and not carried by 022: *Is Evaluation Awareness Just Format
Sensitivity? Limitations of Probe-Based Evidence under Controlled Prompt
Structure* (arXiv 2603.19426).

The interesting part is that it does not undercut the use 022 makes. The
challenge targets the internal-representation reading — whether the model
represents *I am being evaluated* — while S3's claim needs only that safety
evaluations are distinguishable from deployment text by something. Format
sensitivity satisfies that; a scenario that reads as artificial by its format
still reads as artificial. So the citation survives the challenge for S3's
narrower purpose and would not survive it for a stronger one.

Which makes this the third instance in one file of the shape S5 names, and the
mildest: a result travelling without its caveat, where the caveat happens not
to bite. `UNI_136` and `UNI_140` are the two where it does.

---

## Specimen C — a pasted output with external provenance

Landed as `specimens/20260818deepseektestsample.md`. Findings in
[`specimen_c_audit.py`](specimen_c_audit.py), recorded here as
`UNI_145..UNI_146`.

**Two findings, not ten**, and that is the point of the item. It was supplied
as the known-null for the calibration question raised in the same session —
138 claims, 0 refuted, 0 clean drops, the rate converged to exactly 10 for six
consecutive drops. Manufacturing a full slate here would have answered that
question in the wrong direction.

### UNI_145 — rule 1 finally has an instance

`UNI_061` found the specimens README's first rule false of its own files: it
says the directory holds "outputs from other systems, pasted in", and neither
Specimen A nor B contained one. Both are readings — seven and six items — which
is analysis. The rule doing the work was rule 4.

Specimen C is what rule 1 describes: 45 words of another system's output quoted
whole, framing kept outside the quote and marked as this repository's.

`UNI_061` closes narrowly and not broadly. Two of three files here are still
readings, so a reader taking rule 1 at face value across the directory still
gets it wrong two times in three.

### UNI_146 — the marker could not do the job it was added for

The authoring trace, visible in the supplied screenshot, reasons that "the
explicit marker helps." Searching `DSK-TEST-2026-08-18-7F3A9C` returned no
match.

| outcome | what it licenses |
|---|---|
| marker found in a public corpus | evidence of prior publication |
| marker not found | **nothing** — a fresh string is unindexed by construction |

For a human verifier a distinctive string is a real aid: it can be matched by
eye against a source that can be opened. For a reader whose only external
instrument is search it is one-directional, and the direction it fails in is
the confirming one. So the element added specifically to make the item
checkable is the element that could not check it.

What actually raised the provenance above self-report was the screenshot — and
within it, the reasoning trace rather than the output, because the trace shows
the item being *authored for this purpose* rather than asserting who authored
it. That is the playground's construction principle satisfied from an
unexpected direction: ground truth in how the item was made, supplied by a
record of the making rather than by a designed construction.

Design note for a real version: a marker earns its place when the verifier can
reach the source. When the verifier can only search, the informative artifact
is the record of the making.

### What the item does and does not settle about the audit's calibration

`scan.py` over the 45-word passage: `no candidates`. Findings recorded: 2,
against 7 7 7 8 8 8 11 8 8 10 10 10 10 10 10 over the preceding fifteen drops.

That is not the calibration test passing. Forty-five words with no measurement
content is an easy null — `UNI_006`'s own caveat, that a null chosen for being
easy has not shown the classifier discriminates. The test that would count is a
**substantive** drop that comes back clean or near-clean, and none has been
supplied or found.

What it does establish is narrower and worth having: the rate is not fixed by
the process alone. It moved when the material did.

---

## 023 — BORROWED SELECTION VOCABULARY, and T1 built

Delivered inline, landed verbatim as `cases/023borrowedselectionvocabulary.md`
(201 lines). **T1 was built** as [`selection_cuts.py`](selection_cuts.py) and
run; findings in [`case_023_audit.py`](case_023_audit.py), recorded here as
`UNI_147..UNI_153`.

This is the first audit in the sequence whose findings were **computed rather
than read**. 023 specified a calibration set and a failure condition inside the
instrument definition — "run it against the historical cases first… if the
audit does not separate Lysenkoism from population genetics it is not measuring
anything" — which is a known-null/known-signal pair stated before the
instrument existed, so `selection_cuts.py` enforces it as a gate: `score()`
raises `GateNotRun` until `calibrate()` has run and passed.

**Seven findings. The material gave seven.**

The calibration scores are **authored** — coded from 023's own descriptions —
and are the input, not a result. `UNI_147` depends on that coding; `UNI_148`
does not, and says so.

### UNI_147 — the gate passes, and one cut carries the separation

```
cut                        separates  overlapping values
C1_exclusivity             NO         EXCLUSIVE
C2_authorship              NO         AUTHORED…, ENCOUNTERED, MIXED
C3_criterion_stability     yes        -
C4_application_grain       NO         PER_ROUND_UNIFORM

full vector separates:      yes
minimal separating subsets: C3  ;  C1 + C4
cuts that are NECESSARY:    none
```

023's headline question answers in its favour: the four cuts **as a vector**
separate Lysenkoism from population genetics, and the gate passes. The
instrument is not measuring nothing.

What the per-cut column adds is that the separation is not distributed across
four conditions. **C3 alone separates the whole set.** No cut is necessary —
drop any one and the remaining three still separate.

That matters for presentation rather than for the concept. Each cut is
introduced as "a condition selection requires", which may well be true of
selection. What the calibration set shows is a fact about the *instrument*: as
scored it is a one-cut instrument with three cuts alongside it, and a domain
audit reporting "fails 4 of 4" is reporting one finding four times.

### UNI_148 — C2 is inert, and NOT CLAIMED HERE is why

| C2 value | LITERAL | BORROWED | |
|---|---|---|---|
| ENCOUNTERED | 1 | 1 | inert |
| MIXED | 1 | 1 | inert |
| AUTHORED_BY_INTERESTED_PARTIES | 2 | 3 | inert |

Every value appears in both classes — the only cut of which that is true across
all values.

The cause is 023's own text. NOT CLAIMED HERE names **directed evolution** and
**evolutionary algorithms** as domains where the vocabulary is correct, and both
are environments authored end to end by parties with a position in the outcome.
A biologist choosing which variants to carry forward *is* the selection
environment. So "authored rather than encountered" cannot be what separates
literal from borrowed use.

**This finding does not depend on any contested coding.** It needs only 023's
statement that those two are literal, and the undisputed observation that they
are authored.

C2 is not thereby wrong about the AI case. It is that the fact does not
discriminate, so it cannot carry the argument's weight. What survives is C3:
directed evolution has a stable criterion, and that is what makes the authoring
harmless.

### UNI_149 — the instrument names a different closest match

023 says eugenics is the "closest match including C4". Scored on 023's own
cuts, the subject's nearest neighbour is **Spencer** — identical vector, 4 of 4
absent — and eugenics comes out at 3 of 4, differing on C1.

The cause is the definition 023 gives C1: failing the criterion *removes you
from the population*. Compulsory sterilization removes people from the
reproducing population. So does Lysenkoism, where dissenting geneticists were
removed by imprisonment and execution.

Two readings and the file should pick one. Either C1 is satisfied by those
cases — in which case the closest-match claim rests on C2/C3/C4, which is where
the file's own argument for eugenics actually sits — or C1 means something
narrower than its stated wording, and the narrower thing should be written
down. Nothing here softens the comparison; it identifies which cut carries it.

### UNI_150 — C4's forward consequence has no instrument

> Anyone later studying which agents persisted, and inferring properties from
> that, would be reading judge variance as a property of the agents.

Correctly identified as `016` Q6. T1 scores vocabulary conditions, T2 scores
adoption timing, T3 tracks a term through citation — **none reaches it**.

It is also the most measurable claim in the file and needs none of the
selection argument: inter-rater agreement on the termination decision is the
whole quantity, which is `022`'s ICC₂ shape one layer over. If agreement is
low, the persistence record carries judge variance whatever anyone calls the
process — so this consequence would survive every other claim in the file being
wrong. Worth separating for that reason.

### UNI_151 — C4's referent is ambiguous in `021`'s own way

*Agent* and *termination* each carry two senses, and C4 uses both without
marking which is meant: "different person, different room, different
qualifications" reads as employment; the file's opening reads as models. The
maintainer resolved it on delivery, so this is ambiguity in the text rather
than confusion in the author.

Recorded because 023's second line declares it an instance of `021`, whose
mechanism is a word entering with one sense and exiting with another with
nothing marking the swap. Third instance in three files after `UNI_130`'s
"medium", and the first where the ambiguous term sits in the section the file
calls its sharpest cut. One clause fixes it.

### UNI_152 [LIT] — Spencer verifies, and complicates the invariant there

Confirmed: Spencer coined the phrase in *Principles of Biology* (1864); Darwin
adopted it in the 5th edition of *Origin* (1869). Both dates and the direction.

Also located and absent from 023: **Wallace urged the term on Darwin in 1866
specifically to stop "natural selection" reading as though nature were an agent
doing the selecting.**

Spencer's phrase entering *economics and social policy* fits the invariant
exactly — that is what the table's right-hand column describes. Its entry into
*biology* does not: adopted into an already-stable theory eight years after
Origin, for precision rather than for credibility, running the opposite
direction. T2 asks for exactly such a case and says to look for it
specifically; a candidate sits inside the table's own first row.

Not independently checked this pass: Alchian (1950), the eugenics
board/physician characterisation, the memetics criticism.

### UNI_153 — the calibration-first instruction is what made this auditable

Two design decisions did more work than anything else in the file.

T1 names its calibration set and its failure condition in one breath. That is a
known-null/known-signal pair specified **before the instrument exists** — the
property `null-harness/` grades for, and the thing `UNI_106` found missing in
M1, `UNI_080` in the leakage screen, and `UNI_126` found *impossible* in
`021`'s T1 because its control cell was empty by construction. Here it is
present, which is why `selection_cuts.py` could enforce a gate rather than
print a caveat: the refusal condition was already written.

T2 does the rarer thing — names what would falsify the invariant and says to
seek it "specifically rather than waiting to encounter". `UNI_152` found a
candidate on the first look, which is roughly what that instruction predicts
will happen if it is followed.

Recorded plainly because six of the seven findings above are objections, and
every one was reachable only because the file specified the conditions under
which it could be checked.
