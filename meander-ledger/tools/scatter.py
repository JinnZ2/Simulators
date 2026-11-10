"""TOO-SMOOTH CHECK on wavelength / width (work order task 2). stdlib only.

    python3 tools/scatter.py                 # reads data/raw/... (run tools/fetch_data.py first)
    python3 tools/scatter.py --csv PATH      # any copy; the hash is printed, not trusted

Reads the dataset on LINEAR axes first, then on log-log, and reports what the log-log
view compresses. Every number printed is DERIVED from the pinned file; nothing here is
OBSERVED by this folder. The dataset's own measurement chain is in ledger/data_sources.yaml.

Unit of analysis [CHOICE 1]: the file has one row per centerline point, and meander-level
fields (Wavelength (m), Meander length (m), Sinuosity) repeat across the points of one
meander. A meander is one distinct (Wavelength, Meander length, Sinuosity) triple; its
width is the median point width. Point rows are reported beside it, never pooled into it.
Sentinels [CHOICE 2]: Wavelength <= 0 (the file carries -9999) is excluded and counted.
The ratio band 10..14 is the work order's recalled value, not a fitted one.
"""
import collections, csv, hashlib, math, os, random, statistics as st, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from tools import fetch_data

COL_W, COL_L, COL_ML, COL_S = "Water-surface width (m)", "Wavelength (m)", "Meander length (m)", "Sinuosity"
COL_L2 = "wavelength"
BAND = (10.0, 14.0)
SEED = 0


