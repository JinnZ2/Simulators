# SPDX-License-Identifier: CC0-1.0
"""missing_column_finder_stdlib: missing_column_finder.analyse() with the
standard library only.  EXPLORATORY, like the original: it scores nothing
and tests no prediction; every reading it prints is DERIVED.

    python3 ledger/toolkit/missing_column_finder_stdlib.py compare ANCHOR_CSV
    python3 ledger/toolkit/missing_column_finder_stdlib.py run ANCHOR_CSV

Work order TK-G1 (2026-11-23).  The original imports numpy and, through
holdout/phase_b.py, numpy again.  What replaces each part here:

  numpy arrays, np.sum       lists, math.fsum
  phase_b._wls, phase_b.dummy  _wls and dummy below, same formulas
  np.linalg.lstsq            Householder QR on the weighted design, columns
                             scaled to unit length first
  np.linalg.matrix_rank      count of QR diagonal entries above
                             max(rows, cols) * eps * the largest one
  np.random.default_rng      relational-playground/playground/numpy_stream.py
                             (PCG64 replayed in the standard library), plus
                             two calls it does not carry, written here:
                             permutation(n) and the array form random(n).
                             permutation follows numpy's shuffle: for i from
                             n-1 down to 1, j = masked rejection draw on the
                             32-bit stream in [0, i], swap.  Checked against
                             numpy by `compare`, not assumed.

Not ported: synthetic() and gate().  They draw with numpy's normal, uniform,
choice and integers, which numpy_stream does not replay.  The gate for this
tool is ledger/toolkit/gate/gate_missing_column_finder.py.

Added, not in the original: analyse() takes columns, binary, groupings and
study as arguments.  The defaults are the original's, so the default call
is the original's call.  The gate uses the arguments to read synthetic
columns.

`compare` runs the original (numpy needed for that one command) and this
port on the same rows and prints every output number side by side.
"""
import csv
import hashlib
import io
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, "relational-playground", "playground"))

import numpy_stream  # noqa: E402  (standard library only)

BINARY = {
    "Experimental.setting": ("Greenhouse", "Field"), "Approach": ("Self-Sterilized", "Self-Other"),
    "Phase1.culti": ("Monoculture", "Community"), "SoilTp": ("Whole soil", "Inoculum"),
    "Life.form": ("Woody", "Nonwoody"), "F.H": ("Greenhouse", "Field"),
    "Sp.origin": ("Non-native", "Native"),
}
COLUMNS = ["Experimental.setting", "Phase2.time", "Approach", "Phase1.culti", "SoilTp",
           "Life.form", "F.H", "Sp.origin", "MAT", "MAP", "AI", "Latitude.abs"]
GROUPINGS = ["Author", "region", "Year", "Species", "Family"]
REGION_DEG = 20
N_PERM = 499
MIN_EXCESS = 0.02
PERM_SEED = 20261122
ANCHOR_SHA = "e2ea825c7bb1372dc2b9a2d1c46f1c2a14f78b466f0a7f382bacb0c129a29438"
TOLERANCE = 1e-9
EXPIRY = {
    "Author": "a per-study methods table joined on Author: soil source and storage, "
              "sterilisation method, pot volume, inoculum fraction, watering and light regime",
    "region": "site covariates beyond MAT, MAP and AI joined on coordinates: soil pH, "
              "texture, total N and P, land-use history",
    "Year": "method-era fields per study: protocol family, sterilisation method and "
            "response metric as they changed over publication years",
    "Species": "species traits joined on Species: mycorrhizal type, N-fixing status, "
               "growth rate, seed mass",
    "Family": "lineage traits joined on Family: mycorrhizal type, N-fixing status, "
              "a phylogeny for the sampled families",
}
fsum = math.fsum


# ----------------------------------------------------------- numpy's stream
class Rng:
    """numpy.random.default_rng(seed) for the three calls the finder makes."""

    def __init__(self, seed):
        self.g = numpy_stream.default_rng(seed)

    def _interval(self, top):
        if top == 0:
            return 0
        mask = (1 << top.bit_length()) - 1
        while True:
            v = self.g._next32() & mask
            if v <= top:
                return v

    def permutation(self, n):
        a = list(range(n))
        for i in range(n - 1, 0, -1):
            j = self._interval(i)
            a[i], a[j] = a[j], a[i]
        return a

    def random(self, n):
        return [self.g.random() for _ in range(n)]


# ------------------------------------------------------------------ numbers
def _num(s):
    try:
        x = float(s)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def dummy(col, one, zero):
    def f(r):
        if r[col] == one:
            return 1.0
        if r[col] == zero:
            return 0.0
        return None
    return f


