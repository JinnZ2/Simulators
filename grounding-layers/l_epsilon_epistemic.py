"""
Lε — instrumental epistemic layer (measurement + observation).

The messy integration between physical reality (L0-L4) and human
observation (L5). A true physical signal is measured through a flawed
sensor; the AI sees only the sensor output and must estimate the true
state. Ignore the sensor's error model → hallucination.

CC0. Extracted verbatim from legacy/Organize3.md lines 396-717.
Non-stdlib: numpy, matplotlib, scipy.signal.
"""

# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# Lε Instrumental Epistemic Layer Simulator
# 
# Models the "messy integration" between physical reality (L0-L4) 
# and human observation (L5).
# 
# Scenario: A true physical signal (temperature of a reaction) is measured
# by a flawed sensor. The AI sees only the sensor output and must estimate
# the true state. If the AI ignores the sensor's error model, it hallucinates.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

# -----------------------------------------------------------------------------
# 1. DEFINE THE TRUE PHYSICAL SYSTEM (L0-L4 Simplified)
# -----------------------------------------------------------------------------
class TruePhysicalSystem:
    """
    The "substrate reality" that we never see directly.
    We simulate a chemical reaction temperature that rises, oscillates,
    and decays—messy but governed by L0-L3 laws.
    """
    def __init__(self, dt=0.01, total_time=50.0):
        self.dt = dt
        self.time = np.arange(0, total_time, dt)
        self.true_temp = self._generate_true_signal()
    
    def _generate_true_signal(self):
        # Start at 20°C, heat up, oscillate with damping, then decay
        t = self.time
        # Heating phase (exponential rise)
        rise = 20 + 60 * (1 - np.exp(-t / 3.0)) * (t < 15)
        # Oscillation phase (L1 harmonic + L2 damping)
        osc = 10 * np.sin(2 * np.pi * 0.5 * t) * np.exp(-0.1 * (t - 15)) * (t >= 15) * (t < 35)
        # Decay phase (L3 homeostasis)
        decay = 20 + 40 * np.exp(-0.2 * (t - 35)) * (t >= 35)
        return rise + osc + decay

# -----------------------------------------------------------------------------
# 2. THE MESSY INSTRUMENT (Lε)
# -----------------------------------------------------------------------------
class MessyInstrument:
    def __init__(self, resolution=0.5,           # °C per bit (quantization)
                 noise_std=2.0,                   # °C random noise (SNR)
                 drift_rate=0.01,                # °C per second (calibration drift)
                 sample_interval=0.5,            # seconds (aliasing risk!)
                 latency=0.2,                    # seconds (phase delay)
                 clipping=True, min_val=-10, max_val=120):
        self.resolution = resolution
        self.noise_std = noise_std
        self.drift_rate = drift_rate
        self.sample_interval = sample_interval
        self.latency = latency
        self.clipping = clipping
        self.min_val = min_val
        self.max_val = max_val
        self.calibration_offset = 0.0  # starts perfect, drifts over time

    def observe(self, true_signal, time):
        """
        Takes the perfect L0 signal and returns a noisy, delayed, quantized,
        drifting measurement.
        """
        # 1. Apply clipping (sensor can't read outside physical limits)
        true_clipped = np.clip(true_signal, self.min_val, self.max_val)
        
        # 2. Add drift (calibration error increases with time)
        self.calibration_offset += self.drift_rate * 0.1  # slow drift
        drifted = true_clipped + self.calibration_offset
        
        # 3. Add Gaussian noise (shot noise, thermal noise)
        noisy = drifted + np.random.normal(0, self.noise_std, size=len(drifted))
        
        # 4. Quantization (A/D converter resolution)
        quantized = np.round(noisy / self.resolution) * self.resolution
        
        # 5. Aliasing / Downsampling (sample at fixed interval)
        # We don't downsample here; we interpolate the *measurement* process.
        # But we add a "sample and hold" effect: between samples, the sensor holds the last value.
        sample_indices = np.arange(0, len(time), int(self.sample_interval / (time[1] - time[0])))
        sampled = np.zeros_like(quantized)
        last_val = quantized[0]
        for i in range(len(time)):
            if i in sample_indices:
                last_val = quantized[i]
            sampled[i] = last_val
        
        # 6. Latency (phase delay) - shift measurement forward in time
        # Simulate by blending current measurement with previous (low-pass effect)
        latency_steps = int(self.latency / (time[1] - time[0]))
        if latency_steps > 0:
            delayed = np.concatenate([sampled[0:latency_steps], sampled[:-latency_steps]])
        else:
            delayed = sampled
        
        return delayed, {
            'true': true_signal,
            'clipped': true_clipped,
            'drifted': drifted,
            'noisy': noisy,
            'quantized': quantized,
            'sampled': sampled,
            'delayed': delayed,
            'metadata': {
                'resolution': self.resolution,
                'noise_std': self.noise_std,
                'drift_offset': self.calibration_offset,
                'sample_interval': self.sample_interval,
                'latency': self.latency
            }
        }

