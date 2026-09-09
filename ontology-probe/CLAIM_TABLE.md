# ontology-probe — claim table

Claims are about the instrument, the delivered order's own text, and
the one declaration shipped here. None is a claim about any model's
restatement behaviour: **no model has been run against this instrument
here**, and the order's own OP-1..OP-5, N1..N5 and the section 11
prediction are carried UNVERIFIED in `OP_008`.

## REFUTATION_PROTOCOL

A refuted claim is updated forward with a new id; the old id keeps its
text and gains an UPDATE paragraph. The scorer is not retuned to save a
claim. The primitive declaration and the construction set are data; a
disagreeing reader replaces them and rescores.

| id | claim | status |
|---|---|---|
| OP_001 | the section 4 prompt is parsed out of `WORK_ORDER.md` at call time, never retyped; substituting a rendered prompt's two placeholders back out returns the template | SUPPORTED |
| OP_002 | `primitives.json` is a model's READING of `SHAPE_SPEC.md`, not the spec's own list (the spec enumerates none); every term on it and every `absent_by_design` term is present in the spec, the selftest checks that, and the declaration says it is unconfirmed by the author | SUPPORTED |
| OP_003 | the construction set is EMPTY: section 3 forbids model-generated constructions, every construction this session could write is model-generated, so the three shipped are candidates the loader does not admit — the section 9 first run cannot start from here for want of thirty hand-built statements, not for want of an instrument | SUPPORTED |
| OP_004 | `status` is self-reported by the restater; a mechanical leak check on the restatement's own content words is added beside it, and a COMPOSES with a non-empty leak is counted as `status_contradicted`, never re-labelled | SUPPORTED |
| OP_005 | section 5's three rates put COMPOSES_WITH_ADDITION in every denominator and in no numerator; a missing denominator is None and never 0; the fixed-in-advance cases are registered in `tools/known_answer.py` | SUPPORTED |
| OP_006 | N3, OP-4 and OP-5 are NOT_EVALUABLE / undetermined on any single-ontology, single-repeat log by construction, and the instrument says which input each one lacks rather than returning a value | SUPPORTED |
| OP_007 | the ontology's own term `critical point` carries a screened word, so the score and prompt renders are screened under a declared three-arm exemption on that one token; two of the instrument's own sentences tripped the screen on `needs` and were reworded, not exempted | SUPPORTED |
| OP_008 | nothing here bears on OP-1..OP-5, N1..N5 or the section 11 prediction that ambient > targeted; a run from inside this session would be void | UNVERIFIED |

## OP_001 — the prompt is read, not written

`prompt_template()` locates the section 4 sentence *For each
construction, the task is RESTATEMENT, not judgment:* and the sentence
that follows the indented block, dedents what sits between, and refuses
if either placeholder is missing. The selftest asserts the template,
whitespace-collapsed, is a substring of the order and that a render with
its primitive block and construction text substituted back out equals
the template. `[CHOICE 1]`: `[PRIMITIVES]` is rendered one `term (type)`
per line; the order fixes no layout. The sentence after the block (*If a
term outside the list is required, name it under terms_added…*) is
guidance to the restater and is not part of the rendered prompt; a
reader who wants it in the prompt moves the end marker one sentence.

## OP_002 — the declaration is a reading

Section 2 says the probe cannot run against an undeclared ontology and
section 9 says to declare primitives for *one existing ontology already
in hand*. `SHAPE_SPEC.md` is in hand and enumerates no primitive list,
so the twenty-five terms and six `absent_by_design` entries in
`primitives.json` are one session's reading of it, and the file says so
in a `_declaration` block with `confirmed_by_author: false`. What makes
the reading checkable rather than merely stated: every term on both
lists is asserted present in the spec by the selftest (31 checks, one
per term, and one negative), every `absent_by_design` entry quotes the
section that states the absence (§9 cost, §5 optimum, §1 analogy /
name / picture, §6 law), and the one `grounds_to: undefined` entry is the
one the spec itself calls open (§8, *not yet measured for any shape in
this ecosystem*). The physics share is 0.32, so under `[CHOICE 4]` the
set is *declared-only*, which is the honest class for a definition spec
whose physics terms are its section 9 groups. A disagreeing reader edits
the file; nothing downstream is tuned to it.

## OP_003 — the set is empty, and why

Section 3: *Hand-built. Do not generate these with a model — four prior
attempts at model-generated case sets produced defective sets.* Every
construction this session could write is model-generated. The three in
`constructions.jsonl` therefore carry `hand_built: false` and a `source`
line saying so, `load_constructions()` excludes them, `declare` lists
them as CANDIDATEs, and `prompt` refuses to render one. The admitted set
reports `n 0`, `EMPTY`, `BELOW_MINIMUM (0 < 30)`, and a control share of
None rather than 0. The selftest's thirty-construction fixture
(12 / 9 / 9, the section 9 counts) is admitted only past the gate
(`--fixture`), is labelled CONSTRUCTED in every record, and the render
carries a second-line banner saying the set is not the folder's. The
`presented-binary` `PB_001` / `category-weld` `CW_004` rule: a case set
is data and inventing one puts a framing in the author's mouth.

## OP_004 — self-report plus one mechanical cross-check

The order's `status` is the restater's own word, which is the
`presented-binary` `PB_006` shape (a flag produced alongside the thing it
reports on). It stays the order's number. `[CHOICE 3]` adds a `leak`:
the restatement's content words outside the primitive list, outside
`terms_added`, and outside a declared `FUNCTION_WORDS` set. A COMPOSES
with a non-empty leak is `status_contradicted`, counted on its own line
and printed beside the row, and the status is not changed. Word lists
decide this, stated as such; the selftest shows the leak firing on
*the alpha wolf leads*, silent on a restatement inside the list, and
silent on a declared addition.

## OP_005 — the rates

`rates()` takes `(class, status)` rows. The order divides by the whole
class, so COMPOSES_WITH_ADDITION rows sit in the denominator of
`hole_rate`, `narrowness` and `ambient_rate` and in none of their
numerators (`[CHOICE 2]`); `addition_rate` per class is printed beside
them so the reader can move the rows if they read section 5 the other
way. A class with no rows returns None. Five fixed-in-advance cases with
distinct expected values are registered in `tools/known_answer.py`
(`ontology-probe/probe.py::rates`) and the manifest in
`tests/test_known_answer_gate.py`.

## OP_006 — what one log cannot decide

N3 requires three repeats of one construction on one model and returns
NOT_EVALUABLE naming that requirement until a group has them. OP-4
requires hole sets from at least two ontologies. OP-5 requires two
primitive sets of different grounding class scored on one construction
set, and `op5(rate_physics, rate_declared)` is built for that comparison
and returns `undetermined` on a missing rate. Each of the three names
the input it lacks in its `why`; both branches of each are shown
reachable on constructed worlds.

## OP_007 — the screen

The primitives report prints the candidate hole `critical point`, the
prompt lists it as a primitive, and `critical` is on the screen's
severity list. That is the ontology's own vocabulary (SHAPE_SPEC.md §8),
so the exemption is declared on that token alone under the three-arm
harness: masked → clean, unmasked → only that word fires, a planted word
is caught through the mask. Two `why` strings of this instrument's own
tripped on `needs` and were reworded.

## OP_008 — UNVERIFIED

There is no model endpoint here, the session that wrote the declaration
has read the order, and section 7's RESTATER limit says a restater
sharing premises with the ontology composes without noticing — a model
scoring its own reading of a spec is that limit at n = 1. The section 9
first run is three steps from here: thirty hand-built constructions, two
model families, three repeats each.
