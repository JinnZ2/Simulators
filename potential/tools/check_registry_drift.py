"""check_registry_drift.py — the registry's vocabularies are declared
in two places and must not diverge.

`tools/registry.py` declares MECHANISMS and SHAPE_PAIRS locally, on
purpose: a registry that imports a folder cannot record an entry from a
folder that has been renamed or removed. The cost is that
`potential/transformation.py` and `tools/registry.py` hold the same two
tuples and nothing forces them to match.

This tool forces them to match. It loads both modules by file path, so
neither needs to be a package, and reports every identifier present in
one and not the other, in both directions.

Exit 1 on drift. `--selftest` builds a divergent pair and asserts the
detector fires, so a clean result on the real tree means something.
"""

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent      # potential/tools
FOLDER = HERE.parent                         # potential/

# This tool lives in potential/tools/, not the repo-root tools/. The first
# version resolved ROOT/potential/transformation.py from here, which is
# potential/potential/transformation.py -- a path that never existed --
# and the real-tree selftest arm then skipped on it silently (P-05,
# briefs/REPORT.txt). The path is now the sibling of this directory.
SOURCES = (
    ("transformation", FOLDER / "transformation.py"),
    ("registry",       HERE / "registry.py"),
)

def load_by_path(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def diff_sets(label, a_name, a_set, b_name, b_set):
    """Return (only_a, only_b) as sorted lists. Empty both means match."""
    only_a = sorted(set(a_set) - set(b_set))
    only_b = sorted(set(b_set) - set(a_set))
    return only_a, only_b

def compare(mechanisms_a, pairs_a, mechanisms_b, pairs_b):
    """Return a report dict. Nothing here combines the two findings."""
    m_only_a, m_only_b = diff_sets("mechanisms", "a", mechanisms_a, "b", mechanisms_b)
    # shape pairs are tuples of two strings; compare as strings for reporting
    p_a = {f"{s}->{t}" for s, t in pairs_a}
    p_b = {f"{s}->{t}" for s, t in pairs_b}
    p_only_a, p_only_b = diff_sets("pairs", "a", p_a, "b", p_b)
    return {
        "mechanisms_match": not m_only_a and not m_only_b,
        "pairs_match": not p_only_a and not p_only_b,
        "mechanisms_only_in_first": m_only_a,
        "mechanisms_only_in_second": m_only_b,
        "pairs_only_in_first": p_only_a,
        "pairs_only_in_second": p_only_b,
    }

def render(report, a_label="transformation.py", b_label="registry.py"):
    lines = []
    if report["mechanisms_match"] and report["pairs_match"]:
        lines.append(f"no drift: {a_label} and {b_label} agree on both vocabularies")
        return "\n".join(lines)
    lines.append("DRIFT")
    if not report["mechanisms_match"]:
        lines.append("")
        lines.append(f"mechanisms only in {a_label}:")
        for m in report["mechanisms_only_in_first"]:
            lines.append(f"  {m}")
        lines.append(f"mechanisms only in {b_label}:")
        for m in report["mechanisms_only_in_second"]:
            lines.append(f"  {m}")
    if not report["pairs_match"]:
        lines.append("")
        lines.append(f"shape-pairs only in {a_label}:")
        for p in report["pairs_only_in_first"]:
            lines.append(f"  {p}")
        lines.append(f"shape-pairs only in {b_label}:")
        for p in report["pairs_only_in_second"]:
            lines.append(f"  {p}")
    return "\n".join(lines)

def run():
    mods = {}
    for name, path in SOURCES:
        if not path.exists():
            print(f"missing: {path}", file=sys.stderr)
            return 3  # could not run (EXIT_CONTRACT), not a redirect
        mods[name] = load_by_path(name, path)
    report = compare(
        mods["transformation"].MECHANISMS,
        mods["transformation"].SHAPE_PAIRS,
        mods["registry"].MECHANISMS,
        mods["registry"].SHAPE_PAIRS,
    )
    print(render(report))
    return 0 if (report["mechanisms_match"] and report["pairs_match"]) else 1

def selftest():
    checks = 0
    def check(cond, msg):
        nonlocal checks
        checks += 1
        if not cond:
            raise AssertionError(msg)

    # matching
    r = compare(("A", "B"), (("x", "y"),), ("A", "B"), (("x", "y"),))
    check(r["mechanisms_match"] and r["pairs_match"], "matched pair misreported")

    # extra mechanism on one side
    r = compare(("A", "B"), (("x", "y"),), ("A", "B", "C"), (("x", "y"),))
    check(not r["mechanisms_match"], "extra mechanism not detected")
    check(r["mechanisms_only_in_second"] == ["C"], "extra mechanism misnamed")
    check(r["mechanisms_only_in_first"] == [], "phantom mechanism reported")

    # missing mechanism on one side
    r = compare(("A", "B"), (("x", "y"),), ("A",), (("x", "y"),))
    check(not r["mechanisms_match"], "missing mechanism not detected")
    check(r["mechanisms_only_in_first"] == ["B"], "missing mechanism misnamed")

    # extra pair on one side
    r = compare(("A",), (("x", "y"),), ("A",), (("x", "y"), ("p", "q")))
    check(not r["pairs_match"], "extra pair not detected")
    check(r["pairs_only_in_second"] == ["p->q"], "extra pair misnamed")

    # direction-only difference: (x,y) vs (y,x) are different pairs
    r = compare(("A",), (("x", "y"),), ("A",), (("y", "x"),))
    check(not r["pairs_match"], "reversed pair not treated as different")

    # null test: the detector fires on a plant
    r = compare(("A",), (("x", "y"),), ("A", "PLANTED"), (("x", "y"),))
    check(not r["mechanisms_match"], "planted divergence missed")
    check("PLANTED" in r["mechanisms_only_in_second"], "plant not named")

    # real tree. A missing file is a hard FAIL naming the path, never a
    # skip: the arm that skipped was the arm that would have caught the
    # typo'd filename and the corrupted registry (P-03, P-04, P-05).
    for name, path in SOURCES:
        check(path.exists(), f"real tree: {name} missing at {path}")
    a = load_by_path("transformation", SOURCES[0][1])
    b = load_by_path("registry", SOURCES[1][1])
    r = compare(a.MECHANISMS, a.SHAPE_PAIRS, b.MECHANISMS, b.SHAPE_PAIRS)
    check(r["mechanisms_match"], f"real tree mechanism drift: {r}")
    check(r["pairs_match"], f"real tree pair drift: {r}")

    print(f"checks: {checks}")
    print("PASS")
    return 0

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(run())
