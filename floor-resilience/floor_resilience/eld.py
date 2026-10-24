"""Fleet paper-log readiness (work order section 8).

Can each driver fall back to paper if the electronic logging device fails?
"Able" means the driver has kept paper logs in the cab or has done a
week-long paper drill. Unknown answers are counted as unknown, never as no.

Drivers who started after the ELD compliance date (2017-12-18) and have no
recorded drill are flagged: they may never have kept a paper log.

The FMCSA rule text shown in reports comes from data/fmcsa_395_34.yaml and is
marked NOT VERIFIED against the regulation itself. See that file.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from importlib import resources
from typing import Optional

import yaml

from .schema import Site


def load_rules() -> dict:
    text = resources.files("floor_resilience").joinpath(
        "data/fmcsa_395_34.yaml").read_text(encoding="utf-8")
    return yaml.safe_load(text)


@dataclass
class EldResult:
    drivers: int
    able: int
    not_able: int
    unknown: int
    flagged: list[str] = field(default_factory=list)
    no_start_year: int = 0
    rules: dict = field(default_factory=dict)

    @property
    def able_share(self) -> Optional[float]:
        known = self.able + self.not_able
        return self.able / known if known else None

    @property
    def confidence(self) -> float:
        return (self.able + self.not_able) / self.drivers if self.drivers else 0.0


def run(site: Site) -> EldResult:
    rules = load_rules()
    mandate_year = rules["mandate"]["compliance_date"].year  # 2017
    res = EldResult(len(site.drivers), 0, 0, 0, rules=rules)
    for i, d in enumerate(site.drivers):
        label = d.id or f"driver {i + 1}"
        kept, drill = d.has_kept_paper_logs_in_cab, d.completed_week_long_paper_drill
        if kept or drill:
            res.able += 1
        elif kept is False and drill is False:
            res.not_able += 1
        else:
            res.unknown += 1
        if d.start_year is None:
            res.no_start_year += 1
        elif d.start_year > mandate_year and not drill:
            res.flagged.append(label)
    return res