def _xfun(col, binary):
    if col in binary:
        return dummy(col, *binary[col])
    return lambda r: _num(r[col])


def _region(r):
    la, lo = _num(r.get("Latitude")), _num(r.get("Longitude"))
    if la is None or lo is None:
        return None
    return "lat%+04d lon%+04d" % (math.floor(la / REGION_DEG) * REGION_DEG,
                                  math.floor(lo / REGION_DEG) * REGION_DEG)


def _label(r, g):
    if g == "region":
        return _region(r)
    v = r.get(g)
    return v if v not in (None, "", "NA") else None


def _wmean(y, w):
    return fsum(a * b for a, b in zip(w, y)) / fsum(w)


def _wls(x, y, w):
    xm, ym = _wmean(x, w), _wmean(y, w)
    sxx = fsum(wi * (xi - xm) ** 2 for wi, xi in zip(w, x))
    slope = fsum(wi * (xi - xm) * (yi - ym) for wi, xi, yi in zip(w, x, y)) / sxx
    return slope, ym - slope * xm


def tau2_intercept(y, v):
    w = [1.0 / a for a in v]
    ym = _wmean(y, w)
    q = fsum(wi * (yi - ym) ** 2 for wi, yi in zip(w, y))
    c = fsum(w) - fsum(wi * wi for wi in w) / fsum(w)
    return max(0.0, (q - (len(y) - 1)) / c)


def _sst(y, w):
    m = _wmean(y, w)
    return fsum(wi * (yi - m) ** 2 for wi, yi in zip(w, y))


def eta2(e, w, codes, ngroups):
    sw = [0.0] * ngroups
    swe = [0.0] * ngroups
    for ei, wi, c in zip(e, w, codes):
        sw[c] += wi
        swe[c] += wi * ei
    m = fsum(swe) / fsum(sw)
    between = fsum(sw[k] * (swe[k] / sw[k] - m) ** 2 for k in range(ngroups) if sw[k] > 0)
    total = fsum(wi * (ei - m) ** 2 for ei, wi in zip(e, w))
    return between / total if total > 0 else 0.0


def _codes(labels):
    names = sorted(set(labels))
    ix = {n: i for i, n in enumerate(names)}
    return [ix[x] for x in labels], names


def _verdict(obs, null):
    mean = fsum(null) / len(null)
    top = max(null)
    return {"share": obs, "null_mean": mean, "null_max": top, "excess": obs - mean,
            "flag": bool(obs > top and obs - mean >= MIN_EXCESS)}


def lstsq(A, b):
    """Least squares by Householder QR.  A: list of rows.  Returns (beta, rank)."""
    m, n = len(A), len(A[0])
    scale = [math.sqrt(fsum(A[i][j] ** 2 for i in range(m))) or 1.0 for j in range(n)]
    R = [[A[i][j] / scale[j] for j in range(n)] for i in range(m)]
    y = list(b)
    for k in range(n):
        norm = math.sqrt(fsum(R[i][k] ** 2 for i in range(k, m)))
        if norm == 0.0:
            continue
        alpha = -norm if R[k][k] >= 0 else norm
        vk = [R[i][k] for i in range(k, m)]
        vk[0] -= alpha
        vn = fsum(t * t for t in vk)
        if vn == 0.0:
            continue
        for j in range(k, n):
            s = 2.0 * fsum(vk[i - k] * R[i][j] for i in range(k, m)) / vn
            for i in range(k, m):
                R[i][j] -= s * vk[i - k]
        s = 2.0 * fsum(vk[i - k] * y[i] for i in range(k, m)) / vn
        for i in range(k, m):
            y[i] -= s * vk[i - k]
    diag = [abs(R[k][k]) for k in range(n)]
    rank = sum(d > max(m, n) * sys.float_info.epsilon * max(diag) for d in diag)
    beta = [0.0] * n
    for k in range(n - 1, -1, -1):
        beta[k] = (y[k] - fsum(R[k][j] * beta[j] for j in range(k + 1, n))) / R[k][k]
    return [beta[j] / scale[j] for j in range(n)], rank


