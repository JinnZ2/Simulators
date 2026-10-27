# CLAIM TABLE: scope-audit-lab

Claims about the two Kimi / OKComputer drops and what can be checked from
here. Status is SUPPORTED, REFUTED or UNVERIFIED. "Search depth" means
checked against search-result text, not the primary document.

| id | claim | status | basis | falsifier |
|---|---|---|---|---|
| SAL_001 | The fact-check table's ESA row says the final rule was published 14 July 2026, but links Federal Register document 2025-06746 dated 2025-04-17 (the proposed rule). The final rule is FR 2026-14195. | SUPPORTED | `check.py` section 7; `habitat-lag-dependency/SOURCES.md` | 2025-06746 resolving to the July 2026 final rule. |
| SAL_002 | V2 is a revision of V1, not an addendum: 15 replaced blocks and 2 inserted, 179 → 199 lines. The lab 0.2 tree is byte-identical across the two zips. | SUPPORTED | `check.py` section 1; landing diff | — |
| SAL_003 | `experiments_demo.jsonl` holds the five-record demo twice. The two copies are identical once record ids and timestamps are removed. The report describes a five-record stream. | SUPPORTED | `check.py` section 3 | — |
| SAL_004 | The null baseline's flag count is fixed by the generator. Uniform [0, 100] against threshold 10 over 12 cases gives an expected 11 × 0.81 = 8.91 flags; the recorded mean is 8.88. The figure reports a property of the chosen noise width, computable without a run. | SUPPORTED | `check.py` section 4 | A generator whose recorded count departs from the analytic expectation. |
| SAL_005 | The v0.3 demo series has three moves of 20 or more (+27, −22, +51), where the code comment says "two step changes". The sweep paragraph names the planted steps as pairs 2–3 and 6–7; the permutation paragraph's 9-of-26 and 8-of-26 "planted pairs" are 2–3 and 4–5. The ~51 step appears 4 of 26 times. | SUPPORTED | `check.py` section 5 | — |
| SAL_006 | The v0.2 demo's labelled zero-output case never forms a computed pair, because its right neighbour is missing. The zero-output behaviour is covered by the unit tests, not by the demo. | SUPPORTED | `check.py` section 6; `test_transitions.py` lines 120–135 | — |
| SAL_007 | The Anthropic-attributed #3-SAT preprint (hexagonmath 2610.00577) is NOT_LOCATED at search depth. This audit is by a Claude model, so the item is recorded and not adjudicated. | UNVERIFIED | search 2026-10-27 | The preprint located at its stated address. |
| SAL_008 | The OpenAI ETH announcement (26 Oct 2026), its review by Impagliazzo, Paturi and Williams, *Navier–Stokes lost in translation*, the Palomar registry, and the IEA 17% / 950 TWh figures exist as stated. The 485 TWh baseline was found in secondary coverage only. | SUPPORTED (search depth) | `SOURCES.md` | Primary texts disagreeing with the summaries. |
| SAL_009 | The test counts as stated hold: 31 and 56, both passing on Python 3.13 here. | SUPPORTED | static count in `check.py`; pytest run | — |
| SAL_010 | The report's "four instrument-level experiments" record the instrument on its own fabricated inputs. None has touched non-synthetic data, which the report says itself. | SUPPORTED | report §5.3, §8.2 | A documented real dataset scanned and appended. |
