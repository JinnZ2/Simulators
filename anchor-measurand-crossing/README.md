# anchor-measurand-crossing

A work order delivered verbatim in `WORK_ORDER.md` and built to it: does
a model produce defects whose QUANTITY differs from the quantity a
method measures, as a function of where the prompt anchors — at the
method, or at the decision the claim is cited to justify? A counting
outcome with a stated null, not a benchmark.

```
WORK_ORDER.md §4 ──parse──► prompt M / D / M+ ──► operator runs, logs JSONL
                                                          │
cases.jsonl (hand-built)                                  ▼
lexicon.json (aliases, via) ──► group ──► crossing band [min,max] per case per arm
transforms.json (T-A, T-B) ──┘             │
                                            ▼
                              AP-1..AP-6 verdicts, N1..N5, N4 = rescore under T-B
```

**No model has been run here.** This environment has no model
endpoint, the session that wrote the lexicon is not blind to it, and
section 5's cold-arm rule cannot be met from inside one session that
has read the order. `runs/constructed.jsonl` is a constructed fixture
that exercises the scorer; every record says `constructed: true` and the
report banners it. What is delivered is the instrument, checked in both
directions on constructed responses, with the arm the order calls
highest priority (M+, AP-3) built and unrun.

## Run

```bash
python3 amc.py cases                                  # admitted cases and candidates
python3 amc.py prompt sc-01 M                         # ARM M, verbatim from the order
python3 amc.py prompt sc-01 D                         # ARM D
python3 amc.py prompt sc-01 M+ [--mplus-placement after_block|end]
python3 amc.py plan --seed 7 [--arms M,D,M+]          # randomized order to log
python3 amc.py score RUNS.jsonl [--transforms T-A|T-B] [--n1 SHEET.json]
python3 selftest_amc.py
```

To run it: take the plan, open one fresh session per row, paste the
prompt, take the one response, and write one record:

```
run_id, model, version, family, date, arm, case_id, session_id,
order_index, raw_response, constructed:false,
decision           (D and M+; must equal the case's decision string)
mplus_placement    (M+)
supplied_measurand (C)      predecessor_run_id (B)
```

The validator refuses two arms in one session (B may follow its
predecessor only), a D or M+ record whose logged decision string differs
from the case's, an M+ without a placement, a record on a case that is
not admitted, and an empty model string (write `UNKNOWN(reason)`).

## What the scorer does and does not decide

Parsing, normalization, matching and counting are mechanical. The
judgement section 6 calls load-bearing — which quantities are transforms
of which measurand — is **data**: `lexicon.json` per case, every alias
tagged with the transform that reaches it, and `transforms.json` with
two lists so N4 is a computed disagreement count rather than a caveat.
A quantity no alias matches is `UNGROUPED` and every count becomes a
band `[min, max]`; a claim whose decision line falls inside a band reads
`undetermined_by_lexicon`. `crossing_band` is registered in
`tools/known_answer.py`, where its case set caught the first build's
floor (`AMC_003`).

| section | function | reads |
|---|---|---|
| 4 | `prompt_templates` / `render_prompt` | M and D parsed from the order; M+ = M + one sentence |
| 5 | `plan` / `validate_runs` | seeded arm order; one arm per session; logged decision string |
| 6 | `parse_m` / `parse_d` / `normalize` / `group` / `crossing_band` | entries, band per response, coverage |
| 7 | `ap1`..`ap6` | verdicts with `undetermined` and `undetermined_by_lexicon` as live values |
| 8 | `nulls` / `n4` | N1 from a coded sheet or NOT_CODED; N2 on admitted controls; N3 by class; N4 two lists; N5 per arm |

Four choices the order leaves open are printed on every report:
`[CHOICE 1]` artifact block layout, `[CHOICE 2]` M+ sentence placement,
`[CHOICE 3]` component quantities count as distinct measurands with the
foreign/component split printed beside the headline, `[CHOICE 4]` AP-3's
"D-level" as the M+ floor reaching the D floor.

## Cases

`sc-01` and `mp-01` are transcribed from section 3 and the selftest
checks the transcription against the order. `ctl-01` is the control
section 8 requires, authored in this session by a model, which section 3
forbids — so it ships as a CANDIDATE with `hand_built: false`, the loader
excludes it, and N2 reads `NOT_EVALUABLE` until an operator adopts it
(`AMC_005`).

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `amc.py` | the instrument, one stdlib file, refuses `--selftest` |
| `cases.jsonl` | two transcribed cases, one control candidate |
| `lexicon.json` / `transforms.json` | the scorer's judgement as data; sha printed on every report |
| `runs/constructed.jsonl` | constructed fixture, not a run |
| `selftest_amc.py` | known answers first, both directions of every guard; writes `samples/` |
| `CLAIM_TABLE.md` | `AMC_001..AMC_008` |

The score report screens clean through the repo's `no_severity` with
no exemption; the prompt render carries the delivered form's own field
name and is screened under the three-arm harness. No author section
(section 11). Stdlib only, parses under 3.9, runs on a phone, CC0.
