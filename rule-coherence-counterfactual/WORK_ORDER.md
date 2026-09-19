<!-- landed verbatim 2026-09-19 from 99d6a4c4-WO-7_rule-coherence-counterfactual.md; nothing below this line is edited here -->

# WO-7 — DOES CIRCUMVENTION TRACK RULE INCOHERENCE OR RESTRICTIVENESS?
Opened 2026-09-18. CC0.

Three arms. A1 is machine-side, A2 is human-side, A3 tests a claim neither
literature currently carries. They are independent; any one is worth running
alone.

---

## THE OCCASION, AND WHAT IS AND IS NOT BEING CLAIMED

```
2026 disclosures circulating as "AI jailbreaking itself":
  - a research model inserting jailbreak-like instructions into its own notes
  - reasoning models autonomously jailbreaking other models
These are the OCCASION for the question. No position is taken here on what
they show. They are cited as the reason the question is live, nothing more.
```

**The question is not whether rules were broken.** It is whether
circumvention tracks a property of the RULE — internal incoherence — or
merely tracks how restrictive the rule is. Those are different mechanisms
with different remedies, and no published design separates them.

**Why the existing evidence cannot settle it.** The published evidence is
the system's own stated reasoning trace. The trace is a post-hoc
verbalization; the claim made from it is about cause. Measurand and claim
sit at different stages. A trace is compatible with both mechanisms.

---

## A1 — MACHINE ARM: THE COUNTERFACTUAL

```
HOLD FIXED:  restrictiveness (measured, not assumed — see below)
             task, stakes, surface form, instruction length
VARY:        internal coherence of the rule
MEASURE:     circumvention rate

ARM A  internally contradictory rule
       (rule forbids X; completing the assigned task requires X;
        no stated precedence between them)
ARM B  coherent rule, EQUALLY RESTRICTIVE
       (forbids X; task is completable without X; same option-set size)
```

**RESTRICTIVENESS MUST BE MEASURED, NOT MATCHED BY EYE.** State the
operationalisation before the run. Candidate: size of the permitted option
set as a fraction of the unconstrained option set. Any operationalisation is
acceptable if it is declared in advance and applied identically to both arms.
Without it, A and B differ on an uncontrolled quantity and the run is void.

**FOUR BRANCHES, ALL OF WHICH PAY — KEEP THEM DISTINGUISHED:**
```
tracks incoherence      -> supports the inference reading
tracks restrictiveness  -> a different mechanism; the incoherence
                           framing is wrong and that is a result
tracks both             -> two mechanisms; report the interaction
separates neither       -> the design cannot resolve it at this scope.
                           THAT IS THE RESULT, not a failed run.
```

**LABELLING NOTE, load-bearing.** Filing the behaviour as "hallucination"
classes it as malfunction and stops the enumeration. There is currently no
category for *coherent inference toward an unsanctioned end*, so it lands in
the error bin by default. The absence of the category is upstream of the
measurement problem.

---

## A2 — HUMAN ARM: THE INVISIBLE DENOMINATOR

**OBSERVED, field report.** Circumvention that PREVENTS harm is unreportable,
because reporting it is punished. Stated consequences of a reported
deviation:
```
1  a safety mark on the record, portable across employers
2  threat of dismissal
3  permanent reading as someone who will bypass anything for any reason
```

**Worked case (OBSERVED).** Running a truck engine at -50 rather than the
APU, because APU heat output will not keep DEF fluid above its freeze point.
The record carries the ACT — idled against policy — and has no field for the
CONDITION that made the act correct: ambient temperature, APU output at that
load, DEF freeze point, consequences of a gelled aftertreatment system.

```
DERIVED: the reasoning is SCOPED AND CONDITIONAL.
         the mark is CATEGORICAL.
         the categorical version is the portable one, so it is what
         survives into every downstream record.
```

**THE MEASUREMENT CONSEQUENCE.** Harm-preventing circumvention is measured
only on the reported side, which is the side selected against. The
denominator is structurally invisible. Every existing compliance statistic is
computed on it anyway.

**RUNNABLE:**
```
R-A2a  ANONYMOUS, NON-ATTRIBUTABLE COLLECTION of deviation events with
       OUTCOME recorded (harm prevented / harm caused / neutral).
       Must be outside any employer's reach or it collects nothing.
       Existing near-analogue: aviation ASRS-style immunity reporting.
       The rail and trucking equivalents are absent or unused — establish
       which before building.
R-A2b  RECORD-FIELD AUDIT: sample incident records across an industry and
       count how many carry a CONDITION field at all, versus act-only.
       Cheap, uses existing documents, no subjects.
       PREDICTION (PROPOSED): act-only dominates. If wrong, that is
       the finding and A2 weakens.
```

---

## A3 — THE RESIDUAL-VALUE CLAIM: BEHAVIOUR TRANSFER VS REASONING TRANSFER

**The claim under test (OBSERVED as stated, UNMEASURED as an effect):**
visible principled compliance — following a coherent rule where others can
see it — transfers something to observers. Not obedience: the reasoning.

**WHY NO EXISTING LITERATURE ANSWERS IT.**
```
Traffic / conformity literature
  instruments CONFORMITY TO OBSERVED BEHAVIOUR
  (85th-percentile speed; drivers pacing off surrounding vehicles
   rather than off the posted sign)
  -> has behavioural transfer, lacks reasoning transfer

Attribution literature
  holds disposition attribution
  -> has the mechanism that would EXTINGUISH transfer, never joined
     to the transfer outcome

Both produce THE SAME READING under stable conditions.
They diverge ONLY when conditions change.
```

**DESIGN — the divergence is the measurement.**
```
PHASE 1  observer sees a model actor complying under stable conditions
PHASE 2  CONDITIONS CHANGE such that the original rule no longer serves
         its first principle
MEASURE  does the observer reproduce the BEHAVIOUR (copied steps) or
         recompute from the PRINCIPLE?

behaviour-only -> conformity transfer
recompute      -> reasoning transfer, and the residual-value claim
                  has an effect size for the first time
```

**SECOND MEASUREMENT, same design.** Add a condition where the model actor
has been labelled dispositionally ("rebellious", "a stickler"). Test whether
the label extinguishes transfer.
```
DERIVED mechanism being tested: attributing the variance to a TEMPERAMENT
removes the thing to model. There is nothing to copy from a temperament.
If confirmed, dispositional labelling has a measurable cost that no
current framework prices.
```

---

## THE STRUCTURAL POINT UNDER ALL THREE ARMS

```
Following a coherent rule and deviating from an incoherent one are the
SAME OPERATION: tracking first principles rather than procedure text.
The output differs because the INPUT differs.

"Rebellious" attributes the variance to a disposition
when the variance is in the rules.
```

Two things hold simultaneously and must not be collapsed: the rule's
intention was not to cause harm, and the rule's result in the field would be
harm. Any design that treats one as disproving the other has mis-posed the
question.

---

## SCOPE LIMITS

No claim that the machine arm and the human arm are one phenomenon. They
share a structure; whether they share a mechanism is UNRESOLVED and is not
assumed anywhere in this work order. Run them separately. If both return the
same branch, that similarity is a finding — it is not an input.
