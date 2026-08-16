"""
corpus_loop.py -- coherence rises while substrate coupling falls, and the
detector that could see it is on the wrong side of the loop.

CC0-1.0. Standard library only. Deterministic (seeded).

THE LOOP
--------
    corpus -> model -> outputs -> corpus

A model is fitted to a corpus. Its outputs enter the corpus. The next model
is fitted to that. Nothing here is adversarial and no term is malicious; the
only ingredient is that a fit is not an identity map. Any shrinkage toward a
prior, any smoothing, any regularization -- `lam` below -- compounds once its
own output is the next input.

TWO READINGS OF THE SAME RUN
    coherence   model output vs the corpus it was fitted to
    coupling    model output vs a substrate the system did not author

Coherence is cheap, always available, and computable from inside. Coupling
needs a reference no actor inside the loop produced.

WHAT THIS CHECKS
    1  the two curves separate, and lam carries it (lam = 0 is a fixed point)
    2  the model-vs-corpus detector is CONSTANT_SILENT -- structurally, and
       its statistic goes QUIET as the drift completes
    3  a corpus-shift detector DOES fire, and does not discriminate. Run as
       a ../null-harness/ sweep: degrade arm = known signal, improve arm =
       known null, identical in every line but the provenance of the
       injected observations. No threshold separates them.
    4  scheduled anchoring recovers coupling; confidence-triggered anchoring
       never runs, because of 2.

BOTH ARMS USE THE SAME INSTRUMENT NOISE on injection. An earlier version
gave model emissions half the noise of direct measurements, which put the
two arms' detector floors at different heights and made the discrimination
result an artifact of that choice. They are equal here.
"""

from __future__ import annotations

import math
import random

RULE = "=" * 72

N_ITEMS = 240
N_INITIAL = 12          # direct observations per item at generation 0
N_EMIT = 12             # observations injected per item per generation
OBS_NOISE = 0.25        # same in both arms, on both provenances
INITIAL_BIAS = 0.35     # the corpus starts miscalibrated, in both arms
GENERATIONS = 24
SEED = 20260816


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


# ---------------------------------------------------------------------------
# substrate + corpus


def substrate(n: int, seed: int) -> list[float]:
    """Values the system did not author. Fixed for the whole run."""
    rng = random.Random(seed)
    return [rng.uniform(-1.0, 1.0) for _ in range(n)]


def initial_corpus(truth, seed, bias=INITIAL_BIAS):
    rng = random.Random(seed)
    return [[t + bias + rng.gauss(0.0, OBS_NOISE) for _ in range(N_INITIAL)]
            for t in truth]


def corpus_mean(corpus) -> list[float]:
    return [sum(c) / len(c) for c in corpus]


def fit(means) -> list[float]:
    raise NotImplementedError  # see fit_from below; kept out of the way


def fit_from(means, lam: float) -> list[float]:
    """
    The model. Per-item corpus mean, shrunk toward the pooled mean by lam.

    lam is the whole mechanism. It is not a defect -- it is what any
    regularized, capacity-limited or smoothing estimator does. At lam = 0
    the loop is a fixed point and nothing below happens.
    """
    pooled = sum(means) / len(means)
    return [pooled + (1.0 - lam) * (m - pooled) for m in means]


def rmse(a, b) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / len(a))


# ---------------------------------------------------------------------------
# the two arms


