# Effective Redundancy Audit — a test protocol

CC0. stdlib only. Runs on a phone.

A system claims N-fold redundancy. It fails anyway, all N channels down together.
Claim under test: the channels were never N. They shared a node that the
redundancy diagram cannot draw, because the shared node is a **process, an
input, a decision, or a budget** — not a component.

This document is a coding study. An undergraduate with public investigation
reports and a spreadsheet can run it and either confirm or kill the claim.

---

## 1. THE CLAIM (falsifiable)

```
N_nominal  = channels counted on the redundancy diagram
N_eff      = channels that survive failure of every shared node

H1  N_eff separates failed systems from systems that held.
H0  N_eff does not. N_nominal does just as well, or nothing does.

If H0, this method is worthless. That is the point of running it.
```

The interesting prediction is the second half:

```
N_nominal does NOT separate failed from held.
(failures LOOK redundant — that is why they passed their own audit)
N_eff DOES separate them.
```

If the visible count predicted outcome, no one would need this.

---

## 2. THE SHARED-NODE CLASSES (the coding scheme)

Six classes. Each is a yes/no question a non-expert can answer from a report.

```
A  AUTHORIZATION   one release / declaration / approval gates all channels' action
B  INFORMATION     all channels decide from one source
C  DISCRETION      one human decision sits upstream of all delivery
D  MAINTENANCE     one budget / calibration regime degrades all channels together
E  ENVELOPE        all channels sit inside one location or one design-basis number
F  VERIFICATION    all channels were validated against one standard / assumption
```

Coding question, per class, per case:

```
"Is there a node of this class that MORE THAN ONE channel depends on?"
```

Coding question, per channel:

```
"If every shared node you found fails, does THIS channel still work?"
   yes → channel is independent
   no  → channel collapses into the shared failure domain
```

`N_eff` = (count of independent channels) + (1 if any channel collapsed).
All collapsed channels count as **one** domain, not zero.

```
all channels share a node        → N_eff = 1
one channel escapes every node    → N_eff = 2
```

---

## 3. STUDY DESIGN

### 3.1 Sample — the part that kills bad versions of this study

```
DO NOT sample on disasters.
   sampling only failures conditions on the outcome → you cannot test anything.

DO sample on EXPOSURE, then observe outcome.
   pick a hazard class (flood warning, refinery startup, station blackout).
   collect every documented case exposed to it — failed AND held.
```

The held cases are where the method lives or dies. Templates that isolate the
variable (same hazard, one survived):

```
Fukushima Daiichi units 1-4 failed / units 5-6 held  (siting = the only change)
Onagawa held under the same tsunami                   (higher site)
Kerr County TX July 2025 failed / July 2026 held      (same weather, gate behavior changed)
```

Target ~8–15 cases. Public sources: CSB, NTSB, IAEA/INPO, FEMA after-action,
GAO, UN. All free PDFs.

### 3.2 Coding — the part that guards against imposed patterns

```
1. PRE-REGISTER the prediction (Section 1) before you open any report.
2. TWO coders, independently, blind to each other.
3. Each codes the 6 mode flags + per-channel independence from the report text.
4. Compute Cohen's kappa on the 6 mode flags across all cases.

   kappa < 0.6  →  the six classes are narrative, not real structure. STOP.
                   (this is the check on whether the pattern was invented.)
```

If two people reading the same report can't agree which node was shared, the
method is a story, not an instrument. Report the kappa first, always.

### 3.3 Scoring

```
per case:   N_nominal, N_eff, modes_present, outcome (failed / held)

2x2 on (N_eff == 1) vs outcome:

                 failed      held
   N_eff == 1      a          c    ← c = survived with no real redundancy: counterexample
   N_eff  > 1      b          d    ← b = failed WITH real redundancy: counterexample

   prediction: mass on a and d. b and c near zero.
```

### 3.4 What result kills the theory

```
1. b is large        failures had genuinely disjoint deps → shared node isn't the mechanism.
2. c is large        held systems also had N_eff==1 → shared node doesn't cause failure.
3. kappa low         coders disagree on modes → categories aren't real.
4. N_nominal         if channel count separates failed/held as well as N_eff,
   also separates     the invisible node added nothing.
```

Threats 2 and 3 are the honest ones. Foreground them.

---

## 4. CODE (stdlib, phone-buildable)

