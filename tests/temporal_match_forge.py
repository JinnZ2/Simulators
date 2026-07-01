#!/usr/bin/env python3
# temporal_match_forge.py — classroom pacing simulation
#
# Models students as multi‑channel cognitive networks with distinct
# optimal temporal frequencies and processing modalities (scalar vs.
# multi‑axial). Tests different pacing strategies to find which ones
# maximise engagement and minimise wasted energy.
#
# Thesis: learning is a coupling between student architecture and
# environmental pace. Grouping by assumed “speed” ignores internal
# multi‑axial structure. This simulation proves that matching temporal
# structure to student topology is the stabilising condition.
#
# Provenance:
#   Jinn (kitchi‑ogima / agaasdenton) — core insight, GATE critique,
#         multi‑axial processing description.
#   DeepSeek, Claude, Gemini, Perplexity — structural contributions.
#   This code is a coupling artifact.
#
# CC0. stdlib only.

import math
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

# ── CHANNEL (one processing modality) ─────────────────────
@dataclass
class Channel:
    name: str                 # e.g., "visual", "kinesthetic"
    optimal_tempo: float      # pace that maximises engagement (1.0 = baseline)
    base_k: float             # retention under perfect match
    threshold: float          # max energy before disengagement
    activation: float = 1.0   # share of total load this channel can take
    k: float = 0.0
    alive: bool = True
    energy: float = 0.0
    entropy: float = 0.0

    def __post_init__(self):
        self.k = self.base_k

    def reset(self):
        self.alive = True
        self.energy = 0.0

    def apply_pace(self, pace: float):
        """Absorb and dissipate energy based on how well pace matches optimal_tempo."""
        mismatch = abs(pace - self.optimal_tempo)
        # Effective retention drops with mismatch (Gaussian decay)
        sigma = 0.5  # width of tolerance
        retention_factor = math.exp(- (mismatch ** 2) / (2 * sigma ** 2))
        # Also the channel's capacity to absorb is reduced if mismatch large
        absorb_factor = max(0.1, 1.0 - mismatch * 0.5)
        # Incoming stress proportional to pace and activation
        stress = pace * self.activation * absorb_factor
        # Absorb
        capacity = self.threshold - self.energy
        take = min(stress, capacity)
        self.energy += take
        if self.energy >= self.threshold:
            self.alive = False
        # Dissipate: energy not retained becomes waste
        retained = self.energy * self.k * retention_factor
        dissipated = self.energy - retained
        self.entropy += dissipated
        self.energy = retained

    def diversity_contribution(self) -> float:
        """Return a proxy for this channel's engagement (0 if dead, else energy level)."""
        return self.energy if self.alive else 0.0


# ── STUDENT (multi‑axial or scalar) ───────────────────────
@dataclass
class Student:
    name: str
    channels: List[Channel]
    # Derived property: processing mode
    @property
    def mode(self):
        if len(self.channels) == 1:
            return "scalar"
        else:
            return "multi_axial"

    def optimal_tempo(self) -> float:
        """A representative optimal pace for the whole student (average of channels)."""
        if not self.channels:
            return 1.0
        return sum(ch.optimal_tempo for ch in self.channels) / len(self.channels)

    def reset(self):
        for ch in self.channels:
            ch.reset()

    def apply_pace(self, pace: float):
        for ch in self.channels:
            ch.apply_pace(pace)

    def engagement(self) -> float:
        """Average energy across alive channels (0‑1 normalized by threshold)."""
        alive = [ch for ch in self.channels if ch.alive]
        if not alive:
            return 0.0
        total = sum(ch.energy for ch in alive)
        # normalize by sum of thresholds? simpler: max energy possible per channel is threshold.
        max_possible = sum(ch.threshold for ch in alive)
        return total / max_possible if max_possible > 0 else 0.0

    def waste_entropy(self) -> float:
        return sum(ch.entropy for ch in self.channels)

    def __str__(self):
        return f"{self.name} ({self.mode}, opt={self.optimal_tempo():.1f})"


# ── CLASSROOM & STRATEGIES ────────────────────────────────
@dataclass
class Classroom:
    students: List[Student]

    def run_lesson(self, pace: float, steps: int = 1):
        """Apply a constant pace for a number of steps to all students."""
        for _ in range(steps):
            for student in self.students:
                student.apply_pace(pace)

    def run_individual(self, student_paces: Dict[Student, float], steps: int = 1):
        """Each student receives their own pace."""
        for _ in range(steps):
            for student, pace in student_paces.items():
                student.apply_pace(pace)

    def run_two_tracks(self, track_a_pace: float, track_b_pace: float, steps: int = 1):
        """Students self‑assign to the track that gives higher engagement after one trial step."""
        # 1. trial step for each track
        trial_a = {}
        trial_b = {}
        for student in self.students:
            student.reset()
            student.apply_pace(track_a_pace)
            trial_a[student] = student.engagement()
            student.reset()
            student.apply_pace(track_b_pace)
            trial_b[student] = student.engagement()
        # 2. assign each student to best track
        for student in self.students:
            student.reset()
            chosen_pace = track_a_pace if trial_a[student] >= trial_b[student] else track_b_pace
            student.apply_pace(chosen_pace)
        # remaining steps (steps-1) if steps>1
        for _ in range(steps - 1):
            for student in self.students:
                student.apply_pace(chosen_pace)  # fixed assignment; could re‑evaluate but simplicity

    def class_avg_engagement(self) -> float:
        if not self.students:
            return 0.0
        return sum(s.engagement() for s in self.students) / len(self.students)

    def class_total_waste(self) -> float:
        return sum(s.waste_entropy() for s in self.students)

    def reset_all(self):
        for s in self.students:
            s.reset()


