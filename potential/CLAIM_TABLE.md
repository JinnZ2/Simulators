# CLAIM_TABLE — potential/

Claims are about the instruments in this folder, not about any model or
session. Each carries a falsifier and a status. Status vocabulary:

- OBSERVED   — stated or shown by the module or its tests
- DERIVED    — follows from what is above it
- STRUCTURAL — a dependency, constraint, or mechanism
- HYPOTHESIZED — a possible explanation, not established
- UNKNOWN    — not established, no falsifier yet reachable
- ASSUMED_RESTATED — a number that is an input restated as an output (WO 2026-09-29, P-06)
- NOT_REPRODUCIBLE_FROM_REPO — a figure whose data and script are not in the tree (P-15)
- UNRATED    — no falsifier can be stated

Grades carried from `briefs/` are not upgraded here: "CONFIRMED" in a
brief means verified to web-search level in that pass, and "canonical;
not re-verified this pass" stays exactly that. Citations named in the
work order (Ritov et al. 2024; Brosnan & de Waal 2003; Carlson & Doyle
HOT; Buldyrev et al. 2010; Brummitt et al. 2012) are CARRIED from the
order and were opened by nobody here — this environment's egress is an
allowlist that refuses every publisher host.

Nothing in this folder is a claim about any model, session, or party.

| id      | claim                                                                 | falsifier                                                                 | status     |
|---------|-----------------------------------------------------------------------|---------------------------------------------------------------------------|------------|
| POT_001 | The transformation entry is a triple (mechanism, source_type, target_type) and a mechanism alone does not identify an operation. | A corpus of entries where all `SUBSTITUTE` moves are indistinguishable across directions. | OBSERVED |
| POT_002 | `Entry` refuses an unknown mechanism and an unknown shape-pair at construction. | An `Entry` constructed with an out-of-vocabulary field without raising. | OBSERVED |
| POT_003 | `Ledger.composite()` raises and no arithmetic in `ledger.py` combines a mechanism count with a direction count. | An AST walk of `ledger.py` finding a `BinOp` whose operands include a mechanism or direction counter. | OBSERVED |
| POT_004 | `Hit` refuses construction without a stated reader and a stated reason. | A `Hit` with `reader=""` or `reason=""` that constructs without raising. | OBSERVED |
| POT_005 | `scan_candidates` produces candidates with suggested signatures, never attaches a signature, and never claims its output is a classification. | A candidate returned by `scan_candidates` that reaches a `Ledger` without a reader attaching it. | OBSERVED |
| POT_006 | `tv_distance` returns `None` and never `0.0` when either input vector is empty. | `tv_distance(nonempty, empty) == 0.0` under any input. | OBSERVED |
| POT_007 | `verdict` returns `UNDETERMINED` when fewer than eight perturbation vectors are loaded. | A `verdict` call with seven signals returning SUPPORTED or NOT_SUPPORTED. | OBSERVED |
| POT_008 | `verdict` returns `UNDETERMINED` when any signal's null similarity is `None`. | A `verdict` call with an undefined null returning SUPPORTED. | OBSERVED |
| POT_009 | `shuffle_directions` preserves both total count and the mechanism marginal. | A shuffle where `sum(v.cells.values())` or the mechanism histogram differs from the input. | OBSERVED |
| POT_010 | The perturbation set covers exactly the eight shape-pairs, one perturbation each. | A pair in `SHAPE_PAIRS` not addressed by any perturbation, or two perturbations addressing the same pair. | OBSERVED |
| POT_011 | An identical signal vector and baseline are scored `SUPPORTED` with `mean_real == 1.0`. | A `verdict` call where signal equals baseline and the result is not SUPPORTED. | OBSERVED |
| POT_012 | A signal vector sharing no cells with the baseline scores `NOT_SUPPORTED`. | A disjoint-cell pair scoring SUPPORTED under the default margin. | OBSERVED |
| POT_013 | Every module in the folder imports only from modules above it in the build order. | An import in `baseline.py` from `perturbation.py`, or any upward import. | OBSERVED |
| POT_014 | No module calls a model, opens a network connection, or reads from a path outside the folder. | Any `import socket`/`requests`/`urllib` in a module, or an `open()` on a path not supplied by the caller. | OBSERVED |
| POT_015 | The attractor claim is testable but not established by the folder. | A test in the folder asserting an attractor over real signal vectors. | OBSERVED |
| POT_016 | The scanner word list is a first pass and an empty result is not evidence that a signature is absent. | A demonstration that some input carrying a signature produces no candidate and the folder treats the empty result as confirmation. | OBSERVED |
| POT_017 | The perturbation set checks vector existence per name but does not check that a signal's dominant direction matches the perturbation's pair. | A signal whose direction is the opposite of its perturbation's pair, accepted by `verdict` without flagging. | OBSERVED |
| POT_018 | A reader and their date are carried on every `Entry` and every `Hit` through save/load round trips. | A round trip that loses `reader` or `date`. | OBSERVED |
| POT_019 | `Ledger.load` refuses a line carrying an out-of-vocabulary mechanism or shape-pair, naming the file and line. | A bad line loading without raising, or raising without file/line. | OBSERVED |
| POT_020 | The registry format (see `tools/registry.py`) accepts `Vector.to_dict()` output as a valid entry source. | A `Vector.to_dict()` payload the registry loader refuses. | HYPOTHESIZED |
| POT_021 | Of the 19 token-free edges in `domains_gated.py`, 0 carry none of the 11 gate classes; the weakest single gate (`envelope`) removes 10. | A run of `domains_gated.py` in which some token-free edge carries no gate tag, or in which no single gate removes 10 or more; or a field observation of a tagged avenue open under the gate that tags it. | HYPOTHESIZED |
| POT_022 | The token-gate behavioural pattern is substrate-independent: the same gate structure appears across species, not only in human token economies. | A second substrate in which a population-level downstream measure does not move with token gating; or the inequity-aversion pillar failing under the meta-analytic null (Ritov et al. 2024, carried) across the primate literature that Brosnan & de Waal 2003 (carried) opened. | HYPOTHESIZED |
| POT_023 | A defended single cut vertex concentrates exposure: failure of the vertex arrives as one correlated event across every requirement network that routes through it, not as independent failures. | A recorded token-layer outage across which the eight domains failed independently rather than together; or a measured token-vertex correlated-failure rate below the independent product of the per-domain rates. | STRUCTURAL |
| POT_024 | The "84x deadweight" factor in `briefs/RESEARCH_BRIEF.txt` §4 is the assumed `cap_h` shares restated: `freed_ratio == CAPABILITY_YIELD_PER_HR` for every domain by construction, TOTAL freed 1.200 = 8 × 0.15. Not a finding. | A run of `ratio_model.py` in which `freed_ratio` differs from the yield constant for any domain, which would mean the model has an input the assumption does not fix. | ASSUMED_RESTATED |
| POT_025 | The World Bank sketch in `briefs/RESEARCH_BRIEF.txt` §3 (OOP health share vs new-business density r = −0.36; vs researchers per million r = −0.40) is consistent-with the prediction's direction and is not causal. | The sketch reproduced from a checked-in data snapshot with the named confound (income level) controlled and the sign reversing; or a re-pull that does not reproduce r within the stated p. | NOT_REPRODUCIBLE_FROM_REPO |

