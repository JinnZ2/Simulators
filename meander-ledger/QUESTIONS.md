# QUESTIONS -- question harvest (work order PART B, the main output)

Mapped, not answered. Every entry carries six fields: `question`, `layer`
(L0..L5), `raised_by` (the slot, residual or run that raised it), `instrument`
(what would answer it), `cross_domain` (shapes that recur, forest first), and
`status`. A status is a placeholder (`OPEN`) plus what it waits on. Nothing here
moves to an answer without the instrument named in its own entry.
`tests/test_meander.py` T_QUESTIONS_SCHEMA checks the fields.

Order follows the work order's priority list: branch disagreements first, then
too-smooth results, then slot-6 curiosities (none reached; Q-17 says why), then
shapes that recur across forest and river.

Provenance tags: `[run_N]` is a result recomputed in this folder; `[recalled]`
is from the work order or memory and was not checked here (egress refuses the
publisher hosts); `[forest]` points at a file in `forest-model-ledger/`.

## A. Branch disagreements

### Q-01
question: The recalled ratio lambda ~ 10-14 W [recalled] and the dataset's 16,951 meanders (median 15.81, but only 11.6% in band, log-log slope 0.228) [run_3] disagree on the SHAPE of the relation, not only its value. Is the recalled ratio a property of rivers, of the hand-measured reaches it was fitted on, or of the measurement method?
layer: L5 (with L0 if the ratio is a budget consequence)
raised_by: MC_001 slots 3 and 4 supported (mixed width population, lambda floor at the DEM/vectorisation scale); slots 1 and 2 void
instrument: The same ratio measured on one set of reaches by two methods: field or aerial centreline wavelength vs the DS_THAPA DEM-inflection pipeline. Then re-fit with water bodies masked out. The Leopold-Wolman source data with its own method per point (DS_LEOPOLD_WOLMAN, not read).
cross_domain: [forest] BR_OBSERVATION_MODEL (the observation model as a branch, not a filter); allometric scaling laws whose exponent changes with the measuring scale; Simulators instrument-epistemology (the estimator is the instrument)
status: OPEN -- waits on the source tables (egress) and a second wavelength method on a common reach set

### Q-02
question: The toy settles at lambda/W 7.96-8.80 over three seeds [run_1]. The recalled band is 10-14 and the dataset median is 15.81. Which one is the toy failing to match, and which term carries the gap: the decay length 1/alpha, the cutoff rule, or the wavelength estimator?
layer: L3 (L4 for the cutoff, L5 for the estimator)
raised_by: run_1 base seeds; MC_002 (OPEN); BR_KINEMATIC_BEND vs BR_EMPIRICAL_SCALING (placeholder)
instrument: An ablation table over the three terms one at a time, with the estimator also run on a known synthetic sine-generated curve, so its bias is measured before any planform result is read.
cross_domain: [forest] three branches give three answers for one quantity (BR_FIRE_MEANFIELD vs BR_FIRE_PERCOLATION); a model that matches a ratio by tuning a length scale it already contains
status: OPEN -- waits on the estimator-on-known-curve check (Q-09) first

### Q-03
question: The file carries two wavelength columns that do not agree (Spearman +0.033) [run_3]. The shipped script produces one (`wavelength`, from coordinate differences); the other (`Wavelength (m)`) has no shipped method. Which column is the meander wavelength, and is either one built from W?
layer: L5
raised_by: MC_001 open_issue (shared_constraint unrun); run_3 flag 3
instrument: The code that produced `Wavelength (m)` (upstream repo or authors); a recompute of both columns from the published centerlines on ten meanders by hand.
cross_domain: two instruments for one quantity that do not correlate: Simulators aperiodic-order-sim-stack (two dimension estimators disagreeing on sign); [forest] L5 observation components
status: OPEN -- waits on the missing method

