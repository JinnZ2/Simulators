"""L0 audit: budget closure, boundary audit line, leak-vs-noise rule.

misclosure = (pools_end - pools_start) - (boundary_in - boundary_out)

Verdicts (closed set):
  CLOSED   |misclosure| <= numerical tolerance (rel_tol * gross throughput)
  NOISE    above numerical tolerance but <= k_sigma * measurement error
  LEAK     above both
  VOID     budget not represented in the model -- never reported as closed
A simulation has no measurement error: sigma_meas stays None (void) and NOISE
is unreachable. With field data sigma_meas comes from the instrument, and the
rule becomes the leak-vs-noise test proper.
Multi-budget guard: overall PASS needs every NON-VOID budget closed; VOID
budgets are listed, because one closed budget cannot rule out a compensating
error in a budget nobody is keeping.
"""
from . import base

BUDGETS = {
    "N": (base.N_POOLS, base.N_BOUND_IN, base.N_BOUND_OUT),
    "water": (base.W_POOLS, base.W_BOUND_IN, base.W_BOUND_OUT),
    "C": None, "P": None, "energy": None,     # VOID: not represented in the base model
}


def verdict(mis, throughput, rel_tol=1e-9, sigma_meas=None, k_sigma=2.0):
    if abs(mis) <= rel_tol * max(throughput, 1.0):
        return "CLOSED"
    if sigma_meas is not None and abs(mis) <= k_sigma * sigma_meas:
        return "NOISE"
    return "LEAK"


def audit(res, rel_tol=1e-9, sigma_meas=None):
    y0, y, ix = res["y0"], res["y"], base.IX
    out = {}
    for name, spec in BUDGETS.items():
        if spec is None:
            out[name] = dict(verdict="VOID", misclosure=None)
            continue
        pools, bin_, bout = spec
        dpool = sum(y[ix[k]] - y0[ix[k]] for k in pools)
        fin = sum(y[ix[k]] for k in bin_)
        fout = sum(y[ix[k]] for k in bout)
        mis = dpool - (fin - fout)
        out[name] = dict(
            verdict=verdict(mis, fin + fout, rel_tol, (sigma_meas or {}).get(name)),
            misclosure=mis, d_pools=dpool, boundary_in=fin, boundary_out=fout,
            terms={k: (None if k in base.VOID_TERMS else float(y[ix[k]])) for k in bin_ + bout},
        )
    live = [v["verdict"] for v in out.values() if v["verdict"] != "VOID"]
    out["_overall"] = "PASS" if all(v == "CLOSED" for v in live) else "FAIL"
    out["_void_budgets"] = [k for k, v in out.items() if isinstance(v, dict) and v["verdict"] == "VOID"]
    return out


def report(a):
    lines = []
    for k in BUDGETS:
        v = a[k]
        if v["verdict"] == "VOID":
            lines.append(f"{k:7s} VOID    not represented; no closure claimed")
            continue
        lines.append(f"{k:7s} {v['verdict']:7s} misclosure {v['misclosure']:+.3e}   d_pools {v['d_pools']:+.4f}  in {v['boundary_in']:.4f}  out {v['boundary_out']:.4f}")
        lines.append("        boundary: " + "  ".join(f"{t}={'void' if x is None else format(x, '.4f')}" for t, x in v["terms"].items()))
    lines.append(f"overall {a['_overall']}  (void budgets: {', '.join(a['_void_budgets']) or 'none'})")
    return "\n".join(lines)
