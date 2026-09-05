# SPDX-License-Identifier: CC0-1.0
"""
Rule 4 -- vintages are retained, nothing is overwritten.

Every revision to a base entry is a new versioned observation keyed by its
release_date, not a replacement; the prior value stays readable with its own
release date. This is what makes late correction visible: a series
re-benchmarked and overwritten annually cannot audit a slow error, because
the vintage in which the error was live has been destroyed.

The work order says: "Same store as the labor instrument's vintage_store.
Use it here." So this IMPORTS `labor-instrument/vintage_store.py::VintageStore`
rather than copying it -- the two cannot drift. The store's `value` slot holds
the whole `BaseEntry` snapshot; its `versions`/`as_of`/`earliest`/`latest`
give the vintage retrieval Rule 4 and acceptance #4 need. (Its numeric
`revision()` is not used here -- a BaseEntry is not a scalar difference.)

The store also carries a monotonically increasing `base_version` so a derived
aggregate cache can be keyed to the base-entry version (Rule 3).

Stdlib only. Parses under Python 3.9. CC0.
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List, Optional

_LABOR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "labor-instrument")
if _LABOR not in sys.path:
    sys.path.insert(0, _LABOR)

import vintage_store as vs        # noqa: E402  (imported, never copied)

from base_entry import BaseEntry  # noqa: E402


class MissingReleaseDate(Exception):
    pass


class EntryStore:
    """A vintage-retaining store of BaseEntry snapshots, on top of the labor
    instrument's VintageStore. Keyed by (entry_id, period, release_date);
    every version is retained."""

    def __init__(self):
        self._store = vs.VintageStore()
        self._version = 0

    def write(self, entry: BaseEntry) -> None:
        """Write a versioned observation. A revision is a new release_date on
        the same (entry_id, period); the prior vintage is untouched. Requires
        a release_date -- a vintage with no release date cannot be ordered
        against its revisions."""
        if not entry.release_date:
            raise MissingReleaseDate(
                "entry %r has no release_date; a retained vintage must be "
                "orderable by release" % entry.entry_id)
        self._store.add(entry.entry_id, entry.period, entry.release_date,
                        entry, adjustment_status=entry.status)
        self._version += 1

    def versions(self, entry_id: str, period: str) -> List[BaseEntry]:
        return [o.value for o in self._store.versions(entry_id, period)]

    def as_of(self, entry_id: str, period: str,
              release_date: str) -> Optional[BaseEntry]:
        """The vintage current AS OF a release_date -- the latest release on
        or before it (acceptance #4). None if the period had not been
        published then."""
        o = self._store.as_of(entry_id, period, release_date)
        return o.value if o else None

    def latest(self, entry_id: str, period: str) -> Optional[BaseEntry]:
        o = self._store.latest(entry_id, period)
        return o.value if o else None

    def earliest(self, entry_id: str, period: str) -> Optional[BaseEntry]:
        o = self._store.earliest(entry_id, period)
        return o.value if o else None

    def keys(self):
        return self._store.keys()

    def base_version(self) -> int:
        """Monotonic; bumps on every write. A derived aggregate cache keys to
        this so a stale cache is detectable (Rule 3)."""
        return self._version

    def is_empty(self) -> bool:
        return self._store.is_empty()

    def current_entries(self, release_date: Optional[str] = None
                        ) -> List[BaseEntry]:
        """The set an aggregate reads: one entry per (entry_id, period),
        either the latest vintage or the vintage current as of a release_date
        (vintage-aware reads). Absent-status vintages are included -- Rule 7
        keeps them, the aggregate counts them apart."""
        out = []
        for (eid, period) in self._store.keys():
            e = (self.as_of(eid, period, release_date) if release_date
                 else self.latest(eid, period))
            if e is not None:
                out.append(e)
        return out


if __name__ == "__main__":
    import sys as _s
    _s.stderr.write("entry_store.py is a library; its checks live in "
                    "machine-record-format/selftest_mrf.py.\n")
    _s.exit(2)
