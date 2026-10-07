# PROVENANCE -- archive/interaction_class/

The root build of the threshold-states interaction classifier, moved here
whole after the operator chose `threshold-states/interaction.py` as
canonical (2026-10-07). Nothing is deleted and no file content was edited.
Both files are the build commit's blobs, written byte-for-byte.

| file | blob | source |
|---|---|---|
| `interaction_class.py` | `3d0beaa73fd8` | `git show 5587fad:interaction_class.py` |
| `test_interaction_class.py` | `61d5f6810b46` | `git show 5587fad:test_interaction_class.py` |

build commit      5587fad  2026-10-07  threshold-states: ordered interaction test resolves T-7; classifier + tests
canonical build   threshold-states/interaction.py (operator decision, 2026-10-07)
suite             test_interaction_class.py, run from this folder: 33/33, exit 0

What this build is: the pre-split rule. S = sum of all cues, M = max of all
cues, step 0 on S - M, tol a bare number in the response's own units. It
has neither the cue-sign split nor the declared tol mode that the canonical
module now carries, so its verdicts differ from the canonical module's
wherever a cue is negative or a tol is given without a mode.

Between the build and this move, the root copies were an import shim over
the canonical module (commits 3dc3e0d, acd7c6c). The shim held no logic and
is not archived as a build. Its last blobs, for the record:

| file | shim blob |
|---|---|
| `interaction_class.py` | `3e1da88020a4` (acd7c6c) |
| `test_interaction_class.py` | `46f424a513ac` (acd7c6c) |

`git show acd7c6c:<file>` reproduces each. The root `interaction_class.py`
is now a redirect stub; the root `test_interaction_class.py` is removed
(its archived build copy is here).

Before the split, the two builds returned the same verdict on all five
outside cases (threshold-states/samples/run_outside.sample.txt @ bd7d055).
