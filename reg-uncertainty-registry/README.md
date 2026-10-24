# reg-uncertainty-registry

WO-REG-1 (consolidated bundle, `bundle/WORK_ORDER.md`, verbatim). This folder is a machine-readable
registry of regulatory decisions made under scientific uncertainty. It holds direction, two-sided
consequence, cost-bearer, actors, authority chains, conflicts, reversals and gaps. It also holds
the evidence and verification state behind every coded field.

No count is written in this README. Counts are in `REVISED_REPORT.md` and `CLAIM_TABLE.md`, which
`tools/report.py` renders from `registry/`. `tools/validate.py` re-renders both and compares bytes.

```text
bundle/  source/  verification/           inputs: verbatim, pinned (bundle_pins.json, source/PINS.json)
        |                                  the ledger: one row per claim, four-state rule, search-index depth
        v
tools/curation_core|cases|ncr.py         the registry's own coding, as data (PROPOSED, one coder)
        |
tools/build.py ---------> registry/*.json + MANIFEST.json      deterministic; never edited by hand
        |                       |
        |          tools/grade.py   RUS-0.2 from its own text; RUS-0.3 as switches
        |          tools/stats.py   tallies, sweep, bivariate, forcing, reversals, kappa
        v                       v
tools/report.py ----> REVISED_REPORT.md  CLAIM_TABLE.md  CHANGE_LOG.md  schema/QA_MAPPING.md
        |
tools/validate.py     pins, manifest, schema, claims, edges, refs, ledger, statements,
                      configuration, gaps, rebuild, report, tools  (--selftest plants a defect per check)
```

## Read in this order

| file | what it is |
|---|---|
| `REVISED_REPORT.md` | findings F1-F16, each tagged holds / scope-limited / no data / absent; statements corrected; NCR register |
| `CLAIM_TABLE.md` | `RUR_*` claims with status, depth and falsifier |
| `RUS-0.3.md` | the PROPOSED revision of RUS-0.2 (M7, SUB, R6a/R6b, R1 scope, basis, over_possible) |
| `CHANGE_LOG.md` | every edit to a recorded value, in order, with its NCR and its WO-REG-1 / 1a / 1b tag |
| `schema/QA_MAPPING.md` | each nuclear-QA term the work order borrows, against the clause it borrows from |
| `schema/vocabulary.json`, `schema/registry.schema.json` | closed vocabularies and object schema; additions carry a reason |

## Tools

```sh
python3 tools/build.py                 # registry/ from inputs + curation; prints object and edge counts
python3 tools/report.py                # the four rendered documents
python3 tools/validate.py              # all checks on the real registry
python3 tools/validate.py --selftest   # each check fires on a planted defect; then the clean copy passes
python3 tools/stats.py [--section annex|tallies|components|sweep|bivariate|forcing|reversals|mirrors|c2|kappa|text]
python3 tools/chain.py A01             # reasoning chain back to sources, state at each hop, single-failure flags
python3 tools/who.py A01 | --actor ID | --overruled
python3 tools/symmetry.py              # matched profile, different direction, no named exception
python3 tools/gaps.py                  # absences, non-decisions, unmapped ids, unlocated inputs, unsearched rows
python3 tools/reversals.py             # REVERSAL objects by initiator; exact Mann-Whitney on both D01 anchors
```

Each library refuses `--selftest` (exit 2) and names `validate.py`. Everything is standard library
only. Run with `python3 -I` when the inputs are not your own. Outputs are pinned in `samples/`.

## Rules the registry keeps

```text
claim states       VERIFIED / CORRECTED / NOT_FOUND / UNREACHABLE, from tools/check_citations.citation_state (imported)
NOT_FOUND          two empty searches, or a different object at the id; an unsearched row is UNREACHABLE
gaps               are nodes: ENDPOINT_ABSENCE, NON_DECISION, unlocated input, undisclosed conflict
                   (a decision with no located disclosure record carries a CONFLICT node UNREACHABLE,
                   never "no conflict")
direction          stored twice: action (the agency's move) and outcome (legal status at the coding date)
recode             asserts the source carries the from-value, keeps both in history, names its NCR
not testable       a property of the cell counts, reported as such, never as a null
second coder       contamination probe first; kappa per field when the coding returns (state in F15)
```

## Open, and where it is recorded

| item | state |
|---|---|
| second coding (ten rows) | packet and probe pinned in `second_coder/`; coding not returned; F15 / RUR_016 |
| human second coder (RUS-0.2 section 12) | not met; RUR_018, NCR-N24 |
| primary-depth reading of the QA clauses and of most ledger rows | search-index depth only; container DNS refuses publisher hosts; NCR-N23 |
| DTXSID and ontology ids | local-only ids are gap nodes; lookup not run |
| Frame C2 document-level coding | notice level only; gap FR-C2-DOCS |
| sweep variant M6 | does not reproduce; NCR-N07 |

`tools/curation.py`, the first single-file curation module, was split into the three `curation_*`
modules and removed. It remains in history at `294e4af`.

Stdlib only, parses under Python 3.8, CC0.
