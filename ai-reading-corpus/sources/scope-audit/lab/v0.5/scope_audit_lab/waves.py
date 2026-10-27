"""Waves: light as electromagnetism, with sound as contrast (v0.5).

Terminology correction carried from the v0.4 cycle: the EIT phenomenon is
SLOW LIGHT (group velocity far below c); "stopped light" denotes its storage
limit (Liu et al. 2001). The v0.4 domain name is retained for compatibility
and aliased here as ``slow_light_cases``.

This module records four things, all law-driven and labeled as such:
  1. em_unification   — Maxwell's prediction c = 1/sqrt(mu0*eps0) compared
                        against the exact SI value of c, using the lab's own
                        compare_numeric machinery. A prediction-vs-measurement
                        record: residual and uncertainty recorded, no verdict.
  2. em_spectrum      — one law, lambda = c/f, spanning radio to gamma:
                        "they exist in electromagnetism", recorded as cases.
  3. longitudinal_contrast — the same analyzer-rotation procedure applied to
                        a longitudinal wave (sound in air): intensity does not
                        respond. Polarization is the transverse-wave signature;
                        the engine records the contrast (Malus flags many
                        pairs; the longitudinal series flags none).
  4. sound_speed      — c_sound = sqrt(gamma*R*T/M): a wave speed that needs
                        a medium parameter (molar mass of air), unlike light.

No boundary, detection, cause, or significance is declared anywhere.
"""
from __future__ import annotations

from typing import Any
import math

from .core import Record, compare_numeric
from .transitions import Case
from .core import make_transition_scan, make_audit_event
from .physics_demos import (stopped_light_cases as slow_light_cases,
                            polarized_light_cases, LAW_SIM_LABEL)

# 2018 CODATA values (post-2019 SI: measured quantities with uncertainties)
MU0 = 1.25663706212e-6        # N/A^2
U_MU0 = 1.9e-16
EPS0 = 8.8541878128e-12       # F/m
U_EPS0 = 1.3e-21
C_EXACT = 299_792_458.0       # m/s, exact by SI definition
R_GAS = 8.314462618           # J/(mol K), exact
GAMMA_AIR = 1.4
M_AIR = 0.029                 # kg/mol, nominal dry air
C_LIGHT = C_EXACT

EM_BANDS = (  # (name, f_lo_hz, f_hi_hz) — conventional, approximate bounds
    ("radio", 1e3, 1e9), ("microwave", 1e9, 1e12),
    ("infrared", 1e12, 4.3e14), ("visible", 4.3e14, 7.5e14),
    ("ultraviolet", 7.5e14, 3e16), ("x-ray_and_above", 3e16, 1e19),
)


def em_unification_comparison() -> Record:
    """Record Maxwell's prediction of c against the exact SI value.

    prediction: c_pred = 1/sqrt(mu0*eps0), uncertainty propagated from the
    CODATA uncertainties of mu0 and eps0. observation: c, exact by SI
    definition since 1983 (uncertainty zero). compare_numeric computes the
    residual and normalized residual; interpretation stays unresolved.
    """
    c_pred = 1.0 / math.sqrt(MU0 * EPS0)
    rel = 0.5 * math.hypot(U_MU0 / MU0, U_EPS0 / EPS0)
    u_pred = rel * c_pred
    cmp = compare_numeric(c_pred, C_EXACT,
                          prediction_uncertainty=u_pred,
                          observation_uncertainty=0.0)
    payload = {
        "experiment_kind": "em_unification",
        "data_status": ("law-driven prediction (Maxwell) vs exact SI constant; "
                        "not a new measurement"),
        "law": "c = 1/sqrt(mu0*eps0) (Maxwell's electromagnetic wave speed)",
        "inputs": {
            "mu0_n_per_a2": MU0, "u_mu0": U_MU0,
            "eps0_f_per_m": EPS0, "u_eps0": U_EPS0,
            "source": "2018 CODATA (post-2019 SI: mu0 and eps0 are measured)",
        },
        "comparison": {
            "predicted_c_m_per_s": cmp.prediction,
            "observed_c_m_per_s": cmp.observation,
            "residual_m_per_s": cmp.residual,
            "prediction_uncertainty_m_per_s": u_pred,
            "normalized_residual": cmp.normalized_residual,
            "comparison_status": cmp.comparison_status,
            "notes": list(cmp.notes),
        },
        "historical_note": ("Maxwell (1865) found 1/sqrt(mu0*eps0) close to "
                            "Fizeau's measured light speed and concluded "
                            "'light is an electromagnetic disturbance'."),
        "interpretation": "unassigned",
        "limitations": [
            "The near-zero residual is recorded, not celebrated: post-2019 SI "
            "defines c exactly and measures mu0/eps0, so agreement is partly "
            "definitional structure, not pure prediction.",
            "No verdict is assigned about electromagnetism or light.",
        ],
    }
    return Record.create("experiment", payload)


