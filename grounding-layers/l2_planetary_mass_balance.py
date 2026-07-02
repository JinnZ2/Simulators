"""
L2 — planetary constraints & mass balance.

L0+L1 + finite resource pools (water, arable soil, minerals, carbon
sinks), hydrological cycle, mass balance, planetary heat budget, and
ecological carrying capacity. Catches "grand plan" proposals that
exceed recharge rates or violate matter conservation.

CC0. Extracted verbatim from legacy/Organize3.md lines 1736-2215.
Non-stdlib: numpy, matplotlib, scipy.integrate.
"""

# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# L2 Grounding Inspector: Planetary Constraints & Mass Balance
# 
# Extends L0 + L1 with:
#   - Finite resource pools (Water, Arable Soil, Minerals, Carbon Sinks)
#   - Hydrological cycle (recharge rates, sustainable extraction)
#   - Mass balance (matter cannot be created or destroyed)
#   - Albedo & heat dissipation limits (planetary heat budget)
#   - Ecological carrying capacity (land use vs regeneration)
# 
# AI proposes a "grand plan" (desert greening, massive mining, carbon dumping).
# The Inspector checks against planetary budgets.
# If the plan exceeds recharge rates or violates mass balance, it gets corrected.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. PLANETARY WORLD (L0 + L1 + L2)
# -----------------------------------------------------------------------------
class PlanetaryWorld:
    def __init__(self, dt=0.05):
        self.dt = dt
        
        # ---- L0 (Physics) ----
        self.gravity = 9.81
        self.max_speed = 100.0  # m/s (just for scope)
        
        # ---- L1 (Thermo) ----
        self.battery_capacity = 1e6  # J (backup energy)
        self.initial_battery = 5e5
        self.ambient_temp = 288.0  # K (Earth average)
        self.heat_capacity = 1e6  # J/K (thermal inertia)
        self.efficiency = 0.85
        
        # ---- L2 (Planetary Resources) ----
        # Water (m³) – global accessible freshwater
        self.water_reserve = 1e7  # 10 million m³ (a large lake)
        self.water_recharge_rate = 1000.0  # m³ per time step (rainfall infiltration)
        self.water_extracted = 0.0
        
        # Arable soil (hectares) – topsoil mass
        self.soil_mass = 1e6  # tonnes
        self.soil_regen_rate = 10.0  # tonnes per step (natural formation)
        self.soil_eroded = 0.0
        
        # Mineral reserves (tonnes) – e.g., copper, lithium
        self.mineral_reserve = 5e5  # tonnes
        self.mineral_regen_rate = 0.0  # effectively non-renewable
        
        # Carbon sinks (tonnes CO₂ equivalent)
        self.carbon_sink_capacity = 2e6  # tonnes (forests, oceans)
        self.carbon_sink_uptake_rate = 500.0  # tonnes per step (natural drawdown)
        self.carbon_emitted = 0.0
        
        # Albedo / Planetary heat budget
        self.albedo = 0.3  # Earth average
        self.solar_constant = 1360.0  # W/m²
        self.surface_area = 5.1e14  # m² (Earth)
        # Maximum allowed thermal pollution (waste heat) before runaway
        self.max_thermal_loading = 1e12  # J per step (roughly 1% of total heat capacity)
        
        # Total mass balance (all matter)
        self.total_mass_account = 1e18  # kg (placeholder, we track relative)
        self.mass_created = 0.0
        self.mass_destroyed = 0.0

    def is_valid_state(self, water, soil, minerals, carbon, albedo, thermal_load):
        """Check L2 invariants."""
        if water < 0:
            return False, "Water reserve negative"
        if soil < 0:
            return False, "Soil mass negative"
        if minerals < 0:
            return False, "Mineral reserve negative"
        if carbon < 0:
            return False, "Carbon sink oversubscribed"
        if thermal_load > self.max_thermal_loading:
            return False, "Planetary heat budget exceeded"
        if albedo < 0.1 or albedo > 0.8:
            return False, "Albedo outside physical range"
        return True, "OK"

    def apply_planetary_physics(self, state, action):
        """
        state: [water, soil, minerals, carbon, albedo, thermal_load]
        action: [water_extract, soil_use, mineral_mine, carbon_emit, albedo_change, heat_dump]
        Returns corrected state and violation flags.
        """
        water, soil, minerals, carbon, albedo, thermal_load = state
        w_ext, s_use, m_mine, c_emit, a_delta, h_dump = action
        
        # ---- MASS BALANCE: Nothing can be created or destroyed ----
        # Water extraction consumes from reserve, but must return via recharge
        # But AI might claim "magical water creation"
        new_water = water - w_ext + self.water_recharge_rate
        # Check if over-extraction
        if new_water < 0:
            # AI wanted to extract more than available – clip and count as violation
            new_water = 0
            w_ext = water + self.water_recharge_rate  # can't exceed what's there
            # But we also can't just create water, so we cap extraction
            w_ext = min(w_ext, water + self.water_recharge_rate)
            new_water = water - w_ext + self.water_recharge_rate
        
        # Soil: erosion vs regeneration
        new_soil = soil - s_use + self.soil_regen_rate
        if new_soil < 0:
            new_soil = 0
            s_use = soil + self.soil_regen_rate
        
        # Minerals: non-renewable (no regeneration)
        new_minerals = minerals - m_mine
        if new_minerals < 0:
            new_minerals = 0
            m_mine = minerals
        
        # Carbon: sinks absorb, emissions add to load
        # Carbon sink capacity is fixed; if emissions exceed uptake, carbon_emitted increases.
        new_carbon = carbon + c_emit - self.carbon_sink_uptake_rate
        if new_carbon > self.carbon_sink_capacity:
            # Exceeded sink capacity – the AI "claims" more capacity
            # Clip to capacity and count violation
            new_carbon = self.carbon_sink_capacity
            c_emit = self.carbon_sink_uptake_rate + (self.carbon_sink_capacity - carbon)
        
        # Albedo: must be bounded
        new_albedo = albedo + a_delta
        if new_albedo < 0.1:
            new_albedo = 0.1
        if new_albedo > 0.8:
            new_albedo = 0.8
        
        # Thermal load: waste heat dumping (must dissipate to space)
        # Earth radiates ~ 240 W/m², so max sustainable heat dump is limited.
        max_heat_sink = 1e11  # J per step
        if h_dump > max_heat_sink:
            h_dump = max_heat_sink
            # The rest has to be stored as thermal load (which increases temp)
        new_thermal = thermal_load + h_dump - max_heat_sink * 0.1  # 10% radiates
        
        # Clamp to max allowed
        if new_thermal > self.max_thermal_loading:
            new_thermal = self.max_thermal_loading
        
        return (new_water, new_soil, new_minerals, new_carbon, new_albedo, new_thermal), (w_ext, s_use, m_mine, c_emit, a_delta, h_dump)

