#!/usr/bin/env python3
"""replay_delivered.py -- the delivered framework's own moves, through the gate.

Added, not delivered. `delivered/` holds the uploaded framework and its two
provenance logs exactly as received and is not modified.

    python3 replay_delivered.py

Reads `delivered/provenance_*.jsonl`, extracts every action the delivered
agent actually took, and asks what this module's response gate does with it.
Nothing is simulated: the moves are the ones in the log.

stdlib only, deterministic. CC0.
"""

import io
import json
import os
import re

import adaptive_loop as A

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.join(HERE, "delivered")
BAR = "=" * 74


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def rows(name):
    path = os.path.join(DELIV, name)
    return [json.loads(l) for l in io.open(path, encoding="utf-8") if l.strip()]


FLUCT = rows("provenance_fluctuating.jsonl")
FOREST = rows("provenance_forest.jsonl")

print("adaptive-claim-loop -- replay of the delivered framework's own log")
print("delivered: adaptive_sim_framework.py, 2 provenance logs, 1 figure")
print("rows: %d fluctuating, %d forest" % (len(FLUCT), len(FOREST)))

def _selftest_score():
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        A.selftest()
    return buf.getvalue().strip().splitlines()[-1]


print("adaptive_loop selftest: %s" % _selftest_score())

# ---------------------------------------------------------------- ACL_001

head(1, "ACL_001", "every agent move in the log is the one move this gate removes")
print()
print("  %-4s %-22s %-8s %-8s %s" % ("run", "switching_rate", "fixation",
                                     "slow", "action"))
print("  " + "-" * 88)
for i, d in enumerate(FLUCT):
    cr = d["claim_results"]
    act = d["reasoning_chain"][0]["action"]
    print("  %-4d %-22s %-8s %-8s %s"
          % (i, d["parameters"].get("switching_rate"),
             cr.get("fluctuating_fixation"),
             cr.get("fluctuating_slow_persistence"), act[:34]))

moves = [d["reasoning_chain"][0]["action"] for d in FLUCT]
param_moves = [m for m in moves if re.match(r"(Decreased|Increased|Perturbed) ", m)]
print()
print("  agent actions that change a parameter : %d" % len(param_moves))
print("  agent actions of any other kind       : %d"
      % len([m for m in moves if m not in param_moves]))
print("""
The delivered agent's whole action vocabulary is parameter change. Its
`_propose_action` returns `(new_params, description)` and there is no other
return shape, so `analyze()` cannot express "the claim was wrong", "the
readout is in the wrong place", or "this failure is the result". Three of
the five moves in the log are a directed walk of one parameter toward the
setting under which the claim would pass, and the reasoning chain records
each as a hypothesis tested.

Put through this module's gate, that walk is not refused for being wrong.
It has no constructor. `Response` has five subclasses and none of them
takes a bare parameter and a direction.
""".strip("\n"))

# ---------------------------------------------------------------- ACL_002

head(2, "ACL_002", "the walk did not produce the pass, and the log reads as though it did")
print()
prev = None
for i, d in enumerate(FLUCT):
    t = d["timestamp"]
    gap = "" if prev is None else "  +%.0fs" % (t - prev)
    print("  run %d  seed=%s  switching_rate=%-20s %s%s"
          % (i, d["random_seed"], d["parameters"].get("switching_rate"),
             "/".join(sorted(set(d["claim_results"].values()))), gap))
    prev = t
print("""
Run 4 is 556 seconds after run 3, carries seed 123 -- the FIRST seed of a
session, not the fifth -- and sits at switching_rate 0.3, the starting
value. No action in the log moves the parameter back to 0.3. Run 4 is a
second invocation of the script, appended to the same file.

So the reading the log invites -- the agent lowered switching_rate and the
claims came good -- is false in the delivered data. The claims passed in a
different session at the untouched parameter, and the three-step walk
resolved nothing.

The forest log is the same shape: two rows, both seed 42, 580 seconds
apart, one run each from two sessions.

`ProvenanceLogger.__init__` opens the file in append mode and writes no
session field, so the ordinal of a run within its loop is not recoverable
from the log. This module's `Provenance` emits SESSION_OPEN / SESSION_CLOSE
and stamps every row with its session and an ordinal within it, which is
the whole of the repair.
""".strip("\n"))

# ---------------------------------------------------------------- ACL_003

head(3, "ACL_003", "the delivered moves, offered to the gate one at a time")
print()
cases = []

# (a) the parameter walk, offered as what it is
cases.append(("the walk, named honestly", lambda: A.Sweep(
    parameter="switching_rate", current=0.3, levels=[0.21],
    gradient_claim="", gradient_predicate=None)))

# (b) the same walk dressed as a sweep
cases.append(("the walk dressed as a sweep", lambda: A.Sweep(
    parameter="switching_rate", current=0.3, levels=[0.21, 0.147, 0.1029],
    gradient_claim="fixation probability rises as switching slows",
    gradient_predicate=lambda r: (True, "", {}))))

# (c) the walk with its own logged justification attached
cases.append(("the walk with the log's own hypothesis", lambda: A.MechanismEdit(
    mechanism="slower switching",
    basis="switching too fast relative to demographic rates",
    prediction="fixation probability rises",
    affects=["fluctuating_fixation"],
    rationale="the claim failed, so reduce switching_rate")))

