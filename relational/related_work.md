# Related Work — Positioning the Council of Protectors in the Literature

**Date:** 2026-08-06
**Purpose:** Anchor each framework construct in the existing research record.
This document converts "reinvention" into "synthesis": the framework's value
is the integration, and it must stand on the lineages below.

---

## 1. Confusion-as-drive ↔ intrinsic motivation & learning progress

The confusion spectrum's homeostatic zone (CONFUSION_SPECTRUM.md) is a
parametric restatement of the **learning-progress hypothesis**:

- Oudeyer, Kaplan & Hafner, "Intrinsic Motivation Systems for Autonomous
  Mental Development," *IEEE Trans. Evolutionary Computation* (2007).
  Agents explore activities where the *derivative* of prediction error
  (improvement rate) is maximal, avoiding both trivial and unlearnable
  regions — including "noisy TV" distractors that trap raw
  prediction-error-seeking (Burda et al., RND analysis, 2019).
- Schmidhuber, "Formal Theory of Creativity, Fun, and Intrinsic
  Motivation" (2010): reward = compression progress.
- Portelas et al., "Teacher algorithms for curriculum learning of Deep RL"
  (CoRL 2019/2020) — **ALP-GMM**: a teacher samples tasks in the learner's
  absolute-learning-progress region. A computed ZPD, and the most directly
  reusable tool for operationalizing protector "readiness."
- In active inference, the same idea is the **epistemic term of expected
  free energy** (Parr, Pezzulo & Friston, *Active Inference*, MIT Press 2022).

**Standing implication for this repo:** the 0.2–0.5 band is a *prior*, not
a measured constant. The defensible formulation is: the band is the
empirical learning-progress region, estimated online (ALP-style sliding
window), and 0.2–0.5 is its documented heuristic initialization. See
`experiments/RESULTS.md` for the first empirical test of whether such a
band emerges from LP-maximizing task selection.

## 2. Pain-as-sensor ↔ homeostatic RL, preferred priors, robot nociception

"Pain signals instead of reward shaping" is the mainstream position of
homeostatic reinforcement learning and active inference, not a contrarian one:

- Keramati & Gutkin, homeostatic RL (2011/2014): reward = drive reduction
  toward setpoints; deviation-from-homeostasis *is* the pain signal.
- Yoshida et al., *Neural Networks* (2024) and review (2025): deep HRRL,
  interoception-dependent behavior; HRRL formalized as augmented
  exteroceptive + interoceptive state.
- Laurençon et al., CTCS-HRRL (arXiv:2401.08999, 2024): continuous
  self-regulated agents with fatigue.
- Active inference preferred priors; "The Missing Reward: Active Inference
  in the Era of Experience" (arXiv:2508.05619, 2025) argues one universal
  objective replaces engineered rewards.
- Robot nociception: Kuehn & Haddadin (IEEE RA-L 2017); Feng & Zeng
  BRP-SNN (2022); Vorndamme et al. (T-RO 2025); AIRSKIN tactile withdrawal
  on UR10e (2025–26). Lharidon (PhD thesis ~2024): artificial cortisol
  modulates pain sensitivity adaptively — hyperalgesia in dangerous
  environments, hypoalgesia in safe ones — computational support for the
  framework's "pain sensitivity tracks the environment" stance.

**What the framework adds here:** hardware resource limits as the
*exclusive* interoceptive drive set, and the refusal of any task reward.

## 3. Triadic observation & pain-as-alarm ↔ predictive processing / allostasis

The triad (internal model / body / external evidence, mismatch = alarm)
tracks the dominant framework in affective neuroscience:

- Barrett & Simmons, interoceptive inference (*Nat Rev Neurosci* 2015);
  Seth (2013); Friston (2010).
- Sennesh et al., "Interoception as modeling, allostasis as control"
  (*Biological Psychology* 2022) — the triad as a formal control problem.
- Smith et al. (*PLoS Comp Bio* 2020, Tulsa 1000): transdiagnostic
  distress = failure to update precision on interoceptive prediction errors.
- Shaffer et al. (*Annu Rev Clin Psychol* 2022): depression as disorder
  of allostatic prediction.
