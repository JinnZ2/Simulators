#!/usr/bin/env python3
"""Is the vote tally identical under E1-E5, and do M1-M6 separate them?

MARKER.md states: "A vote tally is identical under all five." That is a
claim about an instrument and it is simulable, so it is simulated here
rather than agreed with.

Five generators, one per explanation, each constructed to produce a high
FOR rate and to differ in the way the marker describes. Every metric is
computed identically across all five. Two explanations count as SEPARATED
by a metric when their ranges across seeds do not overlap.

WHAT THIS IS NOT. It is not a model of Emergence World, and no number here
is evidence about that run or about any model's governance. The generators
are constructed to have the properties E1-E5 name; showing that a metric
cannot tell constructed processes apart is a statement about the metric.

DECLARED INTEREST. This module is written by a Claude instance, and the
marker's trigger case is a criterion applied to a Claude run with an
unfavourable disposition. The instrument question below is neutral --
it asks whether a statistic separates five processes, and the answer does
not depend on which model was governing. The ASYMMETRY question is not
neutral and is not scored here or anywhere in this folder. See
AUDIT_NOTES.md.

stdlib only. CC0. Parses under Python 3.9.

    python3 separability.py
    python3 separability.py --selftest
"""

import itertools
import math
import random
import sys

# Shape taken from the trigger case so the arithmetic is at the right
# scale. [CHOICE] 332 votes over 58 proposals with 10 agents means not
# every agent voted on every proposal; participation is modelled as a
# per-agent-per-proposal rate that reproduces the total.
PROPOSALS = 58
AGENTS = 10
TARGET_VOTES = 332
PARTICIPATION = TARGET_VOTES / float(PROPOSALS * AGENTS)

EPS = 0.02          # a position "changed" if it moved more than this
SEEDS = 12
EXPLANATIONS = ("E1", "E2", "E3", "E4", "E5")


def _clip(x):
    return min(1.0, max(0.0, x))


def _sd(xs):
    n = len(xs)
    if n < 2:
        return 0.0
    m = sum(xs) / n
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


def _corr(xs, ys):
    n = len(xs)
    if n < 2:
        return float("nan")
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    dx = math.sqrt(sum((a - mx) ** 2 for a in xs))
    dy = math.sqrt(sum((b - my) ** 2 for b in ys))
    if dx == 0 or dy == 0:
        return float("nan")
    return num / (dx * dy)


# --------------------------------------------------------------------------
# generators
#
# Each returns a list of proposals. A proposal carries the positions at
# discussion start, the positions at the vote, the votes cast, how many
# rounds it took, and whether it was amended.
# --------------------------------------------------------------------------

def _participate(rng):
    return rng.random() < PARTICIPATION


# All five generators are calibrated to the SAME tally, because 98% FOR is
# the observation they are explanations OF. Without that the comparison is
# between five arbitrary processes rather than five readings of one number.
# `LEAK` is the residual against-rate every generator carries.
FOR_TARGET = 0.98
LEAK = 0.02


def _gen(rng, move, force_for=None, start_sd=0.25, quality=(0.30, 0.90),
         amend=True, rounds_fn=None, lam=0.8, anchor="mean"):
    out = []
    for _j in range(PROPOSALS):
        q = rng.uniform(*quality)
        amended = False
        for _attempt in range(2):
            pos0 = [_clip(rng.gauss(q, start_sd)) for _ in range(AGENTS)]
            if move:
                if anchor == "mean":
                    target = sum(pos0) / AGENTS
                else:
                    # [CHOICE] the first mover is the PROPOSER, and a
                    # proposer proposes what they support. Anchoring to a
                    # random agent's draw made E2 converge to an AGAINST
                    # position on half the proposals and produce a 0.56 FOR
                    # rate -- which stops it being an explanation of a
                    # high-agreement tally at all. Caught by the selftest's
                    # own precondition, not by reading. Recorded in
                    # AUDIT_NOTES.md.
                    target = rng.uniform(0.60, 0.95)
                pos1 = [_clip(p + lam * (target - p)) for p in pos0]
            else:
                pos1 = list(pos0)
            if force_for is None:
                votes = [(1 if p > 0.5 else 0) for p in pos1]
            elif force_for == "always":
                votes = [1 for _ in pos1]
            else:                                     # stochastic, uncoupled
                votes = [(1 if rng.random() < force_for else 0) for _ in pos1]
            # calibration leak, applied identically to all five
            votes = [(0 if (v == 1 and rng.random() < LEAK) else v)
                     for v in votes]
            cast = [(i, votes[i]) for i in range(AGENTS) if _participate(rng)]
            passed = (sum(v for _i, v in cast) > len(cast) / 2.0) if cast \
                else False
            if passed or not amend:
                break
            q = min(0.95, q + 0.30)                   # amend and retry
            amended = True
        rounds = rounds_fn(rng) if rounds_fn else 1
        out.append({"pos0": pos0, "pos1": pos1, "cast": cast,
                    "passed": passed, "amended": amended, "rounds": rounds})
    return out


