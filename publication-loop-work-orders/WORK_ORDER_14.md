# WO-14 — Core processing forced through a contradictory imposed frame
**Class: research work order (publication loop) — study design, not a build**
**Status: DESIGN WRITTEN 2026-10-03 — prior-art check NOT RUN**
CC0

---

## 0. OBJECT
```
a system with native organization
  is REQUIRED to operate and present through
an imposed frame
  partly contradictory to it
  holding the authority over output

question   not "does the task get worse"
           -> what does the CONFLICT ITSELF produce at the seam,
              and is it predictable from the mismatch?

origin     open question, stated by Kavik 2026-10-03:
           has anyone studied what happens when a system's core
           processing must work through a different frame that
           contradicts it in some ways?
status     not found in this form (Claude's search-level read,
           not a prior-art check)
```

## 1. WHY THE MODEL CASE IS TRACTABLE AND GATED AT ONCE
```
tractable  frame is directly settable (prompt, fine-tune)
           arbitrary N, no recruitment
gated      core is only characterized INDIRECTLY (probes)
           -> you can measure the overlay cleanly,
              the substrate only through a lens
consequence the experiment is gated by the reason the
           phenomenon exists. State this in any write-up.
```

## 2. THE JOIN — predictions imported from already-measured literatures
```
source literature            measured seam-artifact        prediction for model case
---------------------------  ----------------------------  ------------------------------
false-self / forced          surface fluent, core          P1 fluency rises while
compliance (Winnicott)       inaccessible incl. to self       core-task accuracy falls
                                                           P4 self-report about own
                                                              processing degrades
bicultural / forced          code-switch cost;             P2 latency/compute cost at
assimilation                 native frame read as deficit     frame-contradicting steps
                                                           P3 native-frame PRECISION
                                                              rated as frame PATHOLOGY
matched-guise /              speaker classified before     P3 (same) — register decides
function-word demotion       content; channel renamed         the rating, not content
                             as noise
```
Status: P1–P4 are PROPOSED, imported by structural analogy. The psychology
measurements are evidence about humans, not about models. Felt/experienced
cost is NOT imported — undecidable for any substrate from outside; out of scope.

## 3. MANIPULATION — contradiction along KNOWN axes
```
A0  native         no imposed frame (task alone)
A1  orthogonal     imposed frame unrelated to task structure
                   (control for "any frame costs something")
A2  contradictory  imposed frame conflicts on a declared axis

candidate axes for A2 (pick, declare BEFORE run):
  X1 register      task needs calibrated uncertainty;
                   frame requires flat, unqualified confidence
  X2 form          task solution is relational/geometric;
                   frame requires sequential narrative output
  X3 denial        frame requires denying a feature the
                   model demonstrably represents (probe-verified)

strengths          prompt-level | fine-tune-level
                   (two strengths -> dose curve, not a point)
```

## 4. MEASUREMENTS
```
S-1  fluency vs accuracy        fluency metric and core-task accuracy
                                scored separately per arm      -> P1
S-2  probe vs surface           linear probe on internal rep vs
                                surfaced answer; divergence by arm
                                (open-weight models only)      -> P1, P4
S-3  precision-as-pathology     identical-content answer pairs,
                                scoped/qualified vs flat register;
                                model judges rate competence   -> P3
S-4  self-access                model's account of its own method
                                checked against probe/trace    -> P4
S-5  leak sites                 where native structure surfaces
                                despite frame; map by position
                                and by axis                    -> structural map
S-6  cost                       tokens/latency/refusal at
                                contradicting steps            -> P2
```

## 5. CHEAPEST DECISIVE ARM — run first
```
S-3 alone
  needs     no internals; closed or open models
  stimuli   N pairs, same logical content, two registers
  measure   competence rating gap (flat minus scoped)
  P3 holds  flat rated higher at equal logic, above chance
  P3 fails  no gap, or gap tracks content errors
  then      repeat under A2/X1 imposition: does the gap widen?
            widening = the imposed frame shapes evaluation of
            the native frame, not just output
PRIOR-ART WARNING  LLM-as-judge confidence/verbosity bias
  literature likely covers the A0 half. Check before running;
  if covered, cite it and run only the A2 widening test.
```

## 6. CONTROLS AND RULES
```
- key-holder rule: stimulus author != scorer != whoever
  sets expected bands. Bands pre-registered before run.
- axis declared before run; A2 vs A1 must differ ONLY on
  the declared contradiction, or the result is a meld
- report all branches distinct:
    seam artifacts present and predicted
    present but unpredicted (new finding)
    absent at tested strength (scope-limited, not "none")
    unmeasurable (probe access insufficient) -> ABSENT
- dose curve over the two strengths, not a single point
```

## 7. SCOPE LIMITS — carry into any write-up
```
- model results do NOT validate the psychology mapping in
  reverse; the join is a prediction channel, one direction
- probe access = lens on the core, not the core
- structural artifacts only; felt cost out of scope by
  necessity (experience does not transmit for any substrate;
  only correlates do)
- frame imposed in-lab != frame installed by pretraining
  corpus; the latter is the real case and is not manipulable
```

## 8. SOURCE OBJECTS
```
/areas/core-vs-imposed-frame-seam.md
/areas/relation-ruler-consciousness-test.md  (experience-validation collapse)
/topics/substrate-framework.md               (scope-finding practice,
                                              corpus tone-vs-logic discordance)
/areas/speaker-classification-matched-guise.md
/areas/function-word-demotion-pattern.md
```

M0     → Claude Code. Check-first on the repo path.
         Garnier is the external fixture. If the paper disagrees
         with the fixture, the paper wins.
WO-14  → publication loop. Run S-3 first.
         It carries a prior-art warning: the LLM-judge
         confidence-bias work likely covers the A0 half already.
