"""
Four-box CH4 model, rebuilt from Lamantia et al. 2026 Methods.
Corrected: the model is FORWARD only. Concentrations are prescribed in
observed boxes, TN is interpolated, E = M.C directly. No inversion.
stdlib only.
"""

BOXES = ["NH", "TN", "TS", "SH"]
LIFETIME = {"NH": 15.6, "TN": 6.0, "TS": 6.0, "SH": 24.0}
MOLES_AIR_TOTAL = 1.78e20
MOLAR_MASS_CH4 = 16.0
TG_PER_PPB = (MOLES_AIR_TOTAL / 4) * 1e-9 * MOLAR_MASS_CH4 / 1e12

GISP2_PI = 700.0
WAIS_PI = 652.0          # IPD 48
SCA_PI = 746.0           # GISP2 + 46, = WAIS + 94  (both published offsets)

PUB_POLAR = {"NH": 36.0, "TN": 82.0, "TS": 81.0, "SH": 10.0}
PUB_SCA = {"TN": 88.0, "TS": 125.0}    # TS = 213 - 88


def build_M(T_pairs):
    M = [[0.0] * 4 for _ in range(4)]
    for i, bi in enumerate(BOXES):
        M[i][i] = 1.0 / LIFETIME[bi]
        for j, bj in enumerate(BOXES):
            if i == j:
                continue
            T = T_pairs.get((bi, bj), T_pairs.get((bj, bi)))
            if T is None:
                continue
            M[i][i] += 1.0 / T
            M[i][j] -= 1.0 / T
    return M


def E_of(ppb, T_pairs):
    M = build_M(T_pairs)
    C = [ppb[b] * TG_PER_PPB for b in BOXES]
    return {BOXES[i]: sum(M[i][j] * C[j] for j in range(4)) for i in range(4)}


def interp(frac):
    return GISP2_PI - (GISP2_PI - WAIS_PI) * frac


READINGS = {
    "as TIMES (yr)": {("NH", "TN"): 0.22, ("TN", "TS"): 0.45, ("TS", "SH"): 0.45},
    "as RATES (1/yr)": {("NH", "TN"): 1 / 0.22, ("TN", "TS"): 1 / 0.45,
                        ("TS", "SH"): 1 / 0.45},
}

for label, T_pairs in READINGS.items():
    print("=" * 68)
    print(f"TRANSPORT PARAMETER READ {label}")
    print("=" * 68)

    polar = {"NH": GISP2_PI, "TN": interp(1 / 3), "TS": interp(2 / 3), "SH": WAIS_PI}
    Ep = E_of(polar, T_pairs)
    withsca = dict(polar)
    withsca["TS"] = SCA_PI
    Es = E_of(withsca, T_pairs)

    print(f"{'box':<8}{'polar E':>10}{'pub':>7}{'+SCA E':>10}{'pub':>7}")
    for b in BOXES:
        p = PUB_POLAR[b]
        s = PUB_SCA.get(b, 10.0 if b == "SH" else None)
        ss = f"{s:.0f}" if s is not None else "-"
        print(f"{b:<8}{Ep[b]:>10.1f}{p:>7.0f}{Es[b]:>10.1f}{ss:>7}")
    tp, ts = Ep["TN"] + Ep["TS"], Es["TN"] + Es["TS"]
    print(f"{'tropics':<8}{tp:>10.1f}{163:>7}{ts:>10.1f}{213:>7}")
    print(f"{'A':<8}{tp / ts:>10.3f}{163 / 213:>7.3f}")
    print()

# ---- which transport time reproduces the observed IPD? -------------------
print("=" * 68)
print("CONSISTENCY  what NH-TN exchange time sustains IPD=48 at pub E?")
print("=" * 68)
print(f"{'T scale x':>11}{'implied NH-SH gradient ppb':>30}")
base = {("NH", "TN"): 0.22, ("TN", "TS"): 0.45, ("TS", "SH"): 0.45}


def solve4(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        for j in range(c, n + 1):
            M[c][j] /= pv
        for r in range(n):
            if r != c and M[r][c] != 0.0:
                f = M[r][c]
                for j in range(c, n + 1):
                    M[r][j] -= f * M[c][j]
    return [M[i][n] for i in range(n)]


for scale in [1, 2, 5, 10, 20, 50, 100]:
    T_pairs = {k: v * scale for k, v in base.items()}
    M = build_M(T_pairs)
    C = solve4(M, [PUB_POLAR[b] for b in BOXES])
    ppb = [c / TG_PER_PPB for c in C]
    print(f"{scale:>11}{ppb[0] - ppb[3]:>30.1f}")
print(f"{'observed':>11}{48.0:>30.1f}")
