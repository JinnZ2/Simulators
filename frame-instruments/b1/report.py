"""B1.5 report.py -- report.md from the real and permuted summaries. Six
sections, in order, no others. The permuted result is a SECOND OUTPUT:
if the permuted summary is missing the run is void and nothing is written.

Section 6 (NULLS TRIGGERED, N1-N5) is defined by the reference spec
WORKORDER_runner_up_trace.md. If that file is not present, the section
states so and prints the quantities a null would read, without inventing
the nulls.

Command: python3 report.py --separations S.jsonl --summary SUM.jsonl --summary-permuted SUMP.jsonl --out report.md
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ficommon import Invalid, Run, Void, finish, parse_argv, read_jsonl, usage_exit  # noqa: E402

REF_SPEC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "workorders", "runner_up_trace.md")
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


def render(seps, real, perm):
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
    L += ["## 6. " + SECTIONS[5], ""]
    if os.path.exists(REF_SPEC):
        L += ["Reference spec present at workorders/runner_up_trace.md; N1-N5 are not "
              "implemented in this build and must be read from it.", ""]
    else:
        L += ["The reference spec (WORKORDER_runner_up_trace.md) is not in this tree, so N1-N5 "
              "have no definition here and no null is evaluated or invented. The quantities a "
              "null would read, real beside permuted:", ""]
    L += table(["model_id", "D", "L", "mean_div real", "mean_div permuted", "resync real", "resync permuted"],
               [[c["model_id"], c["D"], c["L"], c["mean_div"],
                 next((p["mean_div"] for p in pc if (p["model_id"], p["D"], p["L"]) == (c["model_id"], c["D"], c["L"])), None),
                 c["resync_rate"],
                 next((p["resync_rate"] for p in pc if (p["model_id"], p["D"], p["L"]) == (c["model_id"], c["D"], c["L"])), None)]
                for c in sorted(rc, key=lambda c: (c["model_id"], c["D"], c["L"]))])
    L += ["", "Stratum averages and rates are identical across REAL and PERMUTED by construction: the "
          "permutation moves tuples between positions inside each (model, D, L) stratum and leaves the "
          "stratum multiset intact. What the null moves is the top-decile position sets, read in the "
          "stability tables of section 5.", "",
          "permute seed(s) carried in the permuted summary: %s (the seed is in the permute run record)" %
          (", ".join(seeds) if seeds else "none"), ""]
    return "\n".join(L)


def main(argv=None):
    try:
        a = parse_argv(argv, __doc__, options=("separations", "summary", "summary_permuted", "out", "runs"),
                       required=("separations", "summary", "summary_permuted", "out"))
    except Invalid as e:
        return usage_exit(e)
    if a is None:
        return 0
    with Run("b1/report.py", vars(a), None, [a.separations, a.summary, a.summary_permuted], a.out, a.runs) as run:
        try:
            if not os.path.exists(a.summary_permuted):
                raise Void("permuted summary missing: %s -- both print or neither does" % a.summary_permuted)
            text = render(read_jsonl(a.separations), read_jsonl(a.summary), read_jsonl(a.summary_permuted))
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        except Void as e:
            return finish(run, "void", notes=str(e))
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        return finish(run, "ok", {"sections": len(SECTIONS), "bytes": len(text)})


if __name__ == "__main__":
    sys.exit(main())
