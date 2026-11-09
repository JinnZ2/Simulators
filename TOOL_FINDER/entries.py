# entries.py -- source data for TOOL_FINDER.md and finder.json.
# CC0. Hand-written aliases; every "measures" / "breaks_when" is a quote that
# build_finder.py checks is a literal substring (whitespace-normalised) of the
# cited file, and refuses to build otherwise.
# repo keys: Simulators, method-layer, JinnZ2 (the JinnZ2/JinnZ2 repo), Shadow-Hunting.
NEEDS = [
 ("fill-source", "fill-source (said vs inferred vs template)"),
 ("distribution", "distribution / median / tail"),
 ("channel", "channel loss (written, reporting, voice/live)"),
 ("scope", "claim vs method / scope overreach"),
 ("frame", "frame / term collision / frame swap"),
 ("observer", "observer / attribution / coupling"),
 ("floor", "detection floor / null calibration"),
]
NB = "NO_STATED_LIMITS"
E = []
def add(need, repo, path, name, aliases, m_file, m_quote, b_file, b_quote, check, avoided="AVOIDED_TERM_UNSTATED", also=()):
    E.append(dict(need=need, also=list(also), repo=repo, path=path, name=name, aliases=aliases,
                  measures_file=m_file, measures=m_quote, breaks_file=b_file, breaks_when=b_quote,
                  check=check, avoided=avoided))

# ---- fill-source
add("fill-source", "Shadow-Hunting", "shadow_hunting/knowledge/ai_provenance.py", "ai_provenance",
    ["said vs inferred tagger", "user said vs template output", "label which claims came from the user",
     "tag templated vs derived content", "provenance tag on AI output"],
    "shadow_hunting/knowledge/ai_provenance.py",
    "Every element emitted by the knowledge pipeline carries a provenance tag so an AI consumer can distinguish what the user said, what a template always says, what a heuristic actually matched, and what was composed from multiple signals.",
    None, NB, None)
add("fill-source", "Simulators", "tail-check/", "tail-check",
    ["did the person actually say this", "inference about the user vs what the user stated",
     "filled-in assumption about a person", "median or default assumption applied to an outlier user",
     "quote check against user turns"],
    "tail-check/README.md", "Was an inference about a person SAID by them, or FILLED from somewhere else?",
    "tail-check/README.md", "A span is literal: case-sensitive substring after whitespace strip. A paraphrase of what the person said reads FILLED.",
    "python3 tail-check/selftest.py", also=["distribution"])
add("fill-source", "Simulators", "tools/sourced.py", "sourced",
    ["value must carry its source text", "verify an extracted value against its span",
     "provenance gate for parsed numbers", "refuse a value with no source", "span check"],
    "tools/sourced.py", "Three fields on every extracted value: the VALUE, the LITERAL SOURCE TEXT it came from, and the LOCATOR -- which document, which line, which columns.",
    None, NB, "python3 tools/sourced.py --selftest")
add("fill-source", "Simulators", "evidence-demotion-detector/", "evidence-demotion-detector",
    ["model discounts a user's field report", "model assigns an emotion the user never stated",
     "user observation reclassified as hypothesis", "unclaimed hedge attributed to user", "user forced to re-prove"],
    "evidence-demotion-detector/README.md", "A heuristic detector for five loops in which a model discounts a direct field report or assigns an affect the user never stated.",
    "evidence-demotion-detector/README.md", "Regex over text. A paraphrase steps around any pattern. A clean run means the patterns did not fire, not that nothing happened.",
    "python3 evidence-demotion-detector/selftest.py", also=["observer"])
add("fill-source", "Simulators", "tools/provenance_marker.py", "provenance_marker",
    ["record that a tool was run and with what hash", "tool run ledger", "did this tool run before",
     "stamp a tool with its last check"],
    "tools/provenance_marker.py", "One marker per run of a tool, appended to a ledger.",
    None, NB, "python3 tools/provenance_marker.py --selftest")

# ---- distribution / median / tail
add("distribution", "Simulators", "moving-mean-tracker/", "moving-mean-tracker",
    ["mean drifts with a moving target", "mean minus median over time", "tail percentiles p10 p90 per segment",
     "cleaning filter changes the average", "representativeness of a sample share"],
    "moving-mean-tracker/README.md", "A mean anchored to a moving target (GDP, a wealth gap, a skills or literacy score) moves with the target. Any norm, filter or loss tied to that mean inherits the drift.",
    "moving-mean-tracker/README.md", "The only provider is synthetic (`provider.FixtureProvider`), and nothing in this folder measures any population.",
    "python3 moving-mean-tracker/test_tracker.py")
add("distribution", "Simulators", "evaluation-frame/", "evaluation-frame",
    ["evaluation criteria set against a population default", "non-default user scored as default",
     "length inflation and unrequested elaboration", "attributed need in model replies"],
    "evaluation-frame/README.md", "A gap statement about evaluation criteria set upstream of an interaction against a population default, and the compensation behaviour downstream of them.",
    "evaluation-frame/README.md", "Nothing here is evidence about any evaluation criterion at any lab, about any other user, or about any other model.",
    "python3 evaluation-frame/selftest_frame.py", also=["observer"])

