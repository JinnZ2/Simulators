# CLAIM TABLE: corn-stunt-forensics

SELF-GRADED, and the harder case: the method is the operator's, the pass
was run by the model, and the model is reporting on it. No cell here is
supported by field data. Every external fact is `[CARRIED]` and
unchecked.

REFUTATION PROTOCOL: a failed check updates the claim. It never adjusts
the pass to rescue it.

| id | claim | status | basis | falsifier |
|---|---|---|---|---|
| CSF_001 | The method (backward bins, frame-cycle, dissonance-as-diagnostic, gap-as-constructive) produced a checkable hypothesis on a system none of its four moves was written for | SUPPORTED, n=1 | D3 exists and names a mechanism with a stated subject | a second pass on a second system producing no checkable output, or D3 turning out to restate a source the pass read |
| CSF_002 | D3, the US second-season / irrigated host ladder, is a HYPOTHESIS and not a finding | UNVERIFIED by construction | nothing here establishes the ladder exists at scale, was present in 2024, or carried the vector population | acreage and planting-date records for late-season and irrigated corn in the affected region, against the vector's host-availability requirement |
| CSF_003 | The ~20-day vector latent period and ~3-week symptom lag put the observable signal after the window in which it could be acted on | DERIVED from CARRIED lags | two carried order-of-magnitude figures; the inference is arithmetic on them | measured lags short enough that a symptom survey is actionable, or an action whose window is wider than the sum |
| CSF_004 | Trap abundance and trap infectivity are different quantities, and an abundance series leads an infectivity series by about the latent period | DERIVED from CARRIED | consequence of CSF_003's first lag | an assay showing infective fraction tracks abundance with no lag |
| CSF_005 | `battery-offgas-prearm/prearm.py`'s rate-of-rise estimator transfers to a trap count series, including the Theil-Sen-over-least-squares choice | ASSERTED, NOT BUILT | the estimator is slope-on-a-noisy-series in both cases; BOP_005 pins why the median slope was chosen | a trap series on which the glitch-rejection property does not hold, or a count distribution for which a median slope is the wrong estimator |
| CSF_006 | Volunteer-corn removal and staggered planting are INTA advice; window compression across neighbours is the opposite move and cannot be taken by one grower | CARRIED (advice); DERIVED (the asymmetry) | INTA items carried; the asymmetry follows from staggering lengthening the regional host window while shortening each field's exposure | the advice as published already addressing the regional window, or a single-grower route to compression |
| CSF_007 | Rows D1, D2, D4, D5 and gaps G1-G5 did not survive the context break and are NOT_RECOVERED rather than reconstructed | SUPPORTED | the folder records them as absent; no content is supplied for any of them | n/a: a reconstruction would refute the discipline, not the claim |
| CSF_008 | The pass had no field data, no trap series and no retrievable primary source; its corpus was six news-and-extension items selected on the outbreak having happened | UNVERIFIED, and this is the folder's own frame-selected-on-the-variable limit | one named 2026 extension source refused CONNECT (egress allowlist) and is carried unchecked | a pass run against a primary corpus assembled before the outcome was known |
| CSF_009 | Nothing here is a statement about any farm, field, grower, extension office, or the actual 2024 outbreak | UNVERIFIED covers the folder | every external fact [CARRIED]; no data read | n/a |

## Note on what a second party can attack cheapest

`CSF_002`. The acreage and planting-date records D3 turns on are
published, and the pass did not reach them. A reader with those records
can refute or support the hypothesis without re-running the method.
