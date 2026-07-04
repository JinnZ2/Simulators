# holistic_field_state.py
# CC0 | stdlib-only | phone-buildable
# grounding-layers/experimental :: Le entry instrument
#
# EXPERIMENTAL. Attempts to calibrate the audit-grade pipeline against
# human sensorimotor sensing. Not (yet) claim-pinned by CLAIMS.md.
# Peer to the L0-L5+Le audit-grade stack in ../ but not part of the
# load-bearing pipeline.
#
# PREMISE
#   The operator is the instrument. One read, many channels, fired together.
#   Diagnosis lives in the COUPLING, not in any isolated channel.
#   Same engine reads a truck front axle or a garden soil-plant-insect stack:
#   both are coupled dynamical systems; you locate where stress concentrates
#   and project how far the system sits from a shift.
#
# ENERGY-FLOW FRAME
#   channels ---> confidence gate ---> coupling graph ---> stress field
#   stress field ---> shift-margin ---> Le verdict ---> cascade compare
#   contradiction ---> log delta ---> update claim   (never retune the read)
#
# SCOPE (see ../SCOPE_TAXONOMY.md):
#   T = universal   (multi-channel read of any coupled system)
#   S = universal   (substrate is caller-declared: garden, truck,
#                    ecosystem, ...)
#   O = any_information_system (the OPERATOR/instrument can be a
#                               human, an AI with sensors, or a
#                               distributed sensor rig)
#   C = culture_neutral (the framework itself is culture-neutral;
#                        specific channel taxonomies and confidence
#                        gates encode the operator's own epistemic
#                        tradition and should be documented per-read)

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------- confidence
class Trust(Enum):
    HIGH     = "any_context"      # bounce, smell, vibration-response: run anywhere
    BASELINE = "known_history"    # taste, mineral, toxin: needs baseline, else gated
    GATED    = "withheld"         # refuse the read (no baseline + real risk)


# ---------------------------------------------------------------- channel
@dataclass
class Channel:
    name: str
    reading: str                 # verb-first state, not a number-if-none-exists
    trust: Trust
    magnitude: float = 0.0        # -1..+1  deviation from baseline (0 = at baseline)
    note: str = ""

    def live(self) -> bool:
        return self.trust is not Trust.GATED


# ---------------------------------------------------------------- coupling
@dataclass
class Edge:
    src: str                      # channel/subsystem that drives
    dst: str                      # channel/subsystem that receives
    mode: str                     # "feeds" | "stresses" | "damps" | "amplifies"
    transfer: float               # 0..1  how much of src's state moves dst


# ---------------------------------------------------------------- field state
@dataclass
class FieldState:
    substrate: str                # "garden" | "truck" | ...
    where: str
    when: str
    channels: list = field(default_factory=list)
    edges: list = field(default_factory=list)

    # --- register a read -------------------------------------------------
    def read(self, ch: Channel):
        self.channels.append(ch)
        return self

    def couple(self, src, dst, mode, transfer):
        self.edges.append(Edge(src, dst, mode, transfer))
        return self

    # --- stress field: where does load concentrate ----------------------
    def stress_field(self) -> dict:
        load = {c.name: 0.0 for c in self.channels if c.live()}
        for e in self.edges:
            if e.dst not in load:
                continue
            src = next((c for c in self.channels if c.name == e.src), None)
            if src is None or not src.live():
                continue
            drive = abs(src.magnitude) * e.transfer
            if e.mode in ("stresses", "amplifies"):
                load[e.dst] += drive
            elif e.mode == "damps":
                load[e.dst] -= drive
        return dict(sorted(load.items(), key=lambda kv: -kv[1]))

    # --- how far from a regime shift ------------------------------------
    def shift_margin(self) -> float:
        # margin = 1 - peak coupled load, clamped. low margin = near a break.
        sf = self.stress_field()
        peak = max(sf.values(), default=0.0)
        return round(max(0.0, 1.0 - peak), 3)

    # --- Le verdict: what enters the cascade ----------------------------
    def verdict(self) -> dict:
        sf = self.stress_field()
        peak_node = next(iter(sf), None)
        return {
            "substrate": self.substrate,
            "where": self.where, "when": self.when,
            "concentration": peak_node,
            "peak_load": round(sf.get(peak_node, 0.0), 3) if peak_node else 0.0,
            "shift_margin": self.shift_margin(),
            "gated": [c.name for c in self.channels if not c.live()],
            "confidence": {c.name: c.trust.value for c in self.channels if c.live()},
        }


