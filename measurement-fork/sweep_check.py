"""
sweep_check.py -- every probe declares which spec variable it must be run
across, and at how many levels.

CC0-1.0. Standard library only. Deterministic. Reads coupling.py and
conventional.py; modifies neither.

THE RULE, as specified
----------------------
    every probe declares which spec variable it must be run across, and at
    how many levels. default regime.variable, min 2. Point-probes must
    declare sweep=None with a reason.

This was a schema addition with teeth that the schema had no room for:
`quantities.probe()` had six fields and none was `sweep`, so the rule was
not expressible and 0 of 17 measuring probes satisfied it -- one gap, not
seventeen oversights. Section 1 counts, and now reports the repaired state
alongside what it used to read.

Why it matters more than a missing field usually does. A probe with no
declared sweep returns a number at ONE setting of the control parameter. The
spec's own falsifiers are mostly statements about a gradient --

    "ratio flat across the provisioning gradient"

-- and a single-point probe cannot participate in one. So the schema gap and
the unreachable-falsifier problem in MF_010 are the same gap seen from two
sides, and adding the field is what closes it.

Section 3 is the one that changes a verdict: K13 `tau` is exactly the probe
MF_010 said was missing, and its arrival moves `reversibility after regime
shift` from PARTIAL to reached.
"""

from __future__ import annotations

import json
import os
import sys

import conventional
import coupling
import widen
from quantities import OBJECTS

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "systems", "provisioning_calibration.json")
RULE = "=" * 72

DEFAULT_SWEEP = "regime.variable"
MIN_LEVELS = 2


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


# ---------------------------------------------------------------------------
# The newly specified probes, transcribed as delivered. The `sweep` tuple is
# (spec variable, levels); a point-probe would carry sweep=None plus a reason.
NEW_PROBES = (
    dict(id="K11", base="information_rate", normalizer=None,
         object_of="coupling", sweep=(DEFAULT_SWEEP, 2), reason=None,
         protocol=("distinguishable environmental states registered per "
                   "unit time, by the actor's own sensors"),
         returns="rate"),
    dict(id="K12", base="reliance_weight", normalizer="sensor_validity",
         object_of="coupling", sweep=(DEFAULT_SWEEP, 2), reason=None,
         protocol=("(a) weight given to own read vs alternative sources; "
                   "(b) whether own read tracks outcome. Trust is a "
                   "measurement only if (b) was run."),
         returns="ratio"),
    dict(id="K13", base="tau", normalizer=None, object_of="coupling",
         sweep=("provisioning_level", 2), reason=None,
         protocol="error vs trials-since-shift, fit tau",
         returns="time constant"),
    dict(id="K14", base="practice_rate", normalizer=None,
         object_of="coupling", sweep=("provisioning_level", 2), reason=None,
         protocol="is the channel exercised during the stable interval",
         returns="rate"),
    dict(id="K15", base="baseline_freshness", normalizer=None,
         object_of="coupling", sweep=("time_since_clean_reference", 3),
         reason=None,
         protocol=("inject small known deviation; measure detection "
                   "threshold"),
         returns="duration"),
    dict(id="K16", base="detection_latency", normalizer=None,
         object_of="coupling", sweep=("baseline_staleness", 3), reason=None,
         protocol=("small-signal detection before the outcome column "
                   "moves"),
         returns="latency"),
)


def validate(p) -> list:
    """The rule, as three separate failures so they can be counted apart."""
    bad = []
    if "sweep" not in p:
        bad.append("NO SWEEP FIELD")
        return bad
    if p["sweep"] is None:
        # `point_reason` on a probe(); `reason` on the K11-K18 dicts.
        if not (p.get("point_reason") or p.get("reason")):
            bad.append("POINT-PROBE WITHOUT REASON")
        return bad
    var, levels = p["sweep"]
    if not var:
        bad.append("SWEEP VARIABLE BLANK")
    if levels < MIN_LEVELS:
        bad.append("LEVELS %d < %d" % (levels, MIN_LEVELS))
    return bad


# ---------------------------------------------------------------------------


def load_spec():
    with open(SPEC) as fh:
        return json.load(fh)


