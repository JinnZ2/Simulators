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

All three hold; none is overturned. Two findings the landing turned up:
`CCC_017` is REFUTED on its delivered instance (`module_f.render()`
trips the repo's own screen on a certainty verb, `CCA_005`), and the
delivered `selftest_ccc_v2.py` exercises v1 `eap_coverage` + v1 `audit`
+ the new `module_f`, so the v2 additions — including the KILL 3 tribal
list — ship **unexercised** (`CCA_006`). The cold-start test runs the
sender's five questions over all fifteen gaps (`CCA_007`): every gap
names a falsifier and an interface; the flags cluster on public-data
access and one-semester scope.

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
| `selftest_ccc_v2.py` | delivered — exercises v1 eap/audit + module_f (1 failure: `CCC_017`) |
| `CLAIM_TABLE_v2.md` | delivered — `CCC_001..CCC_018` |
| `OPEN_QUESTIONS.md` | delivered — 13 gaps, each startable cold |
| `DEEP_RESEARCH.md` | delivered — the roadmap |
| `kill_audit.py` | the kill list under audit + the cold-start test |
| `selftest_kill.py` | the audit's checks; run it, it prints its own count |
| `AUDIT_NOTES.md` | `CCA_001..CCA_009` with REFUTATION_PROTOCOL |
| `samples/` | pinned runs |

Every module refuses `--selftest` rather than exiting 0 on an invocation
that runs nothing. The delivered `selftest_ccc_v2.py` carries one
delivered failure (`CCC_017`, recorded as `CCA_005`) which is not
repaired, because `module_f.py` is delivered.

## Scope

Nothing here bears on any hazard field, velocity band, time slice,
breach, operator error, or exposure count — the spec's actual subject.
The three headline product choices (velocity bands over depth-and-
extent, time slices over the envelope, exposure on the same sheet) are
sound and are not tested here, because testing them is the routing run.

Two declared `no_severity` exemptions, each measured with the three-arm
harness: `means` on the v1 eap report, inside a verbatim quote of the
spec (*"mixed ownership means no entity's plan spans the chain"*); and
`proves` on the kill-audit report, the delivered `module_f` token the
`CCA_005` finding reports — echoing it verbatim is how the finding names
which token fired.

CC0. Stdlib only, parses under 3.9, phone-buildable.