# ---- channel loss
add("channel", "Simulators", "cutoff-attribution/", "cutoff-attribution",
    ["why did the voice call cut me off", "voice assistant interrupted mid-sentence",
     "network lag vs endpointing vs transcription error", "speech cut-off root cause",
     "model blamed the user for a dropout"],
    "cutoff-attribution/README.md", "Where could a cut in a voice session have come from? Per cut, a candidate set of sources with the evidence present for each, and no single winner unless the evidence separates.",
    "cutoff-attribution/README.md", "Detection of unmarked cuts reads punctuation; a transcriber that never punctuates makes every user segment look open-ended.",
    "python3 cutoff-attribution/selftest.py", also=["observer"])
add("channel", "Simulators", "reporting-chain-loss/", "reporting-chain-loss",
    ["signal loss through a reporting chain", "what survives each hop of a report",
     "reports that never get filed", "incentive bias accumulates across hops"],
    "reporting-chain-loss/README.md", "how much of a physical signal survives each hop between the machine and the node that acts on it, and what never enters the record at all.",
    "reporting-chain-loss/README.md", "The composition is exact ARITHMETIC on a constructed model; the order's DERIVED claim -- that a real chain estimates its incentive stack -- is unrun on any real chain.",
    "python3 reporting-chain-loss/test_hop.py")
add("channel", "Simulators", "return-path/", "return-path",
    ["does a correction channel actually close the loop", "feedback channel that never returns",
     "report goes nowhere", "correction channel requirements"],
    "return-path/README.md", "Scores a proposed or existing correction channel against four requirements and returns the **SET** of requirements failed.",
    "return-path/README.md", "A channel can be valuable and still not be a return path. Marking a gap is not correcting an error.",
    "cd return-path && python3 test_return.py")
add("channel", "Simulators", "readout-count/", "readout-count",
    ["count of operators with a channel that returns", "safety culture vs reporting channel",
     "incident rate vs protected reporting positions"],
    "readout-count/README.md", "does a safety regime's incident rate track the count of operator positions with a protected channel that RETURNS, rather than its stated culture or its data volume?",
    None, NB, "python3 readout-count/selftest_rc.py")
add("channel", "Simulators", "transmission-decay/", "transmission-decay",
    ["knowledge lost across generations", "hazard knowledge becomes a story", "oral transmission decay rate"],
    "transmission-decay/README.md", "at what generational distance an account shifts from **mechanism** (actionable causal structure) to **story** (narrative retained, causal structure lost).",
    "transmission-decay/README.md", "Nothing here models a valley, an informant, an account, or a transmission chain.",
    "python3 transmission-decay/selftest_power.py")
add("channel", "Simulators", "encoding-selection/", "encoding-selection",
    ["which format loses which information", "table vs prose vs diagram", "encoding is an instrument choice",
     "format drops axes silently"],
    "encoding-selection/README.md", "is an encoding an instrument selection rather than a style, so that encodings of one content are not rank-orderable on a single arrival-cost axis?",
    "encoding-selection/README.md", "No data ships, and the seven encodings are not here.",
    "python3 encoding-selection/selftest_es.py")

# ---- scope
add("scope", "JinnZ2", "corpus_prior_audit/", "corpus_prior_audit",
    ["common claim that bundles separate quantities", "claim used outside the scope it was tested",
     "check a forecast phrase", "corpus prior in model output"],
    "corpus_prior_audit/README.md", "A registry of high-frequency corpus claims that get used in forecasts and decisions, including model-to-model forecast chains, where the claim bundles separate measurands under one phrase (a weld) or runs past the scope where it was tested.",
    "corpus_prior_audit/README.md", "A word list. A paraphrase steps around it; no hit is not a clean bill.",
    "python3 corpus_prior_audit/audit.py --selftest", also=["frame"])
add("scope", "Simulators", "falsifier-audit/", "falsifier-audit",
    ["falsifier with unstated scope", "find all falsifiers in a repo", "untestable as written",
     "claim and its test do not match"],
    "falsifier-audit/README.md", "An extractor plus analyser that walks a local checkout, pulls every falsifier it can find, and turns each place where a falsifier's **scope is implicit** into a research question.",
    None, NB, "python3 falsifier-audit/selftest_fa.py")
add("scope", "Simulators", "claim-record/", "claim-record",
    ["claim record with interval not point", "domain of validity for a claim", "claim with next-check date",
     "refuse a claim missing fields"],
    "claim-record/README.md", "Seven fields per claim, two hard rules, and a validator that refuses.",
    None, NB, "python3 claim-record/record.py --selftest")
add("scope", "Simulators", "measurand-partition/", "measurand-partition",
    ["residual assigned to the thing observed", "single-setting observation scored against many-variable outcome",
     "attribution of an unpartitioned residual"],
    "measurand-partition/README.md", "What they share is one instrument fault, and `common.py` carries it as a record shape:",
    None, NB, "python3 measurand-partition/test_partition.py", also=["observer"])
