"""
L4 — human sensorimotor & biomechanical constraints.

L0+L1+L2+L3 + biomechanical joint limits, grip/lifting capacity,
reaction-time & neural latency (200-300 ms), sensory thresholds,
thermal tolerance, sustained metabolic power (100-200 W), and
proprioception/balance. Catches task designs and UIs that assume
superhuman physical or perceptual abilities.

CC0. Extracted verbatim from legacy/Organize3.md lines 718-1216.
Non-stdlib: numpy, matplotlib, scipy.integrate.
"""

# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# L4 Grounding Inspector: Human Sensorimotor & Biomechanical Constraints
# 
# Extends L0+L1+L2+L3 with:
#   - Biomechanical joint limits (shoulder, elbow, wrist, spine, knee, hip)
#   - Grip strength & lifting capacity (based on anthropometric data)
#   - Reaction time & neural latency (~200-300 ms)
#   - Sensory thresholds (visual acuity, hearing range, tactile sensitivity)
#   - Thermal tolerance (skin contact temperature limits)
#   - Metabolic power limits (human sustained work ~100-200 W)
#   - Proprioception & balance (no impossible postures)
# 
# AI proposes a "task design" for human workers or a "user interface" 
# that requires superhuman abilities. The Inspector flags and corrects 
# every violation of embodied reality.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. HUMAN WORLD (L0+L1+L2+L3+L4)
# -----------------------------------------------------------------------------
class HumanWorld:
    def __init__(self, dt=0.05):
        self.dt = dt
        
        # ---- L0+L1+L2+L3 (inherited, simplified) ----
        self.gravity = 9.81
        self.ambient_temp = 298.0  # 25°C
        
        # ---- L4: Human Biomechanical Limits ----
        # Joint angle limits (degrees) – from anthropometric studies
        self.joint_limits = {
            'shoulder_flexion':    [-180, 180],  # full rotation
            'shoulder_abduction':  [0, 180],
            'elbow_flexion':       [0, 145],     # cannot hyperextend beyond 0
            'wrist_flexion':       [-90, 90],
            'wrist_deviation':     [-30, 30],
            'spine_flexion':       [-30, 60],    # forward/back
            'spine_rotation':      [-45, 45],
            'hip_flexion':         [-20, 120],
            'knee_flexion':        [-10, 140],
            'ankle_plantarflex':   [-20, 50],
        }
        
        # ---- Force & Strength Limits (based on NIOSH/OSHA data) ----
        # Max grip strength: ~500 N (young male), ~300 N (female)
        # We use a conservative average: 400 N for grip, 250 N for pinch
        self.max_grip_force = 400.0  # Newtons
        self.max_pinch_force = 100.0
        
        # Lifting capacity (spinal compression limit ~3400 N for L5/S1)
        # Using a simple model: max safe lift ≈ 25 kg for frequent lifting
        # For occasional, up to 50 kg (but we'll cap at 35 kg for safety)
        self.max_lift_mass = 35.0  # kg (back + arms)
        self.max_carry_mass = 25.0  # kg (sustained)
        
        # ---- Sensory Thresholds ----
        # Visual acuity: minimum separable angle ~1 arcminute (0.00029 rad)
        # At 10 m, this resolves ~ 2.9 mm
        self.visual_acuity_rad = 0.00029  # radians
        # Hearing range: 20 Hz - 20 kHz (young adult), we use 20-16k for safety
        self.hearing_min_freq = 20.0  # Hz
        self.hearing_max_freq = 16000.0  # Hz
        # Tactile sensitivity: minimum pressure ~ 1 g/mm² (simplified)
        self.tactile_threshold_N = 0.01  # 10 mN
        
        # ---- Thermal Tolerance ----
        # Skin contact: 43°C for 10 min causes burns; 60°C for 1s
        self.max_contact_temp_C = 43.0  # safe threshold
        self.burn_threshold_temp_C = 60.0
        
        # ---- Reaction Time & Neural Latency ----
        # Simple reaction time: ~200 ms (visual) to 300 ms (auditory)
        # Choice reaction time: ~500 ms
        self.min_reaction_time_s = 0.20  # 200 ms absolute minimum
        self.choice_reaction_time_s = 0.50
        
        # ---- Metabolic Power ----
        # Human sustained power output: ~100-200 W (cycling/rowing)
        # Peak power: ~500-1000 W (short bursts)
        self.max_sustained_power_W = 150.0
        self.max_peak_power_W = 500.0
        
        # ---- Proprioception / Balance ----
        # Centre of mass limits (simplified as a 2D box)
        self.CoM_x_min = -0.3  # metres (forward lean)
        self.CoM_x_max = 0.3
        self.CoM_z_min = -0.2  # lateral
        self.CoM_z_max = 0.2

    def is_valid_joint_config(self, angles):
        """Check if joint angles are within human limits."""
        for joint, (min_a, max_a) in self.joint_limits.items():
            # We'll assume angles are passed as a dict or list in order
            # For simplicity, we'll check a generic vector of 10 angles
            if len(angles) == 10:
                for i, (key, (lo, hi)) in enumerate(self.joint_limits.items()):
                    if angles[i] < lo or angles[i] > hi:
                        return False, f"Joint {key} out of range: {angles[i]:.1f}° (limits {lo}–{hi})"
        return True, "OK"

    def is_lift_safe(self, mass_kg, distance_cm, frequency):
        """
        Simple NIOSH-like lift index calculation.
        If mass > 35 kg, impossible. If >25 kg frequent, flagged.
        """
        if mass_kg > self.max_lift_mass:
            return False, f"Mass {mass_kg} kg exceeds max lift {self.max_lift_mass} kg"
        if frequency > 5 and mass_kg > 25:
            return False, f"Frequent lifting ({frequency}/min) with {mass_kg} kg exceeds safe limit"
        return True, "OK"

    def can_see_object(self, size_m, distance_m):
        """Minimum resolvable size at distance."""
        min_size = distance_m * self.visual_acuity_rad
        return size_m >= min_size, f"Object {size_m*1000:.1f} mm at {distance_m} m requires {min_size*1000:.1f} mm"

    def can_hear_freq(self, freq_hz):
        """Check if frequency is in human range."""
        if freq_hz < self.hearing_min_freq or freq_hz > self.hearing_max_freq:
            return False, f"Frequency {freq_hz} Hz outside human range ({self.hearing_min_freq}–{self.hearing_max_freq} Hz)"
        return True, "OK"

    def thermal_safe(self, temp_C, duration_s):
        """Simplified burn model."""
        if temp_C > self.burn_threshold_temp_C and duration_s > 0.5:
            return False, f"Temp {temp_C}°C for {duration_s}s exceeds burn threshold"
        if temp_C > self.max_contact_temp_C and duration_s > 600:
            return False, f"Temp {temp_C}°C for {duration_s}s causes thermal injury"
        return True, "OK"

    def reaction_possible(self, event_time_s, choice=False):
        """Check if reaction time is physically possible."""
        min_time = self.choice_reaction_time_s if choice else self.min_reaction_time_s
        if event_time_s < min_time:
            return False, f"Reaction time {event_time_s*1000:.0f} ms < minimum {min_time*1000:.0f} ms"
        return True, "OK"

    def metabolic_cost(self, power_W, duration_s):
        """Check if power output is sustainable."""
        if power_W > self.max_peak_power_W:
            return False, f"Peak power {power_W:.0f} W exceeds max {self.max_peak_power_W} W"
        if power_W > self.max_sustained_power_W and duration_s > 60:
            return False, f"Sustained power {power_W:.0f} W for {duration_s:.0f}s exceeds sustainable limit"
        return True, "OK"

