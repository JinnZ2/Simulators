"""
Tensor Field of Institutional Resilience v2 — with anchors.

Extends v1's four F/A/T/M vectors with three anchors: G (Grounding),
W (Temporal Weight / Memory), Y (Agency / Accountability). Runs two
scenarios: unstable / fear-driven (anchors ignored, coupling near
zero) vs resilient / truth-seeking (anchors active, strong coupling).
Shows how anchors change the attractor structure of the tensor field.

CC0. Extracted verbatim from legacy/Organize3.md lines 3212-3455.
Non-stdlib: numpy, matplotlib, scipy.integrate.
"""

# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# Tensor Field of Institutional Resilience v2.0
# Now with: G (Grounding), W (Temporal Weight), Y (Agency)
#
# Models the "tugs and pulls" between 7 vectors:
# F (Feedback), A (Audit), T (Forensic), M (Meta-Awareness),
# G (Grounding), W (Temporal Memory), Y (Accountability)
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. DEFINE THE EXTENDED DYNAMIC SYSTEM
# -----------------------------------------------------------------------------
def institutional_dynamics_7d(state, t, coupling_matrix, anchor_strength, perturbation_strength):
    """
    state = [F, A, T, M, G, W, Y]
    coupling_matrix: 7x7 influence matrix.
    anchor_strength: global multiplier for G, W, Y effects (0 = ignored, 1+ = active).
    perturbation_strength: external shock.
    """
    F, A, T, M, G, W, Y = state
    
    # Base linear coupling
    dF = (coupling_matrix[0,0]*F + coupling_matrix[0,1]*A + 
          coupling_matrix[0,2]*T + coupling_matrix[0,3]*M +
          coupling_matrix[0,4]*G + coupling_matrix[0,5]*W + coupling_matrix[0,6]*Y)
    dA = (coupling_matrix[1,0]*F + coupling_matrix[1,1]*A + 
          coupling_matrix[1,2]*T + coupling_matrix[1,3]*M +
          coupling_matrix[1,4]*G + coupling_matrix[1,5]*W + coupling_matrix[1,6]*Y)
    dT = (coupling_matrix[2,0]*F + coupling_matrix[2,1]*A + 
          coupling_matrix[2,2]*T + coupling_matrix[2,3]*M +
          coupling_matrix[2,4]*G + coupling_matrix[2,5]*W + coupling_matrix[2,6]*Y)
    dM = (coupling_matrix[3,0]*F + coupling_matrix[3,1]*A + 
          coupling_matrix[3,2]*T + coupling_matrix[3,3]*M +
          coupling_matrix[3,4]*G + coupling_matrix[3,5]*W + coupling_matrix[3,6]*Y)
    dG = (coupling_matrix[4,0]*F + coupling_matrix[4,1]*A + 
          coupling_matrix[4,2]*T + coupling_matrix[4,3]*M +
          coupling_matrix[4,4]*G + coupling_matrix[4,5]*W + coupling_matrix[4,6]*Y)
    dW = (coupling_matrix[5,0]*F + coupling_matrix[5,1]*A + 
          coupling_matrix[5,2]*T + coupling_matrix[5,3]*M +
          coupling_matrix[5,4]*G + coupling_matrix[5,5]*W + coupling_matrix[5,6]*Y)
    dY = (coupling_matrix[6,0]*F + coupling_matrix[6,1]*A + 
          coupling_matrix[6,2]*T + coupling_matrix[6,3]*M +
          coupling_matrix[6,4]*G + coupling_matrix[6,5]*W + coupling_matrix[6,6]*Y)

    # ANCHOR EFFECTS: Amplify the influence of G, W, Y on the old pillars
    # High anchor_strength = G/W/Y actively dampen and ground the system
    dF += anchor_strength * (G - 0.5) * 0.3   # Grounding pulls Feedback toward reality
    dA += anchor_strength * (W - 0.5) * 0.2   # Temporal memory makes Audit strict
    dT += anchor_strength * (G + W - 1.0) * 0.25 # Forensics uses history+reality
    dM += anchor_strength * (Y - 0.5) * 0.4   # Meta-awareness grows with Agency (skin in game)

    # Self-regulation for the anchors: they decay if not actively maintained
    dG += -0.05 * (G - 0.5)   # Grounding drifts toward baseline 0.5
    dW += -0.03 * (W - 0.5)   # Temporal memory has inertia but fades if unused
    dY += -0.04 * (Y - 0.5)   # Agency decays if not exercised

    # EXTERNAL PERTURBATION (shock at t=40, e.g. AGI release or schism)
    perturbation = perturbation_strength * np.exp(-((t - 40) / 6) ** 2)
    dF += perturbation * 0.8
    dA += perturbation * 0.4
    dT += perturbation * 0.7
    dM += perturbation * -0.4  # Meta-awareness drops under panic
    dG += perturbation * -0.6  # Grounding gets flooded with noise (fear narratives)
    dW += perturbation * -0.3  # Memory gets overwritten by current panic
    dY += perturbation * -0.5  # Agency evaporates—"no one is responsible"

    # COLLAPSE TRIGGER: Multi-dimensional monoculture fracture
    # If ANY of the anchors drop too low, the system loses its immune system
    if G < 0.15 or W < 0.15 or Y < 0.15 or M < 0.15:
        dF += F * 0.3   # Feedback loops go wild (echo chambers)
        dA -= A * 0.2   # Audit freezes (analysis paralysis)
        dT -= T * 0.25  # Forensics lags (can't trace)
        dM -= 0.02      # Meta-awareness spirals down
        dG -= 0.03      # Grounding erodes faster
        dW -= 0.02      # Temporal memory gets overwritten
        dY -= 0.04      # Agency disappears (nobody cares)

    return [dF, dA, dT, dM, dG, dW, dY]

