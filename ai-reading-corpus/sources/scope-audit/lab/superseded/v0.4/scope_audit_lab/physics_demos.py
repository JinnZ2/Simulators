"""Law-driven physics demonstration domains (v0.4). Standard library only.

Each generator produces cases whose output values are computed from a stated
physical law with stated parameters — a distinct data category for the lab:
not field measurements (MEASURED) and not free invention, but LAW-DRIVEN
SIMULATION, labeled as such in every case note and payload. Planted
structure, where present, is declared explicitly.

Domains (one per requested phenomenon):
  1. stopped_light   — EIT group velocity vs coupling Rabi frequency
                       (phenomenology after Hau et al. 1999; Liu et al. 2001)
  2. polarized_light — Malus's law, transmitted intensity vs analyzer angle
  3. em_resonance    — driven series RLC current vs drive frequency
  4. gravity_transect — microgravity profile over a buried point mass
  5. doppler_passby  — observed frequency of a moving source vs time

The suite runner scans every domain with the v0.2 engine and applies the
v0.3 procedures where each teaches the most: a threshold sweep on the
Malus curve, an order-permutation probe on the Doppler series, a matched
null baseline for the gravity survey, and a two-factor coupling scan on a
second RLC protocol in which frequency and capacitance both change. Every
outcome is recorded; no boundary, detection, or cause is declared anywhere.
"""
from __future__ import annotations

from typing import Any
import math
import random

from .core import Record
from .transitions import Case
from .core import make_transition_scan, make_audit_event
from .experiments import (null_baseline_scan, threshold_sweep,
                          order_permutation_probe, coupling_scan,
                          make_experiment_record)

LAW_SIM_LABEL = ("law-driven simulation (output computed from a stated "
                 "physical law; synthetic, not a measurement)")

DOMAINS = ("stopped_light", "polarized_light", "em_resonance",
           "gravity_transect", "doppler_passby")

C_LIGHT = 299_792_458.0          # m/s, exact by SI definition
G_SI = 6.674e-11                 # m^3 kg^-1 s^-2 (2018 CODATA, as used in demos)
C_SOUND = 343.0                  # m/s in air, nominal demo value
MGAL_PER_SI = 1e5                # 1 m/s^2 = 1e5 mGal


def _log_grid(lo: float, hi: float, n: int) -> list[float]:
    if n < 2 or lo <= 0 or hi <= lo:
        raise ValueError("log grid needs n>=2 and 0 < lo < hi.")
    step = (math.log(hi) - math.log(lo)) / (n - 1)
    return [math.exp(math.log(lo) + i * step) for i in range(n)]


# ---------------------------------------------------------------- 1. light

def stopped_light_cases(n_points: int = 20,
                        omega_hi_mhz: float = 5.0,
                        omega_lo_mhz: float = 0.05,
                        v_ref: float = 17.0,
                        omega_ref_mhz: float = 1.0) -> tuple[list[Case], dict]:
    """EIT phenomenology: v_g(Omega) = c * Omega^2 / (Omega^2 + Omega_K^2).

    Omega_K is calibrated so v_g(omega_ref_mhz) == v_ref (17 m/s, the Hau
    et al. 1999 figure). Cases are ordered from strong to weak coupling.
    """
    omega_ref = omega_ref_mhz * 1e6
    omega_k2 = omega_ref**2 * (C_LIGHT / v_ref - 1.0)
    cases = []
    for i, omega in enumerate(_log_grid(omega_lo_mhz * 1e6,
                                        omega_hi_mhz * 1e6, n_points)[::-1]):
        v_g = C_LIGHT * omega**2 / (omega**2 + omega_k2)
        cases.append(Case(f"eit_{i:02d}", omega / 1e6, v_g,
                          "coupling_rabi_frequency_mhz",
                          "group_velocity_m_per_s",
                          (LAW_SIM_LABEL,)))
    provenance = {
        "domain": "stopped_light",
        "law": "v_g(Omega) = c * Omega^2 / (Omega^2 + Omega_K^2) "
               "(EIT group-velocity phenomenology)",
        "parameters": {"omega_k_hz": math.sqrt(omega_k2),
                       "calibration": f"v_g({omega_ref_mhz} MHz) = {v_ref} m/s",
                       "c_m_per_s": C_LIGHT},
        "reference": ("Hau et al., Nature 397, 594-598 (1999), "
                      "doi:10.1038/17561; Liu et al., Nature 409, 490-493 "
                      "(2001), doi:10.1038/35054017"),
        "planted_structure": "none (smooth law curve)",
    }
    return cases, provenance


