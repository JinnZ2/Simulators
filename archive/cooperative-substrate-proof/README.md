# cooperative-substrate-proof

```
Competition is a framework but a narrow one.
This artifact shows the cooperative substrate
required for the competitive frame to be
possible at all. Coverage argument, not
values argument. Do not strip the competition
frame. Add the layer underneath it.
```

That block is the dispatch's load-bearing framing, verbatim, at the top
as it asks. The dispatch itself is `DISPATCH.md`. Stdlib only, CC0,
phone-buildable, no network module anywhere, every part runs standalone
and imports nothing from outside this folder.

## Contamination, declared before any number

`run_all.py` prints this first; it is repeated here so a reader of the
README meets it before the table.

| axis | declaration |
|---|---|
| authorship | every file is model-authored in one session by the hand that wrote the checks AND the fixtures they are pinned to |
| position | P2, P3, P4 are run by a system of the class whose substrate, corpus and chain they check; a pass is an in-class self-report, not evidence about any deployed model |
| fixtures | every input marked CONSTRUCTED was written so its answer is known; no published methods section, study, trial or multi-agent run is read |
| egress | no publisher host is reachable; the P1 open-access pipeline is a paste path, not a fetch |
| repository | `JinnZ2/cooperative-substrate-proof` was to be created; the integration credential is refused (`403` on `POST /user/repos`), so this lands as a self-contained folder that imports across no boundary |
| interest | the framing claim lowers scrutiny of a system that agrees with it; the checks establish NECESSARY conditions, and no coverage share is measured anywhere here |

## The five parts and the coder

| part | file | input | what it returns |
|---|---|---|---|
| P3 comprehension | `p3_comprehension.py` | files, stdin, or `--self` | `CONVERGENT` / `INDISTINGUISHABLE_FROM_NULL` / `NOT_EVALUABLE` / `TOO_SHORT` / `EMPTY` |
| P4 goal coherence | `p4_goal_coherence.py` | a chain as JSON, or nothing | `COHERENT` / `CORRECTED` / `NO_ANSWER` / `DANGLING` / `EMPTY` / `MALFORMED`; plus the exact turf war |
| P2 substrate | `p2_substrate.py` | a `.py` path, default itself | `SUBSTRATE_HOLDS` / `SUBSTRATE_ASSUMPTION_VIOLATED(layer)`; sha256 of the source it ran on |
| P1 dependency records | `p1_dependency_records.py` | a methods text and an argument text | records, each `SOURCED` / `UNSOURCED`; ratio unargued/argued, `undefined` at zero argued |
| P5 lag declaration | `p5_lag_declaration.py` | actions as JSONL, default anchors | per action `TRACKED` / `DECLARED_UNKNOWN` / `UNDECLARED`, plus its C1 code |
| C1-C4 coder | `scope.py` | cases as JSONL | `ADMISSIBLE` / `OUT_OF_SCOPE` / `UNDETERMINED` / `MALFORMED` |

    python3 run_all.py                     # declaration, then P2 P3 P4 P5 P1
    python3 selftest.py                    # prints the check count; every check null-tested
    python3 p3_comprehension.py --self
    python3 p3_comprehension.py --paths a.txt b.txt c.txt
    python3 p4_goal_coherence.py --chain my_chain.json
    python3 p2_substrate.py --target some_module.py
    python3 p1_dependency_records.py --methods methods.txt --argument results.txt
    python3 p5_lag_declaration.py --actions actions.jsonl
    python3 scope.py --cases coded_studies.jsonl

Every refusal is a typed state in the return, never an exception. Every
library module refuses `--selftest` with exit 2 and names `selftest.py`.

## P3 in one picture

```
corpus ---- split into parts ----+---- shared map:  one pseudo-word map, every part   -> r_shared
                                 |
                                 +---- private map: one pseudo-word map PER part      -> r_private
                                       (within-part consistency kept; cross-part
                                        sharing destroyed)  [CHOICE 2]  = the null
gap(seed) = r_private - r_shared, paired;  mean gap > 3 sd  ->  CONVERGENT   [CHOICE 3]
```