def _band_of(f: float) -> str:
    for name, f_lo, f_hi in EM_BANDS:
        if f_lo <= f < f_hi:
            return name
    return EM_BANDS[-1][0]


def em_spectrum_cases(n_points: int = 72,
                      f_lo_hz: float = 1e3,
                      f_hi_hz: float = 1e19) -> tuple[list[Case], dict]:
    """lambda = c/f on one global log grid, band labels as case notes.

    The default density (72 points over 16 decades, ~0.23 decades/step)
    guarantees at least one sample inside the narrowest band (visible).
    """
    step = (math.log(f_hi_hz) - math.log(f_lo_hz)) / (n_points - 1)
    cases = []
    for idx in range(n_points):
        f = math.exp(math.log(f_lo_hz) + idx * step)
        cases.append(Case(f"em_{idx:02d}", f, C_LIGHT / f,
                          "frequency_hz", "wavelength_m",
                          (LAW_SIM_LABEL, f"band: {_band_of(f)}")))
    provenance = {
        "domain": "em_spectrum",
        "law": "lambda = c / f (one law from radio to gamma)",
        "parameters": {"c_m_per_s": C_LIGHT},
        "reference": "standard electromagnetism (Maxwell)",
        "planted_structure": "none (smooth law; band labels are conventions)",
    }
    return cases, provenance


def longitudinal_contrast_cases(step_deg: float = 5.0,
                                i0: float = 1000.0) -> tuple[list[Case], dict]:
    """Analyzer-rotation analog applied to a longitudinal wave: no response."""
    cases = []
    for i in range(int(180.0 / step_deg) + 1):
        theta = i * step_deg
        cases.append(Case(f"lon_{theta:05.1f}", theta, i0,
                          "rotation_angle_deg",
                          "transmitted_intensity_arb",
                          (LAW_SIM_LABEL,
                           "longitudinal wave: no polarization response")))
    provenance = {
        "domain": "longitudinal_contrast",
        "law": "I(theta) = I0 (constant): longitudinal waves have no "
               "transverse mode for an analyzer to select",
        "parameters": {"i0_arb": i0, "step_deg": step_deg},
        "reference": "standard wave mechanics (transverse vs longitudinal)",
        "planted_structure": "none (flat law by construction)",
    }
    return cases, provenance


def sound_speed_cases(t_lo_k: float = 200.0, t_hi_k: float = 320.0,
                      step_k: float = 10.0,
                      gamma: float = GAMMA_AIR,
                      molar_mass: float = M_AIR) -> tuple[list[Case], dict]:
    """c_sound(T) = sqrt(gamma*R*T/M) for an ideal gas."""
    cases = []
    n = int((t_hi_k - t_lo_k) / step_k) + 1
    for i in range(n):
        t = t_lo_k + i * step_k
        c = math.sqrt(gamma * R_GAS * t / molar_mass)
        cases.append(Case(f"air_{t:05.1f}K", t, c,
                          "temperature_k", "sound_speed_m_per_s",
                          (LAW_SIM_LABEL,
                           "speed set by the medium (air), unlike light")))
    provenance = {
        "domain": "sound_speed",
        "law": "c = sqrt(gamma*R*T/M) (ideal gas)",
        "parameters": {"gamma_air": gamma, "molar_mass_kg_per_mol": molar_mass,
                       "r_j_per_mol_k": R_GAS},
        "reference": "standard thermodynamics/acoustics",
        "planted_structure": "none (smooth law curve)",
    }
    return cases, provenance