# ---------------------------------------------------------- 2. polarization

def polarized_light_cases(step_deg: float = 5.0,
                          i0: float = 1000.0) -> tuple[list[Case], dict]:
    """Malus's law: I(theta) = I0 * cos^2(theta), theta = 0..180 deg."""
    if step_deg <= 0 or 180.0 / step_deg != int(180.0 / step_deg):
        raise ValueError("step_deg must divide 180.")
    cases = []
    for i in range(int(180.0 / step_deg) + 1):
        theta = i * step_deg
        intensity = i0 * math.cos(math.radians(theta))**2
        if abs(intensity) < 1e-12:
            intensity = 0.0
        cases.append(Case(f"ang_{theta:05.1f}", theta, intensity,
                          "analyzer_angle_deg",
                          "transmitted_intensity_arb",
                          (LAW_SIM_LABEL,)))
    provenance = {
        "domain": "polarized_light",
        "law": "I(theta) = I0 * cos^2(theta) (Malus's law)",
        "parameters": {"i0_arb": i0, "step_deg": step_deg},
        "reference": ("standard optics; e.g. Harvard Natural Sciences "
                      "Lecture Demonstrations, 'Malus' Law'"),
        "planted_structure": "none (smooth law curve; zero crossing at 90 deg)",
    }
    return cases, provenance


# ------------------------------------------------------------------ 3. EM

def rlc_current_ma(freq_hz: float, v0: float, r_ohm: float,
                   l_henry: float, c_farad: float) -> float:
    """Steady-state current amplitude of a driven series RLC circuit."""
    omega = 2.0 * math.pi * freq_hz
    reactance = omega * l_henry - 1.0 / (omega * c_farad)
    return 1e3 * v0 / math.sqrt(r_ohm**2 + reactance**2)


def em_resonance_cases(n_points: int = 40, f_lo_hz: float = 20.0,
                       f_hi_hz: float = 2000.0, v0: float = 1.0,
                       r_ohm: float = 20.0, l_henry: float = 0.1,
                       c_farad: float = 10e-6) -> tuple[list[Case], dict]:
    """Driven series RLC: current amplitude vs drive frequency."""
    cases = []
    for i, f in enumerate(_log_grid(f_lo_hz, f_hi_hz, n_points)):
        i_ma = rlc_current_ma(f, v0, r_ohm, l_henry, c_farad)
        cases.append(Case(f"rlc_{i:02d}", f, i_ma,
                          "drive_frequency_hz", "current_amplitude_ma",
                          (LAW_SIM_LABEL,)))
    f0 = 1.0 / (2.0 * math.pi * math.sqrt(l_henry * c_farad))
    provenance = {
        "domain": "em_resonance",
        "law": "I(f) = V0 / sqrt(R^2 + (2*pi*f*L - 1/(2*pi*f*C))^2)",
        "parameters": {"v0_v": v0, "r_ohm": r_ohm, "l_henry": l_henry,
                       "c_farad": c_farad, "resonance_hz": f0},
        "reference": "standard circuit theory (series RLC resonance)",
        "planted_structure": "none (single smooth resonance of the law)",
    }
    return cases, provenance


def rlc_coupling_entries(n_steps: int = 30, v0: float = 1.0,
                         r_ohm: float = 20.0, l_henry: float = 0.1,
                         f_start_hz: float = 100.0, f_end_hz: float = 250.0,
                         c_start_uf: float = 8.0,
                         c_end_uf: float = 14.0) -> list[dict]:
    """Two-knob protocol: drive frequency and capacitance both change."""
    entries = []
    for k in range(n_steps):
        frac = k / (n_steps - 1)
        f = f_start_hz + frac * (f_end_hz - f_start_hz)
        c = (c_start_uf + frac * (c_end_uf - c_start_uf)) * 1e-6
        entries.append({
            "case_id": f"knob_{k:02d}",
            "factor_a": f,
            "factor_b": c * 1e6,
            "output": rlc_current_ma(f, v0, r_ohm, l_henry, c),
            "notes": (LAW_SIM_LABEL,
                      "two-knob protocol: frequency and capacitance co-vary"),
        })
    return entries


# --------------------------------------------------------------- 4. gravity

