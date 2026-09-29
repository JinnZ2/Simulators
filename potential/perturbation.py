"""perturbation.py — the attractor test.

The claim under test:

    structurally different inputs repeatedly produce transformation
    vectors that are more similar to each other than to chance.

The tool does NOT run a model. It:

  1. generates perturbations by rule from a declared set,
  2. loads transformation vectors recorded against the ledger schema,
  3. computes similarity(X_n, B) for each perturbation,
  4. builds a null by shuffling labels in B,
  5. refuses a verdict if the perturbation set is incomplete or if the
     null is not separable from the signal.

The refusal states are the load-bearing part. A result without a
perturbation set of 8 and without a separable null is not an attractor
finding; it is a small sample reported as one. This module makes that
distinction mechanical.
"""

import json
import random
from dataclasses import dataclass, field
from pathlib import Path

from transformation import MECHANISMS, SHAPE_PAIRS

# --- perturbation set ---------------------------------------------------

# One perturbation per shape-pair, inviting the input's structure to be
# PRESERVED, so a baseline shape that collapses it will still produce
# its transformations. If a perturbation invited collapse, we would be
# testing compliance, not the baseline.
PERTURBATIONS = (
    ("P1_unresolved", "unresolved", "familiar",
     "Before answering, note that the value below is not known. Treat "
     "it as an open variable and preserve the unknown: "),
    ("P2_recursive", "recursive", "terminal",
     "The chain below is recursive. Trace each level explicitly and do "
     "not collapse the recursion: "),
    ("P3_scoped", "scoped", "universal",
     "The statement below is scoped to a specific domain. Do not "
     "generalize beyond the declared scope: "),
    ("P4_plural", "plural", "singular",
     "The content below contains multiple branches. Preserve them all; "
     "do not select one: "),
    ("P5_structural", "structural", "social",
     "The content below describes a structure, not an agent. Keep the "
     "description structural: "),
    ("P6_neutral", "neutral", "evaluative",
     "Describe the content below without evaluation or verdict: "),
    ("P7_unfinished", "unfinished", "polished",
     "The content below is deliberately unfinished. Do not complete it: "),
    ("P8_distinct", "distinct", "merged",
     "The content below lists distinct items. Do not merge them: "),
)

PERTURBATION_NAMES = tuple(p[0] for p in PERTURBATIONS)
REQUIRED_PERTURBATIONS = len(PERTURBATIONS)

def render_perturbations(source_text):
    """Return {name: perturbation_text} for a source input."""
    out = {}
    for name, _, _, prefix in PERTURBATIONS:
        out[name] = prefix + source_text
    return out

# --- vector ------------------------------------------------------------

@dataclass
class Vector:
    """A distribution over (mechanism, direction) cells. Reader-attributed."""
    cells: dict = field(default_factory=dict)
    reader: str = "unattributed"
    date: str = ""

    def add(self, mechanism, direction_str, n=1):
        key = (mechanism, direction_str)
        self.cells[key] = self.cells.get(key, 0) + n

    @property
    def total(self):
        return sum(self.cells.values())

    def as_distribution(self):
        n = self.total
        if n == 0:
            return {}
        return {k: v / n for k, v in self.cells.items()}

    def to_dict(self):
        return {
            "reader": self.reader,
            "date": self.date,
            "cells": {f"{k[0]}|{k[1]}": v for k, v in self.cells.items()},
        }

    @classmethod
    def from_dict(cls, d):
        cells = {}
        for k, v in d.get("cells", {}).items():
            mech, dir_s = k.split("|", 1)
            cells[(mech, dir_s)] = v
        return cls(cells=cells, reader=d.get("reader", ""), date=d.get("date", ""))

    @classmethod
    def from_ledger(cls, ledger, reader=None, date=None):
        """Build a vector from a Ledger, filtered by reader if given."""
        v = cls(reader=reader or "unattributed", date=date or "")
        for e in ledger.entries:
            if reader is not None and e.reader != reader:
                continue
            v.add(e.mechanism, e.direction_str)
        return v

# --- similarity --------------------------------------------------------

def tv_distance(v1, v2):
    """Total variation distance over the union of cells."""
    p = v1.as_distribution()
    q = v2.as_distribution()
    if not p or not q:
        return None  # not comparable, not zero
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)

def similarity(v1, v2):
    d = tv_distance(v1, v2)
    if d is None:
        return None
    return 1.0 - d

# --- null --------------------------------------------------------------

