# CLAIM TABLE — CREDITING RATE (WORK ORDER L)

Prefix `CRD_` (`CR_` is taken by `claim-record/`). Statuses: SUPPORTED /
REFUTED / UNVERIFIED / OPEN, with the falsifier stated per claim.

---

**CRD_001.** The instrument returns different G values on two constructed
worlds that differ only in whether crediting follows the loanword bin
(`ETYMOLOGY_TRACKING` at gap 0.6; `CONTRIBUTION_TRACKING` at gap 0.0), so
the return is not constant.

*Falsifier:* a pair of worlds with different crediting-by-bin that return the
same value. *Status:* SUPPORTED on the fixtures (`--selftest`).

---

**CRD_002.** Unknown ordering is excluded and counted, never estimated: the
ten items the order names carry `null` attestation years and the run returns
`BLOCKED(insufficient_attested_ordering)` with `ordering_unknown = 10`.

*Falsifier:* any code path that fills a missing year or admits an item
without `ordering_source`. *Status:* SUPPORTED; pinned.

---

**CRD_003.** The blind is structural: a codings file carrying any field
whose name contains `loanword` is refused at load, and the bin meets the
coding only in `join()`.

*Falsifier:* a codings row reaching `join()` with the bin on it. *Status:*
SUPPORTED; pinned. Limit: the blind is a file rule, not a person rule — a
coder who has read `events.jsonl` is not blind, and nothing here can tell.

---

**CRD_004.** The N1 band brackets zero on the constructed worlds and the
`equal` known-answer case sits inside it; the band is a percentile of 2000
seeded label shuffles and the run is deterministic under a fixed seed.

*Falsifier:* a band that excludes zero on a world with equal rates.
*Status:* SUPPORTED on fixtures.

---

**CRD_005.** The pre-stated prediction (retained credited more) is a
DIRECTION only; the script refuses to run without `PREDICTION.md` and
prints its hash, so a change to the prediction after the fact changes the
hash every report carries.

*Falsifier:* a run with no prediction file. *Status:* SUPPORTED; pinned.

---

**CRD_006.** The method layer the order consumes (F branch set, G return
enum) is not in this repository; nothing in the tree carries `branch_set` or
a G enum. G is implemented locally as the five listed values plus one added
BLOCKED reason (`frame_undeclared`); F is emitted as `branch_set.json` in the
order's shape. `archive-siting-bias`, which the branch set links, is also
absent.

*Falsifier:* the layer landing; then this folder imports it and this claim
closes. *Status:* OPEN — named-and-absent, the shape this tree records.

---

**CRD_007.** `CONTRIBUTION_TRACKING` is decided by a stipulated cut
(`MISATTR_MAX = 0.2`) on the misattribution rate, and `MIN_PER_BIN = 3` is
stipulated too. Both are `[CHOICE]` constants printed in the report, with no
basis beyond being stated.

*Falsifier:* a basis for either number. *Status:* OPEN.

---

**CRD_008.** Nothing here is a statement about algebra, paper, printing,
or any tradition. Every real cell is unmeasured: no attestation ordering was
consulted, no corpus declared, no coding done. The instrument is built and
its return is shown to move on constructed data only.

*Falsifier:* a real run. *Status:* UNVERIFIED, and stays so until an operator
supplies the three inputs.

---

# Revision 2 — `CRD_009` onward

`WORK_ORDER_V2.md` delivered verbatim beside the first; `crediting_rate_v2.py`
built beside `crediting_rate.py`, which is unedited. Ids continue; nothing is
renumbered.

---

**CRD_009.** Revision 2 deletes the input `CONTRIBUTION_TRACKING` was read
off. v1 gated it on a misattribution rate — items whose narrative named the
receiving tradition as originator while the attested ordering said otherwise —
and revision 2 says `origination_vs_absorption` is coded *"from attested dates
only, never from narrative"*, which removes the narrative half and with it the
comparison. The revised schema carries **no contribution proxy at all**, so
that return is reachable only by stipulation, while fixture F2 requires it to
be returned on a contribution-tracking world. The order's own fixture list and
its own coding rule point different ways.

The replacement built here is the attested **priority margin**
(`first_attested_receiving - first_attested_source`) read as a Spearman
correlation against crediting — the only contribution-shaped quantity the
revised schema still carries. It is `[CHOICE 8]` with `MARGIN_RHO_MIN = 0.5`,
and it is not in the order.

*Falsifier:* a contribution proxy in the revised schema that this reading
missed. *Status:* SUPPORTED on the order's text; the replacement is a CHOICE.

---

**CRD_010.** The pre-stated ordering and the discriminator are not
independent, and the two branches of the discriminator are not symmetric.
`visible > technical_only >= not_retained` already encodes the visibility
hypothesis: the branch where `technical_only` tracks `not_retained` sits
INSIDE the ordering, and the branch where it tracks `visible` violates
`visible > technical_only` and REFUTES it. One branch confirms the pre-stated
prediction and the other refutes it; they are not two outcomes of one neutral
test. Recorded in `PREDICTION_V2.md` before any run rather than found after
one.

*Falsifier:* a reading of the ordering under which both branches leave it
intact. *Status:* SUPPORTED, from the ordering's own arithmetic.

---

**CRD_011.** The second comparison is NON-STRICT, so the ordering holds with
`technical_only` anywhere from `not_retained` up to just below `visible` and
cannot by itself locate the discriminating bin. `position = (r_tech - r_not) /
(r_vis - r_not)` is reported for that, and its cut (`POSITION_LOW 0.33`,
`POSITION_HIGH 0.67`) is `[CHOICE 4]` — the order names the two readings and
no boundary between them. `BETWEEN` is a first-class reading and F5 returns
it.

