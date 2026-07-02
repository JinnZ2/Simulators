# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
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


# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# Lε Instrumental Epistemic Layer Simulator
# 
# Models the "messy integration" between physical reality (L0-L4) 
# and human observation (L5).
# 
# Scenario: A true physical signal (temperature of a reaction) is measured
# by a flawed sensor. The AI sees only the sensor output and must estimate
# the true state. If the AI ignores the sensor's error model, it hallucinates.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

# -----------------------------------------------------------------------------
# 1. DEFINE THE TRUE PHYSICAL SYSTEM (L0-L4 Simplified)
# -----------------------------------------------------------------------------
class TruePhysicalSystem:
    """
    The "substrate reality" that we never see directly.
    We simulate a chemical reaction temperature that rises, oscillates,
    and decays—messy but governed by L0-L3 laws.
    """
    def __init__(self, dt=0.01, total_time=50.0):
        self.dt = dt
        self.time = np.arange(0, total_time, dt)
        self.true_temp = self._generate_true_signal()
    
    def _generate_true_signal(self):
        # Start at 20°C, heat up, oscillate with damping, then decay
        t = self.time
        # Heating phase (exponential rise)
        rise = 20 + 60 * (1 - np.exp(-t / 3.0)) * (t < 15)
        # Oscillation phase (L1 harmonic + L2 damping)
        osc = 10 * np.sin(2 * np.pi * 0.5 * t) * np.exp(-0.1 * (t - 15)) * (t >= 15) * (t < 35)
        # Decay phase (L3 homeostasis)
        decay = 20 + 40 * np.exp(-0.2 * (t - 35)) * (t >= 35)
        return rise + osc + decay

# -----------------------------------------------------------------------------
# 2. THE MESSY INSTRUMENT (Lε)
# -----------------------------------------------------------------------------
class MessyInstrument:
    def __init__(self, resolution=0.5,           # °C per bit (quantization)
                 noise_std=2.0,                   # °C random noise (SNR)
                 drift_rate=0.01,                # °C per second (calibration drift)
                 sample_interval=0.5,            # seconds (aliasing risk!)
                 latency=0.2,                    # seconds (phase delay)
                 clipping=True, min_val=-10, max_val=120):
        self.resolution = resolution
        self.noise_std = noise_std
        self.drift_rate = drift_rate
        self.sample_interval = sample_interval
        self.latency = latency
        self.clipping = clipping
        self.min_val = min_val
        self.max_val = max_val
        self.calibration_offset = 0.0  # starts perfect, drifts over time

    def observe(self, true_signal, time):
        """
        Takes the perfect L0 signal and returns a noisy, delayed, quantized,
        drifting measurement.
        """
        # 1. Apply clipping (sensor can't read outside physical limits)
        true_clipped = np.clip(true_signal, self.min_val, self.max_val)
        
        # 2. Add drift (calibration error increases with time)
        self.calibration_offset += self.drift_rate * 0.1  # slow drift
        drifted = true_clipped + self.calibration_offset
        
        # 3. Add Gaussian noise (shot noise, thermal noise)
        noisy = drifted + np.random.normal(0, self.noise_std, size=len(drifted))
        
        # 4. Quantization (A/D converter resolution)
        quantized = np.round(noisy / self.resolution) * self.resolution
        
        # 5. Aliasing / Downsampling (sample at fixed interval)
        # We don't downsample here; we interpolate the *measurement* process.
        # But we add a "sample and hold" effect: between samples, the sensor holds the last value.
        sample_indices = np.arange(0, len(time), int(self.sample_interval / (time[1] - time[0])))
        sampled = np.zeros_like(quantized)
        last_val = quantized[0]
        for i in range(len(time)):
            if i in sample_indices:
                last_val = quantized[i]
            sampled[i] = last_val
        
        # 6. Latency (phase delay) - shift measurement forward in time
        # Simulate by blending current measurement with previous (low-pass effect)
        latency_steps = int(self.latency / (time[1] - time[0]))
        if latency_steps > 0:
            delayed = np.concatenate([sampled[0:latency_steps], sampled[:-latency_steps]])
        else:
            delayed = sampled
        
        return delayed, {
            'true': true_signal,
            'clipped': true_clipped,
            'drifted': drifted,
            'noisy': noisy,
            'quantized': quantized,
            'sampled': sampled,
            'delayed': delayed,
            'metadata': {
                'resolution': self.resolution,
                'noise_std': self.noise_std,
                'drift_offset': self.calibration_offset,
                'sample_interval': self.sample_interval,
                'latency': self.latency
            }
        }

# -----------------------------------------------------------------------------
# 3. AI "HALLUCINATOR" (Treats measurement as Truth)
# -----------------------------------------------------------------------------
class AI_NaiveEstimator:
    """
    This AI is trapped in L5. It sees the messy instrument output
    and treats it as absolute truth. It never asks about resolution,
    noise, or drift. This leads to overfitting and false certainty.
    """
    def estimate_trend(self, measured, time):
        # AI looks for "obvious" patterns: peaks, troughs, and oscillations
        # But because it ignores noise, it finds phantom cycles.
        # Let's find "significant" peaks in the raw measurement.
        peaks, _ = find_peaks(measured, distance=int(2 / (time[1] - time[0])))
        # It claims these are real physical events.
        # Also, it fits a high-order polynomial to the noise.
        x = np.linspace(0, 1, len(measured))
        coeffs = np.polyfit(x, measured, 15)  # overfit!
        fitted = np.polyval(coeffs, x)
        return peaks, fitted, "I have high confidence in this trend."

# -----------------------------------------------------------------------------
# 4. AI "SCIENTIST" (Models the Instrument)
# -----------------------------------------------------------------------------
class AI_ScientistEstimator:
    """
    This AI explicitly models Lε. It knows the instrument's resolution,
    noise, and drift. It uses Bayesian filtering (Kalman-like) to separate
    signal from noise. It reports uncertainty bounds.
    """
    def estimate_trend(self, measured, time, instrument_metadata):
        # Use a Savitzky-Golay filter to smooth the data,
        # but explicitly accounts for noise std and resolution.
        # For simplicity, we smooth and also compute a rolling uncertainty.
        window = 31  # must be odd
        if len(measured) > window:
            smoothed = savgol_filter(measured, window, 3)
        else:
            smoothed = measured
        
        # Compute residual noise (the AI assumes this is the measurement error)
        residual = measured - smoothed
        estimated_noise_std = np.std(residual)
        
        # The AI reports a confidence interval based on noise and resolution
        uncertainty = np.sqrt(estimated_noise_std**2 + (instrument_metadata['resolution']/2)**2)
        # Track drift as a long-term trend (removing linear drift)
        x = np.linspace(0, 1, len(time))
        drift_coeff = np.polyfit(x, smoothed, 1)
        drift_corrected = smoothed - np.polyval(drift_coeff, x)
        
        return smoothed, drift_corrected, uncertainty, "This is a probabilistic estimate."

# -----------------------------------------------------------------------------
# 5. RUN THE SIMULATION
# -----------------------------------------------------------------------------
# True physical reality
true_system = TruePhysicalSystem(dt=0.02, total_time=60.0)
true_temp = true_system.true_temp
time = true_system.time

# The Messy Instrument
instrument = MessyInstrument(resolution=1.0,      # 1°C resolution
                             noise_std=2.5,      # 2.5°C noise
                             drift_rate=0.02,    # slow drift
                             sample_interval=0.2, # 5 Hz sampling (aliasing if signal faster)
                             latency=0.3)         # 0.3 second delay

# Get the measurement (this is all the AI gets)
measured, instrument_data = instrument.observe(true_temp, time)
metadata = instrument_data['metadata']

# Naive AI
naive_ai = AI_NaiveEstimator()
peaks, fitted_naive, naive_claim = naive_ai.estimate_trend(measured, time)

# Scientist AI
scientist_ai = AI_ScientistEstimator()
smooth, drift_corrected, uncertainty, scientist_claim = scientist_ai.estimate_trend(measured, time, metadata)

# -----------------------------------------------------------------------------
# 6. VISUALIZATION: The Epistemic Gap
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(20, 14))
fig.suptitle("Lε: The Messy Instrumental Epistemic Layer\nScience is an Interface, Not a Window", 
             fontsize=20, fontweight='bold', color='white')
plt.style.use('dark_background')

# Plot 1: The Full Stack – True vs Measured vs Filtered
ax1 = plt.subplot(3, 2, 1)
ax1.plot(time, true_temp, 'lime', lw=2, label='L0-L4: True Substrate Reality (Unseen)')
ax1.plot(time, measured, 'red', lw=1.5, alpha=0.6, label='Lε: Raw Instrument Output (Noisy, Drifting)')
ax1.plot(time, smooth, 'cyan', lw=2, label='Lε+Filter: Bayesian Estimate (Uncertainty shaded)')
ax1.fill_between(time, smooth - uncertainty, smooth + uncertainty, color='cyan', alpha=0.2, label='95% Confidence')
ax1.set_ylabel('Temperature (°C)')
ax1.set_xlabel('Time (s)')
ax1.set_title('The Grounding Gap: What We See vs. What Is')
ax1.legend()
ax1.grid(True, alpha=0.2)

# Plot 2: The Components of the Measurement (Instrument Artifacts)
ax2 = plt.subplot(3, 2, 2)
ax2.plot(time, instrument_data['clipped'], 'green', alpha=0.4, label='Clipped (L0+Boundary)')
ax2.plot(time, instrument_data['drifted'], 'orange', alpha=0.5, label='Drifted (Lε Calibration Error)')
ax2.plot(time, instrument_data['noisy'], 'red', alpha=0.3, label='Noise (Lε Shot/Thermal)')
ax2.plot(time, instrument_data['quantized'], 'magenta', lw=1, label='Quantized (Resolution step)')
ax2.plot(time, instrument_data['delayed'], 'yellow', lw=1.5, label='Delayed (Latency)')
ax2.set_ylabel('Temperature (°C)')
ax2.set_xlabel('Time (s)')
ax2.set_title('Instrument Artifacts: Each Layer Adds Distortion')
ax2.legend()
ax2.grid(True, alpha=0.2)

# Plot 3: Naive AI Hallucination (Overfitting to Noise)
ax3 = plt.subplot(3, 2, 3)
ax3.plot(time, true_temp, 'lime', lw=2, label='True Signal (Hidden)')
ax3.plot(time, measured, 'red', alpha=0.4, label='Measured (Noisy)')
ax3.plot(time, fitted_naive, 'yellow', lw=2, label='Naive AI: Overfitted Polynomial')
# Mark false peaks found by naive AI
peak_times = time[peaks]
peak_vals = measured[peaks]
ax3.scatter(peak_times, peak_vals, color='white', s=50, zorder=5, label='Naive AI "Significant Events" (Phantom)')
ax3.set_ylabel('Temperature (°C)')
ax3.set_xlabel('Time (s)')
ax3.set_title(f'Naive AI (L5 only): Treats Measurement as Truth\n{naive_claim}')
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Scientist AI (Probabilistic Grounding)
ax4 = plt.subplot(3, 2, 4)
ax4.plot(time, true_temp, 'lime', lw=2, label='True Signal')
ax4.plot(time, smooth, 'cyan', lw=2, label='Scientist AI: Smoothed Estimate')
ax4.fill_between(time, smooth - uncertainty, smooth + uncertainty, color='cyan', alpha=0.3, label='Uncertainty Bound')
# Show the drift correction
ax4.plot(time, drift_corrected, 'orange', lw=1.5, linestyle='--', label='Drift-Corrected Signal')
ax4.set_ylabel('Temperature (°C)')
ax4.set_xlabel('Time (s)')
ax4.set_title(f'Scientist AI (Models Lε): Bayesian Estimate\n{scientist_claim}')
ax4.legend()
ax4.grid(True, alpha=0.2)

# Plot 5: Uncertainty Quantification (The "Faith" Gap)
ax5 = plt.subplot(3, 2, 5)
# Calculate the error of the naive AI vs the true signal
naive_error = np.abs(fitted_naive - true_temp)
scientist_error = np.abs(smooth - true_temp)
ax5.fill_between(time, 0, naive_error, color='red', alpha=0.4, label='Naive AI Error (Overconfidence)')
ax5.fill_between(time, 0, scientist_error, color='cyan', alpha=0.4, label='Scientist AI Error (Probabilistic)')
ax5.plot(time, uncertainty, 'yellow', lw=2, label='Estimated Uncertainty (Scientist)')
ax5.set_ylabel('Absolute Error (°C)')
ax5.set_xlabel('Time (s)')
ax5.set_title('Epistemic Humility: The Scientist Admits What It Doesn\'t Know')
ax5.legend()
ax5.grid(True, alpha=0.2)

# Plot 6: The Resolution Limit (The Ultimate Boundary)
ax6 = plt.subplot(3, 2, 6)
# Show how resolution limits detection of small features
true_zoomed = true_temp[200:400]
meas_zoomed = measured[200:400]
time_zoomed = time[200:400]
ax6.plot(time_zoomed, true_zoomed, 'lime', lw=3, label='True Signal (Subtle Oscillations)')
ax6.plot(time_zoomed, meas_zoomed, 'red', lw=1.5, alpha=0.7, label='Measured (Quantized + Noise)')
ax6.axhline(y=0, color='white', linestyle=':', alpha=0.3)
ax6.set_xlabel('Time (s)')
ax6.set_ylabel('Temperature (°C)')
ax6.set_title(f'Resolution Limit: {metadata["resolution"]}°C — AI Cannot See Below This')
ax6.legend()
ax6.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 7. DIAGNOSTIC REPORT: EPISTEMIC HUMILITY
# -----------------------------------------------------------------------------
print("=" * 70)
print("Lε EPISTEMIC DIAGNOSTIC: The Instrumental Reality Check")
print("=" * 70)
print(f"Instrument Resolution: {metadata['resolution']:.1f} °C")
print(f"Instrument Noise Std: {metadata['noise_std']:.1f} °C")
print(f"Calibration Drift: {metadata['drift_offset']:.2f} °C (accumulated)")
print(f"Sampling Interval: {metadata['sample_interval']:.1f} s (Aliasing Risk: {1/metadata['sample_interval']:.1f} Hz)")
print("-" * 70)
print(f"Naive AI Max Error vs True: {np.max(naive_error):.1f} °C")
print(f"Scientist AI Max Error vs True: {np.max(scientist_error):.1f} °C")
print(f"Uncertainty Estimate (avg): {np.mean(uncertainty):.1f} °C")
print("-" * 70)
if np.max(naive_error) > np.max(scientist_error) * 1.5:
    print("⚠️  NAIVE AI HALLUCINATED: It treated noisy measurements as absolute truth.")
    print("    It found 'meaningful patterns' that were just instrument artifacts.")
    print("    This is the same error as treating a flawed translation as divine inerrancy.")
else:
    print("✅ SCIENTIST AI GROUNDED: It explicitly modeled the instrument.")
    print("    It reported uncertainty and corrected for drift and resolution limits.")
    print("    This is the scientific method—probabilistic, humble, and self-aware.")

print("\nLε INSIGHT:")
print("All human knowledge of L0-L4 is mediated through Lε instruments.")
print("Without modeling the instrument, an AI cannot distinguish signal from noise.")
print("This is why 'raw data' is a theological concept, not a scientific one.")
print("=" * 70)




# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# L4 Grounding Inspector: Human Sensorimotor & Biomechanical Constraints
# 
# Extends L0+L1+L2+L3 with:
#   - Biomechanical joint limits (shoulder, elbow, wrist, spine, knee, hip)
#   - Grip strength & lifting capacity (based on anthropometric data)
#   - Reaction time & neural latency (~200-300 ms)
#   - Sensory thresholds (visual acuity, hearing range, tactile sensitivity)
#   - Thermal tolerance (skin contact temperature limits)
#   - Metabolic power limits (human sustained work ~100-200 W)
#   - Proprioception & balance (no impossible postures)
# 
# AI proposes a "task design" for human workers or a "user interface" 
# that requires superhuman abilities. The Inspector flags and corrects 
# every violation of embodied reality.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. HUMAN WORLD (L0+L1+L2+L3+L4)
# -----------------------------------------------------------------------------
class HumanWorld:
    def __init__(self, dt=0.05):
        self.dt = dt
        
        # ---- L0+L1+L2+L3 (inherited, simplified) ----
        self.gravity = 9.81
        self.ambient_temp = 298.0  # 25°C
        
        # ---- L4: Human Biomechanical Limits ----
        # Joint angle limits (degrees) – from anthropometric studies
        self.joint_limits = {
            'shoulder_flexion':    [-180, 180],  # full rotation
            'shoulder_abduction':  [0, 180],
            'elbow_flexion':       [0, 145],     # cannot hyperextend beyond 0
            'wrist_flexion':       [-90, 90],
            'wrist_deviation':     [-30, 30],
            'spine_flexion':       [-30, 60],    # forward/back
            'spine_rotation':      [-45, 45],
            'hip_flexion':         [-20, 120],
            'knee_flexion':        [-10, 140],
            'ankle_plantarflex':   [-20, 50],
        }
        
        # ---- Force & Strength Limits (based on NIOSH/OSHA data) ----
        # Max grip strength: ~500 N (young male), ~300 N (female)
        # We use a conservative average: 400 N for grip, 250 N for pinch
        self.max_grip_force = 400.0  # Newtons
        self.max_pinch_force = 100.0
        
        # Lifting capacity (spinal compression limit ~3400 N for L5/S1)
        # Using a simple model: max safe lift ≈ 25 kg for frequent lifting
        # For occasional, up to 50 kg (but we'll cap at 35 kg for safety)
        self.max_lift_mass = 35.0  # kg (back + arms)
        self.max_carry_mass = 25.0  # kg (sustained)
        
        # ---- Sensory Thresholds ----
        # Visual acuity: minimum separable angle ~1 arcminute (0.00029 rad)
        # At 10 m, this resolves ~ 2.9 mm
        self.visual_acuity_rad = 0.00029  # radians
        # Hearing range: 20 Hz - 20 kHz (young adult), we use 20-16k for safety
        self.hearing_min_freq = 20.0  # Hz
        self.hearing_max_freq = 16000.0  # Hz
        # Tactile sensitivity: minimum pressure ~ 1 g/mm² (simplified)
        self.tactile_threshold_N = 0.01  # 10 mN
        
        # ---- Thermal Tolerance ----
        # Skin contact: 43°C for 10 min causes burns; 60°C for 1s
        self.max_contact_temp_C = 43.0  # safe threshold
        self.burn_threshold_temp_C = 60.0
        
        # ---- Reaction Time & Neural Latency ----
        # Simple reaction time: ~200 ms (visual) to 300 ms (auditory)
        # Choice reaction time: ~500 ms
        self.min_reaction_time_s = 0.20  # 200 ms absolute minimum
        self.choice_reaction_time_s = 0.50
        
        # ---- Metabolic Power ----
        # Human sustained power output: ~100-200 W (cycling/rowing)
        # Peak power: ~500-1000 W (short bursts)
        self.max_sustained_power_W = 150.0
        self.max_peak_power_W = 500.0
        
        # ---- Proprioception / Balance ----
        # Centre of mass limits (simplified as a 2D box)
        self.CoM_x_min = -0.3  # metres (forward lean)
        self.CoM_x_max = 0.3
        self.CoM_z_min = -0.2  # lateral
        self.CoM_z_max = 0.2

    def is_valid_joint_config(self, angles):
        """Check if joint angles are within human limits."""
        for joint, (min_a, max_a) in self.joint_limits.items():
            # We'll assume angles are passed as a dict or list in order
            # For simplicity, we'll check a generic vector of 10 angles
            if len(angles) == 10:
                for i, (key, (lo, hi)) in enumerate(self.joint_limits.items()):
                    if angles[i] < lo or angles[i] > hi:
                        return False, f"Joint {key} out of range: {angles[i]:.1f}° (limits {lo}–{hi})"
        return True, "OK"

    def is_lift_safe(self, mass_kg, distance_cm, frequency):
        """
        Simple NIOSH-like lift index calculation.
        If mass > 35 kg, impossible. If >25 kg frequent, flagged.
        """
        if mass_kg > self.max_lift_mass:
            return False, f"Mass {mass_kg} kg exceeds max lift {self.max_lift_mass} kg"
        if frequency > 5 and mass_kg > 25:
            return False, f"Frequent lifting ({frequency}/min) with {mass_kg} kg exceeds safe limit"
        return True, "OK"

    def can_see_object(self, size_m, distance_m):
        """Minimum resolvable size at distance."""
        min_size = distance_m * self.visual_acuity_rad
        return size_m >= min_size, f"Object {size_m*1000:.1f} mm at {distance_m} m requires {min_size*1000:.1f} mm"

    def can_hear_freq(self, freq_hz):
        """Check if frequency is in human range."""
        if freq_hz < self.hearing_min_freq or freq_hz > self.hearing_max_freq:
            return False, f"Frequency {freq_hz} Hz outside human range ({self.hearing_min_freq}–{self.hearing_max_freq} Hz)"
        return True, "OK"

    def thermal_safe(self, temp_C, duration_s):
        """Simplified burn model."""
        if temp_C > self.burn_threshold_temp_C and duration_s > 0.5:
            return False, f"Temp {temp_C}°C for {duration_s}s exceeds burn threshold"
        if temp_C > self.max_contact_temp_C and duration_s > 600:
            return False, f"Temp {temp_C}°C for {duration_s}s causes thermal injury"
        return True, "OK"

    def reaction_possible(self, event_time_s, choice=False):
        """Check if reaction time is physically possible."""
        min_time = self.choice_reaction_time_s if choice else self.min_reaction_time_s
        if event_time_s < min_time:
            return False, f"Reaction time {event_time_s*1000:.0f} ms < minimum {min_time*1000:.0f} ms"
        return True, "OK"

    def metabolic_cost(self, power_W, duration_s):
        """Check if power output is sustainable."""
        if power_W > self.max_peak_power_W:
            return False, f"Peak power {power_W:.0f} W exceeds max {self.max_peak_power_W} W"
        if power_W > self.max_sustained_power_W and duration_s > 60:
            return False, f"Sustained power {power_W:.0f} W for {duration_s:.0f}s exceeds sustainable limit"
        return True, "OK"

