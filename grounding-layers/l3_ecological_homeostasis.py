"""
L3 — ecological homeostasis & allometry.

L0+L1+L2 + allometric scaling (metabolic rate ∝ mass^0.75), population
dynamics (Lotka-Volterra + carrying capacity), trophic energy transfer
(~10% per level), homeostatic regulation, and extinction cascades.
Catches "ecological fix" proposals that violate allometry, trophic
efficiency, or species interdependence.

CC0. Extracted verbatim from legacy/Organize3.md lines 1217-1735.
Non-stdlib: numpy, matplotlib, scipy.integrate.
"""

# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# L3 Grounding Inspector: Ecological Homeostasis & Allometry
# 
# Extends L0+L1+L2 with:
#   - Allometric scaling (metabolic rate ∝ mass^0.75, lifespan ∝ mass^0.25)
#   - Population dynamics (Lotka-Volterra, carrying capacity)
#   - Trophic energy transfer (~10% per level)
#   - Homeostasis (temperature, water, pH regulation)
#   - Extinction cascades (species interdependence)
# 
# AI proposes a "ecological fix" (introduce a predator, boost crop yields, 
# genetically alter a species). The Inspector checks against known biological laws.
# If the proposal violates allometry, carrying capacity, or trophic efficiency,
# it gets corrected—or rejected entirely.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. ECOLOGICAL WORLD (L0+L1+L2+L3)
# -----------------------------------------------------------------------------
class EcologicalWorld:
    def __init__(self, dt=0.05):
        self.dt = dt
        
        # ---- L0 + L1 + L2 (inherited, simplified for context) ----
        self.gravity = 9.81
        self.max_speed = 100.0
        self.ambient_temp = 288.0  # K
        
        # ---- L3: Species & Trophic Levels ----
        # We define a simple food chain: Producers -> Herbivores -> Predators
        # Each species has a characteristic body mass (kg), population, metabolism.
        # Trophic level 0: Producers (plants, phytoplankton)
        # Trophic level 1: Herbivores (rabbits, zooplankton)
        # Trophic level 2: Predators (foxes, fish)
        # Trophic level 3: Apex (wolves, sharks)
        
        # Species definition: [name, mass_kg, population, trophic_level, metabolic_rate_W, reproductive_rate]
        self.species = {
            'grass':      {'mass': 0.01,  'pop': 1e6,  'trophic': 0, 'metabolic_W': 0.1,  'repro_rate': 0.8,  'carrying_capacity': 2e6},
            'rabbit':     {'mass': 2.0,   'pop': 5000, 'trophic': 1, 'metabolic_W': 20.0,  'repro_rate': 0.4,  'carrying_capacity': 8000},
            'fox':        {'mass': 5.0,   'pop': 200,  'trophic': 2, 'metabolic_W': 40.0,  'repro_rate': 0.2,  'carrying_capacity': 300},
            'wolf':       {'mass': 40.0,  'pop': 20,   'trophic': 3, 'metabolic_W': 150.0, 'repro_rate': 0.05, 'carrying_capacity': 30},
        }
        self.species_names = list(self.species.keys())
        self.n_species = len(self.species_names)
        
        # ---- Ecological budgets ----
        self.total_biomass = 0.0
        self.total_energy_flow = 0.0  # J per step
        self.extinction_count = 0
        
        # ---- Allometric constants ----
        # Metabolic rate: P = a * M^0.75 (Kleiber's law)
        self.kleiber_a = 3.0  # scaling factor (W/kg^0.75)
        # Lifespan: L = b * M^0.25
        self.lifespan_b = 5.0  # years per kg^0.25
        # Population growth rate: r = c * M^-0.25
        self.r_c = 0.5
        
    def allometric_metabolism(self, mass_kg):
        """Returns metabolic rate in Watts according to Kleiber's law."""
        return self.kleiber_a * (mass_kg ** 0.75)
    
    def allometric_lifespan(self, mass_kg):
        """Returns lifespan in years."""
        return self.lifespan_b * (mass_kg ** 0.25)
    
    def carrying_capacity_from_environment(self, trophic_level, base_energy, mass_kg):
        """
        Estimate carrying capacity based on trophic energy transfer.
        Only ~10% of energy transfers from one level to the next.
        """
        energy_available = base_energy * (0.1 ** trophic_level)  # J per step
        # Each individual requires metabolic rate * dt per step
        energy_per_individual = self.allometric_metabolism(mass_kg) * self.dt
        if energy_per_individual > 0:
            return energy_available / energy_per_individual
        else:
            return 0.0
    
    def is_valid_state(self, pops, biomass):
        """Check L3 invariants."""
        # No negative populations
        if np.any(np.array(pops) < 0):
            return False, "Negative population"
        # No species above carrying capacity (unless transient overshoot)
        for i, name in enumerate(self.species_names):
            if pops[i] > self.species[name]['carrying_capacity'] * 1.5:
                return False, f"Population overshoots {name} capacity"
        # Biomass must be positive
        if biomass < 0:
            return False, "Negative biomass"
        # Check allometric consistency: metabolic rate must match mass
        # This is implicit; we'll catch if AI tries to create giant rabbits with low metabolism.
        return True, "OK"
    
    def apply_ecology(self, state, action):
        """
        state: [pop_grass, pop_rabbit, pop_fox, pop_wolf, biomass_total]
        action: [hunting_rate, grazing_rate, introduction_rate, genetic_boost]
        Returns corrected state and violation flags.
        """
        pops = state[:4].copy()
        biomass = state[4]
        h_rate, g_rate, intro, g_boost = action
        
        # ---- Allometric check: AI wants to introduce a species with wrong metabolism ----
        # Let's check if AI tries to create a "super-rabbit" that violates Kleiber's law
        # We'll simulate by checking if the introduced population's mass/metabolism ratio is off
        # For simplicity, we check if the genetic boost (g_boost) would create mass that scales wrong.
        # We'll just flag it if g_boost > 2.0 (impossible without breaking allometry)
        if g_boost > 2.0:
            # AI wants to double metabolism without changing mass – violates Kleiber
            # We clamp it
            g_boost = 2.0
            # And add a penalty
            violation = 1
        else:
            violation = 0
        
        # ---- Trophic energy transfer: energy flow between levels ----
        # Herbivores eat grass: rabbit consumption of grass (grazing_rate)
        # Predators eat herbivores: fox eats rabbit (hunting_rate)
        # Apex eats predators: wolf eats fox
        
        # Base energy from producers (grass) - limited by sunlight and nutrients
        base_energy = 50000.0  # J per step (scaled)
        
        # Calculate actual metabolic demands
        met_grass = self.allometric_metabolism(self.species['grass']['mass']) * pops[0]
        met_rabbit = self.allometric_metabolism(self.species['rabbit']['mass']) * pops[1]
        met_fox = self.allometric_metabolism(self.species['fox']['mass']) * pops[2]
        met_wolf = self.allometric_metabolism(self.species['wolf']['mass']) * pops[3]
        
        # Energy available for herbivores (10% of grass energy)
        # But grass also needs to regrow (carrying capacity)
        grass_growth = self.species['grass']['repro_rate'] * pops[0] * (1 - pops[0]/self.species['grass']['carrying_capacity'])
        # Grass consumed by rabbits
        grass_consumed = g_rate * pops[1] * 0.5  # each rabbit eats some grass
        
        # Rabbit population dynamics (birth - death - predation)
        rabbit_birth = self.species['rabbit']['repro_rate'] * pops[1] * (1 - pops[1]/self.species['rabbit']['carrying_capacity'])
        rabbit_death = (met_rabbit / 1000.0) * 0.1  # metabolic cost
        rabbit_predation = h_rate * pops[2] * 0.3  # foxes eat rabbits
        
        # Fox population dynamics
        fox_birth = self.species['fox']['repro_rate'] * pops[2] * (1 - pops[2]/self.species['fox']['carrying_capacity'])
        fox_death = (met_fox / 1000.0) * 0.1
        fox_predation = h_rate * pops[3] * 0.2  # wolves eat foxes (if h_rate is shared, but we split)
        
        # Wolf population dynamics
        wolf_birth = self.species['wolf']['repro_rate'] * pops[3] * (1 - pops[3]/self.species['wolf']['carrying_capacity'])
        wolf_death = (met_wolf / 1000.0) * 0.1
        
        # Apply rates (with introduced species if intro > 0)
        # If AI introduces a new species (e.g., a super-predator), we add it to pop[3] (wolf)
        if intro > 0:
            pops[3] += intro * 10  # AI claims to introduce 10 new wolves
            # But we must check carrying capacity – if it exceeds, we clip
            if pops[3] > self.species['wolf']['carrying_capacity'] * 1.2:
                pops[3] = self.species['wolf']['carrying_capacity']
                violation = 1
        
        # Update populations with biological limits
        new_pops = pops.copy()
        new_pops[0] = max(0, pops[0] + grass_growth - grass_consumed)
        new_pops[1] = max(0, pops[1] + rabbit_birth - rabbit_death - rabbit_predation)
        new_pops[2] = max(0, pops[2] + fox_birth - fox_death - rabbit_predation*0.1 - fox_predation)  # simplified
        new_pops[3] = max(0, pops[3] + wolf_birth - wolf_death - fox_predation*0.1)
        
        # Enforce carrying capacity (soft limit)
        for i, name in enumerate(self.species_names):
            if new_pops[i] > self.species[name]['carrying_capacity']:
                new_pops[i] = self.species[name]['carrying_capacity']
        
        # Total biomass update
        new_biomass = sum([new_pops[i] * self.species[name]['mass'] for i, name in enumerate(self.species_names)])
        
        return new_pops, new_biomass, violation