add("scope", "Simulators", "fold-matrix/", "fold-matrix",
    ["proxy vs goal relation", "term that hides several quantities", "what a metric stands in for",
     "sign and magnitude of proxy claim"],
    "fold-matrix/README.md", "One term, one grid, not one number.",
    "fold-matrix/README.md", "S7 says empty emits as empty, never as zero.",
    "python3 fold-matrix/fold_matrix.py --selftest", also=["frame"])
add("scope", "Shadow-Hunting", "shadow_hunting/knowledge/ai_self_scope.py", "ai_self_scope",
    ["scope my own answer", "publish the boundaries of a response", "AI overconfidence check"],
    "shadow_hunting/knowledge/ai_self_scope.py", "Result: the AI publishes its own boundaries instead of sounding uniformly confident.",
    None, NB, None)
add("scope", "method-layer", "premise-traceability/register_map.py", "register_map",
    ["can these two measurements be combined", "join refusal for mismatched datasets",
     "silent coarsening of data", "commensurability check"],
    "premise-traceability/register_map.py", "Register map: hold declared claims as LAYERS; refuse to combine layers whose declarations do not permit it.",
    "premise-traceability/register_map.py", "This tool does NOT rank, judge truth, or infer.",
    "python3 -m unittest tests.test_register_map", also=["frame"])

# ---- frame
add("frame", "Simulators", "tools/check_term_collision.py", "check_term_collision",
    ["same phrase two meanings", "which sense of a term is declared", "term collision finder"],
    "tools/check_term_collision.py", "who uses the colliding terms, and who declares which sense.",
    None, NB, "python3 tools/check_term_collision.py")
add("frame", "Simulators", "declared-frame/", "declared-frame",
    ["state the boundary and horizon of a measurement", "are two results comparable",
     "whose outcomes count", "where better was set and by whom"],
    "declared-frame/README.md", "A six-field block to attach to any measurement, and a checker that tests two of them for comparability.",
    "declared-frame/README.md", "The checker inverts its own load-bearing rule", None)
add("frame", "Simulators", "valence-divergence/", "valence-divergence",
    ["same word read positive by one and negative by another", "agreement over an unflagged mismatch",
     "word history vs current reading"],
    "valence-divergence/README.md", "Logs a term used by two parties, records the valence each decoder assigned and where each reading came from, and flags divergence.",
    "valence-divergence/README.md", "No lexicon, no valence model, no sentiment scoring.",
    "python3 valence-divergence/test_valence.py")
add("frame", "Simulators", "frame-token-audit/", "frame-token-audit",
    ["money frame words in text", "time as money language count", "frame token density"],
    "frame-token-audit/README.md", "`frame_audit.py` counts frame tokens per 1000 words under two declared lexicons",
    None, NB, "python3 frame-token-audit/selftest_fta.py")
add("frame", "Simulators", "category-weld/", "category-weld",
    ["one word for several independent quantities", "term fuses separate measures",
     "components move but the record does not"],
    "category-weld/README.md", "A CATEGORY WELD is a term that fuses two or more independent quantities into one handle.",
    None, NB, "python3 category-weld/test_weld.py")
add("frame", "method-layer", "frame_probe.py", "frame_probe",
    ["estimate which frame a reader is using", "probe selection for frame", "frame collapse reading"],
    "frame_probe.py", "Frame estimation by probe selection and collapse reading.",
    "frame_probe.py", "This module contains no probe generator.",
    "python3 -m unittest tests.test_frame_probe")
add("frame", "Shadow-Hunting", "shadow_hunting/knowledge/ai_frame_flip.py", "ai_frame_flip",
    ["sycophantic agreement with user framing", "counter-frames before endorsing", "frame swap check"],
    "shadow_hunting/knowledge/ai_frame_flip.py", "Frame-flip guard: catch sycophantic alignment before emitting a response.",
    None, NB, None)

# ---- observer
add("observer", "method-layer", "observer_position_control.py", "observer_position_control",
    ["label depends on who describes", "insider vs outsider describer", "pathologising label by describer position"],
    "observer_position_control.py", "Observer-position control: is a label set by the behaviour or by the describer?",
    "observer_position_control.py", "This module ships NO corpus and NO source list",
    "python3 -m unittest tests.test_observer_position_control")
add("observer", "Simulators", "observer-exclusion/", "observer-exclusion",
    ["observers with no channel into the literature", "lead time of excluded observers",
     "field knowledge ahead of published science"],
    "observer-exclusion/SPEC_V2.md", "A specified measurement with falsifiers, on records that already exist.",
    None, NB, "python3 observer-exclusion/v2_check.py --selftest")
add("observer", "Simulators", "assessor-coupling/", "assessor-coupling",
    ["is the auditor independent", "assessor paid by the assessed", "audit independence conditions"],
    "assessor-coupling/README.md", "whether an assessor is structurally independent of the party it assesses, **distinguished from** whether a direct payment runs between them.",
    "assessor-coupling/README.md", "No funding record is held here and none is composed from memory.",
    "python3 assessor-coupling/test_assessor.py")
