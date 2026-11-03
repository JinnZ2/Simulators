README.md — Overview & Index
 
Purpose: Audit high-visibility scientific claims by separating the measured core (common denominator) from the interpretive overlay, then identifying unlogged joins (welds) where terms or claims are transferred across scales, species, or domains without a declared criterion change.
 
Three objects audited:
# Object Domain Measured core Overlay claim
1 Cuprate microstructure (3DXRD) Condensed matter Strain field + reconstructed 3-D microstructure of one LESCO crystal Wide domain walls reinterpret bulk superconductivity
2 NEC / Delta-toxin / CD9 Microbiology / medicine Toxin–CD9 binding, CRISPR screen, mouse protection Macrophage pyroptosis drives multi-organ NEC in humans
3 Anthropic ART Biotech / genomics Sequence association + RNA expression in phage Programmable gene-editing utility in mammalian cells

 
Core findings (one line each):
1. Cuprate: structural observation is solid; the superconductivity-consequence claim is an open inference with two opposing directions both live.
2. NEC: receptor identification is strong; the macrophage-as-primary-driver and mouse→human transfer remain unclosed by direct in-vivo measurement.
3. ART: sequence novelty is real; no enzymatic activity, targeting, or mammalian-cell interaction has been demonstrated. 
Cross-domain pattern: Each case elevates a privileged intermediate node (domain wall / macrophage / ART system) to decisive causal status on the strength of differential evidence, without closing the quantitative necessity of that node under the relevant conditions. Coherence is not closure. 
 
Section 1 — Audit Method (framework/audit-method.md)
 
Core vocabulary
Term Definition
Common denominator The measured object(s) that sit directly on the data. Everything else is overlay.
Overlay Interpretive claims built on the measurement (mechanism, consequence, utility).
Weld A join between distinct objects without a logged criterion move (e.g., same term used for two different thickness scales; species transfer without a scaling law).
Cut Separating a weld to examine its components and test whether the join is licensed.
Gap An unclosed inference between measurement and claim.

 
Procedure
1. Declare the common denominator. What is the shared physical referent? What quantities sit directly on it?
2. List assumptions that must be declared. For each, state what would be required to close it.
3. Identify term welds. Where does one word carry two incompatible referents? Where is existence fused with causal weight?
4. Execute cuts. Separate the weld; check whether the transfer is instrumented.
5. Status each transfer. Closed / open / hypothesis.
6. Design minimum viable verification. What measurement would decide between competing inferences?
7. Extract cross-domain patterns. What structural moves recur across cases? 
Recurring weld types
• Scale transfer: atomic → nanoscale; mouse → human; phage → mammalian cell.
• Existence → causal weight: "X exists" fused with "X is the missing ingredient."
• Average → local: bulk label transferred onto locally heterogeneous reality.
• Protection → full mechanism: successful intervention treated as confirmation of upstream narrative.
• Novelty framing as load-bearing: rhetorical elevation functioning as an implicit completeness claim. 
 
Section 2 — Case 1: Cuprate Microstructure (cases/01-cuprate-microstructure.md)
 
2.1 Common denominator
 
The measured strain field and reconstructed 3-D microstructure of one specific crystal of La₁.₆₇₅Eu₀.₂Sr₀.₁₂₅CuO₄ obtained by scanning 3DXRD.
 
Everything else — domain walls, heterogeneity, phase coexistence, consequences for superconductivity, "40-year assumption" — is interpretive overlay.
 
