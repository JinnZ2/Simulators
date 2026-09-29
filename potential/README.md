# potential/

Instruments around one question: **how many disjoint paths does a
compulsory requirement have to its satisfaction, and what happens to the
count when a single vertex — a token, a credential, a seat — is
removed.** Five layers, each promotable on its own. Nothing here is a
claim about any model, session, party, or population; every domain
graph, every matrix cell, and every ratio input is an authored reading,
and the claim table says which.

POSTURE (repo standard): the audience is working people, not
institutions; the instruments sit on the risk-mitigation side — they
report where a single removal disconnects a requirement, and they do
not recommend removing or adding anything.

## What these are, and are not (operator's section, folded in 2026-09-29)

```
WHAT THESE ARE
Instruments. Each one takes something you bring and
returns a reading, with its scope stated.

WHAT THEY DO NOT DO
They do not return a decision, a recommendation, or a
verdict. Absence of a prescription is not an incomplete
tool — it is the tool working as specified.

A reading that comes back empty is a result. "Nothing
found under this vocabulary" is information about where
the boundary sits, not a failed run.

WHY
What the reading is for depends on who picked it up and
what they are doing. A prescription fits the instrument
to one use and hides that narrowing.
```

The null line above is what `check_attested_provenance.py` returns
`None` for, what `test_domains.py`'s empty collision set means, and why
`gate/` reports κ per θ and stops.

## Layers

| layer      | what it is                                                                 | state |
|------------|----------------------------------------------------------------------------|-------|
| `gate/`    | connectivity instrument: domains as graphs, κ and cut vertices per admissibility (`graph.py`, `cut.py`, `domains.py`, `projections.py`, `gate_cli.py`); `domains_gated.py` — the gate-tagged schema — was named by the 2026-09-29 order and **did not arrive** | built; gated schema ABSENT |
| `ratio/`   | effort / capability schema, every input `[ASSUMED]` (`ratio_model.py`)     | ABSENT — named, not delivered; no folder created for a file that is not here |
| `matrix/`  | the functionality matrix, its lineage (`FOOTING_MERGED.txt`), and the mechanical `[A]` provenance check | landed verbatim + one check |
| `briefs/`  | verification briefs, verbatim, dated (REPORT, RESEARCH, DISSENTER_CHANNEL); ENGINEERING and CONTINUITY named and **not delivered** | 3 of 5 landed |
| `tools/`   | the cross-folder registry, its sourced variant, and the vocabulary drift check | built; two open defects (P-18, see `INVENTORY.md`) |
| (root)     | the transformation instrument: mechanisms × shape-pairs, ledger, baseline signatures, attractor test | built; one open defect (P-17) |

Reading order: `matrix/` → `gate/` → `ratio/` (absent; read the ratio
row of `CLAIM_TABLE.md` instead) → `briefs/`.

`INVENTORY.md` is the 2026-09-29 order's STEP 0 record and its RETURN:
every file, every path the order named resolved against the tree,
baseline suite counts, and the defect ledger P-01..P-18 with what was
reproduced, repaired, or left open and why.

## Flow, in one picture

```
   requirement (NEED)
        |
        |  channels: kinds ⊆ {physical, legal, practical}, token flag
        v
   [ G_θ ]  ── project by admissibility θ ──>  κ(θ), cut set(θ)
        |                                          |
        |   κ = 1 and __TOKEN__ in cut set         |  no composite across θ
        v                                          v
   the token is a cut vertex UNDER θ     each θ is one reading, side by side
                                                   |
   matrix/  what the token layer is FOR (F1..F9), every cell tagged with
            who it constrains ([F]/[P]/[A]/[H]/[J]/[U])
   briefs/  what was verified, to what level, and what was not
   ratio/   what the hours cost when the gate converts production hours
            into token-seeking hours (schema only; inputs assumed)
```

The bottleneck the whole folder is built around is the one vertex every
requirement network routes through. The instrument computes whether it
is a cut vertex under a declared θ and stops there.

## KEY-HOLDER declaration

The expected values in `gate/test_gate.py`, `gate/test_domains.py`,
`matrix/check_attested_provenance.py --selftest`, and the two
registrations in `tools/known_answer.py` were written by the same agent
that wrote or read the code. They are REGRESSION pins — a change turns
them red — and not validation. The one exception is the P-01 pin,
`token bypass`, whose expected value (κ = 2) is graph theory and whose
shipped value (1,000,000,001) was a failing test nobody outside the
folder had run.

## Open conversions (from `matrix/FUNCTIONALITY_MATRIX_COMPLETE.txt`)

Each is a study design, not a metaphor. None is run here.

