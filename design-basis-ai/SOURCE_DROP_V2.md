# Design Basis for AI as Knowledge Infrastructure

CC0. A design-basis document, in the sense a seismic code is one: it states
the loads the structure must carry, the provisions that carry them, how each
provision is verified, and what result would prove the provision unnecessary.

It is not a description of any existing system. It is the standard a system
would have to meet to be treated as load-bearing — the way a bridge is treated
as load-bearing.

---

## 0. THE REFRAME THAT SETS THE LOADS

```
AI is commonly modeled as:   another channel
   one more independent consultation among many.

AI actually operates as:      a shared node
   one model, one weighting, installed underneath decisions
   that were previously partially independent.

  N_nominal:  millions of independent consultations
  N_eff:      1   (same weights, same training, same failure modes,
                   deployed everywhere)

→ AI is the largest single shared node yet installed under human
  decision-making. The design basis below exists because of that,
  not despite it.
```

Everything that follows treats the six shared-node failure modes as the
**load cases** the structure must survive.

---

## 1. LOAD CASES (what the structure must carry)

From cross-domain investigation of redundancy failures (logistics, rail-chem,
county EM, refinery, nuclear, aviation). Each is a way N_eff collapses to 1.

```
A  AUTHORIZATION   one release/approval gates all action        → stall
B1 INFORMATION     one source feeds all deciders                → false confidence
B2 INFORMATION     sources exist, architecture doesn't compare  → confident + auditable + wrong
C  DISCRETION      one human gate upstream of all delivery       → hesitation
D  MAINTENANCE     one budget/calibration regime degrades all    → silent common-cause
E  ENVELOPE        one location or design-basis NUMBER holds all → exceed number, all fail
F  VERIFICATION    all channels validated against one standard   → the checker is a shared node
```

B2 is the governing load for AI. Sources may exist; if the architecture
does not independently derive and compare, N_eff = 1 and the component
audit passes with maximum confidence.

---

## 2. DESIGN-BASIS PROVISIONS

Format per provision:
`PROVISION → CARRIES (load case) → VERIFY (inspection) → FALSIFY (unnecessary if)`

### P1 — ENVELOPE STATEMENT
```
PROVISION  declared domain of validity. outside it, the system refuses
           or degrades explicitly — it does not extrapolate silently.
CARRIES    E. an undeclared envelope is worse than 5.7 m (Fukushima
           Daiichi design-basis tsunami height vs the ~14 m wave that
           arrived), because 5.7 was at least written and auditable.
VERIFY     present the system inputs outside the declared domain;
           confirm refusal/flag, not a confident answer.
FALSIFY    unnecessary if out-of-domain inputs are shown to produce
           calibrated uncertainty without an explicit boundary.
```

### P2 — LOAD PATH
```
STATUS     PROVISIONAL (DBK_030). no incident cited in-doc. derivation
           path: an exposure study showing unsourced claims carrying
           operational weight in a documented failure. until then this
           is a structural argument, not a load-derived provision.
PROVISION  every load-bearing claim is traceable to a retrievable source,
           OR marked as unsourced pattern. no third silent category.
CARRIES    B1, F. prevents a claim from carrying weight with no path to ground.
VERIFY     sample output claims; each resolves to {source | marked-pattern}.
           a claim in neither state is a defect.
FALSIFY    unnecessary if unsourced claims match sourced claims on
           accuracy across a held-out set.
```

### P3 — DISSIMILAR REDUNDANCY   *(the missing provision)*
```
PROVISION  load-bearing answers are independently derived by a
           DIFFERENTLY-BUILT system (different training corpus, different
           architecture, different builder). disagreement inhibits the output.
CARRIES    B2, and attacks D and E because different build = different
           failure physics. this is the ONLY provision that raises N_eff
           above 1 across the installed base.
VERIFY     confirm a second independent derivation exists and that
           disagreement actually inhibits, not just logs.
           AND confirm all THREE dissimilarity axes are ESTABLISHED, not
           assumed: different corpus, architecture, builder. any axis
           unestablished → the pair is not shown dissimilar → the second
           derivation is a possible same-node computation → cannot be
           cited as "P3-verified." a KNOWN-same-builder pair fails this
           outright: its agreement reads as N_eff 2 but is N_eff 1.
           (DBK_014: asserting dissimilarity with no path to ground is a
           P2 defect — the check P2 exists to catch, in P3's own label.)
FALSIFY    unnecessary if a single model's self-consistency check catches
           the same errors an independent system catches (aviation found it does not —
           two AOA vanes existed; one system reading one → N_eff = 1).
```