2.2 Assumptions that must be declared
1. 3DXRD strain maps correctly report the local lattice metric at the claimed spatial resolution (~tens of nm).
2. Broad low-strain regions at 300 K are continuous domain-wall volumes — not unresolved fine twinning, surface artifacts, or beam damage.
3. Low-temperature fine stripes are intrinsic bulk features of the same crystal — not a different volume or cooling-rate artifact.
4. Structural metrics of this type have historically been treated as spatially uniform in the bulk 214-cuprate literature.
5. Wide structural domain walls are capable, in principle, of coupling to electronic degrees of freedom strongly enough to require reinterpretation of prior bulk data. 
2.3 Quantitative claims (sit directly on the common denominator)
Claim Value
Low-strain (tetragonal-like) regions at 300 K ~150 nm thick, continuous volumes
Spacing between wall regions 0.5–2 µm
Wall thickness vs conventional domain wall ~2 orders of magnitude larger
At 100 K Fine orthorhombic-like stripes, 100–200 nm, embedded in tetragonal matrix
Approx. volume fraction of wall regions (300 K, mid-range spacing) ~10–15%
Reconstruction type Bulk (not surface-limited), strain maps from local lattice metric

 
2.4 Term welds
Weld Description
"Domain wall" Simultaneously names (a) classical atomic-scale interface and (b) newly observed ~150 nm low-strain volume. No logged criterion change. Thickness difference is the claim.
"Intrinsic heterogeneity" Fuses existence of spatial variation with the claim that this variation is the missing ingredient governing structural–electronic interplay. Existence ≠ causal weight.
"Nominally orthorhombic / tetragonal" Transfers average-structure label onto local reality the measurement shows is incomplete.
"Significant consequences for interpreting the interplay" Fuses observation with functional consequence. No simultaneous electronic probe on the same volume.
"40-year assumption of uniformity" Treats entire literature as uniformly committed to macroscopic homogeneity. Prior work already discussed twinning, phase coexistence, nanoscale disorder.

 
2.5 Functional transfer — two opposing inferences both live
Inference Mechanism Source
Walls suppress bulk SC Extended LTT-like volumes frustrate Josephson coupling Press framing / extrapolation
Walls enable filamentary SC Boundaries disrupt CDW coherence, open local SC pathways Paper's own low-T discussion + wider literature

 
Status: No local electronic probe (STM, transport, gap map, Josephson coupling) on the reconstructed volumes decides between them. Transfer is open.
 
2.6 Scope of gaps
Gap Status
Measurement layer (strain reconstructions) Closed — stands
Term welds (domain wall, heterogeneity, average/local) Open — no logged criterion moves
Functional transfer (structure → SC consequence) Largest open gap — two opposing inferences live
Historical framing ("40-year assumption") Overstated — prior work documented local deviations
Generality Open — one crystal, one composition
Causal closure Open — no controlled variation of wall thickness/density vs SC response

 
2.7 Minimum viable controlled test
 
Independent variable: Something that systematically changes wall/stripe volume fraction or connectivity while holding doping and average structure constant.
• Controlled cooling rate / annealing through LTO–LTT transition
• Uniaxial strain along [100]/[010] or [110]
• Small chemical substitution shifting LTO–LTT boundary 
Dependent variables (on same crystals/volumes):
• Structural: repeat 3DXRD to quantify wall thickness, volume fraction, connectivity
• Electronic: local SC gap/coherence-peak maps (STM/STS), Josephson plasma frequency, c-axis conductivity, local superfluid density 
Adjudication rule:
• ↑ wall fraction → ↓ bulk/local SC → supports "works against"
• ↑ wall fraction → ↑ filamentary/local SC → supports opposite
• Null result → falsifies strong causal coupling at these length scales 
Still missing: reversible lever with measurable effect; spatial registration between structural reconstruction and electronic probe; baseline statistics across multiple crystals.
 
Bottom line: Structural scales, competing hypotheses, and required measurement classes are defined. Gap is actionable; remaining problems are engineering (clean lever, spatial registration), not conceptual. 
 
Section 3 — Case 2: NEC / Delta-Toxin / CD9 (cases/02-nec-delta-toxin.md)
 
3.1 Common denominator
1. Enrichment of Delta-toxin⁺ C. perfringens (and serological evidence) in a subset of severe/fatal human NEC vs non-NEC controls.
2. Genome-wide CRISPR screen identifying CD9 as required for Delta-toxin cytotoxicity; direct binding to CD9 EC2 domain.
3. Mouse models: purified toxin or toxin⁺ bacteria → intestinal necrosis, multi-organ injury (incl. brain), lethality. Systemic/myeloid Cd9 deletion and neutralizing mAb markedly reduce phenotypes; epithelial-only deletion partial. 
Everything else — macrophage pyroptosis as primary driver, "subset of NEC is a specific-toxin-mediated disorder," therapeutic generalization to human infants — is overlay.
 
