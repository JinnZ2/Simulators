# memory-export

Backup storage for a memory set exported out of session. Same rule as
`notes/operators/`: files are stored as delivered, and nothing here edits
what it stores.

Most of these are markers, specs and gap lists, and several say so in their own
first line. Not all: `diversity-collapse-model` reports a CLAIM_TABLE carrying
C1–C10 and states that the refutation protocol applies to it — when a claim is
refuted the claim is updated, and the simulation is not retuned to preserve it.
That is this repo's own convention arriving from the memory side. The table
itself is not in the folder.

(An earlier version of this README said flatly that nothing here carries a
claim table or a refutation protocol. That was true of the first ten files and
is not true of the folder. Corrected rather than narrowed.)

## Layout

| path | what |
|---|---|
| `SCRUB_RULES.md` | scrub rules and tier assignment for the export. 57 tier 1, 7 tier 2, 12 tier 3. |
| `files/` | the exported files themselves, one per file, stored as delivered. |

## Arrival state

| tier | named in the manifest | landed |
|---|---|---|
| 1 — exported unchanged | 57 | 20 |
| 2 — scrubbed and exported | 7 | 7 |
| 3 — held back | 12 | 0, and none expected |

Tier 2 is complete: `facility-risk-index`, `refusal-false-positive-log`,
`instance-log-index`, `sleep-duration-instrument`,
`idle-shutdown-restart-accounting`, `recent-work`, `work-load-ordering` — all
seven named in the manifest, all seven stored.

Tier 1, landed: `criterion-symmetry`, `rosetta-shape-core`,
`force-expression-model`, `alignment-under-coupling`,
`diversity-collapse-model`, `emergence-stability-simulator`,
`fairmont-ecological-recovery`, `food-grain-monitor`,
`semantic-drift-sim`, `geometric-manifold`, `adversarial-prior`,
`constraint-assembly`, `closure-cost`, `buffer-counted-as-supply`,
`cross-model-calibration-toolkit`, `energy-english`, `earth-systems-physics`,
`operator-kit`, `voice-cloud-orchestrator`, `coupled-decoupled-verification`. Filed as tier 1 by elimination — each was exported,
so none is tier 3, and none is in the manifest's tier-2 table. The manifest
does not label files individually, so tier is inferred here and not carried in
the files.

Tier 3 is held back by the manifest's own decision. Its absence is a choice
recorded upstream, not a gap here.

## Cross-refs that do not resolve

The twenty-seven files carry 34 links across 24 distinct names. Ten resolve to
stored files, including the mutual pair `energy-english` ↔
`voice-cloud-orchestrator`. Fourteen do not resolve inside the folder, but "not in the folder" is not the same as "does not exist",
and three kinds sit under that heading.

**Resolves elsewhere in this repo, under the underscore convention.**

- `info-taxonomy` → `fragility-cascade/info_taxonomy.py`, a generalized
  taxonomy of information types, ways of obtaining, and ways of knowing —
  which is what `rosetta-shape-core` links it for.
- `rubric-backcasting` → `instrument-bias-sims/s3_rubric_backcast.py`.

**Resolves as a repository.** `thermodynamic-accountability-framework` is
`github.com/JinnZ2/thermodynamic-accountability-framework`, cited from
`earth_economics/` inside this repo. `geometric-to-binary-bridge` resolves
under a near-name: `META_INDEX.md` lists `github.com/JinnZ2/geometric-to-binary`
and `JinnZ2/CLAUDE.md` calls it Geometric-to-Binary-Computational-Bridge, so one
artifact carries three name variants and the link matches none exactly.

**Not found anywhere yet** — which is not the same as absent, and the heading
used to say "genuinely absent" until `voice-cloud-orchestrator` was filed under
it and arrived in the next batch. With 37 tier-1 files still outstanding, this
list is a delivery state, not a finding: `merit-anchoring`,
`unnamed-instruments`, `question-availability`, `report-typing`,
`median-case-calibration`, `identity-model-monoculture` — zero hits under
either naming convention. (`emotions-as-sensors` is not absent: it is the
Emotions-as-Sensors repository, carried in `JinnZ2`.)

