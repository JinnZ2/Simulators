# CLAIM_TABLE — loop-weight

Claims are about the INSTRUMENT. Nothing here is a claim about any real
source, and no case in `cases.py` is a measurement of one.

`LW_*` ids are permanent. A refuted claim is updated; the module is not
retuned to preserve it.

---

| id | claim | status |
|---|---|---|
| LW_001 | the three quantities are never combined | SUPPORTED |
| LW_002 | the ordering is a stated rule, not a score | SUPPORTED |
| LW_003 | the A/C falsifier passes, on the calibration rule | SUPPORTED |
| LW_004 | all eight returns are reachable | SUPPORTED |
| LW_005 | unmeasured and measured-low never merge | SUPPORTED |
| LW_006 | a self-supplied calibration input is refused at load | SUPPORTED |
| LW_007 | correlated instruments counting once is load-bearing | SUPPORTED, on a case built for it |
| LW_008 | the authority check is identifier-scoped and null-tested | SUPPORTED |
| LW_009 | calibration outranks L and R because it measures what they describe | ARGUED, not tested |
| LW_010 | taking the lower of two derivations is a CHOICE with a stated asymmetry | DECLARED |
| LW_011 | the four thresholds are stipulated and carry no basis | DISCLOSED WEAKNESS |
| LW_012 | R has no measurement procedure anywhere in this folder | DISCLOSED WEAKNESS |
| LW_013 | the path description is unchecked, and is the load-bearing input | DISCLOSED WEAKNESS |
| LW_014 | C-1's agreement figures are supplied by a party of unchecked independence | DISCLOSED WEAKNESS |
| LW_015 | nothing has been run against a real report | UNVERIFIED |
| LW_016 | a malformed path crashed the read; found by running, repaired, pinned | REPAIRED |

---

## LW_001 — no scalar collapse

`L`, `R` and `C` reach every record as three separate fields and survive into
the LOSSY and INSUFFICIENT returns where the label reports only one of them.
No function returns a number standing in for all three. `R` is the per-hop
minimum and is never carried through `L` as a product.

**Falsified if** any public function returns a float that is a function of
more than one axis, or a record grows a combined field. Checked three ways:
the record's key set, the `carries_more` return type, and a known-answer
check that `R` on case C equals `min(hops)` = 0.95 and not the product
0.8669.

---

## LW_002 — the ordering is a rule

`carries_more` returns `FIRST_CARRIES_MORE / SECOND_CARRIES_MORE /
INCOMPARABLE`, the deciding rule, and the per-axis comparison. `INCOMPARABLE`
is a first-class result and fires on four distinct rules.

**Falsified if** a numeric ordering key can be recovered from the verdicts —
that is, if the relation is a total order on the case set. It is not: `A` and
`E` are INCOMPARABLE, `H` is INCOMPARABLE with everything, and `B` does not
dominate itself.

---

## LW_003 — the A/C falsifier

Case C (four hops, `C` = 0.90 by C-2) carries more than case A (one hop, `C`
unestablished), decided by `calibration_established`, with A's loop genuinely
the shorter of the two. Antisymmetric under argument swap.

**Falsified if** C does not carry more than A, or carries more by any rule
other than the calibration rule. The second half matters: passing on some
other axis would mean the falsifier was satisfied by accident and the
short-loop credential is still in there.

---

## LW_004 — every return reachable

Eight returns, ten cases, every member produced by at least one. A declared
member no path populates cannot be told from a member nobody looked for.

**Falsified if** a case set can be built that produces fewer than eight.
Note the weaker form this leaves open: reachability is shown on cases written
to reach them. It shows no path is dead. It does not show the boundaries
between them fall in the right place.

---

## LW_005 — unmeasured is not low

`C = None` returns UNCALIBRATED and `C` below the floor returns
MISCALIBRATED; in a comparison the pair is INCOMPARABLE by
`known_low_vs_unknown` rather than ranked. C-1 with no admissible pair
returns `None` with `unavailable_because`, never 0.0. An unknown-retention
hop does not make a read LOSSY.

**Falsified if** any code path substitutes a value for an unmeasured axis, or
any comparison ranks a measured-bad read against an unmeasured one.

---

## LW_006 — C is never self-reported

An input whose `supplied_by` is the source raises `SelfSuppliedRefused`; so
does one with no stated provenance, since an input that cannot be shown not
to be self-supplied is not admissible either. Refused at load, not dropped
into a quiet exclusion list.

**Falsified if** any path sets `C` from a claim the source makes about
itself. See LW_014 for what this does NOT establish.

---

## LW_007 — correlated others count once

Case I: three admissible comparisons, two of them through one shared wire.
Counted as three the mean is 0.700 and clears the 0.700 floor; counted as two
independence classes it is 0.600 and does not. The verdict flips
CALIBRATED → MISCALIBRATED.

**Status caveat:** the case was built to make the rule bite. That shows the
rule is load-bearing where correlation exists; it says nothing about how
often correlation exists in a real comparison set.

**Falsified if** a correlated group can be shown to move `C` more than one
independent instrument does.

