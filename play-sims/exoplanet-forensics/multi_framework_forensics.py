"""
Multi-framework exoplanet forensics — transit + RV + microlensing +
astrometry.

Generates a synthetic planetary system, then runs four independent
detection frameworks against it. Cross-correlates who-detected-what to
highlight "hidden gems" — planets one method missed that another
recovered (e.g. a super-Jupiter TESS transits missed but Gaia's
microlensing surfaced).

CC0 / for play. Extracted verbatim from Organize.md lines 2264-2700.
Non-stdlib: numpy, matplotlib, ipywidgets, IPython.display.
"""

# ===================================================================
#  MULTI‑FRAMEWORK EXOPLANET FORENSICS
#  Transit + RV + Microlensing + Astrometry
#  ===================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from ipywidgets import interact, FloatSlider, IntSlider, Dropdown, VBox, HBox, Output, interactive
from IPython.display import display, clear_output
from scipy.stats import norm

# -------------------------------------------------------------------
# 1. Physical constants & planet generator
# -------------------------------------------------------------------
R_sun = 6.957e8          # m
R_jup = 6.991e7          # m
M_sun = 1.989e30         # kg
M_jup = 1.898e27         # kg
AU = 1.496e11            # m
G = 6.674e-11
c = 3e8
pc = 3.086e16            # m

def generate_system(seed=None):
    """Generate a random star+planet system with realistic parameters."""
    np.random.seed(seed)
    
    # Star (solar-type)
    M_star = np.random.uniform(0.5, 1.2) * M_sun
    R_star = np.random.uniform(0.5, 1.2) * R_sun
    dist_pc = np.random.uniform(50, 500)   # distance in parsecs
    
    # Planet (mass, orbit, inclination)
    M_planet = 10 ** np.random.uniform(-1.0, 2.0) * M_jup   # 0.1 to 100 Mjup
    a_au = 10 ** np.random.uniform(-1.0, 2.0)               # 0.1 to 100 AU
    a = a_au * AU
    incl_deg = np.random.uniform(0, 180)                     # inclination (0=face-on)
    incl_rad = np.radians(incl_deg)
    ecc = np.random.uniform(0, 0.5)
    omega = np.random.uniform(0, 2*np.pi)                   # argument of periastron
    
    return {
        'M_star': M_star, 'R_star': R_star, 'dist_pc': dist_pc,
        'M_planet': M_planet, 'a': a, 'a_au': a_au,
        'incl_deg': incl_deg, 'incl_rad': incl_rad,
        'ecc': ecc, 'omega': omega,
        'P_yr': np.sqrt(a_au**3 / (M_star/M_sun)),  # Kepler's law (years)
        'seed': seed
    }

# -------------------------------------------------------------------
# 2. Detection framework functions
# -------------------------------------------------------------------

def detect_transit(system, noise_ppm=100, min_duration=0.5):
    """Transit method (TESS-like)."""
    # Check if inclination is close to 90° (edge-on)
    # Transit probability: (R_star / a) * (1 + R_planet/R_star)
    R_planet = (system['M_planet'] / M_jup)**(1/3) * R_jup  # rough scaling
    prob_transit = (system['R_star'] + R_planet) / system['a']
    prob_transit *= 1 / np.sin(system['incl_rad']) if system['incl_rad'] > 0 else 0
    prob_transit = min(1, prob_transit)
    
    # If inclined, maybe it transits
    transits = np.random.rand() < prob_transit
    
    if not transits:
        return False, 0.0, 0.0
    
    # Transit depth (delta F / F)
    depth_ppm = (R_planet / system['R_star'])**2 * 1e6
    
    # Duration (hours) - simplified
    period_hrs = system['P_yr'] * 365.25 * 24
    duration_hrs = period_hrs * (system['R_star'] / (np.pi * system['a']))
    duration_hrs = max(0.1, duration_hrs)
    
    # Detectability: depth > noise_ppm and duration > min_duration
    detected = depth_ppm > noise_ppm and duration_hrs > min_duration
    
    # Also check if it's not too long (TESS observations ~27 days)
    detected = detected and period_hrs < 27*24
    
    return detected, depth_ppm, duration_hrs

