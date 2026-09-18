# substrate-alternative

Two modules.  One locates money-frame assumptions in text and
proposes nothing.  The other runs a food-distribution coordination
loop on ICS structure with the price signal taken out, and reports
what it could not move as a value rather than as an error.

CC0.  Python 3 standard library only.  No network.  Parses under
3.9.  Phone-buildable.

```
python3 frame_audit.py FILE          locate money-frame tokens
python3 frame_audit.py -             ... from standard input
python3 frame_audit.py --choices

python3 pilot_loop.py --demo         run the constructed scenario
python3 pilot_loop.py --screen       screen the loop for slippage
python3 pilot_loop.py --choices

python3 test_substrate.py            126 checks
```

---

## frame_audit.py -- locate only

```
   text
     |
     v
 [ registry: 165 surfaces, 5 frames, 32 with a second live sense ]
     |
     v
 [ one alternation, longest surface first ]     [CHOICE 1]
     |
     v
 hits ---> token | sentence index | char span | frame
     |
     +---> counts            (all five frames, zeros visible)
     +---> counts_unambiguous
     +---> counts_ambiguous  (never merged with the above)
```

Five frames: `OWNERSHIP`, `PRICE`, `TRANSACTION`,
`SCARCITY_AS_GIVEN`, `VALUE_AS_PRICE`.

There is no replacement field.  There is no score, no verdict and
no rewrite.  A hit is a **location**.  That is enforced by an AST
walk in the suite rather than promised in prose, and the scan is
planted against so its silence means something.

**The limit is stated at the top of the file, not the bottom.**
This is a word list and a paraphrase steps around it:

| sentence                                              | hits |
|-------------------------------------------------------|------|
| `You have to pay for it.`                              | 1    |
| `It takes something from you before you may have it.`  | 0    |
| `They compete.`                                        | 1    |
| `They are competing.`                                  | 0    |

So a zero is a property of **the registry**, never evidence that a
text is frame-free.  The registry's coverage is the measurement;
the text is only the sample.

**Three counts, kept apart.**  `value` (absolute value),
`property` (a property of a system), `cost` (a cost function),
`budget` (an energy budget), `competition` (a measured ecological
interaction), `efficiency` (a measured ratio) -- 32 entries carry
a live non-money sense, each with the sense stated.  They are
counted apart, never silently included and never silently dropped.
The module locates; it does not adjudicate which sense is live.

---

## pilot_loop.py -- ICS with the price signal removed

```
 capacity declarations            need declarations
 (who has what, ready when)       (who needs what, wanted by when)
        \                                /
         \                              /
          +---------> matching <-------+      [CHOICE 2] [CHOICE 3]
                         |                    ours, not ICS's
                         |
          +--------------+---------------+
          |                              |
          v                              v
      ALLOCATED                        UNMET
  from / to / qty / dep /        node / resource / qty / reason
  arr / lag                      a RETURN TYPE, not an error
          |
          v
   lag = arrival - declaration       [CHOICE 6]
          |
          v
   per node, per resource: needed, met, unfilled,
   lags[], max_lag, min_lag     -- no total, no ranking [CHOICE 7]
```

`UNMET` reasons, all four reachable and asserted so:

| reason                  | what it means                          |
|-------------------------|----------------------------------------|
| `NO_CAPACITY_DECLARED`  | nobody declared that resource at all   |
| `CAPACITY_EXHAUSTED`    | it existed and earlier needs drew it   |
| `UNREACHABLE`           | it exists, no route is declared        |
| `ARRIVES_AFTER_HORIZON` | reachable, arrives past the deadline   |

An undeclared route is `None`, never a large number and never
zero.  A node that received nothing has `max_lag None`, never `0`.

### The finding

The screen over the loop's own source:

```
unexempted hits : 0   FLAGGED: False
exempted hits   : 5   -> compensation, cost, finance, procurement
```

Every token that fires is a name **ICS itself gives** a part of
its structure:

```
 ICS General Staff
   Operations   Planning   Logistics   Finance/Administration
                                        |
                        +---------------+---------------+
                        |        |             |        |
                      Time   Procurement   Compensation  Cost
                      Unit      Unit        /Claims Unit  Unit
```

One of four sections, and three of its four units, are the part of
the structure this loop has no channel for.  A pilot that borrows
ICS as a non-monetary substrate has dropped or repurposed a
quarter of what it borrowed, and the doctrine's vocabulary says so
before any of ours does.  That is the single exempted region, and
it is measured in three arms: masked, the file is clean; unmasked,
the carried block is the only thing that fires; planted, a token
outside the region is caught.

### Two limits, stated up front

**It is smaller than it sounds.**  A matching rule that hands
limited capacity to several needs IS a distribution decision.  A
number attached to a unit of food is one such rule.  Removing it
does not remove the decision -- it makes the rule explicit,
logged, and arguable.

**The screen has a blind spot shaped like the substrate.**  ICS is
a *command* structure: it coordinates under a declared incident
with a declared commander.  So this loop substitutes an allocation
rule for one signal **and an authority for another**.
`frame_audit` screens for one vocabulary; the authority assumption
is not in it.  The screen returns clean on a module that made a
second substitution it cannot see.

---

## Carried, not verified

Everything about ICS here -- the General Staff sections, the
Finance/Admin units, ICS-213RR / 211 / 204 / 215, the
resource-status vocabulary, span of control 3-7, the Planning P --
is transcribed from public doctrine **from memory**.  This
environment's network is an allowlist and the doctrine hosts are
not on it, so nobody here opened a source.  The finding above
rests on it and says so.

Every scenario in the folder is constructed.  Nothing here is a
statement about any actual food system.

Findings and their falsifiers: [`CLAIM_TABLE.md`](CLAIM_TABLE.md),
`SA_001..SA_018`.
