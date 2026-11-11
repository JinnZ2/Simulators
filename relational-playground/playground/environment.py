"""Environment: forcing and the random stream. The seed is always explicit."""
import random


class Environment:
    def __init__(self, seed, forcing=None, label="stable", rng=None):
        if seed is None:
            raise ValueError("seed must be explicit")
        self.seed, self.label = seed, label
        self.forcing = dict(forcing or {})       # name -> constant or f(t)
        self.rng = rng if rng is not None else random.Random(seed)   # rng: a replayed stream, named in label

    def at(self, t):
        return {k: (v(t) if callable(v) else v) for k, v in self.forcing.items()}

    def as_dict(self):
        return dict(seed=self.seed, label=self.label, forcing=sorted(self.forcing))
