#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
wo4_survival -- STRUCTURES: SURVIVAL ANALYSIS, MATCHED (WO-4b).

Barns standing 250 years beside code-built structures of similar age,
construction dates in county records for both, and no durability
comparison found. This module is the matched survival analysis as
machinery, run on CONSTRUCTED records so the split the order calls
critical is enforced before any real record exists.

  KAPLAN-MEIER over structure age. The event is FAILED. REMOVED
  (demolished, relocated) is censoring at the removal year, not a
  failure; a structure still standing is censored at the observation
  year; UNKNOWN status is excluded and counted. A record with no
  construction year has no age and is refused.
  THE CRITICAL SPLIT. MAINTAINED-IN-USE and SURVIVING-NEGLECTED are two
  quantities. Every record declares `maintained` in {True, False,
  UNKNOWN}; the curves are computed per population per maintenance
  arm, and there is no function that pools the arms -- `pooled()`
  exists to refuse, naming the split.
  MATCHING. Records are stratified by construction-decade band and
  declared exposure class; a stratum holding one population only is
  reported NOT_MATCHED and enters no comparison.
  THE MARKETING CLAUSE. A durability claim carrying "with proper
  maintenance" is a claim about the maintained arm only; `claim_scope`
  returns which curve it can be read against, from a declared boolean,
  never from the claim's wording.

Nothing here is a statement about any structure in any county; every
record is CONSTRUCTED and marked PROPOSED, and the field report the order
carries is carried here unverified.