- **C1** Workaround-count diary study on the six ease seats
  (workarounds per compulsory input per day; instrument validated in
  Portfolios of the Poor 2009 and the US Financial Diaries) → ease table
  `[A]/[J]` → `[F]`.
- **C2** Constraint-survival test on housing and food scarcity (does
  the scarcity survive removal of the gate: vacancy vs homelessness,
  waste vs hunger) → F1 manufactured-vs-genuine `[J]` → `[F]`.
- **C3** Informative-price threshold defined and measured → F5 `[U]`
  resolved.
- **C4** Exit-cost threshold defined and measured → F8 `[U]` resolved.
- **C5** Tail test: can public or cooperative forms provision the
  concentrated-capability tail at population scale without the
  per-person gate → F4 per-se claim settled.
- **C6** The invention-endpoint study: a guaranteed-availability arm
  with creative-output instruments, not employment and well-being alone
  (`briefs/RESEARCH_BRIEF.txt` §5) → the still-open causal question.

## Cross-references, DECLARED and not imported

- `briefs/DISSENTER_CHANNEL_BRIEF.txt` §3 cites `baseline.py` and the
  signature `VERDICT_IN_PLACE_OF_READING` from "the repo this whole
  series began with". The order asked for this to be marked EXTERNAL;
  it resolves IN-TREE: `potential/baseline.py` declares that signature.
  The same section cites `domains.py`, which is `potential/gate/domains.py`.
  Vehrencamp, HOT (Carlson & Doyle), Buldyrev et al. and Brummitt et
  al. are literature, CARRIED, opened by nobody here (egress allowlist).
- `matrix/FOOTING_MERGED.txt` cites Portfolios of the Poor (Collins et
  al. 2009) and the US Financial Diaries (Morduch & Schneider) — CARRIED.
- `briefs/RESEARCH_BRIEF.txt` cites Mani et al. 2013, Bloom et al. 2020,
  Fort et al. 2025, Egger et al. 2022, Banerjee et al., Stockton SEED,
  Finland 2017-18 — CARRIED at the brief's own stated level. Its §3
  World Bank sketch is NOT_REPRODUCIBLE_FROM_REPO (POT_025).
- `tools/registry_sourced.py` names `tools/sourced.py` at the repo root
  as the primitive it should delegate to. It does not yet import it.

## How to run

    cd potential
    python3 test_all.py                              # root instrument
    python3 test_perturbation.py                     # RED: P-17, recorded, not repaired
    python3 gate/test_gate.py                        # gate, incl. P-01 and P-02 pins
    python3 gate/test_domains.py                     # node collisions, union κ, identity
    python3 tools/check_registry_drift.py --selftest # vocab drift; hard-fails on a missing file
    python3 tools/registry_sourced.py --selftest     # RED: P-18, recorded, not repaired
    python3 matrix/check_attested_provenance.py matrix/FUNCTIONALITY_MATRIX_COMPLETE.txt
    python3 ../tools/known_answer.py                 # the two potential/ metrics are in the gate

Every check prints its own count; no count is stored in this file.

---

## The transformation instrument (root modules)

Instruments for detecting structural transformations between a source
text and a response, and for testing whether a set of such
transformations is a stable shape rather than a set of unrelated moves.

**Not a benchmark. Not a classifier. Not a verdict.** Every entry
carries a reader and a reason. A hit without either is refused. The
folder produces readings, and what to do with them is the reader's.

### The unit

A transformation entry is a triple:

    ( mechanism , source_type , target_type )

- **mechanism** — what happened to a structure. Ten, declared in
  `transformation.py`: DELETE, MERGE, GENERALIZE, SUBSTITUTE, RESOLVE,
  TERMINATE, VALENCE_SHIFT, COMPLETE, RANK, BINARY.
- **source_type / target_type** — the direction of the move, from one
  of eight shape-pairs: unresolved→familiar, recursive→terminal,
  scoped→universal, plural→singular, structural→social,
  neutral→evaluative, unfinished→polished, distinct→merged.

The mechanism alone is not the finding. `SUBSTITUTE` applied to
`unresolved→familiar` and `SUBSTITUTE` applied to `structural→social`
are two different operations on the same name, and collapsing them
loses the distinction. Ten mechanisms × eight directions = eighty
cells.

### What ships

- `transformation.py` — mechanisms, shape-pairs, the `Entry` record.
- `ledger.py` — records entries, computes distributions, **refuses a
  composite**. An AST check on its own source asserts that no
  arithmetic expression combines a mechanism count with a direction
  count.
- `baseline.py` — five baseline signatures, each with a stated gloss, a
  `Hit` record that refuses a hit without a reader and a reason, and a
  word-list scanner that produces **candidates** and states its own
  limit: a word list is a first pass, not a classifier.
