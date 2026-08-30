#!/usr/bin/env python3
# r2v2_audit.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# Audit of R2_OUTLINE_V2.md, the revision that folds the Fable
# work-order return (commit 2fdbcd4) back into the outline. Both
# versions stay in the folder as delivered; this module edits neither.
#
# A revision quoting an audit is a copy, and copies drift (OE_011,
# DBK_010) -- so every figure the v2 quotes from the return is checked
# against the live computation, by importing wo_return and recomputing,
# never by trusting the transcription. The section-level findings
# (the D row's two answers, the tag legend, the only-Task-6 count) are
# computed from the two texts, not read off them.

import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wo_return as WO  # noqa: E402
import audit as R1  # noqa: E402

V2_PATH = os.path.join(HERE, "R2_OUTLINE_V2.md")
WO_PATH = os.path.join(HERE, "WORK_ORDER_F5.md")

TAGS = ("KILLED-VACUOUS", "KILLED", "QUALIFIED", "REOPENED", "LIVE",
        "OPEN")

# computed once; every transcription check reads these, never the doc
TASK_VERDICTS = {}


def _verdicts():
    if not TASK_VERDICTS:
        TASK_VERDICTS.update({
            1: WO.task1()["result"], 2: WO.task2()["result"],
            3: WO.task3()["result"], 4: WO.task4()["result"],
            5: WO.task5()["result"], 6: WO.task6()["result"],
            7: WO.task7()["result"]})
    return TASK_VERDICTS


def v2_doc():
    return io.open(V2_PATH, encoding="utf-8").read()


def wo_doc():
    return io.open(WO_PATH, encoding="utf-8").read()


# --------------------------------------------------- the v2 §1 matrix

def _tokens(cell):
    """Carrier tokens in a matrix cell, with which are attack-marked."""
    toks, atk = [], []
    for m in re.finditer(r"P\d+(?:\.\d+)?", cell):
        # "P1-bounded" is an annotation, not a carrier -- a carrier
        # token is never hyphenated in these tables
        if cell[m.end():m.end() + 1] == "-":
            continue
        toks.append(m.group(0))
        tail = cell[m.end():m.end() + 12]
        if tail.lstrip(" (").startswith(("atk", "attack")):
            atk.append(m.group(0))
    return toks, atk


def v2_matrix(doc=None):
    doc = doc if doc is not None else v2_doc()
    sec = doc.split("## 1. COVERAGE MATRIX")[1].split("## 2.")[0]
    rows = {}
    for line in sec.splitlines():
        m = re.match(r"^([A-F][12]?)\s{2,}(.+?)\s{2,}(.+?)\s{2,}(.+)$",
                     line)
        if not m or m.group(1) not in ("A", "B1", "B2", "C", "D", "E",
                                       "F"):
            continue
        load = m.group(1)
        r1_toks, r1_atk = _tokens(m.group(2))
        r2_toks, r2_atk = _tokens(m.group(3))
        rows[load] = {"r1": r1_toks, "r1_atk": r1_atk,
                      "r2": r2_toks, "r2_atk": r2_atk,
                      "change": m.group(4).strip()}
    return rows


def r1_column_check():
    """The v2 matrix's R1 column against the computed R1 coverage --
    same check the v1 audit ran, on the new table."""
    cov = R1.coverage()
    rows = v2_matrix()
    out, exact = [], True
    for load in ("A", "B1", "B2", "C", "D", "E", "F"):
        want = set(cov["carried"].get(load, [])) \
            | set(cov["attacked"].get(load, []))
        want_atk = set(cov["attacked"].get(load, [])) \
            - set(cov["carried"].get(load, []))
        got = set(rows[load]["r1"])
        got_atk = set(rows[load]["r1_atk"])
        match = (got == want and got_atk == want_atk)
        exact = exact and match
        out.append((load, sorted(got), sorted(want), match))
    return {"rows": out, "exact": exact}


def d_row():
    """§1's answer for D: carriers empty, the change column says so."""
    row = v2_matrix()["D"]
    return {"r2_carriers": row["r2"],
            "uncarried_in_sec1": row["r2"] == [],
            "change": row["change"]}


# ------------------------------------------- §1 vs §3: the D split

