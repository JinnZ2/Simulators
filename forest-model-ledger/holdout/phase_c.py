# SPDX-License-Identifier: CC0-1.0
"""Phase C (reveal + score): verify both seals, then score the sealed Phase B
predictions against the holdout studies.

    python3 holdout/phase_c.py SOURCE_CSV NONCE_A_HEX NONCE_B_HEX

SOURCE_CSV is PSF.data.EL.open.csv as fetched from Zenodo record 10403125.
It is not in this tree and neither is the holdout; this file rebuilds the
holdout from the source and refuses to score unless every seal verifies.

No scoring choice is made here. The fit, the moderator definitions and the
cluster bootstrap are imported from phase_b.py (same functions, same seed,
same replicate count). Nothing is refit, widened or rescued.

Two columns, never merged:
    MODEL  holdout direction against the sealed model direction
    FIT    holdout direction / estimate / interval against the sealed anchor fit
A holdout direction is read only when the holdout 80% interval excludes
zero; otherwise it is INDETERMINATE, neither hit nor miss.
"""
import csv
import hashlib
import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import phase_b  # noqa: E402  (fit, dummy: the Phase B code, unedited)

SOURCE_SHA = "bb56ba5ac31b13be09cf3df42c1215b53255bb1eb3bb8a91838ab8cb4cb5c82c"
HOLDOUT_BYTES = 601888
COMMIT_A = "ce54a50ecc4eba87d9df5ce99db93eddcbf3c1f3243765481d21cb2340c76713"
COMMIT_B = "f5dcc443d5afb4144ea0836015d0694c6796b723aa6d3c34e0bb00d7f7bcc65d"
PRED_SHA = "24477fdf93936f76e2475d337da033f6e304e17ca69203e4daebabfca48a9f26"
PRED_BYTES = 33257
CUTOFF_YEAR = 2018

# id -> (prediction id, column key, xfun, yfun); copied call for call from
# phase_b.build(), lines 409-505.
RR = lambda r: float(r["rr"])  # noqa: E731
FITS = [
    ("B1 AI", "B1", "AI", lambda r: float(r["AI"]), RR),
    ("B1 MAP", "B1", "MAP", lambda r: float(r["MAP"]) / 1000.0, RR),
    ("B2", "B2", "Phase2.time", lambda r: float(r["Phase2.time"]),
     lambda r: abs(float(r["rr"]))),
    ("B3", "B3", "Experimental.setting",
     phase_b.dummy("Experimental.setting", "Greenhouse", "Field"), RR),
    ("B4", "B4", "Life.form", phase_b.dummy("Life.form", "Woody", "Nonwoody"), RR),
    ("R5", "R5", "Sp.origin", phase_b.dummy("Sp.origin", "Non-native", "Native"), RR),
]
CONSTRUCTION = {"B4"}      # direction by construction: reported, not counted
NO_MODEL = {"R5"}          # no model run: MODEL column void
TIME_BINS = [(0, 3, "<= 3 mo"), (3, 6, "3-6 mo"), (6, 12, "6-12 mo"),
             (12, float("inf"), "> 12 mo")]   # reporting bins only; no score uses them


def sha(b):
    return hashlib.sha256(b).hexdigest()


