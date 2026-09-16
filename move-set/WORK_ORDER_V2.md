# WORK ORDER — move set, second order

Delivered 2026-09-16. Landed verbatim. Not edited.

```
repo: JinnZ2/method-layer or sims repo
stdlib only, CC0, phone-buildable

BUILD: move_set_sim.py

PURPOSE: reproduce the audit as a MOVE SET not a
reasoning trace, runnable on any domain of
published artifacts.

MOVES (six, domain-agnostic):
  M1 ask where a number came from
  M2 ask what a term is standing in for
  M3 ask whether a stated relationship is still
     held by anything
  M4 perturb and see what moves
  M5 check whether the instrument would report
     its own failure
  M6 refuse to score what cannot be seen;
     make the absence a first-class value

SCORING RULE (build it in):
  a correctly-refused verdict scores as high as
  a correct one
  absence moves must be selectable

INPUT: any published artifact that ships values and
  states relationships between them

OUTPUT per move:
  move_id / finding / confidence / or ABSENT(reason)
  ABSENT is a valid output, not an error

DEMO: run on at least one public artifact; include
  the input file in the repo.
```
