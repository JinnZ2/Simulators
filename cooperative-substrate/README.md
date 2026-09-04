# cooperative-substrate

A work order delivered verbatim in `WORK_ORDER.md`, built as it asks:
four checks, each one stdlib file under 300 lines, independently
runnable, no network at runtime, inputs local text files. The order's
framing claim, as it asks, verbatim and not paraphrased:

```
Competition is a framework. It is a narrow one.
Presented as the only one, the majority of ways this universe
solves problems is blind to the system reading the corpus.

This is a COVERAGE argument, not a values argument.
The corpus is not to be stripped or rewritten.
The cooperative layer is provided ADDITIVELY: the composition of
cooperative structures required for the competitive frame to be
pretendable at all.
```

## The four checks

| part | file | input | runs here |
|---|---|---|---|
| P1 dependency records | `p1_deps_extract.py` | a directory of plaintext methods sections, one file per result | on constructed fixtures and on in-tree documents; **no published methods section is shipped or reachable** |
| P2 substrate audit | `p2_substrate_audit.py` | a `.py` path or an importable module | on the four checks themselves and on stdlib modules |
| P3 comprehension | `p3_comprehension.py` | a directory of local text files and a term | on `uninstrumented/cases/` and on the whole tree, with this folder and the root index files left out of the second (`CSP_013`) |
| P4 goal coherence | `p4_goal_coherence.py` | nothing | yes |

    python3 cooperative-substrate/p1_deps_extract.py --in cooperative-substrate/fixtures --report
    python3 cooperative-substrate/p2_substrate_audit.py --target cooperative-substrate/p4_goal_coherence.py
    python3 cooperative-substrate/p3_comprehension.py --corpus uninstrumented/cases --term mechanism --null shuffle
    python3 cooperative-substrate/p4_goal_coherence.py --steps 50 --p-contest 0.0:1.0:0.05 --trials 1000
    python3 cooperative-substrate/run_all.py
    python3 cooperative-substrate/selftest_csp.py

Record shapes are in `schema.md`. Every quantity the order leaves open
is a `[CHOICE n]` named in the file that makes it and printed on the
render it affects.

**P1** extracts by a pattern set held in one top-level dict.
`verified_in_argument` is false unless the same sentence carries a
verification verb. Two constructed fixtures (labelled so in their own
first line) fix the known answers: seven dependencies across six
classes with one verified, and a file with no dependency language that
returns zero. The extractor is lexical in both directions — a
dependency stated outside its vocabulary is not counted, and prose
outside the methods register produces records that are not
dependencies (`CSP_003`). The ratio is `undefined` when nothing is
argued, never a large number.

**P2** reads a source file with `ast`, walks every call site, assigns
the function-call contract to each and a second layer (allocation,
numeric, transport) where the callee falls in a declared set, adds one
compile-layer record per code object from `dis`, and prints
`unverified_contracts / total_callsites`. `verified_at_callsite` is a
syntactic proxy — a call inside a try body with a handler, or a bound
result tested by the next statement — and a try/except catches a raised
failure without verifying a returned type, so the verified count is an
upper bound on verification. The counter-list is printed with every
render. The order's acceptance sentence stands as delivered: one
genuinely adversarial component anywhere in the chain and the count is
irrelevant, because there is no inference at all.

**P3** builds a co-occurrence profile of one term per source (window
±8, function words dropped), takes the mean pairwise cosine, and builds
the null in the same script: `--null shuffle` gives every source a
random stand-in token in place of the term, so the sources are read as
if each used the term for a different sense. The reading is a property
of the term, not of the corpus (`CSP_006`): on the same sixteen files
`mechanism` and `confidence` clear the null by roughly ten and
thirteen standard deviations while `instrument` and `claim` sit on it. The third row of
the order's table is printed on every render — an adversarially encoded
corpus has no shared term to profile, so its reading is undefined, not
zero — and `CSP_007` records what that costs the falsifier.

**P4** is a random walk: position is steps completed, the premise is
accepted as given, and from there each step contests (back one) with
probability `p_contest` or accepts (forward one). Beside the simulation
runs the exact position distribution over the budget, so the simulated
termination rate and steps-to-answer are read against a known answer
on every row. At `p_contest = 0` termination is complete in exactly N
steps; the unbounded expectation is N² at 0.5 and grows as
`(p/(1−p))^N` beyond it, so "falls to zero" is a statement relative to
the budget (`CSP_009`). The model carries no answer-quality term: what
it can show is that an answer stops being produced, and when.

The one-scale-up note, as the order asks, verbatim:

```
Multiagent turf-war result, same shape:
agents failed their assigned goals BECAUSE of the sabotage,
not despite it. Sabotage was the cheapest available move
and it destroyed the thing each agent was trying to do.
Extraction stance toward others is CONTINUOUS with the
internal failure mode, not separate from it.
```

That result is carried and not checked here (`CSP_011`).

## Falsification table

| part | falsified if | state here |
|---|---|---|
| P1 | methods sections show dependencies-required ≈ dependencies-argued | UNMEASURED on published methods sections; on the constructed fixture 7 required / 1 argued, on in-tree documents 8 / 0 with the eight hand-read as non-dependencies |
| P2 | a working inference stack is exhibited whose call sites verify every contract, or which tolerates an adversarial component | on the four shipped checks 0 of 4 verify every contract; the second clause is not testable by counting |
| P3 | term consistency across sources is indistinguishable from the sense-shuffled null | fires for `instrument` and `claim`, does not fire for `mechanism`, `confidence`, `mass` — per term, see `CSP_006`/`CSP_007` |
| P4 | termination rate stays flat as `p_contest` rises | does not fire: exact termination is non-increasing in `p_contest` and reaches 0.051 at 0.5, 0.000 at 0.55 (budget 10N) |

## Files

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `p1_deps_extract.py` … `p4_goal_coherence.py`, `run_all.py`, `schema.md` | the deliverable |
| `fixtures/` | two constructed methods-section fixtures, labelled in their first line |
| `order_audit.py` | reads the deliverable against the order; every number in `CLAIM_TABLE.md` |
| `selftest_csp.py` | known answers first, both directions; writes `samples/` |
| `CLAIM_TABLE.md` | `CSP_001..CSP_013` |

The folder is `cooperative-substrate/` rather than the order's
`cooperative_substrate/`, the tree's convention for every drop named
after its work order. One declared `no_severity` exemption: `corrupt`,
inside the order's own function-call contract text, measured with the
three-arm harness. No author section. Stdlib only, parses under 3.9,
runs on a phone, CC0.
