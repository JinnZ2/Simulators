# SPDX-License-Identifier: CC0-1.0
"""unpaid_maintenance.py -- FWO-12. DESIGN plus prior-art check. Runs only on a
declared public dataset; none was found (none could be searched), so the
measurand is NOT_RUN and what executes here is the filter and the prediction
check on CONSTRUCTED records labelled as such.

    python3 unpaid_maintenance.py            the design, the prior-art block, the anchor, the fixtures
    python3 unpaid_maintenance.py --choices  every [CHOICE n] in force
    python3 test_single_channel.py           the checks; this module refuses --selftest

MEASURAND (OBSERVED, the operator's): fixing tools, machines or processes that are
not yours, that nobody asked you to fix, and that return nothing under the wage token.

RECORD SCHEMA a CMMS / work-order export would need to carry
    work_order_id, requester, assignee, asset_owner, planned (bool),
    in_paid_scope (bool: the work sits inside the assignee's paid duties),
    returned_under_token (bool: any pay, bonus or credit attached), source
    unpaid iff  requester != assignee != asset_owner  AND not planned
                AND not in_paid_scope AND not returned_under_token
    a record missing any of those fields is UNKNOWN and enters no share

PRIOR ART (does the discretionary-effort literature COUNT behaviour or SURVEY attitude?)
    NOT_RUN at the document level (egress allowlist).  Memory, unverified: the
    engagement instruments are questionnaires; organisational-citizenship-behaviour
    scales are supervisor- or self-rated, i.e. also questionnaires; whether a
    counted-behaviour study on unsolicited fixing exists is UNKNOWN.  The order's
    expectation (attitude by survey only) is NOT_EVALUABLE here.

MECHANISM STATEMENT (OBSERVED, energetic, not moral; carried): if the token is the
only return and effort above the token threshold returns nothing, conservation of
energy selects for effort at the threshold. The measured "disengagement" is the
correct solution to the payoff structure.
PREDICTION (PROPOSED): unpaid maintenance falls as token-coupling rises.  The
prediction check below returns FALLS / RISES / FLAT / NOT_EVALUABLE over a series
of (coupling, unpaid_share) points; fail_fixture() is a constructed series in
which it RISES, so the prediction can be shown to fail.

Stdlib only. Parses under Python 3.8. No network. CC0.
"""
import sys

FIELDS = ("work_order_id", "requester", "assignee", "asset_owner", "planned", "in_paid_scope",
          "returned_under_token", "source")
UNKNOWN = "UNKNOWN"

ANCHOR = {
    "what": "Linux kernel volunteer share and corporate-authored commit share",
    "values": "volunteer share fell from about 15% to about 6%; corporate-authored commits 84.3% in 2025",
    "source": "CARRIED: web search 2026-09-27, citations in the authoring session; not re-fetched here",
    "not_yet_split_by": "whether the employer had a stake in the subsystem -- the selection-side test (FWO-8 coupling_side)",
}

PRIOR_ART = {
    "status": "NOT_RUN (egress allowlist); memory entries unverified",
    "entries": [
        {"literature": "employee engagement instruments", "measures": "attitude, questionnaire", "counts_behaviour": False},
        {"literature": "organisational citizenship behaviour scales", "measures": "supervisor- or self-rated frequency, questionnaire",
         "counts_behaviour": False},
        {"literature": "counted unsolicited-fixing behaviour from work-order logs", "measures": "NONE RECALLED",
         "counts_behaviour": UNKNOWN},
    ],
}

CHOICES = {
    1: "unpaid requires all three parties distinct, unplanned, outside paid scope and nothing returned under the token",
    2: "a record missing any field is UNKNOWN and enters no share; the share's denominator is the classified records",
    3: "the prediction check needs at least three coupling levels and reads the sign of the endpoint difference against "
       "a declared flat band of 0.02 in share",
}


class DesignError(ValueError):
    pass