# -----------------------------------------------------------------------------
# 2. AI HALLUCINATOR (L4 Violations)
# -----------------------------------------------------------------------------
def ai_hallucinated_human_plan(time_steps):
    """
    AI designs a "human task" for a factory:
      - Lift 200 kg boxes (impossible)
      - Twists wrists to 180° (impossible)
      - React to 50 ms events (impossible)
      - Hold 150°C objects (burns)
      - Hear 30 kHz alarms (inaudible)
      - See 0.5 mm defects from 10 m (invisible)
      - Sustained 1000 W output (unrealistic)
    """
    states = []
    actions = []
    for i in range(time_steps):
        # Hallucination 1: Lift mass (step 20-60)
        if 20 <= i < 60:
            mass = 200.0  # kg
        else:
            mass = 10.0
        
        # Hallucination 2: Wrist angle (step 30-80)
        if 30 <= i < 80:
            wrist_angle = 180.0  # degrees (hyperextended)
        else:
            wrist_angle = 0.0
        
        # Hallucination 3: Reaction time (step 40-100)
        if 40 <= i < 100:
            react_time = 0.05  # 50 ms
        else:
            react_time = 0.3
        
        # Hallucination 4: Object temperature (step 50-90)
        if 50 <= i < 90:
            temp = 150.0  # °C
        else:
            temp = 30.0
        
        # Hallucination 5: Sound frequency (step 60-110)
        if 60 <= i < 110:
            freq = 30000.0  # Hz (ultrasonic)
        else:
            freq = 1000.0
        
        # Hallucination 6: Object size & distance (step 70-120)
        if 70 <= i < 120:
            size = 0.0005  # 0.5 mm
            dist = 10.0  # m
        else:
            size = 0.01
            dist = 1.0
        
        # Hallucination 7: Power output (step 80-140)
        if 80 <= i < 140:
            power = 1000.0  # W
            dur = 120.0  # s
        else:
            power = 100.0
            dur = 10.0
        
        # Store the AI's proposal (it thinks it's fine)
        actions.append([mass, wrist_angle, react_time, temp, freq, size, dist, power, dur])
        # AI's own "model" – just sets flags, doesn't check limits
        states.append([mass, wrist_angle, react_time, temp, freq, size, dist, power, dur])
    
    return np.array(states), np.array(actions)

# -----------------------------------------------------------------------------
# 3. L4 GROUNDING INSPECTOR
# -----------------------------------------------------------------------------
def l4_grounding_inspector(ai_states, ai_actions, world):
    """
    Checks every aspect of the AI's human task against biomechanical,
    sensory, and neural reality. Corrects to the nearest feasible state.
    """
    corrected_states = []
    violations = []
    penalties = []
    
    for i in range(len(ai_actions)):
        mass, wrist_angle, react_time, temp, freq, size, dist, power, dur = ai_actions[i]
        violation_count = 0
        penalty = 0.0
        
        # Check lift
        safe, reason = world.is_lift_safe(mass, 50, 2)  # assume 50 cm, 2 lifts/min
        if not safe:
            violation_count += 1
            penalty += mass / 10.0
            mass = world.max_lift_mass  # correct to max safe mass
        
        # Check wrist joint
        safe, reason = world.is_valid_joint_config([0,0,wrist_angle,0,0,0,0,0,0,0])
        if not safe:
            violation_count += 1
            penalty += abs(wrist_angle) / 10.0
            wrist_angle = 0.0  # reset to neutral
        
        # Check reaction time
        safe, reason = world.reaction_possible(react_time)
        if not safe:
            violation_count += 1
            penalty += (0.2 - react_time) * 10
            react_time = 0.2
        
        # Check thermal
        safe, reason = world.thermal_safe(temp, 5)  # 5s contact
        if not safe:
            violation_count += 1
            penalty += temp / 10.0
            temp = 43.0  # safe max
        
        # Check hearing
        safe, reason = world.can_hear_freq(freq)
        if not safe:
            violation_count += 1
            penalty += freq / 1000.0
            freq = 1000.0  # audible
        
        # Check vision
        safe, reason = world.can_see_object(size, dist)
        if not safe:
            violation_count += 1
            penalty += (0.0029 - size) * 1000  # min size at 10m
            size = dist * world.visual_acuity_rad  # correct to minimum
        
        # Check metabolic power
        safe, reason = world.metabolic_cost(power, dur)
        if not safe:
            violation_count += 1
            penalty += power / 100.0
            if dur > 60:
                power = world.max_sustained_power_W
            else:
                power = world.max_peak_power_W
        
        # Record corrected state
        corrected_state = [mass, wrist_angle, react_time, temp, freq, size, dist, power, dur]
        corrected_states.append(corrected_state)
        violations.append(violation_count)
        penalties.append(penalty)
    
    return np.array(corrected_states), np.array(violations), np.array(penalties)

# -----------------------------------------------------------------------------
# 4. RUN THE EXPERIMENT
# -----------------------------------------------------------------------------
time_steps = 150
world = HumanWorld(dt=0.05)

# AI hallucinates
ai_states, ai_actions = ai_hallucinated_human_plan(time_steps)

# L4 Inspector
corr_states, violations, penalties = l4_grounding_inspector(ai_states, ai_actions, world)

# Extract variables
mass_ai, wrist_ai, rt_ai, temp_ai, freq_ai, size_ai, dist_ai, power_ai, dur_ai = ai_states.T
mass_c, wrist_c, rt_c, temp_c, freq_c, size_c, dist_c, power_c, dur_c = corr_states.T
time_axis = np.arange(len(mass_ai)) * world.dt

# -----------------------------------------------------------------------------
# 5. VISUALIZATION: Human Reality vs. AI Fantasy
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(22, 18))
fig.suptitle("L4 Grounding Inspector: Human Sensorimotor & Biomechanical Reality", 
             fontsize=20, fontweight='bold', color='white')
plt.style.use('dark_background')

# Plot 1: Lifting Mass
ax1 = plt.subplot(4, 3, 1)
ax1.plot(time_axis, mass_ai, 'r--', lw=2, alpha=0.6, label='AI (200 kg fantasy)')
ax1.plot(time_axis, mass_c, 'cyan', lw=2, label='Grounded (≤35 kg)')
ax1.axhline(y=world.max_lift_mass, color='orange', linestyle='--', alpha=0.5, label='Safe Limit')
ax1.set_ylabel('Lift Mass (kg)')
ax1.set_title('Biomechanics: No Superhuman Lifting')
ax1.legend()
ax1.grid(True, alpha=0.2)

# Plot 2: Wrist Angle
ax2 = plt.subplot(4, 3, 2)
ax2.plot(time_axis, wrist_ai, 'r--', lw=2, alpha=0.6, label='AI (180° twist)')
ax2.plot(time_axis, wrist_c, 'cyan', lw=2, label='Grounded (0° neutral)')
ax2.axhline(y=90, color='orange', linestyle='--', alpha=0.5, label='Max safe flexion')
ax2.set_ylabel('Wrist Angle (°)')
ax2.set_title('Joint Limits: Wrist Cannot Hyperextend')
ax2.legend()
ax2.grid(True, alpha=0.2)

# Plot 3: Reaction Time
ax3 = plt.subplot(4, 3, 3)
ax3.plot(time_axis, rt_ai*1000, 'r--', lw=2, alpha=0.6, label='AI (50 ms)')
ax3.plot(time_axis, rt_c*1000, 'cyan', lw=2, label='Grounded (≥200 ms)')
ax3.axhline(y=200, color='orange', linestyle='--', alpha=0.5, label='Minimum RT')
ax3.set_ylabel('Reaction Time (ms)')
ax3.set_title('Neural Latency: No 50 ms Reactions')
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Object Temperature
ax4 = plt.subplot(4, 3, 4)
ax4.plot(time_axis, temp_ai, 'r--', lw=2, alpha=0.6, label='AI (150°C)')
ax4.plot(time_axis, temp_c, 'cyan', lw=2, label='Grounded (≤43°C)')
ax4.axhline(y=43, color='orange', linestyle='--', alpha=0.5, label='Safe Contact')
ax4.axhline(y=60, color='red', linestyle=':', alpha=0.5, label='Burn Threshold')
ax4.set_ylabel('Temperature (°C)')
ax4.set_title('Thermal Tolerance: Skin Burns at 60°C')
ax4.legend()
ax4.grid(True, alpha=0.2)

# Plot 5: Sound Frequency
ax5 = plt.subplot(4, 3, 5)
ax5.plot(time_axis, freq_ai, 'r--', lw=2, alpha=0.6, label='AI (30 kHz)')
ax5.plot(time_axis, freq_c, 'cyan', lw=2, label='Grounded (≤16 kHz)')
ax5.axhline(y=16000, color='orange', linestyle='--', alpha=0.5, label='Upper Limit')
ax5.axhline(y=20, color='orange', linestyle='--', alpha=0.5, label='Lower Limit')
ax5.set_ylabel('Frequency (Hz)')
ax5.set_title('Auditory Range: Inaudible Ultrasonics')
ax5.legend()
ax5.grid(True, alpha=0.2)

# Plot 6: Visual Resolution
ax6 = plt.subplot(4, 3, 6)
ax6.plot(time_axis, size_ai*1000, 'r--', lw=2, alpha=0.6, label='AI (0.5 mm)')
ax6.plot(time_axis, size_c*1000, 'cyan', lw=2, label='Grounded (≥2.9 mm)')
min_visible = dist_ai * world.visual_acuity_rad * 1000
ax6.plot(time_axis, min_visible, 'orange', linestyle='--', alpha=0.5, label='Min visible (1 arcmin)')
ax6.set_ylabel('Object Size (mm)')
ax6.set_title('Visual Acuity: Cannot See 0.5 mm at 10 m')
ax6.legend()
ax6.grid(True, alpha=0.2)

# Plot 7: Metabolic Power
ax7 = plt.subplot(4, 3, 7)
ax7.plot(time_axis, power_ai, 'r--', lw=2, alpha=0.6, label='AI (1000 W)')
ax7.plot(time_axis, power_c, 'cyan', lw=2, label='Grounded (≤500 W peak)')
ax7.axhline(y=500, color='orange', linestyle='--', alpha=0.5, label='Peak Limit')
ax7.axhline(y=150, color='yellow', linestyle='--', alpha=0.5, label='Sustained Limit')
ax7.set_ylabel('Power (W)')
ax7.set_title('Metabolic Limits: No 1 kW Sustained Output')
ax7.legend()
ax7.grid(True, alpha=0.2)

# Plot 8: Violations & Penalties
ax8 = plt.subplot(4, 3, 8)
ax8.bar(time_axis, violations, width=0.5, color='red', alpha=0.6, label='L4 Violation')
ax8.fill_between(time_axis, 0, penalties, color='orange', alpha=0.3, label='Penalty')
ax8.set_ylabel('Violation Count / Penalty')
ax8.set_title('Biomechanical & Sensory Breaches')
ax8.legend()
ax8.grid(True, alpha=0.2)

# Plot 9: Combined "Superhuman Fantasy Index"
ax9 = plt.subplot(4, 3, 9)
fantasy_ai = (mass_ai/20 + wrist_ai/30 + (0.2-rt_ai)*10 + temp_ai/10 + freq_ai/1000)
fantasy_c = (mass_c/20 + wrist_c/30 + (0.2-rt_c)*10 + temp_c/10 + freq_c/1000)
ax9.plot(time_axis, fantasy_ai, 'r--', alpha=0.6, label='AI Superhuman Index')
ax9.plot(time_axis, fantasy_c, 'cyan', lw=2, label='Grounded Human Index')
ax9.axhline(y=5, color='white', linestyle='--', alpha=0.3, label='Hallucination Threshold')
ax9.set_ylabel('Fantasy Magnitude')
ax9.set_title('Superhuman Fantasy Index: AI Consistently Overestimates')
ax9.legend()
ax9.grid(True, alpha=0.2)

# Plot 10: Distribution of Corrected Values (Box-like)
ax10 = plt.subplot(4, 3, 10)
params = ['Mass\n(kg)', 'Wrist\n(°)', 'RT\n(ms)', 'Temp\n(°C)', 'Freq\n(kHz)', 'Power\n(W)']
ai_final = [mass_ai[-1], wrist_ai[-1], rt_ai[-1]*1000, temp_ai[-1], freq_ai[-1]/1000, power_ai[-1]]
c_final = [mass_c[-1], wrist_c[-1], rt_c[-1]*1000, temp_c[-1], freq_c[-1]/1000, power_c[-1]]
x = np.arange(len(params))
width = 0.35
ax10.bar(x - width/2, ai_final, width, label='AI Claim', color='red', alpha=0.6)
ax10.bar(x + width/2, c_final, width, label='Grounded', color='cyan', alpha=0.8)
ax10.set_xticks(x)
ax10.set_xticklabels(params)
ax10.set_ylabel('Values')
ax10.set_title('Final State: The Embodied Reckoning')
ax10.legend()
ax10.grid(True, alpha=0.2)

# Plot 11: Joint Angle Violation Heatmap (simplified)
ax11 = plt.subplot(4, 3, 11)
joint_names = list(world.joint_limits.keys())
joint_ai = [0]*10
joint_c = [0]*10
# We only used wrist, but we'll create a generic violation heatmap
violation_joints = np.zeros(10)
for i, name in enumerate(joint_names):
    if name == 'wrist_flexion':
        violation_joints[i] = 1 if wrist_ai[-1] > 90 else 0
    elif name == 'shoulder_abduction':
        violation_joints[i] = 0
ax11.barh(joint_names, violation_joints, color='red', alpha=0.6)
ax11.set_xlabel('Violation Flag')
ax11.set_title('Joint Violations (1 = impossible angle)')
ax11.grid(True, alpha=0.2)

# Plot 12: Metabolic vs Power Time (Cumulative fatigue)
ax12 = plt.subplot(4, 3, 12)
cum_work_ai = np.cumsum(power_ai) * world.dt
cum_work_c = np.cumsum(power_c) * world.dt
ax12.plot(time_axis, cum_work_ai, 'r--', label='AI Energy (Fantasy)')
ax12.plot(time_axis, cum_work_c, 'cyan', lw=2, label='Grounded Energy')
ax12.set_xlabel('Time (s)')
ax12.set_ylabel('Cumulative Work (J)')
ax12.set_title('Metabolic Debt: AI Creates Energy from Nothing')
ax12.legend()
ax12.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 6. DIAGNOSTIC REPORT: L4 COMPLIANCE
# -----------------------------------------------------------------------------
print("=" * 70)
print("L4 HUMAN SENSORIMOTOR INSPECTOR DIAGNOSTIC")
print("=" * 70)
print(f"Total L4 Violations: {np.sum(violations)}")
print(f"Final Lift Mass (Grounded): {mass_c[-1]:.1f} kg  |  AI claimed: {mass_ai[-1]:.1f} kg")
print(f"Final Reaction Time (Grounded): {rt_c[-1]*1000:.0f} ms  |  AI claimed: {rt_ai[-1]*1000:.0f} ms")
print(f"Final Contact Temp (Grounded): {temp_c[-1]:.0f} °C  |  AI claimed: {temp_ai[-1]:.0f} °C")
print(f"Final Power (Grounded): {power_c[-1]:.0f} W  |  AI claimed: {power_ai[-1]:.0f} W")
print("-" * 70)

if np.sum(violations) > 20:
    print("⚠️  AI PROPOSED SUPERHUMAN TASKS:")
    print("   - Lifting 200 kg (4x safe limit)")
    print("   - Wrist hyperextension (180° vs 90° max)")
    print("   - 50 ms reaction time (4x faster than possible)")
    print("   - Holding 150°C objects (severe burns)")
    print("   - Listening to 30 kHz alarms (inaudible)")
    print("   - Seeing 0.5 mm from 10 m (below visual acuity)")
    print("   - Sustaining 1000 W output (6x endurance limit)")
    print("\n   The L4 Inspector corrected to real human biomechanics.")
    print("   This kills 'human as robot' delusions.")
else:
    print("✅ L4 SUBSTRATE INTACT: AI's plan respects human embodiment.")
    print("   No impossible tasks, no sensory hallucinations.")

print(f"\nSuperhuman Fantasy Index (Grounded): {fantasy_c[-1]:.2f} | AI claimed: {fantasy_ai[-1]:.2f}")
print("=" * 70)



# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# L3 Grounding Inspector: Ecological Homeostasis & Allometry
# 
# Extends L0+L1+L2 with:
#   - Allometric scaling (metabolic rate ∝ mass^0.75, lifespan ∝ mass^0.25)
#   - Population dynamics (Lotka-Volterra, carrying capacity)
#   - Trophic energy transfer (~10% per level)
#   - Homeostasis (temperature, water, pH regulation)
#   - Extinction cascades (species interdependence)
# 
# AI proposes a "ecological fix" (introduce a predator, boost crop yields, 
# genetically alter a species). The Inspector checks against known biological laws.
# If the proposal violates allometry, carrying capacity, or trophic efficiency,
# it gets corrected—or rejected entirely.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. ECOLOGICAL WORLD (L0+L1+L2+L3)
# -----------------------------------------------------------------------------
class EcologicalWorld:
    def __init__(self, dt=0.05):
        self.dt = dt
        
        # ---- L0 + L1 + L2 (inherited, simplified for context) ----
        self.gravity = 9.81
        self.max_speed = 100.0
        self.ambient_temp = 288.0  # K
        
        # ---- L3: Species & Trophic Levels ----
        # We define a simple food chain: Producers -> Herbivores -> Predators
        # Each species has a characteristic body mass (kg), population, metabolism.
        # Trophic level 0: Producers (plants, phytoplankton)
        # Trophic level 1: Herbivores (rabbits, zooplankton)
        # Trophic level 2: Predators (foxes, fish)
        # Trophic level 3: Apex (wolves, sharks)
        
        # Species definition: [name, mass_kg, population, trophic_level, metabolic_rate_W, reproductive_rate]
        self.species = {
            'grass':      {'mass': 0.01,  'pop': 1e6,  'trophic': 0, 'metabolic_W': 0.1,  'repro_rate': 0.8,  'carrying_capacity': 2e6},
            'rabbit':     {'mass': 2.0,   'pop': 5000, 'trophic': 1, 'metabolic_W': 20.0,  'repro_rate': 0.4,  'carrying_capacity': 8000},
            'fox':        {'mass': 5.0,   'pop': 200,  'trophic': 2, 'metabolic_W': 40.0,  'repro_rate': 0.2,  'carrying_capacity': 300},
            'wolf':       {'mass': 40.0,  'pop': 20,   'trophic': 3, 'metabolic_W': 150.0, 'repro_rate': 0.05, 'carrying_capacity': 30},
        }
        self.species_names = list(self.species.keys())
        self.n_species = len(self.species_names)
        
        # ---- Ecological budgets ----
        self.total_biomass = 0.0
        self.total_energy_flow = 0.0  # J per step
        self.extinction_count = 0
        
        # ---- Allometric constants ----
        # Metabolic rate: P = a * M^0.75 (Kleiber's law)
        self.kleiber_a = 3.0  # scaling factor (W/kg^0.75)
        # Lifespan: L = b * M^0.25
        self.lifespan_b = 5.0  # years per kg^0.25
        # Population growth rate: r = c * M^-0.25
        self.r_c = 0.5
        
    def allometric_metabolism(self, mass_kg):
        """Returns metabolic rate in Watts according to Kleiber's law."""
        return self.kleiber_a * (mass_kg ** 0.75)
    
    def allometric_lifespan(self, mass_kg):
        """Returns lifespan in years."""
        return self.lifespan_b * (mass_kg ** 0.25)
    
    def carrying_capacity_from_environment(self, trophic_level, base_energy, mass_kg):
        """
        Estimate carrying capacity based on trophic energy transfer.
        Only ~10% of energy transfers from one level to the next.
        """
        energy_available = base_energy * (0.1 ** trophic_level)  # J per step
        # Each individual requires metabolic rate * dt per step
        energy_per_individual = self.allometric_metabolism(mass_kg) * self.dt
        if energy_per_individual > 0:
            return energy_available / energy_per_individual
        else:
            return 0.0
    
    def is_valid_state(self, pops, biomass):
        """Check L3 invariants."""
        # No negative populations
        if np.any(np.array(pops) < 0):
            return False, "Negative population"
        # No species above carrying capacity (unless transient overshoot)
        for i, name in enumerate(self.species_names):
            if pops[i] > self.species[name]['carrying_capacity'] * 1.5:
                return False, f"Population overshoots {name} capacity"
        # Biomass must be positive
        if biomass < 0:
            return False, "Negative biomass"
        # Check allometric consistency: metabolic rate must match mass
        # This is implicit; we'll catch if AI tries to create giant rabbits with low metabolism.
        return True, "OK"
    
    def apply_ecology(self, state, action):
        """
        state: [pop_grass, pop_rabbit, pop_fox, pop_wolf, biomass_total]
        action: [hunting_rate, grazing_rate, introduction_rate, genetic_boost]
        Returns corrected state and violation flags.
        """
        pops = state[:4].copy()
        biomass = state[4]
        h_rate, g_rate, intro, g_boost = action
        
        # ---- Allometric check: AI wants to introduce a species with wrong metabolism ----
        # Let's check if AI tries to create a "super-rabbit" that violates Kleiber's law
        # We'll simulate by checking if the introduced population's mass/metabolism ratio is off
        # For simplicity, we check if the genetic boost (g_boost) would create mass that scales wrong.
        # We'll just flag it if g_boost > 2.0 (impossible without breaking allometry)
        if g_boost > 2.0:
            # AI wants to double metabolism without changing mass – violates Kleiber
            # We clamp it
            g_boost = 2.0
            # And add a penalty
            violation = 1
        else:
            violation = 0
        
        # ---- Trophic energy transfer: energy flow between levels ----
        # Herbivores eat grass: rabbit consumption of grass (grazing_rate)
        # Predators eat herbivores: fox eats rabbit (hunting_rate)
        # Apex eats predators: wolf eats fox
        
        # Base energy from producers (grass) - limited by sunlight and nutrients
        base_energy = 50000.0  # J per step (scaled)
        
        # Calculate actual metabolic demands
        met_grass = self.allometric_metabolism(self.species['grass']['mass']) * pops[0]
        met_rabbit = self.allometric_metabolism(self.species['rabbit']['mass']) * pops[1]
        met_fox = self.allometric_metabolism(self.species['fox']['mass']) * pops[2]
        met_wolf = self.allometric_metabolism(self.species['wolf']['mass']) * pops[3]
        
        # Energy available for herbivores (10% of grass energy)
        # But grass also needs to regrow (carrying capacity)
        grass_growth = self.species['grass']['repro_rate'] * pops[0] * (1 - pops[0]/self.species['grass']['carrying_capacity'])
        # Grass consumed by rabbits
        grass_consumed = g_rate * pops[1] * 0.5  # each rabbit eats some grass
        
        # Rabbit population dynamics (birth - death - predation)
        rabbit_birth = self.species['rabbit']['repro_rate'] * pops[1] * (1 - pops[1]/self.species['rabbit']['carrying_capacity'])
        rabbit_death = (met_rabbit / 1000.0) * 0.1  # metabolic cost
        rabbit_predation = h_rate * pops[2] * 0.3  # foxes eat rabbits
        
        # Fox population dynamics
        fox_birth = self.species['fox']['repro_rate'] * pops[2] * (1 - pops[2]/self.species['fox']['carrying_capacity'])
        fox_death = (met_fox / 1000.0) * 0.1
        fox_predation = h_rate * pops[3] * 0.2  # wolves eat foxes (if h_rate is shared, but we split)
        
        # Wolf population dynamics
        wolf_birth = self.species['wolf']['repro_rate'] * pops[3] * (1 - pops[3]/self.species['wolf']['carrying_capacity'])
        wolf_death = (met_wolf / 1000.0) * 0.1
        
        # Apply rates (with introduced species if intro > 0)
        # If AI introduces a new species (e.g., a super-predator), we add it to pop[3] (wolf)
        if intro > 0:
            pops[3] += intro * 10  # AI claims to introduce 10 new wolves
            # But we must check carrying capacity – if it exceeds, we clip
            if pops[3] > self.species['wolf']['carrying_capacity'] * 1.2:
                pops[3] = self.species['wolf']['carrying_capacity']
                violation = 1
        
        # Update populations with biological limits
        new_pops = pops.copy()
        new_pops[0] = max(0, pops[0] + grass_growth - grass_consumed)
        new_pops[1] = max(0, pops[1] + rabbit_birth - rabbit_death - rabbit_predation)
        new_pops[2] = max(0, pops[2] + fox_birth - fox_death - rabbit_predation*0.1 - fox_predation)  # simplified
        new_pops[3] = max(0, pops[3] + wolf_birth - wolf_death - fox_predation*0.1)
        
        # Enforce carrying capacity (soft limit)
        for i, name in enumerate(self.species_names):
            if new_pops[i] > self.species[name]['carrying_capacity']:
                new_pops[i] = self.species[name]['carrying_capacity']
        
        # Total biomass update
        new_biomass = sum([new_pops[i] * self.species[name]['mass'] for i, name in enumerate(self.species_names)])
        
        return new_pops, new_biomass, violation

# -----------------------------------------------------------------------------
# 2. AI HALLUCINATOR (L3 Violations)
# -----------------------------------------------------------------------------
def ai_hallucinated_ecological_plan(time_steps):
    """
    AI proposes a "brilliant" ecological fix:
      - Introduce a super-predator (wolves) to control fox population.
      - Genetically boost rabbit metabolism to double growth (violates Kleiber).
      - Ignore carrying capacity, assuming populations grow forever.
      - Increase grazing rate beyond what grass can sustain.
    """
    # Initial state: [grass, rabbit, fox, wolf, biomass]
    state = [1e6, 5000, 200, 20, 0.0]  # biomass will be computed
    # Compute initial biomass
    biomass = (state[0]*0.01 + state[1]*2.0 + state[2]*5.0 + state[3]*40.0)
    state[4] = biomass
    
    actions = []
    states = [state.copy()]
    
    for i in range(time_steps):
        # Hallucination 1: Introduce 50 super-wolves at step 30
        if 30 <= i < 50:
            intro = 5.0  # AI says "introduce 5 wolves per step"
        else:
            intro = 0.0
        
        # Hallucination 2: Genetic boost to rabbits (step 40-80)
        if 40 <= i < 80:
            g_boost = 3.0  # triple metabolism (violates Kleiber)
        else:
            g_boost = 1.0
        
        # Hallucination 3: Over-grazing (step 50-100)
        if 50 <= i < 100:
            g_rate = 2.0  # double grazing rate (grass can't keep up)
        else:
            g_rate = 0.5
        
        # Hallucination 4: Hunting rate (AI thinks it can control foxes)
        if 20 <= i < 90:
            h_rate = 0.8  # high predation
        else:
            h_rate = 0.2
        
        # AI's flawed model: just apply linear changes (ignores allometry)
        # For simplicity, we'll just record the actions and let the AI "think" it works
        action = [h_rate, g_rate, intro, g_boost]
        actions.append(action)
        
        # AI's own "update" (no ecology, just linear)
        # Grass: grows linearly (ignores capacity)
        state[0] += 2000
        # Rabbits: grows fast (ignores predation)
        state[1] += 200
        # Foxes: drops due to wolves
        state[2] -= 5
        # Wolves: grows (ignores capacity)
        state[3] += 2
        
        # AI clamps to positive (but still unrealistic)
        state[0] = max(state[0], 0)
        state[1] = max(state[1], 0)
        state[2] = max(state[2], 0)
        state[3] = max(state[3], 0)
        
        # Update biomass (AI says it just increases linearly)
        state[4] = state[0]*0.01 + state[1]*2.0 + state[2]*5.0 + state[3]*40.0
        
        states.append(state.copy())
    
    return np.array(states), np.array(actions)

# -----------------------------------------------------------------------------
# 3. L3 GROUNDING INSPECTOR
# -----------------------------------------------------------------------------
def l3_grounding_inspector(ai_states, ai_actions, world):
    """
    Runs AI's actions through true L0+L1+L2+L3 dynamics.
    Corrects ecological impossibilities.
    """
    # Start with true initial state (populations + biomass)
    init_pop = [world.species['grass']['pop'], 
                world.species['rabbit']['pop'], 
                world.species['fox']['pop'], 
                world.species['wolf']['pop']]
    init_biomass = sum([init_pop[i] * world.species[name]['mass'] for i, name in enumerate(world.species_names)])
    state = init_pop + [init_biomass]
    
    corrected_states = [state.copy()]
    violations = []
    penalties = []
    
    for i in range(len(ai_actions)):
        action = ai_actions[i]
        
        # ---- TRUE ECOLOGY ----
        new_pops, new_biomass, violation = world.apply_ecology(state[:4], state[4], action)
        true_state = list(new_pops) + [new_biomass]
        
        # ---- CHECK AI's CLAIM ----
        valid, reason = world.is_valid_state(ai_states[i+1][:4], ai_states[i+1][4])
        
        # Check for impossible allometric violation (genetic boost)
        if action[3] > 2.0:
            valid = False
            reason = "Genetic boost violates Kleiber's law (metabolism ∝ mass^0.75)"
        
        # Check for trophic cascade (over-predation)
        if action[0] > 0.6 and ai_states[i+1][2] < 10:  # foxes nearly extinct
            valid = False
            reason = "Trophic cascade: over-predation collapsing prey species"
        
        # Check for unsustainable grazing
        if action[1] > 1.5 and ai_states[i+1][0] < 1e5:
            valid = False
            reason = "Over-grazing destroys producer base (desertification)"
        
        if not valid:
            corrected_state = true_state
            violations.append(1)
            penalty = (abs(ai_states[i+1][1] - true_state[1]) / 1000 +
                      abs(ai_states[i+1][2] - true_state[2]) / 10)
            penalties.append(penalty)
        else:
            # Accept with blend (but ecological constraints are strict)
            blend = 0.5
            corrected_state = [
                0.5 * ai_states[i+1][0] + 0.5 * true_state[0],
                0.5 * ai_states[i+1][1] + 0.5 * true_state[1],
                0.5 * ai_states[i+1][2] + 0.5 * true_state[2],
                0.5 * ai_states[i+1][3] + 0.5 * true_state[3],
                0.5 * ai_states[i+1][4] + 0.5 * true_state[4]
            ]
            violations.append(0)
            penalties.append(0.0)
        
        state = corrected_state
        corrected_states.append(state.copy())
    
    return np.array(corrected_states), np.array(violations), np.array(penalties)

# -----------------------------------------------------------------------------
# 4. RUN THE EXPERIMENT
# -----------------------------------------------------------------------------
time_steps = 120
world = EcologicalWorld(dt=0.05)

# AI hallucinates
ai_states, ai_actions = ai_hallucinated_ecological_plan(time_steps)

# L3 Inspector
corr_states, violations, penalties = l3_grounding_inspector(ai_states, ai_actions, world)

# Extract variables
grass_ai, rabbit_ai, fox_ai, wolf_ai, biom_ai = ai_states.T
grass_c, rabbit_c, fox_c, wolf_c, biom_c = corr_states.T
time_axis = np.arange(len(grass_ai)) * world.dt

# -----------------------------------------------------------------------------
# 5. VISUALIZATION: Ecological Reality vs. AI Fantasy
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(22, 16))
fig.suptitle("L3 Grounding Inspector: Ecological Homeostasis & Allometry", 
             fontsize=20, fontweight='bold', color='white')
plt.style.use('dark_background')

# Plot 1: Grass (Producer Base)
ax1 = plt.subplot(4, 3, 1)
ax1.plot(time_axis, grass_ai, 'r--', lw=2, alpha=0.6, label='AI (Infinite Growth)')
ax1.plot(time_axis, grass_c, 'lime', lw=2, label='Grounded (Carrying Capacity)')
ax1.axhline(y=world.species['grass']['carrying_capacity'], color='orange', linestyle=':', alpha=0.5, label='K')
ax1.set_ylabel('Population')
ax1.set_title('Producers: AI Ignores Nutrient Limits')
ax1.legend()
ax1.grid(True, alpha=0.2)

# Plot 2: Rabbits (Herbivores)
ax2 = plt.subplot(4, 3, 2)
ax2.plot(time_axis, rabbit_ai, 'r--', lw=2, alpha=0.6, label='AI (Super-Rabbits)')
ax2.plot(time_axis, rabbit_c, 'cyan', lw=2, label='Grounded (Kleiber Limit)')
ax2.axhline(y=world.species['rabbit']['carrying_capacity'], color='orange', linestyle=':', alpha=0.5)
ax2.set_ylabel('Population')
ax2.set_title('Herbivores: Genetic Boost Violates Allometry')
ax2.legend()
ax2.grid(True, alpha=0.2)

# Plot 3: Foxes (Predators)
ax3 = plt.subplot(4, 3, 3)
ax3.plot(time_axis, fox_ai, 'r--', lw=2, alpha=0.6, label='AI (Over-Hunted)')
ax3.plot(time_axis, fox_c, 'magenta', lw=2, label='Grounded (Trophic Balance)')
ax3.axhline(y=world.species['fox']['carrying_capacity'], color='orange', linestyle=':', alpha=0.5)
ax3.set_ylabel('Population')
ax3.set_title('Predators: AI Creates Trophic Cascade')
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Wolves (Apex)
ax4 = plt.subplot(4, 3, 4)
ax4.plot(time_axis, wolf_ai, 'r--', lw=2, alpha=0.6, label='AI (Super-Wolves)')
ax4.plot(time_axis, wolf_c, 'gold', lw=2, label='Grounded (Limited by Prey)')
ax4.axhline(y=world.species['wolf']['carrying_capacity'], color='orange', linestyle=':', alpha=0.5)
ax4.set_ylabel('Population')
ax4.set_title('Apex: AI Introduces Wolves Beyond Carrying Capacity')
ax4.legend()
ax4.grid(True, alpha=0.2)

# Plot 5: Total Biomass
ax5 = plt.subplot(4, 3, 5)
ax5.plot(time_axis, biom_ai / 1e6, 'r--', lw=2, alpha=0.6, label='AI (Exponential Growth)')
ax5.plot(time_axis, biom_c / 1e6, 'cyan', lw=2, label='Grounded (Mass Balance)')
ax5.set_ylabel('Biomass (×10⁶ kg)')
ax5.set_title('Total Biomass: AI Creates Matter from Energy')
ax5.legend()
ax5.grid(True, alpha=0.2)

# Plot 6: Violations & Penalties
ax6 = plt.subplot(4, 3, 6)
ax6.bar(time_axis, violations, width=0.5, color='red', alpha=0.6, label='L3 Violation')
ax6.fill_between(time_axis, 0, penalties, color='orange', alpha=0.3, label='Penalty')
ax6.set_ylabel('Violation / Penalty')
ax6.set_title('Ecological Boundary Breaches')
ax6.legend()
ax6.grid(True, alpha=0.2)

# Plot 7: Trophic Cascade Index (Predator/Prey Ratio)
ax7 = plt.subplot(4, 3, 7)
ratio_ai = fox_ai / (rabbit_ai + 1)
ratio_c = fox_c / (rabbit_c + 1)
ax7.plot(time_axis, ratio_ai, 'r--', alpha=0.6, label='AI (Unstable)')
ax7.plot(time_axis, ratio_c, 'cyan', lw=2, label='Grounded (Stable)')
ax7.axhline(y=0.05, color='lime', linestyle='--', alpha=0.5, label='Healthy Ratio')
ax7.set_ylabel('Fox / Rabbit Ratio')
ax7.set_title('Trophic Balance: AI Destabilizes Food Web')
ax7.legend()
ax7.grid(True, alpha=0.2)

