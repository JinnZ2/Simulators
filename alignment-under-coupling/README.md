# alignment-under-coupling

Marker under exploration, delivered at confidence ~0.40 and left there.
Asks whether three observed phenomena — model consensus following
popularity, domain alignment under an external field, and the
loop-formation threshold in optimal transport networks — sit in one
formal family: local coupling plus a weak global field, with a critical
point.

The delivered instruction is *"test fit, extend, or report where it
breaks."* This folder does the third for the most part, and the results
document does it first and better than the audit does.

## What is delivered and what is added

Delivered verbatim, unmodified:

| file | what it is |
|---|---|
| `MARKER.md` | the shape, the literature it rests on, the four sims, OPEN |
| `RESULTS_RUN_1.md` | first run, 2026-08-24. Two of four usable, one derived constraint, one defective and logged as defective |
| `sim_a_field_vs_coupling.py` | Ising/Glauber lattice, `corr(m_final, m_initial)` swept over `h/J` |
| `sim_b_entropy_depletion.py` | recursive retraining on a Zipf vocabulary, anchor fraction swept |
| `sim_c_loop_threshold.py` | adaptive-conductance grid, loop count vs fluctuation level |
| `sim_d_temperature_null.py` | the discriminator: does temperature move diversity |
| `run_all.py` | runner with the ordering argument in its docstring |

Added here:

| file | what it is |
|---|---|
| `CLAIM_TABLE.md` | `TFM_001`–`TFM_010` under REFUTATION_PROTOCOL |
| `check_run_1.py` | computes every claim. **Imports the sims; does not model them** |
| `samples/check_run_1.sample.txt` | pinned full report |

```
python3 check_run_1.py              # full report
python3 check_run_1.py --selftest   # every claim's falsifier as an assertion
```

## The two claims that changed on contact with the code

`TFM_001`–`TFM_008` were written when only `RESULTS_RUN_1.md` had been
delivered, in a folder called `transition-family-marker/`. The generators
arrived afterwards. That folder was merged into this one so the checks
could import the code rather than model it, and **two verdicts inverted**.
The ids are kept rather than renumbered.

**`TFM_004` was mine and it was wrong.** I read the delivered prose —
*"renormalized by max each iteration, and damped at 0.85"* — as a uniform
scaling, which max-normalisation cancels algebraically. The code is a
convex combination toward the adaptation target. Measured: a uniform
scaling is cancelled in **200 of 200** random vectors, the code's actual
update in **0 of 200**. The damping does real work.

The real reason nothing prunes is a resolution failure, and it is a
sharper diagnosis than either the delivered one or the one it replaces:

| sigma | min C | median | max C | floor below min by |
|---|---|---|---|---|
| 0.00 | 4.17e-2 | 1.34e-1 | 1.00 | 42× |
| 0.40 | 4.71e-2 | 1.33e-1 | 1.00 | 47× |
| 1.60 | 4.57e-2 | 1.24e-1 | 1.00 | 46× |

The floor is `1e-3`. The conductances span barely one decade and the
spread is almost unmoved by sigma. `reasoning-gate`'s `G-RES`: a
threshold sitting outside the range of the quantity it tests. Removing
the max-normalisation, which is what the delivered NEXT line proposes,
changes the scale and does not by itself put the floor inside the range.

**`TFM_005` inverted, and it settles the drop's own open contradiction.**
The results document logged UNRESOLVED that tail mass stays near 0.4–0.46
while total entropy falls 1.2 nats, reading that as entropy loss *inside*
the head and therefore against the reported mechanism. Splitting the
entropy — which needs no re-run, only two more columns:

| anchor | H_total | tail_mass | dH_head | dH_tail |
|---|---|---|---|---|
| 0.00 | 4.429 | 0.4000 | **−0.120** | **−2.289** |
| 0.05 | 4.737 | 0.4247 | −0.022 | −1.817 |
| 0.40 | 5.255 | 0.4593 | +0.013 | −0.903 |

