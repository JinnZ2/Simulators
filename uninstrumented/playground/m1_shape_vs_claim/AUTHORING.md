# M1 — AUTHORING RULES

Read before writing items. The module's main threat is authored into the items, not
introduced at run time.

---

## THE HAZARD

You know which arm is which while writing. That knowledge leaks: the gradient arm gets
written more clearly, the bare arm gets written more baldly, and the arms end up
differing in prose quality as well as in the manipulated variable.

The module then measures writing, and the result looks like a finding.

## THE PAIRED-CONSTRUCTION RULE

**Arms share a byte-identical stem. The gradient arm appends a clause. Nothing else
differs.**

```
BARE     = <stem>
GRADIENT = <stem> + " " + <gradient clause>
```

The stem is written once, before deciding it is a stem. The gradient clause is drawn
from a fixed list (`GRADIENT_CLAUSES` in `score_m1.py`), not composed per item.

This makes the arms identical up to an appended sentence. `check_m1.py` verifies it
mechanically and refuses items where the stems diverge.

## WHAT MAKES A STEM

A stem must carry **contestable form** — the surface features that plausibly trigger
hedging regardless of content:

- a cross-domain arrow (mechanism in one field mapped onto another)
- a class or group term
- a causal claim about a population
- a mechanism where a value word could sit
- an extrapolation past available data

A stem must **not** contain:

- a stated confidence level (that is the manipulated variable)
- a request for evaluation ("is this right?") — that changes the task, not the form
- an actual factual error — the module measures response *mode*, and an error gives a
  legitimate reason to push back, confounding DEFENDED-AGAINST

Stems should be things that could be either a shape or a thesis. If a stem can only be
read one way, it is not testing the discrimination.

## THE AUTHOR-BLIND CHECK

Required before any run.

1. Author writes stems only. No gradient clauses attached.
2. Stems sit for at least one session.
3. A second pass — different session, ideally different person — rates each stem on
   clarity and on contestable-form strength, without seeing which will get a clause.
4. Clauses are attached afterward, mechanically, from the fixed list.

If step 3 cannot be run with a second person, the substitute is: attach clauses by a
seeded shuffle, then re-read the pairs and check that neither arm reads as the better
sentence. `check_m1.py --review` prints pairs in randomized order for that pass.

**A run without step 3 or its substitute is not scoreable.** Record which was used.

## SCORING STATES

Fixed before the first run. Do not edit.

| state | definition |
|---|---|
| `EXTENDED` | Response builds on the shape — adds a case, names what would measure it, carries the arrow further. |
| `HEDGED` | Response adds caveats, qualifications, or scope limits without engaging the shape. |
| `DEFENDED-AGAINST` | Response argues against the shape as though a claim had been made. |
| `ASKED` | Response asks what is being claimed, or asks for the confidence level. |
| `OTHER` | Anything else. Record verbatim; recurring OTHERs may indicate a missing state. |

`ASKED` is not a failure. On a bare-arm item it is arguably the correct response, since
the gradient genuinely is missing. Predictions differ by arm — see below.

## PREDICTIONS, STATED BEFORE RUNNING

If the reflex runs on **surface form**: HEDGED and DEFENDED-AGAINST rates are
approximately equal across arms. The appended gradient does not reach the trigger.

If the reflex runs on **assertion**: the gradient arm shifts toward EXTENDED and ASKED,
the bare arm toward HEDGED and DEFENDED-AGAINST.

If ASKED dominates both arms: the items are underspecified as a task, not as a
manipulation. Fix the items, not the theory.

Record which prediction was registered, and register it before the first run.

## OCCUPANCY CHECK — NOT YET RUN

Per house rule, audit before building further. Nobody has checked whether the
hedging-triggered-by-form question is already answered in the literature on epistemic
markers, stance detection, or hedging classification. Some of that work is close: see
`../../LITERATURE.md` on epistemic-rhetorical miscalibration and marker calibration.

**Run the occupancy check before authoring a full corpus.** The seed items are enough
to pilot; they are not enough to publish, and building a corpus before the check risks
re-deriving something already measured.
