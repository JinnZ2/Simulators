# reasoning gate

Fail-closed harness for simulation and audit work. Stdlib only,
no network, phone-buildable. CC0-1.0.

```
guards.json          single source of truth (8 guards, 3 stages)
gate.py              the harness. default deny.
make_docs.py         guards.json -> GUARDS.md (generated, not hand-edited)
GUARDS.md            human-readable, regenerate after any json edit
replay_sim_stack.py  test case: replays an audited stack, gate must
                     pass the sound sim and catch the other two
```

```
python3 gate.py               # selftest
python3 replay_sim_stack.py   # test case
python3 make_docs.py          # regenerate docs
```

## What it enforces

```
PRE   expected output, resolution check, named controls
      with predicted values, discrimination argument
      -> missing any: the sim does not run

MID   every quantity tagged  generator | physical | instrument
      plus the object it is a property of
      -> untagged: not recorded
      -> promotion between layers needs explicit justification

POST  ratio across unlike objects -> void
      claim with no named support -> unsupported, excluded
      convergence claim -> must name what the results share
```

## Status

This is a marker, not a position. It is one shape fitted to one
audited artifact. Test fit, extend it, or report where it breaks.

n=1. The patterns it encodes were back-traced from a single paired
sample: one sound simulation run alongside two deliberately un-gated
ones so the divergence was observable. They are candidate shapes to
check against the next audit, not established results.

`strict=True` denies on post-stage violations too. `strict=False`
logs them as findings and lets the run finish, which is what you
want when the point is to observe the failure.
