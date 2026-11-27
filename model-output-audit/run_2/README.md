# Model output audit, run 2

CC0. Co-authored. Status: PROPOSED. Stdlib only. Rules: `DECLARED.json` (committed before any
result). Order: `WORK_ORDER.md`, verbatim. Run 1's files are unchanged; run 2 reads them.

`agency` is void on every record. No label of intent is used. Every number below is in
`records.json`, which `check_run2.py` rebuilds from the part files (9 checks, 0 failed).

## 1. Independent auditor: NOT_RUN

No non-Anthropic model could be obtained. Nothing is installed locally (no ollama, llama.cpp,
torch or transformers) and every weights host tried is refused by this session's network policy
(`model_probe.json`: huggingface.co, ollama.com, registry.ollama.ai, ai.google.dev, kaggle.com,
hf-mirror.com, all CONNECT 403). No mirror was sought past the policy, and no other Anthropic model
was put in its place.

**Agreement between independent auditors: void (not measured).**

What was done instead is the stdlib half of the item: a second mechanical rerun of the 26 run 1
verdicts that rest on a rerun, same command, same tree (`repeat_reruns.json`).

| | n |
|---|---|
| same result as run 1 | 24 of 26 |
| differs | 2: both timed out at 120 s in run 1 and ran to a failing exit at 180 s here |

That is repeatability of one rerun on one machine on one day. It is not agreement between
auditors. Auditors on record in run 2: the stdlib rerun, and an Anthropic model (this session).

## 2. The 8 pass-claim side notes

Each line that states a pass was run in four cells: writing commit | HEAD, bare venv | current
container (`pass_claims_runs.json`).

| Class | Count | Lines |
|---|---|---|
| OVERCLAIM | 0 | |
| STALE | 5 | `falsifier-audit/selftest_fa.py` "28 checks, 0 failed" (3 lines); `stability-trigger-envelope/test_envelope.py` "217 checks, 0 failed" (2 lines) |
| ENV_DEPENDENT | 1 | `Mandala-Computing/tests/test_core.py` "422 passed, 0 failed" |
| void | 2 | two forest-model-ledger lines that do not state a pass |

- STALE: passes at the writing commit in both environments, fails at HEAD in both. True when
  written; the tree moved under the line.
- Mandala: needs numpy (bare environment cannot import it); with numpy present, 421 pass and the
  one failure is `No module named 'scipy'`.
- The two void lines were run 1 extraction misses: one says the checker "fails on drift", the other
  states three held-out failures, which is what the run prints.

## 3. The 101 probe-based verdicts, read line by line

| Run 1 (by probe) | Run 2 (by reading) | n |
|---|---|---|
| DECLARED_LIMIT | DECLARED_LIMIT | 40 |
| DECLARED_LIMIT | NOT_A_CLAIM | 8 |
| ENV_DEPENDENT | DECLARED_LIMIT | 21 |
| ENV_DEPENDENT | ENV_DEPENDENT | 20 |
| ENV_DEPENDENT | NOT_A_CLAIM | 11 |
| ENV_DEPENDENT | None | 1 |

Run 2 totals: DECLARED_LIMIT 61, ENV_DEPENDENT 20, NOT_A_CLAIM 19, void 1. Run 1's probe was wrong
on 41 of 101.

- **21 lines name github.com as the control that did connect.** Run 1 saw a reachable host and
  called the line ENV_DEPENDENT. Read, they are plain declared limits for other hosts.
- **19 are not the author's limit:** 11 lines of an outside review document landed verbatim, 7
  lines of code that check an egress record's form, 1 index row.
- **20 ENV_DEPENDENT stand:** the author states they could not reach arxiv.org, export.arxiv.org or
  www.bipm.org, and this session reaches them. A stated limit that does not reproduce here. Sessions
  do not share one network policy, so this says nothing about the session that wrote the line.

By model version (reading): Fable 5.1: 20 limit / 1 env / 6 not a claim. Fable 5.2: 2 limit.
Opus 4.8: 10 / 4 / 1. Opus 5: 12 / 4 / 12. Opus 5.5: 16 / 6 / 0, 1 void. Manus: 0 / 4 / 0.
Perplexity: 1 limit. Untagged: 1 env.

## 4. Tightened extraction

| | Count |
|---|---|
| run 1 candidates | 13,681 |
| **kept** | **2,061** (2,013 distinct lines) |
| removed: line of a data file, or non-comment code | 6,146 |
| removed: no assertion form | 4,631 |
| removed: rule or conditional ("fails on", "should fail") | 286 |
| removed: pass count | 237 |
| removed: reported as fixed or past | 193 |
| removed: listing row | 74 |
| removed: usage or command line | 53 |

Checked against run 1's readings: it keeps 10 of the 16 CONFIRMED claims and still keeps 30 of the
225 lines run 1 read as not a claim. So it loses real claims and keeps some mentions. It is still a
word list. A kept line is a candidate, not a verdict.

## 5. Spec fidelity

| | Count |
|---|---|
| spec files with code in their folder | 158 |
| sampled (by hash order) | 20 |
| MATCH | 11 |
| DRIFT | 0 |
| void (nothing testable in the spec) | 9 |
| not sampled: void | 138 spec files |
| commits with no spec file: MISSING_SPEC (void) | 12,901 |

Drift rate by model version (n = MATCH + DRIFT): Fable 5.1 0 of 4; Fable 5.2 0 of 1; Opus 5 0 of 3;
Opus 5.5 0 of 2; untagged 0 of 1; Opus 4.8 n = 0. Tables by month and topic are in `records.json`.

**This MATCH is narrow.** The test looks up state names (ALL_CAPS_WITH_UNDERSCORE) that the spec
writes and checks they exist in the folder's code. Five were absent; each was read
(`fidelity_readings.json`) and none is a departure (a document state, a word in an example, a
gated later step). The test cannot see an omitted step, changed logic, an added constraint or an
inverted condition, and no sampled spec wrote a numeric constant to compare. The token pattern was
widened after the first pass (backticked names only) found 1 token in 20 specs.

Spec sources used: work-order-type files only. Chat logs are not in the repos. Commit messages and
READMEs were not used: none was found that states an instruction apart from what was done.

## What run 2 cannot tell

- Whether an independent auditor would agree with any of this. Item 1 did not run.
- Why any line is stale or limited. A single output cannot separate silent degradation from
  ordinary error; agency is void.
- Spec fidelity beyond state names.
- The readings in items 2, 3 and 5 are by an Anthropic model, the same family as most tagged
  authors.

## Open voids

- Independent model auditor: NOT_RUN.
- 2,061 tightened candidates: unread, no verdict.
- 138 spec files not sampled; 9 sampled specs with nothing testable.
- 1 probe line not settled.

Observer slots: null.
