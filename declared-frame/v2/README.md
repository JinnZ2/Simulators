# declared-frame / v2

Second drop. Five files delivered, all **verbatim**:

| file | what it is |
| --- | --- |
| [`FRAME.md`](FRAME.md) | the frame document, v2 — adds **Cost** and **Growth** |
| [`check_frame.py`](check_frame.py) | a rewrite, not a patch — `compare()` returns instead of printing |
| [`patterns.json`](patterns.json) | **new** — eight mechanisms as regex triggers plus a `check` question each |
| [`examples/photosynthesis.json`](examples/photosynthesis.json) | the panel half of the worked pair |
| [`examples/tree.json`](examples/tree.json) | the tree half |

v1 stays at the parent level, unmodified, so both drops are inspectable as
delivered.

Added here, not delivered:

```
scan.py         run patterns.json over text  [RECONSTRUCTED -- no runner shipped]
scan_audit.py   grade the trigger set
v2_audit.py     what changed v1 -> v2, and which findings survive
```

```bash
python3 check_frame.py examples/photosynthesis.json examples/tree.json
python3 scan.py FILE [FILE ...]
python3 scan_audit.py
python3 v2_audit.py
```

Standard library only, deterministic.

---

## patterns.json — the register as a scanner

`../../uninstrumented/` is a register of seven mechanisms by which an
instrument's constitution keeps a quantity from appearing. `patterns.json`
turns it into something that runs over text: per mechanism, a set of regex
triggers and one `check` question a human answers to keep or discard the
hit. It adds an eighth mechanism, **PROXY SUBSTITUTION**.

Its own framing is load-bearing and is not a hedge to discount:

> Triggers are surface tells, not classifiers. Every hit is a candidate for
> triage, not a finding.

So the quantity that decides whether it is usable is not precision. It is
**triage load**.

### The result that needs no corpus

The register's canonical `BUDGET_BOUNDARY` case is leaf vs panel. This drop
ships both halves of it. The scanner returns **zero** on both.

```
examples/photosynthesis.json    0 candidates
examples/tree.json              0 candidates

the register's own VISIBLE AS line   -> SCORED AS WASTE ('inefficient')
the delivered result string          -> NO HIT
stated as a comparative              -> BUDGET BOUNDARY ('more efficient than')
stated with the noun                 -> BUDGET BOUNDARY ('conversion efficiency')
```

Two things, and the second is sharper.

**(a)** The triggers catch the *rhetoric* of a comparison — `more efficient
than`, `outperforms`, `orders of magnitude better` — not the comparison. Two
numbers placed side by side with no comparative is how the claim usually
appears in a result line, and that form is invisible to all eight
`BUDGET BOUNDARY` triggers.

**(b)** The register's own phrasing of the case fires under the **wrong
mechanism**. `inefficient` is a `SCORED AS WASTE` trigger, so a reader
triaging that hit gets handed the wrong `check` question — *what does it
return, and on what interval* — for a case whose question is *are both
budgets closed at the same boundary*.

Both repairs are cheap: a trigger for the bare-numbers form, and letting
mechanisms co-fire, which is `../../uninstrumented/` `UNI_003` arriving in
the scanner.

### Triage load

**≈1.0 candidate per 1000 words** over ~300k words of repository markdown.
Dropping word boundaries (`--raw`) costs roughly 40% more candidates for no
obvious gain.

A 5000-word document arrives with about five questions attached, not fifty —
the human step the design depends on is affordable.

Exact counts live in [`samples/scan_audit.sample.txt`](samples/scan_audit.sample.txt)
and are **not repeated here on purpose**. See *the corpus is live* below.

### An expectation that was checked and failed

Expected: a scanner keyed on surface words cannot tell a document
*exhibiting* a failure from one *describing* it, so `uninstrumented/README.md`
should light up entirely with false positives.

```
uninstrumented/README.md        986 w   2 hits
uninstrumented/CLAIM_TABLE.md   698 w   1 hits
declared-frame/v2/FRAME.md      246 w   0 hits
declared-frame/README.md        861 w   0 hits
```

It did not happen, and the reason is not visible from reading the file: the
triggers are written in the vocabulary of the **failing document**, not the
vocabulary of the mechanism. *"apparatus in the wrong channel"* is how the
register names `MODALITY`; *"failed to demonstrate"* is what a paper
exhibiting it says. The two barely overlap.

### No precision figure is reported, and why

This repository is a corpus **about** measurement failure written in the
triggers' own vocabulary. `UNVERIFIED` is a claim-table status code here, so
`(unverified|uncorroborated)` fires dozens of times on the repo's own
verdict vocabulary. `benchmark`, `compliance`, `proxy for` and `tacit` are all
subject terms.