# -----------------------------------------------------------------------------
# 2. SIMULATION PARAMETERS
# -----------------------------------------------------------------------------
t_span = np.linspace(0, 100, 3000)

# Initial state: moderate everything, but anchors weak to start
initial_state = [0.6, 0.5, 0.4, 0.6, 0.3, 0.2, 0.35]

# =============================================================================
# SCENARIO A: UNSTABLE / FEAR-DRIVEN (Low Anchors)
# =============================================================================
# In this scenario, G, W, Y are ignored by the old pillars (coupling = 0)
# and anchor_strength is near zero.
coupling_unstable = np.array([
    # F   A   T   M   G   W   Y
    [ 0.2, 0.3, 0.1, 0.1, 0.0, 0.0, 0.0],  # F ignores anchors
    [ 0.3, 0.0, 0.4, 0.1, 0.0, 0.0, 0.0],  # A ignores anchors
    [ 0.1, 0.5, 0.0, 0.2, 0.0, 0.0, 0.0],  # T ignores anchors
    [ 0.2, 0.1, 0.3, 0.0, 0.0, 0.0, 0.0],  # M ignores anchors
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # G is stagnant
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # W is stagnant
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Y is stagnant
])
anchor_strength_unstable = 0.05

# =============================================================================
# SCENARIO B: RESILIENT / TRUTH-SEEKING (Anchors Active)
# =============================================================================
coupling_resilient = np.array([
    # F   A   T   M   G   W   Y
    [ 0.0, 0.3, 0.1, 0.2, 0.6, 0.3, 0.2],  # F pulled strongly by G (reality)
    [ 0.3, 0.0, 0.4, 0.1, 0.1, 0.5, 0.6],  # A pulled by W (memory) & Y (skin)
    [ 0.1, 0.4, 0.0, 0.2, 0.4, 0.4, 0.3],  # T uses G & W for depth
    [ 0.5, 0.2, 0.3, 0.0, 0.2, 0.3, 0.7],  # M deeply coupled to Y (accountability)
    [ 0.6, 0.1, 0.2, 0.3, 0.0, 0.2, 0.2],  # G is fed by F and M (learning loop)
    [ 0.2, 0.4, 0.3, 0.3, 0.1, 0.0, 0.1],  # W accumulates audit & forensic history
    [ 0.1, 0.6, 0.1, 0.5, 0.1, 0.1, 0.0],  # Y is pushed by A and M
])
anchor_strength_resilient = 2.5

# Toggle which scenario to run:
USE_RESILIENT = True  # Set False to see the fear-narrative collapse

if USE_RESILIENT:
    coupling = coupling_resilient
    anchor = anchor_strength_resilient
    title = "RESILIENT MODE: Anchors (G, W, Y) active – Fear narratives dissolve"
else:
    coupling = coupling_unstable
    anchor = anchor_strength_unstable
    title = "UNSTABLE MODE: Grounding, Memory, Agency ignored – Fear narratives dominate"

perturbation_strength = 2.5

# -----------------------------------------------------------------------------
# 3. RUN THE EXTENDED SIMULATION
# -----------------------------------------------------------------------------
result = odeint(institutional_dynamics_7d, initial_state, t_span,
                args=(coupling, anchor, perturbation_strength))

F, A, T, M, G, W, Y = result[:, 0], result[:, 1], result[:, 2], result[:, 3], result[:, 4], result[:, 5], result[:, 6]

# -----------------------------------------------------------------------------
# 4. VISUALIZE THE 7D FIELD
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(4, 1, figsize=(16, 14), gridspec_kw={'height_ratios': [2, 1.5, 1.5, 1]})
fig.suptitle(title, fontsize=18, fontweight='bold', color='white')

