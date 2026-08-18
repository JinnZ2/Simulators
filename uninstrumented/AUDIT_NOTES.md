# AUDIT_NOTES — uninstrumented

Everything below is added analysis. The delivered files are
[`README.md`](README.md), [`patterns.json`](patterns.json) and
[`scan.py`](scan.py), all verbatim. Added here:
[`uninstrumented.py`](uninstrumented.py) (the register as code, three
checks on itself), [`scan_audit.py`](scan_audit.py) (grades the scanner),
[`case_010_audit.py`](case_010_audit.py) and
[`case_011_audit.py`](case_011_audit.py) (checks on the two delivered
cases) and [`CLAIM_TABLE.md`](CLAIM_TABLE.md). `cases/case-010.md` and
`cases/case-011.md` are delivered, verbatim.

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
