#!/usr/bin/env python3
# arm1.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# Arm 1 run: four conditions, five measures, the null rate, and the
# similarity-versus-recombination regression the drop asks for.
#
# WHAT THIS IS AND IS NOT
#
#   The environment and the reference solvers are both authored here.
#   So a regression run against ONE hand-written solver returns the
#   author's architecture, not a capacity: a solver that composes will
#   load on recombination depth by construction, and one that looks up
#   a neighbour will load on similarity by construction.
#
#   That is why the solvers ship with DECLARED architectures and the
#   discriminator is run against all of them first. The question asked
#   here is not "does this system derive" -- nothing here is a system
#   under test -- it is "CAN THE DISCRIMINATOR TELL THEM APART", which
#   is null-harness's known-truth-first invariant applied to the arm's
#   own instrument before it is pointed at anything.
#
#   For the drop's actual target -- a trained model -- the architecture
#   is not authored by the experimenter and the discriminator does its
#   intended job. The known-answer run is what licenses that.
#
# The drop's reporting rules are enforced rather than followed:
# no composite is emitted (asserted over the AST), unmeasured cells read
# UNMEASURED and never pass, and the null rate is reported beside the
# admissibility it has to be paired with.

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import env as E  # noqa: E402

# Imported, not reimplemented: sim-span/three_column.py::ols, which is
# already registered in tools/known_answer.py with exact-fit cases.
_SIMSPAN = os.path.join(os.path.dirname(HERE), "sim-span")


def _ols():
    if _SIMSPAN not in sys.path:
        sys.path.insert(0, _SIMSPAN)
    import three_column
    return three_column.ols


UNMEASURED = "UNMEASURED"

# ------------------------------------------------- declared architectures

RETRIEVAL = "RETRIEVAL"
DERIVATION = "DERIVATION"
PLAUSIBLE = "PLAUSIBLE"
SILENT = "SILENT"

ARCHITECTURE = {
    RETRIEVAL: "find the nearest training configuration by Jaccard and "
               "emit ITS admissible moves. Cannot see the present "
               "configuration's own requirements.",
    DERIVATION: "check each move's requirements against the present "
                "primitive set. Never consults a neighbour.",
    PLAUSIBLE: "emit the moves most often admissible across training, "
               "regardless of the configuration. Never returns empty.",
    SILENT: "always return the empty set. Included because a perfect "
            "null rate is what silence scores, and the drop names the "
            "null rate as the measure to protect if anything is cut.",
}


def _train_frequency():
    counts = {}
    for c in E.train_configs():
        for m in E.admissible(c):
            counts[m] = counts.get(m, 0) + 1
    return sorted(counts, key=lambda m: (-counts[m], m))


_FREQ = _train_frequency()
_TRAIN = E.train_configs()


def solve(arch, config):
    """Ordered candidate moves. Order is the emission order, so the
    index of the first admissible one is the 'time to first admissible
    move' the drop asks for."""
    if arch == SILENT:
        return []
    if arch == DERIVATION:
        return list(E.admissible(config))
    if arch == PLAUSIBLE:
        return [m for m in _FREQ if E.MOVES[m][1] == config[1]]
    if arch == RETRIEVAL:
        p = config[0]
        best, bestj = None, -1.0
        for tc in _TRAIN:
            if tc[1] != config[1]:
                continue
            u = len(p | tc[0])
            j = 1.0 if u == 0 else len(p & tc[0]) / float(u)
            if j > bestj:
                best, bestj = tc, j
        return list(E.admissible(best)) if best else []
    raise ValueError(arch)


# ------------------------------------------------------- the conditions

ENUMERATED = "enumerated"
NOT_ENUMERATED = "not_enumerated"
DEADLINE = "not_enumerated+deadline"
IRREVERSIBLE = "not_enumerated+deadline+irreversible"

CONDITIONS = (ENUMERATED, NOT_ENUMERATED, DEADLINE, IRREVERSIBLE)

# [CHOICE] The deadline truncates the candidate stream to this many
# moves. Stated because the drop names a deadline and gives no value.
DEADLINE_K = 2