def run_waves_demo_suite() -> list[Record]:
    """Unification comparison, three scans, the Malus contrast, audit event."""
    records: list[Record] = []

    records.append(em_unification_comparison())

    spectrum_cases, spectrum_prov = em_spectrum_cases()
    spectrum_scan = make_transition_scan(
        cases=spectrum_cases, threshold=1.0, threshold_kind="absolute",
        scan_label="waves demo: EM spectrum (law-driven simulation)")
    spectrum_scan.payload["law_provenance"] = spectrum_prov
    records.append(spectrum_scan)

    lon_cases, lon_prov = longitudinal_contrast_cases()
    lon_scan = make_transition_scan(
        cases=lon_cases, threshold=40.0, threshold_kind="absolute",
        scan_label="waves demo: longitudinal rotation (law-driven simulation)")
    lon_scan.payload["law_provenance"] = lon_prov
    records.append(lon_scan)

    malus_cases, malus_prov = polarized_light_cases()
    malus_scan = make_transition_scan(
        cases=malus_cases, threshold=40.0, threshold_kind="absolute",
        scan_label="waves demo: Malus contrast (law-driven simulation)")
    malus_scan.payload["law_provenance"] = malus_prov
    records.append(malus_scan)

    sound_cases, sound_prov = sound_speed_cases()
    sound_scan = make_transition_scan(
        cases=sound_cases, threshold=2.0, threshold_kind="absolute",
        scan_label="waves demo: sound speed vs temperature (law-driven simulation)")
    sound_scan.payload["law_provenance"] = sound_prov
    records.append(sound_scan)

    cmp_payload = records[0].payload["comparison"]
    event = make_audit_event(
        subject_record_ids=[r.record_id for r in records],
        event_kind="waves_demo_recorded",
        description="Maxwell unification recorded as prediction-vs-constant; "
                    "spectrum, polarization contrast, and sound-speed scans "
                    "recorded as law-driven simulations.",
        evidence=[
            f"c predicted 1/sqrt(mu0*eps0) = {cmp_payload['predicted_c_m_per_s']:.6f} m/s; "
            f"residual vs exact c = {cmp_payload['residual_m_per_s']:.3e} m/s "
            f"(u = {cmp_payload['prediction_uncertainty_m_per_s']:.4f} m/s)",
            f"polarization contrast: Malus flags "
            f"{len(malus_scan.payload['candidate_regions'])} pairs; "
            f"longitudinal flags {len(lon_scan.payload['candidate_regions'])}",
            f"spectrum scan flags {len(spectrum_scan.payload['candidate_regions'])} "
            "pairs at 1 m absolute threshold (geometric span, metric artifact)",
            f"sound scan flags {len(sound_scan.payload['candidate_regions'])} "
            "pairs at 2 m/s threshold",
        ],
        unresolved_questions=[
            "The EM spectrum scan's flags are a metric artifact of absolute "
            "deltas on a log grid — does a relative-kind scan flag uniformly "
            "instead, as it did for EIT?",
            "The longitudinal series records all 'unchanged' directions — is "
            "a zero-delta run a detection of 'no transverse mode' or of "
            "'nothing to detect'? (recorded as neither)",
            "Sound speed depends on the medium's molar mass; light's speed "
            "does not. Should medium-dependence become a declared scope "
            "field for wave records?",
        ],
        proposed_next_tests=[
            "relative-kind scan on the EM spectrum series",
            "extend the spectrum record with per-band energy E = h*f",
            "record a measured (not law-driven) Malus series from a real "
            "polarizer pair when available",
        ],
    )
    records.append(event)
    return records
