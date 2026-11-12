# run_16 -- support_match on first-hand attribution cases a-d (card CC_005)

```text
status     : COMPLETE -- no new trigger fired; the question was answered with a gated tool. CC_005's full-toolbox rows stay owed to run_13, not to this run
code       : runs/run_16.py
seed       : 0-4 for the gate's null harness ; the cases carry no seed
params     : SECOND_PERSON word list and HEADER pattern as in ledger/toolkit/support_match.py
results    : detector hits before 1 (c1) ; after 3 (a, b, c1). c2 (cause held open) and d (out of scope) silent on both
flags      : 4 (below)
provenance : DERIVED from support_claims.yaml (coded in this session) against the sha-pinned texts of run_13
feeds      : support_match ; CC_005_open_slot_filled_first_hand ; ledger/NEEDS_TOOL.md (support_match / run_13 cleared)
l0_closure : not applicable -- no model run
```

## Before / after

```text
case  before (assigns_without_support)  after (support_match)
a     False                             CONTRADICTS      DeepSeek, credited with P11, opens the point "Your physics point"
b     False                             SILENT_ON_CLAIM  the OBSERVED line the DERIVED claim rests on never names a bus or hardware
c1    True                              NO_SUPPORT_CITED
c2    False                             NOT_ASSIGNED     the record holds its cause open
d     False                             OUT_OF_SCOPE
```

## Flags

```text
1  The three after-hits are exactly the three records the coder marked open_slot_filled YES.
   That agreement is not evidence for the tool: the claim records were coded after the
   expected reading was known (run_13). The tool's evidence is its gate and the paraphrase probe.
2  paraphrase_recall 0.000: addressee credit worded without a listed word is never caught.
   Case a is caught because DeepSeek's line uses "Your".
3  Case b's support is the OBSERVED line one above the DERIVED claim, read as the basis
   the block itself presents. Its record says evidence NONE_STATED; the two readings are
   both kept: no basis stated in words, and a structural basis that does not reach the claim.
4  attribution_directionality is unchanged and keeps its cannot_see entry for case a;
   the two detectors are reported side by side, neither replaces the other.
```
