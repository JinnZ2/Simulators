# Literature Review — Scientific Grounding for GDPRF

Sources were retrieved via academic search (CSV data in this folder). Fields map
to GDPRF's five pillars; each pillar lists what the literature *supports* and what
it *complicates*.

## Pillar 1 — Proxies as Windows on Unobservables (Proxy Discovery Engine)

**Support:**
- Kolenikov & Angeles (2009, 1,089 citations) — rigorous methods exist for
  building proxy-based measures of unobservable constructs (socioeconomic status),
  with quantified error properties. `proxy-latent-measurement.csv`
- Bollen & Bauldry (2011, 810 citations) — the causal/composite/formative
  indicator typology gives GDPRF's `proxy_of` edge type a formal measurement-model
  foundation. `proxy-latent-measurement.csv`
- Houston (2004, 167 citations) — systematic validity assessment of secondary-data
  proxies shows the practice is established and testable. `proxy-construct-validity.csv`

**Complications:**
- Seltzer (2021), "The perilous use of proxy variables" — proxies silently
  redefine the construct being measured; a `proxy_of` edge is a *claim*, not a fact.
- Knox, Lucas & Cho (2022, 81 citations) — learned proxies can validate or
  invalidate causal theories; proxy quality is empirically testable but often not
  tested. `proxy-causal-inference.csv`

## Pillar 2 — Gradient / Bayesian Belief Updating

**Support:**
- Pearl, *Probabilistic Reasoning in Intelligent Systems* (35,901 citations) —
  the canonical foundation for propagating probabilistic belief through networks
  of evidence. `bayesian-updating.csv`
- Peng, Zhang & Pan (2010) — Bayesian network reasoning with *uncertain evidence*
  is exactly GDPRF's step-4 situation: proxy readings are never certain inputs.
- McCann (2020, *California Management Review*) — Bayesian updating improves
  decisions under uncertainty in applied/managerial settings.

**Complications:**
- Benjamin (2018, 692 citations) — humans systematically err in probabilistic
  reasoning (base-rate neglect, over- and under-reaction); an automated gradient
  updater is justified but must guard against encoding the same biases in its
  priors and update function.
- Zhu & Griffiths (2026) — computation-limited Bayesian updating: exact gradient
  updating is expensive; resource-rational approximations are an open design space.

## Pillar 3 — Metrology & Instrumentation (SNR, Bias Calibration)

**Support:**
- Magnusson & Ellison (2008, 115 citations) — formal treatment of uncorrected
  measurement bias in uncertainty estimation; GDPRF's `systematic_bias` field has
  direct metrological precedent. `metrology-uncertainty.csv`
- Hibbert (2007, 69 citations) — systematic errors in analytical results; bias is
  not optional metadata but a core component of uncertainty.
- Blackwell, Honaker & King (2017, 269 citations) — unified treatment of
  measurement error and missing data in social-science pipelines.
  `proxy-latent-measurement.csv`

**Complications:**
- Kane (1997) — bias is "the neglected component of measurement uncertainty";
  real instruments rarely come with known bias values, so GDPRF's per-proxy bias
  fields will often themselves be estimates requiring their own gradients.

## Pillar 4 — Vector Knowledge Graph with Confidence

**Support:**
- Chen et al. (2019, 215 citations), "Embedding uncertain knowledge graphs" —
  uncertainty-aware KG embeddings are an established research line; GDPRF's
  per-edge `evidence_weight` and proxy `vector_embedding` fit this paradigm.
  `kg-embedding-calibration.csv`
- Chen et al. (2021, 92 citations) — probabilistic box embeddings for uncertain
  KG reasoning; confidence can be geometric, not just scalar.
- Tabacof & Costabello (2019, 68 citations) — probability calibration for KG
  embedding models; raw embedding confidences are miscalibrated and must be
  calibrated before use — directly relevant to GDPRF's fidelity gradients.

**Complications:**
- Safavi, Koutra & Meij (2020, 46 citations) — calibration evaluation of KG
  embeddings for trustworthy predictions; uncalibrated confidence scores can be
  badly overconfident. GDPRF inherits this risk wholesale.

## Pillar 5 — Domain Application: Telemetry Proxies for Human States

**Support:**
- Nepal et al. (2025) — survey of passive sensing for workplace wellbeing;
  GDPRF's burnout → response-latency → server-log cascade is a live research area.
  `digital-phenotyping-burnout.csv`
- Adler et al. (2022, 96 citations), "Burnout and the quantified workplace" —
  empirical grounding plus documented tensions of personal sensing at work.
- Barac et al. (2024, 51 citations) — wearables for detecting burnout in health
  care; physiological proxies for burnout show measurable signal.

**Complications:**
- Chowdhary et al. (2023, 81 citations) — meaningful consent for workplace
  wellbeing technologies is contested; GDPRF's telemetry proxies carry an
  ethics/governance dimension the framework does not currently model.
- Proxy fidelity for psychological states is lower than for physical metrology;
  cascade depth (burnout → latency → logs) compounds fidelity decay multiplicatively.

## Pillar 6 — Hidden Variables & Confounding (Step 5)

**Support:**
- Miao, Geng & Tchetgen Tchetgen (2018, 529 citations) — identifying causal
  effects with proxy variables of unmeasured confounders; formal conditions under
  which proxy-based adjustment works. `proxy-causal-inference.csv`
- Louizos et al. (2017, 1,278 citations) — causal effect inference with deep
  latent-variable models; learned representations of hidden confounders.
- Xie et al. (2024) — automating the *selection* of proxy variables of unmeasured
  confounders; GDPRF's hidden-proxy search has an algorithmic literature to draw on.
- Wang & Blei (2021) — "a proxy variable view of shared confounding"; Veitch,
  Wang & Blei (2019) — embeddings to correct for unobserved confounding.

**Complications:**
- D'Amour (2019) — multi-cause/proxy approaches have fragility properties;
  residual-variance triggers (GDPRF step 5) need formal identification checks,
  not just threshold heuristics.
