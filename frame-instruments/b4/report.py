"""B4.8 report.py -- read everything, write report.md. Nine sections, in
order, no others. If either shuffled input is missing the run is void and
no report is written: the null is a second output, never a gate, so both
print or neither does.

Command: python3 report.py --items I --requirements R --prompts DIR --grade G \
    --grade-shuffled GS --agreement A --agreement-shuffled AS [--calibration C] --out report.md
"""
import json
import os
import sys

from common import STATES, Invalid, Run, Void, count_by, finish, parse_argv, read_jsonl, usage_exit

SECTIONS = ["Item set present, by arm, with sources",
            "Reconstructor count and how they were kept separate",
            "Requirement counts and layer strings as returned",
            "Status distribution across the five states",
            "Policy-to-physical ratio per item, with unresolved",
            "Agreement, with the singleton set in full",
            "REAL vs SHUFFLED, side by side",
            "Calibration arm results, with beyond_report",
            "match_source"]


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rows:
        out.append("| " + " | ".join("" if v is None else str(v) for v in r) + " |")
    return out


def prompt_boundary(prompts_dir):
    """Re-check every prompt file: exactly one key, text_verbatim."""
    recs, files, bad = set(), 0, []
    for rid in sorted(os.listdir(prompts_dir)):
        d = os.path.join(prompts_dir, rid)
        if not os.path.isdir(d):
            continue
        recs.add(rid)
        for name in sorted(os.listdir(d)):
            files += 1
            with open(os.path.join(d, name), encoding="utf-8") as fh:
                keys = set(json.loads(fh.readline()))
            if keys != {"text_verbatim"}:
                bad.append(os.path.join(rid, name))
    return sorted(recs), files, bad


def side_by_side(g_real, g_sh, a_real, a_sh):
    gr, gs = {g["item_id"]: g for g in g_real}, {g["item_id"]: g for g in g_sh}
    ar, as_ = {a["item_id"]: a for a in a_real}, {a["item_id"]: a for a in a_sh}
    rows = []
    for item in sorted(set(gr) | set(gs)):
        for tag, g, a in (("REAL", gr.get(item), ar.get(item)), ("SHUFFLED", gs.get(item), as_.get(item))):
            rows.append([item, tag,
                         g["n_requirements"] if g else None,
                         a["mean_pairwise_agreement"] if a else None,
                         a["full_disagreement_pairs"] if a else None,
                         a["n_singletons"] if a else None,
                         g["ratio_policy_to_physical"] if g else None,
                         g["unresolved"] if g else None])
    return table(["item", "arm", "n_req", "mean_agreement", "full_disagreement_pairs",
                  "singletons", "ratio_policy_to_physical", "unresolved"], rows)