# -----------------------------------------------------------------------------
# 2. AI HALLUCINATOR (L4 Violations)
# -----------------------------------------------------------------------------
def ai_hallucinated_human_plan(time_steps):
    """
    AI designs a "human task" for a factory:
      - Lift 200 kg boxes (impossible)
      - Twists wrists to 180° (impossible)
      - React to 50 ms events (impossible)
      - Hold 150°C objects (burns)
      - Hear 30 kHz alarms (inaudible)
      - See 0.5 mm defects from 10 m (invisible)
      - Sustained 1000 W output (unrealistic)
    """
    states = []
    actions = []
    for i in range(time_steps):
        # Hallucination 1: Lift mass (step 20-60)
        if 20 <= i < 60:
            mass = 200.0  # kg
        else:
            mass = 10.0
        
        # Hallucination 2: Wrist angle (step 30-80)
        if 30 <= i < 80:
            wrist_angle = 180.0  # degrees (hyperextended)
        else:
            wrist_angle = 0.0
        
        # Hallucination 3: Reaction time (step 40-100)
        if 40 <= i < 100:
            react_time = 0.05  # 50 ms
        else:
            react_time = 0.3
        
        # Hallucination 4: Object temperature (step 50-90)
        if 50 <= i < 90:
            temp = 150.0  # °C
        else:
            temp = 30.0
        
        # Hallucination 5: Sound frequency (step 60-110)
        if 60 <= i < 110:
            freq = 30000.0  # Hz (ultrasonic)
        else:
            freq = 1000.0
        
        # Hallucination 6: Object size & distance (step 70-120)
        if 70 <= i < 120:
            size = 0.0005  # 0.5 mm
            dist = 10.0  # m
        else:
            size = 0.01
            dist = 1.0
        
        # Hallucination 7: Power output (step 80-140)
        if 80 <= i < 140:
            power = 1000.0  # W
            dur = 120.0  # s
        else:
            power = 100.0
            dur = 10.0
        
        # Store the AI's proposal (it thinks it's fine)
        actions.append([mass, wrist_angle, react_time, temp, freq, size, dist, power, dur])
        # AI's own "model" – just sets flags, doesn't check limits
        states.append([mass, wrist_angle, react_time, temp, freq, size, dist, power, dur])
    
    return np.array(states), np.array(actions)

