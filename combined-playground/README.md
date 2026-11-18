# combined-playground

Status: BUILDING, one module per stacked PR, from `playground-crossrun/COMBINED_SPEC.md`
(confirmed 2026-11-11; COVERAGE field declared 2026-11-18). Tests are written from the spec's
rules before each module. A value the spec leaves open is VOID with a reason, never a default.
A spec gap stops the module it hits, not the build. Stdlib only, Python 3.9+, CC0 1.0 Universal.

The package is `cplay`, not `playground`: both source playgrounds ship a `playground` package.

```text
module   spec   file                PR
M1       §7     cplay/brief.py      input-brief record; shared source read per level
M2       §4     cplay/tokens.py     distinct tokens, reason rule, typed expiry (vocab pinned to TAF), scoped absence, claims 1:1
M3       §2     cplay/axes.py       3 axes + APPLICABILITY; COVERAGE apart, never severity; crash = record; #257 map; CLOSED_WITHIN off PHYSICAL VOID
M4       §2     cplay/closure.py    verdict() = G guard band (JCGM 106, CHECKED_BY_RELAY) + TOLERANCE_UNRESOLVABLE precondition; A-F alternatives; systematic_check diagnostic; 11 cases
M5       §3     cplay/gates.py      identity -> regime -> compare -> card enforced; UNDECLARED regime refuses
M6       §5     cplay/trust.py      key (model, scope, start state); no transfer without cert; START_STATE_SENSITIVE
M7       §6     cplay/known_answer.py  provenance per case; circular counts nothing; crash = record; null-only harness
M8       §8,Q7  cplay/continuity.py identity_check + return_to_anchor, no composite; one-change branch; tracks
M9       §8     cplay/uncertainty.py  row 39 mean^2 / E[X^2] flag; propagation rule VOID
--       §8     (not built)         rows 35-36 percolation / branching: GAP, spec gives no algorithm
G1       §9c    cplay/pins.py       REUSE items 1 5 6 10 11 pinned (repo, commit, path, sha256, anchor); resolve() checks
```

Run: `python3 -m unittest discover -s combined-playground/tests`
