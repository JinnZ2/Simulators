"""
1D FDTD wave propagation through a dust cloud.

Simulates u_tt + eta(x) u_t = c(x)^2 u_xx over a domain with a Gaussian
dust cloud that both slows the wave (lower c) and damps it (higher eta).
Runs a WITH-dust and WITHOUT-dust control, then reports the fractional
energy lost to the cloud.

CC0 / for play. Extracted verbatim from legacy/Organize.md lines 2703-2811.
Non-stdlib: numpy, matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# 1. Simulation parameters
# ----------------------------------------------------------------------
L = 10.0                # domain length
nx = 1000               # number of grid points
dx = L / nx
x = np.linspace(0, L, nx)

c0 = 1.0                # base wave speed (no dust)
eta0 = 0.0              # base damping (no dust)
dt = 0.005              # time step (CFL = c0*dt/dx = 0.5, stable)

nt = 800                # total time steps

# ----------------------------------------------------------------------
# 2. Dust density profile (Gaussian cloud centered at x=5)
# ----------------------------------------------------------------------
dust_peak = 1.0
dust_width = 0.8
dust = dust_peak * np.exp(-((x - 5.0) / dust_width)**2)

# Dust changes the local wave speed (slows it) and adds damping
speed_factor = 1.0 - 0.3 * dust       # speed reduction up to 30%
damping_factor = 0.8 * dust           # damping coefficient

# ----------------------------------------------------------------------
# 3. FDTD solver for: u_tt + eta(x) u_t = c(x)^2 u_xx
# ----------------------------------------------------------------------
def run_simulation(c_profile, eta_profile):
    u = np.zeros(nx)          # current time step
    u_prev = np.zeros(nx)     # previous time step
    u_next = np.zeros(nx)
    
    # Initial condition: Gaussian pulse at x=1.0, moving right
    u = 0.5 * np.exp(-((x - 1.0) / 0.15)**2)
    u_prev = u.copy()
    
    # Store snapshots
    snapshots = []
    times = [0, 300, 600]
    
    for n in range(nt):
        # FDTD update (leapfrog with damping)
        u_next[1:-1] = (2 - eta_profile[1:-1] * dt) * u[1:-1] \
                     + (eta_profile[1:-1] * dt - 1) * u_prev[1:-1] \
                     + (c_profile[1:-1]**2 * dt**2 / dx**2) * (u[2:] - 2*u[1:-1] + u[:-2])
        
        # Absorbing boundaries (simple sponge)
        u_next[0] = u_next[1] * 0.99
        u_next[-1] = u_next[-2] * 0.99
        
        u_prev, u = u, u_next
        
        if n in times:
            snapshots.append(u.copy())
    
    return snapshots

# ----------------------------------------------------------------------
# 4. Run two scenarios: WITH dust and WITHOUT dust (control)
# ----------------------------------------------------------------------
c_dust = c0 * speed_factor
eta_dust = damping_factor

snaps_dust = run_simulation(c_dust, eta_dust)
snaps_clean = run_simulation(c0 * np.ones_like(x), np.zeros_like(x))

# ----------------------------------------------------------------------
# 5. Plot results
# ----------------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(15, 6))
titles = ['t = 0', 't = 1.5 (before dust)', 't = 3.0 (through dust)']

for row, (snaps, label) in enumerate([(snaps_clean, 'No Dust (Control)'),
                                      (snaps_dust, 'With Dust')]):
    for col in range(3):
        ax = axes[row, col]
        ax.plot(x, snaps[col], lw=2)
        if row == 1:
            ax.fill_between(x, -0.5, 0.5, where=(dust > 0.1), 
                            color='gray', alpha=0.3, label='Dust cloud')
        ax.set_ylim(-0.6, 0.6)
        ax.set_xlabel('Distance')
        if col == 0:
            ax.set_ylabel('Wave amplitude')
        if row == 0:
            ax.set_title(titles[col])
        else:
            ax.set_title(titles[col] + ' (damped)')
        if row == 1 and col == 2:
            ax.legend()

plt.tight_layout()
plt.suptitle("Effect of Cosmic Dust on Plasma Wave Propagation", y=1.02, fontsize=14)
plt.show()

# ----------------------------------------------------------------------
# 6. Quantify energy loss
# ----------------------------------------------------------------------
energy_clean = np.sum(snaps_clean[-1]**2) / np.sum(snaps_clean[0]**2)
energy_dust = np.sum(snaps_dust[-1]**2) / np.sum(snaps_dust[0]**2)

print(f"Energy retained (no dust):  {energy_clean:.2%}")
print(f"Energy retained (with dust): {energy_dust:.2%}")
print(f"Additional energy lost to dust: {(1 - energy_dust) - (1 - energy_clean):.2%}")