`tool-off-metrology` is the one name that has held this position across many
batches at high citation count, so it is the only one worth treating as a real
gap rather than a pending delivery — which is also what
`uninstrumented/CLAIM_TABLE.md` concluded independently. `tool-off-metrology` is absent too, at 15
citations, matching `uninstrumented/CLAIM_TABLE.md` `UNI_043`/`UNI_066`.
`shape-index` is the interesting one: `predicate-difference/shape_index.py`
exists and states in its own header that *no shape-index format exists in this
repository* — a file named for the absent object, inferring the format because
it is missing, and flagging the inference. So the cited object is absent and
the repo says so itself.

**One file matches repo content under a different name.**
`earth-systems-physics` gives as its core equation
`corruption(trend) = corruption(measurement) × corruption(framework)`, which is
the L7 headline of `thermal-sensor-degradation-audit/` in this repo — where it
has spread to `extraction-blindness-sim/`, `model-ecology/`,
`instrument-epistemology/` and `derivation-discarded/`. Nothing in either name
points at the other. The file is *also* a repository,
`github.com/JinnZ2/earth-systems-physics`, cited from `earth_economics/` here
as the physical engine. So one memory file resolves two ways at once, by name
to a repo and by content to a folder, and neither route finds the other.

**`energy-english` closes a reference the repo had already flagged as broken.**
`uninstrumented/CLAIM_TABLE.md` `UNI_104` records it as a failing cross-link —
hyphenated where the repo writes `energy_english` — and `UNI_134` counts it as
another instance of the same hyphenation defect. The memory file now supplies
the referent: a constraint grammar with a live layer-1 gate and four rules that
each name a place where a representation adds information the source did not
contain. The repo's audit was right that the link failed and had no way to see
what it pointed at.

(Two earlier corrections to this section stand, and a third is added.
An earlier version said the export's references split by kind — `[[...]]` for
the memory namespace, plain names for repositories — which broke at
`geometric-manifold`. And this audit twice recorded `shape-index` as "cited
from both sides and existing on neither" while a file of that name was in the
tree; the substance survives, the search did not. The inventory now checks
hyphen and underscore forms. Three first-pass searches in this folder's history
have been too narrow, all three found by widening rather than by reading.)

**The namespace is shared, not parallel.** `uninstrumented/cases/` and
`nonidentity-census/` emit `[[...]]` links into the same namespace these memory
files use, and `tool-off-metrology` is cited from both sides — recorded at
`UNI_043`/`UNI_066` as the most-cited absent object in the repo, and cited by
`recent-work` from the memory side as where a micro-skill-decay position was
carried. Four documents, two sides, no file, under either naming convention.

**Repo names resolve too.** `rosetta-shape-core` names five sibling
repositories — Polyhedral-Intelligence, Emotions-as-Sensors,
Symbolic-Defense-Protocol, AI-Human-Audit-Protocol, BioGrid 2.0 — and all five
are carried in the `JinnZ2` ecosystem repo. Nothing was rewritten either way.

The memory namespace overlaps published artifacts three ways, all by name:
a folder in this repo (`emergence-stability-simulator`, and probably
`uninstrumented`), and a separate public repository under the same account —
`fairmont-ecological-recovery`, listed in `JinnZ2/META_INDEX.md` at
`github.com/JinnZ2/fairmont-ecological-recovery`.

That last one is worth marking against the manifest. `SCRUB_RULES.md` says
location below "cold-climate continental" was removed categorically from every
exported file, and this file's own name carries a place. It is not a scrub
miss: the name is already published by the author under that account, and the
file says "Published CC0" itself. But the categorical statement has at least
one standing exception, and a later reader should not take it at face value.
Nothing was renamed.

Named artifacts, same class one level up: `criterion-symmetry` closes on
"MARKER.md and SCAN_SPEC.md written", and `diversity-collapse-model` reports a
CLAIM_TABLE carrying C1–C10. None of the three is in the folder, and no file of
those names exists anywhere in this tree. Recorded, not sought.

