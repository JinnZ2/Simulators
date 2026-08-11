# Framework Overview

## Core Thesis

Incidents rarely result from a single failure point; they occur when minor friction
points across multiple dimensions align. The MSIAF exists to expose how systemic
incentives, infrastructure choices, and regulatory loopholes **passively engineer a
disaster long before a driver ever touches the wheel**.

## The Four Dimensions

### D1 — Human Factors & Physiology
Fatigue, dehydration, micronutrient depletion, circadian misalignment, cognitive
fragmentation, visual tunneling, reaction-time degradation. These are not random
variables — they are the predictable output of compensation and scheduling models.

### D2 — Operations & System Design
Dispatch pressure, algorithmic route density, pick-rate escalation, app notification
design, countdown timers, scheduling without slack, and data feeds whose staleness
or latency is invisible to the operator.

### D3 — Infrastructure & Environment
Road surface quality, intersection geometry, curb/loading-zone policy, signal
phasing, shared human-machine lanes, terminal layouts, pavement fatigue limits,
and municipal code that predates current usage volumes.

### D4 — Financial, Insurance & Regulatory
Penalty clauses (temperature excursion, delivery windows, demurrage), SLA terms,
independent-contractor classification, split-liability staffing, deductible
structures that punish incident reporting, and bonus systems tied solely to
throughput.

## Systemic Interconnection Pathways

Typical alignment cascades:

- **Infrastructure → Operations → Physiology**: Reduced maintenance budgets leave
  tire debris in lanes (D3). Outdated dispatch feeds route vehicles through these
  zones without warning (D2). A driver with mild dehydration or micronutrient
  deficiency experiences micro-delays in visual processing, narrowing evasive
  options (D1).
- **Financial/Insurance → Management → Human Performance**: Strict delivery
  penalties in contract terms (D4) create top-down dispatch pressure (D2), which
  disincentivizes rest, meal, and hydration stops (D1), leading to fatigue and
  compromised spatial awareness in dense traffic.

## The Visibility Asymmetry

High-visibility, low-frequency events (e.g., hazmat spills) absorb regulatory
attention and often already have aligned safety incentives — severe consequences
force proactive planning. The framework's real target is the **mundane,
high-frequency systemic killer**: diffuse penalties that incentivize constant
low-level risk-taking across last-mile delivery, warehousing, drayage, and general
freight — damage that accumulates quietly and never makes the news.

## Closed-Loop Architecture

In proactive form, the cascade becomes a feedback loop:

```
[ D4: FINANCIAL & REGULATORY ]
   ⬇  (incentives and constraints pass to...)
[ D2: OPERATIONS & SYSTEM DESIGN ]
   ⬇  (operational rules shape use of...)
[ D3: INFRASTRUCTURE & ENVIRONMENT ]
   ⬇  (physical environment supports/protects...)
[ D1: HUMAN FACTORS & PHYSIOLOGY ]
   ⬇  (physiological/telematics data feeds back...)
[ BACK TO D4: premiums, bonuses, compliance monitoring ]
```
