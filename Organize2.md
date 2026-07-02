# ===================================================================
#  EXOPLANET DATA ARCHAEOLOGY LAB
#  False positives + Follow-up budget + ML classifier
#  ===================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from ipywidgets import interact, FloatSlider, IntSlider, Dropdown, VBox, HBox, Output, interactive
from IPython.display import display, clear_output
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# -------------------------------------------------------------------
# 1. Physical constants & planet generator (same as before)
# -------------------------------------------------------------------
R_sun = 6.957e8
R_jup = 6.991e7
M_sun = 1.989e30
M_jup = 1.898e27
AU = 1.496e11
G = 6.674e-11
c = 3e8
pc = 3.086e16

def generate_system(seed=None):
    np.random.seed(seed)
    M_star = np.random.uniform(0.5, 1.2) * M_sun
    R_star = np.random.uniform(0.5, 1.2) * R_sun
    dist_pc = np.random.uniform(50, 500)
    M_planet = 10 ** np.random.uniform(-1.0, 2.0) * M_jup
    a_au = 10 ** np.random.uniform(-1.0, 2.0)
    a = a_au * AU
    incl_deg = np.random.uniform(0, 180)
    incl_rad = np.radians(incl_deg)
    ecc = np.random.uniform(0, 0.5)
    omega = np.random.uniform(0, 2*np.pi)
    return {
        'M_star': M_star, 'R_star': R_star, 'dist_pc': dist_pc,
        'M_planet': M_planet, 'a': a, 'a_au': a_au,
        'incl_deg': incl_deg, 'incl_rad': incl_rad,
        'ecc': ecc, 'omega': omega,
        'P_yr': np.sqrt(a_au**3 / (M_star/M_sun)),
        'seed': seed
    }

# -------------------------------------------------------------------
# 2. Detection functions (with false positives)
# -------------------------------------------------------------------
def detect_transit(system, noise_ppm=100, min_snr=5):
    R_planet = (system['M_planet'] / M_jup)**(1/3) * R_jup
    prob_transit = (system['R_star'] + R_planet) / system['a']
    prob_transit *= 1 / np.sin(system['incl_rad']) if system['incl_rad'] > 0 else 0
    prob_transit = min(1, prob_transit)
    transits = np.random.rand() < prob_transit
    if not transits:
        return False, 0.0, 0.0, False
    depth_ppm = (R_planet / system['R_star'])**2 * 1e6
    period_hrs = system['P_yr'] * 365.25 * 24
    duration_hrs = period_hrs * (system['R_star'] / (np.pi * system['a']))
    duration_hrs = max(0.1, duration_hrs)
    # Noise threshold
    snr = depth_ppm / noise_ppm
    detected = snr > min_snr and duration_hrs > 0.5 and period_hrs < 27*24
    # False positive: sometimes a noise spike mimics a transit
    fp = (not detected) and (np.random.rand() < 0.05)  # 5% false alarm
    return detected or fp, depth_ppm, duration_hrs, fp

def detect_rv(system, rv_noise=1.0, min_snr=5):
    K = 28.4 * (system['M_planet'] / M_jup) * (system['P_yr'])**(-1/3) * (system['M_star']/M_sun)**(-2/3)
    K *= 1 / np.sqrt(1 - system['ecc']**2)
    K_obs = K * np.sin(system['incl_rad'])
    snr = K_obs / rv_noise
    detected = snr > min_snr and system['P_yr'] < 10
    fp = (not detected) and (np.random.rand() < 0.03)  # 3% false alarm
    return detected or fp, K_obs, snr, fp

def detect_microlensing(system, background_star_density=100, min_mag=0.1):
    D_l = system['dist_pc'] * pc
    D_s = D_l * 2.0
    M_total = system['M_star'] + system['M_planet']
    theta_E = np.sqrt(4 * G * M_total / c**2 * (D_s - D_l) / (D_l * D_s))
    theta_E_as = theta_E * 206265
    v_t = 20e3
    t_E_days = (theta_E * D_l) / v_t / 86400
    t_E_days = max(0.5, t_E_days)
    impact_param = np.random.uniform(0, 2)
    if impact_param < 1:
        mag = 1 / np.sqrt(1 - impact_param**2) - 1
    else:
        mag = 0
    prob_lens = min(1, background_star_density * (theta_E_as / 3600)**2 * 1000)
    lensing_event = np.random.rand() < prob_lens
    if not lensing_event:
        return False, 0.0, 0.0, 0.0, False
    detected = mag > min_mag and t_E_days > 0.5
    fp = (not detected) and (np.random.rand() < 0.02)  # 2% false alarm
    return detected or fp, mag, t_E_days, theta_E_as, fp

