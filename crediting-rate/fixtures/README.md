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