*Falsifier:* a boundary stated in the order. *Status:* OPEN — the cut is
stipulated.

---

**CRD_012.** `position` is UNDEFINED, never 0.5, when the outer bins do not
separate by `POSITION_MIN_SPREAD` (`[CHOICE 5]`). A midpoint computed on a
denominator near zero is a number about the noise, and it would be
indistinguishable from a measured halfway case. Registered in
`tools/known_answer.py` with five cases: 0.0, 1.0, 0.5 measured, and two
`None`s (no spread, empty middle bin).

*Falsifier:* a `position` value returned on outer bins that do not separate.
*Status:* SUPPORTED; pinned in the registry.

---

**CRD_013.** `model_authored` is three-valued and absent is not false. A list
header with no such field is refused at load, and a `null` returns
`BLOCKED(model_authored is None; absent or null is not false)`. Reading an
absent provenance field as `false` is the contamination going unreported,
which is the one failure a gate against contamination cannot commit.

*Falsifier:* a run proceeding on a list whose header does not declare it.
*Status:* SUPPORTED; pinned.

---

**CRD_014.** `FRAME_ASYMMETRIC` has two readings, and the order states one of
them. The stated rule is that all bins come from the same side. Its own
argument implies a second: a list that is *uniformly* `language_side` passes
the stated rule and still cannot have produced its own `not_retained` bin,
because no linguistic index enumerates a word that did not survive. Both are
implemented, with distinct reasons, and both are exercised.

*Falsifier:* a language-side enumeration of items whose loanword did not
survive. *Status:* SUPPORTED on the order's own argument.

---

**CRD_015.** The blind moved with the revision and stayed structural. v1 kept
the BIN off the coding file; revision 2 says the item name carries its own
bin, so the NAME is what has to be off it. A depth record carrying an `item`
field is refused at load, and the join is on `entry_id`. The limit is
unchanged from v1 and is stated: this is a file rule, not a person rule.

*Falsifier:* a depth record reaching `join()` with a name on it. *Status:*
SUPPORTED; pinned.

---

**CRD_016.** The alias list is the one judgement inside a measure the order
calls mechanical. The order's reason — a leak is harmless because there is no
judgement — holds for the MATCH and not for the LIST: a tradition named by a
word the list lacks reads as uncredited, and nothing here separates that from
a description that does not name it. The list lives in the data file so it can
be diffed, and the render prints its per-tradition size.

*Falsifier:* an alias list derivable rather than declared. *Status:* OPEN.

---

**CRD_017.** The sentence splitter's failure rate is a function of N2's own
control variable. `first N sentences` needs a splitter; an unguarded one
breaks on date abbreviations (`c. 830 CE`), which are commoner in descriptions
of older items — so the measurement error is CORRELATED WITH THE CONTROL, the
one direction it must not take. Both splitters ship and the module reports how
many crediting decisions move between them, broken down by antiquity band. On
`v2.events.splitter`, 8 of 16 items move and all 8 are in the older band; on
F1 the figure is 0 of 17, which is a property of that corpus and not evidence
that the failure mode is absent.

*Falsifier:* an abbreviation-carrying corpus where the moved set is not
concentrated by date. *Status:* SUPPORTED on the constructed corpus.

---

**CRD_018.** The order's NOTE is honoured structurally rather than as a
caveat: the Spearman correlation of the visibility ordinal with antiquity and
with intermediary count is printed ABOVE the rate table, before any fit. On
F5 it reads −0.598 against the date, which is the confound the fixture plants
and the reason that run returns `UNKNOWN_measurable`.

*Falsifier:* a render placing the correlation after the gap. *Status:*
SUPPORTED.

---

**CRD_019.** All seven returns are reachable and all seven occur in the
selftest. `ambiguous` is a bin and never an assignment: ambiguous items are
carried, counted, and enter no rate and no shuffle, asserted against the F1
fixture. `outer_gap` returns `None` for an empty bin and `0.0` for two bins
measured equal.

*Falsifier:* a declared return no path reaches, or an ambiguous item inside a
scored bin. *Status:* SUPPORTED; 50 checks in `--selftest`.

---

**CRD_020.** `load_frame`, `ordering_state` and `outside` are IMPORTED from
`crediting_rate.py` and `spearman` from `readout-count/readout_count.py`;
nothing is copied. v1 is not edited, and the two modules plus the two orders
stay inspectable side by side under this tree's supersession convention.

*Falsifier:* a duplicated definition in `crediting_rate_v2.py`. *Status:*
SUPPORTED.

---

**CRD_021.** `CRD_006` does not close. The method layer (F branch set, G
return enum) is still not in this tree; G is implemented locally as the
order's seven values plus v1's added BLOCKED reasons, and F is emitted as
`branch_set_v2.json` in the order's shape. `archive-siting-bias` is still
absent.

*Falsifier:* the layer landing. *Status:* OPEN — named-and-absent.

---

**CRD_022.** The real run is NOT RUN and the reason is the order's own open
item: a technique-side transmission catalogue to draw ALL bins from,
unidentified, needing a human with library access. Until one exists there is
no admissible item list at all — a list assembled from the language side
fails the frame gate by construction, and a list drafted by a model fails the
contamination gate by declaration, which between them is why no item list was
authored here.

*Falsifier:* a catalogue. *Status:* UNVERIFIED, and it covers the revision.

---

**CRD_023.** Nothing in revision 2 is a statement about algebra, paper,
sine, terracing, any tradition or any person. The tradition names in every
`v2.` fixture are invented (`Meridian`, `Kestrel`), no description was read
from any reference work, and every fixture declares CONSTRUCTED in its own
header. What is established is that the instrument's returns move on
constructed data and that its refusals fire.

*Falsifier:* a real run. *Status:* UNVERIFIED.