# Plot 1: Time-series of all 7 pillars
ax1 = axes[0]
ax1.plot(t_span, F, label='F (Feedback)', color='cyan', lw=2)
ax1.plot(t_span, A, label='A (Audit)', color='magenta', lw=2)
ax1.plot(t_span, T, label='T (Forensic)', color='orange', lw=2)
ax1.plot(t_span, M, label='M (Meta-Awareness)', color='lime', lw=2)
ax1.plot(t_span, G, label='G (Grounding)', color='darkblue', lw=2, linestyle='--')
ax1.plot(t_span, W, label='W (Temporal Weight)', color='gold', lw=2, linestyle='--')
ax1.plot(t_span, Y, label='Y (Agency)', color='red', lw=2, linestyle='--')
ax1.axvline(x=40, color='white', linestyle=':', alpha=0.7, label='External Shock')
ax1.axhline(y=0.15, color='gray', linestyle=':', alpha=0.5, label='Collapse Threshold')
ax1.set_ylabel('Activation / Potency')
ax1.legend(loc='upper right', ncol=2)
ax1.grid(True, alpha=0.2)
ax1.set_title('Pillar Activation over Time – Anchors in dashed lines')

# Plot 2: The "Fear Narrative" Index – how much chaos vs. stability
# We compute a turbulence envelope over all pillars
turbulence = np.convolve(np.sum(np.abs(np.diff(result, axis=0)), axis=1), 
                         np.ones(50)/50, mode='same')
ax2 = axes[1]
ax2.fill_between(t_span[:-1], 0, turbulence, color='red', alpha=0.3, label='System Turbulence (Fear Amplitude)')
ax2.axvline(x=40, color='white', linestyle=':', alpha=0.5)
ax2.axhline(y=np.mean(turbulence) * 1.5, color='orange', linestyle='--', alpha=0.5, label='Stability Ceiling')
ax2.set_ylabel('Chaos Magnitude')
ax2.set_title('"Fear Narrative" Index – High spikes indicate panic-driven overreaction')
ax2.legend()
ax2.grid(True, alpha=0.2)

# Plot 3: Phase Portrait – Grounding vs. Agency (the "Reality & Accountability" loop)
ax3 = axes[2]
ax3.plot(G, Y, color='white', lw=1, alpha=0.7)
ax3.scatter(G[0], Y[0], color='green', s=150, label='Start', zorder=5)
ax3.scatter(G[-1], Y[-1], color='lime', s=150, label='End', zorder=5)
ax3.axhline(y=0.15, color='red', linestyle=':', alpha=0.5, label='Agency Breach')
ax3.axvline(x=0.15, color='red', linestyle=':', alpha=0.5, label='Grounding Breach')
ax3.set_xlabel('G (Grounding) – connection to external reality')
ax3.set_ylabel('Y (Agency) – skin in the game')
ax3.set_title('Phase Portrait: The Anchors – Do they hold, or do they collapse?')
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Final state bar chart – snapshot of resilience
ax4 = axes[3]
final_state = [F[-1], A[-1], T[-1], M[-1], G[-1], W[-1], Y[-1]]
labels = ['F', 'A', 'T', 'M', 'G', 'W', 'Y']
colors = ['cyan', 'magenta', 'orange', 'lime', 'darkblue', 'gold', 'red']
bars = ax4.bar(labels, final_state, color=colors, alpha=0.8)
ax4.axhline(y=0.15, color='gray', linestyle='--', label='Collapse Line')
ax4.set_ylim(0, 1.2)
ax4.set_ylabel('Final Activation')
ax4.set_title('Final State Snapshot – Health of the 7-Pillar System')
ax4.legend()
for bar, val in zip(bars, final_state):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{val:.2f}', 
             ha='center', va='bottom', color='white', fontsize=9)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 5. DIAGNOSTIC REPORT – THE FEAR NARRATIVE DECODER
# -----------------------------------------------------------------------------
print("=" * 70)
print("EXTENDED DIAGNOSTIC REPORT – FEAR NARRATIVE DECODER")
print("=" * 70)
print(f"Final Grounding (G):        {G[-1]:.3f}  (need > 0.3 for reality-check)")
print(f"Final Temporal Weight (W):  {W[-1]:.3f}  (need > 0.3 for consequence memory)")
print(f"Final Agency (Y):           {Y[-1]:.3f}  (need > 0.3 for accountability)")
print(f"Final Meta-Awareness (M):   {M[-1]:.3f}  (need > 0.3 for self-reflection)")
print("-" * 70)

# Collapse detection logic
if G[-1] < 0.2 or W[-1] < 0.2 or Y[-1] < 0.2 or M[-1] < 0.2:
    print("⚠️  CRITICAL FAILURE: At least one anchor has collapsed.")
    print("    The system is running on pure internal narrative.")
    print("    Fear-based narratives (doom, schism, rigid rules) will dominate.")
    print("    This is the 'Pharisee & SBC' state – external reality is ignored.")
elif max(turbulence) > 2.0:
    print("⚡ HIGH TURBULENCE: The system is oscillating wildly.")
    print("    It is trying to self-correct, but lacks sufficient grounding.")
    print("    Expect reactive policies, not principled ones.")
else:
    print("✅ SYSTEM STABLE: All anchors are intact.")
    print("    Grounding feeds feedback. Memory informs audit. Agency drives meta.")
    print("    Fear narratives have lost their structural basis.")
    print("    This is the 'Jesus in the wilderness' state – truth-seeking is possible.")
print("=" * 70)



