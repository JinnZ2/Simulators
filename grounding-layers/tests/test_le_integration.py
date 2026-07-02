#!/usr/bin/env python3
import numpy as np
from l_epsilon_epistemic import EpistemicInstrument

def test_le_integration():
    print("=" * 60)
    print("Lε INTEGRATION CHECK")
    print("=" * 60)

    # Create instrument with bias audit
    instr = EpistemicInstrument(bias_audit=True)
    
    # Generate a true signal and time
    time = np.arange(0, 2.0, 0.02)
    true = 20 + 5 * np.sin(2 * np.pi * 0.5 * time)
    
    # Observe with a human‑centric claim
    claim = "Human intelligence is the only true intelligence."
    measured, meta = instr.observe(true, time, claim_context=claim)
    
    # Check measurement gap
    assert "gap_estimate" in meta, "Missing gap_estimate"
    assert "sigma" in meta["gap_estimate"], "Missing sigma"
    assert "confidence_interval" in meta["gap_estimate"], "Missing confidence_interval"
    
    # Check bias audit
    assert "bias_report" in meta, "Missing bias_report"
    bias_flags = meta["bias_report"].get("bias_flags", [])
    assert "GL_B_015" in bias_flags, "Human‑centrism not flagged"
    
    print("✅ Measurement gap present")
    print(f"   Sigma: {meta['gap_estimate']['sigma']:.3f} °C")
    print(f"   Confidence interval: ±{meta['gap_estimate']['sigma'] * meta['gap_estimate']['confidence']:.3f} °C")
    print("✅ Bias audit flagged human‑centrism")
    print(f"   Flags: {bias_flags}")
    print("=" * 60)

if __name__ == "__main__":
    test_le_integration()