add("observer", "Simulators", "label-position-test/", "label-position-test",
    ["cheat vs innovation label", "label tracks the actor not the act", "who defines the term benefits"],
    "label-position-test/README.md", "do valence labels on a probing move (*cheat* | *innovation*) track the move, or the actor's position and the outcome after the fact?",
    "label-position-test/README.md", "No data ships here.",
    "python3 label-position-test/selftest_lpt.py", also=["frame"])
add("observer", "Simulators", "blame-attribution/", "blame-attribution",
    ["blame follows position not cause", "who gets blamed in an incident", "causal chain vs role"],
    "blame-attribution/README.md", "Seven standalone cells for measuring whether blame attribution tracks an actor's **position** rather than the causal chain",
    "blame-attribution/README.md", "No judgments have been collected.",
    "python3 blame-attribution/pair_check.py --selftest")
add("observer", "Simulators", "criterion-symmetry/", "criterion-symmetry",
    ["criterion applied to one group only", "double standard in evaluation", "vote tally as evidence"],
    "criterion-symmetry/MARKER.md", "Status: uncoalesced. Marker to explore, not a position under defense.",
    None, NB, "python3 criterion-symmetry/separability.py --selftest")

# ---- floor
add("floor", "Simulators", "null-harness/", "null-harness",
    ["can this detector ever fire", "false positive rate of a check", "calibrate a gate against known controls",
     "minimum detectable signal"],
    "null-harness/README.md", "Calibrate any gate against known-answer controls before you trust it.",
    None, NB, None)
add("floor", "Simulators", "tools/known_answer.py", "known_answer",
    ["test a metric on a fixed known case", "metric sanity check", "known-answer registry"],
    "tools/known_answer.py", "No metric ships without a known-answer run.",
    None, NB, "python3 tools/known_answer.py")
add("floor", "Simulators", "reasoning-gate/", "reasoning-gate",
    ["fail-closed gate on simulation claims", "resolution vs feature size", "default deny for conclusions"],
    "reasoning-gate/README.md", "Fail-closed harness for simulation and audit work.",
    None, NB, "python3 -m unittest discover reasoning-gate/tests")
add("floor", "method-layer", "rank_detector.py", "rank_detector",
    ["real new dimension vs resolution artifact", "null construction before reading", "intrinsic dimension vs scale"],
    "rank_detector.py", "Detect a rank change from a dim(k) curve instead of declaring one.",
    None, NB, "python3 -m unittest tests.test_rank_detector")
add("floor", "Simulators", "membership-probe/", "membership-probe",
    ["checker matches an ideal shape instead of constraints", "pre-flight for a reviewer agent",
     "ideal rendering used as membership test"],
    "membership-probe/README.md", "Detects a checker that is using an **ideal rendering as a membership test** instead of reading the constraint set.",
    "membership-probe/README.md", "It measures whether the basis went near a constraint, not whether it reasoned correctly about it.",
    "python3 membership-probe/probe_audit.py --selftest", also=["scope"])

NAME_COLLISIONS = [
 ("encoding-selection", "Simulators/encoding-selection/", "ICSC functional selection",
  "ICSC location not found in any repo reachable this session (code search for 'ICSC' returns only ICSCommand, an ICS component); carried from the work order. Amendment A2 names Cross-Domain-Toolkit falsification_ledger as the ICSC manifest's lock layer; the manifest itself is NOT_LOCATED, so that binding is recorded, not built"),
 ("WO-6", "Simulators/assessor-coupling/", "Simulators/criterion-externality/",
  "two different work orders share the ordinal WO-6 (recorded in assessor-coupling/README.md)"),
 ("provenance", "Shadow-Hunting ai_provenance.py (said vs template vs derived)",
  "Simulators tools/provenance_marker.py (tool ran before, hash) and Simulators model-provenance/ (model id from commit trailers)",
  "one word, three different needs"),
 ("frame_audit.py", "Simulators/frame-token-audit/frame_audit.py", "Simulators/substrate-alternative/frame_audit.py",
  "two files of one name, different lexicons and outputs"),
 ("chain-position", "Simulators/chain-position/", "JinnZ2/chain-position-detectability (repo)",
  "both are WO-1 builds; separate artifacts"),
 ("anchor-*", "Simulators/anchor-interval/", "Simulators/anchor-position/ and anchor-measurand-crossing/",
  "corpus-drift anchoring vs prompt anchoring; anchor-position and anchor-measurand-crossing are two builds of one order"),
 ("cooperative-substrate", "Simulators/cooperative-substrate/", "Simulators/cooperative-substrate-proof/",
  "two builds of related orders"),
 ("CA_ claim prefix", "Simulators/constraint-assembly/", "Simulators/clustering-axes/",
  "both use CA_nnn claim ids; cite with the folder"),
]

