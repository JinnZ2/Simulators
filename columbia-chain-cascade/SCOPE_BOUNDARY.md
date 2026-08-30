# SCOPE BOUNDARY — why this spec is broader than standard practice

Delivered verbatim. CC0.

## The problem

In a cascading dam-failure scenario, things like urban watershed changes,
bridge construction, mining, and industrial landscape alteration are not
separate from dam safety. They are direct, material, contributing factors.
When a model says those things have "no causal relationship" or are "out
of scope," that is usually not a scientific finding. It is a boundary
choice, a modeling limitation, or a narrow definition of "cause."

The system does not care about our institutional boundaries. Physics does
not isolate a dam from the watershed above it, the river below it, the
bridges that constrict flow, the mining that changes sediment and slope
stability, or the human procedures that decide when to open gates,
inspect, maintain, or evacuate. All of those are part of one continuous
causal system.

When we model only a piece of that system, we are not simplifying reality
— we are modeling a different system than the one that actually exists.
And then we are surprised when the real system behaves in ways the model
did not predict.

## Six ways the connection gets lost

### 1. The "proximate trigger" fallacy

Many analyses focus on the immediate trigger: heavy rainfall, earthquake,
overtopping. If the final failure is recorded as "overtopping due to
extreme rainfall," then mining, bridges, urban runoff, and landscape
change can be left out of the official cause.

But those earlier changes altered the conditions that made the trigger
fatal. Mining destabilizes slopes → heavy rain saturates ground →
landslide enters reservoir → displacement wave overtops dam → downstream
bridge traps debris → downstream dam fails.

If the report says "Cause: heavy rainfall," it is not false, but it is
incomplete. The mining, bridge, and landscape changes were causal too —
just not proximate.

So "no direct cause" often means "It was not the final trigger." That is
very different from "It had no effect."

### 2. Scope boundaries in engineering and regulation

Dam safety is split into institutional silos:

- Dam structure and foundation
- Reservoir rim stability
- Upstream watershed hydrology
- Land use planning
- Mining regulation
- Bridge and transportation infrastructure
- Sediment and debris management

A dam safety engineer may look only at the dam. A watershed planner may
look only at runoff. A mining inspector may look only at the mine site.
Each can say "That is outside my scope." But that is an institutional
boundary, not evidence that there is no physical connection.

In a cascading dam failure, the upstream watershed, the reservoir, the
dam, the downstream channel, bridges, and downstream dams are all one
connected system. Separating them is an artificial human division.

### 3. Model boundaries and missing variables

A dam breach model may include reservoir volume, dam height, breach width,
downstream channel slope. But it may not include upstream land cover
change, sediment yield from mining, channel incision from gravel mining,
bridge pier scour, debris availability from urban areas, or slope
instability from road construction.

If a variable is not in the model, the model shows no sensitivity to it.
That is not because the variable is irrelevant. It is because the model
was not built to represent it.

So when someone says "The model shows no connection between mining and
dam failure," what that often really means is "The model did not include
mining as a variable." That is a huge difference.

### 4. Statistical conservatism and lack of data

Dam failures are rare. Cascading dam failures are even rarer. Mining
histories, bridge designs, watershed changes, and local geology vary
widely. With small sample sizes, it is often statistically impossible to
demonstrate a strong correlation — even when a causal pathway is well
understood physically.

So an analyst may say "There is no demonstrated correlation." But the
public hears "There is no relationship." Those are not the same. In many
complex environmental systems, absence of statistical correlation is just
absence of sufficient data. The physical mechanism can still be real.

### 5. Strict causal language

In science and engineering, people are trained to say "causation" only
when there is strong evidence, controlled experiments, or a clear
mechanistic chain. In a specific dam failure, it may be very hard to say
"Mining contributed exactly 18% to this failure." So instead they say
"No direct causal link was established." That is often interpreted as
"There is no connection." But what it often means is "We could not
quantify the contribution precisely."

### 6. AI or language model limitations

If a language model says those things are out of scope or unrelated,
remember: the model may not have your systems perspective. It may not
have enough domain-specific causal context. It may be avoiding
speculation. It may not distinguish between "not proven" and "not real."
A language model is not an authority on geomorphology, dam safety, or
complex cascading failures. Its boundaries are not physical boundaries.

## What this spec does differently

This build spec treats the river basin, infrastructure, and human
decisions as one integrated system. The following modules document
mechanisms that standard breach modeling typically drops:

- **module_f.py** — Antecedent-condition coupling: the operator swap
  (`max` vs. `sum`) is the mathematical form of the proximate-trigger
  fallacy. The independent model (`max`) sees only the wave; the coupled
  model (`sum`) sees the wave plus the antecedent pool. The pool may be
  raised by urban runoff, mining debris, or any upstream landscape change.

- **contributing_inflow.py** — Urban runoff as a pool increment:
  impervious surfaces in Spokane, Tri-Cities, Portland metro, and
  Lewiston raise tributary inflows, raising antecedent pool levels at
  downstream dams. Standard models use naturalized or gage-recorded
  inflows that may not capture recent urbanization.

- **eap_coverage.py** — Governance fragmentation: the fact that no
  single entity's plan spans the chain is the institutional version of
  the scope-boundary problem. USACE plans for USACE dams. PUDs plan for
  PUD dams. Nobody's plan spans the watershed, the bridges, the mining
  slopes, and the urban runoff. The spec records that as data, not
  commentary.

## The knowledge-state vocabulary

When a variable is physically relevant but not yet quantified, the spec
records its epistemic state rather than excluding it. The valid states are:

| State | Meaning | Example |
|-------|---------|---------|
| **UNKNOWN_ATM** | The mechanism is known to exist, but no current value is available. | Urban runoff increment for the Spokane watershed in 2026. |
| **UNDER_STUDY** | Data collection is in progress; value is provisional. | Burn severity for the 2024 fire season, awaiting final MTBS mapping. |
| **NOT_STUDIED** | The mechanism is recognized, but no measurement has ever been attempted for this system. | Debris yield from upstream gravel mining into the Snake River reservoirs. |
| **UNDEFINED** | The variable has no agreed definition or measurement protocol. | "Operational trust" in SCADA telemetry during a cyber event. |

## What is NOT a valid epistemic state

**INSTITUTIONAL_EXCLUSION** is not a valid knowledge state. If a variable
physically influences the system, excluding it because it belongs to a
different agency, company, or regulatory field is a scope error, not an
epistemic one. The physics does not respect institutional boundaries.

The spec refuses to record a variable as absent because of ownership.
Instead, it records the variable as UNKNOWN_ATM, UNDER_STUDY,
NOT_STUDIED, or UNDEFINED — and names what would be needed to move it
to a quantified state.

## The standard

The question should not be:

> "Is this within our regulatory scope?"

But rather:

> "Does this physically influence the system's behavior?"

If the answer is yes, it belongs in the model. End of story.

The system is already interconnected. Our models and institutions are the
only things pretending otherwise. And that pretense has cost lives, money,
energy, and ecosystems on a scale that we are only beginning to
understand.

This spec does not pretend otherwise.
