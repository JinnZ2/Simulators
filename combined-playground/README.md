# combined-playground

Status: BUILDING, one module per stacked PR, from `playground-crossrun/COMBINED_SPEC.md`
(confirmed 2026-11-11; COVERAGE field declared 2026-11-18). Tests are written from the spec's
rules before each module. A value the spec leaves open is VOID with a reason, never a default.
A spec gap stops the module it hits, not the build. Stdlib only, Python 3.9+, CC0 1.0 Universal.

The package is `cplay`, not `playground`: both source playgrounds ship a `playground` package.

```text
module   spec   file                PR
M1       §7     cplay/brief.py      input-brief record; shared source read per level
M2       §4     cplay/tokens.py     distinct tokens, reason rule, typed expiry, scoped absence, claims 1:1
M3       §2     cplay/axes.py       3 axes + APPLICABILITY; COVERAGE apart, never severity; crash = record; #257 map
M4       §2     cplay/closure.py    STOPPED at verdict (spec gap); declarations, prereg hash, R-A4 refusal built
M5       §3     cplay/gates.py      identity -> regime -> compare -> card enforced; UNDECLARED regime refuses
M6       §5     cplay/trust.py      key (model, scope, start state); no transfer without cert; START_STATE_SENSITIVE
```

Run: `python3 -m unittest discover -s combined-playground/tests`
