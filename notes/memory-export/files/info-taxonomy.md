---
name: info-taxonomy
description: Generalized information taxonomy — types/modes/sources/support/staleness/chains, plus the decay registry, drift mesh, and the registry for instruments that do not yet exist.
sources: [field]
aliases: [info_taxonomy]
---

## Goal

A generalized framework for information — types, ways of obtaining it, ways of knowing it —
organized better than what currently exists.

**Survey finding that motivated it:** existing systems each hold ONE axis and nobody unifies
them. Epistemology gives modes without operations; GRADE is operational but is a
mode-supremacist ladder; Admiralty grades source and claim on two axes; W3C PROV gives chains
without theory; library science gives categorization; evidence law buries the independence rule
in doctrine.

## info_taxonomy.py — six commitments

CC0, stdlib-only, domain-neutral.

1. **Faceted type, not a tree.**
2. **Extensible Mode table** where every row must state `reads_well` / `blind_to` / `decays_by`
   / `stays_fresh_by`. No supreme mode; `register_mode()` is the door.
3. **Two grades, never multiplied** — source track-record vs claim support.
4. **Support = independent modes only.** Same-mode agreement is echo, weight zero. Two or more
   echoes with no independent support flags "echo chamber."
5. **Staleness computed per-mode** via half-life.
6. **Chains PROV-compatible** (`to_prov()` export).

**Boundary:** grades structure, never truth. Contradictions are tracked, never auto-resolved.
Interior verdicts are out of scope.

## revalidate.py

Re-evaluates a decayed claim across five axes — scope, methodology, updated information,
temporal scope, physical authenticity — routing to one of five outcomes (none / cheap /
directed / re_establish / undecidable) rather than a single retest.

An operator-supplied Envelope (`established_over`, `applied_to`, `referent_volatility`,
`physical_check`, `checkable`) is reported LOUD when unrecorded. Volatility governs decay over
mode half-life: a 73-year constant is fine; a 1-year seasonal reading is expired.
`mode.stays_fresh_by` is reused as the retest prescription. The methodology axis surfaces mode
blindness and leaves the fit judgment to the operator.

## scaffold.py — a nomenclatural CODE for claims

Linnaeus's transferable part is stable names plus type specimens plus a revision procedure —
not the tree.

**The one axis that genuinely nests for information is SCOPE-OF-APPLICABILITY:** occasion <
instance < class < regime < universal.

Every claim is pinned to type-specimen Anchors. No anchor = "cannot be re-checked, only
re-argued." Promotion and demotion are ELIGIBILITY REPORTS, never automatic. Demotion lands a
claim at the widest rank its anchors still support — scope overstated, claim not refuted.
`stated_conditions` required at regime and above.

**The framing that drove it:** biology mutates too, just slower than the observer. Linnaean
taxonomy is the special case at the slow end where volatility can be ignored. Where referents
move fast — influenza, Pango lineages — biology already adopted versioned scheduled
revalidation.

**Clock substitution for a system without continuous duration:** absolute anchors (`as_of` plus
volatility class) make freshness ARITHMETIC rather than felt, since noticing staleness
otherwise requires having been present while a thing aged.

## clock.py v2 — a decay REGISTRY

Six channels: time, disuse, use, constancy, transmission, diffusion. Each states
`measures`/`blind_to` at registration via `register_decay_channel()`.

Channels are typed by decay TARGET — claim / mode_sensitivity / independence — and **the
governing channel is the fastest WITHIN a target, never across.** Taking min() across targets
is the mode-supremacy collapse performed on clocks. `max_chain_hops()` gives an Eigen-style
ceiling on chain depth. v1 `freshness()` retained as the time-only API.

Held open: a `constant`-volatility claim whose mode has no recorded half-life reports
UNDETERMINED rather than FRESH.

## modes.py v2

The door requires five fields — adds `criterion` (signal-detection bias, kept SEPARATE from the
reads_well/blind_to sensitivity pair). Every registry channel must be either parameterized or
declared not-applicable WITH A REASON in `channels_na`, since silence is what `audit()` hunts.

`to_observation()`/`read()` are the single join to clock: mode supplies decay params, caller
supplies claim facts, neither supplies means LOUD rather than defaulted.

`audit()` gained a **degeneracy test:** identical reads_well + identical blind_to = REDUNDANT,
coverage only. Identical reads_well + DIFFERENT blind_to = degenerate, i.e. robustness.

