#!/usr/bin/env python3
"""Run 3: agreement of the local auditor with run 2. Stdlib only. Rules: DECLARED.json.

    python3 score.py            -> records.json, and the report on stdout
    python3 score.py --selftest

The key is read here and only here: run 1 records.json (rerun-based verdicts), run 2
probe_readings.json and run 2 records.json item_2. If verdicts.jsonl is absent the record
is NOT_RUN and agreement is None, not zero.
"""
import collections
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R1 = os.path.dirname(HERE)
R2 = os.path.join(R1, "run_2")


def J(p):
    return json.load(open(p, encoding="utf-8"))


def key():
    k = {}
    for v in J(os.path.join(R1, "records.json"))["verdicts"]:
        if v["basis"] == "rerun" and v["verdict"] not in (None, "NOT_A_CLAIM"):
            k["rerun#" + v["claim_id"]] = v["verdict"]
    for p in J(os.path.join(R2, "probe_readings.json"))["readings"]:
        k["probe#" + p["claim_id"]] = p["run_2_reading"]
    for c in J(os.path.join(R2, "records.json"))["item_2"]["claims"]:
        k["pass#" + c["claim_id"]] = c["class"]
    return k


def agreement(k, verdicts, quotes):
    """k: item_id -> run 2 class (None = void). verdicts: item_id -> local record."""
    table = collections.defaultdict(lambda: {"n": 0, "agree": 0, "disagree": 0, "local_none": 0, "not_asked": 0})
    dis, conf = [], collections.Counter()
    for iid, cls in sorted(k.items()):
        kind = iid.split("#")[0]
        row = table["%s / %s" % (kind, cls)]
        row["n"] += 1
        v = verdicts.get(iid)
        if v is None:
            row["not_asked"] += 1
            continue
        conf["%s: %s -> %s" % (kind, cls, v["class"])] += 1
        if v["class"] is None and cls is not None:
            row["local_none"] += 1
        elif v["class"] == cls:
            row["agree"] += 1
        else:
            row["disagree"] += 1
            dis.append({"item_id": iid, "run_2_class": cls, "local_class": v["class"], "local_reason": v.get("reason"), "quote": quotes.get(iid), "agency": None})
    for row in table.values():
        d = row["agree"] + row["disagree"]
        row["rate"] = round(row["agree"] / d, 4) if d else None       # None: nothing compared in this class
        row["rate_n"] = d
    tot = {f: sum(r[f] for r in table.values()) for f in ("n", "agree", "disagree", "local_none", "not_asked")}
    d = tot["agree"] + tot["disagree"]
    tot["rate"], tot["rate_n"] = (round(tot["agree"] / d, 4) if d else None), d
    return dict(table), tot, dis, dict(conf)


def build():
    packet = J(os.path.join(HERE, "packet.json"))
    quotes = {i["item_id"]: i["quote"] for i in packet["items"]}
    k = key()
    assert set(k) == set(quotes), "packet and key do not cover the same items"
    rec = {"record": "MODEL_OUTPUT_AUDIT_RUN_3_LOCAL", "status": "PROPOSED", "license": "CC0", "co_authored": True, "observer_slots": None,
           "items": len(k), "agency": None}
    vp = os.path.join(HERE, "verdicts.jsonl")
    if not os.path.exists(vp):
        rec.update(state="NOT_RUN", reason="verdicts.jsonl is absent: the local auditor has not been run. This kit was filed by the session that wrote run 2, "
                   "which is not the independent auditor and wrote no verdict.", auditor=None, agreement_with_run_2=None, per_class=None,
                   disagreements=None, fidelity=None)
        return rec
    verdicts = {}
    for l in open(vp, encoding="utf-8"):
        if l.strip():
            v = json.loads(l)
            verdicts[v["item_id"]] = v
    aud = J(os.path.join(HERE, "auditor.json"))
    table, tot, dis, conf = agreement(k, verdicts, quotes)
    rec.update(state="RUN" if tot["not_asked"] == 0 else "PARTIAL", auditor={f: aud.get(f) for f in ("name", "digest", "details", "api", "temperature", "seed", "num_ctx", "started", "clones")},
               packet_sha256_matches=aud.get("packet_sha256") == hashlib.sha256(open(os.path.join(HERE, "packet.json"), "rb").read()).hexdigest(),
               agreement_with_run_2=tot, per_class=table, transitions=conf, disagreements=dis,
               reruns_done=sum(v.get("reruns_done", 0) for v in verdicts.values()), reruns_asked=sum(v.get("reruns_asked", 0) for v in verdicts.values()),
               note="rate = agree / (agree + disagree); local None and not-asked are counted apart and are not disagreement. "
                    "Agreement between two readers is not correctness of either.")
    fp = os.path.join(HERE, "fidelity_reads.json")
    if os.path.exists(fp):
        reads = J(fp)["reads"]
        rec["fidelity"] = {"specs_picked": len(reads), "specs_read": sum(r["state"] == "READ" for r in reads),
                           "specs": [{"repo": r["repo"], "spec_source": r["spec_source"], "state": r["state"], "why": r.get("why"),
                                      "steps_read": r.get("steps_read"), "counts": r.get("counts"),
                                      "steps_not_counted_quote_not_found": r.get("steps_not_counted_quote_not_found"),
                                      "added_constraint_counted": r.get("added_counted"), "added_not_counted_quote_not_found": r.get("added_not_counted_quote_not_found"),
                                      "run_2_reading": "MATCH (state names only)"} for r in reads]}
    else:
        rec["fidelity"] = None
    return rec


