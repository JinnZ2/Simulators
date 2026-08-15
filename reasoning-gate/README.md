# reasoning-gate

A fail-closed gate that sits between a simulation and its conclusions.

Default is DENY. A sim that does not declare gets no output. A quantity
that is not tagged is not recorded. A ratio across unlike objects is
void. A claim without named support does not enter the conclusion.

The gate checks nothing about arithmetic. Every failure it catches is
one a correct program produces happily: the numbers are right, the code
runs, and the conclusion does not follow.

## Contents

| File | What it is |
| --- | --- |
| [`gate.py`](gate.py) | The gate, **verbatim as delivered**. Not repaired — see the audit below. |
| [`guards.json`](guards.json) | The eight-guard registry. Authored here; the drop did not include it, and `gate.py` refuses to load without it. |
| [`retro_sim_stack.py`](retro_sim_stack.py) | The gate run backwards over [`../aperiodic-order-sim-stack/`](../aperiodic-order-sim-stack/), a drop that already shipped. |
| [`tests/test_gate.py`](tests/test_gate.py) | 38 tests. Guard behaviour, plus four shipped defects locked in. |
| [`samples/`](samples/) | Pinned output of the retro run. |

Stdlib only, no network, Python 3.7+. CC0.

```bash
python3 gate.py                      # self-test: fails closed, loads 8 guards
python3 retro_sim_stack.py           # the retro demonstration
python3 -m unittest discover tests   # 38 tests
```

## The eight guards

| id | Stage | Rule | Denies when |
| --- | --- | --- | --- |
| `G-PRE` | pre | Declare question, statistic and expectation before executing | any field is empty; anything is called before `pre()` |
| `G-FIT` | pre | The statistic must discriminate between the hypotheses in play | no discrimination is declared |
| `G-RES` | pre | instrument × margin ≤ feature | the instrument is coarser than what it must resolve |
| `G-CTRL` | pre + post | Controls named with predicted values, results recorded | a control is undeclared, unpredicted, or never run |
| `G-LAYER` | mid | Tag every quantity `generator` / `physical` / `instrument` and name its object | a quantity is untagged, or crosses layers without justification |
| `G-DIM` | post | A ratio needs both operands to be properties of one object | numerator and denominator belong to different objects |
| `G-SUP` | post | A claim names the recorded quantities supporting it | it names none, or names something unrecorded |
| `G-IND` | post | Convergence requires naming what the converging lines share | nothing is named as shared |

Pre-stage guards always deny. `strict=False` downgrades post-stage
guards to logged findings — useful for auditing something already
finished, which is what the retro run does.

Two distinctions the guards get right and are easy to get wrong:

- **`G-DIM` voids ratios, not comparisons.** Reading one statistic across
  two objects (`D_f(AB)` vs `D_f(cascade)`) is exactly what a comparative
  sim is for. Dividing a property of one object by a property of the
  other is not, even when both are dimensionless and the division runs
  clean.
- **`G-IND` does not forbid convergence claims.** It requires the shared
  input to be named, which downgrades "three independent lines converge"
  to a qualified claim. That is usually the honest version.

## The retro run

`retro_sim_stack.py` applies the gate to the three sims in
[`../aperiodic-order-sim-stack/`](../aperiodic-order-sim-stack/), which
shipped as a finished result with no gate and was audited afterwards.
Every input is sourced — `[R]` report, `[F]` shipped figure, `[C]`
measured by that folder's `finite_n_control.py`, `[G]` `gate.py`'s own
docstring. Nothing is invented for the demonstration.

Against the four findings that audit took four figures and a rerun
control to reach:

| Audit finding | Gate verdict |
| --- | --- |
| **1** — two estimators, opposite signs, one reported | **Partial.** `G-CTRL` gives the Line control one slot both results must occupy, so the disagreement lands beside the claim. The gate cannot compel an author to record a run. |
| **2** — decisive gap ~75% inside the artifact budget | **Caught at `pre()`** by `G-RES`, comparing two declared numbers, before a point set exists. |
| **3** — SIM-C's null entered as positive evidence | **Caught twice** — `G-CTRL` on the unrun positive control, `G-SUP` on the claim naming nothing. |
| **4** — no Bragg peaks in the S(k) figure | **Caught at `pre()`** by `G-RES`. SIM-A never runs. |

Two of the four are pre-stage arithmetic on two declared numbers each.

The run also surfaces two things the audit missed:

- **`G-DIM` voids the ratio 54.1.** SIM-C divides a band-edge splitting
  of the tight-binding lattice model (0.0812) by a splitting of the
  cascade set (0.0015). Both real, both dimensionless, division clean —
  and the quotient is a property of one object over a property of
  another. The report reaches the same place in prose ("the two systems
  operate on very different normalized energy scales") without noticing
  it has voided its own number.
- **`G-IND` downgrades the overall conclusion.** "Three independent
  simulations converge" — but SIM-A and SIM-B are two statistics on the
  same pair of point sets. Naming the shared input turns independent
  confirmation into a qualified claim.

### `G-RES` and SIM-A

The most interesting single result. `gate.py`'s own docstring declares a
k-grid of 0.39 against a Bragg peak width of 0.063 — the k-space
resolution of SIM-A. The grid is 6.2× coarser than the peaks it must
resolve, 12.4× short of the default 2× margin.

That is a quantitative account of the audit's Finding 4. The reason no
eight-fold Bragg star appears in `sim_a_structure_factor.png` is not only
the linear color scale: at that grid spacing the peaks fall between
sample points. **SIM-A could not have resolved Bragg peaks whether or not
they were there**, so its null carries no information about
quasiperiodic order — and the gate reaches that from two numbers,
without rendering a figure.

### `G-RES` and SIM-B: the margin is a policy dial

SIM-B is declared with an artifact floor of 0.252 (measured by
`finite_n_control.py`) against a separation of 0.334. At the default
margin of 2.0 it denies; at 1.0 it passes narrowly. Both are in
`samples/retro_sim_stack.sample.txt`.

That is the audit's "direction survives, magnitude does not" in the form
the gate can enforce — a margin an operator chooses out loud, rather
than a precision quietly implied by quoting three decimals.

## Audit of the gate itself

`gate.py` is checked in exactly as delivered. Four defects found on
landing; each is locked into `tests/test_gate.py::ShippedDefects`
asserting **current** behaviour, so a repair turns a test red on purpose
rather than passing silently.

**D1 — the docstring's usage example denies at `pre()`.** The example
runs `resolution=[Resolution(..., instrument=0.39, feature=0.063)]` and
then continues through `record` / `claim` / `close`. It cannot: 0.39 ×
2.0 > 0.063, so `G-RES` denies and the example never reaches its second
call. Two readings, and I cannot tell them apart from the drop alone —
either it is a doc bug, or the numbers are real SIM-A parameters and the
example is a deliberate demonstration that SIM-A fails the gate. If the
second, it deserves a sentence saying so, because it is presented under
"Usage".

**D2 — `promote()` and `ratio()` silently overwrite.** `record()`
explicitly refuses to overwrite a name. Neither of the other two writers
checks, so `promote("x", "y", ...)` replaces an existing `y` and its
value is gone. This lands in the one operation `G-LAYER` exists to make
explicit: a promotion that silently overwrites a physical quantity with
a generator-derived one is the substitution the guard was written to
prevent.

**D3 — strict `close()` loses the report, and the retry reports a
control as run.** With an unrun control, `_soft` raises before
`self._closed = True` and before the JSON is written. Denying is right;
producing no forensic record is not — the reason for the denial exists
only in the traceback. The gate is also left open, so:

```python
try:
    g.close(observed=...)       # denied: control never run
except GateError:
    pass
g.control_result("positive control", "n/a")   # accepts any string
g.close(observed=...)                          # clean report
```

The finding survives in `findings[]`, so this is not a silent bypass —
but the report's `controls` block now says `run: True` and `summary()`
prints the control as `run`, contradicting the finding below it. A
report should not disagree with itself.

**D4 — a malformed registry loads, then crashes.** `_load_guards`
verifies all eight ids are present but not that each carries a
`fail_message`. A registry missing one loads fine and raises `KeyError` —
not `GateError` — at the moment that guard fires. For a fail-closed tool
that is the wrong order: it fails open at load and hard-crashes at
denial, in the code path that runs precisely when something has gone
wrong.

None of the four undermines the design. D1 is documentation, D2 and D4
are missing checks of a kind the gate imposes on its callers, and D3 is
a fail-closed choice with a reporting consequence. They are listed
because a tool that demands declarations should hold still for one.

## `guards.json`

The registry did not arrive with the module, which fails closed without
it and refuses to load unless all eight ids are present. It is authored
here from `gate.py`'s call sites — each guard's `id` and `fail_message`
are what the module requires; `name`, `rule`, `rationale`, `stage` and
`enforcement` are documentation the module ignores.

The fail messages are the gate's user interface: they are what an
operator reads at the moment they are denied, so each states the rule
violated rather than the check that failed. Rewriting them changes what
the gate says, not what it does.

## Where this sits in the repo

- [`aperiodic-order-sim-stack/`](../aperiodic-order-sim-stack/) — the
  subject of the retro run, and the drop this gate reads as a response
  to.
- [`null-harness/`](../null-harness/) — `G-CTRL` is its central
  invariant expressed as a precondition instead of a measurement. The
  harness measures whether a gate fires on known signal and known null;
  `G-CTRL` refuses to let a run conclude before that measurement exists.
- [`instrument-epistemology/`](../instrument-epistemology/) — `G-RES` and
  `G-LAYER` are its M0–M3 model-dependence ladder and blindness maps in
  enforceable form.
- [`grounding-layers/`](../grounding-layers/) — same
  refuse-to-score-out-of-scope stance as the SCOPE-annotated
  category-error guards, one level down: those refuse claims outside a
  layer's ontology, `G-DIM` refuses quantities outside an object's.
- [`divergence-playground/`](../divergence-playground/) — `G-IND` is its
  `agree_by_accident` cell as a precondition: convergence between
  readers who share an input is not convergence.

## License

CC0-1.0, matching the repository default and the module's own header.
