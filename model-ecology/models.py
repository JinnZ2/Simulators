"""
models.py
---------
Twelve plugins across four mathematical families.

CRITICAL DESIGN CONSTRAINT
--------------------------
Each model computes a REAL rolling estimator from the REAL data. None of them
receives a planted per-family signal.

This matters. If we generated outputs as `family_signal + noise`, then the claim
"same-family models correlate more" (P1) would be true by construction and the
phylogeny module would be measuring its own assumption. Circular. Useless.

By computing genuine estimators, same-family models share only their INHERITED
BIAS -- spectral methods share spectral leakage, geometric methods share
embedding-dimension sensitivity, and so on. P1 then becomes a real empirical
question that CAN COME OUT FALSE. It is allowed to.

Each returns one anomaly/structure score per rolling window.

CC0. stdlib only.
"""

import math
from core import Model, ModelResult, REGISTRY, _mean, _std, pearson


# --------------------------------------------------------------- shared utils

def _win(data, i, w):
    return data[i - w:i]


def _detrend(x):
    n = len(x)
    if n < 2:
        return x[:]
    m = sum(x) / n
    return [v - m for v in x]


# ============================================================ SPECTRAL FAMILY
# Shared inherited bias: assumes stationarity within window; suffers spectral
# leakage; represents structure as sums of global periodic basis functions.

def _dft_power(x, k):
    n = len(x)
    re = sum(x[t] * math.cos(2 * math.pi * k * t / n) for t in range(n))
    im = sum(x[t] * math.sin(2 * math.pi * k * t / n) for t in range(n))
    return (re * re + im * im) / n


class _Rolling(Model):
    window = 40

    def predict(self, data):
        out = []
        for i in range(self.window, len(data) + 1):
            out.append(self.score(_win(data, i, self.window)))
        return ModelResult(prediction=out,
                           uncertainty=[0.1] * len(out),
                           confidence=0.6,
                           assumptions_used=list(self.assumptions))

    def score(self, w):
        raise NotImplementedError