def detect_rv(system, rv_noise=1.0, min_snr=5):
    """Radial Velocity method (ground-based spectrographs)."""
    # Reflex velocity semi-amplitude (m/s)
    # K = (28.4 m/s) * (M_planet/M_jup) * (P_yr)^(-1/3) * (M_star/M_sun)^(-2/3)
    # Simplified, including eccentricity factor
    K = 28.4 * (system['M_planet'] / M_jup) * (system['P_yr'])**(-1/3) * (system['M_star']/M_sun)**(-2/3)
    # Eccentricity correction
    K *= 1 / np.sqrt(1 - system['ecc']**2)
    
    # Inclination dependence (K_obs = K * sin(i))
    K_obs = K * np.sin(system['incl_rad'])
    
    # Detect if SNR > min_snr
    snr = K_obs / rv_noise
    detected = snr > min_snr and system['P_yr'] < 10  # RV works best for short periods
    
    return detected, K_obs, snr

def detect_microlensing(system, background_star_density=100, min_mag=0.1):
    """Microlensing method (Gaia/TESS)."""
    # Einstein radius (in arcseconds)
    # theta_E = sqrt(4 G M / c^2 * (D_s - D_l) / (D_l * D_s))
    D_l = system['dist_pc'] * pc  # lens distance
    # Assume background source at 2x distance
    D_s = D_l * 2.0
    M_total = system['M_star'] + system['M_planet']
    
    theta_E = np.sqrt(4 * G * M_total / c**2 * (D_s - D_l) / (D_l * D_s))
    theta_E_as = theta_E * 206265  # arcseconds
    
    # Einstein crossing time (days) - depends on relative proper motion
    # Assume typical 20 km/s transverse velocity
    v_t = 20e3  # m/s
    t_E_days = (theta_E * D_l) / v_t / 86400
    t_E_days = max(0.5, t_E_days)
    
    # Peak magnification (approximate, for point-source)
    impact_param = np.random.uniform(0, 2)  # relative impact parameter in theta_E units
    if impact_param < 1:
        mag = 1 / np.sqrt(1 - impact_param**2) - 1  # excess mag
    else:
        mag = 0
    
    # Probability of lensing a background star:
    # ~ background_star_density * theta_E^2 (simplified)
    prob_lens = min(1, background_star_density * (theta_E_as / 3600)**2 * 1000)
    lensing_event = np.random.rand() < prob_lens
    
    if not lensing_event:
        return False, 0.0, 0.0, 0.0
    
    # Detect if magnification is significant
    detected = mag > min_mag and t_E_days > 0.5
    
    return detected, mag, t_E_days, theta_E_as

def detect_astrometry(system, astro_noise_as=0.1, min_snr=5):
    """Astrometric method (Gaia-like)."""
    # Astrometric signal: alpha = (M_planet / M_star) * (a / D) * (radians)
    a_rad = system['a'] / (system['dist_pc'] * pc)
    alpha_as = (system['M_planet'] / system['M_star']) * a_rad * 206265
    
    # Inclination dependence (sky projection)
    alpha_obs = alpha_as * np.sin(system['incl_rad'])
    
    # Detectability
    snr = alpha_obs / astro_noise_as
    detected = snr > min_snr and system['P_yr'] < 20  # Gaia observes ~5-10 years
    
    return detected, alpha_obs, snr

