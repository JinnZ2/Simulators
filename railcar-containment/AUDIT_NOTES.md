# AUDIT_NOTES — railcar-containment

The delivered `README.md` heads this folder and describes the delivered
files; this note is the audit's, kept apart from it. The folder is
`railcar-containment/` rather than the delivered `railcar_containment`,
the tree's convention for every drop.

Delivered verbatim: `README.md`, `CLAIMS.md`, `tenability.py`,
`t_hold.py`, `detection_loop.py`, `run_all.py`,
`params/example_lines.json`. Added: `audit.py` (imports the three
screens, edits nothing), `selftest_rail.py`, `CLAIM_TABLE.md`
(`RCT_001..RCT_010`), `samples/`.

    python3 railcar-containment/run_all.py          # the delivered folder
    python3 railcar-containment/audit.py
    python3 railcar-containment/selftest_rail.py

What the audit computes, in one line each:

- the calibrated anchors: CO and visibility exact, **thermal 272.5 s
  against 400 s**, because the anchor lies past the end of the source
  term and the bisection stops at the edge of never (`RCT_002`);
- the volume exponent of `t_available`, 0.79–2.23, with the binding
  channel switching at 200 m³ (`RCT_004`);
- the containment form in `tenability.py` against the linear stretch
  `detection_loop.py` applies — 1.2–1.34× apart, and *never* against
  2300 s at a fraction of 0.1 (`RCT_005`);
- RC_002's crossover: containment at 0.5 and the 100 → 160 m³ volume
  step are the same order, 2.43× against 1.94× (`RCT_006`);
- `t_hold.py`'s default 1.5× margin against the README's "none
  applied", and the README scored 4 of 6 with the `envelope-asymmetry`
  instrument by import (`RCT_007`);
- the params field `offgas_to_flame_s` read by neither line of
  `t_hold.py`, and the two screens' visual latencies on different
  clocks (`RCT_008`);
- RC_005 as arithmetic: a 130 s sensor lead against a 728 s tunnel
  deficit, with the station case as the claim's own falsifier
  (`RCT_009`).

Every FSRI figure is carried at the README's own SOURCE CAVEAT status;
the DOI host refuses CONNECT from here. The audit render screens clean
through the repo's `no_severity` with no exemption. Stdlib only, parses
under 3.9, CC0.
