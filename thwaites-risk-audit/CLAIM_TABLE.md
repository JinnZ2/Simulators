# CLAIM_TABLE — thwaites-risk-audit

Claims about the **delivered documents** and about what the tools they
name actually do. Ids are permanent and are never renumbered; a refuted
claim keeps its id and gains a status.

`TRA_*` are this audit's claims. `THW-01..05` and `THW-F1..F8` are the
**delivered document's own** ids and are not touched.

Nothing here is a statement about Thwaites Glacier, any ice sheet, the
AMOC, ENSO, sea level, or any paper. Every literature figure in the
delivered documents is CARRIED and verified against nothing — the egress
gate refuses every publisher, DOI-resolver and agency host.

Run `python3 thwaites-risk-audit/audit.py` for the numbers and
`python3 thwaites-risk-audit/test_audit.py` for the check count.

---

## The three renderings

### TRA_001 — v2 is a rewrite of v1, not a pure insertion
**Status:** SUPPORTED.
v1 747 lines / 46767 bytes, v2 768 lines / 49981 bytes, similarity
0.9426, opcodes `{equal 714, insert 16, delete 0, replace 38}`. Nothing
was deleted and 38 lines were replaced, so the repairs were applied **in
place** rather than appended — which is why every one of them has to be
checked at the site it changed rather than at the end of the file.
**Falsifier:** an opcode census showing `replace == 0`.

### TRA_002 — the convergence note is refuted by content: one document in two places
**Status:** SUPPORTED, and it is the sharpest finding in the drop.
Section 12c reads *"Repo convergence note: `Simulators/AMOC/research.md`
(commit f35e1f5) independently added Kasuya and Nian while these searches
ran. Same two papers, two independent routes."*

`f35e1f5:AMOC/research.md` is a **byte-exact prefix of v1** — 27070 of
v1's 46767 bytes, 57.9%, sections 1 through 10, under v1's own title
(*"September-2026 Papers"*) and v1's own uncorrected *"Bradley et al."*
heading. It names Kasuya and Nian because **it is this document**, filed
on `main` as AMOC research. The two routes are one route.

Resolved two ways: by the sha the note itself cites, and independently by
walking every commit touching the path for a blob that is a v1 prefix
(`AGA_066`'s discipline — a fixed position in history compares against
whatever bytes sit there). Both return `f35e1f5`.

This is `triad-playground` `TP_003` (a shadow panel's agreement measures
what its members share, not the truth) and
`effective-redundancy-audit`'s shared-node arithmetic arriving on a
citation-convergence claim — in the same document that computes
`N_eff = 1` for somebody else's observing system.
**Falsifier:** the blob at that path and commit not being a prefix of v1.

### TRA_003 — all six repairs are applied, and the first test for one of them was wrong
**Status:** SUPPORTED. R1–R6 each get a mechanical test against v1 and v2
and all six confirm.

Recorded because it was found by running: the first test for **R2** read
*"`UNVERIFIED` in v2 and not in v1"* and returned a **false negative** —
v1 already uses the token for an unrelated lead (the HAL bathymetry
record), so a document-wide token test cannot see a figure-level flag.
`UNI_009` / `T1-1` inside a repair-log checker. The test now reads the
figure's own lines: every line mentioning `2.6 mm/yr` carries the flag in
v2 and none does in v1.
**Falsifier:** any row whose stated repair is absent from v2.

### TRA_026 — R1 did not reach the one document written for a planning meeting
**Status:** SUPPORTED.
R1 renames *Bradley et al.* to *Williams et al.* (Bradley is last author).
Across the five delivered files: v1 names Bradley 12 times and Williams 0;
v2 names Williams 16 and Bradley 4 (in the repair record itself);
`WORKER_FIELD_BRIEF_DESIGN_LIFE.md` names **Bradley twice and Williams
never** — once as the citation for its load-bearing 150-year number and
once in its PROVENANCE line (*"Bradley et al. peer-reviewed"*).

The repair reached the internal audit and not the one-page brief the
document's own section 12d adopts as its audience frame. The two files
with no citation at all are correctly not flagged, so the check is not
`CONSTANT_FIRES`.
**Falsifier:** the brief naming Williams.

---

## What was actually run