def verify(source_path, nonce_a, nonce_b):
    """Step 1. Returns (holdout bytes, predictions dict, results list).
    Raises SystemExit on any mismatch, before any row is read for scoring."""
    out = []
    raw = open(source_path, "rb").read()
    ok = sha(raw) == SOURCE_SHA
    out.append(("a source sha256", ok, "%d bytes" % len(raw)))
    lines = raw.split(b"\r\n")
    assert lines[-1] == b""
    lines = lines[:-1]
    keep = [lines[0]]
    for ln in lines[1:]:
        if int(next(csv.reader([ln.decode("utf-8")]))[2]) > CUTOFF_YEAR:
            keep.append(ln)
    hb = b"\r\n".join(keep) + b"\r\n"
    out.append(("b holdout rebuilt", len(hb) == HOLDOUT_BYTES,
                "%d bytes, %d rows" % (len(hb), len(keep) - 1)))
    out.append(("c sha256(nonce_A || holdout)", sha(nonce_a + hb) == COMMIT_A, COMMIT_A))
    pb = open(os.path.join(HERE, "predictions.json"), "rb").read()
    out.append(("d predictions.json sha256 + bytes",
                sha(pb) == PRED_SHA and len(pb) == PRED_BYTES, "%d bytes" % len(pb)))
    out.append(("d sha256(nonce_B || predictions)", sha(nonce_b + pb) == COMMIT_B, COMMIT_B))
    for name, good, note in out:
        print("  %-36s %s   %s" % (name, "PASS" if good else "FAIL", note))
    if not all(g for _, g, _ in out):
        raise SystemExit("SEAL MISMATCH: nothing scored")
    return hb, json.loads(pb), out


def rows_of(data):
    return list(csv.DictReader(io.StringIO(data.decode("utf-8", errors="replace"), newline="")))


def read_direction(f):
    return f["direction"] if f["interval_excludes_zero"] else "INDETERMINATE"


def score(pred, hold_rows):
    table = []
    for fid, pid, col, xfun, yfun in FITS:
        p = pred["predictions"][pid]
        h = phase_b.fit(hold_rows, xfun, yfun=yfun, label=fid)
        hdir = read_direction(h)
        sealed_fit_dir = p["direction"][col]
        lo, hi = p["interval"][col]
        hlo, hhi = h["interval80"]
        row = {
            "id": fid, "column": col,
            "holdout_estimate": h["estimate"], "holdout_interval80": [hlo, hhi],
            "n_studies": h["n_studies"], "n_rows": h["n_rows"], "rows_dropped": h["rows_dropped"],
            "holdout_direction": hdir,
            "sealed_fit_estimate": p["per_column"][col]["estimate"],
            "sealed_fit_interval80": [lo, hi], "sealed_fit_direction": sealed_fit_dir,
            "fit_direction_hit": "INDETERMINATE" if hdir == "INDETERMINATE"
            else ("hit" if hdir == sealed_fit_dir else "miss"),
            "interval_hit": "yes" if lo <= h["estimate"] <= hi else "no",
            "overlap": "yes" if (hlo <= hi and lo <= hhi) else "no",
        }
        md = p["model_direction"]
        if pid in NO_MODEL:
            row["model_direction"], row["model_hit"], row["model_tag"] = "void", "void", "no model run"
        else:
            row["model_direction"] = md
            if hdir == "INDETERMINATE":
                row["model_hit"] = "INDETERMINATE"
            else:
                row["model_hit"] = "hit" if hdir == md else "miss"
            row["model_tag"] = ""
            if pid == "B1" and row["model_hit"] == "hit":
                row["model_tag"] = "supports A1 (mapping); sign set by construction"
            if pid in CONSTRUCTION:
                row["model_tag"] = "direction by construction, not scored"
        row["counted"] = (pid not in NO_MODEL and pid not in CONSTRUCTION
                          and row["model_hit"] in ("hit", "miss"))
        table.append(row)
    return table


def binom_tail(k, n):
    """P(at least k hits in n) at p = 0.5."""
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2.0 ** n


