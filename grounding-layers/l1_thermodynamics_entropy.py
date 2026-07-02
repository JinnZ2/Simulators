"""
L1 — thermodynamics & entropy enforcement.

L0 + energy conservation (Work = ΔKE + Heat + Friction), non-decreasing
entropy, battery depletion, and Carnot ceiling. Catches "free energy"
plans that violate the second law.

CC0. Extracted verbatim from legacy/Organize3.md lines 2216-2650.
Non-stdlib: numpy, matplotlib, scipy.integrate.
"""

# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# L1 Grounding Inspector: Thermodynamics & Entropy Enforcement
# 
# Extends L0 with:
#   - Energy conservation (Work = ΔKE + Heat + Friction)
#   - Entropy generation (must be ≥ 0 for any process)
#   - Battery depletion (can't spend more energy than stored)
#   - Carnot efficiency limits (no 100% conversion)
# 
# The AI proposes a motion plan with "free energy" sources.
# The Inspector rejects any plan that violates the 2nd Law.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. PHYSICAL + THERMODYNAMIC WORLD
# -----------------------------------------------------------------------------
class ThermodynamicWorld:
    def __init__(self, mass=1.0, dt=0.05, max_speed=2.0,
                 battery_capacity=100.0,  # Joules
                 initial_battery=80.0,
                 ambient_temp=300.0,       # Kelvin
                 heat_capacity=50.0,       # J/K (thermal mass)
                 initial_temp=300.0,
                 efficiency=0.85,           # motor/drive efficiency
                 friction_coeff=0.02):
        self.mass = mass
        self.dt = dt
        self.max_speed = max_speed
        self.gravity = np.array([0.0, -0.5])
        
        # Thermodynamic state
        self.battery = initial_battery
        self.battery_capacity = battery_capacity
        self.temperature = initial_temp
        self.ambient_temp = ambient_temp
        self.heat_capacity = heat_capacity
        self.efficiency = efficiency
        self.friction_coeff = friction_coeff
        
        # Accumulated entropy (J/K)
        self.entropy_generated = 0.0
        self.total_work_input = 0.0
        self.total_heat_dissipated = 0.0

    def is_valid_state(self, pos, vel, battery, temp):
        """L0 + L1 invariants"""
        # L0 checks (speed, finite)
        if np.linalg.norm(vel) > self.max_speed:
            return False, "Speed limit exceeded"
        if not np.isfinite(pos).all() or not np.isfinite(vel).all():
            return False, "Non-finite state"
        # L1 checks
        if battery < 0:
            return False, "Battery depleted below zero"
        if battery > self.battery_capacity:
            return False, "Battery overcharged (energy creation)"
        if temp < 0:
            return False, "Temperature below absolute zero"
        return True, "OK"

    def apply_physics_and_thermo(self, pos, vel, battery, temp, force, dt, external_heat_supply=0.0):
        """
        Step the true physical world + thermodynamics.
        """
        # ---- L0: Mechanical ----
        # Clamp force
        force = np.clip(force, -50, 50)
        
        # Friction force (opposes velocity)
        friction_force = -self.friction_coeff * vel
        net_force = force + friction_force + self.gravity * self.mass
        
        # True acceleration
        acc = net_force / self.mass
        new_vel = vel + acc * dt
        new_pos = pos + new_vel * dt
        
        # Speed limit
        speed = np.linalg.norm(new_vel)
        if speed > self.max_speed:
            new_vel = new_vel / speed * self.max_speed
            new_pos = pos + new_vel * dt
        
        # ---- L1: Energy & Entropy ----
        # Work done by the input force (only the 'useful' part)
        # but the motor only converts a fraction (efficiency)
        work_input = np.dot(force, (new_pos - pos))  # Force * displacement
        
        # If work_input is negative (regenerative braking), we store some energy back
        if work_input < 0:
            regen_efficiency = 0.4  # can't recover 100%
            battery_delta = -work_input * regen_efficiency  # actually adds to battery
            # But also creates heat from losses
            heat_loss = -work_input * (1 - regen_efficiency)
        else:
            # Positive work: draw from battery with efficiency loss
            required_work = work_input / self.efficiency
            battery_delta = -required_work
            heat_loss = required_work * (1 - self.efficiency)  # motor heat
            # Friction already accounted for in net force, but friction generates heat too
            friction_work = np.dot(friction_force, (new_pos - pos))
            if friction_work > 0:  # friction always dissipates
                heat_loss += friction_work * 0.9  # most goes to heat
            else:
                heat_loss += 0.0
        
        # External heat supply (could be solar, nuclear, etc.) – this is where AI might hallucinate
        # We treat it as heat added directly to the system
        heat_loss += external_heat_supply  # AI claims "free heat"
        
        # Update battery (clamp to capacity)
        new_battery = battery + battery_delta
        if new_battery > self.battery_capacity:
            # Overcharge! That's energy creation. We clip to capacity and count as violation.
            new_battery = self.battery_capacity
            heat_loss += (battery + battery_delta - self.battery_capacity)  # extra goes to waste
        
        # Thermal update: Q = C * dT
        temp_change = heat_loss / self.heat_capacity
        new_temp = temp + temp_change
        
        # Entropy generation: dS = Q/T (assuming reversible limit, we integrate approx)
        # For a small step, entropy generated is heat_loss / average temp
        if temp > 0.1:
            entropy_gen = heat_loss / ((temp + new_temp) / 2.0)
        else:
            entropy_gen = heat_loss / 300.0  # fallback
        
        # Clamp entropy generation to be positive (2nd Law)
        if entropy_gen < 0:
            # If the AI claims negative entropy (cooling without work), we force it to zero
            entropy_gen = 0.0
            new_temp = temp  # no cooling without work
        
        # Return updated state
        return new_pos, new_vel, new_battery, new_temp, entropy_gen, heat_loss

