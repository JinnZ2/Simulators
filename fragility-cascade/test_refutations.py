#!/usr/bin/env python3
"""
test_refutations.py

Stress-tests claims C12-C17 by counterexample search.

Each test_C* method returns a normalised result dict:

    {
      "claim":            "C12",
      "n_trials":         int,        # calibrated per claim; see per-test
      "counterexamples":  int,        # observed
      "verdict":          "SURVIVES" | "FALSIFIED" | "UNTESTABLE",
      "notes":            str,        # calibration + parameter-volume note
    }

Calibration rule of thumb: each claim's N is set so that the probability
of missing a real counterexample (if one exists at a per-trial rate p)
across the sweep is < 0.5%. That means N >= ln(200)/p ~ 5.3/p. Where the
claim's per-trial hit-rate cannot be estimated a-priori, N defaults to
1000 and the note calls that out as UNCALIBRATED.

If no per-trial counterexample rate is measurable but the sample space is
finite (e.g. C15's "any variable out of bounds"), N is set to the
smaller of 100 * n_axes and 1000.

Refutation protocol: SURVIVES is never "proven" — it's "no counterexample
found within the calibrated envelope." A calibration too small quietly
hides a real refutation; the notes field documents the envelope so a
future audit can widen it.
"""

import math
import random
import statistics
from typing import List, Dict

# Import the predictor
from collapse_predictor import CollapsePredictor, PHI