3.2 Assumptions that must be declared
1. Human association (toxin⁺ / serology ↔ severe NEC) is causal, not merely correlative.
2. Mouse models recapitulate initiating events and multi-organ cascade of human NEC — not a related but distinct toxinosis.
3. CD9 is the physiologically relevant receptor in vivo as in HeLa/CRISPR system; macrophage CD9 is the dominant target accounting for systemic/neurological injury.
4. Neutralization is sufficient to interrupt cascade even after colonization.
5. Fraction of human NEC that is Delta-toxin–driven is large enough and identifiable early enough for the axis to be therapeutically actionable. 
3.3 Term welds
Weld Description
"NEC" Used for multifactorial clinical syndrome in preterm infants and toxin-driven mouse pathology. Treated as sufficiently equivalent for causal transfer.
"Receptor" Weld of CRISPR hit + binding data in cell lines onto claim that CD9 is operative host factor explaining macrophage tropism and multi-organ injury in animals.
"Primary driver" (macrophage) Weld from differential protection (myeloid vs epithelial knockout); epithelial contribution acknowledged then backgrounded.
"Subset of NEC is specific-toxin-mediated" Fuses existence of toxin⁺ cases with stronger claim that toxin is dominant initiating cause (vs severity amplifier).

 
3.4 Receptor weld — detailed status
 
Measured (sits on data):
• CRISPR screen in HeLa: CD9 top hit
• CD9 KO → ~40,000-fold resistance; overexpression → sensitivity
• Direct binding: GST pulldown, biolayer interferometry, EC2 domain localization
• Anti-EC2 antibody blocks cytotoxicity in vitro
• CD9 expressed on macrophages (scRNA-seq, flow) 
Weld (inference):CD9 is the host receptor explaining macrophage tropism and the primary driver of in-vivo multi-organ pathogenesis. 
Two fused steps:
1. Cell-line receptor → physiologically dominant receptor on relevant cell type in vivo
2. Receptor occupancy on macrophages → causal chain producing intestinal necrosis, BBB failure, lethality 
Where tight: Systemic and myeloid Cd9 deletion strongly protective; epithelial deletion weaker; anti-toxin mAb protective.
 
Where open:
• No direct demonstration of toxin binding CD9 on macrophages inside tissue at pathogenic doses/times
• No quantitative occupancy/dose–response linking CD9 engagement → inflammasome/pyroptosis → BBB failure in vivo
• Alternative/parallel receptors not excluded at organism level (screen was HeLa, not primary macrophages)
• Partial epithelial protection acknowledged but not formally partitioned 
Status: Cell-biological receptor identification strong. Transfer to "macrophage CD9 is operative, rate-limiting host factor" is inference supported by differential knockout but not closed by direct in-vivo binding or quantitative causal attribution.
 
3.5 Human–mouse transfer — full scope
 
Disease-equivalence assumptions:
Dimension Human NEC Mouse model Unlogged difference
Population Almost exclusively preterm Neonatal or 4-week-old Gut/immune maturation differs
Etiology Multifactorial, often polymicrobial/culture-negative High-dose single toxin/strain Initiation sequence differs
Route/timing Enteral bacterial products on immature mucosa Systemic toxin injection short-circuits sequence Route/timing mismatch

 
Brain-injury transfer:
Side Observation Open joint
Human Severe NEC survivors: high neurodevelopmental impairment; toxin⁺ subset (n=2 with imaging): more ventricular enlargement Brain injury thought driven by systemic inflammation/cytokine storm over days–weeks; no evidence Delta toxin necessary for brain injury in ordinary NEC
Mouse Toxin/toxin⁺ bacteria → ependymal injury, ventricular widening; myeloid Cd9 deletion and anti-toxin Ab protect Lesions appear rapidly after high-dose toxin; not shown same macrophage–pyroptosis–BBB sequence operates at human-relevant concentrations/time scales

 
Status: Mouse brain phenotype real and CD9/myeloid-dependent. Correspondence to human NEC-associated brain injury remains inference across dose, timing, developmental stage, mechanism.
 
