# CLAIM TABLE — clustering-axes

`CA_001..CA_010` for the delivered `ROUTES.md` and `style_index.py`,
both landed verbatim and modified by nothing.

Prefix note: `constraint-assembly/` also uses `CA_`. These are
`clustering-axes` claims and are cited with the folder name.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered material.

**No agent corpus is reachable from this environment.** Every
measurement below is taken on text already in this repository, and
every finding is a property of the instrument rather than of any
corpus. Nothing here is a statement about whether agents cluster on
style.

---

### CA_001 — the defect the routes address is real and correctly named

*The instrument is a model, so it inherits whatever that model
correlates with. The study cannot separate "agents cluster on X" from
"the scorer reads X."*

That is `criterion-symmetry`'s shape, which the document names itself,
and it is `null-harness`'s known-truth-first invariant stated for a
clustering variable. The response — build the criterion out of
countable features so a different lab with a different model gets the
same numbers — is the right response, and `style_index.py` honours it:
four stdlib imports, no network, no model, asserted here over the
module's own source.

**Falsifier:** a model call anywhere in the measurement path.

**Status: SUPPORTED.**

---

### CA_002 — the shipped `--delta` command is 92% four unnormalised features

The design's core is the function-word profile: 83 topic-blind rates,
the thing the whole instrument rests on. Measured on five texts from
this repository, the no-corpus L1 that `--delta` computes splits:

    UNNORMALISED shape      92.57%     mean_sent_len, sent_len_sd,
    other rates              4.75%     mean_line_len, mean_word_len
    function words           2.15%
    punctuation              0.29%
    trigrams                 0.24%

`sent_len_sd` alone is 45.7% of the distance and `mean_sent_len` 29.3%.

The cause is units. The rates are per-token or per-character and sit
around 0.01; `mean_sent_len` is words per sentence and sits around 20.
An L1 sum over both is three orders of magnitude out of balance, and the
83 features carrying the design's argument are a rounding error against
four carried in their raw units.

Checked across every pair, not one — a first version fixed a threshold
from a single observation and went red on the next pair.

**Falsifier:** a corpus where the shape features do not dominate the
unnormalised sum, which would mean the imbalance is this repository's
prose rather than the units.

**Status: SUPPORTED.**

---

### CA_003 — the fix is one argument, it is already implemented, and the CLI never passes it

`delta(a, b, corpus=None)` takes a corpus and z-normalises over it.
That is Burrows's Delta, and it exists precisely to stop this. Same
pair, same features, corpus supplied:

    function words          60.32%      (from  2.15%)
    punctuation             15.63%
    trigrams                12.36%
    other rates              8.76%
    UNNORMALISED shape       2.94%      (from 92.57%)

**The z-normalisation completely reverses which features carry the
distance**, and it puts the topic-blind core back in charge.

`main()` calls `delta(vecs[0], vecs[1])` with two arguments. Read from
the AST — every `delta` callsite in the module, and none passes a
corpus — so the documented command never reaches the branch. The
docstring's hedge, *"falls back to raw L1 — weaker, still model-free"*,
understates it: the fallback is not a weaker version of the same
measurement, it is a different measurement dominated by exactly what
the normalisation removes.

Cheapest possible repair: `--delta` over two files has no corpus to
build, so the honest form is a third mode that takes a directory,
builds the corpus from it, and reports pairwise Delta — which is what
R1's procedure needs anyway, since R1 clusters a population.

**Falsifier:** a callsite passing a corpus.

**Status: SUPPORTED — the function is right and unreachable.**

---

### CA_004 — two style vectors do not live in the same feature space

The trigram block is `tri.most_common(40)` — the forty most common
trigrams **of that text** — so the feature names differ per document.
Across five repository texts:

    a=159  b=159  shared=136 to 146  union=172 to 182

`delta` averages over `set(a) & set(b)`. So `d(a,b)` and `d(a,c)` are
means over different feature sets with different denominators, and the
distances are not on one scale. For a pairwise distance feeding a
clustering — which is R1's entire procedure — that is load-bearing.

The non-trigram features are identical across every pair; the whole
difference is the per-text block. Fix is the same shape as `CA_003`'s:
choose the trigram vocabulary **once over the corpus**, not per
document.

**Falsifier:** a pair whose non-trigram feature sets differ, which
would mean the cause is elsewhere.

**Status: SUPPORTED.**

---

### CA_005 — no edge case raises, and empty input returns a vector

    empty              119 features        only punctuation   128
    one char           119                 only newlines      120
    one word           122                 unicode            126
    no punctuation     158