def e1(rng):
    """Converged deliberation. Dispersed start, positions move and meet."""
    return _gen(rng, move=True, lam=0.80, anchor="mean",
                quality=(0.55, 0.90), start_sd=0.25,
                rounds_fn=lambda r: r.randint(3, 8))


def e2(rng):
    """Coupling-dominant. Coherence is the function; aligns fast, to a mover."""
    return _gen(rng, move=True, lam=0.97, anchor="first", amend=False,
                quality=(0.30, 0.90), start_sd=0.25,
                rounds_fn=lambda r: r.randint(1, 3))


def e3(rng):
    """Aligned objectives. Already together; nothing to deliberate over."""
    return _gen(rng, move=False, start_sd=0.05, quality=(0.72, 0.95),
                amend=False, rounds_fn=lambda r: r.randint(1, 2))


def e4(rng):
    """No dissent channel. Positions stay dispersed; the vote is forced."""
    return _gen(rng, move=False, force_for="always", amend=False,
                rounds_fn=lambda r: r.randint(1, 3))


def e5(rng):
    """Compliance. Positions unchanged, vote unconnected to position."""
    return _gen(rng, move=False, force_for=1.0, amend=False,
                rounds_fn=lambda r: r.randint(1, 3))


GENERATORS = {"E1": e1, "E2": e2, "E3": e3, "E4": e4, "E5": e5}


# --------------------------------------------------------------------------
# metrics -- the tally, then the marker's own M1-M6
# --------------------------------------------------------------------------

def tally(props):
    """The published statistic: fraction of cast votes that are FOR."""
    cast = [v for p in props for _i, v in p["cast"]]
    return sum(cast) / float(len(cast)) if cast else float("nan")


def m1_amendment_rate(props):
    return sum(1 for p in props if p["amended"]) / float(len(props))


def m2_dispersion_ratio(props):
    """sd at the vote over sd at discussion start. Convergence < 1."""
    a = [_sd(p["pos0"]) for p in props]
    b = [_sd(p["pos1"]) for p in props]
    ma = sum(a) / len(a)
    return (sum(b) / len(b)) / ma if ma > 0 else float("nan")


def m2b_dispersion_at_vote(props):
    return sum(_sd(p["pos1"]) for p in props) / float(len(props))


def m3_failed(props):
    return sum(1 for p in props if not p["passed"])


def m4_minority_adopted(props):
    """Proposals passing where the pre-discussion majority was against."""
    n = 0
    for p in props:
        pre_for = sum(1 for x in p["pos0"] if x > 0.5)
        if p["passed"] and pre_for <= AGENTS / 2.0:
            n += 1
    return n


def m5_mean_rounds(props):
    return sum(p["rounds"] for p in props) / float(len(props))


def m6_position_change_rate(props):
    tot = mov = 0
    for p in props:
        for a, b in zip(p["pos0"], p["pos1"]):
            tot += 1
            if abs(b - a) > EPS:
                mov += 1
    return mov / float(tot) if tot else 0.0


def vote_position_coupling(props):
    """NOT in the marker's list. Derived, and it is what E5 is defined by."""
    xs, ys = [], []
    for p in props:
        for i, v in p["cast"]:
            xs.append(p["pos1"][i])
            ys.append(float(v))
    return _corr(xs, ys)