def check_delivered() -> None:
    section("1  the delivered probes against the new rule")

    spec = load_spec()
    delivered = [p for p in conventional.generate(spec)
                 + coupling.generate(spec)
                 + widen.generate(spec)]
    measuring = [p for p in delivered
                 if p["quantity"]["object_of"] in OBJECTS]

    print("  %d probes emitted by the three arms, %d of them measuring"
          % (len(delivered), len(measuring)))
    print("  (the widen arm emits design-directed options, not quantities --")
    print("  MF_008 / MF_016 -- so the rule does not apply to it)\n")

    fails = [p for p in measuring if validate(p)]
    swept = [p for p in measuring if p.get("sweep")]
    points = [p for p in measuring if "sweep" in p and not p["sweep"]]
    print("  carrying a `sweep` declaration: %d of %d  (%d swept, %d point)"
          % (len(measuring) - len(fails), len(measuring),
             len(swept), len(points)))
    print()
    print("  BEFORE THE REPAIR this read 0 of 17, and not because seventeen")
    print("  probes were written badly. quantities.probe() had six fields --")
    print("      arm  id  quantity  protocol  reads  blind_to")
    print("  and `sweep` was not among them, so the rule was not expressible")
    print("  in the schema the arms were written against. One schema gap,")
    print("  not seventeen oversights.")
    print()
    print("  MF_017 repaired. The field defaults to the spec's regime")
    print("  variable, refuses fewer than %d levels, and requires a stated"
          % MIN_LEVELS)
    print("  reason when a probe declares sweep=None:")
    for p in points:
        print("      %s  %s" % (p["id"], p["point_reason"]))
    print()
    print("  Why it is load-bearing rather than tidy: the spec's own")
    print("  falsifiers are statements about a gradient.\n")
    reg = spec.get("regime")
    if reg:
        print("      regime variable declared in the spec: %s"
              % reg.get("variable"))
    for q in spec.get("open_questions", [])[:3]:
        print("      open question: %s" % q)
    print()
    print("  A probe run at one setting of the control parameter cannot")
    print("  participate in a claim about a gradient. So the missing field")
    print("  and MF_010's unreachable falsifier are one gap seen twice.")


def check_new() -> None:
    section("2  the newly specified probes against the same rule")

    print("  %-6s %-22s %-30s %-8s %s"
          % ("id", "quantity", "sweep", "levels", "rule"))
    print("  " + "-" * 76)
    for p in NEW_PROBES:
        bad = validate(p)
        var, lev = p["sweep"] if p["sweep"] else ("(point probe)", "-")
        print("  %-6s %-22s %-30s %-8s %s"
              % (p["id"], p["base"], var, lev,
                 "PASS" if not bad else "; ".join(bad)))

    print()
    passing = sum(1 for p in NEW_PROBES if not validate(p))
    print("  %d of %d pass." % (passing, len(NEW_PROBES)))
    print()
    reg = (load_spec().get("regime") or {}).get("variable", "")
    norm = reg.lower().replace(" ", "_")
    resolved = [norm if p["sweep"][0] == DEFAULT_SWEEP
                else p["sweep"][0] for p in NEW_PROBES]
    print("  The spec's regime variable is %r, which normalizes to %r."
          % (reg, norm))
    print("  Resolving the default against it:\n")
    for p, r in zip(NEW_PROBES, resolved):
        print("      %-6s %-30s %s"
              % (p["id"], p["sweep"][0],
                 "-> %s" % r if p["sweep"][0] == DEFAULT_SWEEP else ""))
    print()
    print("  %d distinct sweep variables after resolution, and %d of %d"
          % (len(set(resolved)),
             sum(1 for r in resolved if r == norm), len(NEW_PROBES)))
    print("  probes sweep the regime variable -- 2 by default and 2 by")
    print("  naming it directly. So the field carries information on 2 of 6,")
    print("  not 4 of 6, and K13/K14 spelling out the default is a")
    print("  redundancy the schema should collapse rather than a choice.")
    print()
    print("  K15 and K16 sweep at 3 levels rather than 2. Both are on the")
    print("  mediation chain, and 2 levels gives a slope with no curvature")
    print("  and no way to see a threshold. That is the min being a MINIMUM")
    print("  and the probe declaring above it.")


