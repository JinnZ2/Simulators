"""One-time export of the numpy draws run 9 consumes (seed 0). Needs numpy; the
experiment itself does not. Writes fixtures/numpy_draws_seed0.json.

    python3 export_draws.py        # re-export; the test compares the file's sha256

Order of the stream, as in forest-model-ledger/model/base.py::simulate:
300 lognormal precipitation factors, then uniforms, one per ignition check.
run 9 consumes 1068 uniforms; 1500 are exported.
"""
import json, os
import numpy as np

sd, years, n_uniform = 0.35, 300, 1500
rng = np.random.default_rng(0)
pfacs = rng.lognormal(-0.5 * sd ** 2, sd, size=years)
uni = [rng.random() for _ in range(n_uniform)]
out = dict(source="numpy.random.default_rng(0); numpy %s" % np.__version__, drought_sd=sd,
           pfacs=[float(x).hex() for x in pfacs], uniforms=[float(x).hex() for x in uni])
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "numpy_draws_seed0.json"), "w") as f:
    json.dump(out, f, indent=0)
    f.write("\n")
print("exported", len(pfacs), "factors and", len(uni), "uniforms")
