"""Markdown and self-contained HTML report (work order section 9).

One document model, two renderings. Plain words; every number carries its
tag; an EXAMPLE site says so at the top. Charts are PNG files next to the
Markdown and base64-embedded in the HTML, so the HTML opens on its own.
"""
from __future__ import annotations

import base64
import html
import io
import math
from dataclasses import dataclass, field
from pathlib import Path
from statistics import median
from typing import Any, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from . import tags  # noqa: E402
from . import drain_sim, eld, reserve, scrap as scrap_mod  # noqa: E402
from .indicators import Assessment, assess, load_config  # noqa: E402
from .schema import Site  # noqa: E402
from .stress import power as power_mod, software, vendor as vendor_mod  # noqa: E402

S, A, P, F = tags.SITE_DATA, tags.ASSUMED, tags.PROPOSED, tags.FOUND


# --- document model ---------------------------------------------------------
@dataclass
class Doc:
    blocks: list[tuple] = field(default_factory=list)
    images: dict[str, bytes] = field(default_factory=dict)

    def h(self, level: int, text: str): self.blocks.append(("h", level, text))
    def p(self, text: str): self.blocks.append(("p", text))
    def ul(self, items: list[str]): self.blocks.append(("ul", items))
    def table(self, head: list[str], rows: list[list[Any]]):
        self.blocks.append(("table", head, [[_cell(c) for c in r] for r in rows]))
    def img(self, name: str, png: bytes, alt: str):
        self.images[name] = png
        self.blocks.append(("img", name, alt))


def _cell(c: Any) -> str:
    return "" if c is None else str(c)


def num(v: Optional[float], tag: str, fmt: str = "{:.2f}") -> str:
    if v is None:
        return "no data"
    if isinstance(v, float) and math.isinf(v):
        return f"no veterans ({tag})"
    return f"{fmt.format(v)} ({tag})"


def pct(v: Optional[float], tag: str) -> str:
    return num(v, tag, "{:.0%}")


def to_markdown(doc: Doc) -> str:
    out = []
    for b in doc.blocks:
        if b[0] == "h":
            out.append("#" * b[1] + " " + b[2])
        elif b[0] == "p":
            out.append(b[1])
        elif b[0] == "ul":
            out.append("\n".join(f"- {i}" for i in b[1]))
        elif b[0] == "table":
            head, rows = b[1], b[2]
            esc = lambda s: s.replace("|", "\\|").replace("\n", " ")
            out.append("| " + " | ".join(map(esc, head)) + " |\n|"
                       + "---|" * len(head) + "\n"
                       + "\n".join("| " + " | ".join(map(esc, r)) + " |" for r in rows))
        elif b[0] == "img":
            out.append(f"![{b[2]}]({b[1]})")
        out.append("")
    return "\n".join(out)


_CSS = """
:root{--bg:#fbfaf7;--ink:#1d2329;--muted:#55606a;--rule:#cfd5da;--flag:#a3261e}
@media (prefers-color-scheme: dark){:root{--bg:#14191d;--ink:#e3e8eb;--muted:#99a5ae;--rule:#2f3a42;--flag:#ef7a6f}}
body{margin:0;background:var(--bg);color:var(--ink);font:18px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1000px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:30px;line-height:1.15}h2{margin-top:40px;border-top:2px solid var(--ink);padding-top:12px}
table{border-collapse:collapse;width:100%;font-size:15px;margin:8px 0}
th,td{border-bottom:1px solid var(--rule);padding:7px 8px;text-align:left;vertical-align:top}
th{color:var(--muted);font-weight:600}
.wrap{overflow-x:auto}img{max-width:100%;background:#fff;border:1px solid var(--rule)}
p,li{max-width:75ch}
"""


def to_html(doc: Doc, title: str) -> str:
    parts = [f"<!doctype html><html lang=en><head><meta charset=utf-8>"
             f"<meta name=viewport content='width=device-width,initial-scale=1'>"
             f"<title>{html.escape(title)}</title><style>{_CSS}</style></head><body><main>"]
    e = html.escape
    for b in doc.blocks:
        if b[0] == "h":
            parts.append(f"<h{b[1]}>{e(b[2])}</h{b[1]}>")
        elif b[0] == "p":
            parts.append(f"<p>{e(b[1])}</p>")
        elif b[0] == "ul":
            parts.append("<ul>" + "".join(f"<li>{e(i)}</li>" for i in b[1]) + "</ul>")
        elif b[0] == "table":
            parts.append("<div class=wrap><table><tr>" + "".join(f"<th>{e(h)}</th>" for h in b[1])
                         + "</tr>" + "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r)
                                             + "</tr>" for r in b[2]) + "</table></div>")
        elif b[0] == "img":
            data = base64.b64encode(doc.images[b[1]]).decode()
            parts.append(f"<img alt='{e(b[2])}' src='data:image/png;base64,{data}'>")
    parts.append("</main></body></html>")
    return "".join(parts)


