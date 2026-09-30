# INVENTORY.md — potential/, WORK ORDER 2026-09-29 (land, repair, organize)

STEP 0 record, then the RETURN. Every count below was produced by
running; where a count is quoted from a document it says CARRIED.

```
STATUS KEY   OBSERVED  executed or read here, result in hand
             DERIVED   inferred from code/text, not run
             CARRIED   quoted from an upload or the order, not recomputed here
SOURCE KEY   [RPT]  briefs/REPORT.txt  [C29] the order's own pass  [C29b] this pass
```

## 0.1 — the tree as found (main @ 5b727ca), and as left

```
path                                     bytes  imported-by                        selftest  test file      CC0 hdr
potential/README.md                       7017  -                                  -         -              yes (text)
potential/CLAIM_TABLE.md                  6033  -                                  -         -              no
potential/traformation.py  (-> P-03)      3148  ledger, perturbation, test_all,    no        test_all.py    no
                                                test_perturbation
potential/ledger.py                       3300  test_all, test_perturbation        no        test_all.py    no
potential/baseline.py                     4034  test_all                           no        test_all.py    no
potential/perturbation.py                 9122  perturb_cli, test_perturbation     no        test_perturb.  no
potential/perturb_cli.py                  1565  -                                  no        -              no
potential/test_all.py                     6506  -                                  (is one)  -              no
potential/test_perturbation.py            8195  -                                  (is one)  -              no
potential/gate/README.md                  5795  -                                  -         -              yes (text)
potential/gate/graph.py                   3944  cut, domains, projections, cli     no        test_gate.py   no
potential/gate/cut.py                     4692  projections, test_gate             no        test_gate.py   no
potential/gate/domains.py                 9449  gate_cli, test_gate                no        test_gate.py   no
potential/gate/projections.py             2967  gate_cli, test_gate                no        test_gate.py   no
potential/gate/gate_cli.py                1757  -                                  no        -              no
potential/gate/test_gate.py               6619  -                                  (is one)  -              no
potential/tools/registry.py               9524  registry_sourced, check_drift      no        (drift check)  no
potential/tools/registry_sourced.py      11762  -                                  yes       -              no
potential/tools/check_registry_drift.py   5952  -                                  yes       -              no
```

CC0: no `.py` in the folder carries a license header; both READMEs state
CC0 in prose and the repo's root LICENSE is CC0. Recorded, not changed
(the order says land verbatim and name defects; a header pass is not a
named defect).

Added by this order (all under `potential/`):

```
briefs/REPORT.txt                          verbatim   sha256 7219397b…cc13c
briefs/RESEARCH_BRIEF.txt                  verbatim   sha256 5b595dbe…51a78
briefs/DISSENTER_CHANNEL_BRIEF.txt         verbatim   sha256 e2379760…9abd
matrix/FUNCTIONALITY_MATRIX_COMPLETE.txt   verbatim   sha256 bb835f6f…e2e7
matrix/FOOTING_MERGED.txt                  verbatim   sha256 1eed9bc4…09a59   (lineage step 5)
matrix/check_attested_provenance.py        new        P-16 check, --selftest
matrix/check_attested_provenance.sample.txt new       its output on the landed matrix
gate/test_domains.py                       new        P-11 / P-12 checks on shipped domains.py
INVENTORY.md                               new        this file
```

Not created: `ratio/`. `ratio_model.py` did not arrive, and a folder
holding nothing is a placeholder that reads as a delivery.

## 0.2 — every path the order named, resolved against the real tree

