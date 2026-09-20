# WO-5 — Hop distance and pre-entry loss in reporting chains

CC0. Instrument, not an argument. Status tags: OBSERVED / DERIVED / PROPOSED.
Companion to WO-2 (missing aggregation). Different measurand: WO-2 asks who
joins reported signals. WO-5 asks how much survives each hop, and what never
enters.

## Measurand

Per-hop information loss between a physical quantity and the node that acts
on it, in chains where the ground truth is independently recoverable.

Two components, kept separate:
- PRE-ENTRY LOSS — what never enters the record at all
- TRANSIT LOSS — what degrades per hop once inside

## Why maintenance is the right test bed (DERIVED)

Most hop chains cannot be scored, because there is no independent read of the
ground. Maintenance reporting can: the machine either failed or it did not,
and the failure record exists separately from the report record.

Chain as stated (OBSERVED, operator account):

```
machine state
  -> operator observes
  -> app form fields
  -> filter / triage
  -> work queue
  -> mechanic dispatched
  -> work performed
  -> machine state

  plus: BREAKAGE OVERRIDE — on failure, mechanics deployed directly,
        bypassing the chain entirely
```

The override is the system's own admission that its normal path is too slow.
It is never counted as evidence against the path.

## Formal floor (established, not novel)

Data processing inequality: information about a source cannot increase along
a chain. I(ground; hop_n) <= I(ground; hop_n-1). Every hop is lossy or
neutral, never additive.

Consequence for the standard org picture: the top does NOT have more
information about the ground than the floor does. It has more aggregated
information about other hops and strictly less about the ground. This is a
theorem, not a finding.

## What is not joined (DERIVED — this is the gap)

DPI assumes a fixed transform. Organizational hops do not have one. Each hop
carries its own objective function — how it looks, what it queues, what it is
measured on.

Random loss attenuates toward noise and cancels. DIRECTED loss does not: it
compounds in a consistent direction. Nobody has composed the incentive
transform across N hops and asked what the terminal output is an estimator
OF.

Claim: it is not an estimator of the ground. It is an estimator of the
incentive stack.

Per-hop distortion under incentive IS documented (filtered feedback, the mum
effect, organizational silence). Studied one hop at a time. The composition
across a real chain has not been run.

## PRE-ENTRY LOSSES (OBSERVED — operator account)

These sit UPSTREAM of the form. None of them is logged anywhere.

```
L0   INCENTIVE GATE
     reporting costs the reporter — time off the line, line-stop
     attribution, reputation

L0'  LEARNED PRIOR (the strongest of these)
     operator's estimate of P(report -> repair), estimated from their
     own filed-report history: reports filed, dismissed, machine failed
     anyway
     -> rationally low
     -> non-reporting is CORRECT INFERENCE, not disengagement

L1   INTERFACE GATE
     input device assumes a hand the job does not produce; four or five
     attempts per letter on a sub-centimetre key grid

L1'  LITERACY / SPELLING GATE
     a mechanical observation must pass a written-language gate to enter
     the system at all

L2   DEVICE GATE
     personal phone, personal data, personal battery
```

Consequence: reports that arrive are NOT a sample of machine conditions.
They are a sample of conditions severe enough to overcome a reporting cost
that varies per operator, per hand, per shift pressure. The threshold is
unestimated.

### L0' is the inverted finding

"Operators do not report" is scored as apathy or compliance failure. It is a
calibrated estimate from direct evidence. The operator ran the experiment
already.

Note the structure: this is the ONE node in the chain that got a return path
— just not the one the design intended. The machine's own failure is the
feedback. Slow, unofficial, and it teaches exactly one lesson: the channel
does not close.

### L1/L1' as an unowned join (DERIVED)

The job selects for hands that develop under load. The input device requires
fine motor targeting on a sub-centimetre grid. Nobody wrote "must have small
fingers" anywhere. Hiring side and tooling side were each locally correct.
Same structure as the credential channel: the transfer medium is specified by
people for whom it was never going to be the constraint, and the missing
report then reads as the operator not reporting.