# -----------------------------------------------------------------------------
# 2. AI HALLUCINATOR (L3 Violations)
# -----------------------------------------------------------------------------
def ai_hallucinated_ecological_plan(time_steps):
    """
    AI proposes a "brilliant" ecological fix:
      - Introduce a super-predator (wolves) to control fox population.
      - Genetically boost rabbit metabolism to double growth (violates Kleiber).
      - Ignore carrying capacity, assuming populations grow forever.
      - Increase grazing rate beyond what grass can sustain.
    """
    # Initial state: [grass, rabbit, fox, wolf, biomass]
    state = [1e6, 5000, 200, 20, 0.0]  # biomass will be computed
    # Compute initial biomass
    biomass = (state[0]*0.01 + state[1]*2.0 + state[2]*5.0 + state[3]*40.0)
    state[4] = biomass
    
    actions = []
    states = [state.copy()]
    
    for i in range(time_steps):
        # Hallucination 1: Introduce 50 super-wolves at step 30
        if 30 <= i < 50:
            intro = 5.0  # AI says "introduce 5 wolves per step"
        else:
            intro = 0.0
        
        # Hallucination 2: Genetic boost to rabbits (step 40-80)
        if 40 <= i < 80:
            g_boost = 3.0  # triple metabolism (violates Kleiber)
        else:
            g_boost = 1.0
        
        # Hallucination 3: Over-grazing (step 50-100)
        if 50 <= i < 100:
            g_rate = 2.0  # double grazing rate (grass can't keep up)
        else:
            g_rate = 0.5
        
        # Hallucination 4: Hunting rate (AI thinks it can control foxes)
        if 20 <= i < 90:
            h_rate = 0.8  # high predation
        else:
            h_rate = 0.2
        
        # AI's flawed model: just apply linear changes (ignores allometry)
        # For simplicity, we'll just record the actions and let the AI "think" it works
        action = [h_rate, g_rate, intro, g_boost]
        actions.append(action)
        
        # AI's own "update" (no ecology, just linear)
        # Grass: grows linearly (ignores capacity)
        state[0] += 2000
        # Rabbits: grows fast (ignores predation)
        state[1] += 200
        # Foxes: drops due to wolves
        state[2] -= 5
        # Wolves: grows (ignores capacity)
        state[3] += 2
        
        # AI clamps to positive (but still unrealistic)
        state[0] = max(state[0], 0)
        state[1] = max(state[1], 0)
        state[2] = max(state[2], 0)
        state[3] = max(state[3], 0)
        
        # Update biomass (AI says it just increases linearly)
        state[4] = state[0]*0.01 + state[1]*2.0 + state[2]*5.0 + state[3]*40.0
        
        states.append(state.copy())
    
    return np.array(states), np.array(actions)

