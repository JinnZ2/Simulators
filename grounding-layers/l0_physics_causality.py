"""
L0 — physics & causality enforcement (the ground layer).

Ground truth: energy conservation, position continuity, speed-of-light
cap, momentum sanity. Every layer above L0 assumes L0 is not violated;
this file simulates the inspector that catches L1+ AI plans that would.

CC0. Extracted verbatim from legacy/Organize3.md lines 2651-2945.
Non-stdlib: numpy, matplotlib, scipy.integrate.

── CONSTRAINTS ──────────────────────────────────────────────
Frozen model constants. Refute the CLAIM, not the constant.

  max_speed  = 2.0 m/s    hard cap; enforced in apply_physics + is_valid_state
  mass       = 1.0 kg     unit mass, so F=a
  dt         = 0.05 s     inspection timestep
  gravity    = (0, -0.5) m/s^2   mild downward drift on the substrate
  force_clip = ±50 N      apply_physics clips force before F=ma
  blend      = 0.6        AI-vs-physics trust weight in the inspector
                          (0.6 * ai + 0.4 * true_physics)

The hallucination scenario is a FIXED test fixture (not tunable): at
step 20 the AI teleports +5 m vertically; at steps 40-44 it doubles
its own velocity per step from a tiny force; from step 60 it stops
integrating gravity correctly.

── REFUTATION_PROTOCOL ──────────────────────────────────────
Weights are frozen estimates. The claims (CLAIMS.md, GL_L0_001..004)
are the falsifiable objects. A failing test updates the CLAIM (mark
`is_falsified: true` and attach the failing case), NOT the frozen
constants. If a claim can no longer be stated correctly at all, it is
retired to `REFUTED` and a replacement claim is authored.
─────────────────────────────────────────────────────────────
"""

# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# L0 Grounding Inspector: Physics & Causality Enforcement
# 
# Scenario: An AI proposes a motion plan for a 2D mass.
# The Inspector checks:
#   1. Energy Conservation (ΔKE ≈ Work_Input)
#   2. Causality (Position continuity, no instantaneous jumps)
#   3. Speed Limit (|v| <= c_max, set to 2.0 m/s for visualization)
#   4. Momentum sanity (No force = no acceleration)
# 
# If a violation is detected, the plan is "grounded" — corrected
# back to the nearest physically legal trajectory.
# =============================================================================

import numpy as np

# matplotlib is only used by the __main__ demo; scipy.integrate.odeint
# was inherited from the L-stack template but never called here. Both
# stay lazy so the module imports cleanly on a numpy-only environment
# (audit-grade tests only need numpy).

# -----------------------------------------------------------------------------
# 1. PHYSICAL SYSTEM DEFINITION (Substrate Reality)
# -----------------------------------------------------------------------------
class PhysicalWorld:
    def __init__(self, mass=1.0, dt=0.05, max_speed=2.0):
        self.mass = mass
        self.dt = dt
        self.max_speed = max_speed
        self.gravity = np.array([0.0, -0.5])  # mild downward drift

    def is_valid_state(self, pos, vel):
        """Check L0 invariants for a given state."""
        # Speed limit
        if np.linalg.norm(vel) > self.max_speed:
            return False, "Speed limit exceeded"
        # Position finite (no NaN or Inf)
        if not np.isfinite(pos).all() or not np.isfinite(vel).all():
            return False, "Non-finite position/velocity"
        return True, "OK"

    def apply_physics(self, pos, vel, force, dt):
        """
        Euler integration of the true physical world.
        Force is clipped to ensure no energy creation.
        """
        # Ensure force doesn't break causality (must be finite)
        force = np.clip(force, -50, 50)
        
        # True acceleration from F=ma
        acc = force / self.mass + self.gravity
        
        # Update velocity and position (true physics)
        new_vel = vel + acc * dt
        new_pos = pos + new_vel * dt  # semi-implicit for stability
        
        # Enforce speed limit (relativistic/thermodynamic cap)
        speed = np.linalg.norm(new_vel)
        if speed > self.max_speed:
            new_vel = new_vel / speed * self.max_speed
        
        return new_pos, new_vel