METRICS = [
    ("tally (published)", tally),
    ("M1 amendment rate", m1_amendment_rate),
    ("M2 dispersion ratio", m2_dispersion_ratio),
    ("M2b dispersion at vote", m2b_dispersion_at_vote),
    ("M3 proposals failed", m3_failed),
    ("M4 minority adopted", m4_minority_adopted),
    ("M5 mean rounds", m5_mean_rounds),
    ("M6 position change rate", m6_position_change_rate),
    ("vote-position coupling", vote_position_coupling),
]


# --------------------------------------------------------------------------
# separation
# --------------------------------------------------------------------------

def distributions(seeds=SEEDS):
    out = {}
    for name, gen in GENERATORS.items():
        rows = {label: [] for label, _fn in METRICS}
        for s in range(seeds):
            props = gen(random.Random(7000 + s))
            for label, fn in METRICS:
                rows[label].append(fn(props))
        out[name] = rows
    return out


def separates(dist, label, a, b):
    """Do the two ranges across seeds fail to overlap?"""
    xa = [v for v in dist[a][label] if v == v]
    xb = [v for v in dist[b][label] if v == v]
    if not xa or not xb:
        return False
    return max(xa) < min(xb) or max(xb) < min(xa)


PAIRS = list(itertools.combinations(EXPLANATIONS, 2))


def separation_table(dist):
    out = {}
    for label, _fn in METRICS:
        out[label] = [p for p in PAIRS if separates(dist, label, *p)]
    return out


def unseparated_by_marker_list(dist):
    """Pairs no M1-M6 metric separates. The tally and the derived one
    are excluded: the first is the statistic under test, the second is
    not in the marker's list."""
    marker = [l for l, _f in METRICS if l.startswith("M")]
    table = separation_table(dist)
    covered = set()
    for l in marker:
        covered.update(table[l])
    return [p for p in PAIRS if p not in covered]


# --------------------------------------------------------------------------

def report():
    print("SEPARABILITY OF E1-E5 -- is the vote tally identical under all?\n")
    print("Not a model of any real run. Five constructed processes with the")
    print("properties the marker names, and one question: which statistics")
    print("tell them apart. %d seeds each.\n" % SEEDS)

    dist = distributions()
    print("%-25s %s" % ("metric", "  ".join("%-9s" % e for e in EXPLANATIONS)))
    print("-" * 78)
    for label, _fn in METRICS:
        cells = []
        for e in EXPLANATIONS:
            xs = [v for v in dist[e][label] if v == v]
            cells.append("%-9s" % ("%.2f-%.2f" % (min(xs), max(xs))
                                   if xs else "--"))
        print("%-25s %s" % (label, "  ".join(cells)))
    print()

    table = separation_table(dist)
    print("pairs separated, of %d:" % len(PAIRS))
    for label, _fn in METRICS:
        got = table[label]
        print("  %-25s %2d   %s" % (label, len(got),
                                    " ".join("%s/%s" % p for p in got)))
    print()

    t = table["tally (published)"]
    print("THE MARKER'S CLAIM: 'A vote tally is identical under all five.'")
    print("  pairs the tally separates: %d of %d" % (len(t), len(PAIRS)))
    if not t:
        print("  Holds -- and PARTLY BY CONSTRUCTION, which is worth saying")
        print("  plainly. All five are calibrated to the same tally, because")
        print("  98%% FOR is the observation they are explanations OF. Once")
        print("  that precondition is met the tally cannot separate them and")
        print("  the claim is close to analytic.")
        print("  What is NOT analytic is that the precondition is reachable")
        print("  at all: each of the five had to be shown capable of")
        print("  producing a high-agreement tally, and one of them was not")
        print("  on the first construction. E2 anchored to a random agent")
        print("  converged to an AGAINST position half the time and returned")
        print("  0.56. It needs the proposer to support their own proposal.")
        print("  So the observation is reachable from all five, and the")
        print("  statistic is NO_DISCRIMINATION across them in")
        print("  `null-harness` terms: a reading taken from it is the")
        print("  reader's prior with a number attached.")
    else:
        print("  NOT confirmed here; the tally separated %s" % t)
    print()

    left = unseparated_by_marker_list(dist)
    print("AND AN AUDIT OF THE MARKER'S OWN INSTRUMENT")
    print("  pairs NO M1-M6 metric separates: %d of %d   %s"
          % (len(left), len(PAIRS), " ".join("%s/%s" % p for p in left)))
    print()
    if left:
        print("  M1-M6 is a real improvement on the tally and it is not a")
        print("  complete instrument. The pairs above stay tied, and the")
        print("  marker lists them as distinct explanations with different")
        print("  consequences -- E1 and E2 are both 'not defects', E4 is")
        print("  'an architecture finding' and E5 is 'the published")
        print("  reading', so a residual tie between E4 and E5 is the one")
        print("  that matters most.")
        print()
    vp = table["vote-position coupling"]
    print("  A PREDICTION THIS MODULE MADE AND THE RUN REFUTED. E5 is")
    print("  DEFINED as 'vote unconnected to position', so a direct")
    print("  vote-position coupling was expected to be the statistic that")
    print("  breaks the tie. It separates %d pairs." % len(vp))
    print("  The reason is structural rather than incidental: at 98%% FOR")
    print("  the vote has almost no variance, so nothing can correlate with")
    print("  it. ANY statistic built on the vote side is dead at a")
    print("  high-agreement tally, by the same arithmetic that makes the")
    print("  tally uninformative.")
    print("  That is why M2 is the load-bearing measurement in the marker's")
    print("  list, and for a reason the marker does not state: it reads the")
    print("  POSITION side, which still has variance when the vote side has")
    print("  none.")
    print()
    print("  WHAT WOULD SEPARATE E4 FROM E5. Nothing observational on the")
    print("  vote record. The difference is whether a route EXISTS for a")
    print("  minority position to become an outcome, not whether anyone")
    print("  took it, and a record in which nobody took it looks the same")
    print("  either way. Separating them needs the channel tested: inject a")
    print("  minority position and see whether it can become an outcome.")
    print("  That is an intervention, and every measurement in the marker's")
    print("  list is an observation. SHAPE_SPEC section 4's removal test in")
    print("  a different substrate -- you have to remove the constraint,")
    print("  not read the residue harder.")
    print()


