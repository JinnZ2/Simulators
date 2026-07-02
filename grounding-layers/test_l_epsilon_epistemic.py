#!/usr/bin/env python3
import numpy as np
from l_epsilon_epistemic import EpistemicInstrument

def test_clipping():
    instr = EpistemicInstrument()
    true = np.array([-20, 0, 130])
    time = np.array([0, 1, 2])
    measured, meta = instr.observe(true, time)
    # Clipped values should be -10, 0, 120
    np.testing.assert_allclose(meta['clipped'], np.array([-10, 0, 120]), rtol=1e-5)

def test_quantization():
    instr = EpistemicInstrument(resolution=2.0)
    # Feed a constant signal
    true = np.array([1.0, 1.0, 1.0])
    time = np.array([0, 1, 2])
    measured, meta = instr.observe(true, time)
    # With noise, quantized may vary; but each quantized value should be multiple of 2
    for val in meta['quantized']:
        assert np.isclose(val % 2.0, 0, atol=1e-5) or np.isclose(val % 2.0, 2.0, atol=1e-5), f"{val} not a multiple of 2"

def test_drift_bounded():
    instr = EpistemicInstrument(drift_rate=0.01)
    time = np.arange(0, 10, 0.02)
    true = np.ones_like(time) * 20
    measured, meta = instr.observe(true, time)
    # After 10 seconds, drift should be ≤ 10 * 0.01 * 0.1 + some tolerance
    max_drift = 10 * 0.01 * 0.1 + 0.001
    assert abs(meta['calibration_offset']) <= max_drift, f"Drift {meta['calibration_offset']} exceeds bound"

def test_latency():
    instr = EpistemicInstrument(latency=0.5)
    dt = 0.02
    time = np.arange(0, 10, dt)
    # Step signal
    true = np.zeros_like(time)
    true[100:] = 1.0  # step at t=2.0
    measured, meta = instr.observe(true, time)
    # The delayed signal should show the step at t ≈ 2.5 (latency 0.5)
    # Check that the first index where measured > 0.5 is near index 125
    idx_step = np.argmax(measured > 0.5)
    expected_idx = int((2.0 + 0.5) / dt)
    assert abs(idx_step - expected_idx) <= 5, f"Step at index {idx_step}, expected {expected_idx}"

if __name__ == "__main__":
    test_clipping()
    test_quantization()
    test_drift_bounded()
    test_latency()
    print("All Lε tests passed.")