```
order path                          resolution
gate/domains.py                     PRESENT   potential/gate/domains.py
gate/test_gate.py                   PRESENT   potential/gate/test_gate.py
gate/README*                        PRESENT   potential/gate/README.md
tools/registry.py                   PRESENT   potential/tools/registry.py  -- NOT repo-root tools/;
                                              there is no tools/registry.py at the root.
                                              check_registry_drift.py was written as if it lived at
                                              the root (resolved ROOT/potential/transformation.py,
                                              which from potential/tools/ is
                                              potential/potential/transformation.py). See P-05.
traformation.py                     PRESENT   -> MOVED(to) potential/transformation.py by P-03
transformation.py                   ABSENT    at start (never existed in any commit: git log --all)
                                    PRESENT   after P-03
CLAIM_TABLE.md                      PRESENT   potential/CLAIM_TABLE.md
ANIMAL_ANALOGUE_BRIEF.txt           ABSENT    whole tree (git ls-files), and not in the uploads
wb_gates_scatter.png                ABSENT    whole tree, and not in the uploads
FUNCTIONALITY_MATRIX.txt            ABSENT    whole tree (lineage step 1; not uploaded)
FUNCTIONALITY_MATRIX_MARKED.txt     ABSENT    whole tree (lineage step 3; not uploaded)
FOOTING_MERGED.txt                  ABSENT    at start -> PRESENT potential/matrix/FOOTING_MERGED.txt
```

Uploads the order's STEP 1 names, against the upload directory:

```
REPORT.txt                          delivered   landed briefs/
RESEARCH_BRIEF.txt                  delivered   landed briefs/
ENGINEERING_BRIEF.txt               NOT DELIVERED  (and _2: the byte-identical twin the order
                                                    logs -- neither arrived, so the dup could not
                                                    be confirmed here)
CONTINUITY_BRIEF.txt                NOT DELIVERED
DISSENTER_CHANNEL_BRIEF.txt         delivered   landed briefs/
FUNCTIONALITY_MATRIX_COMPLETE.txt   delivered   landed matrix/
domains_gated.py                    NOT DELIVERED  -> P-11, P-13 not reproducible here
ratio_model.py                      NOT DELIVERED  -> P-06..P-10 not reproducible here
FOOTING_MERGED.txt                  delivered (named in 0.2, not in the STEP 1 table)  landed matrix/
```

Five of nine named uploads arrived. Nothing absent was reconstructed
(`category-weld/` CW_004: the one prior reconstruction in this tree
produced a finding that was an artifact of the reconstruction).

## 0.3 — baseline, before and after

```
check                                            before                       after
python3 tools/known_answer.py                    43 registered / 48 expected  45 / 50   SHORT both times
                                                 41 exercised                 43
                                                 cases PASS 164 FAIL 8        PASS 172 FAIL 8
                                                 disagreeing: 0               0
                                                 exit 1                       exit 1
python3 -m unittest discover tests               133 run, 8 FAIL              133 run, 8 FAIL (same 8)
python3 -m unittest discover -s grounding-layers 215 run, 18 ERROR            215 run, 18 ERROR
python3 tools/check_gate_drift.py                CLEAN                        CLEAN
```

