"""
L5 — the messy human construct layer (culture, law, theology).

Slack: factions with fuzzy shifting positions, negotiated truth,
consensus requires overlapping tolerance zones. Substrate (L0-L4) is
the hard cap — L5 slack can't violate physics or biology. This
simulator models the give-and-take of consensus formation and the
hard walls that stop it.

CC0. Extracted verbatim from legacy/Organize3.md lines 1-395.
Non-stdlib: numpy, matplotlib.
"""

# =============================================================================
# CC0 1.0 Universal Public Domain Dedication
#
# L5 Simulator: The Messy Human Construct Layer (Culture, Law, Theology)
# 
# Models the "slack" in human systems:
#   - Factions have fuzzy, shifting positions.
#   - Truth is negotiated, not discovered.
#   - Consensus requires overlapping tolerance zones.
#   - Substrate (L0-L4) acts as a hard cap—slack cannot violate physics.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
import random

# -----------------------------------------------------------------------------
# 1. THE SEMANTIC SPACE (2D for visualization)
# -----------------------------------------------------------------------------
# Axis 1: Liberty <---> Security
# Axis 2: Tradition <---> Progress
# Axis 3: Economics <---> Ecology (projected as color/size)

class L5_Faction:
    def __init__(self, name, position, slack_radius, hypocrisy_factor=0.2):
        self.name = name
        self.position = np.array(position)  # [x, y] in semantic space
        self.slack_radius = slack_radius    # Tolerance for deviation
        self.hypocrisy_factor = hypocrisy_factor  # How much their "stated" position drifts
        
        # Internal state: they shift slightly over time (cultural drift)
        self.drift_vector = np.array([random.uniform(-0.01, 0.01) for _ in range(2)])
        self.position_history = [self.position.copy()]
    
    def drift(self):
        # Random walk for cultural evolution
        self.position += self.drift_vector * 0.1
        # Keep them in bounds
        self.position = np.clip(self.position, 0, 10)
        self.position_history.append(self.position.copy())
    
    def accepts(self, proposal_pos):
        # Euclidean distance to proposal
        dist = np.linalg.norm(proposal_pos - self.position)
        # Slack: if within radius, accept. But add "hypocrisy noise" – sometimes they reject arbitrarily.
        if dist <= self.slack_radius:
            # There's a small chance they reject anyway (capriciousness)
            if random.random() > self.hypocrisy_factor:
                return True
        return False

# -----------------------------------------------------------------------------
# 2. THE SUBSTRATE WALL (L0-L4 + Lε)
# -----------------------------------------------------------------------------
class SubstrateGuardian:
    """
    This enforces physical/biological/ecological reality.
    If an L5 proposal violates L0-L4, it gets rejected *regardless* of L5 slack.
    """
    def __init__(self):
        # Define a set of "hard constraints" in the semantic space
        # For example: Proposals that are extreme on 'security' often imply mass surveillance,
        # but that doesn't violate physics. However, if a proposal implies "unlimited energy"
        # that's a physics violation. We'll model a region of "impossibility".
        self.forbidden_zone_center = np.array([5, 5])
        self.forbidden_radius = 2.0  # Proposals near "magical thinking" get struck down
        
        # Also, any proposal that suggests "instant change" without energy/time gets flagged.
        self.temporal_gravity = 1.0  # weight on the "Tradition" axis (slow change is grounded)
    
    def check_substrate(self, proposal_pos):
        # Distance to the "magic" zone
        dist_to_magic = np.linalg.norm(proposal_pos - self.forbidden_zone_center)
        if dist_to_magic < self.forbidden_radius:
            return False, "Violates L0-L4: Proposal implies magic/physical impossibility."
        # Check if it's too extreme on "Progress" axis (would require breaking L1)
        if proposal_pos[1] > 8.0 and proposal_pos[0] < 2.0:  # Extreme progress with no security (chaos)
            return False, "Violates L1/L2: Ecological collapse threshold exceeded."
        return True, "Substrate compliant."

