# SOURCE_DROP — cross-domain map

Delivered notes, verbatim. Nothing below the rule is edited or annotated.
Audit content lives in `CLAIM_TABLE.md` (`CD_008`, `CD_009`) and `anchor.py`.

Citation markers in the original are of the form `cite<tool>web_search:NN#M`
and are unresolvable as delivered. `CD_009` records that; no claim in this
folder rests on one.

---

```
notes ftom kimi: Yes. Cross-domain pattern matching is where the interesting fractures show up — where a field has solved a problem your framework is still naming. Let me search several domains that map directly onto your concepts.
Yes. Several fields have been working on pieces of your puzzle for decades, often with formalisms you can borrow directly. Here's a cross-domain map.
1.  Metrology — The Science of Baseline Freshness
The field: National standards bodies (NIST, ILAC, EURAMET) have formalized exactly your K14 → K15 → K16 chain under the name calibration interval determination.
What they know:
•  "Instrument drift" is defined as continuous or incremental variation of an indication over time, due to changes in the metrological characteristics of a measuring instrument cite🛠web_search:20#2:~:text=Instrument drift...continuous or incremental variation
•  Calibration intervals must not be arbitrary. ISO/IEC 17025 requires intervals be technically justified based on historical drift data, not calendar schedules cite🛠web_search:20#2:~:text=No standard imposes a specific interval...technically justified
•  NIST GMP 11 mandates that intervals be adjusted based on measurement assurance data, control charts, and surveillance testing — your "deliberate discipline of openness" operationalized as a federal requirement cite🛠web_search:20#5:~:text=Intervals may be adjusted...measurement assurance data
The 2026 advance: A risk-based Monte Carlo framework now models measurement error as a time-dependent stochastic process, propagating uncertainty through drift to determine when the probability of nonconformance exceeds an acceptable threshold cite🛠web_search:20#6:~:text=measurement error as a time-dependent stochastic process
What you can borrow:
•  Control charts for criteria drift. Metrologists use Shewhart/CUSUM charts on calibration history to detect when an instrument's error trend approaches limits. You could apply this to benchmark scores: plot a frozen model's scores over time; the control limits are your detection_threshold.
•  "As-found" vs. "As-left" data. Metrology distinguishes the reading before adjustment (as-found) from after (as-left). This maps directly to your anchor-version decomposition: as-found = score on old criteria, as-left = score on new criteria. The delta is criteria drift.
The gap they haven't closed: Metrology assumes the measurement standard is stable and the instrument drifts. Your framework inverts this: in AI evaluation, the "instrument" (the model) may be stable while the "standard" (the benchmark) drifts. Metrology has no formalism for standard drift.
----
2.  Adaptive Kalman Filtering — Explore-Exploit as Process Noise Estimation
The field: Control theory. The Kalman filter estimates a system's state from noisy measurements. In nonstationary environments, the process noise covariance Q must be adapted online.
What they know:
•  When the environment is nonstationary, adaptive Kalman filtering techniques dynamically adjust filter parameters based on real-time measurement characteristics... automatically tune the process and measurement noise covariances to match changing conditions cite🛠web_search:20#1:~:text=Adaptive Kalman filtering techniques dynamically adjust...changing conditions
•  If Q is too low (assuming stationarity), the filter stops tracking the true state and lags behind changes. If Q is too high, the filter overreacts to noise.
•  Covariance matching and maximum-likelihood estimation of Q from the innovation sequence are standard techniques.
What you can borrow:
•  Your "optimal exploration rate is a function of the environment's change rate" is exactly the adaptive Q estimation problem. In bandit terms, the innovation sequence is the sequence of reward prediction errors. The variance of innovations estimates the environment's change rate.
•  Dual control (Feldbaum, 1960s): A controller must simultaneously regulate the system and learn about it. The control input has two purposes — maintaining performance (exploit) and generating informative data (explore). This is the formal control-theoretic ancestor of your explore-exploit framing.
The gap they haven't closed: Kalman filters assume Gaussian noise and linear(ized) dynamics. Benchmark criteria drift is discrete, structured, and often directional (harder/easier). The innovation sequence is not Gaussian — it's a mixture of capability gain and criteria jumps.
----
3.  Kuhnian Philosophy of Science — Criteria Drift as Paradigm Change
The field: Thomas Kuhn's Structure of Scientific Revolutions. Normal science → crisis → revolution → new normal science.
What they know:
•  "Normal science" is your stable period. The paradigm sets the problems, methods, and standards of solution. During normal science, the baseline is knowable because the frame is fixed.
•  Paradigm shifts are your regime changes. Debates about legitimate methods, problems, and standards of solution... recur regularly just before and during scientific revolutions cite🛠web_search:21#3:~:text=debates like these do not vanish...scientific revolutions
•  Incommensurability: The standards of assessment are not permanent, theory-independent rules. They are not theory-independent, since they involve comparison to a (paradigm) theory. They are not permanent, since the paradigm may change in a scientific revolution. cite🛠web_search:21#13:~:text=The standards of assessment therefore are not permanent
What you can borrow:
•  Kuhn's five criteria for theory choice (accuracy, consistency, scope, simplicity, fruitfulness) are a declared frame for scientific evaluation. Kuhn's crucial insight was that these criteria function as values that guide theory choice, not as fixed rules that determine it. Different scientists may legitimately weigh these values differently. cite🛠web_search:21#0:~:text=these criteria function as values...weigh these values differently
•  Your Declared Frame block is a formalization of Kuhn's insight — but with a mechanism for comparability that Kuhn denied was possible. Where Kuhn saw incommensurability, your frame block makes differences mechanical.
•  The "crisis" phase in Kuhn maps to your detection latency window — the period between when the paradigm first shows strain and when the outcome column (experimental anomalies) forces a shift.
The gap they haven't closed: Kuhn described the phenomenology but offered no quantitative model. Your drift engine + regression is exactly the quantitative apparatus Kuhn lacked.
----
4.  Computational Semantic Drift — Rubric Drift as Linguistic Change
The field: Diachronic linguistics + NLP. Tracking how word meanings change over time using distributional semantics.
What they know:
•  Words are malleable and their meaning(s) continuously evolve, influenced by social practices, events, and political circumstances. Methods like WiDiD track this via evolutionary clustering of contextualized embeddings cite🛠web_search:21#1:~:text=Words are malleable...continuously evolve
•  Two distinct metrics:
•  Semantic shift = Jensen-Shannon divergence over sense prominence distributions (did the word acquire or lose senses?)
•  Sense shift = cosine distance between sense prototypes (did existing senses change their core meaning?) cite🛠web_search:21#1:~:text=Semantic shift...describes the degree of lexical semantic change
•  Alignment is the hard problem. Diachronic embeddings must be aligned across time periods, but local alignment around a small set of stable words was insufficient cite🛠web_search:21#7:~:text=local alignment around a small set...was insufficient
What you can borrow:
•  Your rubric_dimensions and rubric_weights are sense prominence distributions. A benchmark version is a "word" at a "time period." Semantic shift = did the benchmark gain/lose dimensions? Sense shift = did the weights on existing dimensions change?
•  The alignment problem is your anchor-version problem. To compare scores across criteria versions, you need a "stable semantic anchor" — a subset of the benchmark that did not change, or a frozen model scored on all versions.
•  The law of conformity (frequent words change more slowly) and law of innovation (polysemous words change more rapidly) from Hamilton et al. map to benchmark properties: widely-used benchmarks drift more slowly; multi-dimensional benchmarks drift faster because more components can shift.
The gap they haven't closed: Semantic drift research treats change as descriptive — "the word 'cloud' shifted from meteorology to computing." Your framework treats criteria drift as normative — "the benchmark shifted, and that shift may have inflated reported progress." The linguistic field has no concept of Goodhart corruption or ruler inflation.
----
5.  High Reliability Organizations — Deliberate Discipline of Openness
The field: Weick & Sutcliffe's research on organizations that operate in high-risk environments (aircraft carriers, nuclear power, air traffic control) with very low failure rates.
What they know:
•  Five mindfulness principles:
6.  Preoccupation with failure — actively looking out for weak signals. Reporting weak signals is encouraged and rewarded. cite🛠web_search:21#2:~:text=Pre-occupation with failure...weak signals) that must be investigated
7.  Reluctance to simplify — simple explanations are not accepted. HROs take deliberate steps to create a more complete and nuanced picture. cite🛠web_search:21#8:~:text=Reluctance to Simplify...deliberate steps to create a more complete
8.  Sensitivity to operations — the focus is more on the actual work as it is being done, not plans. Beware the mindless routine. Beware the complacency of all is okay. cite🛠web_search:21#8:~:text=Sensitivity to Operations...Beware the complacency of all is okay
9.  Commitment to resilience — errors don't disable. Fast learning from errors. cite🛠web_search:21#5:~:text=Commitment to Resilience...Fast learning from errors
10.  Deference to expertise — authority migrates to the people with the most expertise, regardless of rank. cite🛠web_search:21#8:~:text=Deference to expertise...regardless of their rank
What you can borrow:
•  Your "subtle test" is HRO "weak signal detection." Your "deliberate discipline of openness" is HRO "preoccupation with failure" during stable periods.
•  The HRO literature formalizes why this discipline is maintained when nothing is wrong: because the world they face is complex, unstable, unknowable, and unpredictable, HROs position themselves to see as much as possible. cite🛠web_search:21#8:~:text=the world they face is complex...see as much as possible
•  "Practical drift" (Snook, 2000) is your baseline_freshness degradation. Work-as-designed slowly diverges from work-as-performed during long stable periods. The divergence is not detected until a failure occurs.
The gap they haven't closed: HROs focus on operational drift (procedures diverging from practice). Your framework focuses on evaluative drift (the ruler moving). An HRO would say "follow the checklist"; your framework asks "has the checklist itself changed, and did anyone notice?"
----
6.  Ecological Resilience / Panarchy — Stability as Substrate
The field: C.S. Holling's adaptive cycle and the panarchy framework. Ecosystems move through exploitation → conservation → release → reorganization.
What they know (from base, not search):
•  The conservation phase is your stable period. Biomass is accumulated, connections are rigidified, and the system appears stable. This is when baselines are most knowable.
•  The release phase (Ω) is your regime change. Rigid structures collapse. The baseline is lost.
•  The reorganization phase (α) is your post-change stable period. New baselines must be established before learning can resume.
•  Revolt and remember: Smaller, faster adaptive cycles can trigger larger, slower ones (revolt). Larger cycles constrain smaller ones (remember). This maps to benchmark versions: a small criteria drift (minor version bump) can cascade into a major paradigm shift.
What you can borrow:
•  The adaptive cycle gives you a temporal topology for your framework. Stable periods are not arbitrary gaps between changes; they are necessary phases where baselines are established. You cannot skip conservation and go straight to exploitation after a release.
•  Resilience is not the ability to resist change; it is the ability to maintain function across change. Your "relational" model (learns the relation, not the surface) is resilient in Holling's sense.
----
7.  Predictive Processing / Cognitive Science — Proprioception as Calibration
The field: The brain as a predictive machine. Friston's free energy principle, Clark's predictive processing.
What they know (from base):
•  The brain maintains a generative model of the world. Prediction errors drive learning.
•  Precision weighting: The brain adjusts the precision (inverse variance) of sensory channels based on expected reliability. Unreliable channels are downweighted.
•  Hyperpriors: Deeply held expectations about the structure of the world (e.g., gravity is constant, ground is firm) that are rarely updated because they are rarely violated.
What you can borrow:
•  Your "stability as substrate" is a hyperprior. Gravity-constancy is a precision-weighted prior with extremely high precision. It is what makes walking learnable.
•  Your "stability as assumption" is an empirical hypothesis with lower precision. "The next surface will behave like this one" is a prediction that can be updated.
•  Precision weighting explains why detection latency rises silently. When a channel (e.g., a peripheral indicator) has not been exercised during stable periods, its precision weight decays. The prediction error from that channel is downweighted, so the signal is not propagated to higher levels until it becomes large enough to overcome the threshold.
----
Synthesis: The Borrowable Toolkit
Your Concept	Domain	Borrowable Tool
K14 practice_rate	Metrology	Control charts, calibration interval algorithms (ILAC-G24)
K15 baseline_freshness	Metrology	As-found / As-left data, drift trend analysis
K16 detection_latency	HROs	Weak signal reporting protocols, near-miss databases
Explore-exploit under nonstationarity	Adaptive Kalman	Innovation-based Q estimation, covariance matching
Criteria drift	Semantic drift	JSD over sense distributions, alignment via stable anchors
Regime change	Kuhn / Panarchy	Paradigm shift detection, adaptive cycle phase identification
Stable period as calibration window	Predictive processing	Precision weighting, hyperprior maintenance
Relational vs. narrow model	Resilience theory	Generalized vs. specified resilience
One Cross-Domain Pattern You May Not Have Named
The "Alignment Problem" appears in every field:
•  Semantic drift: Aligning embedding spaces across time periods. Local alignment around a small set of stable words was insufficient.
•  Metrology: Traceability chains linking shop-floor sensors to NIST standards.
•  Kalman filtering: Coordinate transformations between sensor frames.
•  Your framework: Anchor-version scoring to align model scores across criteria versions.
In every case, the solution is the same: identify an invariant subset that does not change, and use it as the bridge. In semantic drift, it's "stable words." In metrology, it's the primary standard. In your framework, it's a frozen model scored on all versions, or a subset of the benchmark that never changed.
The fields that have solved this best (metrology, geodesy) treat alignment as a first-class problem with its own error budget. Your framework currently treats anchor-version scoring as optional. The cross-domain pattern suggests it should be mandatory — without it, drift is unmeasurable.
```
