"""Vendor and license dependency map (work order section 6c).

Per vendor: machines covered, license checks, whether repair knowledge is in
house or held by the vendor, and the share of line output on that vendor.

A vendor outage is read as: machines with a license check and no full manual
mode stop; machines whose repair knowledge is vendor-held keep running but
cannot be fixed in house. Output shares default to equal (ASSUMED) when the
site does not give them.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from ..schema import Site

STOP_THRESHOLD = 0.30   # ASSUMED: flag a vendor whose outage stops > 30 % of output


@dataclass
class VendorRow:
    vendor: str
    machines: list[str] = field(default_factory=list)
    license_checks: int = 0
    vendor_held_repair: int = 0
    inhouse_repair: int = 0
    unknown_repair: int = 0
    line_share: float = 0.0
    stops_share: float = 0.0
    flagged: bool = False
    share_assumed: bool = False


@dataclass
class VendorResult:
    rows: list[VendorRow]
    shares_assumed: bool
    threshold: float = STOP_THRESHOLD

    @property
    def flagged(self) -> list[str]:
        return [r.vendor for r in self.rows if r.flagged]


def run(site: Site, threshold: float = STOP_THRESHOLD) -> VendorResult:
    ms = site.machines
    given = [m.output_share for m in ms if m.output_share is not None]
    assumed = len(given) < len(ms)
    if ms and not given:
        share = {m.id: 1 / len(ms) for m in ms}
    else:
        rest = max(0.0, 1 - sum(given))
        n_missing = sum(m.output_share is None for m in ms)
        share = {m.id: (m.output_share if m.output_share is not None
                        else (rest / n_missing if n_missing else 0.0)) for m in ms}
    rows: dict[str, VendorRow] = defaultdict(lambda: VendorRow(""))
    for m in ms:
        v = m.vendor or "(vendor not recorded)"
        r = rows[v]
        r.vendor = v
        r.machines.append(m.id)
        r.line_share += share[m.id]
        r.share_assumed |= m.output_share is None
        if m.license_check:
            r.license_checks += 1
            if m.manual_mode != "full":
                r.stops_share += share[m.id]
        k = m.repair_knowledge or "unknown"
        if k == "vendor":
            r.vendor_held_repair += 1
        elif k == "inhouse":
            r.inhouse_repair += 1
        else:
            r.unknown_repair += 1
    for r in rows.values():
        r.flagged = r.stops_share > threshold
    return VendorResult(sorted(rows.values(), key=lambda r: -r.line_share),
                        assumed, threshold)