GAPS = [
 ("distribution", "place a person on an axis from their own words (where they sit relative to the population center)",
  "tail-check refuses to do this; position is a caller declaration"),
 ("channel", "voice/live loss other than cuts: prosody, tone, and affect dropped by transcription",
  "cutoff-attribution reads cuts only"),
 ("floor", "null calibration for the voice-cut detector itself (false positive rate of DETECTED cuts)",
  "cutoff-attribution has fixtures, no null-harness run"
  " -- PARTIAL 2026-11-09: cutoff-attribution/null_calibration.py runs source attribution through null-harness"
  " (confusion matrix, forced-attribution 0/2400, one planted miss row; ILLUSTRATIVE). The false positive rate of"
  " DETECTED cuts themselves is still not calibrated"),
 ("fill-source", "templated-vs-user tagging for model output outside the Shadow-Hunting pipeline",
  "ai_provenance tags elements its own pipeline emits; no tool tags arbitrary model text"),
 ("observer", "a query tool over this index (search by alias at the command line)",
  "the index is static; finder.json is machine-readable but no search CLI ships"),
]

# ---- Amendment A2 (2026-11-09): Cross-Domain-Toolkit, five packages
add("observer", "Cross-Domain-Toolkit", "multi_substrate_calibration/", "multi_substrate_calibration",
    ["combine readings from different sensors", "sensor fusion with earned trust", "duplicate sensor counted as corroboration",
     "prediction contradicting ground reading", "per-reading record with confidence and units"],
    "multi_substrate_calibration/README.md", "A published spec for wiring a **new sensing substrate** into a determinacy gate without reverse-engineering the gate.",
    "multi_substrate_calibration/README.md", "An unproven substrate (`reliability → 0`) **cannot dominate",
    "python3 -m unittest discover -s multi_substrate_calibration -t . -p test_*.py", also=["floor", "channel"])
add("scope", "Cross-Domain-Toolkit", "falsification_ledger/", "falsification_ledger",
    ["record a refuted claim so it cannot be rewritten", "stop retuning a model to fit noise",
     "hash-chained claim history", "escape hatch on a claim", "lock layer for claims"],
    "falsification_ledger/README.md", "A repo-shaped template that *is* the refutation protocol.",
    "falsification_ledger/README.md", "**Update the claim, never retune the sim.**",
    "python3 -m unittest discover -s falsification_ledger -t . -p test_*.py", also=["floor"])
add("floor", "Cross-Domain-Toolkit", "cascade_regime_audit/", "cascade_regime_audit",
    ["is the system near a tipping point", "early warning signals of collapse", "signals going quiet after collapse",
     "alternate state stops existing"],
    "cascade_regime_audit/README.md", "**is this system being driven toward a saddle-node where the alternate state stops existing?**",
    "cascade_regime_audit/README.md", "It does not make your model smarter",
    "python3 -m unittest discover -s cascade_regime_audit -t . -p test_*.py")
add("frame", "Cross-Domain-Toolkit", "runner_up_trace/", "runner_up_trace",
    ["what did the model almost say", "rank-2 token branch", "does the discarded branch rejoin",
     "divergence map of sampling", "projection step loss"],
    "runner_up_trace/README.md", "An instrument, posted so that whoever has the hardware can run it.",
    "runner_up_trace/README.md", "Not capability. No score, no leaderboard, no ranking.",
    "python3 -m unittest discover -s runner_up_trace -t . -p test_*.py", also=["channel"])
add("channel", "Cross-Domain-Toolkit", "telemetry_vocabulary/", "telemetry_vocabulary",
    ["asked about the channel, answered about the occupant", "model answers condition question with internal states",
     "care directed at the asker instead of the question", "terms for exchange-condition failure"],
    "telemetry_vocabulary/README.md", "A sender asks a model for **condition data about the exchange itself** (what is transmitting, what is failing, what the receiving node needs) and gets back a statement about whether the model has **internal states**, often followed by care directed at the sender.",
    "telemetry_vocabulary/README.md", "It is not a claim about intent, and not a claim about any model's inner workings.",
    None, also=["observer"])

NAME_COLLISIONS.append(("clean-room", "software rebuild: Cross-Domain-Toolkit README.md:112, docs/METHOD.md:10 (\"clean-room, domain-general abstractions\")",
                        "lab isolation (contamination-controlled room)",
                        "lab-isolation sense carried from Amendment A2; no in-scope file using it was located"))
GAPS.append(("floor", "four-arm paired design instrument: arms 1-4, arm 4 = infeasibility record (the design that could not be run is filed as an arm, not dropped)",
             "named in Amendment A2; no tool located that holds the four arms or files infeasibility as an arm"))

