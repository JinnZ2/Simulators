"""Transitions along a swept variable: steepest change, variance peak, hysteresis."""


def read(xs, means, variances=None):
    if len(xs) < 3:
        return dict(state="NOT ESTIMABLE", reason="fewer than three levels")
    slopes = [(means[i + 1] - means[i]) / (xs[i + 1] - xs[i]) for i in range(len(xs) - 1)]
    i = max(range(len(slopes)), key=lambda k: abs(slopes[k]))
    out = dict(steepest_between=(xs[i], xs[i + 1]), steepest_slope=slopes[i],
               note="located to the sweep's own spacing, not finer")
    span = max(abs(v) for v in slopes)
    if max(means) == min(means):
        out["steepest_between"], out["note"] = "NONE", "flat response: no transition in the swept range"
    elif span - min(abs(v) for v in slopes) <= 1e-9 * span:
        out["steepest_between"], out["note"] = "NONE", "uniform slope: a ramp has no located transition"
    if variances is not None:
        j = max(range(len(variances)), key=lambda k: variances[k])
        out["variance_peak_at"] = xs[j]
        out["variance_peak"] = variances[j]
    return out


def hysteresis(xs, up, down):
    """up and down are the same levels swept in opposite directions."""
    gaps = [abs(u - d) for u, d in zip(up, down)]
    i = max(range(len(gaps)), key=lambda k: gaps[k])
    return dict(max_gap=gaps[i], at=xs[i], loop_area=sum((xs[k + 1] - xs[k]) * 0.5 * (gaps[k] + gaps[k + 1]) for k in range(len(xs) - 1)))
