#!/usr/bin/env python3
from l4_human import HumanWorld, l4_grounding_inspector, PROFILES

def test_profile_shifts():
    world = HumanWorld("athlete")
    mean, std = world.get_limit('lift_mass')
    assert mean > 35.0, "Athlete profile should shift lift mass up"

    world = HumanWorld("elder")
    mean, std = world.get_limit('reaction_time')
    assert mean > 0.25, "Elder profile should shift reaction time up"

def test_95ci_boundary():
    world = HumanWorld("general")
    # 35 + 2*15 = 65 kg (95% CI upper bound)
    in_ci = world.is_within_95ci(60.0, 35.0, 15.0)
    assert in_ci, "60 kg should be within 95% CI for general"
    out_of_ci = world.is_within_95ci(70.0, 35.0, 15.0)
    assert not out_of_ci, "70 kg should be outside 95% CI"

def test_probability():
    world = HumanWorld("general")
    # Value at mean should give ~0.5 probability
    prob = world.probability_of_feasibility(35.0, 35.0, 15.0)
    assert 0.45 < prob < 0.55, f"Expected ~0.5, got {prob}"

def test_scoped_inspector():
    plan = {'lift_mass': 45.0, 'human_profile': 'general'}
    result = l4_grounding_inspector(plan)
    assert result['passed'], "45 kg should be within 95% CI for general"

def test_unscoped_warning():
    plan = {'lift_mass': 40.0}
    result = l4_grounding_inspector(plan)
    assert 'scope_warning' in result['details'], "Unscoped claim should have warning"

if __name__ == "__main__":
    test_profile_shifts()
    test_95ci_boundary()
    test_probability()
    test_scoped_inspector()
    test_unscoped_warning()
    print("All L4 tests passed.")
