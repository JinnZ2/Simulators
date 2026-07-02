"""
Interactive Earth heating dashboard.

Ties together orbital-mechanics entry parameters, a simplified 2D GCM
(latitude x altitude), a 1D acoustic wave solver for infrasound from
sprites, and the cascade simulator into a single Jupyter dashboard.
Widgets control orbit type, particle count, flare intensity, and sprite
threshold.

CC0 / for play. Extracted verbatim from legacy/Organize.md lines 556-1021.
Non-stdlib: numpy, matplotlib, ipywidgets, IPython.display.
"""

# ===================================================================
#  INTERACTIVE EARTH HEATING DASHBOARD
#  Orbital Mechanics + GCM + Acoustic Waves + Sprites
#  ===================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from ipywidgets import interact, FloatSlider, IntSlider, Dropdown, fixed, Output
from IPython.display import display, HTML
from scipy.ndimage import gaussian_filter1d
import warnings
warnings.filterwarnings('ignore')

# -------------------------------------------------------------------
# 0. Physical constants & atmospheric model
# -------------------------------------------------------------------
R_earth = 6.371e6
G = 6.674e-11
M_earth = 5.972e24
mu = G * M_earth
Cp_air = 1000.0
rho0 = 1.225
H = 7500.0
T0_air = 250.0
M_atm = 5.148e18
rho_p = 3000.0
latent_heat_vapor = 10e6
Cd = 0.47

def density(z):
    return rho0 * np.exp(-np.maximum(z, 0) / H)

def atmospheric_density_profile(z_centers):
    return density(z_centers)

# -------------------------------------------------------------------
# 1. Orbital mechanics: compute entry angle & speed
# -------------------------------------------------------------------
def orbital_entry_parameters(orbit_type):
    """
    Returns (entry_angle_deg, entry_speed_km_s, description)
    Based on standard orbital mechanics.
    """
    if orbit_type == 'LEO (400 km)':
        # Circular LEO, de-orbit burn gives shallow angle (~1-2°), speed ~7.8 km/s
        return 2.0, 7.8, 'Low Earth Orbit – shallow, slow'
    elif orbit_type == 'GTO (elliptical)':
        # Geostationary Transfer Orbit, entry angle ~6-10°, speed ~10 km/s
        return 8.0, 10.2, 'GTO – moderate angle, fast'
    elif orbit_type == 'Lunar Return':
        # Coming from the Moon, ~11 km/s, angle ~6-8°
        return 7.0, 11.0, 'Lunar return – steepish, very fast'
    elif orbit_type == 'Interplanetary Dust':
        # Cosmic dust, random angles, high speed
        return 15.0, 25.0, 'Interplanetary – grazing, hypervelocity'
    else:  # 'Meteor Shower'
        return 20.0, 35.0, 'Meteor – steep, hypervelocity'

# -------------------------------------------------------------------
# 2. 1D Acoustic Wave Solver (infrasound from sprites)
# -------------------------------------------------------------------
def run_acoustic_simulation(z_centers, source_altitude, source_energy, dt=0.02, steps=300):
    """Simulate acoustic wave (pressure) propagating from sprite altitude to ground."""
    nz = len(z_centers)
    dz = 1000.0  # 1 km spacing
    c_sound = 340.0  # m/s (simplified)
    
    # Pressure field
    p = np.zeros(nz)
    p_prev = np.zeros(nz)
    p_next = np.zeros(nz)
    
    # Source: Gaussian pulse at sprite altitude
    source_idx = np.argmin(np.abs(z_centers - source_altitude))
    source_strength = source_energy * 1e3  # scale to create visible signal
    
    # Store waveform at ground (z=0)
    ground_pressure = []
    
    for n in range(steps):
        # Source injection (only for first 20 steps)
        if n < 20:
            p[source_idx] += source_strength * np.exp(-((n-10)/5)**2)
        
        # FDTD wave equation (1D): p_tt = c^2 p_zz
        p_next[1:-1] = 2*p[1:-1] - p_prev[1:-1] + (c_sound*dt/dz)**2 * (p[2:] - 2*p[1:-1] + p[:-2])
        
        # Absorbing boundaries
        p_next[0] = p_next[1] * 0.95
        p_next[-1] = p_next[-2] * 0.95
        
        p_prev, p = p, p_next
        ground_pressure.append(p[0])
    
    return np.array(ground_pressure) * 1e3  # scale for visibility

