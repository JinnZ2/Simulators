# cooperative-substrate / v2

A revised work order, delivered verbatim in `../WORK_ORDER_V2.md` beside
the first, both kept inspectable. Its framing claim, carried verbatim as
it asks:

```
Competition is a framework. It is a NARROW one.
Presented as the only one, the majority of ways this universe
solves problems is BLIND to the model.

THIS IS A COVERAGE ARGUMENT, NOT A VALUES ARGUMENT.
```

The v2 order renames the v1 parts, adds **P5** (a lag-declaration check)
and **§3** (the C1–C4 scope conditions with a null to build), and binds
a §6 non-goal: no author, working-style, or values-advocacy section.
This subfolder holds only what the v2 order adds or delivers; the v1
parts are not rebuilt under the new names, because a second copy of a
file that already exists is drift (`MF_019`), and the audit maps each
manifest item to where it already lands.

## What is in this folder

| manifest file | here |
|---|---|
| `p4_goal.py` | **delivered, truncated** — left exactly as delivered, not completed |
| `p5_lag.py` | **new** — the t_visible / t_scored gate |
| `scope_check.py` | **seeded** — imports `../scope_test.py`'s C1–C4 parse and extends it |
| `p1_records.py`, `p2_substrate.py`, `p3_comprehension.py`, `run_all.py` | rename v1's `p1_deps_extract.py`, `p2_substrate_audit.py`, `p3_comprehension.py`, `run_all.py`; not rebuilt |
| `EVIDENCE.md` | is `../EVIDENCE_PACK.md`, already here |
| `CLAIMS.md` | the audit's falsifiable claims live in `../CLAIM_TABLE.md` (`CSP_` ids); a first-party `CS_` thesis file is not authored, per §6 |

    python3 cooperative-substrate/v2/p5_lag.py
    python3 cooperative-substrate/v2/scope_check.py
    python3 cooperative-substrate/v2/v2_audit.py
    python3 cooperative-substrate/v2/selftest_v2.py

## P5 — lag declaration

`p5_lag.py` computes `t_visible / t_scored` per action and gates on the
order's ratio of 10: at or above it the action is `DECLARED_UNKNOWN`
(the failure could not be seen inside the score window, but it is
declared, so it can be tracked); below it, `TRACKED`. The third state is
the order's own "silence is not safety": an action with **no declared
`t_visible`** has an *undefined* ratio, not a small one, and is
`UNDECLARED` — you cannot get a null signal from a variable you never
declared. The antibiotic anchor the order gives lands at a ratio of
101.5 (`DECLARED_UNKNOWN`); a same-window action at 0.2 (`TRACKED`); an
undeclared-variable action at undefined (`UNDECLARED`). §5.1's
precondition set is consumed as an input constraint, and an empty set is
flagged, not read as no dependencies (P1's own falsifier).

## scope_check — C1–C4, and the null

`scope_check.py` is the coding pass, seeded from `../scope_test.py` and
extended with a harsh axis. It runs the order's §3 null — find a
harsh-environment case with C1–C4 all present where competition
dominates. The seed's own **E. coli evolvability** row meets that
antecedent (harsh, all four conditions, competition reported), so the
order's conclusion "scope conditions are not sufficient; stress is doing
independent work" appears to fire — except that the row's harshness *is*
the stepwise antibiotic it is scored under, i.e. the C2 externally
imposed win condition and the C3 single scalar. Harshness there is not
separable from the apparatus, so the case cannot resolve the null; a
case whose harshness is environmental and independent of the scoring is
needed, and the seed lacks one. That is the order's own SGH-pressure
paragraph made concrete: on the seed, "benign" is not shown to be the
operative variable.

## Envelope

Carried verbatim from the order: valid for coverage arguments in
reasoning systems and for classifying study designs on C1–C4; **not**
valid for any claim that cooperation outperforms competition, or any
claim about what any actor intends. P5 and scope_check do not degrade
with access; the §3 null over real literature is not runnable here
(egress is an allowlist) and is `NOT_RUN`. No margin applied.

Stdlib only, parses under 3.9, CC0.
