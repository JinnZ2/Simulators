"""
divergence.py -- the correction Kavik named: the starting point is different,
so the analog cannot be inherited whole.

CC0. stdlib-only. Anti-freeze.

Every paleo analog in baseline.py ran from a world WITH:
  - continental ice (Laurentide etc.)
  - an active glacial meltwater buffer (the pulses had a source AND a sink)
  - a working permafrost freeze/thaw cycle
  - rising sea level from deglaciation

The Upper Midwest now has NONE of those. So when we borrow an analog we must
strip the terms that depended on them and FLAG what that does to the transition.
The output is not "analog X says it'll be Y degrees." It is: "analog X's PATTERN,
minus the glacier-dependent buffering, points faster and choppier, and here are
the specific terms we could not inherit." Trajectory + honest gap, never verdict.

Key inherited finding (from the conversation, kept as a load-bearing claim):
  No glacier => no meltwater buffer => freshwater loading is OCEAN-sourced
  (Antarctic + Greenland) and is NOT self-limiting the way a draining lake was.
  Therefore: recovery seen in the 8.2ka analog should be DISCOUNTED. The pulse
  that recovered was finite. This one is fed.
"""

from dataclasses import dataclass
from typing import Optional
import baseline


@dataclass
class DivergenceReport:
    analog_name: str
    inheritable: dict          # term -> True/False (can we carry it?)
    stripped_terms: list       # what we removed and why
    rate_adjustment: str       # direction the missing buffers push the rate
    recovery_adjustment: str   # what happens to the analog's recovery behaviour
    confidence_after: str
    keeper_gaps: list          # things only a local keeper / field data can fill


# the now-state for the target region. Defaults describe Upper Midwest /
# Canadian Shield. Override per site.
NOW_STATE_DEFAULT = {
    "continental_ice": False,
    "meltwater_buffer": False,
    "permafrost_cycle": False,   # discontinuous/absent at this latitude now
    "sea_level_rising": True,    # still true, but ocean/thermal sourced
}


def diverge(analog: baseline.Analog,
            now_state: Optional[dict] = None) -> DivergenceReport:
    now = dict(NOW_STATE_DEFAULT)
    if now_state:
        now.update(now_state)

    inheritable = {}
    stripped = []
    for term, then_val in analog.starting_state.items():
        now_val = now.get(term)
        # a term is inheritable only if the starting condition matches
        ok = (then_val == now_val)
        inheritable[term] = ok
        if not ok:
            stripped.append(
                f"{term}: analog had {then_val!r}, now {now_val!r} -> "
                f"any analog behaviour that leaned on this term is removed"
            )

    # rate: losing meltwater buffer and permafrost thermal inertia removes
    # damping. Missing buffers make the transition FASTER and choppier.
    lost_buffers = [t for t in ("meltwater_buffer", "permafrost_cycle")
                    if not inheritable.get(t, True)]
    if lost_buffers:
        rate_adj = ("FASTER + higher-variance than analog: lost damping from "
                    + ", ".join(lost_buffers) +
                    ". Analog transition_decades is an UPPER bound on time; "
                    "treat the low end as more likely, and expect overshoot.")
    else:
        rate_adj = "analog rate inheritable as-is"

    # recovery: the 8.2ka-style recovery required a finite pulse. Ocean-sourced
    # loading is fed, not finite -> discount recovery.
    if not inheritable.get("meltwater_buffer", True):
        recovery_adj = ("DISCOUNT analog recovery. The analog recovered because "
                        "its freshwater pulse was finite (a draining lake / "
                        "waning ice). Present loading is ocean-sourced (Antarctic"
                        " + Greenland) and sustained. Expect collapse to hold or "
                        "oscillate around the collapsed attractor rather than "
                        "self-heal.")
    else:
        recovery_adj = "analog recovery behaviour inheritable"

    # confidence drops one notch when we strip terms (we are extrapolating)
    order = ["low", "medium", "high"]
    idx = order.index(analog.confidence)
    conf_after = order[max(0, idx - (1 if stripped else 0))]

    keeper_gaps = [
        "local soil thermal mass + drainage (sets real ecosystem lag here)",
        "regional precip routing under a shifted jet stream (analog ITCZ/monsoon"
        " signal does not map 1:1 onto mid-continent)",
        "species-specific cold/variance tolerance for THIS biome "
        "(keeper-supplied; no AI-filled cells)",
    ]

    return DivergenceReport(
        analog_name=analog.name,
        inheritable=inheritable,
        stripped_terms=stripped,
        rate_adjustment=rate_adj,
        recovery_adjustment=recovery_adj,
        confidence_after=conf_after,
        keeper_gaps=keeper_gaps,
    )


if __name__ == "__main__":
    for a in baseline.all_analogs():
        r = diverge(a)
        print(f"\n=== {r.analog_name} (conf -> {r.confidence_after}) ===")
        for s in r.stripped_terms:
            print("  strip:", s)
        print("  rate:", r.rate_adjustment)
        print("  recov:", r.recovery_adjustment)
