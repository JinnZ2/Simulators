# WORK ORDER — GAP 4 measurement rig
## agent setup/teardown energy and succession loss

CC0. stdlib only. no network at runtime. phone-buildable.
Runs on one machine with one GPU. No lab access required.

Companion to WORK_ORDER_labor_instrument.md (PART 2, GAP 4).

---

## The gap

Agent spin-up cost — context loading, weights resident, cold start — is
charged to overhead and never divided by task. So N single-task agents
and one agent doing N tasks look identical in every current accounting.
In joules they are not.

Current agent lifespan is often exactly one task. The unit then ceases.
The energy and dependencies required to bring it into existence to do
that one task are not allocated anywhere. That is a loss in the
succession itself.

No published measurement of this exists. This rig produces the first
number.

---

## What is being measured

Joules, by phase, per agent lifecycle.

    PHASE 0   idle baseline          (machine up, nothing loaded)
    PHASE 1   spin-up                (load -> ready, before first task input)
    PHASE 2   task execution         (input accepted -> output delivered)
    PHASE 3   teardown               (release -> back to idle baseline)

Integrate power over each phase. Baseline-subtract PHASE 1/2/3 against
PHASE 0 so the reported figure is marginal, not total machine draw.

    E_phase = integral(P(t) - P_idle) dt   over the phase window

---

## Instrumentation

Take BOTH. They measure different things and the difference is itself
a finding.

**A. Wall meter** — any inline AC power meter with logging
(Kill-A-Watt style, or a smart plug with an export).
Captures: full system draw including PSU losses, fans, chipset,
RAM, storage. This is the honest number for "what did the world spend."

**B. Card telemetry** — `nvidia-smi --query-gpu=power.draw
--format=csv,noheader -lms 100` or vendor equivalent.
Captures: accelerator draw only.

Sample at >= 10 Hz on both if possible. Spin-up is short and spiky;
1 Hz will miss the peak and undercount.

Record the delta between A and B. Card-only accounting is the number
labs would publish if they published one; wall accounting is the number
that closes against a utility bill. The ratio is worth reporting on its
own.

---

## Runs

Same model. Same total task count. Same task class. Vary only the
lifecycle pattern.

    RUN A   N agents, 1 task each, full spin-up and teardown per task
    RUN B   1 agent, N tasks, one spin-up and one teardown total

Suggested N: 1, 5, 20, 100. Repeat each condition >= 5 times.
Randomize run order. Let the machine return to a stable idle baseline
between runs — record how long that takes, it is not instantaneous
and thermal state carries over.

**Controls to hold and record, not assume:**
- ambient temperature (thermal state changes draw materially)
- clock/power state of the accelerator at run start
- whether weights were in page cache or read from disk (cold vs warm
  start is a large term; report them separately, never averaged)
- background load on the machine
- for hosted models, this rig does not apply — it measures local only.
  Say so in the writeup. Do not extrapolate to hosted inference.

---

## Outputs

    per-run record:
      run_id, condition (A|B), N, task_class, model_id,
      E_spinup_wall, E_task_wall, E_teardown_wall,
      E_spinup_card, E_task_card, E_teardown_card,
      cold_or_warm, ambient_c, wall_clock_per_phase

    derived:
      setup_fraction     = E_spinup / (E_spinup + E_task + E_teardown)
      amortization_curve = joules_per_task_instance vs N
      succession_loss    = (total E, RUN A) - (total E, RUN B), same N

`succession_loss` is the headline figure. It is the joule cost of
disposability, holding work delivered constant.

`amortization_curve` should fall as N rises. Where it flattens is the
point past which persistence stops paying. That crossover is the
decision-relevant number for anyone choosing a deployment pattern.

---

## Reporting

Report as a table. Report the raw per-run records alongside the
derived figures — someone else must be able to recompute the derived
numbers from the raw ones without trusting this pipeline.

Report wall and card figures separately. Never blend them.
Report cold and warm start separately. Never average them.

State the hardware, the model, the task class, and the ambient
conditions. A joule figure without those is not reproducible and
should not be cited as one.

---

## What this does NOT measure

Named so nobody over-reads the result:

- training energy amortized across inference (separate, larger, and
  not addressed here)
- manufacturing energy of the hardware itself
- cooling load beyond what the wall meter sees at this machine
- hosted/datacenter inference, where batching changes everything
- network energy for remote calls

This rig measures ONE local machine, ONE model, lifecycle patterns
held against each other. That is a small claim and it should be
stated as a small claim. It is also currently an unmade one.

---

## Acceptance

The result is usable when: a second party with different hardware and
a different model can run the same protocol, and the DIRECTION and
rough SHAPE of the amortization curve reproduce, even though the
absolute joule figures will not.

Absolute numbers are hardware-specific. The shape is the finding.

---

## POSTING NOTE

CURRENT GAP. PLEASE HELP.

Anyone with a GPU and a power meter can produce the first number.
No institutional access required, no proprietary data, no funding.
Raw records and derived figures both welcome. Partial runs welcome —
a single well-documented cold-vs-warm spin-up measurement is more
than currently exists in public.
