# columbia-chain-cascade

A HEC-RAS 2D build spec for a full-chain dam-cascade flood model on the
Columbia and Snake, with swappable initiator modules (single breach,
seismic, hydrologic, cyber, combined) and an antecedent-condition
coupling amplifier.

`SOURCE_DROP.md` is delivered verbatim.

**Two things about this drop set the whole scope.** It is a build spec
for software this environment does not have, on data this environment
cannot reach; and it arrived **truncated**, ending mid-sentence in
Module F — the module the spec itself calls decisive.

    python3 columbia-chain-cascade/audit.py         # what can be said
    python3 columbia-chain-cascade/eap_coverage.py  # the one computation
    python3 columbia-chain-cascade/selftest_ccc.py  # the checks

## The spec cannot be executed here, measured

    HEC-RAS 2D present on this machine:   False   (Windows-only USACE software)
    portal.opentopography.org  000        every DEM, bathymetry,
    www.usgs.gov               000        roughness and dam-geometry
    apps.nationalmap.gov       000        source in section 2 refuses
    charts.noaa.gov            000        CONNECT (allowlist egress)
    nid.sec.usace.army.mil     000
    www.mrlc.gov               000

**No hydraulics are simulated anywhere in this folder.** A flood-hazard
field produced by a stdlib toy would read as a result about a real dam
chain and a real downstream population — the highest-stakes version of
the rule this repository holds everywhere. The audit reports the
blockers; it does not route around them with a model of its own.

This is not a criticism of the spec. A HEC-RAS build spec on 3DEP data
is executable by someone with the engine, a Windows host and open
egress. Saying plainly that it is not runnable from here is more useful
than a toy that pretends otherwise.

## The delivered text is truncated

The spec ends:

    ## 4. MODULE F — ANTECEDENT CONDITION COUPLING (the amplifier)
    This is the part standard breach modeling drops. It is not a
    refinement; it changes the cascade outcome at the next

`audit.truncation()` detects this — the last line carries no closing
punctuation, Module F's header is the highest section reached, nothing
opens after it. Missing and **not reconstructed**: the body of Module F,
the burn-modified roughness values section 2 forward-references to it,
any validation section, any claim table, and the ask. Inventing the
amplifier the author calls decisive would put a mechanism in the
author's mouth.

## What survives: the governance claim

The spec calls ownership *"the governance variable"* and says *"mixed
ownership means no entity's plan spans the chain. Record it as data, not
commentary."* That is the one conclusion needing neither the engine, the
terrain, nor the missing text — only the node list, which is delivered
verbatim.

    no single entity's plan spans the chain:  True
    settled by:  the CA/US boundary in the delivered node list
    authorities, lower bound:  2

An EAP authority cannot cross a national boundary, and the three upper
nodes carry `(CA)` in the delivered text, so at least two authorities
apply. **The finding is robust to the missing per-node ownership**: no
assignment of the 18 nodes to the 5 owner categories can lower the
jurisdiction floor below the 2 the text already carries — owner
assignment can only make the fragmentation finer.

## What is refused

    per-node owner known here:   0 of 18
    exact number of EAP seams:   UNASSIGNED

The exact fragmentation — how many plans, where each seam falls — needs
each node's owner. That is public fact, carried in NID and project
memoranda, and both refuse CONNECT here. **It is not supplied from
memory into a dam-safety artifact.** The `owner` field is `UNASSIGNED`
for every node and the selftest walks the AST of the node table to
assert no other value appears there.

The cost is stated: this folder gives a lower bound, not the seam map.
The seam map is the useful governance product, and it is what whoever
has NID access should build.

## The package — a research agenda, and its kill list under audit

A later drop turns the folder from an audit-of-a-truncated-spec into a
**research agenda published to be picked up cold**. It lands verbatim
beside the v1 files (both stay inspectable): `SCOPE_BOUNDARY.md` (why
the model is broader than standard practice — physics does not respect
institutional boundaries), `knowledge_state.py` (the typing rule
enforced in code — a value asserted without a legitimate epistemic
state raises, and `INSTITUTIONAL_EXCLUSION` is rejected as invalid),
`module_f.py` (the Module F body reconstructed as *arithmetic* — the
operator swap and burn-modified roughness, the ordering `S1 ⊆ S2 ⊆ S3`
proved over 19,200 synthetic combinations, no real structure named),
`contributing_inflow.py` (urban runoff as a parameterized pool
increment), `eap_coverage_v2.py` (the governance record plus tribal
jurisdiction), `audit_v2.py` / `selftest_ccc_v2.py` / `CLAIM_TABLE_v2.md`
(`CCC_001..CCC_018`), `OPEN_QUESTIONS.md` (13 gaps, each
with a knowledge state, a stranger-evaluable falsifier, data sources
with access tiers, and a deliverable interface), and `DEEP_RESEARCH.md`
(the roadmap).

The package arrived with its own **kill list**, sent as *claims under
test* with the instruction that a kill overturned is a better outcome
than one confirmed. `kill_audit.py` adjudicates the three mechanically:

- **KILL 1** — a self-correction reasoning trace left in
  `contributing_inflow.render()` (`CCA_001`): CONFIRMED as an overlay
  artifact, and it lands on an arithmetically sound conclusion.
- **KILL 2** — the stated decisive condition differs from the coded one
  (`CCA_002`): CONFIRMED (prose reads the `max`-flip, code computes the
  `sum`-tip; they diverge on 226 of 540 swept cases) and RESOLVED by
  physics — the wave rides on the standing pool, so `sum` is right and
  the prose is the independent-node default reasserting in the
  translation layer of a module written to refute it.
- **KILL 3** — tribal jurisdiction supplied from memory (`CCA_003`):
  CONFIRMED and sharper — owners are refused-from-memory and carry a
  knowledge-state field; the six tribal rows are supplied from memory,
  finer, with no knowledge-state field, and the authority bound is
  invariant to them. The fix is not to drop tribal (that re-commits the
  `INSTITUTIONAL_EXCLUSION` the repo rejects) but to type it under the
  same discipline the owners carry.

All three hold; none is overturned — and a second pass **sharpens** each
at its root rather than ratifying it. KILL 3 traces to
`DEEP_RESEARCH.md` §6.1: the six tribal rows match its entry, and the
same doc pushed owner-assignments-from-memory (§3/§6.2, calling the
refusal "overly broad") — which the code declined for owners
(AST-checked) and took for tribal, the asymmetry winning where no
external constraint held it (`CCA_011`). KILL 1 and KILL 2 turn out to
be **one contiguous prose zone** in `render()`, and the function's own
docstring states the sum reading correctly — so the drift is confined to
the rendered narrative, not the arithmetic and not even the docstrings
(`CCA_012`).

Two findings the landing turned up: `CCC_017` is REFUTED on its
delivered instance (`module_f.render()` trips the repo's own screen on a
certainty verb, `CCA_005`), and the delivered `selftest_ccc_v2.py`
exercises v1 `eap_coverage` + v1 `audit` + the new `module_f`, so the v2
additions — including the KILL 3 tribal list — ship **unexercised**
(`CCA_006`).

**The cold-start axis** asks whether a stranger can start from this. The
sender corrected its first criterion — *every source tiered, every
non-open source routed; an untiered source is the miss, not a gated one*
— and under that corrected Q1 **all 15 gaps carry the same open item**:
0 of 76 data sources are tiered, and the tier discipline `START_HERE.md`
declares is applied to no source bullet (`CCA_010`). On the axes that
decide whether a gap is a research question at all, every gap names a
stranger-evaluable falsifier and a deliverable interface; the scope flag
falls on three gaps. The two GAP 14 provenance flags (Padhy 2026, Piao
2024) are the model of the citation discipline, and no other unflagged
dead reference is found (`CCA_013`). The three new package cards —
`START_HERE.md` and the GAP 14 / GAP 15 entries — land verbatim, kept as
cards 14/15 beside the byte-identical delivered 13-gap file (`CCA_014`).

**Gap completeness — does each entry give a researcher everything?**
`gap_completeness.py` runs a seventeen-pattern census over the fifteen
entries and a declared per-gap reading. The eight template fields are
15 of 15; the post-graduate essentials split cleanly — prior-art table,
citation status, secondary falsifier, cross-gap coupling and
what-would-move-it are carried **only by gaps 14 and 15**, so what a
researcher wants beyond the template is the shape the author's own
newest cards already take (`CCA_015`). **No gap gives a deliverable
schema**, and gaps 5–9 deliver "referenced by Module A–E" — spec
section names, not code — so the cold-start Q3 was clean on naming and
fails on drop-in for five gaps (`CCA_016`). A known-answer step is
present in gaps 1, 2, 10, 12, 14 and absent from the ten others
(`CCA_017`). And gap 3 (tribal EAP) has no consent or consultation
step before "request or locate" records from six sovereign nations —
an omission at the ethics layer, the cheapest to close, and one a bare
word-list would have hidden because "tribal consultation" appears
there as the quantity being mapped (`CCA_018`).

**Corrections and additions — "repair or add what we are able."** At
the sender's instruction the folder moved from audit to repair, under
one rule: correct prose, docstrings, import targets and data typing;
never a function body. Each correction is shown by the same detector
that caught it, run on the pre-correction revision `399517b` and on the
working tree (`CCA_019`): the KILL 1/2 prose in
`contributing_inflow.render()` now states the sum-tip the code computes;
the six tribal rows in `eap_coverage_v2.py` carry a `knowledge_state`
(validated at import) and a source, recorded beside the bound and not
counted; `module_f`'s last line clears the screen (`CCC_017` green); and
`selftest_ccc_v2.py` / `audit_v2.py` import the v2 modules, so the KILL 3
row is finally under test (102 checks). Every non-render function body is
byte-identical before and after.

