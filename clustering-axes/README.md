# clustering-axes

Six exploration routes for finding what AI agents cluster on when the
clustering axis is **not imported from human social science**, plus a
model-free stylometric instrument for the cheapest of them.

Both delivered verbatim: `ROUTES.md` and `style_index.py`. Audit in
`style_audit.py`, which imports the module and reads the document and
modifies neither. Claims `CA_001..CA_010`.

## The argument, which holds

Existing agent-homophily work clusters on language, topic and gender
performance — three axes taken from human social science, none derived
from the substrate. In at least one case **the clustering variable is
itself a model's judgment**: a zero-shot classifier reads linguistic
features, assigns a score, and homophily is measured on that score. The
instrument is a model, so it inherits whatever that model correlates
with, and the study cannot separate *agents cluster on X* from *the
scorer reads X*.

`criterion-symmetry`'s shape, which the document names, and
`null-harness`'s known-truth-first invariant stated for a clustering
variable. The response — build the criterion from countable features so
a different lab with a different model gets the same numbers off the
same text — is the right response, and the module honours it: four
stdlib imports, no network, no model, asserted over its own source.

## What the audit found

**No agent corpus is reachable from here.** Everything below is
measured on text already in this repository, and every finding is a
property of the instrument rather than of any corpus.

**The shipped `--delta` command is 92% four unnormalised features.**

    UNNORMALISED shape      92.57%    mean_sent_len, sent_len_sd,
    other rates              4.75%    mean_line_len, mean_word_len
    function words           2.15%
    punctuation              0.29%
    trigrams                 0.24%

The 83 function-word rates are the topic-blind core the whole design
rests on, and under the shipped command they are a rounding error. The
cause is units: rates sit around 0.01, words-per-sentence around 20, and
an L1 sum over both is three orders of magnitude out of balance.

**The fix is one argument and it is already implemented.**
`delta(a, b, corpus=...)` z-normalises — that *is* Burrows's Delta, and
it exists to stop exactly this. Same pair, corpus supplied:

    function words          60.32%     (from  2.15%)
    UNNORMALISED shape       2.94%     (from 92.57%)

The normalisation completely reverses which features carry the distance.
`main()` calls `delta` with two arguments, so the documented command
never reaches the branch. Read from the AST, not by regex — a first pass
matched the function *definition* as a callsite.

**Two style vectors do not share a feature space.** The trigram block is
the forty most common trigrams *of that text*, so feature names differ
per document: 159 each, 136–146 shared. `delta` averages over the
intersection, so `d(a,b)` and `d(a,c)` are means over different feature
sets. For a pairwise distance feeding a clustering — R1's whole
procedure — that is load-bearing. Same fix as above: choose the trigram
vocabulary once over the corpus.

**Nothing raises.** Empty input, one character, only newlines, only
punctuation, unicode — all seven edges return a vector, every guard
holds. That is the module's strongest engineering and a real crawl hits
it first.

**The stated 159 is exact**: 83 function words + 19 punctuation + 40
trigram slots + 17 shape and rate features. It is a ceiling rather than
a constant — `the cat sat` gives 122, all of the shortfall trigrams.

Two smaller ones: the Burrows attribution covers the **distance**, not
the fixed function-word list (the canonical feature set is the *N most
frequent words of the corpus*, which would have required a corpus and
so would have forced the normalised path); and R4's *"nothing new to
collect"* is true of the corpora and not of the scoring, which moves its
floor from nothing to one classifier pass without moving it down the
order.

## Running it

    python3 clustering-axes/style_index.py sample.txt
    python3 clustering-axes/style_index.py a.txt b.txt --delta
    python3 clustering-axes/style_audit.py --selftest
    python3 clustering-axes/style_audit.py

Stdlib only, parses under Python 3.9, CC0.

Siblings: `criterion-symmetry/` (the instrument-only-measures-where-it-
was-built-to-look shape the routes name), `null-harness/` (R6 is its
known-null requirement for a clustering), `move-set/` (R5's note that a
finding with no human name scores as no finding is `MV_001`'s subject
from the other side), `nonidentity-census/` (`T1-1`, a word list
deciding word sense — the failure a model-free feature set avoids).
