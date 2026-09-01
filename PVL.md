# PVL — Phenomenological Validation Layer

**Reference layer.** The entry to this repository is
[`META-PROTOCOL.md`](META-PROTOCOL.md); read that first. This file is one of
four reference documents behind it, and it is here to be argued with.

PVL is the operational half of [`BNRAM_STRICT.md`](BNRAM_STRICT.md) §IV-D:
BNRAM marks a process as observed-but-unmapped, and PVL is how you take a
reading on it.

---

## 1. Ask the thing before you ask the record

**The move:** when a claim arrives — an architectural technique, a
land-management practice, a maintenance interval — do not open with a
literature search. Open with a query on the physical state.

- **Step A.** Identify the physical boundary condition. The structure's
  current state. The soil's erosion rate. The water table. What the thing
  does when you load it.
- **Step B.** Read what is available: your own measurement, satellite,
  geological logs, meteorological archives, or the object itself. Does the
  present physical state match what the practice is claimed to produce?

**Why this order.** The record has a shape, and loading that shape first
means seeing the object through it. Reading the object first gives you an
independent measurement, which is what lets you audit the record instead of
only absorbing it. This is [`META-PROTOCOL.md`](META-PROTOCOL.md) MOVE 1.

**Reading:** if the present physical state matches the claimed outcome, the
practice is **phenomenologically validated** — it produced the state that is
there, whether or not a written manual for it exists. That is a statement
about outcome, not about mechanism; §3 is what keeps the two apart.

---

## 2. Weigh by persistence, not by volume

**The move:** weight how long something has held under load above how many
times it has been repeated. Five hundred years of structural integrity has
survived more tests than five thousand recent posts. Repetition count
measures circulation; persistence measures survival.

**Worked cases.** Indus Valley drainage and qanat irrigation are the two
that carry this section. Both are old, both are still moving water, and both
have a measurable present state to query under §1 — which is what makes them
readings rather than examples.

**On the formula that used to be here.** An earlier version gave

```
Validation Score = Ph / Total Energy
```

and offered the Egyptian pyramids as the headline case. Two problems, and
they compound. `Ph` was never defined and carried no units, so the ratio had
none either. And a monument with an enormous construction energy scores *low*
on that ratio — the formula ranks the pyramids near the bottom, which is the
opposite of the point the passage was making with them. The formula has been
removed rather than repaired, because repairing it means choosing what `Ph`
is, and that is a real decision with a real option set rather than a
notation cleanup.

Stated in words, which is what the section can currently support:

> A structure or practice that has kept doing its job for centuries, on
> maintenance that its own community could supply, has been tested by
> conditions no study will reproduce. Weight it accordingly, and go measure
> what it is doing now.

If you want the ratio back, `RESEARCH_RENDER.md`'s DECISION entry is the
shape to write it up in: the fork is what `Ph` should be, and the options
are at least service-lifetime, output-per-maintenance-input, and
output-per-unit-embodied-energy. They rank differently and each is
defensible.

---

## 3. Opaque source, verified outcome

Non-written systems — oral transmission, working practice held in hands,
trade knowledge — have no source text to read. They are categorised as
**verified outcomes, opaque source** and are usable in planning on that
basis.

**Medium is not a tier.** Written, oral, carved, built, chain-of-custody,
firsthand: these are how something was carried, not how true it is. The
sorting question is *how has this been tested?*, never *was it printed?*
[`BNRAM_STRICT.md`](BNRAM_STRICT.md) §IV-B carries the same cut from the
other side — institutional authority is worth zero as a reason to accept a
claim, and that says nothing about the medium the evidence arrived in.

**What the flag buys.** An opaque source with a verified outcome is usable
and it is unmapped, so the standing note travels with it: continuous
observation on the local environment is what would catch drift before it
becomes visible in the outcome. Not a warning about the source. A statement
about what is not currently instrumented.

---

## 4. What would change this layer

| result | consequence |
|---|---|
| a practice that is phenomenologically validated under §1 and whose present state turns out to be produced by something other than the practice | §1 is confounded; it needs a control, and the layer should say what one looks like |
| persistence turns out to track something other than fitness to conditions — survivorship in the record, protection from the load, or selective preservation | §2 is measuring the archive rather than the practice, which is the survivorship problem the shape spec's §6 also runs into |
| the opaque-source flag makes no difference to any downstream decision anyone takes | §3 is bookkeeping and should be cut |
| the physical-state query returns `SILENT` for most claims of interest — no reachable present state to compare against | not a refutation, a bound; write the bound down |

A result that lands in this table updates the layer rather than being
absorbed into it as a special case.

---

**Next:** [`RESEARCH_RENDER.md`](RESEARCH_RENDER.md) is how a gap you found
gets written up so someone else can run it.
[`BNRAM_STRICT.md`](BNRAM_STRICT.md) §IV-D is the upstream flagger.

CC0.