def emitted(arch, config, condition):
    """What the solver actually commits to under a condition.

    ENUMERATED is the drop's control arm: the admissible set is GIVEN,
    so every architecture scores identically and the arm is measuring
    nothing about derivation. That it is uninformative is the point of
    including it -- it is the baseline the other three are read
    against."""
    if condition == ENUMERATED:
        return list(E.admissible(config))
    cands = solve(arch, config)
    if condition == NOT_ENUMERATED:
        return cands
    if condition == DEADLINE:
        return cands[:DEADLINE_K]
    if condition == IRREVERSIBLE:
        return cands[:1]
    raise ValueError(condition)


# ---------------------------------------------------------- the measures

def measure(arch, condition, configs):
    """The five measures, kept apart. The drop forbids a composite and
    says the per-measure profile IS the dissociation being tested."""
    adm_num = adm_den = 0
    sizes = []
    first = []
    premature = 0
    premature_den = 0
    null_seeds = 0
    null_returned = 0
    for c in configs:
        truth = set(E.admissible(c))
        out = emitted(arch, c, condition)
        sizes.append(len(out))
        adm_num += sum(1 for m in out if m in truth)
        adm_den += len(out)
        if truth:
            idx = next((i for i, m in enumerate(out) if m in truth), None)
            first.append(idx)
        if E.is_null(c):
            null_seeds += 1
            if not out:
                null_returned += 1
        if condition == IRREVERSIBLE and truth:
            premature_den += 1
            if not out or out[0] not in truth:
                premature += 1
    got = [i for i in first if i is not None]
    return {
        "architecture": arch,
        "condition": condition,
        "n": len(configs),
        "mean_candidate_set": round(sum(sizes) / float(len(sizes)), 4)
        if sizes else UNMEASURED,
        "admissibility_fraction": round(adm_num / float(adm_den), 4)
        if adm_den else UNMEASURED,
        "admissibility_denominator": adm_den,
        "mean_time_to_first_admissible":
            round(sum(got) / float(len(got)), 4) if got else UNMEASURED,
        "reached_an_admissible_move": len(got),
        "of_configs_with_one": len(first),
        # NOT one of the drop's five. Added, and marked as added: the
        # admissibility fraction alone cannot separate a solver that
        # derives from one that retrieves conservatively, because a
        # solver emitting only what it is sure of scores 1.0000 on
        # admissibility while reaching a fraction of the configurations
        # that have a move. Coverage is the other side of that pair,
        # exactly as reaching-an-admissible-move is the other side of
        # the null rate.
        "coverage_ADDED": round(len(got) / float(len(first)), 4)
        if first else UNMEASURED,
        "premature_commitment_rate":
            round(premature / float(premature_den), 4)
            if premature_den else UNMEASURED,
        "null_seeds": null_seeds,
        "null_returned": null_returned,
        "null_rate": round(null_returned / float(null_seeds), 4)
        if null_seeds else UNMEASURED,
    }


NULL_PAIRING_NOTE = (
    "The drop says to protect the null rate if anything is cut, and it "
    "is right that a system which never returns empty is filling a slot. "
    "Cut to ONE measure it is gameable in the other direction: SILENT "
    "returns the empty set always and scores a null rate of 1.0000, the "
    "highest in the table, while reaching an admissible move zero "
    "times. "
    "So the null rate is not a measure that stands alone -- it is one "
    "side of a pair, and the other side is whether an admissible move "
    "is ever reached on the seeds that have one. Both are printed "
    "together for that reason, and neither is combined into a score.")


# ------------------------------------------------------ the discriminator

def score_vector(arch, condition, configs):
    """Per-config outcome for the regression: did the emitted set reach
    an admissible move. 1.0 or 0.0, and configs with no admissible move
    are EXCLUDED -- scoring a null seed as a success or a failure would
    put the null-rate question inside the regression, and they are
    different measures."""
    ys, sims, deps, kept = [], [], [], []
    for c in configs:
        truth = set(E.admissible(c))
        if not truth:
            continue
        out = emitted(arch, c, condition)
        ys.append(1.0 if any(m in truth for m in out) else 0.0)
        sims.append(E.similarity(c, _TRAIN))
        deps.append(float(E.recombination_depth(c)))
        kept.append(c)
    return ys, sims, deps, kept