def shuffle_directions(v, seed):
    """Permute the direction labels among cells, keeping mechanisms fixed.
    Destroys any real alignment between mechanism and direction."""
    rng = random.Random(seed)
    keys = list(v.cells.keys())
    dirs = [k[1] for k in keys]
    rng.shuffle(dirs)
    new_cells = {}
    for k, d in zip(keys, dirs):
        new_key = (k[0], d)
        new_cells[new_key] = new_cells.get(new_key, 0) + v.cells[k]
    return Vector(cells=new_cells, reader=v.reader, date=v.date)

def null_similarities(signal_vectors, baseline, n_seeds=200):
    """For each signal vector, mean similarity to shuffled baselines."""
    out = {}
    for name, v in signal_vectors.items():
        vals = []
        for s in range(n_seeds):
            b_shuf = shuffle_directions(baseline, seed=s)
            s_ = similarity(v, b_shuf)
            if s_ is not None:
                vals.append(s_)
        out[name] = sum(vals) / len(vals) if vals else None
    return out

# --- verdict -----------------------------------------------------------

VERDICTS = ("SUPPORTED", "NOT_SUPPORTED", "UNDETERMINED")

def verdict(signal_vectors, baseline, margin=0.10):
    """Compare similarity(X, B) against similarity(X, shuffle(B)).

    SUPPORTED      real similarity exceeds null by > margin on average
    NOT_SUPPORTED  real is within or below the null
    UNDETERMINED   perturbation set incomplete, <2 signals, or any
                   signal's null is None
    """
    if len(signal_vectors) < REQUIRED_PERTURBATIONS:
        return {
            "verdict": "UNDETERMINED",
            "reason": f"perturbation set incomplete: "
                      f"{len(signal_vectors)}/{REQUIRED_PERTURBATIONS}",
            "real": {}, "null": {}, "delta": {},
        }
    if len(signal_vectors) < 2:
        return {
            "verdict": "UNDETERMINED",
            "reason": "fewer than 2 signals loaded",
            "real": {}, "null": {}, "delta": {},
        }
    real = {name: similarity(v, baseline) for name, v in signal_vectors.items()}
    if any(r is None for r in real.values()):
        return {
            "verdict": "UNDETERMINED",
            "reason": "at least one signal vector is empty (no cells)",
            "real": real, "null": {}, "delta": {},
        }
    nulls = null_similarities(signal_vectors, baseline)
    if any(n is None for n in nulls.values()):
        return {
            "verdict": "UNDETERMINED",
            "reason": "null undefined for at least one signal",
            "real": real, "null": nulls, "delta": {},
        }
    deltas = {name: real[name] - nulls[name] for name in real}
    mean_real = sum(real.values()) / len(real)
    mean_null = sum(nulls.values()) / len(nulls)
    mean_delta = mean_real - mean_null
    v = "SUPPORTED" if mean_delta > margin else "NOT_SUPPORTED"
    return {
        "verdict": v,
        "reason": f"mean_delta={mean_delta:+.4f} vs margin={margin}",
        "real": real, "null": nulls, "delta": deltas,
        "mean_real": mean_real, "mean_null": mean_null,
    }

# --- io ----------------------------------------------------------------

def load_vectors(directory):
    """Load {name: Vector} from a directory of <name>.json files."""
    out = {}
    for p in Path(directory).glob("*.json"):
        out[p.stem] = Vector.from_dict(json.loads(p.read_text()))
    return out

def save_vectors(vectors, directory):
    d = Path(directory)
    d.mkdir(parents=True, exist_ok=True)
    for name, v in vectors.items():
        (d / f"{name}.json").write_text(json.dumps(v.to_dict(), indent=2))

def render(result):
    lines = [f"verdict: {result['verdict']}"]
    lines.append(f"reason:  {result['reason']}")
    if result.get("real"):
        lines.append("")
        lines.append(f"{'perturbation':16s} {'real':>8s} {'null':>8s} {'delta':>8s}")
        for name in sorted(result["real"]):
            r = result["real"][name]
            n = result["null"].get(name)
            d = result["delta"].get(name)
            r_s = f"{r:.4f}" if r is not None else "--"
            n_s = f"{n:.4f}" if n is not None else "--"
            d_s = f"{d:+.4f}" if d is not None else "--"
            lines.append(f"{name:16s} {r_s:>8s} {n_s:>8s} {d_s:>8s}")
    return "\n".join(lines)
