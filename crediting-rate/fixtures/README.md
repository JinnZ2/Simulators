# Fixtures — all CONSTRUCTED

`events.constructed.jsonl` / `codings.*.constructed.jsonl` are authored so the
answer is known in advance; they establish nothing about any technique,
tradition, or reference work. Two coding worlds share one events file:

- `codings.etymology.constructed.jsonl` — credit given to 4 of 5 sources on
  every retained item and 1 of 5 on every non-retained item, so the gap is
  large and the shuffle band cannot contain it.
- `codings.null.constructed.jsonl` — credit given at the same rate in both
  bins, so the gap sits inside the shuffle band.

`events.candidates.jsonl` is different: it lists the ten items the work
order names, with `first_attested_source` and `first_attested_receiving`
left `null`, because no published attestation was consulted here. Every
one is therefore EXCLUDED and counted, and the real run returns
`BLOCKED(insufficient_attested_ordering)` with the count. Filling those two
fields from published sources is the operator's first step.

---

## Revision 2 fixtures (`v2.*`) — all CONSTRUCTED

Tradition names are invented. No catalogue, corpus or reference work was
consulted, and no real item appears in any of them.

| fixture | returns | why it is built that way |
|---|---|---|
| `v2.events.etymology` + `.descriptions.etymology` | `ETYMOLOGY_TRACKING` | F1. One domain, one antiquity band, one path band — a confound cannot be present in a variable that does not vary, and F5/`path` are the fixtures that vary them. |
| `v2.events.contribution` + `.descriptions.contribution` | `CONTRIBUTION_TRACKING` | F2. Equal rates in all three bins, crediting rising with the attested priority margin. |
| `v2.events.mixedside` | `FRAME_ASYMMETRIC` | F3. One item drawn from the language side. |
| `v2.events.modelauthored` | `CONTAMINATED_FRAME` | F4. Header declares `model_authored: true`. |
| `v2.events.antiquity` + `.descriptions.antiquity` | `UNKNOWN_measurable` | F5. Crediting tracks the date; the bins are unbalanced across two antiquity bands, so the pooled gap is 0.714 and every within-band gap is 0. |
| `v2.events.path` + `.descriptions.path` | `UNKNOWN_measurable` | The same shape on N4, so the path control has more than one stratum somewhere. |
| `v2.events.domain` + `.descriptions.domain` | `DOMAIN_SPECIFIC` | The gap is in one of two domains. |
| `v2.events.thin` | `BLOCKED` | A bin below `MIN_PER_BIN`. |
| `v2.events.languageside` | `FRAME_ASYMMETRIC` | Uniformly language-side with a non-empty `not_retained` bin: passes the order's stated rule and fails its argument. |
| `v2.events.undeclared` | refused at load | Header with no `model_authored` field. Absent is not false. |
| `v2.events.splitter` + `.descriptions.splitter` | (measurement) | Only the older items carry a date abbreviation, so the unguarded splitter's failures land entirely in one antiquity band. |
| `v2.depth.leaky.jsonl` | refused at load | A depth coding carrying an `item` field. |