3.6 Regulatory/incentive precedents that license the transfer
• FDA/translational practice: Animal toxin models (botulinum, anthrax, diphtheria, Shiga) routinely accepted as supporting pathogenesis and antitoxin therapies. Toxin necessary + sufficient in animals + neutralizing Ab protects → human association treated as confirmatory.
• Orphan/rare severe disease logic: Lower bar for high-mortality neonatal conditions.
• Precedent of other bacterial toxins in gut disease: C. difficile, Shiga → "toxin⁺ strains → severe phenotype → antitoxin strategies." Delta toxin slotted into existing groove.
• Publication/funding incentives: Clean molecular axis (toxin–CD9–macrophage) with genetic + antibody protection far more fundable/publishable than "multifactorial, unclear." 
Consequence: Transfer is carried by a well-worn pathway that has worked for other toxins. Pathway still leaves quantitative/developmental mismatches unmeasured. Macrophage-centric mechanism better supported inside mouse than as explanation of human disease spectrum.
 
3.7 Minimum requirements for clean bridge test
# Requirement What it tests
1 Matched toxin exposure metric — measure Delta toxin / neutralizing capacity / anti-toxin titres in human toxin⁺ NEC and mouse models at pathology time points Common exposure scale
2 Cell-type/pathway concordance — in human surgical/autopsy tissue from toxin⁺ cases, quantify CD9, macrophage pyroptosis markers, local inflammasome activation; compare spatial/quantitative pattern to mouse Mechanism-level bridge
3 Developmental/dose scaling — mouse model across postnatal ages and toxin doses bracketing estimated human exposures; require macrophage dependence and brain phenotype intact at lower, human-plausible end Dose/age transfer
4 Temporal sequence test — both species: does macrophage activation/pyroptosis precede BBB failure and brain injury? Causal chain order
5 Fractional attribution in humans — larger toxin⁺ vs toxin⁻ cohort: incremental contribution of Delta-toxin exposure to brain-injury metrics after adjusting for confounders (GA, sepsis, surgery) Human explanatory power
6 Intervention concordance (highest bar) — if anti-Delta mAb or CD9-targeted approach tested in humans, pattern of protection (intestinal vs systemic vs brain) matches mouse ranking Full bridge

 
Decision rule:
• All six hold → bridge provisionally solid
• 1–3 hold, 4–6 fail → toxin is severity amplifier, not primary initiating driver in humans
• 1–2 fail → mouse model is related toxinosis, not recapitulation of human subset 
3.8 Highest-leverage verification experiments (macrophage node)
1. Direct in-vivo engagement: Labeled toxin + flow/imaging mass cytometry or proximity ligation/spatial transcriptomics on same sections as histopathology — quantify CD9 occupancy on tissue-resident/recruited macrophages in neonatal gut, blood, brain-adjacent compartments at pathogenic doses/times.
2. Quantitative dose–response inside macrophage: Inflammasome activation, gasdermin D cleavage, IL-1β release, cell death as continuous function of toxin dose and CD9 surface density on primary macrophages (neonatal vs adult, tissue vs blood). Parallel in myeloid Cd9 heterozygotes/partial knockdown — does protection scale with residual CD9?
3. Spatial/temporal registration of cascade: Simultaneous imaging/multi-omics of macrophage pyroptosis, cytokine gradients, endothelial/BBB integrity, early neuronal injury at multiple early time points — is macrophage death necessary and temporally prior to BBB failure?
4. Fractional contribution test: Restore CD9 selectively in macrophages vs epithelium (and vice versa) in knockout backgrounds; measure recovery of each pathology endpoint (intestinal necrosis score, BBB leakage, ventricular injury, lethality). Numerical partition, not "primary/partial" language.
5. (ART side, if pursued): Test whether ART system, once expressed, produces detectable activity (RNA binding, DNA modification, immune activation) inside primary macrophages or macrophage lines. Negative result bounds whether sequence observation has immediate interface with same cell type central to toxin pathology. 
Priority: 1 & 2 first (direct engagement + quantitative response on macrophage). 3 next (temporal/spatial causality). 4 for formal attribution. These turn macrophage from narrative endpoint into instrumented node. 
 
Section 4 — Case 3: Anthropic ART (cases/03-anthropic-art.md)
 
