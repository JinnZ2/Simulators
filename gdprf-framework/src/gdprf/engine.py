"""GDPRF update engine — operational cycle steps 3, 3.5, 4, 5 (spec v3.0).

Step 3   Metrological evaluation: SNR filter + provenance-weighted bias correction
Step 3.5 Confidence calibration: raw fidelity -> calibrated fidelity
Step 4   Gradient update: log-odds Bayesian update over calibrated evidence
Step 5   Identification gate: hidden-variable search may not update gradients
         unless the gate passes (Miao et al. 2018 conditions / D'Amour 2019 check)
"""
from __future__ import annotations
import math
from dataclasses import dataclass

# --- Amendment 2: provenance weighting of metrological values ---
PROVENANCE_WEIGHTS = {"measured": 1.0, "estimated": 0.6, "assumed": 0.3}


def metrology_weight(source: str) -> float:
    """Weight a metrological value by its provenance (measured > estimated > assumed).

    An 'assumed' systematic bias is treated as a weak prior, not a fixed offset,
    preventing circular updating (Kane 1997)."""
    if source not in PROVENANCE_WEIGHTS:
        raise ValueError(f"unknown provenance source: {source}")
    return PROVENANCE_WEIGHTS[source]


def snr_passes(effect_size: float, noise_floor: float, k: float = 2.0) -> bool:
    """Step 3 SNR filter: a shift must exceed k * noise_floor to count as signal."""
    return abs(effect_size) > k * noise_floor


def bias_correction(raw: float, systematic_bias: float, bias_source: str) -> tuple[float, float]:
    """Apply provenance-weighted bias correction.

    Returns (corrected_value, residual_bias_uncertainty). A measured bias is
    fully corrected; an assumed bias is corrected only partially and leaves
    residual uncertainty that widens the claim's variance margin."""
    w = metrology_weight(bias_source)
    corrected = raw - systematic_bias * w
    residual_uncertainty = abs(systematic_bias) * (1.0 - w)
    return corrected, residual_uncertainty


# --- Amendment 1 / step 3.5: calibration ---

def calibrate_fidelity(proxy: dict, uncalibrated_shrink: float = 0.5) -> tuple[float, bool]:
    """Return (effective_fidelity, was_calibrated).

    Calibrated proxies contribute their calibrated_fidelity. Uncalibrated
    proxies (method 'none') are shrunk toward neutrality (0.5) — evidence from
    an uncalibrated instrument moves the gradient less (Tabacof & Costabello
    2019; Safavi et al. 2020)."""
    cal = proxy.get("calibration", {})
    method = cal.get("method", "none")
    raw = proxy["fidelity_gradient"]
    if method == "none" or cal.get("calibrated_fidelity") is None:
        shrunk = 0.5 + (raw - 0.5) * uncalibrated_shrink
        return shrunk, False
    return cal["calibrated_fidelity"], True


def cascade_fidelity(fidelities: list[float]) -> float:
    """Fidelity decays multiplicatively along a proxy cascade."""
    out = 1.0
    for f in fidelities:
        out *= f
    return out


# --- Step 4: gradient update (log-odds Bayesian) ---

def gradient_update(prior: float, evidences: list[tuple[float, float]]) -> float:
    """Continuous log-odds update.

    evidences: list of (effective_fidelity, signed_coupling) where signed
    coupling in [-1, 1] comes from the edge (negative = disconfirming).
    Each piece of evidence shifts log-odds by coupling * fidelity * LR_strength.
    Returns posterior in (0, 1) — never a boolean."""
    prior = min(max(prior, 1e-6), 1 - 1e-6)
    lo = math.log(prior / (1 - prior))
    for fidelity, coupling in evidences:
        lo += coupling * fidelity * 1.5  # LR strength constant; documented, tunable
    return 1.0 / (1.0 + math.exp(-lo))


# --- Amendment 4 / step 5: identification gate ---

@dataclass
class GateResult:
    status: str            # "passed" | "failed" | "not_triggered"
    action: str            # what the engine did about it
    assumptions: list[str]

def identification_gate(claim: dict) -> GateResult:
    """Hidden-variable search may not update gradients unless the gate passes.

    - Not triggered -> nothing to do.
    - Triggered + gate 'passed' -> exploratory evidence may update (with listed assumptions).
    - Triggered + gate 'pending'/'failed' -> residual variance is reported as
      unexplained ignorance: raise unknown_variable_risk_score instead of
      chasing noise (D'Amour 2019 fragility)."""
    hvs = claim.get("hidden_variable_search", {})
    if not hvs.get("triggered", False):
        return GateResult("not_triggered", "no action", [])
    gate = hvs.get("identification_gate", {})
    status = gate.get("status", "pending")
    assumptions = gate.get("assumptions", [])
    if status == "passed" and assumptions:
        return GateResult("passed", "exploratory evidence admitted under listed assumptions", assumptions)
    return GateResult("failed" if status == "failed" else "pending",
                      "gradient frozen for this branch; unknown_variable_risk_score raised",
                      assumptions)


# --- Enhancement 1 (v3.0): blindness-adjusted likelihood ---
#
# Likelihood_adjusted(D|H) = (1 - P(Blind)) * P(D|H) + P(Blind) * P(Uninformative)
#
# An observation from a proxy in a known blindness state yields near-zero
# information gain — it must NOT shift the posterior toward zero (absence of
# signal is not evidence of absence) and must NOT count as confirmation either.

def blindness_adjusted_evidence(effective_fidelity: float, coupling: float,
                                epistemic_mask_score: float) -> tuple[float, float]:
    """Scale a (fidelity, coupling) evidence pair by the blindness mask.

    P(Blind) = epistemic_mask_score. In a fully blind state (mask -> 1) the
    evidence collapses to zero coupling (uninformative) regardless of what the
    instrument reported. Returns (fidelity, adjusted_coupling)."""
    mask = min(max(epistemic_mask_score, 0.0), 1.0)
    return effective_fidelity, coupling * (1.0 - mask)


def gradient_update_masked(prior: float,
                           evidences: list[tuple[float, float, float]]) -> float:
    """Gradient update over (fidelity, coupling, mask) triples — v3.0 default.

    Blind observations produce no information gain instead of false absence."""
    adjusted = [blindness_adjusted_evidence(f, c, m) for f, c, m in evidences]
    return gradient_update(prior, adjusted)


def transduction_chain_fidelity(chain: list[dict]) -> float:
    """Multiplicative fidelity across a transduction chain
    (phenomenon -> interaction -> transducer -> conditioning -> digitization -> indication)."""
    out = 1.0
    for link in chain:
        out *= link["fidelity"]
    return out


def effective_fidelity_v3(proxy: dict, uncalibrated_shrink: float = 0.5) -> tuple[float, dict]:
    """v3.0 effective fidelity: calibrated fidelity x transduction chain fidelity,
    with traceability penalty for broken/convention-only chains."""
    fid, was_cal = calibrate_fidelity(proxy)
    chain_f = transduction_chain_fidelity(proxy.get("transduction_chain", [])) or 1.0
    trace = proxy.get("traceability_pyramid", {})
    status = trace.get("calibration_chain_status", "intact")
    trace_factor = {"intact": 1.0, "expired": 0.9, "convention_only": 0.8, "broken": 0.6}[status]
    eff = fid * chain_f * trace_factor
    return eff, {"calibrated": was_cal, "calibrated_fidelity": round(fid, 4),
                 "chain_fidelity": round(chain_f, 4),
                 "traceability_factor": trace_factor,
                 "traceability_status": status,
                 "effective": round(eff, 4)}