def run(arm: str, lam: float, generations=GENERATIONS, seed=SEED,
        anchor_every: int | None = None, anchor_frac: float = 1.0):
    """
    arm == "degrade"  model outputs are injected back into the corpus
    arm == "improve"  fresh direct measurements are injected instead

    The two arms differ in ONE branch: the provenance of the injected
    observations. Counts, noise, schedule and item order are identical.
    """
    truth = substrate(N_ITEMS, seed)
    corpus = initial_corpus(truth, seed + 1)
    rng = random.Random(seed + 2)

    history = []
    prev_cm = corpus_mean(corpus)

    for g in range(generations):
        means = corpus_mean(corpus)          # the corpus the model is fitted to
        model = fit_from(means, lam)

        anchored = bool(anchor_every) and g > 0 and g % anchor_every == 0

        for i in range(N_ITEMS):
            if arm == "improve" or anchored:
                k = N_EMIT if arm == "improve" else max(
                    1, int(round(N_EMIT * anchor_frac)))
                src = [truth[i] + rng.gauss(0.0, OBS_NOISE) for _ in range(k)]
            else:
                src = [model[i] + rng.gauss(0.0, OBS_NOISE)
                       for _ in range(N_EMIT)]
            corpus[i].extend(src)

        cm = corpus_mean(corpus)
        history.append({
            "gen": g,
            "coupling_err": rmse(model, truth),      # needs the substrate
            "coherence_err": rmse(model, means),     # D1, computable inside
            "corpus_shift": rmse(cm, prev_cm),       # D2, computable inside
            "anchored": anchored,
        })
        prev_cm = cm

    return history


# ---------------------------------------------------------------------------
# 1  the two curves


def check_separation(lam=0.12) -> None:
    section("1  coherence and coupling separate")

    h = run("degrade", lam)
    print("  lam = %.2f   initial corpus bias = %.2f   %d items, %d gens\n"
          % (lam, INITIAL_BIAS, N_ITEMS, GENERATIONS))
    print("  %-5s %-16s %-16s %s"
          % ("gen", "coupling err", "D1 coherence", "D2 corpus shift"))
    print("  " + "-" * 62)
    for r in h:
        if r["gen"] % 4 == 0 or r["gen"] == GENERATIONS - 1:
            print("  %-5d %-16.4f %-16.4f %.5f"
                  % (r["gen"], r["coupling_err"], r["coherence_err"],
                     r["corpus_shift"]))
    print()
    print("  coupling  %.4f -> %.4f   %s   (needs the substrate)"
          % (h[0]["coupling_err"], h[-1]["coupling_err"],
             "WORSE" if h[-1]["coupling_err"] > h[0]["coupling_err"]
             else "better"))
    print("  D1        %.4f -> %.4f   %s   (computable inside)"
          % (h[0]["coherence_err"], h[-1]["coherence_err"],
             "worse" if h[-1]["coherence_err"] > h[0]["coherence_err"]
             else "BETTER"))
    print("  D2        %.5f -> %.5f  %s   (computable inside)"
          % (h[0]["corpus_shift"], h[-1]["corpus_shift"],
             "worse" if h[-1]["corpus_shift"] > h[0]["corpus_shift"]
             else "QUIETER"))
    print()
    print("  Both statistics computable without the substrate improve or go")
    print("  quiet. The one that needs an unauthored reference degrades.")

    flat = run("degrade", 0.0)
    print()
    print("  Control, lam = 0 (fit is the identity on the corpus mean):")
    print("    coupling  %.4f -> %.4f   drift %+.4f"
          % (flat[0]["coupling_err"], flat[-1]["coupling_err"],
             flat[-1]["coupling_err"] - flat[0]["coupling_err"]))
    print("    the loop is a fixed point and the separation does not appear.")
    print("    So the effect is carried by lam, not by feedback alone.")


# ---------------------------------------------------------------------------
# 2  the internal consistency detector


