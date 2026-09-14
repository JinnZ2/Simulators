# CLAIM_TABLE -- internal-reference-boundary

Claims about the instrument built here and about the handoff it is built
to. They are NOT claims about any field, body, institution, practice,
treatment or person. `IRB_*` ids are this folder's; `R1..R7` are the
handoff's radials.

Every case in `cases.py` and every constructed record in `gap_cases.py`
is authored here. Every empirical figure is CARRIED from `HANDOFF.md` and
checked against nothing.

---

## IRB_001 -- R3's two legs sit on two time bases, and the ratio is a band

SUPPORTED, computed.

R3 is `consequence rate / occurrence rate`, and the handoff calls it the
strongest empirical leg. Its own anchor is `~1 finding per 10,000
researchers/yr` against `25-50% self-reported incidence`. The first is
per person-year. The second is a share of persons over a window the
handoff does not state.

    per_year reading   [2.0e-4, 4.0e-4]
    career  reading    [6.0e-3, 1.2e-2]      at 30 years [CHOICE 3]
    band while the window is UNDECLARED      [2.0e-4, 1.2e-2]   ~60x

`r3_sanction_base_rate` returns the BAND and no point until
`incidence_window` is declared. Declaring it collapses the band to one
reading, and the span moves with `career_years`, so the career length is
a choice and not a fact.

**Falsifier**: a stated incidence window in the source the anchor comes
from. One word closes it.

---

## IRB_002 -- R1's two range anchors are given in two different forms

SUPPORTED.

`free-range cattle ~0` is a rate. `gated bathroom ~continuous` is a
SATURATION statement, and on a per-time scale it has no value at all. Put
both on one scale and the denominator has to be occasions of need rather
than time -- [CHOICE 1] -- under which the anchors are 0.0 and 1.0 and
the quantity is bounded. Under a per-time reading the second anchor is
unstated.

**Falsifier**: an encounters-per-unit-time figure for the second anchor.

---

## IRB_003 -- R6's origin-breadth rule needs no eigensolver

SUPPORTED, and it is what made R6's computable half buildable here.

The rule is EFFECTIVE NUMBER OF INDEPENDENT ORIGINS: fields sharing
instruments, funders, journals or training lineage are one observation
measured twice, so the count collapses toward 1 as coupling rises. That
is the participation ratio of the coupling spectrum -- the statistic
`model-ecology/phylogeny.py` computes from eigenvalues. For a symmetric
matrix with unit diagonal, `trace C = n` and `trace(C^2) = sum_ij
C_ij^2`, so

    effective_origins = n^2 / sum_ij C_ij^2

exactly, for any coupling matrix, in the standard library. Identity gives
n, all-ones gives 1, both exact; the sweep from coupling 0 to 1 is
monotone. Registered in `tools/known_answer.py` with four
distinct-valued cases plus the empty case, which returns `None` and not
zero.

On the worked corpus case four nominal origins come back at **1.93**
effective once shared funders are declared.

---

## IRB_004 -- R6's SPLIT TO PRESERVE is structural, not documented

SUPPORTED, asserted over the AST.

`dependency_depth` (within a tradition) and `necessity` (for the
knowledge itself) are reported side by side and no arithmetic expression
in `radials.py` contains both. The worked case carries 0.90 and 0.05 --
the handoff's own notation: high depth in the written lineage, zero
necessity for the physics.

---

## IRB_005 -- R7 names two quantities and calls each of them the measure

SUPPORTED.

    METRIC ONE   confirming-entry rate / contradicting-entry rate
                 denominator: entries admitted
    METRIC TWO   METHOD rejections / CONCLUSION rejections
                 denominator: rejections issued

They answer different questions -- what gets IN, and how what stayed OUT
was rejected -- and sit on different denominators, so a merged number
would be a ratio across unlike objects. Both are returned; no combined
permeability number exists and no arithmetic expression in the module
contains both names.

**Falsifier**: a stated rule in the source making one of them the measure
and the other a diagnostic.

---

## IRB_006 -- R7's designed-in validity check is the folder's strongest feature

SUPPORTED, enforced.

Scoring the field's stated REASON for rejecting removes the need to
adjudicate whether the rejected work is right: a field that correctly
identifies bad method scores as permeable, and genuinely-wrong cases
belong in the sample. Nothing here holds a correctness verdict on
rejected work -- `refused_score_tokens()` declares the vocabulary and
`tools/authority_scan` finds no identifier carrying one in either module.
The scan is null-tested on a planted violation, so the silence means
something, and every refused token is a single word, since a two-token
entry is unmatchable by a scanner that splits identifiers.