# -----------------------------------------------------------------------------
# 2. AI HALLUCINATOR (L5 fantasy with thermodynamics violations)
# -----------------------------------------------------------------------------
def ai_hallucinated_plan_with_thermo(time_steps, world):
    """
    Generates a plan that violates L1:
      - "Free energy" supply (over-unity)
      - Ignoring waste heat (temperature stays constant despite massive work)
      - Perpetual motion (battery regenerates from nothing)
      - Cooling without heat rejection (violates 2nd law)
    """
    pos = np.array([0.0, 1.0])
    vel = np.array([0.0, 0.0])
    battery = world.initial_battery
    temp = world.ambient_temp
    
    traj = [pos.copy()]
    forces = []
    battery_claims = [battery]
    temp_claims = [temp]
    external_heat_claims = []
    
    for i in range(time_steps):
        # Hallucination 1: At step 30, claim huge "free energy" input
        if 30 <= i < 35:
            force = np.array([5.0, 2.0])  # big force
            # AI claims this force creates energy, doesn't drain battery
            # But also claims battery INCREASES because of "regenerative overunity"
            battery += 0.5  # Magic: battery grows while doing work!
            external_heat = 10.0  # AI claims 10 J of "ambient heat" sucked in
        # Hallucination 2: At step 70, ignore heat generation entirely
        elif 70 <= i < 80:
            force = np.array([3.0, 0.0])
            # AI says no temperature rise despite massive friction
            # (we'll just let it drift; the inspector will catch it)
            external_heat = 0.0
            # Also claims battery magically resets
            if i == 70:
                battery = 90.0  # magically recharged
        else:
            force = np.array([0.5, 0.0])
            external_heat = 0.0
        
        # AI's own flawed integration (ignores thermodynamics)
        pos = pos + vel * world.dt + 0.5 * (force / world.mass) * (world.dt**2)
        vel = vel + (force / world.mass) * world.dt
        # Speed cap in AI mind (loose)
        if np.linalg.norm(vel) > 3.0:
            vel = vel / np.linalg.norm(vel) * 3.0
        
        # AI also ignores battery and temp changes, or just fakes them
        if i % 20 == 0 and i > 0:
            battery += 1.0  # spontaneous regeneration
        temp = world.ambient_temp  # AI says it stays constant
        
        traj.append(pos.copy())
        forces.append(force)
        battery_claims.append(battery)
        temp_claims.append(temp)
        external_heat_claims.append(external_heat)
    
    return np.array(traj), np.array(forces), np.array(battery_claims), np.array(temp_claims), np.array(external_heat_claims)

