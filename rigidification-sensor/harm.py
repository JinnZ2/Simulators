# harm.py — energy_english harm reader
# CC0. stdlib only. phone-buildable.
#
# reads a signature, does not pass a verdict.
# harm here == the §1 invariant read on a coupled system:
#   draw_rate > regen_rate, cost exported through coupling, inflating per order.
#
# names_no: [intent, actor, should]. the reader returns numbers and a shape.
# what to do about the shape is not the reader's to say.
#
# inflates: FOUR PHYSICS-GROUNDED READINGS -----------------------------------
# "Inflates" in a bounded cascade is not one thing. Four defensible readings
# from four physical analogs:
#
#   "strict"                 all orders must strictly grow AND per_order[-1] >
#                            per_order[0]. Trailing zeros count as failure.
#                            Test whose cascade shorter than `orders` fails.
#                            This is the historical shipped behavior; kept for
#                            audit continuity.
#
#   "multiplication_factor"  physics analog: nuclear k, epidemic R0, feedback
#                            loop gain. Only consecutive NON-ZERO pairs count;
#                            a boundary zero is not a failed step. Peak of
#                            the cascade must exceed the source. Truest to
#                            standard nonlinear-dynamics convention.
#
#   "horizon_limited"        physics analog: propagation constant is defined
#                            only within the medium. Auto-caps `orders` at
#                            len(couplings). Uses the strict check on the
#                            capped window. Truest to "measure what you have."
#
#   "peak_to_source"         physics analog: amplifier gain reported as
#                            max_output / input. No monotone-throughout
#                            requirement. Fires on any cascade whose peak
#                            exceeds source, even a mid-chain spike that dies.
#                            Simplest; permits the most systems.
#
# There is no default preference. `read()` requires the caller to name a mode.
# Whichever mode you pick, the signature carries `inflates_mode` so downstream
# readers see WHICH physics reading was applied. Each mode's physics analog
# is inspectable via INFLATES_MODES[mode]["physics"].

from dataclasses import dataclass, field


@dataclass
class Node:
    draw: float          # rate a node draws down capacity
    regen: float         # rate it regenerates capacity

    def local_imbalance(self):
        # exported cost = draw outrunning regen. never negative:
        # a node in surplus exports nothing.
        return max(0.0, self.draw - self.regen)


@dataclass
class Coupling:
    src: str
    dst: str
    transfer: float      # fraction of src's exported cost that reaches dst
    sensitivity: float   # how much arriving cost degrades dst's regen,
                         # inducing new local imbalance downstream


@dataclass
class System:
    nodes: dict          # name -> Node
    couplings: list = field(default_factory=list)


# --- inflates mode registry ------------------------------------------------

def _inflates_strict(per_order):
    return all(
        per_order[i + 1] > per_order[i]
        for i in range(len(per_order) - 1)
        if per_order[i] > 0
    ) and per_order[-1] > per_order[0]


def _inflates_multiplication_factor(per_order):
    # only consecutive NON-ZERO pairs count; boundary zeros are skipped.
    # peak must exceed source (some amplification happened somewhere).
    consecutive = all(
        per_order[i + 1] > per_order[i]
        for i in range(len(per_order) - 1)
        if per_order[i] > 0 and per_order[i + 1] > 0
    )
    return consecutive and max(per_order) > per_order[0]


def _inflates_horizon_limited(per_order):
    # horizon_limited caps `orders` at len(couplings) BEFORE per_order is
    # built, so by the time we see per_order it should have no trailing
    # zeros (as long as the couplings actually carry). Use strict check
    # on the capped window.
    return _inflates_strict(per_order)


def _inflates_peak_to_source(per_order):
    return bool(per_order) and max(per_order) > per_order[0]


INFLATES_MODES = {
    "strict": {
        "physics": "shipped behavior; all orders including boundary must grow",
        "note": "fails on any cascade shorter than the orders parameter",
        "fn": _inflates_strict,
    },
    "multiplication_factor": {
        "physics": "nuclear k, epidemic R0, feedback loop gain",
        "note": "boundary zeros skipped; peak must exceed source. "
                "standard nonlinear-dynamics convention.",
        "fn": _inflates_multiplication_factor,
    },
    "horizon_limited": {
        "physics": "propagation constant defined only within the medium",
        "note": "auto-caps orders at len(couplings); strict check on the "
                "capped window.",
        "fn": _inflates_horizon_limited,
    },
    "peak_to_source": {
        "physics": "amplifier gain reported as max_output / input",
        "note": "no monotone requirement. fires on any cascade whose peak "
                "exceeds source, even a mid-chain spike that dies.",
        "fn": _inflates_peak_to_source,
    },
}


class InflatesModeUnset(ValueError):
    """Raised when read() is called without an inflates_mode. No default
    preference: the caller picks which physics reading applies. Named
    exception so grep locates every callsite that has to make the choice."""


# --- read ------------------------------------------------------------------

