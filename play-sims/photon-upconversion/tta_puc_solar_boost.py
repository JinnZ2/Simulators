"""
Photon upconversion (TTA-PUC) + solar cell efficiency boost.

Models triplet-triplet annihilation upconversion kinetics: sensitiser
absorption, ISC to triplet, energy transfer to annihilator, T-T
annihilation, singlet emission. Reports UC quantum yield vs excitation
intensity and the fractional efficiency boost when an upconversion
layer sits under a bandgap-limited solar cell.

CC0 / for play. Extracted verbatim from legacy/Organize2.md lines 951-1262.
Non-stdlib: numpy, matplotlib, ipywidgets, IPython.display.
"""

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
