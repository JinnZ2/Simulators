"""
interaction_class.py -- import shim. CC0.

Canonical module: threshold-states/interaction.py. This file holds no
logic of its own. It was built separately on 2026-10-07 and consolidated
onto the canonical module the same day. Every name below is the canonical
object, not a copy.

Behaviour that changed in the consolidation (root build -> canonical):
- joint absent (None): was UNRATED, now raises InteractionError.
- one separate response: was BELOW_RESOLUTION, now raises InteractionError
  (an interaction needs two or more cues).
- separate None: was ValueError, now TypeError from list(None).
- classify() returns a dict (relation, step, S, M, I, tol), not a
  (label, detail) tuple. bands() is replaced by rows(joint, S, M, tol).

Stdlib only. Library module: refuses --selftest (exit 2); the checks are
test_interaction_class.py (root) and threshold-states/test_interaction.py.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CANON = os.path.join(_HERE, "threshold-states")
if _CANON not in sys.path:
    sys.path.insert(0, _CANON)

import interaction as _canon  # noqa: E402

CANONICAL_PATH = "threshold-states/interaction.py"

UNRATED = _canon.UNRATED
BELOW_RESOLUTION = _canon.BELOW_RESOLUTION
REDUNDANT = _canon.REDUNDANT
ADDITIVE = _canon.ADDITIVE
RESONANT = _canon.RESONANT
ENHANCED_SUBADDITIVE = _canon.ENHANCED_SUBADDITIVE
ANTAGONISTIC = _canon.ANTAGONISTIC
RELATIONS = _canon.RELATIONS
OPEN_CLASSES = _canon.OPEN_CLASSES
InteractionError = _canon.InteractionError
references = _canon.references
rows = _canon.rows
classify = _canon.classify


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        sys.stderr.write("interaction_class.py is a shim over %s; run: "
                         "python3 test_interaction_class.py\n" % CANONICAL_PATH)
        return 2
    sys.stderr.write(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
