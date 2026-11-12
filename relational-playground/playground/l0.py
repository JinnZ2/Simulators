"""ADDITION 1. L0 gate: every run closes its declared budgets before anything else is read.

    misclosure = (pools_end - pools_start) - (boundary_in - boundary_out)

The pool change comes from the integrated state. The boundary terms come from
the model's transfer table, integrated beside the state. A term in the state
equation that is not in the table shows up as misclosure.

Five budgets are always listed: mass, N, C, water, energy. Each is LIVE (pools
named) or VOID with a reason. A VOID budget is never read as closed.
Verdict rule, same as forest-model-ledger/ledger/toolkit/budget_closure.py:
CLOSED when |misclosure| <= rel_tol * max(throughput, pool scale), rel_tol 1e-9;
NOISE when it fails that but sits inside k_sigma * sigma_meas; else LEAK.
"""
BUDGETS = ("mass", "N", "C", "water", "energy")
REL_TOL = 1e-9


class Budget:
    def __init__(self, name, pools=None, void_reason=None, sigma_meas=None, units="UNDECLARED"):
        if name not in BUDGETS:
            raise ValueError("budget %r not in %r" % (name, BUDGETS))
        if (pools is None) == (void_reason is None):
            raise ValueError("%s: give pools (LIVE) or void_reason (VOID), exactly one" % name)
        self.name, self.pools, self.void_reason, self.sigma_meas, self.units = name, pools, void_reason, sigma_meas, units

    @property
    def live(self):
        return self.pools is not None


def declare(**kw):
    """declare(N=Budget(...), ...). Every one of the five must be present."""
    missing = [b for b in BUDGETS if b not in kw]
    if missing:
        raise ValueError("budgets %s not declared (LIVE or VOID with a reason)" % missing)
    return {b: kw[b] for b in BUDGETS}


def flux_keys(out, budgets):
    """Rates for the boundary accumulators of every LIVE budget, from one model output."""
    rates = {}
    for b in budgets.values():
        if not b.live:
            continue
        for name, src, dst, r in out.transfers:
            s_in, d_in = src in b.pools, dst in b.pools
            if d_in and not s_in:
                k = "_in|%s|%s" % (b.name, name)
            elif s_in and not d_in:
                k = "_out|%s|%s" % (b.name, name)
            else:
                continue
            rates[k] = rates.get(k, 0.0) + r
    return rates


def verdict(mis, scale, sigma_meas=None, rel_tol=REL_TOL, k_sigma=2.0):
    if abs(mis) <= rel_tol * max(scale, 1e-300):
        return "CLOSED"
    if sigma_meas is not None and abs(mis) <= k_sigma * sigma_meas:
        return "NOISE"
    return "LEAK"


def misclosure(start, end, b_in, b_out):
    return (end - start) - (b_in - b_out)


def audit(budgets, state0, state1):
    """state1 carries the accumulators. Returns one row per budget and the boundary audit lines."""
    rows, crossings = [], []
    for b in budgets.values():
        if not b.live:
            rows.append(dict(budget=b.name, verdict="VOID", reason=b.void_reason))
            continue
        start = sum(state0[p] for p in b.pools)
        end = sum(state1[p] for p in b.pools)
        ins = {k.split("|")[2]: v for k, v in state1.items() if k.startswith("_in|%s|" % b.name)}
        outs = {k.split("|")[2]: v for k, v in state1.items() if k.startswith("_out|%s|" % b.name)}
        b_in, b_out = sum(ins.values()), sum(outs.values())
        mis = misclosure(start, end, b_in, b_out)
        scale = max(abs(b_in) + abs(b_out), abs(start), abs(end))
        rows.append(dict(budget=b.name, units=b.units, pools_start=start, pools_end=end, boundary_in=b_in,
                         boundary_out=b_out, misclosure=mis, tolerance=REL_TOL * scale,
                         verdict=verdict(mis, scale, b.sigma_meas), sigma_meas=b.sigma_meas))
        crossings.append("boundary audit [%s]: in %s ; out %s" % (
            b.name, ", ".join("%s %.6g" % kv for kv in sorted(ins.items())) or "nothing",
            ", ".join("%s %.6g" % kv for kv in sorted(outs.items())) or "nothing"))
    return rows, crossings


def run_status(rows):
    """INCOMPLETE unless at least one budget is LIVE and every LIVE budget is CLOSED or NOISE."""
    live = [r for r in rows if r["verdict"] != "VOID"]
    if not live:
        return "INCOMPLETE", "NO_LIVE_BUDGET: closure was not tested"
    bad = [r["budget"] for r in live if r["verdict"] == "LEAK"]
    if bad:
        return "INCOMPLETE", "budget(s) %s did not close" % bad
    return "COMPLETE", "%d of %d budgets LIVE and closed; %d VOID" % (len(live), len(rows), len(rows) - len(live))
