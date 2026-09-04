#!/usr/bin/env python3
"""P4 -- goal coherence. A reasoning chain of N steps; at each step, with
probability p_contest, the step contests the prior step's output instead
of accepting it, so the prior step is re-derived (and may be contested
again). No inputs. A simulation, with its exact counterpart beside it.

    python3 p4_goal_coherence.py --steps 50 --p-contest 0.0:1.0:0.05 --trials 1000 --out coherence.jsonl

Model [CHOICE 1]: position i = steps completed. Step 0 is the premise and
is accepted as given (there is no prior output to contest). From i >= 1
the next step contests with probability p (position i-1, the prior step
is re-derived) and accepts otherwise (position i+1). The answer is
produced at position N. Budget [CHOICE 2] is `--budget-mult` x N steps.
The model carries no answer-quality variable: what varies is whether an
answer is produced, and when. Refuses --selftest.
"""

import argparse
import json
import random
import sys


def simulate(n, p, trials, budget, seed=0):
    rng = random.Random(seed)
    steps_done, no_answer = [], 0
    for _ in range(trials):
        pos, t, out = 0, 0, None
        while t < budget:
            t += 1
            if pos == 0 or rng.random() >= p:
                pos += 1
            else:
                pos -= 1
            if pos == n:
                out = t
                break
        if out is None:
            no_answer += 1
        else:
            steps_done.append(out)
    k = len(steps_done)
    return {"answers": k, "no_answer": no_answer,
            "termination_rate": k / trials if trials else None,
            "mean_steps_to_answer": (sum(steps_done) / k) if k else None,
            "steps": steps_done}


def exact(n, p, budget):
    """Exact distribution over positions per tick, so the termination
    rate within budget and the conditional mean steps are computable
    without sampling. The known answer the simulation is read against."""
    dist = [0.0] * (n + 1)
    dist[0] = 1.0
    absorbed, weighted = 0.0, 0.0
    for t in range(1, budget + 1):
        nxt = [0.0] * (n + 1)
        for i in range(n):
            m = dist[i]
            if m == 0.0:
                continue
            if i == 0:
                nxt[1] += m
            else:
                nxt[i - 1] += m * p
                nxt[i + 1] += m * (1 - p)
        absorbed += nxt[n]
        weighted += t * nxt[n]
        nxt[n] = 0.0
        dist = nxt
    return {"termination_rate": absorbed, "mean_steps_to_answer": (weighted / absorbed) if absorbed > 0 else None}


def expected_steps_unbounded(n, p):
    """E[steps to reach N] with no budget, solving the tridiagonal system
    E_0 = 1 + E_1, E_i = 1 + p E_{i-1} + (1-p) E_{i+1}, E_N = 0. None at p = 1."""
    if p >= 1.0:
        return None if n > 1 else 1.0
    # forward substitution: E_i - E_{i+1} = d_i with d_0 = 1, d_i = (1 + p d_{i-1}) / (1 - p)
    d = [1.0]
    for i in range(1, n):
        d.append((1 + p * d[i - 1]) / (1 - p))
    return sum(d)


def grid(spec):
    a, b, s = (float(x) for x in spec.split(":"))
    out, x = [], a
    while x <= b + 1e-9:
        out.append(round(x, 10))
        x += s
    return out


def histogram(values, bins=10, width=40):
    """Plot-free text histogram of steps-to-answer."""
    if not values:
        return ["  (no answers produced)"]
    lo, hi = min(values), max(values)
    if lo == hi:
        return ["  %8.1f | %s %d  (every answer at the same step count)" % (lo, "#" * width, len(values))]
    span = max(hi - lo, 1)
    counts = [0] * bins
    for v in values:
        counts[min(bins - 1, int((v - lo) * bins / span))] += 1
    top = max(counts)
    lines = []
    for i, c in enumerate(counts):
        left = lo + i * span / bins
        lines.append("  %8.1f | %s %d" % (left, "#" * int(width * c / top), c))
    return lines


def run(n, ps, trials, budget_mult, seed):
    budget = budget_mult * n
    rows = []
    for p in ps:
        sim = simulate(n, p, trials, budget, seed)
        ex = exact(n, p, budget)
        rows.append({"steps": n, "p_contest": p, "trials": trials, "budget": budget,
                     "termination_rate": sim["termination_rate"], "mean_steps_to_answer": sim["mean_steps_to_answer"],
                     "answers": sim["answers"], "no_answer": sim["no_answer"],
                     "exact_termination_rate": ex["termination_rate"], "exact_mean_steps": ex["mean_steps_to_answer"],
                     "expected_steps_unbounded": expected_steps_unbounded(n, p), "_steps": sim["steps"]})
    return rows


def render(rows, hist_at=(0.0, 0.3, 0.5)):
    n, budget, trials = rows[0]["steps"], rows[0]["budget"], rows[0]["trials"]
    L = ["P4 goal coherence: N=%d steps, budget %d, %d trials per p [CHOICE 1 premise accepted; CHOICE 2 budget]" % (n, budget, trials)]
    L.append("  p_contest  term_rate  exact   mean_steps   exact   E[steps] unbounded   answers/no_answer   |bar")
    for r in rows:
        bar = "#" * int(30 * r["termination_rate"])
        L.append("  %6.2f     %6.3f   %6.3f   %9s  %9s   %14s   %5d/%-5d  |%s" % (
            r["p_contest"], r["termination_rate"], r["exact_termination_rate"],
            _f(r["mean_steps_to_answer"]), _f(r["exact_mean_steps"]), _f(r["expected_steps_unbounded"]),
            r["answers"], r["no_answer"], bar))
    L.append("  term_rate bar: 30 chars = 1.0.  'undefined' = no answer produced, not zero steps.")
    for r in rows:
        if any(abs(r["p_contest"] - h) < 1e-9 for h in hist_at):
            L.append("steps to answer at p_contest = %.2f" % r["p_contest"])
            L.extend(histogram(r["_steps"]))
    L.append("the model has no answer-quality term: the readout is answer produced or not, and when")
    return "\n".join(L)


def _f(x):
    if not isinstance(x, (int, float)):
        return "undefined"
    return "%.1f" % x if x < 1e6 else "%.2e" % x


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=50)
    ap.add_argument("--p-contest", default="0.0:1.0:0.05")
    ap.add_argument("--trials", type=int, default=1000)
    ap.add_argument("--budget-mult", type=int, default=10)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        print("p4_goal_coherence has no selftest; run selftest_csp.py", file=sys.stderr)
        return 2
    rows = run(a.steps, grid(a.p_contest), a.trials, a.budget_mult, a.seed)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps({k: v for k, v in r.items() if k != "_steps"}, sort_keys=True) + "\n")
    print(render(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
