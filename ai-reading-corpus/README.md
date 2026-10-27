# scope-habitat-corpus

CC0. A machine-readable bundle built from two upload rounds: 11 uploads (2026-10-27, habitat +
scope-audit lines) and 11 uploads plus a pasted study summary and session transcript (2026-10-28,
all-optical switching line). Duplicates collapsed, versions ordered, claims split into atoms,
every stated number recomputed where it can be done offline.

This is written for AI readers. Read this file, then `ledger/`, then the sources only
where a ledger row points.

## Reader contract

```text
1. A source file is EVIDENCE OF WHAT WAS SAID, not of what is true.
2. Each layer keeps its own status vocabulary. Never translate one into another.
3. Superseded files are audit trail. Cite canonical files only.
4. bundle_status NOT_CHECKED = the only support is model-written research prose.
5. FLAG = a recorded internal inconsistency that still stands. Do not resolve it by picking a side.
6. Unrecorded is UNKNOWN, never zero (H0 §6; the closed-world trap applies to this bundle too).
```

## Energy map

```text
                        HABITAT CHAIN (H0 basis -> H1 verification)
  regulation            ecology               lag                 substrate / knowledge
  HB-01..06  ------->   HB-07..11  ------->   HB-12..14  ------>  HB-15..17  AI power, water, grid
  ESA "harm" removed    no plateau;           extinction debt;    HB-18..24  species = information;
  private land carries  hazard = few          double lag hides     closed world; model collapse
  the exposure          foundational spp      damage before count
       |                      |                                      ^
       +--- HB-05 ------------+--- HB-09 --> HB-16 (flood export) ---+
                                              ^^^^^ BOTTLENECK: DERIVED, unmeasured. G-H3 converts it.

                        SCOPE-AUDIT LINE (R4 report + lab v0.5 code)
  claim generated --> formal check --> record --> verdict (withheld)
  SA-01/02 ETH        SA-03/04 Lean      LB-* lab      SA-05/06 Palomar, AGMAI
                      checks STATEMENT,  records,      separate record from verdict
                      not the CLAIM      never judges
                           ^ INTERFERENCE: "compiles" read as "true" (the spec gap)

                        AOS CHAIN (T0 study summary, R5 report, Simulators drop, T1 transcript)
  thickness ceiling --> stripe law ---------> granular escape --> IFE amplifier --> BARRIER PER BIT
  AO-01..04, AO-15      AO-05 (recomputed)    AO-07 stochastic    AO-08 class fork   AO-11  TERMINAL
  PERCEPTUAL: the       SCOPED: continuous    price: coin flip    0.3 T vs 10 T      unmeasured in
  beam was never in     films only (AO-06)    per grain                              every class;
  the option space                                                                   G-A1 decides
       latency AO-12 / AO-14 and energy AO-13 hang off the side: real ceilings, unmeasured demos

                        METHOD LINE (T1): marker format applied to post-cutoff studies
  MT-01 claim --> MT-02 evidence = corrections --> MT-05/06 two more studies --> MT-07 same
  terminal-node signature: a cheap, unrun measurement.  Status: VOID_SELF_RUN, n unsettled (X-19)

  shared harmonic: every line says the loss/error is invisible from inside the record.
  shared leverage: the first MEASURED record (G-H3 siting map; G-L2 beach-count pilot; G-A1 Sharrock run).
```

## Layout

```text
README.md                          this file
AUDIT_NOTES.md                     what landing in Simulators did to the tree (ARC_001..006)
samples/check_corpus.sample.txt    one in-tree run of tools/check_corpus.py
MANIFEST.json                      every file: sha256, role (canonical/superseded/asset), lineage,
                                   provenance, upload origin; identical-content groups; upload containers
ledger/claims.jsonl                67 atomic claims: HB-* habitat, SA-* scope audit, LB-* lab,
                                   AO-* all-optical switching, MT-* method
ledger/conflicts.jsonl             22 cross-source or internal inconsistencies, X-01..X-22
ledger/gaps.jsonl                  27 open items: H0/H1 gaps, threads A-D, lab, AOS, method, bundle
tools/check_corpus.py              27 checks; recomputes every stated number it can + the FLAG findings
boundary/                          the biomimicry boundary: 6 axes, 15 cases, 6 candidate lines, none
                                   adopted; changelog.jsonl is append-only and hash-chained
tools/boundary.py                  render / verify / log a change / --selftest (19 checks)
sources/habitat/H0_basis.md                    Kavik + Claude, 2026-10-26          canonical
sources/habitat/H1_deep_research_report.md     OKComputer run, verifies H0          canonical
sources/scope-audit/report/R4_v0.5.md          OKComputer run, R1->R4 accreted     canonical
sources/scope-audit/report/superseded/R1..R3   strict prefix drafts of R4           superseded
sources/scope-audit/lab/v0.5/                  scope_audit_lab, 90 tests            canonical
sources/scope-audit/lab/superseded/v0.1..v0.4  earlier versions, kept runnable       superseded
sources/instruments/physical_limits_suite.py   limit record + linked discrepancy    canonical
sources/instruments/physical_discrepancy.py    single-record predecessor            superseded
sources/aos/T0_ucsd_study_summary.md           operator paste: Khalid et al. 2026    canonical
sources/aos/T1_session_transcript.md           operator paste: model turns, + Kimi   canonical
sources/aos/R5_constraint_chain_report.md      OKComputer run, barrier per bit       canonical
sources/aos/figures/                           R5 figures 1-6                        asset
sources/aos/simulators-drop/<folder>/...       9 Simulators artifacts at their target paths;
                                               MANIFEST field simulators_target names each one
  category-weld/welds/        optical_switching_speed, deterministic_switching
  constraint-assembly/cases/  aos-vector-beam (v2; v1 under superseded/), granular-reptation,
                              ife-amplifier-scaling
  presented-binary/cases/     aos-thickness-ceiling
  uninstrumented/cases/       024aoswritelatency.md   (024 collides in Simulators main, X-20)
  scope-bound-shapes/         aos_topology_scope.py   (imports Simulators scope.py)
```

