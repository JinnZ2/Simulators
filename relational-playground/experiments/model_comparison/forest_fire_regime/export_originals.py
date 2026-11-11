"""One-time export (needs numpy and scipy): run the delivered run 6, 7, 8 code
and record its results at full precision, so originals.py can be checked
without either library.

    python3 export_originals.py

Reads forest-model-ledger/runs/run_6.py, run_7.py, run_8.py as delivered and
executes them unchanged. Each file's own loop prints rounded numbers; the loops
below repeat them with a fresh generator of the same seed and keep every digit.
Writes fixtures/originals_expected.json with library versions and source hashes.
"""
import contextlib, hashlib, io, json, os
import numpy as np
import scipy

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "forest-model-ledger", "runs"))
hx = lambda x: float(x).hex()


def load(n):
    path = os.path.join(RUNS, "run_%d.py" % n)
    with open(path, "rb") as f:
        raw = f.read()
    ns, buf = {}, io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(raw, path, "exec"), ns)
    return ns, hashlib.sha256(raw).hexdigest(), buf.getvalue()


out = dict(numpy_version=np.__version__, scipy_version=scipy.__version__, sources={}, printed={})

ns, sha, printed = load(7)
out["sources"]["run_7.py"], out["printed"]["run_7"] = sha, printed.splitlines()
ns["rng"] = np.random.default_rng(3)
rows = []
for dr in np.linspace(0, 1, 11):
    p = 0.2 + 0.75 * dr
    g, s = ns["grid_burn"](0.8, p)
    rows.append(dict(drought=hx(dr), p=hx(p), ode=hx(ns["ode_burn"](0.8, p)), grid_mean=hx(g), grid_sd=hx(s)))
out["run_7"] = rows

ns, sha, printed = load(8)
out["sources"]["run_8.py"], out["printed"]["run_8"] = sha, printed.splitlines()
ns["rng"] = np.random.default_rng(4)
rows = []
for dr in [0.2, 0.4, 0.5, 0.6, 0.7]:
    p = 0.2 + 0.75 * dr
    cells = []
    for s in [0, 0.05, 0.2, 1.0]:
        m, sd = ns["burn"](0.8, p, s)
        cells.append(dict(spot=s, mean=hx(m), sd=hx(sd)))
    rows.append(dict(drought=dr, ode=hx(ns["ode"](0.8, p)), cells=cells))
out["run_8"] = rows

ns, sha, printed = load(6)
out["sources"]["run_6.py"], out["printed"]["run_6"] = sha, printed.splitlines()


def stats(B):
    late = B[B[:, 0] > 1000]
    return dict(B_mean=hx(late[:, 1].mean()), swing=hx(late[:, 1].max() - late[:, 1].min()),
                tree_share=hx((late[:, 2] / late[:, 1]).mean()), Ls_min=hx(late[:, 3].min()), Ls_max=hx(late[:, 3].max()),
                last_row=[hx(v) for v in B[-1]])


r6 = dict(trait=[hx(v) for v in ns["trait"].ravel()], aff=[hx(v) for v in ns["aff"].ravel()], niche=[hx(v) for v in ns["niche"]],
          old_misclosure=[hx(v) for v in ns["mo"]], conserved={})
for thr in [0.6, 0.3, 0.5, 0.8, 1.2]:
    mc, fires, B = ns["conserved"](fire_thr=thr)
    r6["conserved"][repr(thr)] = dict(stats(B), fires=int(fires), mis_max=hx(np.abs(mc).max()), mis_last=hx(mc[-1]))
out["run_6"] = r6

with open(os.path.join(HERE, "fixtures", "originals_expected.json"), "w") as f:
    json.dump(out, f, indent=0)
    f.write("\n")
print("exported runs 6, 7, 8 on numpy", np.__version__, "scipy", scipy.__version__)
