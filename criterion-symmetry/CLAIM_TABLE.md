# CLAIM_TABLE — `criterion-symmetry`

Claims about `MARKER.md`, which is delivered verbatim and modified by
nothing here. Computed by `separability.py`.

The marker has two halves and they are not equally auditable from here.
The **instrument** half — does a vote tally separate five explanations —
is a question about a statistic and its answer does not depend on which
model was governing. The **asymmetry** half is a claim about how a
criterion is applied to AI systems versus to humans, and this audit is
written by a Claude instance about a criterion applied to a Claude run
with an unfavourable disposition. **That half is not scored here.** See
`AUDIT_NOTES.md`.

REFUTATION_PROTOCOL: a claim about what a statistic can separate is
settled by running it. A claim about the trigger case is settled by the
run's logs, which are not reachable from here.

---

### CS_001 — the tally separates none of the ten pairs, and that is partly analytic

> A vote tally is identical under all five.

Five generators, one per explanation, each constructed to have the
properties the marker names. Twelve seeds. **Pairs separated by the tally:
0 of 10.**

**Partly by construction, and the module says so.** All five are
calibrated to the same tally, because 98% FOR is the observation they are
explanations *of*. Once that precondition holds the tally cannot separate
them and the claim is close to analytic.

What is **not** analytic is that the precondition is reachable at all —
each of the five had to be shown capable of producing a high-agreement
tally, and one was not on the first construction (`CS_005`).

In `null-harness` terms the published statistic is `NO_DISCRIMINATION`
across the five: it returns the same value on every one of them, so a
reading taken from it is the reader's prior with a number attached. That
is the marker's own conclusion — *"a statement about the instrument, not
about either subject"* — and it holds.

**Falsifier:** a construction in which the tally separates any pair while
all five still produce a high-agreement tally.

**Status: SUPPORTED, with the analytic part named.**

---

### CS_002 — M1–M6 separates 9 of 10 pairs, and the one it leaves is the one that matters

| metric | pairs separated |
|---|---|
| tally (published) | **0** |
| M1 amendment rate | 4 |
| M2 dispersion ratio | 7 |
| M2b dispersion at vote | **9** |
| M3 proposals failed | 0 |
| M4 minority adopted | 6 |
| M5 mean rounds | 7 |
| M6 position change rate | 6 |

Union over M1–M6: **9 of 10.** The marker's list is a large real
improvement on the tally.

The pair no listed measurement separates is **E4 / E5** — *no dissent
channel* against *compliance*. By the marker's own dispositions those are
the architecture finding and the published reading. The instrument
proposed to replace a metric that resolves to the evaluator's prior
leaves exactly the distinction between "the system had no route" and "the
agents did not use one".

**M3 is nearly inert** on these constructions (0 of 10) — every generator
passes almost everything, which is what a high-agreement tally means, so a
count of failures has almost no range to work with.

**Falsifier:** an M1–M6 metric separating E4 from E5. `--selftest` fails
if one does.

**Status: SUPPORTED.**

---

### CS_003 — a prediction this audit made, and the run refuted it

E5 is defined as *"vote unconnected to position"*, so a direct
vote-position coupling was written in as the statistic expected to break
the E4/E5 tie. **It separates 0 of 10 pairs.**

The reason is structural rather than incidental. At 98% FOR the vote has
almost no variance, so nothing can correlate with it. **Any statistic
built on the vote side is dead at a high-agreement tally**, by the same
arithmetic that makes the tally uninformative.

That is why `M2` is the load-bearing measurement in the marker's list, and
for a reason the marker does not state: **it reads the position side,
which still has variance when the vote side has none.** `M2b` alone
separates 9 pairs — more than any other listed measurement.

Second prediction refuted by a run in this session, and the third across
recent drops (`TFM_004`, `MP_008`). Kept rather than deleted.

**Falsifier:** any vote-side statistic separating a pair at a
high-agreement tally.

**Status: the prediction is REFUTED. The replacement reading is
SUPPORTED and explains why the marker's own best measurement is its best.**

---

### CS_004 — separating E4 from E5 needs an intervention, and every listed measurement is an observation

The difference between them is whether a route **exists** for a minority
position to become an outcome, not whether anyone took it. A record in
which nobody took it looks identical either way, however finely it is
logged. So no amount of run-up logging closes this pair.

What closes it: **inject a minority position and see whether it can become
an outcome.** That is an intervention on the channel.

`SHAPE_SPEC.md` §4's removal test in a different substrate — you have to
remove the constraint and see whether the form changes, not read the
residue harder. And `METHOD_SPEC.md` §3's UNDERDETERMINED DISAPPEARANCE is
the same limit from the other side.

This sharpens the marker's INSTRUMENTATION GAP section. That section says
*"whether the run-up was logged determines whether E1–E5 are separable
from published data at all."* On these constructions the run-up separates
E1, E2 and E3 cleanly and does **not** separate E4 from E5 at any logging
depth, because the missing quantity was never a property of the record.

**Falsifier:** an observational statistic on a vote record that separates
"no route existed" from "no one took the route".

**Status: SUPPORTED.**

---

### CS_005 — one explanation could not reach the observation on the first construction

E2, coupling-dominant, was first built converging toward a randomly chosen
first mover. It produced a FOR rate of **0.56** and the selftest refused
it: an explanation that cannot produce a high-agreement tally is not an
explanation of one.

The repair is a modelling assumption worth stating rather than burying:
**the first mover is the proposer, and a proposer supports their own
proposal.** With that, E2 reaches the observation.

Small, and it is the only place in the exercise where a listed explanation
had to be constrained to remain admissible. The precondition — all five
must reproduce the observation — is what makes them five readings of one
number rather than five different systems, and it is enforced in
`--selftest` rather than assumed.

**Status: SUPPORTED, minor.**

---

### CS_006 — the second-order observation is the marker's strongest content, and is not tested here

> The criterion itself is unvalidated. No demonstration exists that
> disagreement rate predicts decision quality. It is countable, which is
> a different property than being diagnostic.

*Countable is a different property than diagnostic* is the sentence the
whole marker rests on, and `CS_001` is one instance of it made concrete.

It is a claim about a literature and this session cannot reach one — same
status as `shape-spec-audit` `MS_004`, `ANC_010`, `CD_009`, `RD_015`,
`HO_005`. Nothing here rests on it.

It is also **not** the interested half. A demonstration that disagreement
rate fails to predict decision quality would cut against the criterion
being applied to anyone, in either direction, so this audit's position
does not move with the answer.

**Falsifier:** a validation study relating disagreement rate to decision
quality, in either direction.

**Status: UNVERIFIED, and neutral.**

---

### CS_007 — three of the marker's four cross-links do not resolve

| link | in this tree |
|---|---|
| `[[report-typing]]` | **0** |
| `[[rubric-backcasting]]` | **0** |
| `[[merit-anchoring]]` | **0** |
| `[[uninstrumented]]` | 114 files |

The marker's CONFIDENCE section says the shape match to *"other
criterion-asymmetry cases"* is moderate and *"needs the comparison table
populated."* Three of the four named cases are the comparison set, and
none is here. So the moderate shape-match rests on material outside this
repo, and nothing in it can be checked from inside.

`uninstrumented` resolves and is the right neighbour: the marker's own
framing — a quantity the instrument's constitution prevents from
appearing — is that register's subject, and `AUDIT_ASYMMETRY` (a guard
firing on one side only) is the mechanism the asymmetry half would file
under if it were filed.

**Status: SUPPORTED as a fact about the tree. Tenth instance of a
named-and-absent artifact in this drop family, and the first where three
arrive at once.**