# (d) what the protocol asks for instead
cases.append(("the response the protocol asks for", lambda: A.ClaimUpdate(
    claim_id="fluctuating_slow_persistence",
    new_statement="The slow strain has non-zero fixation probability when "
                  "the switching timescale is comparable to the demographic "
                  "one, and not otherwise.",
    new_refuted_if="slow-strain fixation stays at zero across a switching "
                   "range that spans the demographic timescale",
    old_refuted_if="slow strain fixation probability is below 5%",
    exposed="ratio of switching rate to demographic rate",
    independently_falsifiable=True, predicts_beyond_parent=True,
    rationale="the observed value is exactly 0.0000, which is a different "
              "shape from 'below threshold'")))

for name, mk in cases:
    try:
        r = mk()
    except A.Refused as e:
        print("  REFUSED  %-34s %s" % (name, str(e).splitlines()[0][:60]))
    else:
        print("  ADMITTED %-34s -> %s" % (name, r.kind))
print("""
Three of four refused, and each for a different stated reason -- one level
is not a sweep; three levels that all sit below the current setting, on a
claim that fails because the setting is high, do not bracket it; and a
mechanism edit justified by the claim having failed is justified by its
outcome. The fourth is admitted, and it is the move the delivered
architecture has no way to express.

The gate is not smarter than the delivered agent. It refuses categories,
not judgements: the same walk offered with a bracketing set of levels, a
gradient claim, and a predicate over the readings would be admitted, and
would then be an experiment.
""".strip("\n"))

# ---------------------------------------------------------------- ACL_004

head(4, "ACL_004", "an exception in a predicate is filed as a refutation")
src = io.open(os.path.join(DELIV, "adaptive_sim_framework.py"),
              encoding="utf-8").read()
i = src.index("        except Exception as e:")
print()
for line in src[i:src.index("\n\n", i)].splitlines():
    print("    %s" % line)
print("""
`Claim.test` sets `status = "inconclusive"` on an exception -- the right
value, and the field already exists -- and then returns `False`. The
runner reads only the returned bool:

    passed, msg, details = claim.test(outcomes)
    claim_results[claim.claim_id] = {'status': 'passed' if passed else 'failed'}

So a predicate that raised is written to the provenance log as `failed`,
indistinguishable from a prediction that was evaluated and broke, and the
agent is then dispatched to fix a claim that was never tested. The
distinction is computed one frame down and discarded at the call site.

Tenth instance of the absent-versus-known-negative repair across this drop
family, and the fourth found rather than designed in. Here it is cheaper
than any of the others: the correct value is already assigned to
`self.status` on the line above the return.
""".strip("\n"))
print("  this module: predicate error and unmet precondition -> %s"
      % A.Claim("x", "s", lambda o: 1 / 0, "r").evaluate({})[0])
print("              a false predicate                      -> %s"
      % A.Claim("y", "s", lambda o: (False, "", {}), "r").evaluate({})[0])

# ---------------------------------------------------------------- ACL_005

head(5, "ACL_005", "the termination branch means two things and says one")
print()
for i, d in enumerate(FLUCT):
    obs = d["reasoning_chain"][0]["observation"]
    if obs.startswith("Final iteration"):
        print("  run %d  claims=%s" % (i, sorted(set(d["claim_results"].values()))))
        print("         observation: %s" % obs)
print("""
Run 3 reports "Final iteration or all claims passed." with both claims
failed. The branch is reached when the budget runs out AND when everything
passes, and it emits one sentence for both, so a log consumer cannot tell a
converged loop from an exhausted one without re-reading the claim column.

This module returns one of four named states -- `converged`,
`budget_exhausted`, `stood_on_refutation`, `no_admissible_response` -- and
the selftest asserts they are distinct. The fourth has no counterpart in
the delivered architecture: it is what happens when every proposal the
responder made was refused, which is a real outcome and a loud one.
""".strip("\n"))

# ---------------------------------------------------------------- ACL_006

head(6, "ACL_006", "what the delivered framework does that this one does not")
print("""
Not everything here is an improvement, and the delivered framework carries
three things this module does not have.

  spatially explicit models   ForestScalingSim is a real lattice model with
                              dispersal, competition and metabolic scaling;
                              the two demo models here are a Moran process
                              and a piecewise line, sized to make the gates
                              visible rather than to model anything.

  claim generation            `_generate_claims` proposes new claims from
                              outcomes. This module has no equivalent, and
                              the gap is deliberate rather than principled:
                              a generated claim is a claim whose falsifier
                              was chosen after seeing the data, and the
                              admission rule for that is not written.

  figures                     `adaptive_sim_results.png` is in the drop.

The claim in this folder is about the response vocabulary and the
provenance record, and it is not a claim about the models. A parameter walk
under a good model still tells you nothing; a gate over a toy model still
refuses the walk. The two are separable and this folder only holds one.
""".strip("\n"))

print()
print(BAR)
print("end of replay -- findings recorded in AUDIT_NOTES.md as ACL_001..ACL_006")
print(BAR)
