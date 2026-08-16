# CLAIM_TABLE — declared-frame

Claims from [`THE_DECLARED_FRAME.md`](THE_DECLARED_FRAME.md) and
[`check_frame.py`](check_frame.py), and from the audit here.

`who` follows the [`claim-audits/`](../claim-audits/) convention:
**D** = the drop's own claim, **A** = an audit claim added here.

## REFUTATION_PROTOCOL

1. A failed check updates the **claim**, not the tool. `check_frame.py` and
   the doc are checked in verbatim and are not retuned to preserve any entry
   here.
2. Nothing here is a claim about any domain a frame block is attached to.
   The block is an instrument; this folder audits the instrument.

---

## DF_001 — the six-field split is the contribution and it holds

**who:** D · **status:** SUPPORTED

The fields are not interchangeable, and `compare()` treats them in three
distinct ways:

```
boundary          core -- must match
horizon           core -- must match
who_counts        core -- must match
logic             separate mismatch line
sign_source       recorded, never compared
observer_access   recorded, never compared
```

That split is right. `sign_source` and `observer_access` are not
comparability conditions — two results can share a boundary and disagree
about which direction is better, and the disagreement is legible precisely
because both declared it. Making them core would refuse comparisons that are
sound.

**Falsifier:** a case where two results share all three core fields and are
still not comparable. That would mean the core set is incomplete.

**Evidence:** `frame_audit.py` §4.

---

## DF_002 — the checker inverts the rule the doc calls load-bearing

**who:** A · **status:** SUPPORTED

The doc states one rule as load-bearing:

> unpopulated field → visible gap, explorable
> omitted field → invisible, reads as absence
>
> "Omitting the field converts an open question into a settled one by
> silence."

So omission is the worse of the two. In `compare()` it produces the **more
confident** verdict:

```
core field `horizon` on side B:
  omitted      NOT DIRECTLY COMPARABLE      rc 1
  'unknown'    UNDETERMINED                 rc 0
```

Mechanism: `compare()` reads `str(a.get(f, "")).strip()`, so a missing field
becomes `""` and is compared as a value. The `unknown` branch is checked
first and never reached.

The tool does exactly what the doc warns against — it settles the question
by silence — in the function the doc ships to prevent that.

**Fix:** three lines. Treat a missing core field as undetermined, labelled
omitted rather than declared, so the block-level `OMITTED` finding and the
comparability verdict agree.

**Falsifier:** show that a missing core field should be read as a concrete
differing value. The doc argues the opposite in its own load-bearing rule.

**Evidence:** `frame_audit.py` §1.

---

## DF_003 — comparability is exact string equality on free text

**who:** A · **status:** SUPPORTED

Two frames whose boundary differs only in clause order are reported
`NOT DIRECTLY COMPARABLE`.

This is the inverse of the classifier failure in
[`measurement-fork/`](../measurement-fork/): there a token classifier
**over**-matched and marked questions covered that no probe reached. Here
exact equality **under**-matches and marks frames different that are the
same.

Under-matching is the safer direction — refusing a comparison costs less than
licensing a wrong one. The problem is that there is no band for it. A textual
difference gets a verdict that reads as substantive.

**There is no string fix.** Whether two free-text boundaries denote the same
accounting is a judgement. The honest verdict for differing text is the one
the doc already uses for its own middle band: not resolved here.

**Falsifier:** a normalisation that collapses reworded-but-identical
boundaries without collapsing genuinely different ones. Whether that exists
is a measurement; the naive attempts (lowercase, sort tokens) will collapse
`"excludes fabrication"` and `"includes fabrication"`, which is the failure
that matters.

**Evidence:** `frame_audit.py` §2.

---

## DF_004 — the exit code reports block validity, not comparability

**who:** A · **status:** SUPPORTED

```
two complete blocks, genuinely different frames   rc 0
one block missing a field                         rc 1
```

`rc` tracks whether the blocks are well-formed, not whether the results
compare. Defensible — incomparability is a finding, not an error — and
undocumented. A caller scripting `check_frame.py a b && use_both` gets a
pass on two results the tool has just said do not compare.

**Fix:** document `rc`, or add a distinct code for NOT-COMPARABLE so the
verdict is scriptable.

**Evidence:** `frame_audit.py` §3.

---

## DF_005 — the worked pair reaches the void-ratio verdict by a second route

**who:** A · **status:** SUPPORTED

`frames/panel_conversion.json` and `frames/leaf_conversion.json` differ on
all three core fields — the first excludes fabrication, mining, smelting,
transport, installation, maintenance and decommission; the second puts all
of them inside the same photon budget.

So the efficiency ratio between them is a frame difference, and
`check_frame.py` reports it as one.

That is [`measurement-fork/`](../measurement-fork/)'s VOID RATIO cell
arriving by a different route: there, two quantities do not divide because
their `object_of` differs; here, two results do not compare because their
boundaries differ. `reasoning-gate/`'s `G-DIM` is the same check at report
time. Three tools, three stages, one rule.

**Falsifier:** a boundary declaration under which the two are comparable.
Building it means putting the panel's fabrication, transport and disposal
inside the accounting, which is the point the declaration surfaces.

