# SPDX-License-Identifier: CC0-1.0
"""
Checks for the operator-machine-coupling marker, on CONSTRUCTED data. No
fleet, plant, incident, or symbiosis data is read (none is available); every
value here is built by hand with a known answer. Nothing is a result about
any operator, machine, or organism.

    python3 operator-machine-coupling/selftest_omc.py

Prints `selftest: N checks, M failed` and exits non-zero on any failure.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import coupling_separation as cs   # noqa: E402
import discriminators as dc        # noqa: E402
import permission_state as ps      # noqa: E402
import known_answer as ka          # noqa: E402

_checks = 0
_failed = 0


def ok(cond, label):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        print("  FAIL: %s" % label)


O = cs.Obs

# --------------------------------------------------------------------------
print("known-answer gate (interaction_fraction):")
ka.seed()
rows = {r["case"]: r["status"] for r in ka.run(
    "operator-machine-coupling/coupling_separation.py::interaction_fraction")}
ok(rows.get("additive") == ka.PASS, "known-answer: additive -> 0")
ok(rows.get("pure_pairing") == ka.PASS, "known-answer: pure_pairing -> 1")
ok(rows.get("mixed") == ka.PASS, "known-answer: mixed -> 1/21")

# --------------------------------------------------------------------------
print("coupling separation -- recover a planted interaction, 3x3:")
mu = 20.0
a = {"op0": 3.0, "op1": 0.0, "op2": -3.0}
b = {"u0": 3.0, "u1": 0.0, "u2": -3.0}
# row/col-centered interaction with a unique maximum at the average pairing
r = {("op0", "u0"): -1, ("op0", "u1"): -1, ("op0", "u2"): 2,
     ("op1", "u0"): -1, ("op1", "u1"): 3, ("op1", "u2"): -2,
     ("op2", "u0"): 2, ("op2", "u1"): -2, ("op2", "u2"): 0}
obs = [O(i, j, mu + a[i] + b[j] + r[(i, j)]) for i in a for j in b]
d = cs.decompose(obs)
ok(d.status == "OK", "complete design decomposes")
ok(abs(d.a["op1"]) < 1e-9 and abs(d.b["u1"]) < 1e-9,
   "op1 and u1 are exactly average (main effects 0)")
ok(abs(d.r[("op1", "u1")] - 3.0) < 1e-9, "the planted pairing residual is recovered")
ok(abs(d.ss_pair - sum(v ** 2 for v in r.values())) < 1e-9,
   "SS_pair equals the planted interaction sum of squares")
bp = cs.best_pairing(obs)
ok(bp[0] == ("op1", "u1") and abs(bp[1] - 3.0) < 1e-9,
   "best_pairing finds the coupled pair whose partners are both average")

print("coupling separation -- averaging over pairings misses it:")
mis = cs.averaged_over_pairings_misses(obs)
ok(mis["status"] == "OK" and mis["best_pair"]["pair"] == ("op1", "u1"),
   "the discarded best pair is the average-average one")
ok(abs(mis["best_pair"]["main_effects_predicts"] - mu) < 1e-9,
   "a main-effects model predicts the grand mean for that pair")
ok(abs(mis["best_pair"]["observed"] - (mu + 3.0)) < 1e-9,
   "the observed pairing outcome exceeds it by the residual it discards")
ok(mis["discarded_pairing_fraction"] > 0.0,
   "a nonzero pairing fraction is thrown away by averaging")

print("coupling separation -- additive world has no pairing effect:")
add = [O(i, j, mu + a[i] + b[j]) for i in a for j in b]
ok(cs.interaction_fraction(add) == 0.0, "purely additive -> interaction fraction 0")

print("coupling separation -- incomplete design is NOT_ESTIMABLE, not zero:")
inc = [o for o in obs if not (o.operator == "op1" and o.unit == "u1")]
di = cs.decompose(inc)
ok(di.status == cs.NOT_ESTIMABLE and "op1" in di.detail,
   "a missing pairing is NOT_ESTIMABLE and names the missing pair")
ok(cs.interaction_fraction(inc) is None, "incomplete design fraction is None, not 0")
ok(cs.interaction_fraction([O("x", "y", 5.0)]) is None,
   "no structured variation -> None, not 0 (never reads as 'no coupling')")

# --------------------------------------------------------------------------
print("discriminator 1 -- operator error vs coupling failure:")
x1 = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]     # time_on_unit
x2 = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]     # time_in_role (independent of x1)
coup = [-float(v) for v in x1]                # failure drops with time-on-unit
oper = [-float(v) for v in x2]                # failure drops with role time
both = [-float(u) - float(v) for u, v in zip(x1, x2)]
flat = [1.0 for _ in x1]
ok(dc.error_vs_coupling(x1, x2, coup) == dc.COUPLING_FAILURE,
   "drops with time-on-unit, flat in role -> COUPLING_FAILURE")
ok(dc.error_vs_coupling(x1, x2, oper) == dc.OPERATOR_ERROR,
   "drops with role, flat in unit -> OPERATOR_ERROR")
ok(dc.error_vs_coupling(x1, x1, coup) == dc.UNDETERMINED,
   "collinear predictors -> UNDETERMINED (the FAA confound)")
ok(dc.error_vs_coupling(x1, x2, both) == dc.UNDETERMINED,
   "both predictors carry it -> UNDETERMINED, not a false attribution")
ok(dc.error_vs_coupling(x1, x2, flat) == dc.NO_SIGNAL,
   "no variation in the outcome -> NO_SIGNAL")

print("discriminator 2 -- fixed advantage vs convergence curve:")
t = [0, 1, 2, 3, 4, 5, 6, 7]
fixed = [2.0 for _ in t]                       # genotype: flat from first contact
conv = [0.1, 0.6, 1.2, 1.7, 1.9, 2.0, 2.0, 2.0]   # coupling: rises then plateaus
none_adv = [-1.0 for _ in t]
ok(dc.fixed_vs_convergence(t, fixed) == dc.FIXED,
   "flat advantage from first contact -> FIXED (the microbe control case)")
ok(dc.fixed_vs_convergence(t, conv) == dc.CONVERGENCE,
   "advantage accrues with time-in-pairing -> CONVERGENCE")
ok(dc.fixed_vs_convergence(t, none_adv) == dc.UNDETERMINED,
   "no advantage to classify -> UNDETERMINED")

# --------------------------------------------------------------------------
print("permission variable -- three states, collapse, confound, M2:")
R = ps.Rec
# regime_collapse: a 'pooled' label carrying two permission states
recs = [R("pooled", ps.COUPLED_AUTHORIZED, 10, None, None),
        R("pooled", ps.COUPLED_PROHIBITED, 2, "seal", "bearing"),
        R("dedicated", ps.COUPLED_AUTHORIZED, 10, None, None)]
coll = ps.regime_collapse(recs)
ok(len(coll["pooled"]) == 2,
   "a single regime label collapses two permission states")

# attribution: permission drives the outcome; assignment carries it as a confound
conf = ([R("dedicated", ps.COUPLED_AUTHORIZED, 10, None, None)] * 3 +
        [R("dedicated", ps.COUPLED_PROHIBITED, 2, None, None)] +
        [R("pooled", ps.COUPLED_AUTHORIZED, 10, None, None)] +
        [R("pooled", ps.COUPLED_PROHIBITED, 2, None, None)] * 3)
att = ps.attribution(conf)
ok(abs(att["naive_assignment_effect"] - 4.0) < 1e-9,
   "naive assignment effect is +4 (the confound)")
ok(abs(att["controlled_assignment_effect"]) < 1e-9,
   "controlling for permission, the assignment effect is 0 -- it was permission")

# attribution UNDETERMINED when the field is absent
noperm = [R("dedicated", None, 10, None, None),
          R("pooled", None, 2, None, None)]
ok(ps.attribution(noperm)["controlled_assignment_effect"] == ps.UNDETERMINED,
   "absent permission field -> controlled effect UNDETERMINED (the recording problem)")

# attribution UNDETERMINED when permission is collinear with assignment
colin = ([R("dedicated", ps.COUPLED_AUTHORIZED, 10, None, None)] * 3 +
         [R("pooled", ps.COUPLED_PROHIBITED, 2, None, None)] * 3)
ok(ps.attribution(colin)["controlled_assignment_effect"] == ps.UNDETERMINED,
   "permission collinear with assignment -> UNDETERMINED even with the field")

# M2 match rate, gated to the middle case
m2 = [R("pooled", ps.COUPLED_PROHIBITED, 0, "seal", "seal"),
      R("pooled", ps.COUPLED_PROHIBITED, 0, "bearing", "bearing"),
      R("pooled", ps.COUPLED_PROHIBITED, 0, "seal", "gasket"),
      R("dedicated", ps.COUPLED_AUTHORIZED, 0, "x", "x")]   # not middle-case
ok(abs(ps.m2_match_rate(m2) - 2.0 / 3.0) < 1e-9,
   "M2 match rate is 2/3 over the coupled+prohibited records only")
ok(ps.m2_match_rate([R("pooled", None, 0, "a", "a")]) == ps.NOT_RECORDED,
   "no permission field anywhere -> NOT_RECORDED, never 0.0")
raises_ok = True
try:
    ps.validate_state("bogus")
    raises_ok = False
except ValueError:
    pass
ok(raises_ok, "an unknown permission state is refused")

# --------------------------------------------------------------------------
print("demo -- no_severity three-arm exemption (marker's 'operator error'):")
import re                            # noqa: E402
import demo_omc                      # noqa: E402
import no_severity as nosev          # noqa: E402
_text = demo_omc.render()
_exempt = demo_omc._exempt()
_masked = _text
for w in _exempt:
    _masked = re.sub(r"\b%s\b" % w, "X", _masked, flags=re.I)
ok(nosev.check(_masked)[0], "arm 1: render is clean once the exempt token is masked")
_firers = {w.lower() for (_l, w, _s) in nosev.hits(_text)}
ok(_firers == {x.lower() for x in _exempt},
   "arm 2: the declared exemption is exactly the set of firers")
_marker = open(os.path.join(HERE, "MARKER.md")).read().lower()
ok(all(w.lower() in _marker for w in _exempt),
   "arm 3: every exempt token appears in the delivered MARKER.md")
ok(not nosev.check(_masked + "\nthis is wrong")[0],
   "arm 3b: a planted banned word is caught through the exemption")

# --------------------------------------------------------------------------
print("selftest: %d checks, %d failed" % (_checks, _failed))
sys.exit(1 if _failed else 0)
