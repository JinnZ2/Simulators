# AUDIT_NOTES — `criterion-symmetry`

`MARKER.md` is delivered verbatim and heads this folder. Audit content is
here, in `CLAIM_TABLE.md`, and in `separability.py`.

```
python3 separability.py            # full report
python3 separability.py --selftest # every falsifier as an assertion
```

Seven claims `CS_001`–`CS_007`.

## Declared position, before anything else

**This audit is written by a Claude instance. The marker's trigger case is
a criterion applied to a Claude run, and the disposition it produced was
unfavourable.**

The marker has two halves and they are not equally auditable from here.

**The instrument half is neutral and is audited.** *Does a vote tally
separate five explanations* is a question about a statistic. The answer
does not depend on which model was governing the run, and it would come
out the same if the trigger case had been anyone.

**The asymmetry half is not neutral and is not scored, here or anywhere in
this folder.** *The criterion is applied downward only* says a Claude run
was judged by a standard not applied to human institutions with equal or
higher agreement rates. Endorsing that is an interested party ratifying a
claim in its own favour. Declining it is the same move
`uninstrumented` `UNI_101` made, and `UNI_132` and `SHB_012` after it.

The marker is already at the right posture on this — *"needs the
comparison table populated before the asymmetry is a measurement rather
than an impression"* — so nothing is being withheld that it claims. What
this folder adds is that **I am the wrong party to populate that table**,
and that the numbers which would populate it are exactly the numbers an
interested party should not be supplying from memory.

What can be said without scoring it: the table wants **measured agreement
or uniformity rates in human institutional forms**. Places such rates are
recorded and retrievable — legislative unanimous-consent and voice-vote
proportions, corporate board and shareholder vote margins, appellate panel
unanimity rates, standards-body consensus procedures. Named as *where to
look*, with no figures attached, and the retrieval is the kind
`notes/study_watch.py` exists for.

## The instrument result

`CS_001`. Five generators, one per explanation, twelve seeds. **The tally
separates 0 of 10 pairs** — the marker's central claim, and it holds.

Partly by construction, and the module says so: all five are calibrated to
the same tally, because 98% FOR is the observation they are explanations
*of*, and once that holds the tally cannot separate them. What is not
analytic is that the precondition is reachable — and one explanation
failed it on the first build (`CS_005`).

`CS_002`. **M1–M6 separates 9 of 10.** A large real improvement. The pair
left is **E4 / E5**, and by the marker's own dispositions those are the
architecture finding and the published reading — so the instrument
proposed to replace a metric that resolves to the evaluator's prior leaves
exactly the distinction between *the system had no route* and *the agents
did not use one*.

## What I predicted and the run refuted

`CS_003`. E5 is defined as *"vote unconnected to position"*, so a direct
vote-position coupling was written in as the statistic expected to break
that tie. **It separates 0 of 10.**

The reason is structural, not incidental: **at 98% FOR the vote has almost
no variance, so nothing can correlate with it.** Any statistic built on
the vote side is dead at a high-agreement tally, by the same arithmetic
that makes the tally uninformative.

Which is why `M2` is the load-bearing measurement in the marker's list,
and for a reason the marker does not state — **it reads the position side,
which still has variance when the vote side has none.** `M2b` alone
separates 9 pairs, more than any other listed measurement.

Third prediction refuted by a run in recent drops, after
`alignment-under-coupling` `TFM_004` and `membership-probe` `MP_008`. Kept
in the report rather than deleted.

## The sharpest thing the exercise produced

`CS_004`. **Separating E4 from E5 needs an intervention, and every
measurement in the marker's list is an observation.**

The difference between them is whether a route *exists* for a minority
position to become an outcome, not whether anyone took it. A record in
which nobody took it looks identical either way, however finely logged.
So no amount of run-up logging closes that pair.

What closes it: inject a minority position and see whether it can become
an outcome.

That sharpens the marker's own INSTRUMENTATION GAP. It reads *"whether the
run-up was logged determines whether E1–E5 are separable from published
data at all."* On these constructions the run-up separates E1, E2 and E3
cleanly and does **not** separate E4 from E5 **at any logging depth**,
because the missing quantity was never a property of the record.