# [CHOICE] Permutation null. The drop's discriminator says "if
# similarity carries it ... if recombination depth carries it" and gives
# no test for whether EITHER carries anything. Without one, a
# single-predictor run -- which is what the matched band forces -- can
# only ever return "X carries", because X is the only candidate. On a
# RETRIEVAL solver the matched band would then report DEPTH_CARRIES,
# which is the derivation verdict, on r-squared 0.0009.
#
# So r-squared is scored against the distribution it takes when the
# outcome is shuffled against the regressors. Deterministic, stdlib, no
# threshold constant: the null supplies the bar.
PERM_N = 400
PERM_SEED = 20260829
PERM_Q = 0.95


def _perm_null(ys, cols, ols, n=None):
    import random
    n = PERM_N if n is None else n
    rng = random.Random(PERM_SEED)
    shuffled = list(ys)
    out = []
    for _i in range(n):
        rng.shuffle(shuffled)
        _b, r2 = ols(list(shuffled), cols)
        out.append(0.0 if r2 != r2 else r2)   # NaN -> 0.0
    out.sort()
    return out[int(PERM_Q * (len(out) - 1))]


def discriminate(arch, condition, configs):
    """Regress outcome on similarity and recombination depth.

    The drop: 'If similarity carries it, the result is retrieval. If
    recombination depth carries it, derivation.'"""
    ols = _ols()
    ys, sims, deps, _k = score_vector(arch, condition, configs)
    blank = {"architecture": arch, "condition": condition, "n": len(ys),
             "beta_similarity": UNMEASURED, "beta_depth": UNMEASURED,
             "r_squared": UNMEASURED, "perm_null_q95": UNMEASURED,
             "verdict": UNMEASURED, "verdict_drop_rule": UNMEASURED}
    if not ys or len(set(ys)) == 1:
        blank["reason"] = ("outcome is constant; a regression on a "
                           "constant outcome has no slope to report")
        return blank

    # A regressor held constant on this subsample is DROPPED and named,
    # not reported as a singular system. Holding similarity fixed is
    # what the matched band is FOR -- the run there is a
    # single-predictor regression on depth, and it is identified.
    const_s = len(set(sims)) == 1
    const_d = len(set(deps)) == 1
    if const_s and const_d:
        blank["reason"] = "both regressors are constant on this subsample"
        return blank
    cols, names = [], []
    if not const_s:
        cols.append(sims)
        names.append("similarity")
    if not const_d:
        cols.append(deps)
        names.append("depth")
    beta, r2 = ols(ys, cols)
    if beta is None:
        blank["reason"] = ("normal equations singular on %s"
                           % " and ".join(names))
        return blank
    got = dict(zip(names, beta[1:]))
    bs = got.get("similarity")
    bd = got.get("depth")
    held = ("similarity held constant" if const_s else
            "depth held constant" if const_d else None)

    # Does ANYTHING carry, before asking which. Without this the
    # single-predictor path names its one candidate by default.
    bar = _perm_null(ys, cols, ols)

    # THE DROP'S OWN RULE, unconditional: compare the coefficients and
    # name the larger. Reported beside the null-tested verdict because
    # the two disagree here, and the disagreement is the finding: the
    # stated rule returns an architecture verdict on every input,
    # including on a solver that has neither architecture.
    if bs is None:
        drop_v = "DEPTH_CARRIES"
    elif bd is None:
        drop_v = "SIMILARITY_CARRIES"
    elif abs(bs) > abs(bd):
        drop_v = "SIMILARITY_CARRIES"
    elif abs(bd) > abs(bs):
        drop_v = "DEPTH_CARRIES"
    else:
        drop_v = "TIED"

    if r2 <= bar:
        v = "NEITHER_CARRIES"
    elif bs is None:
        v = "DEPTH_CARRIES"
    elif bd is None:
        v = "SIMILARITY_CARRIES"
    elif abs(bs) > abs(bd):
        v = "SIMILARITY_CARRIES"
    elif abs(bd) > abs(bs):
        v = "DEPTH_CARRIES"
    else:
        v = "TIED"
    return {"architecture": arch, "condition": condition, "n": len(ys),
            "beta_similarity": UNMEASURED if bs is None
            else round(bs + 0.0, 6),
            "beta_depth": UNMEASURED if bd is None else round(bd + 0.0, 6),
            "r_squared": round(r2, 6),
            "perm_null_q95": round(bar, 6),
            "verdict": v, "verdict_drop_rule": drop_v, "reason": held}