def classify(rec):
    for f in FIELDS:
        if f not in rec or rec[f] is None:
            return UNKNOWN
    distinct = len({rec["requester"], rec["assignee"], rec["asset_owner"]}) == 3
    if distinct and not rec["planned"] and not rec["in_paid_scope"] and not rec["returned_under_token"]:
        return "UNPAID"
    return "NOT_UNPAID"


def unpaid_share(records, public_source=None):
    """NOT_RUN unless a public dataset is declared; the measurand is not taken on constructed records."""
    if not public_source:
        return {"status": "NOT_RUN", "reason": "no public dataset declared; the order says run only if one is found",
                "share": None}
    cls = [classify(r) for r in records]
    n = sum(1 for c in cls if c != UNKNOWN)
    unk = sum(1 for c in cls if c == UNKNOWN)
    if n == 0:
        return {"status": "NOT_EVALUABLE", "reason": "no classified record", "share": None, "unknown": unk}
    return {"status": "RUN", "share": sum(1 for c in cls if c == "UNPAID") / float(n), "n": n, "unknown": unk,
            "public_source": public_source}


def prediction_check(series, flat_band=0.02):
    """series: [(coupling, unpaid_share)], coupling on one declared scale.  [CHOICE 3]"""
    pts = sorted((c, s) for c, s in series if c is not None and s is not None)
    if len(pts) < 3:
        return "NOT_EVALUABLE"
    delta = pts[-1][1] - pts[0][1]
    if abs(delta) <= flat_band:
        return "FLAT"
    return "FALLS" if delta < 0 else "RISES"


def demo_records():
    s = "CONSTRUCTED: design fixture; no plant, no person"
    return [
        {"work_order_id": 1, "requester": "A", "assignee": "B", "asset_owner": "C", "planned": False,
         "in_paid_scope": False, "returned_under_token": False, "source": s},
        {"work_order_id": 2, "requester": "A", "assignee": "A", "asset_owner": "C", "planned": False,
         "in_paid_scope": False, "returned_under_token": False, "source": s},
        {"work_order_id": 3, "requester": "A", "assignee": "B", "asset_owner": "C", "planned": True,
         "in_paid_scope": True, "returned_under_token": False, "source": s},
        {"work_order_id": 4, "requester": "A", "assignee": "B", "asset_owner": "C", "planned": False,
         "in_paid_scope": False, "returned_under_token": None, "source": s},
    ]


def fail_fixture():
    """CONSTRUCTED: unpaid share RISES with coupling, so the PROPOSED prediction fails on it."""
    return [(0.1, 0.05), (0.5, 0.10), (0.9, 0.20)]


def render(out=None):
    out = out or sys.stdout
    w = out.write
    w("unpaid_maintenance -- FWO-12; DESIGN plus prior-art check; measurand NOT_RUN (no public dataset)\n\n")
    w("record schema: %s\n" % ", ".join(FIELDS))
    w("classification on the CONSTRUCTED fixture: %s\n" % [classify(r) for r in demo_records()])
    r = unpaid_share(demo_records())
    w("unpaid_share on the fixture: %s -- %s\n" % (r["status"], r["reason"]))
    w("\nprior art: %s\n" % PRIOR_ART["status"])
    for e in PRIOR_ART["entries"]:
        w("   %-56s measures: %-48s counts behaviour: %s\n" % (e["literature"], e["measures"], e["counts_behaviour"]))
    w("expected E12.1 (attitude by survey only): NOT_EVALUABLE here\n")
    w("\nanchor: %s\n   %s\n   %s\n   not yet split by: %s\n" % (ANCHOR["what"], ANCHOR["values"], ANCHOR["source"],
                                                                ANCHOR["not_yet_split_by"]))
    w("\nprediction (PROPOSED): unpaid maintenance falls as token-coupling rises -- NOT_RUN\n")
    w("fail fixture (CONSTRUCTED series): prediction_check -> %s\n" % prediction_check(fail_fixture()))
    w("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_single_channel.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
