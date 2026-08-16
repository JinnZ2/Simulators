"""
regress.py — Regress reported model improvement against criteria drift.

No external dependencies. Uses ordinary least squares formulas.
Produces: coefficient, standard error, R², and a lag analysis.

Hypothesis: β_drift > 0 → some reported improvement is ruler movement.
"""
from typing import List, Dict, Tuple, Optional
import math


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

    def to_dict(self) -> Dict:
        return {
            "intercept": round(self.intercept, 6),
            "slope": round(self.slope, 6),
            "r_squared": round(self.r2, 6),
            "n": self.n,
            "se_slope": round(self.se_slope, 6),
            "se_intercept": round(self.se_intercept, 6),
            "interpretation": self._interpret(),
        }

    def _interpret(self) -> str:
        if self.n < 3:
            return "Insufficient data for reliable inference."
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
        self.version_order = [p["to_version"] for p in drift_metrics.pairs]

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

        # Pair with drift
        for i in range(len(ordered_scores)):
            version = ordered_scores[i][0]
            # Find drift for transition INTO this version
            drift_val = 0.0
            for p in self.drift_metrics.pairs:
                if p["to_version"] == version:
                    drift_val = p["composite_drift"]
                    break

            if score_type == "absolute":
                imp = ordered_scores[i][1]
            elif score_type == "delta":
                imp = ordered_scores[i][1] - ordered_scores[i - 1][1] if i > 0 else 0.0
            else:  # relative
                base = ordered_scores[0][1] if ordered_scores[0][1] != 0 else 1.0
                imp = (ordered_scores[i][1] - base) / base

            # Lag handling: skip first `lag` points for improvement
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