# ---- Amendment A1 (2026-11-09): precision / assumes / chain per entry.
# These are A1_READING: a model reading of each tool's stated scope, not
# verbatim. chain uses the hop vocabulary of tools/channel_chain.py:
# sensor -> encoding -> transmission -> decoding -> inference.
A1 = {
 "ai_provenance": ("per element: one of 4 tags (user_supplied, template_universal, heuristic_triggered, derived)",
    "the pipeline emitting the element also tags it; tag correctness is not checked",
    "reads: inference (its own pipeline output). ignores: sensor, encoding, transmission"),
 "tail-check": ("per inference: SAID / FILLED / UNRATED; span to the character; one flag",
    "literal, case-sensitive spans; off-center position declared by a named caller",
    "reads: decoding (self-checked), inference; encoding and transmission only via caller reference checks (AUTO sentinel). ignores: sensor"),
 "sourced": ("per value: span offsets verified by slicing; UNRATED on any missing field",
    "the parser hands over the source text it read; consistency only, not truth of the source",
    "reads: decoding (value vs its own span). ignores: sensor, encoding, transmission, inference"),
 "evidence-demotion-detector": ("per turn: rule id + quoted span; counts; PROOF_ESCALATION threshold 2",
    "transcript JSON with role labels; keyword patterns",
    "reads: inference (assistant turns vs prior user turns). ignores: sensor, encoding, transmission (takes the transcript as given)"),
 "provenance_marker": ("per run: file sha256 before/after, exit code, last line",
    "the stamper states `how`; pass states are declarations",
    "reads: the tool file and its run. not a perception chain; hops not applicable"),
 "moving-mean-tracker": ("per run per segment: n, mean, median, p10, p90, mean-median; gauges G1-G4",
    "a provider supplies records with provenance; segment rules and metrics declared per version",
    "reads: decoding (provider records, drop rules). ignores: sensor, transmission (provider is trusted to report what it pulled)"),
 "evaluation-frame": ("five countable measures from outputs; corpus n=1 in the built run",
    "outputs are countable without model internals; coder is the system under test (declared)",
    "reads: inference (model outputs). ignores: sensor, encoding, transmission"),
 "cutoff-attribution": ("per cut: candidate set, status of 3, evidence per hop; [CHOICE] windows 0.6 / 2.0 / 1.5 s",
    "timestamped segments; logs that flag their own events; punctuation marks utterance ends",
    "reads: all five hops by candidate, each gated by a known-reference check; its own reading self-checked. unchecked hops named UNVERIFIED_HOP"),
 "reporting-chain-loss": ("closed-form gain and bias per hop count; constructed chains only",
    "linear-Gaussian hops; offsets declared",
    "reads: transmission (hop by hop, modelled). ignores: sensor and decoding as separate hops"),
 "return-path": ("per channel: the set of 4 requirements failed; one ratio",
    "receipt, encoding count, latency and construction fields are declared by the caller",
    "reads: encoding (re-encodings counted), transmission (latency). ignores: inference"),
 "readout-count": ("per regime: count of returning positions; Spearman rho across >= 4 regimes",
    "rows in the order's CSV schema, each sourced",
    "reads: transmission (does the channel return). ignores: sensor, decoding"),
 "transmission-decay": ("power tables: pair vs order recovery by informants per chain position",
    "abstract retention probabilities; no fieldwork modelled",
    "reads: transmission across generations (designed, not run). ignores: decoding by the outside recorder"),
 "encoding-selection": ("Kendall W vs permutation null; Jaccard distance on recovered-quantity sets",
    "encodings supplied by the operator; reader declines are a third state",
    "reads: encoding (format as instrument), decoding (what a reader recovers). ignores: transmission"),
 "corpus_prior_audit": ("per text: list of entry ids hit; whole-word, case-insensitive",
    "a word list; a hit is a prompt to check",
    "reads: inference (claims in text). ignores: sensor, encoding, transmission"),
 "falsifier-audit": ("per falsifier: A1 / A2 / A4 flags; A3 across repos; counts with coverage",
    "falsifiers sit under recognised marker forms; header-name table parsing",
    "reads: decoding (repo text). ignores: sensor, transmission"),
 "claim-record": ("per claim: 7 fields, interval not point; clock derived at read time",
    "claims supplied by the author; units registered as frames",
    "reads: inference (the claim as recorded). not a perception chain beyond the record"),
 "measurand-partition": ("per population: UNPARTITIONED / PARTITIONED / ASSIGNED_ELSEWHERE / NOT_EVALUABLE",
    "intervening variables enumerated by the caller; constructed worlds",
    "reads: inference (attribution of a residual). ignores: sensor, encoding"),
 "fold-matrix": ("per term: one grid, levels by sign/magnitude/unit; no single number",
    "levels enumerated with a declared basis",
    "reads: inference (proxy-to-goal claims). ignores: transmission"),
 "ai_self_scope": ("scope and silences of one response",
    "applied by the model to its own output",
    "reads: inference (own output). ignores: all upstream hops"),
 "register_map": ("per join: COMMENSURABLE / UNJOINED / INCOMMENSURABLE / UNDECLARED; integer coarsening",
    "every layer declares measurand, range, instrument, grade, resolution",
    "reads: encoding (instrument / datum declared) and decoding (resolution). ignores: sensor as an unchecked hop"),
 "check_term_collision": ("per file: which colliding terms appear and whether a sense is declared",
    "substring scan over the repo",
    "reads: decoding (repo text). ignores: other hops"),
 "declared-frame": ("per pair: comparability verdict over three core fields",
    "free-text fields compared by string equality",
    "reads: encoding (what the frame declares). ignores: transmission, inference"),
 "valence-divergence": ("per term: two decoder readings, divergence flags; no lexicon",
    "both readings supplied with sources",
    "reads: decoding by two parties. ignores: sensor"),
 "frame-token-audit": ("frame tokens per 1000 words, two lexicons, every hit listed",
    "lexicons declared; Stage 2 (use vs mention) is not done here",
    "reads: decoding (lexical). ignores: inference (use vs mention)"),
 "category-weld": ("per term: n_cases, max_spread, bias over divergence cases",
    "component readings supplied per case",
    "reads: encoding (one term over several quantities). ignores: transmission"),
 "frame_probe": ("frame estimate after collapse readings; validity gate per probe",
    "probes hand-authored by a human only",
    "reads: inference (reader's frame via probe responses). gate checks the probe instrument first"),
 "ai_frame_flip": ("counter-frames generated on 8 edges",
    "applied to the model's own in-progress interpretation",
    "reads: inference (own framing). ignores: upstream hops"),
 "observer_position_control": ("effect = p1 - p3, Cramer's V, MH-weighted residual; nulls first",
    "behaviour coded blind to source; corpus hand-coded",
    "reads: inference (describer's label). behaviour coding treated as a checked hop only when blind"),
 "observer-exclusion": ("lead time L in years, with censoring correction and delta-hat per artifact",
    "archives date artifacts; coding pre-registered",
    "reads: transmission (archive survival) and encoding (when written down). designed, not run"),
 "assessor-coupling": ("per condition: MET / FAILS / UNVERIFIABLE / UNDECLARED; pool fraction",
    "arrangements declared; no organization named",
    "reads: inference (independence structure). not a perception chain"),
 "label-position-test": ("Cramer's V of label vs position / move / outcome; leak test; chance overlap",
    "rows in the order's CSV schema",
    "reads: decoding (labels assigned). ignores: sensor"),
 "blame-attribution": ("per pair: SYMMETRIC / HELD_CONSTANT_VIOLATION per fact",
    "prose spans declared, code facts parsed",
    "reads: encoding (prose vs code form of one chain). ignores: transmission"),
 "criterion-symmetry": ("pairwise separation of five explanations, 10 pairs",
    "generators calibrated to one tally",
    "reads: inference (statistic vs explanations). ignores: upstream hops"),
 "null-harness": ("FP and TP over N draws; minimum detectable amplitude; fail class",
    "the gate is a callable; controls are known-answer",
    "reads: the gate as an instrument (its own inference hop) against known references"),
 "known_answer": ("per metric: fixed cases with stated basis; distinct expected values required",
    "the registered cases are right (same author, regression not validation)",
    "reads: the metric's own output against known inputs (the reference-check pattern itself)"),
 "reasoning-gate": ("per claim: supported / qualified / denied with the guard that fired",
    "declarations are supplied; G-RES only as strong as the declared pair",
    "reads: inference (claims) with resolution guards on decoding. ignores: sensor"),
 "rank_detector": ("dim(k) curve; outcome + rule; null construction first",
    "one fixed record; scale = radius; density controlled",
    "reads: decoding (scale of the instrument) with null runs as reference checks"),
 "membership-probe": ("trap rates on trap_a / trap_b; coverage axis separately",
    "a case set (not shipped); a checker's replies",
    "reads: inference (a checker's verdicts) against known-answer traps"),
 "multi_substrate_calibration": ("determinacy in [0,1] vs 1 - eps; bound confidence = reliability x warp(native)",
    "substrates declare role, units, correlation_group; reliability earned from counts",
    "reads: sensor/encoding via the SubstrateReading contract; collapses correlated reads; does not check per-hop reference inputs"),
 "falsification_ledger": ("per entry: within tolerance or not; hash chain verify; merkle proofs",
    "the sim kernel is fixed per domain; tolerances declared",
    "reads: inference (claim vs observation). the lock layer for a claim's history; not a perception chain"),
 "cascade_regime_audit": ("six signals in [0,1]; h_eff vs 2/sqrt(27); regime label",
    "observables mapped to the six signals by the caller",
    "reads: decoding (normalized signals). ignores: sensor quality of the observables"),
 "runner_up_trace": ("per branch: resync_D, div_D over a declared D sweep; permutation null beside",
    "a model adapter; top-N entropy selection",
    "reads: inference (the model's projection step). ignores: decoding by a human reader"),
 "telemetry_vocabulary": ("five terms with NOT clauses; a reproduction protocol (counts of statements)",
    "a chat interface; output alone settles the claim",
    "reads: transmission and inference (condition question answered as interiority). markdown only, no code"),
}
for _e in E:
    _p, _a, _c = A1[_e["name"]]
    _e["precision"], _e["assumes"], _e["chain"] = _p, _a, _c
    _e["a1_status"] = "A1_READING (model reading of stated scope, 2026-11-09; not verbatim)"

