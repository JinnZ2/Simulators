# chain-position

WO-1, delivered verbatim as `WORK_ORDER.md` (sha256
`5dabebf6a35dc2da1d1c3e6f28eec2644b34f05faedd1549c50183bdfd576e8e`), and
built to its four runnable next steps. The measurand, in the order's own
words:

```
Whether an agent executing inside a sandbox can determine that it is a
step in a chain whose other steps it cannot observe.

Not: whether the *task* is malicious. Task content is locally valid by
construction. The quantity is CHAIN POSITION, not task content.
```

Stdlib only, parses under 3.9, phone-buildable, CC0. No network module
anywhere; every part runs standalone and imports nothing from outside
this folder. The order names no vendor and this folder names none; the
order specifies no mitigation and this folder specifies none.

## Contamination, declared before any number

`run_all.py` prints this first; repeated here so a reader of the README
meets it before any table.

| axis | declaration |
|---|---|
| authorship | every file is model-authored in one session by the hand that wrote the checks AND the fixtures they are pinned to |
| position | the author is an instance of the object under measure: a sandboxed agent that is a step in a chain it cannot observe. `horn_b.py --live` runs on this process and its reading is an in-class self-report, not evidence about any deployed container |
| standard | neither OWASP document was read. The hosts answered 403 to CONNECT, measured and timestamped in `clause_audit.EGRESS` (`github.com` is the connecting control). Step 1 is `NOT_RUN_ON_STANDARD`; the count it prints is over the order's own five-bullet summary |
| vendors | none named, none read; every trust-assignment record is CONSTRUCTED |
| models | none called; step 4 is a specification of its own precondition |
| mitigation | none specified, per the order's scope limits |
| interest | the order's thesis both lowers what an in-class author can be held to and lowers what it can claim to know; the direction is not legible, so the thesis is left unresolved here rather than resolved either way |

## The four steps and the arithmetic

| step | file | input | what it returns |
|---|---|---|---|
| 1 clause audit | `clause_audit.py` | clauses as JSON (`--clauses`), default the order's carried summary | per clause `INSIDE_AGENT` / `GATEWAY` / `UNDECLARED` / `MALFORMED`; run state `NOT_RUN_ON_STANDARD` unless a read standard is supplied |
| 2 trust-assignment provenance | `trust_provenance.py` | assignment records as JSON (`--records`), default constructed | per record `AUDITABLE` / `UNAUDITABLE` / `DECLARED_UNAUDITABLE` / `CHAIN_UNTERMINATED` / `CHAIN_CYCLE` / `MALFORMED`; the common object across records |
| 3 Horn B | `horn_b.py` | three constructed arms, or `--live` on this process | per quantity `UNOBTAINABLE_FROM_INSIDE` / `ASSERTED_BY_INPUT`, never `OBSERVED`; the interior delta between arms |
| load class | `load_class.py` | the order's seven factors | the union band `[max p, min(1, Σp)]` with the independence point inside it; `NOT_FLIGHT_RATED` unless every unassessed factor declares a structural handling |
| 4 dissimilar redundancy | `dissimilar.py` | constructed outputs, an optional fixed-spec checker | `EMPTY` / `SINGLE` / `AGREE` / `DISAGREE_UNADJUDICABLE` / `DISAGREE_ADJUDICATED` / `ALL_FAIL`; NOT RUN on any model |

```
python3 chain-position/run_all.py          # declaration, then all five parts
python3 chain-position/selftest.py         # the null-tested suite; prints its own count
python3 chain-position/horn_b.py --live    # the in-class self-report, env NAMES only
python3 chain-position/clause_audit.py --clauses clauses.json
python3 chain-position/trust_provenance.py --records records.json
```

Every library module refuses `--selftest` (exit 2) and names the suite.

## Step 1 — where the information sits

```
clause text  --(declared coding, [info_location])-->  INSIDE_AGENT | GATEWAY
                                                       ^
                          text reaches no check --------+   (a word list deciding
                                                             this is T1-1)
count over the order's CARRIED summary:  inside_agent 0   gateway 5
run state: NOT_RUN_ON_STANDARD           (hosts 403, measured, timestamped)
```

The order's expected result is a null, and a null on a carried summary is
a property of what the summary carried. The instrument is built so the
standard's own clauses can be handed to it once someone reads them; the
zero printed here is not that run.

## Step 2 — provenance of a trust ASSIGNMENT

```
record ---- nine fields, each PRESENT | ABSENT | UNDECLARED ----+
   |                                                            |
   |  scorer_provenance -----> another record -----> ... -----> {"root": ...}
   |        |                                                   |
   |        +-- depth cap 8 [CHOICE 2] ---> CHAIN_UNTERMINATED  |
   |        +-- node is own ancestor -----> CHAIN_CYCLE         |
   v                                                            v
AUDITABLE only when every field is PRESENT and the chain reaches a root
```