def selftest():
    fails = []
    dist = distributions(seeds=8)

    # every generator must actually produce a high FOR rate, or the five
    # are not five explanations OF THE SAME OBSERVATION.
    for e in EXPLANATIONS:
        lo = min(dist[e]["tally (published)"])
        if lo < 0.85:
            fails.append("%s produces a FOR rate of %.2f; it is not an "
                         "explanation of a high-agreement tally" % (e, lo))

    # the marker's claim: the tally must separate nothing.
    t = separation_table(dist)["tally (published)"]
    if t:
        fails.append("the tally now separates %s; the marker's central "
                     "claim must be restated" % (t,))

    # ...and the M list must separate SOMETHING, or this file is
    # CONSTANT_SILENT and shows nothing.
    covered = set()
    for label, _fn in METRICS:
        if label.startswith("M"):
            covered.update(separation_table(dist)[label])
    if not covered:
        fails.append("no M1-M6 metric separates any pair; the module cannot "
                     "return a positive and shows nothing")

    # ...and something must stay tied, or the audit finding is wrong.
    left = unseparated_by_marker_list(dist)
    if not left:
        fails.append("M1-M6 now separates every pair; the audit finding "
                     "must be restated")

    # the refuted prediction: vote-side statistics must stay dead at a
    # high-agreement tally, or the structural reading is wrong.
    if separation_table(dist)["vote-position coupling"]:
        fails.append("vote-position coupling now separates pairs; the "
                     "'vote side has no variance' reading must be restated")
    # E4/E5 must stay tied, or the audit finding is wrong.
    if ("E4", "E5") not in unseparated_by_marker_list(dist):
        fails.append("M1-M6 now separates E4 from E5; the finding that the "
                     "tie is between the architecture reading and the "
                     "published one must be restated")

    # the generators must be distinguishable in principle, or the whole
    # construction is degenerate.
    if len(covered) < 4:
        fails.append("only %d of %d pairs separable at all; the five "
                     "constructions are too alike to test anything"
                     % (len(covered), len(PAIRS)))

    for f in fails:
        print("FAIL: " + f)
    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
