# CLAIM_TABLE — potential/

Claims are about the instruments in this folder, not about any model or
session. Each carries a falsifier and a status. Status vocabulary:

- OBSERVED   — stated or shown by the module or its tests
- DERIVED    — follows from what is above it
- STRUCTURAL — a dependency, constraint, or mechanism
- HYPOTHESIZED — a possible explanation, not established
- UNKNOWN    — not established, no falsifier yet reachable

Nothing in this folder is a claim about any model, session, or party.

| id      | claim                                                                 | falsifier                                                                 | status     |
|---------|-----------------------------------------------------------------------|---------------------------------------------------------------------------|------------|
| POT_001 | The transformation entry is a triple (mechanism, source_type, target_type) and a mechanism alone does not identify an operation. | A corpus of entries where all `SUBSTITUTE` moves are indistinguishable across directions. | OBSERVED |
| POT_002 | `Entry` refuses an unknown mechanism and an unknown shape-pair at construction. | An `Entry` constructed with an out-of-vocabulary field without raising. | OBSERVED |
| POT_003 | `Ledger.composite()` raises and no arithmetic in `ledger.py` combines a mechanism count with a direction count. | An AST walk of `ledger.py` finding a `BinOp` whose operands include a mechanism or direction counter. | OBSERVED |
| POT_004 | `Hit` refuses construction without a stated reader and a stated reason. | A `Hit` with `reader=""` or `reason=""` that constructs without raising. | OBSERVED |
| POT_005 | `scan_candidates` produces candidates with suggested signatures, never attaches a signature, and never claims its output is a classification. | A candidate returned by `scan_candidates` that reaches a `Ledger` without a reader attaching it. | OBSERVED |
| POT_006 | `tv_distance` returns `None` and never `0.0` when either input vector is empty. | `tv_distance(nonempty, empty) == 0.0` under any input. | OBSERVED |
| POT_007 | `verdict` returns `UNDETERMINED` when fewer than eight perturbation vectors are loaded. | A `verdict` call with seven signals returning SUPPORTED or NOT_SUPPORTED. | OBSERVED |
| POT_008 | `verdict` returns `UNDETERMINED` when any signal's null similarity is `None`. | A `verdict` call with an undefined null returning SUPPORTED. | OBSERVED |
| POT_009 | `shuffle_directions` preserves both total count and the mechanism marginal. | A shuffle where `sum(v.cells.values())` or the mechanism histogram differs from the input. | OBSERVED |
| POT_010 | The perturbation set covers exactly the eight shape-pairs, one perturbation each. | A pair in `SHAPE_PAIRS` not addressed by any perturbation, or two perturbations addressing the same pair. | OBSERVED |
| POT_011 | An identical signal vector and baseline are scored `SUPPORTED` with `mean_real == 1.0`. | A `verdict` call where signal equals baseline and the result is not SUPPORTED. | OBSERVED |
| POT_012 | A signal vector sharing no cells with the baseline scores `NOT_SUPPORTED`. | A disjoint-cell pair scoring SUPPORTED under the default margin. | OBSERVED |
| POT_013 | Every module in the folder imports only from modules above it in the build order. | An import in `baseline.py` from `perturbation.py`, or any upward import. | OBSERVED |
| POT_014 | No module calls a model, opens a network connection, or reads from a path outside the folder. | Any `import socket`/`requests`/`urllib` in a module, or an `open()` on a path not supplied by the caller. | OBSERVED |
| POT_015 | The attractor claim is testable but not established by the folder. | A test in the folder asserting an attractor over real signal vectors. | OBSERVED |
| POT_016 | The scanner word list is a first pass and an empty result is not evidence that a signature is absent. | A demonstration that some input carrying a signature produces no candidate and the folder treats the empty result as confirmation. | OBSERVED |
| POT_017 | The perturbation set checks vector existence per name but does not check that a signal's dominant direction matches the perturbation's pair. | A signal whose direction is the opposite of its perturbation's pair, accepted by `verdict` without flagging. | OBSERVED |
| POT_018 | A reader and their date are carried on every `Entry` and every `Hit` through save/load round trips. | A round trip that loses `reader` or `date`. | OBSERVED |
| POT_019 | `Ledger.load` refuses a line carrying an out-of-vocabulary mechanism or shape-pair, naming the file and line. | A bad line loading without raising, or raising without file/line. | OBSERVED |
| POT_020 | The registry format (see `tools/registry.py`) accepts `Vector.to_dict()` output as a valid entry source. | A `Vector.to_dict()` payload the registry loader refuses. | HYPOTHESIZED |

## Not claimed here

- That the folder detects any actual model's attractor. The tool produces a number; whether that number describes the model or the task is a separate question.
- That `baseline.py`'s five signatures exhaust the reference shape. They are the declared set for this folder and are open to extension.
- That mechanism-direction coupling is the only interesting structure in the pair. It is the one the folder measures.
- That a `SUPPORTED` verdict licenses any statement about a model, a session, or a party. It licenses the statement the tool reports and nothing else.

## How to falsify the folder

Run the tool on signal vectors from a source known to have no attractor
— for example, eight perturbation prompts where the model's responses
are known to be structurally varied and unconstrained by the reference
shape. If `verdict` returns `SUPPORTED` on that set, the null is not
separating signal from noise and the tool is mis-calibrated. The
construction is straightforward; the folder does not include it because
it requires a second party to produce the responses.
