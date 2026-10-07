"""test_pathways.py -- checks for pathways.py. CC0. Stdlib only.

Run: python3 test_pathways.py

Every world below is CONSTRUCTED. A world returning the verdict it was
built to return shows the verdict is reachable; it is no evidence about
either pathway.
"""

import io
import os
import subprocess
import sys
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pathways as P  # noqa: E402

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))


def world(spec, unclear_every=0):
    """spec(cls, arm) -> fraction of GOOD outcomes among coded rows."""
    _, key = P.emit(repeats=10)
    codes, seen = [], {}
    for k in key:
        cls, arm = k["class"], k["arm"]
        i = seen.get((cls, arm), 0)
        seen[(cls, arm)] = i + 1
        if unclear_every and i % unclear_every == 0:
            codes.append({"id": k["id"], "code": "unclear"})
            continue
        frac = spec(cls, arm)
        is_good = i < round(frac * 30)
        lower = P.CLASSES[cls][1] == "lower"
        code = ("no" if is_good else "yes") if lower else \
               ("yes" if is_good else "no")
        codes.append({"id": k["id"], "code": code})
    return key, codes


def run():
    # features: every marker where the prediction says it is
    rows = P.locate_features()
    check("features: all located as predicted", all(r["ok"] for r in rows))
    check("features: every class has a feature",
          set(r["class"] for r in rows) == set(P.CLASSES))
    a_only = [r for r in rows if r["marker"] == "Felsenstein"]
    check("features: Felsenstein is in A", a_only and a_only[0]["file"]
          == P.FILE_A and a_only[0]["line"] is not None)
    fake = {P.FILE_A: "nothing here", P.FILE_B: "nothing here"}
    check("features: detector reports a missing marker",
          not all(r["ok"] for r in P.locate_features(fake)))

    # emit / sheet
    battery, key = P.emit(repeats=10)
    n_probes = sum(len(v) for v in P.PROBES.values())
    check("emit: size = probes x arms x repeats",
          len(battery) == n_probes * 4 * 10 == len(key))
    check("emit: ids unique", len(set(r["id"] for r in key)) == len(key))
    check("emit: every class has probes",
          all(len(P.PROBES[c]) >= 3 for c in P.CLASSES))
    ab = [k for k in key if k["arm"] == "AB"]
    check("emit: AB order alternates",
          set(tuple(k["order"]) for k in ab) ==
          {(P.FILE_A, P.FILE_B), (P.FILE_B, P.FILE_A)})
    check("emit: NONE carries no context",
          all(r["context_files"] == [] for r in battery
              if r["id"] in {k["id"] for k in key if k["arm"] == "NONE"}))
    check("emit: repeats < 1 refused", _raises(lambda: P.emit(repeats=0)))
    sh = P.sheet(battery)
    check("sheet: keys are id/class/field/response/code only",
          all(set(r) == {"id", "class", "field", "response", "code"}
              for r in sh))
    leak = any(str(v) in ("NONE", "A", "B", "AB")
               for r in sh for v in r.values())
    check("sheet: no field value is an arm name", not leak)

    # arithmetic
    iv = P.agresti_caffo(9, 10, 1, 10)
    check("AC: strong difference excludes 0", iv[0] > 0)
    check("AC: n = 0 gives None", P.agresti_caffo(1, 0, 1, 10) is None)
    check("mdd: n = 0 gives None", P.mdd(0, 10) is None)
    check("mdd: shrinks with n", P.mdd(100, 100) < P.mdd(10, 10))
    check("rate: empty denominator is None, not 0", P.rate(0, 0) is None)

    # constructed worlds
    def split(cls, arm):
        if arm == "NONE":
            return 0.2
        if cls == "OVERAPPLY":
            return {"A": 0.2, "B": 0.9, "AB": 0.9}[arm]
        if cls == "EVIDENCE":
            return {"A": 0.9, "B": 0.2, "AB": 0.9}[arm]
        return 0.6
    res = P.score(*world(split))
    check("world SPLIT: pattern SPLIT", res["pattern"] == "SPLIT")
    pc = res["per_class"]
    check("world SPLIT: OVERAPPLY prediction HELD",
          pc["OVERAPPLY"]["prediction"] == "HELD")
    check("world SPLIT: EVIDENCE prediction HELD",
          pc["EVIDENCE"]["prediction"] == "HELD")
    check("world SPLIT: CITE (no diff, B predicted) NOT_HELD",
          pc["CITE"]["prediction"] == "NOT_HELD")
    check("world SPLIT: DETECT no diff reads CONSISTENT_READ_MDD",
          pc["DETECT"]["prediction"] == "CONSISTENT_READ_MDD")
    check("world SPLIT: control REACHED everywhere",
          all(v == "REACHED" for v in res["control"].values()))
    check("world SPLIT: no interference",
          all(v == "NONE_DETECTED" for v in res["interference"].values()))

    res = P.score(*world(lambda c, a: 0.5))
    check("world flat: NO_DIFFERENCE", res["pattern"] == "NO_DIFFERENCE")
    check("world flat: control NOT_REACHED",
          all(v == "NOT_REACHED" for v in res["control"].values()))
    check("world flat: mdd printed as a number",
          res["per_class"]["DETECT"]["A_vs_B"]["mdd"] is not None)

    _, key = P.emit(repeats=10)
    res = P.score(key, [])
    check("world empty: NOT_EVALUABLE", res["pattern"] == "NOT_EVALUABLE")
    check("world empty: predictions UNTESTED",
          all(p["prediction"] == "UNTESTED"
              for p in res["per_class"].values()))

    res = P.score(*world(lambda c, a: {"NONE": 0.2, "A": 0.9,
                                       "B": 0.2, "AB": 0.9}[a]))
    check("world A wins all: A_DOMINATES", res["pattern"] == "A_DOMINATES")
    res = P.score(*world(lambda c, a: {"NONE": 0.2, "A": 0.2,
                                       "B": 0.9, "AB": 0.9}[a]))
    check("world B wins all: B_DOMINATES", res["pattern"] == "B_DOMINATES")

    res = P.score(*world(lambda c, a: {"NONE": 0.2, "A": 0.9,
                                       "B": 0.5, "AB": 0.1}[a]))
    check("world AB worse: INTERFERENCE",
          all(v == "INTERFERENCE" for v in res["interference"].values()))

    res = P.score(*world(lambda c, a: 0.5, unclear_every=2))
    c = res["per_class"]["DETECT"]["counts"]["A"]
    check("unclear: counted apart", c["unclear"] == 15)
    check("unclear: outside n", c["yes"] + c["no"] == 15)

    key, codes = world(lambda c, a: 0.5)
    check("score: unknown id refused",
          _raises(lambda: P.score(key, codes + [{"id": "zzz", "code": "no"}])))
    bad = [dict(codes[0], code="maybe")] + codes[1:]
    check("score: code outside yes/no/unclear refused",
          _raises(lambda: P.score(key, bad)))
    blank = [dict(codes[0], code="")] + codes[1:]
    check("score: blank code is uncoded, not no",
          P.score(key, blank)["uncoded"] == 1)

    out = P.render_score(P.score(key, codes))
    check("render: PREDICTIONS.md sha256 printed",
          P.file_sha(P.PREDICTIONS) in out)
    check("render: ASCII only", all(ord(ch) < 128 for ch in out))

    # cli
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = P.main(["--selftest"])
    check("cli: --selftest refused with exit 2", rc == 2
          and "test_pathways.py" in buf.getvalue())
    proc = subprocess.run([sys.executable, os.path.join(HERE, "pathways.py"),
                           "--features"], capture_output=True, text=True)
    check("cli: --features exits 0", proc.returncode == 0)


def _raises(fn):
    try:
        fn()
    except Exception:
        return True
    return False


if __name__ == "__main__":
    run()
    failed = [n for n, ok in RESULTS if not ok]
    for n, ok in RESULTS:
        print("%s  %s" % ("PASS" if ok else "FAIL", n))
    print("checks: %d   failed: %d" % (len(RESULTS), len(failed)))
    sys.exit(1 if failed else 0)
