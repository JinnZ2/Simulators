# frame-token-audit

A delivered scanner, landed verbatim: `frame_audit.py` counts frame tokens
per 1000 words under two declared lexicons — v0 (five classes: time as
money, persons as stock, world as stock, relation as debt, relabel) and v1
(v0 plus cost/price, capital/market, value/worth, efficiency) — and lists
every hit with its line. The delivery splits the work in two: **Stage 1**,
this file, mechanical; **Stage 2**, a human or model grading each hit USE
vs MENTION and then running a substrate swap → SURVIVES | CHANGES |
COLLAPSES. Stage 2 is not performed here.

```
python3 frame_audit.py v1 FILE...     # delivered: table + result_v1.json in cwd
python3 audit.py                      # what the scanner does, by running it
python3 selftest_fta.py               # prints its count
```

`audit.py` imports the delivered module and edits nothing. What it shows
(`CLAIM_TABLE.md`, `FTA_001..006`): two tokens are declared twice and
three declared tokens can never fire as declared, because the scan sorts
longest-first only inside a class (`we invest in people` is
time-as-money, never relation-as-debt); six v1 tokens are
`ontology-probe`'s `scope_required` terms and seven are `fold-matrix`
register words, read by import — three instruments on one vocabulary
attaching three different states; on the operator's thirty constructions
v0 is silent and v1 fires three times, twice where ontology-probe's own
screen already fires and once on `value` in the field's-value sense; on
the root specs written against the cost frame v1 reads 2.5–5.4 per 1000
and the hits are the argument against the frame plus `returns` as a verb.
A constructed pair (9 hits against 0, matched words) shows the scanner is
not constant. `samples/` carries the render. Stdlib only, parses under
3.9, phone-buildable, CC0.
