# criterion-externality

WO-6 delivered verbatim (`WORK_ORDER.md`) and built to: a proposed
FOURTH independence axis for audit assurance -- whether the standard the
audit is run against is held by either party -- graded C0..C3, against a
published three-axis framework (arXiv:2609.18272) the order's own author
read at abstract level only.

```
  axis 1  PRINCIPAL   who commissions       \
  axis 2  SUBSTRATE   what it runs on        > "are the PARTIES separated"
  axis 3  EVIDENCE    where evidence is from /
  axis 4  CRITERION   who holds the ruler    -- "is the MEASURAND party-held"

  C0 audited party   C1 auditor   C2 third party, discretionary
  C3 a re-runnable procedure: the only rung that is not a claim by someone
```

CC0. Python 3.9+, stdlib only, no network, phone-buildable.
`criterion_externality.py` renders on bare invocation, prints its
choices with `--choices`, and refuses `--selftest` (exit 2);
`python3 test_criterion.py` runs the checks and prints their count.
**The fault model is CONSTRUCTED** and every number it returns is a
property of the construction. The paper's body is not read and its host
refuses CONNECT from here (`R1`, probe recorded in the module), so its
Monte Carlo is not re-run; nothing here is a statement about the paper's
result or about any audit regime (`CEX_010`).

---

## WHAT RUNS

| item | computes | scope |
|---|---|---|
| separating test | axes 1-3 at the top rung and axis 4 at C0 aggregate to 1.00 over three axes and 0.00 over four | arithmetic; needs no model |
| monotonicity | over all 256 grade cells, adding an axis under weakest-link never raises the aggregate and lowers it on a non-empty set | arithmetic |
| R2 | surfaced-fault rate on eight constructed classes with a beta-factor common cause, three axes (ruler unmodelled) against four axes at each C-grade; delta per grade; classes never surfaced | CONSTRUCTED model |
| R4 | per class, sensitivity to beta against sensitivity to the criterion grade; whether any class the criterion excludes is reachable by ANY beta or party count | CONSTRUCTED model |
| R3 | the five regimes the order names, carried UNCODED; the prediction returns NOT_EVALUABLE and both its branches are shown reachable on constructed codings | no real regime is graded |
| arrivals | the three independent arrivals resolved by path and marker in this tree | 2 of 3 resolve |

`expected_rate(p, n, beta, q)` is the beta-factor form in closed form
with the criterion applied at probability `q`, registered in
`tools/known_answer.py`; the Monte Carlo is checked against it.

---

## WHAT THE MODEL SAYS AND WHAT IT DOES NOT

- The **direction** is arithmetic, not a model result: under weakest-link
  aggregation an added axis can only lower the reported number, and a
  coverage gate in front of every party can only move a fault class INTO
  the never-surfaced set, never out of it. The order's R2 question
  "whether any fault class moves out of the never-surfaced half" has one
  answer under a gate, none, before any draw (`CEX_009`).
- The **magnitude** (delta -0.05 at C0 on eight classes, four of eight
  never surfaced) is the construction's and is not the paper's 5.9%.
- **R4 as computed** is a property of the constructed form: the
  beta-factor common cause is a shared draw between parties and has no
  term for what the ruler covers, so a class outside the criterion is
  surfaced at 0.0 at every beta and every party count. Whether the
  paper's own model has such a term is what reading the paper decides
  (`CEX_003`).
- **The C-grades order authorship, not surfaced rate.** C2 covers more
  classes than C1 and applies them at discretion; below a computed
  crossover (q* = 0.959 on this model, against a stipulated 0.7) it
  surfaces FEWER faults than C1. The grading is an ordinal on who holds
  the ruler and is not monotone in the quantity R2 reports (`CEX_005`).
- **The three arrivals** resolve two of three in this tree (`PREAMBLE.md`;
  `frame-instruments/` condition B); the third, the audit-protocol work
  order's C4, is not in this tree. All three are the same operator's
  work, so "not built together" is the claim and "independent" is
  stronger than what is established (`CEX_008`).

Six `[CHOICE n]` markers, each printed where it takes effect.