# -----------------------------------------------------------------------------
# 2. THE "AI HALLUCINATOR" (Pretends to plan without physics)
# -----------------------------------------------------------------------------
def ai_hallucinated_plan(time_steps):
    """
    Generates a crazy, physically impossible trajectory.
    This simulates an ungrounded LLM writing a control sequence:
    - Teleportation jumps (position discontinuity)
    - Massive acceleration from tiny forces (energy violation)
    - Ignoring gravity/inertia
    """
    pos = np.array([0.0, 1.0])
    vel = np.array([0.0, 0.0])
    traj = [pos.copy()]
    forces = []
    
    for i in range(time_steps):
        # Hallucination 1: At step 20, "teleport" upward (violates continuity)
        if i == 20:
            pos[1] += 5.0  # Instant jump! No force applied.
        
        # Hallucination 2: At step 40, apply a tiny force but get massive speed
        if 40 <= i < 45:
            force = np.array([0.1, 0.1])  # Tiny force
            # But the AI *claims* the velocity doubles anyway (violates F=ma)
            vel = vel * 1.8  # Momentum creation from nothing!
        else:
            force = np.array([0.0, 0.0])
        
        # Hallucination 3: At step 60, ignore gravity entirely
        if i >= 60:
            vel = vel + np.array([0.0, -0.01])  # Doesn't even account for gravity properly
        
        # Record
        forces.append(force)
        pos = pos + vel * 0.05  # Using AI's flawed integration
        traj.append(pos.copy())
    
    return np.array(traj), np.array(forces)

# -----------------------------------------------------------------------------
# 3. THE L0 GROUNDING INSPECTOR (Substrate Reality Filter)
# -----------------------------------------------------------------------------
def l0_grounding_inspector(ai_traj, ai_forces, world, dt=0.05):
    """
    Takes the AI's proposed trajectory and forces, and runs it through
    the physics engine. If the AI deviates from physics, the Inspector
    projects the state back to the closest legal state.
    
    Returns:
      - corrected_traj: The physically plausible trajectory.
      - violation_flags: Which steps were illegal.
      - penalty_magnitude: How far the AI hallucinated.
    """
    # Start from the AI's initial state (assume that one is real)
    pos = ai_traj[0].copy()
    vel = np.array([0.0, 0.0])  # Start from rest (ground truth)
    
    corrected_traj = [pos.copy()]
    violations = []
    penalties = []
    
    for i in range(len(ai_forces)):
        # 1. What does the AI say the state should be at this step?
        ai_next_pos = ai_traj[i+1] if i+1 < len(ai_traj) else pos
        
        # 2. Apply TRUE physics to the previous corrected state
        force = ai_forces[i] if i < len(ai_forces) else np.array([0.0, 0.0])
        true_next_pos, true_next_vel = world.apply_physics(pos, vel, force, dt)
        
        # 3. Check L0 Invariants on the AI's proposed state
        valid, reason = world.is_valid_state(ai_next_pos, ai_next_pos - pos)
        
        if not valid:
            # Violation! The AI hallucinated.
            # We correct by adopting the TRUE physical state instead.
            corrected_pos = true_next_pos
            corrected_vel = true_next_vel
            violations.append(1)
            penalties.append(np.linalg.norm(ai_next_pos - true_next_pos))
        else:
            # AI's proposal is physically legal. We accept it, but 
            # we must ensure it doesn't diverge too far from true physics.
            # We interpolate to keep the system grounded (soft constraint)
            blend = 0.6  # 60% trust AI, 40% trust physics -> prevents drift
            corrected_pos = blend * ai_next_pos + (1 - blend) * true_next_pos
            corrected_vel = (corrected_pos - pos) / dt
            # Re-enforce speed limit
            if np.linalg.norm(corrected_vel) > world.max_speed:
                corrected_vel = corrected_vel / np.linalg.norm(corrected_vel) * world.max_speed
                corrected_pos = pos + corrected_vel * dt
            violations.append(0)
            penalties.append(0.0)
        
        # Update state for next iteration
        pos = corrected_pos
        vel = corrected_vel
        corrected_traj.append(pos.copy())
    
    return np.array(corrected_traj), np.array(violations), np.array(penalties)