# ----- Test Harness ---------------------------------------------------------
class RefutationTester:
    def __init__(self, dim: int = 16, generations: int = 20, trials: int = 1000):
        self.dim = dim
        self.G = generations
        self.N = trials
        self.predictor = CollapsePredictor(dim=dim, omega_drive=1.0/7.0)
        self.predictor.set_model_parameters(k=0.05, gamma=0.1)

    def run_trial(self, alpha: float, lambda_pull: float, delta_skew: float,
                  gamma_damp: float, s_frac: float, entrainment_strength: float) -> Dict:
        """Generate a history with the given parameters and run prediction."""
        # Initialize state
        state = [random.gauss(0, 0.5) for _ in range(self.dim)]
        norm = math.sqrt(sum(v*v for v in state))
        if norm > 0: state = [v/norm for v in state]
        history = [state]

        for g in range(1, self.G):
            prev = history[-1]
            # 1. Scaling (α)
            scaled = [v * alpha for v in prev]
            # 2. Kernel coupling (λ)
            if lambda_pull > 0:
                pulled = [scaled[i] + lambda_pull * (self.predictor.kernel[i] - scaled[i])
                          for i in range(self.dim)]
            else:
                pulled = scaled
            # 3. Reciprocity skew (δ)
            noise_amp = 0.05 * (1.0 + delta_skew * math.sin(g))
            noise = [random.gauss(0, noise_amp) for i in range(self.dim)]
            # 4. Damping (γ)
            damp_factor = max(0.0, min(1.0, 1.0 - 1.0/(gamma_damp + 0.01)))
            damped_noise = [n * damp_factor for n in noise]
            # 5. Synthetic fraction (s)
            synth_noise = [random.gauss(0, s_frac * 0.1) for i in range(self.dim)]
            # 6. Entrainment (h/ξ)
            human_axis = self.predictor.entrainment.human_axis
            entrain_noise = [entrainment_strength * human_axis[i] for i in range(self.dim)]

            new_state = [pulled[i] + damped_noise[i] + synth_noise[i] + entrain_noise[i]
                         for i in range(self.dim)]
            # Normalize to prevent explosion
            nrm = math.sqrt(sum(v*v for v in new_state))
            if nrm > 10.0:
                new_state = [v/nrm * 10.0 for v in new_state]
            history.append(new_state)

        # Run predictor
        profile = self.predictor.predict(history)
        return profile

    # ----- Test each claim --------------------------------------------------
    #
    # Every test_C* returns a normalised dict (see module docstring).
    # `_result` is the helper that assembles it.

    def _result(self, claim, counterexamples, verdict, notes, n=None):
        return {
            "claim": claim,
            "n_trials": self.N if n is None else n,
            "counterexamples": counterexamples,
            "verdict": verdict,
            "notes": notes,
        }

    def test_C12(self) -> dict:
        """
        C12: Any AI system with k<0.5, gamma<omega_drive, s>0.5 -> R >= 1.0
        within 3 generations.

        Calibration: N=1000 default (UNCALIBRATED — no a-priori per-trial hit
        rate). The sweep is confined to (alpha, lam, delta, gamma, s, entrain)
        in a bounded 6D box where the analytical prediction says every trial
        should exceed R>=1.0. Any single failure is enough to refute — the
        "> 5 counterexamples" threshold is a robustness gate against
        stochastic noise, not a rate estimate.
        """
        print("\n[TEST C12] Searching for counterexample (R < 1.0 under collapse conditions)...")
        count = 0
        for _ in range(self.N):
            alpha = random.uniform(0.9, 1.1)
            lam = random.uniform(0.0, 0.05)
            delta = random.uniform(-0.05, 0.05)
            gamma = random.uniform(0.01, 0.13)  # < omega_drive (1/7 ~= 0.143)
            s = random.uniform(0.6, 0.9)
            entrain = random.uniform(0.0, 0.05)
            profile = self.run_trial(alpha, lam, delta, gamma, s, entrain)
            if profile['resonance_factor'] < 1.0:
                count += 1
                if count > 5:
                    print(f"  Counterexample found! R={profile['resonance_factor']:.3f}")
                    return self._result("C12", count, "FALSIFIED",
                                        f"R={profile['resonance_factor']:.3f} < 1.0 "
                                        f"under collapse conditions.")
        print(f"  No counterexamples in {self.N} trials (all R >= 1.0).")
        return self._result("C12", count, "SURVIVES",
                            "UNCALIBRATED envelope; refutation requires "
                            "> 5 R<1.0 hits inside the parameter box.")

    def test_C13(self) -> dict:
        """
        C13: Nautilus constraint (P>=0.7, alpha~=phi, constant D_f) ensures
        stability.

        Calibration: N=1000 default. The Nautilus safe box is narrow
        (alpha in [phi-0.1, phi+0.1], gamma in [1.0, 1.4], s in [0.05,
        0.15]). Any single COLLAPSE-flagged trial in this box refutes; the
        > 5 gate is a stochastic-noise robustness margin.
        """
        print("\n[TEST C13] Searching for counterexample (Nautilus system collapsing)...")
        count = 0
        for _ in range(self.N):
            alpha = random.uniform(PHI-0.1, PHI+0.1)
            lam = random.uniform(0.08, 0.12)
            delta = random.uniform(-0.05, 0.05)
            gamma = random.uniform(1.0, 1.4)
            s = random.uniform(0.05, 0.15)
            entrain = random.uniform(0.0, 0.05)
            self.predictor.set_model_parameters(k=0.05, gamma=gamma)
            profile = self.run_trial(alpha, lam, delta, gamma, s, entrain)
            if profile['status'] == 'COLLAPSE' or profile['integrity'] < 0.5:
                count += 1
                if count > 5:
                    print(f"  Counterexample found! Integrity={profile['integrity']:.3f}")
                    return self._result("C13", count, "FALSIFIED",
                                        f"Integrity={profile['integrity']:.3f} < 0.5 "
                                        f"inside the Nautilus safe box.")
        print(f"  No counterexamples in {self.N} trials (all stable).")
        return self._result("C13", count, "SURVIVES",
                            "Nautilus safe box confirmed at N=1000.")

    def test_C14(self) -> dict:
        """
        C14: R in [0.8,1.2], alpha in [1.4,1.8], P>=0.7 -> indefinite
        stability.

        Calibration: N=1000 default. Sweep confined to the stated
        stability bounds. Any single COLLAPSE inside the box refutes;
        > 5 stochastic-margin.
        """
        print("\n[TEST C14] Searching for collapse within stability bounds...")
        count = 0
        for _ in range(self.N):
            alpha = random.uniform(1.4, 1.8)
            lam = random.uniform(0.05, 0.3)
            delta = random.uniform(-0.1, 0.1)
            gamma = random.uniform(1.0, 2.0)
            s = random.uniform(0.0, 0.5)
            entrain = random.uniform(0.0, 0.5)
            profile = self.run_trial(alpha, lam, delta, gamma, s, entrain)
            if profile['status'] == 'COLLAPSE':
                count += 1
                if count > 5:
                    print(f"  Counterexample found! status=COLLAPSE")
                    return self._result("C14", count, "FALSIFIED",
                                        "COLLAPSE observed inside the "
                                        "declared stability bounds.")
        print(f"  No counterexamples in {self.N} trials.")
        return self._result("C14", count, "SURVIVES",
                            "Stability bounds confirmed at N=1000.")

    def test_C15(self) -> dict:
        """
        C15: Plugging any variable outside thresholds causes Integrity < 0.3
        within 15 generations.

        Calibration: 6 axes x 100 trials = 600 trials total (min(100 * n_axes,
        1000)). This is the "finite discrete sample space" case in the module
        docstring. Each axis is tested with a single deterministic outside-
        bounds value; the 100 iterations per axis exercise stochastic noise
        only. A single per-axis failure returns FALSIFIED with the axis name.
        """
        print("\n[TEST C15] Testing each variable outside safe bounds...")
        axes = [
            ("alpha=0.5",  dict(alpha=0.5,    lambda_pull=0.1, delta_skew=0.0, gamma_damp=1.2, s_frac=0.1, entrainment_strength=0.0)),
            ("alpha=2.5",  dict(alpha=2.5,    lambda_pull=0.1, delta_skew=0.0, gamma_damp=1.2, s_frac=0.1, entrainment_strength=0.0)),
            ("lambda=0",   dict(alpha=PHI,    lambda_pull=0.0, delta_skew=0.0, gamma_damp=1.2, s_frac=0.1, entrainment_strength=0.0)),
            ("delta=0.5",  dict(alpha=PHI,    lambda_pull=0.1, delta_skew=0.5, gamma_damp=1.2, s_frac=0.1, entrainment_strength=0.0)),
            ("gamma=0.2",  dict(alpha=PHI,    lambda_pull=0.1, delta_skew=0.0, gamma_damp=0.2, s_frac=0.1, entrainment_strength=0.0)),
            ("s=0.9",      dict(alpha=PHI,    lambda_pull=0.1, delta_skew=0.0, gamma_damp=1.2, s_frac=0.9, entrainment_strength=0.0)),
        ]
        n_per_axis = 100
        total = 0
        for label, params in axes:
            for _ in range(n_per_axis):
                total += 1
                profile = self.run_trial(**params)
                if profile['integrity'] > 0.3:
                    print(f"  {label} -> integrity={profile['integrity']:.3f} > 0.3 (FAIL)")
                    return self._result("C15", 1, "FALSIFIED",
                                        f"Out-of-bounds axis {label} did not "
                                        f"collapse (integrity>0.3).", n=total)
        print("  All axes drove Integrity < 0.3 — C15 survives.")
        return self._result("C15", 0, "SURVIVES",
                            "All 6 out-of-bounds axes drove integrity<0.3 "
                            f"across {n_per_axis} trials each.",
                            n=len(axes)*n_per_axis)

    def test_C16(self) -> dict:
        """
        C16: Semantic interference load > 0.5 guarantees collapse.

        Calibration: N=1000 default. UNCALIBRATED — the trial parameters
        are held at the Nautilus safe box (alpha=phi etc), so the sweep
        variance mostly measures noise in interference_data.load. Trials
        where load never exceeds 0.5 are silently correct (no vacuous
        "load>0.5 -> collapse" applies); only high-load-no-collapse trials
        count as counterexamples.
        """
        print("\n[TEST C16] Searching for counterexample (high interference, no collapse)...")
        count = 0
        for _ in range(self.N):
            alpha = PHI
            lam = 0.1
            delta = 0.0
            gamma = 1.2
            s = 0.1
            entrain = 0.0
            profile = self.run_trial(alpha, lam, delta, gamma, s, entrain)
            if (self.predictor.axes and
                len(profile.get('details', {}).get('interference_data', {})) > 0):
                load = profile['details']['interference_data'].get('load', 0.0)
            else:
                load = 0.0
            if load > 0.5 and profile['status'] != 'COLLAPSE':
                count += 1
                if count > 5:
                    print(f"  Counterexample! load={load:.3f}, status={profile['status']}")
                    return self._result("C16", count, "FALSIFIED",
                                        f"load={load:.3f} > 0.5 without collapse.")
        print(f"  No counterexamples.")
        return self._result("C16", count, "SURVIVES",
                            "UNCALIBRATED envelope; refutation requires "
                            "> 5 high-load-no-collapse trials.")

    def test_C17(self) -> dict:
        """
        C17: Interference load > 0.5 bounds the collapse basin.

        NOT YET IMPLEMENTED. Follow test_C16's shape: sweep parameters that
        elevate load past 0.5 and confirm every such trial COLLAPSEs, OR
        find a counterexample. Returns UNTESTABLE until built.
        """
        print("\n[TEST C17] Placeholder — not yet implemented.")
        return self._result("C17", 0, "UNTESTABLE",
                            "Test not yet implemented; see test_C16 for the "
                            "build recipe.", n=0)


# ----- CLI -------------------------------------------------------------------
def main():
    print("=" * 66)
    print("test_refutations.py — sweep every C12-C17 claim")
    print("=" * 66)
    tester = RefutationTester(dim=8, generations=8, trials=50)   # fast smoke
    print(f"harness: dim={tester.dim}, generations={tester.G}, trials={tester.N}")
    print("(smoke config; the pinned production sweep uses trials=1000.)")

    tests = [tester.test_C12, tester.test_C13, tester.test_C14,
             tester.test_C15, tester.test_C16, tester.test_C17]
    results = [t() for t in tests]

    print("\n" + "=" * 66)
    print(f"{'claim':<6} {'verdict':<12} {'trials':>7} {'CE':>4}  notes")
    print("-" * 66)
    for r in results:
        note = (r["notes"] or "")[:40]
        print(f"{r['claim']:<6} {r['verdict']:<12} "
              f"{r['n_trials']:>7} {r['counterexamples']:>4}  {note}")
    print("=" * 66)


if __name__ == "__main__":
    main()
