"""Indicators I1-I12 (work order section 3).

Each indicator returns value, score (0-4, 4 = healthiest), confidence (0-1),
tag and a plain explanation. With no data the score is None and the
confidence 0: a missing measurement is never scored as good or bad.

The overall score is a weighted mean of the indicators that could be scored,
always reported with the three weakest beside it.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from typing import Callable, Optional

import numpy as np
import yaml

from . import tags
from .schema import Operator, Site
from .scrap import ScrapResult
from .stress.power import PowerResult
from .stress.software import Knockout, bridge_share

VETERAN_MONTHS = 60     # ASSUMED (> 5 years, per the work order)
NEW_HIRE_MONTHS = 12    # ASSUMED
RETIRE_HORIZON = 36     # months, per the work order

PLAIN = {
    "I1": "How much scrap a skilled operator could have caught before it happened.",
    "I2": "Whether safety rules come from workers speaking up or from people getting hurt.",
    "I3": "Whether more repairs are being sent outside each year.",
    "I4": "Whether machines and parts are being replaced faster than they should wear out.",
    "I5": "How many long-time operators you have, and how many stay past the next three years.",
    "I6": "How many machines or jobs only one person knows how to run or fix.",
    "I7": "How many new hires each veteran has to teach.",
    "I8": "Whether the hiring test checks the same skill the job uses.",
    "I9": "How often the person who fixed it is not the person whose name is on the write-up.",
    "I10": "Whether more inspectors and supervisors are being added per operator.",
    "I11": "Whether experienced operators are part of automation projects.",
    "I12": "What keeps running, or can be run by hand, when power or software goes down.",
}
NAMES = {
    "I1": "operator-catchable scrap share", "I2": "safety direction",
    "I3": "outsourcing trend", "I4": "machine/part turnover",
    "I5": "veteran depth", "I6": "sole-knower count", "I7": "mentoring load",
    "I8": "hiring channel match", "I9": "attribution gap",
    "I10": "oversight ratio", "I11": "automation ordering",
    "I12": "fallback readiness",
}


@dataclass
class Indicator:
    id: str
    name: str
    value: Optional[float]
    score: Optional[int]
    confidence: float
    tag: str
    explanation: str
    plain: str = ""

    def __post_init__(self):
        self.plain = PLAIN.get(self.id, "")
        self.confidence = round(max(0.0, min(1.0, self.confidence)), 3)
        if self.score is not None and not self.tag:
            raise ValueError(f"{self.id}: a score needs a tag")


@dataclass
class Assessment:
    indicators: list[Indicator]
    overall: Optional[float]
    weakest: list[Indicator]
    unscored: list[str]
    weights: dict[str, float] = field(default_factory=dict)


def load_config(path: Optional[str | Path] = None) -> dict:
    base = yaml.safe_load(resources.files("floor_resilience").joinpath(
        "data/config.yaml").read_text(encoding="utf-8"))
    if path:
        user = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        for k in ("weights", "cuts"):
            base[k].update(user.get(k) or {})
    return base


def band(value: float, rule: dict) -> int:
    if "higher_better" in rule:
        return sum(value >= c for c in rule["higher_better"])
    return sum(value <= c for c in rule["lower_better"])


def _tag(site: Site, extra: str = "cuts ASSUMED") -> str:
    head = f"{tags.EXAMPLE} " if site.example else ""
    return f"{head}{tags.SITE_DATA}; {extra}"


def _none(iid: str, site: Site, why: str) -> Indicator:
    return Indicator(iid, NAMES[iid], None, None, 0.0, _tag(site), f"No data: {why}")


def _scored(iid, site, value, cfg, conf, expl, tag_extra="cuts ASSUMED"):
    return Indicator(iid, NAMES[iid], value, band(value, cfg["cuts"][iid]),
                     conf, _tag(site, tag_extra), expl)


def _slope(xs: list[float], ys: list[float]) -> float:
    return float(np.polyfit(xs, ys, 1)[0])


def _current(site: Site) -> list[Operator]:
    return [o for o in site.operators if o.left_date is None]


# --- the twelve -------------------------------------------------------------
def i1(site, cfg, scrap: Optional[ScrapResult]):
    if scrap is None or scrap.overall.share is None:
        return _none("I1", site, "no scrap rows with a mapped cause code")
    s = scrap.overall
    return _scored("I1", site, s.share, cfg, scrap.confidence,
                   f"{s.catchable:.0f} of {s.mapped:.0f} mapped scrap units had a "
                   f"cause an operator could catch; {s.unmapped:.0f} units unmapped.")


def i2(site, cfg):
    w = sum(r.origin == "worker_reported" for r in site.safety)
    inc = sum(r.origin == "incident_driven" for r in site.safety)
    if w + inc == 0:
        return _none("I2", site, "no safety rules with a worker or incident origin")
    reg = sum(r.origin == "regulation" for r in site.safety)
    return _scored("I2", site, w / (w + inc), cfg, min(1, (w + inc) / 10),
                   f"{w} rules from worker reports, {inc} written after incidents "
                   f"({reg} from regulation, not counted).")


def i3(site, cfg):
    pts = [(m.year, m.repairs_inhouse / (m.repairs_inhouse + m.repairs_outsourced))
           for m in site.maintenance
           if m.repairs_inhouse is not None and m.repairs_outsourced is not None
           and (m.repairs_inhouse + m.repairs_outsourced) > 0]
    if len(pts) < 2:
        return _none("I3", site, "needs in-house and outsourced repair counts for 2+ years")
    pts.sort()
    sl = _slope([p[0] for p in pts], [p[1] for p in pts])
    return _scored("I3", site, sl, cfg, min(1, (len(pts) - 1) / 4),
                   f"In-house repair share went from {pts[0][1]:.0%} ({pts[0][0]}) to "
                   f"{pts[-1][1]:.0%} ({pts[-1][0]}): {sl:+.1%} per year.")


def i4(site, cfg):
    ratios = [m.replacements_per_year * m.expected_service_life_years
              for m in site.machines
              if m.replacements_per_year is not None and m.expected_service_life_years]
    if not ratios:
        return _none("I4", site, "no machine with both replacement rate and service life")
    v = float(np.mean(ratios))
    return _scored("I4", site, v, cfg, len(ratios) / len(site.machines),
                   f"Replacing at {v:.2f}x the rate expected from service life "
                   f"({len(ratios)} of {len(site.machines)} machines recorded).")


def i5(site, cfg):
    ops = _current(site)
    known = [o for o in ops if o.tenure_months is not None]
    if not known:
        return _none("I5", site, "no operator tenure recorded")
    vets = [o for o in known if o.tenure_months > VETERAN_MONTHS]
    leaving = [o for o in vets if o.retiring_within_months is not None
               and o.retiring_within_months <= RETIRE_HORIZON]
    v = (len(vets) - len(leaving)) / len(known)
    return _scored("I5", site, v, cfg, len(known) / len(ops),
                   f"{len(vets)} of {len(known)} operators have more than 5 years; "
                   f"{len(leaving)} of them retire within 36 months.")


def i6(site, cfg):
    ops = _current(site)
    reported = [o for o in ops if "sole_knower_of" in o.model_fields_set]
    if not reported:
        return _none("I6", site, "no operator has sole_knower_of filled in")
    holders: dict[str, list[Operator]] = {}
    for o in reported:
        for item in o.sole_knower_of:
            holders.setdefault(item, []).append(o)
    sole = {k: v[0] for k, v in holders.items() if len(v) == 1}
    at_risk = [k for k, o in sole.items() if o.retiring_within_months is not None
               and o.retiring_within_months <= RETIRE_HORIZON]
    expl = f"{len(sole)} known by one person only"
    if at_risk:
        expl += f"; {len(at_risk)} of those holders retire within 36 months ({', '.join(sorted(at_risk))})"
    return _scored("I6", site, float(len(sole)), cfg, len(reported) / len(ops), expl + ".")


def i7(site, cfg):
    known = [o for o in _current(site) if o.tenure_months is not None]
    if not known:
        return _none("I7", site, "no operator tenure recorded")
    new = sum(o.tenure_months < NEW_HIRE_MONTHS for o in known)
    vets = sum(o.tenure_months > VETERAN_MONTHS for o in known)
    v = new / vets if vets else (math.inf if new else 0.0)
    ind = _scored("I7", site, v if math.isfinite(v) else 1e9, cfg,
                  len(known) / len(_current(site)),
                  f"{new} new hires (under 1 year) and {vets} veterans.")
    ind.value = v
    return ind


_I8 = {  # (job channel, screen) -> score. PROPOSED.
    ("hands_on", "written"): 0, ("hands_on", "interview"): 2,
    ("hands_on", "hands_on_trial"): 4, ("hands_on", "working_shift"): 4,
    ("mixed", "written"): 2, ("mixed", "interview"): 2,
    ("mixed", "hands_on_trial"): 3, ("mixed", "working_shift"): 4,
    ("written", "written"): 4, ("written", "interview"): 3,
    ("written", "hands_on_trial"): 3, ("written", "working_shift"): 3,
}


def i8(site, cfg):
    h = site.hiring
    if h.screen_type is None:
        return _none("I8", site, "hiring screen type not recorded")
    job, conf = h.job_channel, 1.0
    if job is None:
        job, conf = "hands_on", 0.5   # ASSUMED: a floor role is hands-on
    score = _I8[(job, h.screen_type)]
    expl = f"Job is {job.replace('_', '-')}; screen is {h.screen_type.replace('_', ' ')}."
    if h.job_channel is None:
        expl += " Job channel not recorded; assumed hands-on (ASSUMED)."
    if h.first_year_quit_rate is not None:
        expl += f" First-year quit rate {h.first_year_quit_rate:.0%}."
    return Indicator("I8", NAMES["I8"], float(score), score, conf,
                     _tag(site, "score table PROPOSED"), expl)


def i9(site, cfg):
    recs = [r for r in site.repair_attribution if r.who_fixed and r.who_wrote_up]
    if not recs:
        return _none("I9", site, "no repair records with both who_fixed and who_wrote_up")
    gap = sum(r.who_fixed != r.who_wrote_up for r in recs)
    return _scored("I9", site, gap / len(recs), cfg, min(1, len(recs) / 20),
                   f"In {gap} of {len(recs)} repairs, the name on the write-up is "
                   "not the person who fixed it. The records place the skill wrongly there.")


def i10(site, cfg):
    pts = sorted((o.year, (o.inspectors + o.supervisors) / o.direct_operators)
                 for o in site.oversight
                 if None not in (o.inspectors, o.supervisors, o.direct_operators)
                 and o.direct_operators)
    if len(pts) < 2:
        return _none("I10", site, "needs inspectors, supervisors and operators for 2+ years")
    sl = _slope([p[0] for p in pts], [p[1] for p in pts])
    ind = _scored("I10", site, sl, cfg, min(1, (len(pts) - 1) / 4),
                  f"Oversight per operator went from {pts[0][1]:.2f} ({pts[0][0]}) to "
                  f"{pts[-1][1]:.2f} ({pts[-1][0]}): {sl:+.3f} per year.")
    return ind


def i11(site, cfg):
    known = [p for p in site.automation if p.experienced_operators_involved is not None]
    if not known:
        return _none("I11", site, "no automation projects recorded")
    yes = sum(p.experienced_operators_involved for p in known)
    return _scored("I11", site, yes / len(known), cfg, len(known) / len(site.automation),
                   f"{yes} of {len(known)} automation projects involved experienced operators.")


def i12(site, cfg, power: Optional[PowerResult], kos: Optional[list[Knockout]]):
    parts, confs, expl = [], [], []
    if power is not None and power.ready_share is not None:
        parts.append(power.ready_share)
        confs.append(power.confidence)
        expl.append(f"{power.ready_share:.0%} of known machine x power-state cells run "
                    f"or can be run by a named person; {power.never_tested} cells never tested")
    bs = bridge_share(kos) if kos else None
    if bs is not None:
        parts.append(bs)
        confs.append(1.0)
        expl.append(f"{bs:.0%} of functions hit by a software layer going down can be "
                    "bridged by a person")
    if not parts:
        return _none("I12", site, "no power-state or software-layer data")
    v = float(np.mean(parts))
    return _scored("I12", site, v, cfg, float(np.mean(confs)) * len(parts) / 2,
                   "; ".join(expl) + ".", "partly derived; cuts ASSUMED")


def assess(site: Site, cfg: Optional[dict] = None,
           scrap: Optional[ScrapResult] = None,
           power: Optional[PowerResult] = None,
           kos: Optional[list[Knockout]] = None) -> Assessment:
    cfg = cfg or load_config()
    inds = [i1(site, cfg, scrap), i2(site, cfg), i3(site, cfg), i4(site, cfg),
            i5(site, cfg), i6(site, cfg), i7(site, cfg), i8(site, cfg),
            i9(site, cfg), i10(site, cfg), i11(site, cfg),
            i12(site, cfg, power, kos)]
    w = {k: float(v) for k, v in cfg["weights"].items()}
    scored = [i for i in inds if i.score is not None and w.get(i.id, 0) > 0]
    total = sum(w[i.id] for i in scored)
    overall = sum(w[i.id] * i.score for i in scored) / total if total else None
    # Lowest three scores; an indicator tied with the third is listed too,
    # so a tie never hides a weak component.
    ranked = sorted(scored, key=lambda i: (i.score, int(i.id[1:])))
    cut = ranked[2].score if len(ranked) >= 3 else None
    weakest = ranked[:3] + [i for i in ranked[3:] if i.score == cut]
    unscored = [i.id for i in inds if i.score is None]
    return Assessment(inds, overall, weakest, unscored, w)