# -------------------------------------------------------------------
# 3. Survey many systems
# -------------------------------------------------------------------
def run_survey(n_systems, transit_noise_ppm, rv_noise_ms, lens_density, astro_noise_as, min_snr=5):
    results = []
    
    for i in range(n_systems):
        sys = generate_system(seed=i)
        
        # Run all frameworks
        transit_det, depth, dur = detect_transit(sys, noise_ppm=transit_noise_ppm, min_snr=min_snr)
        rv_det, K, snr_rv = detect_rv(sys, rv_noise=rv_noise_ms, min_snr=min_snr)
        lens_det, mag, tE, thetaE = detect_microlensing(sys, background_star_density=lens_density)
        astro_det, alpha, snr_astro = detect_astrometry(sys, astro_noise_as=astro_noise_as, min_snr=min_snr)
        
        # Compile detection flags
        detections = {
            'Transit': transit_det,
            'RV': rv_det,
            'Microlensing': lens_det,
            'Astrometry': astro_det
        }
        
        # Count frameworks that detected it
        n_det = sum(detections.values())
        
        # Classify "Hidden Gems": detected by Microlensing + Astrometry, but NOT Transit
        is_hidden_gem = lens_det and astro_det and not transit_det
        
        results.append({
            'system': sys,
            'detections': detections,
            'n_det': n_det,
            'is_hidden_gem': is_hidden_gem,
            'depth_ppm': depth, 'K_ms': K, 'mag': mag, 'alpha_as': alpha,
            'a_au': sys['a_au'], 'M_jup': sys['M_planet']/M_jup, 
            'P_yr': sys['P_yr'], 'incl_deg': sys['incl_deg']
        })
    
    return results

