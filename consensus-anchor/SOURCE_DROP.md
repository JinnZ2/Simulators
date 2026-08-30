# Gap: the anchor point of consensus convergence in trained systems

CC0. No rights reserved. Take it, run it, publish it.

## Observation

Trained language models converge on majority/popular positions. This is
reported descriptively and treated as a single phenomenon. It is not one
phenomenon. At least three distinct mechanisms produce the same observable,
and no published work discriminates between them.

Until the anchor is located, mitigation is untargeted: an intervention aimed
at the wrong mechanism leaves the effect intact and consumes the budget.

## The three candidate anchors

```
H1  INHERITED NORM
    Human text encodes consensus-as-truth-signal. The model reproduces a
    social norm present in the corpus as content.
    Locus: corpus semantics.

H2  OBJECTIVE
    Next-token prediction is frequency-weighted by construction. The
    majority reading wins on likelihood alone. No norm required.
    Locus: training objective.

H3  STRUCTURAL COUPLING
    Units under mutual influence align. Convergence is a property of the
    coupled dynamics, independent of what the units encode.
    Locus: interaction topology + coupling strength.
```

These are not mutually exclusive. The design must estimate partial
contribution, not pick a winner.

## Discriminating predictions

```
                         H1        H2        H3
consensus-norm stripped  gone      holds     holds
  from corpus
frequency flattened      holds     gone      holds
  in training
isolated units           holds     holds     gone
  (no mutual influence)
text-free agent pop.     absent    weak      PRESENT
coupling threshold       no        no        YES
  below which no align
order-parameter          no        no        YES
  hysteresis
convergence tracks       weak      MONOTONIC weak
  raw corpus frequency
```

The three unique signatures:

- H1 dies under norm-stripped corpora.
- H2 dies under frequency-flattened training.
- H3 alone predicts a **threshold** and **hysteresis**, and alone predicts
  convergence in populations that have never seen human text.

## Design

Factorial. Every cell run; no cell dropped for looking uninformative.

```
FACTOR A  corpus consensus norm    {present, absent, inverted}
FACTOR B  frequency weighting      {natural, flattened}
FACTOR C  coupling strength J      {0, J1 ... Jk}  (k >= 6, spanning
                                    a suspected critical region)

3 x 2 x (k+1) cells, n seeds each.
```

`A=inverted` matters: a corpus in which minority positions are explicitly
marked as correct. If majority convergence survives inversion, H1 is not
carrying the effect.

`B=flattened` = importance reweighting toward uniform over positions on
contested items, applied at the loss, not at decoding. Decoding-time
temperature is a different variable and must be held fixed.

`C` = degree to which each unit's update depends on peer outputs.
`J=0` is the isolated control.

## Measurements

```
m        order parameter: fraction of population on the modal position
chi      susceptibility: dm / d(external field)
J_c      coupling value at which m departs from chance
tau      relaxation time near J_c            [expect divergence if H3]
hyst     m(J up) - m(J down)                 [expect gap if H3]
d_freq   corr(convergence rate, corpus frequency of position)
                                             [expect ~1 if H2]
```

External field = a small injected bias toward a named position. Susceptibility
near the threshold is the sharpest H3 signature and the cheapest to measure.

## The text-free arm

The strongest single test, and the one that needs no language model.

```
Population of symbolic agents. No human corpus anywhere in the pipeline.
Each agent holds a position vector over an arbitrary discrete space.
Update rule: weighted mix of own prior and sampled peer positions.
Sweep J. Measure m, chi, J_c, hysteresis.
```

If threshold behaviour and hysteresis appear here, H3 is live and is a
property of the topology, not of anything human text contributed. If they
do not appear, H3 is falsified cheaply and early. Run this arm first.

## Falsifiers

```
H1 false if  majority convergence survives A=inverted at equal magnitude
H2 false if  convergence survives B=flattened, or d_freq is not monotone
H3 false if  no J_c exists (m rises smoothly from J=0), or no hysteresis,
             or the text-free population shows no alignment at any J
ALL false if convergence magnitude is invariant across every cell
```

The all-false outcome is a real result and must be reported. It says the
anchor is somewhere none of these three name, and the observable has been
misattributed in the existing literature.

## Instrument caution

Do not gate case admission on record completeness. Any criterion strict
enough to admit only clean cases admits only the cases whose records
happened to survive, which is the bias being measured. Grade the evidence,
let the instruments disagree, and treat divergence between instruments on
the same case as signal about which channel dropped what — not as noise to
be reconciled.

## Adjacent human-side sample

Same shape, independent substrate, already-existing data: transmitted
variants of legal and religious texts, where transmission skew hardens into
division. The measurable is divergence between surviving variant lineages
against transmission distance, not the content of any variant. Useful as an
out-of-domain check on whether the coupling model predicts anything about
systems it was not fitted to.

## What is being asked for

Anyone with compute: run the text-free arm. It is small, it is the fastest
discriminator, and it does not require a trained model. Report the null.