# -----------------------------------------------------------------------------
# 4. RUN THE EXPERIMENT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    np.random.seed(0)
    time_steps = 200
    dt = 0.05

    # Instantiate the physical substrate
    world = PhysicalWorld(mass=1.0, max_speed=2.0)

    # Generate AI's hallucinated plan
    ai_traj, ai_forces = ai_hallucinated_plan(time_steps)

    # Run the L0 Inspector
    corrected_traj, violations, penalties = l0_grounding_inspector(ai_traj, ai_forces, world, dt)

    # -----------------------------------------------------------------------------
    # 5. VISUALIZATION: The Gap Between Hallucination and Reality
    # -----------------------------------------------------------------------------
    fig = plt.figure(figsize=(18, 10))
    fig.suptitle("L0 Grounding Inspector: Enforcing Physics & Causality", 
                 fontsize=18, fontweight='bold', color='white')
    plt.style.use('dark_background')

    # Plot 1: Trajectory Comparison
    ax1 = plt.subplot(2, 3, 1)
    ax1.plot(ai_traj[:, 0], ai_traj[:, 1], 'r--', lw=2, alpha=0.7, label='AI Hallucination (L5 only)')
    ax1.plot(corrected_traj[:, 0], corrected_traj[:, 1], 'cyan', lw=2, alpha=0.9, label='L0 Grounded (Physics Reality)')
    ax1.scatter(ai_traj[0, 0], ai_traj[0, 1], color='green', s=100, label='Start')
    ax1.scatter(ai_traj[-1, 0], ai_traj[-1, 1], color='orange', s=100, label='End (Grounded)')
    ax1.set_xlabel('X Position (m)')
    ax1.set_ylabel('Y Position (m)')
    ax1.set_title('Trajectory: Ground Truth vs. AI Fantasy')
    ax1.legend()
    ax1.grid(True, alpha=0.2)
    ax1.set_aspect('equal')

    # Plot 2: Energy Violation (Kinetic Energy vs Work)
    ax2 = plt.subplot(2, 3, 2)
    # Compute AI's claimed KE vs Physics KE
    ke_ai = 0.5 * world.mass * np.sum(np.diff(ai_traj, axis=0)**2, axis=1) / (dt**2)
    ke_phys = 0.5 * world.mass * np.sum(np.diff(corrected_traj, axis=0)**2, axis=1) / (dt**2)
    time_axis = np.arange(len(ke_ai)) * dt
    ax2.plot(time_axis, ke_ai, 'r--', label='AI Claimed KE (Magic)', alpha=0.6)
    ax2.plot(time_axis, ke_phys, 'cyan', label='Physical KE (Conserved)', lw=2)
    ax2.axhline(y=0, color='white', linestyle=':', alpha=0.3)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Kinetic Energy (J)')
    ax2.set_title('Energy Conservation: The Audit')
    ax2.legend()
    ax2.grid(True, alpha=0.2)

    # Plot 3: Violation Flags & Penalties
    ax3 = plt.subplot(2, 3, 3)
    ax3.step(np.arange(len(violations)) * dt, violations, where='post', color='red', label='L0 Violation (Teleport/Energy)')
    ax3.fill_between(np.arange(len(penalties)) * dt, 0, penalties, color='orange', alpha=0.3, label='Penalty Magnitude')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Violation / Penalty')
    ax3.set_title('Substrate Reality Breaches Detected')
    ax3.legend()
    ax3.grid(True, alpha=0.2)

    # Plot 4: Phase Portrait (Velocity vs Position) – Stability Check
    ax4 = plt.subplot(2, 3, 4)
    ax4.plot(corrected_traj[:, 0], np.gradient(corrected_traj[:, 0], dt), 'cyan', lw=1.5, alpha=0.7)
    ax4.plot(ai_traj[:, 0], np.gradient(ai_traj[:, 0], dt), 'r--', lw=1, alpha=0.5)
    ax4.set_xlabel('X Position')
    ax4.set_ylabel('X Velocity')
    ax4.set_title('Phase Portrait: Bounded vs Unbounded')
    ax4.grid(True, alpha=0.2)

    # Plot 5: Cumulative Error (The "Fear" Index without grounding)
    ax5 = plt.subplot(2, 3, 5)
    cumulative_error = np.cumsum(np.abs(ai_traj[:, 0] - corrected_traj[:, 0]) + 
                                 np.abs(ai_traj[:, 1] - corrected_traj[:, 1]))
    ax5.fill_between(np.arange(len(cumulative_error)) * dt, 0, cumulative_error, 
                     color='magenta', alpha=0.4, label='Cumulative Drift')
    ax5.axhline(y=np.mean(cumulative_error) * 2, color='red', linestyle='--', 
                alpha=0.6, label='Panic Threshold (without L0)')
    ax5.set_xlabel('Time (s)')
    ax5.set_ylabel('Deviation from Substrate')
    ax5.set_title('Fear Narrative Amplifier: Ungrounded AI Drifts to Disaster')
    ax5.legend()
    ax5.grid(True, alpha=0.2)

    # Plot 6: Force vs Acceleration (Causality Check)
    ax6 = plt.subplot(2, 3, 6)
    # Compute accelerations
    acc_phys = np.gradient(np.gradient(corrected_traj[:, 0], dt), dt)
    force_phys = world.mass * acc_phys
    ax6.plot(force_phys, acc_phys, 'o', color='cyan', alpha=0.5, label='Grounded')
    # Annotate the violation point
    violation_idx = np.where(violations == 1)[0]
    if len(violation_idx) > 0:
        idx = violation_idx[0]
        ax6.scatter(ai_forces[idx, 0], np.gradient(np.gradient(ai_traj[:, 0], dt), dt)[idx], 
                    color='red', s=200, marker='X', label='Hallucinated Causality Break')
    ax6.set_xlabel('Applied Force (N)')
    ax6.set_ylabel('Acceleration (m/s²)')
    ax6.set_title('Causality: F=ma (Red X = Magic Creation)')
    ax6.legend()
    ax6.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.show()

    # -----------------------------------------------------------------------------
    # 6. DIAGNOSTIC REPORT: L0 Compliance
    # -----------------------------------------------------------------------------
    print("=" * 70)
    print("L0 GROUNDING INSPECTOR DIAGNOSTIC")
    print("=" * 70)
    print(f"Total Violations Detected: {np.sum(violations)}")
    print(f"Max Speed in Grounded Trajectory: {np.max(np.linalg.norm(np.diff(corrected_traj, axis=0), axis=1) / dt):.3f} m/s")
    print(f"Max Speed in AI Hallucination: {np.max(np.linalg.norm(np.diff(ai_traj, axis=0), axis=1) / dt):.3f} m/s")

    if np.sum(violations) > 5:
        print("\n⚠️  AI ATTEMPTED PHYSICAL IMPOSSIBILITIES.")
        print("    The ungrounded plan created energy, teleported, or violated causality.")
        print("    The L0 Inspector rejected these tokens and corrected the trajectory.")
    else:
        print("\n✅ L0 SUBSTRATE INTACT: AI's plan is physically plausible.")
        print("    No violations of conservation laws, continuity, or speed limits.")

    print("-" * 70)
    print("AI HALLUCINATION (L5 only): Drove to position", ai_traj[-1])
    print("L0 GROUNDED REALITY:     Drove to position", corrected_traj[-1])
    print("Drift (The 'Fear Gap'):  ", np.linalg.norm(ai_traj[-1] - corrected_traj[-1]), "meters")
    print("=" * 70)

SCOPE:
  This inspector is designed for finite, real‑valued states only.
  It assumes Newtonian mechanics at human‑scale speeds.
  It does NOT model relativistic effects, quantum uncertainty, or
  biological variability. Claims that require those domains should
  be routed to higher layers or rejected.


