# TASK 1 — seed sets: FOUND, extracted verbatim

**Status: task 1 complete. Task 2 blocked. Task 5 blocker resolved.**

Seed file landed verbatim at [`seeds/dimension-words.txt`](seeds/dimension-words.txt)
— byte-identical copy, not transcribed.

```
md5  de5cdbb44650e9b88c015737b1170ce2      2450 bytes
src  github.com/wenhaojiangsoc/devaluation @ c22a643
     data/dimension and mapping/dimension-words.txt
```

## Reproduction

```
git clone --depth 1 https://github.com/wenhaojiangsoc/devaluation
cat "devaluation/data/dimension and mapping/dimension-words.txt"
```

The `/data/` page on the author's site is **not reachable** (see Reachability).
The package was found instead through the site repo's bibliography:
`_bibliography/papers.bib` → `code={https://github.com/wenhaojiangsoc/devaluation}`
for `jiang2025devaluation`, ASR, doi `10.1177/00031224251362351`.

---

## The four requested sets

All four are present. Pole word counts as shipped:

| requested | file lists | words (listed / unique) |
| --- | --- | --- |
| moral / evaluation | `good-words` / `bad-words` | 22 / 22 · 23 / 23 |
| potency | `strong-words` / `weak-words` | 19 / 19 · 19 / 19 |
| prestige | `prestige-words` / `common-words` | 14 / 14 · 14 / **13** |
| liveliness | `active-words` / `passive-words` | **5** / 5 · **5** / 5 |

The file ships **14 lists** in total; the four above plus `female`/`male`,
`education`/`uneducation`, `affluent`/`poor`.

## Osgood originals vs Jiang additions

Marked at the level the package supports, which is the **dimension names**, not
the word lists:

| dimension in code | poles | Osgood? |
| --- | --- | --- |
| `evaluation` | good / bad | **Osgood E** |
| `potency` | strong / weak | **Osgood P** |
| `activity` | active / passive | **Osgood A** |
| `prestige` | prestige / common | Jiang addition |
| `gender` | female / male | Jiang addition |
| `education` | education / uneducation | Jiang addition |
| `income` | affluent / poor | Jiang addition |

**Caveat, and it matters for how these get described.** The three EPA
dimensions carry Osgood's names and poles, but the shipped word lists are
**not Osgood's scale items** — Osgood's instrument is bipolar adjective
*rating scales*, these are expanded centroid vocabularies.

**Provenance, from the appendix — this corrects my first reading.** The
replication *repository* carries no citation for the words: none in
`dimension-words.txt`, `embeddings.py` or the notebook. The **appendix
does**, at B.1 / Table S2:

> "When compiling the list, I mainly refer to the work of Kozlowski et al.
> (2019) and Van Loon and Freese (2023), who relied on multiple thesauri,
> including three contemporary thesauri: Bartlett's Roget's Thesaurus,
> Oxford Thesaurus, and Webster's Collegiate Thesaurus; and two historical
> thesauri (Roget 1911; Smith 1910). I also expand the list of words that
> may encode cultural association with women or men..."

The words descend from **Kozlowski et al. 2019 and Van Loon & Freese 2023
via thesauri, plus Jiang's own expansions** — not from Osgood. "Osgood
original" holds for the *dimensions* and for nothing else. My earlier line
that the provenance was unattributed was true of the repository and wrong
about the package as a whole.

**And the shipped lists do not match the appendix's.** Appendix Tables
S2–S4 document pairs — `pure/impure`, `holy/unholy`, `deep/shallow`,
`hot/cold` among others — that are **absent from `dimension-words.txt`**. A
run from the shipped file uses different centroids from the ones the paper
describes. See [`../supplement-placement/`](../supplement-placement/).

---

## Finding: the `moral` dimension is not in the package

`code/measures/embeddings.py:161` maps

```python
"moral": ["moral-words","immoral-words"],
```

**Neither list exists in `dimension-words.txt`.** They appear nowhere in the
repository except as these dict keys (and the same keys in the
`.ipynb_checkpoints` copy). Demonstrated, not inferred:

```
gender       OK
prestige     OK
education    OK
income       OK
moral        KeyError -> missing moral-words, immoral-words
evaluation   OK
potency      OK
activity     OK
```