def mix(rows):
    out = {"Experimental.setting": {}, "Approach": {}, "Phase2.time": {}}
    for r in rows:
        for c in ("Experimental.setting", "Approach"):
            out[c][r[c]] = out[c].get(r[c], 0) + 1
        try:
            t = float(r["Phase2.time"])
            lab = next(n for a, b, n in TIME_BINS if a < t <= b) if t > 0 else "<= 3 mo"
        except ValueError:
            lab = "NA"
        out["Phase2.time"][lab] = out["Phase2.time"].get(lab, 0) + 1
    return out


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    src, na, nb = sys.argv[1], bytes.fromhex(sys.argv[2]), bytes.fromhex(sys.argv[3])
    print("STEP 1 seals")
    hb, pred, _ = verify(src, na, nb)
    hold = rows_of(hb)
    anchor = phase_b.load_rows()
    assert phase_b.sha256_file(phase_b.CSV_PATH) == phase_b.CSV_SHA
    print("  holdout: %d rows, %d studies ; anchor: %d rows, %d studies"
          % (len(hold), len({r["Author"] for r in hold}),
             len(anchor), len({r["Author"] for r in anchor})))

    # same-code check: the imported fit must reproduce every sealed anchor estimate
    worst = 0.0
    for fid, pid, col, xfun, yfun in FITS:
        a = phase_b.fit(anchor, xfun, yfun=yfun)
        s = pred["predictions"][pid]["per_column"][col]
        worst = max(worst, abs(a["estimate"] - s["estimate"]),
                    abs(a["interval80"][0] - s["interval"][0]),
                    abs(a["interval80"][1] - s["interval"][1]))
    print("  same-code check: refit on anchor vs sealed, largest difference %.1e  %s"
          % (worst, "PASS" if worst < 1e-12 else "FAIL"))
    if not worst < 1e-12:
        raise SystemExit("fit code does not reproduce the sealed anchor fits: nothing scored")

    table = score(pred, hold)
    print("\nSTEP 3 holdout estimates")
    print("  id      holdout est   holdout 80% interval     studies  rows  dropped  direction")
    for r in table:
        print("  %-7s %+9.4f   [%+8.4f, %+8.4f]   %5d  %5d  %5d    %s"
              % (r["id"], r["holdout_estimate"], *r["holdout_interval80"], r["n_studies"],
                 r["n_rows"], r["rows_dropped"], r["holdout_direction"]))
    print("\nMODEL column")
    print("  id      sealed model dir   holdout dir     result          counted  tag")
    for r in table:
        print("  %-7s %-18s %-15s %-15s %-8s %s"
              % (r["id"], r["model_direction"], r["holdout_direction"], r["model_hit"],
                 "yes" if r["counted"] else "no", r["model_tag"]))
    print("\nFIT column")
    print("  id      sealed fit est  sealed 80% interval      sealed dir  dir result      interval_hit  overlap")
    for r in table:
        print("  %-7s %+9.4f       [%+8.4f, %+8.4f]   %-10s  %-15s %-13s %s"
              % (r["id"], r["sealed_fit_estimate"], *r["sealed_fit_interval80"],
                 r["sealed_fit_direction"], r["fit_direction_hit"], r["interval_hit"], r["overlap"]))

    counted = [r for r in table if r["counted"]]
    hits = sum(r["model_hit"] == "hit" for r in counted)
    print("\nSTEP 4 baseline (chance 0.5 per scored model direction)")
    if counted:
        print("  scored %d, hits %d, P(at least %d of %d | chance) = %.4f"
              % (len(counted), hits, hits, len(counted), binom_tail(hits, len(counted))))
    else:
        print("  scored 0: no baseline computable")
    print("  scored ids: %s" % (", ".join(r["id"] for r in counted) or "none"))

    print("\nSTEP 5 method mix (row counts)")
    ma, mh = mix(anchor), mix(hold)
    for col in ("Experimental.setting", "Approach", "Phase2.time"):
        keys = sorted(set(ma[col]) | set(mh[col]),
                      key=lambda k: [n for _, _, n in TIME_BINS].index(k)
                      if k in [n for _, _, n in TIME_BINS] else 99)
        for k in keys:
            a, h = ma[col].get(k, 0), mh[col].get(k, 0)
            print("  %-22s %-12s anchor %5d (%.3f)   holdout %5d (%.3f)"
                  % (col, k, a, a / len(anchor), h, h / len(hold)))
    print("\nassumptions per id are in predictions.json; none is re-read or changed here")


if __name__ == "__main__":
    main()