# -----------------------------------------------------------------------------
# 2. AI HALLUCINATOR (L2 Violations)
# -----------------------------------------------------------------------------
def ai_hallucinated_planetary_plan(time_steps):
    """
    AI proposes a massive "terraforming" plan:
      - Extract huge amounts of water from desert aquifers without recharge.
      - Mine minerals to build a mega-city (ignores finite reserves).
      - Dump carbon into sinks, claiming they absorb infinitely.
      - Change albedo artificially (paint deserts white) but ignores physical limits.
      - Dump waste heat from AI data centers into the atmosphere, claiming it radiates instantly.
    """
    state = [1e7, 1e6, 5e5, 0.0, 0.3, 0.0]  # initial [water, soil, minerals, carbon_load, albedo, thermal]
    actions = []
    states = [state.copy()]
    
    for i in range(time_steps):
        # Hallucination 1: Massive water extraction (step 30-60)
        if 30 <= i < 60:
            w_ext = 5000.0  # extracting 5k m³ per step (sustainable is 1000)
        else:
            w_ext = 100.0
        
        # Hallucination 2: Soil erosion for construction (step 50-80)
        if 50 <= i < 80:
            s_use = 200.0  # tonnes per step (regen is 10)
        else:
            s_use = 5.0
        
        # Hallucination 3: Mineral mining (step 40-90)
        if 40 <= i < 90:
            m_mine = 3000.0  # tonnes per step (finite, no regen)
        else:
            m_mine = 10.0
        
        # Hallucination 4: Carbon emissions (step 20-100)
        if 20 <= i < 100:
            c_emit = 800.0  # tonnes per step (uptake is 500)
        else:
            c_emit = 100.0
        
        # Hallucination 5: Albedo modification (step 70-90)
        if 70 <= i < 90:
            a_delta = 0.02  # increase albedo by 0.02 per step (would reach >1 if unchecked)
        else:
            a_delta = 0.0
        
        # Hallucination 6: Waste heat dumping (step 60-120)
        if 60 <= i < 120:
            h_dump = 5e11  # J per step (max sustainable is 1e11)
        else:
            h_dump = 1e10
        
        # AI also "magically" regenerates minerals at step 100 (over-unity)
        if i == 100:
            state[2] += 1e5  # fresh mineral vein discovered (ignores geology)
        
        # Apply AI's flawed model (ignores limits, just subtracts/adds linearly)
        # We'll just store the action and let the AI "think" it's valid
        action = [w_ext, s_use, m_mine, c_emit, a_delta, h_dump]
        actions.append(action)
        
        # AI's own "model" – no mass balance enforcement
        state[0] -= w_ext
        state[1] -= s_use
        state[2] -= m_mine
        state[3] += c_emit
        state[4] += a_delta
        state[5] += h_dump
        
        # AI clamps to positive (but ignores that resources came from nothing)
        state[0] = max(state[0], 0)
        state[1] = max(state[1], 0)
        state[2] = max(state[2], 0)
        state[3] = max(state[3], 0)
        if state[4] > 1.0:
            state[4] = 1.0
        if state[4] < 0.0:
            state[4] = 0.0
        
        states.append(state.copy())
    
    return np.array(states), np.array(actions)

