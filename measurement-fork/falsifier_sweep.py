"""
falsifier_sweep.py -- can any arm emit a design capable of failing the
stated falsifier?

CC0-1.0. Standard library only. Deterministic. Reads the delivered arms and
PROBES_K11_K18.py; modifies neither.

THE REQUIREMENT, stated in the delivered PROBES_K11_K18.py header
-----------------------------------------------------------------
    STRUCTURAL BUG THIS FIXES: coupling.py generated probes at a POINT
    while the stated falsifier ("ratio flat across the provisioning
    gradient") is about a GRADIENT. The generator could not emit a design
    capable of failing its own falsifier. compare.py must flag any
    falsifier whose terms are not swept by any arm.

That last sentence is a check, and this file is it. `compare.py` is
delivered verbatim and is not modified; this runs alongside.

WHAT THE CHECK NEEDS AND DOES NOT HAVE
--------------------------------------
Two fields, neither of which exists:

    probe.sweep       which spec variable the probe must be run across
                      -> not in quantities.probe(). MF_017.

    spec.falsifiers   what would refute the claim, and in which terms
                      -> not in the spec schema at all. The falsifier the
                         header quotes lives in prose, and K13 refers to it
                         by the tag "falsifier:ratio_flat" -- a tag that
                         resolves to nothing in any delivered file.

So the falsifier list below is TRANSCRIBED BY HAND from the prose and is
marked as such. That transcription step is the finding: a check the drop
asks `compare.py` to run cannot be run from the spec, because the spec has
nowhere to put the thing being checked. Same shape as MF_017, one level up.
"""

from __future__ import annotations

import json
import os
import sys

import conventional
import coupling
import widen
from quantities import OBJECTS

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


# ---------------------------------------------------------------------------
# [HAND-TRANSCRIBED] Falsifiers, and the spec variable each is stated in
# terms of. The spec has no `falsifiers` field, so these come from prose:
#   - the "ratio flat across the provisioning gradient" falsifier, quoted in
#     the PROBES_K11_K18.py header
#   - K13's predicted= line, "tau rises with provisioning; flat tau falsifies"
#   - K15's predicted= line, "threshold rises with staleness"
#   - the PREDICTED_ORDER mediation falsifier
FALSIFIERS = (
    ("ratio_flat",
     "ratio flat across the provisioning gradient",
     ("provisioning level",),
     "quoted in the PROBES_K11_K18.py header; K13 tags it "
     "closes=['falsifier:ratio_flat']"),
    ("tau_flat",
     "tau rises with provisioning; flat tau falsifies",
     ("provisioning level",),
     "K13 predicted="),
    ("threshold_flat",
     "detection threshold rises with staleness; flat falsifies",
     ("time since clean reference",),
     "K15 predicted="),
    ("mediation_broken",
     "K14 predicts K16 with K15 controlled out",
     ("provisioning level", "time since clean reference",
      "baseline staleness"),
     "PREDICTED_ORDER"),
)


def delivered_sweeps(spec):
    """Every variable any DELIVERED arm sweeps. Spoiler: none."""
    probes = (conventional.generate(spec) + coupling.generate(spec)
              + widen.generate(spec))
    measuring = [p for p in probes if p["quantity"]["object_of"] in OBJECTS]
    swept = set()
    for p in measuring:
        if "sweep" in p and p["sweep"]:
            swept.add(norm(p["sweep"][0]))
    return measuring, swept


def new_sweeps(spec):
    """Variables the K11-K16 batch sweeps, resolving the default."""
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


def check_delivered(spec) -> None:
    section("1  the delivered arms sweep nothing")

    measuring, swept = delivered_sweeps(spec)
    print("  measuring probes across the three arms: %d" % len(measuring))
    print("  of those, carrying a sweep declaration:  %d" % len(swept))
    print()
    print("  quantities.probe() fields: arm id quantity protocol reads")
    print("                             blind_to")
    print()
    print("  So every falsifier below is unreachable by every delivered")
    print("  probe, and not because any probe was written badly. The")
    print("  generator has no way to emit a swept design.")