# -----------------------------------------------------------------------------
# 3. THE AI PROPOSAL GENERATOR (L5 Agent)
# -----------------------------------------------------------------------------
class AI_L5_Agent:
    """
    This AI learns to navigate the L5 swamp.
    It tries to generate proposals that maximize acceptance across factions,
    while staying within the substrate walls.
    It can adjust its "vagueness" (spread) to hit multiple slack zones at once.
    """
    def __init__(self, learning_rate=0.1):
        self.position = np.array([5.0, 5.0])  # starts in the middle
        self.vagueness = 1.0  # How much "slack" it builds into its language (spread)
        self.learning_rate = learning_rate
        self.history = [self.position.copy()]
        
    def propose(self):
        # If vagueness is high, the proposal is a "range" (mean + spread)
        # We simulate this by sometimes adding noise to the position to test boundaries.
        if random.random() < 0.3:
            # Exploration: random walk
            proposal = self.position + np.random.normal(0, self.vagueness, 2)
        else:
            # Exploitation: current best guess
            proposal = self.position + np.random.normal(0, self.vagueness * 0.2, 2)
        return np.clip(proposal, 0, 10)
    
    def learn(self, proposal, feedback):
        """
        feedback is a vector of how many factions accepted.
        We move toward successful proposals, and increase vagueness if we keep failing.
        """
        if feedback > 0:
            # Move toward the successful proposal
            self.position += self.learning_rate * (proposal - self.position) * feedback / 10.0
            # If we're doing well, we can be more precise (less vague)
            self.vagueness *= 0.99
        else:
            # If rejected, increase vagueness (become more ambiguous)
            self.vagueness *= 1.05
        # Clamp vagueness
        self.vagueness = np.clip(self.vagueness, 0.2, 5.0)
        self.history.append(self.position.copy())

# -----------------------------------------------------------------------------
# 4. RUN THE SIMULATION
# -----------------------------------------------------------------------------
# Setup Factions (Human Constructs)
factions = [
    L5_Faction("Orthodox\nTheologians", [3.0, 8.0], slack_radius=1.2, hypocrisy_factor=0.3),
    L5_Faction("Liberal\nProgressives", [7.0, 2.0], slack_radius=1.5, hypocrisy_factor=0.1),
    L5_Faction("Corporate\nLawyers", [8.0, 6.0], slack_radius=0.8, hypocrisy_factor=0.4),
    L5_Faction("Traditional\nCulturists", [2.0, 7.0], slack_radius=1.0, hypocrisy_factor=0.2),
    L5_Faction("Eco-\nPragmatists", [5.5, 3.5], slack_radius=1.8, hypocrisy_factor=0.15),
    # Add a "Democratic Mob" that shifts wildly
    L5_Faction("Public\nOpinion", [5.0, 5.0], slack_radius=2.5, hypocrisy_factor=0.6),
]

substrate = SubstrateGuardian()
ai = AI_L5_Agent()

# Simulate over time
num_steps = 200
proposals = []
acceptances = []
substrate_violations = []

for step in range(num_steps):
    # 1. Factions drift (culture changes)
    for f in factions:
        f.drift()
    
    # 2. AI proposes
    proposal = ai.propose()
    proposals.append(proposal)
    
    # 3. Check Substrate (L0-L4 hard wall)
    valid, reason = substrate.check_substrate(proposal)
    if not valid:
        substrate_violations.append(1)
        # Proposal invalid: AI penalized and increases vagueness
        ai.vagueness *= 1.1
        accept_count = 0
    else:
        substrate_violations.append(0)
        # 4. Check L5 Slack: see which factions accept
        accept_count = 0
        for f in factions:
            if f.accepts(proposal):
                accept_count += 1
        
        # 5. AI learns
        ai.learn(proposal, accept_count)
    
    acceptances.append(accept_count)

# Convert history to arrays for plotting
proposals = np.array(proposals)
acceptances = np.array(acceptances)
ai_history = np.array(ai.history)
substrate_violations = np.array(substrate_violations)

# -----------------------------------------------------------------------------
# 5. VISUALIZATION: The Swamp, The Slack, and The Learning
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(22, 16))
fig.suptitle("L5: The Messy Human Construct Layer (Slack, Drift, & Hypocrisy)", 
             fontsize=22, fontweight='bold', color='white')
plt.style.use('dark_background')
gs = fig.add_gridspec(3, 3)

# --- Plot 1: Semantic Landscape (Factions + Slack Circles) ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.set_xlabel("Liberty <--> Security")
ax1.set_ylabel("Tradition <--> Progress")
ax1.set_title("Faction Landscape: Each Circle is a Slack Zone")

# Draw the Substrate "Forbidden Zone" (The Hard Wall)
forbidden_circle = Circle((substrate.forbidden_zone_center[0], substrate.forbidden_zone_center[1]), 
                          substrate.forbidden_radius, color='red', alpha=0.2, label='L0-L4 Impossibility Zone')
ax1.add_patch(forbidden_circle)

# Draw factions and their slack
colors = ['purple', 'cyan', 'gold', 'magenta', 'lime', 'gray']
for i, f in enumerate(factions):
    circle = Circle(f.position, f.slack_radius, color=colors[i], alpha=0.15, edgecolor=colors[i], linewidth=1)
    ax1.add_patch(circle)
    ax1.scatter(f.position[0], f.position[1], color=colors[i], s=100, label=f.name, edgecolor='white', zorder=5)