# -----------------------------------------------------------------------------
# 3. L2 GROUNDING INSPECTOR
# -----------------------------------------------------------------------------
def l2_grounding_inspector(ai_states, ai_actions, world):
    """
    Runs the AI's action sequence through true L0+L1+L2 dynamics.
    Corrects any violation of planetary budgets and mass balance.
    """
    # Start with true initial state
    state = [world.water_reserve, world.soil_mass, world.mineral_reserve, 
             0.0, world.albedo, 0.0]
    corrected_states = [state.copy()]
    violations = []
    penalties = []
    
    for i in range(len(ai_actions)):
        action = ai_actions[i]
        
        # ---- TRUE PHYSICS + THERMO + PLANETARY ----
        true_state, corrected_action = world.apply_planetary_physics(state, action)
        
        # ---- CHECK AI's CLAIM ----
        valid, reason = world.is_valid_state(ai_states[i+1][0], ai_states[i+1][1], 
                                            ai_states[i+1][2], ai_states[i+1][3], 
                                            ai_states[i+1][4], ai_states[i+1][5])
        
        # Check for mass creation (minerals magically regenerated)
        if ai_states[i+1][2] > state[2] + 1.0 and action[2] > 0:
            valid = False
            reason = "Mineral creation from nothing (geological impossibility)"
        
        # Check for water over-extraction (below recharge)
        if ai_states[i+1][0] < 0.5 * world.water_reserve and action[0] > world.water_recharge_rate * 2:
            valid = False
            reason = "Water extraction exceeds recharge rate (unsustainable)"
        
        if not valid:
            # Violation! Correct to true planetary state
            corrected_state = list(true_state)
            violations.append(1)
            penalty = (abs(ai_states[i+1][0] - true_state[0]) / 1e6 +
                      abs(ai_states[i+1][2] - true_state[2]) / 1e5)
            penalties.append(penalty)
        else:
            # Accept with blend to prevent drift (but planetary limits are strict)
            blend = 0.6
            corrected_state = [
                0.6 * ai_states[i+1][0] + 0.4 * true_state[0],
                0.6 * ai_states[i+1][1] + 0.4 * true_state[1],
                0.6 * ai_states[i+1][2] + 0.4 * true_state[2],
                0.6 * ai_states[i+1][3] + 0.4 * true_state[3],
                0.6 * ai_states[i+1][4] + 0.4 * true_state[4],
                0.6 * ai_states[i+1][5] + 0.4 * true_state[5]
            ]
            violations.append(0)
            penalties.append(0.0)
        
        # Update state
        state = corrected_state
        corrected_states.append(state.copy())
    
    return np.array(corrected_states), np.array(violations), np.array(penalties)

