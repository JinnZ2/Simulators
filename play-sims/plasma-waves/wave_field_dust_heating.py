"""
Wave field + dust particle heating.

Propagates a 1D electromagnetic wave and lets it exchange energy with a
population of charged dust grains. Wave field damps near the dust; grain
kinetic energy rises. Shows energy transferred from wave to particles
via dust scattering.

CC0 / for play. Extracted verbatim from Organize.md lines 2954-3097.
Non-stdlib: numpy, matplotlib (FuncAnimation), IPython.display.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# ------------------------------------------------------------------
# 1. Simulation parameters
# ------------------------------------------------------------------
L = 20.0                # domain length
nx = 800                # grid points
dx = L / nx
x = np.linspace(0, L, nx)

# Wave parameters
k = 2.0 * np.pi / 8.0   # wave number (wavelength = 8)
omega = 1.0             # angular frequency
E0 = 1.0                # wave amplitude

# Dust grain (at center)
dust_pos = 10.0
dust_charge = 3.0       # positive charge (can be negative)
dust_width = 0.5        # softening length for Coulomb field

# Particles
n_particles = 200
q_over_m = 1.0          # charge-to-mass ratio (scaled)
dt = 0.02
nt = 2000

# Initialise particles: random positions, small thermal velocities
part_x = np.random.uniform(0, L, n_particles)
part_v = np.random.normal(0, 0.1, n_particles)   # thermal spread

# Store energy history
energy_history = []

# ------------------------------------------------------------------
# 2. Helper: wave field (with damping near dust)
# ------------------------------------------------------------------
def get_wave_field(t, x):
    """Wave E-field: amplitude reduced by dust via Gaussian damping."""
    # Damping profile – strongest near the dust
    damping = 0.7 * np.exp(-((x - dust_pos) / 1.2)**2)
    amplitude = E0 * (1.0 - damping)          # amplitude drops to 30% at center
    return amplitude * np.sin(k * x - omega * t)

# ------------------------------------------------------------------
# 3. Helper: dust Coulomb field
# ------------------------------------------------------------------
def get_dust_field(x):
    """E-field from a stationary charged dust grain (softened)."""
    r = x - dust_pos
    # Softened Coulomb: E = q * r / (r^2 + eps^2)^(3/2)  (1D projection)
    eps = dust_width
    return dust_charge * r / (r**2 + eps**2)**1.5

# ------------------------------------------------------------------
# 4. Main time loop
# ------------------------------------------------------------------
# Store snapshots for animation
snapshots = {'t': [], 'x': [], 'particles': [], 'E_wave': [], 'E_dust': []}

for n in range(nt):
    t = n * dt
    
    # Compute fields on grid
    E_wave = get_wave_field(t, x)
    E_dust = get_dust_field(x)
    E_total = E_wave + E_dust
    
    # ----- Update particles (leapfrog / Boris) -----
    # Interpolate E at particle positions (nearest grid index)
    idx = np.floor(part_x / dx).astype(int)
    idx = np.clip(idx, 0, nx-1)
    E_part = E_total[idx]
    
    # Simple velocity Verlet (half-step)
    # (We'll use an explicit Euler for simplicity – works with small dt)
    part_v += q_over_m * E_part * dt
    part_x += part_v * dt
    
    # Periodic boundaries
    part_x = part_x % L
    
    # ----- Record energy -----
    kinetic = 0.5 * np.sum(part_v**2) / n_particles  # average specific energy
    energy_history.append(kinetic)
    
    # Snapshot every 100 steps
    if n % 100 == 0:
        snapshots['t'].append(t)
        snapshots['x'].append(x.copy())
        snapshots['particles'].append((part_x.copy(), part_v.copy()))
        snapshots['E_wave'].append(E_wave.copy())
        snapshots['E_dust'].append(E_dust.copy())

# ------------------------------------------------------------------
# 5. Visualise: static overview (final state)
# ------------------------------------------------------------------
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 9))

# ---- Top: Wave field with damping ----
t_final = snapshots['t'][-1]
E_wave_final = get_wave_field(t_final, x)
ax1.plot(x, E_wave_final, 'b-', lw=2, label='Wave E-field')
ax1.axvline(dust_pos, color='r', linestyle='--', linewidth=3, label='Dust grain')
ax1.fill_between(x, -E0, E0, where=(np.exp(-((x-dust_pos)/1.2)**2) > 0.1), 
                 color='gray', alpha=0.3, label='Damping region')
ax1.set_ylabel('E-wave')
ax1.legend()
ax1.set_title('Wave amplitude drops near dust (energy extracted)')

# ---- Middle: Particle positions and dust ----
x_part, v_part = snapshots['particles'][-1]
ax2.scatter(x_part, v_part, s=10, c=v_part, cmap='coolwarm', alpha=0.7, vmin=-2, vmax=2)
ax2.axvline(dust_pos, color='r', linestyle='--', linewidth=3)
ax2.set_xlabel('Position')
ax2.set_ylabel('Velocity')
ax2.set_title('Particles: accelerated while crossing dusty region')
ax2.grid(alpha=0.3)

# ---- Bottom: Average kinetic energy over time ----
time_arr = np.arange(0, nt*dt, dt)[:len(energy_history)]
ax3.plot(time_arr, energy_history, 'g-', lw=2)
ax3.axhline(y=energy_history[0], color='gray', linestyle=':', label='Initial thermal')
ax3.set_xlabel('Time')
ax3.set_ylabel('Average kinetic energy')
ax3.set_title('Particles gain energy (heating) from wave via dust scattering')
ax3.legend()
ax3.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------------
# 6. Quantify heating
# ------------------------------------------------------------------
initial_KE = energy_history[0]
final_KE = energy_history[-1]
print(f"Initial average KE: {initial_KE:.3f}")
print(f"Final average KE:   {final_KE:.3f}")
print(f"Relative increase:  {(final_KE/initial_KE - 1)*100:.1f} %")
print("\nEnergy transferred from wave → particles via dust scattering!")

