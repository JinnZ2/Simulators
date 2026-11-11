"""Toolkit: assumption_nudge. Anchor test 3: does the anchor hold when each
assumption is nudged?

For every assumption of every component in scope the caller supplies either
nudges (parameter overrides) or the literal reason it cannot be nudged here.
An assumption with neither is refused: unfilled stays void, never dropped.

Per nudge:
  RUN      the nudged model over `seeds`
  RETURN   re-run the un-nudged anchor and require its end state bit-identical
           to the reference, and the default tables unchanged
  BUDGETS  re-close every budget on the nudged runs; report the worst misclosure
  DIFF     each output's mean against the anchor's mean over the same seeds
  READ     inside noise when |diff| <= K_NOISE * sd of that output over the
           anchor's own `noise_seeds`                       [CHOICE: K_NOISE = 2]

Flags:
  EXACT_ZERO   end state bit-identical to the anchor in every seed: the nudge
               reached nothing. Too-smooth trigger.
  ALL_INSIDE   every output inside noise: moved nothing this tool can detect.
               Also a trigger; something may be absorbing the change.
  LEAK / FAIL  a budget did not close under the nudge.

Entry: ledger/toolkit/assumption_nudge.yaml
"""
import glob, hashlib, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE)
import numpy as np
from tools import miniyaml

K_NOISE = 2.0
NOT_NUDGEABLE = "NOT_NUDGEABLE"


class NudgeError(ValueError):
    pass


def scope_assumptions(component_ids, root=HERE):
    out = []
    for cid in component_ids:
        c = miniyaml.load(os.path.join(root, "ledger", "components", cid + ".yaml"))
        for a in c["assumes"]:
            out.append((cid, a["id"], a["text"], a["block"]))
    return out


def check_coverage(scope, nudge_map):
    """Every assumption in scope has nudges or a stated reason. Nothing extra."""
    keys = {(c, a) for c, a, _, _ in scope}
    missing = sorted(keys - set(nudge_map))
    extra = sorted(k for k in nudge_map if k not in keys and k[0] != "UNOWNED")
    if missing:
        raise NudgeError(f"assumptions with neither a nudge nor a reason: {missing}")
    if extra:
        raise NudgeError(f"nudge map names assumptions not in scope: {extra}")
    for k, v in nudge_map.items():
        if isinstance(v, tuple):
            if v[0] != NOT_NUDGEABLE or not str(v[1]).strip():
                raise NudgeError(f"{k}: not-nudgeable entry needs a reason")
        elif not v:
            raise NudgeError(f"{k}: empty nudge list (write the reason instead)")


def fingerprint(*tables):
    return hashlib.sha256(repr([sorted(t.items()) for t in tables]).encode()).hexdigest()


def run(nudge_map, simulate, outputs_fn, audit_fn, default_tables, seeds=(0, 1, 2), noise_seeds=tuple(range(10)), log=None):
    say = log or (lambda s: None)
    fp0 = fingerprint(*default_tables)
    noise_runs = {s: simulate(seed=s) for s in noise_seeds}
    noise_out = {s: outputs_fn(r) for s, r in noise_runs.items()}
    names = list(next(iter(noise_out.values())))
    sd = {n: float(np.std([noise_out[s][n] for s in noise_seeds], ddof=1)) for n in names}
    ref = {s: noise_runs[s] if s in noise_runs else simulate(seed=s) for s in seeds}
    ref_mean = {n: float(np.mean([outputs_fn(ref[s])[n] for s in seeds])) for n in names}
    ref_state0 = ref[seeds[0]]["y"].copy()
    rows = []
    for key in sorted(nudge_map):
        entry = nudge_map[key]
        if isinstance(entry, tuple):
            rows.append(dict(key=key, label="void", not_nudgeable=entry[1]))
            continue
        for nudge in entry:
            runs = {s: simulate(seed=s, params=dict(nudge["params"])) for s in seeds}
            audits = {s: audit_fn(r) for s, r in runs.items()}
            back = simulate(seed=seeds[0])
            returned = bool(np.array_equal(back["y"], ref_state0)) and fingerprint(*default_tables) == fp0
            outs = {s: outputs_fn(r) for s, r in runs.items()}
            mean = {n: float(np.mean([outs[s][n] for s in seeds])) for n in names}
            diff = {n: mean[n] - ref_mean[n] for n in names}
            outside = [n for n in names if abs(diff[n]) > K_NOISE * sd[n]]
            exact = all(np.array_equal(runs[s]["y"], ref[s]["y"]) for s in seeds)
            live = [b for b in audits[seeds[0]] if not b.startswith("_") and audits[seeds[0]][b]["verdict"] != "VOID"]
            worst = {b: max((audits[s][b]["misclosure"] for s in seeds), key=abs) for b in live}
            verdicts = {b: sorted({audits[s][b]["verdict"] for s in seeds}) for b in live}
            closed = all(v == ["CLOSED"] for v in verdicts.values())
            flags = []
            if exact:
                flags.append("EXACT_ZERO")
            elif not outside:
                flags.append("ALL_INSIDE")
            if not closed:
                flags.append("BUDGET_" + "/".join(sorted({x for v in verdicts.values() for x in v if x != "CLOSED"})))
            if not returned:
                flags.append("RETURN_FAILED")
            row = dict(key=key, label=nudge["label"], params=nudge["params"], expect=nudge.get("expect", "void"),
                       returned=returned, closed=closed, worst=worst, verdicts=verdicts,
                       mean=mean, diff=diff, outside=outside, flags=flags)
            rows.append(row)
            say(f"{key[0]} {key[1]} {nudge['label']}: outside {outside} flags {flags}")
    return dict(rows=rows, sd=sd, ref_mean=ref_mean, names=names, seeds=list(seeds), noise_seeds=list(noise_seeds), k=K_NOISE)


