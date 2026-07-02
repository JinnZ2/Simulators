"""
Exoplanet data archaeology — false positives + follow-up budget + ML.

Mines a synthetic transit-survey archive for candidate planets, models
the false-positive tax (eclipsing binaries, blended systems), applies a
follow-up budget constraint, and trains a lightweight classifier to
rank which candidates deserve the next telescope slot.

CC0 / for play. Extracted verbatim from legacy/Organize2.md lines 1-455.
Non-stdlib: numpy, matplotlib, ipywidgets, IPython.display.
"""

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

