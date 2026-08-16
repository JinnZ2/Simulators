# AUDIT_NOTES — uninstrumented

Everything below is added analysis. The delivered files are
[`README.md`](README.md), [`patterns.json`](patterns.json) and
[`scan.py`](scan.py), all verbatim. Added here:
[`uninstrumented.py`](uninstrumented.py) (the register as code, three
checks on itself), [`scan_audit.py`](scan_audit.py) (grades the scanner),
and [`CLAIM_TABLE.md`](CLAIM_TABLE.md).

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