### TRA_004 — no tool run in the document is reproducible from the delivery
**Status:** SUPPORTED.
The method note names nine input files — two closure-cost case files, five
declared-frame blocks, one measurement-fork spec, one chain driver — and
**none is in the delivery**; there is no `.json`, `.jsonl`, `.csv` or
`.txt` anywhere in it. So what is checkable here is not the runs but the
**tools' behaviour**, which is what every `run_*` function does. Each
finding below is therefore about what the tool does when run, not about
whether the document's own run was done correctly.
**Falsifier:** an input file landing.

### TRA_005 — S1's quoted numbers are the module's own defaults, and R4 did not relabel them
**Status:** SUPPORTED.
`0.001 / 0.9989 / 0.0000` and `0.200 / 0.7984 / 0.0000` reproduce
**exactly** from `s1_encounter_denominator.sweep()` with its shipped
defaults (`n_dyads=40, ticks=400, seed=11`). No Thwaites quantity enters,
and the module's own text says the zero is *"by construction."*

R4 relabelled two blocks DEMONSTRATION — the climate-modeling 7/7 and the
chain 4/4 — and left this one under a *"Run output"* heading. All three
are the same class of object.
**Falsifier:** a seed or parameter in the document that is not the
module's default.

### TRA_006 — the chain block is the module's shipped fixture with four node names substituted
**Status:** SUPPORTED.
`chain.signal_chain()` at the boundary inflow parsed out of `chain.py`
(6.0, read from the source rather than retyped) returns
`A 4.20/9.00, B 2.94/12.00, C 2.06/15.00, D 1.44/18.00` — **every number
identical** to the document's `Thwaites_grounding_line`,
`Thwaites_eastern_shelf`, `WAIS_interior_basins`, `coastal_SLR_delivery`
rows, along with the verdict string and the `independent-only: []` line.
The *"declared synthetic Thwaites→WAIS chain"* is `signal_chain()`; the
node names are the only Thwaites content in it.
**Falsifier:** any row differing from the fixture.

### TRA_007 — R4's relabelling is right and its stated reason is wrong
**Status:** SUPPORTED, and the correct reason is stronger.
R4 reads *"sum ≥ max for non-negative inputs, so the 4/4 breach is an
identity, not a Thwaites finding."* `sum ≥ max` guarantees only that RUN
1's breach set is a **subset** of RUN 2's — the one-sidedness — and
guarantees no breach at all. The module ships two nulls that satisfy
`sum ≥ max` and return **REFUTED** (`high_freeboard`, `no_freeboard`), so
the detector does not always fire and 4/4 is a property of the fixture's
antecedent-state band. The relabelling stands; the identity claim does
not.
**Falsifier:** a chain with `sum ≥ max` where the breach count is forced.

### TRA_008 — renaming the columns makes the table read as arithmetically impossible
**Status:** SUPPORTED.
The module labels the two columns `independent` and `coupled` — two
separate chain runs with different wave trajectories. The document labels
them `max` and `sum`, which reads as `max(a,b)` and `a+b` over one pair
per row. For two non-negative numbers `a+b ≤ 2·max(a,b)`, and **all four
rows violate it** (row 1: 9.00 > 2 × 4.20 = 8.40). Under the module's own
column names there is no arithmetic difficulty. The relabelling
introduces an impossibility the original does not have, in the table the
section's headline rests on.
**Falsifier:** a reading of the document's columns under which
`sum ≤ 2·max` holds.

### TRA_009 — the "no shared quantity" sentence is a module constant, and the spec that produced the counts is absent
**Status:** SUPPORTED.
All four quoted lines — *"none -- the arms share no quantity at all. /
That is itself a finding: the designs do not overlap, / so no existing
result speaks to the coupling questions."* — are `compare.py`'s hardcoded
string for an empty cell, and the **shipped** spec
`provisioning_calibration` returns exactly it (`MF_003` records the same).
The probe counts differ (document 8/12/14, shipped spec 7/10/17), so a
Thwaites spec really was built and run; it is not in the delivery, so the
counts are unreproducible and the verdict text is not evidence about any
instrument.
**Falsifier:** the spec landing, or a spec on which the cell is non-empty.