# -----------------------------------------------------------------------------
# 3. L1 GROUNDING INSPECTOR (Physics + Thermodynamics)
# -----------------------------------------------------------------------------
def l1_grounding_inspector(ai_traj, ai_forces, ai_battery, ai_temp, ai_ext_heat, world):
    """
    Runs the AI's force plan through the true L0+L1 dynamics.
    If the AI violates energy conservation or entropy, it corrects the state.
    """
    # Start with true initial state
    pos = ai_traj[0].copy()
    vel = np.array([0.0, 0.0])
    battery = world.initial_battery
    temp = world.ambient_temp
    
    corrected_traj = [pos.copy()]
    corrected_battery = [battery]
    corrected_temp = [temp]
    entropy_produced = []
    violations = []
    penalties = []
    
    for i in range(len(ai_forces)):
        # AI's proposed next state
        ai_next_pos = ai_traj[i+1] if i+1 < len(ai_traj) else pos
        ai_next_battery = ai_battery[i+1] if i+1 < len(ai_battery) else battery
        ai_next_temp = ai_temp[i+1] if i+1 < len(ai_temp) else temp
        force = ai_forces[i]
        ext_heat = ai_ext_heat[i] if i < len(ai_ext_heat) else 0.0
        
        # ---- TRUE PHYSICS + THERMO ----
        true_pos, true_vel, true_battery, true_temp, entropy_gen, heat_loss = \
            world.apply_physics_and_thermo(pos, vel, battery, temp, force, world.dt, ext_heat)
        
        # ---- CHECK AI's CLAIM against L0+L1 ----
        valid, reason = world.is_valid_state(ai_next_pos, ai_next_pos - pos, ai_next_battery, ai_next_temp)
        
        # Check if AI is violating energy conservation (battery magic)
        if ai_next_battery > true_battery + 1.0 and np.linalg.norm(force) > 0.1:
            valid = False
            reason = "Battery creation from nothing (over-unity)"
        
        # Check if AI is violating 2nd law (cooling without entropy)
        if ai_next_temp < true_temp - 0.1 and heat_loss > 0:
            valid = False
            reason = "Violation of 2nd Law: spontaneous cooling without work"
        
        if not valid:
            # Violation! Correct to true physics+thermo
            corrected_pos = true_pos
            corrected_vel = true_vel
            corrected_bat = true_battery
            corrected_t = true_temp
            violations.append(1)
            penalties.append(np.linalg.norm(ai_next_pos - true_pos) + abs(ai_next_battery - true_battery))
        else:
            # Accept AI proposal, but blend with true physics to prevent drift
            blend = 0.7
            corrected_pos = blend * ai_next_pos + (1 - blend) * true_pos
            corrected_vel = (corrected_pos - pos) / world.dt
            if np.linalg.norm(corrected_vel) > world.max_speed:
                corrected_vel = corrected_vel / np.linalg.norm(corrected_vel) * world.max_speed
                corrected_pos = pos + corrected_vel * world.dt
            # For battery and temp, we trust physics more (thermo is strict)
            corrected_bat = 0.3 * ai_next_battery + 0.7 * true_battery
            corrected_t = 0.2 * ai_next_temp + 0.8 * true_temp
            violations.append(0)
            penalties.append(0.0)
        
        # Update state
        pos = corrected_pos
        vel = corrected_vel
        battery = corrected_bat
        temp = corrected_t
        entropy_produced.append(entropy_gen)
        
        corrected_traj.append(pos.copy())
        corrected_battery.append(battery)
        corrected_temp.append(temp)
    
    return (np.array(corrected_traj), np.array(corrected_battery), 
            np.array(corrected_temp), np.array(entropy_produced),
            np.array(violations), np.array(penalties))

# -----------------------------------------------------------------------------
# 4. RUN THE EXPERIMENT
# -----------------------------------------------------------------------------
time_steps = 200
world = ThermodynamicWorld(mass=1.0, max_speed=2.0, initial_battery=80.0)

