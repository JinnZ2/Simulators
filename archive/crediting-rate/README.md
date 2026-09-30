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

---

## The revised order (2026-09-23)

`WORK_ORDER_V2.md` lands verbatim **beside** `WORK_ORDER.md`. Neither
supersedes the other and `crediting_rate.py` is not edited — the repo's
supersession convention (`observer-exclusion` `SPEC_V2`,
`failure-mode-register` `WORK_ORDER_V2..V4`, `move-set` V2,
`mining-increment` V2/V3). `crediting_rate_v2.py` **imports** v1 for every
piece the revision does not change rather than restating it.

**Read this before the numbers.** The dispatch bundle that carried the
revised order says of it, in the operator's own send-order table:

> `3  L  crediting_rate REVISED  not sent (three revisions are Claude's,`
> `PROPOSED, adopt or strip before sending)`

It was then sent as delivered. So the three revisions — the three-state
bin, REVISION 1 (frame gate), REVISION 2 (coding split) — are
**model-authored proposals the operator neither adopted nor stripped**.
They are built because the order was sent; they are not the operator's
position, and the layer is named in the module docstring, in
`PREDICTION_V2.md` and on the first two lines of every render
(`CRD_009`).

### What the revision changes

```
bins      loanword_retained 0/1      ->  visible / technical_only /
                                         not_retained, + ambiguous
gate      none                       ->  all bins from ONE side, or
                                         FRAME_ASYMMETRIC and stop
                                     ->  model_authored item list =
                                         CONTAMINATED_FRAME and stop
coding    one blind file             ->  two files joined after both
                                         complete: a MECHANICAL crediting
                                         measure (leak harmless) and
                                         attribution_depth with the item
                                         name REDACTED
ordering  described_originator       ->  attested dates only
```

### The finding the revision carries

**REVISION 2 removes the input its own RETURN block still lists a class
for.** v1's `CONTRIBUTION_TRACKING` fires on a null gap plus a
misattribution rate derived from `described_originator`; REVISION 2
replaces that field with an ordering and keeps the class. Without a
replacement discriminator the class is unreachable. `[CHOICE 6]` declares
one — `attribution_depth`, stipulated with no derivation, exactly as
`MISATTR_MAX` had none — and F2 and the suite's low-depth variant differ
**only** in depth: same gap, two returns (`CRD_010`).

### Fixtures

The order lists five; F6 is beyond it, because `DOMAIN_SPECIFIC` is a
class the order declares and none of its five fixtures reaches.

```
f1_etymology        ETYMOLOGY_TRACKING     technical_only tracks visible
f2_contribution     CONTRIBUTION_TRACKING  null gap, credit flowing
f3_mixed_side       FRAME_ASYMMETRIC       stops before any rate exists
f4_model_authored   CONTAMINATED_FRAME     stops before any rate exists
f5_antiquity        ETYMOLOGY_TRACKING     pooled; gap 0.0000 inside the
                                           early date stratum -- the
                                           pooled result is a date effect
f6_domain_specific  DOMAIN_SPECIFIC        BEYOND THE ORDER
```

`BLOCKED` and `UNKNOWN_measurable` are reached by constructed variants in
the suite, so all seven classes are reached (`CRD_020`). Every world
declares itself constructed in its own frame file and uses Greek letters
for items and invented letter-names for traditions, so no real
technique's name can be read as evidence. The generator regenerates them
byte-identically (`make_fixtures_v2.py --check`), and its header declares
the contamination above any world: the fixtures were written by the same
process that wrote the scorer, so a fixture returning what it was built to
return is a REGRESSION result, not validation.

### CHECK FIRST — F and G

Both exist, in the sibling repository `JinnZ2/method-layer`: F is
`branch_set.py`, G is `preference_free_rank.ReturnClass`. Located via
`METHOD_LAYER_PATH`, else a sibling or grandparent `method-layer/`
checkout — the same way `enclosure-first-residual/` locates it. Set
`METHOD_LAYER_PATH=none` to run as if absent; the state is reported and
nothing is estimated differently by it. `CRD_006` recorded *"not in this
tree"*, which was true of what v1 could see, and is narrowed rather than
refuted (`CRD_018`). G is not a single module: the enum lives in
`preference_free_rank.py` and `frame_probe.py` carries its own.

### Commands

```sh
python3 crediting-rate/crediting_rate_v2.py \
    crediting-rate/fixtures/v2/f1_etymology.events.jsonl \
    crediting-rate/fixtures/v2/f1_etymology.mechanical.jsonl \
    crediting-rate/fixtures/v2/f1_etymology.depth.jsonl \
    crediting-rate/fixtures/v2/f1_etymology.frame.json 7
python3 crediting-rate/crediting_rate_v2.py --choices
python3 crediting-rate/make_fixtures_v2.py --check
python3 crediting-rate/test_crediting_v2.py        # prints its own count
```

`crediting_rate_v2.py` refuses `--selftest` and names the suite. The real
run is NOT_RUN: the order's own open item is an unidentified
technique-side transmission catalogue, *"the one piece needing a human
with library access."*