4.1 Common denominator
• Sequence association of a reverse-transcriptase family with CRISPR-like repeat arrays
• Arrays produce short RNAs 
4.2 Overlay
• Any enzymatic activity
• Any programmable targeting
• Any interaction with host cells (including macrophages)
• Any capacity to operate inside mammalian cells 
4.3 Alignment with NEC case
Dimension NEC / Delta toxin Anthropic ART
Measured Toxin binds CD9; CD9 enriched on macrophages; myeloid Cd9 deletion protective; epithelial deletion weaker Sequence association of RT family with CRISPR-like arrays; arrays produce short RNAs
Open Quantitative chain from CD9 occupancy on tissue macrophages → inflammasome/pyroptosis magnitude → BBB failure/multi-organ injury Any enzymatic activity, programmable targeting, host-cell interaction
Shared structural feature Causal story handed to macrophage but not instrumented inside it at relevant scale System not yet shown to interact with any mammalian cell; future gene-editing utility would confront same macrophage barrier (delivery, expression, off-target immune activation, intentional targeting of macrophage pathways)

 
4.4 Shared gap structure
1. Cell-type resolution stops at macrophage boundary — both terminate strongest evidence at macrophage membrane or immediate vicinity.
2. Functional transfer is shared open joint — both move from solid molecular observation to organism-level claim without intermediate measurements closing loop on macrophage.
3. Incentive/framing pressure similar — both narratives benefit from elevating macrophage (or potential editing system) to decisive causal node while quantitative/spatial data justifying elevation are missing. 
Curiosity: Two independent high-visibility results both terminate strongest evidence at macrophage membrane or immediate vicinity, then rely on inference to carry rest of pathology or biotechnological promise. That common termination point is the interesting alignment. 
 
Section 5 — Cross-Domain Patterns (patterns/cross-domain-patterns.md)
 
Six recurring structural moves across all three objects:
 
Pattern 1: Observational core + functional overlay
 
Every case has a clean high-resolution measurement (3DXRD strain maps; toxin–CD9 binding + CRISPR screen; sequence association + RNA expression) joined to a stronger claim about mechanism or utility. The join is rarely given its own experimental status.Assumption that may be missed: that the strength of the core automatically licenses the overlay. It does not. The overlay is a separate claim. 
Pattern 2: Privileged intermediate node
 
Each story elevates one intermediate (domain walls/heterogeneity; macrophage; ART system) as decisive causal/enabling object. Differential evidence is offered (knockouts, thickness measurements, sequence novelty), but quantitative necessity of that node is not closed.Assumption that may be missed: that identifying a necessary component is the same as proving it is the rate-limiting or primary driver under the relevant conditions. 
Pattern 3: Scale or species transfer without a scaling law
Case Transfer
Cuprate Atomic-scale domain-wall concepts → 150 nm volumes
NEC Mouse toxinosis → human preterm NEC
ART Phage sequence feature → mammalian gene-editing utility

 
In each case the transfer crosses a scale or organism boundary without an explicit scaling relation or bridging measurement.Assumption that may be missed: that qualitative resemblance plus precedent is sufficient warrant for the transfer. Precedent is not measurement. 
Pattern 4: Historical or novelty framing as load-bearing
 
"40-year assumption of uniformity," "first identification of the virulence factor," "novel enzyme system reminiscent of CRISPR." These frames increase apparent importance while remaining loosely coupled to data.Assumption that may be missed: that rhetorical elevation is merely packaging. It often functions as an implicit claim about completeness or uniqueness that shapes how residual gaps are discounted. 
Pattern 5: Protection or intervention as retrospective validation
 
Antibody protection, myeloid knockout protection, or mere existence of plausible editing system treated as confirmation that preceding causal story is correct. Protection shows necessity of targeted step under conditions tested; it does not automatically confirm full upstream narrative.Assumption that may be missed: that successful intervention equals full mechanistic closure. 
Pattern 6: Single-specimen or early-result generalization
 
One crystal, one small clinical toxin⁺ subset, one search campaign that does not reliably re-find the hit. The move from observed instance to class is made quickly.Assumption that may be missed: that the first high-signal example is representative rather than a boundary case. 
 
Section 6 — Meta-Pattern: The Auditor's Blind Spot (meta/auditor-blind-spot.md)
 
The evaluation frame itself is good at locating welds and open transfers once the object is on the table. The recurring risk is that the same frame can still treat the existence of a coherent story as partial evidence for the story's completeness.Coherence is not closure. 
The patterns above are the places where coherence most often substitutes for the missing measurement. These are the cross-domain regularities most likely to hide assumptions that travel with the auditor rather than with the individual papers.
 