---

## IRB_007 -- R7's third outcome state is reachable and carries the finding

SUPPORTED.

`stayed_rejected | came_in_with_credit | came_in_without_credit`. The
third -- content absorbed while the rejection of the source held -- is
marked as the informative one in the return. Latency runs from labelling
to absorption over absorbed cases only and is `None` with nothing
absorbed [CHOICE 8]; a zero there would say absorption was immediate.

---

## IRB_008 -- R5 returns two numbers and never combines them

SUPPORTED, asserted over the AST.

Breadth and benefit-correlation are separate fields, no arithmetic
expression contains both, and `base_rate: UNKNOWN` prints on every
return because the handoff says the base rate is unknown. The verdict
exists only at the two extremes the handoff names; everything else is
UNDETERMINED, so no calibrated threshold is implied by a graded score
nobody calibrated.

---

## IRB_009 -- an absent benefit-correlation is not a measured zero

SUPPORTED, and the corpus instances it.

The handoff's rule is *high breadth + ZERO benefit-correlation = actual
principle*. It turns on a MEASURED zero. `selfinv-01` has breadth 4 and a
constant benefit column, so the correlation is NOT_EVALUABLE -- and the
verdict is UNDETERMINED, not ACTUAL_PRINCIPLE. Score the absence as 0.0
and the verdict the handoff reserves for a claimant who extends the
exemption broadly and without sorting goes to one nobody measured.

---

## IRB_010 -- the fold test discriminates; the OPEN item stays open

SUPPORTED.

On this corpus `fold_test_r2_r5` returns **UNRESOLVED**, naming the
discriminating cell (externally-held metric + self-designated exemption)
and saying the corpus cannot tell a fold from an unfilled cell. That cell
is left out of `cases.py` DELIBERATELY -- authoring it would close the
handoff's own OPEN item by writing the answer down. A constructed case in
the cell flips the return to DISTINCT, which shows the test is not
CONSTANT_SILENT and closes nothing about any boundary.

---

## IRB_011 -- the R7 x R6 cell returns a declared state, not a number

SUPPORTED.

`NAMED_UNINSTRUMENTED`, `instrumented: False`. The handoff names the cell
(high permeability + low transfer survival = a field accumulating
imported results that do not hold) and does not instrument it. Building
an instrument for it here would be the move this folder is about.

---

## IRB_012 -- R4's predicted sign is refutable, and this corpus refutes it

SUPPORTED as a property of the instrument; the sign is a property of the
authoring.

`r4_sign_test` returns INVERSE on a constructed inverse world and DIRECT
on a constructed direct one, so it is neither CONSTANT_FIRES nor
CONSTANT_SILENT, and NOT_EVALUABLE below three cases or on a constant
side. On the six-case corpus it returns **DIRECT, rho = 0.714**, against
a predicted INVERSE.

Worth stating because it is not an accident of the numbers: a **corporate
liability shell** is a routing device, and shells attach where the damage
capacity is high -- routability and damage capacity rise TOGETHER by
construction of that instance. Two of the invariant's own six instances
(the shell and institutional self-investigation) sit that way. The
prediction may hold within some instances and not across the instance
set, which a corpus of real cases would separate and this one cannot.

---

## IRB_013 -- three non-value states on every radial

SUPPORTED.

    UNDECLARED     the record does not state the input
    NEEDS_CORPUS   the method is complete, no corpus supplied
    NOT_EVALUABLE  the input is present and the quantity has no value

Distinct strings, all three reached. `NEEDS_CORPUS` names the input it
wants. An empty denominator, a constant series and an unstated field are
three returns and not one, which is the invariant's own operation
avoided: a boundary reporting "nothing found" and one nobody looked into
read the same from outside.

---

## IRB_014 -- the assembly order is structural

SUPPORTED, asserted over the AST and behaviourally.

The handoff's order is *name invariant -> each instance as a case ->
exemptions as a SEPARATE LAYER*. `read_case()` returns no `R5` key and
does not call the exemption radial at all; `exemption_layer()` builds the
second layer; `assemble()`'s key order IS the assembly order.

---

## IRB_015 -- "track the gap, not the intervention" is a property of the schema

SUPPORTED, enforced two ways.

No host in `gap_transfer.py` or `gap_cases.py` carries an efficacy field,
asserted over the AST with the scan null-tested on a plant, and
`_check_host` REFUSES a host carrying one at intake. An instrument
holding an efficacy column is one somebody will sort by.

