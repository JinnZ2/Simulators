# loop_weight.py
# CC0 1.0 Universal / public domain dedication.
#
# Source-relevance weighting on feedback-loop structure.
# Stdlib only. No network. Python 3.
#
# MEASURAND
#   For a source reporting on a system, how much information about that
#   system the report can carry.
#
# THREE QUANTITIES, NEVER COMBINED
#   L  loop length        hops between the action/decision and the observation
#   R  per-hop retention  fraction of signal surviving each hop, per hop
#   C  calibration        whether the source's reading maps to the thing
#
#   L is topology. R is channel. C is whether the instrument is pointed at
#   the right thing. They can disagree, and the disagreement is the reading.
#
# WHAT THIS MODULE REFUSES
#   - no scalar collapse. no function here returns one number standing in
#     for all three. R is never raised to the power of L: a cumulative
#     retention figure fuses topology with channel and destroys exactly the
#     disagreement the instrument exists to surface.
#   - no quantity derived from standing, office, tenure, employer, count of
#     works cited, count of people listening, or where a thing was printed.
#     Those are the quantities being replaced; their presence would be a
#     defect, and test_loop.py checks the identifiers of this file for them.
#   - C is never set from a claim the source makes about itself. A
#     calibration input whose provenance is the source is refused at load,
#     not silently dropped.
#
# UNKNOWN IS NOT LOW
#   C is None until one of two derivations succeeds. An unmeasured
#   calibration and a measured-bad one are different states and are never
#   merged: UNCALIBRATED and MISCALIBRATED are separate returns, and in a
#   comparison they are INCOMPARABLE rather than ranked.

from enum import Enum
from typing import NamedTuple


class LoopRead(Enum):
    SHORT_CALIBRATED = "SHORT_CALIBRATED"
    SHORT_UNCALIBRATED = "SHORT_UNCALIBRATED"
    SHORT_MISCALIBRATED = "SHORT_MISCALIBRATED"
    LONG_CALIBRATED = "LONG_CALIBRATED"
    LONG_UNCALIBRATED = "LONG_UNCALIBRATED"
    LONG_MISCALIBRATED = "LONG_MISCALIBRATED"
    LOSSY = "LOSSY"
    INSUFFICIENT = "INSUFFICIENT"


class Carries(Enum):
    FIRST_CARRIES_MORE = "FIRST_CARRIES_MORE"
    SECOND_CARRIES_MORE = "SECOND_CARRIES_MORE"
    INCOMPARABLE = "INCOMPARABLE"


class SelfSuppliedRefused(Exception):
    """A calibration input whose provenance is the source being calibrated."""


class Params(NamedTuple):
    # [CHOICE 1] L <= 1 is SHORT. The order does not set the split.
    short_at_or_below: int = 1
    # [CHOICE 2] any single hop below this makes the read LOSSY.
    lossy_below: float = 0.5
    # [CHOICE 3] C at or above this is established-and-high.
    calibrated_at_or_above: float = 0.7
    # [CHOICE 4] gap between the two C derivations that counts as a
    # disagreement worth printing. Does not change the value.
    derivation_gap: float = 0.2


DEFAULTS = Params()

RULE_UNMEASURED_PATH = "unmeasured_path"
RULE_CALIBRATION_ESTABLISHED = "calibration_established"
RULE_KNOWN_LOW_VS_UNKNOWN = "known_low_vs_unknown"
RULE_CHANNEL_CARRIES = "channel_carries"
RULE_PATH_DOMINANCE = "path_dominance"
RULE_NO_DOMINANCE = "no_dominance"

CAL_HIGH = "established_high"
CAL_LOW = "established_low"
CAL_UNKNOWN = "not_established"


# ---------------------------------------------------------------- L, topology

def loop_length(case):
    """L = number of hops in the DESCRIBED path.

    Counted from the path or not at all. A source's occupation, domain or
    kind never implies a hop count; an absent path returns None and the
    read is INSUFFICIENT.
    """
    path = case.get("path")
    if path is None:
        return None, "path_not_described"
    if not isinstance(path, list):
        return None, "path_not_a_hop_list"
    if not all(isinstance(hop, dict) for hop in path):
        # a list of things that are not hop records is not a described path.
        # Counting it would report a hop count nobody described.
        return None, "path_not_a_hop_list"
    return len(path), None


def hop_ids(case):
    path = case.get("path")
    if not isinstance(path, list):
        return []
    out = []
    for hop in path:
        if not isinstance(hop, dict):
            continue
        hop_id = hop.get("id")
        if hop_id is not None:
            out.append(hop_id)
    return out


# ------------------------------------------------------------- R, the channel

