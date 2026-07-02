"""
Exoplanet population synthesis + survey.

Draws a galactic planet population from occurrence-rate priors
(period-radius-mass), applies a chosen survey method with its noise
floor, characterises what survived, and scores habitability. Interactive
widget over method / noise / sample size.

CC0 / for play. Extracted verbatim from Organize2.md lines 458-948.
Non-stdlib: numpy, matplotlib, ipywidgets, IPython.display.
"""

# ===================================================================
#  EXOPLANET POPULATION SYNTHESIS & SURVEY SIMULATOR
#  Occurrence rates + Observations + Characterisation + Habitability
#  ===================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from ipywidgets import interact, FloatSlider, IntSlider, Dropdown, VBox, HBox, Output, interactive
from IPython.display import display, clear_output
from scipy.stats import powerlaw, lognorm, norm
from astropy import units as u
from astropy.constants import M_sun, R_sun, M_jup, R_jup

# -------------------------------------------------------------------
# 1. Constants & planet population generator
# -------------------------------------------------------------------
M_sun_kg = M_sun.value
R_sun_m = R_sun.value
M_jup_kg = M_jup.value
R_jup_m = R_jup.value
AU_m = 1.496e11
pc_m = 3.086e16

def generate_planet_population(n_planets, seed=None, occurrence_base=1.0):
    """
    Generate n_planets with realistic distributions:
    - Mass: power-law dN/dM ∝ M^{-1.6} (0.5 M_earth to 13 M_jup)
    - Semi-major axis: log-uniform from 0.01 to 100 AU
    - Eccentricity: beta distribution (0.0-0.9)
    - Inclination: isotropic (sin i)
    - Radius: mass-radius relation (simplified)
    """
    np.random.seed(seed)
    # Mass in Earth masses (M_earth)
    M_earth_kg = 5.972e24
    M_min = 0.5  # M_earth
    M_max = 13 * 317.8  # 13 M_jup in M_earth
    # Power-law index -1.6
    mass_samples = powerlaw.rvs(1.6, loc=M_min, scale=M_max-M_min, size=n_planets)
    mass_earth = np.clip(mass_samples, M_min, M_max)
    mass_kg = mass_earth * M_earth_kg
    mass_jup = mass_kg / M_jup_kg
    
    # Semi-major axis (log-uniform in AU)
    a_au = 10 ** np.random.uniform(-2, 2, n_planets)
    a_m = a_au * AU_m
    
    # Eccentricity: beta(0.867, 3.03) from radial velocity surveys
    ecc = np.random.beta(0.867, 3.03, n_planets)
    ecc = np.clip(ecc, 0.0, 0.9)
    
    # Inclination (isotropic): sin(i) uniform in [0,1]
    sin_i = np.random.uniform(0, 1, n_planets)
    incl_deg = np.arcsin(sin_i) * 180 / np.pi
    incl_rad = np.radians(incl_rad)
    
    # Radius: mass-radius relation (from Chen & Kipping 2017)
    # For M < 1 M_earth: R/R_earth = M^0.279
    # For 1 < M < 100 M_earth: R/R_earth = M^0.589
    # For >100: R/R_earth = M^0.010 (gas giant)
    r_earth = 6.371e6
    r_jup = R_jup_m
    r_planet_earth = np.zeros(n_planets)
    for i, m in enumerate(mass_earth):
        if m < 1.0:
            r_planet_earth[i] = m ** 0.279
        elif m < 100:
            r_planet_earth[i] = m ** 0.589
        else:
            r_planet_earth[i] = m ** 0.010 * 11.2  # scale to Jupiter size
    r_planet_m = r_planet_earth * r_earth
    r_planet_jup = r_planet_m / r_jup
    
    # Orbital period (years)
    P_yr = np.sqrt(a_au**3)  # assuming solar mass
    
    # Host star properties (solar-type with dispersion)
    M_star = np.random.normal(1.0, 0.1, n_planets) * M_sun_kg
    R_star = np.random.normal(1.0, 0.1, n_planets) * R_sun_m
    T_eff = np.random.normal(5770, 500, n_planets)  # K
    
    # Distance (pc) – uniform in log space (nearby stars)
    dist_pc = 10 ** np.random.uniform(0.5, 2.5, n_planets)  # 3 to 316 pc
    
    # Occurrence scaling: multiply by occurrence_base to simulate different occurrence rates
    # We'll treat this as a weighting factor; we'll just generate extra planets and sample.
    # For simplicity, we'll just generate fixed number and let the survey simulate detection efficiency.
    
    # Planet types based on mass
    types = np.array(['Sub-Earth', 'Super-Earth', 'Neptune', 'Jupiter', 'Super-Jupiter'])
    type_idx = np.zeros(n_planets, dtype=int)
    for i, m in enumerate(mass_earth):
        if m < 1:
            type_idx[i] = 0
        elif m < 3:
            type_idx[i] = 1
        elif m < 10:
            type_idx[i] = 2
        elif m < 100:
            type_idx[i] = 3
        else:
            type_idx[i] = 4
    
    # Habitable zone (simplified for solar-like stars)
    # HZ = 0.95 * sqrt(L_star/L_sun) ... 1.5 * sqrt(...)
    L_star = (T_eff / 5770)**4 * (R_star / R_sun_m)**2  # in solar luminosities
    hz_inner = 0.75 * np.sqrt(L_star)  # AU
    hz_outer = 1.5 * np.sqrt(L_star)   # AU
    in_hz = (a_au > hz_inner) & (a_au < hz_outer)
    
    # Atmospheric type (based on mass and temperature)
    # We'll assign a simple category for characterisation
    atmos_type = np.array(['none', 'H2/He', 'H2O/CO2', 'rocky'])
    atmos_idx = np.zeros(n_planets, dtype=int)
    for i, m in enumerate(mass_earth):
        if m < 5:
            # rocky or super-earth with thin atmosphere
            atmos_idx[i] = 0 if np.random.rand() < 0.3 else 1
        elif m < 20:
            # Neptunian with H2/He or water
            atmos_idx[i] = 2 if np.random.rand() < 0.5 else 1
        else:
            # Gas giants with H2/He
            atmos_idx[i] = 1
    
    # Compile
    return {
        'mass_earth': mass_earth,
        'mass_kg': mass_kg,
        'mass_jup': mass_jup,
        'a_au': a_au,
        'a_m': a_m,
        'ecc': ecc,
        'incl_deg': incl_deg,
        'incl_rad': incl_rad,
        'r_earth': r_planet_earth,
        'r_m': r_planet_m,
        'r_jup': r_planet_jup,
        'P_yr': P_yr,
        'M_star': M_star,
        'R_star': R_star,
        'T_eff': T_eff,
        'dist_pc': dist_pc,
        'type_idx': type_idx,
        'types': types,
        'in_hz': in_hz,
        'atmos_idx': atmos_idx,
        'atmos_types': ['thin', 'H2/He', 'water/CO2', 'rocky'],
        'L_star': L_star,
    }

