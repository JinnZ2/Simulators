# Paths: open definitions explored by walking them (2026-11-19)

Delivered by chat Claude and relayed by the owner, who said "Yes please commit those" (2026-11-19). Filed verbatim below. Everything after that block is this session's implementation, which is L0 with respect to it.

```text
SILENCE → PATHS → WORN PATH

  OPEN definition (no measurand decides)
      │ lay out the paths (each candidate rule = one branch)
      ▼
  walk each path: run it on real cases, many times, different readers and contexts
      │ every walk recorded with provenance (who, when, which case, which outcome)
      ▼
  the path that stays stable = the low-energy one: few repairs, few exceptions,
  holds across contexts
      │
      ▼
  well-worn path: its authority = its own track record, not a seat

DISCRIMINATOR (from the saying)
  worn by testing    many walks × provenance × outcomes recorded  → reliable
  worn by traffic    many readers just following the others' tracks → popularity
                     (your popularity-as-warning face)
  test: did the walks have independent provenance (L2+), or did each walker see the prior tracks?


path_id | gap_id | candidate rule | walk_id | reader_family | L | exposure to prior walks |
case | outcome (holds / needs exception / breaks / void) | repair_needed | provenance |
date

per path, derived:
  walks · independent walks (L2+, no exposure) · exceptions per walk · breaks
  stability = holds across contexts with few repairs  (no score; show the distribution)
  traffic flag = walks whose walker had seen the prior walks → counted apart
```

## Files

```text
paths.json      the paths: one per candidate rule, for each branch left in ../MEASURANDS.md
walks.jsonl     the walks: one JSON object per line, schema below; EMPTY: no path has been walked
derive.py       per-path counts from the walks; no score, no ranking, no winner
test_derive.py  known-answer cases for derive.py (constructed walks, neutral case names)
```

Run: `python3 derive.py` prints the per-path table. `python3 -m unittest test_derive` runs the tests. Stdlib only.

## Walk schema (one line of walks.jsonl)

```text
path_id                 a path in paths.json
walk_id                 unique
reader_family           model family or pseudonym, never a model identifier
L                       0-4, computed by ../INDEPENDENCE_LEDGER.md's rule; null if not computable
exposure_prior_walks    "yes" / "no" / "unknown"  (did the walker see any earlier walk of this gap)
case                    which case was run (a term id, a fixture id, a source path and lines)
outcome                 "holds" / "needs_exception" / "breaks" / "void"
repair_needed           text, or null
provenance              who recorded it, from which record (path@commit)
date                    YYYY-MM-DD
```

## How derive.py counts

These are this session's reading of the delivered text. Each is open to the next REVIEW:

- **Independent:** L >= 2 **and** `exposure_prior_walks == "no"`.
- **Traffic:** `exposure_prior_walks == "yes"`. Counted apart and never added to independent.
- **Exposure unknown:** a third column. It is neither independent nor traffic, and the walk's L is not trusted beyond what is recorded.
- **L null or below 2 with no exposure:** "dependent", in a fourth column.
- **Reported:** per path, the outcome distribution (holds / needs_exception / breaks / void), the repairs listed, and the number of distinct cases and of distinct reader families among independent walks (the "across contexts" part).

No stability score is computed, and nothing compares one path with another. Which path is worn is read from the distributions, by whoever is in the stage reading them.
