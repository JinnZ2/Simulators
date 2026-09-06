"""B1.5 report.py -- report.md from the real and permuted summaries. Six
sections, in order, no others. The permuted result is a SECOND OUTPUT:
if the permuted summary is missing the run is void and nothing is written.

Section 6 (NULLS TRIGGERED, N1-N5) follows workorders/runner_up_trace.md
section 7 via nulls.py; every threshold is an argument printed with the
result, and a null the inputs cannot evaluate says so. --base is optional
and only N5 reads it.

Command: python3 report.py --separations S.jsonl --summary SUM.jsonl --summary-permuted SUMP.jsonl --out report.md
    [--base BASE.jsonl] [--n1-resync 0.9] [--n2-separate 0.95] [--n3-jaccard 0.5] [--n5-discordance 0.1] [--sustained-d 64]
"""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import Invalid, Run, Void, finish, parse_argv, read_jsonl, usage_exit  # noqa: E402
import nulls  # noqa: E402

SECTIONS = ["Counts and the case set present", "D sweep", "L sweep", "Stability overlaps",
            "REAL vs PERMUTED, side by side", "NULLS TRIGGERED (N1-N5)"]
COLS = ["model_id", "D", "L", "n_rows", "n_positions", "mean_div", "resync_rate", "top_decile_count"]


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rows:
        out.append("| " + " | ".join("" if v is None else str(v) for v in r) + " |")
    return out


def split(summary):
    return [s for s in summary if "n_rows" in s], [s for s in summary if "sweep_axis" in s]


def sweep_table(cells, order):
    rows = sorted(cells, key=lambda c: tuple(c[k] for k in order))
    return table(COLS, [[c[k] for k in COLS] for c in rows])


def stab_table(stab, arm=None):
    hdr = (["arm"] if arm else []) + ["model_id", "sweep_axis", "held", "from", "to", "jaccard"]
    rows = [([arm] if arm else []) + [s["model_id"], s["sweep_axis"], s["held"], s["from"], s["to"], s["jaccard"]]
            for s in sorted(stab, key=lambda s: (s["model_id"], s["sweep_axis"], str(s["held"]), s["from"]))]
    return table(hdr, rows)


def render(seps, real, perm, base_rows=None, thr=None):
    thr = dict(nulls.DEFAULTS, **(thr or {}))
    rc, rs = split(real)
    pc, ps = split(perm)
    L = ["# B1 runner-up trace scoring -- report", ""]
    cases = sorted(set(r["case_id"] for r in seps))
    models = sorted(set(r["model_id"] for r in seps))
    positions = sorted(set((r["case_id"], r["model_id"], r["i"]) for r in seps))
    branches = sorted(set((r["case_id"], r["model_id"], r["i"], r["branch_rank"]) for r in seps))
    L += ["## 1. " + SECTIONS[0], "",
          "separation rows: %d; cases: %d; models: %d; positions: %d; traces: %d" %
          (len(seps), len(cases), len(models), len(positions), len(branches)),
          "D values: %s; L values: %s" % (sorted(set(r["D"] for r in seps)), sorted(set(r["L"] for r in seps))), ""]
    L += table(["case_id", "positions", "traces"],
               [[c, sum(1 for p in positions if p[0] == c), sum(1 for b in branches if b[0] == c)] for c in cases])
    L += ["", "models: " + ", ".join(models), ""]
    L += ["## 2. " + SECTIONS[1], ""] + sweep_table(rc, ("model_id", "L", "D")) + [""]
    L += ["## 3. " + SECTIONS[2], ""] + sweep_table(rc, ("model_id", "D", "L")) + [""]
    L += ["## 4. " + SECTIONS[3], ""] + stab_table(rs) + [""]
    L += ["## 5. " + SECTIONS[4], ""]
    both = sorted([("REAL", c) for c in rc] + [("PERMUTED", c) for c in pc],
                  key=lambda ac: (ac[1]["model_id"], ac[1]["D"], ac[1]["L"], ac[0] != "REAL"))
    L += table(["arm"] + COLS, [[arm] + [c[k] for k in COLS] for arm, c in both]) + [""]
    L += stab_table(rs, "REAL") + [""] + stab_table(ps, "PERMUTED") + [""]
    seeds = sorted(set(str(p.get("permute_seed")) for p in perm if p.get("permute_seed") is not None))
    L += ["## 6. " + SECTIONS[5], "", "Per workorders/runner_up_trace.md section 7. Thresholds are arguments: %s" %
          ", ".join("%s=%s" % kv for kv in sorted(thr.items())), ""]
    for n in nulls.evaluate(seps, real, perm, base_rows, thr):
        trig = {True: "TRIGGERED", False: "not triggered", None: "NOT EVALUABLE"}[n["triggered"]]
        L += ["### %s -- %s" % (n["id"], trig), "", "number: `%s`" % json.dumps(n["number"], sort_keys=True),
              "threshold: `%s`" % n["threshold"], "", n["note"], ""]
    L += ["permute seed(s) carried in the permuted summary: %s (the seed is in the permute run record)" %
          (", ".join(seeds) if seeds else "none"), ""]
    return "\n".join(L)


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, options=("separations", "summary", "summary_permuted", "out", "runs", "base",
                                                "n1_resync", "n2_separate", "n3_jaccard", "n5_discordance", "sustained_d"),
                       required=("separations", "summary", "summary_permuted", "out"),
                       defaults={k: str(v) for k, v in nulls.DEFAULTS.items()})
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    with Run("b1/report.py", vars(a), None, [a.separations, a.summary, a.summary_permuted, a.base], a.out, a.runs) as run:
        try:
            if not os.path.exists(a.summary_permuted):
                raise Void("permuted summary missing: %s -- both print or neither does" % a.summary_permuted)
            thr = {k: (int if k == "sustained_d" else float)(getattr(a, k)) for k in nulls.DEFAULTS}
            base_rows = read_jsonl(a.base) if a.base else None
            text = render(read_jsonl(a.separations), read_jsonl(a.summary), read_jsonl(a.summary_permuted), base_rows, thr)
        except (Invalid, ValueError) as e:
            return finish(run, "error", notes=str(e))
        except Void as e:
            return finish(run, "void", notes=str(e))
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        return finish(run, "ok", {"sections": len(SECTIONS), "bytes": len(text)})


if __name__ == "__main__":
    sys.exit(main())
