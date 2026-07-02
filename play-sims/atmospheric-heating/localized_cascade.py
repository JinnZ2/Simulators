"""
Earth heating with localized cascade events.

Adds a "cascade" trigger: once local heating in an altitude bin exceeds
threshold, further mass shifts thermally-expanded density downward,
increasing drag and re-radiating heat in a runaway loop. Compares
normal-flux vs elevated-flux scenarios and highlights the cascade
signature.

CC0 / for play. Extracted verbatim from Organize.md lines 4014-4352.
Non-stdlib: numpy, matplotlib (FuncAnimation), IPython.display.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# ===================================================================
#          EARTH HEATING WITH LOCALIZED CASCADE EVENTS
# ===================================================================

# Constants
R_earth = 6.371e6
Cp_air = 1000.0
rho_p = 3000.0
M_atm = 5.148e18
latent_heat_vapor = 10e6
H = 7500.0
rho0 = 1.225
Cd = 0.47
T0_air = 250.0          # average upper-atmosphere temperature (K)

# -------------------------------------------------------------------
# 1. Dynamic atmosphere (with thermal feedback)
# -------------------------------------------------------------------
class AtmoCascade:
    def __init__(self, z_centers):
        self.z = z_centers
        self.T_air = np.full(len(z_centers), T0_air)
        self.rho_factor = np.ones(len(z_centers))  # 1.0 = normal
        self.threshold_energy = 5e5                 # J per bin to trigger feedback
        self.cascade_active = False
        
    def density(self, z):
        """Base density with thermal expansion scaling."""
        base = rho0 * np.exp(-np.maximum(z, 0) / H)
        # Interpolate rho_factor onto particle positions
        idx = np.clip(np.floor(z / 1000).astype(int), 0, len(self.z)-1)
        factor = self.rho_factor[idx]
        return base * factor
    
    def deposit_heat(self, energy_per_bin):
        """Update temperature and rho_factor based on energy input."""
        # Convert energy to temperature rise (per m³ column, 1 km height)
        mass_air_per_bin = rho0 * np.exp(-self.z / H) * 1000.0  # kg per m² slice
        dT = np.zeros(len(energy_per_bin))
        mask = mass_air_per_bin > 1e-12
        dT[mask] = energy_per_bin[mask] / (mass_air_per_bin[mask] * Cp_air)
        
        self.T_air += dT
        
        # Thermal expansion: rho ~ 1/T
        self.rho_factor = T0_air / np.maximum(self.T_air, 50.0)
        self.rho_factor = np.clip(self.rho_factor, 0.1, 2.0)  # limit runaway
        
        # Check for cascade trigger
        if np.any(dT > 50.0):
            self.cascade_active = True
            hottest_layer = np.argmax(dT)
            print(f"🔥 CASCADE TRIGGERED at {self.z[hottest_layer]/1000:.0f} km (ΔT = {dT[hottest_layer]:.1f} K)")
        
        return dT

# -------------------------------------------------------------------
# 2. Particle set with fragmentation
# -------------------------------------------------------------------
class ParticleSet:
    def __init__(self, n, scenario, z_centers):
        self.z_centers = z_centers
        log_m = np.random.uniform(-7, 1.7, n)
        self.m = 10**log_m
        self.r = (3 * self.m / (4 * np.pi * rho_p)) ** (1/3)
        self.z = np.random.uniform(120_000, 150_000, n)
        if scenario == 'normal':
            self.v = np.random.uniform(12_000, 35_000, n)
        else:  # storm
            self.v = np.random.uniform(10_000, 45_000, n)
        self.T = np.full(n, 300.0)
        self.active = np.ones(n, dtype=bool)
        self.energy_to_air = np.zeros(n)
        self.fragments = np.zeros(n, dtype=int)   # 0 = original, >0 = fragment
        
    def step(self, dt, atmo):
        rho = atmo.density(self.z)
        A = np.pi * self.r**2
        v_old = self.v.copy()
        
        # Dynamic pressure (for fragmentation)
        q_dyn = 0.5 * rho * v_old**2
        frag_threshold = 1e6   # Pa – typical asteroid strength
        
        # ---- Fragmentation cascade ----
        frag_mask = (q_dyn > frag_threshold) & (self.m > 0.5) & (self.r > 0.05) & self.active
        if np.any(frag_mask):
            n_new_frags = 0
            new_m = []
            new_r = []
            new_z = []
            new_v = []
            new_T = []
            # For each fragmenting particle, create 3–8 fragments
            for i in np.where(frag_mask)[0]:
                n_frag = np.random.randint(3, 8)
                # Mass splits randomly, but total conserved
                mass_frac = np.random.dirichlet(np.ones(n_frag)) * self.m[i]
                for mf in mass_frac:
                    if mf > 1e-6:
                        new_m.append(mf)
                        new_r.append((3 * mf / (4 * np.pi * rho_p)) ** (1/3))
                        # Slight horizontal / vertical spread
                        new_z.append(self.z[i] + np.random.uniform(-200, 200))
                        new_v.append(self.v[i] * np.random.uniform(0.85, 0.95))  # slower
                        new_T.append(300.0)
                        n_new_frags += 1
                # Mark original as inactive (it has broken up)
                self.active[i] = False
                self.energy_to_air[i] = 0.0
            
            # Append new fragments to the arrays
            if n_new_frags > 0:
                self.m = np.concatenate([self.m, np.array(new_m)])
                self.r = np.concatenate([self.r, np.array(new_r)])
                self.z = np.concatenate([self.z, np.array(new_z)])
                self.v = np.concatenate([self.v, np.array(new_v)])
                self.T = np.concatenate([self.T, np.array(new_T)])
                self.active = np.concatenate([self.active, np.ones(n_new_frags, dtype=bool)])
                self.energy_to_air = np.concatenate([self.energy_to_air, np.zeros(n_new_frags)])
                self.fragments = np.concatenate([self.fragments, np.ones(n_new_frags, dtype=int)])
        
        # ---- Drag (recompute with updated arrays) ----
        rho = atmo.density(self.z)
        A = np.pi * self.r**2
        v_old = self.v.copy()
        a = -0.5 * Cd * rho * v_old**2 * A / self.m
        self.v += a * dt
        self.v = np.maximum(self.v, 0.0)
        v_avg = v_old + 0.5 * a * dt
        
        # Energy loss
        dKE = 0.5 * self.m * (v_old**2 - self.v**2)
        heat_air = 0.8 * dKE   # most goes to air
        heat_p = 0.2 * dKE
        
        self.T += heat_p / (self.m * 1000.0 + 1e-15)
        
        # Ablation
        ablating = (self.T > 2500) & (self.m > 1e-12)
        if np.any(ablating):
            excess = (self.T - 2500) * self.m * 1000.0
            dm = np.minimum(excess / latent_heat_vapor, self.m * 0.05)
            dm = np.clip(dm, 0, 1e-6)
            self.m[ablating] -= dm[ablating]
            self.r[ablating] = (3 * self.m[ablating] / (4 * np.pi * rho_p)) ** (1/3)
            self.T[ablating] = 2500
            heat_air[ablating] += dm[ablating] * latent_heat_vapor
        
        # Update position
        self.z += v_avg * dt
        self.energy_to_air = heat_air
        
        # Deactivate if dead
        self.active &= (self.z > 0) & (self.v > 5) & (self.m > 1e-13)

# -------------------------------------------------------------------
# 3. Main simulation with cascade tracking
# -------------------------------------------------------------------
def run_cascade_sim(n_particles, scenario, dt=0.02, steps=450):
    z_bins = np.linspace(0, 150_000, 151)
    z_centers = (z_bins[:-1] + z_bins[1:]) / 2
    dz = z_bins[1] - z_bins[0]
    
    atmo = AtmoCascade(z_centers)
    particles = ParticleSet(n_particles, scenario, z_centers)
    
    energy_dep = np.zeros(len(z_centers))
    plasma_n = np.zeros(len(z_centers))
    dT_history = []
    
    # History for animation
    hist_z, hist_m, hist_T = [], [], []
    
    for step in range(steps):
        # Step particles
        particles.step(dt, atmo)
        
        # Deposit energy into bins
        if np.any(particles.active):
            idx = np.floor(particles.z[particles.active] / dz).astype(int)
            idx = np.clip(idx, 0, len(z_centers)-1)
            energy_vals = particles.energy_to_air[particles.active]
            for i, e in zip(idx, energy_vals):
                energy_dep[i] += e
                plasma_n[i] += e * 1e17 / (dz * np.pi * (50)**2)
        
        # Update atmospheric state (cascade feedback)
        dT = atmo.deposit_heat(energy_dep * 0.1)   # spread over time for stability
        dT_history.append(dT.copy())
        
        # Record for animation
        if step % 5 == 0:
            hist_z.append(particles.z[particles.active].copy())
            hist_m.append(particles.m[particles.active].copy())
            hist_T.append(particles.T[particles.active].copy())
    
    return energy_dep, plasma_n, z_centers, atmo, dT_history, hist_z, hist_m, hist_T

# -------------------------------------------------------------------
# 4. Run scenarios
# -------------------------------------------------------------------
print("🌊 Running with cascade feedback (normal flux)...")
E_norm, n_norm, z, atmo_norm, dT_norm, hz_norm, hm_norm, hT_norm = run_cascade_sim(2000, 'normal')

print("\n🔥 Running MEGA-STORM with cascade feedback...")
E_storm, n_storm, _, atmo_storm, dT_storm, hz_storm, hm_storm, hT_storm = run_cascade_sim(8000, 'storm')

# -------------------------------------------------------------------
# 5. Global heating
# -------------------------------------------------------------------
earth_area = 4 * np.pi * R_earth**2
total_E_storm = np.sum(E_storm) * earth_area
dT_global_storm = total_E_storm / (M_atm * Cp_air)

print(f"\n🌍 Global ΔT (storm with cascade): {dT_global_storm*1000:.3f} mK")
print(f"🔥 Cascade active: {atmo_storm.cascade_active}")

# -------------------------------------------------------------------
# 6. PLOT: Cascade visualisation (Altitude vs Time heat map)
# -------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# ---- Top Left: Energy deposition profile ----
ax = axes[0,0]
ax.barh(z/1000, E_storm, height=1, color='crimson', alpha=0.7, label='Storm')
ax.barh(z/1000, E_norm, height=1, color='skyblue', alpha=0.5, label='Normal')
ax.set_xlabel('Energy (J per m² column)')
ax.set_ylabel('Altitude (km)')
ax.set_title('Energy Deposition with Cascade Feedback')
ax.legend()
ax.grid(alpha=0.3)

# ---- Top Right: Thermal feedback (density reduction) ----
ax = axes[0,1]
ax.plot(z/1000, np.ones_like(z), 'k--', label='No heating (1.0)')
ax.plot(z/1000, atmo_storm.rho_factor, 'r-', lw=2, label='After storm')
ax.plot(z/1000, atmo_norm.rho_factor, 'b-', lw=2, label='After normal flux')
ax.set_xlabel('Altitude (km)')
ax.set_ylabel('Density factor (ρ/ρ₀)')
ax.set_title('Thermal Feedback: Density Reduction Cascade')
ax.legend()
ax.grid(alpha=0.3)
ax.set_ylim(0.5, 1.1)

# ---- Bottom Left: Runaway cascade progression (time vs altitude) ----
ax = axes[1,0]
# Convert dT_history to a 2D array
dT_arr = np.array(dT_storm).T  # shape: (150 bins, n_steps)
# Show a heatmap of the temperature rise over time
extent = [0, len(dT_storm)*0.02, 0, 150]  # time (s), altitude (km)
im = ax.imshow(dT_arr, aspect='auto', origin='lower', cmap='hot', 
               extent=extent, vmin=0, vmax=80)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Altitude (km)')
ax.set_title('Cascade Progression: ΔT (K) over time')
plt.colorbar(im, ax=ax, label='Temperature rise (K)')
# Mark when cascade was triggered
ax.axvline(x=2.0, color='cyan', linestyle='--', label='Cascade trigger (~2s)')
ax.legend()

# ---- Bottom Right: Fragment count & total mass evolution ----
ax = axes[1,1]
# We'll manually compute fragment counts from the history
frag_counts = []
total_mass = []
for i in range(len(hz_storm)):
    z_i = hz_storm[i]
    m_i = hm_storm[i]
    if len(z_i) > 0:
        total_mass.append(np.sum(m_i))
    else:
        total_mass.append(0)
    # Fragments are >0.5m wide? We just estimate >1g
    if len(m_i) > 0:
        frag_counts.append(np.sum(m_i < 0.1))  # small = fragment
    else:
        frag_counts.append(0)

time_axis = np.arange(0, len(frag_counts)*0.1, 0.1)[:len(frag_counts)]
ax.plot(time_axis, np.array(total_mass)/1e3, 'r-', label='Total mass (kg)')
ax.plot(time_axis, frag_counts, 'b-', label='Fragment count')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Mass (kg) / Count')
ax.set_title('Fragmentation Cascade')
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.suptitle('LOCALIZED HEATING CASCADE EVENTS: Thermal Runaway & Fragmentation', y=1.02, fontsize=14)
plt.show()

# -------------------------------------------------------------------
# 7. Critical cascade detection
# -------------------------------------------------------------------
print("\n" + "="*60)
print("💥 CASCADE ANALYSIS")
print("="*60)
# Find the altitude where density dropped most
min_rho_idx = np.argmin(atmo_storm.rho_factor)
print(f"Maximum density reduction at {z[min_rho_idx]/1000:.0f} km")
print(f"→ Density dropped to {atmo_storm.rho_factor[min_rho_idx]*100:.1f}% of normal")
print(f"→ Local temperature rise: {atmo_storm.T_air[min_rho_idx] - T0_air:.1f} K")

# Check for runaway (if density drop leads to deeper penetration)
# Compare energy peak altitudes between normal and storm
peak_norm = z[np.argmax(E_norm)] / 1000
peak_storm = z[np.argmax(E_storm)] / 1000
print(f"Peak heating altitude (normal): {peak_norm:.0f} km")
print(f"Peak heating altitude (storm) : {peak_storm:.0f} km")
if peak_storm < peak_norm:
    print("🚨 CASCADE SHIFT: Heating front moved DOWNWARD by {:.0f} km!".format(peak_norm - peak_storm))
    print("   This is a positive feedback loop – thermal expansion allows")
    print("   deeper penetration, depositing energy lower, further reducing")
    print("   density there. This is the 'localized heating cascade' in action!")
else:
    print("✅ No runaway cascade detected – atmosphere remained stable.")
print("="*60)

# -------------------------------------------------------------------
# 8. (Bonus) Animation of the cascade wave
# -------------------------------------------------------------------
# If you want to animate the heatmap, uncomment:
# fig, ax = plt.subplots()
# im = ax.imshow(dT_arr, aspect='auto', origin='lower', cmap='hot', 
#                extent=extent, vmin=0, vmax=80)
# ax.set_xlabel('Time (s)'); ax.set_ylabel('Altitude (km)')
# def update(frame):
#     im.set_data(dT_arr[:, :frame])
#     return im,
# ani = FuncAnimation(fig, update, frames=len(dT_storm), interval=50)
# HTML(ani.to_jshtml())


