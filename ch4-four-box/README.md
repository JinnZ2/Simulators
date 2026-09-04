# ch4-four-box

Two delivered scripts, landed verbatim: `fourbox_forward.py` rebuilds a
four-box CH4 model forward-only (emissions from prescribed
concentrations, no inversion) and prints the published emissions beside
two readings of the transport parameters plus a consistency scan;
`closure_diagnostic.py` takes the reading that fits and asks what
concentrations reproduce the published +SCA run. `fourbox_audit.py`
runs both with their prints captured and reads them against each other.

    python3 ch4-four-box/fourbox_forward.py
    python3 ch4-four-box/closure_diagnostic.py
    python3 ch4-four-box/fourbox_audit.py
    python3 ch4-four-box/selftest_fb.py

What comes out:

- **The rates reading fits** the published polar-only emissions to
  within 4.2 Tg/yr per box; the times reading misses by 47.7 and gives
  a negative southern source.
- **The two scripts run one operator**; their matrices agree to 2e-16.
- **The closure gap is 59.3 ppb**: with the tropical box at the SCA
  value the southern source goes negative, and keeping it at the
  published +10 needs a southern concentration 59.3 ppb above WAIS.
- **The consistency scan and the emissions fit do not pick the same
  transport**: the reading that fits the emissions yields a polar
  gradient of 150.5 ppb against an observed 48.
- Two known answers on the operator pass.

| file | what |
|---|---|
| `fourbox_forward.py` | delivered verbatim |
| `closure_diagnostic.py` | delivered verbatim |
| `fourbox_audit.py` | the two against each other |
| `selftest_fb.py` | known answers first, both directions |
| `CLAIM_TABLE.md` | `FB_001..FB_007` |
| `samples/` | both scripts' output, the audit render |

Every published figure is carried from the scripts and unchecked.
Nothing here is a statement about the atmosphere. Stdlib only, parses
under 3.9, CC0.