## Claim record

```python
{
  "id": "HB-09",                 # permanent; never renumbered
  "chain": "habitat",            # habitat | scope_audit | lab
  "node": "ecology",             # position in the energy map
  "claim": "...",                # one assertion, paraphrased tight
  "where": ["H0 §2", "H1 §3.2"], # section pointers into sources/
  "origin_tag": "OBSERVED",      # the source's OWN tag, verbatim
  "h1_verdict": "CONFIRMED w/ refinement: ...",   # H1's verdict, verbatim class
  "bundle_status": "NOT_CHECKED",  # NOT_CHECKED | RECOMPUTED | FLAG  (this bundle's set)
  "feeds" / "depends_on": [...],   # edges of the chain
  "conflicts": ["X-.."],           # present when FLAG
  "check": "physics_counts"        # present when RECOMPUTED or FLAG; a row in check_corpus.py
}
```

## Vocabularies (one per layer; no mapping between them)

```text
H0 basis         OBSERVED / DERIVED / PROPOSED / GAP
H1 verification  CONFIRMED / CONFIRMED w/ refinement / Partially / NOT LOCATED
R4 fact-check    Confirmed / Confirmed as the claim / Qualification needed ; claims UNREFEREED
lab records      interpretation "unassigned"; "candidate transition region; cause and significance unassigned"
instruments      evidence MEASURED / ESTIMATED / UNKNOWN / GAP ;
                 access AVAILABLE / UNAVAILABLE / RESTRICTED / NOT_CHECKED / UNKNOWN
drop cases       constraint_class invariant / consumable / soft ; presented-binary documented /
                 asserted / absent ; scope bindings LIVE / FROZEN / UNDECLARED
T1 transcript    VOID_SELF_RUN / NOT_COMPUTABLE / UNRECORDED ; sealed-commit HIT / PARTIAL / MISS
this bundle      NOT_CHECKED / RECOMPUTED / FLAG ; checker PASS / FLAG / NOT_TESTABLE / FAIL
```

## Run

```sh
python3 tools/check_corpus.py          # exit 0 = no FAIL (FLAGs allowed), 1 = FAIL
python3 tools/check_corpus.py --json
SIMULATORS_PATH=/path/to/Simulators python3 tools/check_corpus.py   # 3 sibling checks; else NOT_TESTABLE
cd sources/scope-audit/lab/v0.5 && python3 -m unittest discover -s tests   # 90 tests
python3 -m scope_audit_lab waves-demo --out /tmp/w.jsonl                   # from the same dir
```

Python >= 3.8 for the checker; the lab README states 3.10+. Standard library only. No network.

## Current check state (2026-10-28)

```text
in Simulators (ai-reading-corpus/, the tree is its own sibling):
PASS 14  ledgers, manifest, lab_tests (90/90), maxwell_residual, waves_counts, physics_counts,
         v01_stream_validates, instruments_selftest, landauer_300K,
         aos_delta, aos_pulse_arithmetic, aos_sim_instruments, aos_case_number (landed as 025),
         boundary_log
FLAG 13  esa_60_days (X-01)  r4_fr_url (X-02)  h1_gap_count (X-05)  lab_readme_stale (X-07)
         missing_instruments (X-08)
         aos_kaplan (X-09)  aos_energy (X-10)  aos_latency (X-11)  aos_crpt_carried (X-12)
         aos_weld_encoding (X-15)  aos_scope_verdict (X-16)  aos_ez_contradiction (X-17)
         boundary_hb24 (X-22)
FAIL 0
standalone, no Simulators checkout: aos_sim_instruments, aos_scope_verdict, aos_case_number
         read NOT_TESTABLE, never PASS
```

Every lab number in R4 reproduced. R5's Kaplan table and Delta crossings reproduce; its
energy-per-bit numbers do not. Every claim about the outside world in H1, R4, R5, T0, T1 is
NOT_CHECKED: no source was re-fetched for this bundle (G-B3). Landing notes: `AUDIT_NOTES.md`.

## Biomimicry boundary (boundary/)

```text
where does learning from nature stop?   UNSETTLED; adopted_line = null
L1 organism  L2 species  L3 evolved design  L4 self-organized  L5 non-human  L6 no copy
7 of 15 cases read the same under every line (animals, single cells)
8 of 15 depend on the line: termite mound, Roman concrete, crystal, nacre, virus,
          BZ reaction, river delta, autocatalytic set
Roman concrete is IN under no line (X-22); termite mound is OUT of 'species', IN of 'no copy'
to move the line: edit boundary.json, then tools/boundary.py log; unlogged edits FAIL the check
```

Read `boundary/BOUNDARY.md` for the axes, the rules and the change procedure.

## Extending

```text
new source        -> sources/<line>/, add to MANIFEST (sha256, role, lineage, provenance)
new claim         -> next free id in its chain; origin_tag copied verbatim
claim re-verified -> change bundle_status only; record the source in a new field "bundle_source"
conflict repaired -> its check goes PASS; set the conflict's "resolution" and keep the row
boundary moved    -> edit boundary/boundary.json, run tools/boundary.py log (never edit changelog.jsonl)
stated number     -> gets a check in tools/check_corpus.py before any other file cites it
```
