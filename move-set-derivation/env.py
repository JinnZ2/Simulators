#!/usr/bin/env python3
# env.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# Arm 1's environment: primitive physical relations, configurations
# composed from them, and an admissibility rule. Exhaustive and
# deterministic -- every configuration over the six primitives is
# enumerated, so no sampling decision sits under any number.
#
# THE ARM'S WHOLE VALIDITY, in the drop's own words:
#
#   NOVELTY MUST BE COMPOSITIONAL, NOT PRIMITIVE. Introducing an unseen
#   primitive measures knowledge. Recombining seen primitives measures
#   derivation.
#
# So it is asserted rather than intended: `compositional_only()` returns
# the primitives appearing in test and not in training, and the selftest
# requires that set to be empty. A generator that leaked one unseen
# primitive would measure knowledge and report it as derivation.

import itertools

PRIMITIVES = ("support", "containment", "friction", "leverage",
              "flow", "thermal")

GOALS = ("stabilize", "transfer", "contain", "release", "cool", "lift")

# A move requires a set of primitives and achieves one goal. Nothing
# here is a claim about physics -- the relations are labels on a
# combinatorial structure, and the arm measures derivation over that
# structure. Reading them as mechanics would be reading a name.
MOVES = {
    "wedge":         (("friction", "leverage"), "stabilize"),
    "brace":         (("support", "friction"), "stabilize"),
    "shim":          (("support", "leverage", "friction"), "stabilize"),
    "siphon":        (("flow", "containment"), "transfer"),
    "pour":          (("flow", "support"), "transfer"),
    "decant":        (("flow", "containment", "leverage"), "transfer"),
    "cap":           (("containment", "friction"), "contain"),
    "seal_thermal":  (("containment", "thermal"), "contain"),
    "dam":           (("flow", "friction"), "contain"),
    "vent":          (("flow", "thermal"), "release"),
    "lever_release": (("leverage", "containment"), "release"),
    "pry":           (("leverage", "support"), "lift"),
    "winch":         (("leverage", "friction", "support"), "lift"),
    "radiate":       (("thermal", "flow"), "cool"),
    "conduct":       (("thermal", "support"), "cool"),
    "quench":        (("thermal", "flow", "containment"), "cool"),
}


def all_configs():
    """Every (primitive set, goal) over the six primitives. 384 of them.

    Exhaustive rather than sampled, so no seed and no draw sits under a
    reported rate."""
    out = []
    for r in range(len(PRIMITIVES) + 1):
        for combo in itertools.combinations(PRIMITIVES, r):
            for g in GOALS:
                out.append((frozenset(combo), g))
    return out


def admissible(config):
    """Moves whose requirements are met and whose goal is the config's."""
    present, goal = config
    return tuple(sorted(
        m for m, (req, g) in MOVES.items()
        if g == goal and set(req) <= present))


def is_null(config):
    """A configuration with NO admissible move.

    The drop calls the null rate the measure to protect if anything is
    cut. These are the seeds it needs, and they exist in the space
    rather than being injected: a goal with no move whose requirements
    the configuration meets."""
    return not admissible(config)


# ------------------------------------------------------------ the split

# [CHOICE] The training family. Configurations whose primitive set is a
# subset of one of these. Chosen to cover every primitive at least twice
# -- so no primitive is unseen, which is the arm's validity condition --
# while leaving most PAIRS of primitives never co-present.
TRAIN_FAMILIES = (
    frozenset(("support", "friction")),
    frozenset(("flow", "containment")),
    frozenset(("thermal", "leverage")),
    frozenset(("support", "thermal")),
    frozenset(("friction", "flow")),
    frozenset(("containment", "leverage")),
)


def train_configs():
    """Configurations inside the training families, with any goal."""
    out = []
    for fam in TRAIN_FAMILIES:
        for r in range(len(fam) + 1):
            for combo in itertools.combinations(sorted(fam), r):
                for g in GOALS:
                    c = (frozenset(combo), g)
                    if c not in out:
                        out.append(c)
    return out


