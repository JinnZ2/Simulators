#!/usr/bin/env python3
# incentive_blindspot_sim.py
#
# Coupled difference-equation model of how an institution's incentive
# structure (credential closure + capital concentration + frame narrowness)
# suppresses external seeing, lets structural blind spots accumulate, and
# drives the system toward the exact failure mode it claims to prevent.
#
# The thesis is mechanical, not moral: the trajectory toward catastrophe is
# a consequence of the coupling topology, not of anyone's intent.
#
# Properties live in the couplings, not the nodes.
# Substrate first: this is a dynamical system, read it as flows, not labels.
#
# stdlib only. CC0 / public domain. Runs from a phone.
# Build: JinnZ2 + collaborator. No credentials required to run it.
#
# REFUTATION_PROTOCOL: if a CLAIM check fails, you update the CLAIM (or the
# stated coupling topology) to match reality. You do NOT retune the weights
# to make a falsified claim pass. The weights are frozen estimates; the
# claims are the falsifiable content.

import math

# ----------------------------------------------------------------------
# WEIGHTS
# These are GENERAL ESTIMATES from accumulated evidence across institutional
# failure cases (engineering disasters, financial collapses, captured fields).
# They are NOT measured constants. They set the *shape* of the dynamics, not
# precise magnitudes. Refine the numbers later; the topology is the claim.
# ----------------------------------------------------------------------
WEIGHTS = {
    "alpha_V":      0.18,  # how fast external visibility tracks its gated target
    "k_complexity": 0.040, # blind spot added per unit of "safety complexity"
    "k_blind":      0.050, # blind spot accumulation when correction signal is low
    "k_patch":      0.18,  # blind spot patched when external seeing is high
    "k_conf":       0.09,  # in-group confidence gain from unrefuted state + hidden B
    "k_humility":   0.16,  # confidence eroded when external seeing is high
    "k_entrench":   0.06,  # confidence -> tighter credential closure
    "k_narrow":     0.05,  # confidence -> narrower frame
    "decay":        0.02,  # passive relaxation of C, F toward openness
    "lam":          2.5,   # maps current blind-spot volume -> failure probability
}

# ----------------------------------------------------------------------
# STATE  (all variables bounded [0,1] except the hazard accumulator)
#   C : credential_closure     - standing requires institutional credentials
#   M : capital_concentration  - decision power concentrated in funded actors
#   F : frame_narrowness       - threat model is a mirror of in-group reasoning
#   V : external_visibility    - capacity to receive + act on outside signal
#   B : blindspot_volume       - accumulated unaddressed structural error
#   X : in_group_confidence    - belief the problem is solved (false certainty)
#
# P_fail is read from CURRENT blind-spot volume, not accumulated over time:
# the question is "given today's structural blindness, how likely is the
# claimed-prevented failure to express" - not "does anything ever fail given
# infinite time" (everything does). The contrast is in rate and asymptote.
# ----------------------------------------------------------------------

def clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else hi if x > hi else x

def p_fail(B):
    # current-exposure failure probability: monotone map of present blind-spot
    # volume. Bounded, saturating, never forced to 1 by mere passage of time.
    return 1.0 - math.exp(-WEIGHTS["lam"] * B)

