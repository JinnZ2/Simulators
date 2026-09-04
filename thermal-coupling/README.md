# thermal-coupling

Two delivered MARKER modules, landed verbatim and never edited:
`thermal_coupling.py` (temperature entering a hazard chain at five lag
classes, a product-form coincidence term, claims TC-01..TC-06) and
`airblast_extension.py` (three corrections forced by the Langtang 2015
reconstruction, claims TC-07..TC-11). `coupling_audit.py` imports both
and checks them against their own docstrings, claim tables and demos.

    python3 thermal-coupling/thermal_coupling.py        # the delivered demos
    python3 thermal-coupling/airblast_extension.py      # the extension's demos
    python3 thermal-coupling/coupling_audit.py          # the audit
    python3 thermal-coupling/selftest_tca.py

What comes out:

- **TC-04 is refuted by its own function.** The claim's criterion is
  sensitivity rising toward 0 C; the implemented strength loss is
  concave and sensitivity falls by 3.7× from −9.5 to −1 C. The inline
  comment says the opposite of what the code does.
- **The calibration sentence holds under a flag it does not name** and
  not under the default.
- **"CAL_FOS is the only free parameter"** against 35 numeric literals
  in function bodies, seven functions with no source in their docstring.
- **TC-03's snow half is a docstring**, not code: depth is an input.
- **TC-06's runout multiplier enters no downstream term.**
- **The extension's meltwater calibration is 6.00 by construction**
  where its docstring says 2.3, and its own demo prints both.
- **The extension copies the core's LAG rather than importing it**, and
  reads none of the core's terms.
- The module's stated home folder does not exist, and it cites the
  tree's most-cited absent object.

| file | what |
|---|---|
| `thermal_coupling.py` | delivered verbatim |
| `airblast_extension.py` | delivered verbatim |
| `coupling_audit.py` | both modules against their own claims |
| `selftest_tca.py` | known answers first, both directions |
| `CLAIM_TABLE.md` | `TCA_001..TCA_013` |
| `samples/` | the delivered demos' output, the audit render |

Nothing here is a statement about any slope, snowpack or the cited
literature. Stdlib only, parses under 3.9, CC0.