def detect_astrometry(system, astro_noise_as=0.1, min_snr=5):
    a_rad = system['a'] / (system['dist_pc'] * pc)
    alpha_as = (system['M_planet'] / system['M_star']) * a_rad * 206265
    alpha_obs = alpha_as * np.sin(system['incl_rad'])
    snr = alpha_obs / astro_noise_as
    detected = snr > min_snr and system['P_yr'] < 20
    fp = (not detected) and (np.random.rand() < 0.01)  # 1% false alarm
    return detected or fp, alpha_obs, snr, fp

# -------------------------------------------------------------------
# 3. Survey with false positives
# -------------------------------------------------------------------
def run_survey_with_fp(n_systems, transit_noise, rv_noise, lens_density, astro_noise, min_snr=5):
    results = []
    for i in range(n_systems):
        sys = generate_system(seed=i)
        t_det, depth, dur, t_fp = detect_transit(sys, noise_ppm=transit_noise, min_snr=min_snr)
        rv_det, K, snr_rv, rv_fp = detect_rv(sys, rv_noise=rv_noise, min_snr=min_snr)
        lens_det, mag, tE, thetaE, lens_fp = detect_microlensing(sys, background_star_density=lens_density)
        astro_det, alpha, snr_astro, astro_fp = detect_astrometry(sys, astro_noise_as=astro_noise, min_snr=min_snr)
        
        # Combine flags: candidates are detections (including FPs)
        detections = {
            'Transit': t_det,
            'RV': rv_det,
            'Microlensing': lens_det,
            'Astrometry': astro_det
        }
        false_positives = {
            'Transit': t_fp,
            'RV': rv_fp,
            'Microlensing': lens_fp,
            'Astrometry': astro_fp
        }
        # Determine if it's a real planet (not a false positive)
        is_real = not any(false_positives.values())
        # Hidden gem: real planet, detected by lensing+astro, not transit
        is_hidden_gem = is_real and lens_det and astro_det and not t_det
        
        results.append({
            'system': sys,
            'detections': detections,
            'false_positives': false_positives,
            'is_real': is_real,
            'is_hidden_gem': is_hidden_gem,
            'depth_ppm': depth, 'K_ms': K, 'mag': mag, 'alpha_as': alpha,
            'a_au': sys['a_au'], 'M_jup': sys['M_planet']/M_jup, 
            'P_yr': sys['P_yr'], 'incl_deg': sys['incl_deg'],
            'snr_rv': snr_rv, 'snr_astro': snr_astro
        })
    return results

# -------------------------------------------------------------------
# 4. Follow-up budget optimizer
# -------------------------------------------------------------------
def optimize_followup(results, budget_nights=20, cost_per_candidate=1.0):
    """
    Given a list of results (candidates), allocate follow-up to maximize confirmed planets.
    Simple strategy: prioritize candidates with high SNR and multiple detections.
    """
    # Candidates: systems with at least one detection
    candidates = [r for r in results if any(r['detections'].values())]
    if not candidates:
        return [], 0
    
    # Score each candidate: higher score = more likely to be real
    scores = []
    for r in candidates:
        # Base score: number of detection methods
        n_det = sum(r['detections'].values())
        # SNR bonus (RV and astrometry)
        snr_score = (r['snr_rv'] if r['detections']['RV'] else 0) + \
                    (r['snr_astro'] if r['detections']['Astrometry'] else 0)
        # Microlensing magnification bonus
        lens_score = r['mag'] * 10 if r['detections']['Microlensing'] else 0
        total = n_det * 5 + snr_score * 0.5 + lens_score
        scores.append(total)
    
    # Sort by score descending
    sorted_idx = np.argsort(scores)[::-1]
    # Allocate nights: each candidate costs cost_per_night, but we can observe multiple
    allocated = []
    nights_used = 0
    for idx in sorted_idx:
        if nights_used + cost_per_candidate <= budget_nights:
            allocated.append(candidates[idx])
            nights_used += cost_per_candidate
        else:
            break
    
    # Determine how many of the allocated are real planets
    confirmed = [r for r in allocated if r['is_real']]
    return allocated, len(confirmed), nights_used

# -------------------------------------------------------------------
# 5. Machine Learning classifier for hidden gems
# -------------------------------------------------------------------
def train_ml_classifier(results, test_size=0.3):
    """Train a Random Forest to predict if a candidate is a real planet."""
    # Features: detection flags, SNR, depth, etc.
    X = []
    y = []
    for r in results:
        # Only use candidates (systems with at least one detection)
        if not any(r['detections'].values()):
            continue
        features = [
            r['detections']['Transit'],
            r['detections']['RV'],
            r['detections']['Microlensing'],
            r['detections']['Astrometry'],
            r['snr_rv'] if r['detections']['RV'] else 0,
            r['snr_astro'] if r['detections']['Astrometry'] else 0,
            r['depth_ppm'] if r['detections']['Transit'] else 0,
            r['mag'] if r['detections']['Microlensing'] else 0,
            r['a_au'], r['M_jup'], r['P_yr'], r['incl_deg']
        ]
        X.append(features)
        y.append(1 if r['is_real'] else 0)  # 1 = real, 0 = false positive
    
    if len(X) < 10:
        return None, None, None, None  # Not enough data
    
    X = np.array(X)
    y = np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    # Report
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)
    
    return clf, X_test, y_test, y_pred, report, cm

