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
mine_logs.py         reads gate_*.json + gate_*.denied.json
explore.py           widens one declaration. ranks nothing.
retro_sim_stack.py   second replay, declared differently. disagrees
                     with the first about SIM-B, on purpose.
SIM_STACK_BACKTRACE.md  the audit these guards were back-traced from
AUDIT_NOTES.md       what broke, what was fixed, what is a limit
tests/               69 tests. run: python3 -m unittest discover tests
```

```
python3 gate.py               # selftest
python3 replay_sim_stack.py   # test case
python3 make_docs.py          # regenerate docs
python3 mine_logs.py .        # what fired, what denied, what nobody looked at
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
      physical claim resting on generator-level support
        -> qualified, not supported
      physical claim with NO physical-level support at all
        -> qualified. a residual count is a property of the
           classifier; an artifact floor a property of the
           estimator. neither becomes a property of the
           system by being counted.
        -> does not fire when physical support is present:
           "the separation exceeds the error bar" needs
           the error bar
      convergence claim -> must name what the results share
      divergence -> the author's explicit call, or NOT ASSESSED.
        never inferred by comparing two prose strings
```

Every denial writes `gate_<SIM>.denied.json` before raising. A guard
that stops a run has to leave a record, or it reads as never having
fired.

There is one gate. Everything else imports it:

```
GATE_SRC = os.environ.get("GATE_SRC", ".../reasoning-gate")
sys.path.insert(0, GATE_SRC)
from gate import Gate, Resolution, Control
```

`../tools/check_gate_drift.py` finds any copy, drifted or not, and
`../tests/test_gate_drift.py` fails the suite if one lands. Five
pre-repair copies arrived across three drops before that existed.

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