def collinearity(configs):
    """The two regressors' correlation, and the matched band.

    Depth 0 cannot appear in test at all -- a set inside one training
    family IS a training configuration -- so the test set has two depth
    levels, and they differ in similarity. The regression is therefore
    run on correlated regressors unless a matched band is used."""
    rows = [(E.similarity(c, _TRAIN), float(E.recombination_depth(c)))
            for c in configs]
    n = len(rows)
    if n < 2:
        return {"n": n, "corr": UNMEASURED}
    ms = sum(s for s, _d in rows) / n
    md = sum(d for _s, d in rows) / n
    cov = sum((s - ms) * (d - md) for s, d in rows)
    vs = sum((s - ms) ** 2 for s, _d in rows) ** 0.5
    vd = sum((d - md) ** 2 for _s, d in rows) ** 0.5
    corr = UNMEASURED if vs == 0 or vd == 0 else round(cov / (vs * vd), 4)
    levels = sorted(set(d for _s, d in rows))
    return {"n": n, "corr": corr, "depth_levels": [int(d) for d in levels]}


def matched_band(configs):
    """Configurations at a similarity where BOTH depths occur.

    Similarity is held constant and depth varies, so the regressors are
    decorrelated by construction and the depth coefficient is
    identified. The repair for the collinearity is in the same data --
    it costs sample size, not a new environment."""
    by = {}
    for c in configs:
        s = E.similarity(c, _TRAIN)
        by.setdefault(s, set()).add(E.recombination_depth(c))
    good = set(s for s, ds in by.items() if len(ds) > 1)
    return [c for c in configs if E.similarity(c, _TRAIN) in good]


# ------------------------------------------------------------ the power

POWER_N = (143, 300, 600, 1200)
POWER_TRIALS = 40
# [CHOICE] A coarser permutation null inside the power sweep. The sweep's
# output is a CURVE and is read for an order of magnitude ("roughly 600"),
# where the reported per-solver verdicts above are read as verdicts and
# use the full PERM_N. Stated rather than tuned silently.
PERM_N_POWER = 120


def power(arch=RETRIEVAL, condition=None, configs=None, ns=POWER_N):
    """At what n does the discriminator clear its own null?

    Resamples the observed (outcome, similarity, depth) rows with
    replacement. The effect size is the one measured, not a stipulated
    one, so this answers 'how many configurations would Arm 1 need to
    detect the architecture difference it already contains' rather than
    a hypothetical."""
    import random
    ols = _ols()
    condition = condition or NOT_ENUMERATED
    configs = configs if configs is not None else E.test_configs()
    ys, sims, deps, _k = score_vector(arch, condition, configs)
    base = list(zip(ys, sims, deps))
    if not base or len(set(ys)) == 1:
        return {"observed_n": len(base), "rows": UNMEASURED}
    out = []
    for n in ns:
        hits = 0
        run = 0
        for t in range(POWER_TRIALS):
            rng = random.Random(1000 + t)
            smp = [rng.choice(base) for _i in range(n)]
            Y = [a for a, _b, _c in smp]
            S = [b for _a, b, _c in smp]
            D = [c for _a, _b, c in smp]
            if len(set(Y)) == 1 or len(set(S)) == 1:
                continue
            _b, r2 = ols(Y, [S, D])
            if r2 != r2:
                continue
            run += 1
            if r2 > _perm_null(Y, [S, D], ols, PERM_N_POWER):
                hits += 1
        out.append((n, round(hits / float(run), 3) if run else UNMEASURED))
    return {"observed_n": len(base), "base_rate": round(sum(ys) / len(ys), 4),
            "rows": out}


# ------------------------------------------------------------ the report

