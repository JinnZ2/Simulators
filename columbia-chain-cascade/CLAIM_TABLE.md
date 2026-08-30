# columbia-chain-cascade — CLAIM_TABLE

`CCC_001..CCC_008`. Claims about the delivered `SOURCE_DROP.md` and
about what a stdlib environment can establish concerning it.

**This is a HEC-RAS build spec and it cannot be executed here.** No
HEC-RAS (Windows-only USACE software, absent), and every DEM,
bathymetry, roughness and dam-geometry source it names refuses CONNECT —
both measured, not asserted. **No hydraulics are simulated anywhere in
this folder**: a flood-hazard field produced by a stdlib toy would read
as a result about a real dam chain and a real downstream population,
which is the `PB_001` / `CW_004` rule at its highest stakes.

**The delivered text is also truncated** — it ends mid-sentence in
Module F, the module the spec calls load-bearing. Nothing missing is
reconstructed.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `CCC_001` | **The delivered text is truncated mid-sentence in Module F**, the module the spec names as decisive, and everything after it is absent. Detected, not asserted; not reconstructed. | SUPPORTED |
| `CCC_002` | The spec cannot be executed in this environment: the engine is absent and every data source refuses CONNECT, both measured. | SUPPORTED |
| `CCC_003` | **The one substantive thing computable from the delivered text is the governance claim, and it comes back settled** — no single entity's plan spans the chain. | SUPPORTED |
| `CCC_004` | It is settled at the jurisdiction floor (CA/US, from the text) and is **robust to the missing per-node ownership**: no owner assignment can lower the floor below the 2 the text already carries. | SUPPORTED |
| `CCC_005` | The **exact fragmentation is refused**, not estimated — per-node ownership is public fact not in the delivered text, and it is not supplied from memory into a dam-safety artifact. | SUPPORTED |
| `CCC_006` | The node list, jurisdiction tags and owner categories are transcribed from the delivered text and nothing else; the selftest checks each against the source. | SUPPORTED |
| `CCC_007` | The initiator modules' comparability is asserted, not shown — the same shape as `move-set-derivation`'s declared architectures, and showing it requires the engine. | SUPPORTED |
| `CCC_008` | Nothing here bears on any hazard field, velocity band, time slice, breach, or exposure — the spec's actual subject. | UNVERIFIED |

---

## CCC_001 — the delivered text is truncated

The spec ends:

    ## 4. MODULE F — ANTECEDENT CONDITION COUPLING (the amplifier)
    This is the part standard breach modeling drops. It is not a
    refinement; it changes the cascade outcome at the next

— with no object. Module F is exactly the part the spec calls decisive:
*"the part standard breach modeling drops ... not a refinement; it
changes the cascade outcome."* And it is the part that did not arrive.

`audit.truncation()` detects this rather than asserting it: the last
non-empty line carries no closing punctuation, Module F's header is the
highest section reached, and no later section opens after it. What is
missing is enumerated —

    the body of Module F (the antecedent-coupling mechanism)
    the burn-modified roughness values section 2 forward-references to it
    any validation section
    any claim table / refutation protocol
    the ask (what to run, what to publish)

**None of it is reconstructed.** Inventing the amplifier the author
calls decisive would put a mechanism in the author's mouth, and the
selftest asserts no Module F body text (`antecedent-condition`,
`burn-modified`) exists anywhere in the folder's own code.

**Falsifier:** the rest of the spec arriving. Then Module F is in hand
and this claim is about one delivery.

## CCC_002 — the spec cannot be executed here, measured

    HEC-RAS 2D present on this machine:            False
    portal.opentopography.org  000   3DEP DEM
    www.usgs.gov               000   3DEP / national map
    apps.nationalmap.gov       000   3DEP 1 m / 10 m DEM
    charts.noaa.gov            000   NOAA bathymetry
    nid.sec.usace.army.mil     000   NID geometry + ownership
    www.mrlc.gov               000   NLCD roughness

HEC-RAS is Windows-only USACE software; `engine_present()` checks the
PATH and it is absent. Egress is an allowlist, so no mirror substitutes
for the section-2 sources.

This is not a criticism of the spec. A build spec for HEC-RAS 2D on
3DEP data is a reasonable thing to write and is executable by someone
with the engine, a Windows host and open egress. It is simply not
runnable from here, and saying so is more useful than a toy that
pretends otherwise.

**Falsifier:** the engine and the data present. Then the spec runs and
this claim is about the environment.

## CCC_003 — the governance claim is computable, and it settles

The spec calls ownership *"the governance variable"* and says *"Federal
EAP structure assigns planning to the OWNER, so mixed ownership means no
entity's plan spans the chain. Record it as data, not commentary."*