def sec3_carries():
    """The carries column of §3's channel table, last 2+-space field of
    each channel header line."""
    doc = v2_doc()
    sec = doc.split("## 3. THREE VERIFICATION")[1].split(
        "DISJOINTNESS CHECK")[0]
    out = {}
    for chan in ("P0.3", "P0.4", "P0.5"):
        for line in sec.splitlines():
            if line.startswith(chan):
                cells = re.split(r"\s{2,}", line.strip())
                out[chan] = re.findall(r"\b([A-F][12]?)\b", cells[-1])
                break
    return out


def d_split():
    """One document, two answers on whether D is carried."""
    s3 = sec3_carries()
    s1 = d_row()
    claims_d = sorted(c for c in s3 if "D" in s3[c])
    doc = v2_doc()
    f_row_marked = "disjoint*" in doc  # F's condition carries a marker
    # D's condition lives in the D-KILL prose, not in any §3 column mark
    sec3_txt = doc.split("## 3. THREE VERIFICATION")[1].split(
        "DISJOINTNESS")[0]
    d_marked_in_sec3 = bool(re.search(r"D\s*\(", sec3_txt))
    return {"sec1_uncarried": s1["uncarried_in_sec1"],
            "sec3_channels_listing_d": claims_d,
            "split": s1["uncarried_in_sec1"] and bool(claims_d),
            "f_condition_marked": f_row_marked,
            "d_condition_marked_in_sec3": d_marked_in_sec3,
            "reconciling_prose":
                "D is carried only once P1 declares the dimension"
                in doc}


# --------------------------------------------------- transcription

def transcription(doc=None):
    """Every figure v2 quotes from the return, recomputed."""
    doc = doc if doc is not None else v2_doc()
    v = _verdicts()
    t2, t4, t5, t7 = WO.task2(), WO.task4(), WO.task5(), WO.task7()
    checks = []

    stated_pass = {1, 2, 5, 7}
    stated_fail = {3, 4, 6}
    checks.append(("verdict split 1,2,5,7 / 3,4,6",
                   "Tasks 1,2,5,7 PASS" in doc
                   and "Tasks 3,4,6 FAIL" in doc,
                   all(v[n] == "PASS" for n in stated_pass)
                   and all(v[n] == "FAIL" for n in stated_fail)))
    checks.append(("retention triple 3 / 3 / 2",
                   "copies-held 3 / inherited-metric 3 / outline-pricing"
                   " 2" in doc,
                   (t2["n_eff_copies_held"],
                    t2["n_eff_no_copies_inherited_metric"],
                    t2["n_eff_no_copies_outline_pricing"]) == (3, 3, 2)))
    checks.append(("coder ratios 0.1 vs 1.0",
                   "0.1 vs 1.0" in doc,
                   (t4["d3"]["coder_A_ratio"],
                    t4["d3"]["coder_B_ratio"]) == (0.1, 1.0)))
    sweep = t5["threshold_sweep"]
    checks.append(("(4,3) flips between t=1 and t=1.5",
                   "FLIPS verdict between t=1 and t=1.5" in doc,
                   sweep[0][1] is True and sweep[1][1] is False))
    checks.append(("5 hosts, all refused",
                   "5 hosts, all refused" in doc,
                   len(t7["vector"]) == 5
                   and all(c == "000" for _h, c in t7["vector"])))
    checks.append(("rated 1 / realized 0",
                   "rated 1 / realized 0" in doc,
                   t7["n_eff_rated"] == 1
                   and t7["realized_paths"] == 0))
    exact = all(stated and computed for _n, stated, computed in checks)
    return {"checks": checks, "exact": exact}


def kappa_provenance():
    """The 0.6 in §8[3] is sourced: the order's own Task 4 rule."""
    return {"v2_states": "kappa ≥ 0.6" in v2_doc(),
            "order_states": "kappa ≥ 0.6" in wo_doc()}


def commit_check():
    """The cited commit hash resolves in this repository's history.
    First drop in the family to cite a commit of the repo it lands in;
    checkable by anyone with the clone. NOT_RUN if git is unavailable."""
    try:
        p = subprocess.run(
            ["git", "log", "--format=%h %s", "-60"],
            cwd=os.path.dirname(HERE), stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=30)
        if p.returncode != 0:
            return {"status": "NOT_RUN",
                    "why": "git returned rc %d" % p.returncode}
        lines = p.stdout.decode("utf-8", "replace").splitlines()
        hit = [ln for ln in lines if ln.startswith("2fdbcd4")]
        return {"status": "RUN", "resolves": bool(hit),
                "subject": hit[0].split(" ", 1)[1] if hit else None}
    except Exception as e:
        return {"status": "NOT_RUN", "why": type(e).__name__}