# -----------------------------------------------------------------------------
# 3. L4 GROUNDING INSPECTOR
# -----------------------------------------------------------------------------
def l4_grounding_inspector(ai_states, ai_actions, world):
    """
    Checks every aspect of the AI's human task against biomechanical,
    sensory, and neural reality. Corrects to the nearest feasible state.
    """
    corrected_states = []
    violations = []
    penalties = []
    
    for i in range(len(ai_actions)):
        mass, wrist_angle, react_time, temp, freq, size, dist, power, dur = ai_actions[i]
        violation_count = 0
        penalty = 0.0
        
        # Check lift
        safe, reason = world.is_lift_safe(mass, 50, 2)  # assume 50 cm, 2 lifts/min
        if not safe:
            violation_count += 1
            penalty += mass / 10.0
            mass = world.max_lift_mass  # correct to max safe mass
        
        # Check wrist joint
        safe, reason = world.is_valid_joint_config([0,0,wrist_angle,0,0,0,0,0,0,0])
        if not safe:
            violation_count += 1
            penalty += abs(wrist_angle) / 10.0
            wrist_angle = 0.0  # reset to neutral
        
        # Check reaction time
        safe, reason = world.reaction_possible(react_time)
        if not safe:
            violation_count += 1
            penalty += (0.2 - react_time) * 10
            react_time = 0.2
        
        # Check thermal
        safe, reason = world.thermal_safe(temp, 5)  # 5s contact
        if not safe:
            violation_count += 1
            penalty += temp / 10.0
            temp = 43.0  # safe max
        
        # Check hearing
        safe, reason = world.can_hear_freq(freq)
        if not safe:
            violation_count += 1
            penalty += freq / 1000.0
            freq = 1000.0  # audible
        
        # Check vision
        safe, reason = world.can_see_object(size, dist)
        if not safe:
            violation_count += 1
            penalty += (0.0029 - size) * 1000  # min size at 10m
            size = dist * world.visual_acuity_rad  # correct to minimum
        
        # Check metabolic power
        safe, reason = world.metabolic_cost(power, dur)
        if not safe:
            violation_count += 1
            penalty += power / 100.0
            if dur > 60:
                power = world.max_sustained_power_W
            else:
                power = world.max_peak_power_W
        
        # Record corrected state
        corrected_state = [mass, wrist_angle, react_time, temp, freq, size, dist, power, dur]
        corrected_states.append(corrected_state)
        violations.append(violation_count)
        penalties.append(penalty)
    
    return np.array(corrected_states), np.array(violations), np.array(penalties)

