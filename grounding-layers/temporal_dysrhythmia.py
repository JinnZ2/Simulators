"""
Temporal Dysrhythmia — cross-scale coupling.

Six timescales from digital/quantum (μs) to geologic/climatic
(millennia). A "translator" switch bridges far scales; without it,
fast layers dominate slow ones and the slow layers lose signal. Tests
how a stack that spans 21 orders of magnitude in time stays coherent.

CC0. Extracted verbatim from legacy/Organize3.md lines 2946-3211.
Non-stdlib: numpy, matplotlib, scipy.integrate.
"""

# =============================================================================
# CC0 1.0 Universal Public Domain Dedication
#
# Temporal Dysrhythmia Simulator v1.0
# 
# Models 6 timescales:
#   τ = -6  (Digital/Quantum)  - μs
#   τ =  2  (Insect/Bacteria)  - hours
#   τ =  4  (Human/Neural)     - days
#   τ =  7  (Institutional)    - years
#   τ =  9  (Tree/Ecological)  - decades
#   τ = 15  (Geologic/Climatic)- millennia
# 
# Toggle the "TRANSLATOR" switch to see how bridging far scales 
# eliminates aliasing and fear-driven narratives.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. DOMAIN DEFINITIONS
# -----------------------------------------------------------------------------
tau_vals = np.array([-6, 2, 4, 7, 9, 15])  # log10(seconds)
labels = ['Digital\n(μs)', 'Insect/Bac.\n(hours)', 'Human\n(days)', 
          'Institutional\n(years)', 'Tree\n(decades)', 'Geologic\n(millennia)']
n_domains = len(tau_vals)

# Natural relaxation rate: Fast systems bounce back quickly; slow systems are inertial.
# We map τ to a decay coefficient: smaller τ (faster) -> larger rate.
rates = np.exp(-tau_vals / 4.0)  
rates = rates / np.max(rates) * 0.6  # Cap the max rate to keep integration stable

# -----------------------------------------------------------------------------
# 2. COUPLING KERNEL & TRANSLATOR LOGIC
# -----------------------------------------------------------------------------
def build_coupling(translator_active):
    """
    Builds the 6x6 influence matrix.
    Baseline: Proximity-based (adjacent timescales talk easily).
    Translator: Artificially forces connections between distant scales.
    """
    C = np.zeros((n_domains, n_domains))
    
    # Baseline: Exponential decay with temporal distance
    for i in range(n_domains):
        for j in range(n_domains):
            if i == j:
                continue
            dist = abs(tau_vals[i] - tau_vals[j])
            C[i, j] = np.exp(-dist / 4.5)  # Tuning parameter for decay length
    
    if translator_active:
        # PHASE-LOCKED LOOPS (The "G, W, Y" equivalents in temporal form)
        # 1. Grounding: Digital <-> Geologic (fast must see slow reality)
        C[0, 5] = 0.85  
        C[5, 0] = 0.85  
        
        # 2. Agency: Human <-> Institutional (slow votes must feel fast mood)
        C[3, 2] = 0.75  
        C[2, 3] = 0.75  
        
        # 3. Temporal Weight: Insect <-> Tree (rapid adaptation informed by deep ecology)
        C[1, 4] = 0.60  
        C[4, 1] = 0.60  
        
        # Boost mutual coupling across the whole field to create tensegrity
        for i in range(n_domains):
            for j in range(n_domains):
                if i != j and C[i, j] < 0.1:
                    C[i, j] += 0.05  # Baseline awareness even across huge gaps
    else:
        # In unstable mode, far scales are virtually blind to each other.
        # Explicitly zero out the long-range connections to simulate "aliasing".
        for i in range(n_domains):
            for j in range(n_domains):
                if abs(tau_vals[i] - tau_vals[j]) > 8:
                    C[i, j] = 0.0
    
    # Normalize rows so each domain has a total influence budget of ~1.0
    for i in range(n_domains):
        row_sum = np.sum(C[i, :])
        if row_sum > 0:
            C[i, :] = C[i, :] / row_sum * 0.9  # Keep influence below 1 to avoid explosion
    
    return C