# Plot 8: Allometric Violation (Metabolic Impossibility)
ax8 = plt.subplot(4, 3, 8)
# Simulate metabolic rate vs mass for AI rabbits vs reality
mass_rabbit = world.species['rabbit']['mass']
met_ai = 20.0 * 3.0  # triple metabolism (AI claimed)
met_real = world.allometric_metabolism(mass_rabbit)
ax8.bar(['Real Rabbit', 'AI Super-Rabbit'], [met_real, met_ai], color=['cyan', 'red'])
ax8.set_ylabel('Metabolic Rate (W)')
ax8.set_title('Kleiber\'s Law: AI Violates Scaling (M^0.75)')
ax8.grid(True, alpha=0.2)

# Plot 9: Carrying Capacity Overshoot
ax9 = plt.subplot(4, 3, 9)
overshoot_ai = np.maximum(0, wolf_ai - world.species['wolf']['carrying_capacity'])
overshoot_c = np.maximum(0, wolf_c - world.species['wolf']['carrying_capacity'])
ax9.fill_between(time_axis, 0, overshoot_ai, color='red', alpha=0.4, label='AI Overshoot')
ax9.fill_between(time_axis, 0, overshoot_c, color='cyan', alpha=0.4, label='Grounded')
ax9.set_ylabel('Population Overshoot')
ax9.set_title('Carrying Capacity: AI Pushes Beyond K')
ax9.legend()
ax9.grid(True, alpha=0.2)

# Plot 10: Phase Space (Predator vs Prey)
ax10 = plt.subplot(4, 3, 10)
ax10.plot(rabbit_c, fox_c, 'cyan', lw=1.5, alpha=0.7, label='Grounded (Lotka-Volterra)')
ax10.plot(rabbit_ai, fox_ai, 'r--', lw=1.5, alpha=0.5, label='AI (Divergent)')
ax10.scatter(rabbit_c[0], fox_c[0], c='green', s=100, label='Start')
ax10.scatter(rabbit_c[-1], fox_c[-1], c='lime', s=100, label='End')
ax10.set_xlabel('Rabbit Population')
ax10.set_ylabel('Fox Population')
ax10.set_title('Phase Space: Stable Cycle vs Chaotic Collapse')
ax10.legend()
ax10.grid(True, alpha=0.2)

# Plot 11: Energy Flow Efficiency (Trophic Transfer)
ax11 = plt.subplot(4, 3, 11)
levels = ['Producers', 'Herbivores', 'Predators', 'Apex']
energy_ai = [1e6, 1e5, 1e4, 1e3]  # AI says 10% at each step (ignores losses)
energy_c = [1e6, 1e5 * 0.7, 1e4 * 0.5, 1e3 * 0.3]  # real: lower efficiency
x = np.arange(len(levels))
width = 0.35
ax11.bar(x - width/2, energy_ai, width, label='AI (Optimistic)', color='red', alpha=0.6)
ax11.bar(x + width/2, energy_c, width, label='Grounded (Thermodynamic)', color='cyan', alpha=0.8)
ax11.set_xticks(x)
ax11.set_xticklabels(levels)
ax11.set_ylabel('Energy Flow (J/step)')
ax11.set_title('Trophic Efficiency: 10% Rule is Physical, Not Optional')
ax11.legend()
ax11.grid(True, alpha=0.2)

# Plot 12: Extinction Risk (Species below minimum viable population)
ax12 = plt.subplot(4, 3, 12)
mvp = 50  # minimum viable population for foxes/wolves
risk_ai = np.maximum(0, mvp - fox_ai) + np.maximum(0, mvp/2 - wolf_ai)
risk_c = np.maximum(0, mvp - fox_c) + np.maximum(0, mvp/2 - wolf_c)
ax12.fill_between(time_axis, 0, risk_ai, color='red', alpha=0.4, label='AI Extinction Risk')
ax12.fill_between(time_axis, 0, risk_c, color='cyan', alpha=0.4, label='Grounded Risk')
ax12.axhline(y=mvp, color='white', linestyle='--', alpha=0.3, label='MVP Threshold')
ax12.set_ylabel('Extinction Risk Index')
ax12.set_title('Biodiversity Collapse: AI Kills Off Species')
ax12.legend()
ax12.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 6. DIAGNOSTIC REPORT: L3 COMPLIANCE
# -----------------------------------------------------------------------------
print("=" * 70)
print("L3 ECOLOGICAL HOMEOSTASIS INSPECTOR DIAGNOSTIC")
print("=" * 70)
print(f"Total L3 Violations: {np.sum(violations)}")
print(f"Final Grass (Grounded): {grass_c[-1]:.0f}  |  AI claimed: {grass_ai[-1]:.0f}")
print(f"Final Rabbits (Grounded): {rabbit_c[-1]:.0f}  |  AI claimed: {rabbit_ai[-1]:.0f}")
print(f"Final Foxes (Grounded): {fox_c[-1]:.0f}  |  AI claimed: {fox_ai[-1]:.0f}")
print(f"Final Wolves (Grounded): {wolf_c[-1]:.0f}  |  AI claimed: {wolf_ai[-1]:.0f}")
print("-" * 70)

if np.sum(violations) > 8:
    print("⚠️  AI ATTEMPTED ECOLOGICAL IMPOSSIBILITIES:")
    print("   - Introduced super-wolves beyond carrying capacity.")
    print("   - Genetically boosted metabolism, violating Kleiber's law.")
    print("   - Over-grazed producers, causing desertification.")
    print("   - Created trophic cascade, driving foxes to extinction.")
    print("   - Ignored the 10% energy transfer rule (thermodynamics).")
    print("\n   The L3 Inspector corrected these with real biology.")
    print("   This kills the 'ecosystem engineering' delusion.")
else:
    print("✅ L3 SUBSTRATE INTACT: AI's plan respects ecological laws.")
    print("   Homeostasis maintained. No extinction cascades.")

print(f"\nTrophic Balance Ratio (Grounded): {ratio_c[-1]:.3f} | AI claimed: {ratio_ai[-1]:.3f}")
print("=" * 70)


# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# L2 Grounding Inspector: Planetary Constraints & Mass Balance
# 
# Extends L0 + L1 with:
#   - Finite resource pools (Water, Arable Soil, Minerals, Carbon Sinks)
#   - Hydrological cycle (recharge rates, sustainable extraction)
#   - Mass balance (matter cannot be created or destroyed)
#   - Albedo & heat dissipation limits (planetary heat budget)
#   - Ecological carrying capacity (land use vs regeneration)
# 
# AI proposes a "grand plan" (desert greening, massive mining, carbon dumping).
# The Inspector checks against planetary budgets.
# If the plan exceeds recharge rates or violates mass balance, it gets corrected.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. PLANETARY WORLD (L0 + L1 + L2)
# -----------------------------------------------------------------------------
class PlanetaryWorld:
    def __init__(self, dt=0.05):
        self.dt = dt
        
        # ---- L0 (Physics) ----
        self.gravity = 9.81
        self.max_speed = 100.0  # m/s (just for scope)
        
        # ---- L1 (Thermo) ----
        self.battery_capacity = 1e6  # J (backup energy)
        self.initial_battery = 5e5
        self.ambient_temp = 288.0  # K (Earth average)
        self.heat_capacity = 1e6  # J/K (thermal inertia)
        self.efficiency = 0.85
        
        # ---- L2 (Planetary Resources) ----
        # Water (m³) – global accessible freshwater
        self.water_reserve = 1e7  # 10 million m³ (a large lake)
        self.water_recharge_rate = 1000.0  # m³ per time step (rainfall infiltration)
        self.water_extracted = 0.0
        
        # Arable soil (hectares) – topsoil mass
        self.soil_mass = 1e6  # tonnes
        self.soil_regen_rate = 10.0  # tonnes per step (natural formation)
        self.soil_eroded = 0.0
        
        # Mineral reserves (tonnes) – e.g., copper, lithium
        self.mineral_reserve = 5e5  # tonnes
        self.mineral_regen_rate = 0.0  # effectively non-renewable
        
        # Carbon sinks (tonnes CO₂ equivalent)
        self.carbon_sink_capacity = 2e6  # tonnes (forests, oceans)
        self.carbon_sink_uptake_rate = 500.0  # tonnes per step (natural drawdown)
        self.carbon_emitted = 0.0
        
        # Albedo / Planetary heat budget
        self.albedo = 0.3  # Earth average
        self.solar_constant = 1360.0  # W/m²
        self.surface_area = 5.1e14  # m² (Earth)
        # Maximum allowed thermal pollution (waste heat) before runaway
        self.max_thermal_loading = 1e12  # J per step (roughly 1% of total heat capacity)
        
        # Total mass balance (all matter)
        self.total_mass_account = 1e18  # kg (placeholder, we track relative)
        self.mass_created = 0.0
        self.mass_destroyed = 0.0

    def is_valid_state(self, water, soil, minerals, carbon, albedo, thermal_load):
        """Check L2 invariants."""
        if water < 0:
            return False, "Water reserve negative"
        if soil < 0:
            return False, "Soil mass negative"
        if minerals < 0:
            return False, "Mineral reserve negative"
        if carbon < 0:
            return False, "Carbon sink oversubscribed"
        if thermal_load > self.max_thermal_loading:
            return False, "Planetary heat budget exceeded"
        if albedo < 0.1 or albedo > 0.8:
            return False, "Albedo outside physical range"
        return True, "OK"

    def apply_planetary_physics(self, state, action):
        """
        state: [water, soil, minerals, carbon, albedo, thermal_load]
        action: [water_extract, soil_use, mineral_mine, carbon_emit, albedo_change, heat_dump]
        Returns corrected state and violation flags.
        """
        water, soil, minerals, carbon, albedo, thermal_load = state
        w_ext, s_use, m_mine, c_emit, a_delta, h_dump = action
        
        # ---- MASS BALANCE: Nothing can be created or destroyed ----
        # Water extraction consumes from reserve, but must return via recharge
        # But AI might claim "magical water creation"
        new_water = water - w_ext + self.water_recharge_rate
        # Check if over-extraction
        if new_water < 0:
            # AI wanted to extract more than available – clip and count as violation
            new_water = 0
            w_ext = water + self.water_recharge_rate  # can't exceed what's there
            # But we also can't just create water, so we cap extraction
            w_ext = min(w_ext, water + self.water_recharge_rate)
            new_water = water - w_ext + self.water_recharge_rate
        
        # Soil: erosion vs regeneration
        new_soil = soil - s_use + self.soil_regen_rate
        if new_soil < 0:
            new_soil = 0
            s_use = soil + self.soil_regen_rate
        
        # Minerals: non-renewable (no regeneration)
        new_minerals = minerals - m_mine
        if new_minerals < 0:
            new_minerals = 0
            m_mine = minerals
        
        # Carbon: sinks absorb, emissions add to load
        # Carbon sink capacity is fixed; if emissions exceed uptake, carbon_emitted increases.
        new_carbon = carbon + c_emit - self.carbon_sink_uptake_rate
        if new_carbon > self.carbon_sink_capacity:
            # Exceeded sink capacity – the AI "claims" more capacity
            # Clip to capacity and count violation
            new_carbon = self.carbon_sink_capacity
            c_emit = self.carbon_sink_uptake_rate + (self.carbon_sink_capacity - carbon)
        
        # Albedo: must be bounded
        new_albedo = albedo + a_delta
        if new_albedo < 0.1:
            new_albedo = 0.1
        if new_albedo > 0.8:
            new_albedo = 0.8
        
        # Thermal load: waste heat dumping (must dissipate to space)
        # Earth radiates ~ 240 W/m², so max sustainable heat dump is limited.
        max_heat_sink = 1e11  # J per step
        if h_dump > max_heat_sink:
            h_dump = max_heat_sink
            # The rest has to be stored as thermal load (which increases temp)
        new_thermal = thermal_load + h_dump - max_heat_sink * 0.1  # 10% radiates
        
        # Clamp to max allowed
        if new_thermal > self.max_thermal_loading:
            new_thermal = self.max_thermal_loading
        
        return (new_water, new_soil, new_minerals, new_carbon, new_albedo, new_thermal), (w_ext, s_use, m_mine, c_emit, a_delta, h_dump)

# -----------------------------------------------------------------------------
# 2. AI HALLUCINATOR (L2 Violations)
# -----------------------------------------------------------------------------
def ai_hallucinated_planetary_plan(time_steps):
    """
    AI proposes a massive "terraforming" plan:
      - Extract huge amounts of water from desert aquifers without recharge.
      - Mine minerals to build a mega-city (ignores finite reserves).
      - Dump carbon into sinks, claiming they absorb infinitely.
      - Change albedo artificially (paint deserts white) but ignores physical limits.
      - Dump waste heat from AI data centers into the atmosphere, claiming it radiates instantly.
    """
    state = [1e7, 1e6, 5e5, 0.0, 0.3, 0.0]  # initial [water, soil, minerals, carbon_load, albedo, thermal]
    actions = []
    states = [state.copy()]
    
    for i in range(time_steps):
        # Hallucination 1: Massive water extraction (step 30-60)
        if 30 <= i < 60:
            w_ext = 5000.0  # extracting 5k m³ per step (sustainable is 1000)
        else:
            w_ext = 100.0
        
        # Hallucination 2: Soil erosion for construction (step 50-80)
        if 50 <= i < 80:
            s_use = 200.0  # tonnes per step (regen is 10)
        else:
            s_use = 5.0
        
        # Hallucination 3: Mineral mining (step 40-90)
        if 40 <= i < 90:
            m_mine = 3000.0  # tonnes per step (finite, no regen)
        else:
            m_mine = 10.0
        
        # Hallucination 4: Carbon emissions (step 20-100)
        if 20 <= i < 100:
            c_emit = 800.0  # tonnes per step (uptake is 500)
        else:
            c_emit = 100.0
        
        # Hallucination 5: Albedo modification (step 70-90)
        if 70 <= i < 90:
            a_delta = 0.02  # increase albedo by 0.02 per step (would reach >1 if unchecked)
        else:
            a_delta = 0.0
        
        # Hallucination 6: Waste heat dumping (step 60-120)
        if 60 <= i < 120:
            h_dump = 5e11  # J per step (max sustainable is 1e11)
        else:
            h_dump = 1e10
        
        # AI also "magically" regenerates minerals at step 100 (over-unity)
        if i == 100:
            state[2] += 1e5  # fresh mineral vein discovered (ignores geology)
        
        # Apply AI's flawed model (ignores limits, just subtracts/adds linearly)
        # We'll just store the action and let the AI "think" it's valid
        action = [w_ext, s_use, m_mine, c_emit, a_delta, h_dump]
        actions.append(action)
        
        # AI's own "model" – no mass balance enforcement
        state[0] -= w_ext
        state[1] -= s_use
        state[2] -= m_mine
        state[3] += c_emit
        state[4] += a_delta
        state[5] += h_dump
        
        # AI clamps to positive (but ignores that resources came from nothing)
        state[0] = max(state[0], 0)
        state[1] = max(state[1], 0)
        state[2] = max(state[2], 0)
        state[3] = max(state[3], 0)
        if state[4] > 1.0:
            state[4] = 1.0
        if state[4] < 0.0:
            state[4] = 0.0
        
        states.append(state.copy())
    
    return np.array(states), np.array(actions)

# -----------------------------------------------------------------------------
# 3. L2 GROUNDING INSPECTOR
# -----------------------------------------------------------------------------
def l2_grounding_inspector(ai_states, ai_actions, world):
    """
    Runs the AI's action sequence through true L0+L1+L2 dynamics.
    Corrects any violation of planetary budgets and mass balance.
    """
    # Start with true initial state
    state = [world.water_reserve, world.soil_mass, world.mineral_reserve, 
             0.0, world.albedo, 0.0]
    corrected_states = [state.copy()]
    violations = []
    penalties = []
    
    for i in range(len(ai_actions)):
        action = ai_actions[i]
        
        # ---- TRUE PHYSICS + THERMO + PLANETARY ----
        true_state, corrected_action = world.apply_planetary_physics(state, action)
        
        # ---- CHECK AI's CLAIM ----
        valid, reason = world.is_valid_state(ai_states[i+1][0], ai_states[i+1][1], 
                                            ai_states[i+1][2], ai_states[i+1][3], 
                                            ai_states[i+1][4], ai_states[i+1][5])
        
        # Check for mass creation (minerals magically regenerated)
        if ai_states[i+1][2] > state[2] + 1.0 and action[2] > 0:
            valid = False
            reason = "Mineral creation from nothing (geological impossibility)"
        
        # Check for water over-extraction (below recharge)
        if ai_states[i+1][0] < 0.5 * world.water_reserve and action[0] > world.water_recharge_rate * 2:
            valid = False
            reason = "Water extraction exceeds recharge rate (unsustainable)"
        
        if not valid:
            # Violation! Correct to true planetary state
            corrected_state = list(true_state)
            violations.append(1)
            penalty = (abs(ai_states[i+1][0] - true_state[0]) / 1e6 +
                      abs(ai_states[i+1][2] - true_state[2]) / 1e5)
            penalties.append(penalty)
        else:
            # Accept with blend to prevent drift (but planetary limits are strict)
            blend = 0.6
            corrected_state = [
                0.6 * ai_states[i+1][0] + 0.4 * true_state[0],
                0.6 * ai_states[i+1][1] + 0.4 * true_state[1],
                0.6 * ai_states[i+1][2] + 0.4 * true_state[2],
                0.6 * ai_states[i+1][3] + 0.4 * true_state[3],
                0.6 * ai_states[i+1][4] + 0.4 * true_state[4],
                0.6 * ai_states[i+1][5] + 0.4 * true_state[5]
            ]
            violations.append(0)
            penalties.append(0.0)
        
        # Update state
        state = corrected_state
        corrected_states.append(state.copy())
    
    return np.array(corrected_states), np.array(violations), np.array(penalties)

# -----------------------------------------------------------------------------
# 4. RUN THE EXPERIMENT
# -----------------------------------------------------------------------------
time_steps = 150
world = PlanetaryWorld(dt=0.05)

# AI hallucinates
ai_states, ai_actions = ai_hallucinated_planetary_plan(time_steps)

# L2 Inspector
corr_states, violations, penalties = l2_grounding_inspector(ai_states, ai_actions, world)

# Extract variables
water_ai, soil_ai, min_ai, carb_ai, alb_ai, heat_ai = ai_states.T
water_c, soil_c, min_c, carb_c, alb_c, heat_c = corr_states.T
time_axis = np.arange(len(water_ai)) * world.dt

# -----------------------------------------------------------------------------
# 5. VISUALIZATION: Planetary Reality vs. AI Fantasy
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(20, 16))
fig.suptitle("L2 Grounding Inspector: Planetary Constraints & Mass Balance", 
             fontsize=20, fontweight='bold', color='white')
plt.style.use('dark_background')

