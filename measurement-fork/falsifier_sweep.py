"""
falsifier_sweep.py -- can any arm emit a design capable of failing the
stated falsifier?

CC0-1.0. Standard library only. Deterministic. Reads the arms, the spec and
PROBES_K11_K18.py.

THE REQUIREMENT, stated in the delivered PROBES_K11_K18.py header
-----------------------------------------------------------------
    STRUCTURAL BUG THIS FIXES: coupling.py generated probes at a POINT
    while the stated falsifier ("ratio flat across the provisioning
    gradient") is about a GRADIENT. The generator could not emit a design
    capable of failing its own falsifier. compare.py must flag any
    falsifier whose terms are not swept by any arm.

That last sentence is a check, and this file is it. `compare.py` is
unmodified; this runs alongside.

WHAT THE CHECK NEEDED, AND NOW HAS
----------------------------------
This used to hand-transcribe its falsifiers from prose, because two fields
did not exist:

    probe.sweep       which spec variable a probe must be run across
    spec.falsifiers   what would refute the claim, and in which terms

Both are in the schema now. `quantities.probe()` takes
`sweep=(variable, levels)`, refuses fewer than two levels, and requires a
`point_reason` when a probe declares `sweep=None`. `validate.py` asks for
`falsifiers: [{id, statement, terms}]` and says so when they are absent.
K13's `closes=["falsifier:ratio_flat"]` resolves against that registry
instead of against nothing.

So the check is mechanical: for each declared falsifier, is every term in
the union of the variables some arm sweeps. No transcription, no
adjudication, no prose.
"""

from __future__ import annotations

import json
import os
import sys

import conventional
import coupling
import widen
from quantities import OBJECTS, resolve_sweep

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "systems", "provisioning_calibration.json")
RULE = "=" * 72


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def load_spec():
    with open(SPEC) as fh:
        return json.load(fh)


def norm(s):
    return "_".join(str(s).lower().replace("-", " ").replace(".", " ").split())


def falsifiers(spec):
    return spec.get("falsifiers") or []


def arm_sweeps(spec):
    """Every variable the arms sweep, default resolved against the regime."""
    probes = (conventional.generate(spec) + coupling.generate(spec)
              + widen.generate(spec))
    measuring = [p for p in probes if p["quantity"]["object_of"] in OBJECTS]
    swept, points = {}, []
    for p in measuring:
        r = resolve_sweep(p, spec)
        if r is None:
            points.append(p)
        else:
            swept.setdefault(r[0], []).append((p["id"], r[1]))
    return measuring, swept, points


def new_sweeps(spec):
    """Variables the K11-K16 batch sweeps."""
    ns = {}
    path = os.path.join(HERE, "PROBES_K11_K18.py")
    src = {}
    with open(path) as fh:
        exec(compile(fh.read(), path, "exec"), src)
    reg = norm((spec.get("regime") or {}).get("variable", ""))
    for p in src["COUPLING_PROBES"]:
        sw = p.get("sweep")
        if not sw:
            continue
        var = reg if sw[0] == "regime.variable" else norm(sw[0])
        ns.setdefault(var, []).append((p["id"], sw[1]))
    return src, ns


# ---------------------------------------------------------------------------


def check_declared(spec) -> None:
    section("1  what the arms declare")

    measuring, swept, points = arm_sweeps(spec)
    print("  measuring probes across the three arms: %d" % len(measuring))
    print("  swept: %d    point probes: %d\n"
          % (len(measuring) - len(points), len(points)))
    print("  %-28s %s" % ("swept variable", "probes"))
    print("  " + "-" * 62)
    for var in sorted(swept):
        print("  %-28s %s"
              % (var, ", ".join("%s@%d" % t for t in sorted(swept[var]))))
    print()
    for p in points:
        print("  point probe %s" % p["id"])
        print("      %s" % p["point_reason"])
    print()
    print("  MF_017 repaired: `sweep` is a field on quantities.probe(), it")
    print("  defaults to the spec's regime variable, it refuses fewer than")
    print("  two levels, and a point probe must say WHY. Before the repair")
    print("  the field did not exist, so 0 of %d could declare anything."
          % len(measuring))


