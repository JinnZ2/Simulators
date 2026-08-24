# watch

One file per run, `YYYY-MM-DD.md`, written by `../study_watch.py` on a
GitHub Actions runner and landed by pull request. The pull request is the
gate. Nothing here merges itself.

## Silence from this action is not evidence of absence

Stage 1 is a keyword query. Anything the query never returns is invisible to
this pipeline, **and the size of that set is not measurable from inside it.**
A run with no rows means the query returned nothing. It does not mean nothing
exists.

This is the same false-negative structure as a pre-publication gate: a
rejected-and-correct paper and a rejected-and-wrong one leave the same
record, so the gate cannot produce its own miss rate. Neither can this. The
entry it is watching for —
`../../uninstrumented/cases/024refusalfalsepositiverate.md` — is about
exactly that shape.

## Notification only

No count, no rate, no trend, no "N papers this month" appears in a run file,
and none should be added.

A keyword query selects its frame on searchability. Any number computed over
its results measures the query, not the field. Emitting one would be the
failure `nonidentity-census` T2 refused twice — once when the bulk APIs were
blocked and once when a snippet sample was available and declined.

**If a future change makes this action produce a rate, that change is
wrong.** `assert_no_metric()` in `../study_watch.py` refuses it at write
time, and `tests/test_study_watch.py` asserts the refusal fires.

Known limit of that guard, recorded rather than repaired: it matches the
word, not the quantity. A sentence forbidding rates contains the word and is
refused, which is why the run-file preamble is worded around its own
vocabulary. Left strict — over-refusing a line the module authored is the
cheap direction, and an exemption list is the first thing a real rate would
arrive through. The exemption boundary is by line: entry-derived query
strings and retrieved titles are data and are exempt; everything the module
composes is checked.

## The columns

| column | what it is |
|---|---|
| `entry_id` | the entry being watched |
| `query_string` | stage 1's exact query, logged verbatim. **This is the instrument** |
| `candidate` | a retrieved title, unranked and unscored |
| `source` | crossref, openalex or arxiv |
| `matches_would_measure` | `UNADJUDICATED` on every row, by design — see below |
| `decided_by` | `LEXICAL` or `PREDICATE`, carried from T1. The filter's self-report |
| `notes` | the verb-first residue a reviewer reads to make the call |

`matches_would_measure` is never filled mechanically. All eight
`uninstrumented.ENTRIES` WOULD MEASURE strings return `UNDECIDABLE` under the
verb-first test, because a WOULD MEASURE is a **design** — an instrument, an
interval, a comparison — and a candidate is a **claim**. They are different
grammatical kinds of thing and nothing here compares them. A reviewer decides
in the pull request. Filling the column would be inventing a matcher the work
order did not specify.

`decided_by` is worth reading before `matches_would_measure`. A `LEXICAL`
value means a word list proposed that reading, which is the failure
`nonidentity-census` T1-1 measured at 10 of 12.

## NIL RESULT and NOT WATCHABLE

Both sections are always present. A nil result is a recorded outcome, not an
omission. An entry with no WOULD MEASURE is listed as `NOT WATCHABLE` and
skipped; none is invented for it.

CC0.