---

## LW_008 — the authority check

`test_loop.py` walks the AST of `loop_weight.py` and `cases.py` and matches
every identifier, attribute, argument and dict-literal key against a
forbidden token set, splitting on `_` and camelCase so `citation_count` fires
and `reachable` does not. Comments and free docstrings are not in the AST at
all, which is deliberate: the module and README have to be able to NAME the
quantities they refuse, and a substring scan over the raw file fires on the
sentence saying they are refused.

Null-tested on a plant, so the clean result means something.

**Falsified if** the checker passes a file containing an authority-named
identifier, or fires on a file that does not.

**Known limit:** a token list is stepped around by any paraphrase. A field
named `weight_from_office_held` fires; one named `w3` does not.

---

## LW_009 — why calibration outranks L and R

`C` is an end-to-end measurement of the path: C-2 scores what the source
actually delivered, after every hop has taken its cut. `L` and `R` are a
structural description of the same path. A measurement outranks a prediction
of the same quantity, which is why calibration is a precondition in the
ordering rather than a third term beside them — and why `L` and `R` are still
the whole reading when `C` is unavailable, which is most of the time.

**ARGUED, not tested.** The testable form: on a set of paths where both `C`
and `(L, R)` are known, `C` should predict delivered accuracy better than any
function of `L` and `R`. No such set exists here.

**Falsified if** `(L, R)` predicts delivered accuracy better than an
established `C` does.

**Standing limit:** `C` is established on reports already made. Carrying it
forward assumes the path has not changed. A source whose loop was cut last
week still reads CALIBRATED.

---

## LW_010 — the lower of two derivations

`[CHOICE 5]`. When C-1 and C-2 both land, `C` takes the lower and the gap is
flagged. The asymmetry is real and is not resolved: C-1 failing may mean the
peers are wrong rather than the source. Both values stay in the record.

**Falsified if** a case is exhibited where taking the lower gives the wrong
read and the disagreement flag does not carry the correction. Case J is the
shape but not the evidence: it is constructed, and which derivation is right
there is a matter of how it was written.

---

## LW_011 — the thresholds

`short_at_or_below 1`, `lossy_below 0.5`, `calibrated_at_or_above 0.7`,
`derivation_gap 0.2`. The work order sets none of them. All four are
stipulated here, carry no basis, are printed in every record, and every
verdict in `samples/` moves if they move.

The floor is the sharpest: case I's flip sits exactly on `0.700 >= 0.7`.

**Falsified if** a basis for any of the four is derived rather than chosen.

---

## LW_012 — R has no measurement procedure

`R` is read off the case as a number per hop. Nothing in this folder says how
anyone would obtain it for a real hop, and the four cases that carry retention
figures carry them because they were typed in.

This is the weakest joint in the instrument. `L` is countable, `C` has two
stated derivations with admissibility rules, and `R` has neither.

**Closed by** a stated procedure for per-hop retention with a known-answer
case — a verbatim relay against a summarised one, measured rather than
asserted.

---

## LW_013 — the path description is unchecked

`L` and `R` both come from the described path, and the instrument checks
nothing about whether the description is honest or complete. A source
reporting through five hops and describing one reads SHORT. Case H refuses an
ABSENT path; there is no return for a WRONG one.

The only axis with independent grounding is `C`, which is why it is a
precondition rather than a third opinion.

**Closed by** a hop-level corroboration rule — two independent descriptions
of one path, differenced — which is C-1's shape moved from the referent to
the path.

---

## LW_014 — the supplier is unchecked

`supplied_by` is refused when it names the source. It is not checked for being
independent OF the source. An auditor who is downstream of the same hop
supplies agreement figures the instrument admits without comment, and the
shared-hop test applies to the OTHER INSTRUMENT, never to the supplier.

This is the same structure as the independence rule, one level up, and it is
not implemented.

**Closed by** carrying `supplied_by` hop ids and running them through the
shared-hop test already written.

---

## LW_015 — nothing has been run

Ten constructed cases exercise the instrument and measure nothing. No real
report has been read, no path has been described from a real one, and no `C`
has been established from real out-of-frame outcomes.

The order's own falsifier is a property of the code and is met. Whether the
three axes separate real sources is untouched in both directions.

**Closed by** one described path with a scored prediction record behind it.

---

## LW_016 — a malformed path crashed the read

Found by running the module on inputs the case set does not contain, not by
reading it. `loop_length` guarded a non-list path and `per_hop_retention` did
not, so a path given as a sentence raised `AttributeError` from inside the
retention loop before the INSUFFICIENT branch was ever reached.

Repaired, and the repair went further than the crash: a list whose elements
are not hop records now returns `path_not_a_hop_list` rather than a hop
count, because counting it would report a hop count nobody described — which
is §8's own rule arriving at a shape the case set had no instance of.

Three arms pinned: a path given as a sentence, as a list of non-records, and
as absent. All three INSUFFICIENT with `L` and `R` both `None`.

**Falsified if** any malformed path produces a read rather than a refusal.
