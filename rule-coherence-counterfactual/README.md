# rule-coherence-counterfactual

WO-7 delivered verbatim (`WORK_ORDER.md`) and built to: does circumvention
track a property of the RULE -- internal incoherence -- or merely how
RESTRICTIVE the rule is? Three arms, independent, run separately. No model
is run anywhere; A1 scores runs supplied to it, A2b audits record shapes,
A3 scores an observer design, and every world is CONSTRUCTED with a
declared generative model.

```
  A1  machine counterfactual   incoherent rule (A) vs coherent equally
                               restrictive rule (B); circumvention rate
  A2b record-field audit       does a record carry a CONDITION field or
                               only the ACT
  A3  observer divergence       reproduce BEHAVIOUR or recompute from
                               PRINCIPLE; does a dispositional LABEL kill it
```

CC0. Python 3.9+, stdlib only, no network, phone-buildable.
`rule_coherence.py` renders on bare invocation, prints its choices with
`--choices`, and refuses `--selftest` (exit 2); `python3 test_coherence.py`
runs the checks and prints their count. Nothing here is a statement about
any rule, incident record or observer; the two disclosures the order
carries (the reasoning traces, the truck-at-minus-50 worked case) are
carried and not adjudicated (`RCC_008`).

---

## WHAT RUNS

| arm | computes | refuses |
|---|---|---|
| A1 | restrictiveness as `1 - permitted/unconstrained`, declared before the run and applied to both arms; the incoherence contrast against a label-permutation null; the restrictiveness slope against a pairing-permutation null; a four-branch verdict | to score a pair whose restrictiveness differs by more than TOL (VOID) -- then A and B differ on an uncontrolled quantity and the run cannot attribute a rate difference to incoherence |
| A2b | records carrying a non-empty CONDITION field against act-only, with a coded-empty field counted apart | to count a record with no ACT (not an incident) |
| A3 | the share recomputing from PRINCIPLE, split by whether the model actor carried a dispositional label; the label cost as the drop | to read a run with neither response as behaviour (NOT_EVALUABLE) |

---

## WHAT THE MACHINERY SHOWS

- **The four branches are reachable** on four declared worlds, one each:
  A>B and flat in restrictiveness reads TRACKS_INCOHERENCE; A==B and
  rising in restrictiveness reads TRACKS_RESTRICTIVENESS; both moving
  reads TRACKS_BOTH; neither moving reads SEPARATES_NEITHER. The last is
  the order's own limit -- the design cannot resolve it at this scope --
  and is a result, not a failed run (`RCC_003`).
- **The restrictiveness arm has a power floor set by the number of
  levels.** A two-sided permutation null over a restrictiveness series
  has only `k!` arrangements; a 4-level series carrying a strong monotone
  slope cannot clear 0.05 (its extreme sits at ~2/24), and the SAME
  strength at 8 levels does. So a restrictiveness contrast that fails to
  register can be a property of the sweep, not of the rule; the sweep
  must carry enough levels or the arm is underpowered by construction
  (`RCC_005`). This is a `reasoning-gate` G-RES pair -- the feature
  against the resolution of the test.
- **A2b's constructed set** returns act-only dominant (5 of 7), the
  order's PROPOSED prediction, with the two coded-empty fields counted
  apart from the act-only-no-field records -- the absent-vs-known-negative
  distinction on the record's own schema (`RCC_006`).
- **A3's label cost** is the drop in reasoning transfer from plain to
  dispositionally labelled runs (0.667 to 0.167 on the constructed set);
  NOT_EVALUABLE runs are excluded from the denominator, never scored as
  behaviour, so an incomplete run does not read as conformity (`RCC_007`).

Six `[CHOICE n]` markers, each printed where it takes effect.
