#!/usr/bin/env python3
"""run_all.py -- §6: run residual.py over the fixture set. The fixtures
are OUR format (falsifier records), constructed from this repo's own
claim shapes -- no registrar data is fabricated. Each fixture is round
tripped through every registrar.

Real registrars are NOT-IMPLEMENTED (spec unfetched, egress refused), so
their verdict is NO-MERGE with an egress breaks_at -- a valid, reportable
outcome (§0), not a failure. The mock registrars exercise the residual
machinery so the classifier is shown to fire on each class. Stdlib only,
parses under 3.9.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import registrars as RG            # noqa: E402
import residual as R              # noqa: E402

# ---- OUR-format fixtures (constructed; not registrar data) ----------------
FIXTURES = [
    {
        "claim": "the RATES reading reproduces the polar-only CH4 emissions",
        "falsifier": "any reading as times that reproduces 163 Tg/yr",
        "measured_as": {"quantity": "tropics source", "units_with_cut": "Tg/yr; within 0.5 of 163",
                        "how_obtained": "forward four-box steady state"},
    },
    {
        "claim": "SCOPE-DIFFERENT requires a transform, not units",
        "falsifier": "a reading under which SCOPE-DIFFERENT needs neither units nor a transform",
        "scope_transform": {"reference": "the drawn accounting boundary",
                            "maps_to": "the same term in another substrate",
                            "breaks_at": "where an out-of-boundary dependency is load-bearing"},
        "branch_record": {"rule_as_stated": "MEASURED needs units",
                          "forcing_case": "a scope note with no transform",
                          "axis": "units vs transform",
                          "derivation": "frame information is not in the quantity's units",
                          "frame_note": "rescope, not narrow"},
    },
]


def real_registrar_report():
    """Every real registrar: NO-MERGE with the egress breaks_at, spec
    unfetched -- a valid reportable outcome, marked UNVERIFIED."""
    rows = []
    for name, reg in RG.REGISTRARS.items():
        v = R.verdict(name, merge=False, breaks_at=reg.reason)
        rows.append({"registrar": name, "verified": reg.verified, "verdict": v["verdict"],
                     "breaks_at": v["breaks_at"], "spec_url": reg.spec_url})
    return rows


def mock_round_trips():
    """The machinery, exercised on the fixtures through the declared test
    doubles -- one per residual class."""
    mocks = [RG.identity_registrar(), RG.drops_branch_registrar(),
             RG.coerces_falsifier_registrar(), RG.flattens_measured_registrar(),
             RG.requires_id_registrar(with_origin=True)]
    out = []
    for fx in FIXTURES:
        for reg in mocks:
            rt = R.round_trip_out_in(fx, reg)
            out.append({"fixture": fx["claim"][:40], "registrar": reg.name,
                        "classes": R.residual_by_class(rt["residual"]),
                        "residual": rt["residual"]})
    return out


def render():
    L = ["merge-path: round trip over the fixture set (residual = a field list, not a score)",
         "",
         "REAL registrars -- spec unfetched (egress 403 CONNECT), UNVERIFIED, NO-MERGE:"]
    for row in real_registrar_report():
        L.append("  %-20s verified=%s  %s" % (row["registrar"], row["verified"], row["verdict"]))
        L.append("    breaks_at: %s" % row["breaks_at"])
    L.append("")
    L.append("MOCK registrars -- declared test doubles, exercising the residual classes:")
    for row in mock_round_trips():
        cls = row["classes"]
        active = ", ".join("%s=%d" % (c, cls[c]) for c in R.RESIDUAL_CLASSES if cls[c])
        L.append("  %-42s %-24s [%s]" % (row["fixture"], row["registrar"], active or "lossless"))
    return "\n".join(L)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        print("run_all has no selftest; run selftest.py", file=sys.stderr)
        return 2
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main())
