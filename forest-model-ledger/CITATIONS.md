# Citation status -- figures the cross-model audit follow-up leans on (work order 2026-11-10, item 4)

Source text: `ledger/toolkit/cases/texts/kimi_substrate_neutral_intelligence_audit.md`
(sha256 pinned in `ledger/toolkit/cases/texts/MANIFEST.yaml`). Two states, kept apart:

```text
IN_AUDIT_TEXT   the figure is on the stated line of the pinned audit, as the audit states it
UNCHECKED       not checked against the primary source; publisher hosts are not reachable
                from this session (egress), and nothing here is filled from memory
```

Every row is IN_AUDIT_TEXT and UNCHECKED. IN_AUDIT_TEXT is not verification: it shows
this ledger quotes the audit correctly, nothing about whether the audit quotes its sources
correctly.

```text
figure                                   audit line  cited to                                  status
~20% introspection success, best models     149     Anthropic 2026, arXiv 2601.01828          IN_AUDIT_TEXT, UNCHECKED
pea learning: ~9-20 plants per condition,   217     Gagliano et al. 2016, Sci Rep             IN_AUDIT_TEXT, UNCHECKED
  p <= 0.0027
pea replication: 40-61 per condition,       217     Markel 2020, eLife 57614                  IN_AUDIT_TEXT, UNCHECKED
  p = 0.335 and p = 0.387
eval awareness AUC ~0.83 vs human 0.92      209     Needham et al. 2025, arXiv 2505.23836     IN_AUDIT_TEXT, UNCHECKED
Registered Reports positive rate 96%->44%   225     Scheel et al. 2021                        IN_AUDIT_TEXT, UNCHECKED
```

## Possible overstatement (noted, not adjudicated)

Audit line 199 says of Schaeffer, Miranda and Koyejo 2023 that the emergence "was **in
the ruler, not the model**". The work order flags this as possibly stronger than the
source's own hedged framing ("may be" an artifact of metric choice). This session cannot
read the paper and does not settle it; the gap between "may be" and "was" is the item.
Thin volume: one paper carries the claim in the audit, and it is used again at lines 245
and 262. UNCHECKED.