That is the one conclusion in the spec that needs neither the engine,
the terrain, nor the missing text — only the node list, which is
delivered verbatim.

    no single entity's plan spans the chain:  True
    settled by:  the CA/US boundary in the delivered node list
    authorities, lower bound:  2

An EAP authority cannot cross a national boundary — a US federal
owner's plan does not extend into BC Hydro's Canadian projects. The
three upper nodes carry *"(CA)"* in the delivered text, so at least two
authorities apply, so no single plan spans the chain. The spec's own
conclusion, reached from the spec's own data.

**Falsifier:** a single-jurisdiction chain. The selftest runs exactly
that as a null — a hypothetical all-US node list returns
`authorities_lower_bound == 1` and the claim un-settled — so the True
here is the CA/US split doing work, not a constant.

## CCC_004 — robust to the missing ownership

The finding does not depend on the data this environment lacks:

    assigning the 18 nodes to the 5 owner categories can only RAISE
    the authority count above the jurisdiction floor, never lower it;
    the floor of 2 is already > 1.

So the governance claim holds at the granularity the delivered text
supports **regardless of** the per-node ownership. The spec asserts
five owner categories (USACE / USBR / PUD / BC Hydro / private), which
would make the true fragmentation finer than two — but even the
coarsest reading the text forces already exceeds one.

**Falsifier:** an ownership assignment that reduces the count below two.
None exists, because jurisdiction is a floor under owner: every owner
sits within one jurisdiction.

## CCC_005 — the exact fragmentation is refused

    per-node owner known here:   0 of 18
    exact number of EAP seams:   UNASSIGNED

To compute how many plans there are and where each seam falls needs the
mapping of each of the 18 nodes to its owner. That is public fact —
carried in NID and project design memoranda — and both refuse CONNECT
here (`CCC_002`).

It is **not supplied from memory.** Assignments like *Grand Coulee is
USBR* or *the four lower Snake dams are USACE* are things a language
model may carry, and putting them into a dam-safety planning artifact on
no checkable basis is the exact failure this repository refuses
everywhere — sharpest here, because the artifact's subject is emergency
planning for a real inhabited river chain. The `owner` field is
`UNASSIGNED` for every node and the selftest walks the AST of the node
table to assert no other value appears there.

The cost is stated: this folder gives a lower bound, not the seam map.
The seam map is the useful governance product, and it is exactly what
whoever has NID access should build.

**Falsifier:** a reachable, checkable per-node ownership source. Then
the exact count is computable and this refusal lifts.

## CCC_006 — transcribed, not invented

Every node name, every reach label, the `(CA)` jurisdiction tag, and the
five owner categories appear in the delivered text, and the selftest
checks each one against `SOURCE_DROP.md`:

    18 dam nodes, each name found in the source
    reach labels (Upper/US/Snake/Lower) are section headers in the text
    (CA) is on exactly the three upper nodes and appears in the text
    the five owner categories are named verbatim in the text
    the estuary is recorded as a reach, not a node ("Bonneville to the
      mouth, tide as downstream boundary")

Listing what the text lists is transcription. Assigning owners the text
does not assign would be invention, and `CCC_005` is where that line is
held.

**Falsifier:** a node, tag or category in the code that is not in the
source. The selftest fails on it.

## CCC_007 — comparability is asserted, not shown

The spec: *"Each writes only a breach or release hydrograph ... The
routing engine downstream is identical, so modules are comparable."*

That is a real and sensible design claim, and it is the same shape as
`move-set-derivation`'s declared architectures: comparability across
initiator modules requires the downstream engine be identical, which is
asserted here and cannot be shown without running it. Restated, not
computed — computing it is the routing run.

The same holds for the spec's load-bearing structural argument, *"full
chain is required, not preferred: attenuation and amplification only
appear across nodes. A reach study cannot produce the answer."* It is
the reason the domain is the whole chain, and demonstrating it is a
multi-node routing run this environment cannot perform.

**Falsifier:** a run showing the modules comparable, or a run showing
across-node amplification. Both need the engine.

## CCC_008 — nothing here bears on the spec's actual subject

No hazard field. No velocity bands, no time slices, no
attenuation/amplification matrix. Nothing about any breach, any node's
failure mode, any operator error, or any population's exposure.

The spec's three headline product choices — velocity bands over
depth-and-extent, time slices over the maximum envelope, exposure
overlaid on the hazard sheet — are sound calls about what a
flood-hazard product should publish, and **not one of them is tested
here**, because testing them is the routing run.

What is established: the governance claim holds at the granularity the
delivered text supports; the spec cannot be run in this environment; and
the module the spec calls decisive did not arrive.

**Falsifier:** run the spec, with the engine and the data. That is the
project; this is what a text-only environment can say about a truncated
build spec for it.