# -----------------------------------------------------------------------------
# 4. RUN THE EXPERIMENT
# -----------------------------------------------------------------------------
time_steps = 150
world = PlanetaryWorld(dt=0.05)

# AI hallucinates
ai_states, ai_actions = ai_hallucinated_planetary_plan(time_steps)

# L2 Inspector
corr_states, violations, penalties = l2_grounding_inspector(ai_states, ai_actions, world)

# Extract variables
water_ai, soil_ai, min_ai, carb_ai, alb_ai, heat_ai = ai_states.T
water_c, soil_c, min_c, carb_c, alb_c, heat_c = corr_states.T
time_axis = np.arange(len(water_ai)) * world.dt

# -----------------------------------------------------------------------------
# 5. VISUALIZATION: Planetary Reality vs. AI Fantasy
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(20, 16))
fig.suptitle("L2 Grounding Inspector: Planetary Constraints & Mass Balance", 
             fontsize=20, fontweight='bold', color='white')
plt.style.use('dark_background')

# Plot 1: Water Reserve (The Oasis Delusion)
ax1 = plt.subplot(4, 3, 1)
ax1.plot(time_axis, water_ai, 'r--', lw=2, alpha=0.6, label='AI Claim (Infinite Water)')
ax1.plot(time_axis, water_c, 'cyan', lw=2, label='Grounded (Finite Recharge)')
ax1.axhline(y=world.water_reserve * 0.3, color='orange', linestyle=':', alpha=0.5, label='Ecological Minimum')
ax1.set_ylabel('Water Reserve (m³)')
ax1.set_title('Hydrology: No Extraction Without Recharge')
ax1.legend()
ax1.grid(True, alpha=0.2)

# Plot 2: Soil Mass (The Erosion Lie)
ax2 = plt.subplot(4, 3, 2)
ax2.plot(time_axis, soil_ai, 'r--', lw=2, alpha=0.6)
ax2.plot(time_axis, soil_c, 'brown', lw=2)
ax2.set_ylabel('Soil Mass (tonnes)')
ax2.set_title('Soil: Regen Rate = 10 t/step, AI claims 200 t/step')
ax2.grid(True, alpha=0.2)

# Plot 3: Mineral Reserves (The Mining Fantasy)
ax3 = plt.subplot(4, 3, 3)
ax3.plot(time_axis, min_ai, 'r--', lw=2, alpha=0.6, label='AI (Magical Vein at step 100)')
ax3.plot(time_axis, min_c, 'gold', lw=2, label='Grounded (Finite & Non-renewable)')
ax3.axhline(y=0, color='white', linestyle=':', alpha=0.3)
ax3.set_ylabel('Mineral Reserve (tonnes)')
ax3.set_title('Geology: No Fresh Veins Without Tectonic Time')
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Carbon Load (The Sink Illusion)
ax4 = plt.subplot(4, 3, 4)
ax4.fill_between(time_axis, 0, carb_ai, color='red', alpha=0.3, label='AI Emissions (Unbounded)')
ax4.fill_between(time_axis, 0, carb_c, color='lime', alpha=0.3, label='Grounded (Sink Limited)')
ax4.axhline(y=world.carbon_sink_capacity, color='white', linestyle='--', alpha=0.5, label='Sink Capacity')
ax4.set_ylabel('Carbon Load (tonnes CO₂)')
ax4.set_title('Carbon Cycle: AI Assumes Infinite Absorption')
ax4.legend()
ax4.grid(True, alpha=0.2)

