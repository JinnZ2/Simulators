# CLAIM_TABLE — grounded-work-stack

Claims about `REPORT.md` (an outside report, landed verbatim) and about this
folder's checker. Each id is recomputed by `check.py`; `test_check.py` holds
the checks on the checker. Nothing here verifies a citation.

| id | claim | status | falsifier |
|---|---|---|---|
| GWS_001 | The Mars Climate Orbiter factor "4.45" is lbf→N (4.4482216…) at the precision the report writes it. | HOLDS | 4.45 ± 0.005 failing to contain the defined conversion. |
| GWS_002 | Asana's 60 / 27 / 13 shares sum to 100. The 103 + 209 + 352 hour losses sum to 664, a total the report does not state. | HOLDS | Shares not summing to 100. |
| GWS_003 | 15,057 → 4,590 alerts is a 69.5% cut, which the report writes as 70% at whole-percent precision. | HOLDS | The cut falling outside 70 ± 0.5. |
| GWS_004 | "1.8 hours per day, roughly nine full workweeks per year" needs 200 working days at 40 h/week. A 250-day year gives 11.25 weeks. "Nearly 20%" holds for a 9-h day; on an 8-h day the share is 22.5%. Neither the day count nor the day length is stated. | CONDITIONAL | A stated day count and day length making both figures follow. |
| GWS_005 | The text gives override rates as "90–96%" at 3 sites. The report's own fig3 plots a 53% bar outside that range. It also draws the 49–96% meta-range as a single 90% bar, which is neither the range's midpoint nor its top. | TENSION | Fig3 values transcribed wrongly here (a hand transcription, declared). |
| GWS_006 | §5.3 reads the override stream as physicians usually right (7.3% of alerts appropriate). §9 lists "the 96% overridden alert" among failures that "did not lack the signal". One rate, two opposite readings. | TENSION | A sentence in the report reconciling the two readings. |
| GWS_007 | "30%" names two quantities. The conclusion's "a third of the preventable harm lives [in the seam]" reads one trial's reduction as a located share. A reduction bounds that share from below, if the intervention acts only at the seam. | READING | — |
| GWS_008 | "Four independent working examples" matches the §5 table's four working rows. The four names in the preceding sentence include two the table marks as not working for corrections ("proposed for training data"; "EU-wide by Dec 2026"). | TENSION | The table marking signed provenance and co-determination as working correction channels. |
| GWS_009 | I-PASS appears as nine centers and 10,740 admissions at every site, fig3 included. | HOLDS | Any site disagreeing. |
| GWS_010 | 79 distinct URLs over 64 hosts; none fetched (egress allowlist). | UNVERIFIED | — |
| GWS_011 | Each of the four elements has an in-tree instrument by path: reasoning-gate G-DIM, tools/presignal_ledger.py, reporting-chain-loss, return-path. The mapping is a reading. Two are partial: G-DIM checks units, not conservation; reporting-chain-loss measures information loss, not elapsed time. | RESOLVES | A named path absent. |
| GWS_012 | Nothing in this folder bears on whether the framework, or any cited study, is right. | UNVERIFIED | — |
