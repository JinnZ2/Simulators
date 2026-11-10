"""L0 audit for the meander toy: misclosure per budget plus the boundary audit line.

misclosure = (store_end - store_start) - (sum in - sum out)

Verdicts are the forest ledger's closed set (forest-model-ledger/model/l0_audit.py),
restated here because that module imports numpy through its base model; tests/
test_meander.py checks the two agree on fixed cases whenever the forest module loads.
  CLOSED  |misclosure| <= rel_tol * max(gross throughput, 1)
  NOISE   above that but <= k_sigma * sigma_meas (unreachable here: no measurement)
  LEAK    above both
  VOID    budget not represented; never CLOSED, never 0
An IDENTITY flag marks a budget that closes because its two sides are the same
expression in this model. Such a closure is not evidence of anything.
"""

def verdict(mis, throughput, rel_tol=1e-9, sigma_meas=None, k_sigma=2.0):
    if abs(mis) <= rel_tol * max(throughput, 1.0):
        return "CLOSED"
    if sigma_meas is not None and abs(mis) <= k_sigma * sigma_meas:
        return "NOISE"
    return "LEAK"


def audit(res, rel_tol=1e-9):
    L = res["ledger"]
    d_store = L["store"] - res["store0"]
    fin = L["inflow"] + L["bank_input"]
    fout = L["point_bar"] + L["oxbow_fill"] + L["outflow"]
    mis = d_store - (fin - fout)
    sed = dict(verdict=verdict(mis, fin + fout, rel_tol), misclosure=mis, d_store=d_store,
               boundary=dict(inflow=L["inflow"], bank_input=L["bank_input"],
                             floodplain_loss=L["point_bar"] + L["oxbow_fill"], outflow=L["outflow"],
                             groundwater=None, overbank_fines=None),
               identity=False)
    w = res["water"]
    wmis = w["Q_in"] - w["Q_out"]
    water = dict(verdict=verdict(wmis, w["Q_in"] + w["Q_out"], rel_tol), misclosure=wmis,
                 boundary=dict(Q_in=w["Q_in"], Q_out=w["Q_out"], evaporation=None, seepage=None,
                               tributaries=None),
                 identity=True)
    e = res["energy"]
    emis = e["source"] - e["dissipation"]
    energy = dict(verdict=verdict(emis, e["source"] + e["dissipation"], rel_tol), misclosure=emis,
                  boundary=dict(potential_drop=e["source"], friction=e["dissipation"], bank_work=None,
                                transport_work=None),
                  identity=True)
    out = dict(sediment=sed, water=water, energy=energy, momentum=dict(verdict="VOID", misclosure=None))
    live = [v["verdict"] for v in out.values() if v["verdict"] != "VOID"]
    out["_overall"] = "PASS" if all(v == "CLOSED" for v in live) else "FAIL"
    out["_void"] = [k for k, v in out.items() if isinstance(v, dict) and v.get("verdict") == "VOID"]
    out["_identity"] = [k for k, v in out.items() if isinstance(v, dict) and v.get("identity")]
    return out


def report(a):
    L = []
    for k in ("sediment", "water", "energy", "momentum"):
        v = a[k]
        if v["verdict"] == "VOID":
            L.append(f"{k:9s} VOID    not represented; no closure claimed")
            continue
        tag = "  [IDENTITY: both sides are one expression here; carries no information]" if v["identity"] else ""
        L.append(f"{k:9s} {v['verdict']:7s} misclosure {v['misclosure']:+.3e}{tag}")
        L.append("          boundary: " + "  ".join(
            f"{t}={'void' if x is None else format(x, '.4f')}" for t, x in v["boundary"].items()))
    L.append(f"overall   {a['_overall']}  (void: {', '.join(a['_void']) or 'none'}; identity: {', '.join(a['_identity']) or 'none'})")
    return "\n".join(L)