### TRA_010 — a fourth arm is not expressible in `compare.py`
**Status:** SUPPORTED.
`arms` is a hardcoded three-key dict over three fixed generators
(`conventional`, `coupling`, `widen`), read from the AST. Section 13 says
Zeising was *"run through the measurement-fork as a fourth arm"* and
section 14 concludes *"THW-02 is now a four-arm result."* Whatever was
run, the fourth instrument entered as probes inside one of the three
existing arms, so *no shared quantity across four arms* is not what
`compare.py` computed — it computed no shared quantity across its three.
**Falsifier:** a fourth key in that dict.

### TRA_011 — the v2 output fence carries an authored parenthetical
**Status:** SUPPORTED.
The section-13 fence reads
`none -- the arms share no quantity at all.   (unchanged with arm 4)`.
`compare.py` prints four fixed lines for that cell and prints no
parenthetical. The fence mixes tool output and authored annotation
without marking which is which.
**Falsifier:** that string appearing in `compare.py`.

### TRA_012 — `[COVERED widen]` means the question was reached, and the document reads it as residual
**Status:** SUPPORTED.
`compare.py` prints `[COVERED <arms>]` inside the RESIDUAL section for a
question **some arm reached**; only `[ NO ARM ]` lines are residual. The
document's v2 fence shows `[COVERED widen] whether acoustic impedance,
radar reflectivity, and resistivity can be joint-inverted…` and the prose
reads it as *"registered in the residual cell."* It is the opposite.

Worse for the line and better for the conclusion: a `COVERED`-by-widen is
`MF_004`, a known false positive — the widen arm emits options about the
**design**, not quantities — and the defect **stands unrepaired**, since
the residual loop still pools every arm and `compare.py` contains no
`is_quantity` filter. So the document's substantive point (a joint
inversion would have to *construct* the shared quantity) is right **in
spite of** the line it cites.
**Falsifier:** an `is_quantity` filter in that loop.

### TRA_013 — κ = 0.000 is forced by the reported N_eff and carries no agreement information
**Status:** SUPPORTED, and the document's own reason is the weaker one.
`N_eff = 1` means every channel collapsed — the second coder marked every
channel the same way, i.e. a **constant** coder. Swept over all 62
non-degenerate first codings of six channels, `cohen_kappa(c1, [shared]×6)`
returns exactly `0.0` in **62 of 62**. Two equal constant coders return
`1.0`, so the value is not a floor of the statistic.

So κ = 0.000 is the arithmetic consequence of the reported `N_eff = 1`
and says nothing about agreement: two independent human coders who both
reached `N_eff = 1` the same way would also produce 0.000. R6 flags it
*"INVALID AS RELIABILITY: both codings by one model"* — true, and it would
be uninformative with two real coders. `null-harness`
`NO_DISCRIMINATION` on an inter-rater statistic.
**Falsifier:** a non-constant second coding that yields 0.000 for an
independent reason.

### TRA_014 — the closure-cost render is genuine and its verdict restates an auditor-entered input
**Status:** SUPPORTED; the second half is the document's own.
`closure.py --case <name>` emits exactly the labels the document quotes
(`VARIABLE`, `INFORMATION AVAILABILITY`, `PROCEDURE GAP RIVAL / collapsed
into closure`), so a real case file was rendered. The case file is absent
(`TRA_004`).

The repair log's own *"still unrepaired"* line already says the verdict
*"restates an auditor-entered input ('availability: present')"* — which is
right, and is `CC_002`'s neighbour: the `rules` column is a function of
the availability field the auditor set. Recorded as something the
document caught about itself.
**Falsifier:** a code path in which that column is derived rather than
read.

### TRA_015 — `check_frame.py` emits no frame flag
**Status:** SUPPORTED.
On a single block the checker prints *"all six fields declared"* plus any
`unknown ->` list, and returns 0. It contains no string matching `flag`.
Section 13's per-paper *"frame flag: `boundary`"* / *"`who_counts`"*
labels are authored classifications, in a sentence whose first clause
(*"accepted by `check_frame.py`"*) is the tool's. A single-block
acceptance is a well-formedness statement only.
**Falsifier:** a flag in the checker's output.

### TRA_016 — the frame-quality ranking is over the one field the instrument never compares
**Status:** SUPPORTED.
`CORE = ["boundary", "horizon", "who_counts"]`; `DF_001` records
`sign_source` and `observer_access` as *recorded but never compared*.
Section 14 ranks the corpus by `observer_access`. So the ranking reads
back the author's own declarations in the one field `compare()` does not
score. The document does say *"as the proxy"*, which is partial credit.
**Falsifier:** `observer_access` entering `CORE`.

### TRA_017 — the OIR numbers reproduce and the document scopes its own transfer down
**Status:** SUPPORTED.
`pipeline.py`'s `false_alarm_heavy` ensemble returns
`false-alarm rate 0.5   miss rate 0.0` — the document's figures exactly —
and the document presents them as OIR's own standing finding rather than
as a Thwaites measurement. Section 12a then demotes the transfer to
*"candidate cross-domain shape, constraint sets uncompared"* on the
operator's critique, naming `SS_005` / `TP_008` / `RCC_008` as the
discipline. Recorded as correct handling.
**Falsifier:** the rates not reproducing.

### TRA_018 — the spinodal moves with the grid, and the quoted figure is the coarsest
**Status:** SUPPORTED.
`StommelBox.hysteresis_band` returns the last grid point at which both
states coexist, so every value is a **lower bound**. Over six ordinary
(range, n) choices it runs **0.2278 to 0.2380**, spread 0.0102. The
document's `F ≈ 0.228` is reproduced exactly by `(0.0, 1.0, 80)` — the
coarsest grid and the lowest of the six — and three decimals state a
precision the method does not have. `reasoning-dial` `RD_002` and
`model-ecology`'s window result on a new substrate.

The direction runs toward the document's own posture: an under-estimated
collapse threshold is the short end.
**Falsifier:** a convergence study showing the reported value is the
limit.

### TRA_019 — "≈ 0.50 Sv" is the calibration's own anchor read back out
**Status:** SUPPORTED.
`sitespec.ForcingCalibration` declares `sv_at_F0 = 0.15`,
`sv_at_spinodal = 0.50` and `spinodal_F = 0.217`. So *"collapse spinodal
at F ≈ 0.228 (≈ 0.50 Sv on the declared calibration)"* is the anchor
restated, not a threshold computed in sverdrups — and converting the
document's **own** F through the calibration gives **0.5177 Sv**, because
0.50 corresponds to the hardcoded 0.217, a third value for the spinodal
alongside the document's 0.228 and the tool's 0.2278–0.2380.
**Falsifier:** a derivation of 0.50 Sv that does not use the anchor.

### TRA_020 — the document's own opening rule is not applied where the tool hands it a band
**Status:** SUPPORTED.
The document opens *"report the band, plan against the short end."* The
calibration's docstring supplies a published band — collapse thresholds
*"cluster ~0.1-0.4 Sv of ADDED freshwater"* — and the anchor's added flux
(0.50 − 0.15 = **0.35 Sv**) sits inside it, near the top. Section 7 uses
the single anchor: against 0.35 Sv the 0.030 Sv flux is ~12× below;
against the cluster's low end of 0.1 Sv it is ~3.3× below. *"Well below
the collapse threshold as a magnitude"* holds at one end of the band and
is much less comfortable at the other, and the document does not report
the band it was handed.
**Falsifier:** the docstring not stating a range, or the added-flux
reading being wrong.

### TRA_021 — the flux conversion is exact
**Status:** SUPPORTED. 2.6 mm/yr of global mean SLE over 3.61e14 m² is
**0.02974 Sv**; the document states *"≈ 0.030 Sv."* Exact. `sle_to_sv`
returns `None` for an absent input and `0.0` for a measured zero, so an
absent figure never reads as no flux.
**Falsifier:** a different ocean-area convention moving the third digit.

### TRA_022 — the one arithmetic step that runs toward overstating
**Status:** SUPPORTED.
*"order 50–60 Gt of added basal melt over the event (~0.15 mm SLE
one-time pulse)"*. At 361.8 Gt per mm, 50–60 Gt is **0.138–0.166 mm** —
so `~0.15 mm` is exact **for grounded ice**. The quantity named is
ice-shelf **basal** melt, melt at the base of **floating** ice, per the
document's own mechanism paragraph (*CDW flows … under the ice shelves*).
The direct sea-level contribution of floating-ice melt is the
displacement residual, `1 − ρ_ice/ρ_seawater` ≈ 0.107, giving
**0.015–0.018 mm** — about **9.3× smaller**. The sea-level consequence of
shelf melt is the downstream dynamic response of grounded ice: a
different quantity, with a lag, and the document's own operator-swap
framing is the right place for it.

Every other finding here runs the other way; this is the one that runs
toward the risk-forward reading, which is where a worst-case-planning
document is most exposed.
**Falsifier:** the 50–60 Gt being grounded-ice loss rather than basal
melt.

### TRA_023 — "schema-conformant" covers four of five blocks, and none in the register's own block form
**Status:** SUPPORTED.
Four fenced `GAP_ID` blocks parse (THW-01..04), each carrying **7 of 7**
schema fields with an in-vocabulary `STATE`. But `markers.FIELD_RE`
requires four leading spaces and the fenced blocks have none, so the
register's own reader ingests **0 of 4 as delivered** — the blocks carry
the right field *names* and not the register's block *form*. THW-05 is
prose with an inline `STATE: unowned` and is not a block at all, so it
parses as nothing.
**Falsifier:** `parse_entries` reading the delivered text.

### TRA_024 — THW-02's KIND contradicts its own STATE
**Status:** SUPPORTED.
`KIND` is single-valued over two values and THW-02 carries **two**:
`knowledge (measurement genuinely absent) + boundary-artifact (funding by
instrument)`. That is `GM_010`'s shape reached by an author who has not
read the register — independent recurrence.

Sharper: `markers.kind_forced("assembly")` reads the register's own
definition (*"all components present in separate literatures, never
combined"*), finds an existence claim, and **forces**
`boundary-artifact` — so the `knowledge` half contradicts the entry's own
STATE. The entry's `WHAT_IS_MISSING` states both things at once (a shared
quantity, which is `assembly`; and *"pore pressure unmeasured by all"*,
which is `knowledge`), so it is two gaps in one block — `UNI_020`'s
*declines to be one quantity* arriving in this schema.
**Falsifier:** an `assembly` definition that makes no existence claim.

### TRA_025 — the 7/7 block is NOT_RUN here, measured
**Status:** SUPPORTED. `climate-modeling` needs numpy and scipy and both
are absent in this environment, so the block is unreproducible here and
the state is probed rather than assumed. The document's R4 already
relabels it a DEMONSTRATION, and `CLAUDE.md` independently records
*7 built → 7 FAIL* for the suite's own synthetic cases.
**Falsifier:** numpy and scipy being present.

### TRA_027 — every publication claim is CARRIED
**Status:** UNVERIFIED, and it covers the folder.
15 DOIs are named in v2 and **0** are verified here: the egress gate is an
allowlist and only `github.com` answers, so no publisher, resolver or
agency host is reachable. Every paper, author list, date, journal, figure,
ENSO status line, and the R5 DOI conflict itself is carried and enters no
verdict. `ANC_010` / `MS_004` status.
**Falsifier:** a reachable source.

---

## What holds

### TRA_028 — the document's repair discipline is the strongest thing in the drop
**Status:** SUPPORTED, and recorded because it is unusual.
It ships a six-row repair log **before** its own body; flags its own
load-bearing figure UNVERIFIED inline at all three sites rather than in a
footnote; **retires** a falsifier (THW-F1) when its premise turned out not
to be in the source and re-derives the section from the abstract;
relabels two of its own headline results DEMONSTRATION; enters a
counterweight that cuts against its own coupling narrative (Höse) and
writes a falsifier (THW-F8) that *"pits the two sections against each
other deliberately"*; scopes down its own over-transfer on the operator's
critique (12a); and carries a *"still unrepaired"* list naming two
unsourced assumptions in its own load-bearing section.

`TRA_002`, `TRA_010`, `TRA_012`, `TRA_013`, `TRA_020` and `TRA_022` are
findings the document did not reach. `TRA_003`, `TRA_007`, `TRA_014`,
`TRA_017` and `TRA_025` are places it reached them first or nearly.
**Falsifier:** a repair in the log that is absent from v2 — tested, and
none is.

---

Scope: `TRA_001..TRA_028`. Check count printed by
`python3 thwaites-risk-audit/test_audit.py`.