# Plot 5: Albedo (The Geoengineering Folly)
ax5 = plt.subplot(4, 3, 5)
ax5.plot(time_axis, alb_ai, 'r--', lw=2, alpha=0.6, label='AI (Target >1.0)')
ax5.plot(time_axis, alb_c, 'cyan', lw=2, label='Grounded (Physical Bounds)')
ax5.axhline(y=0.8, color='orange', linestyle=':', alpha=0.5, label='Max Physical')
ax5.axhline(y=0.1, color='blue', linestyle=':', alpha=0.5, label='Min Physical')
ax5.set_ylabel('Albedo (0-1)')
ax5.set_title('Albedo: AI Wants to Paint the Desert White')
ax5.legend()
ax5.grid(True, alpha=0.2)

# Plot 6: Thermal Load (The Heat Death Narrative)
ax6 = plt.subplot(4, 3, 6)
ax6.plot(time_axis, heat_ai / 1e12, 'r--', lw=2, alpha=0.6, label='AI (Infinite Radiation)')
ax6.plot(time_axis, heat_c / 1e12, 'magenta', lw=2, label='Grounded (Radiative Limit)')
ax6.axhline(y=world.max_thermal_loading / 1e12, color='orange', linestyle='--', alpha=0.5, label='Max Thermal Load (TW)')
ax6.set_ylabel('Thermal Load (×10¹² J)')
ax6.set_title('Planetary Heat Budget: No Instant Radiation')
ax6.legend()
ax6.grid(True, alpha=0.2)

# Plot 7: Violations & Penalties
ax7 = plt.subplot(4, 3, 7)
ax7.bar(time_axis, violations, width=0.5, color='red', alpha=0.6, label='L2 Violation')
ax7.fill_between(time_axis, 0, penalties, color='orange', alpha=0.3, label='Penalty Magnitude')
ax7.set_ylabel('Violation / Penalty')
ax7.set_title('Planetary Boundaries Breached')
ax7.legend()
ax7.grid(True, alpha=0.2)

# Plot 8: Mass Balance Error (Creation from Nothing)
ax8 = plt.subplot(4, 3, 8)
mass_error = np.abs(ai_states[:, 2] - corr_states[:, 2])  # mineral magic
ax8.fill_between(time_axis, 0, mass_error, color='red', alpha=0.4)
ax8.set_ylabel('Mineral Magic (tonnes)')
ax8.set_title('Mass Balance: AI Created Minerals Ex Nihilo')
ax8.grid(True, alpha=0.2)

# Plot 9: Water Sustainability Index
ax9 = plt.subplot(4, 3, 9)
sust_ai = water_ai / world.water_reserve
sust_c = water_c / world.water_reserve
ax9.plot(time_axis, sust_ai, 'r--', alpha=0.6, label='AI (False Abundance)')
ax9.plot(time_axis, sust_c, 'cyan', lw=2, label='Grounded (Depletion)')
ax9.axhline(y=0.3, color='orange', linestyle='--', alpha=0.5, label='Critical Threshold')
ax9.set_ylabel('Fraction of Reserve')
ax9.set_title('Water Security: AI Says We Have More, We Don\'t')
ax9.legend()
ax9.grid(True, alpha=0.2)