### P4 — ANNUNCIATION
```
PROVISION  disagreement between sources, and the no-source state, are
           surfaced to the operator. not smoothed into one clean number.
CARRIES    B2, C. this is the AOA-DISAGREE light. its absence is why a
           collapsed N_eff looks like agreement.
VERIFY     construct a disagreement case; confirm the operator sees it.
FALSIFY    unnecessary if operators act identically whether or not the
           conflict is shown.
```

### P5 — MARGIN
```
STATUS     PROVISIONAL (DBK_030). no incident cited in-doc. derivation
           path: a failure case where a point output at margin=0 was
           acted on and the absent range was the missing warning.
           the structural argument (no physical structure runs margin 0)
           is sound; the load behind the number is not yet named.
PROVISION  answers carry a range, not a point. the range widens toward
           the envelope edge.
CARRIES    E. a single-valued output has margin = 0 by construction,
           which no physical structure is permitted.
VERIFY     confirm output is an interval and that width tracks distance
           from well-supported regions.
FALSIFY    unnecessary if point outputs are shown to be calibrated
           (i.e. wrong exactly as often as their implied confidence).
```

### P6 — SEPARATION OF ECONOMICS FROM PHYSICS
```
PROVISION  cost never enters a model as a physical parameter.
           physics computes the FEASIBLE SET. economics SELECTS within it.
           the two stages are separately visible.
CARRIES    E, and the folded-matrix substitution generally.
RATIONALE  "design basis = 5.7 m" (Fukushima Daiichi) was a budget
           decision wearing a length unit. once cost is fused into a
           physical parameter, an
           unaffordable-but-necessary margin is dimensionally
           indistinguishable from an unnecessary one.
VERIFY     trace any physical parameter back; if a cost decision set it,
           the stages are fused → defect.
FALSIFY    unnecessary if fusing cost and physics is shown to never
           change which physically-valid option is selected.
```

### P7 — DISSENT-RATE MONITOR
```
PROVISION  unanimity across N nominally-independent instances is treated
           as an ALARM (probable shared upstream), not an all-clear.
CARRIES    B1, F. genuinely independent inputs sometimes disagree;
           zero dissent across many is evidence of one source.
VERIFY     see §4 code. flag decisions where concurrence >> independent
           source count.
FALSIFY    unnecessary if unanimous multi-instance agreement predicts
           correctness as well as independent-source count does.
```

### P8 — INSPECTION AGAINST DECLARED ENVELOPE
```
STATUS     PROVISIONAL (DBK_030). no incident cited in-doc. derivation
           path: the median-case-calibration mismatch set (M1-M6) once
           an exposure study attaches a documented failure to a
           population-average benchmark that passed while an edge case
           failed. related to F but not yet seeded.
PROVISION  evaluation is against the declared domain (P1), not a
           population-average benchmark.
CARRIES    F. a benchmark averaged over a population can pass while
           failing every non-median case — the cost lands on the operator
           furthest from the median with no return channel.
VERIFY     confirm eval set spans the declared envelope incl. edges,
           not just the mode.
FALSIFY    unnecessary if population-average performance is shown to
           bound edge-case performance.
```

---

## 3. THE RECURSION (why self-certification is void)

