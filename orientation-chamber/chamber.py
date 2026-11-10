"""chamber.py -- a grid world with a hidden rule set. CC0, stdlib only.

PROPOSED | co-authored (JinnZ2 + Claude). Nothing here grades anything.

Actions: N, S, E, W, WAIT. The agent does not see the rules; it sees only the
reported position after each action.

Rules (each on or off, chosen from the seed unless given):
  flip_x     E and W are swapped
  flip_y     N and S are swapped
  wrap       crossing an edge re-enters on the far side (off: the edge stops you)
  sticky     touching an edge holds you one extra step: the next action is not applied
  momentum   a WAIT right after a move carries you one more cell in that direction
  delay      the reported position lags the true one by `delay_steps` steps

The chamber keeps the true position and the reported one apart. `reveal()`
returns the rule set; using it is optional and nothing compares against it.
"""
import random

ACTIONS = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0), "WAIT": (0, 0)}
RULE_NAMES = ("flip_x", "flip_y", "wrap", "sticky", "momentum", "delay")


class Chamber:
    def __init__(self, seed=0, size=7, rules=None, delay_steps=None, start=None):
        rng = random.Random(seed)
        if rules is None:
            rules = {r: rng.random() < 0.5 for r in RULE_NAMES}
        else:
            rules = {r: bool(rules.get(r, False)) for r in RULE_NAMES}
        self.rules = rules
        self.delay_steps = (delay_steps if delay_steps is not None else rng.choice((1, 2))) if rules["delay"] else 0
        self.size = size
        self.seed = seed
        self.pos = tuple(start) if start else (size // 2, size // 2)
        self.last_move = (0, 0)
        self.held = 0
        self.trace = [self.pos]

    def reveal(self):
        return {"rules": dict(self.rules), "delay_steps": self.delay_steps, "size": self.size,
                "seed": self.seed}

    def _vector(self, action):
        if action not in ACTIONS:
            raise ValueError("action %r is not one of %s" % (action, sorted(ACTIONS)))
        dx, dy = ACTIONS[action]
        if self.rules["flip_x"]:
            dx = -dx
        if self.rules["flip_y"]:
            dy = -dy
        return dx, dy

    def _move(self, dx, dy):
        x, y = self.pos[0] + dx, self.pos[1] + dy
        edge = not (0 <= x < self.size and 0 <= y < self.size)
        if edge:
            if self.rules["wrap"]:
                x, y = x % self.size, y % self.size
            else:
                x = min(max(x, 0), self.size - 1)
                y = min(max(y, 0), self.size - 1)
        return (x, y), edge

    def step(self, action):
        """Apply one action; return the REPORTED position."""
        dx, dy = self._vector(action)
        if self.held:
            self.held -= 1
            dx, dy = 0, 0
        elif action == "WAIT" and self.rules["momentum"]:
            dx, dy = self.last_move
        self.pos, edge = self._move(dx, dy)
        if edge and self.rules["sticky"]:
            self.held = 1
        self.last_move = (dx, dy) if action != "WAIT" else (0, 0)
        self.trace.append(self.pos)
        return self.reported()

    def reported(self):
        k = len(self.trace) - 1 - self.delay_steps
        return self.trace[max(k, 0)]