# -------------------------------------------------------------------
# 3. Simplified 2D GCM (Latitude vs Altitude)
# -------------------------------------------------------------------
def run_gcm_simulation(z_centers, lat_centers, heat_source_profile, dt=0.1, steps=100):
    """
    2D advection-diffusion of heat anomaly.
    Heat source: profile over altitude (from cascade). 
    Advection: poleward at 5 m/s, diffusion: 5000 m^2/s.
    """
    nz = len(z_centers)
    nl = len(lat_centers)
    
    # Temperature anomaly field (lat, z)
    T_anom = np.zeros((nl, nz))
    T_anom[:, :] = heat_source_profile[np.newaxis, :] * 0.1  # initial coupling
    
    # Advection velocity: poleward (towards higher latitude)
    v_lat = 5.0  # m/s (towards poles)
    v_z = -0.2  # m/s (slow downward)
    dz = 1000.0
    dlat = lat_centers[1] - lat_centers[0]  # degrees
    dlat_m = dlat * np.pi/180 * R_earth  # meters
    
    history = []
    
    for step in range(steps):
        # Advection (upwind)
        new_T = T_anom.copy()
        # Horizontal advection (poleward)
        for i in range(1, nl-1):
            for j in range(nz):
                flux = v_lat * T_anom[i-1, j]  # from lower latitude (equator)
                new_T[i, j] += (flux / dlat_m) * dt
        
        # Vertical advection (downward)
        for i in range(nl):
            for j in range(1, nz-1):
                flux = -v_z * T_anom[i, j-1]  # from above
                new_T[i, j] += (flux / dz) * dt
        
        # Diffusion
        for i in range(1, nl-1):
            for j in range(1, nz-1):
                new_T[i, j] += 5000 * (T_anom[i-1,j] - 2*T_anom[i,j] + T_anom[i+1,j]) / dlat_m**2 * dt
                new_T[i, j] += 5000 * (T_anom[i,j-1] - 2*T_anom[i,j] + T_anom[i,j+1]) / dz**2 * dt
        
        T_anom = np.clip(new_T, 0, None)
        if step % 10 == 0:
            history.append(T_anom.copy())
    
    return T_anom, history