def per_hop_retention(case):
    """R = the worst single-hop retention in the described path.

    Per hop, as the order states. The minimum is reported because one dead
    hop is a dead path; the per-hop figures stay in the record. The product
    across hops is deliberately not computed anywhere in this module.
    """
    path = case.get("path")
    if not isinstance(path, list):
        # a path that is not a hop list is not a described path. The read is
        # INSUFFICIENT on L; R is unmeasured rather than crashing here.
        return None, 0, 0
    known = []
    unknown = 0
    for hop in path:
        if not isinstance(hop, dict):
            unknown += 1
            continue
        value = hop.get("retention")
        if value is None:
            unknown += 1
        else:
            known.append(float(value))
    if not known:
        return None, unknown, len(path)
    return min(known), unknown, len(path)


# ------------------------------------------------------- C-1, DISAGREEMENT

def _check_not_self_supplied(source_id, records, kind):
    for rec in records:
        if rec.get("supplied_by") is None:
            raise SelfSuppliedRefused(
                "%s record %r states no provenance; C may not be set from an "
                "input whose supplier is unstated" % (kind, rec.get("id"))
            )
        if rec.get("supplied_by") == source_id:
            raise SelfSuppliedRefused(
                "%s record %r is supplied by the source being calibrated (%r); "
                "C is never self-reported" % (kind, rec.get("id"), source_id)
            )


def _independence_classes(others):
    """Others sharing a hop with EACH OTHER are one instrument, not N.

    Union-find over hop ids. Used only to stop correlated instruments from
    counting once each inside C-1. Class count never enters a comparison and
    is never a tie-breaker.
    """
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for rec in others:
        parent[rec["id"]] = rec["id"]
    for i, a in enumerate(others):
        for b in others[i + 1:]:
            if set(a["hops"]) & set(b["hops"]):
                union(a["id"], b["id"])
    classes = {}
    for rec in others:
        classes.setdefault(find(rec["id"]), []).append(rec)
    return list(classes.values())


def calibration_c1(case):
    """C from divergence against independent instruments on the same referent.

    Independence is asserted per pair and stored. A pair sharing a hop with
    the source is excluded whatever the assertion says, and an assertion
    contradicted by a shared hop is reported as its own finding.
    """
    source_id = case.get("source_id")
    comparisons = case.get("comparisons") or []
    _check_not_self_supplied(source_id, comparisons, "comparison")
    own = set(hop_ids(case))

    admitted = []
    excluded = []
    contradicted = []
    for rec in comparisons:
        other_hops = list(rec.get("other_hop_ids") or [])
        asserted = bool(rec.get("independence_asserted"))
        shared = sorted(own & set(other_hops))
        agreement = rec.get("agreement")
        if shared:
            excluded.append({"id": rec.get("id"), "reason": "shares_hop_with_source",
                             "shared_hops": shared})
            if asserted:
                contradicted.append({"id": rec.get("id"), "shared_hops": shared})
            continue
        if not asserted:
            excluded.append({"id": rec.get("id"), "reason": "independence_not_asserted"})
            continue
        if agreement is None:
            excluded.append({"id": rec.get("id"), "reason": "no_agreement_recorded"})
            continue
        admitted.append({"id": rec.get("id"), "hops": other_hops,
                         "agreement": float(agreement)})

    record = {
        "derivation": "C-1",
        "value": None,
        "pairs_admitted": len(admitted),
        "pairs_excluded": excluded,
        "independence_assertions_contradicted": contradicted,
        "independent_classes": 0,
        "class_values": [],
    }
    if not admitted:
        record["unavailable_because"] = "no_admissible_independent_pair"
        return record

    classes = _independence_classes(admitted)
    class_values = []
    for group in classes:
        class_values.append(sum(r["agreement"] for r in group) / float(len(group)))
    record["independent_classes"] = len(classes)
    record["class_values"] = class_values
    record["value"] = sum(class_values) / float(len(class_values))
    return record


# --------------------------------------------- C-2, OUT-OF-FRAME OUTCOME

def calibration_c2(case):
    """C from prior predictions scored against outcomes the source did not
    define, select or time, and stated before resolution.
    """
    source_id = case.get("source_id")
    predictions = case.get("predictions") or []
    _check_not_self_supplied(source_id, predictions, "prediction")

    admitted = []
    excluded = []
    for rec in predictions:
        pid = rec.get("id")
        reason = None
        for field in ("outcome_defined_by", "outcome_selected_by", "outcome_timed_by"):
            holder = rec.get(field)
            if holder is None:
                reason = "%s_unstated" % field
                break
            if holder == source_id:
                reason = "%s_is_the_source" % field
                break
        if reason is None:
            stated = rec.get("stated_at")
            resolved = rec.get("resolved_at")
            if stated is None or resolved is None:
                reason = "not_timestamped"
            elif not stated < resolved:
                reason = "not_stated_before_resolution"
            elif rec.get("correct") is None:
                reason = "outcome_not_scored"
        if reason:
            excluded.append({"id": pid, "reason": reason})
        else:
            admitted.append(rec)

    record = {
        "derivation": "C-2",
        "value": None,
        "predictions_admitted": len(admitted),
        "predictions_excluded": excluded,
    }
    if not admitted:
        record["unavailable_because"] = "no_admissible_out_of_frame_prediction"
        return record
    hits = sum(1 for r in admitted if r.get("correct"))
    record["value"] = hits / float(len(admitted))
    return record