# ---------------------------------------------------------------- refutation
def compare(prediction: dict, measured: dict) -> dict:
    # cascade predicted a coupled state; operator read the real one.
    # return the delta. contradiction updates the CLAIM, never the read.
    keys = ("concentration", "peak_load", "shift_margin")
    delta = {}
    for k in keys:
        p, m = prediction.get(k), measured.get(k)
        if isinstance(p, (int, float)) and isinstance(m, (int, float)):
            delta[k] = round(m - p, 3)
        else:
            delta[k] = (p, m) if p != m else None
    matched = all(
        (v is None) or (isinstance(v, float) and abs(v) < 0.15)
        for v in delta.values()
    )
    return {
        "match": matched,
        "delta": delta,
        "action": "hold_model" if matched else "log_delta -> update_claim",
    }


# ================================================================ demo
if __name__ == "__main__":

    # ---- GARDEN: soil-plant-insect coupled read (known ground) ---------
    g = FieldState("garden", "home_plot_east", "2026-07-03T06:20")
    g.read(Channel("soil_bounce", "slow rebound, staying compressed",
                   Trust.HIGH, magnitude=+0.55,
                   note="mycorrhizal thinning, worm activity down"))
    g.read(Channel("soil_smell", "flat, low petrichor",
                   Trust.HIGH, magnitude=+0.40))
    g.read(Channel("soil_taste", "not run", Trust.GATED,
                   note="skipped - not needed, baseline already set by bounce"))
    g.read(Channel("plant_vigor", "lower-leaf stress, turgor holding",
                   Trust.HIGH, magnitude=+0.35))
    g.read(Channel("insect_diversity", "pollinators present, decomposers sparse",
                   Trust.HIGH, magnitude=+0.30))
    g.read(Channel("predator_activity", "few insectivores working the plot",
                   Trust.HIGH, magnitude=+0.25))
    g.read(Channel("humidity_skin", "dry air, UV sharp on skin",
                   Trust.HIGH, magnitude=+0.45))

    # coupling geometry: how the read moves together
    g.couple("humidity_skin", "soil_bounce", "stresses", 0.6)
    g.couple("soil_bounce",   "plant_vigor", "stresses", 0.7)
    g.couple("soil_bounce",   "insect_diversity", "stresses", 0.5)
    g.couple("insect_diversity", "predator_activity", "feeds", 0.8)
    g.couple("insect_diversity", "predator_activity", "stresses", 0.4)

    print("GARDEN verdict :", g.verdict())

    # ---- TRUCK: same engine, mechanical substrate ----------------------
    t = FieldState("truck", "front_axle", "2026-07-03T14:10")
    t.read(Channel("bump_response", "sharper return on right side seams",
                   Trust.HIGH, magnitude=+0.50,
                   note="kingpin play, front axle right"))
    t.read(Channel("steering_feel", "slight wander loading into curves",
                   Trust.HIGH, magnitude=+0.35))
    t.read(Channel("tire_wear_read", "inner-edge feather, right front",
                   Trust.HIGH, magnitude=+0.30))
    t.couple("bump_response", "steering_feel", "amplifies", 0.7)
    t.couple("bump_response", "tire_wear_read", "stresses", 0.6)

    print("TRUCK  verdict :", t.verdict())

    # ---- refutation: cascade predicted vs operator read ----------------
    predicted = {"concentration": "plant_vigor",
                 "peak_load": 0.30, "shift_margin": 0.70}
    print("COMPARE        :", compare(predicted, g.verdict()))