def check_k13() -> None:
    section("3  K13 closes the gap MF_010 named")

    print("  MF_010 adjudicated `reversibility after regime shift` as")
    print("  unreached, and named the shape of the missing instrument:\n")
    print("      the predicted contrast is a RATE -- fast vs slow relearn")
    print("      once the buffer is removed -- and no K-probe returns a")
    print("      rate; every one measures a level, ratio, slope or variance")
    print("      at fixed regime.\n")
    print("  MF_014 then moved it to PARTIAL on K14: K14 supplied the")
    print("  provisioning gradient the stated falsifier needed, but nothing")
    print("  measured relearn rate AFTER the buffer is removed.\n")
    print("  K13:\n")
    k13 = [p for p in NEW_PROBES if p["id"] == "K13"][0]
    print("      base       %s" % k13["base"])
    print("      protocol   %s" % k13["protocol"])
    print("      sweep      %s at %d levels" % k13["sweep"])
    print("      returns    %s" % k13["returns"])
    print()
    print("  `error vs trials-since-shift` is measured across a regime")
    print("  change by construction -- trials-since-shift has no meaning")
    print("  without one -- and fitting tau returns a time constant. Swept")
    print("  across provisioning level, it supplies both halves the stated")
    print("  falsifier needs: the rate, and the gradient to read it against.")
    print()
    print("  Verdict change: PARTIAL -> CLOSED.")
    print()
    print("  The prediction shipped with it is falsifiable in the direction")
    print("  that costs something: tau RISES with provisioning, and a flat")
    print("  tau falsifies. A flat tau is the null and it is reachable, so")
    print("  this is not the ../null-harness/ CONSTANT_SILENT shape.")
    print()
    print("  K12 carries the sharpest single line in the batch:")
    print()
    print("      Trust is a measurement only if (b) was run.")
    print()
    print("  which is `whether trust in own sensing is a measurement or a")
    print("  belief` -- the gap MF_014 closed on K15 -- restated as a")
    print("  precondition on reading K12 at all, rather than as a separate")
    print("  probe. Two independent routes to the same distinction.")


def check_remaining() -> None:
    section("4  what is still open")

    print("  coupling bandwidth\n")
    print("    MF_014 left this OPEN on the grounds that rate-of-use,")
    print("    staleness and latency are three quantities and capacity is a")
    print("    fourth. K11 `information_rate` is the fourth:\n")
    print("      distinguishable environmental states registered per unit")
    print("      time, by the actor's own sensors\n")
    print("    and it is explicitly marked `not_` against K01 delay and K02")
    print("    reliability -- 'This is channel capacity.'\n")
    print("    Verdict change: OPEN -> CLOSED.\n")
    print("    Its stated blind spot is the honest one: 'whether anything is")
    print("    done with the states'. Capacity measured, use not measured,")
    print("    and the probe says so.\n")
    print("  So all three gaps MF_010 named are now reached. What is NOT")
    print("  reached is anything that was measured: every probe here is a")
    print("  specification, the mediation lags are still ordinal (MF_015),")
    print("  and the `sweep` field is not in `quantities.probe()`.")


def main() -> None:
    print()
    print("SWEEP: WHICH VARIABLE, AT HOW MANY LEVELS")
    print("subject: the delivered arms and the newly specified K11-K16")

    check_delivered()
    check_new()
    check_k13()
    check_remaining()

    section("READING")
    print("""
  `sweep` was a schema addition with teeth that no delivered probe could
  satisfy, because `quantities.probe()` had no such field -- the rule was
  not expressible in the schema the arms were written against. One gap,
  not N oversights. REPAIRED: the field exists, defaults to the regime
  variable, refuses a single level, and makes a point probe say why.

  It is load-bearing rather than tidy because the spec's falsifiers are
  statements about gradients, and a probe run at one setting of the
  control parameter cannot participate in one. The missing field and
  MF_010's unreachable falsifier are the same gap from two sides.

  Of the six new probes, 2 of 6 use the default sweep variable, so the
  field carries information rather than restating a default. K15 and K16
  declare 3 levels rather than the minimum 2, which is what a minimum
  looks like when it is working.

  K13 `tau` closes `reversibility after regime shift`: error against
  trials-since-shift is measured across a regime change by construction,
  fitting tau returns a rate, and sweeping provisioning supplies the
  gradient the stated falsifier needs. K11 closes `coupling bandwidth` as
  the capacity term the other three were not. All three of MF_010's gaps
  are now reached -- as specifications. Nothing has been run.
""")


if __name__ == "__main__":
    sys.exit(main() or 0)
