"""Closure diagnostic. Transport params read as RATES (1/yr) — the reading
that reproduces the published polar-only run."""

BOXES = ["NH", "TN", "TS", "SH"]
LIFETIME = {"NH": 15.6, "TN": 6.0, "TS": 6.0, "SH": 24.0}
RATE = {("NH", "TN"): 0.22, ("TN", "TS"): 0.45, ("TS", "SH"): 0.45}  # 1/yr
TG_PER_PPB = (1.78e20 / 4) * 1e-9 * 16.0 / 1e12

GISP2, WAIS, SCA = 700.0, 652.0, 746.0
PUB_SCA = {"NH": None, "TN": 88.0, "TS": 125.0, "SH": 10.0}


def rate(a, b):
    return RATE.get((a, b), RATE.get((b, a)))


def M():
    m = [[0.0] * 4 for _ in range(4)]
    for i, bi in enumerate(BOXES):
        m[i][i] = 1.0 / LIFETIME[bi]
        for j, bj in enumerate(BOXES):
            if i == j:
                continue
            k = rate(bi, bj)
            if k is None:
                continue
            m[i][i] += k
            m[i][j] -= k
    return m


def E(ppb):
    m = M()
    C = [ppb[b] * TG_PER_PPB for b in BOXES]
    return {BOXES[i]: sum(m[i][j] * C[j] for j in range(4)) for i in range(4)}


print("=" * 64)
print("D1  what C_TN reproduces the published +SCA TN = 88 Tg/yr?")
print("=" * 64)
lo, hi = 600.0, 900.0
for _ in range(200):
    mid = (lo + hi) / 2
    e = E({"NH": GISP2, "TN": mid, "TS": SCA, "SH": WAIS})
    if e["TN"] < 88.0:
        lo = mid
    else:
        hi = mid
tn_needed = (lo + hi) / 2
e = E({"NH": GISP2, "TN": tn_needed, "TS": SCA, "SH": WAIS})
print(f"C_TN required        {tn_needed:8.1f} ppb")
print(f"  (linear interp was {700 - 48/3:8.1f} ppb)")
print(f"resulting E_TS       {e['TS']:8.1f}   published 125")
print(f"resulting E_SH       {e['SH']:8.1f}   FIXED AT 10 in paper")
print(f"resulting tropics    {e['TN']+e['TS']:8.1f}   published 213")
print()

print("=" * 64)
print("D2  what C_SH keeps E_SH = 10 with C_TS = SCA?")
print("=" * 64)
lo, hi = 500.0, 900.0
for _ in range(200):
    mid = (lo + hi) / 2
    e2 = E({"NH": GISP2, "TN": tn_needed, "TS": SCA, "SH": mid})
    if e2["SH"] < 10.0:
        lo = mid
    else:
        hi = mid
sh_needed = (lo + hi) / 2
print(f"C_SH required        {sh_needed:8.1f} ppb")
print(f"WAIS observed        {WAIS:8.1f} ppb")
print(f"CLOSURE GAP          {sh_needed - WAIS:8.1f} ppb")
print()

print("=" * 64)
print("D3  attenuation A, both runs, rates reading")
print("=" * 64)
polar = E({"NH": GISP2, "TN": 700 - 48/3, "TS": 700 - 2*48/3, "SH": WAIS})
tp = polar["TN"] + polar["TS"]
print(f"polar-only tropics   {tp:8.1f}   published 163")
print(f"+SCA tropics (mine)  {e['TN']+e['TS']:8.1f}   published 213")
print(f"A (mine)             {tp/(e['TN']+e['TS']):8.3f}")
print(f"A (published)        {163/213:8.3f}")