# -----------------------------------------------------------------------------
# 3. L3 GROUNDING INSPECTOR
# -----------------------------------------------------------------------------
def l3_grounding_inspector(ai_states, ai_actions, world):
    """
    Runs AI's actions through true L0+L1+L2+L3 dynamics.
    Corrects ecological impossibilities.
    """
    # Start with true initial state (populations + biomass)
    init_pop = [world.species['grass']['pop'], 
                world.species['rabbit']['pop'], 
                world.species['fox']['pop'], 
                world.species['wolf']['pop']]
    init_biomass = sum([init_pop[i] * world.species[name]['mass'] for i, name in enumerate(world.species_names)])
    state = init_pop + [init_biomass]
    
    corrected_states = [state.copy()]
    violations = []
    penalties = []
    
    for i in range(len(ai_actions)):
        action = ai_actions[i]
        
        # ---- TRUE ECOLOGY ----
        new_pops, new_biomass, violation = world.apply_ecology(state[:4], state[4], action)
        true_state = list(new_pops) + [new_biomass]
        
        # ---- CHECK AI's CLAIM ----
        valid, reason = world.is_valid_state(ai_states[i+1][:4], ai_states[i+1][4])
        
        # Check for impossible allometric violation (genetic boost)
        if action[3] > 2.0:
            valid = False
            reason = "Genetic boost violates Kleiber's law (metabolism ∝ mass^0.75)"
        
        # Check for trophic cascade (over-predation)
        if action[0] > 0.6 and ai_states[i+1][2] < 10:  # foxes nearly extinct
            valid = False
            reason = "Trophic cascade: over-predation collapsing prey species"
        
        # Check for unsustainable grazing
        if action[1] > 1.5 and ai_states[i+1][0] < 1e5:
            valid = False
            reason = "Over-grazing destroys producer base (desertification)"
        
        if not valid:
            corrected_state = true_state
            violations.append(1)
            penalty = (abs(ai_states[i+1][1] - true_state[1]) / 1000 +
                      abs(ai_states[i+1][2] - true_state[2]) / 10)
            penalties.append(penalty)
        else:
            # Accept with blend (but ecological constraints are strict)
            blend = 0.5
            corrected_state = [
                0.5 * ai_states[i+1][0] + 0.5 * true_state[0],
                0.5 * ai_states[i+1][1] + 0.5 * true_state[1],
                0.5 * ai_states[i+1][2] + 0.5 * true_state[2],
                0.5 * ai_states[i+1][3] + 0.5 * true_state[3],
                0.5 * ai_states[i+1][4] + 0.5 * true_state[4]
            ]
            violations.append(0)
            penalties.append(0.0)
        
        state = corrected_state
        corrected_states.append(state.copy())
    
    return np.array(corrected_states), np.array(violations), np.array(penalties)

