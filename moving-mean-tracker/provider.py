"""
moving-mean-tracker/provider.py -- the data interface, kept dumb on purpose.

A provider RETURNS RECORDS AND PROVENANCE. That is its whole job. It does
not compute a mean, it does not score, it does not decide what a number
means, and it does not decide what counts as noise. If an upstream source
drops records as noise, the provider reports each one as dropped, together
with the rule the source applied. The tracker reads those rules and never
invents them. (Checked by test_tracker.py from this file's AST: no
statistics import, no import of tracker.py, and no function that returns
anything except a list of records.)

A record is a dict with exactly four keys:

    id          string, unique within one pull
    attrs       dict of the fields the segment rules read
    values      dict metric name -> number, plus physical companion fields
                when the config declares one
    provenance  dict:
                  source           string
                  pull_date        YYYY-MM-DD
                  query            string, what was asked of the source
                  filters_applied  list of strings, every filter in force
                  dropped          bool
                  drop_rule        string when dropped; None when not

Only one provider ships: FixtureProvider, which produces synthetic data.
Live sources (distributional accounts, adult literacy and skills surveys,
training-text snapshots, filtered and unfiltered) come later, each as its
own Provider subclass. The network may be unavailable here, so no live
fetch exists in this build, and nothing in the shipped data is a
measurement of anything.

Run: python3 test_tracker.py
"""

from __future__ import annotations

import random
import sys

FIXTURE_SOURCE = "FIXTURE (synthetic, moving-mean-tracker/provider.py)"

# Segment layout of the fixture, matching config.example.json.
BANDS = ("low", "mid", "high")
REGIONS = ("north", "south")
# Synthetic dollar level per income band and the synthetic physical
# quantity (kcal/day) that travels with it. Invented numbers; their only
# job is to differ between bands.
BAND_LEVEL = {"low": 20000.0, "mid": 55000.0, "high": 140000.0}
BAND_KCAL = {"low": 2100.0, "mid": 2400.0, "high": 2600.0}


class Provider(object):
    """The interface. pull() returns a list of records in the shape above."""

    def pull(self, period, pull_date):
        raise NotImplementedError


class FixtureProvider(Provider):
    """Deterministic synthetic records.

    knobs (all optional):
      seed            int, default 0
      n_per_band      int, default 60
      price_index     float, default 1.0. Scales dollars only and leaves
                      the physical quantity unchanged (the G4 case).
      tail            {"band": B, "top_fraction": f, "factor": k}.
                      Multiplies the dollar values of the top f of band B's
                      records by k. Values above the band's median stay
                      above it, so the median does not move (the G1 case).
      drop            {"band": B, "fraction": f, "rule": R}. Marks the
                      lowest-valued f of band B's records as dropped by
                      rule R, the way an upstream noise filter would (the
                      G3 case). The records are still returned, flagged.
      omit_region     bool. Leaves the region attr off every record. The
                      tracker reads such a record as unassigned on that
                      axis.
    """

    def __init__(self, **knobs):
        allowed = {"seed", "n_per_band", "price_index", "tail", "drop",
                   "omit_region"}
        extra = set(knobs) - allowed
        if extra:
            raise ValueError("unknown fixture knobs: %s" % sorted(extra))
        self.knobs = dict(knobs)

    def pull(self, period, pull_date):
        k = self.knobs
        rng = random.Random(k.get("seed", 0))
        n = int(k.get("n_per_band", 60))
        price = float(k.get("price_index", 1.0))
        tail = k.get("tail")
        drop = k.get("drop")
        query = "fixture pull period=%s n_per_band=%d" % (period, n)
        filters = []
        if drop:
            filters.append("drop:%s" % drop["rule"])
        records = []
        for band in BANDS:
            raw = []
            for i in range(n):
                spread = 0.6 + 0.8 * rng.random()
                dollars = BAND_LEVEL[band] * spread
                kcal = BAND_KCAL[band] * (0.9 + 0.2 * rng.random())
                raw.append((i, dollars, kcal, REGIONS[i % 2]))
            # rank order by dollars, used only to place the tail and drop
            # knobs; the provider reports what it did, not what it means
            order = sorted(range(n), key=lambda j: raw[j][1])
            stretched = set()
            if tail and tail.get("band") == band:
                m = int(round(n * float(tail["top_fraction"])))
                stretched = set(order[n - m:]) if m else set()
            dropped = set()
            drop_rule = None
            if drop and drop.get("band") == band:
                m = int(round(n * float(drop["fraction"])))
                dropped = set(order[:m])
                drop_rule = drop["rule"]
            for j in range(n):
                i, dollars, kcal, region = raw[j]
                if j in stretched:
                    dollars = dollars * float(tail["factor"])
                attrs = {"band_label": band}
                if not k.get("omit_region"):
                    attrs["region"] = region
                is_dropped = j in dropped
                records.append({
                    "id": "%s-%s-%03d" % (period, band, i),
                    "attrs": attrs,
                    "values": {"consumption": dollars * price,
                               "consumption_kcal": kcal},
                    "provenance": {
                        "source": FIXTURE_SOURCE,
                        "pull_date": pull_date,
                        "query": query,
                        "filters_applied": list(filters),
                        "dropped": is_dropped,
                        "drop_rule": drop_rule if is_dropped else None,
                    },
                })
        return records


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        print("provider.py has no selftest; run: python3 test_tracker.py")
        sys.exit(2)
    print(__doc__.strip().splitlines()[0])
    sys.exit(0)