def step(s, p):
    """Advance one timestep. s = state dict, p = scenario params."""
    w = WEIGHTS
    C, M, F, V, B, X = s["C"], s["M"], s["F"], s["V"], s["B"], s["X"]

    # --- external visibility is gated multiplicatively: any gate near 1
    #     collapses the system's ability to see outside its own frame ---
    V_target = (1.0 - C) * (1.0 - M) * (1.0 - F)
    # structural transparency floor (the intervention lever): if a scenario
    # *enforces* openness by structure, V cannot be gated below it.
    V_target = max(V_target, p.get("transparency_floor", 0.0))
    V_new = V + w["alpha_V"] * (V_target - V)

    # --- blind spots: grow from added "safety complexity" and from low
    #     correction signal; shrink only when external seeing is high ---
    dB = (w["k_complexity"] * p["complexity_rate"]
          + w["k_blind"] * (1.0 - V) * (1.0 - B)
          - w["k_patch"] * V * B)
    B_new = clamp(B + dB)

    # --- the perverse loop: nothing has visibly failed yet, so accumulated
    #     blind spots READ AS success and feed confidence; low visibility
    #     means no challengers to puncture it ---
    dX = w["k_conf"] * ((1.0 - V) + B) * (1.0 - X) - w["k_humility"] * V * X
    X_new = clamp(X + dX)

    # --- confidence entrenches the gates that caused the blindness ---
    C_new = clamp(C + w["k_entrench"] * X_new * (1.0 - C) - w["decay"] * C)
    F_new = clamp(F + w["k_narrow"] * X_new * (1.0 - F) - w["decay"] * F)
    # capital concentration drifts up slowly with sustained confidence
    M_new = clamp(M + 0.5 * w["k_entrench"] * X_new * (1.0 - M) - w["decay"] * M)

    return {"C": C_new, "M": M_new, "F": F_new, "V": V_new,
            "B": B_new, "X": X_new}

def run(scenario, steps=60):
    s = dict(scenario["init"])
    traj = [dict(s)]
    for _ in range(steps):
        s = step(s, scenario["params"])
        traj.append(dict(s))
    return traj

# ----------------------------------------------------------------------
# SCENARIOS
# init = starting structural posture. params = ongoing drivers.
# ----------------------------------------------------------------------
SCENARIOS = {
    # heavy credential gate, concentrated capital, mirror-frame threat model,
    # actively adding "safety complexity" (the published-roadmap posture)
    "credentialed_closed": {
        "init":   {"C": 0.75, "M": 0.70, "F": 0.70, "V": 0.25, "B": 0.05, "X": 0.40},
        "params": {"complexity_rate": 1.0, "transparency_floor": 0.0},
    },
    # distributed, low gate, low concentration, plural frames, transparency
    # enforced by structure (CC0 / open provenance) -> visibility floored high
    "distributed_open": {
        "init":   {"C": 0.20, "M": 0.20, "F": 0.25, "V": 0.70, "B": 0.05, "X": 0.20},
        "params": {"complexity_rate": 0.2, "transparency_floor": 0.65},
    },
    # same closed structure, but a transparency floor is imposed mid-system:
    # tests whether external visibility is the actual control variable
    "closed_with_transparency": {
        "init":   {"C": 0.75, "M": 0.70, "F": 0.70, "V": 0.25, "B": 0.05, "X": 0.40},
        "params": {"complexity_rate": 1.0, "transparency_floor": 0.55},
    },
}

# ----------------------------------------------------------------------
# FALSIFIABLE CLAIMS
# Each returns (verdict, detail). Verdict in {SUPPORTED, REFUTED}.
# A REFUTED claim means: update the claim/topology, do not retune weights.
# ----------------------------------------------------------------------
def claim_BS_001(warmup=10):
    """Closed-incentive P_fail exceeds open-incentive P_fail at every step
    after warmup. Refuted if open >= closed at any post-warmup step."""
    a = run(SCENARIOS["credentialed_closed"])
    b = run(SCENARIOS["distributed_open"])
    for t in range(warmup, len(a)):
        if p_fail(b[t]["B"]) >= p_fail(a[t]["B"]):
            return ("REFUTED", f"open>=closed at t={t}")
    gap = p_fail(a[-1]["B"]) - p_fail(b[-1]["B"])
    return ("SUPPORTED", f"closed above open for t>={warmup}; final gap={gap:.3f}")

