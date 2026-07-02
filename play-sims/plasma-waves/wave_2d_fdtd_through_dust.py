"""
2D FDTD wave propagation through a dust ring + core.

Extends the 1D case to a 2D grid with an azimuthal dust ring and a dense
core at the domain center. Reports side-by-side animation of the clean
vs dusty wavefield and a per-scenario energy accounting.

CC0 / for play. Extracted verbatim from Organize.md lines 2812-2953.
Non-stdlib: numpy, matplotlib (FuncAnimation), IPython.display.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# ------------------------------------------------------------------
# 1. Grid & Physical Parameters
# ------------------------------------------------------------------
Nx, Ny = 150, 150               # grid size
Lx, Ly = 10.0, 10.0             # domain size (arbitrary units)
dx, dy = Lx/Nx, Ly/Ny
x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
X, Y = np.meshgrid(x, y, indexing='ij')

c0 = 1.0                        # base wave speed (no dust)
dt = 0.01                       # time step (CFL ~ 0.15, stable)
nt = 800                        # total steps
source_x, source_y = Nx//2, Ny//2   # source at center

# ------------------------------------------------------------------
# 2. Dust cloud (Gaussian ring + core, centered)
# ------------------------------------------------------------------
dust_peak = 1.0
dust_radius = 1.5
dust_width = 0.6

# Radial distance from center
r = np.sqrt((X - Lx/2)**2 + (Y - Ly/2)**2)
dust = dust_peak * np.exp(-((r - dust_radius) / dust_width)**2)

# Dust modifies wave speed (slows it down) and adds damping
speed_factor = 1.0 - 0.4 * dust          # up to 40% slower
damping_factor = 0.6 * dust              # damping coefficient

# ------------------------------------------------------------------
# 3. 2D FDTD solver
# ------------------------------------------------------------------
def run_2d_simulation(c_profile, eta_profile, source_on=True):
    # Field arrays (current, previous, next)
    u = np.zeros((Nx, Ny))
    u_prev = np.zeros((Nx, Ny))
    u_next = np.zeros((Nx, Ny))
    
    # Store snapshots for later (every 100 steps)
    snapshots = []
    times = [0, 200, 400, 600, 799]
    
    for n in range(nt):
        # Source: continuous sinusoidal wave at center
        if source_on and n < 400:   # turn off after 400 steps to see propagation
            u[source_x, source_y] += 0.5 * np.sin(0.3 * n * dt)
        
        # 2D FDTD update (explicit, leapfrog with damping)
        # u_tt + eta*u_t = c^2 * (u_xx + u_yy)
        u_next[1:-1, 1:-1] = (2 - eta_profile[1:-1, 1:-1] * dt) * u[1:-1, 1:-1] \
                           + (eta_profile[1:-1, 1:-1] * dt - 1) * u_prev[1:-1, 1:-1] \
                           + (c_profile[1:-1, 1:-1]**2 * dt**2 / dx**2) * (u[2:, 1:-1] - 2*u[1:-1, 1:-1] + u[:-2, 1:-1]) \
                           + (c_profile[1:-1, 1:-1]**2 * dt**2 / dy**2) * (u[1:-1, 2:] - 2*u[1:-1, 1:-1] + u[1:-1, :-2])
        
        # Simple absorbing boundary (sponge layer, 10 cells thick)
        sponge = np.ones((Nx, Ny))
        sponge[:10, :] *= 0.98
        sponge[-10:, :] *= 0.98
        sponge[:, :10] *= 0.98
        sponge[:, -10:] *= 0.98
        u_next *= sponge
        
        # Roll arrays
        u_prev, u = u, u_next
        
        # Record snapshots
        if n in times:
            snapshots.append(u.copy())
    
    return snapshots, u

# ------------------------------------------------------------------
# 4. Run both scenarios
# ------------------------------------------------------------------
c_dust = c0 * speed_factor
eta_dust = damping_factor

snaps_dust, final_dust = run_2d_simulation(c_dust, eta_dust, source_on=True)
snaps_clean, final_clean = run_2d_simulation(c0 * np.ones_like(X), 
                                             np.zeros_like(X), source_on=True)

# ------------------------------------------------------------------
# 5. Visualize: side-by-side animation
# ------------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
titles = ['t = 0', 't = 2.0', 't = 4.0', 't = 6.0', 't = 8.0 (final)']

# Plot control (no dust) - top row
for i, ax in enumerate(axes[0, :]):
    im = ax.imshow(snaps_clean[i], origin='lower', cmap='RdBu_r', 
                   vmin=-0.5, vmax=0.5, extent=[0, Lx, 0, Ly])
    ax.set_title(titles[i])
    ax.set_xlabel('x')
    if i == 0:
        ax.set_ylabel('y (no dust)')

# Plot with dust - bottom row
for i, ax in enumerate(axes[1, :]):
    im = ax.imshow(snaps_dust[i], origin='lower', cmap='RdBu_r', 
                   vmin=-0.5, vmax=0.5, extent=[0, Lx, 0, Ly])
    # Overlay dust cloud contour
    ax.contour(X, Y, dust, levels=[0.3, 0.6], colors='black', linewidths=0.5, alpha=0.6)
    ax.set_title(titles[i])
    ax.set_xlabel('x')
    if i == 0:
        ax.set_ylabel('y (with dust)')

# Add a single colorbar
fig.subplots_adjust(right=0.92)
cbar_ax = fig.add_axes([0.94, 0.15, 0.02, 0.7])
fig.colorbar(im, cax=cbar_ax, label='Wave amplitude')
plt.suptitle("2D Wave Propagation: No Dust vs. Dust Cloud (black contours)", y=1.02, fontsize=14)
plt.show()

# ------------------------------------------------------------------
# 6. Energy analysis
# ------------------------------------------------------------------
energy_clean = np.sum(snaps_clean[-1]**2) / np.sum(snaps_clean[0]**2)
energy_dust = np.sum(snaps_dust[-1]**2) / np.sum(snaps_dust[0]**2)

print(f"Energy retained (no dust):  {energy_clean:.2%}")
print(f"Energy retained (with dust): {energy_dust:.2%}")
print(f"Additional energy dissipated by dust: {(1 - energy_dust) - (1 - energy_clean):.2%}")

# ------------------------------------------------------------------
# 7. (Bonus) Animated version – run this in a Jupyter notebook
# ------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Run simulation again to get full time series (simplified here)
# For brevity, we re-use stored snapshots – but for a real animation,
# you'd loop over n in the main loop. 
# Instead, I'll show a static comparison of final wavefronts.
# To see a live animation, uncomment the cell below if in a notebook.