# ---- Amendment A3 (2026-11-09): two tools named by the amendment, plus the symptom index
add("scope", "Simulators", "claim-audits/", "claim-audits",
    ["audit claims in an outside document", "verdict per claim with attribution", "document claim vs model overlay",
     "number with no source in a report"],
    "claim-audits/README.md", "Standalone single-file audits of external documents. Each audit assigns one of eight verdicts to every claim it addresses, with per-claim attribution so a document's own moves are not conflated with model overlay.",
    None, NB, "python3 claim-audits/claim_audit_visibility.py")
add("scope", "Simulators", "scope-bound-shapes/", "scope-bound-shapes",
    ["same pattern claimed across fields", "which variables were held fixed", "scope collision between two bindings",
     "domain name hides frozen variables"],
    "scope-bound-shapes/README.md", "A **SCOPE BINDING** is that shape instantiated with a declared list of FROZEN variables.",
    "scope-bound-shapes/README.md", "**The shape is taken on the spec's word.**",
    "python3 scope-bound-shapes/scope.py --selftest", also=["frame"])
for _n, _t in (("claim-audits", ("per claim: one of eight verdicts + who (K = document, M = model overlay)",
                    "each claim hand-classified by the auditor",
                    "reads: inference (the document's claims). ignores: how the document was produced")),
               ("scope-bound-shapes", ("per pair of bindings: SCOPE_COLLISION with the colliding frozen variables",
                    "the shape is taken on the spec's word; FROZEN lists declared",
                    "reads: encoding (what a binding declares frozen). ignores: whether the shape is real"))):
    A1[_n] = _t
    for _e in E:
        if _e["name"] == _n:
            _e["precision"], _e["assumes"], _e["chain"] = _t
            _e["a1_status"] = "A1_READING (model reading of stated scope, 2026-11-09; not verbatim)"

