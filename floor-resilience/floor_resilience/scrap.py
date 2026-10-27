"""Scrap reclassification (work order section 4).

The scrap log records a cause code that names the machine. This module maps
each code to the human catch that was missing (an editable YAML, OBSERVED)
and reports the share of scrapped units an operator could have caught.

Shares are weighted by units. Unmapped codes are counted and left out of the
share, never guessed.
"""
from __future__ import annotations

import datetime as dt
from collections import defaultdict
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from typing import Optional

import yaml

from .schema import Operator, ScrapRow, Site

FLAG_RISE = 0.10          # ASSUMED share rise that counts as a flag
FLAG_WINDOW_DAYS = 180    # ASSUMED window before/after a departure
FLAG_MIN_UNITS = 50.0     # ASSUMED units needed in each window
VETERAN_TENURE_MONTHS = 60  # ASSUMED (> 5 years, as in indicator I5)


def load_map(path: Optional[str | Path] = None) -> dict:
    if path is None:
        text = resources.files("floor_resilience").joinpath(
            "data/scrap_map.yaml").read_text(encoding="utf-8")
    else:
        text = Path(path).read_text(encoding="utf-8")
    return (yaml.safe_load(text) or {}).get("codes", {})


@dataclass
class Share:
    catchable: float = 0.0
    uncatchable: float = 0.0
    unmapped: float = 0.0

    @property
    def mapped(self) -> float:
        return self.catchable + self.uncatchable

    @property
    def share(self) -> Optional[float]:
        return self.catchable / self.mapped if self.mapped else None


@dataclass
class DepartureFlag:
    person: str
    machine: str
    left_date: dt.date
    share_before: float
    share_after: float

    @property
    def rise(self) -> float:
        return self.share_after - self.share_before


@dataclass
class ScrapResult:
    overall: Share
    by_machine: dict[str, Share]
    by_shift: dict[str, Share]
    by_month: dict[str, Share]
    rows: int
    unmapped_codes: dict[str, float]
    missing_catch: dict[str, float]          # what was missing -> units
    flags: list[DepartureFlag] = field(default_factory=list)
    checked_departures: int = 0

    @property
    def confidence(self) -> float:
        if not self.rows:
            return 0.0
        total = self.overall.mapped + self.overall.unmapped
        mapped_frac = self.overall.mapped / total if total else 0.0
        return round(min(1.0, self.rows / 50) * mapped_frac, 3)  # 50 rows ASSUMED


def _add(share: Share, row: ScrapRow, codes: dict) -> None:
    entry = codes.get(row.logged_cause_code or "")
    if entry is None:
        share.unmapped += row.units
    elif entry.get("catchable"):
        share.catchable += row.units
    else:
        share.uncatchable += row.units


def _window_share(rows: list[ScrapRow], codes: dict, machine: str,
                  start: dt.date, end: dt.date) -> Share:
    s = Share()
    for r in rows:
        if r.machine == machine and start <= r.date < end:
            _add(s, r, codes)
    return s


def _is_veteran(o: Operator) -> bool:
    return (o.tenure_months or 0) > VETERAN_TENURE_MONTHS


def departure_flags(site: Site, codes: dict) -> tuple[list[DepartureFlag], int]:
    """Machines whose catchable share rose after a named veteran left."""
    flags, checked = [], 0
    win = dt.timedelta(days=FLAG_WINDOW_DAYS)
    for o in site.operators:
        if o.left_date is None or not _is_veteran(o):
            continue
        for m in o.machines:
            before = _window_share(site.scrap, codes, m, o.left_date - win, o.left_date)
            after = _window_share(site.scrap, codes, m, o.left_date, o.left_date + win)
            if before.mapped < FLAG_MIN_UNITS or after.mapped < FLAG_MIN_UNITS:
                continue
            checked += 1
            if after.share - before.share >= FLAG_RISE:
                flags.append(DepartureFlag(o.label, m, o.left_date,
                                           before.share, after.share))
    return flags, checked


def reclassify(site: Site, codes: Optional[dict] = None) -> ScrapResult:
    codes = load_map() if codes is None else codes
    overall = Share()
    by_machine: dict[str, Share] = defaultdict(Share)
    by_shift: dict[str, Share] = defaultdict(Share)
    by_month: dict[str, Share] = defaultdict(Share)
    unmapped: dict[str, float] = defaultdict(float)
    missing: dict[str, float] = defaultdict(float)
    for r in site.scrap:
        _add(overall, r, codes)
        _add(by_machine[r.machine or "unknown"], r, codes)
        _add(by_shift[r.shift or "unknown"], r, codes)
        _add(by_month[r.date.strftime("%Y-%m")], r, codes)
        entry = codes.get(r.logged_cause_code or "")
        if entry is None:
            unmapped[r.logged_cause_code or "(blank)"] += r.units
        elif entry.get("catchable"):
            missing[entry.get("missing_catch", "unnamed catch")] += r.units
    flags, checked = departure_flags(site, codes)
    return ScrapResult(overall, dict(by_machine), dict(by_shift),
                       dict(sorted(by_month.items())), len(site.scrap),
                       dict(unmapped), dict(missing), flags, checked)
