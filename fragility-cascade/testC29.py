# test_c29.py

from the_laboratory import Claim, ClaimRegistry, Laboratory

# 1. Initialize
registry = ClaimRegistry(storage_file="test_claims.json")
system_state = {
    "anchoring": 0.8,
    "damping": 0.7,
    "drive": 0.2,
    "domain": "ai_model_collapse",
    "scale": "generation",
    "regime": "recursive_training",
}
lab = Laboratory(registry, system_state)

# 2. Create a test claim (deliberately vague)
claim = Claim(
    id="C29_TEST",
    statement="Coherens predicts collapse risk continuously and reliably.",
    domain="ai_model_collapse",
    refutation_criteria="If C > 1.0 but collapse occurs, or C < 0.5 but stability persists, refute.",
)
registry.add(claim)

# 3. Run the loop 10 times with varying experiments
experiments = [
    {"name": f"experiment_{i}"} for i in range(10)
]

results = []
for exp in experiments:
    result = lab.run_loop("C29_TEST", exp)
    results.append(result)
    print(f"  Iteration: {result['status']}, C={result.get('coherens', 'N/A')}")

# 4. Check convergence
standing = lab.find_standing_hypotheses()
print(f"\nStanding hypotheses: {len(standing)}")
for h in standing:
    print(f"  - {h.statement} (status: {h.status})")