# -------------------------------------------------------------------
# 2. Survey simulator (multiple methods)
# -------------------------------------------------------------------
def simulate_survey(pop, method='transit', instrument_params=None):
    """
    Simulate detection of planets given a survey method.
    Returns boolean array of detected planets.
    """
    n = len(pop['mass_earth'])
    detected = np.zeros(n, dtype=bool)
    
    if method == 'transit':
        # TESS-like: noise_ppm, observing duration, cadence
        noise_ppm = instrument_params.get('noise_ppm', 100)
        min_transit_duration_hrs = instrument_params.get('min_duration', 0.5)
        max_period_days = instrument_params.get('max_period_days', 27)
        # Transit probability
        r_planet = pop['r_m']
        r_star = pop['R_star']
        a = pop['a_m']
        incl = pop['incl_rad']
        prob_transit = (r_star + r_planet) / a / np.sin(incl)  # sin i factor
        prob_transit = np.clip(prob_transit, 0, 1)
        transits = np.random.rand(n) < prob_transit
        if not np.any(transits):
            return detected
        # SNR: depth = (r_planet/r_star)^2 * 1e6
        depth_ppm = (r_planet / r_star)**2 * 1e6
        snr = depth_ppm / noise_ppm
        # Period
        period_days = pop['P_yr'] * 365.25
        # Duration
        dur_hrs = period_days * 24 * (r_star / (np.pi * a))  # rough
        # Detect if SNR > threshold and duration > min and period < max
        detected = transits & (snr > 5) & (dur_hrs > min_transit_duration_hrs) & (period_days < max_period_days)
        
    elif method == 'rv':
        # Ground-based RV: noise in m/s, observation span
        rv_noise = instrument_params.get('rv_noise', 1.0)
        min_snr = instrument_params.get('min_snr', 5)
        max_period_years = instrument_params.get('max_period_years', 10)
        # K amplitude (m/s)
        K = 28.4 * (pop['mass_jup']) * (pop['P_yr'])**(-1/3) * (pop['M_star']/M_sun_kg)**(-2/3)
        K *= 1 / np.sqrt(1 - pop['ecc']**2)
        K_obs = K * np.sin(pop['incl_rad'])
        snr = K_obs / rv_noise
        detected = (snr > min_snr) & (pop['P_yr'] < max_period_years)
        
    elif method == 'astrometry':
        # Gaia-like: noise in micro-arcsec
        astro_noise_as = instrument_params.get('astro_noise_as', 0.5) * 1e-3  # convert mas to as
        min_snr = instrument_params.get('min_snr', 5)
        max_period_years = instrument_params.get('max_period_years', 10)
        # Astrometric signal (as)
        a_rad = pop['a_m'] / (pop['dist_pc'] * pc_m)
        alpha_as = (pop['mass_jup'] / (pop['M_star']/M_sun_kg)) * a_rad * 206265
        alpha_obs = alpha_as * np.sin(pop['incl_rad'])
        snr = alpha_obs / astro_noise_as
        detected = (snr > min_snr) & (pop['P_yr'] < max_period_years)
        
    elif method == 'microlensing':
        # Simulate microlensing event detection (simplified)
        # Probability of lensing a background star
        lens_density = instrument_params.get('lens_density', 100)  # per sq deg
        # Einstein radius
        D_l = pop['dist_pc'] * pc_m
        D_s = D_l * 2.0
        M_total = pop['M_star'] + pop['mass_kg']
        theta_E = np.sqrt(4 * 6.674e-11 * M_total / (3e8)**2 * (D_s - D_l) / (D_l * D_s))
        theta_E_as = theta_E * 206265
        prob_lens = lens_density * (theta_E_as / 3600)**2 * 1000  # rough
        prob_lens = np.clip(prob_lens, 0, 1)
        lens_event = np.random.rand(n) < prob_lens
        if not np.any(lens_event):
            return detected
        # Magnification (assuming random impact parameter)
        impact = np.random.uniform(0, 1, n)  # in units of theta_E
        mag = 1 / np.sqrt(1 - impact**2) - 1  # excess
        detected = lens_event & (mag > 0.1) & (pop['P_yr'] > 0.5)  # long period
    return detected