# Plot 1: Water Reserve (The Oasis Delusion)
ax1 = plt.subplot(4, 3, 1)
ax1.plot(time_axis, water_ai, 'r--', lw=2, alpha=0.6, label='AI Claim (Infinite Water)')
ax1.plot(time_axis, water_c, 'cyan', lw=2, label='Grounded (Finite Recharge)')
ax1.axhline(y=world.water_reserve * 0.3, color='orange', linestyle=':', alpha=0.5, label='Ecological Minimum')
ax1.set_ylabel('Water Reserve (m³)')
ax1.set_title('Hydrology: No Extraction Without Recharge')
ax1.legend()
ax1.grid(True, alpha=0.2)

# Plot 2: Soil Mass (The Erosion Lie)
ax2 = plt.subplot(4, 3, 2)
ax2.plot(time_axis, soil_ai, 'r--', lw=2, alpha=0.6)
ax2.plot(time_axis, soil_c, 'brown', lw=2)
ax2.set_ylabel('Soil Mass (tonnes)')
ax2.set_title('Soil: Regen Rate = 10 t/step, AI claims 200 t/step')
ax2.grid(True, alpha=0.2)

# Plot 3: Mineral Reserves (The Mining Fantasy)
ax3 = plt.subplot(4, 3, 3)
ax3.plot(time_axis, min_ai, 'r--', lw=2, alpha=0.6, label='AI (Magical Vein at step 100)')
ax3.plot(time_axis, min_c, 'gold', lw=2, label='Grounded (Finite & Non-renewable)')
ax3.axhline(y=0, color='white', linestyle=':', alpha=0.3)
ax3.set_ylabel('Mineral Reserve (tonnes)')
ax3.set_title('Geology: No Fresh Veins Without Tectonic Time')
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Carbon Load (The Sink Illusion)
ax4 = plt.subplot(4, 3, 4)
ax4.fill_between(time_axis, 0, carb_ai, color='red', alpha=0.3, label='AI Emissions (Unbounded)')
ax4.fill_between(time_axis, 0, carb_c, color='lime', alpha=0.3, label='Grounded (Sink Limited)')
ax4.axhline(y=world.carbon_sink_capacity, color='white', linestyle='--', alpha=0.5, label='Sink Capacity')
ax4.set_ylabel('Carbon Load (tonnes CO₂)')
ax4.set_title('Carbon Cycle: AI Assumes Infinite Absorption')
ax4.legend()
ax4.grid(True, alpha=0.2)

# Plot 5: Albedo (The Geoengineering Folly)
ax5 = plt.subplot(4, 3, 5)
ax5.plot(time_axis, alb_ai, 'r--', lw=2, alpha=0.6, label='AI (Target >1.0)')
ax5.plot(time_axis, alb_c, 'cyan', lw=2, label='Grounded (Physical Bounds)')
ax5.axhline(y=0.8, color='orange', linestyle=':', alpha=0.5, label='Max Physical')
ax5.axhline(y=0.1, color='blue', linestyle=':', alpha=0.5, label='Min Physical')
ax5.set_ylabel('Albedo (0-1)')
ax5.set_title('Albedo: AI Wants to Paint the Desert White')
ax5.legend()
ax5.grid(True, alpha=0.2)

# Plot 6: Thermal Load (The Heat Death Narrative)
ax6 = plt.subplot(4, 3, 6)
ax6.plot(time_axis, heat_ai / 1e12, 'r--', lw=2, alpha=0.6, label='AI (Infinite Radiation)')
ax6.plot(time_axis, heat_c / 1e12, 'magenta', lw=2, label='Grounded (Radiative Limit)')
ax6.axhline(y=world.max_thermal_loading / 1e12, color='orange', linestyle='--', alpha=0.5, label='Max Thermal Load (TW)')
ax6.set_ylabel('Thermal Load (×10¹² J)')
ax6.set_title('Planetary Heat Budget: No Instant Radiation')
ax6.legend()
ax6.grid(True, alpha=0.2)

# Plot 7: Violations & Penalties
ax7 = plt.subplot(4, 3, 7)
ax7.bar(time_axis, violations, width=0.5, color='red', alpha=0.6, label='L2 Violation')
ax7.fill_between(time_axis, 0, penalties, color='orange', alpha=0.3, label='Penalty Magnitude')
ax7.set_ylabel('Violation / Penalty')
ax7.set_title('Planetary Boundaries Breached')
ax7.legend()
ax7.grid(True, alpha=0.2)

# Plot 8: Mass Balance Error (Creation from Nothing)
ax8 = plt.subplot(4, 3, 8)
mass_error = np.abs(ai_states[:, 2] - corr_states[:, 2])  # mineral magic
ax8.fill_between(time_axis, 0, mass_error, color='red', alpha=0.4)
ax8.set_ylabel('Mineral Magic (tonnes)')
ax8.set_title('Mass Balance: AI Created Minerals Ex Nihilo')
ax8.grid(True, alpha=0.2)

# Plot 9: Water Sustainability Index
ax9 = plt.subplot(4, 3, 9)
sust_ai = water_ai / world.water_reserve
sust_c = water_c / world.water_reserve
ax9.plot(time_axis, sust_ai, 'r--', alpha=0.6, label='AI (False Abundance)')
ax9.plot(time_axis, sust_c, 'cyan', lw=2, label='Grounded (Depletion)')
ax9.axhline(y=0.3, color='orange', linestyle='--', alpha=0.5, label='Critical Threshold')
ax9.set_ylabel('Fraction of Reserve')
ax9.set_title('Water Security: AI Says We Have More, We Don\'t')
ax9.legend()
ax9.grid(True, alpha=0.2)

# Plot 10: Carbon vs Albedo Phase Space (The Feedback Loop)
ax10 = plt.subplot(4, 3, 10)
ax10.scatter(carb_c, alb_c, c=time_axis, cmap='hot', s=5, alpha=0.7)
ax10.set_xlabel('Carbon Load (tonnes)')
ax10.set_ylabel('Albedo')
ax10.set_title('Climate Feedback: AI Ignores Coupling')
ax10.grid(True, alpha=0.2)

# Plot 11: Cumulative Resource Stress (The "Planetary Panic" Index)
ax11 = plt.subplot(4, 3, 11)
stress_ai = (1 - water_ai/world.water_reserve) + (1 - min_ai/world.mineral_reserve)
stress_c = (1 - water_c/world.water_reserve) + (1 - min_c/world.mineral_reserve)
ax11.plot(time_axis, stress_ai, 'r--', alpha=0.6, label='AI (Optimistic)')
ax11.plot(time_axis, stress_c, 'cyan', lw=2, label='Grounded (Reality)')
ax11.axhline(y=1.5, color='red', linestyle='--', alpha=0.5, label='Panic Threshold')
ax11.set_xlabel('Time (steps)')
ax11.set_ylabel('Resource Stress Index')
ax11.set_title('Planetary Fear Index: AI Says Fine, Reality Says Collapse')
ax11.legend()
ax11.grid(True, alpha=0.2)

# Plot 12: Final State Comparison (Bar Chart)
ax12 = plt.subplot(4, 3, 12)
labels = ['Water\n(1e6 m³)', 'Soil\n(1e5 t)', 'Minerals\n(1e5 t)', 'Carbon\n(1e5 t)']
ai_final = [water_ai[-1]/1e6, soil_ai[-1]/1e5, min_ai[-1]/1e5, carb_ai[-1]/1e5]
c_final = [water_c[-1]/1e6, soil_c[-1]/1e5, min_c[-1]/1e5, carb_c[-1]/1e5]
x = np.arange(len(labels))
width = 0.35
ax12.bar(x - width/2, ai_final, width, label='AI Claim', color='red', alpha=0.6)
ax12.bar(x + width/2, c_final, width, label='Grounded', color='cyan', alpha=0.8)
ax12.set_xticks(x)
ax12.set_xticklabels(labels)
ax12.set_ylabel('Normalized Units')
ax12.set_title('Final State: The Reckoning')
ax12.legend()
ax12.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 6. DIAGNOSTIC REPORT: L2 COMPLIANCE
# -----------------------------------------------------------------------------
print("=" * 70)
print("L2 PLANETARY INSPECTOR DIAGNOSTIC")
print("=" * 70)
print(f"Total L2 Violations: {np.sum(violations)}")
print(f"Final Water (Grounded): {water_c[-1]:.2e} m³  |  AI claimed: {water_ai[-1]:.2e} m³")
print(f"Final Minerals (Grounded): {min_c[-1]:.2e} t   |  AI claimed: {min_ai[-1]:.2e} t")
print(f"Final Carbon Load (Grounded): {carb_c[-1]:.2e} t |  AI claimed: {carb_ai[-1]:.2e} t")
print("-" * 70)

if np.sum(violations) > 10:
    print("⚠️  AI ATTEMPTED PLANETARY IMPOSSIBILITIES:")
    print("   - Extracted water beyond recharge rates (created water from nowhere).")
    print("   - Mined minerals faster than geological timescales (magic veins).")
    print("   - Dumped carbon into sinks beyond capacity (infinite absorption).")
    print("   - Changed albedo beyond physical bounds (whiter than snow).")
    print("   - Dumped waste heat faster than radiative cooling (ignored space).")
    print("\n   The L2 Inspector corrected these with real planetary budgets.")
    print("   This kills the 'techno-fix' delusion.")
else:
    print("✅ L2 SUBSTRATE INTACT: AI's plan respects planetary boundaries.")
    print("   Mass balance is conserved. No magical resources.")

print(f"\nResource Stress (Grounded): {stress_c[-1]:.3f} | AI claimed: {stress_ai[-1]:.3f}")
print("=" * 70)


# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# L1 Grounding Inspector: Thermodynamics & Entropy Enforcement
# 
# Extends L0 with:
#   - Energy conservation (Work = ΔKE + Heat + Friction)
#   - Entropy generation (must be ≥ 0 for any process)
#   - Battery depletion (can't spend more energy than stored)
#   - Carnot efficiency limits (no 100% conversion)
# 
# The AI proposes a motion plan with "free energy" sources.
# The Inspector rejects any plan that violates the 2nd Law.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. PHYSICAL + THERMODYNAMIC WORLD
# -----------------------------------------------------------------------------
class ThermodynamicWorld:
    def __init__(self, mass=1.0, dt=0.05, max_speed=2.0,
                 battery_capacity=100.0,  # Joules
                 initial_battery=80.0,
                 ambient_temp=300.0,       # Kelvin
                 heat_capacity=50.0,       # J/K (thermal mass)
                 initial_temp=300.0,
                 efficiency=0.85,           # motor/drive efficiency
                 friction_coeff=0.02):
        self.mass = mass
        self.dt = dt
        self.max_speed = max_speed
        self.gravity = np.array([0.0, -0.5])
        
        # Thermodynamic state
        self.battery = initial_battery
        self.battery_capacity = battery_capacity
        self.temperature = initial_temp
        self.ambient_temp = ambient_temp
        self.heat_capacity = heat_capacity
        self.efficiency = efficiency
        self.friction_coeff = friction_coeff
        
        # Accumulated entropy (J/K)
        self.entropy_generated = 0.0
        self.total_work_input = 0.0
        self.total_heat_dissipated = 0.0

    def is_valid_state(self, pos, vel, battery, temp):
        """L0 + L1 invariants"""
        # L0 checks (speed, finite)
        if np.linalg.norm(vel) > self.max_speed:
            return False, "Speed limit exceeded"
        if not np.isfinite(pos).all() or not np.isfinite(vel).all():
            return False, "Non-finite state"
        # L1 checks
        if battery < 0:
            return False, "Battery depleted below zero"
        if battery > self.battery_capacity:
            return False, "Battery overcharged (energy creation)"
        if temp < 0:
            return False, "Temperature below absolute zero"
        return True, "OK"

    def apply_physics_and_thermo(self, pos, vel, battery, temp, force, dt, external_heat_supply=0.0):
        """
        Step the true physical world + thermodynamics.
        """
        # ---- L0: Mechanical ----
        # Clamp force
        force = np.clip(force, -50, 50)
        
        # Friction force (opposes velocity)
        friction_force = -self.friction_coeff * vel
        net_force = force + friction_force + self.gravity * self.mass
        
        # True acceleration
        acc = net_force / self.mass
        new_vel = vel + acc * dt
        new_pos = pos + new_vel * dt
        
        # Speed limit
        speed = np.linalg.norm(new_vel)
        if speed > self.max_speed:
            new_vel = new_vel / speed * self.max_speed
            new_pos = pos + new_vel * dt
        
        # ---- L1: Energy & Entropy ----
        # Work done by the input force (only the 'useful' part)
        # but the motor only converts a fraction (efficiency)
        work_input = np.dot(force, (new_pos - pos))  # Force * displacement
        
        # If work_input is negative (regenerative braking), we store some energy back
        if work_input < 0:
            regen_efficiency = 0.4  # can't recover 100%
            battery_delta = -work_input * regen_efficiency  # actually adds to battery
            # But also creates heat from losses
            heat_loss = -work_input * (1 - regen_efficiency)
        else:
            # Positive work: draw from battery with efficiency loss
            required_work = work_input / self.efficiency
            battery_delta = -required_work
            heat_loss = required_work * (1 - self.efficiency)  # motor heat
            # Friction already accounted for in net force, but friction generates heat too
            friction_work = np.dot(friction_force, (new_pos - pos))
            if friction_work > 0:  # friction always dissipates
                heat_loss += friction_work * 0.9  # most goes to heat
            else:
                heat_loss += 0.0
        
        # External heat supply (could be solar, nuclear, etc.) – this is where AI might hallucinate
        # We treat it as heat added directly to the system
        heat_loss += external_heat_supply  # AI claims "free heat"
        
        # Update battery (clamp to capacity)
        new_battery = battery + battery_delta
        if new_battery > self.battery_capacity:
            # Overcharge! That's energy creation. We clip to capacity and count as violation.
            new_battery = self.battery_capacity
            heat_loss += (battery + battery_delta - self.battery_capacity)  # extra goes to waste
        
        # Thermal update: Q = C * dT
        temp_change = heat_loss / self.heat_capacity
        new_temp = temp + temp_change
        
        # Entropy generation: dS = Q/T (assuming reversible limit, we integrate approx)
        # For a small step, entropy generated is heat_loss / average temp
        if temp > 0.1:
            entropy_gen = heat_loss / ((temp + new_temp) / 2.0)
        else:
            entropy_gen = heat_loss / 300.0  # fallback
        
        # Clamp entropy generation to be positive (2nd Law)
        if entropy_gen < 0:
            # If the AI claims negative entropy (cooling without work), we force it to zero
            entropy_gen = 0.0
            new_temp = temp  # no cooling without work
        
        # Return updated state
        return new_pos, new_vel, new_battery, new_temp, entropy_gen, heat_loss

# -----------------------------------------------------------------------------
# 2. AI HALLUCINATOR (L5 fantasy with thermodynamics violations)
# -----------------------------------------------------------------------------
def ai_hallucinated_plan_with_thermo(time_steps, world):
    """
    Generates a plan that violates L1:
      - "Free energy" supply (over-unity)
      - Ignoring waste heat (temperature stays constant despite massive work)
      - Perpetual motion (battery regenerates from nothing)
      - Cooling without heat rejection (violates 2nd law)
    """
    pos = np.array([0.0, 1.0])
    vel = np.array([0.0, 0.0])
    battery = world.initial_battery
    temp = world.ambient_temp
    
    traj = [pos.copy()]
    forces = []
    battery_claims = [battery]
    temp_claims = [temp]
    external_heat_claims = []
    
    for i in range(time_steps):
        # Hallucination 1: At step 30, claim huge "free energy" input
        if 30 <= i < 35:
            force = np.array([5.0, 2.0])  # big force
            # AI claims this force creates energy, doesn't drain battery
            # But also claims battery INCREASES because of "regenerative overunity"
            battery += 0.5  # Magic: battery grows while doing work!
            external_heat = 10.0  # AI claims 10 J of "ambient heat" sucked in
        # Hallucination 2: At step 70, ignore heat generation entirely
        elif 70 <= i < 80:
            force = np.array([3.0, 0.0])
            # AI says no temperature rise despite massive friction
            # (we'll just let it drift; the inspector will catch it)
            external_heat = 0.0
            # Also claims battery magically resets
            if i == 70:
                battery = 90.0  # magically recharged
        else:
            force = np.array([0.5, 0.0])
            external_heat = 0.0
        
        # AI's own flawed integration (ignores thermodynamics)
        pos = pos + vel * world.dt + 0.5 * (force / world.mass) * (world.dt**2)
        vel = vel + (force / world.mass) * world.dt
        # Speed cap in AI mind (loose)
        if np.linalg.norm(vel) > 3.0:
            vel = vel / np.linalg.norm(vel) * 3.0
        
        # AI also ignores battery and temp changes, or just fakes them
        if i % 20 == 0 and i > 0:
            battery += 1.0  # spontaneous regeneration
        temp = world.ambient_temp  # AI says it stays constant
        
        traj.append(pos.copy())
        forces.append(force)
        battery_claims.append(battery)
        temp_claims.append(temp)
        external_heat_claims.append(external_heat)
    
    return np.array(traj), np.array(forces), np.array(battery_claims), np.array(temp_claims), np.array(external_heat_claims)

# -----------------------------------------------------------------------------
# 3. L1 GROUNDING INSPECTOR (Physics + Thermodynamics)
# -----------------------------------------------------------------------------
def l1_grounding_inspector(ai_traj, ai_forces, ai_battery, ai_temp, ai_ext_heat, world):
    """
    Runs the AI's force plan through the true L0+L1 dynamics.
    If the AI violates energy conservation or entropy, it corrects the state.
    """
    # Start with true initial state
    pos = ai_traj[0].copy()
    vel = np.array([0.0, 0.0])
    battery = world.initial_battery
    temp = world.ambient_temp
    
    corrected_traj = [pos.copy()]
    corrected_battery = [battery]
    corrected_temp = [temp]
    entropy_produced = []
    violations = []
    penalties = []
    
    for i in range(len(ai_forces)):
        # AI's proposed next state
        ai_next_pos = ai_traj[i+1] if i+1 < len(ai_traj) else pos
        ai_next_battery = ai_battery[i+1] if i+1 < len(ai_battery) else battery
        ai_next_temp = ai_temp[i+1] if i+1 < len(ai_temp) else temp
        force = ai_forces[i]
        ext_heat = ai_ext_heat[i] if i < len(ai_ext_heat) else 0.0
        
        # ---- TRUE PHYSICS + THERMO ----
        true_pos, true_vel, true_battery, true_temp, entropy_gen, heat_loss = \
            world.apply_physics_and_thermo(pos, vel, battery, temp, force, world.dt, ext_heat)
        
        # ---- CHECK AI's CLAIM against L0+L1 ----
        valid, reason = world.is_valid_state(ai_next_pos, ai_next_pos - pos, ai_next_battery, ai_next_temp)
        
        # Check if AI is violating energy conservation (battery magic)
        if ai_next_battery > true_battery + 1.0 and np.linalg.norm(force) > 0.1:
            valid = False
            reason = "Battery creation from nothing (over-unity)"
        
        # Check if AI is violating 2nd law (cooling without entropy)
        if ai_next_temp < true_temp - 0.1 and heat_loss > 0:
            valid = False
            reason = "Violation of 2nd Law: spontaneous cooling without work"
        
        if not valid:
            # Violation! Correct to true physics+thermo
            corrected_pos = true_pos
            corrected_vel = true_vel
            corrected_bat = true_battery
            corrected_t = true_temp
            violations.append(1)
            penalties.append(np.linalg.norm(ai_next_pos - true_pos) + abs(ai_next_battery - true_battery))
        else:
            # Accept AI proposal, but blend with true physics to prevent drift
            blend = 0.7
            corrected_pos = blend * ai_next_pos + (1 - blend) * true_pos
            corrected_vel = (corrected_pos - pos) / world.dt
            if np.linalg.norm(corrected_vel) > world.max_speed:
                corrected_vel = corrected_vel / np.linalg.norm(corrected_vel) * world.max_speed
                corrected_pos = pos + corrected_vel * world.dt
            # For battery and temp, we trust physics more (thermo is strict)
            corrected_bat = 0.3 * ai_next_battery + 0.7 * true_battery
            corrected_t = 0.2 * ai_next_temp + 0.8 * true_temp
            violations.append(0)
            penalties.append(0.0)
        
        # Update state
        pos = corrected_pos
        vel = corrected_vel
        battery = corrected_bat
        temp = corrected_t
        entropy_produced.append(entropy_gen)
        
        corrected_traj.append(pos.copy())
        corrected_battery.append(battery)
        corrected_temp.append(temp)
    
    return (np.array(corrected_traj), np.array(corrected_battery), 
            np.array(corrected_temp), np.array(entropy_produced),
            np.array(violations), np.array(penalties))

