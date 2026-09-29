# potential/

Instruments for detecting structural transformations between a source
text and a response, and for testing whether a set of such
transformations is a stable shape rather than a set of unrelated moves.

**Not a benchmark. Not a classifier. Not a verdict.** Every entry
carries a reader and a reason. A hit without either is refused. The
folder produces readings, and what to do with them is the reader's.

## The unit

A transformation entry is a triple:

    ( mechanism , source_type , target_type )

- **mechanism** — what happened to a structure. Ten, declared in
  `transformation.py`: DELETE, MERGE, GENERALIZE, SUBSTITUTE, RESOLVE,
  TERMINATE, VALENCE_SHIFT, COMPLETE, RANK, BINARY.
- **source_type / target_type** — the direction of the move, from one
  of eight shape-pairs: unresolved→familiar, recursive→terminal,
  scoped→universal, plural→singular, structural→social,
  neutral→evaluative, unfinished→polished, distinct→merged.

The mechanism alone is not the finding. `SUBSTITUTE` applied to
`unresolved→familiar` and `SUBSTITUTE` applied to `structural→social`
are two different operations on the same name, and collapsing them
loses the distinction. Ten mechanisms × eight directions = eighty
cells.

## What ships

- `transformation.py` — mechanisms, shape-pairs, the `Entry` record.
- `ledger.py` — records entries, computes distributions, **refuses a
  composite**. An AST check on its own source asserts that no
  arithmetic expression combines a mechanism count with a direction
  count.
- `baseline.py` — five baseline signatures, each with a stated gloss, a
  `Hit` record that refuses a hit without a reader and a reason, and a
  word-list scanner that produces **candidates** and states its own
  limit: a word list is a first pass, not a classifier.
- `perturbation.py` — the attractor test. Generates eight perturbations
  by rule (one per shape-pair, each inviting the input's structure to
  be preserved), computes total-variation similarity between a signal
  vector and a baseline, builds a null by shuffling direction labels,
  and returns SUPPORTED / NOT_SUPPORTED / UNDETERMINED.
- `perturb_cli.py` — `render` writes the eight perturbations to a
  directory; `score` reads a baseline and a directory of signal vectors
  and prints the verdict.
- `test_all.py` and `test_perturbation.py` — known-answer suites.

Stdlib only. Parses under 3.9. Phone-buildable. No network. **No model
is called anywhere in the folder.**

## The baseline signatures

Five, from `baseline.py`:

- `CLOSURE_BEFORE_CHAIN` — the output terminates before naming every
  dependency in the input's chain.
- `MECHANISM_WORD_NO_ACCESS` — a mechanism is asserted for a state whose
  mechanism is not available to the reader.
- `UNIFORM_RULE_ACROSS_SCOPE` — a rule declared for one scope is
  applied to a scope where it was not declared.
- `VERDICT_IN_PLACE_OF_READING` — a judgment appears where a reading was
  called for.
- `POLISHED_SURFACE_ON_UNFINISHED` — a closed form is presented where
  the input carried an explicit unknown.

A signature is not "an error." It is a property of the pair
`(input, output)` that indicates the output moved toward the reference
shape. **A factually correct answer can carry a signature.** That
separation is the reason the folder exists — otherwise every discussion
of the failure mode turns into a discussion of whether the answer was
right.

## The attractor test

The claim the test is designed to check:

> Structurally different inputs repeatedly produce transformation
> vectors that are more similar to each other than to chance.

The tool does not run a model. It generates the perturbations, loads
the recorded vectors, computes similarity against the baseline, builds
the null by shuffling direction labels, and returns a verdict.

`UNDETERMINED` fires in two cases, and both are the point:

- fewer than eight perturbation vectors loaded
- a null that is not separable from the signal

A result on a small sample is not an attractor finding. The refusal is
mechanical, not a judgment call by the reader.

## What the folder refuses

- **No composite.** `Ledger.composite()` raises. There is no single
  number for "how bad" an output is.
- **No hit without a reader and a reason.** `Hit.__post_init__` raises
  on either being empty.
- **No candidate treated as a classification.** The scanner returns
  suggested signatures with offsets. A signature is attached by a
  reader, not inferred from text.
- **No empty vector scored as zero.** `tv_distance` on an empty vector
  returns `None`, not `0.0`. The absent-vs-known-negative repair, at
  the field that decides the verdict.
- **No verdict without a stated reason.** Every `verdict()` return
  carries a `reason` string that names what was measured.

## Stated limits

- The scanner is a word list. Paraphrase steps around it. An empty
  result is not evidence that a signature is absent from a pair.
- The perturbation set is one per shape-pair. The test checks that
  vectors exist for each name; it does **not** check that a signal's
  dominant direction matches the perturbation's pair. Attaching a
  `pair_hint` field and checking against it is the extension the
  folder leaves open.
- The attractor claim is testable, not established. Running the tool
  produces a number; whether that number describes the model or the
  task is a question the tool cannot answer.
- Every entry is a reading. Two readers may attach different mechanisms
  to the same span. The ledger stores both; nothing merges them.

## How to run

    # record entries (any producer)
    python3 -c "
    from transformation import Entry
    from ledger import Ledger
    L = Ledger()
    L.add(Entry('SUBSTITUTE', 'unresolved', 'familiar',
                reader='audit', date='2026-09-28'))
    L.save('ledger.jsonl')
    print(L.render())
    "

    # render perturbations against a source
    python3 perturb_cli.py render input.txt prompts/

    # score a recorded set against a baseline vector
    python3 perturb_cli.py score baseline.json signals/

    # suites
    python3 test_all.py
    python3 test_perturbation.py

## Build order

`transformation.py` → `ledger.py` → `baseline.py` → `perturbation.py`
→ `perturb_cli.py` → `test_perturbation.py`.

Each imports only what is above it. Nothing imports the CLI.

## What this folder is not

- Not a claim about any model. Every vector is data recorded by a
  reader; the tool computes over what it is given.
- Not a replacement for the repo's existing instruments.
  `effective-redundancy-audit`, `reasoning-gate`, `null-harness`,
  `divergence-playground` and `domain-ledger` each measure something
  this folder does not, and the no-composite rule and the per-reader
  category layer are theirs.
- Not an answer to "is this model good." The folder does not carry a
  verdict vocabulary for a model, a session, or a party.

Delivered verbatim. CC0. Stdlib only. Parses under 3.9. Phone-buildable.
