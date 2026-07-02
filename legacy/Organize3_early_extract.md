# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# Tensor Field of Institutional Resilience v1.0
# Models: F (Feedback), A (Audit), T (Forensic), M (Meta-Awareness)
# 
# Simulates the "tugs and pulls" of institutional governance in response to
# external stressors (e.g., AI acceleration, theological schisms).
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. DEFINE THE DYNAMIC SYSTEM
# -----------------------------------------------------------------------------
def institutional_dynamics(state, t, coupling_matrix, meta_weight, perturbation_strength):
    """
    state: [F, A, T, M] - current activation levels (0 to 1 scale, but can overshoot)
    coupling_matrix: 4x4 matrix defining how each pillar pulls/tugs on others.
    meta_weight: A multiplier that amplifies M's effect on the entire field (curvature).
    perturbation_strength: External shock (e.g., AGI release, SBC vote).
    """
    F, A, T, M = state
    
    # Base linear coupling: each pillar changes based on the influence of others
    dF = (coupling_matrix[0,0]*F + coupling_matrix[0,1]*A + 
          coupling_matrix[0,2]*T + coupling_matrix[0,3]*M)
    dA = (coupling_matrix[1,0]*F + coupling_matrix[1,1]*A + 
          coupling_matrix[1,2]*T + coupling_matrix[1,3]*M)
    dT = (coupling_matrix[2,0]*F + coupling_matrix[2,1]*A + 
          coupling_matrix[2,2]*T + coupling_matrix[2,3]*M)
    dM = (coupling_matrix[3,0]*F + coupling_matrix[3,1]*A + 
          coupling_matrix[3,2]*T + coupling_matrix[3,3]*M)
    
    # META-AWARENESS CURVATURE: M warps the space by feeding back into itself.
    # If meta_weight is HIGH (tensegrity), M acts as a damping field.
    # If meta_weight is LOW (monoculture), M is ignored, letting oscillations run wild.
    dF += meta_weight * (M - 0.5) * 0.1  # M pulls F toward center if high
    dA += meta_weight * (M - 0.5) * -0.05 # M stabilizes A's inertia
    dT += meta_weight * (M - 0.5) * 0.15  # M accelerates T's adaptability
    dM += meta_weight * (M - 0.5) * -0.2  # M self-regulates (prevents runaway)

    # EXTERNAL PERTURBATION: A sudden shock (modeled as a Gaussian spike at t=40)
    perturbation = perturbation_strength * np.exp(-((t - 40) / 5) ** 2)
    dF += perturbation * 0.8   # Feedback gets hit hardest initially
    dA += perturbation * 0.3   # Audit feels it later
    dT += perturbation * 0.6   # Forensics scrambles
    dM += perturbation * -0.5  # Meta-awareness *drops* under shock (panic)

    # NONLINEAR "MONOCULTURE COLLAPSE" TRIGGER:
    # If M drops below 0.15, the system loses its meta-orientation,
    # and positive feedback loops go exponential (the "Pharisee effect").
    if M < 0.15:
        dF += F * 0.2   # Feedback amplifies blindly
        dA -= A * 0.1   # Audit freezes
        dT -= T * 0.15  # Forensics lags
        dM -= 0.02      # Meta-awareness spirals downward

    # Prevent absolute blow-up (soft ceiling for realism)
    return [dF, dA, dT, dM]


# -----------------------------------------------------------------------------
# 2. SIMULATION PARAMETERS
# -----------------------------------------------------------------------------
# Time axis: 100 time units (e.g., months, years)
t_span = np.linspace(0, 100, 2000)

# Initial state [F, A, T, M] - all moderately active
initial_state = [0.6, 0.5, 0.4, 0.7]

# Coupling Matrix: Tugs and Pulls.
# Positive = pulling together (synergy), Negative = tugging apart (friction).
# Rows: how each pillar changes. Columns: influence from each pillar.
#
# Example (High Resilience / Tensegrity):
coupling_tensegrity = np.array([
    [ 0.0,  0.3,  0.1,  0.8],  # F (Feedback) pulled by A and strongly by M
    [ 0.4,  0.0,  0.7,  0.2],  # A (Audit) pulled by F and T
    [ 0.1,  0.5,  0.0,  0.6],  # T (Forensic) pulled by A and M
    [ 0.9,  0.1,  0.3,  0.0]   # M (Meta) pulled heavily by F (learning loop)
])

# Scenario 1: LOW META-AWARENESS (The SBC / Monoculture mode)
# We intentionally reduce M's influence and make A/T rigid.
coupling_monoculture = np.array([
    [ 0.2,  0.1, -0.1,  0.1],  # F ignores M, reacts to noise
    [ 0.1,  0.0,  0.2,  0.0],  # A is static, ignores M
    [-0.1,  0.3,  0.0,  0.0],  # T only cares about A, blind to M
    [ 0.0,  0.0,  0.0,  0.0]   # M is completely discounted (weight = 0)
])