@REGISTRY.model
class Fourier(_Rolling):
    name, family = "fourier", "spectral"
    assumptions = ["stationarity", "global periodic basis", "linearity"]
    limitations = ["leakage", "blind to transients"]

    def score(self, w):
        x = _detrend(w)
        lo = sum(_dft_power(x, k) for k in range(1, 5))
        hi = sum(_dft_power(x, k) for k in range(5, len(x) // 2))
        return lo / (lo + hi + 1e-9)


@REGISTRY.model
class Wavelet(_Rolling):
    name, family = "wavelet", "spectral"
    assumptions = ["dyadic scales", "compact basis", "local stationarity"]
    limitations = ["scale quantization"]

    def score(self, w):
        x = _detrend(w)
        # Haar band energies, coarse vs fine
        cur, energies = x[:], []
        while len(cur) > 1:
            nxt = [(cur[i] + cur[i + 1]) / 2 for i in range(0, len(cur) - 1, 2)]
            det = [(cur[i] - cur[i + 1]) / 2 for i in range(0, len(cur) - 1, 2)]
            energies.append(sum(d * d for d in det))
            cur = nxt
        if not energies:
            return 0.0
        coarse = sum(energies[len(energies) // 2:])
        return coarse / (sum(energies) + 1e-9)


@REGISTRY.model
class Hilbert(_Rolling):
    name, family = "hilbert", "spectral"
    assumptions = ["narrowband", "analytic signal", "instantaneous frequency exists"]
    limitations = ["meaningless for broadband"]

    def score(self, w):
        x = _detrend(w)
        env = [abs(x[i]) for i in range(len(x))]
        return (_std(env) / (abs(_mean(env)) + 1e-9)) / 10.0


@REGISTRY.model
class EMD(_Rolling):
    name, family = "emd", "spectral"
    assumptions = ["adaptive basis", "envelope sifting", "local extrema meaningful"]
    limitations = ["mode mixing", "no theory"]

    def score(self, w):
        x = _detrend(w)
        ext = sum(1 for i in range(1, len(x) - 1)
                  if (x[i] - x[i - 1]) * (x[i] - x[i + 1]) > 0)
        return ext / len(x)


# =========================================================== STATISTICAL FAMILY
# Shared inherited bias: summary statistics over the window; second-order or
# information-theoretic; discards phase and geometry.

@REGISTRY.model
class Autocorrelation(_Rolling):
    name, family = "autocorrelation", "statistical"
    assumptions = ["second-order structure suffices", "weak stationarity"]
    limitations = ["blind to nonlinearity"]

    def score(self, w):
        return abs(pearson(w[:-1], w[1:]))


@REGISTRY.model
class Hurst(_Rolling):
    name, family = "hurst", "statistical"
    assumptions = ["self-similarity", "power-law scaling"]
    limitations = ["unstable on short windows"]

    def score(self, w):
        x = _detrend(w)
        cum, s = [], 0.0
        for v in x:
            s += v
            cum.append(s)
        R = max(cum) - min(cum)
        S = _std(x)
        return math.log(R / S + 1e-9) / math.log(len(x)) if S > 0 else 0.0


@REGISTRY.model
class MutualInformation(_Rolling):
    name, family = "mutual_information", "statistical"
    assumptions = ["binning valid", "iid samples"]
    limitations = ["bin-count sensitive"]

    def score(self, w, bins=4):
        a, b = w[:-1], w[1:]
        lo, hi = min(w), max(w)
        if hi - lo < 1e-9:
            return 0.0
        def bi(v):
            return min(bins - 1, int((v - lo) / (hi - lo) * bins))
        joint, pa, pb = {}, {}, {}
        for x, y in zip(a, b):
            i, j = bi(x), bi(y)
            joint[(i, j)] = joint.get((i, j), 0) + 1
            pa[i] = pa.get(i, 0) + 1
            pb[j] = pb.get(j, 0) + 1
        n = len(a)
        mi = 0.0
        for (i, j), c in joint.items():
            pij, pi, pj = c / n, pa[i] / n, pb[j] / n
            mi += pij * math.log(pij / (pi * pj) + 1e-12)
        return mi


@REGISTRY.model
class TransferEntropy(_Rolling):
    name, family = "transfer_entropy", "statistical"
    assumptions = ["Markov order 1", "binning valid"]
    limitations = ["data hungry"]

    def score(self, w):
        # self-TE proxy: conditional predictability gain from lag-2 over lag-1
        r1 = abs(pearson(w[1:], w[:-1]))
        r2 = abs(pearson(w[2:], w[:-2]))
        return max(0.0, r2 - r1 * r1)


# ============================================================= GEOMETRIC FAMILY
# Shared inherited bias: reconstructs a state space; sensitive to embedding
# dimension and neighborhood radius; treats trajectory shape as primary.

@REGISTRY.model
class DelayEmbedding(_Rolling):
    name, family = "delay_embedding", "geometric"
    assumptions = ["deterministic attractor", "Takens embedding valid"]
    limitations = ["dimension/lag choice"]

    def score(self, w, tau=2):
        pts = [(w[i], w[i + tau]) for i in range(len(w) - tau)]
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        r = [math.dist(p, (cx, cy)) for p in pts]
        return _std(r) / (_mean(r) + 1e-9)


@REGISTRY.model
class Koopman(_Rolling):
    name, family = "koopman", "geometric"
    assumptions = ["linear evolution of observables", "attractor exists"]
    limitations = ["dictionary choice dominates"]

    def score(self, w):
        # best one-step linear operator; score = residual energy fraction
        a, b = w[:-1], w[1:]
        denom = sum(x * x for x in a)
        k = sum(x * y for x, y in zip(a, b)) / denom if denom > 1e-12 else 0.0
        resid = sum((y - k * x) ** 2 for x, y in zip(a, b))
        total = sum(y * y for y in b) + 1e-9
        return resid / total


@REGISTRY.model
class Recurrence(_Rolling):
    name, family = "recurrence", "geometric"
    assumptions = ["neighborhood radius meaningful", "trajectory revisits"]
    limitations = ["radius sensitive"]

    def score(self, w):
        eps = 0.4 * _std(w) + 1e-9
        n = len(w)
        hits = sum(1 for i in range(n) for j in range(i + 1, n)
                   if abs(w[i] - w[j]) < eps)
        return 2.0 * hits / (n * (n - 1))


@REGISTRY.model
class PersistentHomology(_Rolling):
    name, family = "persistent_homology", "geometric"
    assumptions = ["topological features persist", "filtration meaningful"]
    limitations = ["expensive", "coarse"]

    def score(self, w):
        # 0-dim persistence proxy on the sublevel-set filtration of the series:
        # total lifetime of local-minimum components
        lifetimes = []
        for i in range(1, len(w) - 1):
            if w[i] < w[i - 1] and w[i] < w[i + 1]:
                peak = min(max(w[:i] or [w[i]]), max(w[i:] or [w[i]]))
                lifetimes.append(peak - w[i])
        return sum(lifetimes) / (len(w) * (_std(w) + 1e-9))


# ========================================================== PROBABILISTIC FAMILY
# Shared inherited bias: posterior over latent states; prior-sensitive;
# structure = parameter change.

@REGISTRY.model
class BayesianChangepoint(_Rolling):
    name, family = "bayesian_changepoint", "probabilistic"
    assumptions = ["piecewise constant mean", "Gaussian likelihood", "prior on run length"]
    limitations = ["prior dominates on short data"]

    def score(self, w):
        best = 0.0
        n = len(w)
        for c in range(n // 4, 3 * n // 4):
            l, r = w[:c], w[c:]
            d = abs((_mean(l) or 0) - (_mean(r) or 0))
            pooled = (_std(l) + _std(r)) / 2 + 1e-9
            best = max(best, d / pooled)
        return best


@REGISTRY.model
class HMM(_Rolling):
    name, family = "hmm", "probabilistic"
    assumptions = ["discrete latent states", "Markov transitions"]
    limitations = ["state count must be chosen"]

    def score(self, w):
        med = sorted(w)[len(w) // 2]
        states = [1 if v > med else 0 for v in w]
        switches = sum(1 for i in range(1, len(states)) if states[i] != states[i - 1])
        return switches / len(states)


@REGISTRY.model
class GaussianProcess(_Rolling):
    name, family = "gaussian_process", "probabilistic"
    assumptions = ["smoothness", "kernel choice", "Gaussian noise"]
    limitations = ["kernel is the model"]

    def score(self, w):
        # roughness penalty under a smoothness prior
        d2 = [w[i - 1] - 2 * w[i] + w[i + 1] for i in range(1, len(w) - 1)]
        return _std(d2) / (_std(w) + 1e-9)


def all_models():
    return [cls() for cls in REGISTRY.models.values()]