def num(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def meanders(rows):
    """Group point rows into meanders. Returns (list of dicts, counts)."""
    groups, sentinel, nowidth = {}, 0, 0
    for r in rows:
        lam, w = num(r[COL_L]), num(r[COL_W])
        if lam is None or lam <= 0:
            sentinel += 1
            continue
        if w is None or w <= 0:
            nowidth += 1
            continue
        key = (r[COL_L], r[COL_ML], r[COL_S])
        g = groups.setdefault(key, dict(lam=lam, widths=[], slopes=[], geo=[], prov=[], cls=[], lam2=[]))
        g["widths"].append(w)
        s = num(r.get("Slope (degrees)"))
        if s is not None:
            g["slopes"].append(s)
        g["geo"].append(r.get("MAJOR1", "").strip() or "void")
        g["prov"].append(r.get("Province", "").strip() or "void")
        g["cls"].append(r.get("Meander Class", "").strip() or "void")
        l2 = num(r.get(COL_L2))
        if l2 is not None:
            g["lam2"].append(l2)
    out = []
    mixed = dict(geo=0, prov=0, cls=0)
    for g in groups.values():
        # [CHOICE 3] a meander's label is its points' most common value, ties broken by the
        # value itself. A first version used max(set(xs)), whose tie order follows the
        # string hash, so labels changed between runs; meanders with >1 distinct label
        # are counted and reported, never silently resolved.
        mode = lambda xs: sorted(collections.Counter(xs).items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        for k in mixed:
            mixed[k] += len(set(g[k])) > 1
        out.append(dict(lam=g["lam"], w=st.median(g["widths"]), npts=len(g["widths"]),
                        w_spread=(max(g["widths"]) / min(g["widths"])),
                        slope=(st.median(g["slopes"]) if g["slopes"] else None),
                        geo=mode(g["geo"]), prov=mode(g["prov"]), cls=mode(g["cls"]),
                        lam2=(st.median(g["lam2"]) if g["lam2"] else None)))
    return out, dict(point_rows=len(rows), sentinel=sentinel, no_width=nowidth, meanders=len(out),
                     mixed_geo=mixed["geo"], mixed_prov=mixed["prov"], mixed_cls=mixed["cls"])


def q(xs, p):
    xs = sorted(xs)
    i = (len(xs) - 1) * p
    lo, hi = math.floor(i), math.ceil(i)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def ols(x, y):
    """slope, intercept, r2. None on a degenerate x."""
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    if sxx == 0:
        return None
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    syy = sum((b - my) ** 2 for b in y)
    b = sxy / sxx
    r2 = (sxy * sxy) / (sxx * syy) if syy else None
    return b, my - b * mx, r2


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    if len(x) < 3:
        return None
    fit = ols(ranks(x), ranks(y))
    if fit is None or fit[2] is None:
        return None
    rho = math.sqrt(fit[2])
    return rho if fit[0] >= 0 else -rho


def ratio_summary(R):
    lo, hi = BAND
    return dict(n=len(R), median=st.median(R), p25=q(R, .25), p75=q(R, .75), p05=q(R, .05), p95=q(R, .95),
                min=min(R), max=max(R), in_band=sum(lo <= r <= hi for r in R) / len(R),
                below_5=sum(r < 5 for r in R) / len(R), above_30=sum(r > 30 for r in R) / len(R),
                above_100=sum(r > 100 for r in R) / len(R))


def histogram(R, edges, width=50):
    counts = [0] * (len(edges))
    for r in R:
        for i in range(len(edges) - 1):
            if edges[i] <= r < edges[i + 1]:
                counts[i] += 1
                break
        else:
            counts[-1] += 1
    top = max(counts) or 1
    lines = []
    for i, c in enumerate(counts):
        lab = f"{edges[i]:>5.0f}-{edges[i+1]:<5.0f}" if i < len(edges) - 1 else f"{edges[-1]:>5.0f}+     "
        lines.append(f"  {lab} {c:6d} {'#' * round(width * c / top)}")
    return lines


def ascii_scatter(x, y, xmax, ymax, cols=60, rows=20, lines_ratio=(10, 14)):
    """LINEAR axes. Points beyond the window are counted, not drawn."""
    grid = [[" "] * cols for _ in range(rows)]
    off = 0
    for a, b in zip(x, y):
        if a > xmax or b > ymax:
            off += 1
            continue
        c = min(cols - 1, int(a / xmax * cols))
        r = rows - 1 - min(rows - 1, int(b / ymax * rows))
        cur = grid[r][c]
        grid[r][c] = "." if cur == " " else ("o" if cur == "." else "#")
    for k in lines_ratio:                      # the band, drawn as lambda = k * W
        for c in range(cols):
            w = (c + 0.5) / cols * xmax
            r = rows - 1 - int(k * w / ymax * rows)
            if 0 <= r < rows and grid[r][c] == " ":
                grid[r][c] = "-"
    out = [f"  lambda (m) 0..{ymax:.0f} linear  ^"]
    out += ["  |" + "".join(row) for row in grid]
    out.append("  +" + "-" * cols + f"> W (m) 0..{xmax:.0f} linear")
    out.append(f"  . 1 pt  o 2  # 3+   '-' lambda = 10 W and 14 W   off-window: {off}")
    return out


def null_shuffle(M, seed=SEED, reps=200):
    """Slot 5 null: break the pairing, keep both marginals. What does log-log show then?"""
    rng = random.Random(seed)
    lw = [math.log10(m["w"]) for m in M]
    ll = [math.log10(m["lam"]) for m in M]
    r2s, meds = [], []
    for _ in range(reps):
        s = ll[:]
        rng.shuffle(s)
        r2s.append(ols(lw, s)[2])
        meds.append(st.median(10 ** (b - a) for a, b in zip(lw, s)))
    return dict(reps=reps, r2_max=max(r2s), median_ratio_p05=q(meds, .05), median_ratio_p95=q(meds, .95))


def group_table(M, key, min_n=30):
    groups = {}
    for m in M:
        groups.setdefault(m[key], []).append(m["lam"] / m["w"])
    rows = []
    for g, R in groups.items():
        if len(R) >= min_n:
            rows.append((g, len(R), st.median(R), q(R, .25), q(R, .75), sum(BAND[0] <= r <= BAND[1] for r in R) / len(R)))
    small = sum(len(R) for g, R in groups.items() if len(R) < min_n)
    return sorted(rows, key=lambda t: -t[1]), small


def analyse(path):
    rows = load(path)
    M, counts = meanders(rows)
    R = [m["lam"] / m["w"] for m in M]
    lw = [math.log10(m["w"]) for m in M]
    ll = [math.log10(m["lam"]) for m in M]
    a = dict(counts=counts, ratio=ratio_summary(R))
    a["linear_fit"] = ols([m["w"] for m in M], [m["lam"] for m in M])
    a["loglog_fit"] = ols(lw, ll)
    lr = [math.log10(r) for r in R]
    a["sd_log10_ratio"] = st.pstdev(lr)
    a["sd_log10_w"] = st.pstdev(lw)
    a["null"] = null_shuffle(M)
    a["geo"] = group_table(M, "geo")
    a["prov"] = group_table(M, "prov")
    a["cls"] = group_table(M, "cls")
    sl = [(m["slope"], m["lam"] / m["w"]) for m in M if m["slope"] is not None]
    a["slope_n"] = len(sl)
    a["slope_rho"] = spearman([s for s, _ in sl], [r for _, r in sl]) if sl else None
    a["w_rho"] = spearman([m["w"] for m in M], R)
    l2 = [(m["lam"], m["lam2"], m["w"]) for m in M if m["lam2"] is not None]
    a["lam2_n"] = len(l2)
    a["lam2_rho"] = spearman([x for x, _, _ in l2], [y for _, y, _ in l2])
    a["lam2_ratio_median"] = st.median(y / w for _, y, w in l2) if l2 else None
    a["multi_point"] = sum(m["npts"] > 1 for m in M)
    a["w_spread_median"] = st.median(m["w_spread"] for m in M if m["npts"] > 1) if a["multi_point"] else None
    pts = [num(r[COL_L]) / num(r[COL_W]) for r in rows if (num(r[COL_L]) or 0) > 0 and (num(r[COL_W]) or 0) > 0]
    a["point_ratio"] = ratio_summary(pts)
    a["_M"], a["_R"] = M, R
    return a


def render(a, path):
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    c, r = a["counts"], a["ratio"]
    L = ["TOO-SMOOTH CHECK  wavelength / width   (all numbers DERIVED from the pinned file)",
         f"file sha256 {h[:16]}...  {'MATCH' if h == fetch_data.SHA256 else 'DIFFERS from pin'}",
         f"point rows {c['point_rows']}  sentinel lambda<=0 excluded {c['sentinel']}  width<=0 {c['no_width']}  meanders [CHOICE 1] {c['meanders']}",
         f"meanders whose points carry > 1 label [CHOICE 3]: geology {c['mixed_geo']}  province {c['mixed_prov']}  class {c['mixed_cls']}",
         "",
         "RATIO lambda/W, per meander (LINEAR summary)",
         f"  median {r['median']:.2f}   IQR {r['p25']:.2f} .. {r['p75']:.2f}   p05..p95 {r['p05']:.2f} .. {r['p95']:.2f}   min {r['min']:.3f}  max {r['max']:.0f}",
         f"  in recalled band 10..14: {r['in_band']:.3f}   below 5: {r['below_5']:.3f}   above 30: {r['above_30']:.3f}   above 100: {r['above_100']:.3f}",
         "  histogram (linear bins of the ratio):"]
    L += histogram(a["_R"], [0, 2, 4, 6, 8, 10, 12, 14, 16, 20, 30, 50, 100, 200])
    pr = a["point_ratio"]
    L += [f"  per POINT row instead (repeats a meander once per point): n {pr['n']} median {pr['median']:.2f}  in band {pr['in_band']:.3f}", ""]
    M = a["_M"]
    xmax, ymax = q([m["w"] for m in M], .95), q([m["lam"] for m in M], .95)
    L.append("LINEAR AXES (window = 95th percentile of each axis)")
    L += ascii_scatter([m["w"] for m in M], [m["lam"] for m in M], xmax, ymax)
    b, i, r2 = a["linear_fit"]
    bl, il, r2l = a["loglog_fit"]
    L += ["",
          "FITS",
          f"  linear  lambda = {b:.2f} W + {i:.0f}          R2 {r2:.3f}",
          f"  log-log log lambda = {bl:.3f} log W + {il:.3f}   R2 {r2l:.3f}",
          f"  sd log10(ratio) {a['sd_log10_ratio']:.3f}  vs  sd log10(W) {a['sd_log10_w']:.3f}",
          f"    -> one sd of the ratio is a factor {10 ** a['sd_log10_ratio']:.2f}; W spans a factor {10 ** a['sd_log10_w']:.2f} per sd",
          f"  Spearman(ratio, W) {a['w_rho']:+.3f}   (a constant ratio would read ~0)",
          "",
          "SLOT 5 NULL (pairing shuffled, marginals kept; seed 0, 200 reps)",
          f"  log-log R2 max under null {a['null']['r2_max']:.4f}   median ratio p05..p95 {a['null']['median_ratio_p05']:.2f} .. {a['null']['median_ratio_p95']:.2f}",
          "",
          "DEPENDENCE (groups with n >= 30 meanders; bank material is NOT in the file: MAJOR1 is mapped surface geology)"]
    for title, (tab, small) in (("MAJOR1 geology unit", a["geo"]), ("physiographic province", a["prov"]), ("dataset's own meander class", a["cls"])):
        L.append(f"  {title}   (meanders in groups < 30: {small})")
        L.append("    group                     n   median  p25..p75       in band")
        for g, n, med, p25, p75, ib in tab[:12]:
            L.append(f"    {g[:24]:24s} {n:5d}  {med:7.2f}  {p25:6.2f}..{p75:<7.2f}  {ib:.3f}")
    L += [f"  slope: Spearman(ratio, Slope degrees) {a['slope_rho']:+.3f} over {a['slope_n']} meanders",
          "",
          "SECOND WAVELENGTH COLUMN ('wavelength', from Scripts/Amplitude_Wavelength)",
          f"  meanders with it {a['lam2_n']}   Spearman with 'Wavelength (m)' {a['lam2_rho']:+.3f}   median wavelength/W {a['lam2_ratio_median']:.2f}",
          "",
          "WIDTH INSIDE ONE MEANDER",
          f"  meanders with > 1 point {a['multi_point']}   median max/min point width {a['w_spread_median']:.2f}"]
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("refused: tools/scatter.py has no selftest; run python3 tests/test_meander.py")
        sys.exit(2)
    path = sys.argv[sys.argv.index("--csv") + 1] if "--csv" in sys.argv else fetch_data.PATH
    if not os.path.exists(path):
        print(f"NOT_PRESENT {path}; run python3 tools/fetch_data.py")
        sys.exit(3)
    print(render(analyse(path), path))
