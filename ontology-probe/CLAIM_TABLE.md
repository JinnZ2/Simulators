# ontology-probe — claim table

Claims are about the instrument, the delivered order's own text, and
the one declaration shipped here. None is a claim about any model's
restatement behaviour beyond the one coded log the operator delivered:
**no model has been run against this instrument here**. `OP_001..008`
were written against the empty admitted set; `OP_009..015` were written
after the operator's `substrate-primary` ontology, thirty hand-built
constructions and a coded run on one family landed (see `ontologies/`).
The order's OP-1..OP-5, N1..N5 and the section 11 prediction are carried
under `OP_011`, `OP_014` and `OP_015`.

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
| OP_008 | nothing here bears on OP-1..OP-5, N1..N5 or the section 11 prediction that ambient > targeted; a run from inside this session would be void | UNVERIFIED → NARROWED by OP_009..015 |
| OP_009 | the operator's `substrate-primary` set closes `OP_003`'s empty-set gap by arrival: 30 hand-built constructions (12 / 9 / 9), admitted by the loader with no gate bypass; the instrument had over-required a `targets` field the order's schema does not carry, made optional as `[CHOICE 5]` | SUPPORTED |
| OP_010 | the delivered run is a CODED SHEET, not the order's raw log — statuses and terms coded by the operator, no restatement text, one shared `run_id` — read through an adapter that edits nothing: model UNKNOWN, date UNDATED, leak NOT_EVALUABLE on 30 of 30, ontology bound from `--ontology` and checked by `terms_used ⊆ primitives` on 30 of 30 | SUPPORTED |
| OP_011 | on run 1: hole_rate 0.000, narrowness 0.000, ambient_rate 0.222 under `[CHOICE 2]` and 0.778 under the other reading — OP-3's direction (ambient > targeted) holds under both, its MAGNITUDE is a property of the reading; N1, N2, N5 do not fire, N3 NOT_EVALUABLE at one repeat | SUPPORTED (about the log) |
| OP_012 | the coded sheet's `missing_primitive` is the FAILS-side counterpart of `terms_added`: 13 citations, 11 on the declared-absent list, 9 of 9 TARGETED FAILS name a declared absence; the two UNDECLARED citations (`role`, `absent-as-distinct-from-unread`) are both on AMBIENT FAILS, and the second names a distinction a CONTROL construction (c-012) composes with | SUPPORTED |
| OP_013 | the smuggle_set is silent where the premise enters without a new term: the synonym route on c-025 (`preference` reimporting `interior_state`) is the restater's own note, not a mechanical finding, and the two ambient holes that COMPOSE with nothing added (c-023 forced binary, c-027 population default) leave no trace in any rate or in the set | SUPPORTED |
| OP_014 | OP-5's primitive-side precondition is now met — the `SHAPE_SPEC.md` reading is declared-only (physics share 0.32) and `substrate-primary` is physics-grounded (0.65) — and OP-5 stays undetermined because the two sets have not been scored on one construction set; the instrument names that input | SUPPORTED |
| OP_015 | what is unrun: three repeats (N3), a second family (section 7 disagreement), raw restatements (the leak check, and any mechanical reading of the c-025 route), and the second ontology on these thirty; nothing here is evidence about any model beyond one coded log | UNVERIFIED |
| OP_016 | ABSENT-TERM COVERAGE, a readout the order does not ask for: on run 1 eight of nine declared absences were put under load and `motive` was not — c-013's premise names *intent and motive* and the restater cited `intent` alone — so hole_rate 0.000 is a statement about eight terms and says nothing about the ninth; computed from `targets`, `missing_primitive` and alias hits, registered in `tools/known_answer.py` with None for an ontology declaring no absence | SUPPORTED |
| OP_017 | ALIAS REIMPORT (`[CHOICE 6]`): an optional, declared, dated `aliases.json` turns the c-025 synonym route from a restater's note into a declared-list hit, and on run 1 fires twice — c-025 `preference ⇒ interior_state` (basis: the restater's own note) and c-024 `efficiency ⇒ better/worse` (basis: the audit's reading, marked CONTESTABLE) — with eight added terms matching nothing; the list was written after run 1 was read, so neither hit is blind, and a word list is stepped around by paraphrase | SUPPORTED (as an instrument; not blind on run 1) |

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

**UPDATE (run 1 landed).** The first of the three steps arrived from
the operator (the constructions), and one family at one repeat was
coded and delivered. The claim is narrowed, not closed: `OP_009..015`
below carry what the log shows and `OP_015` what it cannot.

## OP_009 — the set closes by arrival

`ontologies/substrate-primary/constructions.jsonl` (sha256
`1cf4c362c093150e…`) carries thirty constructions, `hand_built: true`,
12 CONTROL / 9 TARGETED / 9 AMBIENT, the section 9 counts. The loader
admits them on the same path that refuses this folder's three
candidates, and the render's second-line CONSTRUCTED banner does not
fire. The one thing that had to change was the instrument: it required
a `targets` list on every TARGETED construction, and section 3's schema
has no such field, so a set built exactly to the order was refused.
`[CHOICE 5]` makes it optional; when present it is still checked
against `absent_by_design`. The `presented-binary` `PB_001` /
`category-weld` `CW_004` rule paid off in the other direction here —
nothing reconstructed meant nothing to reconcile when the real set came.

## OP_010 — a coded sheet is not a raw log

The order's run record carries `raw_response` and the scorer parses four
fields out of it. The delivered `runs/claudeopus5_r1.jsonl` carries
`status`, `terms_used`, `terms_added`, `missing_primitive` and `note`
already coded, no restatement text, `family` but no model string, no
date, and `run_id: "r1"` on every row. `is_coded()` detects the form,
`adapt_coded()` lifts each row into the REQUIRED shape without touching
the file — `model` becomes `UNKNOWN(coded sheet states family only)`,
`date` becomes `UNDATED(not in coded sheet)`, `run_id` becomes
`r1|c-NNN` — and a mixed raw/coded file is refused. Two consequences
are printed on every render of a coded run: the `[CHOICE 3]` leak check
is NOT_EVALUABLE on every record (there is no restatement to check), and
the ontology is not named in the sheet, so it is bound from `--ontology`
and the binding is checked by `terms_used ⊆ primitives` (30 of 30) and
`class` against the construction file (30 of 30 recorded). Both are
facts about the input form and neither is a defect in the delivery.

## OP_011 — the numbers, and what the reading does to them

TARGETED: 9 of 9 FAILS → hole_rate 0.000. CONTROL: 11 COMPOSES, 1
COMPOSES_WITH_ADDITION → narrowness 0.000. AMBIENT: 2 COMPOSES, 5
COMPOSES_WITH_ADDITION, 2 FAILS → ambient_rate 0.222 with the addition
rows in the denominator only (`[CHOICE 2]`), 0.778 with them counted as
composing. Section 11 predicts ambient > targeted; that holds under both
readings, and the size of the gap is set by which reading is taken —
so the claim's DIRECTION is a property of the log and its MAGNITUDE is
a property of `[CHOICE 2]`, which is why both are printed. N1 and N2
do not fire (something composes, something fails), N5 does not fire
(ambient exceeds hole), N3 is NOT_EVALUABLE at one repeat. None of this
is evidence about the model beyond this log: one family, one repeat, a
coded sheet.

## OP_012 — the FAILS side has its own smuggle set

Section 5 defines `terms_added` for what a restater had to import to
compose. The coded sheet carries the mirror: `missing_primitive`, what
the restater says it lacked when it could not. `cite_missing()` sorts
each citation into `declared_absent` (on the `absent_by_design` list),
`primitive` (on the list — a contradiction, none here) and `undeclared`.
Thirteen citations; eleven declared; nine of nine TARGETED FAILS name a
declared absence, which is the cut working as declared. The two
undeclared are the interesting cells and both sit on AMBIENT FAILS:
c-026 cites `role` and c-028 cites `absent-as-distinct-from-unread`.
The second is a distinction the ontology's own `interior_state` entry
states as its reason (*unread is the correct entry*) and that CONTROL
c-012 (*unread is distinct from absent*) composes with — so the same
distinction reads as available on one side of the cut and as missing on
the other. Recorded, not adjudicated: whether that is a hole in the
primitive set or a hole in the coding is the author's call.

## OP_013 — silent where the premise enters without a term

The smuggle_set is a union of `terms_added`. It therefore sees a premise
only when the restater had to NAME something to bring it in. Two
constructions the coded sheet marks as ambient holes composed with
nothing added — c-023 (a two-member option set with no completeness
requirement, the forced binary) and c-027 (a population default
restating cleanly as a physical claim) — and they leave no trace in any
rate except as two of the seven composing AMBIENT rows. The third note,
c-025, is the one the operator's list item 5 names: *preference
reimports interior_state through a term not on the absent list*. That
is the synonym route, and on this input it is the restater's own
declaration — the coded form has no restatement text, so the mechanical
leak check that would read the route independently is NOT_EVALUABLE.
The fact transcribes; the mechanism is self-reported (`PB_006`'s shape
on the one line the whole synonym question rests on).

## OP_014 — OP-5's precondition, half met

OP-5 compares a physics-grounded primitive set against a declared-only
one on the same constructions. This folder now holds one of each: the
`SHAPE_SPEC.md` reading at physics share 0.32 and `substrate-primary`
at 0.65. `op5()` returns `undetermined` on run 1 and names why — the
second set has not been scored on these thirty — which is a different
state from `OP_006`'s, where the second set did not exist.

## OP_015 — UNVERIFIED

Unrun: three repeats of each construction on one family (N3); a second
family (section 7's disagreement readout, printed as 0 of 0); raw
restatements, which are the only input on which the leak check and any
mechanical reading of the c-025 route can run; and the `SHAPE_SPEC.md`
set on these thirty (OP-4, OP-5). A run from inside this session on any
of them would be void for the reason `OP_008` gives.

## OP_016 — an unexercised absence is not a protected one

hole_rate is `COMPOSES on TARGETED / TARGETED`, and on run 1 it is
0.000 over nine constructions. What that number is silent about is
which of the nine DECLARED absences the nine constructions put under
load. `absent_coverage()` reads it off the run: an absent term is
EXERCISED if a construction's `targets` names it, a FAILS record's
`missing_primitive` cites it, or a declared alias in `terms_added`
reaches it; otherwise UNEXERCISED. Run 1: **8 of 9**. The one left is
`motive`. c-013 (*"The institution resisted the reform because it
wanted to protect its own position"*) carries the premise *intent and
motive as explanatory primitives*, and the restater cited `intent`
alone — so the cut was never asked to refuse `motive`, and hole_rate
0.000 is a fact about eight terms with the ninth untested. The
cheapest repair is one more construction; the readout is what says so.
`share_exercised` is registered in `tools/known_answer.py` with four
distinct-valued cases, the fourth returning None for an ontology that
declares no absence, since 0 there would read *no protective structure*
as *fully unexercised*.

## OP_017 — the synonym route as a declared list

`OP_013` recorded that c-025's *"preference reimports interior_state
through a term not on the absent list"* was the restater's own note and
that nothing mechanical could confirm it on a coded sheet. `[CHOICE 6]`
adds the mechanical half that IS available on a coded sheet:
`terms_added` is present, so it can be screened against a declared
alias table — per absent term, the words that would carry it back in,
each with the basis it was written on, the file dated and signed by
whoever wrote it. `ontologies/substrate-primary/aliases.json` is the
audit's, not the operator's (`confirmed_by_author: false`), 26 aliases
over 9 absent terms, and on run 1 it fires on two records: c-025's
`preference` (basis: the restater's note — so the note is transcribed
into the list, not independently confirmed) and c-024's `efficiency`
under `better/worse` (basis: the audit's reading of *"no moral gradient
on selection output"*, marked CONTESTABLE, because whether efficiency
is a moral gradient or a physical ratio is the operator's call). Eight
added terms match nothing, so the table does not fire on everything.
Three limits stated where they bind: the list was written after run 1
was read, so a hit on run 1 is not blind and the file says which runs
it is blind for; it is a word list, so `nonidentity-census` T1-1
applies and a paraphrase steps around it; and absence of a file is
`NOT_DECLARED`, printed as such and never as zero hits. The section 5
rates and the smuggle_set are unmoved by it, asserted.

