#!/usr/bin/env python3
"""M3 decompose -- for any two-period comparison, join M1 (vintage_store)
against M2 (instrument_registry) and a NAICS crosswalk, and split the delta:

    real_change | revision | boundary_crossing

Boundary crossings come from the crosswalk. Where a code splits ambiguously,
the split fraction is carried as a SPREAD, so boundary_crossing is a band and
real_change inherits it. **Never a point estimate where the crosswalk is
ambiguous**: `as_point()` on an ambiguous result raises. Stdlib only, parses
under 3.9.
"""

import sys
from collections import namedtuple

Band = namedtuple("Band", "lo hi")


class AmbiguousPoint(Exception):
    """Raised when a point estimate is demanded of an ambiguous (banded)
    decomposition -- the crosswalk split is a spread."""


def point(x):
    return Band(x, x)


def is_point(b):
    return b.lo == b.hi


def sub(scalar, b):
    """scalar - Band -> Band (interval subtraction)."""
    return Band(scalar - b.hi, scalar - b.lo)


def add(a, b):
    return Band(a.lo + b.lo, a.hi + b.hi)


def as_point(b):
    if not is_point(b):
        raise AmbiguousPoint("decomposition is a band [%g, %g]; the crosswalk "
                             "split is ambiguous, so no point estimate is emitted" % (b.lo, b.hi))
    return b.lo


def boundary_effect(crosswalk, sector, applies):
    """The reclassification magnitude the boundary change moved for this
    sector, as a Band. crosswalk[sector] is either a number (unambiguous) or
    a (lo, hi) pair (ambiguous split fractions carried as a spread). No NAICS
    change in the span, or no crosswalk entry, -> point(0)."""
    if not applies or crosswalk is None or sector not in crosswalk:
        return point(0.0)
    v = crosswalk[sector]
    if isinstance(v, (tuple, list)):
        lo, hi = float(v[0]), float(v[1])
        return Band(min(lo, hi), max(lo, hi))
    return point(float(v))


def decompose(series_id, period_a, period_b, store, registry, sector,
              crosswalk=None, at_release=None):
    """Split the delta between period_a and period_b for series_id.

    Returns a dict with raw_delta, revision, boundary_crossing (Band),
    real_change (Band), ambiguous (bool), and a status. If either endpoint
    is missing from the store the delta is UNRECOVERABLE (no data); if either
    endpoint has a single vintage the revision is UNKNOWN and real_change
    inherits that as a widened band edge rather than a false point."""
    lo_obs = store.latest(series_id, period_a) if at_release is None else store.as_of(series_id, period_a, at_release)
    hi_obs = store.latest(series_id, period_b) if at_release is None else store.as_of(series_id, period_b, at_release)
    if lo_obs is None or hi_obs is None:
        return {"series_id": series_id, "status": "UNRECOVERABLE",
                "reason": "one or both endpoints absent from the vintage store "
                          "(no ALFRED data fetched; egress-blocked)",
                "real_change": None}
    raw = hi_obs.value - lo_obs.value

    rev_a = store.revision(series_id, period_a)
    rev_b = store.revision(series_id, period_b)
    revision_known = rev_a is not None and rev_b is not None
    revision = (rev_b - rev_a) if revision_known else None

    applies = bool(registry.boundary_changes(period_a, period_b))
    boundary = boundary_effect(crosswalk, sector, applies)

    rev_band = point(revision) if revision_known else point(0.0)
    real = sub(raw, add(rev_band, boundary))
    if not revision_known:
        # revision is unattributed: widen real_change to say so, do not
        # pretend the residual is clean real change.
        real = Band(min(real.lo, raw - boundary.hi), max(real.hi, raw - boundary.lo))

    return {
        "series_id": series_id, "period_a": period_a, "period_b": period_b,
        "sector": sector, "status": "OK",
        "raw_delta": raw,
        "revision": revision if revision_known else "UNKNOWN (single vintage)",
        "boundary_crossing": boundary,
        "real_change": real,
        "ambiguous": (not is_point(boundary)) or (not revision_known),
    }


def render(result):
    if result["status"] != "OK":
        return "%s x %s: %s -- %s" % (result["series_id"], result.get("period_b", "?"),
                                      result["status"], result.get("reason", ""))
    b = result["boundary_crossing"]
    r = result["real_change"]
    rev = result["revision"]
    bc = "%g" % b.lo if is_point(b) else "[%g, %g]" % (b.lo, b.hi)
    rc = "%g" % r.lo if is_point(r) else "[%g, %g]" % (r.lo, r.hi)
    return ("%s  %s->%s  raw=%g | real_change=%s | revision=%s | boundary=%s%s"
            % (result["sector"], result["period_a"], result["period_b"],
               result["raw_delta"], rc, rev, bc,
               "  (band: crosswalk ambiguous or revision unknown)" if result["ambiguous"] else ""))


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("decompose has no selftest; run selftest.py", file=sys.stderr)
        sys.exit(2)
    print("M3 decompose -- import and call decompose(); needs a loaded "
          "vintage store (egress-blocked here). Run selftest.py.", file=sys.stderr)
    sys.exit(2)