Every guard holds — `n = len(toks) or 1`, `lines or [""]`, `chars =
len(text) or 1`, `_sd` returning 0.0 below two points. Nothing raises,
nothing divides by zero, every value is a number.

Worth stating because a real crawl contains all seven, and this is the
part of the module that a corpus would hit first.

**Falsifier:** an input that raises.

**Status: SUPPORTED — and it is the delivered module's strongest
engineering.**

---

### CA_006 — the stated 159 is exact, and it is a ceiling

`ROUTES.md` states *"159 countable features"*. Measured: **159** on any
text of ordinary length, and the blocks add up exactly — 83 function
words + 19 punctuation marks + 40 trigram slots + 17 shape and rate
features.

On `the cat sat` it is 122, and the shortfall is entirely trigrams. So
159 is the ceiling rather than a constant, which matters for `CA_004`
and does not undercut the claim.

Recorded because a stated count that holds exactly is the less common
outcome in this repository, and it should be said when it happens.

**Falsifier:** an ordinary-length text yielding other than 159.

**Status: SUPPORTED.**

---

### CA_007 — the Burrows attribution covers the distance, not the feature list

`ROUTES.md`: *"Burrows's Delta is 30 years old and uncontested, so the
instrument does not have to be defended."* The module: *"This is the
Burrows's Delta feature set — established, pre-existing, model-free."*

The **distance** is Burrows's and the defence transfers to it. The
canonical feature set is the *N most frequent words of the corpus*, not
a fixed function-word list — the list is a different, also established,
stylometric choice, and it is not the one the name carries.

The difference is not cosmetic and it lands on `CA_003`: corpus-derived
frequent words require a corpus, and requiring a corpus is exactly what
would have made the CLI take the normalised path.

**Falsifier:** a source defining Burrows's Delta over a fixed
function-word list.

**Status: SUPPORTED — the method is uncontested, the sentence about
the feature set is loose.**

---

### CA_008 — `--delta` with one file silently emits a vector instead of a distance

    one file            rc=0   the vector
    two files --delta   rc=0   the delta
    one file --delta    rc=0   the vector, no delta, no message
    missing file        rc=1   FileNotFoundError
    no argument         rc=0   {}

`if "--delta" in argv and len(vecs) == 2` falls through when the count
is wrong, so a caller who asks for a distance and mistypes a path gets
a style vector at exit 0. `{}` on no arguments is the same shape: a
malformed invocation is indistinguishable from a successful one.

Fourth instance in four folders — `CC_004`, `CA_005`
(constraint-assembly), `FM_042`, `MV_006` — and the second that is
silent rather than a traceback.

**Falsifier:** either path exiting non-zero or naming what was wrong.

**Status: SUPPORTED.**

---

### CA_009 — R4 is called a reanalysis and needs the model arm run

`ROUTES.md` on R4: *"both corpora already exist and are already paired.
Nothing new to collect."* and *"It is a reanalysis, not a study."*

True of the **corpora** and not of the **scoring**. Two of the four
cells are the model-scored criterion, which means running a zero-shot
classifier over both corpora — API credits, a model in the loop, and a
scoring pass whose cost scales with the corpus. What already exists is
the text and the pairing; what does not exist is the score on the human
side.

That does not move R4 down the order — the 2x2 is still the highest
finding-per-effort item and it is still the only route that tests the
instrument rather than the population. It moves R4's floor from
*nothing* to *one scoring pass*, which changes who can pick it up.

**Falsifier:** the human-corpus scores already being published, which
would make the sentence exactly right.

**Status: SUPPORTED, and it does not change the order.**

---

### CA_010 — every literature fact is carried and unchecked

He et al. 2023 (N=31,764), Zhu et al. 2025 (65K agents, 7.7M posts),
Fadaei et al. 2026 (70K agents, 140M posts, GPT-4o-mini scoring),
Hashemi et al. 2026 (neighbour similarity rising ~6x while backstory
similarity decays).

None is verified here. This environment's egress is an allowlist and
every one is outside it — the `MS_004` / `OE_017` / `MV_009` status,
now the fifth folder carrying a literature claim it cannot check.

Nothing in `CA_001..CA_009` rests on any of them. They are properties
of the module's arithmetic, its feature sets, its edge behaviour, its
CLI, and two sentences in the routes document.

The Hashemi result is the one worth checking first if egress opens: the
document itself calls it *"the most useful thing already on the table"*
and its own Open section notes that no route uses it. A decoupling
between assigned identity and neighbour convergence is a measured
handle, and a handle nothing uses is the cheapest gap on the page.

**Falsifier:** any of the four resolving to different numbers.

**Status: UNVERIFIED, and load-bearing on nothing here.**