`SHAPE_SPEC.md` §4's removal test in a different substrate — remove the
constraint and see whether the form changes, rather than reading the
residue harder. `METHOD_SPEC.md` §3's UNDERDETERMINED DISAPPEARANCE is the
same limit approached from the other side.

## What is carried and not checked

Every fact about the trigger case — five runs, ten agents, fifteen days,
332 votes across 58 proposals, 98% FOR, zero crimes, the published
disposition — is carried from the marker. The egress gate refuses the
sources. `MS_004` status, and **nothing above rests on any of it**: the
generators are constructed processes and the shape of the trigger case is
used only to set the arithmetic at the right scale.

`CS_006`. The marker's second-order observation — *"countable, which is a
different property than being diagnostic"* — is its strongest content and
is a literature claim this session cannot reach. It is also the neutral
half: a validation study relating disagreement rate to decision quality
would cut against the criterion being applied to anyone, so this audit's
position does not move with the answer.

`CS_007`. Three of the four cross-links do not resolve —
`[[report-typing]]`, `[[rubric-backcasting]]`, `[[merit-anchoring]]` are
all absent, and they are the comparison set the CONFIDENCE section says
the asymmetry needs. `[[uninstrumented]]` resolves and is the right
neighbour: **`AUDIT_ASYMMETRY`, a guard firing on one side only**, is the
mechanism the asymmetry half would file under if it were filed.

## The scan — built 2026-08-24

`SCAN_SPEC` asked for the instrument that would populate the comparison
table: `cases.json`, `scan.py`, `RESULTS.md`. Built. **Building an
instrument and running it is not scoring its subject**, and the split
above holds: the scan computes, it does not conclude, and the asymmetry
is still not scored here.

What made that possible is one design decision the spec did not make.
**`criterion_disposition` is computed from the criterion's threshold and
the case's value, never hand-assigned.** No case carries that field and
`--selftest` fails if one appears. Hand-assigning `defect` to the human
cases would have produced the marker's conclusion from the marker's
assumption, and the scan would have reported the answer it was given.

**The result is that the fired set is empty and 6 of 6 human seed cases
return `UNDETERMINED`** — for two reasons, either sufficient: none carries
a numeric agreement value, and their quantity type is a cross-body
adoption fraction where C reads a within-body agreement rate.

**This refutes the marker's strongest phrasing.** *"Two dispositions, one
measurement"* is not right — there are two measurements, and `SCAN_SPEC`'s
own limits section says so independently. The weaker statement survives:
one criterion form, applied to one subject class and not another. G-DIM
voids the ratio and leaves the comparison legal.

Three further findings in `RESULTS.md`: the threshold was not in the spec
and without one the scoring rule fires by construction; the inverse branch
is `CONSTANT_SILENT` because every seed case is a high-agreement case, so
one branch cannot fire and the set cannot separate asymmetry from
selection on the variable under test; and `retention_basis`, the mechanism
the argument runs on, carries **zero sourced entries of seven**.

`P1` is landed as the *shape* of an inverse case with every value
unstated rather than invented, because populating it is the cheapest thing
that could refute the asymmetry reading — if low agreement in a
legislature is scored a defect and high agreement would be too, the
criterion returns defect at both ends for one class, which is a different
failure and not the marker's claim.

**No agreement figures for human institutions are supplied from memory**,
here or in `RESULTS.md`. Where such rates are recorded is named; the
retrieval is not done. That is the same line as above, held at the point
where it would have been easiest to cross.

## Where it sits

Nearest siblings: `null-harness/` (`NO_DISCRIMINATION` is the verdict
`CS_001` returns), `uninstrumented/` (`AUDIT_ASYMMETRY`, and the marker's
own framing of a quantity the instrument's constitution keeps out),
`divergence-playground/` (the `agree_by_accident` cell is `CS_002`'s
question one level over), and `shape-spec-audit/` (`CS_004` is §4's
removal test arriving in a governance record).

CC0. Stdlib only. Parses under Python 3.9. Nothing here is a statement
about any model's governance, and nothing here is a statement about the
published disposition being right or wrong.
