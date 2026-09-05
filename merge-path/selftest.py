#!/usr/bin/env python3
"""selftest.py -- §6 S1..S5 for the merge-path machinery, plus null tests
both directions and the egress/UNVERIFIED invariants. Known answers on
constructed data; no registrar spec is fetched or fabricated.

    python3 merge-path/selftest.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import registrars as RG            # noqa: E402
import residual as R              # noqa: E402
import convert_out as CO          # noqa: E402
import convert_in as CI           # noqa: E402
import run_all as RA              # noqa: E402
import report as RP               # noqa: E402
import no_severity                # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


RECORD = {
    "claim": "a claim",
    "falsifier": "what would refute it",
    "measured_as": {"quantity": "q", "units_with_cut": "u; cut at 3", "how_obtained": "h"},
    "branch_record": {"rule_as_stated": "r", "forcing_case": "f", "axis": "a",
                      "derivation": "d", "frame_note": "n"},
}


def main():
    print("selftest (merge-path)")
    for f in ("residual.py", "convert_out.py", "convert_in.py", "run_all.py", "report.py"):
        rc = __import__("subprocess").run([sys.executable, os.path.join(HERE, f), "--selftest"],
                                          capture_output=True).returncode
        check("%s refuses --selftest with rc 2" % f, rc == 2)

    # ---- S1: identity round trip within our own format is lossless
    ident = RG.identity_registrar()
    rt = R.round_trip_out_in(RECORD, ident)
    check("S1: identity round trip is lossless (recovered == original, empty residual)",
          rt["recovered"] == RECORD and rt["residual"] == [] and rt["diff"] == [])

    # ---- S2: an unmappable field produces a DROPPED entry, not a silent pass
    drops = RG.drops_branch_registrar()
    rt2 = R.round_trip_out_in(RECORD, drops)
    dropped = [e for e in rt2["residual"] if e["class"] == "DROPPED" and e["field"] == "branch_record"]
    check("S2: the unmappable branch_record is reported DROPPED, not silently lost",
          dropped and "branch_record" not in rt2["recovered"]
          and any(d["field"] == "branch_record" and d["class"] == "DROPPED" for d in rt2["diff"]))

    # ---- S3: a COERCED mapping is detected (source field into a slot of different meaning)
    coerce = RG.coerces_falsifier_registrar()
    rt3 = R.round_trip_out_in(RECORD, coerce)
    check("S3: writing the falsifier into a different-meaning slot is flagged COERCED",
          any(e["class"] == "COERCED" and e["field"] == "falsifier" for e in rt3["residual"]))
    check("COERCED and ADDED are the silent-wrongness classes, always counted (visible as a zero)",
          set(R.SILENT_WRONGNESS) == {"COERCED", "ADDED"}
          and all(c in R.residual_by_class([]) for c in R.RESIDUAL_CLASSES))

    # ---- S4: an ADDED field carries a stated origin; none is a hard failure
    ok_add = RG.requires_id_registrar(with_origin=True)
    tgt, res = CO.convert_out(RECORD, ok_add)
    added = [e for e in res if e["class"] == "ADDED" and e["field"] == "registration_id"]
    check("S4: an ADDED field with a stated origin converts and names its origin", added and added[0]["origin"])
    bad_add = RG.requires_id_registrar(with_origin=False)
    raised = False
    try:
        CO.convert_out(RECORD, bad_add)
    except RG.ConversionFailure:
        raised = True
    check("S4: an ADDED field with no origin is a hard failure (ConversionFailure)", raised)

    # ---- S5: a NO-MERGE verdict carries a breaks_at; one without is a hard failure
    v = R.verdict("some_registrar", merge=False, breaks_at="the spec was not fetched")
    check("S5: a NO-MERGE with a breaks_at is valid", v["verdict"] == "NO-MERGE" and v["breaks_at"])
    raised5 = False
    try:
        R.verdict("some_registrar", merge=False, breaks_at="")
    except RG.VerdictError:
        raised5 = True
    check("S5: a NO-MERGE with no breaks_at is a hard failure (VerdictError)", raised5)

    # ---- null test both directions: FLATTENED and the IN direction
    flat = RG.flattens_measured_registrar()
    tf, rf = CO.convert_out(RECORD, flat)
    check("FLATTENED fires when a dict is collapsed to a string slot",
          any(e["class"] == "FLATTENED" and e["field"] == "measured_as" for e in rf)
          and isinstance(tf["measure_text"], str))
    # IN direction on a registrar-native field with no falsifier home -> DROPPED
    rec_in, res_in = CI.convert_in({"claim": "c", "provenance_graph": "<rdf>"}, ident)
    check("IN direction: a registrar-native field with no falsifier slot is DROPPED",
          any(e["class"] == "DROPPED" and e["field"] == "provenance_graph" for e in res_in))

    # ---- egress / UNVERIFIED invariants: every real registrar is unfetched and NOT-IMPLEMENTED
    check("every real registrar is UNVERIFIED (spec unfetched) and NOT-IMPLEMENTED",
          all((not reg.verified and not reg.implemented and reg.reason) for reg in RG.REGISTRARS.values()))
    ni, nires = CO.convert_out(RECORD, RG.REGISTRARS["nanopublications"])
    check("a real registrar's convert_out returns NOT-IMPLEMENTED with the egress reason, not a guess",
          ni.get("status") == "NOT-IMPLEMENTED" and nires[0]["class"] == "NOT-IMPLEMENTED" and "403" in nires[0]["detail"])
    check("every real registrar's NO-MERGE verdict carries the egress breaks_at",
          all(row["verdict"] == "NO-MERGE" and row["breaks_at"] for row in RA.real_registrar_report()))
    check("no mock is presented as a real registrar (is_mock set on every test double)",
          RG.identity_registrar().is_mock and RG.coerces_falsifier_registrar().is_mock
          and all(not reg.is_mock for reg in RG.REGISTRARS.values()))

    # ---- renders screen clean
    out = RA.render()
    rep = RP.merge_report()
    check("run_all render screens clean", not no_severity.hits(out))
    check("report render screens clean", not no_severity.hits(rep))
    check("screen fires on a planted word", bool(no_severity.hits(rep + "\nthis is wrong\n")))

    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    with open(os.path.join(HERE, "samples", "run_all.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out + "\n")
    RP.main(["--write"])
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
