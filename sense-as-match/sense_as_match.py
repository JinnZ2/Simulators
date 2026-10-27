# SPDX-License-Identifier: CC0-1.0
"""
sense_as_match.py -- reduce a pattern from any channel to its SHAPE, match
the shape against a held set IN SHAPE SPACE, and refuse to force a pattern
that has not settled.

Rebuilt from WORK_ORDER.md. No original was recovered and none was sought.
The repo-root file of the same name is a different instrument (its own
docstring calls it sense_at_match.py: a word's sense gated at the match
site). It is not edited here.

THE MEASURAND AND THE METHOD
    A pattern is a sequence of readings. Its SHAPE is what is left after the
    channel's own properties are taken out: the offset (where the channel
    zeroes), the gain (its units and sensitivity) and the sampling (how many
    readings it took over the span). The channel is METHOD. It is carried in
    the result for audit and enters no function that decides a state.

THREE RETURN STATES
    KNOWN        the observations settle on a held shape.
    NEW          they settle on no held shape AND are definite: they agree
                 with each other closely enough to be one shape. The shape
                 is registered.
    UNCOALESCED  anything else. Held with a probability field over the
                 candidates. Never forced to the nearest neighbour: an
                 observation that is outside every held shape's radius is
                 counted toward NEW, not toward the shape it happens to be
                 closest to, and an observation inside two radii splits its
                 weight between them.

THE PROBABILITY FIELD
    Each reducible observation puts weight 1 on the candidates it reaches:
    split evenly across every held shape within RADIUS, or all on NEW when
    it reaches none. The field is that weight divided by the number of
    observations. It collapses only when one candidate's share reaches
    COLLAPSE (declared, > 0.5 so two candidates cannot both reach it), and
    only once MIN_OBS observations exist. Adding observations is the
    update; the field is recomputed from all of them.

GAPS, marked in-line as [GAP n]:
    1  a flat pattern (zero spread) has no shape under this reduction. It
       is excluded and counted, not matched. A constant IS a shape; this
       reduction cannot carry it.
    2  shapes are one-dimensional sequences. Multi-channel, 2-D or
       event-time patterns have no reduction here.
    3  sign is kept: a pattern and its mirror image are different shapes.
       Whether a channel can invert polarity is a property of the channel,
       and taking it out would need the channel in the match.
    4  the registered NEW shape is the mean of its observations. The
       observations that put weight on NEW are not split into more than one
       novel shape.
    5  a shape that genuinely lies between two held shapes, inside both
       radii, can never collapse: each observation of it puts at most half
       its weight on either, and none on NEW, so no amount of evidence of
       that same shape moves it. It stays UNCOALESCED until differently
       placed evidence arrives. Held open is the order's rule for plastic
       patterns; that it is held open FOREVER for this one geometry is a
       limit, not a finding.

Library module: refuses --selftest (exit 2) and names test_sense.py.
`--choices` prints every [CHOICE n]. stdlib only, parses under 3.9.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field

KNOWN = "KNOWN"
NEW = "NEW"
UNCOALESCED = "UNCOALESCED"
STATES = (KNOWN, NEW, UNCOALESCED)

NEW_SLOT = "NEW"  # the field's name for "reaches no held shape"

CHOICES = {
    1: "SHAPE = the readings linearly resampled to LENGTH points, mean "
       "removed, divided by the population standard deviation. This takes "
       "out offset, gain and sampling count, which are properties of the "
       "channel, and keeps the form.",
    2: "distance in shape space is RMS difference between two shapes. For "
       "shapes reduced this way, RMS = sqrt(2 * (1 - r)), r the Pearson "
       "correlation, so RADIUS 0.5 means r >= 0.875.",
    3: "an observation within RADIUS of more than one held shape splits its "
       "weight evenly between them. It is never given to the nearer one: "
       "that is the nearest-neighbour forcing the order refuses.",
    4: "an observation within RADIUS of no held shape puts its weight on "
       "NEW, not on its nearest held shape.",
    5: "COLLAPSE (default 0.8) must be > 0.5, so no two candidates can both "
       "reach it and a tie can never collapse.",
    6: "MIN_OBS (default 2): a single observation carries no measure of its "
       "own dispersion, so by default it cannot be called settled. MIN_OBS "
       "1 is allowed and declared; it still cannot produce NEW, because "
       "definiteness needs a spread and one observation has none.",
    7: "DEFINITE = the observations weighting NEW have mean pairwise RMS "
       "distance <= SPREAD (default 0.35, r >= ~0.94). Spread of fewer than "
       "two observations is None, never 0.",
    8: "the result of an UNCOALESCED match carries shape None. The nearest "
       "held shape is not reported, so no caller can read it as the answer.",
}


@dataclass(frozen=True)
class Params:
    length: int = 32         # [CHOICE 1]
    radius: float = 0.5      # [CHOICE 2]
    collapse: float = 0.8    # [CHOICE 5]
    min_obs: int = 2         # [CHOICE 6]
    spread: float = 0.35     # [CHOICE 7]

    def __post_init__(self):
        if self.length < 3:
            raise ValueError("length must be >= 3")
        if not (self.radius > 0):
            raise ValueError("radius must be > 0")
        if not (0.5 < self.collapse <= 1.0):
            raise ValueError("collapse must be in (0.5, 1.0]  [CHOICE 5]")
        if self.min_obs < 1:
            raise ValueError("min_obs must be >= 1")
        if not (self.spread > 0):
            raise ValueError("spread must be > 0")


# ----------------------------------------------------------------- shape --

def _finite(xs):
    return all(isinstance(x, (int, float)) and not isinstance(x, bool)
               and math.isfinite(x) for x in xs)


def _resample(values, length):
    n = len(values)
    out = []
    for i in range(length):
        pos = i * (n - 1) / (length - 1)
        lo = int(math.floor(pos))
        hi = min(lo + 1, n - 1)
        frac = pos - lo
        out.append(values[lo] * (1 - frac) + values[hi] * frac)
    return out


def reduce_shape(values, length=Params.length):
    """Readings -> shape tuple, or None when the readings have no shape
    under this reduction (fewer than two readings, a non-finite reading,
    or zero spread -- [GAP 1])."""
    values = list(values)
    if len(values) < 2 or not _finite(values):
        return None
    r = _resample(values, length)
    mean = sum(r) / length
    sd = math.sqrt(sum((x - mean) ** 2 for x in r) / length)
    if sd == 0:
        return None  # [GAP 1] a constant has no shape here
    return tuple((x - mean) / sd for x in r)


def distance(a, b):
    """RMS difference between two shapes of equal length.  [CHOICE 2]"""
    if a is None or b is None or len(a) != len(b):
        return None
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / len(a))


def shape_distance(a_values, b_values, length=Params.length):
    """Distance between the shapes of two raw patterns; None if either has
    no shape. The known-answer metric."""
    return distance(reduce_shape(a_values, length),
                    reduce_shape(b_values, length))


def spread(shapes):
    """Mean pairwise distance. None for fewer than two shapes: one shape has
    no dispersion to measure, which is not a dispersion of zero."""
    shapes = list(shapes)
    if len(shapes) < 2:
        return None
    ds = [distance(shapes[i], shapes[j])
          for i in range(len(shapes)) for j in range(i + 1, len(shapes))]
    return sum(ds) / len(ds)


def mean_shape(shapes, length):
    shapes = list(shapes)
    avg = [sum(s[i] for s in shapes) / len(shapes) for i in range(length)]
    return reduce_shape(avg, length)


# ------------------------------------------------------------ held set ----

class KnownSet:
    """Held shapes by name. Shapes are stored reduced; registration of a NEW
    shape returns its name."""

    def __init__(self, params=None):
        self.params = params or Params()
        self.shapes = {}
        self._n = 0

    def add(self, values, name=None):
        s = reduce_shape(values, self.params.length)
        if s is None:
            raise ValueError("a held shape must be reducible  [GAP 1]")
        return self._put(s, name)

    def _put(self, shape, name=None):
        self._n += 1
        name = name or "S%d" % self._n
        if name in self.shapes or name == NEW_SLOT:
            raise ValueError("shape name %r is taken" % name)
        self.shapes[name] = shape
        return name


@dataclass
class Incoming:
    """One or more observations of one pattern, and the channel(s) they came
    through. `channel` is METHOD: stored for audit, read by no decision."""
    observations: list
    channel: dict = field(default_factory=dict)


# --------------------------------------------------------------- match ----
# Nothing below this line until `match` names the channel. test_sense.py
# reads the AST of _field and _decide to hold that.

def _field(shapes, held, radius):
    weights = {}
    for s in shapes:
        reach = [name for name, h in held.items() if distance(s, h) <= radius]
        if reach:
            w = 1.0 / len(reach)                   # [CHOICE 3] [GAP 5]
            for name in reach:
                weights[name] = weights.get(name, 0.0) + w
        else:
            weights[NEW_SLOT] = weights.get(NEW_SLOT, 0.0) + 1.0  # [CHOICE 4]
    n = len(shapes)
    return {k: v / n for k, v in weights.items()} if n else {}


def _novel(shapes, held, radius):
    return [s for s in shapes
            if not any(distance(s, h) <= radius for h in held.values())]


def _decide(shapes, held, params):
    """(state, winner, field, reason). Reads shapes only."""
    fld = _field(shapes, held, params.radius)
    if not shapes:
        return UNCOALESCED, None, fld, "no reducible observation"
    winner = max(sorted(fld), key=lambda k: fld[k])
    share = fld[winner]
    if len(shapes) < params.min_obs:
        return (UNCOALESCED, None, fld,
                "%d observation(s), MIN_OBS %d  [CHOICE 6]"
                % (len(shapes), params.min_obs))
    if share < params.collapse:
        return (UNCOALESCED, None, fld,
                "largest share %.3f (%s) below COLLAPSE %.2f"
                % (share, winner, params.collapse))
    if winner != NEW_SLOT:
        return KNOWN, winner, fld, "share %.3f >= COLLAPSE" % share
    sp = spread(_novel(shapes, held, params.radius))
    if sp is None or sp > params.spread:
        return (UNCOALESCED, None, fld,
                "novel but not definite: spread %s, SPREAD %.2f  [CHOICE 7]"
                % ("None" if sp is None else "%.3f" % sp, params.spread))
    return NEW, None, fld, "novel and definite: spread %.3f" % sp


def match(incoming, known_set):
    """incoming: Incoming. known_set: KnownSet (mutated only by a NEW).
    -> {state, shape, between, field, reason, n_obs, n_unreducible,
        audit, pending}"""
    p = known_set.params
    shapes, unreducible = [], 0
    for obs in incoming.observations:
        s = reduce_shape(obs, p.length)
        if s is None:
            unreducible += 1
        else:
            shapes.append(s)
    state, winner, fld, reason = _decide(shapes, known_set.shapes, p)
    out = {"state": state, "shape": None, "between": None, "field": fld,
           "reason": reason, "n_obs": len(shapes),
           "n_unreducible": unreducible,
           "audit": {"channel": incoming.channel},  # stored, not matched
           "pending": None}
    if state == KNOWN:
        out["shape"] = winner
    elif state == NEW:
        novel = _novel(shapes, known_set.shapes, p.radius)
        out["shape"] = known_set._put(mean_shape(novel, p.length))  # [GAP 4]
    else:
        out["between"] = sorted(fld, key=lambda k: (-fld[k], k))   # [CHOICE 8]
        out["pending"] = incoming
    return out


def update(result, evidence, known_set, channel=None):
    """Add observations to an UNCOALESCED result and re-match. The field is
    recomputed from every observation so far. `channel` is appended to the
    audit trail only."""
    if result["state"] != UNCOALESCED or result["pending"] is None:
        raise ValueError("only an UNCOALESCED result carries a pending field")
    prior = result["pending"]
    trail = prior.channel.get("trail", [dict(prior.channel)])
    if channel is not None:
        trail = trail + [channel]
    merged = Incoming(list(prior.observations) + list(evidence),
                      {"trail": trail})
    return match(merged, known_set)


# --------------------------------------------------------------- CLI ------

def render_choices():
    return "\n".join("[CHOICE %d] %s" % (k, v) for k, v in sorted(CHOICES.items()))


def main(argv):
    if "--selftest" in argv:
        print("sense_as_match.py is a library module; run test_sense.py",
              file=sys.stderr)
        return 2
    if "--choices" in argv:
        print(render_choices())
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