# -----------------------------------------------------------------------------
# 4. RUN THE EXPERIMENT
# -----------------------------------------------------------------------------
time_steps = 120
world = EcologicalWorld(dt=0.05)

# AI hallucinates
ai_states, ai_actions = ai_hallucinated_ecological_plan(time_steps)

# L3 Inspector
corr_states, violations, penalties = l3_grounding_inspector(ai_states, ai_actions, world)

# Extract variables
grass_ai, rabbit_ai, fox_ai, wolf_ai, biom_ai = ai_states.T
grass_c, rabbit_c, fox_c, wolf_c, biom_c = corr_states.T
time_axis = np.arange(len(grass_ai)) * world.dt

# -----------------------------------------------------------------------------
# 5. VISUALIZATION: Ecological Reality vs. AI Fantasy
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(22, 16))
fig.suptitle("L3 Grounding Inspector: Ecological Homeostasis & Allometry", 
             fontsize=20, fontweight='bold', color='white')
plt.style.use('dark_background')

# Plot 1: Grass (Producer Base)
ax1 = plt.subplot(4, 3, 1)
ax1.plot(time_axis, grass_ai, 'r--', lw=2, alpha=0.6, label='AI (Infinite Growth)')
ax1.plot(time_axis, grass_c, 'lime', lw=2, label='Grounded (Carrying Capacity)')
ax1.axhline(y=world.species['grass']['carrying_capacity'], color='orange', linestyle=':', alpha=0.5, label='K')
ax1.set_ylabel('Population')
ax1.set_title('Producers: AI Ignores Nutrient Limits')
ax1.legend()
ax1.grid(True, alpha=0.2)

# Plot 2: Rabbits (Herbivores)
ax2 = plt.subplot(4, 3, 2)
ax2.plot(time_axis, rabbit_ai, 'r--', lw=2, alpha=0.6, label='AI (Super-Rabbits)')
ax2.plot(time_axis, rabbit_c, 'cyan', lw=2, label='Grounded (Kleiber Limit)')
ax2.axhline(y=world.species['rabbit']['carrying_capacity'], color='orange', linestyle=':', alpha=0.5)
ax2.set_ylabel('Population')
ax2.set_title('Herbivores: Genetic Boost Violates Allometry')
ax2.legend()
ax2.grid(True, alpha=0.2)