def calibration(case, params=DEFAULTS):
    """Run both admissible derivations. Report both. Never impute.

    [CHOICE 5] When both derivations land, C takes the LOWER of the two: a
    calibration established by one check and refuted by another is not
    established. The asymmetry is real and is stated rather than hidden --
    C-1 failing may mean the peers are wrong, not the source. Both values
    are always in the record so a reader can take the other view.
    """
    c1 = calibration_c1(case)
    c2 = calibration_c2(case)
    values = [r["value"] for r in (c1, c2) if r["value"] is not None]
    used = [r["derivation"] for r in (c1, c2) if r["value"] is not None]
    record = {"c1": c1, "c2": c2, "derivations_used": used,
              "value": None, "derivations_disagree": False, "state": CAL_UNKNOWN}
    if not values:
        return record
    record["value"] = min(values)
    if len(values) == 2 and abs(values[0] - values[1]) > params.derivation_gap:
        record["derivations_disagree"] = True
    record["state"] = (CAL_HIGH if record["value"] >= params.calibrated_at_or_above
                       else CAL_LOW)
    return record


# ------------------------------------------------------------------- the read

def read(case, params=DEFAULTS):
    """Return the three quantities side by side plus a routing label.

    The label is a routing label over the three, not a score derived from
    them: every axis stays in the record at full value, including on LOSSY
    and INSUFFICIENT returns where the label reports only one of them.
    """
    length, length_note = loop_length(case)
    retention, unknown_hops, total_hops = per_hop_retention(case)
    cal = calibration(case, params)

    record = {
        "source_id": case.get("source_id"),
        "referent": case.get("referent"),
        "loop_length": length,
        "loop_length_note": length_note,
        "per_hop_retention": retention,
        "retention_unknown_hops": unknown_hops,
        "hops_described": total_hops,
        "calibration": cal,
        "params": params._asdict(),
    }

    if length is None:
        record["verdict"] = LoopRead.INSUFFICIENT
        record["verdict_because"] = length_note
        return record

    if retention is not None and retention < params.lossy_below:
        # R dominates regardless of L. The order is explicit and the reason
        # is that a hop below the floor has already destroyed the signal
        # whatever the topology around it. C stays in the record.
        record["verdict"] = LoopRead.LOSSY
        record["verdict_because"] = "a hop retains %.3f, below %.3f" % (
            retention, params.lossy_below)
        return record

    short = length <= params.short_at_or_below
    state = cal["state"]
    table = {
        (True, CAL_HIGH): LoopRead.SHORT_CALIBRATED,
        (True, CAL_LOW): LoopRead.SHORT_MISCALIBRATED,
        (True, CAL_UNKNOWN): LoopRead.SHORT_UNCALIBRATED,
        (False, CAL_HIGH): LoopRead.LONG_CALIBRATED,
        (False, CAL_LOW): LoopRead.LONG_MISCALIBRATED,
        (False, CAL_UNKNOWN): LoopRead.LONG_UNCALIBRATED,
    }
    record["verdict"] = table[(short, state)]
    record["verdict_because"] = "L=%d, calibration %s" % (length, state)
    return record


# --------------------------------------------------------------- the ordering