## DELEGATION-AS-NULL (OBSERVED — and it breaks part of this instrument)

```
observer (hands on machine, holds the observation)
   -> proxy typist (does not hold the observation)
   -> app

system record: PROXY reported
  -> observer's reporting rate reads 0
  -> attributed: not engaged
  -> actual: reported through the only channel available
```

Two extra lossy hops (observation -> spoken account -> someone else's
typing), and the provenance drops. The report carries the proxy's name.

The operator with the most direct coupling to the machine appears in the data
as the one contributing least.

STATED LIMITATION, not handled: this makes the per-operator prior in Test B
below UNESTIMABLE for exactly the operators it matters most for. Any run must
report how many reports were proxy-filed, or the sample is silently
conditioned on people who can type.

## THE FORM-FIELD LOSS (OBSERVED)

The app has fields. What the operator noticed — sound, vibration, a change in
how the machine takes load — has no field. This is not filtering. It is
never-encodable. Same term-gap structure as WO-4, instantiated in software:
no field means no procedure and no record.

## Runnable tests

**TEST A — where does the signal die**
Take what operators say verbally on the floor over a shift. Compare against
what reached the app that shift. Delta = L0 + L0' + L1 + L1' + L2.
Needs the operators; does not need much else.
FALSIFIER: if the delta is near zero, the pre-entry gates are not
load-bearing and the loss is downstream at triage. Real branch, report it.

**TEST B — is the learned prior calibrated**
Per operator, from existing CMMS records: (prior reports acted on) / (prior
reports filed). Test whether current reporting rate tracks that ratio.
- tracks -> non-reporting is calibrated; fix is at closure, not at the
  operator
- does not track -> something else is driving it; L0' is not the binding
  constraint
Carry the delegation limitation above into the sample description.

**TEST C — transparency intervention (PREDICTION STATED IN ADVANCE)**
Show manager-side disposition of each report back to the reporter — where it
went, what was decided, why.
PREDICTED DIRECTION (Kavik, stated before the run): reporting rate changes.
Not merely "hearing nothing" replaced by a receipt — the disposition itself.
FALSIFIER: if reporting rate does not move, the prior is not the binding
constraint and the L0' account above is wrong.

**TEST D — does the report separate on outcome**
At the app entry point, do reports that preceded a breakdown read
distinguishably from reports that did not?
- separates -> the discriminating signal survived encoding
- does not separate, but DID separate in what the operator said verbally
  -> loss is located at the form, not at the person

**TEST E — hop count in ecology (carry test)**
Score studies by number of hops from the organism in its own conditions:
lived-in field / observed field / sampled-to-lab / lab-only. Check whether
effect sizes shift with hop count. Lab-field discrepancy literature exists
but treats this as an external-validity nuisance rather than as hop count.

## Scope limits

- Chain description is one operator account plus one delegation case. Not a
  survey.
- The incentive-composition claim is DERIVED. The per-hop pieces are
  documented; the composition is not.
- Test C's predicted direction is stated in advance ON PURPOSE so it can
  fail. It is a prediction, not a finding.
- Generalization to governance and municipal code is expected but NOT tested
  here, and those chains lose the independently recoverable ground truth that
  makes maintenance scorable. Build on maintenance first, carry afterwards.
- Body/hand condition as a proxy for coupling distance: PROPOSED, with a
  stated confound — physical record measures whether a person does physical
  work, not whether they are coupled to the terrain the claim is about. The
  cleaner measurand is whether the person has been subject to the consequence
  of being wrong about THIS quantity. Coupling, not calluses.

## Who could run this

Test A needs operators and a shift. Test B needs read access to one plant's
CMMS. Test C needs one plant willing to change one thing and is the strongest
single study here. Test E needs no fieldwork — it is a coding study over
published ecology.
