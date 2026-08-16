"""
regress.py — Regress reported model improvement against criteria drift.

No external dependencies. Uses ordinary least squares formulas.
Produces: coefficient, standard error, R², and a lag analysis.

Hypothesis: β_drift > 0 → some reported improvement is ruler movement.
"""
from typing import List, Dict, Tuple, Optional
import math


def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for the incomplete beta. Numerical Recipes form."""
    tiny = 1e-30
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 200):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-12:
            break
    return h


def _betai(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log(1.0 - x))
    front = math.exp(lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def t_two_sided_p(t: float, df: int) -> Optional[float]:
    """
    Two-sided p for a t statistic. CD_007: the README's decision rule says
    'positive and significant' and the delivered module computed no test at
    all. Returns None when there is no degrees of freedom to test with --
    which is where the demo data sits.
    """
    if df < 1 or t != t or t in (float("inf"), float("-inf")):
        return None
    return _betai(0.5 * df, 0.5, df / (df + t * t))


def mean(vals: List[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0


def variance(vals: List[float]) -> float:
    m = mean(vals)
    return sum((x - m) ** 2 for x in vals) / len(vals) if vals else 0.0


def covariance(x: List[float], y: List[float]) -> float:
    if len(x) != len(y) or not x:
        return 0.0
    mx, my = mean(x), mean(y)
    return sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / len(x)


class RegressionResult:
    def __init__(self, intercept: float, slope: float, r2: float,
                 n: int, se_slope: float, se_intercept: float):
        self.intercept = intercept
        self.slope = slope
        self.r2 = r2
        self.n = n
        self.se_slope = se_slope
        self.se_intercept = se_intercept

    @property
    def df(self) -> int:
        return max(self.n - 2, 0)

    @property
    def t_slope(self) -> Optional[float]:
        if self.se_slope in (0.0, float("inf")) or self.df < 1:
            return None
        return self.slope / self.se_slope

    @property
    def p_slope(self) -> Optional[float]:
        t = self.t_slope
        return None if t is None else t_two_sided_p(t, self.df)

    def to_dict(self) -> Dict:
        # CD_007: r_squared was emitted as 1.0 at n = 2 -- arithmetic, since
        # two points define a line -- next to an interpretation string that
        # said the data was insufficient. The guard was in the sentence and
        # not in the data. It is in the data now: below three points the
        # field is null and `insufficient` is true.
        enough = self.n >= 3
        t = self.t_slope
        p = self.p_slope
        return {
            "intercept": round(self.intercept, 6),
            "slope": round(self.slope, 6),
            "r_squared": round(self.r2, 6) if enough else None,
            "n": self.n,
            "df": self.df,
            "se_slope": round(self.se_slope, 6),
            "se_intercept": round(self.se_intercept, 6),
            "t_slope": round(t, 6) if t is not None else None,
            "p_slope": round(p, 6) if p is not None else None,
            "significant_at_05": (p is not None and p < 0.05),
            "insufficient": not enough,
            "interpretation": self._interpret(),
        }

    def _interpret(self) -> str:
        if self.n < 3:
            return ("Insufficient data for reliable inference "
                    "(n=%d, df=%d)." % (self.n, self.df))
        p = self.p_slope
        if p is None or p >= 0.05:
            return ("Slope %+.4f, but not significant (t=%s, df=%d, p=%s). "
                    "The decision rule reads the SIGN of a significant "
                    "slope; this one does not clear the test."
                    % (self.slope,
                       "n/a" if self.t_slope is None
                       else "%.2f" % self.t_slope,
                       self.df,
                       "n/a" if p is None else "%.3f" % p))
        parts = []
        if self.slope > 0:
            parts.append(
                f"Positive slope: +{self.slope:.4f} improvement per unit drift. "
                "Some reported gain may be criteria inflation."
            )
        elif self.slope < 0:
            parts.append(
                f"Negative slope: {self.slope:.4f}. Stricter criteria may mask real gains."
            )
        else:
            parts.append("Zero slope: reported improvement orthogonal to criteria drift.")
        parts.append(f"R² = {self.r2:.3f} — drift explains {self.r2*100:.1f}% of improvement variance.")
        parts.append(f"t = {self.t_slope:.2f}, df = {self.df}, "
                     f"p = {self.p_slope:.4f}.")
        return " ".join(parts)


def ols_regression(x: List[float], y: List[float]) -> RegressionResult:
    """Simple linear regression: y = intercept + slope * x."""
    n = len(x)
    if n < 2 or n != len(y):
        return RegressionResult(0.0, 0.0, 0.0, n, float('inf'), float('inf'))

    mx, my = mean(x), mean(y)
    var_x = variance(x)
    if var_x == 0:
        return RegressionResult(my, 0.0, 0.0, n, float('inf'), float('inf'))

    cov = covariance(x, y)
    slope = cov / var_x
    intercept = my - slope * mx

    # R²
    ss_res = sum((yi - (intercept + slope * xi)) ** 2 for xi, yi in zip(x, y))
    ss_tot = sum((yi - my) ** 2 for yi in y)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    # Standard errors (simplified, assumes homoskedasticity)
    mse = ss_res / (n - 2) if n > 2 else 0.0
    se_slope = math.sqrt(mse / (var_x * n)) if n > 2 else float('inf')
    se_intercept = math.sqrt(mse * (1.0 / n + (mx ** 2) / (var_x * n))) if n > 2 else float('inf')

    return RegressionResult(intercept, slope, r2, n, se_slope, se_intercept)


class DriftRegressor:
    """
    Builds time-series from store data and runs the core regression:

        Δscore_model = β₀ + β₁·composite_drift + ε

    Can also run with lag: does drift at t predict improvement at t+k?
    """

    def __init__(self, score_matrix: Dict[str, Dict[str, float]],
                 drift_metrics: "DriftMetrics"):
        """
        score_matrix: {model_name: {version_id: score}}
        drift_metrics: output from DriftEngine.compute_history()
        """
        self.score_matrix = score_matrix
        self.drift_metrics = drift_metrics
        # CD_004: version_order was [p["to_version"] ...], which drops the
        # FIRST criteria version and every score attached to it. A model
        # measured at the first and last version -- the longest baseline in
        # a dataset -- filtered down to one score and returned ([], []).
        # The from_version of the first pair is that missing head.
        pairs = drift_metrics.pairs
        self.version_order = (
            ([pairs[0]["from_version"]] if pairs else [])
            + [p["to_version"] for p in pairs])
        # transition -> (from_version, drift), so a delta can be paired with
        # the drift across the SAME interval rather than with whatever
        # happens to sit at that index.
        self.transition = {p["to_version"]:
                           (p["from_version"], p["composite_drift"])
                           for p in pairs}

    def span_drift(self, from_version: str, to_version: str):
        """
        Total composite drift across every transition between two versions.
        None if the pair is not spanned by the recorded transitions.

        CD_004: a model measured at the first and last version is the
        LONGEST baseline in a dataset and the most informative row in it.
        Pairing only single transitions silently discards exactly that row.
        """
        order = self.version_order
        if from_version not in order or to_version not in order:
            return None
        i, j = order.index(from_version), order.index(to_version)
        if j <= i:
            return None
        total = 0.0
        for k in range(i + 1, j + 1):
            entry = self.transition.get(order[k])
            if entry is None:
                return None
            total += entry[1]
        return total

    def regress_pooled(self, lag: int = 0, score_type: str = "delta"):
        """
        One fit over every model's observations.

        CD_006-adjacent: composite_drift is a property of the ARTIFACT, not
        of any model, so every per-model regression runs against the same
        x-vector. Four models gave four slopes -- of two different signs --
        from one criteria history, decided entirely by which model was
        picked. The quantity the design asks about is a property of the
        ruler, so the fit that answers it pools.
        """
        xs, ys = [], []
        for model in sorted(self.score_matrix):
            x, y = self.build_series(model, lag=lag, score_type=score_type)
            xs.extend(x)
            ys.extend(y)
        return ols_regression(xs, ys)

    def build_series(self, model_name: str, lag: int = 0,
                     score_type: str = "absolute") -> Tuple[List[float], List[float]]:
        """
        Returns (drift_values, improvement_values).

        score_type:
          "absolute"  — raw score at each version
          "delta"     — score change from previous version
          "relative"  — (score - baseline) / baseline
        """
        scores = self.score_matrix.get(model_name, {})
        if not scores:
            return [], []

        drifts: List[float] = []
        improvements: List[float] = []

        # Build ordered list of (version, score)
        ordered_scores = []
        for v in self.version_order:
            if v in scores:
                ordered_scores.append((v, scores[v]))

        if len(ordered_scores) < 2:
            return [], []

        # CD_003: the loop below used to run from i = 0 and set
        # improvement = 0.0 at the head, pairing a FABRICATED y with a real
        # drift value. For a model scored at v1.0 and v2.0 that planted zero
        # replaced a measured delta. A delta needs two endpoints, so the
        # series starts at the first transition, not at the first version.
        if score_type == "delta":
            for i in range(1, len(ordered_scores)):
                prev_v, prev_s = ordered_scores[i - 1]
                this_v, this_s = ordered_scores[i]
                # Drift across the SAME interval the delta spans. A model
                # scored at v1.0 and v3.1 skipped two versions, so its delta
                # is matched against the ruler movement over that whole
                # span, not against one transition of it.
                drift_val = self.span_drift(prev_v, this_v)
                if drift_val is None:
                    continue
                if (i - 1) >= lag:
                    drifts.append(drift_val)
                    improvements.append(this_s - prev_s)
            return drifts, improvements

        for i in range(len(ordered_scores)):
            version = ordered_scores[i][0]
            drift_val = self.transition.get(version, (None, 0.0))[1]

            if score_type == "absolute":
                imp = ordered_scores[i][1]
            else:  # relative
                base = ordered_scores[0][1] if ordered_scores[0][1] != 0 else 1.0
                imp = (ordered_scores[i][1] - base) / base

            if i >= lag:
                drifts.append(drift_val)
                improvements.append(imp)

        return drifts, improvements

    def regress(self, model_name: str, lag: int = 0,
                score_type: str = "delta") -> RegressionResult:
        x, y = self.build_series(model_name, lag=lag, score_type=score_type)
        return ols_regression(x, y)

    def regress_all_models(self, lag: int = 0,
                           score_type: str = "delta") -> Dict[str, RegressionResult]:
        results = {}
        for model in self.score_matrix:
            results[model] = self.regress(model, lag=lag, score_type=score_type)
        return results
