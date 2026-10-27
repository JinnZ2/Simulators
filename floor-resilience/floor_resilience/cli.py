"""Command line: ``floorres assess | sim | stress``. No network calls."""
from __future__ import annotations

import argparse
import sys
from dataclasses import fields
from typing import Optional

from . import drain_sim, report
from .schema import load_site
from .stress import power, software, vendor


def _assess(args) -> int:
    site, gaps = load_site(args.site)
    a = report.analyze(site, gaps, args.config, sim_runs=args.runs, seed=args.seed)
    md, htm = report.write(a, args.out)
    asm = a.assessment
    if asm.overall is not None:
        weak = ", ".join(f"{i.id} {i.name} {i.score}/4" for i in asm.weakest)
        print(f"overall {asm.overall:.1f}/4 (weights PROPOSED, cuts ASSUMED); weakest: {weak}")
    else:
        print("no indicator could be scored; see Data gaps")
    print(f"{len(a.gaps)} data gaps")
    print(f"wrote {md}\nwrote {htm}")
    return 0


def _sim(args) -> int:
    over = {f.name: getattr(args, f.name) for f in fields(drain_sim.Params)
            if getattr(args, f.name, None) is not None}
    p = drain_sim.Params(**over)
    site = None
    if args.site:
        site, gaps = load_site(args.site)
        for g in gaps:
            print(f"data gap: {g}", file=sys.stderr)
    r = drain_sim.simulate(p, seed=args.seed, rng=args.rng, site=site)
    print(f"source: {r.source}; rng: {args.rng}; seed {args.seed}; runs {r.params.runs} "
          "(all constants ASSUMED)")
    for n in r.notes:
        print(f"note: {n}")
    print("month  scrap  veterans  inspectors  outsourced")
    for m in range(0, r.params.months, max(1, r.params.months // 10)):
        print(f"{m + 1:5d} {r.scrap[m]:6.0f} {r.vets[m]:9.2f} {r.inspectors[m]:11d} {r.outsourced[m]:11.2f}")
    s = r.summary()
    print(f"scrap change by month {r.params.months}: {s['scrap_change']:+.1%}")
    print(f"veterans down 30%: month {s['indicator_month']}; scrap up 50%: month "
          f"{s['alarm_month']}; lead time: {s['lead_time_months']} months")
    return 0


def _stress(args) -> int:
    site, gaps = load_site(args.site)
    for g in gaps:
        print(f"data gap: {g}", file=sys.stderr)
    pr = power.run(site)
    print("POWER  machine x state")
    for c in pr.cells:
        who = ", ".join(c.who_can_run) or "-"
        print(f"  {c.machine:12s} {c.state:12s} {c.status:14s} who: {who}; tested: {c.last_tested}")
    if pr.plan.budget_kw is not None:
        print(f"  minimal plan {pr.plan.budget_kw:g} kW: keep {pr.plan.keep}, shed {pr.plan.shed}, "
              f"unknown draw {pr.plan.unknown_draw}")
    layers = [args.layer] if args.layer else [l.id for l in site.software_layers]
    for lid in layers:
        k = software.knockout(site, lid)
        print(f"SOFTWARE  {lid} down (with {', '.join(x for x in k.down if x != lid) or 'nothing else'})")
        for m in k.machines:
            if m.status != "OK":
                print(f"  machine {m.machine}: {m.status}{' [hidden chain]' if m.hidden_chain else ''}")
        for f in k.functions:
            if f.status != "OK":
                print(f"  function {f.function}: {f.status}{' by ' + f.bridge if f.status == 'BRIDGED' else ''}")
    vr = vendor.run(site)
    print("VENDOR" + ("  (output shares ASSUMED equal where missing)" if vr.shares_assumed else ""))
    for r in vr.rows:
        flag = "  FLAG" if r.flagged else ""
        print(f"  {r.vendor:20s} line {r.line_share:.0%}  stops {r.stops_share:.0%}{flag}")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="floorres", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("assess", help="score a site and write report.md + report.html")
    a.add_argument("site")
    a.add_argument("--out", default="floorres-report")
    a.add_argument("--config", default=None, help="YAML overriding weights and cuts")
    a.add_argument("--runs", type=int, default=40)
    a.add_argument("--seed", type=int, default=1000)
    a.set_defaults(fn=_assess)
    s = sub.add_parser("sim", help="run the skill-drain simulation")
    s.add_argument("--site", default=None, help="start from a site file instead of the default plant")
    s.add_argument("--rng", choices=["numpy", "js"], default="numpy",
                   help="js replays the published model's generator exactly")
    s.add_argument("--seed", type=int, default=1000)
    for f in fields(drain_sim.Params):
        typ = type(f.default)
        s.add_argument(f"--{f.name.replace('_', '-')}", dest=f.name, type=typ, default=None,
                       help=f"default {f.default} (ASSUMED)")
    s.set_defaults(fn=_sim)
    t = sub.add_parser("stress", help="power, software and vendor stress tests")
    t.add_argument("site")
    t.add_argument("--layer", default=None, help="knock out only this software layer")
    t.set_defaults(fn=_stress)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