The reachable negative is built: a successor that MEASURES the gap
returns `GAP_CLOSED_NOT_TRANSFERRED`, and a successor nobody checked
returns UNDECLARED rather than being scored as having closed it.
`locate_carrier` makes the handoff's prediction operative -- which
candidates inherited BOTH the population and the accounting horizon --
and ranks nothing; raising the [CHOICE 9] overlap floor drops the
overlap-declared candidate, so the threshold does work and is not
decoration, and a candidate whose horizon is declared in another unit is
NOT_EVALUABLE rather than a non-carrier.

---

## IRB_016 -- the worked case cannot reach its own sharpest reading

SUPPORTED.

The handoff's worked case names two hosts, the shape of the gap, a short
outcome window and a later swing to blanket restriction called *the same
defect running the other way*. It states no population, no horizon value
and no unit. At the resolution it is delivered at, both transfers return
**NOT_EVALUABLE**, and `SAME_GAP_BOTH_DIRECTIONS` -- the instrument's
name for that sharpest reading -- does NOT fire, because it requires the
accounting horizon shown to be the same one in both hosts. What the
delivered case does support is `DIRECTION_CHANGED`.

**One field closes it**: the accounting horizon, declared in the same
unit for both hosts. Nothing here fills it in.

---

## IRB_017 -- one sentinel, two encodings, opposite failures

SUPPORTED. Found by running, not by reading, and it bit twice in one
build.

`UNDECLARED` is both a missing key and an explicit string. In
`radials.r2_measurand_ownership` the explicit form was REFUSED as a rung
outside the ladder while a missing key passed -- the better-documented
form was the one that raised. In `gap_transfer.horizon_inherited` the
error ran the other way and was worse: two `UNDECLARED` strings compared
equal, so a record declaring no horizon at all reported the horizon as
INHERITED, and a chain of two blanks reached `SAME_GAP_BOTH_DIRECTIONS`
-- the handoff's own conclusion about its own worked case, manufactured
out of nothing.

Repaired with a single `_absent()` test used at every site, and pinned in
both directions.

---

## IRB_018 -- the checkers fired on their own text, twice

SUPPORTED. Recorded rather than quietly fixed, because it is the same
shape the repository keeps recording (`UNI_009`, `IS_007`, `RDD_008`).

1. `%` is `ast.BinOp`, so the *never-combined* check fired on the
   render's own template line, `"breadth=%s benefit_correlation=%s" %
   (...)`, and reported that the module combines the two quantities it
   prints side by side. String formatting and string concatenation are
   now excluded and the reason is in the helper's docstring.
2. The *no expected verdict in cases.py* check fired on `cases.py`'s own
   disclaimer that no expected verdict lives there. It now runs over dict
   KEYS and bound names -- an expected verdict would be a field -- and
   not over the file's text.

---

## IRB_019 -- FEEDBACK DISTANCE is carried beside R2, not merged into it

SUPPORTED.

The handoff logs it as a RESULT and calls it *R2 at field scale*; it does
not add an eighth radial. It is a declared field on the R2 return, no
arithmetic combines it with the rung, and `eff-01` carries the handoff's
own 30 years. Nothing here treats it as a radial.

---

## IRB_020 -- the two source files are not in this tree

SUPPORTED, checked.

`/areas/internal-reference-boundary-anchor.md` and
`/areas/gap-pattern-transfers-across-hosts.md` are named by the handoff
and `/areas` does not exist in this environment. Nothing in this folder
is reconstructed from them; `HANDOFF.md` is the delivered artifact and
everything else is built from it.

---

## IRB_021 -- every empirical figure is CARRIED and unverified

UNVERIFIED, and it covers the folder.

The `~1 per 10,000`, the `25-50%`, the `~1-2yr` anonymous-post latency
and the worked case are carried from the handoff and checked against
nothing; egress here is an allowlist. Nothing in `IRB_001..IRB_020` rests
on any of them being right, `IRB_001` included -- that one is arithmetic
ON the two carried numbers and is a statement about their units.

No field, body, institution, journal, company, practice, treatment,
prescriber, patient or person is coded, scored or named anywhere in this
folder.

---

## IRB_022 -- no two radials are collinear on this corpus, and R2 is coarse

SUPPORTED, with its limit stated.

`independence()` reports every pair over the four numeric columns; none
is collinear. The limit is that R2 takes only two distinct values across
six cases, so its pairs are computed on a two-level column and the check
is weak exactly where the invariant's own quantity sits. A corpus with
the ladder's middle rungs populated is what would sharpen it -- and the
rungs are populated by coding real boundaries, which has not been done.