**The baseline is red for reasons outside potential/, and none of the
eight is in KNOWN_RED.md.** The order says stop and report on that
condition. The reason for proceeding, stated rather than assumed: the
eight failures are four in `tests/test_known_answer_gate.py` (five
`_tra_sle_to_sv` registrations in `thwaites-risk-audit` that `seed()`
cannot reach; five metrics in `EXPECTED_METRICS` never registered; the
tool exits 1) and four in `tests/test_run_manifest.py` (the argparse
selftest form and a redirect target, KNOWN_RED §10's subject); the 18
grounding-layers errors are the import failures CLAUDE.md already
records as "not green". None of these touches a path this order
changes, and the failing SET is identical before and after, which is
the check that the potential/ work moved none of them. The eight
unrecorded failures are the interesting rows for whoever updates
KNOWN_RED.md next; this order did not.

The eight known-answer FAILs are the same 8 before and after: two
PINNED RED by design (AGENTS.md §3) plus six on metrics outside this
folder; "disagreeing with the registry: 0" in both runs.

Tests the two discovers do NOT reach, and their state:

```
potential/test_all.py                          before: ImportError (P-03)   after: 44 checks PASS
potential/test_perturbation.py                 before: ImportError (P-03)   after: RED, P-17 (new, listed)
potential/gate/test_gate.py                    before: FAIL kappa=1000000001 (P-01)   after: 53 checks PASS
potential/gate/test_domains.py                 (new)                        6 checks PASS
potential/tools/check_registry_drift.py --selftest  before: 11 PASS with the real-tree arm SKIPPED
                                               after: 15 PASS; with transformation.py removed: exit 1
potential/tools/check_registry_drift.py        before: "missing: .../potential/potential/transformation.py" exit 2
                                               after: "no drift" exit 0; missing file -> exit 3
potential/tools/registry_sourced.py --selftest before: SyntaxError at import of registry.py (P-04)
                                               after: RED, P-18 (new, listed)
potential/matrix/check_attested_provenance.py --selftest  (new)   16 checks PASS
```

## 0.4 — claim ids

Highest existing id in `CLAIM_TABLE.md`: POT_020. POT_021..023 were
free; the uploads' suggested labels land on them. The ratio row and the
World Bank row take POT_024 and POT_025.

---

# RETURN

## Defects P-01..P-16, plus two found by running

```
id    status         what was done / why not
----  -------------  ----------------------------------------------------------------
P-01  FIXED          REPRODUCED first: test_gate.py failed at
                     test_token_not_cut_when_bypass_exists with kappa = 1000000001.
                     _split_nodes gave the direct s->t edge capacity 10**9; it now
                     gets 1 (a direct edge is exactly one path). The failing test is
                     kept as the pin; test_direct_edge_counts_as_one_path adds the
                     lone-direct-edge case and records a limit: two direct channels
                     between one pair collapse to one adjacency edge in _adj.
                     Registered: potential/gate/cut.py::vertex_connectivity in
                     tools/known_answer.py, 'token bypass (P-01 pin)' among 5 cases.
P-02  FIXED          REPRODUCED: README water table vs gate_cli project water
                     disagreed on all / physical / practical (3 of 5). The block is
                     now REGENERATED from projections.render and PINNED by
                     test_readme_water_table_matches_render (shown to fire on a
                     hand-edited number, then restored). No number hand-typed.
P-03  FIXED          git mv traformation.py transformation.py. Importers: ledger,
                     perturbation, test_all, test_perturbation, check_registry_drift.
                     All run; test_perturbation.py then fails for its own reason (P-17).
P-04  FIXED (note)   REPRODUCED and WORSE than reported: registry.py did not import
                     at all -- `"DELETE "",` is an unterminated string literal, a
                     SyntaxError, not a trailing space. "Restore from last clean
                     commit" has no target: registry.py has one commit (79d40b2) and
                     the corruption is in it. Repaired to transformation.py's
                     declared tuples, which is the authority check_registry_drift
                     compares against, plus the stray `",` in the docstring.
                     check_registry_drift now proves the two agree.
P-05  FIXED          REPRODUCED: real-tree arm skipped (file absent). Now a missing
                     file is a hard FAIL naming the path (exit 1; shown by removing
                     transformation.py and running). Also fixed the path itself --
                     the tool resolved potential/potential/transformation.py because
                     it was written for repo-root tools/ and lives in potential/tools/.
                     run() returns 3 on a missing file (EXIT_CONTRACT: could not run).
P-06  OPEN           ratio_model.py NOT DELIVERED. Carried as POT_024 ASSUMED_RESTATED.
P-07  OPEN           same file. The measurand-meld reading is recorded in POT_024's
                     scope note; the split tuple is not built for a file not here.
P-08  OPEN           same file.
P-09  OPEN           same file; RESEARCH_BRIEF §4 lands verbatim, its "division by
                     zero" sentence unedited, the [ASSUMED] reading in POT_024's note.
P-10  OPEN           same file.
P-11  PARTLY REPRODUCED  domains_gated.py NOT DELIVERED, so the 19-vs-17 count is
                     not recomputable. The mechanism IS reproduced on shipped
                     domains.py: node_collisions() = {ROUGH: shelter+sleep,
                     SHELTER_SYS: shelter+sleep}; a union graph over raw names has
                     kappa 18 against 20 namespaced (gate/test_domains.py). Whether
                     the brief's union was namespaced: NOT KNOWN from here.
P-12  PARTLY REPRODUCED  domains.py half: identity's only token-free first hop is
                     CASH_INFORMAL (pinned). Whether cash is a bearer token is a
                     schema declaration the graph does not carry; not declared here,
                     since declaring it changes an authored reading. Scope note on
                     POT_021.
P-13  OPEN           domains_gated.py NOT DELIVERED. Carried as a scope note on POT_021.
P-14  FIXED (as a row)  ENGINEERING brief NOT DELIVERED; the same-availability row is
                     computed in POT_023's scope note: (1e-3)^8 = 1e-24 vs 1e-3.
P-15  FIXED (as status)  No data, script, or png anywhere in the tree. POT_025
                     NOT_REPRODUCIBLE_FROM_REPO.
P-16  FIXED (as a check)  matrix/check_attested_provenance.py: 16 [A] cells,
                     0 carry the standing note, 0 carry a date, 16 NEITHER.
                     Count and line numbers; no cell rewritten. Word-list limit
                     stated in the module. Registered in tools/known_answer.py
                     (None on no [A] cell, never 0).
P-17  NEW, OPEN      test_perturbation.py: test_verdict_supported_synthetic reads
                     the module-level PERTURBATIONS at line 102 and re-imports it at
                     line 105 inside the same function, which makes the name local
                     and raises UnboundLocalError at 102. Masked by P-03 until now.
                     Not named by the order: listed, not repaired.
P-18  NEW, OPEN      registry_sourced.py --selftest asserts
                     report.verified != report.unverified on a fixture that yields 1
                     and 1, so the selftest fails on its own fixture. Masked by P-04
                     (registry.py would not import) until now. Not named by the
                     order: listed, not repaired.
```

## Claim ids assigned

POT_021 (gate tags, HYPOTHESIZED), POT_022 (substrate-independence,
HYPOTHESIZED), POT_023 (defended cut vertex, STRUCTURAL), POT_024
(ratio, ASSUMED_RESTATED), POT_025 (World Bank sketch,
NOT_REPRODUCIBLE_FROM_REPO). Every row carries a falsifier.

## In the tree, not named by the order — listed, not acted on

- `potential/tools/registry_sourced.py` (11.7 KB): not in the order's
  0.2 list. Carries P-18. Its docstring names `tools/sourced.py` at the
  repo root as the primitive it should delegate to and does not import it.
- `gate/README.md` said `cut_vertices` raises for κ=0; the code returns
  `(0, set())` and always has. One sentence corrected to the code while
  the water block was regenerated (same file, same reason: prose said one
  thing and the code another). The prose "two physical channels that do
  not require a token" is still true and was left.
- `potential/` has no entry in the root `CLAUDE.md`, `README.md` or
  `CATALOGUE.md`. Not added.
- `tools/known_answer.py` reports two metrics "registered and never
  exercised" and five "expected and NOT registered", all outside this
  folder, all pre-existing (identical before/after).
- No `.py` under `potential/` carries a CC0 header.

## Cross-repo refs

`briefs/DISSENTER_CHANNEL_BRIEF.txt` §3's `baseline.py` /
`VERDICT_IN_PLACE_OF_READING` resolves IN-TREE to
`potential/baseline.py`; the order asked for it to be marked EXTERNAL,
and it is not external. Recorded in README.md.

## Verification method for citations

None fetched. Every literature reference in the briefs, the matrix, and
the order's own STEP 3 is CARRIED. This environment's egress is an
allowlist that refuses publisher hosts; nothing was looked up.
