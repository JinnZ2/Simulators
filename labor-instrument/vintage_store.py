#!/usr/bin/env python3
"""M1 vintage_store -- key every observation by (series_id, period,
release_date). The cell holds EVERY version ever published, not the current
one; the revision history is the signal, not noise.

    record: series_id, period, release_date, value, adjustment_status

The real fill is ALFRED observation vintages, which this environment cannot
fetch (egress allowlist: alfred.stlouisfed.org answered no on CONNECT,
probed 2026-09-05T14:02Z). So the store ships EMPTY of real data; it is
loaded from constructed vintages in the selftest, and from a real ALFRED
pull by whoever has network. Nothing is fabricated into it here. Stdlib
only, parses under 3.9.
"""

import sys
from collections import namedtuple

Obs = namedtuple("Obs", "series_id period release_date value adjustment_status")


class VintageStore:
    """(series_id, period) -> list of Obs across release_dates, kept sorted
    by release_date. Every version is retained."""

    def __init__(self):
        self._cells = {}

    def add(self, series_id, period, release_date, value, adjustment_status="SA"):
        key = (series_id, period)
        obs = Obs(series_id, period, release_date, value, adjustment_status)
        versions = self._cells.setdefault(key, [])
        # a re-published (series, period, release_date) replaces that exact
        # version; different release_dates accumulate.
        versions[:] = [o for o in versions if o.release_date != release_date]
        versions.append(obs)
        versions.sort(key=lambda o: o.release_date)
        return obs

    def versions(self, series_id, period):
        return list(self._cells.get((series_id, period), []))

    def earliest(self, series_id, period):
        v = self.versions(series_id, period)
        return v[0] if v else None

    def latest(self, series_id, period):
        v = self.versions(series_id, period)
        return v[-1] if v else None

    def as_of(self, series_id, period, release_date):
        """The version that was current AS OF a given release_date -- the
        latest release on or before it. None if the period had not yet been
        published then."""
        v = [o for o in self.versions(series_id, period) if o.release_date <= release_date]
        return v[-1] if v else None

    def revision(self, series_id, period, from_release=None, to_release=None):
        """The revision component for one period: value at to_release minus
        value at from_release. Defaults to latest minus earliest -- the total
        the period has moved across all vintages. Returns None if the period
        has fewer than two versions (no revision observable)."""
        v = self.versions(series_id, period)
        if len(v) < 2:
            return None
        lo = v[0] if from_release is None else self.as_of(series_id, period, from_release)
        hi = v[-1] if to_release is None else self.as_of(series_id, period, to_release)
        if lo is None or hi is None:
            return None
        return hi.value - lo.value

    def is_empty(self):
        return not self._cells

    def keys(self):
        return sorted(self._cells)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("vintage_store has no selftest; run selftest.py", file=sys.stderr)
        sys.exit(2)
    print("M1 vintage_store -- import and use VintageStore; it ships empty of "
          "real data (ALFRED egress-blocked). Run selftest.py for the checks.",
          file=sys.stderr)
    sys.exit(2)
