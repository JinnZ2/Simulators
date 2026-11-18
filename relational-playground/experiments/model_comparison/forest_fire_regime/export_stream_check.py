"""One-time export (needs numpy): numpy's own output for an interleaved call
pattern, so playground/numpy_stream.py can be checked without numpy.

    python3 export_stream_check.py

Pattern per seed, 700 calls: call i uses i % 7 -> 0,1,3,6 random() ; 2 integers(100) ;
4 integers(120) ; 5 integers(3). Then a 5 x 7 random block, read in C order.
"""
import json, os
import numpy as np

out = dict(source="numpy.random.default_rng(seed)", numpy_version=np.__version__, pattern=__doc__.split("Pattern")[1].strip(), seeds={})
for seed in (0, 2, 3, 4, 12345, 2 ** 40 + 7):
    g, vals = np.random.default_rng(seed), []
    for i in range(700):
        k = i % 7
        if k in (0, 1, 3, 6):
            vals.append(float(g.random()).hex())
        else:
            vals.append(int(g.integers({2: 100, 4: 120, 5: 3}[k])))
    out["seeds"][str(seed)] = dict(calls=vals, block=[float(v).hex() for v in g.random((5, 7)).ravel()])
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "numpy_stream_check.json"), "w") as f:
    json.dump(out, f, indent=0)
    f.write("\n")
print("exported", len(out["seeds"]), "seeds, numpy", np.__version__)