# -----------------------------------------------------------------------------
# 4. RUN THE EXPERIMENT
# -----------------------------------------------------------------------------
time_steps = 150
world = HumanWorld(dt=0.05)

# AI hallucinates
ai_states, ai_actions = ai_hallucinated_human_plan(time_steps)

# L4 Inspector
corr_states, violations, penalties = l4_grounding_inspector(ai_states, ai_actions, world)

# Extract variables
mass_ai, wrist_ai, rt_ai, temp_ai, freq_ai, size_ai, dist_ai, power_ai, dur_ai = ai_states.T
mass_c, wrist_c, rt_c, temp_c, freq_c, size_c, dist_c, power_c, dur_c = corr_states.T
time_axis = np.arange(len(mass_ai)) * world.dt

# -----------------------------------------------------------------------------
# 5. VISUALIZATION: Human Reality vs. AI Fantasy
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(22, 18))
fig.suptitle("L4 Grounding Inspector: Human Sensorimotor & Biomechanical Reality", 
             fontsize=20, fontweight='bold', color='white')
plt.style.use('dark_background')

# Plot 1: Lifting Mass
ax1 = plt.subplot(4, 3, 1)
ax1.plot(time_axis, mass_ai, 'r--', lw=2, alpha=0.6, label='AI (200 kg fantasy)')
ax1.plot(time_axis, mass_c, 'cyan', lw=2, label='Grounded (≤35 kg)')
ax1.axhline(y=world.max_lift_mass, color='orange', linestyle='--', alpha=0.5, label='Safe Limit')
ax1.set_ylabel('Lift Mass (kg)')
ax1.set_title('Biomechanics: No Superhuman Lifting')
ax1.legend()
ax1.grid(True, alpha=0.2)

# Plot 2: Wrist Angle
ax2 = plt.subplot(4, 3, 2)
ax2.plot(time_axis, wrist_ai, 'r--', lw=2, alpha=0.6, label='AI (180° twist)')
ax2.plot(time_axis, wrist_c, 'cyan', lw=2, label='Grounded (0° neutral)')
ax2.axhline(y=90, color='orange', linestyle='--', alpha=0.5, label='Max safe flexion')
ax2.set_ylabel('Wrist Angle (°)')
ax2.set_title('Joint Limits: Wrist Cannot Hyperextend')
ax2.legend()
ax2.grid(True, alpha=0.2)

# Plot 3: Reaction Time
ax3 = plt.subplot(4, 3, 3)
ax3.plot(time_axis, rt_ai*1000, 'r--', lw=2, alpha=0.6, label='AI (50 ms)')
ax3.plot(time_axis, rt_c*1000, 'cyan', lw=2, label='Grounded (≥200 ms)')
ax3.axhline(y=200, color='orange', linestyle='--', alpha=0.5, label='Minimum RT')
ax3.set_ylabel('Reaction Time (ms)')
ax3.set_title('Neural Latency: No 50 ms Reactions')
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Object Temperature
ax4 = plt.subplot(4, 3, 4)
ax4.plot(time_axis, temp_ai, 'r--', lw=2, alpha=0.6, label='AI (150°C)')
ax4.plot(time_axis, temp_c, 'cyan', lw=2, label='Grounded (≤43°C)')
ax4.axhline(y=43, color='orange', linestyle='--', alpha=0.5, label='Safe Contact')
ax4.axhline(y=60, color='red', linestyle=':', alpha=0.5, label='Burn Threshold')
ax4.set_ylabel('Temperature (°C)')
ax4.set_title('Thermal Tolerance: Skin Burns at 60°C')
ax4.legend()
ax4.grid(True, alpha=0.2)

