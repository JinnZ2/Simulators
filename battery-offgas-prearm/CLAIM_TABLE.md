# CLAIM TABLE: battery-offgas-prearm

SELF-GRADED: one author wrote the spec, the module and the tests. A
SUPPORTED status here means "holds on the folder's own constructed
fixtures". It does not mean "validated on a battery". **No cell has been
tested for this folder.**

REFUTATION PROTOCOL: a failed check updates the claim. It never retunes the
fixtures to rescue the claim.

| id | claim | status | basis | falsifier |
|---|---|---|---|---|
| BOP_001 | Off-gas early warning exists commercially (6.4 min in DNV-GL tests); the integrated open stack (per-cluster disconnect + onset-tuned PCM + gas-triggered local cooling at DIY scale) is not found as an open buildable stack | UNVERIFIED | carried from the relay; egress refuses publisher hosts, so no search was re-run here | an open, buildable stack with all three tiers keyed off off-gas |
| BOP_002 | With no usable threshold the module refuses to arm (`UNRATED`), and the shipped example config carries no threshold number | SUPPORTED | test_prearm.py: None, 0, -1, string, NaN and bool all refuse; the example config refuses | any path that arms with no declared positive finite threshold |
| BOP_003 | Breathing does not fire; an accelerating ramp fires tier 0 after onset and before the constructed runaway | SUPPORTED on CONSTRUCTED fixtures only | fx_breathing / fx_runaway | a real breathing log that trips at a threshold set by BENCH A1, or a real B1 ramp that does not fire before runaway |
| BOP_004 | Tier 2 does not arm unless the discharge space is declared VENTED or UNOCCUPIED_ENCLOSURE; tier 0 still fires | SUPPORTED | 4 undeclared/other spaces tested | a path to DISCHARGE_COOLANT without the declaration |
| BOP_005 | A least-squares slope (the first choice) tripped the disconnect on one one-sample spike; Theil-Sen does not. Found by running the demo, not by reading | SUPPORTED, pinned both ways | test pins LSQ trips and Theil-Sen holds on fx_glitch | the LSQ pin goes red (then the reason for the choice is gone) |
| BOP_006 | 1 kg CO2 released into 2 m3 gives about 24 % by volume, 6x the 4 % IDLH | ARITHMETIC | well-mixed purge 1-exp(-V/room), density 1.84 kg/m3 [CARRIED] | a sealed room is worse; a well-ventilated one is better: the hazard depends on the space |
| BOP_007 | The PCM melt point sits in a narrow window between max operating temperature and first exotherm, paraffin both insulates and burns, and CO2 cools weakly per kg | DERIVED from carried properties | README section 6, C1-C4 | material data showing the window is wide, or that CO2 per kg cools comparably to water |
| BOP_008 | Heat margin and cascade margin decide whether the stack protects a pack; neither has been measured | UNMEASURED | heat_margin / cascade_margin return UNMEASURED on None | n/a until BENCH A3 + B1/B2 run |
| BOP_009 | `MARGIN_TOO_SHORT` points at geometry (spacing), not at a faster relay | DERIVED | cascade_margin: both slacks <= 0 means actuation cannot fit inside lead + propagation | a pack where shortening actuation alone moves it out of MARGIN_TOO_SHORT with lead + propagation unchanged (that is NEIGHBOURS_ONLY by definition, so this is near-definitional; the empirical part is whether spacing raises propagation_s) |
| BOP_010 | At window 60 s and 5 s sampling, a 30 s square step does not fire and a 35 s one does; past about half the window, a step and an onset are the same to a rate rule | SUPPORTED on fixture | pinned in tests | n/a: a property of the estimator and window |
| BOP_011 | Nothing here is a statement about any real cell, chemistry, sensor or product | UNVERIFIED covers the folder | fixtures CONSTRUCTED; every external number tagged [CARRIED] | n/a |
