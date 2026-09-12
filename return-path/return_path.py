# SPDX-License-Identifier: CC0-1.0
"""
return_path.py -- score a correction channel against four requirements.

Returns the SET of requirements failed. Does not rank channels, does not
recommend, does not resolve. It does not ask whether a channel is useful:
a channel can be valuable and still not be a return path. Marking a gap is
not correcting an error.

THE FOUR CHECKS (WORK_ORDER.md, section "Checks")

    C1_RECEIPT       fires if receipt != MANDATORY
    C2_SIGNAL        fires if signal_encodings > 0
    C3_LATENCY       fires if latency >= build_on_time
    C4_CONSTRUCTION  fires if construction != SLOW_SIDE_ONLY

Each reads its own fields and no others, so the four are independent by
construction; `independence()` measures that rather than asserting it.

WHAT THIS MODULE DOES NOT HOLD

    - no field named or derived from the standing family the order bans
      (institution, authority, credential, venue, reach, audience size,
      reputation of either party). Checked in test_return.py by an AST
      walk over identifiers and dict keys, null-tested on a plant.
    - no field scoring the CONTENT of the correction. `scope_note` is
      carried verbatim into the output and read by no check; the test
      asserts that from the AST, not from this sentence.
    - no conversion of times and no default for either. Both times or no
      rating.

SIX PLACES THE ORDER LEAVES A DECISION OPEN. Every one is in `CHOICES`,
printed in the header of every render, and none is silent.

Stdlib only. No network. Parses under Python 3.9. ASCII only. CC0.

    python3 return_path.py            # render the case set
    python3 test_return.py            # the checks
"""

from __future__ import annotations

import math

# --------------------------------------------------------------------------
# schema vocabularies. Declared, closed, and never extended by inference.

RECEIPT_VALUES = ("MANDATORY", "ELECTIVE", "UNSPECIFIED")
ENCODER_VALUES = ("SLOW_SIDE", "FAST_SIDE", "THIRD_PARTY", "NONE")
CONSTRUCTION_VALUES = ("SLOW_SIDE_ONLY", "REQUIRES_FAST_SIDE",
                       "REQUIRES_THIRD_PARTY")

REQUIRED_FIELDS = ("channel_id", "receipt", "signal_encodings",
                   "encoder_position", "latency", "build_on_time",
                   "time_unit", "construction", "scope_note")

CHECK_CODES = ("C1_RECEIPT", "C2_SIGNAL", "C3_LATENCY", "C4_CONSTRUCTION")
FLAG_CODES = ("F_UNSPECIFIED_RECEIPT", "F_FAST_SIDE_ENCODER")

GRADED = "RETURN_PATH_GRADED"
NOT_A_RETURN_PATH = "NOT_A_RETURN_PATH"
INTAKE_INCOMPLETE = "INTAKE_INCOMPLETE"

# ratio states, kept apart because `ratio: None` has three causes and a
# reader of the number alone cannot tell them.
RATIO_COMPUTED = "COMPUTED"
RATIO_UNDEFINED = "UNDEFINED_ZERO_BUILD_ON_TIME"
RATIO_NOT_COMPUTED = "NOT_COMPUTED"


CHOICES = {
    1: ("grade takes a third value INTAKE_INCOMPLETE, with `missing` and "
        "`invalid` lists, and `failed`/`flags` are None rather than [] when "
        "no check ran. The order names INTAKE_INCOMPLETE as a return and "
        "gives the grade field two values; [] would say 'four checks ran, "
        "none fired'."),
    2: ("`ratio_state` is emitted beside `ratio`. A ratio of None has three "
        "causes -- not computed, zero build_on_time, absent intake -- and "
        "the number cannot carry which."),
    3: ("`time_unit` is carried into the output. The order's return holds "
        "neither time and the ratio is dimensionless, so without the unit "
        "no output can be read back against its own intake."),
    4: ("F_RATIO is NOT emitted into `flags`. Its own definition is 'always "
        "reported as a number', so as a flag it fires on every channel and "
        "separates nothing; its home is the `ratio` field the return "
        "already declares."),
    5: ("scope_note == '' is a supplied value; scope_note absent is not. "
        "An empty note is a submitter who wrote nothing there, which is a "
        "different state from a submitter who did not answer."),
    7: ("`encoder_position` is one field and `signal_encodings` may be 2 or "
        "more. Where the encoders differ the field names the FIRST one, "
        "because the order's rationale is about the first re-encoding. The "
        "cost is that F_FAST_SIDE_ENCODER is only as good as that choice: "
        "a slow-side first encoder followed by a fast-side second does not "
        "raise it."),
    6: ("a present-but-unusable field (out of vocabulary, negative time, "
        "non-integer encoding count) lands in `invalid`, not in `missing`. "
        "Both return INTAKE_INCOMPLETE. Absent and present-and-wrong are "
        "different states and the order names only the first."),
}