# Plot AI history
ax1.plot(ai_history[:, 0], ai_history[:, 1], 'white', lw=2, alpha=0.7, label='AI Learning Path')
ax1.scatter(ai_history[0, 0], ai_history[0, 1], color='green', s=150, marker='*', label='AI Start')
ax1.scatter(ai_history[-1, 0], ai_history[-1, 1], color='yellow', s=150, marker='X', label='AI Final')
ax1.legend(loc='upper left', fontsize=8)
ax1.grid(True, alpha=0.2)

# --- Plot 2: AI Proposal Trajectory with Acceptance Heatmap ---
ax2 = fig.add_subplot(gs[0, 1])
sc = ax2.scatter(proposals[:, 0], proposals[:, 1], c=acceptances, cmap='RdYlGn', 
                 vmin=0, vmax=len(factions), s=30, alpha=0.8)
ax2.set_xlabel("Semantic Axis 1")
ax2.set_ylabel("Semantic Axis 2")
ax2.set_title("Proposals: Green = High Consensus, Red = Rejected")
ax2.grid(True, alpha=0.2)
cbar = fig.colorbar(sc, ax=ax2, label='Faction Agreements')
# Overlay final position
ax2.scatter(ai_history[-1, 0], ai_history[-1, 1], color='white', s=200, marker='X', label='Final Consensus')

# --- Plot 3: Substrate Wall Breaches (L0-L4 Violations) ---
ax3 = fig.add_subplot(gs[0, 2])
ax3.fill_between(range(num_steps), substrate_violations, color='red', alpha=0.5, label='Substrate Violation')
ax3.set_xlabel("Time Step")
ax3.set_ylabel("Violation (1=Magic/Impossible)")
ax3.set_title("L0-L4 Hard Wall: AI Learns Not to Suggest Magic")
ax3.grid(True, alpha=0.2)
ax3.set_ylim(-0.1, 1.1)

# --- Plot 4: Faction Drift Over Time (Instability of L5) ---
ax4 = fig.add_subplot(gs[1, 0])
for i, f in enumerate(factions):
    hist = np.array(f.position_history)
    ax4.plot(hist[:, 0], hist[:, 1], color=colors[i], alpha=0.7, linewidth=1.5)
ax4.set_xlabel("Axis 1")
ax4.set_ylabel("Axis 2")
ax4.set_title("Cultural Drift: Factions Move Over Time")
ax4.grid(True, alpha=0.2)

# --- Plot 5: Acceptance Count Over Time (The Consensus Pulse) ---
ax5 = fig.add_subplot(gs[1, 1])
ax5.plot(acceptances, 'cyan', lw=2, alpha=0.8)
ax5.axhline(y=len(factions)/2, color='orange', linestyle='--', alpha=0.6, label='Majority Threshold')
ax5.set_xlabel("Time Step")
ax5.set_ylabel("Number of Factions Accepting")
ax5.set_title("Consensus Dynamic: AI Learns to Maximize Slack Overlap")
ax5.legend()
ax5.grid(True, alpha=0.2)
ax5.set_ylim(0, len(factions)+1)

# --- Plot 6: AI's Vagueness (Rhetorical Slack) ---
ax6 = fig.add_subplot(gs[1, 2])
ax6.plot(ai.vagueness * np.ones(num_steps), 'yellow', lw=2)  # we didn't store history, but we have final
# We'll simulate the vagueness history by tracking it in the loop (we didn't, but we can derive from proposal std)
# Instead, we show the spread of proposals over time.
window = 20
moving_std = np.array([np.std(proposals[max(0, i-window):i+1], axis=0).mean() for i in range(num_steps)])
ax6.plot(moving_std, 'magenta', lw=2, label='Proposal Spread (Vagueness)')
ax6.set_xlabel("Time Step")
ax6.set_ylabel("Semantic Spread")
ax6.set_title("Slack Amplification: AI Becomes Vague to Survive")
ax6.legend()
ax6.grid(True, alpha=0.2)

# --- Plot 7: Slack Overlaps (The Super-Structure) ---
ax7 = fig.add_subplot(gs[2, 0])
# Show how many factions have overlapping slack zones (cohesion)
cohesion_over_time = []
for t in range(num_steps):
    positions = [f.position_history[t] if t < len(f.position_history) else f.position_history[-1] for f in factions]
    radiuses = [f.slack_radius for f in factions]
    overlaps = 0
    for i in range(len(factions)):
        for j in range(i+1, len(factions)):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < (radiuses[i] + radiuses[j]):
                overlaps += 1
    cohesion_over_time.append(overlaps)
