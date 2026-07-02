"""
Atmospheric meteor heating with 1 km altitude bins — early draft.

Uses a 150-bin column, generates particles with realistic mass/speed
distributions, drops them through drag + ablation, and deposits kinetic
energy into altitude bins. This file is a DRAFT — the main loop is
stubbed with a pass and a note pointing at the "integrated version"
(dust_debris_basic.py) that actually runs to completion.

CC0 / for play. Extracted verbatim from legacy/Organize.md lines 3354-3736.
Non-stdlib: numpy, matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# 1. Atmospheric model & constants
# ------------------------------------------------------------------
H = 7500.0                # scale height (m)
rho0 = 1.225              # sea-level density (kg/m^3)
Cd = 0.47                 # drag coefficient (sphere)
Cp = 1000.0               # specific heat of air (J/(kg·K))

altitude_max = 150_000    # 150 km
n_bins = 150              # 1 km bins
z_edges = np.linspace(0, altitude_max, n_bins + 1)
z_centers = (z_edges[:-1] + z_edges[1:]) / 2

def density(z):
    """Exponential atmosphere (with a tiny floor to avoid infinities)."""
    return np.maximum(rho0 * np.exp(-z / H), 1e-12)

# ------------------------------------------------------------------
# 2. Particle generator
# ------------------------------------------------------------------
def generate_particles(n, scenario='normal'):
    """
    Generate a batch of incoming particles.
    Returns arrays: mass, radius, velocity, altitude.
    """
    # Masses: log-uniform from 1e-8 kg (dust) to 100 kg (small asteroid/debris)
    log_m_min, log_m_max = -8, 2
    mass = 10 ** np.random.uniform(log_m_min, log_m_max, n)
    
    # Density of particle material (kg/m^3) – assume 3000 for rock/metal
    rho_p = 3000
    radius = (3 * mass / (4 * np.pi * rho_p)) ** (1/3)
    
    # Initial altitude: start at 150 km with a small spread
    altitude = np.random.uniform(140_000, 150_000, n)
    
    # Velocities
    if scenario == 'normal':
        # Cosmic dust / meteors: 15–35 km/s
        velocity = np.random.uniform(15_000, 35_000, n)
    elif scenario == 'debris_storm':
        # Mix of orbital debris (7–8 km/s) and some meteors
        frac_debris = 0.7
        debris_mask = np.random.rand(n) < frac_debris
        velocity = np.random.uniform(7_000, 8_500, n)   # LEO re-entry
        velocity[~debris_mask] = np.random.uniform(15_000, 35_000, sum(~debris_mask))
    else:  # mega_event (asteroid breakup or Kessler catastrophe)
        # Massive influx, all speeds high
        velocity = np.random.uniform(10_000, 40_000, n)
    
    return mass, radius, velocity, altitude

# ------------------------------------------------------------------
# 3. Core simulation function
# ------------------------------------------------------------------
def run_heating_simulation(n_particles_total, scenario, injection_duration=5.0):
    """
    n_particles_total: total number of particles injected over `injection_duration` seconds.
    """
    dt = 0.05                 # time step (50 ms)
    max_steps = 400           # total simulate for 20 seconds (particles cross in ~10s)
    n_per_step = max(1, int(n_particles_total / (injection_duration / dt)))
    
    # Storage: energy deposited per altitude bin
    energy_deposited = np.zeros(n_bins)
    
    # Particle arrays (we build them incrementally)
    masses = np.array([])
    radii = np.array([])
    velocities = np.array([])
    altitudes = np.array([])
    active = np.array([], dtype=bool)
    
    total_kinetic_initial = 0.0
    total_energy_record = []   # cumulative deposited energy over time
    time_record = []
    
    # Pre-compute bin indices for altitude
    for step in range(max_steps):
        t = step * dt
        
        # ---- 4a. Inject new particles (for the first few seconds) ----
        if t < injection_duration:
            new_m, new_r, new_v, new_z = generate_particles(n_per_step, scenario)
            masses = np.concatenate([masses, new_m])
            radii = np.concatenate([radii, new_r])
            velocities = np.concatenate([velocities, new_v])
            altitudes = np.concatenate([altitudes, new_z])
            total_kinetic_initial += np.sum(0.5 * new_m * new_v**2)
            active = np.concatenate([active, np.ones(len(new_m), dtype=bool)])
        
        # ---- 4b. Update existing particles ----
        if len(masses) == 0:
            continue
        
        # Drag force parameters
        area = np.pi * radii**2
        rho = density(altitudes)
        
        # Deceleration: a = 0.5 * Cd * rho * v^2 * A / m
        # (Use sign – velocity is always positive downward)
        v_old = velocities.copy()
        accel = -0.5 * Cd * rho * velocities**2 * area / masses
        velocities += accel * dt
        # Ensure no negative velocities
        velocities = np.maximum(velocities, 0.0)
        
        # Update position
        altitudes += v_old * dt   # use old velocity for better energy conservation
        
        # ---- 4c. Energy deposition ----
        delta_E = 0.5 * masses * (v_old**2 - velocities**2)
        
        # Add to bins if particle is active and altitude is within domain
        valid = (altitudes >= 0) & (altitudes < altitude_max) & active
        bin_indices = np.floor(altitudes[valid] / 1000).astype(int)  # 1 km bins
        # Accumulate energy
        for idx, e in zip(bin_indices, delta_E[valid]):
            if 0 <= idx < n_bins:
                energy_deposited[idx] += e
        
        # ---- 4d. Remove inactive particles (hit ground or escape) ----
        active &= (altitudes > 0) & (altitudes < altitude_max) & (velocities > 0)
        
        # ---- 4e. Record cumulative energy ----
        total_energy_record.append(np.sum(energy_deposited))
        time_record.append(t)
        
        # Early exit if no particles left
        if not np.any(active) and t > injection_duration:
            break
    
    return energy_deposited, total_energy_record, time_record, total_kinetic_initial

# ------------------------------------------------------------------
# 4. Run two scenarios
# ------------------------------------------------------------------
print("Simulating normal cosmic dust flux...")
E_dep_norm, E_cum_norm, t_norm, KE_init_norm = run_heating_simulation(
    n_particles_total=5000, scenario='normal', injection_duration=3.0
)

print("Simulating major debris / asteroid storm...")
E_dep_storm, E_cum_storm, t_storm, KE_init_storm = run_heating_simulation(
    n_particles_total=50000, scenario='mega_event', injection_duration=3.0
)

# ------------------------------------------------------------------
# 5. Convert to temperature rise
# ------------------------------------------------------------------
def compute_temperature_rise(energy_dep, column_area=1.0):
    """
    Compute the temperature increase in a 1 m² atmospheric column.
    Mass of air in each 1 km bin = density * height * area.
    """
    dT = np.zeros(n_bins)
    for i in range(n_bins):
        z = z_centers[i]
        rho = density(z)
        # Mass of air in this 1 km slice per m²
        mass_air = rho * 1000.0 * column_area
        if mass_air > 1e-12:
            dT[i] = energy_dep[i] / (mass_air * Cp)
    return dT

dT_norm = compute_temperature_rise(E_dep_norm)
dT_storm = compute_temperature_rise(E_dep_storm)

# ------------------------------------------------------------------
# 6. Visualise everything
# ------------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# ---- Row 0: Normal flux ----
ax = axes[0,0]
ax.barh(z_centers/1000, E_dep_norm, height=1, color='skyblue')
ax.set_xlabel('Energy deposited (J per bin)')
ax.set_ylabel('Altitude (km)')
ax.set_title('Normal dust: Energy deposition')
ax.grid(alpha=0.3)

ax = axes[0,1]
ax.plot(t_norm, np.array(E_cum_norm) / 1e6, 'b-')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Cumulative energy (MJ)')
ax.set_title('Normal dust: Cumulative heating')
ax.grid(alpha=0.3)

ax = axes[0,2]
ax.barh(z_centers/1000, dT_norm, height=1, color='orange')
ax.set_xlabel('Temperature rise (K)')
ax.set_title('Normal dust: Local ΔT')
ax.grid(alpha=0.3)

# ---- Row 1: Storm event ----
ax = axes[1,0]
ax.barh(z_centers/1000, E_dep_storm, height=1, color='crimson')
ax.set_xlabel('Energy deposited (J per bin)')
ax.set_ylabel('Altitude (km)')
ax.set_title('Debris storm: Energy deposition')
ax.grid(alpha=0.3)

ax = axes[1,1]
ax.plot(t_storm, np.array(E_cum_storm) / 1e6, 'r-')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Cumulative energy (MJ)')
ax.set_title('Debris storm: Cumulative heating')
ax.grid(alpha=0.3)

ax = axes[1,2]
ax.barh(z_centers/1000, dT_storm, height=1, color='darkred')
ax.set_xlabel('Temperature rise (K)')
ax.set_title('Debris storm: Local ΔT')
ax.grid(alpha=0.3)

plt.tight_layout()
plt.suptitle('Atmospheric Heating by Space Particles & Debris', y=1.02, fontsize=16)
plt.show()

# ------------------------------------------------------------------
# 7. Quantitative summary
# ------------------------------------------------------------------
total_E_norm = np.sum(E_dep_norm)
total_E_storm = np.sum(E_dep_storm)

print("\n" + "="*50)
print("HEATING SUMMARY (per 1 m² atmospheric column)")
print("="*50)
print(f"Normal flux  : {total_E_norm/1e6:.2f} MJ deposited")
print(f"Debris storm : {total_E_storm/1e6:.2f} MJ deposited")
print(f"→ Storm is {total_E_storm/total_E_norm:.1f}x more energetic")
print("-"*50)

# Peak temperature rises
peak_dT_norm = np.max(dT_norm)
peak_dT_storm = np.max(dT_storm)
print(f"Peak local ΔT (normal)  : {peak_dT_norm:.2f} K at ~{z_centers[np.argmax(dT_norm)]/1000:.0f} km")
print(f"Peak local ΔT (storm)   : {peak_dT_storm:.2f} K at ~{z_centers[np.argmax(dT_storm)]/1000:.0f} km")
print("-"*50)
print("💡 Even huge storms heat locally by dozens/hundreds of Kelvin in the")
print("mesosphere. Globally, the effect is tiny compared to solar radiation,")
print("but it significantly affects upper-atmosphere chemistry, meteor trails,")
print("and re-entry plasma physics!")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# ------------------------------------------------------------------
# 0. Physical constants
# ------------------------------------------------------------------
R_earth = 6.371e6                # Earth radius (m)
g = 9.81                         # gravity (m/s²) – we ignore it for vertical (drag dominates)
Cp_air = 1000.0                  # air specific heat (J/kg·K)
rho_p = 3000.0                   # particle density (kg/m³)
M_atm = 5.148e18                 # total mass of atmosphere (kg)
latent_heat_vapor = 10e6         # energy to vaporise 1 kg of rock (J/kg)

# ------------------------------------------------------------------
# 1. Atmospheric model
# ------------------------------------------------------------------
H = 7500.0
rho0 = 1.225
def density(z):
    z = np.maximum(z, 0)
    return rho0 * np.exp(-z / H)

# ------------------------------------------------------------------
# 2. Particle class (using arrays for performance)
# ------------------------------------------------------------------
class ParticleSet:
    def __init__(self, n, scenario='normal'):
        self.n = n
        # Mass: log-uniform from 1e-7 to 50 kg
        log_m = np.random.uniform(-7, 1.7, n)
        self.mass = 10**log_m
        self.radius = (3 * self.mass / (4 * np.pi * rho_p)) ** (1/3)
        
        # Initial altitude: 120–150 km
        self.z = np.random.uniform(120_000, 150_000, n)
        
        # Velocities based on scenario
        if scenario == 'normal':
            self.v = np.random.uniform(12_000, 40_000, n)
        else:  # 'storm' or 'mega'
            self.v = np.random.uniform(7_000, 45_000, n)
        
        # Thermal state
        self.temp = np.full(n, 300.0)        # surface temp (K)
        self.ablated_mass = np.zeros(n)
        self.active = np.ones(n, dtype=bool)
        self.trail_energy = []               # store trail per altitude
        
    def step(self, dt, atmos_density):
        # ---- Drag & heating ----
        rho = atmos_density
        area = np.pi * self.radius**2
        v2 = self.v**2
        
        # Drag deceleration (a = 0.5 * Cd * rho * v^2 * A / m)
        Cd = 0.47
        a_drag = -0.5 * Cd * rho * v2 * area / self.mass
        self.v += a_drag * dt
        self.v = np.maximum(self.v, 0.0)
        v_avg = self.v + 0.5 * a_drag * dt  # energy-conserving average
        
        # ---- Heating from kinetic loss ----
        dKE = 0.5 * self.mass * (v_avg**2 - self.v**2)
        # Fraction of energy goes into heating the particle (not air yet)
        heating_fraction = 0.3               # 30% heats the particle, 70% heats surrounding air immediately
        heat_to_particle = dKE * heating_fraction
        heat_to_air = dKE * (1 - heating_fraction)
        
        # Particle temperature rise (Cp_particle ~ 1000 J/kg·K)
        Cp_p = 1000.0
        self.temp += heat_to_particle / (self.mass * Cp_p + 1e-12)
        
        # ---- Ablation (if temp > 2500 K, vaporise) ----
        ablation_mask = (self.temp > 2500) & (self.mass > 1e-10)
        if np.any(ablation_mask):
            # Amount vaporised: enough to keep temp at 2500 K
            excess_energy = (self.temp - 2500) * self.mass * Cp_p
            dm = np.minimum(excess_energy / latent_heat_vapor, self.mass * 0.1)  # cap to 10% per step
            dm = np.clip(dm, 0, 1e-6)   # stability limit
            self.mass[ablation_mask] -= dm[ablation_mask]
            self.ablated_mass[ablation_mask] += dm[ablation_mask]
            self.radius[ablation_mask] = (3 * self.mass[ablation_mask] / (4 * np.pi * rho_p)) ** (1/3)
            self.temp[ablation_mask] = 2500   # reset to melting point
            
            # The ablated material adds extra energy to air
            heat_to_air += dm * latent_heat_vapor
        
        # ---- Update altitude ----
        self.z += v_avg * dt
        
        # ---- Store trail energy (for plasma calculation) ----
        # Deposit the heat_to_air into the surrounding bin
        # (We handle this outside the class for simplicity)
        self.trail_energy.append((self.z.copy(), heat_to_air.copy()))
        
        # ---- Deactivate if hit ground or stopped ----
        self.active &= (self.z > 0) & (self.v > 10) & (self.mass > 1e-12)

# ------------------------------------------------------------------
# 3. Main simulation loop (with recording)
# ------------------------------------------------------------------
def run_full_sim(n_particles, scenario, dt=0.02, max_steps=600):
    particles = ParticleSet(n_particles, scenario)
    
    # Grid for recording
    z_bins = np.linspace(0, 150_000, 151)
    z_centers = (z_bins[:-1] + z_bins[1:]) / 2
    dz = z_bins[1] - z_bins[0]
    
    # Storage
    energy_dep_vs_z = np.zeros(len(z_centers))
    plasma_n_e = np.zeros(len(z_centers))
    particle_history = []  # for animation
    
    # Temporary storage for trails
    trail_buffer = []
    
    for step in range(max_steps):
        # Get atmospheric density at particle locations
        rho_at_z = density(particles.z)
        
        # Step particles
        particles.step(dt, rho_at_z)
        
        # Deposit energy into bins (from the trail_buffer collected in step)
        # We'll use the direct heat_to_air from the step – simplified: we compute dKE manually
        # Actually, let's just do it per particle directly in the loop for accuracy.
        # I'll refactor the ParticleSet to return energy deposits per step.
        pass  # (See full integrated code below)

# ------------------------------------------------------------------
# 4. I'll rewrite this as a single, clean, integrated function
#    for the final answer to avoid fragmented logic.
# ------------------------------------------------------------------
