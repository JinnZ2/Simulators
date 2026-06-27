---
file_role: navigation
source: claude
original_filename: (none — created during reorg)
summary: Final report on the incentive-blindspot-sim/ reorganization. What moved, what was renamed, source tags assigned, test result, residual uncertainties.
---

# REORG_REPORT

Reorganization of `incentive-blindspot-sim/` per handoff. Branch:
`claude/reorg-incentive-blindspot-sim2` (off `origin/main`, since the
handoff's "Current contents" matches `main`, not the in-progress
feature branch).

## Moves (history preserved via `git mv`)

| Old path | New path |
|---|---|
| `incentive_blindspot_sim.py` | `sim/incentive_blindspot_sim.py` |
| `samples/` | `sim/samples/` |
| `tests/` | `sim/tests/` |
| `Preamble.md` | `sim/00_physics_aperture.md` |
| `Audit.md` | `development-record/01_bnram_strict_v2_finalized_addendum.md` |
| `Plz.md` | `development-record/02_pvl_specification_empirical_validation.md` |
| `Audit2.md` | `development-record/03_sria_self_referential_integrity_audit.md` |

Decision on `tests/`: moved under `sim/` (vs leaving at root). Rationale:
`tests/test_incentive_blindspot_sim.py` uses
`sys.path.insert(0, ... '..')` to find the module, so the module has
to sit one level above the tests directory. Keeping tests at root would
have required editing that path-hack. Under `sim/` the existing hack
resolves `..` to `sim/` which contains the module — no test edits
needed. The handoff explicitly authorized either placement.

## Created

- `LICENSE` — full CC0 1.0 Universal text. Makes the "nothing to
  consolidate under one name" property legally real rather than just
  asserted in comments.
- `README.md` — rewritten per spec: title + thesis, read-first link to
  the aperture, run line, four-line map of what's here, claims link,
  provenance line. Short.
- `sim/CLAIMS.md` — falsifiable-claim register extracted verbatim from
  the four `claim_BS_*` functions in the code (statements, refutation
  conditions, current verdicts). REFUTATION_PROTOCOL stated at top. No
  new claims authored.
- `development-record/INDEX.md` — one-row-per-file navigation for the
  development record, with source tag and one-line summary per entry.
- `REORG_REPORT.md` — this file.

## Front-matter

Prepended to every existing `.md`:

| File | role | source | confidence |
|------|------|--------|------------|
| `sim/00_physics_aperture.md` | physics-grounding | unverified | — |
| `sim/samples/README.md` | artifact | operator | high |
| `development-record/01_bnram_strict_v2_finalized_addendum.md` | development-record | gemini | low |
| `development-record/02_pvl_specification_empirical_validation.md` | development-record | unverified | — |
| `development-record/03_sria_self_referential_integrity_audit.md` | development-record | gemini | low |

The three new files (`README.md`, `sim/CLAIMS.md`, `INDEX.md`,
`REORG_REPORT.md`) carry front-matter inline at creation.

## Source-tag reasoning

The two `gemini` tags rest on **register heuristics only**: structured
explanation register, numbered roman-numeral sections, formal mandates
(shall / must), prose scaffolding around each rule, and (on `03`) the
"You are absolutely correct" opener acknowledging operator critique.
These match the Gemini signature in the handoff. Confidence is flagged
low so the operator can reclassify if their session-context memory
disagrees.

`02_pvl_specification...` opens "Here is the consolidated text from
all four images, merged into a single coherent document" — that signals
the operator first extracted text from screenshots and then asked an
AI to organize it. The originating model is too uncertain to claim;
`unverified`.

`sim/00_physics_aperture.md` (`Preamble.md`) is short and lacks any
distinctive register signature; `unverified`.

## Aperture reconciliation

The handoff anticipated the possibility of two aperture drafts. There
is only one in this branch's state: `Preamble.md` → `sim/00_physics_aperture.md`.
A more elaborate `00_APERTURE.md` exists on the feature branch
`claude/token-minimizer-emergence-sim-T4pjn` (it maps each of C, M, F,
V, B, X to its physical function and the conservation law underneath
— Shannon channel capacity, Ashby variety, observability, the second
law). That is the more complete version. **Recommendation, to be
applied later by the operator or in a follow-up commit:** merge the
feature-branch aperture into `sim/00_physics_aperture.md` here, and
demote the current `Preamble.md` content into `development-record/`
as `00_preamble_early_draft.md`. I did not do that automatically
because:

1. The handoff scope was reorganization of the existing contents on
   `main`, not cross-branch merging.
2. The two documents are both "physics-grounding" but at different
   scopes (the Preamble is a generic operational protocol; the
   feature-branch aperture is variable-specific).

## Tests

After all moves:

```
$ cd sim && python3 -m unittest discover tests
Ran 27 tests in 0.004s
OK
```

All 27 tests pass with **zero changes** to the test code. The path-hack
keeps working because `tests/` and the module both sit one level deep
under `sim/`.

## Hard-rules compliance

- ✅ **Nothing deleted.** Every original file is in the new tree.
- ✅ **No substance edited.** Only front-matter prepended.
- ✅ **Original filenames preserved** in every front-matter block.
- ✅ **`git mv`** used for every move; history is preserved as renames.
- ✅ **Commits in logical chunks** with clear messages:
  - `reorg: separate artifact from development record; add CC0 LICENSE`
  - `reorg: add front-matter to all .md files (role, source, original_filename, summary)`
  - `reorg: add LANDING + CLAIMS + INDEX + REORG_REPORT navigation files`
- ✅ **One final push** at the end of the reorganization.

## What I could not classify confidently

- Source attribution on `01` and `03` is a register guess, not a
  recovered session fact. Confidence flagged low. If the operator's
  memory says these were DeepSeek or Claude, the front-matter should
  be corrected on next pass.
- The `02_pvl_specification...` source is genuinely unknown given the
  image-extraction opener; left as `unverified`.

## Final state

```
incentive-blindspot-sim/
├── README.md                                                   (rewritten)
├── REORG_REPORT.md                                             (new — this file)
├── LICENSE                                                     (new — CC0 1.0)
├── sim/
│   ├── 00_physics_aperture.md                                  (← Preamble.md, +front-matter)
│   ├── CLAIMS.md                                               (new — extracted from code)
│   ├── incentive_blindspot_sim.py                              (moved, unmodified)
│   ├── samples/
│   │   ├── README.md                                           (+front-matter)
│   │   └── demo.sample.txt
│   └── tests/
│       ├── __init__.py
│       └── test_incentive_blindspot_sim.py                     (unmodified — path-hack still resolves)
└── development-record/
    ├── INDEX.md                                                (new — navigation)
    ├── 01_bnram_strict_v2_finalized_addendum.md                (← Audit.md, +front-matter)
    ├── 02_pvl_specification_empirical_validation.md            (← Plz.md, +front-matter)
    └── 03_sria_self_referential_integrity_audit.md             (← Audit2.md, +front-matter)
```
