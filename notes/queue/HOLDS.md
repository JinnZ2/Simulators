# HOLDS -- which session holds which branch, and which paths it may touch

Operator protocol, 2026-10-07:

- Every session reads this file before starting work on a branch.
- It adds a row for any branch it takes.
- It skips any branch another session holds.
- The merge rule's scope check reads `allowed_paths`: a diff that touches
  a path outside its branch's allowed_paths fails the check.

`allowed_paths` is a comma-separated list. A trailing `/*` covers
everything under that directory. Status is HELD while work is open, then
MERGED (with PR and merge sha), RELEASED, or ABANDONED. A row is never
deleted; a finished row stays as the record.

| branch | allowed_paths | holder_session | started | status |
|---|---|---|---|---|
| claude/threshold-states-escape | threshold-states/*, interaction_class.py, test_interaction_class.py, .github/workflows/test.yml, threshold-states-in-animal-escape.md [a], archive/interaction_class/* [a], tests/test_archive_expected_red.py [a] | session_01Y4zVdoRHPDHpVwSPbqbeLR, session_014bxQGPgkmsJRWUx92REKSs | 2026-10-05 | MERGED #123 (c7aa5f2) |
| claude/repin-sense-as-match | KNOWN_RED.md | session_014bxQGPgkmsJRWUx92REKSs | 2026-10-07 | MERGED #124 (2cb6eca) |
| claude/queue-holds | notes/queue/HOLDS.md | session_014bxQGPgkmsJRWUx92REKSs | 2026-10-07 | MERGED #125 (731a94d) |
| claude/interaction-spec-q1-q4 | threshold-states-in-animal-escape.md, notes/queue/HOLDS.md, threshold-states/* [g] | session_014bxQGPgkmsJRWUx92REKSs | 2026-10-07 | MERGED #127 (71df45c) |
| claude/holds-relation-axes | notes/queue/HOLDS.md | session_014bxQGPgkmsJRWUx92REKSs | 2026-10-07 | MERGED #128 (7397ebf) |
| JinnZ2/Polyhedral-Intelligence: claude/relation-two-axes [h] | ontology/relation_classes.json, ontology/relation_class.py, ontology/relation_classes.md, tests/test_relation_class.py, CLAUDE.md | session_014bxQGPgkmsJRWUx92REKSs | 2026-10-07 | MERGED Polyhedral-Intelligence #15 (fdd84ee) |
| claude/human-sensing-prior-cc0-cbm411 | CLAUDE.md, README.md, human-sensing-prior/PATHWAYS.md, human-sensing-prior/PATHWAY_B.md, human-sensing-prior/PREDICTIONS.md, human-sensing-prior/pathways.py, human-sensing-prior/test_pathways.py, human-sensing-prior/samples/features.sample.txt, human-sensing-prior/samples/lengths.sample.txt, human-sensing-prior/samples/score_unrun.sample.txt, notes/queue/HOLDS.md, human-sensing-prior/samples/pilot_unrun.sample.txt [b], human-sensing-prior/registered/human-sensing-prior.7f780aa.md [b] | session_014bxQGPgkmsJRWUx92REKSs, session_01U4mRsfZAdaV1xWBmZSRbjK [b] | 2026-10-07 | MERGED #126 (a1ea7ae); pilot RUNNER_READY, job loaded, not run [c][e][f] |
| claude/battery-offgas-prearm | battery-offgas-prearm/*, notes/queue/HOLDS.md [i] | session_019vfUAFE1MxwGdZjKisbdba | 2026-10-08 | PR #130 (merged by its own session when failures == KNOWN_RED pins) |
| claude/corn-stunt-forensics | corn-stunt-forensics/*, notes/queue/HOLDS.md [j] | session_019vfUAFE1MxwGdZjKisbdba | 2026-10-08 | MERGED #131 (705cbca) |
| claude/moving-mean-tracker | moving-mean-tracker/*, notes/queue/HOLDS.md, CLAUDE.md, README.md, tools/known_answer.py, tests/test_known_answer_gate.py [k] | session_014bxQGPgkmsJRWUx92REKSs | 2026-10-08 | HELD |

[a] Backfilled after the fact. These paths are in #123's diff and not in
the operator's backfill list: `threshold-states/*, interaction_class.py,
test_interaction_class.py, .github/workflows/<ci file>`.
- `threshold-states-in-animal-escape.md` sits at the repo root, so
  `threshold-states/*` does not cover it. It carries the section 8
  rewrite that removes the duplicated literature table.
- `archive/interaction_class/*` and `tests/test_archive_expected_red.py`
  carry the archive move the operator ordered on 2026-10-07 (root build to
  `archive/` plus a redirect).

Under the operator's list alone, #123's scope check would fail on these 5
files. They are recorded here, not hidden.

Rule from 2026-10-07 on (operator): the session taking a hold declares
allowed_paths here BEFORE starting work. A backfill written chat-side
always lags the diff.

claude/human-sensing-prior-cc0-cbm411: allowed_paths is the branch's diff
against main (merge-base 9262516) as it stood before any work, plus this
file. The branch was opened by another session; this session took the
hold to merge it, and its row was declared in the branch's first commit,
before main was merged in.

[b] Backfilled after the fact, 2026-10-07. Session
session_01U4mRsfZAdaV1xWBmZSRbjK opened this branch. It continued work on
the branch at the operator's direction, and it did not read this file
before doing so. Its commit b0c8795 (amendment 2 harness) was made before
it fetched the hold. Two paths in that commit and its follow-up are
outside the declared list, and both are new files:
- `samples/pilot_unrun.sample.txt` is the sample output of the pilot gate
  that amendment 2 item 2 adds.
- `registered/human-sensing-prior.7f780aa.md` is a byte copy of pathway A
  at 7f780aa, sha256 1a42dc8c...cbd7, the pin in amendment 2 item 4.
  It is needed because the merge of main (79e6374) moved the working copy
  of A off the pin.

Under the declared list alone, the scope check would fail on these 2
files. They are recorded here, not hidden.

[c] 2026-10-07, operator. The human-sensing-prior pilot (amendment 2
item 2) is BLOCKED_ON_RUNNER. There is no model endpoint in the Claude
Code environment, and the operator is on a phone. A chat-side API runner
artifact may be built; that decision is pending. The hold stays HELD.

[d] 2026-10-08, declared before work. The runner dispatch (emit job,
runner manifest, runner import) adds one path to this branch's
allowed_paths: `human-sensing-prior/runs/*`, which holds the committed
job files. The other files it touches are already in the list.

[e] 2026-10-08. Pilot status BLOCKED_ON_RUNNER -> RUNNER_READY. The
chat-side runner artifact exists; amendment 3 (6d186b9) records it, and
the pilot job human-sensing-prior/runs/pilot-2026-10-08a.json (6f1544c,
270 items) is committed. The hold stays HELD.

[f] 2026-10-08, recorded chat-side, no Claude Code action. The pilot job
was loaded into the runner. Job file sha256
5e55685f8f8922186a843782c773456e5d72394550626114c123528382b86457, the raw
bytes of human-sensing-prior/runs/pilot-2026-10-08a.json at 5a9642e
(rechecked here against the committed blob). All 270 prompt hashes were
recomputed under the runner's assembly rule: 0 mismatches. Order seed
1114932034, recorded at load before any call. The job file carries no seed
field, so this footnote is where the seed lives. No call had been made when
these were recorded. The pilot's run record must cite both values.

Footnote letters: main's [b] and [c] were relabeled [g] and [h] when
main was merged into claude/human-sensing-prior-cc0-cbm411 (2026-10-08).
That branch had used [b]..[f] for its own row. No footnote text changed.

[g] Widened 2026-10-07 BEFORE the build work starts, in its own commit,
on the operator's dispatch "§8 interaction precedence: resolve OPEN,
commit cases, then build". `threshold-states/*` carries
`outside_cases_v2.json` (committed alone, before any code change), the
Q1-Q4 build of `interaction.py`, its tests, the runner and the samples.

[h] A branch in another repository. Polyhedral-Intelligence carries no
HOLDS file, so the hold is declared here, before work, per the operator's
dispatch "RELATION ONTOLOGY: split class into two axes" (2026-10-07).
`CLAUDE.md` is listed because its Emotion Glyph Map note names the enum's
members; it is touched only if that list must change.

[i] Declared 2026-10-08 BEFORE any file under `battery-offgas-prearm/`
exists, in its own commit, on a peer session's relay of the operator's
voice request ("mark that up for a buildable spec"). The peer's request
is not the operator's approval of anything outside these paths; the root
`CLAUDE.md` index is NOT in scope and is not edited by this hold.
`tools/known_answer.py` is not in scope either: the trigger module's
known answers live in its own test file.

[j] Declared 2026-10-08 BEFORE any file under `corn-stunt-forensics/` exists,
in its own commit, on the operator's voice request to land the forensic-pass
test on the 2024 corn stunt outbreak as a folder with a claim table, plus the
insect-biology angle (thermal limits, evolution, vector competence, season
temperature projections). Root `CLAUDE.md` index is not in scope.

[k] 2026-10-08, declared before work, on the operator's dispatch "#126
follow-up + MOVING-MEAN TRACKER build". The new folder is
`moving-mean-tracker/` (stdlib, CC0, PROPOSED instrument, fixture provider
only, no live data). `CLAUDE.md` and `README.md` carry the index entry.
`tools/known_answer.py` and `tests/test_known_answer_gate.py` are listed
because the repo's standing rule is that no metric ships without a
known-answer run, and registering one touches both files.

Footnote letters: claude/moving-mean-tracker declared its hold as [i] on
its own branch while main used [i] for claude/battery-offgas-prearm. When
main was merged into the tracker branch (2026-10-09) the tracker's [i] was
relabeled [k]. No footnote text changed. The same merge records two
statuses from the PR record: #126 (a1ea7ae) and #131 (705cbca).