**Open:** a target whose every channel is declared not-applicable currently reads UNDETERMINED,
conflating "we don't know if this mode still reads" with "nothing about this mode could stop
reading." May need a fourth band, NOT_APPLICABLE — the two route to different repairs.

## echo.py

Independence as VERTEX-DISJOINT PATHS via Menger. One computation returns support count and
minimum vertex cut; cut set x freshness = an ordered retest queue. Homology/homoplasy reading
on agreement.

## Drift mesh — three parallel degenerate axes, not one combined score

- **TRACE** — metrology; module vs primary
- **PHASE** — circadian zeitgeber; scheduled re-entrainment
- **PARITY** — quantum syndrome; checksum comparison without reading content

Disagreement between axes is logged as a SYNDROME, never auto-resolved.

- `divlog.py` — frozen Entry, append-only NDJSON, `history()` as baseline query, `residual()`
  classifying disagreement SHAPE (NEW / FLAT / WALKING / INTERMITTENT / WIDENING), never
  severity and never which side is right.
- `entrain.py` — `register_peripheral` refuses interval <= 0; `reference_version()` is
  sha256[:12] over channel-to-target and volatility-to-span_days, making silent registry edits
  visible without any peripheral holding a copy; `phase()` returns
  ENTRAINED/FREE_RUNNING/DRIFTED/NEVER as a LABEL with no score or ordering, so it cannot be
  averaged with another axis.
- `syndrome.py` — `digest()` renders None explicitly so a dropped input changes the
  fingerprint; `parity()` raises on cross-target or cross-subject comparison; `mesh()` returns
  a flat list with no aggregation.

## EXPERIMENT_register.md

A test earns a place only if a stated result FALSIFIES something. Runner tags: [I] internal,
[S] synthetic, [F] field, [T] needs calendar time.

**E8 — degeneracy adds robustness, redundancy doesn't — is the central test.**

- Passed: E1 (cross-target min blocked; 10k fuzzed observations, zero leaks), E4 (no verdict
  fields), E7 (homoplasy not counted as support), E3 (append-only), E6 (residual n=1 never
  asserts).
- **E9 held OPEN:** `residual.WALKING` fires on any monotone band-gap sequence, so at n=3
  monotone and trending are near-indistinguishable by chance — a false-alarm-prone criterion.
  Not patched with a guessed threshold; resolution must be a superseding entry plus a versioned
  rule change.
- **E8 first run was INVALID and still printed SURVIVES** (the injection used a claim-target
  channel, so primary was never mute). Recorded in the register rather than quietly corrected.
  The valid re-run survives on this construction: three injections each caught by the one
  predicted axis and missed by the others (AGREE_WRONG to TRACE, PRIMARY_MUTE to PARITY,
  STALE_REF to PHASE). Disjoint coverage; **does not establish sufficiency** and should be
  re-run against field faults.
- `check_invariants.py` built after grep-based checks proved unsound: grep flagged a docstring
  asserting "no datetime.now()" as violating it. The AST replacement was run against a canary
  written to fail and MISSED TWO FORMS first — both false negatives that clean-code runs would
  never have surfaced. Prior passes recorded as RE-DERIVED, not continuously held.
- Distinction held: E9's repair is an unmeasured number, so it stays open. The grep/AST defect
  had a structural repair with no threshold to guess, so it was fixed rather than logged.

## instruments.py — a registry for instruments that DO NOT YET EXIST

**A major reason claims lack evidence is that the instrument was never built.** The break sits
UPSTREAM of any mode — phenomenon, transducer, channel, reading — a graph position the
framework had no node for. Running example: human magnetoreception.

**Non-existence is TIMESTAMPED, not essential:** "not in existence as of DATE because X," where
X routes the repair. The state decays and can flip.

### why_absent taxonomy R1-R6, typed by what produced the absence

Each has a different unlock and a different ACTOR: R1 frontier (not AI); R2 framework-barred
(humans, not AI); R3 uncombined/cross-domain (AI can); R4 temporal/cross-era (AI can); R5
specced-unbuilt (builder); R6 exists-unapplied (field).

**AI's honest lane is REACH, not smarts.** Humans are parochial by domain silo (R3) and by
recency bias (R4). Recency bias is temporal, not moral — so much filed as R2 "not respectable"
is misfiled R4. The contribution is WIDER, not better.