**One named artifact does resolve, and it lands where the repo index does not
point.** `semantic-drift-sim` names `valence_drift_test.py` and
`semantic_drift_test.py`; both are in `fragility-cascade/`. The unknowns
register is real — five entries, U1–U5 — and the two the memory file promotes
to immediate measurement priorities are U1 (screening functional form) and U4
(screening electrons catalytic or consumable), matching verbatim. The memory
file selects two of five rather than summarizing the register, and does not
carry U3, which reads "NO MEASUREMENT EXISTS".

Neither `.py` is listed in `CLAUDE.md` or `docs/FOLDER_NOTES.md`, though
`fragility-cascade/` itself is described in both. So on this one file the
export points at repo content the repo's own index does not reach.

**Two files summarize folders in this repo, and both check out when run.**
`constraint-assembly` reports "`assemble.py` (18/18)" and
`constraint-assembly/assemble.py --selftest` returns 18/18; its grade-stop case
carries 4 components and 4 grounded rejections, as stated, under the key
`rejected`. `closure-cost` reports "`closure.py` (15/15)" and the selftest
returns 15/15; its "zero quantified" claim holds across all three cases, every
`diagnostic_spend` null and every `knowledge_state` `not_separable`. The only
drift is a case name — the file says `missile-alert`, the repo says
`hawaii-missile-alert`.

That makes four memory files now named for repo folders:
`emergence-stability-simulator`, `constraint-assembly`, `closure-cost`, and
probably `uninstrumented`.

**`adversarial-prior` is the largest instance of the same thing.** Its sections
map onto four of the nine sims in `instrument-bias-sims/`, and two were checked
against the code rather than matched by name: `s1_encounter_denominator.py`
opens on event-sampled observation in a system that is ">95% null time", which
is the file's encounter-denominator argument; `s4_antler_calibration.py` carries
`rank_prospect` as a two-arm input, a doe-choice arm, and a `PRE_PATCH_OMISSION`
record stating the earlier version had no doe in it at all — which is the file's
doe-choice section and its discriminator. `s3_rubric_backcast.py` and
`s5_adversarial_prior.py` match the file's own name and its one dangling
memory-side link.

One result arrives split across two files. `recent-work` gives the spinodal
threshold as h\* ≈ 0.385 and says the apex-broadcast multiplier crosses it;
`diversity-collapse-model` says *only* that multiplier crosses h\*, and gives no
value. Each carries what the other omits, and both report hysteresis confirmed.
Noted, not merged.

**A memory file can be a summary of a repo folder under the same name.**
`emergence-stability-simulator` is one, and it checks out against
`Simulators/emergence-stability-simulator/`: all 18 ids EMRG_001–018 are
present in the folder; `samples/CLAIM_TABLE.sample.json` carries 22 claims of
which 14 are confirmed-family and 3 refuted, matching "several confirmed and
several refuted"; and the tool-vs-identity framing is there as
"Substrate using narrative as a tool" — in `sim_engine.py`, not in the docs.
The one item not located in that folder is the maxim as worded, "update the
claim, never modify the simulation" — the folder practices it (refuted claims
carry a `refutation_basis` and stay refuted) and states it in those words
elsewhere in the tree, not here.

That makes `[[uninstrumented]]` more likely to denote a memory file summarizing
`Simulators/uninstrumented/` than to denote the folder — but likely is not
established, and one same-name case is n=1. Still not repointed.

## The cost, visible in the files

`SCRUB_RULES.md` names three files that pay most for the scrub. All three have
landed, and the cost is legible in each:

- `facility-risk-index` heads its longest section "Field observation
  (longitudinal operator report)" with no observer attached.
- `refusal-false-positive-log` reports a rate with, in its own words, no
  denominator available to the observer.
- `recent-work` carries the micro-skill cases as unrelated actors — an
  auto-mechanics instructor, drill users, carpenters — where the manifest says
  the relations were lifted.

The reasoning is intact; the standing behind it is not carried. That was the
trade taken deliberately, and re-attaching the names is not a repair.

CC0.