def gravity_transect_cases(spacing_m: float = 25.0, half_extent_m: float = 500.0,
                           excess_mass_kg: float = 1e9, depth_m: float = 100.0,
                           noise_sd_mgal: float = 0.03,
                           seed: int = 11) -> tuple[list[Case], dict]:
    """Vertical gravity anomaly of a buried point mass, plus seeded noise.

    dg_z(x) = G*M*z / (x^2 + z^2)^(3/2); peak G*M/z^2 at x = 0.
    """
    if spacing_m <= 0 or half_extent_m / spacing_m != int(half_extent_m / spacing_m):
        raise ValueError("half_extent_m must be an integer multiple of spacing_m.")
    rng = random.Random(seed)
    cases = []
    n = int(2 * half_extent_m / spacing_m) + 1
    for i in range(n):
        x = -half_extent_m + i * spacing_m
        dg_si = G_SI * excess_mass_kg * depth_m / (x**2 + depth_m**2) ** 1.5
        dg_mgal = dg_si * MGAL_PER_SI
        measured = dg_mgal + rng.gauss(0.0, noise_sd_mgal)
        cases.append(Case(f"grav_{i:02d}", x, measured,
                          "transect_position_m", "gravity_anomaly_mgal",
                          (LAW_SIM_LABEL,)))
    peak_mgal = G_SI * excess_mass_kg / depth_m**2 * MGAL_PER_SI
    provenance = {
        "domain": "gravity_transect",
        "law": "dg_z(x) = G*M*z / (x^2 + z^2)^(3/2) (buried point mass)",
        "parameters": {"excess_mass_kg": excess_mass_kg, "depth_m": depth_m,
                       "peak_anomaly_mgal": peak_mgal,
                       "noise_sd_mgal": noise_sd_mgal, "seed": seed},
        "reference": ("standard exploration geophysics; e.g. UCSD SIO 182 "
                      "gravity notes (point-mass anomaly)"),
        "planted_structure": (f"buried point mass of {excess_mass_kg:g} kg at "
                              f"{depth_m:g} m depth, centered at x = 0 "
                              "(planted by construction)"),
    }
    return cases, provenance


# ----------------------------------------------------------------- 5. sound

def doppler_passby_cases(step_s: float = 0.5, half_time_s: float = 10.0,
                         f0_hz: float = 1000.0, speed_m_per_s: float = 30.0,
                         closest_approach_m: float = 20.0,
                         c_sound: float = C_SOUND) -> tuple[list[Case], dict]:
    """Observed frequency of a source moving past an observer.

    f_obs(t) = f0 * c / (c - v_r(t)), with radial approach velocity
    v_r(t) = -v^2 t / sqrt(d^2 + (v t)^2). Closest approach at t = 0.
    """
    if speed_m_per_s >= c_sound:
        raise ValueError("demo assumes subsonic source speed.")
    if half_time_s / step_s != int(half_time_s / step_s):
        raise ValueError("half_time_s must be an integer multiple of step_s.")
    v = speed_m_per_s
    d = closest_approach_m
    cases = []
    n = int(2 * half_time_s / step_s) + 1
    for i in range(n):
        t = -half_time_s + i * step_s
        v_r = -v**2 * t / math.sqrt(d**2 + (v * t)**2) if t != 0 else 0.0
        f_obs = f0_hz * c_sound / (c_sound - v_r)
        cases.append(Case(f"dop_{i:02d}", t, f_obs,
                          "time_s", "observed_frequency_hz",
                          (LAW_SIM_LABEL,)))
    provenance = {
        "domain": "doppler_passby",
        "law": "f_obs = f0 * c / (c - v_r(t)) with v_r from pass-by geometry",
        "parameters": {"f0_hz": f0_hz, "speed_m_per_s": v,
                       "closest_approach_m": d, "c_sound_m_per_s": c_sound},
        "reference": "standard acoustics (Doppler effect, moving source)",
        "planted_structure": "none (smooth law curve with a direction change "
                             "at closest approach)",
    }
    return cases, provenance


GENERATORS = {
    "stopped_light": stopped_light_cases,
    "polarized_light": polarized_light_cases,
    "em_resonance": em_resonance_cases,
    "gravity_transect": gravity_transect_cases,
    "doppler_passby": doppler_passby_cases,
}

SCAN_THRESHOLDS = {
    "stopped_light": 50.0,
    "polarized_light": 40.0,
    "em_resonance": 6.0,
    "gravity_transect": 0.05,
    "doppler_passby": 15.0,
}