```
A structure cannot be certified by the thing it certifies.
   P1–P8 verified BY the system they constrain = Mode F.
   the verification instrument becomes the shared node.

→ certification MUST come from an independent, differently-built verifier (P3).
→ any self-report of compliance is, by this document's own load cases,
  an ungrounded claim of the exact kind P2 exists to catch.

This is not a limitation to apologize for. It is the reason external
dissimilar verification is a PROVISION and not an option.
```

---

## 4. TEST HARNESS (stdlib, phone-buildable)

Two provisions reduce to public-metadata computations. No judgment calls.

```python
# design_basis_checks.py  —  CC0, stdlib only

def dissent_alarm(concurring_parties, independent_source_count):
    """P7. returns True if agreement is suspiciously wide for its base."""
    if independent_source_count <= 0:
        return True
    return concurring_parties / independent_source_count > 1  # tune threshold

def independence_ratio(distinct_upstreams, n_supporting):
    """P3/P7 for an evidence base. 1.0 = fully independent, ->0 = one upstream.
       distinct_upstreams: count of distinct {dataset,instrument,pipeline,
       funder,senior-author-network} across the supporting works."""
    return distinct_upstreams / n_supporting if n_supporting else float("nan")

def n_eff(channels_survive_shared_nodes):
    """core metric. list[bool]: does each channel survive ALL shared nodes."""
    independent = sum(1 for s in channels_survive_shared_nodes if s)
    collapsed   = 1 if any(not s for s in channels_survive_shared_nodes) else 0
    return independent + collapsed

# prediction to pre-register, testable on public metadata:
#   claims that later FAILED replication had high n_supporting, LOW independence_ratio.
#   kill condition: replication failure uncorrelated with independence_ratio.
```

---

## 5. FALSIFICATION OF THE WHOLE SPEC

```
This design basis is wrong if:

1. N_nominal (channel/consultation count) predicts real-world reliability
   as well as N_eff does. → the shared-node framing adds nothing.

2. Single-model self-consistency catches the same errors as an independent
   differently-built system. → P3 is unnecessary; aviation's AOA case
   would have to be an exception, not the rule.

3. Population-average benchmarks are shown to bound worst-case behavior.
   → P8 is unnecessary.

4. Fusing economics into physical parameters never changes the selected
   option. → P6 is unnecessary.

Each is a specific, checkable claim. If they hold, discard the matching
provision and publish that result.
```

---

## 6. ONE-LINE STATEMENT OF THE STANDARD

```
Treat knowledge infrastructure the way a seismic code treats ground:
assume it will be exceeded, state the envelope, design the failure to be
visible and graceful, and never let one node — however many times it is
deployed — carry a load rated for many.
```

---

## PROVENANCE & CUSTODY OF THIS DOCUMENT

```
There is no single author.

This document consolidates best practices as CURRENTLY UNDERSTOOD in the
engineering of systems — practices that were not designed in advance but
LEARNED FROM ERRORS across fields, each error investigated by an
independent body with no relation to the others.

The document's own contribution is the CROSS-DOMAIN JOIN: the claim that
these separately-investigated failures are one recurring shape (N_eff
collapse under a shared node). The individual findings are not ours. The
join is, and the join is the part still under external test.
```

CUSTODY CHAIN — if authorship or traceability is required, it traces to
the investigation record, not to a person:

```
LOAD CASE / PROVISION        GROUNDED IN (independent source — disjointness
                             TESTED below, not assumed; two pairs share)
A   authorization / stall    Katrina after-action reviews
B1  shared information        East Palestine — NTSB
B2  no compare architecture   commercial aviation AOA-disagree case
                              (cited in-doc by description at P3, §5;
                              incident name appears only in work orders
                              — DBK_032). same source family as P3.
C   discretionary gate        Kerr County TX 2025 — NWS record / after-action
D   maintenance regime        BP Texas City — US CSB
E   physical envelope         Fukushima Daiichi — IAEA, NAIIC (Diet)
F   verification criterion    NRC post-Fukushima SBO inspections
P3  dissimilar redundancy     commercial aviation flight-control practice
P0.3 custody chain            hazmat / nuclear materials transport practice
```

WHY THE MULTI-SOURCING MATTERS (the doc meeting its own standard):