# -------------------------------------------------------------------
# 4. Visualisation engine
# -------------------------------------------------------------------
def plot_survey(results, highlight_gems=True):
    n = len(results)
    if n == 0:
        print("No results to plot.")
        return
    
    # Extract data
    M_jup = np.array([r['M_jup'] for r in results])
    a_au = np.array([r['a_au'] for r in results])
    P_yr = np.array([r['P_yr'] for r in results])
    incl = np.array([r['incl_deg'] for r in results])
    
    # Detection flags
    transit_flags = np.array([r['detections']['Transit'] for r in results])
    rv_flags = np.array([r['detections']['RV'] for r in results])
    lens_flags = np.array([r['detections']['Microlensing'] for r in results])
    astro_flags = np.array([r['detections']['Astrometry'] for r in results])
    hidden_gems = np.array([r['is_hidden_gem'] for r in results])
    
    # Prepare figure
    fig = plt.figure(figsize=(16, 12))
    gs = gridspec.GridSpec(2, 3, height_ratios=[1, 0.8])
    
    # ---- Panel 1: Mass vs Semi-major Axis (the "Discovery Space") ----
    ax = fig.add_subplot(gs[0, 0])
    # Plot all planets as small dots
    ax.scatter(a_au, M_jup, c='lightgray', s=30, alpha=0.5, label='Undetected')
    
    # Highlight detected by each method (with jitter for visibility)
    if np.any(transit_flags):
        ax.scatter(a_au[transit_flags], M_jup[transit_flags], c='cyan', s=60, 
                   edgecolors='k', label='Transit', zorder=3)
    if np.any(rv_flags):
        ax.scatter(a_au[rv_flags], M_jup[rv_flags], c='orange', s=60, 
                   edgecolors='k', label='RV', zorder=4)
    if np.any(lens_flags):
        ax.scatter(a_au[lens_flags], M_jup[lens_flags], c='magenta', s=60, 
                   edgecolors='k', label='Microlensing', zorder=5)
    if np.any(astro_flags):
        ax.scatter(a_au[astro_flags], M_jup[astro_flags], c='lime', s=60, 
                   edgecolors='k', label='Astrometry', zorder=6)
    
    # Highlight Hidden Gems (Gaia23bra b analogues)
    if highlight_gems and np.any(hidden_gems):
        ax.scatter(a_au[hidden_gems], M_jup[hidden_gems], s=200, 
                   facecolors='none', edgecolors='red', linewidths=3, 
                   label='⭐ Hidden Gem! (no transit, lensing+astro)', zorder=10)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Semi-major axis (AU)')
    ax.set_ylabel('Planet Mass (M_Jupiter)')
    ax.set_title('Exoplanet Discovery Space')
    ax.legend(loc='lower right', fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_xlim(0.05, 200)
    ax.set_ylim(0.05, 200)
    
    # ---- Panel 2: Period vs Inclination (Transit geometry) ----
    ax = fig.add_subplot(gs[0, 1])
    ax.scatter(P_yr, incl, c='lightgray', s=20, alpha=0.4, label='All')
    if np.any(transit_flags):
        ax.scatter(P_yr[transit_flags], incl[transit_flags], c='cyan', s=40, label='Transiting')
    # Draw the transit zone (inclination near 90°)
    ax.axhspan(85, 95, alpha=0.1, color='cyan', label='Transit zone')
    ax.set_xscale('log')
    ax.set_xlabel('Orbital Period (years)')
    ax.set_ylabel('Inclination (degrees)')
    ax.set_title('Transit Geometry: Edge-on planets')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # ---- Panel 3: Detection overlaps (Venn-style bar chart) ----
    ax = fig.add_subplot(gs[0, 2])
    methods = ['Transit', 'RV', 'Microlensing', 'Astrometry']
    counts = [np.sum(transit_flags), np.sum(rv_flags), np.sum(lens_flags), np.sum(astro_flags)]
    colors = ['cyan', 'orange', 'magenta', 'lime']
    bars = ax.bar(methods, counts, color=colors, alpha=0.7, edgecolor='k')
    # Add total number of planets
    ax.axhline(y=n, color='gray', linestyle='--', label=f'Total planets = {n}')
    ax.set_ylabel('Number of detections')
    ax.set_title('Detection yield per framework')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    # Add numbers on bars
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{count}', ha='center', va='bottom')
    
    # ---- Panel 4: Hidden Gems: Gaia23bra b analogues ----
    ax = fig.add_subplot(gs[1, 0])
    if np.any(hidden_gems):
        gem_data = results[hidden_gems]
        gem_mass = [r['M_jup'] for r in gem_data]
        gem_a = [r['a_au'] for r in gem_data]
        ax.scatter(gem_a, gem_mass, s=150, c='red', marker='*', label='Hidden Gems', zorder=10)
        # Add annotations
        for i, r in enumerate(gem_data):
            ax.annotate(f"P={r['P_yr']:.1f}yr", (r['a_au'], r['M_jup']), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Semi-major axis (AU)')
        ax.set_ylabel('Mass (M_Jup)')
        ax.set_title(f'⭐ {np.sum(hidden_gems)} Hidden Gems found!')
        ax.grid(alpha=0.3)
        # Add a note about Gaia23bra b
        ax.text(0.05, 0.95, 'Gaia23bra b analogue:\nSuper-Jupiter, wide orbit,\nno transit, lensing+astro', 
                transform=ax.transAxes, fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    else:
        ax.text(0.5, 0.5, 'No hidden gems found\n(try adjusting sensitivities)', 
                ha='center', va='center', transform=ax.transAxes, fontsize=12)
        ax.set_title('Hidden Gems')
    
    # ---- Panel 5: Detection method combination matrix (heatmap) ----
    ax = fig.add_subplot(gs[1, 1])
    # Count planets detected by each combination (only considering top 3 for simplicity)
    combo_counts = {}
    for r in results:
        flags = r['detections']
        combo = (flags['Transit'], flags['RV'], flags['Microlensing'], flags['Astrometry'])
        combo_counts[combo] = combo_counts.get(combo, 0) + 1
    
    # Build a simplified matrix: Transit vs Microlensing (highlighting the cross-correlation)
    transit_vs_lens = np.zeros((2, 2))
    for r in results:
        t = int(r['detections']['Transit'])
        l = int(r['detections']['Microlensing'])
        transit_vs_lens[l, t] += 1  # rows: lens, cols: transit
    
    im = ax.imshow(transit_vs_lens, cmap='Blues', origin='lower', vmin=0, vmax=n//2)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['No Transit', 'Transit'])
    ax.set_yticklabels(['No Lens', 'Microlens'])
    ax.set_xlabel('Transit detection')
    ax.set_ylabel('Microlensing detection')
    ax.set_title('Cross-correlation: Transit vs Microlensing')
    # Add numbers in cells
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f'{transit_vs_lens[i, j]:.0f}', 
                    ha='center', va='center', color='black' if transit_vs_lens[i, j] < n//4 else 'white')
    plt.colorbar(im, ax=ax, fraction=0.05, label='Count')
    
    # ---- Panel 6: Summary stats ----
    ax = fig.add_subplot(gs[1, 2])
    ax.axis('off')
    n_det_all = np.sum([r['n_det'] for r in results])
    mean_det = n_det_all / n
    n_gems = np.sum(hidden_gems)
    
    # Text summary
    summary = f"""
    📊 SURVEY SUMMARY
    ─────────────────────────
    Total systems:        {n}
    Total detections:     {n_det_all} (avg {mean_det:.2f} per system)
    
    Detection breakdown:
      • Transit:         {np.sum(transit_flags)}
      • RV:              {np.sum(rv_flags)}
      • Microlensing:    {np.sum(lens_flags)}
      • Astrometry:      {np.sum(astro_flags)}
    
    ⭐ Hidden Gems:       {n_gems}
      (Microlensing + Astrometry, no Transit)
    
    ─────────────────────────
    💡 "When you cross-correlate
       frameworks, you find planets
       that each one alone would miss."
    """
    ax.text(0.05, 0.95, summary, transform=ax.transAxes, fontsize=11, 
            verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
    
    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------------
# 5. Interactive wrapper
# -------------------------------------------------------------------
def run_interactive_survey(n_systems=100, transit_noise=100, rv_noise=1.0, 
                           lens_density=50, astro_noise=0.5, highlight=True):
    results = run_survey(n_systems, transit_noise, rv_noise, lens_density, astro_noise)
    plot_survey(results, highlight_gems=highlight)
    
    # Additional stats printed
    n_gems = np.sum([r['is_hidden_gem'] for r in results])
    print(f"\n🔍 Found {n_gems} Hidden Gems (Gaia23bra b analogues) out of {n_systems} systems.")
    if n_gems > 0:
        gem_masses = [r['M_jup'] for r in results if r['is_hidden_gem']]
        gem_a = [r['a_au'] for r in results if r['is_hidden_gem']]
        print(f"   Mass range: {np.min(gem_masses):.1f} - {np.max(gem_masses):.1f} Mjup")
        print(f"   Orbit range: {np.min(gem_a):.1f} - {np.max(gem_a):.1f} AU")

# -------------------------------------------------------------------
# 6. Interactive controls
# -------------------------------------------------------------------
style = {'description_width': 'initial'}

controls = {
    'n_systems': IntSlider(value=150, min=30, max=300, step=10, 
                           description='Number of systems', style=style),
    'transit_noise': FloatSlider(value=100, min=10, max=500, step=10, 
                                 description='Transit noise (ppm)', style=style),
    'rv_noise': FloatSlider(value=1.0, min=0.1, max=5.0, step=0.1, 
                            description='RV noise (m/s)', style=style),
    'lens_density': FloatSlider(value=50, min=5, max=200, step=5, 
                                description='Background star density', style=style),
    'astro_noise': FloatSlider(value=0.5, min=0.05, max=2.0, step=0.05, 
                               description='Astrometry noise (mas)', style=style),
    'highlight': Dropdown(options=[True, False], value=True, description='Highlight gems', style=style)
}

out = Output()
def update(**kwargs):
    with out:
        clear_output(wait=True)
        run_interactive_survey(**kwargs)

interactive_widget = interactive(update, **controls)
display(HBox([VBox([controls[k] for k in controls]), out]))

# -------------------------------------------------------------------
# 7. Run default case (showing the "Gaia23bra b" effect)
# -------------------------------------------------------------------
print("🚀 RUNNING MULTI-FRAMEWORK EXOPLANET SURVEY")
print("   Simulating how TESS+Gaia found a super-Jupiter via microlensing")
print("   while transit surveys missed it.\n")
run_interactive_survey(n_systems=150, transit_noise=100, rv_noise=1.0, 
                       lens_density=50, astro_noise=0.5, highlight=True)
