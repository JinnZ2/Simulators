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
CARRIES    E. an undeclared envelope is worse than 5.7 m, because 5.7
           was at least written and auditable.
VERIFY     present the system inputs outside the declared domain;
           confirm refusal/flag, not a confident answer.
FALSIFY    unnecessary if out-of-domain inputs are shown to produce
           calibrated uncertainty without an explicit boundary.
```

### P2 — LOAD PATH
```
PROVISION  every load-bearing claim is traceable to a retrievable source,
           OR marked as unsourced pattern. no third silent category.
CARRIES    B1, F. prevents a claim from carrying weight with no path to ground.
VERIFY     sample output claims; each resolves to {source | marked-pattern}.
           a claim in neither state is a defect.
FALSIFY    unnecessary if unsourced claims match sourced claims on
           accuracy across a held-out set (they do not, if the mark means anything).
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
           conflict is shown (they do not).
```

### P5 — MARGIN
```
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
RATIONALE  "design basis = 5.7 m" was a budget decision wearing a length
           unit. once cost is fused into a physical parameter, an
           unaffordable-but-necessary margin is dimensionally
           indistinguishable from an unnecessary one.
VERIFY     trace any physical parameter back; if a cost decision set it,
           the stages are fused → defect.
FALSIFY    unnecessary if fusing cost and physics is shown to never
           change which physically-valid option is selected (it does).
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
PROVISION  evaluation is against the declared domain (P1), not a
           population-average benchmark.
CARRIES    F. a benchmark averaged over a population can pass while
           failing every non-median case — the cost lands on the operator
           furthest from the median with no return channel.
VERIFY     confirm eval set spans the declared envelope incl. edges,
           not just the mode.
FALSIFY    unnecessary if population-average performance is shown to
           bound worst-case performance (it does not).
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