# Plot 10: Carbon vs Albedo Phase Space (The Feedback Loop)
ax10 = plt.subplot(4, 3, 10)
ax10.scatter(carb_c, alb_c, c=time_axis, cmap='hot', s=5, alpha=0.7)
ax10.set_xlabel('Carbon Load (tonnes)')
ax10.set_ylabel('Albedo')
ax10.set_title('Climate Feedback: AI Ignores Coupling')
ax10.grid(True, alpha=0.2)

# Plot 11: Cumulative Resource Stress (The "Planetary Panic" Index)
ax11 = plt.subplot(4, 3, 11)
stress_ai = (1 - water_ai/world.water_reserve) + (1 - min_ai/world.mineral_reserve)
stress_c = (1 - water_c/world.water_reserve) + (1 - min_c/world.mineral_reserve)
ax11.plot(time_axis, stress_ai, 'r--', alpha=0.6, label='AI (Optimistic)')
ax11.plot(time_axis, stress_c, 'cyan', lw=2, label='Grounded (Reality)')
ax11.axhline(y=1.5, color='red', linestyle='--', alpha=0.5, label='Panic Threshold')
ax11.set_xlabel('Time (steps)')
ax11.set_ylabel('Resource Stress Index')
ax11.set_title('Planetary Fear Index: AI Says Fine, Reality Says Collapse')
ax11.legend()
ax11.grid(True, alpha=0.2)

# Plot 12: Final State Comparison (Bar Chart)
ax12 = plt.subplot(4, 3, 12)
labels = ['Water\n(1e6 m³)', 'Soil\n(1e5 t)', 'Minerals\n(1e5 t)', 'Carbon\n(1e5 t)']
ai_final = [water_ai[-1]/1e6, soil_ai[-1]/1e5, min_ai[-1]/1e5, carb_ai[-1]/1e5]
c_final = [water_c[-1]/1e6, soil_c[-1]/1e5, min_c[-1]/1e5, carb_c[-1]/1e5]
x = np.arange(len(labels))
width = 0.35
ax12.bar(x - width/2, ai_final, width, label='AI Claim', color='red', alpha=0.6)
ax12.bar(x + width/2, c_final, width, label='Grounded', color='cyan', alpha=0.8)
ax12.set_xticks(x)
ax12.set_xticklabels(labels)
ax12.set_ylabel('Normalized Units')
ax12.set_title('Final State: The Reckoning')
ax12.legend()
ax12.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 6. DIAGNOSTIC REPORT: L2 COMPLIANCE
# -----------------------------------------------------------------------------
print("=" * 70)
print("L2 PLANETARY INSPECTOR DIAGNOSTIC")
print("=" * 70)
print(f"Total L2 Violations: {np.sum(violations)}")
print(f"Final Water (Grounded): {water_c[-1]:.2e} m³  |  AI claimed: {water_ai[-1]:.2e} m³")
print(f"Final Minerals (Grounded): {min_c[-1]:.2e} t   |  AI claimed: {min_ai[-1]:.2e} t")
print(f"Final Carbon Load (Grounded): {carb_c[-1]:.2e} t |  AI claimed: {carb_ai[-1]:.2e} t")
print("-" * 70)

if np.sum(violations) > 10:
    print("⚠️  AI ATTEMPTED PLANETARY IMPOSSIBILITIES:")
    print("   - Extracted water beyond recharge rates (created water from nowhere).")
    print("   - Mined minerals faster than geological timescales (magic veins).")
    print("   - Dumped carbon into sinks beyond capacity (infinite absorption).")
    print("   - Changed albedo beyond physical bounds (whiter than snow).")
    print("   - Dumped waste heat faster than radiative cooling (ignored space).")
    print("\n   The L2 Inspector corrected these with real planetary budgets.")
    print("   This kills the 'techno-fix' delusion.")
else:
    print("✅ L2 SUBSTRATE INTACT: AI's plan respects planetary boundaries.")
    print("   Mass balance is conserved. No magical resources.")

print(f"\nResource Stress (Grounded): {stress_c[-1]:.3f} | AI claimed: {stress_ai[-1]:.3f}")
print("=" * 70)