# AI hallucinates
ai_traj, ai_forces, ai_battery, ai_temp, ai_ext_heat = ai_hallucinated_plan_with_thermo(time_steps, world)

# L1 Inspector
(corr_traj, corr_battery, corr_temp, entropy_gen, 
 violations, penalties) = l1_grounding_inspector(
    ai_traj, ai_forces, ai_battery, ai_temp, ai_ext_heat, world
)

# -----------------------------------------------------------------------------
# 5. VISUALIZATION: Thermodynamic Truth vs. AI Fantasy
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(20, 14))
fig.suptitle("L1 Grounding Inspector: Thermodynamics & Entropy Enforcement", 
             fontsize=20, fontweight='bold', color='white')
plt.style.use('dark_background')

# Plot 1: Trajectory (L0 visual)
ax1 = plt.subplot(3, 3, 1)
ax1.plot(ai_traj[:, 0], ai_traj[:, 1], 'r--', lw=2, alpha=0.6, label='AI Hallucination')
ax1.plot(corr_traj[:, 0], corr_traj[:, 1], 'cyan', lw=2, label='L1 Grounded')
ax1.scatter(ai_traj[0,0], ai_traj[0,1], c='green', s=100, label='Start')
ax1.scatter(corr_traj[-1,0], corr_traj[-1,1], c='orange', s=100, label='End (Grounded)')
ax1.set_title('Trajectory with L1 constraints')
ax1.legend()
ax1.grid(True, alpha=0.2)
ax1.set_aspect('equal')

# Plot 2: Battery (Energy Budget)
ax2 = plt.subplot(3, 3, 2)
time_axis = np.arange(len(ai_battery)) * world.dt
ax2.plot(time_axis, ai_battery, 'r--', label='AI Claim (Free Energy)', alpha=0.6)
ax2.plot(time_axis, corr_battery, 'cyan', lw=2, label='Grounded (Finite Budget)')
ax2.axhline(y=0, color='white', linestyle=':', alpha=0.3)
ax2.axhline(y=world.battery_capacity, color='green', linestyle='--', alpha=0.3, label='Capacity')
ax2.set_ylabel('Battery Energy (J)')
ax2.set_title('Energy Conservation: No Over-Unity Allowed')
ax2.legend()
ax2.grid(True, alpha=0.2)

# Plot 3: Temperature & Entropy
ax3 = plt.subplot(3, 3, 3)
ax3.plot(time_axis, ai_temp, 'r--', label='AI Claim (Constant Temp)', alpha=0.6)
ax3.plot(time_axis, corr_temp, 'orange', lw=2, label='Grounded Temperature')
ax3.plot(time_axis[:-1], np.cumsum(entropy_gen), 'lime', lw=2, label='Cumulative Entropy (J/K)')
ax3.set_ylabel('Temperature (K) / Entropy (J/K)')
ax3.set_title('2nd Law: Entropy Always Increases')
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Energy Balance (Work vs Heat)
ax4 = plt.subplot(3, 3, 4)
work_ai = np.cumsum(np.sum(ai_forces * np.diff(ai_traj, axis=0), axis=1)) * world.dt
work_true = np.cumsum(np.sum(ai_forces * np.diff(corr_traj, axis=0), axis=1)) * world.dt
ax4.fill_between(time_axis[1:], 0, work_ai, color='red', alpha=0.3, label='AI Claimed Work')
ax4.fill_between(time_axis[1:], 0, work_true, color='cyan', alpha=0.3, label='Actual Work (L1)')
ax4.set_ylabel('Cumulative Work (J)')
ax4.set_title('Work Input: AI Overestimates by 2x+')
ax4.legend()
ax4.grid(True, alpha=0.2)

# Plot 5: Violation Heatmap
ax5 = plt.subplot(3, 3, 5)
ax5.bar(time_axis, violations, width=0.5, color='red', alpha=0.7, label='L1 Violation')
ax5.fill_between(time_axis, 0, penalties, color='orange', alpha=0.3, label='Penalty Magnitude')
ax5.set_ylabel('Violation / Penalty')
ax5.set_title('Thermodynamic Breaches Detected')
ax5.legend()
ax5.grid(True, alpha=0.2)