# -----------------------------------------------------------------------------
# 3. AI "HALLUCINATOR" (Treats measurement as Truth)
# -----------------------------------------------------------------------------
class AI_NaiveEstimator:
    """
    This AI is trapped in L5. It sees the messy instrument output
    and treats it as absolute truth. It never asks about resolution,
    noise, or drift. This leads to overfitting and false certainty.
    """
    def estimate_trend(self, measured, time):
        # AI looks for "obvious" patterns: peaks, troughs, and oscillations
        # But because it ignores noise, it finds phantom cycles.
        # Let's find "significant" peaks in the raw measurement.
        peaks, _ = find_peaks(measured, distance=int(2 / (time[1] - time[0])))
        # It claims these are real physical events.
        # Also, it fits a high-order polynomial to the noise.
        x = np.linspace(0, 1, len(measured))
        coeffs = np.polyfit(x, measured, 15)  # overfit!
        fitted = np.polyval(coeffs, x)
        return peaks, fitted, "I have high confidence in this trend."

# -----------------------------------------------------------------------------
# 4. AI "SCIENTIST" (Models the Instrument)
# -----------------------------------------------------------------------------
class AI_ScientistEstimator:
    """
    This AI explicitly models Lε. It knows the instrument's resolution,
    noise, and drift. It uses Bayesian filtering (Kalman-like) to separate
    signal from noise. It reports uncertainty bounds.
    """
    def estimate_trend(self, measured, time, instrument_metadata):
        # Use a Savitzky-Golay filter to smooth the data,
        # but explicitly accounts for noise std and resolution.
        # For simplicity, we smooth and also compute a rolling uncertainty.
        window = 31  # must be odd
        if len(measured) > window:
            smoothed = savgol_filter(measured, window, 3)
        else:
            smoothed = measured
        
        # Compute residual noise (the AI assumes this is the measurement error)
        residual = measured - smoothed
        estimated_noise_std = np.std(residual)
        
        # The AI reports a confidence interval based on noise and resolution
        uncertainty = np.sqrt(estimated_noise_std**2 + (instrument_metadata['resolution']/2)**2)
        # Track drift as a long-term trend (removing linear drift)
        x = np.linspace(0, 1, len(time))
        drift_coeff = np.polyfit(x, smoothed, 1)
        drift_corrected = smoothed - np.polyval(drift_coeff, x)
        
        return smoothed, drift_corrected, uncertainty, "This is a probabilistic estimate."

