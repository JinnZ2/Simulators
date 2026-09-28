# SPDX-License-Identifier: CC0-1.0
"""tax_step.py -- FWO-13. The tax step registered as a named conversion point
with its OWN row type, beside (never inside) the FWO-6 register.

    python3 tax_step.py              the rows, the consequence, the prior-art block, the FWO-6 cross-reference
    python3 tax_step.py --choices    every [CHOICE n] in force
    python3 test_single_channel.py   the checks; this module refuses --selftest

ROW TYPE  tax_step  {id, route, converts_how, provenance, status, source}
    provenance  OBSERVED / DERIVED / PROPOSED (the order's key)
    status      REGISTERED needs provenance OBSERVED or a VERIFIED source; PROPOSED can
                only be CANDIDATE; the constructor refuses REGISTERED on a PROPOSED row
                (that refusal is the fail fixture)
    an FWO-6-shaped record (one carrying `reconversions`) is refused here: the tax step
    is not an entry in that register, it is a step every entry can pass through, and
    load_register() still reads the FWO-6 file unchanged for the cross-reference

APPEARANCE 3 (volunteer or unpaid repair) is PROPOSED in the order with "verify or drop".
    Neither is possible here: the fringe-benefit and gift rules are not reachable
    (egress allowlist).  The memory reading -- the value of services a volunteer gives
    is not income to the volunteer, and a recipient of free services generally has no
    reportable income either -- would DROP it, and a memory reading is not a
    verification.  It stays CANDIDATE with the memory reading carried as unverified.

Stdlib only. Parses under Python 3.8. No network. CC0.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import dependency_chain_audit as D  # noqa: E402  FWO-6 register loader, reused

TAX_STEP = "tax_step"
PROVENANCE = ("OBSERVED", "DERIVED", "PROPOSED")
STATUSES = ("REGISTERED", "CANDIDATE")
REGISTER_PATH = os.path.join(HERE, "tax_step_register.json")

CHOICES = {
    1: "REGISTERED requires OBSERVED provenance or a source starting VERIFIED; PROPOSED rows are CANDIDATE only",
    2: "appearance 3 stays CANDIDATE: neither verified nor dropped, the memory reading carried unverified",
    3: "the cross-reference counts FWO-6 entries with a tax mechanism; it adds no row to either register",
}


class TaxRowError(ValueError):
    pass


def tax_row(rid, route, converts_how, provenance, status, source, memory_reading=""):
    if provenance not in PROVENANCE:
        raise TaxRowError("%s: provenance is one of %s" % (rid, PROVENANCE))
    if status not in STATUSES:
        raise TaxRowError("%s: status is one of %s" % (rid, STATUSES))
    if status == "REGISTERED" and not (provenance == "OBSERVED" or source.startswith("VERIFIED")):
        raise TaxRowError("%s: REGISTERED requires OBSERVED provenance or a VERIFIED source; got %s / %s [CHOICE 1]"
                          % (rid, provenance, source.split(":")[0]))
    if not isinstance(source, str) or not source:
        raise TaxRowError("%s: source is required" % rid)
    return {"type": TAX_STEP, "id": rid, "route": route, "converts_how": converts_how,
            "provenance": provenance, "status": status, "source": source, "memory_reading": memory_reading}


def refuse_fwo6_shape(record):
    if "reconversions" in record or "changed" in record:
        raise TaxRowError("an FWO-6 entry shape is refused here: the tax step is its own row type, not a register entry")
    if record.get("type") != TAX_STEP:
        raise TaxRowError("type must be %r" % TAX_STEP)
    return record


def seed_rows():
    o = "CARRIED: the order's table row, OBSERVED there (a report from operation)"
    return [
        tax_row("barter_for_materials", "barter for materials",
                "taxable event; settlement requires money", "OBSERVED", "REGISTERED", o),
        tax_row("non_monetary_recognition", "non-monetary recognition (gift, meal, gift card)",
                "assigned dollar value, reported as compensation, employer pays to give it",
                "OBSERVED", "REGISTERED", o),
        tax_row("volunteer_unpaid_repair", "volunteer or unpaid repair", "candidate only",
                "PROPOSED", "CANDIDATE",
                "CARRIED: the order's table row, PROPOSED there with 'verify or drop'; neither done (egress)",
                memory_reading="UNVERIFIED: the value of a volunteer's services is not income to the volunteer, and a "
                               "recipient of free services generally has no reportable income; if that holds, the "
                               "route does not convert at the tax step and the row is dropped [CHOICE 2]"),
    ]


CONSEQUENCE = ("OBSERVED (carried, the operator's): the cheapest permitted recognition channel is the paycheck. "
               "People reachable only through other channels go flat or leave. The remaining population then "
               "confirms that money is what motivates people. Self-validating; the same shape as the melds in "
               "meld-as-error-class (named there; not in this tree).")

PRIOR_ART = {
    "status": "NOT_RUN (egress allowlist); entries CARRIED_FROM_MEMORY, unverified",
    "entries": [
        {"what": "de minimis fringe-benefit exclusion (small, infrequent, hard-to-account-for items excluded from wages)",
         "constrains": "non-monetary recognition: an item above the de minimis line is wages",
         "framed_as": "compliance"},
        {"what": "cash and cash-equivalents (gift cards) never de minimis, whatever the amount",
         "constrains": "the gift card in appearance 2",
         "framed_as": "compliance"},
        {"what": "anyone treating these rules as CHANNEL REMOVAL rather than compliance",
         "constrains": "NONE RECALLED", "framed_as": "unbounded null: no corpus searched"},
    ],
}


def write_register(path=REGISTER_PATH):
    data = {"_what": "FWO-13 tax-step register: the tax step as a named conversion point with its own row type",
            "_row_type": TAX_STEP,
            "_fields": "id; route; converts_how; provenance in OBSERVED/DERIVED/PROPOSED; status in REGISTERED/CANDIDATE; "
                       "source; memory_reading (UNVERIFIED where present)",
            "consequence": CONSEQUENCE, "prior_art": PRIOR_ART, "rows": seed_rows()}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    return data


def load(path=REGISTER_PATH):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return [refuse_fwo6_shape(r) for r in data["rows"]]


def fwo6_cross_reference():
    """FWO-6 entries whose reconversions carry a tax mechanism.  [CHOICE 3]"""
    entries = D.load_register()
    hits = [e["id"] for e in entries if any(rc["mechanism"] == "tax" for rc in e["reconversions"])]
    return {"fwo6_entries": len(entries), "with_tax_mechanism": hits}


def fail_fixture():
    """CONSTRUCTED: a PROPOSED row asking to be REGISTERED; the constructor refuses it."""
    return dict(rid="z_fail", route="fixture", converts_how="fixture", provenance="PROPOSED",
                status="REGISTERED", source="CONSTRUCTED: fail fixture")


def check_expectations(rows):
    by = dict((r["id"], r) for r in rows)
    v = ("volunteer_unpaid_repair" in by and by["volunteer_unpaid_repair"]["status"] == "CANDIDATE"
         and sum(1 for r in rows if r["status"] == "REGISTERED") == 2)
    return [("E13.1 appearances 1 and 2 REGISTERED; appearance 3 CANDIDATE", "MATCH" if v else "MISMATCH")]


def render(out=None):
    out = out or sys.stdout
    w = out.write
    rows = seed_rows()
    w("tax_step -- FWO-13; the tax step as its own conversion-point row type\n\n")
    for r in rows:
        w("== %s  [%s / %s]\n   route: %s\n   converts: %s\n   source: %s\n" % (
            r["id"], r["provenance"], r["status"], r["route"], r["converts_how"], r["source"]))
        if r["memory_reading"]:
            w("   memory reading: %s\n" % r["memory_reading"])
    w("\nconsequence: %s\n" % CONSEQUENCE)
    w("\nprior art (fringe-benefit / de minimis as a constraint on non-monetary recognition): %s\n" % PRIOR_ART["status"])
    for e in PRIOR_ART["entries"]:
        w("   %s\n      constrains: %s\n      framed as:  %s\n" % (e["what"], e["constrains"], e["framed_as"]))
    x = fwo6_cross_reference()
    w("\nFWO-6 cross-reference: %d entries, tax mechanism on %s\n" % (x["fwo6_entries"], x["with_tax_mechanism"]))
    for l, v in check_expectations(rows):
        w("expected %-64s %s\n" % (l, v))
    try:
        tax_row(**fail_fixture())
        w("fail fixture (CONSTRUCTED, PROPOSED asking REGISTERED): NOT REFUSED\n")
    except TaxRowError as e:
        w("fail fixture (CONSTRUCTED, PROPOSED asking REGISTERED): refused -- %s\n" % e)
    w("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_single_channel.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    if "--write" in argv:
        write_register()
        print("wrote %s" % REGISTER_PATH)
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
