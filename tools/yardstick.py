"""Coupling vs border-maintenance energy: a yardstick.

CC0. Stdlib only. Parses under Python 3.9. Companion to
tools/coupling_vs_border_energy_yardstick.md, which states what this reads
and where it stops.

The glyph READS. It does not determine value for anyone. This module stops
at the readout: a fraction, a band, a list of gaps and a list of loops. It
ranks nothing, scores nobody, and names no actor.

Input, one JSON list of items:

    {"item": "name", "spend": 50, "class": "coupling|border|coordinating",
     "depends_on": ["other item", ...]}

    coupling      spend that connects parts so something moves between them
    border        spend that holds a separation in place
    coordinating  a boundary that does work for the parts it separates

`depends_on` names what an item needs in order to exist: X depends_on Y
means Y is spent so that X can stand.

Readouts, never merged into one number:

    DIRECT       border spend / classified spend
    ROLLED UP    border spend plus the spend of every non-border item that
                 exists to hold a border item up, through the depends_on
                 tree. An item reached from a border item AND from a
                 coupling or coordinating root is SHARED; it is never split
                 by an assumed ratio, so the rolled-up reading is a band
                 [exclusive, exclusive + shared] whenever SHARED is non-empty
    GAPS         items with no class, an unknown class, or an unknown
                 dependency. A gap never enters a fraction; the span its
                 spend could move each fraction across is printed beside it
    LOOPS        dependency cycles through a border item, e.g.
                 enforcement -> administration -> funding -> extraction ->
                 enforcement

Commands:

    python3 tools/yardstick.py items.json          readout of one snapshot
    python3 tools/yardstick.py --compare a.json b.json
                                                   two dated snapshots side
                                                   by side; trajectory read
                                                   from spend
    python3 tools/yardstick.py --toy               the ILLUSTRATIVE toy
    python3 tools/yardstick.py --selftest          known answers + the md

Exit contract: 0 readout produced / selftest passed, 1 selftest failed,
3 input unreadable. Every run ends with a VERDICT line.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTE = os.path.join(HERE, "coupling_vs_border_energy_yardstick.md")

COUPLING = "coupling"
BORDER = "border"
COORDINATING = "coordinating"
CLASSES = (COUPLING, BORDER, COORDINATING)

READS_LINE = ("The glyph READS. It does not determine value for anyone.")
INDEX_LINE = ("reads energy routed to coupling vs to holding separations; "
              "a readout, not a ranking.")

# ILLUSTRATIVE: made-up round numbers. Not a measurement of any place,
# body or organization. The loop is the shape the note names.
TOY = [
    {"item": "road_repair", "spend": 100, "class": COUPLING,
     "depends_on": []},
    {"item": "shared_clinic", "spend": 80, "class": COUPLING,
     "depends_on": ["general_treasury"]},
    {"item": "market_exchange", "spend": 60, "class": COUPLING,
     "depends_on": ["records_office"]},
    {"item": "standards_protocol", "spend": 20, "class": COORDINATING,
     "depends_on": []},
    {"item": "general_treasury", "spend": 20, "class": COORDINATING,
     "depends_on": []},
    {"item": "records_office", "spend": 10, "class": COORDINATING,
     "depends_on": []},
    {"item": "border_enforcement", "spend": 50, "class": BORDER,
     "depends_on": ["enforcement_admin", "records_office"]},
    {"item": "enforcement_admin", "spend": 30, "class": COORDINATING,
     "depends_on": ["enforcement_funding"]},
    {"item": "enforcement_funding", "spend": 20, "class": COORDINATING,
     "depends_on": ["extraction_levy"]},
    {"item": "extraction_levy", "spend": 40, "class": None,
     "depends_on": ["border_enforcement"]},
    {"item": "differentiation_ads", "spend": 30, "class": BORDER,
     "depends_on": []},
    {"item": "unlabelled_line", "spend": 10, "class": "",
     "depends_on": []},
]


class InputError(ValueError):
    pass


def load_items(raw):
    """Validate a parsed JSON list. Refuses what would make a fraction
    wrong (a missing or non-numeric or negative spend, a repeated item);
    keeps what is merely unknown (class, dependency) as a gap."""
    if not isinstance(raw, list):
        raise InputError("input must be a JSON list of items")
    items, seen = [], set()
    for n, it in enumerate(raw, 1):
        if not isinstance(it, dict):
            raise InputError("item %d is not an object" % n)
        name = it.get("item")
        if not isinstance(name, str) or not name.strip():
            raise InputError("item %d has no name" % n)
        if name in seen:
            raise InputError("item %r repeated" % name)
        spend = it.get("spend")
        if isinstance(spend, bool) or not isinstance(spend, (int, float)):
            raise InputError("item %r: spend %r is not a number"
                             % (name, spend))
        if spend < 0:
            raise InputError("item %r: negative spend %r" % (name, spend))
        deps = it.get("depends_on", [])
        if deps is None:
            deps = []
        if not isinstance(deps, list) or not all(
                isinstance(d, str) for d in deps):
            raise InputError("item %r: depends_on must be a list of names"
                             % name)
        seen.add(name)
        items.append({"item": name, "spend": float(spend),
                      "class": it.get("class"), "depends_on": list(deps)})
    return items


def _reach(starts, graph):
    out, stack = set(), list(starts)
    while stack:
        cur = stack.pop()
        for nxt in graph.get(cur, ()):
            if nxt not in out:
                out.add(nxt)
                stack.append(nxt)
    return out


def _cycles_through(start, graph):
    """Simple cycles through `start`, as name lists, shortest first."""
    found = []

    def walk(node, path):
        for nxt in graph.get(node, ()):
            if nxt == start:
                found.append(path + [start])
            elif nxt not in path:
                walk(nxt, path + [nxt])
    walk(start, [start])
    return sorted(found, key=lambda c: (len(c), c))


def read(items):
    """The readout. Returns a dict; nothing in it is a verdict."""
    by = {it["item"]: it for it in items}
    graph = {it["item"]: [d for d in it["depends_on"] if d in by]
             for it in items}
    gaps = []
    for it in items:
        c = it["class"]
        if c is None or c == "":
            gaps.append((it["item"], it["spend"], "no class"))
        elif c not in CLASSES:
            gaps.append((it["item"], it["spend"],
                         "class %r is not one of %s" % (c, "/".join(CLASSES))))
    dangling = [(it["item"], d) for it in items for d in it["depends_on"]
                if d not in by]
    gap_names = set(g[0] for g in gaps)
    classified = [it for it in items if it["item"] not in gap_names]
    total = sum(it["spend"] for it in classified)
    gap_spend = sum(g[1] for g in gaps)
    border = [it["item"] for it in classified if it["class"] == BORDER]
    b_spend = sum(by[n]["spend"] for n in border)

    from_border = _reach(border, graph)
    roots = [it["item"] for it in classified
             if it["class"] in (COUPLING, COORDINATING)
             and it["item"] not in from_border]
    from_roots = _reach(roots, graph) | set(roots)
    support = sorted(n for n in from_border
                     if n not in border and n not in gap_names)
    exclusive = [n for n in support if n not in from_roots]
    shared = [n for n in support if n in from_roots]
    gap_support = sorted(n for n in from_border if n in gap_names)
    ex_spend = sum(by[n]["spend"] for n in exclusive)
    sh_spend = sum(by[n]["spend"] for n in shared)

    def frac(x, d):
        return None if d <= 0 else x / d

    loops = []
    for b in border:
        for cyc in _cycles_through(b, graph):
            key = tuple(sorted(cyc[:-1]))
            if key not in [tuple(sorted(c[:-1])) for c in loops]:
                loops.append(cyc)

    every = total + gap_spend
    return {
        "n_items": len(items),
        "classified_spend": total,
        "gap_spend": gap_spend,
        "gaps": gaps,
        "dangling": dangling,
        "border": border,
        "direct": frac(b_spend, total),
        "rolled_exclusive": frac(b_spend + ex_spend, total),
        "rolled_with_shared": frac(b_spend + ex_spend + sh_spend, total),
        "exclusive": exclusive,
        "shared": shared,
        "gap_support": gap_support,
        "direct_gap_span": (frac(b_spend, every),
                            frac(b_spend + gap_spend, every)),
        "rolled_gap_span": (frac(b_spend + ex_spend, every),
                            frac(b_spend + ex_spend + sh_spend + gap_spend,
                                 every)),
        "loops": loops,
    }


def _f(v):
    return "none (no classified spend)" if v is None else "%.3f" % v


def _span(pair):
    lo, hi = pair
    if lo is None:
        return "none"
    return "[%.3f, %.3f]" % (lo, hi)


def render(rd, label=None):
    L = []
    if label:
        L.append("snapshot  %s" % label)
    L.append("items %d   classified spend %g   gap spend %g"
             % (rd["n_items"], rd["classified_spend"], rd["gap_spend"]))
    L.append("border fraction, direct           %s" % _f(rd["direct"]))
    if rd["shared"]:
        L.append("border fraction, rolled up        [%s, %s]  (band: "
                 "shared items are not split)"
                 % (_f(rd["rolled_exclusive"]),
                    _f(rd["rolled_with_shared"])))
    else:
        L.append("border fraction, rolled up        %s"
                 % _f(rd["rolled_exclusive"]))
    L.append("  rolled up, exclusive support    %s"
             % (", ".join(rd["exclusive"]) or "none"))
    L.append("  rolled up, shared (not split)   %s"
             % (", ".join(rd["shared"]) or "none"))
    L.append("gaps (never assumed; outside every fraction):")
    if not rd["gaps"] and not rd["dangling"]:
        L.append("  none")
    for name, spend, why in rd["gaps"]:
        tag = "  [holds up a border item]" if name in rd["gap_support"] \
            else ""
        L.append("  %-22s %8g  %s%s" % (name, spend, why, tag))
    for name, dep in rd["dangling"]:
        L.append("  %-22s depends on %r, which is not in the input"
                 % (name, dep))
    L.append("if the gaps were classified, over all spend: direct %s, "
             "rolled up %s" % (_span(rd["direct_gap_span"]),
                               _span(rd["rolled_gap_span"])))
    L.append("loops through a border item:")
    if not rd["loops"]:
        L.append("  none")
    for cyc in rd["loops"]:
        L.append("  " + " -> ".join(cyc))
    L.append("This is a readout, not a ranking. It reads throughput and "
             "trajectory, not truth or worth.")
    return L


def compare_lines(a, b, la, lb):
    L = ["%-34s %-20s %s" % ("", la, lb)]
    rows = (("border fraction, direct", "direct"),
            ("rolled up, exclusive", "rolled_exclusive"),
            ("rolled up, with shared", "rolled_with_shared"))
    for title, key in rows:
        va, vb = a[key], b[key]
        if va is None or vb is None:
            move = "not comparable (no classified spend)"
        elif abs(vb - va) < 1e-12:
            move = "unchanged"
        else:
            move = "%+.3f" % (vb - va)
        L.append("%-34s %-20s %-10s %s" % (title, _f(va), _f(vb), move))
    L.append("gap spend %34g %20g" % (a["gap_spend"], b["gap_spend"]))
    L.append("Trajectory is read from spend, not stated aim. A movement in a "
             "fraction is a readout; it is not a verdict on anyone.")
    return L


# ---------------------------------------------------------------- note

def fenced(doc, name):
    m = re.findall(r"```%s\n(.*?)```" % re.escape(name), doc, re.S)
    if len(m) != 1:
        raise ValueError("expected one %s block, found %d" % (name, len(m)))
    return m[0]


def toy_block():
    return "".join(ln + "\n" for ln in render(read(load_items(TOY))))


# ---------------------------------------------------------------- selftest

def _item(name, spend, cls, deps=()):
    return {"item": name, "spend": spend, "class": cls,
            "depends_on": list(deps)}


def selftest():
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    def expect_error(raw):
        try:
            load_items(raw)
        except InputError:
            return True
        return False

    def near(a, b):
        return a is not None and abs(a - b) < 1e-9

    rd = read(load_items([_item("a", 10, COUPLING)]))
    check("all coupling: direct fraction 0", near(rd["direct"], 0.0))
    rd = read(load_items([_item("a", 10, BORDER)]))
    check("all border: direct fraction 1", near(rd["direct"], 1.0))
    rd = read(load_items([_item("a", 30, COUPLING), _item("b", 10, BORDER)]))
    check("30 coupling + 10 border: direct 0.25", near(rd["direct"], 0.25))
    rd = read(load_items([_item("a", 30, COUPLING), _item("b", 10, BORDER),
                          _item("c", 60, None)]))
    check("a gap never enters the fraction (still 0.25)",
          near(rd["direct"], 0.25))
    check("a gap is listed, with its spend",
          rd["gaps"] == [("c", 60.0, "no class")])
    check("the gap span shows how far the gap could move it",
          near(rd["direct_gap_span"][0], 0.1)
          and near(rd["direct_gap_span"][1], 0.7))
    rd = read(load_items([_item("a", 10, "bordr")]))
    check("an unknown class is a gap, not a guess",
          rd["gaps"] and "not one of" in rd["gaps"][0][2]
          and rd["direct"] is None)
    rd = read(load_items([_item("b", 10, BORDER, ["admin"]),
                          _item("admin", 10, COORDINATING),
                          _item("c", 20, COUPLING)]))
    check("rollup: admin held up only by a border item rolls up",
          near(rd["direct"], 0.25) and near(rd["rolled_exclusive"], 0.5)
          and rd["exclusive"] == ["admin"] and not rd["shared"])
    rd = read(load_items([_item("b", 10, BORDER, ["rec"]),
                          _item("rec", 10, COORDINATING),
                          _item("c", 20, COUPLING, ["rec"])]))
    check("rollup: an item shared with a coupling root is a band, "
          "never split", rd["shared"] == ["rec"]
          and near(rd["rolled_exclusive"], 0.25)
          and near(rd["rolled_with_shared"], 0.5))
    rd = read(load_items([_item("enf", 10, BORDER, ["adm"]),
                          _item("adm", 10, COORDINATING, ["fund"]),
                          _item("fund", 10, COORDINATING, ["ext"]),
                          _item("ext", 10, COORDINATING, ["enf"])]))
    check("a self-feeding loop through a border item is reported",
          rd["loops"] == [["enf", "adm", "fund", "ext", "enf"]])
    rd = read(load_items([_item("a", 10, BORDER, ["ghost"])]))
    check("an unknown dependency is reported, not assumed",
          rd["dangling"] == [("a", "ghost")])
    rd = read(load_items([]))
    check("an empty input reads none, not zero", rd["direct"] is None)
    check("negative spend is refused",
          expect_error([_item("a", -1, COUPLING)]))
    check("a boolean spend is refused",
          expect_error([_item("a", True, COUPLING)]))
    check("a repeated item is refused",
          expect_error([_item("a", 1, COUPLING), _item("a", 2, BORDER)]))
    toy = read(load_items(TOY))
    check("toy: direct = border 80 / classified 420",
          near(toy["direct"], 80.0 / 420.0))
    check("toy: rolled up is the band [130/420, 140/420] (records_office "
          "shared, not split)", near(toy["rolled_exclusive"], 130.0 / 420.0)
          and near(toy["rolled_with_shared"], 140.0 / 420.0)
          and toy["shared"] == ["records_office"])
    check("toy: the levy loop is found",
          ["border_enforcement", "enforcement_admin", "enforcement_funding",
           "extraction_levy", "border_enforcement"] in toy["loops"])
    a = read(load_items([_item("a", 30, COUPLING), _item("b", 10, BORDER)]))
    b = read(load_items([_item("a", 30, COUPLING), _item("b", 30, BORDER)]))
    cmp_ = "\n".join(compare_lines(a, b, "t0", "t1"))
    check("compare prints the movement and no verdict",
          "+0.250" in cmp_ and "not a verdict" in cmp_)

    try:
        with open(NOTE, "r", encoding="utf-8") as fh:
            doc = fh.read()
        noted = True
    except OSError as ex:
        noted = False
        check("the note is readable", False, str(ex))
    if noted:
        try:
            got = fenced(doc, "yardstick-toy")
        except ValueError as ex:
            got = "missing: %s" % ex
        check("the note's toy block equals the computed readout",
              got == toy_block(), "rerun --toy and paste")
        planted = doc.replace("direct           0.190",
                              "direct           0.191", 1)
        try:
            caught = fenced(planted, "yardstick-toy") != toy_block()
        except ValueError:
            caught = True
        check("plant: an edited toy number in the note is caught",
              planted != doc and caught)
        flat = re.sub(r"\s+", " ", doc)
        low = flat.lower()
        check("the note says the glyph reads and stops at the readout",
              READS_LINE in flat and "stops at the readout" in flat)
        check("the note carries the index line", INDEX_LINE in flat)
        check("the note labels the toy ILLUSTRATIVE", "ILLUSTRATIVE" in doc)
        for edge in ("not truth or moral worth",
                     "does the boundary keep its own upkeep",
                     "classification is a boundary choice",
                     "the reader is coupled"):
            check("honest edge stated: %s" % edge, edge in low)
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                        "sheet-structure-scan"))
        import no_severity
        text = toy_block() + "\n".join(compare_lines(a, b, "t0", "t1"))
        check("the readout screens clean through no_severity",
              not no_severity.hits(text), str(no_severity.hits(text)))
    except ImportError:
        check("no_severity available", False)
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as fh:
        src = fh.read()
    imports = set(re.findall(r"^(?:import|from) (\w+)", src, re.M))
    check("module-level imports only stdlib json/os/re/sys",
          imports <= {"json", "os", "re", "sys"}, ",".join(sorted(imports)))

    failed = 0
    for name, ok, detail in results:
        failed += 0 if ok else 1
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name,
                            ("  [%s]" % detail) if detail and not ok
                            else ""))
    print("VERDICT: %s   checks=%d failed=%d"
          % ("PASS" if not failed else "FAIL", len(results), failed))
    return 0 if not failed else 1


# ---------------------------------------------------------------- main

def _load_path(path):
    with open(path, "r", encoding="utf-8") as fh:
        return load_items(json.load(fh))


def main(argv):
    if argv[:1] == ["--selftest"]:
        return selftest()
    try:
        if argv[:1] == ["--toy"]:
            print("ILLUSTRATIVE toy: made-up round numbers")
            for ln in render(read(load_items(TOY))):
                print(ln)
        elif argv[:1] == ["--compare"] and len(argv) == 3:
            a, b = _load_path(argv[1]), _load_path(argv[2])
            for ln in compare_lines(read(a), read(b), argv[1], argv[2]):
                print(ln)
        elif len(argv) == 1 and not argv[0].startswith("--"):
            for ln in render(read(_load_path(argv[0])), argv[0]):
                print(ln)
        else:
            print(__doc__.split("Commands:")[1].split("Exit contract")[0])
            print("VERDICT: SKIP   reason=usage")
            return 3
    except (OSError, ValueError) as ex:
        print("could not read the input: %s" % ex)
        print("VERDICT: SKIP   reason=%s" % type(ex).__name__)
        return 3
    print("VERDICT: READOUT")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
