# operator-machine-coupling

`MARKER.md` is a delivered research gap (verbatim, CC0, public domain):
machine operation is accounted for as *operator × machine-class*, and the
**coupling between a specific operator and a specific unit** — the pairing —
is acknowledged everywhere and measured nowhere. The marker is posted as a
gap, not a finding: **nothing in it is a result.**

What this folder adds is the **instruments** the gap's measurables need,
built and null-tested on **constructed** data. No fleet, plant, incident, or
symbiosis data is read (none is available — egress is an allowlist), and
every literature claim in the marker is carried, not verified. The load-
bearing sentence — "measuring pairings instead of averaging over them" — is
made mechanical.

## The instruments

- **`coupling_separation.py`** — the pairing separation. An outcome for
  operator *i* on unit *j* splits into `mu + a_i + b_j + r_ij`: two main
  effects and the **interaction** `r_ij`, which is the coupling. A model that
  fits only the main effects reports `r_ij` as noise and cannot see it. This
  is the same operation as plant breeding's GCA/SCA (diallel) and the
  chimpanzee hammer-anvil (a)/(b) separation — one operation, three
  vocabularies, no cross-citation (all carried). `interaction_fraction` is
  registered in `tools/known_answer.py`. An incomplete design is
  `NOT_ESTIMABLE` (the pairing is invisible where it was never observed);
  no structured variation is `None`, never 0.

- **`discriminators.py`** — two shape tests. `error_vs_coupling`: coupling
  failure tracks time-on-**that-unit**, operator error tracks time-in-role;
  collinear hour-counts return `UNDETERMINED` (the FAA confound), not a false
  attribution. `fixed_vs_convergence`: genotype matching is a `FIXED`
  advantage (the ideal control case), coupling is a `CONVERGENCE` curve.

- **`permission_state.py`** — the three-state permission variable
  (coupled+authorized / coupled+prohibited / decoupled). `regime_collapse`
  shows a single regime label collapsing the three; `attribution` shows a
  naive assignment effect that is actually permission, and `UNDETERMINED`
  when the field is absent or collinear (the recording problem);
  `m2_match_rate` scores the cleanest test case (COUPLED_PROHIBITED) and
  returns `NOT_RECORDED`, never 0.0, when the field is absent.

## The measurables (from the marker)

M0 tool/equipment service life vs assignment structure (FIRST PASS ONLY — it
attributes nothing on its own; its cost-boundary problem is a **declared-
boundary failure**, the same instrument as `machine-record-format` Rule 5 and
`declared-frame`'s VOID RATIO); M1 assignment vs failure mode; M2 work-order
lag and operator diagnostic accuracy (the coupled+prohibited case);
M3 diagnostic accuracy vs certification status; M4 convergence rate on an
unfamiliar unit. **M1 is runnable today** on fleet or plant maintenance data
by anyone who has it — the join is assignment history × failure record ×
hours-on-that-unit; all three fields exist, nobody has joined them.

## Files

| file | what |
|---|---|
| `MARKER.md` | the delivered research gap, verbatim |
| `coupling_separation.py` | the pairing / interaction separation (GCA/SCA) |
| `discriminators.py` | operator-error-vs-coupling and fixed-vs-convergence |
| `permission_state.py` | the three-state permission variable + the confound |
| `demo_omc.py` | a worked pass on constructed data, screened through `no_severity` |
| `selftest_omc.py` | 36 checks — the three instruments, both null directions |
| `CLAIM_TABLE.md` | `OMC_001..OMC_007` |
| `samples/omc_demo.sample.txt` | one constructed report |

## Run

```
python3 operator-machine-coupling/selftest_omc.py     # 36 checks
python3 operator-machine-coupling/demo_omc.py         # the worked pass
python3 tools/known_answer.py                         # interaction_fraction known-answer
```

Library modules refuse `--selftest` with rc 2. The demo screens clean through
`sheet-structure-scan/no_severity` under one declared three-arm exemption
(`error`, the marker's own "operator error" category name). Stdlib only,
parses under Python 3.9, phone-buildable, CC0.

## What this is not

Not a result. The cross-species and cross-literature equivalence the marker
assembles is an **open question**, not a claim: the separation method is
substrate-general and built here, but nothing here shows the substrates share
a mechanism, and plant partner-specificity is kept separate per the marker's
own "Not claimed" note. If someone runs a join and finds no relation, that is
a finding and should be posted.