**This does not break the paper.** `distance.ipynb` computes seven
dimensions — prestige, potency, income, gender, evaluation, education,
activity — and never calls `moral`. The key is a dead code path that would
raise if called.

**But it settles a naming question that matters for task 3.** The paper's
"moral standing" is the **`evaluation`** dimension (good/bad, Osgood E).
`moral` and `evaluation` are not two axes with one missing; there is one
axis and the code carries a vestigial second name for it.

## Data-quality observations on the shipped lists

- `common-words` lists **`humble` twice** — 14 tokens, 13 unique. The
  centroid is computed over the listed tokens, so `humble` carries double
  weight against the prestige pole.
- `poor-words` lists **`cheap` twice and `indigence` twice** — 39 listed, 37
  unique.
- `good-words` 22 vs `bad-words` 23 — poles are **unbalanced by one**.
- `active-words` / `passive-words` carry **5 words each**, against 39 for
  income. The liveliness axis rests on `fast lively loud sharp active` vs
  `slow quiet silent static calm`.
- `poor-words` contains the bare token **`skin`**, which reads as a
  truncation artifact rather than a poverty term.
- `affluent-words` mixes person-properties with **goods-properties**
  (`expensive`, `costly`, `exorbitant`, `invaluable`, `priceless`).

None of these is fatal and all of them move a centroid. They are recorded
because the drift check reads distances against these centroids.

---

## Task 2: BLOCKED — embeddings are not reachable

`data/embedding vectors/README.md` in the package:

> Due to the file size limit, the embeddings are uploaded to the dropbox
> folder [COCHA](...) and [Ngram](...).

The repository ships **no vectors** — that directory contains only the
README. Both Dropbox hosts are refused by the egress policy:

```
www.dropbox.com            CONNECT tunnel failed (curl 56)
dl.dropboxusercontent.com  CONNECT tunnel failed (curl 56)
```

The **HistWords fallback is also blocked**: `nlp.stanford.edu` is refused
the same way. So there is no substitute instrument available either, and
the DIFFERENT INSTRUMENT log entry is not needed — nothing to log it
against.

Task 2 does not proceed. Seed sets alone cannot produce a drift check.

---

## Task 5 blocker: RESOLVED — Ngrams reachable, COHA not

| host | status |
| --- | --- |
| `storage.googleapis.com` (Google Books Ngrams) | **REACHABLE** |
| `raw.githubusercontent.com`, `github.com` | REACHABLE |
| `pypi.org` | REACHABLE |
| `wenhaojiangsoc.github.io` | 403 policy denial |
| `www.dropbox.com`, `dl.dropboxusercontent.com` | 403 policy denial |
| `nlp.stanford.edu` (HistWords) | 403 policy denial |
| `www.english-corpora.org` (COHA/COCA) | 403 policy denial |
| `books.google.com` | 403 policy denial |

Google Books Ngrams **v3 (20200217), eng-us** is live and serving real data:

```
curl -sSI "https://storage.googleapis.com/books/ngrams/books/20200217/eng-us/2-00000-of-00365.gz"
# HTTP/2 200, content-length: 544942904
```

Shard counts read from the published manifests:

| order | shards | ~compressed total at shard-0 size |
| --- | --- | --- |
| 2-gram | 365 | ~199 GB |
| 3-gram | 4 178 | ~2.3 TB |
| 4-gram | 3 936 | ~2.1 TB |
| 5-gram | 11 145 | ~6.1 TB |

**Reachable is not tractable, and the gap is large.** Available disk in this
session is **30 GB**. The 2-gram set alone is ~6.6× that; 5-grams are ~200×.
Shards are hash-partitioned, so a target vocabulary does **not** localise —
a filtered pass needs every shard.

What is feasible: **stream-and-filter**, never storing a shard. 2-grams
(~199 GB transferred) is a long batch job, not a session. 5-grams (~6.1 TB)
is not a batch job either at any plausible rate here.

**Two structural limits on Ngrams for the predicate scan**, independent of
size:

1. **No document context and no parse.** An n-gram gives adjacency, not
   dependency. `woman` + adjective within 5 tokens is approximable; a
   predicate attaching across a copula or a relative clause is not.
2. **Type-level counts only.** There is no way to condition on a *work
   domain* held constant, which the method requires — the corpus carries no
   document, genre or topic field to hold anything constant by.

Point 2 is the harder one. It is not a size problem and more n-grams do not
fix it.

CC0.