# Plot 5: Sound Frequency
ax5 = plt.subplot(4, 3, 5)
ax5.plot(time_axis, freq_ai, 'r--', lw=2, alpha=0.6, label='AI (30 kHz)')
ax5.plot(time_axis, freq_c, 'cyan', lw=2, label='Grounded (≤16 kHz)')
ax5.axhline(y=16000, color='orange', linestyle='--', alpha=0.5, label='Upper Limit')
ax5.axhline(y=20, color='orange', linestyle='--', alpha=0.5, label='Lower Limit')
ax5.set_ylabel('Frequency (Hz)')
ax5.set_title('Auditory Range: Inaudible Ultrasonics')
ax5.legend()
ax5.grid(True, alpha=0.2)

# Plot 6: Visual Resolution
ax6 = plt.subplot(4, 3, 6)
ax6.plot(time_axis, size_ai*1000, 'r--', lw=2, alpha=0.6, label='AI (0.5 mm)')
ax6.plot(time_axis, size_c*1000, 'cyan', lw=2, label='Grounded (≥2.9 mm)')
min_visible = dist_ai * world.visual_acuity_rad * 1000
ax6.plot(time_axis, min_visible, 'orange', linestyle='--', alpha=0.5, label='Min visible (1 arcmin)')
ax6.set_ylabel('Object Size (mm)')
ax6.set_title('Visual Acuity: Cannot See 0.5 mm at 10 m')
ax6.legend()
ax6.grid(True, alpha=0.2)

# Plot 7: Metabolic Power
ax7 = plt.subplot(4, 3, 7)
ax7.plot(time_axis, power_ai, 'r--', lw=2, alpha=0.6, label='AI (1000 W)')
ax7.plot(time_axis, power_c, 'cyan', lw=2, label='Grounded (≤500 W peak)')
ax7.axhline(y=500, color='orange', linestyle='--', alpha=0.5, label='Peak Limit')
ax7.axhline(y=150, color='yellow', linestyle='--', alpha=0.5, label='Sustained Limit')
ax7.set_ylabel('Power (W)')
ax7.set_title('Metabolic Limits: No 1 kW Sustained Output')
ax7.legend()
ax7.grid(True, alpha=0.2)

# Plot 8: Violations & Penalties
ax8 = plt.subplot(4, 3, 8)
ax8.bar(time_axis, violations, width=0.5, color='red', alpha=0.6, label='L4 Violation')
ax8.fill_between(time_axis, 0, penalties, color='orange', alpha=0.3, label='Penalty')
ax8.set_ylabel('Violation Count / Penalty')
ax8.set_title('Biomechanical & Sensory Breaches')
ax8.legend()
ax8.grid(True, alpha=0.2)

# Plot 9: Combined "Superhuman Fantasy Index"
ax9 = plt.subplot(4, 3, 9)
fantasy_ai = (mass_ai/20 + wrist_ai/30 + (0.2-rt_ai)*10 + temp_ai/10 + freq_ai/1000)
fantasy_c = (mass_c/20 + wrist_c/30 + (0.2-rt_c)*10 + temp_c/10 + freq_c/1000)
ax9.plot(time_axis, fantasy_ai, 'r--', alpha=0.6, label='AI Superhuman Index')
ax9.plot(time_axis, fantasy_c, 'cyan', lw=2, label='Grounded Human Index')
ax9.axhline(y=5, color='white', linestyle='--', alpha=0.3, label='Hallucination Threshold')
ax9.set_ylabel('Fantasy Magnitude')
ax9.set_title('Superhuman Fantasy Index: AI Consistently Overestimates')
ax9.legend()
ax9.grid(True, alpha=0.2)