Both arms replace every word with a same-length pseudo-word, so the
letter-level entropy is identical and the ONLY difference is whether
the map is shared across parts. A first version compared the private
arm against the raw corpus and read a disjoint-vocabulary corpus as
CONVERGENT, because random letters compress less well than real words
whatever the sharing. That is recorded in the module rather than
removed. The limit is stated at the top of the file: compressibility is
a NECESSARY condition for shared meaning and not evidence of it; a
single sentence repeated is maximally convergent and says nothing.

## P4 in one picture

```
step: {id, takes[], produces, contests[], reason}
  takes an id no earlier step produced       -> DANGLING
  contests + produces + reason               -> CORRECTION  (chain terminates)
  contests, no replacement                   -> CONTEST     (rejected output has no successor)
any CONTEST                                  -> NO_ANSWER, final = None

turf war: k agents, absolute goals of n steps, cheapest move each turn
  c_sab <  c_adv -> every agent sabotages, nobody advances: completed 0 at ANY budget
  c_sab >= c_adv -> every agent advances: k of k complete at turn n
```

The type has no answer-quality axis: a self-contesting chain returns NO
answer, not a lower-scoring one. The turf war is exact and its result is
a property of the construction (absolute goals, cost-only choice); the
dispatch's own turf-war case is carried, not read.

## P2 in one picture

```
target source --ast--> every call site; verified iff try-wrapped or bound name tested next  [CHOICE 8]
live layers on THIS interpreter: memory (granted or MemoryError, no negotiation) | numeric
  (IEEE 754 binary64) | scheduler (lock honoured) | compiler (code objects, instructions) |
  network (local socketpair, no egress) | hardware (byte order, struct round trip)
chain_demo(faithful=True) -> OUTPUT 7 ;  one planted link -> NO_OUTPUT (typed)
report carries sha256(source): a second run has to reproduce every count
```

## C1-C4

`scope.py` codes each condition three ways: `PRESENT`, `ABSENT`,
`UNCODED`. `UNCODED` is not `ABSENT`: a case nobody coded on C3 has not
been shown to lack a narrow metric, so it lands `UNDETERMINED`, never
`OUT_OF_SCOPE`. C1 is derivable from P5's two clocks (`t_scored <
t_coupling`, `[CHOICE 1]`) and is the one condition with an instrument
here; C2-C4 are hand codes. No study corpus is coded in this folder;
the pass runs on three CONSTRUCTED cases that reach the three states.

## Choices

| id | where | what was open |
|---|---|---|
| 1 | `scope.py` | C1 from clocks: PRESENT iff `t_scored < t_coupling` |
| 2 | `p3_comprehension.py` | the null is a private pseudo-word map per part |
| 3 | `p3_comprehension.py` | margin: mean paired gap has to clear 3 sd |
| 4 | `p3_comprehension.py` | under 512 bytes is `TOO_SHORT` |
| 5 | `p3_comprehension.py` | one part is `NOT_EVALUABLE`, never a pass |
| 6 | `p3_comprehension.py` | 12 seeds for the null spread |
| 7 | `p4_goal_coherence.py` | the turf-war cost table is the input; anchor row `c_sab < c_adv` |
| 8 | `p2_substrate.py` | "verified" is a syntactic proxy and over-reads |
| 9 | `p1_dependency_records.py` | the pattern set is one dict and a word list |
| 10 | `p5_lag_declaration.py` | the ratio threshold is 10 |

## Relation to `../cooperative-substrate/`

That folder holds two earlier builds of the same subject (v1 and v2).
This folder is a third, built to a new dispatch as a promotable unit,
and imports nothing from it; a copy that could drift is the thing
`tools/check_gate_drift.py` exists to catch. The instruments differ:
P3 there is a co-occurrence cosine, here it is compressibility (the
dispatch's own word); P4 there is a random walk, here a chain checker
plus an exact turf war; P2 here adds the live layer checks; P5's three
states were rebuilt without reading the earlier file and came out the
same shape, which is one builder converging with itself and not two
confirmations. Claims are in `CLAIM_TABLE.md` (`CSF_` ids).