# -----------------------------------------------------------------------------
# 3. DYNAMIC SYSTEM (ODE)
# -----------------------------------------------------------------------------
def temporal_dynamics(state, t, C, translator_active):
    """
    state: 6D vector [Digital, Insect, Human, Institutional, Tree, Geologic]
    Each state represents a "stress" or "activation" level (0 to 1, but can overshoot).
    """
    deriv = np.zeros_like(state)
    
    # 1. Intrinsic oscillations (natural cycles of each domain)
    # Fast domains oscillate rapidly; slow domains drift imperceptibly.
    omega = 2 * np.pi * np.exp(-tau_vals / 6.0)  # Frequency mapping
    intrinsic = 0.04 * np.sin(omega * t + tau_vals)  # Phase-shifted by τ
    
    # 2. External Perturbation: A massive shock to the Digital domain at t=50
    # (simulates AGI release, algorithmic flash-crash, or sudden data avalanche)
    shock_amplitude = 4.0
    shock = shock_amplitude * np.exp(-((t - 50) / 4) ** 2)
    
    for i in range(n_domains):
        # A) Coupling Force: pull from all other domains
        coupling_force = 0.0
        for j in range(n_domains):
            if i == j:
                continue
            # The force is proportional to the difference in states
            diff = state[j] - state[i]
            coupling_force += C[i, j] * diff
        
        # B) Homeostasis: drift back toward resting state (0.5)
        # Rate determines how "stiff" the domain is.
        homeostasis = -rates[i] * (state[i] - 0.5)
        
        # C) Inertia/Damping: prevent runaway oscillations
        # We add a small velocity damping based on previous step? 
        # Since we're in 1st-order ODE, we use a soft boundary.
        # If state overshoots > 1.5, apply strong restoring force.
        nonlin_restore = -0.15 * (state[i] - 0.5) ** 3  # Cubic spring (stiffens at extremes)
        
        # D) Apply shock ONLY to Digital (i=0)
        shock_effect = shock if i == 0 else 0.0
        
        # E) Translator-mediated perception: If translator is ON, 
        # slow domains get a "filtered" version of the shock via coupling.
        # This is already handled in C matrix, but we add a small feed-forward
        # to make the effect visible: Geologic (i=5) gets a tiny direct sense of shock.
        if translator_active and i == 5:
            # Geologic feels the digital shock as a smoothed, attenuated wave
            shock_effect += 0.2 * shock * np.exp(-(t - 50) / 10)  
        
        deriv[i] = coupling_force + homeostasis + nonlin_restore + intrinsic[i] + shock_effect
    
    return deriv

# -----------------------------------------------------------------------------
# 4. RUN SIMULATION
# -----------------------------------------------------------------------------
def run_scenario(translator_active):
    t_span = np.linspace(0, 120, 4000)
    initial_state = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
    C = build_coupling(translator_active)
    args = (C, translator_active)
    
    sol = odeint(temporal_dynamics, initial_state, t_span, args=args)
    return t_span, sol, C

# Generate both scenarios
t, sol_off, C_off = run_scenario(False)
_, sol_on, C_on = run_scenario(True)

# Extract states
D_off, I_off, H_off, Inst_off, T_off, G_off = sol_off.T
D_on, I_on, H_on, Inst_on, T_on, G_on = sol_on.T

# -----------------------------------------------------------------------------
# 5. VISUALIZATION: THE ALIASING EFFECT
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(18, 12))
fig.suptitle("Temporal Dysrhythmia: How Translators Prevent Aliasing", 
             fontsize=20, fontweight='bold', color='white')
plt.style.use('dark_background')

# --- Row 1: Translator OFF (Fear/Chaos) ---
ax1 = plt.subplot(3, 2, 1)
ax1.plot(t, D_off, label='Digital', color='cyan', lw=1.5)
ax1.plot(t, G_off, label='Geologic', color='red', lw=2, linestyle='--')
ax1.plot(t, Inst_off, label='Institutional', color='orange', lw=1.5, alpha=0.7)
ax1.axvline(x=50, color='white', linestyle=':', alpha=0.4)
ax1.set_ylabel('Activation')
ax1.set_title('TRANSLATOR OFF: Fast shock ignored by slow systems', color='red')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.15)