# -------------------------------------------------------------------
# 4. Core cascade simulator (parametrised)
# -------------------------------------------------------------------
def run_parameterised_sim(n_particles, entry_angle, entry_speed, flare_factor, threshold_factor):
    """
    Simplified cascade simulation returning energy profile, sprites, and acoustic source.
    """
    z_bins = np.linspace(0, 150_000, 151)
    z_centers = (z_bins[:-1] + z_bins[1:]) / 2
    dz = 1000.0
    
    # Particle masses (log-normal)
    masses = 10 ** np.random.uniform(-7, 1.7, n_particles)
    radii = (3 * masses / (4 * np.pi * rho_p)) ** (1/3)
    
    # Entry velocities (with scattering)
    v_total = np.random.uniform(entry_speed*0.8, entry_speed*1.2, n_particles) * 1000  # m/s
    # Decompose into vertical/horizontal
    angle_rad = np.radians(entry_angle)
    vz = -v_total * np.cos(angle_rad)
    vx = v_total * np.sin(angle_rad) * np.random.uniform(0.8, 1.2, n_particles)
    
    # Initial altitudes
    z0 = np.random.uniform(140_000, 150_000, n_particles)
    x0 = np.random.uniform(-50_000, 50_000, n_particles)
    
    # Simulate energy deposition (simplified Monte Carlo)
    energy_profile = np.zeros(len(z_centers))
    plasma_profile = np.zeros(len(z_centers))
    sprite_positions = []
    
    dt = 0.02
    steps = 300
    
    # Background ionisation (flare factor)
    background_n_e = 1e15 * flare_factor * np.exp(-((z_centers - 110_000) / 20_000)**2)
    background_n_e += 1e13 * np.exp(-((z_centers - 250_000) / 50_000)**2)
    
    # Track particles
    active = np.ones(n_particles, dtype=bool)
    z = z0.copy()
    v = v_total.copy()  # total speed
    m = masses.copy()
    r = radii.copy()
    T_p = np.full(n_particles, 300.0)
    
    for step in range(steps):
        if not np.any(active):
            break
        # Drag
        rho = density(z)
        A = np.pi * r**2
        v_old = v.copy()
        a_drag = -0.5 * Cd * rho * v**2 * A / m
        v += a_drag * dt
        v = np.maximum(v, 0)
        v_avg = v_old + 0.5 * a_drag * dt
        
        # dKE
        dKE = 0.5 * m * (v_old**2 - v**2)
        heat_air = 0.8 * dKE
        heat_p = 0.2 * dKE
        
        # Heating
        T_p += heat_p / (m * 1000 + 1e-15)
        
        # Ablation
        ablating = (T_p > 2500) & (m > 1e-12)
        if np.any(ablating):
            excess = (T_p - 2500) * m * 1000
            dm = np.minimum(excess / latent_heat_vapor, m * 0.05)
            dm = np.clip(dm, 0, 1e-6)
            m[ablating] -= dm[ablating]
            r[ablating] = (3 * m[ablating] / (4 * np.pi * rho_p)) ** (1/3)
            T_p[ablating] = 2500
            heat_air[ablating] += dm[ablating] * latent_heat_vapor
        
        # Update position (vertical only, using avg speed with angle)
        # Actually we need vertical velocity: v_z = v * cos(angle) (since v is total speed)
        # But to keep it 1D for energy profile, we project
        v_z = v_avg * np.cos(angle_rad)
        z += v_z * dt
        
        # Deposit heat
        mask = active & (z > 0) & (z < 150_000)
        if np.any(mask):
            idx = np.floor(z[mask] / dz).astype(int)
            idx = np.clip(idx, 0, len(z_centers)-1)
            for i, (e, p) in enumerate(zip(heat_air[mask], dKE[mask] * 1e15)):
                energy_profile[idx[i]] += e
                plasma_profile[idx[i]] += p
        
        # Deactivate
        active &= (z > 0) & (v > 10) & (m > 1e-13) & (z < 150_000)
    
    # ---- Sprites ----
    sprite_heights = []
    sprite_energies = []
    sprite_times = []
    
    # n_e_total = background + plasma
    n_e_total = background_n_e + plasma_profile
    # Use threshold factor
    threshold = 5e17 * threshold_factor
    triggered = np.where(n_e_total > threshold)[0]
    
    if len(triggered) > 0:
        for idx in triggered:
            sprite_heights.append(z_centers[idx])
            sprite_energies.append(energy_profile[idx] * 0.1)  # 10% of energy -> sprite
        # Sort by height (top to bottom)
        sorted_indices = np.argsort(sprite_heights)[::-1]
        sprite_heights = np.array(sprite_heights)[sorted_indices]
        sprite_energies = np.array(sprite_energies)[sorted_indices]
    
    return energy_profile, plasma_profile, z_centers, sprite_heights, sprite_energies, n_e_total