Audit-frame checklist
 
When evaluating any new object:
[ ] What is the common denominator? (What sits directly on the data?)
[ ] What is overlay? (Mechanism, consequence, utility claims)
[ ] Where are the term welds? (One word, two referents? Existence fused with causal weight?)
[ ] What is the privileged intermediate node? Is its quantitative necessity closed?
[ ] Is there a scale/species transfer? Is there a scaling law or bridging measurement?
[ ] Is novelty framing doing load-bearing work?
[ ] Is protection/intervention being used as retrospective validation?
[ ] Is a single specimen/early result being generalized to a class?
[ ] Is coherence being mistaken for closure? 
 
Section 7 — Verification Protocols (experiments/verification-protocols.md)
 
Cuprate: controlled causal test
 
Goal: Decide between "walls suppress SC" and "walls enable filamentary SC."
 
Lever: Cooling rate/annealing through LTO–LTT; uniaxial strain; small chemical substitution shifting LTO–LTT boundary — changes wall/stripe volume fraction while holding doping/average structure constant.
 
Readout: Repeat 3DXRD (wall thickness, volume fraction, connectivity) + local electronic probe on same volumes (STM/STS gap maps, Josephson plasma resonance, c-axis conductivity, local superfluid density).
 
Decision rule: ↑ wall fraction → ↓ SC (suppression) vs ↑ SC (filamentary) vs null (no strong coupling at these scales).
 
Engineering gaps: Reversible lever with measurable effect; spatial registration between structure and electronic probe; baseline statistics across crystals.
 
NEC: bridge test (6 requirements)
1. Matched toxin exposure metric (human vs mouse)
2. Cell-type/pathway concordance in human tissue (CD9, pyroptosis markers, inflammasome)
3. Developmental/dose scaling in mouse (bracket human exposures)
4. Temporal sequence test (macrophage activation before BBB failure?)
5. Fractional attribution in humans (incremental effect after confounders)
6. Intervention concordance (pattern of protection matches mouse ranking) 
Decision rule:
• All six → bridge provisionally solid
• 1–3 hold, 4–6 fail → severity amplifier, not primary driver
• 1–2 fail → related toxinosis, not recapitulation 
NEC: macrophage node instrumentation (priority order)
1. Direct in-vivo engagement (labeled toxin + spatial methods on histopathology sections)
2. Quantitative dose–response inside macrophage (pyroptosis markers vs toxin dose/CD9 density; partial knockdown scaling)
3. Spatial/temporal registration of cascade (multi-omics at early time points)
4. Fractional contribution test (selective CD9 restoration in macrophages vs epithelium)
5. ART side: test activity in primary macrophages (negative result is high-value) 
ART: bounding experiments
• Express ART system in primary macrophages / macrophage lines
• Assay for RNA binding, DNA modification, immune activation
• Negative result bounds whether sequence observation has immediate interface with macrophage — the cell type central to the toxin pathology alignment 
 
Summary Map
┌─────────────────────────────────────────────────────────────────────┐
│                    COMMON DENOMINATOR (measured)                    │
│  Cuprate: 3DXRD strain field, one crystal                           │
│  NEC: toxin–CD9 binding, CRISPR screen, mouse protection            │
│  ART: sequence association + RNA expression                         │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │   TERM WELDS (unlogged)  │
              │  • Domain wall: atomic vs 150 nm
              │  • Receptor: cell line vs in vivo
              │  • NEC: clinical vs mouse
              │  • Novelty framing as load-bearing
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │  FUNCTIONAL TRANSFER     │
              │  (largest open gap)      │
              │  • Structure → SC consequence
              │  • Mouse → human disease
              │  • Phage → mammalian utility
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │  PRIVILEGED NODE         │
              │  (asserted, not closed)  │
              │  • Domain wall
              │  • Macrophage
              │  • ART system
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │  VERIFICATION PROTOCOLS  │
              │  (actionable, engineering-limited)
              └─────────────────────────┘
 
Meta-rule: Coherence is not closure. The auditor's own frame is vulnerable to treating a well-formed story as partial evidence of its completeness.
