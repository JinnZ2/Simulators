#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
draw_frame -- D-C1 of WORK ORDER M revision 2.

Rev 1 seeded Arm A's corpus from recall, and five of the twelve seeds
failed the order's own admission rule: they were reversed or did not exist
before Y. A list drawn by recalling memorable reversals is selected on the
variable under test, and the selection cannot be declared because recall
has no frame. This module replaces it with a DECLARED draw:

  1. one Y-vintage indexed source, fixed before the draw (a textbook
     edition, a guideline set, a review index as of Y) -- recorded as
     source_id, edition, index_size
  2. rows drawn BY POSITION from a seeded RNG, the seed recorded
  3. fate adjudicated AFTER the draw, by a rule written BEFORE it
     (the fate_rule string, hashed into the frame id)
  4. frame bias is then declarable; recall bias never is

The output is a frame_declaration block that Arm A requires (HARD GATE in
revision_survival.score_arm_a): no block, no score; a row whose position
is not in the draw, no score.

WHAT THIS FILE DOES NOT DO. It does not draw from a real source. No
Y-vintage index is reachable from this environment (egress allowlist), and
the dispatch forbids populating the corpus from model recall, including
this session's. So `draw()` produces positions and a declaration and the
rows they name are the operator's to look up. The shipped run carries NO
frame and Arm A refuses on that, which is the correct outcome.

Python 3.9, ASCII only, stdlib only. Refuses --selftest; the checks live
in test_revision.py.
"""

from __future__ import annotations

import hashlib
import json
import random
import sys


class RefusedFrame(ValueError):
    """Raised on a draw that cannot be declared."""


REQUIRED = ("source_id", "edition", "index_size", "rng_seed", "n",
            "positions", "fate_rule", "frame_id")


def draw(source_id, edition, index_size, rng_seed, n, fate_rule):
    """Return a frame_declaration dict. Positions are a sample without
    replacement from range(index_size) under random.Random(rng_seed), so
    the same inputs give the same positions on any machine (the stdlib
    Mersenne Twister is deterministic under a fixed seed). Sorted, so the
    order carries no information that could be read as a ranking."""
    if not isinstance(source_id, str) or not source_id.strip():
        raise RefusedFrame("source_id must be a non-empty string")
    if not isinstance(edition, str) or not edition.strip():
        raise RefusedFrame("edition must be a non-empty string (a source "
                           "without an edition is not Y-vintage)")
    if not isinstance(index_size, int) or isinstance(index_size, bool) \
            or index_size <= 0:
        raise RefusedFrame("index_size must be a positive int")
    if not isinstance(rng_seed, int) or isinstance(rng_seed, bool):
        raise RefusedFrame("rng_seed must be an int, recorded")
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise RefusedFrame("n must be a positive int")
    if n > index_size:
        raise RefusedFrame("n %d exceeds index_size %d" % (n, index_size))
    if not isinstance(fate_rule, str) or not fate_rule.strip():
        raise RefusedFrame("fate_rule must be stated before the draw")
    positions = sorted(random.Random(rng_seed).sample(range(index_size), n))
    body = {"source_id": source_id, "edition": edition,
            "index_size": index_size, "rng_seed": rng_seed, "n": n,
            "positions": positions, "fate_rule": fate_rule}
    body["frame_id"] = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=True).encode("ascii")).hexdigest()
    return body


def check_frame(frame):
    """Validate a declaration. Recomputes the frame_id, so an edited
    position list or fate rule no longer verifies. Returns the frame or
    raises RefusedFrame naming the field."""
    if not isinstance(frame, dict):
        raise RefusedFrame("frame_declaration absent")
    for k in REQUIRED:
        if k not in frame:
            raise RefusedFrame("frame_declaration missing %s" % k)
    redo = draw(frame["source_id"], frame["edition"], frame["index_size"],
                frame["rng_seed"], frame["n"], frame["fate_rule"])
    if redo["positions"] != list(frame["positions"]):
        raise RefusedFrame("positions do not reproduce from the seed")
    if redo["frame_id"] != frame["frame_id"]:
        raise RefusedFrame("frame_id does not verify")
    return frame


def in_draw(frame, position):
    """True iff `position` is one the declared draw produced. A row with
    no position is not in the draw; None is not a position."""
    if position is None or isinstance(position, bool) \
            or not isinstance(position, int):
        return False
    return position in set(frame["positions"])


def render(frame):
    out = ["frame_declaration",
           "  source_id   %s" % frame["source_id"],
           "  edition     %s" % frame["edition"],
           "  index_size  %d" % frame["index_size"],
           "  rng_seed    %d" % frame["rng_seed"],
           "  n           %d" % frame["n"],
           "  fate_rule   %s" % frame["fate_rule"],
           "  frame_id    %s" % frame["frame_id"],
           "  positions   %s" % " ".join(str(p) for p in frame["positions"])]
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("draw_frame.py carries no selftest; run "
                         "python3 test_revision.py\n")
        return 2
    args = {}
    for a in argv:
        if a.startswith("--") and "=" in a:
            k, v = a[2:].split("=", 1)
            args[k] = v
    need = ("source", "edition", "index-size", "seed", "n", "fate-rule")
    if not all(k in args for k in need):
        sys.stderr.write("usage: draw_frame.py --source=ID --edition=E "
                         "--index-size=N --seed=S --n=K --fate-rule=TEXT\n"
                         "no draw is shipped: no Y-vintage index is "
                         "reachable here and recall is forbidden (D-C1)\n")
        return 2
    try:
        f = draw(args["source"], args["edition"], int(args["index-size"]),
                 int(args["seed"]), int(args["n"]), args["fate-rule"])
    except (RefusedFrame, ValueError) as e:
        sys.stderr.write("refused: %s\n" % e)
        return 1
    sys.stdout.write(render(f))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