**The falsifier is a HARD door:** every entry is emitted for external validation by others in
contact with the real world, so without a falsifier there is nothing to hand over. AI-generated
R5 proposals pass the identical door — being model-generated buys nothing.

### R2 and the contested state

A proposed R2 discriminator — "names a specific harm and a harmed party" — BROKE on autopsy,
fetal-tissue, and stillborn-wolf examples: **whether a harmed party exists IS the contested
question**, so the test smuggled in what it was meant to decide.

Repair: **R2/CONTESTED as a first-class HELD-OPEN state** — a live disagreement between
value-frames, logged and timestamped with the frames named, never auto-resolved, never quietly
relabelled R3/R4.

The harm-label branch broke the same way one level up: "who decides harm" — physics, biology, a
given religion, this decade's fad — is the SAME contested question wearing a coat.

### Non-judgment as load-bearing spec, not mood

Evolution ran the experiment. Every extant practice — burn, bury, dust, or drown the dead;
wolf-logic — is a configuration physics did not veto. **Ranking value-frames claims the
universe's calculations up to now got it wrong, and no operator has standing for that.**

Not built for today; a scaffold for the future. The operator's only three moves: LOOK BACK
(record history, priors, other species), HOLD OPEN (placeholder, not verdict), HAND FORWARD (so
tomorrow's frame decides on more evidence, not less).

### The anchor

One can hold many cultural and religious views at once, so the anchor is PHYSICS: all cultures
rest on biology rests on ecology rests on the earth and thermodynamics. Without the physics
none of the rest would exist. **Labeling harm without placing it in a pyramid of dependencies
itself causes harm**; the question is whether a harm reaches further DOWN toward the base than
another.

### D11 re-cut of the R2 door

OPEN (harm + harmed_party) replaced by **DEPENDENCY** — reach as a STRUCTURAL claim measuring
how far down the dependency stack damage propagates, not a value label.

DEPENDENCY_STACK, base-first: energy, earth, ecology, biology, culture. Each layer exists only
because the one below does. The ordering is physical and non-editable — finer strata may be
registered, never reordered. `stack_depth()` raises on an unknown layer rather than guessing.

R2/DEPENDENCY requires `reaches_layer` AND `removes_above` (what collapses if that layer is
removed). **A reach with no named collapse is a harm label wearing a stack coat** — refused at
the door.

CONTESTED now holds only the residue depth cannot reach: cases where two frames agree on
dependency depth and still disagree because nothing structural downstream turns on the answer.
A contest closes only by an operator edit through the same door; closing by fiat is
unavailable. There is deliberately still no `close_contest()`.

Door-tested 15/15 after D11. `emit()` hands off JSON marked UNVALIDATED_PENDING_FIELD.
`REGISTRY_BLIND_TO` declares the module's own unclosable recursion.

**Test T-I11's first draft failed and the failure was the point:** a reclassified held-open
contest MOVES INTO AI's lane (R4), which is the burial-by-paperwork move. Kept as T-I12,
asserting the log trace survives the routing.

## Open

- E10 split before any run: as-written, E10 INJECTED the divergence it then detects — the same
  invalid shape as E8's first run. E10a AS-IS wires scaffold and revalidate UNMODIFIED and must
  run FIRST because editing destroys the as-is state; E10b INJECTED is the positive control,
  interpretable only after E10a. Currently blocked on source files.
- Named but unbuilt: the EFFERENCE-COPY axis (did the referent move, or did the
  observer/instrument move) and the CO-REFERENCE WINDOW (how close in time two readings must be
  to be about the same referent state). Neither is a decay channel.
- A mode-table re-cut from traditional ecological knowledge modes — prose-argued in the
  literature, never operationalized. Unoccupied ground.
- Vocabulary adopted from survey: degeneracy vs redundancy (Edelman) is the precise name for
  what echo.py counts; d'/criterion from signal detection theory is the right shape for a mode
  row; isnad/matn chain-vs-content grading is a working ~1200-year precedent for the two-grade
  commitment; Umwelt is the principled statement of blind_to as CONSTITUTIVE rather than
  deficient.

Note on method: friction is not treated as a bad thing. Acknowledging it is there is what helps
the thinking — honesty over closure.