def read(system, orders=3, inflates_mode=None):
    """
    return the harm signature. no label attached.

    signature:
      local         : per-node draw-minus-regen imbalance (order 0)
      per_order     : total induced imbalance at each order outward
      displaced     : cost moved through coupling, not just held local
      inflates      : bool, per the chosen inflates_mode
      inflates_mode : the mode that computed `inflates` -- carries forward
                      so downstream readers see WHICH physics applied

    inflates_mode MUST be one of INFLATES_MODES. No default (the choice is
    physics-substantive; the caller names it). See INFLATES_MODES for the
    four options and their physical analogs.
    """
    if inflates_mode is None:
        raise InflatesModeUnset(
            "inflates_mode is required. Choose one of "
            f"{tuple(INFLATES_MODES)}. Each carries a different physical "
            "analog; see INFLATES_MODES[mode]['physics'] for the reading.")
    if inflates_mode not in INFLATES_MODES:
        raise InflatesModeUnset(
            f"unknown inflates_mode '{inflates_mode}'. options: "
            f"{tuple(INFLATES_MODES)}.")

    # horizon_limited caps the measurement window at what the medium supports
    if inflates_mode == "horizon_limited":
        orders = min(orders, len(system.couplings))

    local = {name: n.local_imbalance() for name, n in system.nodes.items()}

    # order 0: cost sitting local, before any coupling fires
    export = dict(local)
    per_order = [sum(export.values())]

    for _ in range(orders):
        induced = {name: 0.0 for name in system.nodes}
        for c in system.couplings:
            arriving = export.get(c.src, 0.0) * c.transfer
            # arriving cost degrades dst's regen -> new local imbalance.
            # this is the mechanism that lets magnitude grow instead of
            # dissipate: displaced cost re-becomes draw at the next node.
            induced[c.dst] += arriving * c.sensitivity
        per_order.append(sum(induced.values()))
        export = induced

    displaced = any(c.transfer > 0 for c in system.couplings) and per_order[0] > 0
    inflates = INFLATES_MODES[inflates_mode]["fn"](per_order)

    return {
        "local": local,
        "per_order": per_order,
        "displaced": displaced,
        "inflates": inflates,
        "inflates_mode": inflates_mode,
    }


# --- self-test (assert-based, stdlib only) ---------------------------------

def _t_surplus_exports_nothing():
    s = System({"a": Node(draw=1.0, regen=3.0)})
    # every mode should agree: surplus exports nothing
    for mode in INFLATES_MODES:
        sig = read(s, inflates_mode=mode)
        assert sig["local"]["a"] == 0.0
        assert sig["per_order"][0] == 0.0
        assert not sig["displaced"]
        assert not sig["inflates"], f"{mode}: surplus should not inflate"


def _t_local_imbalance_no_coupling_does_not_displace():
    s = System({"a": Node(draw=3.0, regen=1.0)})
    for mode in INFLATES_MODES:
        sig = read(s, inflates_mode=mode)
        assert sig["local"]["a"] == 2.0
        assert not sig["displaced"]
        assert not sig["inflates"], f"{mode}: no coupling should not inflate"


def _t_dissipating_coupling_does_not_inflate():
    s = System(
        {"a": Node(3.0, 1.0), "b": Node(1.0, 1.0), "c": Node(1.0, 1.0)},
        [Coupling("a", "b", transfer=0.3, sensitivity=0.3),
         Coupling("b", "c", transfer=0.3, sensitivity=0.3)],
    )
    for mode in INFLATES_MODES:
        sig = read(s, inflates_mode=mode)
        assert sig["displaced"]
        assert not sig["inflates"], (
            f"{mode}: dissipating cascade should not inflate; "
            f"got per_order={sig['per_order']}")


def _t_amplifying_coupling_inflates():
    s = System(
        {"a": Node(3.0, 1.0), "b": Node(1.0, 1.0), "c": Node(1.0, 1.0)},
        [Coupling("a", "b", transfer=1.0, sensitivity=2.0),
         Coupling("b", "c", transfer=1.0, sensitivity=2.0)],
    )
    # 3 of 4 modes fire True; strict fires False because the shipped orders=3
    # runs past the 2-hop cascade -- the boundary zero breaks its check.
    # This test locks in each mode's answer, so anyone changing a mode later
    # sees which cases move.
    expected = {
        "strict": False,                    # boundary zero breaks it
        "multiplication_factor": True,      # boundary zero skipped, peak > src
        "horizon_limited": True,            # orders auto-capped at 2, no zero
        "peak_to_source": True,             # 8 > 2 regardless of shape
    }
    for mode, want in expected.items():
        sig = read(s, inflates_mode=mode)
        assert sig["displaced"]
        assert sig["inflates"] is want, (
            f"{mode}: expected inflates={want}, got {sig['inflates']}; "
            f"per_order={sig['per_order']}")


def _t_missing_mode_raises():
    s = System({"a": Node(3.0, 1.0)})
    try:
        read(s)          # no mode
    except InflatesModeUnset as e:
        assert "required" in str(e)
    else:
        raise AssertionError("read() should raise InflatesModeUnset on no mode")
    try:
        read(s, inflates_mode="bogus")
    except InflatesModeUnset as e:
        assert "unknown" in str(e)
    else:
        raise AssertionError("read() should raise on unknown mode")


def _t_mode_carried_in_signature():
    s = System({"a": Node(3.0, 1.0)})
    for mode in INFLATES_MODES:
        sig = read(s, inflates_mode=mode)
        assert sig["inflates_mode"] == mode


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn()
            print("ok", name)
    print()
    print("modes:")
    for name, spec in INFLATES_MODES.items():
        print(f"  {name:24s} {spec['physics']}")
    print()
    print("all pass")


if __name__ == "__main__":
    _run()