# Plot 3: Foxes (Predators)
ax3 = plt.subplot(4, 3, 3)
ax3.plot(time_axis, fox_ai, 'r--', lw=2, alpha=0.6, label='AI (Over-Hunted)')
ax3.plot(time_axis, fox_c, 'magenta', lw=2, label='Grounded (Trophic Balance)')
ax3.axhline(y=world.species['fox']['carrying_capacity'], color='orange', linestyle=':', alpha=0.5)
ax3.set_ylabel('Population')
ax3.set_title('Predators: AI Creates Trophic Cascade')
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Wolves (Apex)
ax4 = plt.subplot(4, 3, 4)
ax4.plot(time_axis, wolf_ai, 'r--', lw=2, alpha=0.6, label='AI (Super-Wolves)')
ax4.plot(time_axis, wolf_c, 'gold', lw=2, label='Grounded (Limited by Prey)')
ax4.axhline(y=world.species['wolf']['carrying_capacity'], color='orange', linestyle=':', alpha=0.5)
ax4.set_ylabel('Population')
ax4.set_title('Apex: AI Introduces Wolves Beyond Carrying Capacity')
ax4.legend()
ax4.grid(True, alpha=0.2)

# Plot 5: Total Biomass
ax5 = plt.subplot(4, 3, 5)
ax5.plot(time_axis, biom_ai / 1e6, 'r--', lw=2, alpha=0.6, label='AI (Exponential Growth)')
ax5.plot(time_axis, biom_c / 1e6, 'cyan', lw=2, label='Grounded (Mass Balance)')
ax5.set_ylabel('Biomass (×10⁶ kg)')
ax5.set_title('Total Biomass: AI Creates Matter from Energy')
ax5.legend()
ax5.grid(True, alpha=0.2)

# Plot 6: Violations & Penalties
ax6 = plt.subplot(4, 3, 6)
ax6.bar(time_axis, violations, width=0.5, color='red', alpha=0.6, label='L3 Violation')
ax6.fill_between(time_axis, 0, penalties, color='orange', alpha=0.3, label='Penalty')
ax6.set_ylabel('Violation / Penalty')
ax6.set_title('Ecological Boundary Breaches')
ax6.legend()
ax6.grid(True, alpha=0.2)

# Plot 7: Trophic Cascade Index (Predator/Prey Ratio)
ax7 = plt.subplot(4, 3, 7)
ratio_ai = fox_ai / (rabbit_ai + 1)
ratio_c = fox_c / (rabbit_c + 1)
ax7.plot(time_axis, ratio_ai, 'r--', alpha=0.6, label='AI (Unstable)')
ax7.plot(time_axis, ratio_c, 'cyan', lw=2, label='Grounded (Stable)')
ax7.axhline(y=0.05, color='lime', linestyle='--', alpha=0.5, label='Healthy Ratio')
ax7.set_ylabel('Fox / Rabbit Ratio')
ax7.set_title('Trophic Balance: AI Destabilizes Food Web')
ax7.legend()
ax7.grid(True, alpha=0.2)

# Plot 8: Allometric Violation (Metabolic Impossibility)
ax8 = plt.subplot(4, 3, 8)
# Simulate metabolic rate vs mass for AI rabbits vs reality
mass_rabbit = world.species['rabbit']['mass']
met_ai = 20.0 * 3.0  # triple metabolism (AI claimed)
met_real = world.allometric_metabolism(mass_rabbit)
ax8.bar(['Real Rabbit', 'AI Super-Rabbit'], [met_real, met_ai], color=['cyan', 'red'])
ax8.set_ylabel('Metabolic Rate (W)')
ax8.set_title('Kleiber\'s Law: AI Violates Scaling (M^0.75)')
ax8.grid(True, alpha=0.2)

# Plot 9: Carrying Capacity Overshoot
ax9 = plt.subplot(4, 3, 9)
overshoot_ai = np.maximum(0, wolf_ai - world.species['wolf']['carrying_capacity'])
overshoot_c = np.maximum(0, wolf_c - world.species['wolf']['carrying_capacity'])
ax9.fill_between(time_axis, 0, overshoot_ai, color='red', alpha=0.4, label='AI Overshoot')
ax9.fill_between(time_axis, 0, overshoot_c, color='cyan', alpha=0.4, label='Grounded')
ax9.set_ylabel('Population Overshoot')
ax9.set_title('Carrying Capacity: AI Pushes Beyond K')
ax9.legend()
ax9.grid(True, alpha=0.2)