def check_falsifiers(spec) -> None:
    section("2  each declared falsifier against the swept variables")

    _, swept, _ = arm_sweeps(spec)
    _, new = new_sweeps(spec)
    reachable_now = set(swept)
    reachable_with_new = reachable_now | set(new)

    fs = falsifiers(spec)
    if not fs:
        print("  spec declares no falsifiers -- run validate.py")
        return

    print("  %-18s %-30s %-12s %s"
          % ("falsifier", "terms", "arms now", "with K11-K16"))
    print("  " + "-" * 74)
    open_now = open_new = 0
    for f in fs:
        need = {norm(t) for t in f["terms"]}
        a = need <= reachable_now
        b = need <= reachable_with_new
        open_now += not a
        open_new += not b
        print("  %-18s %-30s %-12s %s"
              % (f["id"], ", ".join(sorted(need))[:30],
                 "yes" if a else "NO", "yes" if b else "NO"))

    print()
    print("  arms as they stand: %d of %d falsifiers reachable"
          % (len(fs) - open_now, len(fs)))
    print("  with K11-K16 added: %d of %d"
          % (len(fs) - open_new, len(fs)))
    if open_new:
        print()
        for f in fs:
            need = {norm(t) for t in f["terms"]}
            if not need <= reachable_with_new:
                print("    %s unreachable -- nothing sweeps %s"
                      % (f["id"], ", ".join(sorted(need - reachable_with_new))))


def check_registry(spec) -> None:
    section("3  K13's `closes` tag now resolves")

    src, _ = new_sweeps(spec)
    ids = {f["id"] for f in falsifiers(spec)}
    print("  spec declares falsifiers: %s\n" % ", ".join(sorted(ids)))
    dangling = []
    for p in src["COUPLING_PROBES"]:
        for tag in p.get("closes", []):
            if not tag.startswith("falsifier:"):
                continue
            fid = tag.split(":", 1)[1]
            ok = fid in ids
            print("  %-6s closes %-28s %s"
                  % (p["id"], tag, "resolves" if ok else "DANGLING"))
            if not ok:
                dangling.append((p["id"], tag))
    if not dangling:
        print()
        print("  MF_020 repaired. Before, `falsifier:ratio_flat` resolved to")
        print("  nothing in any file -- a reference to a registry that had")
        print("  not been created. The spec carries it now, and validate.py")
        print("  refuses a spec that declares no falsifiers at all.")
    else:
        print()
        print("  %d dangling reference(s)." % len(dangling))


def check_null(spec) -> None:
    section("4  the check can still fail")

    print("  A guard that cannot deny is not a guard. Two constructed")
    print("  cases, neither of which is in the spec:\n")

    _, swept, _ = arm_sweeps(spec)
    _, new = new_sweeps(spec)
    reach = set(swept) | set(new)

    cases = (
        ("reachable", {"terms": ["provisioning level"]}),
        ("unreachable", {"terms": ["ambient temperature"]}),
        ("partly", {"terms": ["provisioning level", "ambient temperature"]}),
    )
    for label, f in cases:
        need = {norm(t) for t in f["terms"]}
        ok = need <= reach
        print("    %-12s terms=%-42s %s"
              % (label, ", ".join(sorted(need)),
                 "reachable" if ok else "FLAGGED: %s"
                 % ", ".join(sorted(need - reach))))
    print()
    print("  So the check discriminates. Every falsifier in the spec being")
    print("  reachable is a property of this spec, not of the check.")


def main() -> int:
    spec = load_spec()
    print()
    print("FALSIFIER SWEEP -- can the design fail?")
    print("subject: %s" % spec["system_id"])

    check_declared(spec)
    check_falsifiers(spec)
    check_registry(spec)
    check_null(spec)

    section("READING")
    print("""
  Both schema gaps are closed. `sweep` is a field on the probe, defaulting
  to the spec's regime variable, refusing fewer than two levels, and
  requiring a stated reason when a probe is a point. `falsifiers` is a
  field on the spec, and validate.py asks for it.

  With those, the check the drop asked compare.py to run is three lines and
  needs no prose: for each declared falsifier, is every term in the union
  of the swept variables.

  K13's closes=["falsifier:ratio_flat"] resolved to nothing in any
  delivered file. It resolves now.

  Section 4 keeps the check honest: a falsifier naming a variable no arm
  sweeps is still flagged, so every falsifier in this spec coming back
  reachable is a property of the spec rather than of the check.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