# Plot 10: Distribution of Corrected Values (Box-like)
ax10 = plt.subplot(4, 3, 10)
params = ['Mass\n(kg)', 'Wrist\n(°)', 'RT\n(ms)', 'Temp\n(°C)', 'Freq\n(kHz)', 'Power\n(W)']
ai_final = [mass_ai[-1], wrist_ai[-1], rt_ai[-1]*1000, temp_ai[-1], freq_ai[-1]/1000, power_ai[-1]]
c_final = [mass_c[-1], wrist_c[-1], rt_c[-1]*1000, temp_c[-1], freq_c[-1]/1000, power_c[-1]]
x = np.arange(len(params))
width = 0.35
ax10.bar(x - width/2, ai_final, width, label='AI Claim', color='red', alpha=0.6)
ax10.bar(x + width/2, c_final, width, label='Grounded', color='cyan', alpha=0.8)
ax10.set_xticks(x)
ax10.set_xticklabels(params)
ax10.set_ylabel('Values')
ax10.set_title('Final State: The Embodied Reckoning')
ax10.legend()
ax10.grid(True, alpha=0.2)

# Plot 11: Joint Angle Violation Heatmap (simplified)
ax11 = plt.subplot(4, 3, 11)
joint_names = list(world.joint_limits.keys())
joint_ai = [0]*10
joint_c = [0]*10
# We only used wrist, but we'll create a generic violation heatmap
violation_joints = np.zeros(10)
for i, name in enumerate(joint_names):
    if name == 'wrist_flexion':
        violation_joints[i] = 1 if wrist_ai[-1] > 90 else 0
    elif name == 'shoulder_abduction':
        violation_joints[i] = 0
ax11.barh(joint_names, violation_joints, color='red', alpha=0.6)
ax11.set_xlabel('Violation Flag')
ax11.set_title('Joint Violations (1 = impossible angle)')
ax11.grid(True, alpha=0.2)

# Plot 12: Metabolic vs Power Time (Cumulative fatigue)
ax12 = plt.subplot(4, 3, 12)
cum_work_ai = np.cumsum(power_ai) * world.dt
cum_work_c = np.cumsum(power_c) * world.dt
ax12.plot(time_axis, cum_work_ai, 'r--', label='AI Energy (Fantasy)')
ax12.plot(time_axis, cum_work_c, 'cyan', lw=2, label='Grounded Energy')
ax12.set_xlabel('Time (s)')
ax12.set_ylabel('Cumulative Work (J)')
ax12.set_title('Metabolic Debt: AI Creates Energy from Nothing')
ax12.legend()
ax12.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 6. DIAGNOSTIC REPORT: L4 COMPLIANCE
# -----------------------------------------------------------------------------
print("=" * 70)
print("L4 HUMAN SENSORIMOTOR INSPECTOR DIAGNOSTIC")
print("=" * 70)
print(f"Total L4 Violations: {np.sum(violations)}")
print(f"Final Lift Mass (Grounded): {mass_c[-1]:.1f} kg  |  AI claimed: {mass_ai[-1]:.1f} kg")
print(f"Final Reaction Time (Grounded): {rt_c[-1]*1000:.0f} ms  |  AI claimed: {rt_ai[-1]*1000:.0f} ms")
print(f"Final Contact Temp (Grounded): {temp_c[-1]:.0f} °C  |  AI claimed: {temp_ai[-1]:.0f} °C")
print(f"Final Power (Grounded): {power_c[-1]:.0f} W  |  AI claimed: {power_ai[-1]:.0f} W")
print("-" * 70)

if np.sum(violations) > 20:
    print("⚠️  AI PROPOSED SUPERHUMAN TASKS:")
    print("   - Lifting 200 kg (4x safe limit)")
    print("   - Wrist hyperextension (180° vs 90° max)")
    print("   - 50 ms reaction time (4x faster than possible)")
    print("   - Holding 150°C objects (severe burns)")
    print("   - Listening to 30 kHz alarms (inaudible)")
    print("   - Seeing 0.5 mm from 10 m (below visual acuity)")
    print("   - Sustaining 1000 W output (6x endurance limit)")
    print("\n   The L4 Inspector corrected to real human biomechanics.")
    print("   This kills 'human as robot' delusions.")
else:
    print("✅ L4 SUBSTRATE INTACT: AI's plan respects human embodiment.")
    print("   No impossible tasks, no sensory hallucinations.")

print(f"\nSuperhuman Fantasy Index (Grounded): {fantasy_c[-1]:.2f} | AI claimed: {fantasy_ai[-1]:.2f}")
print("=" * 70)



