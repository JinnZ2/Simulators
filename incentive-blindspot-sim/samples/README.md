# Sample outputs

Committed artifact from `python3 incentive_blindspot_sim.py`.

- `demo.sample.txt` — three scenarios (`credentialed_closed`,
  `distributed_open`, `closed_with_transparency`) printed every 10
  steps over a 60-step horizon, then all four `CLAIM_BS_*` verdicts,
  then the headline divergence:

  | regime | final B | final P_fail |
  |--------|--------|--------------|
  | credentialed_closed | 1.00 | 0.918 |
  | distributed_open | 0.19 | 0.377 |
  | closed + transparency floor | 0.51 | 0.724 |

All four claims SUPPORTED on the shipped weights. The headline
contrast — same closed structure, transparency floor cuts final
blind-spot volume in half — is the load-bearing finding: visibility
is the control variable, not the gates.
