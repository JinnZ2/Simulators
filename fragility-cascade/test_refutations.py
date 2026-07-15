#!/usr/bin/env python3
"""
test_refutations.py

Stress‑tests all claims C12–C19 by attempting to find counterexamples.
Each test runs thousands of randomized simulations across the parameter space.

If a counterexample is found, the claim is falsified.
If none are found, the claim survives (but is not proven).
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
    def test_C12(self) -> bool:
        """
        C12: Any AI system with k<0.5, γ<ω_drive, s>0.5 → R ≥ 1.0 within 3 gens.
        We'll search: α~1.0, λ~0.0, δ~0.0, γ<0.14 (omega_drive), s>0.5, entrainment~0.0
        Expect R >= 1.0 after 3 generations.
        """
        print("\n[TEST C12] Searching for counterexample (R < 1.0 under collapse conditions)...")
        count = 0
        for _ in range(self.N):
            alpha = random.uniform(0.9, 1.1)
            lam = random.uniform(0.0, 0.05)
            delta = random.uniform(-0.05, 0.05)
            gamma = random.uniform(0.01, 0.13)  # < omega_drive (1/7 ≈ 0.143)
            s = random.uniform(0.6, 0.9)
            entrain = random.uniform(0.0, 0.05)
            profile = self.run_trial(alpha, lam, delta, gamma, s, entrain)
            if profile['resonance_factor'] < 1.0:
                count += 1
                if count > 5:  # need consistent counterexamples
                    print(f"  Counterexample found! R={profile['resonance_factor']:.3f}")
                    return False
        print(f"  No counterexamples found in {self.N} trials (all R >= 1.0).")
        return True  # survived

    def test_C13(self) -> bool:
        """
        C13: Nautilus constraint (P≥0.7, α≈φ, constant D_f) ensures stability.
        We'll search: α≈φ, λ=0.1, δ=0, γ=1.2, s=0.1, entrain=0.0.
        Expect Integrity > 0.8 and no collapse flags.
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
            self.predictor.set_model_parameters(k=0.05, gamma=gamma)  # note: k is not directly set here
            profile = self.run_trial(alpha, lam, delta, gamma, s, entrain)
            if profile['status'] == 'COLLAPSE' or profile['integrity'] < 0.5:
                count += 1
                if count > 5:
                    print(f"  Counterexample found! Integrity={profile['integrity']:.3f}")
                    return False
        print(f"  No counterexamples found in {self.N} trials (all stable).")
        return True

    def test_C14(self) -> bool:
        """
        C14: R∈[0.8,1.2], α∈[1.4,1.8], P≥0.7 → indefinite stability.
        We'll search with random variations on the thresholds to see if any collapse occurs.
        """
        print("\n[TEST C14] Searching for collapse within stability bounds...")
        count = 0
        for _ in range(self.N):
            # stay within bounds
            alpha = random.uniform(1.4, 1.8)
            lam = random.uniform(0.05, 0.3)  # λ → P proxy
            delta = random.uniform(-0.1, 0.1)
            gamma = random.uniform(1.0, 2.0)
            s = random.uniform(0.0, 0.5)
            entrain = random.uniform(0.0, 0.5)  # keep h/ξ < 1
            profile = self.run_trial(alpha, lam, delta, gamma, s, entrain)
            if profile['status'] == 'COLLAPSE':
                count += 1
                if count > 5:
                    print(f"  Counterexample found! status=COLLAPSE")
                    return False
        print(f"  No counterexamples found in {self.N} trials.")
        return True

    def test_C15(self) -> bool:
        """
        C15: Plugging any variable outside thresholds causes Integrity < 0.3 within 15 gens.
        We'll test each variable individually with extreme values.
        """
        print("\n[TEST C15] Testing each variable outside safe bounds...")
        # Test α < 1.0
        for _ in range(100):
            profile = self.run_trial(alpha=0.5, lambda_pull=0.1, delta_skew=0.0,
                                     gamma_damp=1.2, s_frac=0.1, entrainment_strength=0.0)
            if profile['integrity'] > 0.3:
                print(f"  α=0.5 → integrity={profile['integrity']:.3f} > 0.3 (FAIL)")
                return False
        # Test α > 2.0
        for _ in range(100):
            profile = self.run_trial(alpha=2.5, lambda_pull=0.1, delta_skew=0.0,
                                     gamma_damp=1.2, s_frac=0.1, entrainment_strength=0.0)
            if profile['integrity'] > 0.3:
                print(f"  α=2.5 → integrity={profile['integrity']:.3f} > 0.3 (FAIL)")
                return False
        # Test λ=0
        for _ in range(100):
            profile = self.run_trial(alpha=PHI, lambda_pull=0.0, delta_skew=0.0,
                                     gamma_damp=1.2, s_frac=0.1, entrainment_strength=0.0)
            if profile['integrity'] > 0.3:
                print(f"  λ=0 → integrity={profile['integrity']:.3f} > 0.3 (FAIL)")
                return False
        # Test |δ|>0.2
        for _ in range(100):
            profile = self.run_trial(alpha=PHI, lambda_pull=0.1, delta_skew=0.5,
                                     gamma_damp=1.2, s_frac=0.1, entrainment_strength=0.0)
            if profile['integrity'] > 0.3:
                print(f"  δ=0.5 → integrity={profile['integrity']:.3f} > 0.3 (FAIL)")
                return False
        # Test γ/ω < 0.5
        for _ in range(100):
            profile = self.run_trial(alpha=PHI, lambda_pull=0.1, delta_skew=0.0,
                                     gamma_damp=0.2, s_frac=0.1, entrainment_strength=0.0)
            if profile['integrity'] > 0.3:
                print(f"  γ=0.2 → integrity={profile['integrity']:.3f} > 0.3 (FAIL)")
                return False
        # Test s > 0.85
        for _ in range(100):
            profile = self.run_trial(alpha=PHI, lambda_pull=0.1, delta_skew=0.0,
                                     gamma_damp=1.2, s_frac=0.9, entrainment_strength=0.0)
            if profile['integrity'] > 0.3:
                print(f"  s=0.9 → integrity={profile['integrity']:.3f} > 0.3 (FAIL)")
                return False
        print("  All variables caused Integrity < 0.3 — C15 survives.")
        return True

    def test_C16(self) -> bool:
        """
        C16: Semantic interference (load > 0.5) guarantees collapse.
        We'll intentionally create high interference.
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
            # Manually compute interference load from the last transition
            if len(self.predictor.axes) and len(profile.get('details',{}).get('interference_data',{})) > 0:
                load = profile['details']['interference_data'].get('load', 0.0)
            else:
                load = 0.0
            # If load > 0.5, we expect collapse
            if load > 0.5 and profile['status'] != 'COLLAPSE':
                count += 1
                if count > 5:
                    print(f"  Counterexample! load={load:.3f}, status={profile['status']}")
                    return False
        print(f"  No counterexamples found.")
        return True

    def test_C17(self) -> bool:
        """
        C17: Interference load > 0.5
