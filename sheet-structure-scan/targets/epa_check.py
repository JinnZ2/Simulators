#!/usr/bin/env python3
"""
epa_check -- the three EPA workbooks, pre-registered before the data.

The workbooks are named in targets/EPA.md. None has been read: this
session's egress gateway answers 403 to CONNECT for www.epa.gov, logged
at 2026-08-25T15:14:12Z through 15:14:13Z, DNS resolving normally, so it
is a policy denial and not a network fault.

WHY THIS FILE EXISTS ANYWAY. The Emission Factors Hub was handed over as
a known-answer case -- almost entirely terminal constants by design, with
variance and provenance in a separate document -- with the standard
attached: if the scan does not light that up, the scan is broken. That is
the right standard and it is not yet a measurement, because "light up"
has no value. PREDICTIONS below fixes one, per target, per readout,
before any file is opened.

THE PAIR IS THE TEST, NOT EITHER WORKBOOK. A Hub run alone cannot
separate "the scan works and the Hub is flat" from "the scan reports
everything flat". The Local GHG Inventory Tool is the other arm: if the
scan returns the same profile for a workbook of live formula chains, the
scan is the thing being measured. Neither result means anything without
the other, so `--check` reports a target's own verdict and refuses to
call the instrument until both arms are in.

THE SYNTHETIC WORKBOOKS IN --selftest ARE NOT EPA. They test whether the
criterion can separate the two shapes at all. A criterion that returns
the same verdict for a flat table and a formula chain is not a
measurement of either, and that is checkable without leaving the room.
Nothing in the selftest is evidence about any EPA product.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import scans           # noqa: E402
import sheetmodel      # noqa: E402
from sheetmodel import CONSTANT_NUMBER, CYCLE, DERIVED  # noqa: E402

# Frozen 2026-08-25, before any target file was opened. patterns.json was
# edited earlier the same day and the edit is recorded in its own _note;
# no edit to that file can make the variance or sample-size patterns
# fire, which is why the differential in EFH-P3 is the load-bearing part.
PREDICTIONS = {
    "efh": {
        "name": "EPA GHG Emission Factors Hub",
        "shape": "a flat reference table: hardcoded factors, units in the "
                 "headers, variance and provenance in a separate document",
        "checks": [
            ("EFH-P1", "derived_share", "<", 0.05,
             "the stated design is hardcoded numbers, so formulas should be "
             "rare"),
            ("EFH-P2", "rank_zero_share", ">", 0.95,
             "a workbook of terminal constants has nothing downstream of "
             "anything, so deps x ddepth is zero almost everywhere and the "
             "rank column carries no ordering. This is the readout the "
             "target was handed over to test"),
            ("EFH-P3a", "unit_present", ">", 0.70,
             "an emission factor without a unit is not a factor; the units "
             "are in the headers"),
            ("EFH-P3b", "variance_present", "<", 0.10,
             "the stated design puts variance in a separate document"),
            ("EFH-P3c", "sample_present", "<", 0.10,
             "same, for the sample size behind each factor"),
            ("EFH-P4", "listed_col_share", "<", 0.10,
             "repeated headers across sheets all govern constants at depth "
             "zero, so they agree in construction and are counted rather "
             "than listed. A flat table should produce many groups and "
             "almost no collisions. Column axis: the row axis lists once "
             "per record, so a row-axis count measures table height"),
        ],
    },
    "local": {
        "name": "EPA Local GHG Inventory Tool",
        "shape": "sector calculators with live formula chains across "
                 "community and government-operations modules",
        "checks": [
            ("LOC-P1", "derived_share", ">", 0.20, "live calculators"),
            ("LOC-P2", "rank_zero_share", "<", 0.95,
             "the arm that decides whether EFH-P2 measured the Hub or "
             "measured the scan"),
            ("LOC-P3", "max_pdepth", ">", 2.0,
             "sector calculators chain through intermediates"),
            ("LOC-P4", "listed_col_count", ">", 0.0,
             "the same label carried by a community sheet and a "
             "government-operations sheet at different constructions is "
             "the case scan three was built for. Column axis for the same "
             "reason as EFH-P4: SSS_005 measured the row axis listing once "
             "per record, and a row-axis count is nearly unfalsifiable on "
             "any multi-sheet workbook"),
        ],
    },
    "simplified": {
        "name": "EPA Simplified GHG Emissions Calculator",
        "shape": "smaller, mixed",
        "checks": [],
        "no_threshold_reason":
            "no structural description was given for this one beyond its "
            "size, and a threshold guessed from that would be a number "
            "dressed as a prediction. It is the first run: the profile is "
            "reported and nothing is scored.",
    },
}


# ---------------------------------------------------------------- profile

def _is_label(wb, cell):
    lrow, lcol = scans.sheet_labels(wb, cell.sheet)
    return cell.row == lrow or cell.col == lcol


def value_cells(wb):
    """Numeric constants that are not themselves labels.

    The flag set for the companion readout. Chosen here rather than left
    to --all because SSS_003 measured what --all does to the composition:
    on the demo workbook 15 of 23 absence rows were label cells and
    strays. A stated flag rule is not scan one; it is a declared sample,
    and it prints into the report."""
    return sorted(c.key for c in wb.cells.values()
                  if c.kind == CONSTANT_NUMBER and not _is_label(wb, c))


def profile(wb, radius=scans.DEFAULT_RADIUS, patterns=None):
    patterns = patterns if patterns is not None else scans.load_patterns()[0]
    cells = list(wb.cells.values())
    n = len(cells) or 1
    derived = sum(1 for c in cells if c.kind == DERIVED)
    ranks = [wb.rank(c.key) for c in cells]
    zero = sum(1 for r in ranks if r == 0)
    cyc = sum(1 for r in ranks if r == CYCLE)
    depths = [wb.precedent_depth(c.key) for c in cells]
    finite = [d for d in depths if d != CYCLE]

    flags = value_cells(wb)
    two = scans.scan_two(wb, flags, radius, patterns)
    m = len(two) or 1
    rate = {}
    for kind in scans.COMPANION_KINDS:
        rate[kind] = sum(1 for r in two if kind not in r["absent"]
                         and kind not in r["not_searched"]) / float(m)

    listed, same, total = scans.scan_three(wb)
    ge2 = len(listed) + same
    col_listed = [r for r in listed if r["axis"] == "column"]

    return {
        "sheets": len(wb.sheets),
        "cells": len(cells),
        "derived": derived,
        "derived_share": derived / float(n),
        "rank_zero_share": zero / float(n),
        "rank_cycle": cyc,
        "max_pdepth": float(max(finite)) if finite else 0.0,
        "value_cells": len(flags),
        "unit_present": rate["unit"],
        "date_present": rate["date"],
        "sample_present": rate["sample_size"],
        "variance_present": rate["variance_sibling"],
        "groups_ge2": ge2,
        "groups_ge2_col": _col_groups(wb),
        "listed_count": float(len(listed)),
        "listed_col_count": float(len(col_listed)),
        "listed_row_count": float(len(listed) - len(col_listed)),
        "listed_share": (len(listed) / float(ge2)) if ge2 else 0.0,
        "listed_col_share": (len(col_listed) / float(_col_groups(wb)))
                            if _col_groups(wb) else 0.0,
    }


def _col_groups(wb):
    """Column-axis label groups with two or more occurrences."""
    seen = {}
    for sheet in wb.sheets:
        lrow, lcol = scans.sheet_labels(wb, sheet)
        if not lrow:
            continue
        maxr, maxc = wb.extent(sheet)
        for c in range(1, maxc + 1):
            x = wb.at(sheet, lrow, c)
            if x is None or x.kind != "CONSTANT_TEXT":
                continue
            if not scans.governed(wb, sheet, lrow, c, "column", lrow, lcol):
                continue
            seen[scans.normalize(x.value)] = seen.get(
                scans.normalize(x.value), 0) + 1
    return sum(1 for v in seen.values() if v > 1)


# A readout computed as a share needs its denominator to exist. Without
# this, EFH-P4 passes on a single-sheet workbook where no label can
# appear twice -- a predicate satisfied by an empty result set, which is
# the failure this repository recorded as PCH_001 and found here by
# running the criterion rather than by reading it.
DENOMINATOR = {
    "listed_col_share": "groups_ge2_col",
    "listed_share": "groups_ge2",
    "unit_present": "value_cells",
    "variance_present": "value_cells",
    "sample_present": "value_cells",
    "date_present": "value_cells",
}


def score(prof, target):
    spec = PREDICTIONS[target]
    out = []
    for cid, field, op, thr, why in spec["checks"]:
        got = prof.get(field)
        if got is None:
            out.append((cid, field, op, thr, None, "NOT_MEASURED", why))
            continue
        den = DENOMINATOR.get(field)
        if den is not None and not prof.get(den):
            out.append((cid, field, op, thr, got, "NOT_DETERMINABLE", why))
            continue
        ok = (got > thr) if op == ">" else (got < thr)
        out.append((cid, field, op, thr, got, "HELD" if ok else "NOT_HELD",
                    why))
    return out


# ---------------------------------------------------------------- render

def render(prof, target, path):
    spec = PREDICTIONS[target]
    lines = [
        "target        %s" % spec["name"],
        "file          %s" % os.path.basename(path),
        "predicted     %s" % spec["shape"],
        "flag rule     numeric constants that are not labels (%d of %d cells)"
        % (prof["value_cells"], prof["cells"]),
        "",
        "sheets                %d" % prof["sheets"],
        "cells                 %d" % prof["cells"],
        "derived               %d  (%.3f)" % (prof["derived"],
                                              prof["derived_share"]),
        "rank == 0             %.3f" % prof["rank_zero_share"],
        "rank == CYCLE         %d" % prof["rank_cycle"],
        "max precedent depth   %.0f" % prof["max_pdepth"],
        "",
        "companion PRESENT rate over the flag set",
        "  unit                %.3f" % prof["unit_present"],
        "  date                %.3f" % prof["date_present"],
        "  sample_size         %.3f" % prof["sample_present"],
        "  variance_sibling    %.3f" % prof["variance_present"],
        "",
        "label groups >= 2     %d  (column axis: %d)"
        % (prof["groups_ge2"], prof["groups_ge2_col"]),
        "  listed, column      %.0f  (%.3f)" % (prof["listed_col_count"],
                                                prof["listed_col_share"]),
        "  listed, row         %.0f" % prof["listed_row_count"],
        "",
    ]
    rows = score(prof, target)
    if not rows:
        lines.append("no threshold was registered for this target.")
        lines.append(spec.get("no_threshold_reason", ""))
    else:
        lines.append(scans.table(
            ["check", "readout", "predicted", "observed", "state"],
            [[cid, field, "%s %s" % (op, thr),
              "-" if got is None else "%.3f" % got, state]
             for cid, field, op, thr, got, state, _why in rows]))
        held = sum(1 for r in rows if r[5] == "HELD")
        lines += ["", "%d of %d registered predictions held." % (held, len(rows))]
    lines += [
        "",
        "This is one arm. A profile from the other arm is what decides "
        "whether these numbers describe the workbook or describe the scan.",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------- selftest

def _hub_sheet(name, n=12, offset=0.0):
    rows = {
        "A1": ("t", "Fuel Type"),
        "B1": ("t", "Heat Content (mmBtu/short ton)"),
        "C1": ("t", "CO2 Factor (kg CO2/mmBtu)"),
        "D1": ("t", "CH4 Factor (g CH4/mmBtu)"),
        "E1": ("t", "N2O Factor (g N2O/mmBtu)"),
    }
    for i in range(2, n + 2):
        rows["A%d" % i] = ("t", "Fuel %d" % (i - 1))
        rows["B%d" % i] = ("n", "%0.2f" % (18.0 + i + offset))
        rows["C%d" % i] = ("n", "%0.2f" % (90.0 + i + offset))
        rows["D%d" % i] = ("n", "%0.3f" % (0.010 + i / 1000.0))
        rows["E%d" % i] = ("n", "%0.3f" % (0.001 + i / 10000.0))
    return (name, rows)


def _hub_shape():
    """A flat reference table across two sheets sharing their headers.

    Two sheets rather than one because a single-sheet workbook cannot
    produce a column-axis label group, and EFH-P4 would then pass with an
    empty denominator. The one-sheet version is kept below as the case
    that pins the NOT_DETERMINABLE branch.
    """
    return [_hub_sheet("Stationary Combustion"),
            _hub_sheet("Mobile Combustion", n=9, offset=3.0)]


def _hub_one_sheet():
    return [_hub_sheet("Stationary Combustion")]


def _chain_shape():
    """Live calculators: every value cell derived from the sheet before."""
    a = {"A1": ("t", "Activity"), "B1": ("t", "Quantity (mmBtu)")}
    b = {"A1": ("t", "Activity"), "B1": ("t", "Emissions"),
         "C1": ("t", "Subtotal"), "D1": ("t", "Total")}
    c = {"A1": ("t", "Activity"), "B1": ("t", "Total")}
    for i in range(2, 10):
        a["A%d" % i] = ("t", "Act %d" % (i - 1))
        a["B%d" % i] = ("n", "%d" % (100 + i))
        b["A%d" % i] = ("t", "Act %d" % (i - 1))
        b["B%d" % i] = ("f", "Inputs!B%d*53.06" % i)
        b["C%d" % i] = ("f", "B%d/1000" % i)
        b["D%d" % i] = ("f", "C%d*1.0" % i)
        c["A%d" % i] = ("t", "Act %d" % (i - 1))
        c["B%d" % i] = ("f", "Community!D%d" % i)
    return [("Inputs", a), ("Community", b), ("Government Operations", c)]


def _selftest():
    import tempfile
    import fixture
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-56s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("epa_check selftest")
    print("  the two workbooks below are SYNTHETIC. They test whether the")
    print("  criterion separates a flat table from a formula chain. Nothing")
    print("  here is evidence about any EPA product.")
    d = tempfile.mkdtemp()
    hub = sheetmodel.read(
        fixture.write_demo(os.path.join(d, "hub.xlsx"), _hub_shape()))
    chain = sheetmodel.read(
        fixture.write_demo(os.path.join(d, "chain.xlsx"), _chain_shape()))
    ph, pc = profile(hub), profile(chain)

    def states(prof, target):
        return [r[5] for r in score(prof, target)]

    # A criterion that fires on both shapes measures neither.
    ck("hub shape holds every efh prediction",
       states(ph, "efh"), ["HELD"] * 6)

    # EFH-P4 is a share. On a one-sheet workbook no label can appear
    # twice, the denominator is empty, and the check passed vacuously
    # until this was found by running it. Pinned in both directions.
    one = sheetmodel.read(
        fixture.write_demo(os.path.join(d, "hub1.xlsx"), _hub_one_sheet()))
    p1 = profile(one)
    ck("one sheet: no column group exists", p1["groups_ge2_col"], 0)
    ck("and EFH-P4 says so rather than passing",
       states(p1, "efh")[5], "NOT_DETERMINABLE")
    ck("two sheets: the denominator exists",
       ph["groups_ge2_col"] > 0, True)
    ck("chain shape does NOT hold efh-P1", states(pc, "efh")[0], "NOT_HELD")
    ck("chain shape does NOT hold efh-P2", states(pc, "efh")[1], "NOT_HELD")
    ck("chain shape holds every local prediction",
       states(pc, "local"), ["HELD"] * 4)
    ck("hub shape does NOT hold local-P1", states(ph, "local")[0], "NOT_HELD")
    ck("hub shape does NOT hold local-P2", states(ph, "local")[1], "NOT_HELD")

    # The differential in EFH-P3 is the part no pattern edit can reach.
    ck("hub: unit present, variance and sample absent",
       (ph["unit_present"] > 0.7, ph["variance_present"] < 0.1,
        ph["sample_present"] < 0.1), (True, True, True))

    ck("hub rank column carries no ordering",
       ph["rank_zero_share"], 1.0)
    ck("chain rank column does",
       pc["rank_zero_share"] < 0.95, True)

    # LOC-P4 counts COLUMN-axis collisions. The row axis lists once per
    # record (SSS_005), so a row-axis count measures table height and is
    # nearly unfalsifiable on any multi-sheet workbook.
    ck("chain: one column collision, many row rows",
       (pc["listed_col_count"], pc["listed_row_count"] > 1.0), (1.0, True))
    ck("hub: repeated headers agree, so none is listed",
       ph["listed_col_count"], 0.0)

    ck("simplified registers no threshold",
       PREDICTIONS["simplified"]["checks"], [])
    ck("and says why",
       bool(PREDICTIONS["simplified"].get("no_threshold_reason")), True)

    out = render(ph, "efh", "hub.xlsx")
    import no_severity
    ck("emitted profile carries no screened word",
       no_severity.check(out)[0], True)

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


USAGE = """usage:
  epa_check.py --check WORKBOOK.xlsx --as efh|local|simplified
  epa_check.py --selftest
  epa_check.py --predictions

Targets and the reason each threshold is what it is: targets/EPA.md"""


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if "--predictions" in argv:
        for key in ("efh", "local", "simplified"):
            spec = PREDICTIONS[key]
            print("%s -- %s" % (key, spec["name"]))
            print("  %s" % spec["shape"])
            for cid, field, op, thr, why in spec["checks"]:
                print("    %-9s %-18s %s %-6s  %s" % (cid, field, op, thr, why))
            if not spec["checks"]:
                print("    none registered: %s"
                      % spec.get("no_threshold_reason", ""))
            print("")
        return 0
    if "--check" not in argv:
        print(USAGE)
        return 2
    path = argv[argv.index("--check") + 1]
    target = argv[argv.index("--as") + 1] if "--as" in argv else None
    if target not in PREDICTIONS:
        sys.stderr.write("--as must be one of: %s\n"
                         % ", ".join(sorted(PREDICTIONS)))
        return 2
    wb = sheetmodel.read(path)
    print(render(profile(wb), target, path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
