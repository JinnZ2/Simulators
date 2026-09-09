# crediting-rate

WORK ORDER L, delivered verbatim in `WORK_ORDER.md` and built here. Does
attribution of an imported technique track CONTRIBUTION, or track whether
the loanword survived into the receiving language? A rate comparison across
loanword bins with the attested ordering held; not an argument about any one
case.

```
events.jsonl ─┐ (bin + attested ordering)
              ├─► join (only here) ─► gap ─► N1 shuffle band ─► G return
codings.jsonl ┘ (crediting per reference source, coded BLIND)
                                     └─► N2 date / N3 domain / N4 path strata
```

## Run

```bash
python3 crediting_rate.py events.jsonl codings.jsonl frame.json [seed]
python3 crediting_rate.py --selftest
```

- `events.jsonl`: `item, domain, source_tradition, receiving_tradition,
  first_attested_source, first_attested_receiving, intermediary_count,
  loanword_retained (0 | 1 | "ambiguous"), ordering_source`. Ordering is
  known only when both years are integers and a published source is named;
  unknown is EXCLUDED and counted, never estimated; receiving-first is
  `reversed` and excluded too (not an import).
- `codings.jsonl`: `item, source_id, coder_id, credits_source (0/1),
  attribution_depth (0..3), described_originator (source | receiving |
  unstated)`. Any field containing `loanword` is refused: the coder never
  sees the bin, and the two files meet only in `join()`.
- `frame.json`: `corpus, edition, date`. The frame is a parameter; running a
  second frame is the replication. `UNDECLARED` in any field returns
  `BLOCKED(frame_undeclared)`, an addition to the order's single BLOCKED
  reason, because an undeclared frame is not a run.
- `PREDICTION.md` was written before any coding; the script refuses to run
  without it and prints its sha256 in every report.

## Return (G)

| return | condition |
|---|---|
| `BLOCKED(insufficient_attested_ordering)` | fewer than `MIN_PER_BIN` (3, a `[CHOICE]`) items with attested ordering in either bin |
| `ETYMOLOGY_TRACKING(gap, ci)` | gap outside the N1 shuffle band and positive, the pre-stated direction |
| `DOMAIN_SPECIFIC(domain, gap, ci)` | pooled gap outside the band but exactly one domain carries it (N3's rule) |
| `CONTRIBUTION_TRACKING(gap, ci)` | gap inside the band and misattribution rate ≤ `MISATTR_MAX` (0.2, a `[CHOICE]`) |
| `UNKNOWN_measurable(reason)` | gap inside the band with misattribution above the cut, or outside the band against the predicted direction |

The N1 band is a percentile interval over `SHUFFLES` (2000) seeded
reassignments of the bin labels across included items; the `ci95` is a
seeded bootstrap over items. N2, N3 and N4 each report the gap and its own
band inside every stratum, so a confound shows as a gap that survives in
one stratum and not another. The method layer the order consumes (F, G) is
not in this tree: G is the five values above, F is `branch_set.json` in the
order's shape.

## State

No real coding exists. `fixtures/events.candidates.jsonl` lists the ten items
the order names with both attestation years `null`, because no published
source was consulted here; the real run returns
`BLOCKED(insufficient_attested_ordering)` with ten excluded. The two
constructed worlds under `fixtures/` return different values of G, so the
return is not constant. Filling the ten orderings from published sources,
declaring a frame, and coding blind are the operator's steps, in that order.

`samples/` holds the selftest transcript and the four rendered returns.
`bin_gap` is registered in `tools/known_answer.py`. Claims in
`CLAIM_TABLE.md` (`CRD_`). Stdlib only, parses under 3.9, CC0.