---

## DF_006 — nothing has been attached to a real result

**who:** A · **status:** UNVERIFIED

The two frames here are written from the drop's own worked example. The
load-bearing question for the block is untouched: **does declaring the frame
change what anyone does?**

The stated benefit is that frame disagreements stop being argued as data
disagreements. That is a claim about a process, and the measurement is
whether two parties who disagree, given both blocks, locate the disagreement
faster than without.

**Falsifier:** run it. Two results, two declared blocks, one disagreement,
and a record of where the parties looked first.

---

## DF_007 — every field in the block is switchable, so nothing adjudicates

**who:** A · **status:** SUPPORTED

The six fields are all **layer 1** in the sense the source notes give it:
cultural frames, many, each internally valid, switchable, none privileged.
`compare()` is right not to rank them — two results that count different
people are two accountings, and neither is wrong.

The cost is visible in one run. `layer_zero.py` §1 puts two pairs through
the unmodified `compare()`:

| pair | differs on | verdict |
| --- | --- | --- |
| A | `who_counts` — a pure convention | `NOT DIRECTLY COMPARABLE` |
| B | a `boundary` that does not close — an input that physically crossed it entered the budget as zero | `NOT DIRECTLY COMPARABLE` |

Same verdict. The tool has no way to say that one of them fails to
conserve, because conservation is not one of the six fields and there is
nothing in the block that is not a declaration. So the position *"this
frame is internally coherent and does not match the shape"* is not
statable by the instrument built to make frames comparable.

**A seventh free-text field does not fix it.** Comparability here is string
equality over declarations, so two frames declaring incompatible physics
land back on `NOT DIRECTLY COMPARABLE`, which is where they already are.
The repair is an **evaluated** term rather than a compared one: an
inputs/outputs list per frame, with units, and one check for closure. Two
numbers and a subtraction — the `../reasoning-gate/` `G-RES` shape, where
the author declares a pair and the tool does arithmetic on it.

`K18` in `../measurement-fork/` specifies exactly that audit (name every
input and every disposal path, which are inside the boundary, which
outside, and who set the line). It sits there as a widen move pointed at a
design. Here it would be a check.

**Falsifier:** a free-text seventh field, or any string-compared field,
that returns a different verdict for pair B than for pair A. If declaration
alone can carry the distinction, the evaluated-term argument is
unnecessary.

**Evidence:** `layer_zero.py` §1–§2.

---

## DF_008 — the v2 rewrite makes the verdict scriptable and leaves three findings standing

**who:** A · **status:** SUPPORTED

`v2/check_frame.py` is a rewrite, not a patch. `compare()` returns a
`(verdict, why)` pair instead of printing, which is a real gain: the verdict
is scriptable for the first time.

| finding | v2 |
| --- | --- |
| `DF_002` omission is the more confident verdict | **unchanged** |
| `DF_003` comparability is exact string equality | **unchanged** |
| `DF_004` exit code tracks nothing useful | **worse** — rc=0 on every path, where v1 returned 1 on a malformed block |
| `DF_007` nothing in the block adjudicates | **unchanged** |

`DF_002` is now visible in a single stdout: the tool prints *"omission reads
as absence of the issue"* and three lines later issues the settled verdict on
that field. Warning and verdict contradict each other in one run.

`DF_004`'s repair is one line and is **only reachable because of the
rewrite** — route the returned verdict into the exit code
(`DIRECTLY COMPARABLE` → 0, `LOGIC MISMATCH` / `NOT DIRECTLY COMPARABLE` → 1,
`UNDETERMINED` → 2).

**New in v2:** the single-verdict return preempts. A pair that is both
undetermined on one core field and substantively different on another comes
back `UNDETERMINED` with the difference unreported; v1 printed both. The
precedence is right — an unknown field should not be resolved into a
comparability claim — and the loss is in the return TYPE. A verdict plus a
findings list keeps both, which is the shape `../reasoning-gate/` already
uses.

**Falsifier:** a caller for whom the collapsed verdict is sufficient — one
that never needs to know a second core field differed once the first was
undetermined. Then the return type is adequate and this is decoration.

**Evidence:** `v2/v2_audit.py` §1–§4.

---

## DF_009 — the scanner returns zero on the drop's own worked example

**who:** A · **status:** SUPPORTED

`v2/patterns.json` turns `../uninstrumented/`'s register into regex triggers
over text, with a `check` question per mechanism. It adds an eighth
mechanism, `PROXY SUBSTITUTION`.

The register's canonical `BUDGET_BOUNDARY` case is leaf vs panel, and this
drop ships both halves of it as declared-frame examples. **The scanner
returns zero candidates on both.** No corpus, no threshold, no adjudication.

```
the register's own VISIBLE AS line   -> SCORED AS WASTE ('inefficient')
the delivered result string          -> NO HIT
stated as a comparative              -> BUDGET BOUNDARY ('more efficient than')
stated with the noun                 -> BUDGET BOUNDARY ('conversion efficiency')
```

