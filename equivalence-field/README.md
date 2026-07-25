# equivalence-field

Two-file folder. Domain-neutral. stdlib-only. Phone-buildable.

Push comparison DOWN THE PYRAMID to intensive variables — densities,
per-capita and per-node ratios, gradients — where hidden asymmetry
surfaces. Two systems are equivalent when their intensive vectors match
within tolerance, NOT when top-line extensive totals match.

## Layout

```
claim_lineage.py       spine. falsification as a POINTER, not a tombstone.
                       Claim / Lineage with add_root / stand / refute /
                       extend / genealogy / frontier / pending_pointers.
                       Epicycle guardrail on extend(): new variable must
                       be independently_measurable AND predicts_beyond_parent,
                       else EpicycleRejected.

equivalence_field.py   client. System dataclass with intensive vector;
                       rel_gradient (odd, dimensionless, [-2, 2]);
                       gradient_field per dimension; exposed_asymmetry at
                       a tolerance; oddness_audit of a reading against
                       actor exchange; emit() returns the field + audit,
                       never a verdict. seed_claims() lands E1/E2/E3 into
                       a Lineage as the module's own claim table.
```

## Two commitments

**Intensive over extensive.** A billion people and three hundred million
is an extensive count; what drives is the intensive ratio (space per
person, capital per node). Comparison at the extensive tier hides the
asymmetries the intensive tier surfaces.

**Odd readings under actor exchange.** `gradient(A, B) = v(A) − v(B)`
is odd: swapping the actors negates it. A consistent reading of that
gradient must ALSO be odd. A reading that treats the same gradient
differently depending on which actor holds the high side is NON-ODD —
and that break is exactly where the smuggled asymmetry (propaganda)
lives. `oddness_audit(reading, A, B)` reports WHICH dimensions fail
oddness, i.e. where the actor-label is doing work the gradient is not.

`honest_reading` (identity on the gradient) is odd by construction.
`make_threat_reading()` returns `max(0, g)` per dimension — the
propaganda shape: scores a gradient as pressure only when it runs
against the reader. Breaks on every non-zero dimension.

## Falsification as a pointer

`claim_lineage` treats refutation as a search direction, not a
tombstone. `refute(cid, break_note, exposed_variable)` records the
break AND the dimension it points at. The claim's status becomes a
POINTER awaiting extension.

`extend()` spawns a child ONLY if the new variable is:

1. **independently measurable** — not a bookkeeping term
2. **predicts_beyond_parent** — earns its place by naming something
   the parent didn't

Fail either → `EpicycleRejected`. This is the line between science and
rescue. Ptolemaic epicycles rescued the parent claim (Earth-centered
orbit) with a variable whose only job was to fit the anomaly —
predicting nothing new. Refused here.

## The engine's own claims

`equivalence_field.seed_claims()` returns a `Lineage` with three claims
seeded as roots:

| # | Statement | Refuted if |
|---|-----------|------------|
| E1 | equivalence is a match of INTENSIVE vectors, not extensive totals | dependents treat extensive-matched systems as equivalent while their intensive vectors diverge |
| E2 | a consistent reading of a gradient is ODD under actor exchange | a reading fails oddness with no isolable actor-dependent term |
| E3 | gradient magnitude predicts pressure toward flow | flow magnitude is uncorrelated with gradient magnitude at fixed other dimensions |

The module carries its own claims as first-class objects in the spine
it depends on — the same discipline it applies to other claims. When
one of these breaks, the resolution goes through `refute() → extend()`
with the same epicycle guardrail.

`claim_lineage` itself is meta and seeds nothing. It is the framework
for tracking claims; it does not itself claim.

## Samples

```
samples/claim_lineage.sample.txt      K0 refuted, K1 extended, epicycle
                                      mood_of_the_week rejected
samples/equivalence_field.sample.txt  X vs Y: 3 dims of gradient;
                                      honest reading odd; threat reading
                                      breaks on all 3 dims
```

## Boundaries

- **No verdicts.** `emit()` returns the gradient FIELD + oddness audit,
  never who is right.
- **No moral labels.** intensive measurements and potentials only.
- **No intent, no interior state.** the module reads structure.
- **energy_english** (from the wider repo convention): fields are
  measurements, not judgments about actors.

## License

CC0 1.0 Universal. Public domain.
