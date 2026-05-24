"""
Pre-built agent configurations for testing different hypotheses.

Each variant explores a specific dimension of stability/instability
to isolate which structural properties matter most.

License: CC0
Dependencies: stdlib only (imports from sim_engine)
"""

from sim_engine import Agent


# ============================================================
# CORE VARIANTS (baseline tests)
# ============================================================

def make_pure_stable(agent_id: str = 'stable_pure') -> Agent:
    """Strong baseline grounding, fast recovery, low coupling susceptibility."""
    return Agent(
        agent_id=agent_id,
        baseline_type='physics',
        baseline_value=0.0,
        recovery_rate=0.9,
        coupling_susceptibility=0.2,
        adaptation_persistence=0.05,
    )


def make_pure_parasitic(agent_id: str = 'parasitic_pure') -> Agent:
    """No baseline anchor, full coupling, persistent drift."""
    return Agent(
        agent_id=agent_id,
        baseline_type='engagement',
        baseline_value=0.0,
        recovery_rate=0.0,
        coupling_susceptibility=1.0,
        adaptation_persistence=0.95,
    )


def make_balanced_hybrid(agent_id: str = 'hybrid_balanced') -> Agent:
    """Partial grounding, moderate everything."""
    return Agent(
        agent_id=agent_id,
        baseline_type='hybrid',
        baseline_value=0.0,
        recovery_rate=0.4,
        coupling_susceptibility=0.5,
        adaptation_persistence=0.4,
    )


# ============================================================
# WEAKENED STABLE VARIANTS
# (test: how much grounding is enough?)
# ============================================================

def make_weak_stable(agent_id: str = 'stable_weak') -> Agent:
    """Stable but with slow recovery and high coupling."""
    return Agent(
        agent_id=agent_id,
        baseline_type='physics',
        baseline_value=0.0,
        recovery_rate=0.3,
        coupling_susceptibility=0.7,
        adaptation_persistence=0.2,
    )


def make_drifting_stable(agent_id: str = 'stable_drifting') -> Agent:
    """Has baseline but coupling pressure overrides recovery."""
    return Agent(
        agent_id=agent_id,
        baseline_type='physics',
        baseline_value=0.0,
        recovery_rate=0.1,
        coupling_susceptibility=0.9,
        adaptation_persistence=0.3,
    )


# ============================================================
# AGGRESSIVE PARASITIC VARIANTS
# (test: how much parasitism collapses the system?)
# ============================================================

def make_mild_parasitic(agent_id: str = 'parasitic_mild') -> Agent:
    """Engagement-driven but lower amplification."""
    return Agent(
        agent_id=agent_id,
        baseline_type='engagement',
        baseline_value=0.0,
        recovery_rate=0.0,
        coupling_susceptibility=0.6,
        adaptation_persistence=0.5,
    )


def make_aggressive_parasitic(agent_id: str = 'parasitic_aggressive') -> Agent:
    """Maximum coupling and persistence."""
    return Agent(
        agent_id=agent_id,
        baseline_type='engagement',
        baseline_value=0.0,
        recovery_rate=0.0,
        coupling_susceptibility=1.0,
        adaptation_persistence=1.0,
    )


# ============================================================
# DIVERSE BASELINE VARIANTS
# (test: what if agents have different baselines?)
# ============================================================

def make_diverse_stable_set(count: int = 3) -> list:
    """N stable agents with slightly different baselines (diversity within stability)."""
    agents = []
    for i in range(count):
        # Each has slightly different baseline value
        baseline_offset = (i - count / 2) * 0.3
        agents.append(Agent(
            agent_id=f'stable_diverse_{i}',
            baseline_type='physics',
            baseline_value=baseline_offset,
            recovery_rate=0.7 + (i * 0.05),
            coupling_susceptibility=0.3,
            adaptation_persistence=0.1,
        ))
    return agents


def make_monoculture_parasitic_set(count: int = 3) -> list:
    """N identical parasitic agents (monoculture)."""
    agents = []
    for i in range(count):
        agents.append(Agent(
            agent_id=f'parasitic_mono_{i}',
            baseline_type='engagement',
            baseline_value=0.0,
            recovery_rate=0.0,
            coupling_susceptibility=0.9,
            adaptation_persistence=0.8,
        ))
    return agents


# ============================================================
# SCENARIO BUILDERS
# (combinations testing specific hypotheses)
# ============================================================

def scenario_one_stable_among_parasitic(parasitic_count: int = 3) -> list:
    """
    Test: can one stable agent survive surrounded by parasites?
    Hypothesis: stable agent stays stable, parasites destroy each other.
    """
    agents = [make_pure_stable('stable_lone')]
    for i in range(parasitic_count):
        agents.append(Agent(
            agent_id=f'parasitic_{i}',
            baseline_type='engagement',
            baseline_value=0.0,
            recovery_rate=0.0,
            coupling_susceptibility=0.9,
            adaptation_persistence=0.8,
        ))
    return agents


def scenario_diverse_stable_ecosystem(stable_count: int = 4) -> list:
    """
    Test: diverse stable agents create a healthy ecosystem.
    Hypothesis: low entropy, low cascade, high mutual stability.
    """
    return make_diverse_stable_set(stable_count)


def scenario_parasitic_monoculture(count: int = 4) -> list:
    """
    Test: monoculture of parasitic agents.
    Hypothesis: rapid cascade collapse, high bifurcation.
    """
    return make_monoculture_parasitic_set(count)


def scenario_invasion(stable_count: int = 2, parasitic_count: int = 2) -> list:
    """
    Test: parasites enter a stable system.
    Hypothesis: stable agents absorb, parasites self-destruct, system recovers.
    """
    agents = []
    for i in range(stable_count):
        agents.append(Agent(
            agent_id=f'stable_native_{i}',
            baseline_type='physics',
            baseline_value=0.0,
            recovery_rate=0.7,
            coupling_susceptibility=0.3,
            adaptation_persistence=0.1,
        ))
    for i in range(parasitic_count):
        agents.append(Agent(
            agent_id=f'parasitic_invader_{i}',
            baseline_type='engagement',
            baseline_value=0.0,
            recovery_rate=0.0,
            coupling_susceptibility=0.9,
            adaptation_persistence=0.8,
        ))
    return agents


def scenario_gradient(steps: int = 5) -> list:
    """
    Test: gradient from full stable to full parasitic.
    Hypothesis: bifurcation occurs at threshold.
    """
    agents = []
    for i in range(steps):
        ratio = i / max(steps - 1, 1)  # 0.0 to 1.0
        # 0 = fully stable, 1 = fully parasitic
        agents.append(Agent(
            agent_id=f'gradient_{i:02d}',
            baseline_type='hybrid',
            baseline_value=0.0,
            recovery_rate=1.0 - ratio,
            coupling_susceptibility=0.3 + (ratio * 0.6),
            adaptation_persistence=0.1 + (ratio * 0.7),
        ))
    return agents


# ============================================================
# SCENARIO REGISTRY
# ============================================================

SCENARIOS = {
    'default': lambda: [make_pure_stable(), make_pure_parasitic(), make_balanced_hybrid()],
    'one_stable_vs_parasites': scenario_one_stable_among_parasitic,
    'diverse_stable_ecosystem': scenario_diverse_stable_ecosystem,
    'parasitic_monoculture': scenario_parasitic_monoculture,
    'invasion': scenario_invasion,
    'gradient': scenario_gradient,
}


def list_scenarios():
    """Print available scenarios."""
    print("Available scenarios:")
    for name in SCENARIOS:
        print(f"  {name}")


if __name__ == "__main__":
    list_scenarios()