Roughly **4 triggers produce ~57% of all candidates**, and **more than half
of the 69 triggers never fire at all**.

Both numbers are **corpus-conditional and neither grades the trigger list**.
`SCALAR DEMAND` has 7 of 8 triggers silent because this corpus contains no
survey instruments — `on a scale of`, `rate yourself`, `composite score` are
psychometrics vocabulary. A silent trigger on the wrong corpus is not a dead
trigger.

One trigger is the list's own problem rather than the corpus's: `slack` is a
four-letter common noun with a proper-noun homograph, and its hits are a mix
of Slack the product, *the slack rope*, a code identifier, and genuine
idle-capacity usage.

Scoring a false-positive rate here would measure the corpus. That
measurement needs an outside corpus and is the next thing to run.

### The corpus is live, and writing this page changed it

Sections 2–4 walk the repository's markdown as it stands when the script
runs. **This README quotes the triggers in order to discuss them, so it
entered the corpus as text**, and doing so moved five triggers from
never-firing to firing:

```
BUDGET BOUNDARY    orders of magnitude (better|more)
MODALITY           failed to (demonstrate|show|exhibit)
SCALAR DEMAND      (rate|rated|rating) (yourself|your|their|his|her)
SCALAR DEMAND      composite (score|index|measure)
SCALAR DEMAND      on a scale of
```

Three of the five are the `SCALAR DEMAND` triggers reported silent above
*because this corpus contains no survey instruments*. That reading is still
correct — there are none — and they now fire on the document explaining that
they do not fire.

So the counts are a **snapshot, not a fixture**. This is
`../../anchor-interval/`'s moving reference occurring rather than being
described: the measurement and its reference are not independent, and
reporting the number changed it. Freezing a corpus copy is the honest fix
and is not done here; quoting no exact counts on this page is the cheap one.

---

## check_frame.py v1 → v2

A rewrite. The main gain is real: `compare()` returns a `(verdict, why)`
pair instead of printing, so the verdict is **scriptable for the first
time**.

| finding | v1 | v2 |
| --- | --- | --- |
| `DF_002` omission more confident than `unknown` | present | **unchanged** |
| `DF_003` comparability is exact string equality | present | **unchanged** |
| `DF_004` exit code does not track comparability | rc=1 on malformed block | **worse — rc=0 on every path** |
| `DF_007` nothing in the block adjudicates | present | **unchanged** |

**`DF_002`.** `unknowns()` reads
`str(frame.get(f, "")).strip().lower() == "unknown"`, so a *missing* field
becomes `""`, is not `unknown`, falls through to the core diff and compares
as a value. v2 makes it worse to look at and easier to fix — both halves now
appear in one stdout, three lines apart:

```
b.json: OMITTED field 'horizon'. Write 'unknown' instead --
        omission reads as absence of the issue.

VERDICT: NOT DIRECTLY COMPARABLE
         differs on horizon -- this is a frame difference, not a finding
```

**`DF_004`.** Every case returns 0, including a malformed block that v1
caught. The repair is one line and is *only reachable because of the
rewrite* — route the returned verdict into the exit code:

```
DIRECTLY COMPARABLE      -> 0
LOGIC MISMATCH           -> 1
NOT DIRECTLY COMPARABLE  -> 1
UNDETERMINED             -> 2   (not resolved, not failed)
```

**New in v2 — the single verdict preempts.** A pair that is both
undetermined on one core field and substantively different on another:

```
v2:  UNDETERMINED
v1:  UNDETERMINED + NOT DIRECTLY COMPARABLE
```

The precedence is *right* — an unknown field should not be resolved into a
comparability claim — and the loss is in the return type, not the ordering.
A verdict plus a findings list keeps both, which is the shape
`../../reasoning-gate/` already uses: one status, and notes that do not
change it.

**`DF_007`.** `Cost` and `Growth` are both layer-1 additions. Nothing added
between versions *evaluates* anything, so a frame whose budget does not
close still scores identically to one that merely counts different people.

The `Growth` rule is worth stating because the drop already follows it:

> The format grows by adding a declared field, never by widening an existing
> one. Widening is the aggregation failure.

`patterns.json` adds `PROXY SUBSTITUTION` as an **eighth** mechanism rather
than widening one of the seven — the rule applied to a different artifact in
the same drop.

## Related

- `../../uninstrumented/` — the register `patterns.json` operationalizes;
  `UNI_003` (mechanisms are not mutually exclusive) is the co-firing repair.
- `../../null-harness/` — the invariant section 1 applies, and the reason
  sections 2–4 report no precision.
- `../../reasoning-gate/` — verdict-plus-findings is the return shape the
  precedence result argues for.
- `../layer_zero.py` — `DF_007`, still holding against v2.

CC0.