def check_silent(lam=0.12) -> None:
    section("2  model-vs-corpus consistency: CONSTANT_SILENT, structurally")

    h = run("degrade", lam)
    print("  detector D1: fire when the model departs from the corpus it was")
    print("  fitted to. The cheapest available check, and the one a system")
    print("  can always run on itself.\n")
    print("  %-5s %-16s %-16s" % ("gen", "D1", "coupling err"))
    print("  " + "-" * 40)
    for r in h:
        if r["gen"] % 4 == 0 or r["gen"] == GENERATIONS - 1:
            print("  %-5d %-16.5f %-16.4f"
                  % (r["gen"], r["coherence_err"], r["coupling_err"]))

    mono = all(b["coherence_err"] <= a["coherence_err"] + 1e-12
               for a, b in zip(h, h[1:]))
    print()
    print("  monotonically non-increasing: %s" % mono)
    print("  fell by %.1f%% while coupling error rose by %.1f%%"
          % (100 * (1 - h[-1]["coherence_err"] / h[0]["coherence_err"]),
             100 * (h[-1]["coupling_err"] / h[0]["coupling_err"] - 1)))
    print()
    print("  D1 = lam x (spread of corpus item means about their pooled")
    print("  mean). Every generation shrinks that spread and re-injects the")
    print("  shrunk values, so D1 decays -- slower than geometrically, since")
    print("  the pool accumulates and old observations are not evicted. It is")
    print("  not measuring drift. It is measuring how much of the corpus the")
    print("  model has yet to write, and it falls BECAUSE the drift is")
    print("  proceeding.\n")
    print("  This is not an empirical result -- it is what the arithmetic")
    print("  says. Cf. ../null-harness/ CONSTANT_SILENT: a gate whose fire")
    print("  branch is unreachable by construction.")


# ---------------------------------------------------------------------------
# 3  the corpus-shift detector fires, and does not discriminate


def check_discrimination() -> None:
    section("3  corpus-shift detector: fires, and does not discriminate")

    print("  detector D2: fire when the corpus moves between generations.")
    print("  A real design -- this is what a distribution-shift monitor")
    print("  does -- and unlike D1 its fire branch is reachable.\n")
    print("  Run as a ../null-harness/ sweep:")
    print("    known signal  degrade arm, coupling gets WORSE")
    print("    known null    improve arm, coupling gets BETTER")
    print("  identical in every line but the provenance of the injected")
    print("  observations.\n")

    lams = (0.02, 0.04, 0.08, 0.12, 0.20, 0.30, 0.45)
    print("  %-7s %-13s %-13s %-13s %-13s"
          % ("lam", "coupling deg", "coupling imp", "D2 peak deg",
             "D2 peak imp"))
    print("  " + "-" * 64)

    sig, null = [], []
    worse = better = 0
    for lam in lams:
        d = run("degrade", lam)
        i = run("improve", lam)
        sig.extend(r["corpus_shift"] for r in d)
        null.extend(r["corpus_shift"] for r in i)
        worse += d[-1]["coupling_err"] > d[0]["coupling_err"]
        better += i[-1]["coupling_err"] < i[0]["coupling_err"]
        print("  %-7.2f %-13.4f %-13.4f %-13.5f %-13.5f"
              % (lam, d[-1]["coupling_err"], i[-1]["coupling_err"],
                 max(r["corpus_shift"] for r in d),
                 max(r["corpus_shift"] for r in i)))

    print()
    print("  coupling direction is unambiguous: degrade ends worse than it")
    print("  started in %d of %d rows, improve ends better in %d of %d."
          % (worse, len(lams), better, len(lams)))
    print()
    print("  The null column is constant in lam because the improve arm")
    print("  never receives a model output, so lam is not in its path. That")
    print("  is the arms being identical except for provenance, not a bug.")
    print()
    print("  Now sweep a threshold on D2 over all %d signal and %d null"
          % (len(sig), len(null)))
    print("  samples and ask what any threshold can buy:\n")
    print("  %-14s %-10s %-10s %-10s" % ("threshold", "TP", "FP", "TP - FP"))
    print("  " + "-" * 48)

    lo, hi = min(sig + null), max(sig + null)
    best = None
    fp_ge_tp = True
    for k in range(21):
        thr = lo + (hi - lo) * k / 20.0
        tp = sum(1 for x in sig if x > thr) / len(sig)
        fp = sum(1 for x in null if x > thr) / len(null)
        fp_ge_tp = fp_ge_tp and fp >= tp
        if k % 4 == 0:
            print("  %-14.5f %-10.3f %-10.3f %-10.3f" % (thr, tp, fp, tp - fp))
        if best is None or (tp - fp) > best[3]:
            best = (thr, tp, fp, tp - fp)

    print()
    print("  best separation anywhere on the sweep:")
    print("    threshold %.5f   TP %.3f   FP %.3f   TP-FP %.3f" % best)
    print("  FP >= TP at EVERY threshold on the sweep: %s" % fp_ge_tp)
    print()
    verdict = ("NO_DISCRIMINATION" if best[3] < 0.5
               else "SEPARATES on this parameterization")
    print("  verdict: %s" % verdict)
    print()
    if fp_ge_tp:
        print("  Stronger than undiscriminating: on this run D2 is")
        print("  ANTI-correlated with what matters. The improving arm moves")
        print("  the corpus MORE than the degrading one, because correcting a")
        print("  0.35 bias is a bigger displacement than shrinking toward a")
        print("  pooled mean. A monitor tuned to fire on real degradation")
        print("  fires harder on real repair. The only threshold with")
        print("  TP - FP = 0 is the one that fires on nothing.")
        print()
    print("  D2 reports that the corpus moved. It does not report which way,")
    print("  because it is computed entirely from quantities the loop")
    print("  produced. The sign of the movement is the whole question, and")
    print("  the sign requires a reference no actor inside the loop wrote.")


