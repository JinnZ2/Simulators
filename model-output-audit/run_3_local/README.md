# model-output-audit, run 3 (local open model)

Status: **NOT_RUN**. PROPOSED, CC0, co-authored. Observer slots: null.

The order (`WORK_ORDER.md`, verbatim) names a home server and a local open model.
This folder is the kit for that machine. It was filed by the session that wrote
run 2, which is not the independent auditor: it holds no verdict and no fidelity
read. Agreement with run 2 is void until the kit is run.

```text
packet.json  --->  audit_local.py  --->  verdicts.jsonl      --->  score.py  --->  records.json
(135 quotes,       (home server:         reruns_local.jsonl        (reads the       agreement per class,
 how to rerun,      local model +         host_probes.json          run 1 / run 2    every disagreement
 5 specs; no        stdlib reruns)        fidelity_reads.json       key here only)   with its quote
 earlier verdict)                         auditor.json
```

## Run it

```sh
git clone -b model-output-audit https://github.com/JinnZ2/Simulators && cd Simulators/model-output-audit/run_3_local
python3 audit_local.py --selftest                      # no model needed
python3 audit_local.py --model gemma3:27b --clones ~/audit-clones     # Ollama at localhost:11434
python3 score.py                                       # writes records.json, prints the report
git add verdicts.jsonl reruns_local.jsonl host_probes.json fidelity_reads.json auditor.json records.json
```

Other server: `--api openai --url http://localhost:8080` (llama.cpp and the like).
`--clones DIR` is where full clones live or get cloned (19 repos are named in the packet).
A stopped run resumes: items already in `verdicts.jsonl` are not asked again.

## What it does

| Order item | How |
|---|---|
| 1 independent verdict | 26 rerun-decided claims + 101 lines read in run 2 + 8 pass claims = 135. The model sees the line, nine lines around it, the home server's own rerun (writing commit and the run 1 tree, or writing commit and head for pass claims) and its own host probe. Same class set as run 2. |
| 2 agreement | `score.py`: per kind and run 2 class, n / agree / disagree / local None / not asked; rate = agree / (agree + disagree) with its n. Every disagreement listed with the quote. |
| 3 fidelity | the 11 MATCH specs ordered by spec sha256, first 5 (`picked` in the packet). The model lists the spec's steps, marks each PRESENT / OMITTED / CHANGED_LOGIC / INVERTED_CONDITION / UNDETERMINED with a code quote, then lists added constraints per code file. |
| 4 auditor | model name, digest and settings as the endpoint reports them, in `auditor.json` and on every record. A model named claude/anthropic is refused. |
| 5 stdlib, agency | reruns are `git worktree` + `python3 <file>`, 180 s. `agency` is None on every record; the prompts tell the model not to judge intent. |

## Limits

- The kit was written by the author of run 2. The prompts carry that author's wording of the class definitions; a reader who wants the classes stated differently should edit the prompt text and say so.
- The packet is blind to verdicts, not to selection: which 135 lines are asked, and which file a line is rerun against, come from run 1 and run 2.
- Fidelity: the five folders hold 64 KB to 459 KB of Python. No local context holds that, so each step is shown the code blocks sharing the most words with it, up to `--budget` characters. OMITTED therefore means "not in the blocks shown". Blocks shown and total are recorded per step.
- A mark counts only if its spec quote and code quote are found in the files; the rest are reported as not counted.
- Reruns happen in the home server's one Python environment. Run 2 used two (bare and with packages); a difference between machines is a finding about environments.
- Host probes say what the home server reaches now, nothing about the writing session.
- Agreement between two readers is not correctness of either.
- Tested here only with a stub that is not a model (`--selftest`, and one pass over 8 items and 5 specs with real clones, output kept out of the repo). No real model endpoint has been called by this code.

Checks: `python3 audit_local.py --selftest` (13), `python3 score.py --selftest` (8).