def _png(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    return buf.getvalue()


# --- analysis bundle --------------------------------------------------------
@dataclass
class Analysis:
    site: Site
    gaps: list[str]
    scrap: scrap_mod.ScrapResult
    power: power_mod.PowerResult
    knockouts: list[software.Knockout]
    php: software.PhpScenario
    vendors: vendor_mod.VendorResult
    sim: Optional[drain_sim.SimResult]
    reserve_cost: reserve.ReserveCost
    fleet: Optional[eld.EldResult]
    assessment: Assessment


def analyze(site: Site, gaps: Optional[list[str]] = None,
            config_path: Optional[str] = None, sim_runs: int = 40,
            seed: int = 1000) -> Analysis:
    gaps = list(gaps or [])
    cfg = load_config(config_path)
    sc = scrap_mod.reclassify(site)
    pw = power_mod.run(site)
    kos = software.all_knockouts(site)
    php = software.php2shell_scenario(site)
    vd = vendor_mod.run(site)
    sim = None
    try:
        sim = drain_sim.simulate(drain_sim.Params(runs=sim_runs), seed=seed, site=site)
    except ValueError as exc:
        gaps.append(f"skill-drain projection not run: {exc}")
    rc = reserve.cost(site.reserve_line)
    fleet = eld.run(site) if site.drivers else None
    asm = assess(site, cfg, sc, pw, kos)
    for ind in asm.indicators:
        if ind.score is None:
            gaps.append(f"{ind.id} {ind.name}: {ind.explanation[len('No data: '):]}")
    if sc.unmapped_codes:
        gaps.append("scrap codes not in the map (left out of the share): "
                    + ", ".join(f"{k} ({v:.0f} units)" for k, v in sc.unmapped_codes.items()))
    if site.machines and vd.shares_assumed:
        gaps.append("machine output shares missing for some machines; equal shares assumed (ASSUMED)")
    unknown_layers = sorted({l for k in kos for l in k.unknown_layers})
    if not kos:
        unknown_layers = sorted({l for m in site.machines for l in m.software_layers})
    if unknown_layers:
        gaps.append("software layers named on machines but not described: " + ", ".join(unknown_layers))
    if site.power_budget.minimal_kw is None and site.machines:
        gaps.append("minimal-power kW budget not given; no load-shed plan")
    if sim:
        gaps += [f"skill-drain projection: {n}" for n in sim.notes]
    if rc.missing:
        gaps.append("reserve-line costing inputs missing: " + ", ".join(rc.missing))
    return Analysis(site, gaps, sc, pw, kos, php, vd, sim, rc, fleet, asm)


# --- sections ---------------------------------------------------------------
def _summary(doc: Doc, a: Analysis):
    asm = a.assessment
    doc.h(2, "Summary")
    if asm.overall is None:
        doc.p("No indicator could be scored from this file. See Data gaps.")
    else:
        weak = "; ".join(f"{i.id} {i.name} = {i.score}/4" for i in asm.weakest)
        tie = (f" ({len(asm.weakest)} listed because of a tie at the third-lowest score)"
               if len(asm.weakest) > 3 else "")
        doc.p(f"Overall: {asm.overall:.1f} out of 4 (weighted mean; weights {P}, "
              f"score cuts {A}). It is an average of "
              f"{len(asm.indicators) - len(asm.unscored)} indicators, so read it "
              f"with the weakest three{tie}: {weak}.")
    if asm.unscored:
        doc.p("Not scored for lack of data: " + ", ".join(asm.unscored) + ".")
    doc.ul([f"{i.id}: {i.plain} {i.explanation}" for i in asm.weakest])


def _indicator_table(doc: Doc, a: Analysis):
    doc.h(2, "Indicators")
    doc.p("Score 0 to 4; 4 is healthiest. Confidence 0 to 1 shows how much of "
          "the needed data the site file had.")
    rows = []
    for i in a.assessment.indicators:
        v = None if i.value is None else (f"{i.value:.3g}" if math.isfinite(i.value) else "no veterans")
        rows.append([i.id, i.plain, v or "no data",
                     "-" if i.score is None else f"{i.score}/4",
                     f"{i.confidence:.2f}", i.tag, i.explanation])
    doc.table(["id", "what it checks", "value", "score", "confidence", "tag", "reading"], rows)


def _scrap(doc: Doc, a: Analysis):
    sc = a.scrap
    doc.h(2, "Scrap: what the log says vs what was missing")
    if not sc.rows:
        doc.p("No scrap rows in the site file.")
        return
    doc.p(f"The scrap log names a machine cause on every row. Read against the "
          f"code map ({tags.OBSERVED}), {pct(sc.overall.share, S)} of mapped "
          f"scrapped units came from causes a skilled operator could catch early.")
    doc.table(["missing catch", "units"],
              [[k, f"{v:.0f} ({S})"] for k, v in sorted(sc.missing_catch.items(), key=lambda kv: -kv[1])])
    doc.table(["machine", "catchable share", f"mapped units ({S})"],
              [[m, pct(s.share, S), f"{s.mapped:.0f}"] for m, s in sorted(sc.by_machine.items())])
    doc.table(["shift", "catchable share", f"mapped units ({S})"],
              [[m, pct(s.share, S), f"{s.mapped:.0f}"] for m, s in sorted(sc.by_shift.items())])
    months = [m for m, s in sc.by_month.items() if s.share is not None]
    if months:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(months, [sc.by_month[m].share for m in months], marker="o", color="#b86a00")
        ax.set_ylim(0, 1)
        ax.set_ylabel("catchable share")
        ax.set_title("Scrap an operator could have caught, by month (SITE DATA)")
        ax.tick_params(axis="x", rotation=60, labelsize=7)
        doc.img("scrap_monthly.png", _png(fig), "catchable scrap share by month")
    if sc.flags:
        doc.p(f"Machines whose catchable share rose by {scrap_mod.FLAG_RISE:.0%} or more "
              f"after a veteran left (window {scrap_mod.FLAG_WINDOW_DAYS} days each side; "
              f"thresholds {A}):")
        doc.table(["machine", "veteran who left", "left", "before", "after"],
                  [[f.machine, f.person, f.left_date, pct(f.share_before, S), pct(f.share_after, S)]
                   for f in sc.flags])
    else:
        doc.p(f"No machine flagged after a veteran left ({sc.checked_departures} "
              "machine-departures had enough scrap rows to check).")


def _drain(doc: Doc, a: Analysis):
    doc.h(2, "Skill-drain projection")
    sim = a.sim
    if sim is None:
        doc.p("Not run: the site file has no current operators.")
        return
    doc.p(f"Starting from this site's operators ({sim.params.n_operators} people, "
          f"screen: {sim.params.screen.replace('_', '-')}, reserve line: {sim.params.reserve}). "
          f"Every model constant is {A}; this is the shape of the mechanism, not a forecast. "
          f"{sim.params.runs} seeded runs averaged.")
    rows = [[m, num(sim.scrap[m - 1], A, "{:.0f}"), num(sim.vets[m - 1], A, "{:.1f}"),
             num(float(sim.inspectors[m - 1]), A, "{:.0f}")] for m in (1, 12, 24, 36, 48, 60)
            if m <= sim.params.months]
    doc.table(["month (index)", "scrapped parts", "veterans on floor", "inspectors"], rows)
    lt = sim.lead_time
    doc.p(f"Early warning: veterans fall 30% by month {sim.indicator_month or 'never'}; "
          f"scrap rises 50% by month {sim.alarm_month or 'never'}"
          + (f" — {lt} months of warning ({A})." if lt is not None else ".")
          + " The lead time is sensitive: in the default plant the expected scrap "
            "curve peaks only a few points above the 50% alarm, so the alarm month "
            "moves a lot between runs.")
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(range(1, sim.params.months + 1), sim.scrap, color="#b86a00", label="scrap")
    ax.axhline(sim.base * 1.5, color="#a3261e", ls=":", label="alarm (+50%)")
    ax2 = ax.twinx()
    ax2.plot(range(1, sim.params.months + 1), sim.vets, color="#1f6f8b", ls="--", label="veterans")
    ax.set_xlabel("month")
    ax.set_ylabel("scrapped parts")
    ax2.set_ylabel("veterans")
    ax.set_title("Projection (all constants ASSUMED)")
    ax.legend(loc="upper left", fontsize=8)
    doc.img("drain_projection.png", _png(fig), "skill-drain projection")


def _stress(doc: Doc, a: Analysis):
    doc.h(2, "Stress tests")
    doc.h(3, "Power states")
    pw = a.power
    if not pw.cells:
        doc.p("No machines in the site file.")
    else:
        by = {}
        for c in pw.cells:
            by.setdefault(c.machine, {})[c.state] = c
        rows = []
        for m, st in by.items():
            row = [m]
            for s in power_mod.STATES:
                c = st[s]
                who = ", ".join(c.who_can_run) or "no one named"
                extra = f"; who: {who}" if c.status.startswith("MANUAL") else ""
                rehome = "; re-home after dropout" if c.rehome_after_dropout else ""
                row.append(f"{c.status}{extra}{rehome}; tested: {c.last_tested}")
            rows.append(row)
        doc.table(["machine", "no power", "intermittent / surging", "minimal power"], rows)
        doc.p("RUNS = keeps running. MANUAL = a named person can run it by hand. "
              "MANUAL_NO_ONE = a manual way exists but no one on site is recorded "
              "as able to do it. STOPS = no way to run it. UNKNOWN = no record.")
        pl = pw.plan
        if pl.budget_kw is not None:
            doc.p(f"Minimal-power plan for {pl.budget_kw:g} kW ({S}): keep "
                  f"{', '.join(pl.keep) or 'nothing'} ({pl.used_kw:g} kW); shed "
                  f"{', '.join(pl.shed) or 'nothing'}"
                  + (f"; draw unknown, not planned: {', '.join(pl.unknown_draw)}" if pl.unknown_draw else "")
                  + ". Greedy by priority, 1 first.")
    doc.h(3, "Software layer knockout")
    if not a.knockouts:
        doc.p("No software layers described.")
    for k in a.knockouts:
        hit = [m for m in k.machines if m.status != "OK"]
        funcs = [f for f in k.functions if f.status != "OK"]
        doc.p(f"If {k.layer} goes down (also takes down: "
              f"{', '.join(x for x in k.down if x != k.layer) or 'nothing else'}):")
        items = [f"machine {m.machine}: {m.status}" + (" (hidden chain: it does not use "
                 f"{k.layer} directly)" if m.hidden_chain else "") for m in hit]
        items += [f"function {f.function}: {f.status}" + (f" by {f.bridge}" if f.status == "BRIDGED" else "")
                  + (f" ({'; '.join(f.because)})" if f.because else "") for f in funcs]
        doc.ul(items or ["nothing stops"])
    php = a.php
    doc.h(3, "Worked example: PHP layer down (PHP2Shell)")
    fx = php.facts
    doc.p(f"{fx['name']} ({', '.join(fx['cves'])}; CVSS v4 {fx['cvss_v4']}, no login "
          f"needed). Patches released {fx['dates']['patches_released']} for PHP "
          f"{', '.join(fx['fixed_versions'].values())}; nothing from the PHP project for "
          f"branches below {fx['no_upstream_patch_below']}. ({F} at search-result depth "
          f"only; the PHP advisory itself was not opened. Check php.net before acting.)")
    if not php.cases:
        doc.p("This site lists no PHP layer.")
    for lid, status, k in php.cases:
        stopped = [f.function for f in k.functions if f.status == "STOPS"]
        bridged = [f"{f.function} (by {f.bridge})" for f in k.functions if f.status == "BRIDGED"]
        doc.ul([f"layer {lid}: {status}",
                "functions that stop: " + (", ".join(stopped) or "none"),
                "functions a person keeps going: " + (", ".join(bridged) or "none"),
                "hidden chains: " + (", ".join(k.hidden_chains) or "none")])
    doc.h(3, "Vendor dependency")
    vd = a.vendors
    if not vd.rows:
        doc.p("No machines in the site file.")
    else:
        doc.table(["vendor", "machines", f"license checks ({S})", "repair knowledge (in-house / vendor / unknown)",
                   "share of line", "output stopped if vendor down", "flag"],
                  [[r.vendor, ", ".join(r.machines), r.license_checks,
                    f"{r.inhouse_repair} / {r.vendor_held_repair} / {r.unknown_repair}",
                    pct(r.line_share, A if r.share_assumed else S),
                    pct(r.stops_share, A if r.share_assumed else S),
                    f"over {vd.threshold:.0%} ({A})" if r.flagged else ""] for r in vd.rows])


def _reserve(doc: Doc, a: Analysis):
    doc.h(2, "Reserve line")
    doc.ul(reserve.SPEC)
    rc = a.reserve_cost
    doc.table(["item", "value"], [
        ["wage cost per year", num(rc.wage_cost, S, "{:,.0f}")],
        ["output value of the reserve line per year", num(rc.output_value, S, "{:,.0f}")],
        ["premium (net yearly cost)", num(rc.premium, S, "{:,.0f}")],
        ["expected avoided outage loss per year", num(rc.expected_avoided_loss,
                                                     A if rc.assumed else S, "{:,.0f}")],
        ["avoided loss per unit of premium", num(rc.ratio, A if rc.assumed else S, "{:.2f}")],
    ])
    if rc.premium is not None and rc.premium <= 0:
        doc.p("The line's output covers its wage cost; the insurance costs nothing net.")
    if rc.assumed:
        doc.p("Assumed: " + "; ".join(rc.assumed) + ".")
    doc.p(reserve.POLICY_NOTE)


def _fleet(doc: Doc, a: Analysis):
    if a.fleet is None:
        return
    fl = a.fleet
    doc.h(2, "Fleet: paper-log fallback")
    doc.p(f"{fl.able} of {fl.drivers} drivers can fall back to paper logs; "
          f"{fl.not_able} cannot; {fl.unknown} not recorded. Share able among known: "
          f"{pct(fl.able_share, S)}.")
    if fl.flagged:
        doc.p("Started after the ELD compliance date (2017-12-18) with no paper drill "
              "on record: " + ", ".join(fl.flagged) + ".")
    r = fl.rules
    doc.p(f"What the rule asks, as found at search-result depth on {r['checked']} "
          f"(status: {r['status']}; verify against 49 CFR 395.34 before relying on it):")
    doc.ul([f"{x['text']} [{x['cite']}]" for x in r["rules"]])


def _field_measures(doc: Doc, a: Analysis):
    recs = a.site.repair_attribution
    doc.h(2, "Field measures (research gap 5)")
    doc.p("Raw counts only, for the open question of how floor skill shows up "
          "outside reading tests. Not scored.")
    titled = {o.label: o.titled for o in a.site.operators}
    groups: dict[str, list] = {}
    for r in recs:
        t = titled.get(r.who_fixed or "")
        key = "titled fixer" if t else ("untitled fixer" if t is False else "fixer not matched")
        groups.setdefault(key, []).append(r)
    rows = []
    for key, rs in sorted(groups.items()):
        leads = [r.detection_lead_hours for r in rs if r.detection_lead_hours is not None]
        ff = [r.first_fix for r in rs if r.first_fix is not None]
        called = sum(bool(r.called_after_titled_failed) for r in rs)
        rows.append([key, len(rs),
                     f"{median(leads):.1f} h (n={len(leads)})" if leads else "not recorded",
                     f"{sum(ff)}/{len(ff)}" if ff else "not recorded", called])
    if rows:
        doc.table(["group", f"repairs ({S})", f"median fault-detection lead ({S})",
                   f"first-time fixes ({S})", f"called after a titled mechanic failed ({S})"], rows)
    memos = sum(bool(r.voice_memo) for r in recs)
    photos = sum(bool(r.photo) for r in recs)
    doc.p(f"{memos} repair records carry a voice memo and {photos} a photo (file "
          "references only).")


def build(a: Analysis) -> Doc:
    doc = Doc()
    name = a.site.name or "unnamed site"
    doc.h(1, f"Floor resilience assessment: {name}")
    if a.site.example:
        doc.p("EXAMPLE: this is an invented plant. No number here describes a real site.")
    doc.p("Tags: SITE DATA = from the site file; ASSUMED = placeholder you can change; "
          "PROPOSED = untested design choice; OBSERVED = floor observation; "
          "FOUND = checked against a published source.")
    _summary(doc, a)
    _indicator_table(doc, a)
    _scrap(doc, a)
    _drain(doc, a)
    _stress(doc, a)
    _reserve(doc, a)
    _fleet(doc, a)
    _field_measures(doc, a)
    doc.h(2, "Data gaps")
    doc.ul(a.gaps or ["none recorded"])
    return doc


def write(a: Analysis, out_dir: str | Path) -> tuple[Path, Path]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    doc = build(a)
    md, htm = out / "report.md", out / "report.html"
    md.write_text(to_markdown(doc), encoding="utf-8")
    htm.write_text(to_html(doc, f"Floor resilience: {a.site.name or 'site'}"), encoding="utf-8")
    for name, png in doc.images.items():
        (out / name).write_bytes(png)
    return md, htm