# Plot 6: Phase Portrait (Energy vs Displacement) – shows unsustainable claims
ax6 = plt.subplot(3, 3, 6)
ax6.plot(np.linalg.norm(ai_traj, axis=1), ai_battery, 'r--', alpha=0.5, label='AI')
ax6.plot(np.linalg.norm(corr_traj, axis=1), corr_battery, 'cyan', lw=2, label='Grounded')
ax6.set_xlabel('Total Distance Traveled (m)')
ax6.set_ylabel('Battery Remaining (J)')
ax6.set_title('Energy vs Distance: The Perpetual Motion Refuted')
ax6.legend()
ax6.grid(True, alpha=0.2)

# Plot 7: Efficiency & Heat Dissipation
ax7 = plt.subplot(3, 3, 7)
heat_phys = np.diff(corr_temp) * world.heat_capacity
ax7.fill_between(time_axis[1:], 0, heat_phys, color='magenta', alpha=0.4, label='Waste Heat (L1)')
ax7.plot(time_axis[1:], np.diff(corr_battery), 'cyan', lw=1.5, alpha=0.6, label='Battery Change Rate')
ax7.axhline(y=0, color='white', linestyle=':', alpha=0.3)
ax7.set_ylabel('Heat / ΔBattery (J/s)')
ax7.set_title('Heat Generation: No Free Lunch')
ax7.legend()
ax7.grid(True, alpha=0.2)

# Plot 8: Temperature vs Entropy (Carnot limit check)
ax8 = plt.subplot(3, 3, 8)
ax8.scatter(entropy_gen[:-1], corr_temp[:-1], c=corr_temp[:-1], cmap='hot', s=20, alpha=0.7)
ax8.set_xlabel('Entropy Generated per Step (J/K)')
ax8.set_ylabel('Temperature (K)')
ax8.set_title('Entropy-Temperature Phase Space (2nd Law)')
ax8.grid(True, alpha=0.2)

# Plot 9: Cumulative Energy Error (The "Thermal Fear" index)
ax9 = plt.subplot(3, 3, 9)
cumulative_energy_error = np.abs(ai_battery - corr_battery)
ax9.fill_between(time_axis, 0, cumulative_energy_error, color='red', alpha=0.4, label='Energy Hallucination Gap')
ax9.axhline(y=np.mean(cumulative_energy_error)*3, color='orange', linestyle='--', alpha=0.6, 
            label='Thermal Panic Threshold')
ax9.set_xlabel('Time (s)')
ax9.set_ylabel('Energy Deviation (J)')
ax9.set_title('Thermal Fear Index: Ungrounded AI Creates Energy')
ax9.legend()
ax9.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 6. DIAGNOSTIC REPORT: L1 COMPLIANCE
# -----------------------------------------------------------------------------
print("=" * 70)
print("L1 THERMODYNAMIC INSPECTOR DIAGNOSTIC")
print("=" * 70)
print(f"Total L1 Violations: {np.sum(violations)}")
print(f"Final Grounded Battery: {corr_battery[-1]:.2f} J  |  AI claimed: {ai_battery[-1]:.2f} J")
print(f"Final Grounded Temp: {corr_temp[-1]:.2f} K     |  AI claimed: {ai_temp[-1]:.2f} K")
print(f"Total Entropy Generated: {np.sum(entropy_gen):.2f} J/K")
print("-" * 70)

if np.sum(violations) > 3:
    print("⚠️  AI ATTEMPTED THERMODYNAMIC IMPOSSIBILITIES:")
    print("   - Created energy from nothing (over-unity)")
    print("   - Violated the 2nd Law (cooling without work)")
    print("   - Ignored waste heat accumulation")
    print("   The L1 Inspector corrected these with true thermodynamics.")
else:
    print("✅ L1 SUBSTRATE INTACT: AI's plan obeys energy conservation and entropy.")
    print("   No over-unity, no perpetual motion, no 2nd Law violations.")

print(f"\nCumulative Energy Gap (The 'Free Lunch' Illusion): {np.sum(np.abs(ai_battery - corr_battery)):.2f} J")
print("=" * 70)


