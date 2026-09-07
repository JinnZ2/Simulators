"""F) branch_set.py -- serialize a held branch set so it survives transport
to a model or a reader. Collapse happens at MEASUREMENT, not at intake: a
branch is eliminated by its discriminator, never by being unfashionable.

branches.jsonl, one row per branch:
  branch_id, result_id (the result it fits), origin_domain,
  generator, predicted_divergence, discriminator, cost (number),
  status            open | eliminated | survived
  suppression_cause prior | access | null
  access_kind       no_vocabulary | cross_discipline | instrument_missing   (when access)
  predicts_elsewhere[]  {domain (must differ from origin_domain), already_in_record y|n|unknown}
  instrument_history?   {phenomenon_before, made_readable, discipline_crossed,
                         question_askable_date, instrument_built_date}
                        lag = built - askable (years). A long lag marks ACCESS
                        suppression, not difficulty: when lag >= --lag-years
                        (default 20, printed) and suppression_cause is not
                        access, the row is flagged, never rewritten.
Outputs:
  queue        open branches ranked by priority DESC then cost ASC, where
               priority = number of open branches fitting the same result_id
               (N generators fitting one result RAISES priority) -- the
               cheapest discriminator runs first, not the most central one
  eliminated   every eliminated branch with the discriminator that did it;
               each elimination is a result
  gaps         predicts_elsewhere entries with already_in_record unknown,
               crossed with the branch's suppression, each triaged by rule:
                 answerable_now   already_in_record = y  (go read the record)
                 buildable        access_kind = instrument_missing
                 simulable        suppression_cause = prior (a prior is testable
                                  by simulation; no access is missing)
                 blocked(+blocker) access_kind = no_vocabulary | cross_discipline
Command: python3 branch_set.py BRANCHES.jsonl [--lag-years 20] [--json]
         python3 branch_set.py --new > BRANCHES.jsonl
         python3 branch_set.py --selftest
"""
import json
import sys

STATUS = ("open", "eliminated", "survived")
SUPPRESSION = ("prior", "access", None)
ACCESS = ("no_vocabulary", "cross_discipline", "instrument_missing")
RECORD = ("y", "n", "unknown")
FIELDS = ("branch_id", "result_id", "origin_domain", "generator", "predicted_divergence", "discriminator", "cost",
          "status", "suppression_cause", "predicts_elsewhere")
SKELETON = {"branch_id": "", "result_id": "", "origin_domain": "", "generator": "", "predicted_divergence": "",
            "discriminator": "", "cost": 0, "status": "open", "suppression_cause": None, "access_kind": None,
            "predicts_elsewhere": [{"domain": "", "already_in_record": "unknown"}],
            "instrument_history": {"phenomenon_before": "", "made_readable": "", "discipline_crossed": "",
                                   "question_askable_date": "", "instrument_built_date": ""}}


def year(s):
    try:
        return int(str(s)[:4])
    except (TypeError, ValueError):
        return None


def validate(rows):
    probs, ids = [], set()
    for k, r in enumerate(rows, 1):
        w = "row %d" % k
        for f in FIELDS:
            if f not in r:
                probs.append("%s: missing %s" % (w, f))
        if probs and probs[-1].startswith(w):
            continue
        if r["branch_id"] in ids:
            probs.append("%s: duplicate branch_id" % w)
        ids.add(r["branch_id"])
        if r["status"] not in STATUS:
            probs.append("%s: status must be one of %s" % (w, STATUS))
        if r["suppression_cause"] not in SUPPRESSION:
            probs.append("%s: suppression_cause must be prior|access|null" % w)
        if r["suppression_cause"] == "access" and r.get("access_kind") not in ACCESS:
            probs.append("%s: access suppression requires access_kind in %s" % (w, ACCESS))
        if not isinstance(r["cost"], (int, float)) or isinstance(r["cost"], bool) or r["cost"] < 0:
            probs.append("%s: cost must be a number >= 0" % w)
        for j, p in enumerate(r["predicts_elsewhere"]):
            if p.get("domain") == r["origin_domain"]:
                probs.append("%s: predicts_elsewhere[%d] domain equals origin_domain" % (w, j))
            if p.get("already_in_record") not in RECORD:
                probs.append("%s: predicts_elsewhere[%d] already_in_record must be y|n|unknown" % (w, j))
        if r["status"] == "eliminated" and not str(r["discriminator"]).strip():
            probs.append("%s: an eliminated branch must name the discriminator that eliminated it" % w)
    if probs:
        raise ValueError("\n".join(probs))
    return rows


def lag(r):
    h = r.get("instrument_history") or {}
    a, b = year(h.get("question_askable_date")), year(h.get("instrument_built_date"))
    return (b - a) if (a is not None and b is not None) else None


def triage(r, p):
    if p["already_in_record"] == "y":
        return "answerable_now"
    if r["suppression_cause"] == "access":
        if r["access_kind"] == "instrument_missing":
            return "buildable"
        return "blocked(%s)" % r["access_kind"]
    if r["suppression_cause"] == "prior":
        return "simulable"
    return "blocked(no suppression stated; nothing names what would settle it)"


