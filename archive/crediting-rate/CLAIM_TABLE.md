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

# WORK ORDER L, REVISED — `CRD_009..CRD_021`

`WORK_ORDER_V2.md` lands verbatim beside `WORK_ORDER.md`; neither
supersedes the other and `crediting_rate.py` is not edited.
`crediting_rate_v2.py` imports v1 for every piece the revision does not
change. Run `python3 crediting-rate/test_crediting_v2.py` for the count.

---

**CRD_009.** The three revisions are **model-authored and were sent
un-adjudicated.** The dispatch bundle's own send-order table reads *"3 L
crediting_rate REVISED not sent (three revisions are Claude's, PROPOSED,
adopt or strip before sending)"*, and it was then sent as delivered. So
the three-state bin, REVISION 1 and REVISION 2 are proposals the operator
neither adopted nor stripped. The layer is named in the module docstring,
in `PREDICTION_V2.md` and on the first two lines of every render, because
`AUDIT_CONTRACT.md` layers a co-produced document before auditing it and
a later reader would otherwise read the revision as the operator's
position. v1's order carries no such note and is the operator's.

*Falsifier:* the bundle not carrying that line, or the operator adopting
or stripping the revisions. *Status:* SUPPORTED, and it is a fact about
the delivery rather than about the design.

---

**CRD_010.** **REVISION 2 removes the input its own RETURN block still
lists a class for.** v1's `CONTRIBUTION_TRACKING` fires on a gap inside
the shuffle band AND `misattr <= MISATTR_MAX`, where `misattributed` is
`int(any(c["described_originator"] == "receiving" ...))`. REVISION 2
replaces `described_originator` with *"origination_vs_absorption coded
from attested dates only, never from narrative"* — an **ordering**, not a
misattribution rate — and the RETURN block still lists
`CONTRIBUTION_TRACKING`. Without a replacement discriminator the class is
unreachable in v2 and every null gap lands on `UNKNOWN_measurable`.

`[CHOICE 6]` supplies one: `attribution_depth`, the crediting measure
REVISION 2 keeps. A null gap with credit flowing is contribution
tracking; a null gap with nobody crediting anyone is not, because then the
bin cannot be the variable. The cut is **stipulated and has no
derivation**, exactly as `MISATTR_MAX` had none, and F2 and the suite's
low-depth variant differ **only** in depth — same gap, two returns.

*Falsifier:* a reading of the revision under which the class keeps an
input. *Status:* SUPPORTED.

---

**CRD_011.** REVISION 1's frame gate fires **both ways and before any
rate exists.** A mixed-side item list returns `FRAME_ASYMMETRIC` naming
both sides (F3); `model_authored=True` returns `CONTAMINATED_FRAME` (F4);
and both returns carry no `rates` key at all, so nothing downstream can
read a number off a stopped run. A single-side list whose side cannot
enumerate a bin present also stops, since no linguistic index exists for
a word that did not survive.

*Falsifier:* a stopped run carrying a rate. *Status:* SUPPORTED on the
fixtures.

---

**CRD_012.** v1's shuffler is **binary** and v2's bins are three-state,
so v2 has its own — and the two are checked to agree to 1e-12 on a
two-bin input rather than the second one being asserted equivalent. v2
reaches `V1.outside`, `V1.load_frame`, `V1.ordering_state`, `V1._jsonl`
and `V1._is_int` directly and claims to reach `V1.bin_gap` and
`V1.shuffle_band` nowhere.

*Falsifier:* the two bands differing on a binary input. *Status:*
SUPPORTED.

---

**CRD_013.** REVISION 2's redaction is **structural, not an instruction
to the coder.** A depth file carrying `item`, or any field whose name
contains `bin`, `loanword`, `retain`, `etymolog` or `visible`, is refused
at load. The join key is `sha256(item|salt)[:16]` with the salt in the
events manifest, so the handle carries no readable content — `UNI_078`,
where a field documented as an "opaque handle" spelled out the arm on
every row.

*Falsifier:* a depth record from which the bin is recoverable without the
events file. *Status:* SUPPORTED.

---

**CRD_014.** The crediting measure is mechanical and **moves with N**,
which is read from the mechanical data file per record rather than from a
module constant. The same description scores 0 at N=2 and 1 at N=3
because the tradition is named in sentence three. The match is
case-insensitive on a word boundary (`[CHOICE 1]`), so
`Sigmaically` does not count and `SIGMAIC` does.

*Falsifier:* a description whose score does not move with N when the name
sits outside the first N sentences. *Status:* SUPPORTED.

---

