# DISPATCH — M0 scope move for move_set_sim.py
**Target: Claude Code**
**Repo: wherever move_set_sim.py lives (JinnZ2/method-layer or sims repo) — CHECK FIRST, report path before building**
stdlib only, CC0, phone-buildable

---

## WHY
```
current move set  M1..M6 run on the claim AS STATED
gap               nothing checks whether the stated box
                  is the real box before the moves run
failure it causes moves reason correctly inside a box
                  that isn't there — clean output, wrong scope
source            2026-10-03 session, scope-finding practice
                  (named instrument, Kavik's standing practice)
```

## BUILD
```
M0  scope check — runs BEFORE M1, output bounds M1..M6

INPUT
  claim       as stated (title / abstract / citation line)
  artifact    methods-level text or structured fields

SUB-CHECKS (each returns value | ABSENT(reason))
  S1  COUNT        n of units actually measured in THIS artifact
                   (not n cited from prior work)
  S2  MODE         measured | modeled | simulated | robotic proxy
  S3  REFERENT     the system named in the claim vs the system
                   the data came from (organism vs proxy, field vs lab)
  S4  LOGIC        sufficiency | necessity | both | unstated
                   (existence proof shows sufficiency only)
  S5  LOCATION     where the real scope is stated:
                   abstract | methods only | not stated

OUTPUT
  claimed_scope   (from claim)
  actual_scope    (from S1..S4)
  gap_list        one row per mismatch: field / claimed / actual
  status          NO_GAP | GAP | ABSENT(reason)

RULES
  - S5 = "methods only" is a FINDING, not a pass
    (scope exists but is not where the claim travels)
  - missing scope statement -> ABSENT, never NO_GAP
  - cited n from prior work does NOT fill S1
  - M1..M6 receive actual_scope; any M-finding that
    depends on claimed_scope beyond actual_scope is tagged
    OUT_OF_SCOPE, not scored
  - scoring rule unchanged: correct ABSENT scores as high
    as a correct finding
```

## DEMO FIXTURE — external, precedes implementation
```
artifact  Garnier, Combe, Jost, Theraulaz (2013)
          PLOS Comp Biol 9(3) e1002903
          "Do Ants Need to Estimate the Geometrical Properties
           of Trail Bifurcations to Find an Efficient Route?
           A Swarm Robotics Test Bed"

expected (traceable to the publication, not to this build):
  S1  10 robots (Alice); 0 ant colonies in this paper
  S2  robotic proxy, light trails
  S3  claim names ants; data from robots; ant comparison is
      a citation to earlier colony work
  S4  sufficiency (local rule is enough); silent on necessity
      — robots were PROGRAMMED with the local rule
  S5  scope legible in methods, title reads as ant finding
  status  GAP

VERIFY each expected value against the paper before
committing the fixture. If any differs, the paper wins —
report the difference, do not adjust the check to match.
```

## TESTS — must cover failure paths
```
T1  Garnier fixture            -> GAP, all 5 rows populated
T2  claim matches data exactly -> NO_GAP
T3  artifact with no methods   -> ABSENT(no scope source)
T4  cited-n-only artifact      -> S1 ABSENT, not filled
T5  M-finding beyond scope     -> OUT_OF_SCOPE tag present
```

## CARRY FROM DISPATCH 4 OPEN DEFECTS
```
- register M0 EXPLICITLY, not reachable-from-module-tail
  (that shape has landed 3 times; do not make it 4).
  If cheap: add the structural check that fails the run
  on any tail-only registration.
- key-holder rule: T2..T5 inputs are implementation-first
  -> declare as REGRESSION, not validation. Only T1 is
  externally traceable.
- report denominators with one number per set.
```

## RETURN
```
path found | files changed | commit hash
suite result | T1..T5 pass/fail
any fixture value that disagreed with the paper
```
