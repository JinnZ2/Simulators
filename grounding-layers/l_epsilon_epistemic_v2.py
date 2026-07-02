#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# Lε: Epistemic Instrumentation Layer
#
# Models the sensor that mediates between L0-L4 and L5.
# It adds: resolution, noise, drift, sampling rate, latency, and clipping.
#
# CONSTRAINTS (frozen for audit):
#   resolution    = 1.0   °C (quantization step)
#   noise_std     = 2.5   °C
#   drift_rate    = 0.02  °C per second
#   sample_interval = 0.2 s (5 Hz)
#   latency       = 0.3   s
#   clipping      = True  (sensor has finite range)
#   min_val       = -10   °C
#   max_val       = 120   °C
#
# These constants are frozen. If a test fails, DO NOT retune them.
# Update the claims in CLAIMS.md instead.
# =============================================================================

import numpy as np

class EpistemicInstrument:
    """
    A sensor that takes a true continuous signal and returns a measurement
    with added epistemic artifacts.
    """
    def __init__(self,
                 resolution=1.0,
                 noise_std=2.5,
                 drift_rate=0.02,
                 sample_interval=0.2,
                 latency=0.3,
                 clipping=True,
                 min_val=-10,
                 max_val=120):
        
        # === FROZEN CONSTRAINTS (audit-grade) ===
        self.resolution = resolution
        self.noise_std = noise_std
        self.drift_rate = drift_rate
        self.sample_interval = sample_interval
        self.latency = latency
        self.clipping = clipping
        self.min_val = min_val
        self.max_val = max_val
        
        # Stateful drift offset (starts at zero, accumulates)
        self.calibration_offset = 0.0

    def observe(self, true_signal, time):
        """
        true_signal: 1D numpy array of true values.
        time: 1D numpy array of timestamps.
        
        Returns:
          measured: 1D numpy array of measurements.
          metadata: dict of intermediate artifacts (for debugging).
        """
        # 1. Clipping
        if self.clipping:
            clipped = np.clip(true_signal, self.min_val, self.max_val)
        else:
            clipped = true_signal
        
        # 2. Drift (accumulates)
        self.calibration_offset += self.drift_rate * 0.1  # per step
        drifted = clipped + self.calibration_offset
        
        # 3. Noise (Gaussian)
        noisy = drifted + np.random.normal(0, self.noise_std, size=len(drifted))
        
        # 4. Quantization
        quantized = np.round(noisy / self.resolution) * self.resolution
        
        # 5. Sampling (sample-and-hold effect)
        dt = time[1] - time[0] if len(time) > 1 else 0.01
        sample_steps = int(self.sample_interval / dt)
        if sample_steps < 1:
            sample_steps = 1
        sampled = np.zeros_like(quantized)
        last_val = quantized[0]
        for i in range(len(time)):
            if i % sample_steps == 0:
                last_val = quantized[i]
            sampled[i] = last_val
        
        # 6. Latency (phase delay via linear interpolation)
        latency_steps = int(self.latency / dt)
        if latency_steps > 0:
            delayed = np.concatenate([sampled[0:latency_steps], sampled[:-latency_steps]])
        else:
            delayed = sampled
        
        metadata = {
            "clipped": clipped,
            "drifted": drifted,
            "noisy": noisy,
            "quantized": quantized,
            "sampled": sampled,
            "delayed": delayed,
            "calibration_offset": self.calibration_offset,
        }
        return delayed, metadata

# -----------------------------------------------------------------------------
# Demo (pinned output)
# -----------------------------------------------------------------------------
def demo():
    """Run a demo and print pinned numbers for audit."""
    np.random.seed(42)  # for reproducibility
    
    dt = 0.02
    time = np.arange(0, 10, dt)
    # A simple true signal: sine wave + linear trend
    true_signal = 20 + 10 * np.sin(2 * np.pi * 0.5 * time) + 0.5 * time
    
    instr = EpistemicInstrument()
    measured, meta = instr.observe(true_signal, time)
    
    # Pinned outputs (to be checked in tests)
    print("=" * 50)
    print("Lε DEMO PINNED OUTPUT")
    print("=" * 50)
    print(f"Final calibration offset: {meta['calibration_offset']:.3f} °C")
    print(f"Mean measurement error:   {np.mean(measured - true_signal):.3f} °C")
    print(f"Max measurement error:    {np.max(np.abs(measured - true_signal)):.3f} °C")
    print(f"Standard deviation of error: {np.std(measured - true_signal):.3f} °C")
    print("=" * 50)
    return measured, meta

if __name__ == "__main__":
    demo()


patch:
# Add at the top
from cultural_lens import CulturalLens

# Add to __init__
def __init__(self, ..., bias_audit: bool = False):
    # ... existing init ...
    self.bias_audit = bias_audit
    if bias_audit:
        self.bias_lens = CulturalLens()
    else:
        self.bias_lens = None

# Add to observe signature
def observe(self, true_signal, time, claim_context: str = None):
    # ... existing measurement ...
    if self.bias_audit and claim_context:
        bias_report = self.bias_lens.annotate(claim_context, {})
        # Add to metadata
        metadata["bias_report"] = bias_report
    return measured, metadata