```python
# effective_redundancy.py  —  CC0, stdlib only
from dataclasses import dataclass, field
from math import comb

MODES = {
    "A": "authorization", "B": "information", "C": "discretion",
    "D": "maintenance",   "E": "envelope",    "F": "verification",
}

@dataclass
class Channel:
    name: str
    survives_all_shared_nodes: bool   # coder's call, considering EVERY mode

@dataclass
class Case:
    name: str
    domain: str
    outcome: str                      # "failed" | "held"
    modes_present: set = field(default_factory=set)   # subset of MODES
    channels: list = field(default_factory=list)      # list[Channel]

    @property
    def n_nominal(self):
        return len(self.channels)

    @property
    def n_eff(self):
        independent = [c for c in self.channels if c.survives_all_shared_nodes]
        collapsed   = 1 if any(not c.survives_all_shared_nodes
                               for c in self.channels) else 0
        return len(independent) + collapsed


def contingency(cases):
    a = b = c = d = 0
    for x in cases:
        collapsed = (x.n_eff == 1)
        failed    = (x.outcome == "failed")
        if   collapsed and     failed: a += 1
        elif not collapsed and failed: b += 1   # counterexample
        elif collapsed and not failed: c += 1   # counterexample
        else:                          d += 1
    return a, b, c, d


def fisher_exact_2sided(a, b, c, d):
    n, r1, c1 = a+b+c+d, a+b, a+c
    r2 = c + d
    def prob(x):
        return comb(r1, x) * comb(r2, c1 - x) / comb(n, c1)
    p_obs = prob(a)
    lo, hi = max(0, c1 - r2), min(r1, c1)
    return sum(prob(x) for x in range(lo, hi+1) if prob(x) <= p_obs * 1.0000001)


def nominal_means(cases):
    f = [x.n_nominal for x in cases if x.outcome == "failed"]
    h = [x.n_nominal for x in cases if x.outcome == "held"]
    mean = lambda v: sum(v)/len(v) if v else float("nan")
    return mean(f), mean(h)            # prediction: these are CLOSE


def cohen_kappa(c1, c2):               # two coders, aligned label lists
    n = len(c1)
    po = sum(1 for x, y in zip(c1, c2) if x == y) / n
    labels = set(c1) | set(c2)
    pe = sum((c1.count(l)/n) * (c2.count(l)/n) for l in labels)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def report(cases):
    a, b, c, d = contingency(cases)
    mf, mh = nominal_means(cases)
    print(f"n = {len(cases)}")
    print(f"2x2  [Neff==1]  failed={a} held={c}   [Neff>1] failed={b} held={d}")
    print(f"counterexamples: failed-with-redundancy={b}  held-without={c}")
    print(f"Fisher two-sided p = {fisher_exact_2sided(a,b,c,d):.4f}")
    print(f"mean N_nominal   failed={mf:.1f}  held={mh:.1f}   (predict: close)")
    for x in cases:
        print(f"  {x.name:28s} Nnom={x.n_nominal} Neff={x.n_eff} "
              f"modes={sorted(x.modes_present)} -> {x.outcome}")
```

---

## 5. WORKED EXAMPLE (so you see the coding move)

Kerr County TX, July 4 2025. Public reports: NWS issued 22 warnings; forecast
and radar were correct. Channels that could reach a person, and whether each
survives failure of the shared nodes:

```
shared node C (discretion): one county activation decision upstream of delivery
shared node (reception):    a channel delivered at 3am reaches no one asleep w/o a receiver on

  WEA to all phones     county never sent it          -> dies on C        -> collapses
  CodeRED               county-activated, +enrollment  -> dies on C        -> collapses
  sirens                did not exist                  -> n/a
  NOAA weather radio    fires on NWS, NOT the county   -> survives C
                        but needs a receiver on at 3am -> dies on reception-> collapses

  independent channels = 0
  N_eff = 0 + 1 = 1        N_nominal ~ 4
  outcome = failed
```

Teaching point: weather radio escaped Mode C — so a naive coder stops at
N_eff = 2. You do not stop. You test the channel against **every** node. It
shared a reception dependency, so it collapses too. N_eff = 1.

Control, same county, next year: activation behavior changed, four alerts
issued early. The discretion node stopped collapsing everything. Held.

```python
cases = [
    Case("Kerr County 2025", "county_em", "failed", {"C"}, [
        Channel("WEA_all_phones", False),
        Channel("CodeRED",        False),
        Channel("weather_radio",  False),   # escapes C, dies on reception
    ]),
    Case("Kerr County 2026", "county_em", "held", set(), [
        Channel("WEA_all_phones", True),
        Channel("CodeRED",        True),
    ]),
    # ... your 8-15 cases here, coded blind, two coders
]
report(cases)
```

---

## 6. SEED CASES — DO NOT TEST ON THESE

These built the hypothesis. Testing on them is circular. They are here only to
show the coding format and to let the code run before you have your own data.

```
Katrina staging      logistics   A            staged supply, no assembly owner        failed
East Palestine       rail-chem   B            6 agencies, 1 NS-mediated hazard input   failed
Kerr County 2025     county_em   C            1 activation gate over all delivery      failed
BP Texas City        refinery    D            deferred maint degraded all instruments  failed
Fukushima 1-4        nuclear     E,F          basement elevation < design basis        failed
Fukushima 5-6        nuclear     (E escaped)  1 air-cooled DG above envelope           held
```

Your job is the cases NOT on this list.

---

## 7. THE RECURSION (why this survives every reform)

```
Mode F is the audit itself.
The instrument that certifies redundancy is validated against one standard.
So the checker is a shared node.
Counting channels always passes, because the diagram cannot draw
   a process, an input, a decision, or a budget.

The test in this document is an attempt to build the missing instrument.
If Section 3.4 kills it, it was the wrong instrument — say so and publish that.
```