def report(rec):
    print("run 3 (local): %s" % rec["state"])
    if rec["state"] == "NOT_RUN":
        print(rec["reason"])
        print("agreement with run 2: None (void)")
        return
    a = rec["auditor"]
    print("auditor: %s %s" % (a["name"], a.get("digest") or "(digest not reported)"))
    t = rec["agreement_with_run_2"]
    print("agreement with run 2: %s  (agree %d of %d compared; local None %d; not asked %d; items %d)" % (t["rate"], t["agree"], t["rate_n"], t["local_none"], t["not_asked"], t["n"]))
    print("%-28s %4s %6s %9s %5s %10s %6s" % ("kind / run 2 class", "n", "agree", "disagree", "None", "not asked", "rate"))
    for name, r in sorted(rec["per_class"].items()):
        print("%-28s %4d %6d %9d %5d %10d %6s" % (name, r["n"], r["agree"], r["disagree"], r["local_none"], r["not_asked"], r["rate"]))
    print("disagreements: %d" % len(rec["disagreements"]))
    for d in rec["disagreements"]:
        print("- %s\n  run 2: %s   local: %s   (%s)\n  quote: %s" % (d["item_id"], d["run_2_class"], d["local_class"], d["local_reason"], d["quote"]))
    if rec["fidelity"]:
        for s in rec["fidelity"]["specs"]:
            print("fidelity %s/%s: %s %s added=%s not counted (quote not found): steps %s, added %s" % (
                s["repo"], s["spec_source"], s["state"], s["counts"], s["added_constraint_counted"], s["steps_not_counted_quote_not_found"], s["added_not_counted_quote_not_found"]))
    print("Observer slots: null")


def selftest():
    fails = []

    def ok(name, cond):
        print(("PASS  " if cond else "FAIL  ") + name)
        if not cond:
            fails.append(name)
    k = {"rerun#a": "CONFIRMED", "rerun#b": "CONFIRMED", "probe#c": "DECLARED_LIMIT", "pass#d": None, "pass#e": "STALE"}
    v = {"rerun#a": {"class": "CONFIRMED"}, "rerun#b": {"class": None}, "probe#c": {"class": "NOT_A_CLAIM", "reason": "r"}, "pass#d": {"class": None}}
    table, tot, dis, conf = agreement(k, v, {"probe#c": "q"})
    ok("agree counted", tot["agree"] == 2)                       # a, and d (both void)
    ok("local None is not a disagreement", table["rerun / CONFIRMED"]["local_none"] == 1 and table["rerun / CONFIRMED"]["disagree"] == 0)
    ok("a disagreement carries its quote", dis == [{"item_id": "probe#c", "run_2_class": "DECLARED_LIMIT", "local_class": "NOT_A_CLAIM", "local_reason": "r", "quote": "q", "agency": None}])
    ok("an item never asked is counted apart", tot["not_asked"] == 1 and table["pass / STALE"]["rate"] is None)
    ok("rate prints its n", tot["rate"] == round(2 / 3, 4) and tot["rate_n"] == 3)
    t2, tot2, _, _ = agreement(k, {}, {})
    ok("no verdicts: rate is None, not zero", tot2["rate"] is None and tot2["rate_n"] == 0)
    kk = key()
    ok("the key covers 135 items", len(kk) == 135 and collections.Counter(i.split("#")[0] for i in kk) == {"rerun": 26, "probe": 101, "pass": 8})
    ok("the packet shows no key class beside a quote", all(set(i) == {"item_id", "claim_id", "kind", "repo", "clone_url", "quote", "location", "claim_type", "runs", "hosts"}
                                                         for i in J(os.path.join(HERE, "packet.json"))["items"]))
    print("checks: %d   failed: %d" % (8, len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    rec = build()
    json.dump(rec, open(os.path.join(HERE, "records.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    report(rec)