Three additions close what the completeness census found, as far as it
can be closed without authoring literature from memory:
`initiator_schemas.py` (`CCA_020`) gives gaps 5–9 the column lists and a
drop-in loader that refuses a short row or the rejected state;
`gap_addenda.json` (`CCA_021`, built by `build_addenda.py`, which refuses
a bullet it cannot match) tiers all 76 sources with a route for every
non-open one — carried, not probed — plus a known-answer candidate per
gap, the gap 3 consent step, and the schema pointers; and
`UNDERGRADUATE_RESEARCH_GAPS_V2.md` (`CCA_022`, generated by
`assemble_gaps_v2.py`) is verbatim v1 + the two cards slotted in as
entries 14 and 15 + the addenda as fenced blocks — **stripping the
fences returns v1 byte-for-byte**, so the delivered file is never edited.
On the assembled file: known-answer 15/15, schema 5/5, consent 1/1, tiers
76/76 (46 OPEN / 18 GATED / 9 REQUESTABLE / 3 UNKNOWN). Prior-art table,
citation status, secondary falsifier and what-would-move-it stay at gaps
14/15 only — left unauthored on purpose, since a prior-art table is
citations and citations from memory are the dead-reference hazard the
GAP 14 flags exist to catch.

    python3 columbia-chain-cascade/assemble_gaps_v2.py  # regenerate V2 (round-trip checked)
    python3 columbia-chain-cascade/build_addenda.py     # regenerate the registry
    python3 columbia-chain-cascade/initiator_schemas.py # the drop-in schemas
    python3 columbia-chain-cascade/gap_completeness.py  # the completeness census
    python3 columbia-chain-cascade/kill_audit.py     # the kill audit
    python3 columbia-chain-cascade/selftest_kill.py  # its checks
    python3 columbia-chain-cascade/module_f.py       # the amplifier arithmetic

## Files

| file | what |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim, truncated as delivered, not edited |
| `eap_coverage.py` | v1 governance record — the one computation from the text |
| `audit.py` | v1 executability + truncation, each blocker measured |
| `selftest_ccc.py` | the v1 checks; run it, it prints its own count |
| `CLAIM_TABLE.md` | `CCC_001..CCC_008` with REFUTATION_PROTOCOL |
| `SCOPE_BOUNDARY.md` | delivered — why the model is broader than standard practice |
| `knowledge_state.py` | delivered — the epistemic-state typing rule, enforced in code |
| `module_f.py` | delivered — the Module F body as arithmetic (`S1 ⊆ S2 ⊆ S3`) |
| `contributing_inflow.py` | delivered — urban runoff as a pool increment |
| `eap_coverage_v2.py` | delivered — governance record + tribal jurisdiction |
| `audit_v2.py` | delivered — v1 audit, module-F-aware |
| `selftest_ccc_v2.py` | delivered, corrected — exercises the v2 modules and the typed tribal rows (green) |
| `CLAIM_TABLE_v2.md` | delivered — `CCC_001..CCC_018` |
| `UNDERGRADUATE_RESEARCH_GAPS.md` | delivered — 13 gaps, kept byte-identical |
| `START_HERE.md` | delivered — orientation for a stranger picking it up cold |
| `GAP_14_mining_hydrology.md` | delivered — gap 14 card (folder: `mining-increment/`) |
| `GAP_15_bridge_impoundment.md` | delivered — gap 15 card (folder: `bridge-impoundment/`) |
| `DEEP_RESEARCH.md` | delivered — the roadmap (and the root of the KILL 3 tribal data) |
| `kill_audit.py` | the kill list under audit + the two-axis cold-start test |
| `gap_completeness.py` | per-gap census + reading: what a researcher would still lack |
| `initiator_schemas.py` | the drop-in gaps 5–9 lacked: column lists, a refusing loader, one interface |
| `build_addenda.py` / `gap_addenda.json` | tiers + routes for 76 sources, known-answer candidates, consent step, schema pointers — carried, not probed |
| `assemble_gaps_v2.py` / `UNDERGRADUATE_RESEARCH_GAPS_V2.md` | v1 + cards 14/15 + addenda, fenced; strip returns v1 byte-for-byte |
| `selftest_kill.py` | the audit's checks; run it, it prints its own count |
| `AUDIT_NOTES.md` | `CCA_001..CCA_022` with REFUTATION_PROTOCOL |
| `samples/` | pinned runs |

Every module refuses `--selftest` rather than exiting 0 on an invocation
that runs nothing. The delivered `selftest_ccc_v2.py` was green after the
`CCC_017` correction and the retargeting (`CCA_019`).

## Scope

Nothing here bears on any hazard field, velocity band, time slice,
breach, operator error, or exposure count — the spec's actual subject.
The three headline product choices (velocity bands over depth-and-
extent, time slices over the envelope, exposure on the same sheet) are
sound and are not tested here, because testing them is the routing run.

One declared `no_severity` exemption, measured with the three-arm
harness: `means` on the v1 eap report, inside a verbatim quote of the
spec (*"mixed ownership means no entity's plan spans the chain"*). The
`proves` exemption on the kill-audit report retired with the `module_f`
correction; that report is clean with no mask.

CC0. Stdlib only, parses under 3.9, phone-buildable.