def render(res):
    names = res["names"]
    L = [f"seeds {res['seeds']}   noise band: {res['k']} x sd over anchor seeds {res['noise_seeds']}   [CHOICE]",
         "anchor mean (same seeds) and noise sd per output:"]
    L += [f"  {n:14s} mean {res['ref_mean'][n]:12.4f}   sd {res['sd'][n]:10.4f}   smallest detectable change {100 * res['k'] * res['sd'][n] / abs(res['ref_mean'][n]) if res['ref_mean'][n] else float('nan'):6.1f} %"
          for n in names]
    L.append("")
    L.append(f"{'component':24s} {'A':3s} {'nudge':26s} {'ret':3s} {'N mis':>10s} {'W mis':>10s}  largest move, then outputs outside noise (diff), then flags")
    for r in res["rows"]:
        if "not_nudgeable" in r:
            L.append(f"{r['key'][0]:24s} {r['key'][1]:3s} {'void':26s}  --  not nudgeable here: {r['not_nudgeable']}")
            continue
        out = ", ".join(f"{n} {r['diff'][n]:+.3g}" for n in r["outside"]) or "none"
        top = max(names, key=lambda n: abs(r["diff"][n]) / res["sd"][n] if res["sd"][n] else 0.0)
        ratio = abs(r["diff"][top]) / res["sd"][top] if res["sd"][top] else float("nan")
        L.append(f"{r['key'][0]:24s} {r['key'][1]:3s} {r['label']:26s} {'ok' if r['returned'] else 'NO':3s} "
                 f"{r['worst'].get('N', float('nan')):+10.2e} {r['worst'].get('water', float('nan')):+10.2e}  "
                 f"largest {ratio:5.1f} sd ({top})  outside: {out}   {' '.join(r['flags']) or '-'}")
    run_rows = [r for r in res["rows"] if "not_nudgeable" not in r]
    void = [r for r in res["rows"] if "not_nudgeable" in r]
    L.append("")
    L.append(f"nudges run {len(run_rows)}   assumptions not nudgeable here {len(void)}")
    L.append(f"returned to anchor bit-identical: {sum(r['returned'] for r in run_rows)} of {len(run_rows)}")
    L.append(f"budgets closed under the nudge:   {sum(r['closed'] for r in run_rows)} of {len(run_rows)}")
    for flag in ("EXACT_ZERO", "ALL_INSIDE"):
        hit = [f"{r['key'][0]}.{r['key'][1]} {r['label']}" for r in run_rows if flag in r["flags"]]
        L.append(f"{flag}: {len(hit)}" + ("".join("\n    " + h for h in hit)))
    return "\n".join(L)


if __name__ == "__main__":
    print("refused: this is a library. Run runs/run_11.py; the checks live in forest-model-ledger/tests/test_l0.py")
    sys.exit(2)
