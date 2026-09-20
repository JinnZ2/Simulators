# CLAIM_TABLE -- additivity-inheritance

Claims are about the INSTRUMENT and the delivered order. Corpora are
CONSTRUCTED, R3 is NOT_RUN, the history is CARRIED and unread. `AI_*` ids
are permanent. A refuted claim is updated; the checks are not retuned to
preserve it.

---

| id | claim | status |
|---|---|---|
| AI_001 | R1 codes a corpus by the order's four codes and the C-share (present-and-unstated) rises monotonically with declared field distance on a corpus built to carry that shape; the non-monotone finding branch is reachable | SUPPORTED, [CHOICE 1]; known-answer run on the coder |
| AI_002 | R2 counts non-additive phenomena that had to fight the frame; 3 of 4 on the constructed set, share None on empty | SUPPORTED, constructed |
| AI_003 | R3 is NOT_RUN: prior art at the merge specifically is unsearched and the hosts are egress-blocked; if it exists WO-9 becomes a pointer | NOT_RUN, recorded |
| AI_004 | R4 reproduces the citation-trace false negative on the eugenics/Mendel graph: the citation trace does not reach the precondition, the structural trace does; and with a citation edge both traces reach it, so it is not CONSTANT_SILENT | SUPPORTED, [CHOICE 3]; the order's portable result |
| AI_005 | on a balanced 2x2 the additive model's residual IS the interaction SS = (a-b-c+d)^2/4 = 9 on the demo cells; a real interaction is assigned to noise by the decomposition, arithmetic not a downstream choice | SUPPORTED, arithmetic; registered |
| AI_006 | no primary source is read and every corpus is CONSTRUCTED; the lineage claim (variance partitioning descends from the merge, heritability inherits additivity) is CARRIED and not verified here, and the order says test it first | UNVERIFIED |

---

## AI_004 -- the false negative reproduced

The order's methodological result generalises past the genetics: citation
tracing cannot detect a precondition carried by a shared structural
inheritance. The graph is CONSTRUCTED to the order's own description --
both camps inherit the fork (an inheritance edge), the fork carries the
eugenics precondition, and the camps and Fisher cite each other (citation
edges). A BFS over citation edges from the Fisher synthesis does not reach
the precondition; a BFS that also follows inheritance edges does. That is
the false negative, and it is a property of which edges the trace follows,
not of the particular history. When the precondition is reachable by a
citation edge, both traces reach it -- so the instrument distinguishes the
two cases and does not simply always miss.

## AI_005 -- the interaction is lost by the decomposition, not later

Candidate 1 of the order says additivity is what the gas-molecule device
buys: effects sum, variance partitions, and anything non-additive survives
only as nuisance. On a balanced 2x2 that is exact. The total SS partitions
into SS_G + SS_E + SS_interaction with no remainder, and a main-effects
model -- the additive one -- has SS_interaction as its residual. So a real
gene-environment interaction of size (a-b-c+d)^2/4 is not modelled and
mis-assigned somewhere downstream; it is assigned to the residual by the
decomposition itself. The demo cells `[[10,12],[12,20]]` give 9, checked
by hand and registered.
