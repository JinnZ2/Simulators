#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
wo1_partition -- PARTITION A DEFICIT LABEL, built to WO-1.

A "deficit" score is a residual: what is left after frame (A1), channel
(A2), frequency band (A3) and domain load (A4) go unmeasured. This module
does two things and refuses a third.

  1. RESIDUAL GATE. A performance score is reported as a residual
     candidate only when all four axes were MEASURED SEPARATELY, before
     scoring, and the interaction term was entered. Otherwise it returns
     NOT_SEPARABLE naming the axes that were not measured. It does not
     estimate what an unmeasured axis would have contributed; the
     design separates, it does not demonstrate.
  2. TWO-SETTING ARM. Same individual, two reference settings, both
     labels recorded. The share of individuals whose label moved between
     settings is a FLOOR on how much of the label is displacement from a
     reference rather than a property. One such individual establishes the
     floor; an individual labelled at one setting only is UNBOUNDED, and
     an arm with no individual labelled twice is NOT_RUN, never zero.
  3. It does NOT model how an axis maps to performance. No such model
     is in the order and inventing one would put the residual's size in
     this file's hands.

Nothing here is a statement about any individual. Every record in the
demo is CONSTRUCTED and marked PROPOSED.

Python 3.9, ASCII only, stdlib only. Refuses --selftest.
"""

from __future__ import annotations

import sys

from common import Refused, absent, refuse_selftest

AXES = ("A1_FRAME", "A2_CHANNEL", "A3_FREQUENCY", "A4_DOMAIN_LOAD")
AXIS_STATES = ("MEASURED", "UNMEASURED")
CHOICES = {
    1: "an axis is MEASURED only if its record says so AND names an "
       "instrument; a value with no instrument is UNMEASURED",
    2: "the two-setting floor is a share of individuals labelled at two or "
       "more settings; single-setting individuals are counted apart as "
       "UNBOUNDED, never in the denominator",
}


def read_observation(rec):
    """One individual at one setting. Fields: individual, setting, label,
    performance, axes{A1..A4: {state, instrument}}, interaction_entered,
    status."""
    for k in ("individual", "setting", "label", "performance", "axes",
              "interaction_entered", "status"):
        if k not in rec:
            raise Refused("observation %s: missing %s"
                          % (rec.get("individual"), k))
    if absent(rec["individual"]) or absent(rec["setting"]):
        raise Refused("observation: individual and setting are required")
    if rec["status"] not in ("OBSERVED", "DERIVED", "PROPOSED"):
        raise Refused("observation %s: status %r" % (rec["individual"],
                                                      rec["status"]))
    axes = rec["axes"]
    for a in AXES:
        if a not in axes:
            raise Refused("observation %s: axis %s not entered (an axis "
                          "nobody entered is not UNMEASURED, it is absent)"
                          % (rec["individual"], a))
        st = axes[a].get("state")
        if st not in AXIS_STATES:
            raise Refused("observation %s: axis %s state %r"
                          % (rec["individual"], a, st))
        if st == "MEASURED" and absent(axes[a].get("instrument")):
            raise Refused("observation %s: axis %s MEASURED with no "
                          "instrument [CHOICE 1]" % (rec["individual"], a))
    if rec["interaction_entered"] not in (True, False):
        raise Refused("observation %s: interaction_entered must be a bool"
                      % rec["individual"])
    return dict(rec)


def residual(obs):
    """STEP 3. Returns the residual candidate only when every axis is
    measured and the interaction is entered; else NOT_SEPARABLE naming
    what is missing. The residual VALUE is the performance score itself
    -- nothing is subtracted, because no axis-to-performance model exists
    in the order -- and the readout says what state it is in."""
    missing = [a for a in AXES if obs["axes"][a]["state"] != "MEASURED"]
    if not obs["interaction_entered"]:
        missing.append("INTERACTION")
    if missing:
        return {"individual": obs["individual"], "setting": obs["setting"],
                "state": "NOT_SEPARABLE", "missing": missing,
                "residual": None, "label": obs["label"],
                "reads": "the label is instrument-setting plus whatever "
                         "the unmeasured axes carry; nothing here is "
                         "deficit yet"}
    return {"individual": obs["individual"], "setting": obs["setting"],
            "state": "RESIDUAL_CANDIDATE", "missing": [],
            "residual": obs["performance"], "label": obs["label"],
            "reads": "all four axes entered separately; the residual is "
                     "what could be called deficit and its size is NOT "
                     "shown to be non-zero"}


def two_setting_bound(observations):
    """TWO-SETTING ARM. Groups by individual; counts those labelled at two
    or more settings; the floor is the share of those whose label differs
    across settings. [CHOICE 2]."""
    by = {}
    for o in observations:
        by.setdefault(o["individual"], {})[o["setting"]] = o["label"]
    two, moved, unbounded = [], [], []
    for ind, labels in sorted(by.items()):
        if len(labels) < 2:
            unbounded.append(ind)
            continue
        two.append(ind)
        if len(set(labels.values())) > 1:
            moved.append(ind)
    if not two:
        return {"state": "NOT_RUN", "floor": None, "n_two_settings": 0,
                "moved": [], "unbounded": unbounded,
                "reads": "no individual was labelled at two settings; the "
                         "arm was not run and the floor is not zero"}
    floor = len(moved) / float(len(two))
    return {"state": "FLOOR_ESTABLISHED" if moved else "NO_CASE_FOUND",
            "floor": floor, "n_two_settings": len(two), "moved": moved,
            "unbounded": unbounded,
            "reads": ("%d of %d labels moved between settings; at least "
                      "that share of the label is displacement from a "
                      "reference" % (len(moved), len(two))) if moved else
                     ("%d individuals labelled twice, none moved; the "
                      "floor is 0 on this set and the bound is not "
                      "established above it" % len(two))}


# --- constructed demo, PROPOSED ---------------------------------------------

def _obs(ind, setting, label, perf, measured, interaction=False):
    axes = {}
    for a in AXES:
        if a in measured:
            axes[a] = {"state": "MEASURED", "instrument": "constructed"}
        else:
            axes[a] = {"state": "UNMEASURED", "instrument": None}
    return read_observation({"individual": ind, "setting": setting,
                             "label": label, "performance": perf,
                             "axes": axes, "interaction_entered": interaction,
                             "status": "PROPOSED"})


DEMO = [
    _obs("p-01", "S-written", "deficit", 0.35, ()),
    _obs("p-01", "S-spatial", "typical", 0.80, ()),
    _obs("p-02", "S-written", "deficit", 0.30, ()),
    _obs("p-02", "S-spatial", "deficit", 0.33, ()),
    _obs("p-03", "S-written", "deficit", 0.40, ()),
    _obs("p-04", "S-written", "deficit", 0.38, AXES, interaction=True),
    _obs("p-05", "S-written", "deficit", 0.36, AXES[:3], interaction=True),
]


def render(observations=None):
    obs = DEMO if observations is None else observations
    out = ["WO-1  PARTITION A DEFICIT LABEL   (data CONSTRUCTED, PROPOSED)",
           "-" * 72]
    for o in obs:
        r = residual(o)
        out.append("  %-6s %-10s %-8s %-18s missing %s"
                   % (r["individual"], r["setting"], r["label"], r["state"],
                      ",".join(r["missing"]) or "-"))
    b = two_setting_bound(obs)
    out.append("")
    out.append("  two-setting arm  %s   floor %s   n(two settings) %d   "
               "moved %s   unbounded %s  [CHOICE 2]"
               % (b["state"], "--" if b["floor"] is None
                  else "%.2f" % b["floor"], b["n_two_settings"],
                  ",".join(b["moved"]) or "-", ",".join(b["unbounded"]) or "-"))
    out.append("  " + b["reads"])
    out.append("  no claim that any residual is zero; no claim about any "
               "individual")
    for k in sorted(CHOICES):
        out.append("  [CHOICE %d] %s" % (k, CHOICES[k]))
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        return refuse_selftest("wo1_partition.py")
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
