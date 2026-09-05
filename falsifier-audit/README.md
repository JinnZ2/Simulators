# falsifier-audit

An extractor plus analyser that walks a local checkout, pulls every
falsifier it can find, and turns each place where a falsifier's **scope is
implicit** into a research question. Built to the delivered
[`WORK_ORDER.md`](WORK_ORDER.md).

It is **not a linter**. It grades no falsifier good or bad and emits no
fixes. The premise is that a falsifier is itself a claim and is frame-bound;
where its scope is unstated, a frame is being inherited silently, and that
site is a place where the corpus holds more information than it states. The
output is therefore additive — questions the repos do not already ask — not
corrective. Every queue entry is a QUESTION with status `OPEN`, the only
machine-set value; nothing is ranked or scored, because ranking would import
a priority the instrument has no basis for.

## Run

```
python3 inventory.py [root ...]     # marker-form inventory — run first
python3 run_all.py   [root ...]     # inventory -> extract -> checks -> queue
python3 run_all.py --write          # also (re)write QUEUE.md
python3 selftest_fa.py              # the checks; writes samples/ and QUEUE.md
```

Default root is the checkout root (`HERE/..`). Stdlib only, parses under
Python 3.9, phone-buildable, no network. The instruments refuse
`--selftest` with rc 2 and name where the checks live; `selftest_fa.py`
prints `selftest: N checks, M failed`.

## Marker inventory (run first, per the order)

The order's first task is to scan the tree and report the falsifier marker
forms actually present, before building the extractor around any of them.
`inventory.py` counts each form; the corpus carries these, in rough order of
frequency:

- **`REFUTATION_PROTOCOL` sections** — the dominant form (~110 files). A
  prose block per claim table, not a per-row cell.
- **prose `Falsifier:` / `Falsified if:`** — a bold or heading claim line
  followed by a falsifier sentence.
- **claim-table columns** named `falsifier` / `falsified by` / `falsified
  if` / `refuted by`, position varying by table.
- **`falsifier_shape` / `falsifier_value` fields** and JSON/YAML
  `falsifier` keys.
- **`FALSIFIER` block labels** inside a work-order or spec.

`extract.py` builds records around the two forms that carry an attached
claim on the same structure — the **table column** and the prose
**`Falsified if:`** — because those are the two where `attached_to` is
locatable verbatim. The rest are counted in the inventory and not extracted;
that is a coverage statement, not a judgement, and it is printed on every
run so an unscanned form does not read as a clean one.

## The record

```
FALSIFIER RECORD
  id            repo:path:line
  text          the falsifier as written, verbatim
  attached_to   the claim it tests, verbatim, if locatable
  attach_status LOCATED | NOT-FOUND
  repo          source repo (top folder)
  form          table | prose
```

`attach_status: NOT-FOUND` is a finding in its own right — a falsifier with
no locatable claim — and is emitted, never dropped. An empty or
punctuation-only falsifier cell (`—`, `n/a`) is **skipped and counted**,
not recorded, and the skipped count is reported: an absent falsifier and a
present-but-unparsed one are different results.

## The four checks

Each runs independently; a falsifier may hit several; nothing is aggregated
into a score. Heuristics are stated at the callsite. A noisy check that is
cheap to dismiss is acceptable, a silent one is not — so the hits show their
matched and unmatched terms.

- **A1 UNFALSIFIABLE-AS-WRITTEN** — fires when the falsifier states no
  number, comparison, unit, or observable-outcome word. It cannot fail as
  written, so the claim it guards is currently unguarded. Emits: *what
  quantity, in what units, would make this fail?*
- **A2 CLAIM-TEST DRIFT** — fires (LOCATED records only) when fewer than a
  third [CHOICE 1] of the falsifier's load-bearing terms appear in the claim
  it is attached to. The test may be testing something adjacent to the
  claim. Emits: *which moved, the claim or the test?* — with the matched and
  unmatched terms shown.
- **A3 CROSS-REPO INCOMPATIBILITY** — the order's highest-expected-yield
  check. Indexes by **axis**, not by rule or repo (axes recur across the
  corpus; rule wordings do not), and looks within an axis for records from
  different repos carrying conflicting numeric cutoffs or opposite
  directions. Emits: *what distinguishes the contexts, and is the difference
  real or is one cutoff inherited?*
- **A4 FIXED-REFERENCE-BODY** — fires on an undeclared reference term
  (`baseline`, `the null`, `chance`, `control`, `relative to`, `matched`,
  …). The geocentric shape: a falsifier can PASS while testing the wrong
  thing because the frame supplied the reference silently. These are
  **rescope** candidates, not narrow ones. Emits: *what is the reference
  body, and what happens if it moves?*

## What A3 returned, and why it is not a bug

On this corpus A3 emits **zero** entries: the numeric-bearing falsifiers on
any shared axis are folder-local, so no two folders quantify one axis
incompatibly — which is the same unquantified property A1 flags from the
other side. This is reported as a result, not hidden, and the check is **not
silent**: its null test (`selftest_fa.py`) fires on a constructed pair of
records from two repos carrying opposite directions on one axis, and stays
silent when both are in one repo or carry the same cutoff. A larger or more
numeric corpus is what would populate A3.

## Self-reference

The tool's own `QUEUE.md`, `samples/`, `README.md` and `AUDIT_NOTES.md` are
excluded from the scan (`SELF_EXCLUDE`), so a re-run does not read its own
emitted queue — or an authored doc that quotes a marker to document it — as
corpus and inflate the next run (the loop `uninstrumented/` records as
`UNI_010`). This README and `AUDIT_NOTES.md` quote `Falsified if:` and the
falsifier header names to explain the checks, which the prose extractor
would otherwise match. `WORK_ORDER.md` — the delivered spec — is left
scannable and carries no attachable marker, so it contributes no records;
that is checked by the record count, not assumed.

## `[CHOICE]` constants

- `A2` share threshold `0.34` — a third of the falsifier's terms in the
  claim (`checks.py`).
- `AXIS_VOCAB` — the recurring measurable-axis word list A3 indexes on
  (`axes.py`); extend as the corpus grows.
- the `OBSERVABLE` / `UNIT_WORDS` / `REFERENCE_TERMS` vocabularies
  (`checks.py`).

Each is printed or discoverable at the callsite. CC0.