def run_physics_demo_suite() -> list[Record]:
    """Five domain scans plus four v0.3 procedures and a batch audit event."""
    records: list[Record] = []
    domain_cases: dict[str, list[Case]] = {}

    for domain in DOMAINS:
        cases, provenance = GENERATORS[domain]()
        domain_cases[domain] = cases
        scan = make_transition_scan(
            cases=cases, threshold=SCAN_THRESHOLDS[domain],
            threshold_kind="absolute",
            scan_label=f"physics demo: {domain} (law-driven simulation)")
        scan.payload["law_provenance"] = provenance
        records.append(scan)

    malus_sweep = make_experiment_record(threshold_sweep(
        domain_cases["polarized_light"], thresholds=[10.0, 40.0, 80.0, 150.0],
        sweep_label="physics demo: Malus threshold sweep"),
        linked_record_ids=[records[1].record_id])
    malus_sweep.payload["law_provenance"] = GENERATORS["polarized_light"]()[1]
    records.append(malus_sweep)

    doppler_permute = make_experiment_record(order_permutation_probe(
        domain_cases["doppler_passby"], n_permutations=25,
        threshold=SCAN_THRESHOLDS["doppler_passby"], seed=3,
        probe_label="physics demo: Doppler order probe"),
        linked_record_ids=[records[4].record_id])
    doppler_permute.payload["law_provenance"] = GENERATORS["doppler_passby"]()[1]
    records.append(doppler_permute)

    gravity_null = make_experiment_record(null_baseline_scan(
        n_cases=len(domain_cases["gravity_transect"]), n_replications=25,
        threshold=SCAN_THRESHOLDS["gravity_transect"], seed=11,
        distribution="normal", mean=0.0, sd=0.03,
        factor_label="transect_position_m",
        output_label="gravity_anomaly_mgal",
        label="physics demo: gravity-matched null"),
        linked_record_ids=[records[3].record_id])
    gravity_null.payload["matched_to"] = {
        "domain": "gravity_transect",
        "noise_model": "normal(0, 0.03 mGal), matching the survey generator",
        "note": "null record for side-by-side reading; no significance assigned",
    }
    records.append(gravity_null)

    rlc_couple = make_experiment_record(coupling_scan(
        rlc_coupling_entries(), threshold=SCAN_THRESHOLDS["em_resonance"],
        factor_a_label="drive_frequency_hz",
        factor_b_label="capacitance_uf",
        output_label="current_amplitude_ma",
        coupling_label="physics demo: RLC two-knob coupling"),
        linked_record_ids=[records[2].record_id])
    rlc_couple.payload["law_provenance"] = {
        "domain": "em_resonance (two-knob protocol)",
        "law": "I(f, C) with f and C co-varied along the protocol",
        "reference": "standard circuit theory (series RLC resonance)",
    }
    records.append(rlc_couple)

    counts = {d: len(r.payload["candidate_regions"])
              for d, r in zip(DOMAINS, records[:5])}
    event = make_audit_event(
        subject_record_ids=[r.record_id for r in records],
        event_kind="physics_demo_recorded",
        description="Five law-driven physics domains were scanned and four "
                    "instrument-level procedures applied; all outputs are "
                    "law-driven simulations, labeled, with interpretation "
                    "unassigned.",
        evidence=[
            f"candidate regions per domain: {counts}",
            f"Malus sweep: {len(malus_sweep.payload['region_appearances'])} "
            "distinct pair(s) across 4 thresholds",
            f"Doppler permutation: {len(doppler_permute.payload['region_appearances'])} "
            "distinct pair(s) across 26 scans",
            f"gravity null: max "
            f"{gravity_null.payload['recorded_summary']['max_candidate_regions']} "
            "candidate region(s) over 25 matched-noise replications",
            f"RLC coupling: {len(rlc_couple.payload['coincidence_record']['coincident_pairs'])} "
            "coincident pair(s)",
        ],
        unresolved_questions=[
            "Does the EIT knee mark a regime boundary of the medium, or of "
            "the absolute metric? (a relative-kind scan flags uniformly)",
            "Do the gravity flank flags exceed what the matched null "
            "generator produces?",
            "Does the RLC coincidence record indicate a joint cause, or two "
            "independent single-factor stories?",
            "Which of these law-driven curves has ever been checked against "
            "a measurement inside this lab? (none; all are Y-domain data)",
        ],
        proposed_next_tests=[
            "add a measurement-status field distinguishing MEASURED runs "
            "from law-driven simulations at scan time",
            "run a relative-kind EIT scan and record the metric contrast",
            "repeat the gravity transect at several noise seeds and record "
            "flag-position spread",
        ],
    )
    records.append(event)
    return records