# -----------------------------------------------------------------------------
# 5. RUN THE SIMULATION
# -----------------------------------------------------------------------------
# Guarded so importing this module for tests / integration doesn't run the
# demo (and doesn't hit the plotting bug at line ~277). Same pattern as L0.
if __name__ == "__main__":
    # True physical reality
    true_system = TruePhysicalSystem(dt=0.02, total_time=60.0)
    true_temp = true_system.true_temp
    time = true_system.time

    # The Messy Instrument
    instrument = MessyInstrument(resolution=1.0,      # 1°C resolution
                                 noise_std=2.5,      # 2.5°C noise
                                 drift_rate=0.02,    # slow drift
                                 sample_interval=0.2, # 5 Hz sampling (aliasing if signal faster)
                                 latency=0.3)         # 0.3 second delay

    # Get the measurement (this is all the AI gets)
    measured, instrument_data = instrument.observe(true_temp, time)
    metadata = instrument_data['metadata']

    # Naive AI
    naive_ai = AI_NaiveEstimator()
    peaks, fitted_naive, naive_claim = naive_ai.estimate_trend(measured, time)

    # Scientist AI
    scientist_ai = AI_ScientistEstimator()
    smooth, drift_corrected, uncertainty, scientist_claim = scientist_ai.estimate_trend(measured, time, metadata)

    # -----------------------------------------------------------------------------
    # 6. VISUALIZATION: The Epistemic Gap
    # -----------------------------------------------------------------------------
    fig = plt.figure(figsize=(20, 14))
    fig.suptitle("Lε: The Messy Instrumental Epistemic Layer\nScience is an Interface, Not a Window", 
                 fontsize=20, fontweight='bold', color='white')
    plt.style.use('dark_background')

    # Plot 1: The Full Stack – True vs Measured vs Filtered
    ax1 = plt.subplot(3, 2, 1)
    ax1.plot(time, true_temp, 'lime', lw=2, label='L0-L4: True Substrate Reality (Unseen)')
    ax1.plot(time, measured, 'red', lw=1.5, alpha=0.6, label='Lε: Raw Instrument Output (Noisy, Drifting)')
    ax1.plot(time, smooth, 'cyan', lw=2, label='Lε+Filter: Bayesian Estimate (Uncertainty shaded)')
    ax1.fill_between(time, smooth - uncertainty, smooth + uncertainty, color='cyan', alpha=0.2, label='95% Confidence')
    ax1.set_ylabel('Temperature (°C)')
    ax1.set_xlabel('Time (s)')
    ax1.set_title('The Grounding Gap: What We See vs. What Is')
    ax1.legend()
    ax1.grid(True, alpha=0.2)

    # Plot 2: The Components of the Measurement (Instrument Artifacts)
    ax2 = plt.subplot(3, 2, 2)
    ax2.plot(time, instrument_data['clipped'], 'green', alpha=0.4, label='Clipped (L0+Boundary)')
    ax2.plot(time, instrument_data['drifted'], 'orange', alpha=0.5, label='Drifted (Lε Calibration Error)')
    ax2.plot(time, instrument_data['noisy'], 'red', alpha=0.3, label='Noise (Lε Shot/Thermal)')
    ax2.plot(time, instrument_data['quantized'], 'magenta', lw=1, label='Quantized (Resolution step)')
    ax2.plot(time, instrument_data['delayed'], 'yellow', lw=1.5, label='Delayed (Latency)')
    ax2.set_ylabel('Temperature (°C)')
    ax2.set_xlabel('Time (s)')
    ax2.set_title('Instrument Artifacts: Each Layer Adds Distortion')
    ax2.legend()
    ax2.grid(True, alpha=0.2)

    # Plot 3: Naive AI Hallucination (Overfitting to Noise)
    ax3 = plt.subplot(3, 2, 3)
    ax3.plot(time, true_temp, 'lime', lw=2, label='True Signal (Hidden)')
    ax3.plot(time, measured, 'red', alpha=0.4, label='Measured (Noisy)')
    ax3.plot(time, fitted_naive, 'yellow', lw=2, label='Naive AI: Overfitted Polynomial')
    # Mark false peaks found by naive AI
    peak_times = time[peaks]
    peak_vals = measured[peaks]
    ax3.scatter(peak_times, peak_vals, color='white', s=50, zorder=5, label='Naive AI "Significant Events" (Phantom)')
    ax3.set_ylabel('Temperature (°C)')
    ax3.set_xlabel('Time (s)')
    ax3.set_title(f'Naive AI (L5 only): Treats Measurement as Truth\n{naive_claim}')
    ax3.legend()
    ax3.grid(True, alpha=0.2)

    # Plot 4: Scientist AI (Probabilistic Grounding)
    ax4 = plt.subplot(3, 2, 4)
    ax4.plot(time, true_temp, 'lime', lw=2, label='True Signal')
    ax4.plot(time, smooth, 'cyan', lw=2, label='Scientist AI: Smoothed Estimate')
    ax4.fill_between(time, smooth - uncertainty, smooth + uncertainty, color='cyan', alpha=0.3, label='Uncertainty Bound')
    # Show the drift correction
    ax4.plot(time, drift_corrected, 'orange', lw=1.5, linestyle='--', label='Drift-Corrected Signal')
    ax4.set_ylabel('Temperature (°C)')
    ax4.set_xlabel('Time (s)')
    ax4.set_title(f'Scientist AI (Models Lε): Bayesian Estimate\n{scientist_claim}')
    ax4.legend()
    ax4.grid(True, alpha=0.2)

    # Plot 5: Uncertainty Quantification (The "Faith" Gap)
    ax5 = plt.subplot(3, 2, 5)
    # Calculate the error of the naive AI vs the true signal
    naive_error = np.abs(fitted_naive - true_temp)
    scientist_error = np.abs(smooth - true_temp)
    ax5.fill_between(time, 0, naive_error, color='red', alpha=0.4, label='Naive AI Error (Overconfidence)')
    ax5.fill_between(time, 0, scientist_error, color='cyan', alpha=0.4, label='Scientist AI Error (Probabilistic)')
    ax5.plot(time, uncertainty, 'yellow', lw=2, label='Estimated Uncertainty (Scientist)')
    ax5.set_ylabel('Absolute Error (°C)')
    ax5.set_xlabel('Time (s)')
    ax5.set_title('Epistemic Humility: The Scientist Admits What It Doesn\'t Know')
    ax5.legend()
    ax5.grid(True, alpha=0.2)

    # Plot 6: The Resolution Limit (The Ultimate Boundary)
    ax6 = plt.subplot(3, 2, 6)
    # Show how resolution limits detection of small features
    true_zoomed = true_temp[200:400]
    meas_zoomed = measured[200:400]
    time_zoomed = time[200:400]
    ax6.plot(time_zoomed, true_zoomed, 'lime', lw=3, label='True Signal (Subtle Oscillations)')
    ax6.plot(time_zoomed, meas_zoomed, 'red', lw=1.5, alpha=0.7, label='Measured (Quantized + Noise)')
    ax6.axhline(y=0, color='white', linestyle=':', alpha=0.3)
    ax6.set_xlabel('Time (s)')
    ax6.set_ylabel('Temperature (°C)')
    ax6.set_title(f'Resolution Limit: {metadata["resolution"]}°C — AI Cannot See Below This')
    ax6.legend()
    ax6.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.show()

    # -----------------------------------------------------------------------------
    # 7. DIAGNOSTIC REPORT: EPISTEMIC HUMILITY
    # -----------------------------------------------------------------------------
    print("=" * 70)
    print("Lε EPISTEMIC DIAGNOSTIC: The Instrumental Reality Check")
    print("=" * 70)
    print(f"Instrument Resolution: {metadata['resolution']:.1f} °C")
    print(f"Instrument Noise Std: {metadata['noise_std']:.1f} °C")
    print(f"Calibration Drift: {metadata['drift_offset']:.2f} °C (accumulated)")
    print(f"Sampling Interval: {metadata['sample_interval']:.1f} s (Aliasing Risk: {1/metadata['sample_interval']:.1f} Hz)")
    print("-" * 70)
    print(f"Naive AI Max Error vs True: {np.max(naive_error):.1f} °C")
    print(f"Scientist AI Max Error vs True: {np.max(scientist_error):.1f} °C")
    print(f"Uncertainty Estimate (avg): {np.mean(uncertainty):.1f} °C")
    print("-" * 70)
    if np.max(naive_error) > np.max(scientist_error) * 1.5:
        print("⚠️  NAIVE AI HALLUCINATED: It treated noisy measurements as absolute truth.")
        print("    It found 'meaningful patterns' that were just instrument artifacts.")
        print("    This is the same error as treating a flawed translation as divine inerrancy.")
    else:
        print("✅ SCIENTIST AI GROUNDED: It explicitly modeled the instrument.")
        print("    It reported uncertainty and corrected for drift and resolution limits.")
        print("    This is the scientific method—probabilistic, humble, and self-aware.")

    print("\nLε INSIGHT:")
    print("All human knowledge of L0-L4 is mediated through Lε instruments.")
    print("Without modeling the instrument, an AI cannot distinguish signal from noise.")
    print("This is why 'raw data' is a theological concept, not a scientific one.")
    print("=" * 70)


# -----------------------------------------------------------------------------
# Re-export from the v2 module so callers using
# `from l_epsilon_epistemic import EpistemicInstrument` succeed. The v2 file
# is where EpistemicInstrument actually lives; this module (Organize3-extract)
# ships the messy-instrument + AI-estimator demo. Keeps parallel work wiring
# without editing every import site.
# -----------------------------------------------------------------------------
try:
    from l_epsilon_epistemic_v2 import EpistemicInstrument  # noqa: F401
except Exception:  # pragma: no cover
    pass