def analyse(rows, lag_years=20):
    validate(rows)
    open_ = [r for r in rows if r["status"] == "open"]
    fit = {}
    for r in open_:
        fit[r["result_id"]] = fit.get(r["result_id"], 0) + 1
    queue = sorted(open_, key=lambda r: (-fit[r["result_id"]], r["cost"], r["branch_id"]))
    queue = [{"branch_id": r["branch_id"], "result_id": r["result_id"], "priority": fit[r["result_id"]], "cost": r["cost"],
              "discriminator": r["discriminator"]} for r in queue]
    elim = [{"branch_id": r["branch_id"], "result_id": r["result_id"], "eliminated_by": r["discriminator"],
             "predicted_divergence": r["predicted_divergence"]} for r in rows if r["status"] == "eliminated"]
    gaps, flags = [], []
    for r in rows:
        lg = lag(r)
        if lg is not None and lg >= lag_years and r["suppression_cause"] != "access":
            flags.append({"branch_id": r["branch_id"], "lag_years": lg,
                          "note": "lag >= %d years marks ACCESS suppression; row states %r" % (lag_years, r["suppression_cause"])})
        for p in r["predicts_elsewhere"]:
            if p["already_in_record"] != "n":
                gaps.append({"branch_id": r["branch_id"], "domain": p["domain"], "already_in_record": p["already_in_record"],
                             "suppression_cause": r["suppression_cause"], "access_kind": r.get("access_kind"),
                             "lag_years": lg, "triage": triage(r, p)})
    return {"n_branches": len(rows), "by_status": {s: sum(1 for r in rows if r["status"] == s) for s in STATUS},
            "lag_years_threshold": lag_years, "queue": queue, "eliminated": elim, "gaps": gaps, "lag_flags": flags,
            "intake_rule": "N generators fitting one result raises priority; cheapest discriminator first; each elimination is a result"}


def render(a):
    L = ["branches %d  %s  lag threshold %d y" % (a["n_branches"], a["by_status"], a["lag_years_threshold"]), "QUEUE (priority desc, cost asc):"]
    L += ["  %-14s result %-10s priority %d cost %-6s %s" % (q["branch_id"], q["result_id"], q["priority"], q["cost"], q["discriminator"]) for q in a["queue"]]
    L += ["ELIMINATED:"] + ["  %-14s by: %s" % (e["branch_id"], e["eliminated_by"]) for e in a["eliminated"]]
    L += ["GAPS (predicts elsewhere, record unknown or y):"]
    L += ["  %-14s -> %-14s record=%s  %s" % (g["branch_id"], g["domain"], g["already_in_record"], g["triage"]) for g in a["gaps"]]
    L += ["LAG FLAGS:"] + ["  %s: %s" % (f["branch_id"], f["note"]) for f in a["lag_flags"]]
    return "\n".join(L)


def fixture():
    def b(i, res, cost, status="open", sup=None, ak=None, pe=None, hist=None):
        return {"branch_id": i, "result_id": res, "origin_domain": "recsys", "generator": "gen " + i, "predicted_divergence": "div " + i,
                "discriminator": "disc " + i, "cost": cost, "status": status, "suppression_cause": sup, "access_kind": ak,
                "predicts_elsewhere": pe or [], "instrument_history": hist}
    return [b("g_model", "R1", 5.0),
            b("h_catalog", "R1", 1.0, sup="prior", pe=[{"domain": "survey_methodology", "already_in_record": "unknown"}]),
            b("m_matcher", "R1", 0.5, sup="access", ak="no_vocabulary", pe=[{"domain": "metrology", "already_in_record": "y"}]),
            b("contract", "R1", 2.0, status="eliminated", sup="access", ak="instrument_missing",
              pe=[{"domain": "form_design", "already_in_record": "unknown"}],
              hist={"question_askable_date": "1990", "instrument_built_date": "2026"}),
            b("lone", "R2", 0.1, sup="prior", hist={"question_askable_date": "2000", "instrument_built_date": "2030"})]


def selftest():
    a = analyse(fixture())
    ids = [q["branch_id"] for q in a["queue"]]
    assert ids == ["m_matcher", "h_catalog", "g_model", "lone"], ids   # R1 has 3 open fits: priority 3, cheapest first
    assert a["eliminated"][0]["eliminated_by"] == "disc contract"
    tri = {g["branch_id"]: g["triage"] for g in a["gaps"]}
    assert tri == {"h_catalog": "simulable", "m_matcher": "answerable_now", "contract": "buildable"}, tri
    assert [f["branch_id"] for f in a["lag_flags"]] == ["lone"]           # 30-year lag, cause stated prior -> flagged
    bad = fixture(); bad[0]["predicts_elsewhere"] = [{"domain": "recsys", "already_in_record": "n"}]
    try:
        analyse(bad); raise AssertionError("same-domain prediction accepted")
    except ValueError:
        pass
    bad = fixture(); bad[3]["discriminator"] = ""
    try:
        analyse(bad); raise AssertionError("elimination without discriminator accepted")
    except ValueError:
        pass
    print("branch_set selftest: 6 checks OK")


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if argv == ["--new"]:
        print(json.dumps(SKELETON, sort_keys=True)); return 0
    if not argv or "--help" in argv:
        print(__doc__); return 2
    with open(argv[0], encoding="utf-8") as fh:
        rows = [json.loads(ln) for ln in fh if ln.strip()]
    ly = int(argv[argv.index("--lag-years") + 1]) if "--lag-years" in argv else 20
    a = analyse(rows, ly)
    print(json.dumps(a, indent=1, sort_keys=True) if "--json" in argv else render(a))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