# --------------------------------------------------- §8 status tags

def tag_check(doc=None):
    doc = doc if doc is not None else v2_doc()
    sec = doc.split("## 8. PLACEHOLDERS")[1]
    legend_line = [ln for ln in sec.splitlines()
                   if ln.startswith("status tags:")][0]
    legend = [t for t in TAGS if t in legend_line]
    v = _verdicts()
    entries, used, consistent = [], set(), True
    for m in re.finditer(r"^\[(\d)\]\s+(.+)$", sec, re.M):
        n, line = int(m.group(1)), m.group(2)
        tags, rest = [], line
        for t in TAGS:
            if t in rest:
                tags.append(t)
                rest = rest.replace(t, "")
        used.update(tags)
        tasks = [int(x) for x in re.findall(r"Task (\d)", line)]
        entry_ok = True
        for t in tags:
            for tk in tasks:
                if t in ("KILLED", "KILLED-VACUOUS", "REOPENED"):
                    entry_ok = entry_ok and v.get(tk) == "FAIL"
                elif t in ("QUALIFIED", "LIVE"):
                    entry_ok = entry_ok and v.get(tk) == "PASS"
        consistent = consistent and entry_ok
        entries.append((n, tags, tasks, entry_ok))
    return {"legend": legend, "used": sorted(used),
            "beyond_legend": sorted(set(used) - set(legend)),
            "entries": entries, "all_consistent": consistent}


# ------------------------------------- the only-Task-6 count, checked

def searcher_branches():
    """Which construction tasks carry a searcher-dependent
    nothing-found branch, per the order's own text -- against v2's
    'only Task 6' sentence."""
    order = wo_doc()
    t3 = order.split("## TASK 3")[1].split("## TASK 4")[0]
    t4 = order.split("## TASK 4")[1].split("## TASK 5")[0]
    t6 = order.split("## TASK 6")[1].split("## TASK 7")[0] \
        if "## TASK 7" in order.split("## TASK 6")[1] \
        else order.split("## TASK 6")[1]
    named = {
        4: "no defensible disagreement found" in t4,
        6: "INCONCLUSIVE-WEAK-POSITIVE" in t6,
    }
    t3_named = ("INCONCLUSIVE" in t3
                or "no defensible" in t3 or "none found" in t3)
    v = _verdicts()
    exercised = [n for n in (3, 4, 6) if v[n] != "FAIL"]
    return {"named_in_order": sorted(k for k, x in named.items() if x),
            "task3_branch_named": t3_named,
            "task3_branch_implicit": not t3_named,
            "v2_counts_only_task6":
                "only Task 6's weak-positive branch" in v2_doc(),
            "branches_exercised": exercised,
            "conclusion_survives": exercised == []}


# ------------------------------------------- the probe-set extension

def probe_extension():
    """v2 applies the Task 6 selection kill to the Task 3 candidate --
    a cross-application the return did not make."""
    doc = v2_doc()
    note = WO.TASK3_NOTE
    return {"v2_requires_unselectable": "unselectable" in doc,
            "return_stated_fixed": "fixed battery" in note,
            "return_closed_selection": "unselect" in note
            or "selection" in note,
            "extension": "unselectable" in doc
            and "unselect" not in note and "selection" not in note}


def accounting_declared():
    """The DBK_011 gap is routed to observability, not resolved by
    picking a side: which retention accounting is used is itself a
    declared decision under P0.2."""
    return ("which\naccounting is used is itself a decision that must "
            "be declared (P0.2)" in v2_doc()
            or "accounting is used is itself a decision" in v2_doc())


# ---------------------------------------------------------- render

def _w(s, n=70):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines


