#!/usr/bin/env python3
# The file shipped with NO import statements at all -- it uses
# `EpistemicInstrument` and `np` with nothing bringing them into
# scope, so all three tests raised NameError. Extraction artifact
# from a context where both were already bound. The names are the
# ones the module actually exports; nothing else is changed.
import numpy as np
from l_epsilon_epistemic_v2 import EpistemicInstrument

def test_gap_estimate():
    instr = EpistemicInstrument()
    time = np.arange(0, 1, 0.02)
    true = np.ones_like(time) * 20
    measured, meta = instr.observe(true, time)
    assert 'sigma' in meta['gap_estimate'], "Gap estimate missing"
    assert meta['gap_estimate']['confidence'] == 0.95, "Confidence default mismatch"

def test_instrument_scoped():
    instr = EpistemicInstrument()
    assert instr.instrument_scoped(50.0) == True, "50°C should be in range"
    assert instr.instrument_scoped(150.0) == False, "150°C should be out of range"

def test_bias_integration():
    instr = EpistemicInstrument(bias_audit=True)
    time = np.arange(0, 1, 0.02)
    true = np.ones_like(time) * 20
    measured, meta = instr.observe(true, time, claim_context="Human intelligence is supreme.")
    assert 'bias_report' in meta, "Bias audit not triggered"
    assert 'GL_B_015' in meta['bias_report'].get('bias_flags', []), "Human-centrism not flagged"