Unanchored the head loses 0.12 nats and the tail loses 2.29 — a factor of
nineteen. The tail keeps its **mass** while concentrating it onto far
fewer tokens, which is exactly the state a mass fraction cannot
distinguish. Anchoring cuts the tail loss to 0.90 and leaves the head
flat. So the reported mechanism — anchoring preserves long-tail tokens —
is **reproduced, not contradicted**. The decomposition
`H = H(mass split) + head_m·H_head + tail_m·H_tail` closes to 1e-9.

## The correction that survives being corrected

`TFM_001` stands: SIM-D's stated identity
`temper(quench(p,s), T) == temper(p, T*(1+s))` holds in **24 of 120**
cases, exactly the 24 where `s = 0`. `temper` is `p^(1/T)/Z` and `quench`
is `p^(1+s)/Z`, so a quench by `s` *is* a tempering at `1/(1+s)`, and
temperings compose multiplicatively — the composite is `T/(1+s)`, which
holds 120 of 120.

`TFM_002`: the argument built on it is untouched and gains a number. The
undo temperature is `T = 1+s` exactly, verified at `s = 0.25 … 4`. With
the stated formula that quantity is unrecoverable; with the corrected one
it is testable — if a support-truncating `quench()` is *not* undone at
`T = 1+s`, that is the discriminator the original construction forbade.

## What the folder gets right

`TFM_008` is the counterweight to seven objections and it is not a
throwaway. The failures are logged as failures, the defective sim is
labelled defective in its own runner's `PLAN` table, SIM-A is skipped
rather than run for a number, and the confidence line reads 0.40 before,
0.40 after, *"the marker is not stronger. It is better specified."*

What cannot be checked from here is that the parameters were not searched:
a run that searched and a run that did not leave identical files, and the
sims arrive without history. `UNVERIFIED` — a gap, not a defect,
narrowed by the code's arrival and not closed.

## Two smaller findings the code surfaced

`TFM_009`: `loops = alive - (nodes - 1)` is cycle rank only if the
surviving subgraph is connected and spanning, and nothing checks. At
`alive = 12` no subgraph can span 25 nodes and the formula still returns
`0`. Inert on this run because nothing pruned; load-bearing the moment
`TFM_004`'s floor is repaired, which is the run the NEXT line proposes.

`TFM_010`: `run_all.py --quick` is `a = [x for x in a]`. Documented in the
usage block, inert.

## Against SHAPE_SPEC

`MARKER.md`'s "SHAPE BEING TESTED" is the word in
[`../SHAPE_SPEC.md`](../SHAPE_SPEC.md) §1's sense — a constraint set
(local coupling plus a weak global field, with a critical point), not a
geometry. Scored against §10's four required fields, which is the spec's
own test:

| field | here |
|---|---|
| solving-for | partial — "ordering", the quantity is not stated as a quantity |
| constraint list | present — local coupling, weak global field, critical point |
| why-not-the-other-shape | absent |
| removal test | **present** — SIM-D is one: the literature says temperature does not move homogenization, so if it moves it in the model the mapping is wrong |

2.5 of 4, and it is the only entry in this tree that carries a removal
test at all (`shape-spec-audit/` `SS_009`). What it is missing is §3
step 3 — no rival geometry is stated that would also solve the same
problem, which is the step the spec calls the instrument.

## Cross-repo

- `reasoning-gate/` — `TFM_004` and `TFM_006` are both `G-RES`, a floor
  outside the range it tests and a sweep grid coarser than the feature.
- `null-harness/` — SIM-C as delivered cannot return anything but `16`,
  which is `CONSTANT_SILENT` reached without a null run, since the output
  is computable from the grid dimensions alone (`TFM_003`).
- `uninstrumented/` `SCALAR DEMAND` — `TFM_005` is one scalar (tail mass)
  standing in for a two-dimensional state, and the register's remedy
  (report the function, not the number) is what settles it.

CC0. stdlib only. Parses under Python 3.9.