Python 3.9, ASCII only, stdlib only. Refuses --selftest.
"""

from __future__ import annotations

import sys

from common import Refused, refuse_selftest

POPULATIONS = ("TRANSMITTED", "CODE_BUILT")
STATUSES = ("STANDING", "FAILED", "REMOVED", "UNKNOWN")
MAINTAINED = (True, False, "UNKNOWN")
CHOICES = {
    1: "matching strata are (construction decade, declared exposure class)",
    2: "REMOVED is censoring at the removal year, never an event",
}


class PooledRefused(Refused):
    """Raised by pooled(): the two maintenance arms are not one quantity."""


def read_structure(rec):
    for k in ("id", "population", "built", "exposure", "status", "maintained",
              "observed", "tag"):
        if k not in rec:
            raise Refused("structure %s: missing %s" % (rec.get("id"), k))
    if rec["population"] not in POPULATIONS:
        raise Refused("structure %s: population %r" % (rec["id"], rec["population"]))
    if rec["status"] not in STATUSES:
        raise Refused("structure %s: status %r" % (rec["id"], rec["status"]))
    if rec["maintained"] not in MAINTAINED:
        raise Refused("structure %s: maintained %r" % (rec["id"], rec["maintained"]))
    if rec["tag"] not in ("OBSERVED", "DERIVED", "PROPOSED"):
        raise Refused("structure %s: tag %r" % (rec["id"], rec["tag"]))
    b = rec["built"]
    if b is None or isinstance(b, bool) or not isinstance(b, int):
        raise Refused("structure %s: no construction year, no age" % rec["id"])
    if rec["status"] in ("FAILED", "REMOVED"):
        e = rec.get("event")
        if e is None or isinstance(e, bool) or not isinstance(e, int) or e < b:
            raise Refused("structure %s: %s needs an event year >= built"
                          % (rec["id"], rec["status"]))
    if rec["observed"] < b:
        raise Refused("structure %s: observed before built" % rec["id"])
    return dict(rec)


def age_and_event(rec):
    """(age at event or censoring, event flag) or None for UNKNOWN."""
    if rec["status"] == "UNKNOWN":
        return None
    if rec["status"] == "FAILED":
        return rec["event"] - rec["built"], True
    if rec["status"] == "REMOVED":
        return rec["event"] - rec["built"], False       # [CHOICE 2]
    return rec["observed"] - rec["built"], False


def kaplan_meier(records):
    """Step function as a list of (age, survival, at_risk, events). None
    with no usable record, never a flat 1.0 over nothing."""
    pairs = [age_and_event(r) for r in records]
    pairs = [p for p in pairs if p is not None]
    if not pairs:
        return None
    pairs.sort()
    s = 1.0
    out = []
    ages = sorted(set(a for a, _ in pairs))
    for a in ages:
        at_risk = sum(1 for t, _ in pairs if t >= a)
        d = sum(1 for t, e in pairs if t == a and e)
        if d:
            s *= 1.0 - d / float(at_risk)
        out.append((a, s, at_risk, d))
    return out


def strata(records):
    """[CHOICE 1]. Returns {(decade, exposure): {population: [records]}}."""
    st = {}
    for r in records:
        key = (r["built"] // 10 * 10, r["exposure"])
        st.setdefault(key, {}).setdefault(r["population"], []).append(r)
    return st


def split_curves(records):
    """The critical split: per population, per maintenance arm, over
    MATCHED strata only. Unmatched strata and UNKNOWN-maintenance records
    are reported apart."""
    st = strata(records)
    matched, unmatched = {}, []
    for key, pops in st.items():
        if all(p in pops for p in POPULATIONS):
            matched[key] = pops
        else:
            unmatched.append(key)
    arms = {}
    unknown_maint = []
    for pops in matched.values():
        for pop, recs in pops.items():
            for r in recs:
                if r["maintained"] == "UNKNOWN":
                    unknown_maint.append(r["id"])
                    continue
                arm = "MAINTAINED_IN_USE" if r["maintained"] else "SURVIVING_NEGLECTED"
                arms.setdefault((pop, arm), []).append(r)
    curves = {k: kaplan_meier(v) for k, v in arms.items()}
    n_arm = {k: len(v) for k, v in arms.items()}
    return {"matched_strata": sorted(matched), "unmatched_strata": sorted(unmatched),
            "curves": curves, "n_arm": n_arm,
            "unknown_maintenance": sorted(unknown_maint),
            "n_matched": sum(len(r) for pops in matched.values()
                             for r in pops.values())}


def pooled(records):
    """Refused. The two maintenance arms are different quantities and the
    order says do not collapse them."""
    raise PooledRefused("MAINTAINED_IN_USE and SURVIVING_NEGLECTED are not "
                        "one curve; read split_curves() and report both")


def survival_at(curve, age):
    """S(age) read off a step function; None with no curve, 1.0 before the
    first observed age only when that age is recorded."""
    if not curve:
        return None
    s = 1.0
    for a, sv, _, _ in curve:
        if a > age:
            break
        s = sv
    return s


def claim_scope(years, conditional_on_maintenance):
    """Which arm a durability claim can be read against. Declared, never
    parsed from wording."""
    if conditional_on_maintenance not in (True, False):
        raise Refused("conditional_on_maintenance must be declared")
    return {"years": years,
            "readable_against": ("MAINTAINED_IN_USE",) if conditional_on_maintenance
            else ("MAINTAINED_IN_USE", "SURVIVING_NEGLECTED"),
            "reads": "a claim conditional on maintenance says nothing about "
                     "the neglected arm" if conditional_on_maintenance else
                     "an unconditional claim is read against both arms"}


# --- constructed demo, PROPOSED ---------------------------------------------

def _s(sid, pop, built, exposure, status, maintained, observed=2026, event=None):
    return read_structure({"id": sid, "population": pop, "built": built,
                           "exposure": exposure, "status": status,
                           "maintained": maintained, "observed": observed,
                           "event": event, "tag": "PROPOSED"})


DEMO = [
    _s("t-01", "TRANSMITTED", 1870, "ridge", "STANDING", True),
    _s("t-02", "TRANSMITTED", 1875, "ridge", "STANDING", False),
    _s("t-03", "TRANSMITTED", 1872, "ridge", "FAILED", False, event=1998),
    _s("t-04", "TRANSMITTED", 1878, "ridge", "REMOVED", True, event=1960),
    _s("c-01", "CODE_BUILT", 1874, "ridge", "STANDING", True),
    _s("c-02", "CODE_BUILT", 1871, "ridge", "FAILED", False, event=1951),
    _s("c-03", "CODE_BUILT", 1879, "ridge", "FAILED", True, event=2003),
    _s("c-04", "CODE_BUILT", 1876, "ridge", "STANDING", "UNKNOWN"),
    _s("t-05", "TRANSMITTED", 1900, "valley", "STANDING", True),   # unmatched
    _s("t-06", "TRANSMITTED", 1905, "valley", "UNKNOWN", True),
]


def render(records=None):
    rs = DEMO if records is None else records
    sp = split_curves(rs)
    out = ["WO-4b  STRUCTURES: MATCHED SURVIVAL, TWO ARMS   (records "
           "CONSTRUCTED, PROPOSED)", "-" * 72,
           "  matched strata %s   unmatched %s   records in matched strata %d"
           % (sp["matched_strata"], sp["unmatched_strata"], sp["n_matched"]),
           "  maintenance UNKNOWN, excluded and counted: %s"
           % (sp["unknown_maintenance"] or "-")]
    for (pop, arm), curve in sorted(sp["curves"].items()):
        out.append("  %-12s %-20s n %d   S(100) %s   S(150) %s"
                   % (pop, arm, sp["n_arm"][(pop, arm)],
                      "%.2f" % survival_at(curve, 100),
                      "%.2f" % survival_at(curve, 150)))
    try:
        pooled(rs)
    except PooledRefused as e:
        out.append("  pooled(): REFUSED -- %s" % e)
    c = claim_scope(150, True)
    out.append("  '150 years with proper maintenance' reads against %s only"
               % ",".join(c["readable_against"]))
    out.append("  the Driftless field report is carried from the order, "
               "unverified; no county record was read")
    for k in sorted(CHOICES):
        out.append("  [CHOICE %d] %s" % (k, CHOICES[k]))
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        return refuse_selftest("wo4_survival.py")
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