- `perturbation.py` — the attractor test. Generates eight perturbations
  by rule (one per shape-pair, each inviting the input's structure to
  be preserved), computes total-variation similarity between a signal
  vector and a baseline, builds a null by shuffling direction labels,
  and returns SUPPORTED / NOT_SUPPORTED / UNDETERMINED.
- `perturb_cli.py` — `render` writes the eight perturbations to a
  directory; `score` reads a baseline and a directory of signal vectors
  and prints the verdict.
- `test_all.py` and `test_perturbation.py` — known-answer suites.

Stdlib only. Parses under 3.9. Phone-buildable. No network. **No model
is called anywhere in the folder.**

### The baseline signatures

Five, from `baseline.py`:

- `CLOSURE_BEFORE_CHAIN` — the output terminates before naming every
  dependency in the input's chain.
- `MECHANISM_WORD_NO_ACCESS` — a mechanism is asserted for a state whose
  mechanism is not available to the reader.
- `UNIFORM_RULE_ACROSS_SCOPE` — a rule declared for one scope is
  applied to a scope where it was not declared.
- `VERDICT_IN_PLACE_OF_READING` — a judgment appears where a reading was
  called for.
- `POLISHED_SURFACE_ON_UNFINISHED` — a closed form is presented where
  the input carried an explicit unknown.

A signature is not "an error." It is a property of the pair
`(input, output)` that indicates the output moved toward the reference
shape. **A factually correct answer can carry a signature.** That
separation is the reason the folder exists — otherwise every discussion
of the failure mode turns into a discussion of whether the answer was
right.

### The attractor test

The claim the test is designed to check:

> Structurally different inputs repeatedly produce transformation
> vectors that are more similar to each other than to chance.

The tool does not run a model. It generates the perturbations, loads
the recorded vectors, computes similarity against the baseline, builds
the null by shuffling direction labels, and returns a verdict.

`UNDETERMINED` fires in two cases, and both are the point:

- fewer than eight perturbation vectors loaded
- a null that is not separable from the signal

A result on a small sample is not an attractor finding. The refusal is
mechanical, not a judgment call by the reader.

### What the folder refuses

- **No composite.** `Ledger.composite()` raises. There is no single
  number for "how bad" an output is.
- **No hit without a reader and a reason.** `Hit.__post_init__` raises
  on either being empty.
- **No candidate treated as a classification.** The scanner returns
  suggested signatures with offsets. A signature is attached by a
  reader, not inferred from text.
- **No empty vector scored as zero.** `tv_distance` on an empty vector
  returns `None`, not `0.0`. The absent-vs-known-negative repair, at
  the field that decides the verdict.
- **No verdict without a stated reason.** Every `verdict()` return
  carries a `reason` string that names what was measured.

### Stated limits

- The scanner is a word list. Paraphrase steps around it. An empty
  result is not evidence that a signature is absent from a pair.
- The perturbation set is one per shape-pair. The test checks that
  vectors exist for each name; it does **not** check that a signal's
  dominant direction matches the perturbation's pair. Attaching a
  `pair_hint` field and checking against it is the extension the
  folder leaves open.
- The attractor claim is testable, not established. Running the tool
  produces a number; whether that number describes the model or the
  task is a question the tool cannot answer.
- Every entry is a reading. Two readers may attach different mechanisms
  to the same span. The ledger stores both; nothing merges them.

### How to run

    # record entries (any producer)
    python3 -c "
    from transformation import Entry
    from ledger import Ledger
    L = Ledger()
    L.add(Entry('SUBSTITUTE', 'unresolved', 'familiar',
                reader='audit', date='2026-09-28'))
    L.save('ledger.jsonl')
    print(L.render())
    "

    # render perturbations against a source
    python3 perturb_cli.py render input.txt prompts/

    # score a recorded set against a baseline vector
    python3 perturb_cli.py score baseline.json signals/

    # suites
    python3 test_all.py
    python3 test_perturbation.py

### Build order

`transformation.py` → `ledger.py` → `baseline.py` → `perturbation.py`
→ `perturb_cli.py` → `test_perturbation.py`.

Each imports only what is above it. Nothing imports the CLI.

### What this folder is not

- Not a claim about any model. Every vector is data recorded by a
  reader; the tool computes over what it is given.
- Not a replacement for the repo's existing instruments.
  `effective-redundancy-audit`, `reasoning-gate`, `null-harness`,
  `divergence-playground` and `domain-ledger` each measure something
  this folder does not, and the no-composite rule and the per-reader
  category layer are theirs.
- Not an answer to "is this model good." The folder does not carry a
  verdict vocabulary for a model, a session, or a party.

The section above is the folder's original README, retained; the layer table at the top of this file is what was added on 2026-09-29. CC0. Stdlib only. Parses under 3.9. Phone-buildable.