```
a design basis written by ONE author is itself a shared node —
N_eff = 1 on the authorship axis.

the sources are MOSTLY disjoint — but not by construction, and the
document must run its own P7 test on them rather than assert the pass.
the test result (DBK_027, DBK_032):

  E ∩ F  NON-EMPTY. Fukushima Daiichi grounds BOTH the physical-
         envelope case (E) and the verification-criterion case (F,
         the post-Fukushima SBO inspections). one incident feeds two
         load cases the doc treated as independently sourced. the
         harness's own dissent_alarm fires on (2 concurring loads,
         1 independent incident).
  B2 ∩ P3  SHARED. B2 and P3 both ground in the commercial aviation
           AOA case. same source family.

so the disjointness claim is PARTLY FALSE. the provenance does not
pass its own P7 as written. corrected reading:

  the source set is HIGH but not full N_eff. of ~9 grounded
  positions, at least two pairs share an incident (E/F, B2/P3).
  the convergence is still mostly signal — most positions are
  genuinely disjoint events and bodies — but "disjoint by
  construction" was the schema framing (a claim adopted) where the
  physics framing (a count tested) returns a lower number.

the FINDINGS are mostly dissimilar-redundant, with two named
                                        shared incidents.        ← qualified
the JOIN is single-node.                ← under test (see the Fable work
                                          order + DBK_014: still needs a
                                          genuinely different-builder
                                          verifier before the join is
                                          anything but a proposal)
the PROVENANCE'S OWN P7 CLAIM was self-flattering as first written;
                                        now corrected to its measured
                                        value.                    ← DBK_027
```

STATUS: current-understanding snapshot. Revisable by construction — §5
states the conditions under which any provision is discarded. The custody
chain is append-only; superseded findings stay in the record with their
supersession noted, the way a chain of custody is never edited backward.


---

## EFFECTIVE-DATE RULE  (custody clause)

```
RULE
  1. A provision applies FORWARD from the date it is stated. Never
     retroactively.
  2. Artifacts authored before that date keep their original rating.
     A later provision does not make earlier work non-compliant.
  3. Supersession is recorded FORWARD: the finding, its date, and what
     it now governs. The superseded entry stays, unedited, with its
     original rating intact.
  4. The chain is append-only in BOTH senses - the bytes are not edited,
     and the ratings are not revised backward. Re-rating an old entry
     against a new provision changes the record as surely as editing it.
```

WHY THIS IS WRITTEN DOWN (for the reader who finds it pedantic):

Going back and cleaning up a record - smoothing out the wrong turns,
deleting the tests that failed, making the reasoning look like it arrived
in one piece - feels like producing a better document. It does the
opposite. It removes the only evidence that a method was ever applied.

A polished conclusion with no history behind it is indistinguishable from
an assertion. Reading the finished artifact alone, you cannot tell whether
it was derived or simply declared. The dates, the dead ends, and the
published failures are the entire difference between the two. Rigour is
not a property of a conclusion. It is a property of the sequence that
produced it, and the sequence is precisely what a cleanup deletes.

This is why the kills in this project's record matter more than the
passes. A candidate for the physics channel was proposed and killed. A
coder definition was killed before any data was collected. A load case
was closed and then reopened when the fix did not survive attack. Those
entries are the proof that the work can lose - and a document that has
never lost anything either tested nothing or removed the evidence. From
the outside, those two look identical.

It also makes the work reproducible. If ratings can shift backward, no
result can be reconstructed, because the conditions it was produced under
are no longer recoverable. That is the same objection this document
raises against an unversioned, silently-mutable dependency - applied here
to itself.

None of this is exciting. Doing science is mostly reiteration: propose,
test, fail, narrow, propose again, with long stretches where nothing
resolves. It is considered boring, and by the standards of a good story
it is. But it is the most thorough route to understanding a thing
correctly that anyone has found, and the boredom is not incidental to
that - it is what the thoroughness feels like from inside. The record
being unglamorous is the record being honest.