# ------------------------------------------------------------------ analyse
def analyse(rows, perm_seed=PERM_SEED, n_perm=N_PERM, columns=None, binary=None,
            groupings=None, study="Author"):
    columns = COLUMNS if columns is None else columns
    binary = BINARY if binary is None else binary
    groupings = GROUPINGS if groupings is None else groupings
    base = []
    for r in rows:
        y, v = _num(r["rr"]), _num(r["var"])
        if y is None or v is None or not v > 0:
            continue
        base.append((r, y, v))
    y = [b[1] for b in base]
    v = [b[2] for b in base]
    t0 = tau2_intercept(y, v)
    w = [1.0 / (vi + t0) for vi in v]
    out = {"rows": len(base), "studies": len({b[0][study] for b in base}),
           "tau2_intercept": t0, "columns": {}, "groupings": {}, "candidates": []}

    X = {}
    for col in columns:
        f = _xfun(col, binary)
        x = [f(b[0]) for b in base]
        X[col] = x
        ok = [i for i, xi in enumerate(x) if xi is not None]
        xs = [x[i] for i in ok]
        if len(ok) < 3 or max(xs) - min(xs) == 0:
            out["columns"][col] = {"share_alone": None, "rows": len(ok), "slope": None,
                                   "state": "not checkable (no variation on this side)"}
            continue
        ys, ws = [y[i] for i in ok], [w[i] for i in ok]
        slope, icpt = _wls(xs, ys, ws)
        sse = fsum(wi * (yi - icpt - slope * xi) ** 2 for wi, xi, yi in zip(ws, xs, ys))
        out["columns"][col] = {"share_alone": 1.0 - sse / _sst(ys, ws), "rows": len(ok),
                               "slope": slope, "state": "fitted"}

    used = [c for c in columns if out["columns"][c]["state"] == "fitted"]
    full = [i for i in range(len(base)) if all(X[c][i] is not None for c in used)]
    yf, wf = [y[i] for i in full], [w[i] for i in full]
    A = [[1.0] + [X[c][i] for c in used] for i in full]
    sq = [math.sqrt(a) for a in wf]
    beta, rank = lstsq([[a * s for a in row] for row, s in zip(A, sq)],
                       [a * s for a, s in zip(yf, sq)])
    e = [yi - fsum(a * b for a, b in zip(row, beta)) for yi, row in zip(yf, A)]
    rws = [base[i][0] for i in full]
    together = 1.0 - fsum(wi * ei * ei for wi, ei in zip(wf, e)) / _sst(yf, wf)
    out["together"] = {"share": together, "left": 1.0 - together, "rows": len(full),
                       "columns_used": used, "rank": rank}

    rng = Rng(perm_seed)
    n = len(e)
    scode, snames = _codes([r[study] for r in rws])
    S = len(snames)
    s_w, s_we = [0.0] * S, [0.0] * S
    for ei, wi, c in zip(e, wf, scode):
        s_w[c] += wi
        s_we[c] += wi * ei
    s_m = [a / b for a, b in zip(s_we, s_w)]
    e_in = [ei - s_m[c] for ei, c in zip(e, scode)]
    order0 = sorted(range(n), key=lambda i: scode[i])

    null = []
    for _ in range(n_perm):
        p = rng.permutation(n)
        null.append(eta2([e[i] for i in p], [wf[i] for i in p], scode, S))
    out["groupings"][study] = {"groups": S, "lab": _verdict(eta2(e, wf, scode, S), null),
                               "between_study": None, "within_study": None}

    for g in [x for x in groupings if x != study]:
        labels = [_label(r, g) for r in rws]
        have = [x is not None for x in labels]
        nh = sum(have)
        rec = {"rows_labelled": nh, "between_study": None, "within_study": None, "lab": None}
        if nh < 3:
            out["groupings"][g] = dict(rec, groups=0)
            continue
        gcode, gnames = _codes([x if x is not None else "\0" for x in labels])
        G = len(gnames)
        rec["groups"] = len({x for x in labels if x is not None})
        modal = [-1] * S
        per = [[0.0] * G for _ in range(S)]
        seen = [False] * S
        for i in range(n):
            if have[i]:
                per[scode[i]][gcode[i]] += wf[i]
                seen[scode[i]] = True
        for s in range(S):
            if seen[s]:
                modal[s] = per[s].index(max(per[s]))
        ks = [s for s in range(S) if modal[s] >= 0]
        if len(ks) >= 3 and len({modal[s] for s in ks}) > 1:
            sm, swt, mc = [s_m[s] for s in ks], [s_w[s] for s in ks], [modal[s] for s in ks]
            null = []
            for _ in range(n_perm):
                p = rng.permutation(len(sm))
                null.append(eta2([sm[i] for i in p], [swt[i] for i in p], mc, G))
            rec["between_study"] = _verdict(eta2(sm, swt, mc, G), null)
        by_s = {}
        for i in range(n):
            if have[i]:
                by_s.setdefault(scode[i], set()).add(gcode[i])
        idx = [i for i in range(n) if have[i]]
        gh = [gcode[i] for i in idx]
        if any(len(x) > 1 for x in by_s.values()):
            obs = eta2([e_in[i] for i in idx], [wf[i] for i in idx], gh, G)
            null = []
            for _ in range(n_perm):
                u = rng.random(n)
                r_ = sorted(range(n), key=lambda i: (scode[i], u[i]))
                ep, wp = [0.0] * n, [0.0] * n
                for a, b in zip(order0, r_):
                    ep[a], wp[a] = e_in[b], wf[b]
                null.append(eta2([ep[i] for i in idx], [wp[i] for i in idx], gh, G))
            rec["within_study"] = _verdict(obs, null)
        else:
            rec["within_study"] = "nested in %s (constant inside every study)" % study
        rec["top"] = []
        gw, gwe, gn = [0.0] * G, [0.0] * G, [0] * G
        for i in idx:
            gw[gcode[i]] += wf[i]
            gwe[gcode[i]] += wf[i] * e[i]
            gn[gcode[i]] += 1
        gm = [gwe[k] / (gw[k] if gw[k] > 0 else 1) for k in range(G)]
        for k in sorted(range(G), key=lambda k: -abs(gm[k]) * (gn[k] >= 20))[:3]:
            if gn[k] >= 20:
                rec["top"].append((gnames[k].encode("ascii", "replace").decode(), gm[k], gn[k]))
        out["groupings"][g] = rec

    for g in groupings:
        rec = out["groupings"][g]
        hits = [k for k in ("lab", "between_study", "within_study")
                if isinstance(rec.get(k), dict) and rec[k]["flag"]]
        if hits:
            out["candidates"].append({
                "clusters_by": g, "tests_flagged": hits, "groups": rec["groups"],
                "excess": {k: rec[k]["excess"] for k in hits},
                "top": rec.get("top", []),
                "expiry_condition": EXPIRY.get(g, "NOT RECORDED")})
    return out