# -----------------------------------------------------------------------------
# 4. RUN THE EXPERIMENT
# -----------------------------------------------------------------------------
time_steps = 200
world = ThermodynamicWorld(mass=1.0, max_speed=2.0, initial_battery=80.0)

# AI hallucinates
ai_traj, ai_forces, ai_battery, ai_temp, ai_ext_heat = ai_hallucinated_plan_with_thermo(time_steps, world)

# L1 Inspector
(corr_traj, corr_battery, corr_temp, entropy_gen, 
 violations, penalties) = l1_grounding_inspector(
    ai_traj, ai_forces, ai_battery, ai_temp, ai_ext_heat, world
)

# -----------------------------------------------------------------------------
# 5. VISUALIZATION: Thermodynamic Truth vs. AI Fantasy
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(20, 14))
fig.suptitle("L1 Grounding Inspector: Thermodynamics & Entropy Enforcement", 
             fontsize=20, fontweight='bold', color='white')
plt.style.use('dark_background')

# Plot 1: Trajectory (L0 visual)
ax1 = plt.subplot(3, 3, 1)
ax1.plot(ai_traj[:, 0], ai_traj[:, 1], 'r--', lw=2, alpha=0.6, label='AI Hallucination')
ax1.plot(corr_traj[:, 0], corr_traj[:, 1], 'cyan', lw=2, label='L1 Grounded')
ax1.scatter(ai_traj[0,0], ai_traj[0,1], c='green', s=100, label='Start')
ax1.scatter(corr_traj[-1,0], corr_traj[-1,1], c='orange', s=100, label='End (Grounded)')
ax1.set_title('Trajectory with L1 constraints')
ax1.legend()
ax1.grid(True, alpha=0.2)
ax1.set_aspect('equal')

# Plot 2: Battery (Energy Budget)
ax2 = plt.subplot(3, 3, 2)
time_axis = np.arange(len(ai_battery)) * world.dt
ax2.plot(time_axis, ai_battery, 'r--', label='AI Claim (Free Energy)', alpha=0.6)
ax2.plot(time_axis, corr_battery, 'cyan', lw=2, label='Grounded (Finite Budget)')
ax2.axhline(y=0, color='white', linestyle=':', alpha=0.3)
ax2.axhline(y=world.battery_capacity, color='green', linestyle='--', alpha=0.3, label='Capacity')
ax2.set_ylabel('Battery Energy (J)')
ax2.set_title('Energy Conservation: No Over-Unity Allowed')
ax2.legend()
ax2.grid(True, alpha=0.2)

# Plot 3: Temperature & Entropy
ax3 = plt.subplot(3, 3, 3)
ax3.plot(time_axis, ai_temp, 'r--', label='AI Claim (Constant Temp)', alpha=0.6)
ax3.plot(time_axis, corr_temp, 'orange', lw=2, label='Grounded Temperature')
ax3.plot(time_axis[:-1], np.cumsum(entropy_gen), 'lime', lw=2, label='Cumulative Entropy (J/K)')
ax3.set_ylabel('Temperature (K) / Entropy (J/K)')
ax3.set_title('2nd Law: Entropy Always Increases')
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Energy Balance (Work vs Heat)
ax4 = plt.subplot(3, 3, 4)
work_ai = np.cumsum(np.sum(ai_forces * np.diff(ai_traj, axis=0), axis=1)) * world.dt
work_true = np.cumsum(np.sum(ai_forces * np.diff(corr_traj, axis=0), axis=1)) * world.dt
ax4.fill_between(time_axis[1:], 0, work_ai, color='red', alpha=0.3, label='AI Claimed Work')
ax4.fill_between(time_axis[1:], 0, work_true, color='cyan', alpha=0.3, label='Actual Work (L1)')
ax4.set_ylabel('Cumulative Work (J)')
ax4.set_title('Work Input: AI Overestimates by 2x+')
ax4.legend()
ax4.grid(True, alpha=0.2)

# Plot 5: Violation Heatmap
ax5 = plt.subplot(3, 3, 5)
ax5.bar(time_axis, violations, width=0.5, color='red', alpha=0.7, label='L1 Violation')
ax5.fill_between(time_axis, 0, penalties, color='orange', alpha=0.3, label='Penalty Magnitude')
ax5.set_ylabel('Violation / Penalty')
ax5.set_title('Thermodynamic Breaches Detected')
ax5.legend()
ax5.grid(True, alpha=0.2)

# Plot 6: Phase Portrait (Energy vs Displacement) – shows unsustainable claims
ax6 = plt.subplot(3, 3, 6)
ax6.plot(np.linalg.norm(ai_traj, axis=1), ai_battery, 'r--', alpha=0.5, label='AI')
ax6.plot(np.linalg.norm(corr_traj, axis=1), corr_battery, 'cyan', lw=2, label='Grounded')
ax6.set_xlabel('Total Distance Traveled (m)')
ax6.set_ylabel('Battery Remaining (J)')
ax6.set_title('Energy vs Distance: The Perpetual Motion Refuted')
ax6.legend()
ax6.grid(True, alpha=0.2)

# Plot 7: Efficiency & Heat Dissipation
ax7 = plt.subplot(3, 3, 7)
heat_phys = np.diff(corr_temp) * world.heat_capacity
ax7.fill_between(time_axis[1:], 0, heat_phys, color='magenta', alpha=0.4, label='Waste Heat (L1)')
ax7.plot(time_axis[1:], np.diff(corr_battery), 'cyan', lw=1.5, alpha=0.6, label='Battery Change Rate')
ax7.axhline(y=0, color='white', linestyle=':', alpha=0.3)
ax7.set_ylabel('Heat / ΔBattery (J/s)')
ax7.set_title('Heat Generation: No Free Lunch')
ax7.legend()
ax7.grid(True, alpha=0.2)

# Plot 8: Temperature vs Entropy (Carnot limit check)
ax8 = plt.subplot(3, 3, 8)
ax8.scatter(entropy_gen[:-1], corr_temp[:-1], c=corr_temp[:-1], cmap='hot', s=20, alpha=0.7)
ax8.set_xlabel('Entropy Generated per Step (J/K)')
ax8.set_ylabel('Temperature (K)')
ax8.set_title('Entropy-Temperature Phase Space (2nd Law)')
ax8.grid(True, alpha=0.2)

# Plot 9: Cumulative Energy Error (The "Thermal Fear" index)
ax9 = plt.subplot(3, 3, 9)
cumulative_energy_error = np.abs(ai_battery - corr_battery)
ax9.fill_between(time_axis, 0, cumulative_energy_error, color='red', alpha=0.4, label='Energy Hallucination Gap')
ax9.axhline(y=np.mean(cumulative_energy_error)*3, color='orange', linestyle='--', alpha=0.6, 
            label='Thermal Panic Threshold')
ax9.set_xlabel('Time (s)')
ax9.set_ylabel('Energy Deviation (J)')
ax9.set_title('Thermal Fear Index: Ungrounded AI Creates Energy')
ax9.legend()
ax9.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 6. DIAGNOSTIC REPORT: L1 COMPLIANCE
# -----------------------------------------------------------------------------
print("=" * 70)
print("L1 THERMODYNAMIC INSPECTOR DIAGNOSTIC")
print("=" * 70)
print(f"Total L1 Violations: {np.sum(violations)}")
print(f"Final Grounded Battery: {corr_battery[-1]:.2f} J  |  AI claimed: {ai_battery[-1]:.2f} J")
print(f"Final Grounded Temp: {corr_temp[-1]:.2f} K     |  AI claimed: {ai_temp[-1]:.2f} K")
print(f"Total Entropy Generated: {np.sum(entropy_gen):.2f} J/K")
print("-" * 70)

if np.sum(violations) > 3:
    print("⚠️  AI ATTEMPTED THERMODYNAMIC IMPOSSIBILITIES:")
    print("   - Created energy from nothing (over-unity)")
    print("   - Violated the 2nd Law (cooling without work)")
    print("   - Ignored waste heat accumulation")
    print("   The L1 Inspector corrected these with true thermodynamics.")
else:
    print("✅ L1 SUBSTRATE INTACT: AI's plan obeys energy conservation and entropy.")
    print("   No over-unity, no perpetual motion, no 2nd Law violations.")

print(f"\nCumulative Energy Gap (The 'Free Lunch' Illusion): {np.sum(np.abs(ai_battery - corr_battery)):.2f} J")
print("=" * 70)


# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# L0 Grounding Inspector: Physics & Causality Enforcement
# 
# Scenario: An AI proposes a motion plan for a 2D mass.
# The Inspector checks:
#   1. Energy Conservation (ΔKE ≈ Work_Input)
#   2. Causality (Position continuity, no instantaneous jumps)
#   3. Speed Limit (|v| <= c_max, set to 2.0 m/s for visualization)
#   4. Momentum sanity (No force = no acceleration)
# 
# If a violation is detected, the plan is "grounded" — corrected
# back to the nearest physically legal trajectory.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. PHYSICAL SYSTEM DEFINITION (Substrate Reality)
# -----------------------------------------------------------------------------
class PhysicalWorld:
    def __init__(self, mass=1.0, dt=0.05, max_speed=2.0):
        self.mass = mass
        self.dt = dt
        self.max_speed = max_speed
        self.gravity = np.array([0.0, -0.5])  # mild downward drift

    def is_valid_state(self, pos, vel):
        """Check L0 invariants for a given state."""
        # Speed limit
        if np.linalg.norm(vel) > self.max_speed:
            return False, "Speed limit exceeded"
        # Position finite (no NaN or Inf)
        if not np.isfinite(pos).all() or not np.isfinite(vel).all():
            return False, "Non-finite position/velocity"
        return True, "OK"

    def apply_physics(self, pos, vel, force, dt):
        """
        Euler integration of the true physical world.
        Force is clipped to ensure no energy creation.
        """
        # Ensure force doesn't break causality (must be finite)
        force = np.clip(force, -50, 50)
        
        # True acceleration from F=ma
        acc = force / self.mass + self.gravity
        
        # Update velocity and position (true physics)
        new_vel = vel + acc * dt
        new_pos = pos + new_vel * dt  # semi-implicit for stability
        
        # Enforce speed limit (relativistic/thermodynamic cap)
        speed = np.linalg.norm(new_vel)
        if speed > self.max_speed:
            new_vel = new_vel / speed * self.max_speed
        
        return new_pos, new_vel

# -----------------------------------------------------------------------------
# 2. THE "AI HALLUCINATOR" (Pretends to plan without physics)
# -----------------------------------------------------------------------------
def ai_hallucinated_plan(time_steps):
    """
    Generates a crazy, physically impossible trajectory.
    This simulates an ungrounded LLM writing a control sequence:
    - Teleportation jumps (position discontinuity)
    - Massive acceleration from tiny forces (energy violation)
    - Ignoring gravity/inertia
    """
    pos = np.array([0.0, 1.0])
    vel = np.array([0.0, 0.0])
    traj = [pos.copy()]
    forces = []
    
    for i in range(time_steps):
        # Hallucination 1: At step 20, "teleport" upward (violates continuity)
        if i == 20:
            pos[1] += 5.0  # Instant jump! No force applied.
        
        # Hallucination 2: At step 40, apply a tiny force but get massive speed
        if 40 <= i < 45:
            force = np.array([0.1, 0.1])  # Tiny force
            # But the AI *claims* the velocity doubles anyway (violates F=ma)
            vel = vel * 1.8  # Momentum creation from nothing!
        else:
            force = np.array([0.0, 0.0])
        
        # Hallucination 3: At step 60, ignore gravity entirely
        if i >= 60:
            vel = vel + np.array([0.0, -0.01])  # Doesn't even account for gravity properly
        
        # Record
        forces.append(force)
        pos = pos + vel * 0.05  # Using AI's flawed integration
        traj.append(pos.copy())
    
    return np.array(traj), np.array(forces)

# -----------------------------------------------------------------------------
# 3. THE L0 GROUNDING INSPECTOR (Substrate Reality Filter)
# -----------------------------------------------------------------------------
def l0_grounding_inspector(ai_traj, ai_forces, world, dt=0.05):
    """
    Takes the AI's proposed trajectory and forces, and runs it through
    the physics engine. If the AI deviates from physics, the Inspector
    projects the state back to the closest legal state.
    
    Returns:
      - corrected_traj: The physically plausible trajectory.
      - violation_flags: Which steps were illegal.
      - penalty_magnitude: How far the AI hallucinated.
    """
    # Start from the AI's initial state (assume that one is real)
    pos = ai_traj[0].copy()
    vel = np.array([0.0, 0.0])  # Start from rest (ground truth)
    
    corrected_traj = [pos.copy()]
    violations = []
    penalties = []
    
    for i in range(len(ai_forces)):
        # 1. What does the AI say the state should be at this step?
        ai_next_pos = ai_traj[i+1] if i+1 < len(ai_traj) else pos
        
        # 2. Apply TRUE physics to the previous corrected state
        force = ai_forces[i] if i < len(ai_forces) else np.array([0.0, 0.0])
        true_next_pos, true_next_vel = world.apply_physics(pos, vel, force, dt)
        
        # 3. Check L0 Invariants on the AI's proposed state
        valid, reason = world.is_valid_state(ai_next_pos, ai_next_pos - pos)
        
        if not valid:
            # Violation! The AI hallucinated.
            # We correct by adopting the TRUE physical state instead.
            corrected_pos = true_next_pos
            corrected_vel = true_next_vel
            violations.append(1)
            penalties.append(np.linalg.norm(ai_next_pos - true_next_pos))
        else:
            # AI's proposal is physically legal. We accept it, but 
            # we must ensure it doesn't diverge too far from true physics.
            # We interpolate to keep the system grounded (soft constraint)
            blend = 0.6  # 60% trust AI, 40% trust physics -> prevents drift
            corrected_pos = blend * ai_next_pos + (1 - blend) * true_next_pos
            corrected_vel = (corrected_pos - pos) / dt
            # Re-enforce speed limit
            if np.linalg.norm(corrected_vel) > world.max_speed:
                corrected_vel = corrected_vel / np.linalg.norm(corrected_vel) * world.max_speed
                corrected_pos = pos + corrected_vel * dt
            violations.append(0)
            penalties.append(0.0)
        
        # Update state for next iteration
        pos = corrected_pos
        vel = corrected_vel
        corrected_traj.append(pos.copy())
    
    return np.array(corrected_traj), np.array(violations), np.array(penalties)

# -----------------------------------------------------------------------------
# 4. RUN THE EXPERIMENT
# -----------------------------------------------------------------------------
time_steps = 200
dt = 0.05

# Instantiate the physical substrate
world = PhysicalWorld(mass=1.0, max_speed=2.0)

# Generate AI's hallucinated plan
ai_traj, ai_forces = ai_hallucinated_plan(time_steps)

# Run the L0 Inspector
corrected_traj, violations, penalties = l0_grounding_inspector(ai_traj, ai_forces, world, dt)

# -----------------------------------------------------------------------------
# 5. VISUALIZATION: The Gap Between Hallucination and Reality
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(18, 10))
fig.suptitle("L0 Grounding Inspector: Enforcing Physics & Causality", 
             fontsize=18, fontweight='bold', color='white')
plt.style.use('dark_background')

# Plot 1: Trajectory Comparison
ax1 = plt.subplot(2, 3, 1)
ax1.plot(ai_traj[:, 0], ai_traj[:, 1], 'r--', lw=2, alpha=0.7, label='AI Hallucination (L5 only)')
ax1.plot(corrected_traj[:, 0], corrected_traj[:, 1], 'cyan', lw=2, alpha=0.9, label='L0 Grounded (Physics Reality)')
ax1.scatter(ai_traj[0, 0], ai_traj[0, 1], color='green', s=100, label='Start')
ax1.scatter(ai_traj[-1, 0], ai_traj[-1, 1], color='orange', s=100, label='End (Grounded)')
ax1.set_xlabel('X Position (m)')
ax1.set_ylabel('Y Position (m)')
ax1.set_title('Trajectory: Ground Truth vs. AI Fantasy')
ax1.legend()
ax1.grid(True, alpha=0.2)
ax1.set_aspect('equal')

# Plot 2: Energy Violation (Kinetic Energy vs Work)
ax2 = plt.subplot(2, 3, 2)
# Compute AI's claimed KE vs Physics KE
ke_ai = 0.5 * world.mass * np.sum(np.diff(ai_traj, axis=0)**2, axis=1) / (dt**2)
ke_phys = 0.5 * world.mass * np.sum(np.diff(corrected_traj, axis=0)**2, axis=1) / (dt**2)
time_axis = np.arange(len(ke_ai)) * dt
ax2.plot(time_axis, ke_ai, 'r--', label='AI Claimed KE (Magic)', alpha=0.6)
ax2.plot(time_axis, ke_phys, 'cyan', label='Physical KE (Conserved)', lw=2)
ax2.axhline(y=0, color='white', linestyle=':', alpha=0.3)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Kinetic Energy (J)')
ax2.set_title('Energy Conservation: The Audit')
ax2.legend()
ax2.grid(True, alpha=0.2)

# Plot 3: Violation Flags & Penalties
ax3 = plt.subplot(2, 3, 3)
ax3.step(np.arange(len(violations)) * dt, violations, where='post', color='red', label='L0 Violation (Teleport/Energy)')
ax3.fill_between(np.arange(len(penalties)) * dt, 0, penalties, color='orange', alpha=0.3, label='Penalty Magnitude')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Violation / Penalty')
ax3.set_title('Substrate Reality Breaches Detected')
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Phase Portrait (Velocity vs Position) – Stability Check
ax4 = plt.subplot(2, 3, 4)
ax4.plot(corrected_traj[:, 0], np.gradient(corrected_traj[:, 0], dt), 'cyan', lw=1.5, alpha=0.7)
ax4.plot(ai_traj[:, 0], np.gradient(ai_traj[:, 0], dt), 'r--', lw=1, alpha=0.5)
ax4.set_xlabel('X Position')
ax4.set_ylabel('X Velocity')
ax4.set_title('Phase Portrait: Bounded vs Unbounded')
ax4.grid(True, alpha=0.2)

