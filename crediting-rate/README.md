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
one stratum and not another.

The method layer the order consumes is two pieces in two states. **F**, the
branch set, exists at `JinnZ2/method-layer` — carried from the operator and
verified against nothing here, that repository being outside this session's
GitHub scope — so `branch_set.json` is an emission in F's shape pointing at a
real consumer rather than a stand-in for a missing build. **G**, the return
envelope, is absent: none of method-layer's five tools (`branch_set`,
`preference_free_rank`, `rank_detector`, `frame_probe`,
`observer_position_control`, same provenance) is one. The order's instruction
for that state is to define the enum locally and mark it, so the five values
above are the local definition and `G_ABSENT` is the mark — declared in
`crediting_rate_v2.py`, printed in every render, asserted in the selftest.

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

# Revision 2

`WORK_ORDER_V2.md` is the revised dispatch, landed verbatim beside the
first. Both orders and both modules stay inspectable; v1 is delivered work
and is not edited. `crediting_rate_v2.py` is a separate module rather than
a patch, because the bins went from two to three, the blind moved from the
bin to the item NAME, crediting became mechanical, and two returns were
added — that is a different scorer, not an edit to one.

```
events.jsonl ──► CONTAMINATED_FRAME? ──► FRAME_ASYMMETRIC? ──► BLOCKED?
  (item list)     model_authored          same side for            thin bin
                                          all bins                 or undeclared frame
                                                     │
descriptions.jsonl ──► mechanical crediting ─────────┤
  (+ N, + aliases)     (alias in first N sentences)  ├──► gap ──► N1 band
                                                     │      └──► N2 / N3 / N4
depth.jsonl ──────────► attribution depth ───────────┘
  (item name redacted, joined on entry_id)
```

## Pre-stated prediction

Recorded here as the order requires, and in `PREDICTION_V2.md` with a hash
the module prints in every report:

    crediting_rate(visible) > crediting_rate(technical_only)
      >= crediting_rate(not_retained)

`technical_only` is the discriminating bin: the word survived and a general
reader cannot see it. If it tracks `not_retained`, visibility is the
variable; if it tracks `visible`, retention is.

**The two readings are not symmetric with respect to this prediction.**
"Tracks `not_retained`" sits inside the ordering; "tracks `visible`"
violates `visible > technical_only` and refutes it. The ordering already
encodes the visibility hypothesis, so one branch of the discriminator is a
confirmation of the pre-stated ordering and the other is a refutation of
it, and they are not two outcomes of one neutral test. The second
comparison is non-strict as well, so the ordering holds across a continuum
and cannot by itself say where `technical_only` sits; that is reported
separately as

    position = (r_technical - r_not) / (r_visible - r_not)

with 0.0 at `not_retained`, 1.0 at `visible`, a declared `[CHOICE]` cut,
and **UNDEFINED — never 0.5 — when the outer bins do not separate**.

## Run

```bash
python3 crediting_rate_v2.py events.jsonl descriptions.jsonl depth.jsonl frame.json [seed]
python3 crediting_rate_v2.py --selftest
python3 crediting_rate_v2.py --choices
```

- `events.jsonl` — the item list. First record is the list header and it
  carries `model_authored`, which is three-valued: `true` stops the run at
  `CONTAMINATED_FRAME`, `false` proceeds, and **absent stops it too**, with
  the refusal saying so. An absent provenance field read as `false` is the
  contamination going unreported, which is the one failure a gate against
  contamination cannot commit. Each event carries
  `frame_source: {name, side}` with `side` in
  `technique_side | language_side`, plus the three-state `bin` and
  `ambiguous`, which is a bin and never an assignment.