SCHEMA_ADDITIONS = ("grade: INTAKE_INCOMPLETE", "missing", "invalid",
                    "ratio_state", "time_unit")


class IntakeError(Exception):
    """Raised only by callers that ask for a check on an unvalidated channel."""


# --------------------------------------------------------------------------
# intake. No field may be inferred.

def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def intake(channel):
    """Return (missing, invalid). Either non-empty means INTAKE_INCOMPLETE."""
    if not isinstance(channel, dict):
        return list(REQUIRED_FIELDS), ["channel: not a mapping"]

    missing = [f for f in REQUIRED_FIELDS if f not in channel]
    invalid = []

    def bad(field, why):
        invalid.append("%s: %s" % (field, why))

    if "channel_id" in channel and not (
            isinstance(channel["channel_id"], str) and channel["channel_id"]):
        bad("channel_id", "not a non-empty string")

    if "receipt" in channel and channel["receipt"] not in RECEIPT_VALUES:
        bad("receipt", "not one of %s" % (RECEIPT_VALUES,))

    if "signal_encodings" in channel:
        v = channel["signal_encodings"]
        if not isinstance(v, int) or isinstance(v, bool):
            bad("signal_encodings", "not an int")
        elif v < 0:
            bad("signal_encodings", "negative")

    if "encoder_position" in channel and \
            channel["encoder_position"] not in ENCODER_VALUES:
        bad("encoder_position", "not one of %s" % (ENCODER_VALUES,))

    for field in ("latency", "build_on_time"):
        if field in channel:
            v = channel[field]
            if not _is_number(v):
                bad(field, "not a number")
            elif not math.isfinite(v):
                bad(field, "not finite")
            elif v < 0:
                bad(field, "negative")

    if "time_unit" in channel and not (
            isinstance(channel["time_unit"], str) and channel["time_unit"]):
        bad("time_unit", "not a non-empty string; both times or no rating")

    if "construction" in channel and \
            channel["construction"] not in CONSTRUCTION_VALUES:
        bad("construction", "not one of %s" % (CONSTRUCTION_VALUES,))

    # [CHOICE 5] present-and-empty is supplied; absent is not.
    if "scope_note" in channel and not isinstance(channel["scope_note"], str):
        bad("scope_note", "not a string")

    # the order's one stated cross-field rule.
    if channel.get("encoder_position") == "NONE" and \
            isinstance(channel.get("signal_encodings"), int) and \
            not isinstance(channel.get("signal_encodings"), bool) and \
            channel["signal_encodings"] > 0:
        bad("encoder_position",
            "NONE is valid only when signal_encodings == 0")

    return missing, invalid


# --------------------------------------------------------------------------
# the four checks. Each reads its own fields and no others.

def c1_receipt(channel):
    """Fires unless receipt is enforced by structure."""
    return channel["receipt"] != "MANDATORY"


def c2_signal(channel):
    """Fires on any re-encoding. Counts encodings; does not read who wrote."""
    return channel["signal_encodings"] > 0


def c3_latency(channel):
    """Fires when the signal arrives no sooner than the output is built on."""
    return channel["latency"] >= channel["build_on_time"]


def c4_construction(channel):
    """Fires unless the party already paying can build it alone."""
    return channel["construction"] != "SLOW_SIDE_ONLY"


CHECKS = (("C1_RECEIPT", c1_receipt),
          ("C2_SIGNAL", c2_signal),
          ("C3_LATENCY", c3_latency),
          ("C4_CONSTRUCTION", c4_construction))

