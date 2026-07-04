# field_compass.py
# CC0 | stdlib-only | phone-buildable
# grounding-layers/experimental :: orientation layer over the coupled field
#
# EXPERIMENTAL. Attempts to calibrate the audit-grade pipeline against
# human sensorimotor sensing. Not (yet) claim-pinned by CLAIMS.md.
# See ../USAGE.md for the audit-grade entry point (`audit()`); this
# instrument is peer to that but not part of the load-bearing L0-L5+Le
# stack.
#
# NOT a translator. An ALIGNER.
# Two processors read the same system from different substrates:
#   human  -> sensorimotor verdict (harmonics, damping, phase, feel)
#   AI     -> cascade prediction   (constraint propagation, coupling math)
# The compass points at the DELTA. Knowledge lives in the mismatch,
# not in either read alone.
#
# ENERGY FLOW
#   human read ─┐
#               ├─► align on shared frame ─► delta field ─► verdict
#   AI predict ─┘                                │
#                                                ├─ match  : hold model
#                                                └─ miss   : log delta
#                                                            update CLAIM
#                                                            (read never retuned)
#
# SCOPE (see ../SCOPE_TAXONOMY.md):
#   T = universal   (aligner logic is timescale-invariant)
#   S = universal
#   O = any_information_system (either processor -- human or AI --
#                               reads the same coupled system through
#                               a different substrate)
#   C = culture_neutral (the ALIGNER logic itself doesn't encode any
#                        specific epistemic tradition; specific reads
#                        and their frames carry their own scope)

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Callable


# ---------------------------------------------------------------- substrate
class Node(Enum):
    HUMAN = "sensorimotor"      # in the system, coupled, native harmonic read
    AI    = "constraint"        # outside, propagates coupling math


# ---------------------------------------------------------------- read
@dataclass
class Read:
    node: Node
    concentration: str          # where load/stress locates in the coupled system
    peak_load: float            # 0..1
    shift_margin: float         # 0..1  (1 = far from break, 0 = at break)
    signature: dict = field(default_factory=dict)  # harmonic detail, free-form
    note: str = ""


# ---------------------------------------------------------------- frame
@dataclass
class Frame:
    # the shared coordinate both reads must land in before they can be compared
    system: str                 # "truck_front_end" | "garden_plot" | ...
    driver: str                 # perturbation source: "groove_65mph" | "UV_dry" ...
    channels: tuple = ()        # which channels are in-frame for this compare

    def in_frame(self, r: Read) -> bool:
        return r.concentration in self.channels or not self.channels


# ---------------------------------------------------------------- compass
@dataclass
class Compass:
    frame: Frame
    human: Optional[Read] = None
    ai: Optional[Read] = None
    tol: float = 0.15           # match band on scalar channels

    def orient(self, r: Read):
        if r.node is Node.HUMAN:
            self.human = r
        else:
            self.ai = r
        return self

    # --- delta field: where the two reads diverge -----------------------
    def delta(self) -> dict:
        h, a = self.human, self.ai
        if h is None or a is None:
            return {"ready": False, "missing": Node.AI.value if a is None else Node.HUMAN.value}

        loc_match = (h.concentration == a.concentration)
        d_load = round(h.peak_load - a.peak_load, 3)
        d_margin = round(h.shift_margin - a.shift_margin, 3)
        scalar_ok = abs(d_load) < self.tol and abs(d_margin) < self.tol
        match = loc_match and scalar_ok

        return {
            "ready": True,
            "frame": self.frame.system,
            "driver": self.frame.driver,
            "location": {"human": h.concentration, "ai": a.concentration,
                         "agree": loc_match},
            "d_peak_load": d_load,       # + = human reads MORE stress than model
            "d_shift_margin": d_margin,  # - = human reads system CLOSER to break
            "match": match,
        }


# ---------------------------------------------------------------- verdict
def verdict(c: Compass) -> dict:
    d = c.delta()
    if not d.get("ready"):
        return {"action": "await_read", **d}

    if d["match"]:
        return {"action": "hold_model", "learned": None, **d}

    # WHERE did the model deform — that names what AI has to learn
    if not d["location"]["agree"]:
        lesson = ("coupling_topology_wrong: model located stress at "
                  f"{d['location']['ai']}, system broadcasts it at "
                  f"{d['location']['human']}")
    elif d["d_shift_margin"] < -c.tol:
        lesson = ("early_broadcast: human reads wear/stress before model's "
                  "threshold — coupling surfaces failure earlier than predicted")
    elif d["d_peak_load"] > c.tol:
        lesson = ("amplification_underweighted: model damped a channel the "
                  "coupling actually amplifies")
    else:
        lesson = "scalar_drift: magnitudes diverge, topology holds"

    return {
        "action": "log_delta -> update_claim",
        "learned": lesson,
        "rule": "update the CLAIM. never retune the human read.",
        **d,
    }


# ================================================================ demo
if __name__ == "__main__":

    # ---- TRUCK, US-54 WI, 65 mph, lateral groove --------------------
    frame = Frame(
        system="truck_front_end",
        driver="groove_65mph_speed_dependent_pitch",
        channels=("steering_feel", "tie_rod_right", "bump_response"),
    )

    # human sensorimotor read (the actual field read from the cab)
    human = Read(
        node=Node.HUMAN,
        concentration="tie_rod_right",
        peak_load=0.42,
        shift_margin=0.55,          # early — no tire feather yet
        signature={
            "pitch": "speed_dependent (tracks rpm, not groove)",
            "persists_across_surface": True,
            "right_amplitude": "elevated",
            "left_amplitude": "baseline",
            "steering_feedback": "pull_right_into_column",
            "damping": "right stiffer/noisier than left",
        },
        note="just started; preemptive service window open",
    )

    # AI cascade prediction BEFORE hearing the human read
    ai_naive = Read(
        node=Node.AI,
        concentration="steering_feel",   # model blames the symptom site
        peak_load=0.30,
        shift_margin=0.72,               # model thinks lots of margin left
        note="assumed symmetric bearing geometry, groove-coupled vibration",
    )

    c = Compass(frame).orient(human).orient(ai_naive)
    v = verdict(c)
    print("TRUCK compass verdict:")
    for k, val in v.items():
        print(f"  {k}: {val}")
