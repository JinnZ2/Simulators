# supplement-placement

**Marker under exploration.** Steps 3 and 4 of the main-text/supplement audit,
plus the citation half.

```
python3 placement.py [--selftest]     # 24 checks
```

Object: Jiang 2025, *American Sociological Review*, doi
`10.1177/00031224251362351`. Main text 41pp, online appendix 40pp — the
supplement is **the same size as the paper**.

## Step 3 — the test as specified cannot separate the hypotheses

Main-text elements are primary analyses; supplement elements are robustness
and validation. "Supporting" and "weakening" are **not independent** of
"primary" and "robustness": a robustness check is by construction the only
place a weakening result can appear, because it is the only place an
alternative gets estimated. **A paper's primary figure cannot come out
against its own finding** — if it did, the finding would be different.

So comparing all 10 main-text elements against all 28 supplement ones gives
7/7 supporting vs 11/12 — which *looks* like a result and is an artefact of
genre. The comparison is restricted to the **comparable class**: elements
that could have come out either way (validation and robustness), wherever
they sit.

| | SUPPORTS | WEAKENS |
| --- | --- | --- |
| MAIN | 5 | **0** |
| SUPPLEMENT | 11 | **1** |

main rate 1.000 · supplement rate 0.917 · **Fisher exact p = 1.000**

**Verdict: NOT_ESTABLISHED — and p = 1.000 is not evidence the filter is
absent.** There is exactly **one** weakening element in the entire paper
(Figure S17, evidence for the queuing effect on potency — the competing
mechanism; the author argues those estimates are biased). With one weakening
element there is no power to detect anything, and the same table would return
p = 1.000 under a strong filter too. The instrument ran; the sample cannot
answer.

Five comparable-class elements (Tables S6–S8, Figures S11, S13) carry
**UNDETERMINED** — no direction stated in the extracted text. That missing
data is one-sided: if any is weakening, the supplement cell moves and the
main-text cell cannot. It can only move the result *toward* the hypothesis.

## Step 4 — the reachability cost

| item | paywalled | machine readable | in package |
| --- | --- | --- | --- |
| main text PDF | yes (Sage) | **yes** | author copy |
| online appendix | no | **yes** | author copy |
| replication code | no | yes | yes |
| **trained embeddings** | no | unverified | **NO** |

Both PDFs have real text layers — checked, not inferred. The appendix reports
`/Font 0` and 45 images, which reads as image-only and **is not**: fonts sit
in object streams, and it carries 133 BT blocks and 2025 text operators.

**Verdict: NOT_REPRODUCIBLE_AS_SHIPPED.** The vectors are the instrument's
state and they are not in the package — `data/embedding vectors/` holds a
README pointing at Dropbox, and nothing else. Retraining from the corpora
would be a different training run, not a replication.

**Nothing here was actually blocked by a paywall.** The main text is behind
one and the author posts a copy. What is unreachable is a **Dropbox link**.

**And the shipped instrument is not the documented instrument.** Appendix
Tables S2–S4 document bipolar pairs absent from `dimension-words.txt`:

| dimension | documented, not shipped |
| --- | --- |
| Potency | deep/shallow, thick/thin, large/small, complex/simple, … |
| Evaluation | pure/impure, holy/unholy, valiant/fiendish, … |
| Activity | hot/cold, burning/freezing, active/inactive, … |

Neither is thereby wrong. They are not the same instrument, and a run from
the shipped file uses different centroids from the ones the paper describes.

## The citation half — not runnable

All four citation indices are refused by this session's egress policy:
`api.crossref.org`, `api.semanticscholar.org`, `api.openalex.org`,
`opencitations.net` — CONNECT tunnel failed on each. Without a citation graph
there is no set of citing papers to read. A citation *list* would not answer
it anyway: the question is whether the caveat travelled, which needs the
citing full texts.

## What this does not establish

- **n = 1 paper**, and the claim is about a practice. One article is an
  anecdote about a practice-level filter.
- **Classification is this module's, made after seeing placement.** Criteria
  are stated and direction quotes the author where the text states one, which
  limits the room but does not close it. A blind pass — captions stripped of
  location, sorted by someone else — is what this needs, and n=1 would still
  sink it.
- **It is the paper this work already depends on.** Tasks 1–5 use Jiang's
  instrument. Auditing the placement decisions of the same author whose seed
  file is in use is not independent, and a practice-level claim needs papers
  sampled without reference to which ones were already in hand.

CC0. Stdlib only. Parses under Python 3.9.
