#!/usr/bin/env python3
# test_epsilon_with_bias.py

from l_epsilon_epistemic import EpistemicInstrument
import numpy as np

def test_epsilon_bias_aware():
    instr = EpistemicInstrument(bias_audit=True)
    time = np.arange(0, 10, 0.02)
    true = 20 + 5 * np.sin(time)
    
    claim = "Human intelligence is the only true intelligence."
    measured, meta = instr.observe(true, time, claim_context=claim)
    
    # Should contain a bias_report
    assert "bias_report" in meta, "Bias report missing when bias_audit=True"
    bias_flags = meta["bias_report"].get("bias_flags", [])
    assert "GL_B_015" in bias_flags, "Human‑centrism not flagged in instrument audit"
    print("✅ Lε bias integration passes.")

if __name__ == "__main__":
    test_epsilon_bias_aware()