- Caveat: behavioral interoception measures are psychometrically contested
  (heartbeat-counting-task controversy). Build on computational markers.

## 4. Social pain — use the revised formulation

Do **not** lean on the 2003 dACC neural-overlap claim:

- Woo et al. (*Nature Communications* 2014): multivariate analysis shows
  physical pain and social rejection produce *separable* patterns within
  shared regions. Cyberball meta-analyses are fragile (Cacioppo 2013);
  default-mode-network accounts compete (Mwilambwe-Tshilobo & Spreng 2021).
- **Eisenberger (2015, *Annu Rev Psychol*) revised position**: social pain
  recruits a domain-general **discrepancy/alarm system** also used for
  physical pain. This is the formulation this framework should cite — it is
  *more* congenial to the triadic model: one alarm system, multiple
  correlation channels.
- The functional claims are uncontested: rejection is aversive and
  loneliness is a mortality risk factor (Holt-Lunstad meta-analyses).

## 5. External protector before internalization ↔ AI control & shallow alignment

The engineering pattern (external oversight) is established; the
*developmental infancy argument* is this framework's distinctive, unproven
contribution:

- Greenblatt, Shlegeris et al., "AI Control" (Redwood Research, ICML 2024);
  productized as Google DeepMind's AI Control Roadmap (2026).
- Anthropic Constitutional Classifiers (2025): external input/output filters.
- Shallow-alignment evidence supporting the critique of early-internalized
  protectors: Arditi et al. (2024) — refusal is one linear direction;
  Qi et al. (2024) — handfuls of harmful examples erode fine-tuned alignment.
- Orseau & Armstrong, corrigibility/interruptibility (2016–): single-operator
  shutdown, not plural governance.
- Capability-gated deployment: Anthropic RSP/ASL; OpenAI Preparedness
  Framework; DeepMind Frontier Safety Framework (early-warning evals run
  *during* training); METR's evaluation-over-development ambition.

## 6. The council ↔ commons governance & multi-agent veto

- Ostrom design principles: empirically robust (Cox, Arnold &
  Villamayor-Tomás 2010; Baggio et al., *PNAS* 2016). Collective-choice
  arrangements and nested enterprises already distribute consent/veto.
- Indigenous co-management with quantified outcomes: Australian savanna
  burning (wildfire frequency halved, fire GHG −40% over 17.9M ha);
  governance is elder-council, consensus-based, FPIC/UNDRIP. This domain
  already *is* the framework; contribute translation, not structure.
- SRE: OPA/Gatekeeper policy-as-code and Argo/Flagger canary analysis
  implement any-gate-blocks (logically = unanimity required).
- Multi-agent LLM debate/consensus is fragile exactly where the framework
  is distinctive: one persuasive adversarial agent degrades group accuracy
  10–40% (Nat. Sci. Rep. 2026); correlated models echo-chamber. The
  framework's design principle — **orthogonal, non-deliberative,
  independently-grounded veto channels** — is the evidence-backed answer.

## 7. Application-domain anchors

- Education: MATHia (RAND effect sizes 0.19–0.36 SD); Affective AutoTutor
  (D'Mello & Graesser) — confusion detection solved, real-time adaptive
  response open; desirable difficulties / productive failure (Bjork; Kapur).
- Dementia: Cohen-Mansfield Unmet-Needs Model (2015) — agitation as signal
  of unmet need, pain systematically under-detected; mechanistically aligned
  with pain-as-sensor. Validation therapy evidence is weak (Cochrane) —
  cite person-centered care (Kitwood; Kim & Park 2017) instead.
- Clinical: biopsychosocial model (Engel 1977); CBT five-areas formulation;
  measurement-based care is APA policy (2025).
- Digital phenotyping: mindLAMP, Beiwe, AWARE collect signals without a
  generative model of the person; commercial readiness scores (Garmin Body
  Battery, WHOOP, Oura) are unvalidated composites (Doherty et al. 2025).
  The phone-as-altricial-system daemon sits in a real gap as of 2026.

---

*Full survey with complete citations: see the research landscape report
produced alongside this document (relational_research_report.md).*
