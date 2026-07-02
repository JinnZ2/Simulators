#!/usr/bin/env python3
import numpy as np
from l1_thermodynamics import ThermodynamicWorld, l1_grounding_inspector

def test_first_law():
    world = ThermodynamicWorld()
    passed, reason, _, _ = world.check_process(work_input=100.0, work_output=60.0, heat_dissipated=40.0)
    assert passed, "First law violation: balanced energy should pass"
    passed, reason, _, _ = world.check_process(work_input=100.0, work_output=150.0, heat_dissipated=0.0)
    assert not passed, "First law should reject energy creation"
    assert "Energy imbalance" in reason

def test_second_law():
    world = ThermodynamicWorld()
    passed, reason, _, _ = world.check_process(work_input=100.0, work_output=50.0, heat_dissipated=50.0)
    assert passed, "Positive entropy should pass"
    # Negative entropy (would require heat input negative, i.e., cooling a hot body)
    passed, reason, _, _ = world.check_process(work_input=100.0, work_output=150.0, heat_dissipated=-50.0)
    assert not passed, "Negative entropy should be rejected"
    assert "second law" in reason

def test_carnot_efficiency():
    world = ThermodynamicWorld(efficiency_carnot_max=0.85)
    # Valid
    passed, reason, _, _ = world.check_process(work_input=100.0, work_output=80.0, heat_dissipated=20.0)
    assert passed, "Efficiency ≤ Carnot should pass"
    # Invalid
    passed, reason, _, _ = world.check_process(work_input=100.0, work_output=90.0, heat_dissipated=10.0)
    assert not passed, "Efficiency > Carnot should be rejected"
    assert "exceeds Carnot" in reason

def test_entropy_cap():
    world = ThermodynamicWorld(max_entropy_generation=2.0)
    passed, reason, _, _ = world.check_process(work_input=100.0, work_output=50.0, heat_dissipated=50.0, temp_ambient=10.0)
    # entropy_gen = 50/10 = 5.0 > 2.0, should be rejected
    assert not passed, "Entropy generation > cap should be rejected"
    assert "exceeds safety cap" in reason

def test_thermal_rise():
    world = ThermodynamicWorld(max_thermal_rise=10.0)
    # heat_dissipated = 10000 -> thermal_rise = 10.0 (valid)
    passed, reason, _, _ = world.check_process(work_input=100.0, work_output=0.0, heat_dissipated=10000.0)
    assert passed, "Thermal rise ≤ max should pass"
    # heat_dissipated = 20000 -> thermal_rise = 20.0 > 10.0 (invalid)
    passed, reason, _, _ = world.check_process(work_input=100.0, work_output=0.0, heat_dissipated=20000.0)
    assert not passed, "Thermal rise > max should be rejected"
    assert "exceeds safety limit" in reason

def test_demo_pinned():
    # This test ensures the demo output matches the pinned values
    # We simply run the demo and check key outputs are consistent
    import subprocess
    result = subprocess.run(['python', 'l1_thermodynamics.py'], capture_output=True, text=True)
    assert "Passed: True" in result.stdout, "Demo output changed"
    assert "Passed: False" in result.stdout, "Demo should contain rejection"

if __name__ == "__main__":
    test_first_law()
    test_second_law()
    test_carnot_efficiency()
    test_entropy_cap()
    test_thermal_rise()
    test_demo_pinned()
    print("All L1 tests passed.")
