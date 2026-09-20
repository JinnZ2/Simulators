#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
wo5_deselection -- DESELECTION SCORED ON THE WRONG OUTCOME (WO-5).

The failure category is manufactured by the choice of measurand: score on
the podium and every non-podium athlete is a failure; score on what was
learned and every trained athlete gained it, the released ones included.
This module scores one constructed cohort under both measurands and
reports the size of the category that exists under one and not the other.

  PODIUM   outcome per athlete is SELECTED or not; the failure set is
           the deselected.
  LEARNED  per capacity, the deselected group against UNTRAINED age
           peers: AHEAD / BEHIND / TIE under a declared margin.
           NOT_COMPUTABLE with no untrained peers -- the comparison the
           order says nobody runs needs the group nobody recruits.
  MANUFACTURED  athletes classed as failures under PODIUM and AHEAD on
           at least one capacity under LEARNED.
  IMPORT LINE  the sports frame carries the deselection problem only if
           the podium is imported with it as the measurand; a frame
           import must declare its measurand apart from its fields, and
           an undeclared measurand is refused, never defaulted to PODIUM.

The order's prediction (deselected ahead on nearly everything except the
measure they were released for) is PROPOSED. The demo cohort is
CONSTRUCTED to that shape, so what the demo shows is that the instrument
RECOVERS the shape when it is present -- a known-answer run on the
scorer, and no evidence about any athlete.