**CRD_015.** F5 is the antiquity confound and **the pooled result is a
date effect.** The pooled gap (0.5000) clears its band
([-0.3750, 0.3750]) and the return is `ETYMOLOGY_TRACKING`; inside the
early date stratum the gap is exactly **0.0000**, and the late stratum
has **no gap at all** because only one bin is present there. The N2/N4
correlates are printed **before** the fit, per the order's own NOTE, so
the confound (mean attestation 835 / 985 / 1135 by bin) is visible above
the number it explains.

*Falsifier:* a date-sorted world whose stratified gap does not collapse.
*Status:* SUPPORTED on the fixture.

---

**CRD_016.** The discriminating bin is **reported and not forced.**
`technical_only` tracks `visible` on F1 (retention is the variable),
returns `UNDETERMINED` on F2 where the two anchors do not differ, and can
return `MIDPOINT`. And `gap` means the **pooled** gap on every branch
including `DOMAIN_SPECIFIC`, where an earlier version put the domain's
gap under that key and the pooled one under another — one name, two
quantities by branch, which is `measurement-fork`'s VOID RATIO in this
module's own return shape. Found by reading a probe's output and
misreading it.

*Falsifier:* a branch on which `gap` is not the pooled gap. *Status:*
SUPPORTED.

---

**CRD_017.** `model_authored` must be an **explicit boolean**: an events
file with no `_manifest`, or a manifest without the field, is refused
rather than read as `False`. The gate that stops the whole run is the one
place a missing declaration would be cheapest to read as a clean bill,
so the absent-vs-known-negative repair is applied there first.

*Falsifier:* an events file with no declaration that runs. *Status:*
SUPPORTED.

---

**CRD_018.** The CHECK FIRST answer, and it **differs from `CRD_006`'s.**
F (`branch_set.py`) and G (`preference_free_rank.ReturnClass`) exist in
the sibling repository `JinnZ2/method-layer`; `crediting_rate_v2.py`
locates it the way `enclosure-first-residual/` does (`METHOD_LAYER_PATH`,
else a sibling or grandparent checkout) and reports `present` or `absent`
as a measured state. `CRD_006` says *"the method layer the order consumes
(F branch set, G return enum) is not in this tree"* — true of what v1
could see, since it looked inside `Simulators`, and the later folder
looks for a sibling repo. Two folders answering one CHECK FIRST two ways;
the later answer is the right one and `CRD_006` is narrowed rather than
refuted. G is **not a single module**: the enum lives in
`preference_free_rank.py` and `frame_probe.py` carries its own
`SessionOutcome`.

*Falsifier:* a standalone G module in `method-layer`. *Status:*
SUPPORTED.

---

**CRD_019.** Three of this build's own checks were wrong and were found
by running. Two claimed v2 reached `V1.bin_gap` and `V1.shuffle_band`,
which it does not and should not (`CRD_012`). The third was a substring
scan asserting `described_originator` appears nowhere in v2 — and it
fires on the three comments in which v2 **names the field it removed**,
which is `UNI_009` / `T1-1` inside the check written against exactly that
removal. Replaced by an AST walk requiring the field to reach no
constant, name or attribute; the module is then required to name it in
prose at least three times, so the structural form is the only form the
test can take.

*Falsifier:* a version of the check that passes on a v2 using the field.
*Status:* SUPPORTED.

---

**CRD_020.** All seven return classes are reached. Five by shipped
fixtures — `ETYMOLOGY_TRACKING` (F1, F5), `CONTRIBUTION_TRACKING` (F2),
`FRAME_ASYMMETRIC` (F3), `CONTAMINATED_FRAME` (F4), `DOMAIN_SPECIFIC`
(F6) — and two by constructed variants in the suite (`BLOCKED`,
`UNKNOWN_measurable`). **F6 is beyond the order**: the order lists five
fixtures and none reaches `DOMAIN_SPECIFIC`, a class its own RETURN block
declares, and a declared member no path populates cannot be told from one
nobody looked for. Its construction is the informative part — a domain's
shuffle band is set by its **within-bin spread**, so a domain can fail to
clear only when its items disagree internally, which is why a clean
second domain always clears and the branch cannot fire on two clean
domains.

*Falsifier:* a declared return class no path reaches. *Status:*
SUPPORTED.

---

**CRD_021.** UNVERIFIED, and it covers the v2 half. Nothing has been run
on any real item list, and the order's own REAL-RUN SPEC names why: *"a
technique-side transmission catalogue to draw ALL bins from. Unidentified.
This is the one piece needing a human with library access."* Every world
is constructed, declares itself so in its own frame file, and uses Greek
letters for items and invented letter-names for traditions **precisely so
no real technique's name can be read as evidence**. The fixtures were
written by the same process that wrote the scorer, so a fixture returning
what it was built to return is a REGRESSION result and not validation —
declared in the generator's header, above any world. `ambiguous` is its
own bin and is never assigned: it is excluded and counted.

*Falsifier:* a run on a real catalogue. *Status:* UNVERIFIED.