# which intake fields each check reads. Used by `independence()`, and the
# test asserts this table against the function bodies rather than trusting
# it.
CHECK_FIELDS = {"C1_RECEIPT": ("receipt",),
                "C2_SIGNAL": ("signal_encodings",),
                "C3_LATENCY": ("latency", "build_on_time"),
                "C4_CONSTRUCTION": ("construction",)}


def ratio(latency, build_on_time):
    """latency / build_on_time, or None where there is no denominator.

    None is not a small ratio and is not a zero. `ratio_state` carries the
    reason.
    """
    if not _is_number(latency) or not _is_number(build_on_time):
        return None
    if build_on_time == 0:
        return None
    return latency / build_on_time


def flags_for(channel):
    fired = []
    if channel["receipt"] == "UNSPECIFIED":
        fired.append("F_UNSPECIFIED_RECEIPT")
    if channel["encoder_position"] == "FAST_SIDE" and \
            channel["signal_encodings"] > 0:
        fired.append("F_FAST_SIDE_ENCODER")
    return fired


# --------------------------------------------------------------------------

def read(channel):
    """Score one channel. The SET is the output; it is not collapsed."""
    missing, invalid = intake(channel)
    get = channel.get if isinstance(channel, dict) else (lambda k: None)

    if missing or invalid:
        return {"channel_id": get("channel_id"),
                "failed": None,            # [CHOICE 1] no check ran
                "flags": None,
                "ratio": None,
                "ratio_state": RATIO_NOT_COMPUTED,
                "grade": INTAKE_INCOMPLETE,
                "scope_note": get("scope_note"),
                "time_unit": get("time_unit"),
                "missing": missing,
                "invalid": invalid}

    failed = [code for code, fn in CHECKS if fn(channel)]
    r = ratio(channel["latency"], channel["build_on_time"])
    return {"channel_id": channel["channel_id"],
            "failed": failed,
            "flags": flags_for(channel),
            "ratio": r,
            "ratio_state": RATIO_COMPUTED if r is not None else RATIO_UNDEFINED,
            "grade": GRADED if not failed else NOT_A_RETURN_PATH,
            "scope_note": channel["scope_note"],
            "time_unit": channel["time_unit"],
            "missing": [],
            "invalid": []}


# --------------------------------------------------------------------------
# properties the order states in prose, measured rather than asserted.

_IDEAL = {"channel_id": "probe", "receipt": "MANDATORY", "signal_encodings": 0,
          "encoder_position": "NONE", "latency": 1.0, "build_on_time": 100.0,
          "time_unit": "hours", "construction": "SLOW_SIDE_ONLY",
          "scope_note": "constructed probe, not a channel anyone runs"}

_FLIPS = {"C1_RECEIPT": {"receipt": "ELECTIVE"},
          "C2_SIGNAL": {"signal_encodings": 1, "encoder_position": "THIRD_PARTY"},
          "C3_LATENCY": {"latency": 500.0},
          "C4_CONSTRUCTION": {"construction": "REQUIRES_FAST_SIDE"}}


def independence():
    """Case B's property, generalised: flipping one check's own fields moves
    that check and no other.

    The C2 flip has to move encoder_position too, because NONE is invalid
    above zero encodings -- so the C2 row is a two-field flip by the order's
    own cross-field rule, and that is recorded rather than hidden.
    """
    rows = []
    base = read(_IDEAL)
    for code in CHECK_CODES:
        ch = dict(_IDEAL)
        ch.update(_FLIPS[code])
        got = read(ch)
        rows.append({"flipped": code,
                     "fields": sorted(_FLIPS[code]),
                     "failed": got["failed"],
                     "isolated": got["failed"] == [code]})
    return {"baseline_failed": base["failed"],
            "rows": rows,
            "all_isolated": all(r["isolated"] for r in rows)}


def encoder_reaches_no_check():
    """encoder_position is flag-only: at fixed encodings, moving it does not
    move `failed`. Measured over the whole declared vocabulary."""
    out = []
    for encodings in (0, 1):
        for pos in ENCODER_VALUES:
            ch = dict(_IDEAL)
            ch["signal_encodings"] = encodings
            ch["encoder_position"] = pos
            got = read(ch)
            out.append({"encodings": encodings, "encoder_position": pos,
                        "grade": got["grade"], "failed": got["failed"],
                        "flags": got["flags"]})
    distinct = {tuple(r["failed"]) for r in out
                if r["failed"] is not None and r["encodings"] == 1}
    return {"rows": out, "failed_sets_at_one_encoding": sorted(distinct),
            "encoder_moves_failed": len(distinct) > 1}