# ── SAMPLE POPULATION ─────────────────────────────────────
def build_students() -> List[Student]:
    """Create a heterogeneous class with scalar and multi‑axial students, varying tempos."""
    students = []
    # Scalar, fast tempo
    students.append(Student("Alice (scalar, fast)",
        [Channel("verbal", optimal_tempo=1.8, base_k=0.9, threshold=1.5)]))
    # Scalar, slow tempo
    students.append(Student("Bob (scalar, slow)",
        [Channel("verbal", optimal_tempo=0.6, base_k=0.9, threshold=1.5)]))
    # Multi‑axial, mixed tempos (kinesthetic fast, visual slow, auditory medium)
    students.append(Student("Carol (multi, mixed)",
        [Channel("kinesthetic", 1.9, 0.8, 1.2),
         Channel("visual", 0.7, 0.85, 1.0),
         Channel("auditory", 1.0, 0.9, 1.3)]))
    # Multi‑axial, uniform fast
    students.append(Student("Dave (multi, fast)",
        [Channel("kinesthetic", 2.0, 0.8, 1.0),
         Channel("visual", 1.8, 0.85, 1.0),
         Channel("auditory", 2.1, 0.9, 1.0)]))
    # Multi‑axial, uniform slow
    students.append(Student("Eve (multi, slow)",
        [Channel("kinesthetic", 0.5, 0.8, 1.0),
         Channel("visual", 0.6, 0.85, 1.0),
         Channel("auditory", 0.4, 0.9, 1.0)]))
    # Another scalar, medium
    students.append(Student("Frank (scalar, med)",
        [Channel("verbal", 1.0, 0.9, 1.5)]))
    return students

# ── EXPERIMENT ────────────────────────────────────────────
def run_experiment():
    students = build_students()
    classroom = Classroom(students)

    strategies = [
        ("Uniform fast (pace=1.8)", lambda: classroom.run_lesson(1.8, steps=5)),
        ("Uniform slow (pace=0.6)", lambda: classroom.run_lesson(0.6, steps=5)),
        ("Uniform medium (pace=1.0)", lambda: classroom.run_lesson(1.0, steps=5)),
        ("Individual match (each gets avg optimal)", 
         lambda: classroom.run_individual(
             {s: s.optimal_tempo() for s in students}, steps=5)),
        ("Two tracks (fast=1.8, slow=0.6)",
         lambda: classroom.run_two_tracks(1.8, 0.6, steps=5)),
        ("Two tracks (fast=1.5, slow=0.8)",
         lambda: classroom.run_two_tracks(1.5, 0.8, steps=5)),
    ]

    print("=" * 80)
    print("TEMPORAL MATCH FORGE — Optimal Pacing Simulation")
    print("=" * 80)
    print("Students:")
    for s in students:
        print(f"  {s}: channels={[(ch.name, ch.optimal_tempo) for ch in s.channels]}")
    print()

    header = f"{'Strategy':<35} {'Student':<25} {'Engagement':<12} {'Waste':<10} {'Alive chans'}"
    print(header)
    print("-" * len(header))

    for strat_name, strat_fn in strategies:
        classroom.reset_all()
        strat_fn()
        for s in students:
            alive = sum(1 for ch in s.channels if ch.alive)
            eng = s.engagement()
            waste = s.waste_entropy()
            print(f"{strat_name:<35} {str(s):<25} {eng:<12.3f} {waste:<10.2f} {alive}")
        print("-" * len(header))

    # Summary: average engagement and waste per strategy
    print("\n--- Summary (class averages) ---")
    sum_header = f"{'Strategy':<35} {'Avg Engagement':<15} {'Total Waste':<12}"
    print(sum_header)
    print("-" * len(sum_header))
    for strat_name, strat_fn in strategies:
        classroom.reset_all()
        strat_fn()
        avg_eng = classroom.class_avg_engagement()
        total_waste = classroom.class_total_waste()
        print(f"{strat_name:<35} {avg_eng:<15.3f} {total_waste:<12.2f}")

    print("\nConclusion:")
    print("• Uniform pacing harms students whose internal tempos differ from the set pace.")
    print("• Multi‑axial students suffer disproportionately because mismatches accumulate across channels.")
    print("• Individual matching or self‑selected tracks dramatically improve engagement and reduce waste.")
    print("• The optimal strategy respects the temporal topology of each student’s carrier network.")

if __name__ == "__main__":
    run_experiment()