# -------------------------------------------------------------------
# 3. Atmospheric characterisation & habitability
# -------------------------------------------------------------------
def characterise_atmospheres(pop, detected_mask, jwst_time_hrs=10, transmission_snr_threshold=5):
    """
    For detected planets, compute whether JWST can characterise the atmosphere.
    Transmission spectroscopy metric: SNR ∝ (R_p/R_star)^2 * sqrt(time) * sqrt(number of transits)
    """
    n = len(pop['mass_earth'])
    char_detected = np.zeros(n, dtype=bool)
    atmos_score = np.zeros(n)
    habitability = np.zeros(n)
    
    # For each planet, if detected and has atmosphere, check characterisation
    for i in range(n):
        if not detected_mask[i]:
            continue
        # Transmission signal (depth)
        depth = (pop['r_m'][i] / pop['R_star'][i])**2
        # Number of transits during JWST campaign (assume 1 year)
        n_transits = min(10, 365.25 / (pop['P_yr'][i] * 365.25) + 1)
        # SNR for JWST (simplified)
        snr_trans = depth * np.sqrt(jwst_time_hrs * n_transits) * 1000  # scaling
        if snr_trans > transmission_snr_threshold:
            char_detected[i] = True
            atmos_score[i] = snr_trans
        
        # Habitability: for rocky planets in HZ
        if pop['type_idx'][i] <= 1 and pop['in_hz'][i]:  # rocky/super-earth in HZ
            # Compute ESI-like score (0-1)
            # Factor 1: radius (0.5-2.0 Earth radii)
            r_factor = 1 - abs(pop['r_earth'][i] - 1.0) / 1.5
            r_factor = np.clip(r_factor, 0, 1)
            # Factor 2: stellar flux (insolation)
            flux = (pop['L_star'][i]) / (pop['a_au'][i]**2)
            flux_earth = 1.0  # solar constant at 1 AU
            flux_factor = 1 - abs(flux - flux_earth) / flux_earth
            flux_factor = np.clip(flux_factor, 0, 1)
            # Factor 3: mass (0.5-2 Earth masses)
            m_factor = 1 - abs(pop['mass_earth'][i] - 1.0) / 1.5
            m_factor = np.clip(m_factor, 0, 1)
            habitability[i] = (r_factor + flux_factor + m_factor) / 3
        else:
            habitability[i] = 0.0
    
    return char_detected, atmos_score, habitability