Python 3.9, ASCII only, stdlib only. Refuses --selftest.
"""

from __future__ import annotations

import sys

from common import Refused, absent, refuse_selftest

GROUPS = ("SELECTED", "DESELECTED", "UNTRAINED_PEER")
CAPACITIES = ("balance", "spatial_awareness", "load_tolerance",
              "controlled_falling", "transferable_motor_structure")
MEASURANDS = ("PODIUM", "LEARNED")
MARGIN = 0.05    # [CHOICE 1]
CHOICES = {
    1: "AHEAD/BEHIND require the group averages to differ by more than %.2f on "
       "a [0,1] scale; inside that is TIE" % MARGIN,
    2: "LEARNED compares group AVERAGES; no per-athlete rank is produced",
}


def read_athlete(rec):
    for k in ("id", "group", "measures", "released_for", "tag"):
        if k not in rec:
            raise Refused("athlete %s: missing %s" % (rec.get("id"), k))
    if rec["group"] not in GROUPS:
        raise Refused("athlete %s: group %r" % (rec["id"], rec["group"]))
    if rec["tag"] not in ("OBSERVED", "DERIVED", "PROPOSED"):
        raise Refused("athlete %s: tag %r" % (rec["id"], rec["tag"]))
    for c in CAPACITIES:
        if c not in rec["measures"]:
            raise Refused("athlete %s: capacity %s not entered" % (rec["id"], c))
        v = rec["measures"][c]
        if v is not None and (isinstance(v, bool) or not isinstance(v, (int, float))
                              or not 0 <= v <= 1):
            raise Refused("athlete %s: %s must be in [0,1] or None" % (rec["id"], c))
    if rec["group"] == "DESELECTED":
        if rec["released_for"] not in CAPACITIES and rec["released_for"] != "UNDECLARED":
            raise Refused("athlete %s: released_for must name a capacity or "
                          "UNDECLARED" % rec["id"])
    elif rec["released_for"] is not None:
        raise Refused("athlete %s: released_for only on DESELECTED" % rec["id"])
    return dict(rec)


def score_podium(athletes):
    """PODIUM: SELECTED succeeds, the rest fail. Untrained peers are not on
    the scale at all and are counted apart."""
    succ = [a["id"] for a in athletes if a["group"] == "SELECTED"]
    fail = [a["id"] for a in athletes if a["group"] == "DESELECTED"]
    off = [a["id"] for a in athletes if a["group"] == "UNTRAINED_PEER"]
    return {"measurand": "PODIUM", "success": succ, "failure": fail,
            "not_on_scale": off}


def _mean(vals):
    vals = [v for v in vals if v is not None]
    return (sum(vals) / len(vals)) if vals else None


def score_learned(athletes):
    """LEARNED: deselected group mean against untrained peers, per
    capacity. [CHOICE 1] [CHOICE 2]."""
    des = [a for a in athletes if a["group"] == "DESELECTED"]
    unt = [a for a in athletes if a["group"] == "UNTRAINED_PEER"]
    if not unt:
        return {"measurand": "LEARNED", "state": "NOT_COMPUTABLE",
                "per_capacity": {}, "n_deselected": len(des), "n_untrained": 0,
                "reads": "no untrained age peers entered; the comparison "
                         "cannot be run and reads nothing"}
    if not des:
        return {"measurand": "LEARNED", "state": "NOT_COMPUTABLE",
                "per_capacity": {}, "n_deselected": 0, "n_untrained": len(unt),
                "reads": "no deselected athletes entered"}
    per = {}
    for c in CAPACITIES:
        md = _mean(a["measures"][c] for a in des)
        mu = _mean(a["measures"][c] for a in unt)
        if md is None or mu is None:
            per[c] = {"verdict": "UNMEASURED", "deselected": md, "untrained": mu}
            continue
        diff = md - mu
        v = "AHEAD" if diff > MARGIN else ("BEHIND" if diff < -MARGIN else "TIE")
        per[c] = {"verdict": v, "deselected": md, "untrained": mu}
    return {"measurand": "LEARNED", "state": "COMPUTED", "per_capacity": per,
            "n_deselected": len(des), "n_untrained": len(unt),
            "reads": "%d of %d capacities AHEAD for the deselected group"
                     % (sum(1 for p in per.values() if p["verdict"] == "AHEAD"),
                        len(CAPACITIES))}


def manufactured(athletes):
    """Athletes that are failures under PODIUM and whose group is AHEAD on
    at least one capacity under LEARNED. None (not 0) when LEARNED cannot
    run."""
    pod = score_podium(athletes)
    lea = score_learned(athletes)
    if lea["state"] != "COMPUTED":
        return {"state": "NOT_COMPUTABLE", "count": None, "ids": [],
                "released_for_behind": None}
    ahead = [c for c, p in lea["per_capacity"].items() if p["verdict"] == "AHEAD"]
    ids = pod["failure"] if ahead else []
    # the prediction's exception: the released-for capacity
    rf = [a["released_for"] for a in athletes if a["group"] == "DESELECTED"]
    rf_named = [c for c in rf if c in CAPACITIES]
    rf_behind = [c for c in set(rf_named)
                 if lea["per_capacity"][c]["verdict"] != "AHEAD"]
    return {"state": "COMPUTED", "count": len(ids), "ids": ids,
            "ahead_on": ahead,
            "released_for": sorted(set(rf_named)),
            "released_for_undeclared": rf.count("UNDECLARED"),
            "released_for_behind": sorted(rf_behind)}


def import_line(frame_fields, measurand):
    """The IMPORT NOTE: the frame's fields and its measurand are separate
    declarations. An undeclared measurand is refused, never PODIUM by
    default."""
    if absent(measurand):
        raise Refused("import: the measurand must be declared apart from "
                      "the frame's fields; PODIUM is not a default")
    if measurand not in MEASURANDS:
        raise Refused("import: measurand %r" % measurand)
    return {"frame_fields": list(frame_fields), "measurand": measurand,
            "podium_imported": measurand == "PODIUM",
            "reads": "the deselection problem travels with the frame" if
            measurand == "PODIUM" else "frame imported, podium left behind"}


# --- constructed demo, PROPOSED (built to the prediction's shape) ----------

def _a(aid, group, vals, released=None):
    return read_athlete({"id": aid, "group": group,
                         "measures": dict(zip(CAPACITIES, vals)),
                         "released_for": released, "tag": "PROPOSED"})


DEMO = [
    _a("s-01", "SELECTED", (0.9, 0.9, 0.9, 0.9, 0.9)),
    _a("s-02", "SELECTED", (0.85, 0.9, 0.95, 0.9, 0.9)),
    _a("d-01", "DESELECTED", (0.8, 0.8, 0.5, 0.8, 0.8), "load_tolerance"),
    _a("d-02", "DESELECTED", (0.75, 0.85, 0.45, 0.8, 0.75), "load_tolerance"),
    _a("d-03", "DESELECTED", (0.8, 0.75, 0.5, 0.85, 0.8), "load_tolerance"),
    _a("u-01", "UNTRAINED_PEER", (0.5, 0.5, 0.5, 0.4, 0.5)),
    _a("u-02", "UNTRAINED_PEER", (0.55, 0.45, 0.5, 0.45, 0.5)),
    _a("u-03", "UNTRAINED_PEER", (0.5, 0.55, 0.5, 0.4, 0.55)),
]


def render(athletes=None):
    ath = DEMO if athletes is None else athletes
    pod = score_podium(ath)
    lea = score_learned(ath)
    man = manufactured(ath)
    out = ["WO-5  DESELECTION SCORED TWO WAYS   (cohort CONSTRUCTED to the "
           "prediction's shape, PROPOSED)", "-" * 72,
           "  PODIUM   success %d   failure %d   not on scale %d"
           % (len(pod["success"]), len(pod["failure"]), len(pod["not_on_scale"])),
           "  LEARNED  %s   deselected n %d   untrained n %d  [CHOICE 2]"
           % (lea["state"], lea["n_deselected"], lea["n_untrained"])]
    for c, p in lea["per_capacity"].items():
        out.append("    %-28s %-8s deselected %.2f   untrained %.2f"
                   % (c, p["verdict"], p["deselected"], p["untrained"]))
    out.append("  " + lea["reads"])
    rf_v = {c: lea["per_capacity"][c]["verdict"] for c in man.get("released_for", [])}
    out.append("  MANUFACTURED failure category: %s   ahead on %s   released "
               "for %s"
               % ("--" if man["count"] is None else man["count"],
                  ",".join(man.get("ahead_on", [])) or "-",
                  ", ".join("%s (%s under LEARNED)" % kv for kv in sorted(rf_v.items()))
                  or "-"))
    il = import_line(["reportable conditions", "input history",
                      "mismatch as pairing", "transfer"], "LEARNED")
    out.append("  import line: measurand %s   podium imported %s"
               % (il["measurand"], il["podium_imported"]))
    out.append("  the demo recovers a shape it was built to carry; it is a "
               "known-answer run on the scorer and no evidence about athletes")
    for k in sorted(CHOICES):
        out.append("  [CHOICE %d] %s" % (k, CHOICES[k]))
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        return refuse_selftest("wo5_deselection.py")
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
