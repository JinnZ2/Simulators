# samples/

Captured demo output. One file per audit-grade layer.

- [`l0_demo.sample.txt`](l0_demo.sample.txt) — output of the L0
  demo (the `if __name__ == "__main__":` block in
  `../l0_physics_causality.py`) under `np.random.seed(0)` with the
  shipped constants.

Regenerate with:

```
MPLBACKEND=Agg python3 -c "
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt; plt.show = lambda *a, **k: None
import runpy
runpy.run_path('grounding-layers/l0_physics_causality.py', run_name='__main__')
" 2>&1 | tail -20 > grounding-layers/samples/l0_demo.sample.txt
```

The `MPLBACKEND=Agg` and `plt.show` monkeypatch suppress the
interactive window; only the diagnostic print block is captured.

The pinned numbers (violations count, drift, end positions) also live
in [`../tests/test_l0_physics_causality.py::TestDemoPinnedNumbers_GL_L0_PIN`](../tests/test_l0_physics_causality.py)
— if the sample drifts, that test surfaces the delta.