# -------------------------------------------------------------------
# 4. Mission cost model
# -------------------------------------------------------------------
def mission_cost(method, duration_years, number_of_targets):
    """
    Simplified cost model in arbitrary units.
    Transit: cheap per target, needs spacecraft.
    RV: moderate cost per target, ground-based.
    Astrometry: expensive per target.
    Microlensing: moderate cost for survey.
    """
    if method == 'transit':
        cost = 50 + 0.1 * number_of_targets * duration_years
    elif method == 'rv':
        cost = 20 + 0.5 * number_of_targets * duration_years
    elif method == 'astrometry':
        cost = 100 + 1.0 * number_of_targets * duration_years
    elif method == 'microlensing':
        cost = 30 + 0.3 * number_of_targets * duration_years
    else:
        cost = 100
    return cost

# -------------------------------------------------------------------
# 5. Main interactive function
# -------------------------------------------------------------------
def run_population_survey(n_planets=5000, occurrence_scale=1.0,
                          method='transit', noise_ppm=100, rv_noise=1.0,
                          astro_noise=0.5, lens_density=50, jwst_time=10,
                          show_characterisation=True, show_habitability=True):
    # Generate population
    pop = generate_planet_population(n_planets, seed=42, occurrence_base=occurrence_scale)
    
    # Instrument params
    if method == 'transit':
        params = {'noise_ppm': noise_ppm, 'min_duration': 0.5, 'max_period_days': 27}
    elif method == 'rv':
        params = {'rv_noise': rv_noise, 'min_snr': 5, 'max_period_years': 10}
    elif method == 'astrometry':
        params = {'astro_noise_as': astro_noise, 'min_snr': 5, 'max_period_years': 10}
    elif method == 'microlensing':
        params = {'lens_density': lens_density}
    else:
        params = {}
    
    # Simulate detection
    detected = simulate_survey(pop, method, params)
    
    # Characterisation & habitability
    if show_characterisation:
        char_detected, atmos_score, habitability = characterise_atmospheres(pop, detected, jwst_time)
    else:
        char_detected = np.zeros(n_planets, dtype=bool)
        atmos_score = np.zeros(n_planets)
        habitability = np.zeros(n_planets)
    
    # Cost
    n_targets = int(np.sum(detected))
    cost = mission_cost(method, 3, n_targets)  # assume 3-year mission
    
    # ---- Plotting ----
    fig = plt.figure(figsize=(16, 12))
    gs = gridspec.GridSpec(2, 3, height_ratios=[1, 1])
    
    # Panel 1: Mass vs Semi-major axis (discovery space)
    ax = fig.add_subplot(gs[0, 0])
    ax.scatter(pop['a_au'], pop['mass_earth'], s=5, alpha=0.3, label='All')
    if np.any(detected):
        ax.scatter(pop['a_au'][detected], pop['mass_earth'][detected], s=20, c='red', label='Detected')
    if show_characterisation and np.any(char_detected):
        ax.scatter(pop['a_au'][char_detected], pop['mass_earth'][char_detected], s=60, facecolors='none', edgecolors='cyan', linewidths=1.5, label='Characterised')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('Semi-major axis (AU)'); ax.set_ylabel('Mass (M_earth)')
    ax.set_title(f'Discovery space ({method})')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_xlim(0.01, 100); ax.set_ylim(0.5, 5000)
    
    # Panel 2: Detection yield by planet type
    ax = fig.add_subplot(gs[0, 1])
    types = pop['types']
    unique_types = np.unique(types)
    counts_all = [np.sum(types == t) for t in unique_types]
    counts_det = [np.sum(types[detected] == t) for t in unique_types]
    x = np.arange(len(unique_types))
    width = 0.35
    ax.bar(x - width/2, counts_all, width, label='All', color='gray', alpha=0.6)
    ax.bar(x + width/2, counts_det, width, label='Detected', color='red', alpha=0.8)
    ax.set_xticks(x); ax.set_xticklabels(unique_types, rotation=45)
    ax.set_ylabel('Count')
    ax.set_title('Yield by planet type')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    # Panel 3: Period vs distance (detectability)
    ax = fig.add_subplot(gs[0, 2])
    ax.scatter(pop['P_yr'], pop['dist_pc'], s=5, alpha=0.3, label='All')
    if np.any(detected):
        ax.scatter(pop['P_yr'][detected], pop['dist_pc'][detected], s=20, c='red', label='Detected')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('Orbital Period (yr)'); ax.set_ylabel('Distance (pc)')
    ax.set_title('Period–distance detectability')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Panel 4: Habitability (if enabled)
    ax = fig.add_subplot(gs[1, 0])
    if show_habitability and np.any(habitability > 0):
        # Habitable zone planets
        hz_mask = pop['in_hz'] & (pop['type_idx'] <= 1)  # rocky/super-earth
        if np.any(hz_mask):
            ax.scatter(pop['a_au'][hz_mask], pop['mass_earth'][hz_mask], c=habitability[hz_mask], s=30, cmap='RdYlGn', vmin=0, vmax=1)
            ax.set_xscale('log'); ax.set_yscale('log')
            ax.set_xlabel('Semi-major axis (AU)'); ax.set_ylabel('Mass (M_earth)')
            ax.set_title('Habitability score (green = high)')
            plt.colorbar(ax.collections[0], ax=ax, fraction=0.05, label='Habitability')
            ax.grid(alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'No habitable planets', ha='center', va='center', transform=ax.transAxes)
    else:
        ax.text(0.5, 0.5, 'Habitability disabled', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Habitability')
    
    # Panel 5: Characterisation yield (if enabled)
    ax = fig.add_subplot(gs[1, 1])
    if show_characterisation:
        # Show SNR distribution for characterised planets
        if np.any(char_detected):
            snr_vals = atmos_score[char_detected]
            ax.hist(snr_vals, bins=20, color='cyan', alpha=0.7)
            ax.set_xlabel('Transmission SNR (JWST)')
            ax.set_ylabel('Count')
            ax.set_title(f'Characterisation yield: {np.sum(char_detected)} planets')
        else:
            ax.text(0.5, 0.5, 'No characterisation possible', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Characterisation')
    else:
        ax.text(0.5, 0.5, 'Characterisation disabled', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Characterisation')
    ax.grid(alpha=0.3)
    
    # Panel 6: Summary stats + cost
    ax = fig.add_subplot(gs[1, 2])
    ax.axis('off')
    n_detected = np.sum(detected)
    n_char = np.sum(char_detected) if show_characterisation else 0
    n_hz = np.sum(pop['in_hz'] & (pop['type_idx'] <= 1)) if show_habitability else 0
    total_mass = np.sum(pop['mass_earth'])
    summary = f"""
    📊 SURVEY STATISTICS
    ──────────────────────────────
    Population:             {n_planets} planets
    Method:                 {method}
    Detected:               {n_detected} ({n_detected/n_planets*100:.1f}%)
    Characterised (JWST):   {n_char}
    Habitable candidates:   {n_hz}
    
    Mission cost:           {cost:.0f} units
    Planets per cost:       {n_detected/cost:.2f}
    ──────────────────────────────
    Total mass (M_earth):   {total_mass:.2e}
    Average period:         {np.mean(pop['P_yr']):.2f} yr
    Average distance:       {np.mean(pop['dist_pc']):.1f} pc
    """
    ax.text(0.05, 0.95, summary, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
    
    plt.tight_layout()
    plt.show()
    
    # Additional prints
    print(f"\n🔭 Survey yield: {n_detected} planets detected with {method}.")
    if show_characterisation:
        print(f"🪐 Atmospheric characterisation possible for {n_char} planets with JWST.")
    if show_habitability:
        print(f"🌍 {n_hz} rocky planets in the habitable zone.")

# -------------------------------------------------------------------
# 6. Interactive widgets
# -------------------------------------------------------------------
style = {'description_width': 'initial'}
controls = {
    'n_planets': IntSlider(value=5000, min=1000, max=20000, step=500, description='Population size', style=style),
    'occurrence_scale': FloatSlider(value=1.0, min=0.1, max=3.0, step=0.1, description='Occurrence scale', style=style),
    'method': Dropdown(options=['transit', 'rv', 'astrometry', 'microlensing'], value='transit', description='Survey method', style=style),
    'noise_ppm': FloatSlider(value=100, min=10, max=500, step=10, description='Transit noise (ppm)', style=style),
    'rv_noise': FloatSlider(value=1.0, min=0.1, max=5.0, step=0.1, description='RV noise (m/s)', style=style),
    'astro_noise': FloatSlider(value=0.5, min=0.05, max=2.0, step=0.05, description='Astrometry noise (mas)', style=style),
    'lens_density': FloatSlider(value=50, min=5, max=200, step=5, description='Lens density', style=style),
    'jwst_time': FloatSlider(value=10, min=1, max=50, step=1, description='JWST time (hrs)', style=style),
    'show_characterisation': Dropdown(options=[True, False], value=True, description='Show characterisation', style=style),
    'show_habitability': Dropdown(options=[True, False], value=True, description='Show habitability', style=style)
}

out = Output()
def update(**kwargs):
    with out:
        clear_output(wait=True)
        run_population_survey(**kwargs)

interactive_widget = interactive(update, **controls)
display(HBox([VBox([controls[k] for k in controls]), out]))

# -------------------------------------------------------------------
# 7. Run default case
# -------------------------------------------------------------------
print("🚀 RUNNING EXOPLANET POPULATION SYNTHESIS & SURVEY")
print("   Simulating a galactic population and surveying with the chosen method.\n")
run_population_survey(n_planets=5000, method='transit', noise_ppm=100,
                      show_characterisation=True, show_habitability=True)
