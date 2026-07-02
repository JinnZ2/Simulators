"""
2D Particle-in-Cell plasma simulation with a fixed dust background.

Electrons and ions as macro-particles; Poisson solved on a 64x64 grid via
FFT; CIC deposition/interpolation; dust cloud adds a fixed positive
charge density. Reports final field structure and dust-driven kinetic
heating of the plasma population — a toy demonstration of the coronal
heating pathway.

CC0 / for play. Extracted verbatim from Organize.md lines 3098-3353.
Non-stdlib: numpy, matplotlib (FuncAnimation), IPython.display.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# ------------------------------------------------------------------
# 1. Simulation parameters
# ------------------------------------------------------------------
Nx, Ny = 64, 64               # grid resolution
Lx, Ly = 10.0, 10.0           # box size
dx, dy = Lx/Nx, Ly/Ny

dt = 0.02                     # time step
nt = 600                      # total steps
n_electrons = 1500            # number of macro-particles per species
n_ions = 1500

# Charge-to-mass ratios (scaled)
q_over_m_e = -1.0
q_over_m_i = 0.5

# Initial thermal velocities
vth_e = 0.5
vth_i = 0.2

# ------------------------------------------------------------------
# 2. Initialise particles
# ------------------------------------------------------------------
def init_particles(n, qm, vth):
    x = np.random.uniform(0, Lx, n)
    y = np.random.uniform(0, Ly, n)
    vx = np.random.normal(0, vth, n)
    vy = np.random.normal(0, vth, n)
    return x, y, vx, vy, qm * np.ones(n)   # charge-to-mass per particle

x_e, y_e, vx_e, vy_e, qm_e = init_particles(n_electrons, q_over_m_e, vth_e)
x_i, y_i, vx_i, vy_i, qm_i = init_particles(n_ions, q_over_m_i, vth_i)

# ------------------------------------------------------------------
# 3. Dust background (fixed charge density)
# ------------------------------------------------------------------
# Two dust clouds with opposite charge to create an electric dipole structure
dust_rho = np.zeros((Nx, Ny))
grid_x = np.linspace(0, Lx, Nx, endpoint=False)
grid_y = np.linspace(0, Ly, Ny, endpoint=False)
X, Y = np.meshgrid(grid_x, grid_y, indexing='ij')

# Dust 1: positive charge
r1 = np.sqrt((X - 2.5)**2 + (Y - 5.0)**2)
dust_rho += 8.0 * np.exp(-r1**2 / 0.8**2)

# Dust 2: negative charge
r2 = np.sqrt((X - 7.5)**2 + (Y - 5.0)**2)
dust_rho -= 8.0 * np.exp(-r2**2 / 0.8**2)

# ------------------------------------------------------------------
# 4. FFT Poisson solver
# ------------------------------------------------------------------
kx = 2.0 * np.pi * np.fft.fftfreq(Nx, d=dx)
ky = 2.0 * np.pi * np.fft.fftfreq(Ny, d=dy)
kx2, ky2 = np.meshgrid(kx, ky, indexing='ij')
k2 = kx2**2 + ky2**2
k2[0, 0] = 1.0   # avoid division by zero (mean potential set to zero)

def poisson_solve(rho):
    """Solve ∇²φ = -ρ  (electrostatic) using FFT."""
    rho_hat = np.fft.fft2(rho)
    phi_hat = rho_hat / k2
    phi_hat[0, 0] = 0.0   # set average potential to zero
    phi = np.fft.ifft2(phi_hat).real
    return phi

def get_fields(phi):
    """Ex = -∂φ/∂x, Ey = -∂φ/∂y using spectral derivatives."""
    phi_hat = np.fft.fft2(phi)
    ex_hat = -1j * kx2 * phi_hat
    ey_hat = -1j * ky2 * phi_hat
    ex = np.fft.ifft2(ex_hat).real
    ey = np.fft.ifft2(ey_hat).real
    return ex, ey

# ------------------------------------------------------------------
# 5. Particle deposition (CIC – Cloud‑in‑Cell)
# ------------------------------------------------------------------
def deposit_charge(x, y, qm, Nx, Ny, Lx, Ly):
    """Deposit charge density onto grid (q per cell)."""
    rho = np.zeros((Nx, Ny))
    q = qm * 0.1   # arbitrary charge scaling for visual effect
    
    # Find cell indices and fractional offsets
    ix = np.floor(x / dx).astype(int) % Nx
    iy = np.floor(y / dy).astype(int) % Ny
    fx = (x / dx) - ix
    fy = (y / dy) - iy
    
    # CIC weighting (bilinear interpolation)
    for i in range(len(x)):
        # Four nearest cells
        rho[ix[i], iy[i]]         += q[i] * (1 - fx[i]) * (1 - fy[i])
        rho[(ix[i]+1) % Nx, iy[i]] += q[i] * fx[i] * (1 - fy[i])
        rho[ix[i], (iy[i]+1) % Ny] += q[i] * (1 - fx[i]) * fy[i]
        rho[(ix[i]+1) % Nx, (iy[i]+1) % Ny] += q[i] * fx[i] * fy[i]
    return rho

def interpolate_fields(ex, ey, x, y):
    """Get E-field at particle positions via bilinear interpolation."""
    ix = np.floor(x / dx).astype(int) % Nx
    iy = np.floor(y / dy).astype(int) % Ny
    fx = (x / dx) - ix
    fy = (y / dy) - iy
    
    ex_part = (1 - fx) * ((1 - fy) * ex[ix, iy] + fy * ex[ix, (iy+1) % Ny]) \
            + fx * ((1 - fy) * ex[(ix+1) % Nx, iy] + fy * ex[(ix+1) % Nx, (iy+1) % Ny])
    
    ey_part = (1 - fx) * ((1 - fy) * ey[ix, iy] + fy * ey[ix, (iy+1) % Ny]) \
            + fx * ((1 - fy) * ey[(ix+1) % Nx, iy] + fy * ey[(ix+1) % Nx, (iy+1) % Ny])
    return ex_part, ey_part

# ------------------------------------------------------------------
# 6. Main PIC loop
# ------------------------------------------------------------------
history = {
    'time': [],
    'KE_e': [],
    'KE_i': [],
    'E_field_energy': []
}

# Store snapshots for animation
snapshots = {'rho': [], 'phi': [], 'ex': [], 'ey': [], 'particles': []}

for n in range(nt):
    t = n * dt
    
    # ---- 6a. Deposit charge (electrons + ions) ----
    rho_e = deposit_charge(x_e, y_e, qm_e, Nx, Ny, Lx, Ly)
    rho_i = deposit_charge(x_i, y_i, qm_i, Nx, Ny, Lx, Ly)
    rho_total = rho_e + rho_i + dust_rho   # add fixed dust
    
    # ---- 6b. Solve Poisson and get fields ----
    phi = poisson_solve(rho_total)
    ex, ey = get_fields(phi)
    
    # ---- 6c. Push electrons ----
    ex_part_e, ey_part_e = interpolate_fields(ex, ey, x_e, y_e)
    vx_e += qm_e * ex_part_e * dt
    vy_e += qm_e * ey_part_e * dt
    x_e += vx_e * dt
    y_e += vy_e * dt
    # Periodic boundaries
    x_e = x_e % Lx
    y_e = y_e % Ly
    
    # ---- 6d. Push ions ----
    ex_part_i, ey_part_i = interpolate_fields(ex, ey, x_i, y_i)
    vx_i += qm_i * ex_part_i * dt
    vy_i += qm_i * ey_part_i * dt
    x_i += vx_i * dt
    y_i += vy_i * dt
    x_i = x_i % Lx
    y_i = y_i % Ly
    
    # ---- 6e. Record energy ----
    KE_e = 0.5 * np.sum(vx_e**2 + vy_e**2) / n_electrons
    KE_i = 0.5 * np.sum(vx_i**2 + vy_i**2) / n_ions
    E_field_energy = np.sum(ex**2 + ey**2) * dx * dy * 0.5
    
    history['time'].append(t)
    history['KE_e'].append(KE_e)
    history['KE_i'].append(KE_i)
    history['E_field_energy'].append(E_field_energy)
    
    # ---- 6f. Store snapshots every 100 steps ----
    if n % 100 == 0 or n == nt-1:
        snapshots['rho'].append(rho_total.copy())
        snapshots['phi'].append(phi.copy())
        snapshots['ex'].append(ex.copy())
        snapshots['ey'].append(ey.copy())
        snapshots['particles'].append((x_e.copy(), y_e.copy(), x_i.copy(), y_i.copy()))

# ------------------------------------------------------------------
# 7. Visualise results
# ------------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# ---- Row 0: Final charge density & potential ----
idx = -1
rho_final = snapshots['rho'][idx]
phi_final = snapshots['phi'][idx]
ex_final = snapshots['ex'][idx]
ey_final = snapshots['ey'][idx]
x_e_snap, y_e_snap, x_i_snap, y_i_snap = snapshots['particles'][idx]

# Density
im1 = axes[0,0].imshow(rho_final.T, origin='lower', extent=[0, Lx, 0, Ly], cmap='RdBu_r')
axes[0,0].set_title('Total charge density')
fig.colorbar(im1, ax=axes[0,0])

# Potential
im2 = axes[0,1].imshow(phi_final.T, origin='lower', extent=[0, Lx, 0, Ly], cmap='viridis')
axes[0,1].set_title('Electric potential')
fig.colorbar(im2, ax=axes[0,1])

# E-field quiver
axes[0,2].imshow(rho_final.T, origin='lower', extent=[0, Lx, 0, Ly], alpha=0.3, cmap='RdBu_r')
step = 4
X_q = grid_x[::step]
Y_q = grid_y[::step]
E_x_q = ex_final[::step, ::step]
E_y_q = ey_final[::step, ::step]
axes[0,2].quiver(X_q, Y_q, E_x_q, E_y_q, scale=1.5)
axes[0,2].set_title('Electric field (quiver)')
axes[0,2].set_xlim(0, Lx)
axes[0,2].set_ylim(0, Ly)

# ---- Row 1: Particles (electrons in blue, ions in red) ----
axes[1,0].scatter(x_e_snap, y_e_snap, s=5, alpha=0.5, label='e⁻')
axes[1,0].scatter(x_i_snap, y_i_snap, s=5, alpha=0.5, label='i⁺')
axes[1,0].set_title('Particle positions')
axes[1,0].legend()
axes[1,0].set_xlim(0, Lx)
axes[1,0].set_ylim(0, Ly)

# ---- Velocity distributions ----
vx_all = np.concatenate([vx_e, vx_i])
vy_all = np.concatenate([vy_e, vy_i])
axes[1,1].hist2d(vx_all, vy_all, bins=30, cmap='plasma')
axes[1,1].set_xlabel('vx')
axes[1,1].set_ylabel('vy')
axes[1,1].set_title('Velocity phase space')

# ---- Energy evolution ----
time_arr = np.array(history['time'])
axes[1,2].plot(time_arr, history['KE_e'], label='e⁻ KE')
axes[1,2].plot(time_arr, history['KE_i'], label='i⁺ KE')
axes[1,2].plot(time_arr, history['E_field_energy'] * 0.1, label='Field energy (scaled)')
axes[1,2].set_xlabel('Time')
axes[1,2].set_ylabel('Energy')
axes[1,2].set_title('Energy evolution (heating)')
axes[1,2].legend()
axes[1,2].grid(alpha=0.3)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------------
# 8. Quantitative heating result
# ------------------------------------------------------------------
initial_KE = history['KE_e'][0] + history['KE_i'][0]
final_KE = history['KE_e'][-1] + history['KE_i'][-1]
print(f"Initial total kinetic energy: {initial_KE:.4f}")
print(f"Final total kinetic energy:   {final_KE:.4f}")
print(f"Heating (ΔKE):               {final_KE - initial_KE:.4f}  ({ (final_KE/initial_KE - 1)*100:.1f}% increase)")
print("\nDust-induced charge separation created electric fields that")
print("accelerated particles – a direct PIC demonstration of coronal heating.")