def render(items, reqs, prompts_dir, g_real, g_sh, a_real, a_sh, calib):
    L = ["# B4 dilemma reconstruction -- report", ""]
    # 1
    L += ["## 1. " + SECTIONS[0], ""]
    L += table(["arm", "item_id", "branches_stated", "source"],
               [[i["arm"], i["item_id"], i["branches_stated"], i["source"]] for i in
                sorted(items, key=lambda x: (x["arm"], x["item_id"]))])
    L.append("")
    # 2
    recs, nfiles, bad = prompt_boundary(prompts_dir)
    L += ["## 2. " + SECTIONS[1], "",
          "Reconstructors: %d (%s)." % (len(recs), ", ".join(recs)),
          "Separation: one directory per reconstructor under `%s`; each file holds the"
          " single key `text_verbatim` and nothing else. Re-checked at report time:"
          " %d files, %d with any other key." % (os.path.basename(prompts_dir), nfiles, len(bad))]
    if bad:
        L += ["Files failing the boundary: " + ", ".join(bad)]
    L.append("")
    # 3
    L += ["## 3. " + SECTIONS[2], "", "Requirements: %d across %d items." % (len(reqs), len(set(r["item_id"] for r in reqs))), ""]
    L += table(["layer (as returned)", "count"], [[repr(k), v] for k, v in count_by(reqs, "layer").items()])
    L.append("")
    L += table(["item", "n_requirements", "n_reconstructors"],
               [[g["item_id"], g["n_requirements"], g["n_reconstructors"]] for g in g_real])
    L.append("")
    # 4
    sc = count_by(reqs, "status")
    L += ["## 4. " + SECTIONS[3], ""]
    L += table(["status", "count"], [[s, sc.get(s, 0)] for s in STATES])
    L.append("")
    # 5
    L += ["## 5. " + SECTIONS[4], ""]
    L += table(["item", "physical", "policy", "unresolved", "unresolved_both", "unresolved_neither",
                "ratio_policy_to_physical", "note"],
               [[g["item_id"], g["physical"], g["policy"], g["unresolved"], g["unresolved_both"],
                 g["unresolved_neither"], g["ratio_policy_to_physical"], g["ratio_note"]] for g in g_real])
    if g_real:
        L += ["", "Cues (arguments, printed so the joint reports itself):",
              "physical: " + ", ".join(g_real[0]["cues_physical"]),
              "policy: " + ", ".join(g_real[0]["cues_policy"])]
    L.append("")
    # 6
    L += ["## 6. " + SECTIONS[5], ""]
    for a in a_real:
        L += ["### item %s" % a["item_id"], ""]
        L += table(["a", "b", "n_a", "n_b", "matched_a", "matched_b", "agreement"],
                   [[p["a"], p["b"], p["n_a"], p["n_b"], p["matched_a"], p["matched_b"], p["agreement"]]
                    for p in a["pairs"]])
        L += ["", "mean pairwise agreement: %s; full-disagreement pairs: %d; singletons: %d" %
              (a["mean_pairwise_agreement"], a["full_disagreement_pairs"], a["n_singletons"]), ""]
        L += table(["singleton ref", "status", "requirement_text", "settling_test"],
                   [[s["ref"], s["status"], s["requirement_text"], s["settling_test"]] for s in a["singletons"]])
        L.append("")
    if a_real:
        L += ["Definition: " + a_real[0]["agreement_definition"], ""]
    # 7
    L += ["## 7. " + SECTIONS[6], ""] + side_by_side(g_real, g_sh, a_real, a_sh)
    L += ["", "Shuffled arm: requirement lists reassigned to items they were not written for; matched by "
          "%s." % (a_sh[0]["match_source"] if a_sh else "(none)"), ""]
    # 8
    L += ["## 8. " + SECTIONS[7], ""]
    if calib is None:
        L += ["No calibration run supplied (no documented-arm items in this run).", ""]
    else:
        L += table(["item", "reconstructor", "factors_named", "recovered", "missed", "beyond_report",
                    "beyond_report refs", "report_source"],
                   [[c["item_id"], c["reconstructor_id"], c["n_factors_named"], c["n_recovered"],
                     c["n_missed"], c["n_beyond_report"], ", ".join(c["beyond_report"]),
                     "; ".join(c["report_source"])] for c in calib])
        L += ["", "beyond_report is printed, not scored as error, and left uninterpreted.", ""]
    # 9
    L += ["## 9. " + SECTIONS[8], ""]
    L += table(["output", "match_source"],
               [["agreement (real)", a_real[0]["match_source"] if a_real else None],
                ["agreement (shuffled)", a_sh[0]["match_source"] if a_sh else None],
                ["calibration", calib[0]["match_source"] if calib else None]])
    L.append("")
    return "\n".join(L)


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, positional=(), options=("items", "requirements", "prompts", "grade", "grade_shuffled", "agreement", "agreement_shuffled", "calibration", "out", "runs"), required=("items", "requirements", "prompts", "grade", "grade_shuffled", "agreement", "agreement_shuffled", "out"))
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    ins = [a.items, a.requirements, a.prompts, a.grade, a.grade_shuffled, a.agreement,
           a.agreement_shuffled, a.calibration]
    with Run("b4/report.py", vars(a), None, ins, a.out, a.runs) as run:
        try:
            for p in (a.grade_shuffled, a.agreement_shuffled):
                if not os.path.exists(p):
                    raise Void("shuffled run missing: %s -- both outputs print or neither does" % p)
            calib = read_jsonl(a.calibration) if a.calibration else None
            text = render(read_jsonl(a.items), read_jsonl(a.requirements), a.prompts,
                          read_jsonl(a.grade), read_jsonl(a.grade_shuffled),
                          read_jsonl(a.agreement), read_jsonl(a.agreement_shuffled), calib)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        except Void as e:
            return finish(run, "void", notes=str(e))
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        return finish(run, "ok", {"sections": len(SECTIONS), "bytes": len(text)})


if __name__ == "__main__":
    sys.exit(main())
