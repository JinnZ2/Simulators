"""
Earth heating by space dust & debris — integrated fireball simulation.

The clean re-write of meteor_heating_bins.py: particles descend under
drag, deposit heat via ablation, and the atmospheric column tracks
per-bin temperature rise. Baseline (Interplanetary Dust) vs elevated-flux
(Asteroid Belt Debris) scenarios; two-panel animation of the fireball
cascade.

CC0 / for play. Extracted verbatim from Organize.md lines 3738-4012.
Non-stdlib: numpy, matplotlib (FuncAnimation), IPython.display.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# ===================================================================
#                  EARTH HEATING BY SPACE DUST & DEBRIS
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

def density(z):
    return rho0 * np.exp(-np.maximum(z, 0) / H)

# -------------------------------------------------------------------
# Particle set
# -------------------------------------------------------------------
class ParticleSet:
    def __init__(self, n, scenario):
        log_m = np.random.uniform(-7, 1.7, n)
        self.m = 10**log_m
        self.r = (3 * self.m / (4 * np.pi * rho_p)) ** (1/3)
        self.z = np.random.uniform(120_000, 150_000, n)
        if scenario == 'normal':
            self.v = np.random.uniform(12_000, 40_000, n)
        else:
            self.v = np.random.uniform(7_000, 45_000, n)
        self.T = np.full(n, 300.0)
        self.active = np.ones(n, dtype=bool)
        self.energy_to_air = np.zeros(n)   # per step

    def step(self, dt):
        rho = density(self.z)
        A = np.pi * self.r**2
        v_old = self.v.copy()
        
        # Drag
        a = -0.5 * Cd * rho * v_old**2 * A / self.m
        self.v += a * dt
        self.v = np.maximum(self.v, 0.0)
        v_avg = v_old + 0.5 * a * dt
        
        # Kinetic energy loss
        dKE = 0.5 * self.m * (v_old**2 - self.v**2)
        
        # Split: 30% heats particle, 70% directly heats air
        heat_p = 0.3 * dKE
        heat_air = 0.7 * dKE
        
        # Particle temperature
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
            heat_air += dm * latent_heat_vapor   # vaporisation adds extra heat to air
        
        # Update altitude
        self.z += v_avg * dt
        self.energy_to_air = heat_air
        
        # Deactivate
        self.active &= (self.z > 0) & (self.v > 5) & (self.m > 1e-13)

# -------------------------------------------------------------------
# Main run function
# -------------------------------------------------------------------
def run_simulation(n_particles, scenario, dt=0.02, steps=400):
    particles = ParticleSet(n_particles, scenario)
    z_bins = np.linspace(0, 150_000, 151)
    z_centers = (z_bins[:-1] + z_bins[1:]) / 2
    dz = z_bins[1] - z_bins[0]
    
    energy_dep = np.zeros(len(z_centers))
    plasma_n = np.zeros(len(z_centers))
    
    # For animation
    history = {'z': [], 'v': [], 'm': [], 'T': [], 'r': [], 'step': []}
    
    for step in range(steps):
        particles.step(dt)
        
        # Deposit energy into bins
        active = particles.active
        if np.any(active):
            idx = np.floor(particles.z[active] / dz).astype(int)
            idx = np.clip(idx, 0, len(z_centers)-1)
            for i, e in zip(idx, particles.energy_to_air[active]):
                energy_dep[i] += e
                # Ionisation: 1 J = 1e17 electrons (simple scaling)
                plasma_n[i] += e * 1e17 / (dz * np.pi * (100)**2)  # per m³
        
        # Record for animation (downsample)
        if step % 5 == 0:
            history['z'].append(particles.z.copy())
            history['v'].append(particles.v.copy())
            history['m'].append(particles.m.copy())
            history['T'].append(particles.T.copy())
            history['r'].append(particles.r.copy())
            history['step'].append(step * dt)
    
    return energy_dep, plasma_n, z_centers, history

# -------------------------------------------------------------------
# Run two scenarios
# -------------------------------------------------------------------
print("🔥 Running normal dust flux...")
E_norm, n_norm, z, hist_norm = run_simulation(2000, 'normal', steps=350)

print("💥 Running mega debris storm...")
E_storm, n_storm, _, hist_storm = run_simulation(8000, 'storm', steps=350)

# -------------------------------------------------------------------
# Global heating estimate
# -------------------------------------------------------------------
earth_area = 4 * np.pi * R_earth**2
total_E_norm = np.sum(E_norm) * earth_area      # Joules
total_E_storm = np.sum(E_storm) * earth_area

dT_global_norm = total_E_norm / (M_atm * Cp_air)
dT_global_storm = total_E_storm / (M_atm * Cp_air)

# -------------------------------------------------------------------
# Plasma & radio effects (critical frequency)
# -------------------------------------------------------------------
def critical_freq(ne):
    # fp = 8980 * sqrt(ne)  (ne in m^-3)
    return 8980 * np.sqrt(np.maximum(ne, 0))

fp_norm = critical_freq(n_norm)
fp_storm = critical_freq(n_storm)

# -------------------------------------------------------------------
# PLOTTING (static overview)
# -------------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# Row 0: Normal
ax = axes[0,0]
ax.barh(z/1000, E_norm, height=1, color='skyblue')
ax.set_title('Normal: Energy / km')
ax.set_xlabel('J per m² column')

ax = axes[0,1]
ax.plot(z/1000, fp_norm/1e6, 'b-')
ax.set_title('Normal: Plasma freq (MHz)')
ax.set_xlabel('Altitude (km)')
ax.grid(alpha=0.3)

ax = axes[0,2]
ax.barh(z/1000, n_norm, height=1, color='lightgreen')
ax.set_title('Normal: Electron density')
ax.set_xlabel('e⁻ / m³')

# Row 1: Storm
ax = axes[1,0]
ax.barh(z/1000, E_storm, height=1, color='crimson')
ax.set_title('Storm: Energy / km')
ax.set_xlabel('J per m² column')

ax = axes[1,1]
ax.plot(z/1000, fp_storm/1e6, 'r-')
ax.set_title('Storm: Plasma freq (MHz)')
ax.set_xlabel('Altitude (km)')
ax.grid(alpha=0.3)

ax = axes[1,2]
ax.barh(z/1000, n_storm, height=1, color='darkred')
ax.set_title('Storm: Electron density')
ax.set_xlabel('e⁻ / m³')

plt.tight_layout()
plt.suptitle('Atmospheric Heating & Plasma by Space Influx', y=1.02, fontsize=14)
plt.show()

# -------------------------------------------------------------------
# Global & radio summary
# -------------------------------------------------------------------
print("\n" + "="*60)
print("🌍 GLOBAL HEATING (entire atmosphere)")
print("="*60)
print(f"Normal flux:  {total_E_norm/1e18:.3f} EJ (exajoules) → ΔT = {dT_global_norm*1000:.3f} mK")
print(f"Storm:        {total_E_storm/1e18:.3f} EJ → ΔT = {dT_global_storm*1000:.3f} mK")
print("\n📡 RADIO EFFECTS (ionosphere blackout)")
print("-"*60)
print(f"Normal: peak plasma frequency = {np.max(fp_norm)/1e6:.2f} MHz (blocks shortwave radio)")
print(f"Storm:  peak plasma frequency = {np.max(fp_storm)/1e6:.2f} MHz (blocks FM/VHF!)")
print("="*60)

# -------------------------------------------------------------------
# ANIMATION – Fireballs falling & burning
# -------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
ax1.set_xlim(-100, 100)
ax1.set_ylim(0, 150)
ax1.set_xlabel('Horizontal spread (km)')
ax1.set_ylabel('Altitude (km)')
ax1.set_title('Particles burning up')
ax2.set_xlim(0, 150)
ax2.set_ylim(0, 150)
ax2.set_xlabel('Altitude (km)')
ax2.set_title('Cumulative energy deposition')
ax2.grid(alpha=0.3)

# Use the storm history for animation (more action)
scat = ax1.scatter([], [], s=[], c=[], cmap='hot', vmin=300, vmax=3500, alpha=0.8)
# Energy line
line, = ax2.plot([], [], 'r-', lw=2)
# We'll accumulate energy per bin during animation

# Pre-compute cumulative energy for animation
cumulative_E = np.cumsum(E_storm)  # just for display

def init():
    scat.set_offsets(np.empty((0, 2)))
    scat.set_sizes([])
    scat.set_array([])
    line.set_data([], [])
    return scat, line

# We need to extract frames for the animation
# Let's use the stored history
frames = len(hist_storm['z'])

def animate(i):
    z_i = hist_storm['z'][i]
    m_i = hist_storm['m'][i]
    T_i = hist_storm['T'][i]
    v_i = hist_storm['v'][i]
    
    # Select active particles (m > 0)
    mask = m_i > 1e-14
    if np.any(mask):
        z_plot = z_i[mask] / 1000
        # Random horizontal spread
        x_plot = np.random.uniform(-50, 50, len(z_plot))
        sizes = np.clip(m_i[mask] * 1000, 5, 200)
        temps = T_i[mask]
        scat.set_offsets(np.column_stack([x_plot, z_plot]))
        scat.set_sizes(sizes)
        scat.set_array(temps)
    else:
        scat.set_offsets(np.empty((0, 2)))
    
    # Update energy deposition profile (show it building up)
    # We'll just show the final line for simplicity, or animate cumulative
    line.set_data(z/1000, E_storm * (i / frames))
    ax2.set_title(f'Energy deposited (t = {hist_storm["step"][i]:.1f} s)')
    
    return scat, line

ani = FuncAnimation(fig, animate, init_func=init, frames=frames, interval=50, blit=False)

# To display in Jupyter:
# HTML(ani.to_jshtml())
# Or save:
# ani.save('fireballs.gif', writer='pillow', fps=20)

plt.show()
print("\n🎬 To see the animation, run the cell above in a Jupyter notebook,")
print("or use: ani.save('fireballs.gif') to save as a GIF.")