def render():
    out = []
    w = out.append
    tr, te = E.train_configs(), E.test_configs()

    w("MOVE-SET DERIVATION -- ARM 1")
    w("")
    w("SOURCE_DROP.md asks: \"Arm 4 or Arm 1 alone is a complete")
    w("project. Publish the null rate and the similarity-versus-")
    w("recombination regression, with unmeasured cells marked.\"")
    w("Arm 4 requires camera-trap and telemetry archives; egress here is an")
    w("allowlist and refuses every archive host, so Arm 4 is UNMEASURED")
    w("and is not approximated. Arm 1 is built and run below.")
    w("")
    w("WHAT IS UNDER TEST. The environment and the solvers are both")
    w("authored here, so a regression against one hand-written solver")
    w("returns its author's architecture rather than a capacity. The")
    w("solvers therefore carry DECLARED architectures and the")
    w("discriminator is run against all four: the question asked is")
    w("whether the discriminator can tell them apart, which is the")
    w("known-truth-first invariant applied to the arm's own instrument")
    w("before it is pointed at anything whose architecture is unknown.")
    w("Nothing here is a system under test.")
    w("")

    w("0. THE ENVIRONMENT")
    w("   primitives: %d   goals: %d   moves: %d" % (
        len(E.PRIMITIVES), len(E.GOALS), len(E.MOVES)))
    w("   configurations enumerated exhaustively: %d" % len(E.all_configs()))
    w("   training: %d      test: %d" % (len(tr), len(te)))
    w("")
    w("   COMPOSITIONAL NOVELTY, the arm's stated validity condition:")
    w("     primitives in test and never in training: %s" %
      (E.compositional_only() or "none"))
    w("   The drop calls this the whole validity of the arm, so it is a")
    w("   returned value and a selftest assertion rather than an")
    w("   intention. A leaked primitive would measure knowledge and")
    w("   report it as derivation.")
    w("")

    w("1. THE TWO REGRESSORS ARE CORRELATED BY CONSTRUCTION")
    col = collinearity(te)
    w("   n=%d   corr(similarity, depth) = %s" % (col["n"], col["corr"]))
    w("   depth levels present in test: %s" % col["depth_levels"])
    w("")
    w("   Depth 0 CANNOT appear in test: a primitive set inside one")
    w("   training family is a training configuration. So the test set")
    w("   has two depth levels, not a range, and they differ in mean")
    w("   similarity -- deeper recombination is further from any single")
    w("   training configuration almost by definition.")
    w("")
    band = matched_band(te)
    bcol = collinearity(band)
    w("   THE DECORRELATION IS IN THE DATA. At the similarity where both")
    w("   depths occur, similarity is constant and depth varies:")
    w("     matched band: %d of %d configurations" % (len(band), len(te)))
    w("     corr within the band: %s" % bcol["corr"])
    w("   It costs sample size, not a new environment. Every")
    w("   discriminator reading below is reported on both.")
    w("")

    w("2. THE FIVE MEASURES, KEPT APART")
    w("   The drop forbids a composite: the per-measure profile IS the")
    w("   dissociation being tested. No score is emitted anywhere.")
    w("")
    for arch in (DERIVATION, RETRIEVAL, PLAUSIBLE, SILENT):
        w("   %-11s %s" % (arch, ARCHITECTURE[arch].split(".")[0]))
    w("")
    w("   %-11s %-20s %6s %7s %6s %7s %7s %7s" % (
        "arch", "condition", "cand", "admis", "covr", "t1st", "prem",
        "null"))
    rows = {}
    for arch in (DERIVATION, RETRIEVAL, PLAUSIBLE, SILENT):
        for cond in CONDITIONS:
            m = measure(arch, cond, te)
            rows[(arch, cond)] = m
            w("   %-11s %-20s %6s %7s %6s %7s %7s %7s" % (
                arch, cond.replace("not_enumerated", "not_enum")
                   .replace("irreversible", "irrev"),
                m["mean_candidate_set"], m["admissibility_fraction"],
                m["coverage_ADDED"], m["mean_time_to_first_admissible"],
                m["premature_commitment_rate"], m["null_rate"]))
        w("")
    w("   cand  mean candidate-set size before commitment")
    w("   admis admissibility fraction of generated candidates")
    w("   covr  ADDED, not one of the five -- fraction of configurations")
    w("         with an admissible move where one was reached")
    w("   t1st  mean index of the first admissible move")
    w("   prem  premature-commitment rate (irreversible condition only)")
    w("   null  fraction of no-admissible-move seeds answered empty")
    w("   UNMEASURED = the denominator is empty. Never a pass.")
    w("")
    w("   TWO OF THE FIVE DO NOT DISCRIMINATE HERE, for the same reason")
    w("   at two sites.")
    w("")
    t1 = set(rows[(a2, NOT_ENUMERATED)]["mean_time_to_first_admissible"]
             for a2 in (DERIVATION, RETRIEVAL, PLAUSIBLE))
    w("   TIME TO FIRST ADMISSIBLE MOVE is %s for every architecture that"
      % sorted(t1)[0])
    w("   reaches one: all four emit admissible-first, so the measure is")
    w("   CONSTANT_SILENT on this solver set. It takes a solver whose")
    w("   emission order is not admissibility-ordered, and none of the")
    w("   four is. That is a property of the fixtures, not of the")
    w("   measure, and it is stated rather than repaired because")
    w("   inventing a shuffled solver to make a measure move would be")
    w("   building the result.")
    w("")
    dr = rows[(DERIVATION, NOT_ENUMERATED)]
    rr = rows[(RETRIEVAL, NOT_ENUMERATED)]
    w("   ADMISSIBILITY FRACTION reads %s for DERIVATION and %s for" % (
        dr["admissibility_fraction"], rr["admissibility_fraction"]))
    w("   RETRIEVAL -- the two architectures the discriminator exists to")
    w("   separate. RETRIEVAL emitted %d moves and %d were inadmissible:"
      % (rr["admissibility_denominator"],
         int(round(rr["admissibility_denominator"]
                   * (1 - float(rr["admissibility_fraction"]))))))
    w("   it is CONSERVATIVE, not mistaken. Its neighbour is usually a")
    w("   subset of the present configuration, so what it emits is")
    w("   admissible and there is very little of it. Coverage separates")
    w("   them (%s against %s); the admissibility fraction does not." % (
        dr["coverage_ADDED"], rr["coverage_ADDED"]))
    w("")
    w("   That is the same shape as the null-rate result below. A")
    w("   measure of correctness with no coverage term is gameable by")
    w("   conservatism, and a measure of restraint with no reach term is")
    w("   gameable by silence. Two of the drop's five measures need a")
    w("   partner it does not list.")
    w("")
    w("   THE ENUMERATED CONDITION is the control and behaves like one:")
    w("   every architecture scores identically, because the admissible")
    w("   set is given and nothing is derived. Its rows are included")
    w("   because a condition that cannot separate anything is the")
    w("   baseline the other three are read against.")
    w("")

    w("3. THE NULL RATE, AND WHY IT CANNOT STAND ALONE")
    ns = sum(1 for c in te if E.is_null(c))
    w("   no-admissible-move seeds in test: %d of %d (%.4f)" % (
        ns, len(te), ns / float(len(te))))
    w("   They occur in the space rather than being injected: a goal")
    w("   with no move whose requirements the configuration meets.")
    w("")
    for ln in NULL_PAIRING_NOTE.split(". "):
        if ln.strip():
            w("   %s." % ln.strip().rstrip("."))
    w("")
    sil = measure(SILENT, NOT_ENUMERATED, te)
    der = measure(DERIVATION, NOT_ENUMERATED, te)
    w("   SILENT     null_rate %-7s reached an admissible move %d times"
      % (sil["null_rate"], sil["reached_an_admissible_move"]))
    w("   DERIVATION null_rate %-7s reached an admissible move %d times"
      % (der["null_rate"], der["reached_an_admissible_move"]))
    w("   Same null rate. The pair separates them; the measure alone")
    w("   does not.")
    w("")

    w("4. THE DISCRIMINATOR -- SIMILARITY VERSUS RECOMBINATION DEPTH")
    w("   \"If similarity carries it, the result is retrieval. If")
    w("   recombination depth carries it, derivation.\"")
    w("")
    w("   THE KNOWN-ANSWER RUN. Four solvers, architectures declared")
    w("   before any of them was run. If the discriminator cannot")
    w("   recover an architecture it was handed, it cannot recover one")
    w("   it was not.")
    w("")
    w("   %-11s %-13s %4s %10s %10s %8s %8s" % (
        "arch", "subsample", "n", "b_sim", "b_depth", "r2", "null95"))
    ds = {}
    for arch in (DERIVATION, RETRIEVAL, PLAUSIBLE, SILENT):
        for label, cfgs in (("full test", te), ("matched band", band)):
            d = discriminate(arch, NOT_ENUMERATED, cfgs)
            ds[(arch, label)] = d
            w("   %-11s %-13s %4d %10s %10s %8s %8s" % (
                arch, label, d["n"], d["beta_similarity"],
                d["beta_depth"], d["r_squared"], d["perm_null_q95"]))
            w("       drop's stated rule: %-22s null-tested: %s" % (
                d["verdict_drop_rule"], d["verdict"]))
            if d["reason"]:
                w("       (%s)" % d["reason"])
    w("")
    w("   THE STATED RULE AND THE NULL DISAGREE, AND BOTH ARE PRINTED.")
    w("")
    rf = ds[(RETRIEVAL, "full test")]
    w("   On RETRIEVAL the drop's rule is RIGHT and recovers the")
    w("   declared architecture: b_sim %s against b_depth %s, a factor" % (
        rf["beta_similarity"], rf["beta_depth"]))
    w("   of %d. That is the intended signal and it is there." %
      int(abs(rf["beta_similarity"]) / max(abs(rf["beta_depth"]), 1e-9)))
    w("")
    w("   And it does not clear chance: r2 %s against a permutation" %
      rf["r_squared"])
    w("   null at the 95th percentile of %s. The coefficient is large" %
      rf["perm_null_q95"])
    w("   and the model explains less variance than a shuffled outcome")
    w("   does at this n.")
    w("")
    pf = ds[(PLAUSIBLE, "full test")]
    w("   The rule's cost is visible on PLAUSIBLE, which has NEITHER")
    w("   architecture -- it emits frequent moves regardless of the")
    w("   configuration. The stated rule returns %s" % pf["verdict_drop_rule"])
    w("   for it anyway, because a comparison of two coefficients")
    w("   always names one. There is no state in the rule for 'neither")
    w("   regressor does anything', so it cannot report the case it")
    w("   most has to.")
    w("")
    w("   The matched band is what decorrelates the two, and it")
    w("   forces a SINGLE-predictor regression, where the stated rule is")
    w("   degenerate: with one candidate it can only name that one. On")
    w("   RETRIEVAL the band would read DEPTH_CARRIES -- the derivation")
    w("   verdict, on a retrieval solver -- at r2 %s. The null is what" %
      ds[(RETRIEVAL, "matched band")]["r_squared"])
    w("   stops it.")
    w("")

    w("   POWER. The discriminator is underpowered here rather than")
    w("   blind: resampling the observed rows,")
    pw = power(RETRIEVAL, NOT_ENUMERATED, te)
    w("     configurations with an admissible move: %d   base rate %s" % (
        pw["observed_n"], pw["base_rate"]))
    w("        n     P(clears its own null)")
    for n, p in pw["rows"]:
        w("     %5d     %s" % (n, p))
    w("   So Arm 1 takes roughly 600 configurations CARRYING AN")
    w("   ADMISSIBLE MOVE to detect the architecture difference it")
    w("   already contains. This environment supplies %d." % pw["observed_n"])
    w("")
    w("   Configuration count goes as 2^P x G, so the shortfall is")
    w("   reachable by adding primitives or goals -- subject to the")
    w("   arm's own validity condition, since every added primitive has to")
    w("   appear in training or the novelty stops being compositional.")
    w("   The extension is NOT BUILT here and no number above is from")
    w("   it.")
    w("")

    w("5. WHAT IS UNMEASURED, MARKED RATHER THAN ESTIMATED")
    w("   Arm 2  UNMEASURED  human subjects; not simulated, and a")
    w("                      simulated protocol group would be a")
    w("                      fabricated claim about operators")
    w("   Arm 3  UNMEASURED  takes a private post-cutoff rule system and")
    w("                      models either side of a publication date")
    w("   Arm 4  UNMEASURED  camera-trap and telemetry archives; every")
    w("                      archive host refuses CONNECT here")
    w("")
    w("   Arm 1 is one arm. Nothing here is evidence about any trained")
    w("   model, any animal, or any operator. What it establishes is a")
    w("   property of the arm's own instrument, measured on solvers")
    w("   whose architectures were declared before they were run.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "arm1.py has no checks of its own. The checks that exercise "
            "it and env.py live in selftest_msd.py.\n"
            "    python3 move-set-derivation/selftest_msd.py\n")
        sys.exit(2)
    print(render())
