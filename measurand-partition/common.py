#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
common -- the structure the five work orders share, as one record shape.

  An observation made in ONE setting is scored against an outcome
  produced by MANY unmeasured variables, and the entire residual is
  assigned to the thing being observed.

`attribution()` takes that as four fields and returns where the residual
was assigned relative to what was measured. It grades nothing: whether the
assignment is right is not a property of the record; whether the record
SAYS the variables were measured is.

Status tags are the delivery's: OBSERVED / DERIVED / PROPOSED. Anything
PROPOSED is a design and not a finding, and every module here marks its
constructed data PROPOSED.

Python 3.9, ASCII only, stdlib only. Refuses --selftest; the checks live
in test_partition.py.
"""

from __future__ import annotations

import sys

STATUS = ("OBSERVED", "DERIVED", "PROPOSED")

ATTRIBUTION = ("UNPARTITIONED", "PARTITIONED", "ASSIGNED_ELSEWHERE",
               "NOT_EVALUABLE")


class Refused(ValueError):
    """Raised at intake. A refused record never reaches a readout."""


def absent(v):
    return v is None or v == "" or v == "UNDECLARED"


def attribution(observed, setting, unmeasured, assigned_to):
    """Where the residual went.

    observed     the thing scored (a child, a judgment, a method, an athlete)
    setting      the ONE setting the observation was made in
    unmeasured   the variables between observation and outcome that were
                 NOT measured -- a list; None means nobody enumerated them,
                 which is a different state from an empty list
    assigned_to  what the residual was assigned to

    UNPARTITIONED      unmeasured variables exist and the residual went to
                       the observed thing -- the shared fault
    PARTITIONED        nothing between observation and outcome is unmeasured
    ASSIGNED_ELSEWHERE unmeasured variables exist and the residual was not
                       assigned to the observed thing
    NOT_EVALUABLE      the unmeasured set was never enumerated
    """
    if absent(observed) or absent(setting) or absent(assigned_to):
        raise Refused("attribution: observed, setting and assigned_to are "
                      "required")
    if unmeasured is None:
        verdict = "NOT_EVALUABLE"
    elif not unmeasured:
        verdict = "PARTITIONED"
    elif assigned_to == observed:
        verdict = "UNPARTITIONED"
    else:
        verdict = "ASSIGNED_ELSEWHERE"
    return {"observed": observed, "setting": setting,
            "unmeasured": None if unmeasured is None else list(unmeasured),
            "assigned_to": assigned_to, "verdict": verdict}


# the four populations the delivery names, as records; every unmeasured
# list is the delivery's own partial list, carried
POPULATIONS = [
    attribution("the child", "one assessment setting",
                ["frame", "channel", "frequency band", "domain load",
                 "their interaction"], "the child"),
    attribution("the observer's judgment", "one observation",
                ["nutrition", "hydration", "sleep opportunity",
                 "training load", "coaching contact",
                 "endocrine developmental timing",
                 "experienced social environment"],
                "the observer's judgment"),
    attribution("the building method", "the documentation gate",
                ["load capacity", "survival, maintained", "survival, neglected"],
                "the building method"),
    attribution("the released athlete", "the program's podium",
                ["balance", "spatial awareness", "load tolerance",
                 "controlled falling", "transferable motor structure"],
                "the released athlete"),
]


def refuse_selftest(name):
    sys.stderr.write("%s carries no selftest; run python3 test_partition.py\n"
                     % name)
    return 2


def render():
    out = ["COMMON STRUCTURE -- four populations, one record shape", "-" * 60]
    for r in POPULATIONS:
        out.append("  %-28s %-14s unmeasured %d  residual -> %s"
                   % (r["observed"], r["verdict"], len(r["unmeasured"]),
                      r["assigned_to"]))
    out.append("  a record whose unmeasured set was never enumerated reads "
               "NOT_EVALUABLE, not PARTITIONED")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        return refuse_selftest("common.py")
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
