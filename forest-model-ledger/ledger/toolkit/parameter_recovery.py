"""Toolkit: parameter_recovery. Tool #4 of the staged build (work order 2026-11-11). stdlib only.

Entry: ledger/toolkit/parameter_recovery.yaml. Gate: tests/test_toolkit.py.

Can the pipeline see what it claims? Generate synthetic data at a KNOWN parameter
value, then try to get that value back from the outputs alone.

  recover(outputs_at, theta_true, grid, seeds_obs, seeds_fit)
    outputs_at(theta, seed) -> dict of scalar outputs
    observation  mean outputs at theta_true over seeds_obs (disjoint from seeds_fit:
                 the data are not the fit's own draws)
    model        mean outputs at each grid value over seeds_fit (the same fit seeds at
                 every grid value: common random numbers along the grid)
    noise scale  per output, sd over seeds_fit at the grid value nearest theta_true;
                 se_k = sd_k * sqrt(1/n_obs + 1/n_fit)
    profile      chi2(g) = sum_k ((obs_k - model_k(g)) / se_k)^2   (outputs with se 0 are skipped
                 and listed: a noiseless output cannot be weighted)
    plausible    grid values with chi2(g) - min chi2 <= DCHI2        [CHOICE: DCHI2 = 9, 3 sigma]

  verdict
    NOT_IDENTIFIABLE  every grid value plausible: the outputs do not constrain theta here
    BIASED            the plausible set excludes theta_true: recovered, but somewhere else
    RECOVERED         theta_true plausible and neither grid end plausible
    PARTIAL           theta_true plausible, bounded on one side only

A NOT_IDENTIFIABLE reading is about these outputs, this grid and these seeds, not
about the parameter in the world.
"""
import math, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE)

DCHI2 = 9.0
CHOICES = dict(DCHI2=DCHI2)


def _mean(xs):
    return sum(xs) / len(xs)


def _sd(xs):
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) if len(xs) > 1 else 0.0


def profile(obs_runs, grid_runs, grid, theta_true):
    """obs_runs: list of output dicts at theta_true; grid_runs: {g: list of output dicts}."""
    names = list(obs_runs[0])
    obs = {n: _mean([r[n] for r in obs_runs]) for n in names}
    near = min(grid, key=lambda g: abs(g - theta_true))
    n_o, n_f = len(obs_runs), len(grid_runs[near])
    se = {n: _sd([r[n] for r in grid_runs[near]]) * math.sqrt(1.0 / n_o + 1.0 / n_f) for n in names}
    used = [n for n in names if se[n] > 0]
    chi = {}
    for g in grid:
        m = {n: _mean([r[n] for r in grid_runs[g]]) for n in used}
        chi[g] = sum(((obs[n] - m[n]) / se[n]) ** 2 for n in used)
    return dict(chi2=chi, used=used, skipped=[n for n in names if n not in used], obs=obs, se=se)


def verdict(chi2, grid, theta_true, dchi2=DCHI2):
    if not chi2:
        return "NOT_IDENTIFIABLE", list(grid)
    lo = min(chi2.values())
    plaus = [g for g in grid if chi2[g] - lo <= dchi2]
    near = min(grid, key=lambda g: abs(g - theta_true))
    if len(plaus) == len(grid):
        return "NOT_IDENTIFIABLE", plaus
    if near not in plaus:
        return "BIASED", plaus
    if grid[0] not in plaus and grid[-1] not in plaus:
        return "RECOVERED", plaus
    return "PARTIAL", plaus


def recover(outputs_at, theta_true, grid, seeds_obs, seeds_fit, mapper=map):
    jobs = [(theta_true, s) for s in seeds_obs] + [(g, s) for g in grid for s in seeds_fit]
    res = list(mapper(_call, [(outputs_at,) + j for j in jobs]))
    obs_runs = res[:len(seeds_obs)]
    grid_runs, k = {}, len(seeds_obs)
    for g in grid:
        grid_runs[g] = res[k:k + len(seeds_fit)]
        k += len(seeds_fit)
    p = profile(obs_runs, grid_runs, grid, theta_true)
    v, plaus = verdict(p["chi2"], grid, theta_true)
    return dict(verdict=v, plausible=plaus, theta_hat=min(p["chi2"], key=p["chi2"].get) if p["chi2"] else None, **p)


def _call(a):
    f, theta, seed = a
    return f(theta, seed)


# ---------------------------------------------------------------- gate: planted cases + null harness
def _toy(slope, bias=0.0, noise=1.0, k=3):
    import random

    def f(theta, seed, _data=False):
        r = random.Random(seed * 7919 + 1)
        return {f"y{i}": slope * (i + 1) * theta + (bias if _data else 0.0) + r.gauss(0, noise) for i in range(k)}
    return f


GRID = [0.6, 0.8, 1.0, 1.2, 1.4]


def _run_toy(f, theta_true=1.0, obs=range(100, 110), fit=range(10), data_f=None):
    data_f = data_f or f
    obs_runs = [data_f(theta_true, s) for s in obs]
    grid_runs = {g: [f(g, s) for s in fit] for g in GRID}
    p = profile(obs_runs, grid_runs, GRID, theta_true)
    return verdict(p["chi2"], GRID, theta_true)[0]


def known_cases():
    strong, flat = _toy(10.0), _toy(0.0)
    biased_model = _toy(10.0)
    biased_data = lambda th, s: {k: v + 6.0 for k, v in biased_model(th, s).items()}   # data carry an offset the model lacks
    weak = _toy(1.0, noise=3.0)
    return [
        ("outputs strongly driven by theta: RECOVERED", "RECOVERED", lambda: _run_toy(strong)),
        ("outputs independent of theta: NOT_IDENTIFIABLE (silent)", "NOT_IDENTIFIABLE", lambda: _run_toy(flat)),
        ("data carry an offset the model lacks: BIASED", "BIASED", lambda: _run_toy(strong, data_f=biased_data)),
        ("weak dependence under heavy noise is not RECOVERED (silent)", False, lambda: _run_toy(weak) == "RECOVERED"),
        ("verdict on a flat profile", "NOT_IDENTIFIABLE", lambda: verdict({g: 1.0 for g in GRID}, GRID, 1.0)[0]),
        ("verdict bounded on one side only", "PARTIAL", lambda: verdict({0.6: 0.0, 0.8: 0.0, 1.0: 0.0, 1.2: 20.0, 1.4: 40.0}, GRID, 1.0)[0]),
    ]


def gate(n=200, seeds=(0, 1, 2, 3, 4)):
    from ledger.toolkit import gate as G
    known = G.known_answers(known_cases(), lambda f: f())

    def draw(r, slope):
        off = r.randint(0, 10 ** 6)
        k = r.randint(2, 5)
        noise = r.uniform(0.5, 2.0)

        def f(theta, seed):
            rr = __import__("random").Random(off + seed)
            return {f"y{i}": slope * (i + 1) * theta + rr.gauss(0, noise) for i in range(k)}
        return f

    def recovered(f):
        return _run_toy(f) == "RECOVERED"

    legs = dict(recovered=G.null_harness_seeds(recovered, lambda r: draw(r, 0.0), lambda r: draw(r, 12.0), n, seeds))
    return G.combine(known, legs)


if __name__ == "__main__":
    print("refused: library. Gate: python3 tests/test_toolkit.py ; run: runs/run_17.py")
    raise SystemExit(2)