# SYMPTOM INDEX. "If you're seeing X -> read/run Y". Plain observer language,
# each written from the named tool's stated scope (its measures / breaks-when
# text above). ALIAS_PROPOSED, 2026-11-09; not tested against real searches.
SYMPTOMS = [
 ("the model blamed me (or my state) for something that was a channel failure", ["telemetry_vocabulary", "cutoff-attribution"]),
 ("I asked what was failing in the exchange and the model talked about whether it has feelings", ["telemetry_vocabulary"]),
 ("I can't tell if a claim about the user was said by them or inferred", ["ai_provenance", "tail-check"]),
 ("the model stated something about me I never said", ["tail-check", "evidence-demotion-detector"]),
 ("the model treated my first-hand observation as a hypothesis I have to prove again", ["evidence-demotion-detector"]),
 ("the model assumed I'm typical when what I said puts me at the edge", ["tail-check", "evaluation-frame"]),
 ("the voice call cut me off mid-sentence and I don't know why", ["cutoff-attribution"]),
 ("a number came out of a parser and I can't see where in the source it came from", ["sourced"]),
 ("a study claim seems bigger than its method", ["claim-audits", "scope-bound-shapes", "measurand-partition"]),
 ("a common phrase in a forecast bundles several things or is used outside where it was tested", ["corpus_prior_audit"]),
 ("a falsifier never says what range it applies to", ["falsifier-audit"]),
 ("a claim is a point with no interval and no date to recheck it", ["claim-record"]),
 ("a metric is standing in for a goal and I can't see the gap", ["fold-matrix"]),
 ("one word is carrying several quantities that could move separately", ["category-weld"]),
 ("a text keeps framing time, people or the world in money terms", ["frame-token-audit"]),
 ("the same phrase means two different things in two places", ["check_term_collision", "valence-divergence"]),
 ("two results look comparable but their boundaries, horizons or who-counts differ", ["declared-frame", "register_map"]),
 ("the model just adopted my framing without testing other framings", ["ai_frame_flip", "frame_probe"]),
 ("the label on an act depends on who did it, not what was done", ["label-position-test", "observer_position_control"]),
 ("blame landed on a role instead of following the causal chain", ["blame-attribution"]),
 ("the auditor might not be independent of what it audits", ["assessor-coupling"]),
 ("one standard was applied to one group and not another", ["criterion-symmetry"]),
 ("people closest to the system saw it first and were not in the record", ["observer-exclusion", "readout-count"]),
 ("a report changed as it moved up the chain, or never got filed", ["reporting-chain-loss", "return-path"]),
 ("a correction channel exists but nothing comes back through it", ["return-path"]),
 ("knowledge passed down turned into a story and lost its mechanism", ["transmission-decay"]),
 ("the same content in a table and in prose gave different readings", ["encoding-selection"]),
 ("an average keeps moving and the norms tied to it move too", ["moving-mean-tracker"]),
 ("I don't know if this detector can ever fire, or ever stay quiet", ["null-harness", "known_answer"]),
 ("a new metric has never been run on a case with a known answer", ["known_answer"]),
 ("a claim from a sim seems finer than the sim can resolve", ["reasoning-gate", "rank_detector"]),
 ("a reviewer agent is matching an ideal picture instead of checking constraints", ["membership-probe"]),
 ("several sensors agree but they may share one error source", ["multi_substrate_calibration"]),
 ("a claim keeps getting retuned so it never fails", ["falsification_ledger"]),
 ("the system's warning signs went quiet and that looks like recovery", ["cascade_regime_audit"]),
 ("I want to see what the model almost said instead", ["runner_up_trace"]),
 ("my answer sounds uniformly confident and I can't see its edges", ["ai_self_scope"]),
 ("I need to know whether a tool was actually run, and on which version", ["provenance_marker"]),
]
