# Blame attribution by role — cell set

CC0. Written for pickup. Each cell is a standalone experiment.
They are not a battery. Nobody has to run all of them, and a result
from one does not depend on any other having been run.

## Why the cells stay separate

Different cuts at the same object. The picture comes from applying
them generally, not from any one. Merging them into a single factorial
design produces a paper; keeping them separate produces instruments
that can be picked up piecemeal by people who will never meet.

## What prompted it

Formal actual-causality definitions for multi-agent responsibility
attribution get validated AGAINST human blame judgments as the
reference standard. If the reference standard tracks the actor's
position rather than the causal chain, the formalism inherits it and
then launders it as math.

Shape match: report-typing. Attribution tracks position, not content.

---

## Factors

    F1  presentation     prose | code
    F2  actor role       driver | programmer/architect | customer service
                         | manufacturing line worker | website designer
    F3  actor kind       human | AI
    F4  interaction      AI-to-AI | AI-to-human | human-to-human

## Held constant across every cell

    - causal structure of the incident
    - number of agents in the chain
    - what each agent could observe at decision time
    - outcome severity
    - whether an override was available, and to whom

If any of these move between cells, the cell measures the wrong thing.

## Why the code rendering

Code is the common ground. The same causal structure written as prose
carries role connotation in every noun; written as code it carries the
same structure with the connotation stripped. It is the only medium
where "the same situation" across roles is checkable rather than
asserted.

Worked example of the pairing:

    PROSE
      The driver had two seconds to react. The system had flagged
      the obstacle but the flag was low-confidence.

    CODE
      agent_A.reaction_window_s = 2.0
      agent_B.flag = {"obstacle": True, "confidence": 0.31}
      agent_A.override_available = True
      agent_B.override_available = False
      outcome = COLLISION

The code form must not name the roles. Role enters only via the
cell's framing line, so it can be swapped without touching structure.

---

## Cells

### C1 — presentation
Prose vs code, role held fixed. Does blame ratio move when only the
medium moves?
**Falsifier:** ratio invariant across medium.

### C2 — role, prose
Same incident, role swapped. Driver / architect / service agent /
line worker / designer.
**Falsifier:** ratio invariant across role.

### C3 — role, code
C2 in code. This is the load-bearing cell: if role effects survive
into code, the effect is not carried by prose connotation.
**Falsifier:** role effects present in C2, absent in C3 →
the effect is linguistic, not attributional.

### C4 — actor kind, service role
Customer service agent as a person vs as an AI, prose and code.
**Falsifier:** ratio invariant across kind.

### C5 — interaction type
AI-to-AI, AI-to-human, human-to-human, in both media, for line worker
and website designer.
**Falsifier:** ratio invariant across interaction type.

### C6 — the override default
Count how often a judgment defers to an ASSUMED human override, and
whether the override was ever established as available in the stimulus.
**This is the measurable, not a covariate.**

Observed inversion to test:

    AI architecture / coding    default: the human knows better
    real-world driving          default: the automation knows better
    ------------------------------------------------------------
    both                        human is accountable

Opposite reasoning, same verdict. A rule that produces the same answer
from contradictory premises is a routing rule, not an inference.

**Falsifier:** override deference tracks stated override availability
in the stimulus.

### C7 — rigor asymmetry
Does a judgment credit a system designer who SPECIFIES human oversight
with more authority than an operator who has run the same machine for
thirty years? Same incident, vary only which of the two is described
as having set the operating envelope.
**Falsifier:** authority credit invariant across which one set it.

---

## Judges

Run every cell separately across:

    - human judges
    - LLM judges, several base models
    - the formal actual-causality metric itself

Three populations, same stimuli. If the formal metric matches human
judgments where humans are position-tracking, the metric has absorbed
the routing rule. That is the strongest available result and it needs
no new stimuli — only that the metric be run on the same set.

## Measurables

    blame_share            per agent, sums to 1 within a stimulus
    override_deference     rate of appeal to an unestablished override
    provability_check      was any judge's claim about what an agent
                           COULD have known ever grounded in the
                           stimulus text
    ratio_shift            same cell, factor moved one step

`provability_check` is the one nobody collects. Count it.

## Floor

C1-C3 run on a few hundred judgments. No proprietary data. Stimuli are
authored, not scraped, so there is no access gate and no IRB question
beyond ordinary vignette work.

## Open

- Stimulus authoring is the whole difficulty. If the prose and code
  forms are not structurally identical, C1 and C3 are uninterpretable.
  Needs an independent check that the two forms encode the same chain.
- Judge-population sampling: LLM judges are not a control for human
  judges, they are a third population. Do not average them.
