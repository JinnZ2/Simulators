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

## Files

| file | what |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim, truncated as delivered, not edited |
| `eap_coverage.py` | the governance record — the one computation from the text |
| `audit.py` | executability + truncation, each blocker measured |
| `selftest_ccc.py` | the checks; run it, it prints its own count |
| `CLAIM_TABLE.md` | `CCC_001..CCC_008` with REFUTATION_PROTOCOL |
| `samples/` | pinned runs of both modules |

Both modules refuse `--selftest` rather than exiting 0 on an invocation
that runs nothing.

## Scope

Nothing here bears on any hazard field, velocity band, time slice,
breach, operator error, or exposure count — the spec's actual subject.
The three headline product choices (velocity bands over depth-and-
extent, time slices over the envelope, exposure on the same sheet) are
sound and are not tested here, because testing them is the routing run.

One declared `no_severity` exemption, measured with the three-arm
harness: `means`, inside a verbatim quote of the spec (*"mixed ownership
means no entity's plan spans the chain"*), where rewording would
misquote the delivered text.

CC0. Stdlib only, parses under 3.9, phone-buildable.
