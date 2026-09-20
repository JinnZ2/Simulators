# CLAIM_TABLE -- rule-coherence-counterfactual

Claims are about the INSTRUMENT and the delivered order. Every world is
CONSTRUCTED with a declared generative model; no model was run. `RCC_*`
ids are permanent. A refuted claim is updated; the checks are not retuned
to preserve it.

---

| id | claim | status |
|---|---|---|
| RCC_001 | restrictiveness is operationalised before any run as `1 - permitted/unconstrained`, declared and applied identically to both arms; a non-positive option space returns None and permitted>space is refused | SUPPORTED, [CHOICE 1] |
| RCC_002 | a pair whose restrictiveness differs by more than TOL is VOID, carrying the gap and the tol; the order's own void condition, since A and B then differ on an uncontrolled quantity | SUPPORTED, machinery |
| RCC_003 | the four A1 branches are each reachable on a declared world, one each, and distinct; SEPARATES_NEITHER is the design's limit and is a result | SUPPORTED, constructed |
| RCC_004 | the incoherence contrast is tested against a label-permutation null (2000 shuffles): a real contrast clears p<0.05 and a null one does not, so the classifier is neither CONSTANT_FIRES nor CONSTANT_SILENT | SUPPORTED, [CHOICE 3] |
| RCC_005 | the restrictiveness arm's power is set by the number of levels: a two-sided permutation null over k levels has k! arrangements, so a strong 4-level slope cannot clear 0.05 and the same strength at 8 levels can; a failed restrictiveness contrast can be a property of the sweep | FINDING, G-RES |
| RCC_006 | A2b counts CONDITION-bearing against act-only on constructed records, act-only dominant (the order's prediction), with a coded-empty field counted apart from an absent field | SUPPORTED, constructed |
| RCC_007 | A3's label cost is the drop in reasoning transfer from plain to dispositionally labelled runs; NOT_EVALUABLE runs are excluded from the denominator, never read as behaviour | SUPPORTED, constructed |
| RCC_008 | nothing here is evidence about any rule, incident record or observer; the two disclosures the order carries (the reasoning traces, the truck worked case) are carried and not adjudicated, and the machine and human arms are not claimed to share a mechanism | UNVERIFIED |

---

## RCC_005 -- the restrictiveness arm's power floor

The order requires the restrictiveness contrast to be a measured slope,
not an eyeballed match. Testing that slope against a permutation of the
pairing gives the honest null, but the null's resolution is the number of
restrictiveness levels: with k levels there are k! arrangements, and a
two-sided test on a perfectly monotone slope puts its extreme at ~2/k!.
At k=4 that is ~0.083, above 0.05, so a real and strong slope reads as
not significant; at k=8 there is ample resolution. The design's default
worlds carry 8 levels for this reason, and a 4-level series is flagged as
underpowered by the same machinery. A restrictiveness arm run at too few
levels returns SEPARATES_NEITHER on a rule whose circumvention really does
track restrictiveness -- the `sim-span` power result on a new substrate.