# -------------------------------------------------------------------
# 6. Visualisation engine (upgraded)
# -------------------------------------------------------------------
def plot_survey_with_fp(results, budget_nights=20, show_ml=True):
    n = len(results)
    if n == 0:
        print("No results.")
        return
    
    # Extract data
    M_jup = np.array([r['M_jup'] for r in results])
    a_au = np.array([r['a_au'] for r in results])
    P_yr = np.array([r['P_yr'] for r in results])
    incl = np.array([r['incl_deg'] for r in results])
    is_real = np.array([r['is_real'] for r in results])
    is_hidden_gem = np.array([r['is_hidden_gem'] for r in results])
    
    # Detection flags
    transit_flags = np.array([r['detections']['Transit'] for r in results])
    rv_flags = np.array([r['detections']['RV'] for r in results])
    lens_flags = np.array([r['detections']['Microlensing'] for r in results])
    astro_flags = np.array([r['detections']['Astrometry'] for r in results])
    
    # False positives
    fp_flags = np.array([any(r['false_positives'].values()) for r in results])
    
    # Follow-up optimization
    allocated, confirmed_count, nights_used = optimize_followup(results, budget_nights)
    allocated_idx = [results.index(r) for r in allocated]
    
    # ML (if requested)
    if show_ml:
        clf, X_test, y_test, y_pred, report, cm = train_ml_classifier(results)
        ml_available = clf is not None
    else:
        ml_available = False
    
    # Figure
    fig = plt.figure(figsize=(18, 12))
    gs = gridspec.GridSpec(2, 3, height_ratios=[1, 1])
    
    # ---- Panel 1: Discovery space with FP markers ----
    ax = fig.add_subplot(gs[0, 0])
    # All candidates (grey)
    ax.scatter(a_au, M_jup, c='lightgray', s=20, alpha=0.4, label='Candidates')
    # Real planets (green)
    real_mask = is_real & ~fp_flags
    ax.scatter(a_au[real_mask], M_jup[real_mask], c='green', s=40, label='Real planets', alpha=0.7)
    # False positives (red x)
    fp_mask = fp_flags
    ax.scatter(a_au[fp_mask], M_jup[fp_mask], marker='x', c='red', s=50, label='False positives')
    # Hidden gems (stars)
    gem_mask = is_hidden_gem
    if np.any(gem_mask):
        ax.scatter(a_au[gem_mask], M_jup[gem_mask], marker='*', s=200, c='gold', 
                   edgecolors='black', label='⭐ Hidden Gems')
    # Follow-up allocated (cyan circles)
    if allocated_idx:
        ax.scatter(a_au[allocated_idx], M_jup[allocated_idx], facecolors='none', 
                   edgecolors='cyan', s=150, linewidths=2, label='Follow-up allocated')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('Semi-major axis (AU)'); ax.set_ylabel('Mass (M_Jup)')
    ax.set_title('Discovery Space with FPs & Follow-up')
    ax.legend(loc='lower right', fontsize=7)
    ax.grid(alpha=0.3)
    ax.set_xlim(0.05, 200); ax.set_ylim(0.05, 200)
    
    # ---- Panel 2: Follow-up budget efficiency ----
    ax = fig.add_subplot(gs[0, 1])
    # Show how many real vs FP among allocated
    if allocated:
        real_alloc = [r for r in allocated if r['is_real']]
        fp_alloc = [r for r in allocated if not r['is_real']]
        labels = ['Real confirmed', 'False positives']
        sizes = [len(real_alloc), len(fp_alloc)]
        colors = ['green', 'red']
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, explode=(0.05, 0))
        ax.set_title(f'Follow-up result (nights used: {nights_used:.1f}/{budget_nights})')
    else:
        ax.text(0.5, 0.5, 'No candidates to follow up', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Follow-up allocation')
    
    # ---- Panel 3: False positive rate per method ----
    ax = fig.add_subplot(gs[0, 2])
    methods = ['Transit', 'RV', 'Microlensing', 'Astrometry']
    fp_counts = [np.sum([r['false_positives'][m] for r in results]) for m in methods]
    real_counts = [np.sum([r['detections'][m] and r['is_real'] for r in results]) for m in methods]
    total_counts = [fp_counts[i] + real_counts[i] for i in range(4)]
    # Bar chart with stacked
    x = np.arange(len(methods))
    width = 0.6
    ax.bar(x, real_counts, width, label='Real', color='green', alpha=0.7)
    ax.bar(x, fp_counts, width, bottom=real_counts, label='False positive', color='red', alpha=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.set_ylabel('Count')
    ax.set_title('Detection breakdown: Real vs FP')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    # ---- Panel 4: ML classifier performance ----
    ax = fig.add_subplot(gs[1, 0])
    if ml_available:
        # Show confusion matrix
        im = ax.imshow(cm, cmap='Blues', origin='lower', vmin=0, vmax=cm.max())
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(['Predicted FP', 'Predicted Real'])
        ax.set_yticklabels(['True FP', 'True Real'])
        ax.set_title('ML Confusion Matrix')
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f'{cm[i, j]}', ha='center', va='center', 
                        color='white' if cm[i, j] > cm.max()/2 else 'black')
        plt.colorbar(im, ax=ax, fraction=0.05)
        # Print accuracy
        acc = report['accuracy']
        ax.set_xlabel(f'Accuracy: {acc:.2f}')
    else:
        ax.text(0.5, 0.5, 'Not enough candidates\nfor ML training', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('ML Classifier')
    
    # ---- Panel 5: Hidden gems and their properties ----
    ax = fig.add_subplot(gs[1, 1])
    if np.any(is_hidden_gem):
        gem_data = results[is_hidden_gem]
        gem_mass = [r['M_jup'] for r in gem_data]
        gem_a = [r['a_au'] for r in gem_data]
        gem_p = [r['P_yr'] for r in gem_data]
        ax.scatter(gem_a, gem_mass, s=150, c='gold', marker='*', label='Hidden Gems', zorder=10)
        for i, r in enumerate(gem_data):
            ax.annotate(f"P={r['P_yr']:.1f}yr", (r['a_au'], r['M_jup']), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        ax.set_xscale('log'); ax.set_yscale('log')
        ax.set_xlabel('Semi-major axis (AU)'); ax.set_ylabel('Mass (M_Jup)')
        ax.set_title(f'⭐ {np.sum(is_hidden_gem)} Hidden Gems detected')
        ax.grid(alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'No hidden gems found', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Hidden Gems')
    
    # ---- Panel 6: Summary stats ----
    ax = fig.add_subplot(gs[1, 2])
    ax.axis('off')
    n_candidates = np.sum([any(r['detections'].values()) for r in results])
    n_real = np.sum(is_real)
    n_fp = np.sum(fp_flags)
    n_gems = np.sum(is_hidden_gem)
    n_allocated = len(allocated)
    n_confirmed = confirmed_count
    summary = f"""
    📊 SURVEY + FOLLOW-UP SUMMARY
    ──────────────────────────────
    Total systems:           {n}
    Candidates detected:     {n_candidates}
    Real planets:            {n_real}
    False positives:         {n_fp}
    Hidden Gems (lens+astro):{n_gems}
    
    Follow-up budget:        {budget_nights} nights
    Nights used:             {nights_used:.1f}
    Planets confirmed:       {n_confirmed}
    Confirmation efficiency: {n_confirmed/n_allocated*100 if n_allocated>0 else 0:.1f}%
    """
    ax.text(0.05, 0.95, summary, transform=ax.transAxes, fontsize=11, 
            verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
    
    plt.tight_layout()
    plt.show()
    
    # Print ML report if available
    if ml_available:
        print("\n🤖 Machine Learning Classification Report:")
        print(classification_report(y_test, y_pred))

# -------------------------------------------------------------------
# 7. Interactive wrapper
# -------------------------------------------------------------------
def run_interactive_survey_full(n_systems=100, transit_noise=100, rv_noise=1.0,
                                lens_density=50, astro_noise=0.5, budget=20, show_ml=True):
    results = run_survey_with_fp(n_systems, transit_noise, rv_noise, lens_density, astro_noise)
    plot_survey_with_fp(results, budget_nights=budget, show_ml=show_ml)
    print(f"\n🔍 Found {np.sum([r['is_hidden_gem'] for r in results])} Hidden Gems.")

# -------------------------------------------------------------------
# 8. Interactive controls
# -------------------------------------------------------------------
style = {'description_width': 'initial'}
controls = {
    'n_systems': IntSlider(value=150, min=30, max=300, step=10, description='Number of systems', style=style),
    'transit_noise': FloatSlider(value=100, min=10, max=500, step=10, description='Transit noise (ppm)', style=style),
    'rv_noise': FloatSlider(value=1.0, min=0.1, max=5.0, step=0.1, description='RV noise (m/s)', style=style),
    'lens_density': FloatSlider(value=50, min=5, max=200, step=5, description='Lens density', style=style),
    'astro_noise': FloatSlider(value=0.5, min=0.05, max=2.0, step=0.05, description='Astrometry noise (mas)', style=style),
    'budget': IntSlider(value=20, min=5, max=60, step=5, description='Follow-up budget (nights)', style=style),
    'show_ml': Dropdown(options=[True, False], value=True, description='Show ML classifier', style=style)
}

out = Output()
def update(**kwargs):
    with out:
        clear_output(wait=True)
        run_interactive_survey_full(**kwargs)

interactive_widget = interactive(update, **controls)
display(HBox([VBox([controls[k] for k in controls]), out]))

# -------------------------------------------------------------------
# 9. Run a default case (simulating the Gaia23bra b discovery)
# -------------------------------------------------------------------
print("🚀 RUNNING FULL SURVEY + FOLLOW-UP + ML")
print("   Simulating TESS+Gaia microlensing discovery with false positives,\n   follow-up optimisation, and ML to identify hidden gems.\n")
run_interactive_survey_full(n_systems=150, transit_noise=100, rv_noise=1.0,
                            lens_density=50, astro_noise=0.5, budget=20, show_ml=True)



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


# ===================================================================
#  PHOTON UPCONVERSION SEARCH & EXPLORE SIMULATOR
#  TTA-PUC kinetics + Solar cell efficiency boost
#  ===================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from ipywidgets import interact, FloatSlider, IntSlider, Dropdown, VBox, HBox, Output, interactive
from IPython.display import display, clear_output
from scipy.optimize import minimize_scalar

# -------------------------------------------------------------------
# 1. Physical constants and parameters
# -------------------------------------------------------------------
h = 6.626e-34          # J·s
c = 3e8                # m/s
q = 1.602e-19          # C
eV = q

# Solar spectrum (AM1.5G) simplified as a blackbody at 5770 K with scaling
# We'll use a simple photon flux model: blackbody spectrum in W/m^2/nm
def solar_flux(wavelength_nm, T=5770, scale=0.7):
    """Blackbody spectral radiance (W/m^2/nm) scaled to AM1.5G."""
    lam = wavelength_nm * 1e-9  # m
    # Planck function: B_lambda = (2hc^2/lambda^5) / (exp(hc/(lambda kT))-1)
    B = (2*h*c**2 / lam**5) / (np.exp(h*c/(lam*1.38e-23*T)) - 1)
    # Convert to W/m^2/nm (multiply by pi and convert to per nm)
    flux = B * np.pi * 1e-9  # per nm
    return flux * scale  # rough scaling to match AM1.5

# -------------------------------------------------------------------
# 2. TTA-PUC kinetic model
# -------------------------------------------------------------------
def tta_puc_quantum_yield(I_exc, sigma_s, tau_T, k_TT, phi_ISC=0.9, phi_ET=0.8, phi_em=0.9):
    """
    Compute upconversion quantum yield (UC QY) for given excitation intensity (I_exc in W/m^2).
    Parameters:
    - sigma_s: sensitizer absorption cross-section (m^2) times concentration (1/m^3) -> effective absorption coefficient (1/m)
    - tau_T: triplet lifetime (s)
    - k_TT: triplet-triplet annihilation rate (m^3/s)
    - phi_ISC: intersystem crossing efficiency
    - phi_ET: triplet energy transfer efficiency
    - phi_em: emitter singlet emission efficiency
    """
    # Triplet population (steady state) from rate equation:
    # d[T]/dt = phi_ISC * phi_ET * I_exc * sigma_s - [T]/tau_T - 2*k_TT*[T]^2 = 0
    # Solve quadratic: 2*k_TT*[T]^2 + (1/tau_T)*[T] - phi_ISC*phi_ET*I_exc*sigma_s = 0
    a = 2 * k_TT
    b = 1.0 / tau_T
    c = - phi_ISC * phi_ET * I_exc * sigma_s
    if c <= 0:
        return 0.0, 0.0
    disc = b**2 - 4*a*c
    if disc < 0:
        return 0.0, 0.0
    T_pop = (-b + np.sqrt(disc)) / (2*a)
    # Upconversion rate = phi_ISC*phi_ET * k_TT * T_pop^2 (annihilation produces high-energy photons)
    UC_rate = phi_ISC * phi_ET * k_TT * T_pop**2
    # Also triplet decay rate = T_pop / tau_T
    # Quantum yield = UC_rate / (I_exc * sigma_s)  (energy conservation)
    # Actually UC QY = (UC_rate) / (I_exc * sigma_s) but we need to account for excitation loss
    # More precisely: number of upconverted photons = UC_rate * phi_em (since each annihilated pair yields one photon)
    upconverted_photons = UC_rate * phi_em
    absorbed_photons = I_exc * sigma_s  # per unit time per unit volume? Actually it's per area.
    # But we treat I_exc as per area, sigma_s is absorption coefficient (1/m). 
    # For simplicity, we define quantum yield as ratio of emitted high-energy photons to absorbed photons:
    QY = upconverted_photons / (I_exc * sigma_s) if I_exc*sigma_s > 0 else 0
    return QY, T_pop

# -------------------------------------------------------------------
# 3. Solar cell model with upconversion
# -------------------------------------------------------------------
def solar_cell_efficiency_with_UC(lambda_nm, bandgap_eV, uc_qy_func, I_solar, uc_wavelength_nm=413):
    """
    Compute solar cell efficiency gain using upconversion.
    - lambda_nm: array of wavelengths (nm) for solar spectrum
    - bandgap_eV: bandgap energy of solar cell (eV)
    - uc_qy_func: function that returns UC QY for given input intensity at a specific wavelength.
    - I_solar: solar flux (W/m^2/nm) as function of wavelength.
    - uc_wavelength_nm: wavelength of upconverted emission (e.g., 413 nm).
    """
    # Solar spectrum photon flux (photon flux per nm)
    photon_flux_nm = I_solar(lambda_nm) / (h*c / (lambda_nm*1e-9))  # photons/s/m^2/nm
    # Bandgap edge wavelength (nm)
    lambda_g_nm = 1240 / bandgap_eV  # nm
    
    # Photons below bandgap (longer wavelength) that can be upconverted
    # We'll assume upconversion works for wavelengths longer than lambda_g (i.e., below bandgap)
    # Actually upconversion converts low-energy photons (e.g., 533 nm) to high-energy (413 nm)
    # We'll focus on a specific input wavelength (e.g., 533 nm) for simplicity, but can extend.
    # For a broadband model, we could integrate over a range. We'll do a simplified one: we assume all below-bandgap photons at a specific wavelength (e.g., 533 nm) are upconverted.
    # But for more realistic, we can scan over a range. Let's do a two-wavelength model: input at 533 nm, output at 413 nm.
    
    # For this simulation, we'll assume the upconversion is applied to the 533 nm photons (or a narrow band).
    # The solar flux at 533 nm:
    I_533 = I_solar(533)  # W/m^2/nm
    # Photon flux at 533 nm (per nm)
    photon_flux_533 = I_533 / (h*c/(533e-9))  # photons/s/m^2/nm
    # We'll treat this as the excitation intensity for the UC process.
    # But the UC QY depends on the intensity of that light.
    # We'll use the TTA-PUC model to compute QY as a function of intensity.
    # However, the intensity is not just the monochromatic flux; it's the actual power density.
    # Let's assume we can concentrate the light or use a certain fraction.
    # We'll use a parameter "fraction_of_below_bandgap_light" that we can sweep.
    
    # For simplicity, we'll compute the total below-bandgap power and assume a fraction is used for UC.
    below_gap_mask = lambda_nm > lambda_g_nm
    P_below = np.trapz(I_solar(lambda_nm[below_gap_mask]), lambda_nm[below_gap_mask])  # W/m^2
    
    # We'll assume we can couple a fraction f_UC of this below-gap power into the UC material.
    # The UC process will convert some of that to above-gap photons.
    # The efficiency of conversion is the UC QY at the excitation intensity.
    # We'll compute QY at the peak intensity of that band.
    # For a first approximation, we'll take the average intensity of the below-gap band.
    avg_intensity = P_below / (lambda_nm[-1] - lambda_g_nm)  # W/m^2/nm
    
    # But UC QY depends on the actual irradiance (W/m^2) on the material, not per nm.
    # Let's assume we have a narrowband laser at 533 nm with intensity I_laser (W/m^2).
    # For this simulation, we'll sweep the laser intensity and see the gain.
    # We'll create a function that returns the solar cell Jsc (A/m^2) with and without UC.
    
    # Without UC:
    # Photons with energy > bandgap contribute to current: each photon gives one electron.
    above_gap_mask = lambda_nm <= lambda_g_nm
    Jsc_noUC = q * np.trapz(photon_flux_nm[above_gap_mask], lambda_nm[above_gap_mask])  # A/m^2
    
    # With UC: we convert some below-gap photons to above-gap.
    # Let's choose a specific input wavelength for UC, e.g., 533 nm.
    # The UC QY at that wavelength's intensity.
    # We'll compute the output photon flux = UC_QY * input photon flux at 533 nm.
    # Then these photons (at 413 nm) contribute to current.
    # Let's assume we can focus all below-gap light into the UC material with efficiency f_coupling.
    # We'll treat the excitation intensity I_exc as the actual solar irradiance at 533 nm integrated over a narrow band.
    # But to explore, we'll let user adjust the excitation power density (W/m^2) and the material parameters.
    
    # So we'll define a function that takes (I_exc, sigma_s, tau_T, k_TT) and returns the UC QY.
    # Then the additional current = UC_QY * (photon_flux at the excitation wavelength) * q * f_coupling.
    
    # For the interactive, we'll allow user to set material parameters and see the gain.
    # We'll also allow scanning over I_exc to see the optimal intensity.
    
    # We'll return the Jsc with and without UC, and the enhancement factor.
    return Jsc_noUC, 0.0  # placeholder; we'll compute inside the interactive function

# -------------------------------------------------------------------
# 4. Main interactive function
# -------------------------------------------------------------------
def run_uc_simulator(sigma_s=1e-3, tau_T=1e-3, k_TT=1e-20, phi_ISC=0.9, phi_ET=0.8, phi_em=0.9,
                     I_exc_range=(1e-3, 1e3), Npoints=100, bandgap_eV=1.1, show_solar_spectrum=True):
    """
    Interactive simulation: compute UC QY as function of excitation intensity,
    and compute the equivalent solar cell efficiency gain.
    """
    # Create intensity array
    I_exc = np.logspace(np.log10(I_exc_range[0]), np.log10(I_exc_range[1]), Npoints)
    UC_QY = np.zeros_like(I_exc)
    T_pop = np.zeros_like(I_exc)
    for i, I in enumerate(I_exc):
        qy, tp = tta_puc_quantum_yield(I, sigma_s, tau_T, k_TT, phi_ISC, phi_ET, phi_em)
        UC_QY[i] = qy
        T_pop[i] = tp
    
    # Solar cell model: we'll compute the additional current from upconversion of 533 nm photons.
    # Assume we use a narrow band at 533 nm with intensity I_exc (which is the actual power density).
    # The photon flux at 533 nm (photons/s/m^2) for the given intensity:
    photon_flux_input = I_exc / (h*c/(533e-9))  # photons/s/m^2
    # Upconverted photon flux at 413 nm:
    photon_flux_uc = UC_QY * photon_flux_input  # assuming each input photon that is upconverted yields one output photon (simplified)
    # Current contributed (A/m^2):
    J_uc = q * photon_flux_uc  # A/m^2
    
    # Also compute equivalent solar cell efficiency gain: assume 1 sun = 1000 W/m^2
    P_sun = 1000  # W/m^2
    # Without UC, only above-bandgap photons contribute. We'll compute Jsc_noUC using solar spectrum.
    # For simplicity, we'll approximate Jsc_noUC = 30 mA/cm^2 for Si cell (typical) = 300 A/m^2
    Jsc_noUC = 300  # A/m^2
    # The upconversion adds J_uc to the current.
    J_total = Jsc_noUC + J_uc
    # Power output = J_total * V_oc, assume V_oc ~ 0.7 V for Si
    V_oc = 0.7
    P_out = J_total * V_oc  # W/m^2
    P_out_noUC = Jsc_noUC * V_oc
    efficiency_noUC = P_out_noUC / P_sun * 100  # %
    efficiency_UC = P_out / P_sun * 100  # %
    efficiency_gain = (efficiency_UC - efficiency_noUC) / efficiency_noUC * 100  # percent increase
    
    # Also compute the optimal intensity for maximum UC QY (saturation)
    # Find the intensity where UC_QY is maximized (or where it saturates)
    max_qy_idx = np.argmax(UC_QY)
    I_opt = I_exc[max_qy_idx]
    qy_max = UC_QY[max_qy_idx]
    
    # ---- PLOT ----
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 3, height_ratios=[1, 1])
    
    # Panel 1: UC Quantum Yield vs Excitation Intensity
    ax = fig.add_subplot(gs[0, 0])
    ax.plot(I_exc, UC_QY*100, 'b-', lw=2)
    ax.set_xscale('log')
    ax.set_xlabel('Excitation intensity (W/m²)')
    ax.set_ylabel('UC Quantum Yield (%)')
    ax.set_title('TTA-PUC Efficiency')
    ax.grid(True, alpha=0.3)
    ax.axvline(I_opt, color='r', linestyle='--', label=f'Optimal I = {I_opt:.2f} W/m²')
    ax.legend()
    
    # Panel 2: Triplet population
    ax = fig.add_subplot(gs[0, 1])
    ax.plot(I_exc, T_pop, 'r-', lw=2)
    ax.set_xscale('log')
    ax.set_xlabel('Excitation intensity (W/m²)')
    ax.set_ylabel('Triplet population (arb. units)')
    ax.set_title('Triplet density')
    ax.grid(True, alpha=0.3)
    
    # Panel 3: Solar cell current gain
    ax = fig.add_subplot(gs[0, 2])
    ax.plot(I_exc, J_uc, 'g-', lw=2)
    ax.set_xscale('log')
    ax.set_xlabel('Excitation intensity (W/m²)')
    ax.set_ylabel('Added current (A/m²)')
    ax.set_title('Upconversion photocurrent')
    ax.grid(True, alpha=0.3)
    
    # Panel 4: Efficiency vs intensity
    ax = fig.add_subplot(gs[1, 0])
    ax.plot(I_exc, efficiency_UC, 'purple', lw=2, label='With UC')
    ax.axhline(efficiency_noUC, color='gray', linestyle='--', label='Without UC')
    ax.set_xscale('log')
    ax.set_xlabel('Excitation intensity (W/m²)')
    ax.set_ylabel('Solar cell efficiency (%)')
    ax.set_title('Efficiency enhancement')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Panel 5: Efficiency gain % vs intensity
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(I_exc, efficiency_gain, 'orange', lw=2)
    ax.set_xscale('log')
    ax.set_xlabel('Excitation intensity (W/m²)')
    ax.set_ylabel('Relative efficiency gain (%)')
    ax.set_title('Percentage improvement')
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='k', linestyle='-', alpha=0.5)
    
    # Panel 6: Parameter summary and optimal values
    ax = fig.add_subplot(gs[1, 2])
    ax.axis('off')
    summary = f"""
    📊 UPCONVERSION SIMULATION SUMMARY
    ──────────────────────────────────
    Material parameters:
    σ_s (abs. coeff): {sigma_s:.3f} m⁻¹
    τ_T (triplet lifetime): {tau_T*1e3:.2f} ms
    k_TT (TTA rate): {k_TT:.2e} m³/s
    φ_ISC: {phi_ISC:.2f}
    φ_ET: {phi_ET:.2f}
    φ_em: {phi_em:.2f}
    
    Optimal excitation: {I_opt:.2f} W/m²
    Max UC QY: {qy_max*100:.1f}%
    Max efficiency gain: {np.max(efficiency_gain):.1f}%
    Corresponding efficiency: {efficiency_UC[max_qy_idx]:.2f}%
    """
    ax.text(0.05, 0.95, summary, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
    
    plt.tight_layout()
    plt.show()
    
    # Print additional info
    print(f"Optimal excitation intensity: {I_opt:.2f} W/m²")
    print(f"Max UC quantum yield: {qy_max*100:.1f}%")
    print(f"Max efficiency gain: {np.max(efficiency_gain):.1f}% at {I_exc[np.argmax(efficiency_gain)]:.2f} W/m²")

# -------------------------------------------------------------------
# 5. Interactive controls (search space)
# -------------------------------------------------------------------
style = {'description_width': 'initial'}
controls = {
    'sigma_s': FloatSlider(value=1e-3, min=1e-5, max=1e-1, step=1e-4, description='σ_s (abs. coeff, m⁻¹)', style=style, continuous_update=False),
    'tau_T': FloatSlider(value=1e-3, min=1e-5, max=1e-2, step=1e-4, description='τ_T (s)', style=style, continuous_update=False),
    'k_TT': FloatSlider(value=1e-20, min=1e-22, max=1e-18, step=1e-21, description='k_TT (m³/s)', style=style, continuous_update=False),
    'phi_ISC': FloatSlider(value=0.9, min=0.1, max=1.0, step=0.05, description='φ_ISC', style=style, continuous_update=False),
    'phi_ET': FloatSlider(value=0.8, min=0.1, max=1.0, step=0.05, description='φ_ET', style=style, continuous_update=False),
    'phi_em': FloatSlider(value=0.9, min=0.1, max=1.0, step=0.05, description='φ_em', style=style, continuous_update=False),
    'I_exc_range': (0.001, 1000),  # not a slider, we'll let user adjust via log scale? We'll use fixed range.
    'Npoints': IntSlider(value=100, min=20, max=200, step=10, description='Points', style=style, continuous_update=False),
    'bandgap_eV': FloatSlider(value=1.1, min=0.5, max=2.0, step=0.05, description='Bandgap (eV)', style=style, continuous_update=False)
}

out = Output()
def update(sigma_s, tau_T, k_TT, phi_ISC, phi_ET, phi_em, Npoints, bandgap_eV):
    with out:
        clear_output(wait=True)
        run_uc_simulator(sigma_s, tau_T, k_TT, phi_ISC, phi_ET, phi_em,
                         I_exc_range=(0.001, 1000), Npoints=Npoints, bandgap_eV=bandgap_eV)

interactive_widget = interactive(update, **{k: v for k, v in controls.items() if k not in ['I_exc_range']})
display(HBox([VBox([controls[k] for k in controls if k not in ['I_exc_range']]), out]))

# -------------------------------------------------------------------
# 6. Default run
# -------------------------------------------------------------------
print("🚀 PHOTON UPCONVERSION EXPLORER")
print("   Adjust material parameters to find optimal upconversion conditions.")
print("   The simulation shows UC quantum yield, triplet population, and solar cell efficiency gain.\n")
run_uc_simulator(sigma_s=1e-3, tau_T=1e-3, k_TT=1e-20, phi_ISC=0.9, phi_ET=0.8, phi_em=0.9,
                 I_exc_range=(0.001, 1000), Npoints=100, bandgap_eV=1.1)