- `descriptions.jsonl` — header carries `sentences_scanned` (the order's N)
  and the tradition `aliases` map. Both are in the data file because both
  are judgements made once, and a judgement in a data file can be diffed.
- `depth.jsonl` — keyed on `entry_id`; a record carrying an `item` field is
  refused at load. The blind moved with the revision: v1 kept the BIN off
  the coding file, and revision 2 says the item name carries its own bin,
  so the NAME is what has to be off it.
- `frame.json` — unchanged from v1, still a declared parameter.

## The two frame-asymmetry readings

The order states one rule — all bins drawn from the same side — and its own
argument implies a second. A list that is *uniformly* `language_side`
passes the stated rule and still cannot have produced its own
`not_retained` bin, because no linguistic index enumerates a word that did
not survive. Both return `FRAME_ASYMMETRIC`, with distinct reasons, and
both are exercised.

## What revision 2 removed, and what replaced it

`origination_vs_absorption` is now coded *"from attested dates only, never
from narrative"*. v1 read `CONTRIBUTION_TRACKING` off a misattribution
rate — items whose narrative named the receiving tradition as originator
while the ordering said otherwise — and the revision deletes the narrative
half and with it the comparison. **The revised schema carries no
contribution proxy at all**, so `CONTRIBUTION_TRACKING` is reachable only
by stipulation, while fixture F2 requires it to be returned on a
contribution-tracking world.

The replacement built here is the attested **priority margin**
(`first_attested_receiving - first_attested_source`), the only
contribution-shaped quantity the revised schema still carries, read as a
Spearman correlation against crediting. It is `[CHOICE 8]` and it is not in
the order.

## The one judgement inside the mechanical measure

Crediting is a case-folded substring test over a declared alias list, and
the order's reason for calling it mechanical — a leak is harmless because
there is no judgement — holds for the *match*. It does not hold for the
*list*: a tradition named by a word the list lacks reads as uncredited, and
nothing here can tell that from a description that does not name it. The
render prints the per-tradition alias count for that reason.

The sentence splitter is the sharper version of the same problem. `first N
sentences` needs a splitter, and an unguarded one breaks on date
abbreviations (`c. 830 CE`), which are commoner in descriptions of older
items — **so its failure rate is a function of antiquity, which is N2's own
control variable**. The module ships both splitters and reports how many
crediting decisions move between them, broken down by antiquity band. On
the splitter fixture, 8 of 16 items move and **all 8 are in the older
band**; on F1 the figure is 0 of 17, which is a property of that corpus and
not evidence that the failure mode is absent.

## Nulls, reported in the order the order asks for

The NOTE is honoured structurally: the correlation of the visibility
ordinal with antiquity and with intermediary count is printed **above** the
rate table, before any fit, because retained items cluster through one
transmission route and one period. N1 is a seeded label shuffle across the
three bins; N2, N3 and N4 report the gap and its own band inside every
stratum. A pooled gap outside the band with no stratum outside its own is
returned as `UNKNOWN_measurable` naming the control it vanished under.

## Return

`ETYMOLOGY_TRACKING` · `CONTRIBUTION_TRACKING` · `UNKNOWN_measurable` ·
`DOMAIN_SPECIFIC` · `BLOCKED` · `FRAME_ASYMMETRIC` · `CONTAMINATED_FRAME`.
All seven occur in the selftest.

## REAL RUN: NOT RUN

The open item is the order's own: **a technique-side transmission catalogue
to draw ALL bins from.** It is unidentified. It is the one piece needing a
human with library access, and until it exists there is no admissible item
list, because a list assembled from the language side fails the frame gate
by construction and a list drafted by a model fails the contamination gate
by declaration.

Everything under `fixtures/` prefixed `v2.` is CONSTRUCTED and says so in
its own header. No catalogue was consulted, no corpus declared, no
description read from any reference work. The tradition names are invented
(`Meridian`, `Kestrel`); nothing here is a statement about algebra, paper,
sine, any tradition, or any person.

`position` is registered in `tools/known_answer.py`. Revision-2 claims are
`CRD_009` onward in `CLAIM_TABLE.md`. Check count printed by
`python3 crediting_rate_v2.py --selftest`.