**(a)** The triggers catch the RHETORIC of a comparison, not the comparison.
Two numbers side by side with no comparative — the usual form in a result
line — is invisible to all eight `BUDGET BOUNDARY` triggers.

**(b)** The register's own phrasing fires under the WRONG mechanism, so a
reader triaging that hit is handed the wrong `check` question.

Both repairs are cheap: a trigger for the bare-numbers form, and letting
mechanisms co-fire — which is `UNI_003` arriving in the scanner.

**Falsifier:** a `BUDGET_BOUNDARY` trigger that fires on
`"silicon PV converts ~22% of incident photons; leaf converts ~1-2%"`
without also firing across a corpus at a rate that breaks the triage load in
`DF_010`. The two constraints are what make this non-trivial.

**Evidence:** `v2/scan_audit.py` §1.

---

## DF_010 — triage load is low; no precision figure is reportable from this repo

**who:** A · **status:** SUPPORTED (load) · UNVERIFIED (precision)

`patterns.json` states its own standard — *"every hit is a candidate for
triage, not a finding"* — so the binding quantity is not precision but how
many `check` questions a human must answer per unit of text.

**≈1.0 candidate per 1000 words** over ~300k words of repository markdown;
dropping word boundaries costs roughly 40% more for no obvious gain. A
5000-word document arrives with about five questions attached. Affordable.

**The precision figure is not reported and will not be from this corpus.**
This repository is a corpus *about* measurement failure written in the
triggers' own vocabulary: `UNVERIFIED` is a claim-table status code here, so
`(unverified|uncorroborated)` fires dozens of times on the repo's own
verdict vocabulary. `benchmark`, `compliance`, `proxy for`, `tacit` are all subject
terms. Scoring a false-positive rate on it would measure the corpus.

Two corpus-conditional numbers, neither of which grades the trigger list:
**4 triggers produce ~57% of all candidates**, and **more than half of the 69
triggers never fire**. `SCALAR DEMAND` has 7 of 8 silent because there are no
survey instruments here — a silent trigger on the wrong corpus is not a dead
trigger.

One trigger is the list's own problem: `slack` is a four-letter common noun
with a proper-noun homograph, and its hits mix Slack the product, *the
slack rope*, a code identifier, and genuine idle-capacity usage.

**An expectation that was checked and failed:** use-mention was expected to
dominate — a surface-word scanner should not distinguish a document
exhibiting a failure from one describing it. `uninstrumented/README.md`
returns 2 hits in 986 words and `v2/FRAME.md` returns none. The triggers are
written in the vocabulary of the failing document, not of the mechanism, and
the two barely overlap. That separation is load-bearing and is not visible
from reading the file.

**The corpus is live, and writing the audit changed it.** `v2/README.md`
quotes the triggers in order to discuss them, so it entered the corpus as
text — and moved five triggers from never-firing to firing, three of them the
`SCALAR DEMAND` triggers reported silent *because this corpus contains no
survey instruments*. That reading is still correct and they now fire on the
document explaining that they do not. Counts are a snapshot, not a fixture;
no exact figure is quoted outside the pinned sample. This is
`../anchor-interval/`'s moving reference occurring rather than being
described.

**Falsifier:** an outside corpus — one not about its own subject — scored
for precision. That is the measurement this claim exists to say has not been
run.

**Evidence:** `v2/scan_audit.py` §2–§5.

---

## Repairs

`DF_002` and `DF_004` are **repaired in `v2/check_frame.py`**. `DF_003` and
`DF_007` are not, and are not defects — they are limits on what the tool can
promise, recorded rather than papered over.

### `DF_002` — omission no longer produces the more confident verdict

`compare()` gained a three-line `omitted()` check that runs **before** the
unknown check:

```
side B        was                        now
omitted       NOT DIRECTLY COMPARABLE    UNDETERMINED   rc 2
'unknown'     UNDETERMINED               UNDETERMINED   rc 2
```

The doc says an omitted field *"converts an open question into a settled one
by silence"*, so it must not settle anything. It now returns the open verdict
and says which core field is missing, which matches the `OMITTED` warning the
same run already printed three lines above.

### `DF_004` — the exit code carries the verdict

```
DIRECTLY COMPARABLE      -> 0
LOGIC MISMATCH           -> 1
NOT DIRECTLY COMPARABLE  -> 1
UNDETERMINED             -> 2
```

`UNDETERMINED` is deliberately **not** 1. It is neither a pass nor a failure,
and a caller that treats it as either has resolved a gap the tool refused to
resolve. `check_frame.py a b && use_both` now stops on a pair the tool has
said does not compare.

This repair is only reachable because of the v2 rewrite — `compare()` returns
a value, so there is a verdict to route. `DF_008` recorded that as the
rewrite's real gain; this is it being spent.

### Not repaired, on purpose

`DF_003` — comparability is exact string equality on free text. There is no
string fix: whether two free-text boundaries denote the same accounting is a
judgement, and under-matching is the safe direction.

`DF_007` — nothing in the block adjudicates. That is the boundary of what a
frame-declaration instrument can do, and the repair is an evaluated term
(inputs/outputs with units, one closure check), not a seventh compared field.