def falsifier_e_carried_by():
    """Case E fails C2 with a SLOW_SIDE encoder too, so the FAST_SIDE half of
    the falsifier adds no scoring power: C2 fires on the count alone."""
    rows = []
    for pos in ("FAST_SIDE", "SLOW_SIDE", "THIRD_PARTY"):
        ch = dict(_IDEAL)
        ch["signal_encodings"] = 1
        ch["encoder_position"] = pos
        got = read(ch)
        rows.append({"encoder_position": pos, "failed": got["failed"],
                     "flags": got["flags"], "grade": got["grade"]})
    return {"rows": rows,
            "all_fail_c2": all("C2_SIGNAL" in r["failed"] for r in rows),
            "only_fast_side_flags": [r["encoder_position"] for r in rows
                                     if "F_FAST_SIDE_ENCODER" in r["flags"]]}


# --------------------------------------------------------------------------

def _fmt(v, width):
    s = "--" if v is None else str(v)
    return s[:width].ljust(width)


def render(channels):
    lines = []
    lines.append("channel                     grade                "
                 "failed                                              "
                 "flags                  ratio")
    lines.append("-" * 135)
    for ch in channels:
        r = read(ch)
        failed = "--" if r["failed"] is None else (
            ", ".join(r["failed"]) if r["failed"] else "(none)")
        flags = "--" if r["flags"] is None else (
            ", ".join(f[2:] for f in r["flags"]) if r["flags"] else "(none)")
        ratio_s = "--" if r["ratio"] is None else "%.4g" % r["ratio"]
        lines.append("%s %s %s %s %s" % (
            _fmt(r["channel_id"], 27), _fmt(r["grade"], 20),
            _fmt(failed, 51), _fmt(flags, 22), ratio_s))
        if r["grade"] == INTAKE_INCOMPLETE:
            lines.append("    missing: %s" % (r["missing"] or "(none)"))
            lines.append("    invalid: %s" % (r["invalid"] or "(none)"))
        elif r["ratio"] is None:
            lines.append("    ratio: %s" % r["ratio_state"])
    lines.append("")
    lines.append("The set is the output. failed=None means no check ran "
                 "(intake); failed=[] means four ran and none fired.")
    lines.append("F_RATIO is not in the flags column: see CHOICE 4.")
    return "\n".join(lines)


def render_choices():
    lines = ["CHOICES -- decisions the order leaves open, taken here:"]
    for n in sorted(CHOICES):
        body = CHOICES[n]
        lines.append("  [CHOICE %d] %s" % (n, body))
    lines.append("")
    lines.append("SCHEMA ADDITIONS beyond the order's stated return: %s"
                 % ", ".join(SCHEMA_ADDITIONS))
    return "\n".join(lines)


def main():
    import cases
    print(render_choices())
    print()
    print(render(cases.CASES))
    print()
    ind = independence()
    print("independence: flip one check's fields, does only that check move?")
    for row in ind["rows"]:
        print("  %-16s fields %-32s -> failed %s%s"
              % (row["flipped"], ",".join(row["fields"]), row["failed"],
                 "" if row["isolated"] else "   NOT ISOLATED"))
    print("  baseline failed: %s   all isolated: %s"
          % (ind["baseline_failed"], ind["all_isolated"]))
    print()
    enc = encoder_reaches_no_check()
    print("encoder_position against the scored set, at one encoding:")
    print("  distinct failed sets across all four positions: %s"
          % (enc["failed_sets_at_one_encoding"],))
    print("  encoder_position moves `failed`: %s" % enc["encoder_moves_failed"])
    fal = falsifier_e_carried_by()
    print("  case E with the encoder moved: all fail C2 = %s, "
          "flagged only at %s" % (fal["all_fail_c2"], fal["only_fast_side_flags"]))


if __name__ == "__main__":
    main()
