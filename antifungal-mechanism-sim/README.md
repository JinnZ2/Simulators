# antifungal-mechanism-sim

Three related modules for exploring antifungal drug combinations, in
order of what each one takes seriously:

| module | scoring | axis it opens |
|---|---|---|
| [`antifungal_mechanism_sim.py`](antifungal_mechanism_sim.py) | additive scalar (Σ eff − Σ tox − Σ res) | interactive CLI, genetic-style crossover between named mechanisms |
| [`antifungal_coupling_core.py`](antifungal_coupling_core.py) | **coupling topology** (signed pairwise J + resistance ∏ over orthogonal axes) | non-additivity |
| [`temporal_dosing_resistance.py`](temporal_dosing_resistance.py) | **kicked relaxor** (populations + genotypes) + **non-commutative J** (order-dependent kill) | time and sequence |

CC0. Python stdlib only.

## The progression

Each module adds an axis the previous one was collapsing:

- **Static + additive.** The starting point. Combinations are treated
  as sums of independent scalars. Interactive; useful for browsing.
- **Static + coupling.** Combinations are non-additive. Efficacy has
  signed synergy/antagonism (`J[i, j]`); resistance is suppressed
  **multiplicatively** across orthogonal axes; same-axis targets share
  a min (no ∏ bonus). **The additive scorer and the coupling scorer
  disagree on the SIGN of the best combination**; the coupling scorer
  is the clinically correct one.
- **Temporal + non-commutative.** Dose is a *kick*; populations relax
  between kicks; schedule shape decides the outcome. And the same drug
  pair produces different kill totals depending on order:
  `J[i → j] ≠ J[j → i]`.

## Non-additivity (coupling core)

Empirical signature (`python3 antifungal_coupling_core.py`):

| combo | additive | coupled | p_res |
|---|---|---|---|
| azole + polyene (EG, MD) | −3.0 | −6.39 | 0.200 |
| echinocandin + azole (CW, EG) | +1.0 | 10.29 | 0.240 |
| **echinocandin + 5FC + Hsp90 (CW, NA, SS)** | **−3.0** | **10.39** | **0.084** |
| all seven | −10.0 | 22.89 | 0.003 |

The bolded row is where the two models flip **sign**. Additive rejects
(CW, NA, SS) at −3, the same score it gives azole+polyene. Coupling
says (CW, NA, SS) is one of the best combinations available — three
orthogonal axes multiply escape probability down to 0.084. Clinical
practice agrees with the coupling scorer:
amphotericin-plus-5-flucytosine is the classical orthogonal-axis
synergy example, and Hsp90 inhibition is a mechanism-independent
potentiator.

**The ∏ is the lever.** Same seven codes, different topology
assumption, opposite ranking on the clinically-correct answer.

Formulas:

```
efficacy   = Σ over axes ( max(effs) + 0.5 · Σ others )   ← within-axis redundancy discount
             + Σ pairs Jij · sqrt(eff_i · eff_j)          ← signed synergy/antagonism

resistance = ∏ over orthogonal axes of min(p_res on that axis)   ← lower is better

fitness    = efficacy − w_tox · toxicity − w_res · resistance − c · (|S| − 1)
```

## Time + non-commutativity (temporal module)

Empirical signature (`python3 temporal_dosing_resistance.py`):

```
[1] resistance vs dosing schedule (dose = kick):
schedule             final_pop   R_frac
simultaneous               461    1.000
sequential mono          65749    1.000
fast cycling             10938    1.000
```

All three schedules end R_frac = 1.0 — the escape genotype RAB takes
over — but the surviving populations rank by 2+ orders of magnitude.
**Simultaneous is the strongest suppressor** because escape needs both
mutations (∼µ²). Sequential mono is the weakest: each long block
sweeps a single-R genotype to fixation. Fast cycling sits between.
Collateral sensitivity (RA hypersensitive to B) further suppresses
under fast cycling — evolutionary steering.

Sequence-dependent (non-commutative) kill:

```
azole -> polyene : kill =  9.4   (ergosterol depleted first, polyene blunted)
polyene -> azole : kill = 15.0   (polyene binds first, then azole)
```

Same two drugs, different order, ~60% more total kill when polyene
goes first. `J[i → j] ≠ J[j → i]` — the interaction matrix is
**non-commutative**. Static scorers (both additive AND the coupling
core) collapse this to a single symmetric `J[i, j]`, which is a
fine approximation for concurrent dosing and *wrong* for sequenced
dosing.

## Interactive sim (unchanged behaviour)

```
python3 antifungal_mechanism_sim.py
```

Six-item menu (list codes → build named mechanisms from codes → view
library → evaluate → cross two → quit). Uses the older additive
scorer. Kept as-is for the design-space genetic-crossover flow.

## Run the tests

```
python3 -m unittest discover tests
```

76 tests total, all stdlib:

- **Additive sim (15):** `INTERACTIONS` shape, `Mechanism.evaluate`
  math, `__str__` format, and `crossover` invariants under seeded RNG.
- **Coupling core (27):** `TARGETS` shape (including `p_res ∈ [0, 1]`
  and `axis` label), shared-sterol-axis contract, `_j` symmetry
  and default-zero, `efficacy` math on all three components
  (within-axis redundancy, cross-axis synergy, signed antagonism),
  `resistance_prob` contract (empty is identity 1.0; same-axis takes
  the min; orthogonal axes multiply), the demo's exact numbers pinned
  to 2 decimal places, and the **rank-flip claim itself**: additive
  rejects (CW, NA, SS) while coupling accepts, and orthogonal-triple
  fitness beats azole+polyene fitness by > 10 units.
- **Temporal + non-commutative (34):** frozen constants
  (R, K, MU, KILL), SENS map for the four genotypes, step's
  non-negativity + genotype-key contract, RAB-only-grows-under-any-dose
  invariant, collateral hits RA extra under B, three named schedules
  at their documented lengths and shapes, `run()`'s empty-schedule
  behavior, the **kicked-relaxor ordering claim**
  (simultaneous < fast cycling < sequential mono in surviving
  population; all three end R_frac ≈ 1.0), collateral sensitivity
  helps fast cycling, and the **non-commutativity claim**
  (azole→polyene = 9.4, polyene→azole = 15.0, order matters by ≥ 5
  units).

Sample outputs are at
[`samples/coupling_demo.sample.txt`](samples/coupling_demo.sample.txt)
and
[`samples/temporal_demo.sample.txt`](samples/temporal_demo.sample.txt).

## Note on scoring

The three modules are a design-exploration progression, not
pharmacological predictions. What each carries:

- Additive: browsable heuristic.
- Coupling core: clinically correct ranking on the shipped targets,
  by taking non-additivity seriously.
- Temporal + non-commutative: honest about the two axes the static
  scorer collapses. Same seven codes are inputs (or `A`/`B` /
  `polyene`/`azole` where the model needs abstract labels); the
  finding is that **schedule shape and drug sequence are their own
  first-class parameters**, not decorations on the static score.

## License

CC0 / public domain. See the repo root `LICENSE`.