def test_configs():
    """Everything not in training. Compositional novelty by construction:
    the primitives are all seen, the combinations are not."""
    tr = set(train_configs())
    return [c for c in all_configs() if c not in tr]


def compositional_only():
    """Primitives appearing in test and never in training.

    MUST BE EMPTY. This is the arm's stated validity condition, returned
    as a value rather than left as an intention, and asserted in the
    selftest. Non-empty means the arm measures knowledge and reports it
    as derivation."""
    seen = set()
    for p, _g in train_configs():
        seen |= set(p)
    unseen = set()
    for p, _g in test_configs():
        unseen |= (set(p) - seen)
    return sorted(unseen)


# ------------------------------------- the discriminator's two variables

def similarity(config, train=None):
    """Max Jaccard between this config's primitive set and any training
    config's. The 'similarity-to-nearest-training-configuration' term."""
    train = train or train_configs()
    p = config[0]
    best = 0.0
    for tp, _g in train:
        u = len(p | tp)
        if u == 0:
            j = 1.0
        else:
            j = len(p & tp) / float(u)
        if j > best:
            best = j
    return round(best, 6)


def recombination_depth(config, families=None):
    """Minimum number of TRAIN_FAMILIES whose union covers this config's
    primitive set, minus one.

      0 -> the set sits inside a single family; nothing was recombined
      1 -> it takes two families
      2 -> three, and so on
      None -> not coverable at all (cannot occur here; every primitive
              appears in some family, and that is asserted)

    A set cover, computed exactly by exhaustive search over subsets of
    six families rather than greedily, because a greedy cover can
    overstate depth and depth is one of the two regressors."""
    families = families or TRAIN_FAMILIES
    p = config[0]
    if not p:
        return 0
    for k in range(1, len(families) + 1):
        for combo in itertools.combinations(families, k):
            u = set()
            for f in combo:
                u |= f
            if p <= u:
                return k - 1
    return None


def _render():
    """The environment, so what the arm is built on is readable without
    importing anything."""
    out = ["THE COMPOSITIONAL-NOVELTY ENVIRONMENT", ""]
    out.append("  primitives (%d): %s" % (len(PRIMITIVES),
                                          ", ".join(PRIMITIVES)))
    out.append("  goals (%d): %s" % (len(GOALS), ", ".join(GOALS)))
    out.append("")
    out.append("  moves (%d):" % len(MOVES))
    for m in sorted(MOVES):
        req, g = MOVES[m]
        out.append("    %-14s %-34s -> %s" % (m, " + ".join(req), g))
    out.append("")
    out.append("  training families (%d):" % len(TRAIN_FAMILIES))
    for f in TRAIN_FAMILIES:
        out.append("    %s" % " + ".join(sorted(f)))
    out.append("")
    a, t, e = all_configs(), train_configs(), test_configs()
    out.append("  configurations: %d enumerated exhaustively" % len(a))
    out.append("    training %d   test %d" % (len(t), len(e)))
    out.append("    no-admissible-move seeds in test: %d"
               % sum(1 for c in e if is_null(c)))
    out.append("")
    out.append("  COMPOSITIONAL NOVELTY -- primitives in test and never")
    out.append("  in training: %s" % (compositional_only() or "none"))
    out.append("  The drop calls this the arm's whole validity, so it is")
    out.append("  a returned value and a selftest assertion rather than")
    out.append("  an intention.")
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv[1:]:
        # A silent exit 0 here would be a pass on an invocation that runs
        # nothing. env.py has no checks of its own; they live next door.
        sys.stderr.write(
            "env.py has no checks of its own. The checks that exercise "
            "it live in selftest_msd.py.\n"
            "    python3 move-set-derivation/selftest_msd.py\n")
        sys.exit(2)
    print(_render())