# ------------------------------------------------------------------ compare
def flatten(o, path=""):
    """Every number in an analyse() result, with its path."""
    if isinstance(o, bool) or o is None or isinstance(o, str):
        return [(path, o)] if isinstance(o, (bool, str)) or o is None else []
    if isinstance(o, (int, float)):
        return [(path, o)]
    if isinstance(o, dict):
        return [x for k in o for x in flatten(o[k], "%s/%s" % (path, k))]
    return [x for i, v in enumerate(o) for x in flatten(v, "%s[%d]" % (path, i))]


def load(path):
    raw = open(path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != ANCHOR_SHA:
        raise SystemExit("anchor_studies.csv sha256 mismatch (%s): stop" % sha)
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace"), newline="")))


def compare(path):
    rows = load(path)
    port = dict(flatten(analyse(rows)))
    import missing_column_finder as original   # numpy; this command only
    import numpy
    orig = dict(flatten(_plain(original.analyse(rows))))
    print("anchor_studies.csv sha256 %s (asserted), %d rows" % (ANCHOR_SHA, len(rows)))
    print("numpy %s; tolerance %.0e; seed %d; shuffles %d" % (numpy.__version__, TOLERANCE,
                                                             PERM_SEED, N_PERM))
    print("%-58s %22s %22s %10s" % ("output", "original", "port", "abs diff"))
    over = numbers = other_bad = 0
    for k in list(orig) + [k for k in port if k not in orig]:
        a, b = orig.get(k, "ABSENT"), port.get(k, "ABSENT")
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) \
                and not isinstance(a, bool) and not isinstance(b, bool):
            d = abs(a - b)
            numbers += 1
            over += d > TOLERANCE
            fmt = "%22d %22d" if isinstance(a, int) and isinstance(b, int) else "%22.15g %22.15g"
            print(("%-58s " + fmt + " %10.1e%s") % (k, a, b, d, "  EXCEEDS" if d > TOLERANCE else ""))
        elif a != b:
            other_bad += 1
            print("%-58s %22s %22s %10s" % (k, str(a)[:22], str(b)[:22], "DIFFERS"))
    print("numbers compared: %d; above tolerance: %d; non-numeric cells that differ: %d"
          % (numbers, over, other_bad))


def _plain(o):
    """numpy scalars and tuples -> plain Python, so both sides flatten alike."""
    if isinstance(o, dict):
        return {k: _plain(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_plain(v) for v in o]
    if hasattr(o, "item") and not isinstance(o, (str, bytes)):
        return o.item()
    return o


def main():
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "compare":
        return compare(a[1])
    if len(a) == 2 and a[0] == "run":
        for k, val in flatten(analyse(load(a[1]))):
            print("%-58s %s" % (k, val))
        return
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