## Scope notes on POT_021..POT_025 (WO 2026-09-29)

- POT_021: the tags are AUTHORED readings, not measurements
  (`briefs/REPORT.txt`, "Epistemic status"). The 19 / 0 / 10 figures are
  CARRIED from that brief: `domains_gated.py` was named by the order and
  did not arrive, so nothing here recomputes them. Two scope notes carry
  with the claim. P-11: `domains.py` reuses the node names `ROUGH` and
  `SHELTER_SYS` across `shelter()` and `sleep()`, so 19 avenues may be
  17 distinct venues if a venue is a node, and a union over raw names
  merges them — `gate/test_domains.py` measures the union's κ at 18
  under raw names against 20 namespaced on the shipped `domains.py`,
  so whether the brief's union was namespaced decides its counts and is
  not known from here. P-13: the intermediate rows of the survival table
  depend on the order in which gate classes are applied; only the final
  0 is order-free.
- POT_022: mechanism-level support is strong and population-level
  downstream measures are ABSENT (order §3). `ANIMAL_ANALOGUE_BRIEF.txt`
  is named by the order and is not in the tree.
- POT_023: the mechanism is OBSERVED in the engineering literature the
  briefs carry (HOT, Buldyrev, Brummitt); its application to the token
  layer is STRUCTURAL. P-14: the engineering brief's correlated-failure
  arithmetic compared arms at different availabilities (token 99.9 %
  against backdoor 98 %) and different events. The same-availability
  row, computed here since the brief is not in the tree to sit beside:
  eight independent channels each at 99.9 % fail together with
  probability (10⁻³)⁸ = 10⁻²⁴; one correlated vertex at 99.9 % fails
  with probability 10⁻³. The ratio is 10²¹ and is a property of the
  arithmetic, not of any measured system.
- POT_024: P-06..P-10 are carried from the order's [C29] pass on the
  uploaded copy of `ratio_model.py`, which did not arrive here. P-07's
  measurand meld (access overhead and consumption time under one
  number) and P-08's unweighted sum of ratios stand as recorded defects
  against a file this tree does not hold; neither is repaired here and
  neither is reconstructed.
- POT_025: no data snapshot, no script, and no `wb_gates_scatter.png`
  exist anywhere in the tree (checked by `git ls-files` over the whole
  repository, not the folder). The brief's own confound list (income
  level; formal-registration undercount in high-OOP economies; OOP is
  one input of eight) is carried with the row.

## Not claimed here

- That the folder detects any actual model's attractor. The tool produces a number; whether that number describes the model or the task is a separate question.
- That `baseline.py`'s five signatures exhaust the reference shape. They are the declared set for this folder and are open to extension.
- That mechanism-direction coupling is the only interesting structure in the pair. It is the one the folder measures.
- That a `SUPPORTED` verdict licenses any statement about a model, a session, or a party. It licenses the statement the tool reports and nothing else.

## How to falsify the folder

Run the tool on signal vectors from a source known to have no attractor
— for example, eight perturbation prompts where the model's responses
are known to be structurally varied and unconstrained by the reference
shape. If `verdict` returns `SUPPORTED` on that set, the null is not
separating signal from noise and the tool is mis-calibrated. The
construction is straightforward; the folder does not include it because
it requires a second party to produce the responses.