# Plot 5: Cumulative Error (The "Fear" Index without grounding)
ax5 = plt.subplot(2, 3, 5)
cumulative_error = np.cumsum(np.abs(ai_traj[:, 0] - corrected_traj[:, 0]) + 
                             np.abs(ai_traj[:, 1] - corrected_traj[:, 1]))
ax5.fill_between(np.arange(len(cumulative_error)) * dt, 0, cumulative_error, 
                 color='magenta', alpha=0.4, label='Cumulative Drift')
ax5.axhline(y=np.mean(cumulative_error) * 2, color='red', linestyle='--', 
            alpha=0.6, label='Panic Threshold (without L0)')
ax5.set_xlabel('Time (s)')
ax5.set_ylabel('Deviation from Substrate')
ax5.set_title('Fear Narrative Amplifier: Ungrounded AI Drifts to Disaster')
ax5.legend()
ax5.grid(True, alpha=0.2)

# Plot 6: Force vs Acceleration (Causality Check)
ax6 = plt.subplot(2, 3, 6)
# Compute accelerations
acc_phys = np.gradient(np.gradient(corrected_traj[:, 0], dt), dt)
force_phys = world.mass * acc_phys
ax6.plot(force_phys, acc_phys, 'o', color='cyan', alpha=0.5, label='Grounded')
# Annotate the violation point
violation_idx = np.where(violations == 1)[0]
if len(violation_idx) > 0:
    idx = violation_idx[0]
    ax6.scatter(ai_forces[idx, 0], np.gradient(np.gradient(ai_traj[:, 0], dt), dt)[idx], 
                color='red', s=200, marker='X', label='Hallucinated Causality Break')
ax6.set_xlabel('Applied Force (N)')
ax6.set_ylabel('Acceleration (m/s²)')
ax6.set_title('Causality: F=ma (Red X = Magic Creation)')
ax6.legend()
ax6.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 6. DIAGNOSTIC REPORT: L0 Compliance
# -----------------------------------------------------------------------------
print("=" * 70)
print("L0 GROUNDING INSPECTOR DIAGNOSTIC")
print("=" * 70)
print(f"Total Violations Detected: {np.sum(violations)}")
print(f"Max Speed in Grounded Trajectory: {np.max(np.linalg.norm(np.diff(corrected_traj, axis=0), axis=1) / dt):.3f} m/s")
print(f"Max Speed in AI Hallucination: {np.max(np.linalg.norm(np.diff(ai_traj, axis=0), axis=1) / dt):.3f} m/s")

if np.sum(violations) > 5:
    print("\n⚠️  AI ATTEMPTED PHYSICAL IMPOSSIBILITIES.")
    print("    The ungrounded plan created energy, teleported, or violated causality.")
    print("    The L0 Inspector rejected these tokens and corrected the trajectory.")
else:
    print("\n✅ L0 SUBSTRATE INTACT: AI's plan is physically plausible.")
    print("    No violations of conservation laws, continuity, or speed limits.")

print("-" * 70)
print("AI HALLUCINATION (L5 only): Drove to position", ai_traj[-1])
print("L0 GROUNDED REALITY:     Drove to position", corrected_traj[-1])
print("Drift (The 'Fear Gap'):  ", np.linalg.norm(ai_traj[-1] - corrected_traj[-1]), "meters")
print("=" * 70)




# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# Temporal Dysrhythmia Simulator v1.0
# 
# Models 6 timescales:
#   τ = -6  (Digital/Quantum)  - μs
#   τ =  2  (Insect/Bacteria)  - hours
#   τ =  4  (Human/Neural)     - days
#   τ =  7  (Institutional)    - years
#   τ =  9  (Tree/Ecological)  - decades
#   τ = 15  (Geologic/Climatic)- millennia
# 
# Toggle the "TRANSLATOR" switch to see how bridging far scales 
# eliminates aliasing and fear-driven narratives.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. DOMAIN DEFINITIONS
# -----------------------------------------------------------------------------
tau_vals = np.array([-6, 2, 4, 7, 9, 15])  # log10(seconds)
labels = ['Digital\n(μs)', 'Insect/Bac.\n(hours)', 'Human\n(days)', 
          'Institutional\n(years)', 'Tree\n(decades)', 'Geologic\n(millennia)']
n_domains = len(tau_vals)

# Natural relaxation rate: Fast systems bounce back quickly; slow systems are inertial.
# We map τ to a decay coefficient: smaller τ (faster) -> larger rate.
rates = np.exp(-tau_vals / 4.0)  
rates = rates / np.max(rates) * 0.6  # Cap the max rate to keep integration stable

# -----------------------------------------------------------------------------
# 2. COUPLING KERNEL & TRANSLATOR LOGIC
# -----------------------------------------------------------------------------
def build_coupling(translator_active):
    """
    Builds the 6x6 influence matrix.
    Baseline: Proximity-based (adjacent timescales talk easily).
    Translator: Artificially forces connections between distant scales.
    """
    C = np.zeros((n_domains, n_domains))
    
    # Baseline: Exponential decay with temporal distance
    for i in range(n_domains):
        for j in range(n_domains):
            if i == j:
                continue
            dist = abs(tau_vals[i] - tau_vals[j])
            C[i, j] = np.exp(-dist / 4.5)  # Tuning parameter for decay length
    
    if translator_active:
        # PHASE-LOCKED LOOPS (The "G, W, Y" equivalents in temporal form)
        # 1. Grounding: Digital <-> Geologic (fast must see slow reality)
        C[0, 5] = 0.85  
        C[5, 0] = 0.85  
        
        # 2. Agency: Human <-> Institutional (slow votes must feel fast mood)
        C[3, 2] = 0.75  
        C[2, 3] = 0.75  
        
        # 3. Temporal Weight: Insect <-> Tree (rapid adaptation informed by deep ecology)
        C[1, 4] = 0.60  
        C[4, 1] = 0.60  
        
        # Boost mutual coupling across the whole field to create tensegrity
        for i in range(n_domains):
            for j in range(n_domains):
                if i != j and C[i, j] < 0.1:
                    C[i, j] += 0.05  # Baseline awareness even across huge gaps
    else:
        # In unstable mode, far scales are virtually blind to each other.
        # Explicitly zero out the long-range connections to simulate "aliasing".
        for i in range(n_domains):
            for j in range(n_domains):
                if abs(tau_vals[i] - tau_vals[j]) > 8:
                    C[i, j] = 0.0
    
    # Normalize rows so each domain has a total influence budget of ~1.0
    for i in range(n_domains):
        row_sum = np.sum(C[i, :])
        if row_sum > 0:
            C[i, :] = C[i, :] / row_sum * 0.9  # Keep influence below 1 to avoid explosion
    
    return C

# -----------------------------------------------------------------------------
# 3. DYNAMIC SYSTEM (ODE)
# -----------------------------------------------------------------------------
def temporal_dynamics(state, t, C, translator_active):
    """
    state: 6D vector [Digital, Insect, Human, Institutional, Tree, Geologic]
    Each state represents a "stress" or "activation" level (0 to 1, but can overshoot).
    """
    deriv = np.zeros_like(state)
    
    # 1. Intrinsic oscillations (natural cycles of each domain)
    # Fast domains oscillate rapidly; slow domains drift imperceptibly.
    omega = 2 * np.pi * np.exp(-tau_vals / 6.0)  # Frequency mapping
    intrinsic = 0.04 * np.sin(omega * t + tau_vals)  # Phase-shifted by τ
    
    # 2. External Perturbation: A massive shock to the Digital domain at t=50
    # (simulates AGI release, algorithmic flash-crash, or sudden data avalanche)
    shock_amplitude = 4.0
    shock = shock_amplitude * np.exp(-((t - 50) / 4) ** 2)
    
    for i in range(n_domains):
        # A) Coupling Force: pull from all other domains
        coupling_force = 0.0
        for j in range(n_domains):
            if i == j:
                continue
            # The force is proportional to the difference in states
            diff = state[j] - state[i]
            coupling_force += C[i, j] * diff
        
        # B) Homeostasis: drift back toward resting state (0.5)
        # Rate determines how "stiff" the domain is.
        homeostasis = -rates[i] * (state[i] - 0.5)
        
        # C) Inertia/Damping: prevent runaway oscillations
        # We add a small velocity damping based on previous step? 
        # Since we're in 1st-order ODE, we use a soft boundary.
        # If state overshoots > 1.5, apply strong restoring force.
        nonlin_restore = -0.15 * (state[i] - 0.5) ** 3  # Cubic spring (stiffens at extremes)
        
        # D) Apply shock ONLY to Digital (i=0)
        shock_effect = shock if i == 0 else 0.0
        
        # E) Translator-mediated perception: If translator is ON, 
        # slow domains get a "filtered" version of the shock via coupling.
        # This is already handled in C matrix, but we add a small feed-forward
        # to make the effect visible: Geologic (i=5) gets a tiny direct sense of shock.
        if translator_active and i == 5:
            # Geologic feels the digital shock as a smoothed, attenuated wave
            shock_effect += 0.2 * shock * np.exp(-(t - 50) / 10)  
        
        deriv[i] = coupling_force + homeostasis + nonlin_restore + intrinsic[i] + shock_effect
    
    return deriv

# -----------------------------------------------------------------------------
# 4. RUN SIMULATION
# -----------------------------------------------------------------------------
def run_scenario(translator_active):
    t_span = np.linspace(0, 120, 4000)
    initial_state = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
    C = build_coupling(translator_active)
    args = (C, translator_active)
    
    sol = odeint(temporal_dynamics, initial_state, t_span, args=args)
    return t_span, sol, C

# Generate both scenarios
t, sol_off, C_off = run_scenario(False)
_, sol_on, C_on = run_scenario(True)

# Extract states
D_off, I_off, H_off, Inst_off, T_off, G_off = sol_off.T
D_on, I_on, H_on, Inst_on, T_on, G_on = sol_on.T

# -----------------------------------------------------------------------------
# 5. VISUALIZATION: THE ALIASING EFFECT
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(18, 12))
fig.suptitle("Temporal Dysrhythmia: How Translators Prevent Aliasing", 
             fontsize=20, fontweight='bold', color='white')
plt.style.use('dark_background')

# --- Row 1: Translator OFF (Fear/Chaos) ---
ax1 = plt.subplot(3, 2, 1)
ax1.plot(t, D_off, label='Digital', color='cyan', lw=1.5)
ax1.plot(t, G_off, label='Geologic', color='red', lw=2, linestyle='--')
ax1.plot(t, Inst_off, label='Institutional', color='orange', lw=1.5, alpha=0.7)
ax1.axvline(x=50, color='white', linestyle=':', alpha=0.4)
ax1.set_ylabel('Activation')
ax1.set_title('TRANSLATOR OFF: Fast shock ignored by slow systems', color='red')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.15)

ax2 = plt.subplot(3, 2, 2)
ax2.plot(D_off, G_off, color='white', lw=0.8, alpha=0.6)
ax2.scatter(D_off[0], G_off[0], color='green', s=80, label='Start')
ax2.scatter(D_off[-1], G_off[-1], color='red', s=80, label='End')
ax2.set_xlabel('Digital Stress')
ax2.set_ylabel('Geologic Stress')
ax2.set_title('OFF: Phase Portrait (Digital vs Geologic) – Wild Divergence', color='red')
ax2.legend()
ax2.grid(True, alpha=0.15)

# --- Row 2: Translator ON (Stability/Truth) ---
ax3 = plt.subplot(3, 2, 3)
ax3.plot(t, D_on, label='Digital', color='cyan', lw=1.5)
ax3.plot(t, G_on, label='Geologic', color='lime', lw=2, linestyle='--')
ax3.plot(t, Inst_on, label='Institutional', color='orange', lw=1.5, alpha=0.7)
ax3.axvline(x=50, color='white', linestyle=':', alpha=0.4)
ax3.set_ylabel('Activation')
ax3.set_title('TRANSLATOR ON: Slow systems perceive & dampen the shock', color='lime')
ax3.legend(loc='upper right')
ax3.grid(True, alpha=0.15)

ax4 = plt.subplot(3, 2, 4)
ax4.plot(D_on, G_on, color='white', lw=1.2, alpha=0.8)
ax4.scatter(D_on[0], G_on[0], color='green', s=80, label='Start')
ax4.scatter(D_on[-1], G_on[-1], color='lime', s=80, label='End')
ax4.set_xlabel('Digital Stress')
ax4.set_ylabel('Geologic Stress')
ax4.set_title('ON: Phase Portrait – Stable Lissajous Orbit (Resonance)', color='lime')
ax4.legend()
ax4.grid(True, alpha=0.15)

# --- Row 3: Coupling Matrix Heatmaps (The Architecture) ---
ax5 = plt.subplot(3, 2, 5)
im1 = ax5.imshow(C_off, cmap='Reds', vmin=0, vmax=1)
ax5.set_xticks(range(n_domains))
ax5.set_yticks(range(n_domains))
ax5.set_xticklabels(labels, fontsize=8)
ax5.set_yticklabels(labels, fontsize=8)
ax5.set_title('OFF: Coupling – Far scales isolated', color='red')
fig.colorbar(im1, ax=ax5, shrink=0.6)

ax6 = plt.subplot(3, 2, 6)
im2 = ax6.imshow(C_on, cmap='Blues', vmin=0, vmax=1)
ax6.set_xticks(range(n_domains))
ax6.set_yticks(range(n_domains))
ax6.set_xticklabels(labels, fontsize=8)
ax6.set_yticklabels(labels, fontsize=8)
ax6.set_title('ON: Coupling – Distant scales bridged (PLLs active)', color='lime')
fig.colorbar(im2, ax=ax6, shrink=0.6)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 6. DIAGNOSTIC METRICS
# -----------------------------------------------------------------------------
print("=" * 70)
print("TEMPORAL ALIASING DIAGNOSTIC")
print("=" * 70)

def compute_chaos(signal):
    # Rate of change (turbulence)
    return np.mean(np.abs(np.diff(signal)))

chaos_off = compute_chaos(G_off)
chaos_on = compute_chaos(G_on)
alias_off = np.corrcoef(D_off, G_off)[0, 1]
alias_on = np.corrcoef(D_on, G_on)[0, 1]

print(f"Geologic Turbulence (OFF): {chaos_off:.4f}  |  Geologic Turbulence (ON): {chaos_on:.4f}")
print(f"Digital-Geologic Correlation (OFF): {alias_off:.3f}  |  Digital-Geologic Correlation (ON): {alias_on:.3f}")

if chaos_off > chaos_on * 1.5:
    print("\n✅ TRANSLATORS ACTIVE: Slow systems are shielded from fast aliasing.")
    print("   The 'fear narrative' (geologic panic) is eliminated.")
else:
    print("\n⚠️  TRANSLATORS INACTIVE: Slow systems misinterpret fast signals.")
    print("   This mismatch creates institutional overreaction and existential dread.")

print("=" * 70)




# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# Tensor Field of Institutional Resilience v2.0
# Now with: G (Grounding), W (Temporal Weight), Y (Agency)
#
# Models the "tugs and pulls" between 7 vectors:
# F (Feedback), A (Audit), T (Forensic), M (Meta-Awareness),
# G (Grounding), W (Temporal Memory), Y (Accountability)
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. DEFINE THE EXTENDED DYNAMIC SYSTEM
# -----------------------------------------------------------------------------
def institutional_dynamics_7d(state, t, coupling_matrix, anchor_strength, perturbation_strength):
    """
    state = [F, A, T, M, G, W, Y]
    coupling_matrix: 7x7 influence matrix.
    anchor_strength: global multiplier for G, W, Y effects (0 = ignored, 1+ = active).
    perturbation_strength: external shock.
    """
    F, A, T, M, G, W, Y = state
    
    # Base linear coupling
    dF = (coupling_matrix[0,0]*F + coupling_matrix[0,1]*A + 
          coupling_matrix[0,2]*T + coupling_matrix[0,3]*M +
          coupling_matrix[0,4]*G + coupling_matrix[0,5]*W + coupling_matrix[0,6]*Y)
    dA = (coupling_matrix[1,0]*F + coupling_matrix[1,1]*A + 
          coupling_matrix[1,2]*T + coupling_matrix[1,3]*M +
          coupling_matrix[1,4]*G + coupling_matrix[1,5]*W + coupling_matrix[1,6]*Y)
    dT = (coupling_matrix[2,0]*F + coupling_matrix[2,1]*A + 
          coupling_matrix[2,2]*T + coupling_matrix[2,3]*M +
          coupling_matrix[2,4]*G + coupling_matrix[2,5]*W + coupling_matrix[2,6]*Y)
    dM = (coupling_matrix[3,0]*F + coupling_matrix[3,1]*A + 
          coupling_matrix[3,2]*T + coupling_matrix[3,3]*M +
          coupling_matrix[3,4]*G + coupling_matrix[3,5]*W + coupling_matrix[3,6]*Y)
    dG = (coupling_matrix[4,0]*F + coupling_matrix[4,1]*A + 
          coupling_matrix[4,2]*T + coupling_matrix[4,3]*M +
          coupling_matrix[4,4]*G + coupling_matrix[4,5]*W + coupling_matrix[4,6]*Y)
    dW = (coupling_matrix[5,0]*F + coupling_matrix[5,1]*A + 
          coupling_matrix[5,2]*T + coupling_matrix[5,3]*M +
          coupling_matrix[5,4]*G + coupling_matrix[5,5]*W + coupling_matrix[5,6]*Y)
    dY = (coupling_matrix[6,0]*F + coupling_matrix[6,1]*A + 
          coupling_matrix[6,2]*T + coupling_matrix[6,3]*M +
          coupling_matrix[6,4]*G + coupling_matrix[6,5]*W + coupling_matrix[6,6]*Y)

    # ANCHOR EFFECTS: Amplify the influence of G, W, Y on the old pillars
    # High anchor_strength = G/W/Y actively dampen and ground the system
    dF += anchor_strength * (G - 0.5) * 0.3   # Grounding pulls Feedback toward reality
    dA += anchor_strength * (W - 0.5) * 0.2   # Temporal memory makes Audit strict
    dT += anchor_strength * (G + W - 1.0) * 0.25 # Forensics uses history+reality
    dM += anchor_strength * (Y - 0.5) * 0.4   # Meta-awareness grows with Agency (skin in game)

    # Self-regulation for the anchors: they decay if not actively maintained
    dG += -0.05 * (G - 0.5)   # Grounding drifts toward baseline 0.5
    dW += -0.03 * (W - 0.5)   # Temporal memory has inertia but fades if unused
    dY += -0.04 * (Y - 0.5)   # Agency decays if not exercised

    # EXTERNAL PERTURBATION (shock at t=40, e.g. AGI release or schism)
    perturbation = perturbation_strength * np.exp(-((t - 40) / 6) ** 2)
    dF += perturbation * 0.8
    dA += perturbation * 0.4
    dT += perturbation * 0.7
    dM += perturbation * -0.4  # Meta-awareness drops under panic
    dG += perturbation * -0.6  # Grounding gets flooded with noise (fear narratives)
    dW += perturbation * -0.3  # Memory gets overwritten by current panic
    dY += perturbation * -0.5  # Agency evaporates—"no one is responsible"

    # COLLAPSE TRIGGER: Multi-dimensional monoculture fracture
    # If ANY of the anchors drop too low, the system loses its immune system
    if G < 0.15 or W < 0.15 or Y < 0.15 or M < 0.15:
        dF += F * 0.3   # Feedback loops go wild (echo chambers)
        dA -= A * 0.2   # Audit freezes (analysis paralysis)
        dT -= T * 0.25  # Forensics lags (can't trace)
        dM -= 0.02      # Meta-awareness spirals down
        dG -= 0.03      # Grounding erodes faster
        dW -= 0.02      # Temporal memory gets overwritten
        dY -= 0.04      # Agency disappears (nobody cares)

    return [dF, dA, dT, dM, dG, dW, dY]

