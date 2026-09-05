# SPDX-License-Identifier: CC0-1.0
"""
A worked pass over the format on CONSTRUCTED entries: parallel views, an
aggregate recomputed at read time, a retained vintage revision, the four
absence states kept apart, a boundary-mismatch refusal, and the bisection
structure verdicts. No row is a measurement of anything; every value is built
by hand to exercise the format. The emitted text is screened through
sheet-structure-scan/no_severity.

    python3 machine-record-format/demo.py            # print
    python3 machine-record-format/demo.py --write    # write samples/
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import base_entry as be           # noqa: E402
import views as vw                # noqa: E402
import aggregate as ag            # noqa: E402
import entry_store as es          # noqa: E402
import bisect_structure as bs     # noqa: E402
import no_severity                # noqa: E402

S = be.State
B = be.Boundary
GATE = B(("extraction",), ("transport",), "gate-to-gate")


def mk(eid, joules, status=be.MEASURED, exposure=10.0, release="2026-01-10"):
    if status in be.ABSENT:
        exposure = None            # an all-absent entry carries no measured column
    return be.write_base_entry(
        entry_id=eid, input_state=S("ore", 100.0, "kg"),
        output_state=S("metal", 5.0, "kg"), exposure=exposure,
        exposure_unit="person-hours", joules_in=joules, period="2026",
        observation_method="meter", provenance="constructed",
        status=status, boundary=GATE, release_date=release)


def render():
    L = []
    L.append("MACHINE-RECORD-FORMAT DEMO -- CONSTRUCTED ENTRIES, NOT A MEASUREMENT")
    L.append("=" * 66)

    ents = [mk("a", 100.0), mk("b", 50.0), mk("c", 30.0),
            mk("d", 0.0, status=be.MEASURED_ZERO),
            mk("e", None, status=be.UNMEASURED_NO_INSTRUMENT)]
    L.append("")
    L.append("base entries (transformations; no category field on any record):")
    for e in ents:
        L.append("  %s  %s->%s  exposure=%s %s  joules=%s  status=%s"
                 % (e.entry_id, e.input_state.quantity, e.output_state.quantity,
                    e.exposure, e.exposure_unit,
                    "--" if e.joules_in is None else e.joules_in, e.status))

    reg = vw.ViewRegistry()
    reg.add_view(vw.View("v1", "metabolic_class", "energy analyst", ("", ""),
                         {"a": "hot", "b": "hot", "c": "cold", "d": "cold",
                          "e": "cold"}))
    reg.add_view(vw.View("v2", "process_stage", "process analyst", ("", ""),
                         {"a": "primary", "b": "secondary", "c": "primary",
                          "d": "secondary", "e": "primary"}))
    L.append("")
    L.append("two parallel views, neither canonical (Rule 2). one entry, "
             "both labels side by side:")
    for eid in ("a", "c", "e"):
        L.append("  %s : %s" % (eid, reg.labels_for(eid)))

    L.append("")
    L.append("aggregate computed at read time (Rule 3), grouped by each view "
             "in turn; measured_zero and unmeasured counted apart (Rule 7):")
    for vid in reg.view_ids():
        spec = ag.AggregateSpec("sum_%s" % vid, vid, ag.SUM)
        res = ag.compute(spec, ents, reg, base_version=1)
        L.append("  view %s (%s):" % (vid, reg.get(vid).view_name))
        for g in res.groups:
            L.append("    %-10s joules=%s  measured=%d zero=%d unmeasured=%d"
                     % (g.label, "NOT_COMPUTABLE" if g.value is None
                        else "%.1f" % g.value, g.n_measured, g.n_measured_zero,
                        g.n_absent))

    L.append("")
    L.append("vintages retained; a revision does not overwrite (Rule 4):")
    store = es.EntryStore()
    store.write(mk("a", 100.0, release="2026-01-10"))
    store.write(mk("a", 118.0, release="2026-03-10"))
    L.append("  entry a, versions: %s"
             % [(v.release_date, v.joules_in) for v in store.versions("a", "2026")])
    L.append("  as of 2026-02-01: joules=%s (the vintage live then)"
             % store.as_of("a", "2026", "2026-02-01").joules_in)
    L.append("  latest:           joules=%s" % store.latest("a", "2026").joules_in)

    L.append("")
    L.append("boundary declared always (Rule 5). two boundaries with no "
             "declared reconciliation do not sum:")
    other = B(("extraction", "transport"), (), "cradle-to-gate")
    reg2 = vw.ViewRegistry()
    reg2.add_view(vw.View("v", "one", "f", ("", ""), {"p": "g", "q": "g"}))
    mixed = [mk("p", 100.0), be.write_base_entry(
        entry_id="q", input_state=S("ore", 1.0, "kg"),
        output_state=S("metal", 1.0, "kg"), exposure=1.0,
        exposure_unit="person-hours", joules_in=50.0, period="2026",
        observation_method="meter", provenance="constructed",
        status=be.MEASURED, boundary=other, release_date="2026-01-10")]
    try:
        ag.compute(ag.AggregateSpec("s", "v", ag.SUM), mixed, reg2, 1)
        L.append("  (unexpected: the sum did not refuse)")
    except be.BoundaryMismatch:
        L.append("  gate-to-gate + cradle-to-gate -> refused (no reconciliation)")
    recon = [be.Reconciliation(GATE.key(), other.key(), 0.0, "declared equal")]
    r = ag.compute(ag.AggregateSpec("s", "v", ag.SUM), mixed, reg2, 1, recon)
    L.append("  with a declared reconciliation -> sums to %.1f"
             % r.by_label()["g"].value)

    L.append("")
    L.append("bisection as a structure test (Rule / diagnostic). the span is "
             "a methodology registry, not calendar time:")
    span = ["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8"]
    v = bs.locate(span, lambda sub: "m5" in sub)
    L.append("  one change carries the signal -> %s, address=%s"
             % (v.structure, bs.address(v)))
    v2 = bs.structure_verdict(span, lambda sub: "m2" in sub or "m7" in sub)
    L.append("  signal on both halves          -> %s (no address reported)"
             % v2.structure)

    return "\n".join(L)


def main(argv):
    text = render()
    clean, h = no_severity.check(text)
    if not clean:
        sys.stderr.write("no_severity screen FAILED on the demo:\n")
        for lineno, word, line in h:
            sys.stderr.write("  line %d: %r in %r\n" % (lineno, word, line))
        return 1
    if "--write" in argv:
        out = os.path.join(HERE, "samples", "mrf_demo.sample.txt")
        with open(out, "w") as fh:
            fh.write(text + "\n")
        sys.stderr.write("wrote %s (no_severity: clean)\n" % out)
    else:
        print(text)
        sys.stderr.write("\n(no_severity: clean)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