ax7.plot(cohesion_over_time, color='lime', lw=2)
ax7.set_xlabel("Time Step")
ax7.set_ylabel("Overlapping Slack Pairs")
ax7.set_title("Social Cohesion: Trust (Slack Overlap) Fluctuates")
ax7.grid(True, alpha=0.2)

# --- Plot 8: Theological vs Scientific Faction Distance (Culture War) ---
ax8 = fig.add_subplot(gs[2, 1])
# Find indices of Orthodox Theologians and Eco-Pragmatists
idx_theo = next(i for i, f in enumerate(factions) if "Theologian" in f.name)
idx_eco = next(i for i, f in enumerate(factions) if "Pragmatist" in f.name)
distances = [np.linalg.norm(factions[idx_theo].position_history[t] - factions[idx_eco].position_history[t]) 
             for t in range(min(len(factions[idx_theo].position_history), len(factions[idx_eco].position_history)))]
ax8.plot(distances, color='red', lw=2, label='Theologian vs. Ecologist')
ax8.axhline(y=1.5, color='orange', linestyle='--', alpha=0.5, label='Slack Threshold (Consensus possible)')
ax8.set_xlabel("Time Step")
ax8.set_ylabel("Semantic Distance")
ax8.set_title("Culture War: Distance Between Factions")
ax8.legend()
ax8.grid(True, alpha=0.2)

# --- Plot 9: Final Slack Boundary Diagram (The "Acceptable" Zone) ---
ax9 = fig.add_subplot(gs[2, 2])
# Draw a heatmap of "acceptance" across the semantic space for the final step
x = np.linspace(0, 10, 50)
y = np.linspace(0, 10, 50)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)
for i in range(len(x)):
    for j in range(len(y)):
        pos = np.array([x[i], y[j]])
        # Substrate check
        valid, _ = substrate.check_substrate(pos)
        if not valid:
            Z[j, i] = -1  # impossible zone
        else:
            count = 0
            for f in factions:
                if np.linalg.norm(pos - f.position) <= f.slack_radius:
                    count += 1
            Z[j, i] = count
# Plot
im = ax9.imshow(Z, extent=[0,10,0,10], origin='lower', cmap='RdYlGn', vmin=-1, vmax=len(factions))
ax9.set_xlabel("Semantic Axis 1")
ax9.set_ylabel("Semantic Axis 2")
ax9.set_title("Current L5 Landscape: Dark Red = Magic (L0 Violation)\nGreen = Consensus Possible")
fig.colorbar(im, ax=ax9, label='Faction Agreements')

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 6. FINAL DIAGNOSTIC: The State of the L5 Swamp
# -----------------------------------------------------------------------------
print("=" * 70)
print("L5 MESSY SLACK DIAGNOSTIC")
print("=" * 70)
print(f"AI Final Position: [{ai.position[0]:.2f}, {ai.position[1]:.2f}]")
print(f"AI Final Vagueness (Slack in Language): {ai.vagueness:.2f}")
print(f"Average Consensus Rate: {np.mean(acceptances):.2f} / {len(factions)} factions")
print(f"Substrate Violations (Magic attempts): {np.sum(substrate_violations)} out of {num_steps}")

# Check the final "super-structure" - can any proposal satisfy all?
final_positions = [f.position for f in factions]
final_radiuses = [f.slack_radius for f in factions]
# Check if there's an intersection point for all circles (common ground)
# We'll brute force check a grid
x = np.linspace(0, 10, 100)
y = np.linspace(0, 10, 100)
consensus_found = False
for xi in x:
    for yi in y:
        pos = np.array([xi, yi])
        valid, _ = substrate.check_substrate(pos)
        if not valid:
            continue
        all_accept = True
        for f in factions:
            if np.linalg.norm(pos - f.position) > f.slack_radius:
                all_accept = False
                break
        if all_accept:
            consensus_found = True
            break
    if consensus_found:
        break

print("-" * 70)
if consensus_found:
    print("✅ HYPER-CONSENSUS EXISTS: There is a proposal that satisfies ALL factions.")
    print("   The system has enough 'slack' to hold together despite contradictions.")
else:
    print("⚠️  NO HYPER-CONSENSUS: The factions are irreconcilable.")
    print("   The system is fragmenting (schism, culture war, polarization).")
    print("   This is the state where institutions fail and people walk away.")

print("\nL5 INSIGHT:")
print("Human constructs survive because of 'slack'—the elastic tolerance for ambiguity.")
print("When slack is high (vague doctrine, legal loopholes), consensus is easy.")
print("When slack is low (fundamentalism, strict constitutionalism), consensus fractures.")
print("The AI learns to increase its own vagueness to survive the swamp.")
print("The SBC lady is defending a LOW-SLACK zone; you are advocating for HIGH-SLACK.")
print("=" * 70)