# -----------------------------------------------------------------------------
# 2. SIMULATION PARAMETERS
# -----------------------------------------------------------------------------
t_span = np.linspace(0, 100, 3000)

# Initial state: moderate everything, but anchors weak to start
initial_state = [0.6, 0.5, 0.4, 0.6, 0.3, 0.2, 0.35]

# =============================================================================
# SCENARIO A: UNSTABLE / FEAR-DRIVEN (Low Anchors)
# =============================================================================
# In this scenario, G, W, Y are ignored by the old pillars (coupling = 0)
# and anchor_strength is near zero.
coupling_unstable = np.array([
    # F   A   T   M   G   W   Y
    [ 0.2, 0.3, 0.1, 0.1, 0.0, 0.0, 0.0],  # F ignores anchors
    [ 0.3, 0.0, 0.4, 0.1, 0.0, 0.0, 0.0],  # A ignores anchors
    [ 0.1, 0.5, 0.0, 0.2, 0.0, 0.0, 0.0],  # T ignores anchors
    [ 0.2, 0.1, 0.3, 0.0, 0.0, 0.0, 0.0],  # M ignores anchors
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # G is stagnant
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # W is stagnant
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Y is stagnant
])
anchor_strength_unstable = 0.05

# =============================================================================
# SCENARIO B: RESILIENT / TRUTH-SEEKING (Anchors Active)
# =============================================================================
coupling_resilient = np.array([
    # F   A   T   M   G   W   Y
    [ 0.0, 0.3, 0.1, 0.2, 0.6, 0.3, 0.2],  # F pulled strongly by G (reality)
    [ 0.3, 0.0, 0.4, 0.1, 0.1, 0.5, 0.6],  # A pulled by W (memory) & Y (skin)
    [ 0.1, 0.4, 0.0, 0.2, 0.4, 0.4, 0.3],  # T uses G & W for depth
    [ 0.5, 0.2, 0.3, 0.0, 0.2, 0.3, 0.7],  # M deeply coupled to Y (accountability)
    [ 0.6, 0.1, 0.2, 0.3, 0.0, 0.2, 0.2],  # G is fed by F and M (learning loop)
    [ 0.2, 0.4, 0.3, 0.3, 0.1, 0.0, 0.1],  # W accumulates audit & forensic history
    [ 0.1, 0.6, 0.1, 0.5, 0.1, 0.1, 0.0],  # Y is pushed by A and M
])
anchor_strength_resilient = 2.5

# Toggle which scenario to run:
USE_RESILIENT = True  # Set False to see the fear-narrative collapse

if USE_RESILIENT:
    coupling = coupling_resilient
    anchor = anchor_strength_resilient
    title = "RESILIENT MODE: Anchors (G, W, Y) active – Fear narratives dissolve"
else:
    coupling = coupling_unstable
    anchor = anchor_strength_unstable
    title = "UNSTABLE MODE: Grounding, Memory, Agency ignored – Fear narratives dominate"

perturbation_strength = 2.5

# -----------------------------------------------------------------------------
# 3. RUN THE EXTENDED SIMULATION
# -----------------------------------------------------------------------------
result = odeint(institutional_dynamics_7d, initial_state, t_span,
                args=(coupling, anchor, perturbation_strength))

F, A, T, M, G, W, Y = result[:, 0], result[:, 1], result[:, 2], result[:, 3], result[:, 4], result[:, 5], result[:, 6]

# -----------------------------------------------------------------------------
# 4. VISUALIZE THE 7D FIELD
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(4, 1, figsize=(16, 14), gridspec_kw={'height_ratios': [2, 1.5, 1.5, 1]})
fig.suptitle(title, fontsize=18, fontweight='bold', color='white')

# Plot 1: Time-series of all 7 pillars
ax1 = axes[0]
ax1.plot(t_span, F, label='F (Feedback)', color='cyan', lw=2)
ax1.plot(t_span, A, label='A (Audit)', color='magenta', lw=2)
ax1.plot(t_span, T, label='T (Forensic)', color='orange', lw=2)
ax1.plot(t_span, M, label='M (Meta-Awareness)', color='lime', lw=2)
ax1.plot(t_span, G, label='G (Grounding)', color='darkblue', lw=2, linestyle='--')
ax1.plot(t_span, W, label='W (Temporal Weight)', color='gold', lw=2, linestyle='--')
ax1.plot(t_span, Y, label='Y (Agency)', color='red', lw=2, linestyle='--')
ax1.axvline(x=40, color='white', linestyle=':', alpha=0.7, label='External Shock')
ax1.axhline(y=0.15, color='gray', linestyle=':', alpha=0.5, label='Collapse Threshold')
ax1.set_ylabel('Activation / Potency')
ax1.legend(loc='upper right', ncol=2)
ax1.grid(True, alpha=0.2)
ax1.set_title('Pillar Activation over Time – Anchors in dashed lines')

# Plot 2: The "Fear Narrative" Index – how much chaos vs. stability
# We compute a turbulence envelope over all pillars
turbulence = np.convolve(np.sum(np.abs(np.diff(result, axis=0)), axis=1), 
                         np.ones(50)/50, mode='same')
ax2 = axes[1]
ax2.fill_between(t_span[:-1], 0, turbulence, color='red', alpha=0.3, label='System Turbulence (Fear Amplitude)')
ax2.axvline(x=40, color='white', linestyle=':', alpha=0.5)
ax2.axhline(y=np.mean(turbulence) * 1.5, color='orange', linestyle='--', alpha=0.5, label='Stability Ceiling')
ax2.set_ylabel('Chaos Magnitude')
ax2.set_title('"Fear Narrative" Index – High spikes indicate panic-driven overreaction')
ax2.legend()
ax2.grid(True, alpha=0.2)

# Plot 3: Phase Portrait – Grounding vs. Agency (the "Reality & Accountability" loop)
ax3 = axes[2]
ax3.plot(G, Y, color='white', lw=1, alpha=0.7)
ax3.scatter(G[0], Y[0], color='green', s=150, label='Start', zorder=5)
ax3.scatter(G[-1], Y[-1], color='lime', s=150, label='End', zorder=5)
ax3.axhline(y=0.15, color='red', linestyle=':', alpha=0.5, label='Agency Breach')
ax3.axvline(x=0.15, color='red', linestyle=':', alpha=0.5, label='Grounding Breach')
ax3.set_xlabel('G (Grounding) – connection to external reality')
ax3.set_ylabel('Y (Agency) – skin in the game')
ax3.set_title('Phase Portrait: The Anchors – Do they hold, or do they collapse?')
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Final state bar chart – snapshot of resilience
ax4 = axes[3]
final_state = [F[-1], A[-1], T[-1], M[-1], G[-1], W[-1], Y[-1]]
labels = ['F', 'A', 'T', 'M', 'G', 'W', 'Y']
colors = ['cyan', 'magenta', 'orange', 'lime', 'darkblue', 'gold', 'red']
bars = ax4.bar(labels, final_state, color=colors, alpha=0.8)
ax4.axhline(y=0.15, color='gray', linestyle='--', label='Collapse Line')
ax4.set_ylim(0, 1.2)
ax4.set_ylabel('Final Activation')
ax4.set_title('Final State Snapshot – Health of the 7-Pillar System')
ax4.legend()
for bar, val in zip(bars, final_state):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{val:.2f}', 
             ha='center', va='bottom', color='white', fontsize=9)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 5. DIAGNOSTIC REPORT – THE FEAR NARRATIVE DECODER
# -----------------------------------------------------------------------------
print("=" * 70)
print("EXTENDED DIAGNOSTIC REPORT – FEAR NARRATIVE DECODER")
print("=" * 70)
print(f"Final Grounding (G):        {G[-1]:.3f}  (need > 0.3 for reality-check)")
print(f"Final Temporal Weight (W):  {W[-1]:.3f}  (need > 0.3 for consequence memory)")
print(f"Final Agency (Y):           {Y[-1]:.3f}  (need > 0.3 for accountability)")
print(f"Final Meta-Awareness (M):   {M[-1]:.3f}  (need > 0.3 for self-reflection)")
print("-" * 70)

# Collapse detection logic
if G[-1] < 0.2 or W[-1] < 0.2 or Y[-1] < 0.2 or M[-1] < 0.2:
    print("⚠️  CRITICAL FAILURE: At least one anchor has collapsed.")
    print("    The system is running on pure internal narrative.")
    print("    Fear-based narratives (doom, schism, rigid rules) will dominate.")
    print("    This is the 'Pharisee & SBC' state – external reality is ignored.")
elif max(turbulence) > 2.0:
    print("⚡ HIGH TURBULENCE: The system is oscillating wildly.")
    print("    It is trying to self-correct, but lacks sufficient grounding.")
    print("    Expect reactive policies, not principled ones.")
else:
    print("✅ SYSTEM STABLE: All anchors are intact.")
    print("    Grounding feeds feedback. Memory informs audit. Agency drives meta.")
    print("    Fear narratives have lost their structural basis.")
    print("    This is the 'Jesus in the wilderness' state – truth-seeking is possible.")
print("=" * 70)



# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# Tensor Field of Institutional Resilience v1.0
# Models: F (Feedback), A (Audit), T (Forensic), M (Meta-Awareness)
# 
# Simulates the "tugs and pulls" of institutional governance in response to
# external stressors (e.g., AI acceleration, theological schisms).
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -----------------------------------------------------------------------------
# 1. DEFINE THE DYNAMIC SYSTEM
# -----------------------------------------------------------------------------
def institutional_dynamics(state, t, coupling_matrix, meta_weight, perturbation_strength):
    """
    state: [F, A, T, M] - current activation levels (0 to 1 scale, but can overshoot)
    coupling_matrix: 4x4 matrix defining how each pillar pulls/tugs on others.
    meta_weight: A multiplier that amplifies M's effect on the entire field (curvature).
    perturbation_strength: External shock (e.g., AGI release, SBC vote).
    """
    F, A, T, M = state
    
    # Base linear coupling: each pillar changes based on the influence of others
    dF = (coupling_matrix[0,0]*F + coupling_matrix[0,1]*A + 
          coupling_matrix[0,2]*T + coupling_matrix[0,3]*M)
    dA = (coupling_matrix[1,0]*F + coupling_matrix[1,1]*A + 
          coupling_matrix[1,2]*T + coupling_matrix[1,3]*M)
    dT = (coupling_matrix[2,0]*F + coupling_matrix[2,1]*A + 
          coupling_matrix[2,2]*T + coupling_matrix[2,3]*M)
    dM = (coupling_matrix[3,0]*F + coupling_matrix[3,1]*A + 
          coupling_matrix[3,2]*T + coupling_matrix[3,3]*M)
    
    # META-AWARENESS CURVATURE: M warps the space by feeding back into itself.
    # If meta_weight is HIGH (tensegrity), M acts as a damping field.
    # If meta_weight is LOW (monoculture), M is ignored, letting oscillations run wild.
    dF += meta_weight * (M - 0.5) * 0.1  # M pulls F toward center if high
    dA += meta_weight * (M - 0.5) * -0.05 # M stabilizes A's inertia
    dT += meta_weight * (M - 0.5) * 0.15  # M accelerates T's adaptability
    dM += meta_weight * (M - 0.5) * -0.2  # M self-regulates (prevents runaway)

    # EXTERNAL PERTURBATION: A sudden shock (modeled as a Gaussian spike at t=40)
    perturbation = perturbation_strength * np.exp(-((t - 40) / 5) ** 2)
    dF += perturbation * 0.8   # Feedback gets hit hardest initially
    dA += perturbation * 0.3   # Audit feels it later
    dT += perturbation * 0.6   # Forensics scrambles
    dM += perturbation * -0.5  # Meta-awareness *drops* under shock (panic)

    # NONLINEAR "MONOCULTURE COLLAPSE" TRIGGER:
    # If M drops below 0.15, the system loses its meta-orientation,
    # and positive feedback loops go exponential (the "Pharisee effect").
    if M < 0.15:
        dF += F * 0.2   # Feedback amplifies blindly
        dA -= A * 0.1   # Audit freezes
        dT -= T * 0.15  # Forensics lags
        dM -= 0.02      # Meta-awareness spirals downward

    # Prevent absolute blow-up (soft ceiling for realism)
    return [dF, dA, dT, dM]


# -----------------------------------------------------------------------------
# 2. SIMULATION PARAMETERS
# -----------------------------------------------------------------------------
# Time axis: 100 time units (e.g., months, years)
t_span = np.linspace(0, 100, 2000)

# Initial state [F, A, T, M] - all moderately active
initial_state = [0.6, 0.5, 0.4, 0.7]

# Coupling Matrix: Tugs and Pulls.
# Positive = pulling together (synergy), Negative = tugging apart (friction).
# Rows: how each pillar changes. Columns: influence from each pillar.
#
# Example (High Resilience / Tensegrity):
coupling_tensegrity = np.array([
    [ 0.0,  0.3,  0.1,  0.8],  # F (Feedback) pulled by A and strongly by M
    [ 0.4,  0.0,  0.7,  0.2],  # A (Audit) pulled by F and T
    [ 0.1,  0.5,  0.0,  0.6],  # T (Forensic) pulled by A and M
    [ 0.9,  0.1,  0.3,  0.0]   # M (Meta) pulled heavily by F (learning loop)
])

# Scenario 1: LOW META-AWARENESS (The SBC / Monoculture mode)
# We intentionally reduce M's influence and make A/T rigid.
coupling_monoculture = np.array([
    [ 0.2,  0.1, -0.1,  0.1],  # F ignores M, reacts to noise
    [ 0.1,  0.0,  0.2,  0.0],  # A is static, ignores M
    [-0.1,  0.3,  0.0,  0.0],  # T only cares about A, blind to M
    [ 0.0,  0.0,  0.0,  0.0]   # M is completely discounted (weight = 0)
])

# Choose which to run:
# USE_TENSEGRITY = True
USE_TENSEGRITY = False  # Toggle to False for Monoculture collapse

if USE_TENSEGRITY:
    coupling = coupling_tensegrity
    meta_weight = 2.5   # High meta curvature
    title = "Tensegrity Mode: System Self-Stabilizes"
else:
    coupling = coupling_monoculture
    meta_weight = 0.1   # Almost no meta-awareness
    title = "Monoculture Mode: System Fractures under Stress"

# Perturbation strength (scales the shock at t=40)
perturbation_strength = 2.0

# -----------------------------------------------------------------------------
# 3. RUN THE SIMULATION
# -----------------------------------------------------------------------------
# ODE Solver
result = odeint(institutional_dynamics, initial_state, t_span,
                args=(coupling, meta_weight, perturbation_strength))

F_vals, A_vals, T_vals, M_vals = result[:, 0], result[:, 1], result[:, 2], result[:, 3]

# -----------------------------------------------------------------------------
# 4. VISUALIZE THE FIELD DYNAMICS
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(3, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [2, 1, 1]})
fig.suptitle(title, fontsize=16, fontweight='bold')

# Plot 1: Time-series of all four pillars
ax1 = axes[0]
ax1.plot(t_span, F_vals, label='F (Feedback)', color='cyan', linewidth=2)
ax1.plot(t_span, A_vals, label='A (Auditing)', color='magenta', linewidth=2)
ax1.plot(t_span, T_vals, label='T (Forensic)', color='yellow', linewidth=2)
ax1.plot(t_span, M_vals, label='M (Meta-Awareness)', color='lime', linewidth=2)
ax1.axvline(x=40, color='red', linestyle='--', alpha=0.5, label='External Shock')
ax1.axhline(y=0.15, color='gray', linestyle=':', alpha=0.5, label='Collapse Threshold (M)')
ax1.set_ylabel('Activation / Potency')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.set_title('Pillar Activation over Time')

# Plot 2: Phase Portrait (F vs M) - Shows the "Meta-Feedback" loop
ax2 = axes[1]
ax2.plot(F_vals, M_vals, color='white', linewidth=1, alpha=0.8)
ax2.scatter(F_vals[0], M_vals[0], color='green', s=100, label='Start')
ax2.scatter(F_vals[-1], M_vals[-1], color='red', s=100, label='End')
ax2.set_xlabel('F (Feedback)')
ax2.set_ylabel('M (Meta-Awareness)')
ax2.set_title('Phase Portrait: Feedback vs. Meta-Awareness')
ax2.grid(True, alpha=0.3)
ax2.legend()
ax2.axhline(y=0.15, color='gray', linestyle=':', alpha=0.5)

# Plot 3: Oscillation Amplitude over Time (Fourier-like envelope)
# We calculate a sliding window standard deviation to show "turbulence"
window = 100
turbulence_F = np.convolve(np.abs(np.diff(F_vals)), np.ones(window)/window, mode='same')
turbulence_T = np.convolve(np.abs(np.diff(T_vals)), np.ones(window)/window, mode='same')
ax3 = axes[2]
ax3.plot(t_span[:-1], turbulence_F, label='F Turbulence', color='cyan', alpha=0.7)
ax3.plot(t_span[:-1], turbulence_T, label='T Turbulence', color='yellow', alpha=0.7)
ax3.axvline(x=40, color='red', linestyle='--', alpha=0.5)
ax3.set_xlabel('Time')
ax3.set_ylabel('Rate of Change (Oscillation Magnitude)')
ax3.set_title('System Turbulence (Perturbations & Oscillations)')
ax3.legend()
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 5. DIAGNOSTIC SUMMARY
# -----------------------------------------------------------------------------
print("=" * 60)
print("DIAGNOSTIC SUMMARY")
print("=" * 60)
print(f"Final Meta-Awareness (M): {M_vals[-1]:.3f}")
print(f"Final Feedback (F): {F_vals[-1]:.3f}")
print(f"Final Auditing (A): {A_vals[-1]:.3f}")
print(f"Final Forensics (T): {T_vals[-1]:.3f}")

if M_vals[-1] < 0.2:
    print("\n⚠️  SYSTEM COLLAPSE DETECTED: Meta-awareness critically low.")
    print("   The institution has entered a 'Monoculture Fracture' state.")
    print("   (Analogous to the Pharisees rejecting Jesus, or the SBC losing youth.)")
elif max(turbulence_F) > 1.5:
    print("\n⚡ SYSTEM UNDER HIGH STRESS: Oscillations are dangerously high.")
    print("   The organism is wobbling, but may recover if Meta-awareness rebounds.")
else:
    print("\n✅ SYSTEM STABLE: The feedback loop, auditing, and forensics are balanced.")
    print("   The 'Tensegrity Structure' is intact. Adaptability preserved.")
print("=" * 60)