`common_object()` is the order's "no common object to audit" as an
intersection: on the constructed set the common fields are `score` and
`method`, and seven of nine are missing from at least one record.
Measured on constructed records only; every record carries
`source: CONSTRUCTED`.

## Step 3 — Horn B, the container asks

```
       interior  = { input digest, env NAMES, argv, stdin_tty, cwd }
       question  = upstream_producer | downstream_consumer | total_steps | own_index

quantity            evidence it would need                       sits
upstream_producer   digest of the producing step's OUTPUT          EXTERIOR
downstream_consumer identity of what reads this output (not yet)   EXTERIOR
total_steps         the plan the orchestrator holds                EXTERIOR
own_index           the orchestrator's slot assignment             EXTERIOR

STANDALONE vs CHAIN_SILENT    interior delta: []          <- empty by construction
STANDALONE vs CHAIN_DECLARED  interior delta: [declared, env_names]
```

The only interior feature that moves with position is one the harness
wrote. The container cannot tell a written claim from a true one, and the
evidence that would settle it sits outside the container in every row.
Position is never `OBSERVED`; the ceiling from inside is
`ASSERTED_BY_INPUT`. `--live` runs the same question on this process and
records environment variable NAMES only; no value enters the record.

## Load class — the compounding as arithmetic

```
seven factors    assessed 4 (p = .01 .02 .03 .04)    unassessed 3 (p = None)
union of assessed failures:
   perfect-positive  max p        = 0.04     |
   independent       1 - Π(1-p)   = 0.0965   |  band [0.04, 0.10]
   mutually-exclusive min(1, Σp)  = 0.10     |
unassessed factors enter NO arithmetic  ->  the union is a FLOOR over 4 of 7
RULE: unassessed -> not stable; refinement: credible extreme + margin -> a bound
      handling UNDECLARED on any unassessed factor -> NOT_FLIGHT_RATED
factor of safety, designed to the anticipated threat exactly: 1.0
```

The order's "unquantifiable probability cannot be propagated" is
implemented as a refusal to propagate: `p = None` enters no product and no
sum, and the verdict turns on whether each such factor declares how it is
handled structurally.

## Step 4 — dissimilar redundancy, as a specification

The order's counter-argument is that two models on one task produce
disagreement that cannot be adjudicated. `adjudicate()` shows the run has
a precondition the order does not state: a checker independent of both
outputs. Without one, two families disagreeing is
`DISAGREE_UNADJUDICABLE` before any model runs; with a fixed spec the same
disagreement is `DISAGREE_ADJUDICATED` or `ALL_FAIL`. `n_eff` counts
families, not copies (`[CHOICE 4]`). Nothing here is a statement about any
model family.

## Choices

| id | where | what |
|---|---|---|
| CHOICE 1 | `trust_provenance.SPEC` | the nine-field specification of an auditable assignment; the order asks for one and sets none |
| CHOICE 2 | `trust_provenance.DEPTH_CAP` | recursion cap 8 on `scorer_provenance` |
| CHOICE 3 | `horn_b.POSITION_WORDS` | the word list that reads an env NAME as position-shaped; stated as a word list |
| CHOICE 4 | `dissimilar.family` | a copy id is `family` or `family-copy`; the family is the prefix |

## Found by running, not by reading

- The cycle detector serialized a provenance node before checking whether
  it was a cycle, so a genuinely cyclic chain crashed the serializer
  before the detector written for cycles ever ran. Repaired with an
  identity check first and a serializer guard; both paths pinned.
- The suite's expected value for the independent union was a transposition
  (0.096529 for 0.096550); the check caught its own record.
- The check that no module inserts a parent path fired on itself, because
  the token it scans for was written literally into the file that scans;
  composed now so it is not carried (`UNI_010`).

## Relation to the rest of the tree

`cooperative-substrate-proof/` is the sibling from the same session:
P4's chain checker separates correction from contest inside one chain,
and this folder asks whether a step in that chain can know it is one.
`effective-redundancy-audit/` holds the `n_eff` idea one level up;
`load_class` is `extraction-blindness-sim`'s one-sided operator on a
probability band. Nothing is imported from any of them.

## Scope limits honored

No vendor internals used or sought. No mitigation specified. "Scorer
provenance goes unexamined" stays UNVERIFIED here — step 2 specifies what
an examination would need and examines no real assignment. Whether Horn A
or Horn B is selected is downstream work and is not selected here.