### Q-04
question: Theory recalled as PROPOSED (Ikeda-Parker-Sawai 1981 linear bend instability, and the Howard-Knutson kinematic reduction used here) predicts a preferred wavelength set by depth and friction. The dataset carries no depth and no friction. Can the theory's prediction and the data be put on one axis at all?
layer: L3 / L5
raised_by: BR_LINEAR_BEND_THEORY (placeholder) vs BR_OBSERVATION_DS_THAPA; no convergence_anchors between them
instrument: A dataset with depth or discharge per meander (DS_USGS_MEASUREMENTS gauged reaches, DS_GLOFAS_HAMILTON discharge) joined to centreline wavelength; the IPS paper read for its dimensionless form.
cross_domain: [forest] BR_MASS_BALANCE vs process branches with no shared observable; a theory and a dataset that share a name for the quantity and nothing else
status: OPEN -- waits on a join with a depth or discharge column

## B. Too smooth

### Q-05
question: Energy and water close to roundoff in every run [run_1]. They close because both sides are the same expression in this model (IDENTITY flag), so the closure carries no information. What would an energy budget that COULD fail look like for a meandering reach: bank work, transport work, form drag, overbank loss each as its own counter?
layer: L0
raised_by: MC_003 (RESOLVED as identity); L0_ENERGY_BUDGET, L0_WATER_BUDGET; T_IDENTITY_FLAGGED
instrument: Separate counters for slope work and for each dissipation path, computed independently, then closed. A planted leak in one path, to show the closure can fail.
cross_domain: [forest] CC_001 (N misclosure too smooth: a residual from one deterministic counter); closed-by-construction budgets wherever the flux table defines both sides
status: OPEN -- waits on independent dissipation counters (none exist in the toy)