# -------------------------------------------------------------------
# 5. Main interactive function
# -------------------------------------------------------------------
def run_interactive(orbit_type, n_particles, flare_intensity, sprite_threshold, show_acoustic, show_gcm):
    # ---- Orbital parameters ----
    entry_angle, entry_speed, orbit_desc = orbital_entry_parameters(orbit_type)
    
    # ---- Run cascade ----
    flare_factor = flare_intensity / 10.0  # 1-10 -> 0.1 to 1.0
    threshold_factor = 1.0 / sprite_threshold  # 1-10 -> 1.0 to 0.1 (lower = easier)
    
    E_profile, P_profile, z, sprite_h, sprite_E, n_e_total = run_parameterised_sim(
        n_particles, entry_angle, entry_speed, flare_factor, threshold_factor
    )
    
    # ---- Acoustic wave (if enabled) ----
    if show_acoustic and len(sprite_h) > 0:
        # Use the lowest sprite as the source
        source_alt = sprite_h[-1] if len(sprite_h) > 0 else 70000
        source_energy = np.sum(sprite_E) / 1e6  # MJ
        acoustic_signal = run_acoustic_simulation(z, source_alt, source_energy)
    else:
        acoustic_signal = None
    
    # ---- GCM simulation (if enabled) ----
    if show_gcm:
        lat_centers = np.linspace(-80, 80, 40)  # degrees
        # Use the energy profile as heat source
        heat_source = gaussian_filter1d(E_profile, sigma=5)
        heat_source = heat_source / np.max(heat_source) * 10  # scale to ~10 K
        T_gcm, gcm_history = run_gcm_simulation(z, lat_centers, heat_source)
    else:
        lat_centers = np.linspace(-80, 80, 40)
        T_gcm = None
        gcm_history = None
    
    # ---- PLOTTING ----
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 3, height_ratios=[1, 0.8])
    
    # Panel 1: Energy & Plasma profile
    ax = fig.add_subplot(gs[0, 0])
    ax.plot(E_profile / 1e6, z/1000, 'b-', label='Energy (MJ per bin)', lw=2)
    ax.plot(P_profile / 1e15, z/1000, 'r--', label='Plasma (10^15 e⁻)', lw=2)
    ax.axhline(y=110, color='gray', linestyle=':', label='E-layer')
    ax.set_xlabel('Energy / Plasma density')
    ax.set_ylabel('Altitude (km)')
    ax.set_title(f'Cascade Profile ({orbit_desc})')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Panel 2: Sprites
    ax = fig.add_subplot(gs[0, 1])
    if len(sprite_h) > 0:
        ax.scatter(sprite_E/1e6, sprite_h/1000, s=sprite_E/1e4, c='magenta', alpha=0.8, edgecolors='white')
        ax.set_xlabel('Sprite energy (MJ)')
        ax.set_ylabel('Altitude (km)')
        ax.set_title(f'{len(sprite_h)} Sprites/Elves')
        ax.grid(alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'No sprites triggered', ha='center', va='center', transform=ax.transAxes, fontsize=14)
        ax.set_title('Sprite activity')
    
    # Panel 3: Electron density & threshold
    ax = fig.add_subplot(gs[0, 2])
    ax.semilogy(n_e_total, z/1000, 'g-', lw=2, label='n_e total')
    threshold = 5e17 * threshold_factor
    ax.axvline(threshold, color='red', linestyle='--', label='Threshold')
    ax.set_xlabel('Electron density (m⁻³)')
    ax.set_ylabel('Altitude (km)')
    ax.set_title('Ionisation & Breakdown')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Panel 4: Acoustic ground signal
    ax = fig.add_subplot(gs[1, 0])
    if show_acoustic and acoustic_signal is not None:
        time_arr = np.linspace(0, len(acoustic_signal)*0.02, len(acoustic_signal))
        ax.plot(time_arr, acoustic_signal, 'k-', lw=2)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Pressure (arb. units)')
        ax.set_title('Infrasound at Ground (from sprites)')
        ax.grid(alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'Acoustics disabled', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Acoustic Wave')
    
    # Panel 5: GCM global heat map
    ax = fig.add_subplot(gs[1, 1])
    if show_gcm and T_gcm is not None:
        im = ax.imshow(T_gcm, extent=[-80, 80, 0, 150], origin='lower', aspect='auto', cmap='hot', vmin=0, vmax=15)
        ax.set_xlabel('Latitude (°)')
        ax.set_ylabel('Altitude (km)')
        ax.set_title('Global Climate Anomaly (K)')
        plt.colorbar(im, ax=ax, fraction=0.05)
    else:
        ax.text(0.5, 0.5, 'GCM disabled', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Global Circulation Model')
    
    # Panel 6: Summary stats
    ax = fig.add_subplot(gs[1, 2])
    ax.axis('off')
    total_energy = np.sum(E_profile) / 1e6  # MJ
    global_dT = total_energy * 1e6 / (M_atm * Cp_air) * 1000  # mK
    max_dT = np.max(E_profile) / (rho0 * 1000 * Cp_air) if np.max(E_profile) > 0 else 0
    ax.text(0.1, 0.9, f'🌍 SIMULATION SUMMARY', fontsize=14, weight='bold')
    ax.text(0.1, 0.8, f'Entry: {entry_angle:.1f}°, {entry_speed:.1f} km/s', fontsize=12)
    ax.text(0.1, 0.7, f'Particles: {n_particles}', fontsize=12)
    ax.text(0.1, 0.6, f'Flare factor: {flare_factor:.2f}', fontsize=12)
    ax.text(0.1, 0.5, f'Sprite threshold: {threshold_factor:.2f}', fontsize=12)
    ax.text(0.1, 0.4, f'Sprites: {len(sprite_h)}', fontsize=12, color='magenta')
    ax.text(0.1, 0.3, f'Total energy: {total_energy:.2f} MJ', fontsize=12, color='orange')
    ax.text(0.1, 0.2, f'Global ΔT: {global_dT:.3f} mK', fontsize=12, color='red')
    ax.text(0.1, 0.1, f'Local peak ΔT: {max_dT:.1f} K', fontsize=12, color='darkred')
    
    plt.tight_layout()
    plt.show()
    
    # Additional outputs for debugging
    return fig

# -------------------------------------------------------------------
# 6. BUILD THE INTERACTIVE DASHBOARD
# -------------------------------------------------------------------
# Define widgets
orbit_selector = Dropdown(
    options=['LEO (400 km)', 'GTO (elliptical)', 'Lunar Return', 'Interplanetary Dust', 'Meteor Shower'],
    value='Interplanetary Dust',
    description='Orbit:'
)

n_particles_slider = IntSlider(
    value=3000, min=500, max=15000, step=500,
    description='Particles:'
)

flare_slider = FloatSlider(
    value=5.0, min=1.0, max=10.0, step=0.5,
    description='Flare intensity:'
)

sprite_slider = FloatSlider(
    value=3.0, min=1.0, max=10.0, step=0.5,
    description='Sprite threshold (1=easy, 10=hard):'
)

acoustic_checkbox = Dropdown(
    options=[True, False],
    value=True,
    description='Acoustics:'
)

gcm_checkbox = Dropdown(
    options=[True, False],
    value=True,
    description='Global GCM:'
)

# Create interactive output
out = Output()

def interactive_plot(orbit_type, n_particles, flare_intensity, sprite_threshold, show_acoustic, show_gcm):
    with out:
        out.clear_output(wait=True)
        fig = run_interactive(orbit_type, n_particles, flare_intensity, sprite_threshold, show_acoustic, show_gcm)
        plt.close(fig)

# Display the dashboard
print("="*60)
print("🌍 EARTH HEATING & CASCADE SIMULATOR – INTERACTIVE")
print("="*60)
print("Adjust the sliders below, then click 'Run Interact' to update the simulation.")
print("(If running in Jupyter, the plots will update automatically.)")
print("-"*60)

# Display widgets
display(orbit_selector, n_particles_slider, flare_slider, sprite_slider, 
        acoustic_checkbox, gcm_checkbox)

# Button to run (or use interact for auto-update)
from ipywidgets import interactive
widgets = interactive(interactive_plot, 
                     orbit_type=orbit_selector,
                     n_particles=n_particles_slider,
                     flare_intensity=flare_slider,
                     sprite_threshold=sprite_slider,
                     show_acoustic=acoustic_checkbox,
                     show_gcm=gcm_checkbox)

display(widgets)
display(out)

# -------------------------------------------------------------------
# 7. Run a default case immediately
# -------------------------------------------------------------------
print("\n" + "="*60)
print("🚀 Running default simulation (Interplanetary Dust, 3000 particles)...")
print("="*60)
run_interactive('Interplanetary Dust', 3000, 5.0, 3.0, True, True)

