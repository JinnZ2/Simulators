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
  "location not found in any repo reachable this session (search for 'ICSC' returned no hit); carried from the work order"),
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
  "cutoff-attribution has fixtures, no null-harness run"),
 ("fill-source", "templated-vs-user tagging for model output outside the Shadow-Hunting pipeline",
  "ai_provenance tags elements its own pipeline emits; no tool tags arbitrary model text"),
 ("observer", "a query tool over this index (search by alias at the command line)",
  "the index is static; finder.json is machine-readable but no search CLI ships"),
]