def carries_more(a, b):
    """Which of two reads carries more information about its referent.

    A stated dominance rule, not a score. Returns one of three ordinal
    verdicts, the rule that decided, and the per-axis comparison. No number
    is produced at any point, and INCOMPARABLE is a first-class result --
    two reads differing on axes that do not dominate are not ranked.

    Precedence, in order:
      1. an unmeasured path is not a read. INCOMPARABLE.
      2. calibration is a PRECONDITION, not a term. A read whose mapping to
         the referent is established and high carries more than one whose
         mapping is unestablished or refuted, whatever its L and R -- this
         is what stops a short loop from rescuing an always-wrong
         instrument. Established-low against unestablished is INCOMPARABLE:
         a measured-bad instrument and an unmeasured one are different
         states, not two points on one scale.
      3. a channel measured not to carry loses to one that carries.
      4. within the same calibration state and channel state, Pareto
         dominance on L (lower is more) and R (higher is more). No
         dominance, no verdict.
    """
    axes = {
        "loop_length": (a.get("loop_length"), b.get("loop_length")),
        "per_hop_retention": (a.get("per_hop_retention"), b.get("per_hop_retention")),
        "calibration": (a["calibration"]["value"], b["calibration"]["value"]),
        "calibration_state": (a["calibration"]["state"], b["calibration"]["state"]),
    }

    def out(verdict, rule, note):
        return {"verdict": verdict, "rule": rule, "note": note, "axes": axes}

    va, vb = a.get("verdict"), b.get("verdict")
    if va is LoopRead.INSUFFICIENT or vb is LoopRead.INSUFFICIENT:
        return out(Carries.INCOMPARABLE, RULE_UNMEASURED_PATH,
                   "L is unmeasured on at least one side; no read to compare")

    sa, sb = a["calibration"]["state"], b["calibration"]["state"]
    if sa != sb:
        if sa == CAL_HIGH:
            return out(Carries.FIRST_CARRIES_MORE, RULE_CALIBRATION_ESTABLISHED,
                       "the first read's mapping to the referent is established and high; "
                       "the second read's is %s" % sb)
        if sb == CAL_HIGH:
            return out(Carries.SECOND_CARRIES_MORE, RULE_CALIBRATION_ESTABLISHED,
                       "the second read's mapping to the referent is established and high; "
                       "the first read's is %s" % sa)
        return out(Carries.INCOMPARABLE, RULE_KNOWN_LOW_VS_UNKNOWN,
                   "one calibration is measured low and the other is not measured; "
                   "different states, not ranked")

    la, lb = va is LoopRead.LOSSY, vb is LoopRead.LOSSY
    if la != lb:
        if lb:
            return out(Carries.FIRST_CARRIES_MORE, RULE_CHANNEL_CARRIES,
                       "the second read has a hop below the retention floor; the first does not")
        return out(Carries.SECOND_CARRIES_MORE, RULE_CHANNEL_CARRIES,
                   "the first read has a hop below the retention floor; the second does not")

    better_a = better_b = False
    compared = []
    al, bl = axes["loop_length"]
    if al is not None and bl is not None:
        compared.append("loop_length")
        if al < bl:
            better_a = True
        elif bl < al:
            better_b = True
    ar, br = axes["per_hop_retention"]
    if ar is not None and br is not None:
        compared.append("per_hop_retention")
        if ar > br:
            better_a = True
        elif br > ar:
            better_b = True
    if better_a and not better_b:
        return out(Carries.FIRST_CARRIES_MORE, RULE_PATH_DOMINANCE,
                   "same calibration and channel state; the first dominates on %s" % ", ".join(compared))
    if better_b and not better_a:
        return out(Carries.SECOND_CARRIES_MORE, RULE_PATH_DOMINANCE,
                   "same calibration and channel state; the second dominates on %s" % ", ".join(compared))
    return out(Carries.INCOMPARABLE, RULE_NO_DOMINANCE,
               "axes tie or conflict; no dominance on %s" % (", ".join(compared) or "any shared axis"))


DECLARATION = {
    "measurand": "information carried by a source report about a referent system",
    "axes": ["loop_length", "per_hop_retention", "calibration"],
    "returns": [m.name for m in LoopRead],
    "scalar_collapse": False,
    "self_report_admitted": False,
    "unknown_states": ["UNCALIBRATED", "INSUFFICIENT"],
}


def render(records):
    lines = []
    head = "%-22s %-20s %5s %6s %7s  %s" % (
        "source", "verdict", "L", "R", "C", "calibration by")
    lines.append(head)
    lines.append("-" * len(head))
    for rec in records:
        cal = rec["calibration"]
        lines.append("%-22s %-20s %5s %6s %7s  %s" % (
            str(rec["source_id"])[:22],
            rec["verdict"].name,
            "--" if rec["loop_length"] is None else rec["loop_length"],
            "--" if rec["per_hop_retention"] is None else "%.2f" % rec["per_hop_retention"],
            "--" if cal["value"] is None else "%.2f" % cal["value"],
            ", ".join(cal["derivations_used"]) or "none admissible",
        ))
    lines.append("")
    lines.append("L, R and C are reported side by side and are never combined.")
    lines.append("-- under C is UNCALIBRATED: not measured. It is not a low value.")
    return "\n".join(lines)


if __name__ == "__main__":
    import cases
    reads = [read(c) for c in cases.CASES]
    print(render(reads))
    print()
    a = [r for r in reads if r["source_id"] == "A_one_hop_unchecked"][0]
    c = [r for r in reads if r["source_id"] == "C_four_hop_relay"][0]
    verdict = carries_more(c, a)
    print("falsifier, case C against case A:")
    print("  %s by rule %s" % (verdict["verdict"].name, verdict["rule"]))
    print("  %s" % verdict["note"])