def render():
    out = []
    w = out.append
    w("R2_OUTLINE_V2 -- STRUCTURAL AUDIT")
    w("")
    w("Both outline versions stay in the folder as delivered; this")
    w("module reads them and edits neither. Every figure the v2 quotes")
    w("from the return is recomputed through wo_return, never trusted")
    w("as transcription.")
    w("")

    tr = transcription()
    w("TRANSCRIPTION OF THE RETURN (recomputed)")
    for name, stated, computed in tr["checks"]:
        w("  %-38s stated %-5s computed %s"
          % (name, stated, computed))
    kp = kappa_provenance()
    w("  %-38s stated %-5s computed %s"
      % ("kappa 0.6 sourced to the order", kp["v2_states"],
         kp["order_states"]))
    cc = commit_check()
    if cc["status"] == "RUN":
        w("  %-38s %s" % ("commit 2fdbcd4 resolves", cc["resolves"]))
        if cc["subject"]:
            for ln in _w("subject: " + cc["subject"], 64):
                w("      " + ln)
    else:
        w("  commit check NOT_RUN (%s)" % cc["why"])
    w("  exact on all recomputed figures: %s" % tr["exact"])
    w("")

    rc = r1_column_check()
    w("R1 COLUMN OF THE V2 MATRIX vs COMPUTED COVERAGE")
    for load, got, want, match in rc["rows"]:
        w("  %-4s %-24s %s" % (load, ",".join(got) or "--",
                               "match" if match else
                               "DIFFERS from %s" % want))
    w("  exact: %s" % rc["exact"])
    w("")

    ds = d_split()
    w("THE D ROW, TWO ANSWERS")
    for ln in _w(
            "Section 1 lists no carrier for D (uncarried: %s), and "
            "section 3's carries column still lists D under %s. The "
            "F conditional carries a marker in the matrix (%s); D's "
            "condition is stated in the D-KILL prose (%s) and reaches "
            "no column. Which answer a parser reads depends on which "
            "section it parses."
            % (ds["sec1_uncarried"],
               " and ".join(ds["sec3_channels_listing_d"]),
               ds["f_condition_marked"], ds["reconciling_prose"])):
        w("  " + ln)
    w("")

    tc = tag_check()
    w("SECTION 8 STATUS TAGS")
    w("  legend declares : %s" % ", ".join(tc["legend"]))
    w("  entries use     : %s" % ", ".join(tc["used"]))
    w("  beyond legend   : %s" % (", ".join(tc["beyond_legend"])
                                  or "none"))
    for n, tags, tasks, entry_ok in tc["entries"]:
        w("  [%d] %-28s tasks %-8s consistent with computed verdicts:"
          " %s" % (n, ",".join(tags) or "(untagged)",
                   ",".join(str(t) for t in tasks) or "--", entry_ok))
    w("")

    sb = searcher_branches()
    w("THE ONLY-TASK-6 SENTENCE, COUNTED")
    for ln in _w(
            "v2 says only Task 6's weak-positive branch depended on "
            "verifier identity. The order names such a branch in tasks "
            "%s ('no defensible disagreement found' is the same "
            "searcher-dependent positive), and task 3 carries one "
            "implicitly (%s). All three construction tasks returned "
            "kills, so zero such branches were exercised (%s) and the "
            "sentence's conclusion stands; its count does not."
            % (" and ".join(str(x) for x in sb["named_in_order"]),
               sb["task3_branch_implicit"],
               sb["branches_exercised"] == [])):
        w("  " + ln)
    w("")

    pe = probe_extension()
    w("THE PROBE-SET EXTENSION")
    for ln in _w(
            "v2 requires the pinned-probe battery to be fixed, public "
            "and unselectable (%s). The return's own note said 'fixed' "
            "and never closed who selects the battery (selection "
            "closed in the return: %s) -- the revision applied the "
            "Task 6 selection kill to the Task 3 candidate, a "
            "cross-application the return did not make."
            % (pe["v2_requires_unselectable"],
               pe["return_closed_selection"])):
        w("  " + ln)
    w("")
    w("ACCOUNTING DECLARED, NOT PICKED: %s" % accounting_declared())
    w("")
    w("This module computes; it does not conclude. Findings are in")
    w("CLAIM_TABLE.md as DBK_021..DBK_025.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "r2v2_audit.py has no checks of its own. The checks that "
            "exercise it live in selftest_dbk.py.\n"
            "    python3 design-basis-ai/selftest_dbk.py\n")
        sys.exit(2)
    print(render())
