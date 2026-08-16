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