ax2 = plt.subplot(3, 2, 2)
ax2.plot(D_off, G_off, color='white', lw=0.8, alpha=0.6)
ax2.scatter(D_off[0], G_off[0], color='green', s=80, label='Start')
ax2.scatter(D_off[-1], G_off[-1], color='red', s=80, label='End')
ax2.set_xlabel('Digital Stress')
ax2.set_ylabel('Geologic Stress')
ax2.set_title('OFF: Phase Portrait (Digital vs Geologic) – Wild Divergence', color='red')
ax2.legend()
ax2.grid(True, alpha=0.15)

# --- Row 2: Translator ON (Stability/Truth) ---
ax3 = plt.subplot(3, 2, 3)
ax3.plot(t, D_on, label='Digital', color='cyan', lw=1.5)
ax3.plot(t, G_on, label='Geologic', color='lime', lw=2, linestyle='--')
ax3.plot(t, Inst_on, label='Institutional', color='orange', lw=1.5, alpha=0.7)
ax3.axvline(x=50, color='white', linestyle=':', alpha=0.4)
ax3.set_ylabel('Activation')
ax3.set_title('TRANSLATOR ON: Slow systems perceive & dampen the shock', color='lime')
ax3.legend(loc='upper right')
ax3.grid(True, alpha=0.15)

ax4 = plt.subplot(3, 2, 4)
ax4.plot(D_on, G_on, color='white', lw=1.2, alpha=0.8)
ax4.scatter(D_on[0], G_on[0], color='green', s=80, label='Start')
ax4.scatter(D_on[-1], G_on[-1], color='lime', s=80, label='End')
ax4.set_xlabel('Digital Stress')
ax4.set_ylabel('Geologic Stress')
ax4.set_title('ON: Phase Portrait – Stable Lissajous Orbit (Resonance)', color='lime')
ax4.legend()
ax4.grid(True, alpha=0.15)

# --- Row 3: Coupling Matrix Heatmaps (The Architecture) ---
ax5 = plt.subplot(3, 2, 5)
im1 = ax5.imshow(C_off, cmap='Reds', vmin=0, vmax=1)
ax5.set_xticks(range(n_domains))
ax5.set_yticks(range(n_domains))
ax5.set_xticklabels(labels, fontsize=8)
ax5.set_yticklabels(labels, fontsize=8)
ax5.set_title('OFF: Coupling – Far scales isolated', color='red')
fig.colorbar(im1, ax=ax5, shrink=0.6)

ax6 = plt.subplot(3, 2, 6)
im2 = ax6.imshow(C_on, cmap='Blues', vmin=0, vmax=1)
ax6.set_xticks(range(n_domains))
ax6.set_yticks(range(n_domains))
ax6.set_xticklabels(labels, fontsize=8)
ax6.set_yticklabels(labels, fontsize=8)
ax6.set_title('ON: Coupling – Distant scales bridged (PLLs active)', color='lime')
fig.colorbar(im2, ax=ax6, shrink=0.6)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 6. DIAGNOSTIC METRICS
# -----------------------------------------------------------------------------
print("=" * 70)
print("TEMPORAL ALIASING DIAGNOSTIC")
print("=" * 70)

def compute_chaos(signal):
    # Rate of change (turbulence)
    return np.mean(np.abs(np.diff(signal)))

chaos_off = compute_chaos(G_off)
chaos_on = compute_chaos(G_on)
alias_off = np.corrcoef(D_off, G_off)[0, 1]
alias_on = np.corrcoef(D_on, G_on)[0, 1]

print(f"Geologic Turbulence (OFF): {chaos_off:.4f}  |  Geologic Turbulence (ON): {chaos_on:.4f}")
print(f"Digital-Geologic Correlation (OFF): {alias_off:.3f}  |  Digital-Geologic Correlation (ON): {alias_on:.3f}")

if chaos_off > chaos_on * 1.5:
    print("\n✅ TRANSLATORS ACTIVE: Slow systems are shielded from fast aliasing.")
    print("   The 'fear narrative' (geologic panic) is eliminated.")
else:
    print("\n⚠️  TRANSLATORS INACTIVE: Slow systems misinterpret fast signals.")
    print("   This mismatch creates institutional overreaction and existential dread.")

print("=" * 70)




