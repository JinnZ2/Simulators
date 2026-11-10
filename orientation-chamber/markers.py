"""markers.py -- marks an agent may place in the chamber. CC0, stdlib only.

PROPOSED | co-authored (JinnZ2 + Claude). Placing marks is optional.

A mark sits at the TRUE cell the agent occupies when it places it, and the
agent senses marks in the cell it is actually in. That is a channel separate
from the reported position, so marks keep working when `delay` makes the
report lag; whether they help depends on whether the agent's model of what
an action does is right (under flip_x, "go E to an unmarked cell" leads W).

Types:
  FADING    strength starts at FADE_LIFE and drops by 1 per chamber step;
            gone at 0
  LANDMARK  stores the cell's distances to the four fixed edges; relocalize()
            reads the OFFSET between that record and the current cell
  REPEL     "already searched here"; persistent
  VOID      a cleared patch: the cell and its 4 neighbours read as searched
  PLACED    a persistent object; carries a note, no search meaning

usage_counts() reports which types were used. search_trial() runs one seeded
searcher with a given mark type (or none) and reports its re-search rate:
re-visits of an already-visited cell over all visits. That is a reading of
one searcher in one chamber, not a rating of the mark type.
"""
import random

from chamber import ACTIONS, Chamber

TYPES = ("FADING", "LANDMARK", "REPEL", "VOID", "PLACED")
SEARCH_MEANING = ("FADING", "REPEL", "VOID")
FADE_LIFE = 6  # [CHOICE 2] steps a FADING mark lasts; stipulated


class Markers:
    def __init__(self, chamber):
        self.ch = chamber
        self.marks = []          # dicts: type, cell, placed_at, note, (life | edges)
        self._seen_step = len(chamber.trace)

    def _tick(self):
        now = len(self.ch.trace)
        for m in self.marks:
            if m["type"] == "FADING":
                m["life"] = max(0, m["life"] - (now - self._seen_step))
        self._seen_step = now

    def place(self, kind, note=None):
        if kind not in TYPES:
            raise ValueError("mark type %r not in %s" % (kind, TYPES))
        self._tick()
        cell = self.ch.pos
        m = {"type": kind, "cell": cell, "placed_at": len(self.ch.trace) - 1, "note": note}
        if kind == "FADING":
            m["life"] = FADE_LIFE
        if kind == "LANDMARK":
            m["edges"] = self.edges(cell)
        self.marks.append(m)
        return m

    def edges(self, cell):
        n = self.ch.size - 1
        return {"W": cell[0], "E": n - cell[0], "S": cell[1], "N": n - cell[1]}

    def here(self, cell=None):
        self._tick()
        cell = self.ch.pos if cell is None else cell
        return [m for m in self.marks if m["cell"] == cell and not (m["type"] == "FADING" and m["life"] == 0)]

    def searched(self, cell):
        """True if a FADING / REPEL / VOID mark says this cell was searched."""
        self._tick()
        for m in self.marks:
            if m["type"] not in SEARCH_MEANING or (m["type"] == "FADING" and m["life"] == 0):
                continue
            if m["cell"] == cell:
                return True
            if m["type"] == "VOID" and abs(m["cell"][0] - cell[0]) + abs(m["cell"][1] - cell[1]) == 1:
                return True
        return False

    def relocalize(self, landmark):
        """OFFSET between a LANDMARK's stored edge distances and the current cell's."""
        now = self.edges(self.ch.pos)
        return {k: now[k] - landmark["edges"][k] for k in now}

    def usage_counts(self):
        return {t: sum(1 for m in self.marks if m["type"] == t) for t in TYPES}


def _plain_next(pos, a, size):
    dx, dy = ACTIONS[a]
    return (min(max(pos[0] + dx, 0), size - 1), min(max(pos[1] + dy, 0), size - 1))


def search_trial(seed, mark=None, steps=60, rules=None):
    """One seeded searcher. With `mark`, it places that mark each step and prefers
    actions whose plain-physics next cell (from the TRUE cell) is not marked searched.
    Returns visits, re-visits and the re-search rate. Same chamber and RNG either way."""
    if mark is not None and mark not in SEARCH_MEANING:
        raise ValueError("search_trial uses a mark with search meaning: %s" % (SEARCH_MEANING,))
    ch = Chamber(seed=seed, rules=rules, start=None)
    mk = Markers(ch)
    rng = random.Random(seed * 7919 + 1)
    moves = ("N", "S", "E", "W")
    visited, revisits = {ch.pos}, 0
    for _ in range(steps):
        if mark is not None:
            mk.place(mark)
        order = list(moves)
        rng.shuffle(order)
        if mark is not None:
            fresh = [a for a in order if not mk.searched(_plain_next(ch.pos, a, ch.size))]
            order = fresh + [a for a in order if a not in fresh]
        ch.step(order[0])
        if ch.pos in visited:
            revisits += 1
        visited.add(ch.pos)
    return {"mark": mark or "none", "visits": steps, "revisits": revisits,
            "re_search_rate": revisits / float(steps), "cells_seen": len(visited),
            "usage": mk.usage_counts()}


def compare_marks(seed, steps=60, rules=None):
    """re-search rate without marks and with each search-meaning mark; same seed throughout."""
    return [search_trial(seed, m, steps, rules) for m in (None,) + SEARCH_MEANING]


def render(rows):
    from common import header
    L = [header(), "", "re-search rate by mark type (one seeded searcher; a reading, not a rating)"]
    for r in rows:
        L.append("  %-8s visits %3d  revisits %3d  rate %.3f  cells seen %2d"
                 % (r["mark"], r["visits"], r["revisits"], r["re_search_rate"], r["cells_seen"]))
    return "\n".join(L)


if __name__ == "__main__":
    import sys
    a = sys.argv[1:]
    if a and (a[0].startswith("-") and a[0] != "--seed"):
        print("usage: python3 markers.py [--seed N]   (tests: python3 tests/test_chamber.py)")
        sys.exit(2)
    seed = int(a[1]) if a[:1] == ["--seed"] else 7
    print(render(compare_marks(seed)))