# ---------------------------------------------------------------------------
# 4  anchoring


def check_anchor(lam=0.12) -> None:
    section("4  scheduled anchoring recovers; triggered anchoring never runs")

    base = run("degrade", lam)
    print("  no anchoring              final coupling err  %.4f\n"
          % base[-1]["coupling_err"])
    print("  %-16s %-10s %-16s" % ("anchor every", "frac", "final coupling"))
    print("  " + "-" * 46)
    for every in (12, 8, 6, 4, 3, 2):
        h = run("degrade", lam, anchor_every=every, anchor_frac=1.0)
        print("  %-16d %-10.2f %-16.4f"
              % (every, 1.0, h[-1]["coupling_err"]))
    print()
    for frac in (0.25, 0.5, 1.0):
        h = run("degrade", lam, anchor_every=4, anchor_frac=frac)
        print("  every 4, frac %.2f       final coupling  %.4f"
              % (frac, h[-1]["coupling_err"]))

    print()
    print("  Same anchoring, triggered by internal confidence instead of the")
    print("  calendar. The trigger is D1 from section 2.\n")

    fired = [r["gen"] for r in base
             if r["coherence_err"] > base[0]["coherence_err"]]
    print("    D1 at gen 0    %.5f" % base[0]["coherence_err"])
    print("    D1 at gen %-4d %.5f" % (GENERATIONS - 1,
                                       base[-1]["coherence_err"]))
    print("    generations where D1 exceeds its gen-0 value: %d" % len(fired))
    print()
    print("    So a confidence-triggered anchor interval never fires, and")
    print("    its final coupling error is the no-anchoring number, %.4f."
          % base[-1]["coupling_err"])
    print()
    print("  The schedule is not a convenience. It is the only form the")
    print("  interval can take, because the statistic that would trigger it")
    print("  is computed inside the layer it would be detecting.")


# ---------------------------------------------------------------------------


def main() -> None:
    print()
    print("CORPUS LOOP: COHERENCE UP, COUPLING DOWN")
    print("substrate = %d values the system did not author; seed %d"
          % (N_ITEMS, SEED))

    check_separation()
    check_silent()
    check_discrimination()
    check_anchor()

    section("READING")
    print("""
  The separation needs no bad actor. It needs a fit that is not an
  identity map and a path from output back to input. At lam = 0 the loop
  is a fixed point and nothing happens; every lam > 0 compounds.

  D1 -- model against the corpus it was fitted to -- is CONSTANT_SILENT by
  arithmetic, and its statistic IMPROVES as the drift completes, because it
  is measuring how much of the corpus the model has yet to write.

  D2 -- corpus now against corpus then -- is a real detector with a
  reachable fire branch, and on the null-harness sweep it does not
  discriminate: the degrading and improving arms are identical in every
  line but the provenance of what is injected, and no threshold on D2
  separates them. Direction is not in the signal.

  So the interval has to be scheduled. A confidence-triggered anchor never
  runs: the quantity that would trigger it is the quantity that goes quiet
  as the drift finishes.
""")


if __name__ == "__main__":
    main()
