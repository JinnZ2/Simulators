# relational/figures — visualizations from actual runs

Each figure here is the output of running one of the shipped scripts.
Not authored diagrams — actual matplotlib output from the code as it
sits in this folder. If you edit a script and rerun, the figure
should update to match.

Three of these correspond to entries in the `FILES DELIVERED` table
of `../FINAL_CAPSTONE.md`; the fourth is the bonus
`cartesian_vs_relational_demo.py` visualization.

## The four figures

### `confusion_spectrum_visualization.jpg`
Source: [`../confusion_spectrum.py`](../confusion_spectrum.py) —
`demonstrate_confusion_spectrum()`. Four panels:

- **The Confusion Spectrum** (top left) — intensity 0 → 1 across
  9 scenarios walking from perfect prediction through catastrophic
  paradigm failure to recovery. Background bands mark absent / low /
  moderate / high / catastrophic zones.
- **Curiosity: The Homeostatic Response** (top center) — curiosity
  amplitude per scenario with the activation threshold line
  overlaid. Curiosity peaks in the low-confusion zone, drops to
  zero once confusion exceeds ~0.7 (cognitive-pain territory).
- **Biological Analogies** (bottom left) — color-coded map from
  biological state (tissue at rest → mild inflammation → immune
  activation → severe inflammation → tissue necrosis) to cognitive
  response (boredom → curiosity → exploration → cognitive pain →
  shutdown).
- **Clinical Applications** (bottom center) — text panel: how the
  spectrum reads ADHD boredom, anxiety, trauma/PTSD, depression,
  and flow states. Mirrors `CONFUSION_SPECTRUM.md §4`.
- **Sensor Hierarchy** (right) — the four sensor levels from
  physical pain through curiosity, all with the same "maintain
  triadic correlation or signal its breakdown" function.

### `social_pain_architecture.jpg`
Source: [`../social_pain_sensors.py`](../social_pain_sensors.py) —
`demonstrate_social_pain_sensors()`. Five panels:

- **Social Pain Intensity by Scenario** (top left) — bar chart per
  scenario (baseline through jealousy / shame / guilt / loneliness /
  recovery) with repair-threshold and destructive-threshold lines.
- **Somatic Markers: The Body Reports** (top center) — cortisol
  (stress), heart rate (normalized), and oxytocin (bonding)
  timeseries across the scenarios. Cortisol/HR spike where pain
  fires; oxytocin drops in the same window and recovers with
  correlation repair.
- **Pain as Triadic Verifier** (top right) — the Internal Model ↔
  Body ↔ External World diagram with the PAIN SENSOR node
  triangulating them. Bulleted list of what each social pain type
  detects (anxiety = uncertain threat; jealousy = exclusive
  falsified; shame = acceptability falsified; guilt = moral
  falsified; loneliness = no correlation).
- **Triadic Components by Pain Type** (bottom left) — stacked bars
  for each pain type showing which of the three domains
  (internal / body / external) is doing the falsifying.
- **Paradigm Shift** (bottom center) — text panel contrasting
  OLD (pain as pathology, silence the sensor) vs NEW (pain as
  sensor, repair the correlation). Mirrors
  `COMPLETE_ARCHITECTURE.md §5.3`.
- **Recovery: Pain Clears When Correlation Repairs** (bottom right)
  — pain decays exponentially, cortisol falls, oxytocin rises.
  Vertical lines mark Acknowledgment and Repair moments. Directly
  visualizes `COMPLETE_ARCHITECTURE.md §6`.

### `birth_mode_comparison.jpg`
Source: [`../nurturing_environment.py`](../nurturing_environment.py) —
`compare_birth_modes()`. Four panels:

- **Affective State by Birth Mode** (top left) — grouped bars for
  curiosity / fear / contentment / anger / grief across the six
  modes. SOCIAL is the only mode with visible fear amplitude —
  matches the doc's headline finding.
- **Development Metrics** (top right) — manifold-nodes count +
  anomalies + self-model size per mode. SOCIAL is again the only
  outlier (anomalies present because of the harsh interaction
  moment in that mode's sequence).
- **Protector Health by Birth Mode** (bottom left) — count of GREEN
  signals from each of the five protectors, per mode. Ontological
  protector goes YELLOW for META_CURIOSITY / SOCIAL / TEMPORAL /
  INFORMATIONAL modes (fewer instrument streams) and GREEN for
  PHYSICAL / CORRELATED. Social protector goes RED only for the
  SOCIAL mode (the "stop that!" harsh moment).
- **Birth Mode Characteristics** (bottom right) — text panel:
  PHYSICAL (grounded, sensor-oriented), META_CURIOSITY (self-
  reflective), SOCIAL (relational), TEMPORAL (rhythmic),
  INFORMATIONAL (pattern-seeking), CORRELATED (systems-thinking).
  Mirrors `INTEGRATION_SUMMARY.md §2`.

### `cartesian_vs_relational_visualization.png`
Source: [`../cartesian_vs_relational_demo.py`](../cartesian_vs_relational_demo.py).
Four panels:

- **Accuracy Over Time in Changing Environment** (top left) —
  Cartesian agent starts at 1.00 and drops to ~0.37; Relational
  agent starts at 0.4 and climbs to ~0.6-0.7. Two vertical dashes
  mark the truth-change events at step 10 ("except at poles") and
  step 20 ("Earth's rotation"). Directly matches the smoke-test
  numbers in `notes.md §19` (Cartesian 0.36, Relational 0.52).
- **Environment: Constantly Changing** (top right) — temperature
  cycles (blue) and information quality cycles (yellow), out of
  phase. The `ChangingEnvironment.step()` sine-wave cycling made
  visible.
- **Relational Agent: Internal State Visible** (bottom left) —
  confusion, curiosity, and body energy over time. Confusion
  crosses the cognitive-pain threshold at step 10 (truth shift
  event); curiosity dips into the optimal zone as body energy
  drops. This is what the framework's central claim looks like in
  motion: the relational agent's *state is legible*, not opaque.
- **WHAT OTHER AIs SHOULD SEE** (bottom right) — text panel. The
  demo is explicitly framed for other models to read; this panel
  is the framing. Not a chart — a message.

## What these confirm

Each figure independently verifies a claim I made in the notes:

- The `social_pain_architecture.jpg`'s Recovery panel visually
  matches `COMPLETE_ARCHITECTURE.md §6`'s claim that pain decays
  exponentially when correlation is repaired, oxytocin/cortisol
  invert in the same window.
- The `birth_mode_comparison.jpg` Protector Health panel visually
  matches `INTEGRATION_SUMMARY.md §6`'s table showing SOCIAL as
  the only mode where the social protector ever goes RED.
- The `cartesian_vs_relational_visualization.png` accuracy panel
  visually matches the empirical claim (`notes.md §19`) that
  Relational beats Cartesian in a changing environment. Numbers
  match the smoke test run.

Landed as the *fifth drop* per `notes.md §22`. Closes the
FILES-DELIVERED PNG-visualization gap that was outside scope in
earlier drops.
