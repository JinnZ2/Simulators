# observer-position-control -- claim table

| id | claim | status | number | falsifier |
|---|---|---|---|---|
| OPC_001 | Null (a) is enforced structurally: a behavior file carrying any field beyond the four blind-coded ones is refused with the reason "coder was not blind". | SUPPORTED | selftest: `position` in behavior file → refused | such a file accepted |
| OPC_002 | On a constructed corpus where behavior is identical across positions and labels follow position, the verdict is `OBSERVER_INDEXED` with V 0.853 raw, 0.817 within era, 0.862 within literature, 0.853 within intensity band, and the stated prediction hits on all three positions. | SUPPORTED (fixture) | `samples/indexed.sample.txt` | a real corpus is the only test that matters; this shows the branch is reachable |
| OPC_003 | Removing one behavior component from the own-population descriptions flips the verdict to `BEHAVIOR_DIFFERS` and nothing further is returned. | SUPPORTED (fixture) | component V 0.674 on `arousal_persists` | a differing-behavior corpus reaching `OBSERVER_INDEXED` |
| OPC_004 | Perfect position × decade confounding returns `UNKNOWN_measurable` naming era, never `EXPLAINED_BY_ERA` and never `OBSERVER_INDEXED`. | SUPPORTED (fixture) | `samples/era.sample.txt` | a perfectly confounded corpus returning either explained verdict |
| OPC_005 | A constant label reads as `NO_ASSOCIATION` (V = 0); fewer than `min_cell` held-fixed sources in any position reads as `UNKNOWN_measurable`. | SUPPORTED | selftest | either returning a positional verdict |
| OPC_006 | No corpus has been coded. Every number above is on constructed rows and nothing here bears on the order's question. | UNVERIFIED | -- | a blind-coded published corpus run through the script |