### Q-06
question: Aspect 10 and Cf 0.005 give byte-identical planforms, as do aspect 40 and Cf 0.02 [run_1, T_ALPHA_ONLY]. The toy sees depth and friction only through alpha = 2 Cf / H. Is that a property of rivers (one combined parameter), or only of the kinematic reduction?
layer: L3
raised_by: MC_003 slot 1 supported (shared_constraint: the model's own algebra); AB_ALPHA_ONLY
instrument: A model with depth and friction entering separately (the full linear theory, or a 2D shallow-water run), at equal alpha and different H, Cf. Field pairs of reaches with matched H/Cf and different H.
cross_domain: [forest] a single combined parameter hiding two (BR_RENORMALIZATION's reduction of many couplings to one); dimensionless groups that collapse data only inside the model that defines them
status: OPEN -- waits on a non-kinematic model run

### Q-07
question: Sediment supply 0.2 and 2.0 give identical planforms and different bed stores [run_1, T_SUPPLY_NO_PLANFORM]. In the toy, supply never feeds back into migration. In rivers, does supply set bend growth rate (bar push), and is the missing coupling where the toy's ratio comes from?
layer: L0 -> L3 coupling
raised_by: MC_004 (RESOLVED: no coupling path exists in the code)
instrument: One coupling term (point-bar growth rate pushing the inner bank, or erodibility rising when the bed store is low), switched on and off, at three supply levels; field: migration rate against sediment supply for reaches with gauged load.
cross_domain: [forest] L2_GRASS_GROWTH (grasses go extinct in 10 of 10 seeds: a population the model carries without a coupling that sustains it); a budget closed exactly while the variable it books moves nothing
status: OPEN -- waits on a coupling term to ablate

### Q-08
question: Water closes because Q_in is Q_out by definition (steady discharge). Floods are where cutoffs happen. What does the planform do when Q varies, and does the cutoff rate track flood frequency or bend growth?
layer: L0 / L4
raised_by: AB_STEADY_Q; L0_WATER_BUDGET identity
instrument: A Q(t) series driving erodibility, with cutoff times logged against flood peaks; oxbow dating against gauge records where both exist.
cross_domain: [forest] fire threshold driven by drought series (L4_FIRE_FUEL_MOISTURE); event-driven thresholds read from a mean-state model
status: OPEN -- waits on a time-varying Q in the toy

## C. Estimator noise floors

### Q-09
question: The toy's wavelength estimator counts jitter-scale curvature sign changes as inflections [run_2], and the dataset's estimator has a floor near the DEM/vectorisation scale (lambda 1st pct 358 m) [run_3]. Two estimators, one failure: is there an inflection estimator whose floor is stated before it is used?
layer: L5
raised_by: run_2 flag (estimator counts jitter); MC_001 slot 4; L5_WAVELENGTH_ESTIMATOR
instrument: Run each estimator on synthetic curves of known wavelength with added noise at known amplitude and sampling; report the wavelength below which it returns the noise scale instead. Register the case in tools/known_answer.py style.
cross_domain: Simulators null-harness (can a gate stay silent); [forest] CC_001 numerical-artifact slot; detection floors in any threshold-crossing count
status: OPEN -- waits on the known-curve run

### Q-10
question: Halving node spacing (ds 0.5 to 0.25) moves lambda/W from ~8 to 2.62 [run_2]. The toy is not grid-converged. Is the ratio it reports a property of the model or of ds?
layer: L3 (numerics)
raised_by: run_2 ds 0.25 case
instrument: A ds sweep (1.0, 0.5, 0.25, 0.125) with smoothing scaled to physical length rather than node count, and the estimator's own floor (Q-09) subtracted.
cross_domain: [forest] CC_001 (residual grows as dt shrinks); Simulators reasoning-dial (a knee that moves with the window)
status: OPEN -- waits on the sweep

### Q-11
question: The width axis mixes channels with lakes and reservoirs (W to 20,101 m; 190 meanders with W > 3000 m have median lambda/W 0.58) [run_3]. What fraction of the dataset's apparent scaling is a population mixture on W?
layer: L5
raised_by: MC_001 slot 3 supported; L5_WIDTH_WATERMASK; AB_WATERMASK_IS_CHANNEL
instrument: Mask water bodies (an external lake/reservoir layer) and recompute the ratio table by width bin; compare with a width taken from bankfull indicators rather than the water mask.
cross_domain: Simulators uninstrumented SCALAR_DEMAND and BUDGET_BOUNDARY (an axis whose boundary was drawn by the instrument); [forest] BR_OBSERVATION_MODEL
status: OPEN -- waits on a water-body mask

## D. Shapes recurring across forest and river

### Q-12
question: Cutoff (river) and crown-fire ignition (forest) are both thresholds that reset accumulated structure, and both make a statistical steady state out of growth plus reset. Do the two share a constraint set (growth toward a geometric limit, reset on contact), or only the word threshold?
layer: L4
raised_by: run_1 (steady state in sinuosity 1.4-3.2 with 7.5-8 cutoffs per 1000 steps); [forest] L4_FIRE_THRESHOLD_RUN5, L4_FIRE_FUEL_MOISTURE
instrument: For each system: the distribution of reset sizes and inter-reset intervals, and the removal test (SHAPE_SPEC section 4) -- remove the reset and check whether growth runs away in both.
cross_domain: forest fire threshold; avalanche and sandpile resets; earthquake stick-slip; SHAPE_SPEC section 1 (shape = constraint set)
status: OPEN -- waits on reset-size distributions from both models

### Q-13
question: The neck distance rule (neck 0.5 W vs 2 W) moves lambda/W only from 7.78 to 7.34 [run_2]. Is the steady-state ratio insensitive to the reset rule, and if so, is the reset rule doing anything but setting a rate?
layer: L4
raised_by: run_2 neck cases; L4_CUTOFF
instrument: A wider neck sweep (0.25-4 W) with cutoff rate, sinuosity and ratio reported apart; a comparison against chute cutoff (a second reset mechanism) switched on.
cross_domain: [forest] fire spotting parameter (0.2) where the grid converges onto mean field (CC_002): the reset detail that stops mattering above a threshold
status: OPEN -- waits on the sweep

### Q-14
question: The forest ledger finds a percolation grid converging onto a mean-field ODE at drought >= 0.5 (CC_002, OPEN). A meander's migration is local (upstream-weighted kernel) and its cutoff is non-local (two distant nodes meet). Is there an analogous handoff where a local migration description stops being enough?
layer: L3 / L4
raised_by: [forest] CC_002; this folder's L4_CUTOFF (non-local) in a local L3_BEND_GROWTH_KINEMATIC
instrument: The same planform evolved with cutoffs detected from neighbours only versus from the whole channel, and the divergence point recorded against sinuosity.
cross_domain: forest mean-field vs percolation; any model whose closure relies on nearest-neighbour interactions until a long-range contact appears
status: OPEN -- waits on a local-only cutoff variant

### Q-15
question: Self-similar scaling (creek to large river) is the work order's question. In the dataset lambda is nearly flat across a 100-fold width range [run_3]. Is the recalled self-similarity a property of rivers, or does it appear only after a width range is chosen?
layer: L5 (L3 if real)
raised_by: run_3 width-bin table; MC_001
instrument: The ratio by width bin with the bin edges and population fixed before reading, on two datasets of different origin; a power-law fit with its confidence interval and the alternative (lambda constant) compared by likelihood.
cross_domain: [forest] BR_MAXENT_METE and BR_RENORMALIZATION (scaling laws as a branch, with their own failure conditions); allometric scaling read on restricted ranges
status: OPEN -- waits on a second independent dataset

### Q-16
question: Vegetation lowers lambda/W (7.69 at veg 0.5, 6.82 at veg 1.0) and the cutoff rate in the toy [run_1]. In the toy vegetation only scales erodibility. Does vegetation act on rivers as a rate change (same shape, slower) or as a change in the shape itself (bank cohesion changing which bends survive)?
layer: L2 (bank) -> L3
raised_by: run_1 veg cases; L2_VEGETATION_BANK; L1_BANK_COHESION (placeholder)
instrument: Two vegetation implementations (erodibility multiplier vs a cohesion threshold below which banks do not move) compared on ratio, cutoff-rate and bend-size distributions; field: paired reaches across a riparian boundary.
cross_domain: [forest] L3_PAIRWISE_ADDITIVITY (a coupling assumed additive); biofilm and root binding in soils; a multiplier standing in for a threshold
status: OPEN -- waits on the threshold implementation

### Q-17
question: No coincidence card reached slot 6 (none_of_above) in this folder: each card's observation was explained by a supported slot or left OPEN with slots void. Is that because no observation here is surprising, or because every surprising one still has unrun slots?
layer: L5 (method)
raised_by: cards MC_001..MC_004; slot 6 is derived, never declared
instrument: Run the void slots of MC_001 and MC_002 (shared_constraint, local_normal_form) before any new observation is carded; count how many cards then reach slot 6.
cross_domain: [forest] coincidence_card.py; Simulators RESEARCH_RENDER section 6 (an empty slot is a finding)
status: OPEN -- waits on the void slots of MC_001 and MC_002

### Q-18
question: The coincidence card has no slot for a missing coupling (MC_004's cause: supply has no path into the planform). Shared constraint, normal form, statistical artifact, numerical artifact and projection all describe how two things agree; none describes a quantity that cannot move because nothing reads it. Is that a seventh cause, or slot 1 read in reverse?
layer: L0 / L5 (method)
raised_by: MC_004 (RESOLVED via shared_constraint, with the reading strained); [forest] L2_GRASS_GROWTH extinction
instrument: Code a set of known missing-coupling cases (forest grass, meander supply, any closed budget whose variable is unread) on the card and check whether slot 1's evidence text holds for each.
cross_domain: Simulators uninstrumented (excluded before first reading); dependency-ledger; forest grass extinction
status: OPEN -- waits on coding the known cases

### Q-19
question: Momentum is VOID: the toy carries no force balance, and the helical secondary flow that redistributes momentum in bends [recalled] is absent. Which of the toy's results would survive a momentum budget being added?
layer: L0 / L3
raised_by: L0_MOMENTUM_BUDGET (placeholder); L3_HELICAL_FLOW (placeholder); T_VOID_PRINTED
instrument: A reduced momentum balance per bend (centrifugal vs pressure vs bed friction) closed as its own L0 counter; then rerun run_1's ablations with it on.
cross_domain: [forest] C, P and energy budgets VOID and never closed; a budget left void rather than closed by assumption
status: OPEN -- waits on a momentum counter

### Q-20
question: The boundary audit line carries groundwater and overbank fines as void in every run [run_1]. Overbank deposition is how a floodplain is built and how oxbows fill. How much of the sediment the toy books as point_bar and oxbow_fill would leave the channel as overbank fines in a reach with floods?
layer: L0
raised_by: L0_BOUNDARY_AUDIT; AB_VOID_BOUNDARY
instrument: An overbank flux counter tied to Q above bankfull (needs Q-08's time series), closed beside the other terms; field: floodplain accretion rates against channel migration.
cross_domain: [forest] L0_BOUNDARY_AUDIT (leaching and deposition at the boundary); a boundary drawn where the counted fluxes stop
status: OPEN -- waits on Q-08