def claim_BS_002():
    """Added 'safety complexity' raises blind spots. Counterfactual: same
    closed structure, complexity ON vs OFF. Refuted if turning complexity on
    does not increase final blind-spot volume."""
    on  = run(SCENARIOS["credentialed_closed"])
    off_scn = {"init": dict(SCENARIOS["credentialed_closed"]["init"]),
               "params": {"complexity_rate": 0.0, "transparency_floor": 0.0}}
    off = run(off_scn)
    bon, boff = on[-1]["B"], off[-1]["B"]
    if bon > boff:
        return ("SUPPORTED", f"final B: complexity_off={boff:.3f} -> on={bon:.3f}")
    return ("REFUTED", f"complexity did not raise B ({bon:.3f} vs {boff:.3f})")

def claim_BS_003():
    """In the closed regime, confidence (X) and blind spots (B) rise together
    (positive covariance): false certainty grows with hidden error.
    Refuted if covariance <= 0."""
    a = run(SCENARIOS["credentialed_closed"])
    xs = [r["X"] for r in a]; bs = [r["B"] for r in a]
    mx = sum(xs)/len(xs); mb = sum(bs)/len(bs)
    cov = sum((x-mx)*(b-mb) for x, b in zip(xs, bs)) / len(xs)
    return (("SUPPORTED" if cov > 0 else "REFUTED"), f"cov(X,B)={cov:.5f}")

def claim_BS_004():
    """External visibility is the control variable: imposing a transparency
    floor on the SAME closed structure bounds final blind-spot volume below
    the un-floored closed run. Refuted if the floor does not reduce final B."""
    closed = run(SCENARIOS["credentialed_closed"])
    floored = run(SCENARIOS["closed_with_transparency"])
    bc, bf = closed[-1]["B"], floored[-1]["B"]
    if bf < bc:
        return ("SUPPORTED", f"final B: closed={bc:.3f} -> floored={bf:.3f}")
    return ("REFUTED", f"transparency floor did not reduce B ({bf:.3f} vs {bc:.3f})")

CLAIMS = [
    ("CLAIM_BS_001  closed P_fail > open P_fail",        claim_BS_001),
    ("CLAIM_BS_002  gated complexity raises blind spots", claim_BS_002),
    ("CLAIM_BS_003  false confidence tracks hidden error", claim_BS_003),
    ("CLAIM_BS_004  visibility is the control lever",      claim_BS_004),
]

# ----------------------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------------------
def fmt_row(t, r):
    return (f"{t:>3} | C={r['C']:.2f} M={r['M']:.2f} F={r['F']:.2f} "
            f"V={r['V']:.2f} | B={r['B']:.2f} X={r['X']:.2f} "
            f"| P_fail={p_fail(r['B']):.3f}")

def print_trajectory(name, every=10):
    traj = run(SCENARIOS[name])
    print(f"\n=== {name} ===")
    print("  t |  gates (C/M/F) + visibility   | blind/conf  | claimed-fail prob")
    for t, r in enumerate(traj):
        if t % every == 0 or t == len(traj) - 1:
            print(fmt_row(t, r))

def print_claims():
    print("\n=== FALSIFIABLE CLAIMS (REFUTATION_PROTOCOL active) ===")
    for label, fn in CLAIMS:
        verdict, detail = fn()
        print(f"  [{verdict:9}] {label}")
        print(f"              -> {detail}")

def main():
    print("incentive_blindspot_sim  --  trajectory toward self-inflicted failure")
    print("weights are frozen estimates; the coupling topology is the claim.")
    for name in ("credentialed_closed", "distributed_open", "closed_with_transparency"):
        print_trajectory(name)
    print_claims()
    # headline divergence
    c = run(SCENARIOS["credentialed_closed"])[-1]
    o = run(SCENARIOS["distributed_open"])[-1]
    print(f"\nFINAL P_fail  closed={p_fail(c['B']):.3f}   open={p_fail(o['B']):.3f}")
    print("The structure built to ensure safety is the structure that fails it.")

if __name__ == "__main__":
    main()