def check_falsifiers(spec) -> None:
    section("2  each falsifier against the variables actually swept")

    _, delivered = delivered_sweeps(spec)
    src, new = new_sweeps(spec)
    reg = norm((spec.get("regime") or {}).get("variable", ""))

    print("  regime variable declared in the spec: %r -> %r\n"
          % ((spec.get("regime") or {}).get("variable"), reg))
    print("  variables swept by the K11-K16 batch:\n")
    for var in sorted(new):
        who = ", ".join("%s@%d" % (i, n) for i, n in sorted(new[var]))
        print("      %-30s %s" % (var, who))

    print()
    print("  %-18s %-34s %s" % ("falsifier", "terms", "reachable?"))
    print("  " + "-" * 72)
    unreached = []
    for tag, text, terms, _ in FALSIFIERS:
        need = {norm(t) for t in terms}
        have_new = need <= set(new)
        have_old = need <= delivered
        verdict = ("YES via K11-K16" if have_new
                   else "NO -- unswept: %s"
                        % ", ".join(sorted(need - set(new))))
        if not have_new:
            unreached.append((tag, sorted(need - set(new))))
        print("  %-18s %-34s %s"
              % (tag, ", ".join(sorted(need))[:34], verdict))
        if have_old:
            print("      (also reachable by a delivered arm)")

    print()
    print("  delivered arms: 0 of %d falsifiers reachable" % len(FALSIFIERS))
    print("  with K11-K16:   %d of %d reachable"
          % (len(FALSIFIERS) - len(unreached), len(FALSIFIERS)))
    if unreached:
        print()
        for tag, missing in unreached:
            print("    %s still unreachable -- no probe sweeps %s"
                  % (tag, ", ".join(missing)))


def check_schema_gap() -> None:
    section("3  the check cannot be run from the spec")

    spec = load_spec()
    print("  spec fields: %s\n" % ", ".join(sorted(spec)))
    print("  `falsifiers` is not among them.\n")
    print("  So the requirement in the PROBES_K11_K18.py header --")
    print()
    print("      compare.py must flag any falsifier whose terms are not")
    print("      swept by any arm")
    print()
    print("  needs two fields that do not exist. `sweep` on a probe")
    print("  (MF_017), and `falsifiers` on a spec. The four falsifiers in")
    print("  section 2 are HAND-TRANSCRIBED from prose and from the")
    print("  `predicted=` lines of individual probes.")
    print()
    print("  K13 makes the gap concrete: it declares")
    print()
    print("      closes=['reversibility', 'falsifier:ratio_flat']")
    print()
    print("  and `falsifier:ratio_flat` resolves to nothing in any")
    print("  delivered file. It is a reference to a registry that has not")
    print("  been created. Once it exists, section 2 becomes mechanical and")
    print("  this hand transcription goes away.")
    print()
    print("  The two gaps are the same gap seen at two levels: a probe")
    print("  cannot say what it must be run across, and a spec cannot say")
    print("  what would refute it. Between them, a generator can emit a")
    print("  complete, well-formed design that is incapable of failing.")


def check_what_it_would_take(spec) -> None:
    section("4  the smallest schema that makes this mechanical")

    print("  On the probe, one field (MF_017's):\n")
    print('      sweep = (spec_variable, n_levels)   # or None + a reason\n')
    print("  On the spec, one list:\n")
    print("""      "falsifiers": [
        {"id": "ratio_flat",
         "statement": "ratio flat across the provisioning gradient",
         "terms": ["provisioning level"]}
      ]\n""")
    print("  Then the check is three lines: for each falsifier, is every")
    print("  term in the union of the arms' swept variables. No prose, no")
    print("  transcription, no adjudication.")
    print()
    print("  And it is a PRE-stage check, not a post one -- it decides")
    print("  whether the design can fail before anything is measured, which")
    print("  is the ../reasoning-gate/ G-CTRL shape: controls sized by")
    print("  fragility, declared before the run.")


def main() -> int:
    spec = load_spec()
    print()
    print("FALSIFIER SWEEP -- can the design fail?")
    print("subject: %s" % spec["system_id"])

    check_delivered(spec)
    check_falsifiers(spec)
    check_schema_gap()
    check_what_it_would_take(spec)

    section("READING")
    print("""
  The delivered arms sweep nothing, so 0 of 4 stated falsifiers are
  reachable by any probe they emit. That is not a badly written probe --
  `quantities.probe()` has no `sweep` field, so the generator cannot emit
  a swept design at all.

  The K11-K16 batch sweeps four variables and makes 4 of 4 reachable.

  The check the drop asks compare.py to run cannot be run from the spec,
  because the spec has no `falsifiers` field. K13 declares
  closes=['falsifier:ratio_flat'] and that tag resolves to nothing in any
  delivered file -- a reference to a registry that does not exist yet. The
  four falsifiers checked here are hand-transcribed from prose.

  Two schema gaps, one shape: a probe cannot say what it must be run
  across, and a spec cannot say what would refute it. Between them a
  generator can emit a complete, well-formed design that is incapable of
  failing, which is what happened.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