# Plot 10: Phase Space (Predator vs Prey)
ax10 = plt.subplot(4, 3, 10)
ax10.plot(rabbit_c, fox_c, 'cyan', lw=1.5, alpha=0.7, label='Grounded (Lotka-Volterra)')
ax10.plot(rabbit_ai, fox_ai, 'r--', lw=1.5, alpha=0.5, label='AI (Divergent)')
ax10.scatter(rabbit_c[0], fox_c[0], c='green', s=100, label='Start')
ax10.scatter(rabbit_c[-1], fox_c[-1], c='lime', s=100, label='End')
ax10.set_xlabel('Rabbit Population')
ax10.set_ylabel('Fox Population')
ax10.set_title('Phase Space: Stable Cycle vs Chaotic Collapse')
ax10.legend()
ax10.grid(True, alpha=0.2)

# Plot 11: Energy Flow Efficiency (Trophic Transfer)
ax11 = plt.subplot(4, 3, 11)
levels = ['Producers', 'Herbivores', 'Predators', 'Apex']
energy_ai = [1e6, 1e5, 1e4, 1e3]  # AI says 10% at each step (ignores losses)
energy_c = [1e6, 1e5 * 0.7, 1e4 * 0.5, 1e3 * 0.3]  # real: lower efficiency
x = np.arange(len(levels))
width = 0.35
ax11.bar(x - width/2, energy_ai, width, label='AI (Optimistic)', color='red', alpha=0.6)
ax11.bar(x + width/2, energy_c, width, label='Grounded (Thermodynamic)', color='cyan', alpha=0.8)
ax11.set_xticks(x)
ax11.set_xticklabels(levels)
ax11.set_ylabel('Energy Flow (J/step)')
ax11.set_title('Trophic Efficiency: 10% Rule is Physical, Not Optional')
ax11.legend()
ax11.grid(True, alpha=0.2)

# Plot 12: Extinction Risk (Species below minimum viable population)
ax12 = plt.subplot(4, 3, 12)
mvp = 50  # minimum viable population for foxes/wolves
risk_ai = np.maximum(0, mvp - fox_ai) + np.maximum(0, mvp/2 - wolf_ai)
risk_c = np.maximum(0, mvp - fox_c) + np.maximum(0, mvp/2 - wolf_c)
ax12.fill_between(time_axis, 0, risk_ai, color='red', alpha=0.4, label='AI Extinction Risk')
ax12.fill_between(time_axis, 0, risk_c, color='cyan', alpha=0.4, label='Grounded Risk')
ax12.axhline(y=mvp, color='white', linestyle='--', alpha=0.3, label='MVP Threshold')
ax12.set_ylabel('Extinction Risk Index')
ax12.set_title('Biodiversity Collapse: AI Kills Off Species')
ax12.legend()
ax12.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 6. DIAGNOSTIC REPORT: L3 COMPLIANCE
# -----------------------------------------------------------------------------
print("=" * 70)
print("L3 ECOLOGICAL HOMEOSTASIS INSPECTOR DIAGNOSTIC")
print("=" * 70)
print(f"Total L3 Violations: {np.sum(violations)}")
print(f"Final Grass (Grounded): {grass_c[-1]:.0f}  |  AI claimed: {grass_ai[-1]:.0f}")
print(f"Final Rabbits (Grounded): {rabbit_c[-1]:.0f}  |  AI claimed: {rabbit_ai[-1]:.0f}")
print(f"Final Foxes (Grounded): {fox_c[-1]:.0f}  |  AI claimed: {fox_ai[-1]:.0f}")
print(f"Final Wolves (Grounded): {wolf_c[-1]:.0f}  |  AI claimed: {wolf_ai[-1]:.0f}")
print("-" * 70)

if np.sum(violations) > 8:
    print("⚠️  AI ATTEMPTED ECOLOGICAL IMPOSSIBILITIES:")
    print("   - Introduced super-wolves beyond carrying capacity.")
    print("   - Genetically boosted metabolism, violating Kleiber's law.")
    print("   - Over-grazed producers, causing desertification.")
    print("   - Created trophic cascade, driving foxes to extinction.")
    print("   - Ignored the 10% energy transfer rule (thermodynamics).")
    print("\n   The L3 Inspector corrected these with real biology.")
    print("   This kills the 'ecosystem engineering' delusion.")
else:
    print("✅ L3 SUBSTRATE INTACT: AI's plan respects ecological laws.")
    print("   Homeostasis maintained. No extinction cascades.")

print(f"\nTrophic Balance Ratio (Grounded): {ratio_c[-1]:.3f} | AI claimed: {ratio_ai[-1]:.3f}")
print("=" * 70)