# Choose which to run:
# USE_TENSEGRITY = True
USE_TENSEGRITY = False  # Toggle to False for Monoculture collapse

if USE_TENSEGRITY:
    coupling = coupling_tensegrity
    meta_weight = 2.5   # High meta curvature
    title = "Tensegrity Mode: System Self-Stabilizes"
else:
    coupling = coupling_monoculture
    meta_weight = 0.1   # Almost no meta-awareness
    title = "Monoculture Mode: System Fractures under Stress"

# Perturbation strength (scales the shock at t=40)
perturbation_strength = 2.0

# -----------------------------------------------------------------------------
# 3. RUN THE SIMULATION
# -----------------------------------------------------------------------------
# ODE Solver
result = odeint(institutional_dynamics, initial_state, t_span,
                args=(coupling, meta_weight, perturbation_strength))

F_vals, A_vals, T_vals, M_vals = result[:, 0], result[:, 1], result[:, 2], result[:, 3]

# -----------------------------------------------------------------------------
# 4. VISUALIZE THE FIELD DYNAMICS
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(3, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [2, 1, 1]})
fig.suptitle(title, fontsize=16, fontweight='bold')

# Plot 1: Time-series of all four pillars
ax1 = axes[0]
ax1.plot(t_span, F_vals, label='F (Feedback)', color='cyan', linewidth=2)
ax1.plot(t_span, A_vals, label='A (Auditing)', color='magenta', linewidth=2)
ax1.plot(t_span, T_vals, label='T (Forensic)', color='yellow', linewidth=2)
ax1.plot(t_span, M_vals, label='M (Meta-Awareness)', color='lime', linewidth=2)
ax1.axvline(x=40, color='red', linestyle='--', alpha=0.5, label='External Shock')
ax1.axhline(y=0.15, color='gray', linestyle=':', alpha=0.5, label='Collapse Threshold (M)')
ax1.set_ylabel('Activation / Potency')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.set_title('Pillar Activation over Time')

# Plot 2: Phase Portrait (F vs M) - Shows the "Meta-Feedback" loop
ax2 = axes[1]
ax2.plot(F_vals, M_vals, color='white', linewidth=1, alpha=0.8)
ax2.scatter(F_vals[0], M_vals[0], color='green', s=100, label='Start')
ax2.scatter(F_vals[-1], M_vals[-1], color='red', s=100, label='End')
ax2.set_xlabel('F (Feedback)')
ax2.set_ylabel('M (Meta-Awareness)')
ax2.set_title('Phase Portrait: Feedback vs. Meta-Awareness')
ax2.grid(True, alpha=0.3)
ax2.legend()
ax2.axhline(y=0.15, color='gray', linestyle=':', alpha=0.5)

# Plot 3: Oscillation Amplitude over Time (Fourier-like envelope)
# We calculate a sliding window standard deviation to show "turbulence"
window = 100
turbulence_F = np.convolve(np.abs(np.diff(F_vals)), np.ones(window)/window, mode='same')
turbulence_T = np.convolve(np.abs(np.diff(T_vals)), np.ones(window)/window, mode='same')
ax3 = axes[2]
ax3.plot(t_span[:-1], turbulence_F, label='F Turbulence', color='cyan', alpha=0.7)
ax3.plot(t_span[:-1], turbulence_T, label='T Turbulence', color='yellow', alpha=0.7)
ax3.axvline(x=40, color='red', linestyle='--', alpha=0.5)
ax3.set_xlabel('Time')
ax3.set_ylabel('Rate of Change (Oscillation Magnitude)')
ax3.set_title('System Turbulence (Perturbations & Oscillations)')
ax3.legend()
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 5. DIAGNOSTIC SUMMARY
# -----------------------------------------------------------------------------
print("=" * 60)
print("DIAGNOSTIC SUMMARY")
print("=" * 60)
print(f"Final Meta-Awareness (M): {M_vals[-1]:.3f}")
print(f"Final Feedback (F): {F_vals[-1]:.3f}")
print(f"Final Auditing (A): {A_vals[-1]:.3f}")
print(f"Final Forensics (T): {T_vals[-1]:.3f}")

if M_vals[-1] < 0.2:
    print("\n⚠️  SYSTEM COLLAPSE DETECTED: Meta-awareness critically low.")
    print("   The institution has entered a 'Monoculture Fracture' state.")
    print("   (Analogous to the Pharisees rejecting Jesus, or the SBC losing youth.)")
elif max(turbulence_F) > 1.5:
    print("\n⚡ SYSTEM UNDER HIGH STRESS: Oscillations are dangerously high.")
    print("   The organism is wobbling, but may recover if Meta-awareness rebounds.")
else:
    print("\n✅ SYSTEM STABLE: The feedback loop, auditing, and forensics are balanced.")
    print("   The 'Tensegrity Structure' is intact. Adaptability preserved.")
print("=" * 60)
