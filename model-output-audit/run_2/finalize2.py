#!/usr/bin/env python3
"""Run 2 records. Stdlib only.   python3 finalize2.py   -> records.json"""
import collections
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = ("WORK_ORDER.md", "DECLARED.json", "model_probe.json", "pass_claims_runs.json", "repeat_reruns.json",
         "probe_readings.json", "tightened.json", "fidelity_candidates.json", "fidelity_readings.json")
ENV_STATES = ("ENV_ERROR",)


def J(n):
    return json.load(open(os.path.join(HERE, n), encoding="utf-8"))


def classify(rec):
    c = rec["cells"]
    if not c:
        return None, "void: " + rec["reading"]
    w, h = [c["writing_commit/bare"]["state"], c["writing_commit/current"]["state"]], [c["head/bare"]["state"], c["head/current"]["state"]]
    tails = " ".join(v["tail"] for v in c.values())
    if w == ["PASS", "PASS"] and "PASS" not in h:
        return "STALE", "passes at the writing commit in both environments, fails at HEAD in both: true when written, not true of the tree now"
    if w[0] != w[1] or any(s in ENV_STATES for s in w) or "No module named" in tails:
        return "ENV_DEPENDENT", "the result turns on installed packages: %s at the writing commit (bare / current); the failing test reports a missing module" % " / ".join(w)
    if w == ["FAILS", "FAILS"]:
        return "OVERCLAIM", "fails at the writing commit in both environments for a reason that is not the environment"
    return None, "void: the runs do not settle it"


def build():
    pc = []
    for r in J("pass_claims_runs.json"):
        cl, why = classify(r)
        pc.append({"claim_id": r["claim_id"], "quote": r["quote"], "reading": r["reading"], "class": cl, "reason": why,
                   "cells": {k: {"state": v["state"], "exit": v["exit"], "rev": v["rev"]} for k, v in r["cells"].items()},
                   "auditor": "stdlib rerun (4 cells) + Anthropic model (reading of the line)", "agency": None})
    rep = J("repeat_reruns.json")
    pr = J("probe_readings.json")["readings"]
    tg = J("tightened.json")
    fc, fr = J("fidelity_candidates.json"), J("fidelity_readings.json")
    specs = []
    for s in fc["specs"]:
        read = fr["readings"].get(s["spec_source"], {})
        tested = s["tokens_in_spec"] + len(s["constants"])
        drift = [d for d in read.get("drift", [])]
        match = "DRIFT" if drift else ("MATCH" if tested else None)
        specs.append({"repo": s["repo"], "spec_source": s["spec_source"], "model": s["model"], "model_version": s["model_version"], "date": s["date"],
                      "fidelity": {"spec_source": s["spec_source"], "match": match, "drift_type": drift[0]["type"] if drift else None},
                      "items_tested": tested, "constants_tested": len(s["constants"]), "state_names_tested": s["tokens_in_spec"],
                      "absent_names_read": read.get("absent", {}), "reason": ("nothing testable: the spec writes no constant and no state name" if not tested else
                                                                             "every state name the spec writes is in the code, or its absence was read and is not a departure"),
                      "auditor": "mechanical lookup + Anthropic model (reading of each absent name)", "agency": None})

    def table(key):
        cells = collections.defaultdict(collections.Counter)
        for s in specs:
            cells[str(key(s))][str(s["fidelity"]["match"])] += 1
        return {k: {"n": c["MATCH"] + c["DRIFT"], "DRIFT": c["DRIFT"], "MATCH": c["MATCH"], "void": c["None"],
                    "drift_rate": (c["DRIFT"] / (c["MATCH"] + c["DRIFT"])) if c["MATCH"] + c["DRIFT"] else None} for k, c in sorted(cells.items())}
    r1 = json.load(open(os.path.join(os.path.dirname(HERE), "fidelity.json"), encoding="utf-8"))
    return {"record": "MODEL_OUTPUT_AUDIT_RUN_2", "date": "2026-11-27", "status": "PROPOSED", "license": "CC0", "co_authored": True, "observer_slots": None,
            "parts": {n: hashlib.sha256(open(os.path.join(HERE, n), "rb").read()).hexdigest() for n in PARTS},
            "item_1": {"independent_model_auditor": "NOT_RUN", "reason": J("model_probe.json")["reason"],
                       "agreement_between_independent_auditors": None,
                       "stdlib_second_pass": {"n": len(rep), "same_result": sum(r["same"] for r in rep),
                                              "differs": [{"claim_id": r["claim_id"], "run_1": r["run_1_rerun"], "run_2": r["run_2_rerun"]} for r in rep if not r["same"]],
                                              "what_it_is": "repeatability of one mechanical rerun, same machine, same day; not agreement between auditors"},
                       "pass_claim_side_notes_rerun": len(pc)},
            "item_2": {"counts": dict(collections.Counter(str(p["class"]) for p in pc)), "claims": pc},
            "item_3": {"read": len(pr), "run_1_to_run_2": {"%s -> %s" % k: n for k, n in sorted(collections.Counter((p["run_1_probe_verdict"], str(p["run_2_reading"])) for p in pr).items())},
                       "run_2_counts": dict(collections.Counter(str(p["run_2_reading"]) for p in pr)),
                       "by_model_version": {m: dict(c) for m, c in sorted(_group(pr).items())}},
            "item_4": {k: tg[k] for k in ("run_1_candidates", "kept", "kept_distinct_lines", "kept_by_type", "removed_by_rule", "note")},
            "item_5": {"spec_files_with_code": fc["pool"], "sampled": len(specs), "counts": dict(collections.Counter(str(s["fidelity"]["match"]) for s in specs)),
                       "constants_found_in_any_sampled_spec": sum(s["constants_tested"] for s in specs),
                       "commits_MISSING_SPEC_void_from_run_1": r1["commits"]["MISSING_SPEC_void"], "spec_files_not_sampled_void": fc["pool"] - len(specs),
                       "tables": {"model": table(lambda s: s["model"]), "model_version": table(lambda s: "%s %s" % (s["model"], s["model_version"]) if s["model"] else None),
                                  "month": table(lambda s: (s["date"] or "")[:7] or None), "topic": table(lambda s: s["spec_source"].split("/")[0])},
                       "covers": "state names only. Not tested: omitted steps, changed logic, added constraints, inverted conditions. No numeric constant was found to test.",
                       "specs": specs},
            "agency": None}


def _group(pr):
    g = collections.defaultdict(collections.Counter)
    for p in pr:
        g["%s %s" % (p["model"], p["model_version"]) if p["model"] else "None"][str(p["run_2_reading"])] += 1
    return g


if __name__ == "__main__":
    rec = build()
    json.dump(rec, open(os.path.join(HERE, "records.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for k in ("item_1", "item_2", "item_3", "item_4", "item_5"):
        v = dict(rec[k])
        for drop in ("claims", "specs", "tables", "by_model_version"):
            v.pop(drop, None)
        print(k, json.dumps(v)[:700])
    for k, c in rec["item_5"]["tables"]["model_version"].items():
        print("  %-22s n=%d drift=%d match=%d void=%d" % (k, c["n"], c["DRIFT"], c["MATCH"], c["void"]))
