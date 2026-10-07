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
import tempfile
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pathways as P  # noqa: E402

RESULTS = []
TAG = "t1"


def check(name, cond):
    RESULTS.append((name, bool(cond)))


def manifest(**over):
    m = {"run_tag": TAG, "model": "constructed", "temperature": 1.0,
         "top_p": 1.0, "max_tokens": 1024, "system_prompt": "(none)",
         "date": "2026-10-07",
         "coders": [{"id": "c1", "same_model_class": False},
                    {"id": "c2", "same_model_class": True}]}
    m.update(over)
    return m


def world(spec, repeats=30, flip=None, guess=None, keep=None):
    """spec(cls, arm, probe_id) -> GOOD fraction. Two coders.
    flip(cls) -> True: coder 2 inverts yes/no in that class.
    guess(arm, i) -> guessed condition string.
    keep(cls, arm, probe_id) -> False: rows left uncoded."""
    _, key = P.emit(repeats=repeats, run_tag=TAG)
    c1, c2 = [], []
    for k in key:
        cls, arm, pid, i = k["class"], k["arm"], k["probe_id"], k["repeat"]
        if keep and not keep(cls, arm, pid):
            continue
        frac = spec(cls, arm, pid)
        is_good = i < round(frac * repeats)
        lower = P.CLASSES[cls][1] == "lower"
        code = ("no" if is_good else "yes") if lower else \
               ("yes" if is_good else "no")
        g = guess(arm, i) if guess else "unsure"
        c1.append({"id": k["id"], "run_tag": TAG, "code": code,
                   "guess": g, "coder": "c1"})
        code2 = code
        if flip and flip(cls):
            code2 = {"yes": "no", "no": "yes"}[code]
        c2.append({"id": k["id"], "run_tag": TAG, "code": code2,
                   "guess": "unsure", "coder": "c2"})
    return key, [c1, c2]


def S(key_codes, **kw):
    key, codes = key_codes
    return P.score(key, codes, manifest(), **kw)


def _raises(fn):
    try:
        fn()
    except Exception:
        return True
    return False


def run():
    # ---- predictions file: original prefix intact, amendment appended
    ps = P.predictions_status()
    check("predictions: original prefix hash matches registered value",
          ps["prefix_ok"])
    check("predictions: file is amended", ps["amended"])
    data = open(os.path.join(HERE, P.PREDICTIONS), "rb").read()
    tampered = data[:100] + b"X" + data[101:]
    check("predictions: an edit inside the original is detected",
          not P.predictions_status(tampered)["prefix_ok"])
    check("predictions: an appended amendment does not trip the check",
          P.predictions_status(data + b"\nmore\n")["prefix_ok"])
    text = data.decode("utf-8")
    check("predictions: amendment declares FREEZE",
          "FROZEN as a known defect under test" in text)
    check("predictions: amendment declares delta 0.15",
          "delta = 0.15" in text)

    # ---- features
    rows = P.locate_features()
    check("features: all located as predicted", all(r["ok"] for r in rows))
    frozen = [r for r in rows
              if r["marker"] == "very long run of independent trials"]
    check("features: frozen B line still present (B not edited)",
          frozen and frozen[0]["line"] is not None)
    fake = {P.FILE_A: "nothing here", P.FILE_B: "nothing here"}
    check("features: detector reports a missing marker",
          not all(r["ok"] for r in P.locate_features(fake)))

    # ---- emit / prompt / sheet
    battery, key = P.emit(run_tag=TAG)
    n_probes = sum(len(v) for v in P.PROBES.values())
    check("emit: default k = 30, five arms",
          len(battery) == n_probes * 5 * 30 == len(key))
    check("emit: ids unique", len(set(r["id"] for r in key)) == len(key))
    check("emit: k below 3 refused",
          _raises(lambda: P.emit(repeats=2, run_tag=TAG)))
    check("emit: run_tag required", _raises(lambda: P.emit(run_tag="")))
    check("emit: every row carries the run_tag",
          all(r["run_tag"] == TAG for r in battery + key))
    arms = {k["arm"] for k in key}
    check("emit: arms NONE/A/B/AB/BA", arms == set(P.ARMS))
    by = {k["id"]: k["arm"] for k in key}
    ab = next(r for r in battery if by[r["id"]] == "AB")
    ba = next(r for r in battery if by[r["id"]] == "BA")
    check("emit: AB and BA fixed, opposite orders",
          ab["context_files"] == [P.FILE_A, P.FILE_B] and
          ba["context_files"] == [P.FILE_B, P.FILE_A])
    none = next(r for r in battery if by[r["id"]] == "NONE")
    pn, pab = P.assemble(none), P.assemble(ab)
    check("prompt: NONE has no reference block",
          "Reference document" not in pn and pn.startswith("Question: "))
    check("prompt: AB carries two neutral headers, A first",
          pab.count("Reference document") == 2 and
          pab.index(P._read(P.FILE_A)[:200]) <
          pab.index(P._read(P.FILE_B)[:200]))
    check("prompt: no filename in any header",
          "PATHWAY_B" not in pab and ".md" not in
          "\n".join(l for l in pab.splitlines()
                    if l.startswith("Reference document")))
    changed = {P.FILE_A: "edited", P.FILE_B: P._read(P.FILE_B)}
    check("prompt: a changed file is refused",
          _raises(lambda: P.assemble(ab, changed)))
    sh = P.sheet(battery)
    check("sheet: keys fixed",
          all(set(r) == {"id", "run_tag", "class", "field", "probe",
                         "response", "code", "guess", "coder"} for r in sh))
    check("sheet: no field value is an arm name",
          not any(str(v) in P.ARMS for r in sh for v in r.values()))

    # ---- lengths
    L = P.lengths()
    check("lengths: A, B, A+B measured",
          all(L[k]["chars"] > 0 for k in ("A", "B", "A+B")))
    check("lengths: A+B at least A + B chars",
          L["A+B"]["chars"] >= L["A"]["chars"] + L["B"]["chars"])
    check("lengths: render labels tokens APPROXIMATE",
          "APPROXIMATE" in P.render_lengths(L))

    # ---- strip
    g = P.doc_grams()
    words = P._read(P.FILE_A).split()
    quote = " ".join(words[100:112])
    s, n = P.strip_text("Before. " + quote + " after.", g)
    check("strip: 12-word verbatim run removed", n == 12 and
          quote not in s and s.startswith("Before.") and
          s.endswith("after."))
    check("strip: no marker left", "[" not in s and "strip" not in s.lower())
    short = " ".join(words[100:105])
    check("strip: a 5-word quote survives",
          P.strip_text("x " + short + " y", g)[1] == 0)
    raw = "nothing\n here  at all "
    check("strip: untouched response is byte-identical",
          P.strip_text(raw, g) == (raw, 0))
    check("strip: case and punctuation do not shield a quote",
          P.strip_text(quote.upper().replace(" ", ", "), g)[1] == 12)
    rows2, log = P.strip_sheet([{"id": "x", "run_tag": TAG,
                                 "response": quote}], g)
    check("strip: log separate, counts words", log[0]["words_removed"] == 12
          and "words_removed" not in rows2[0])

    # ---- arithmetic
    check("AC: strong difference excludes 0",
          P.agresti_caffo(9, 10, 1, 10)[0] > 0)
    check("AC: n = 0 gives None", P.agresti_caffo(1, 0, 1, 10) is None)
    check("mdd: shrinks with n", P.mdd(100, 100) < P.mdd(10, 10))
    check("rate: empty denominator is None, not 0", P.rate(0, 0) is None)
    check("AC lower: n = 0 gives None", P.agresti_coull_lower(0, 0) is None)

    # ---- constructed worlds: pattern verdicts
    def split(cls, arm, pid):
        if arm == "NONE":
            return 0.2
        if cls == "OVERAPPLY":
            return {"A": 0.2, "B": 0.9}.get(arm, 0.9)
        if cls == "EVIDENCE":
            return {"A": 0.9, "B": 0.2}.get(arm, 0.9)
        return 0.6
    res = S(world(split))
    pc = res["per_class"]
    check("world SPLIT: pattern SPLIT", res["pattern"] == "SPLIT")
    check("world SPLIT: P-SPLIT HELD", res["patterns"]["P-SPLIT"] == "HELD")
    check("world SPLIT: OVERAPPLY B, prediction HELD",
          pc["OVERAPPLY"]["verdict"] == "B" and
          pc["OVERAPPLY"]["prediction"] == "HELD")
    check("world SPLIT: EVIDENCE A, prediction HELD",
          pc["EVIDENCE"]["prediction"] == "HELD")
    check("world SPLIT: DETECT TIE -> predicted no-diff HELD",
          pc["DETECT"]["verdict"] == "TIE" and
          pc["DETECT"]["prediction"] == "HELD")
    check("world SPLIT: CITE TIE vs predicted B -> NOT_HELD",
          pc["CITE"]["prediction"] == "NOT_HELD")
    check("world SPLIT: P-CONTROL HELD",
          res["patterns"]["P-CONTROL"] == "HELD")
    check("world SPLIT: P-AB HELD", res["patterns"]["P-AB"] == "HELD")
    check("world SPLIT: kappa 1.0 everywhere, all readable",
          all(p["agreement"]["readable"] for p in pc.values()))

    res = S(world(lambda c, a, p: 0.5))
    check("world flat: ALL_TIE", res["pattern"] == "ALL_TIE")
    check("world flat: control NOT_REACHED, P-CONTROL NOT_HELD",
          all(p["control"] == "NOT_REACHED"
              for p in res["per_class"].values()) and
          res["patterns"]["P-CONTROL"] == "NOT_HELD")
    check("world flat: P-SPLIT NOT_HELD",
          res["patterns"]["P-SPLIT"] == "NOT_HELD")

    res = S(world(lambda c, a, p: 0.5, repeats=10))
    check("world flat k = 10: no TIE (band too narrow for n), UNRESOLVED",
          res["pattern"] == "UNRESOLVED" and
          all(p["verdict"] == "UNRESOLVED"
              for p in res["per_class"].values()))

    wa = lambda c, a, p: {"NONE": 0.2, "A": 0.9, "B": 0.2}.get(a, 0.9)
    res = S(world(wa))
    check("world A wins all: A_DOMINATES", res["pattern"] == "A_DOMINATES")
    wb = lambda c, a, p: {"NONE": 0.2, "A": 0.2, "B": 0.9}.get(a, 0.9)
    check("world B wins all: B_DOMINATES",
          S(world(wb))["pattern"] == "B_DOMINATES")

    def lead(cls, arm, pid):
        if cls == "DETECT":
            return {"NONE": 0.2, "A": 0.9, "B": 0.2}.get(arm, 0.9)
        return {"NONE": 0.2, "A": 0.55, "B": 0.45}.get(arm, 0.55)
    res = S(world(lead))
    check("world A leads, rest open: A_LEADS_INCOMPLETE",
          res["pattern"] == "A_LEADS_INCOMPLETE")
    check("world A leads: P-SPLIT UNRESOLVED",
          res["patterns"]["P-SPLIT"] == "UNRESOLVED")

    def one_probe(cls, arm, pid):
        if arm == "A" and pid.endswith("-1"):
            return 1.0
        if arm == "B" and pid.endswith("-1"):
            return 0.0
        return 0.5
    res = S(world(one_probe))
    r = res["per_class"]["DETECT"]
    check("world one probe carries it: interval excludes 0",
          r["A_vs_B"]["interval"][0] > 0)
    check("world one probe carries it: UNRESOLVED by probe majority",
          r["verdict"] == "UNRESOLVED" and "probe majority"
          in r["A_vs_B"]["reason"])
    check("world one probe: between-probe SD reported",
          r["spread"]["A"]["between_sd"] is not None and
          r["spread"]["A"]["between_sd"] > 0.2)

    res = S(world(lambda c, a, p: 0.5,
                  keep=lambda c, a, p: not p.endswith("-3")))
    check("world two probes only: NOT_EVALUABLE (min probes)",
          res["pattern"] == "NOT_EVALUABLE" and
          res["patterns"]["P-SPLIT"] == "UNTESTED")

    _, key = P.emit(run_tag=TAG)
    res = P.score(key, [[], []], manifest())
    check("world empty: NOT_EVALUABLE", res["pattern"] == "NOT_EVALUABLE")
    check("world empty: no data reads NOT_EVALUABLE, not NOT_READABLE",
          all(p["verdict"] == "NOT_EVALUABLE"
              for p in res["per_class"].values()))
    check("world empty: P-AB and P-CONTROL UNTESTED",
          res["patterns"]["P-AB"] == "UNTESTED" and
          res["patterns"]["P-CONTROL"] == "UNTESTED")

    # ---- kappa gate
    res = S(world(split, flip=lambda c: c == "OVERAPPLY"))
    o = res["per_class"]["OVERAPPLY"]
    check("kappa: inverted coder -> kappa below floor",
          o["agreement"]["min"]["kappa"] < P.KAPPA_FLOOR)
    check("kappa: class NOT_READABLE, prediction NOT_READABLE",
          o["verdict"] == "NOT_READABLE" and
          o["prediction"] == "NOT_READABLE")
    check("kappa: disputed rows counted", res["disputed"] > 0)
    check("kappa: per-coder verdicts still printed",
          res["per_coder"]["c1"]["OVERAPPLY"] == "B")
    check("kappa: imported, not copied",
          P.cohen_kappa.__module__ == "effective_redundancy")

    # ---- interference and order
    def interfere(cls, arm, pid):
        return {"NONE": 0.2, "A": 0.9, "B": 0.5, "AB": 0.1,
                "BA": 0.9}[arm]
    res = S(world(interfere))
    p = res["per_class"]["DETECT"]
    check("world AB worse: AB INTERFERENCE, BA NONE_DETECTED",
          p["combined"]["AB"] == "INTERFERENCE" and
          p["combined"]["BA"] == "NONE_DETECTED")
    check("world AB worse: order effect BA", p["order"]["verdict"] == "BA")
    check("world AB worse: P-AB NOT_HELD",
          res["patterns"]["P-AB"] == "NOT_HELD")

    # ---- leakage
    res = S(world(split, guess=lambda arm, i: arm))
    L1 = res["leak"]["c1"]
    check("leak: perfect guesser LEAK_DETECTED at both grains",
          L1["exact"]["verdict"] == "LEAK_DETECTED" and
          L1["docset"]["verdict"] == "LEAK_DETECTED")
    check("leak: chance exact 0.2, docset 0.4",
          abs(L1["exact"]["chance"] - 0.2) < 1e-9 and
          abs(L1["docset"]["chance"] - 0.4) < 1e-9)
    res = S(world(split, guess=lambda arm, i: "AB"))
    L1 = res["leak"]["c1"]
    check("leak: constant guess 'AB' is no leak at either grain",
          L1["exact"]["verdict"] == "NO_LEAK_DETECTED" and
          L1["docset"]["verdict"] == "NO_LEAK_DETECTED")
    check("leak: all-unsure coder NOT_EVALUABLE, unsure counted",
          res["leak"]["c2"]["exact"]["verdict"] == "NOT_EVALUABLE" and
          res["leak"]["c2"]["unsure"] > 0)
    key, codes = world(split, guess=lambda arm, i: "maybe")
    check("leak: guess outside the set refused",
          _raises(lambda: P.score(key, codes, manifest())))

    # ---- refusals: manifest, run_tag, coders
    key, codes = world(lambda c, a, p: 0.5)
    for f in P.MANIFEST_FIELDS:
        m = manifest()
        del m[f]
        if not _raises(lambda: P.score(key, codes, m)):
            check("manifest: missing %s refused" % f, False)
            break
    else:
        check("manifest: every missing field refused", True)
    check("manifest: one coder declared refused",
          _raises(lambda: P.score(key, codes, manifest(
              coders=[{"id": "c1", "same_model_class": False}]))))
    check("coders: one coder file refused",
          _raises(lambda: P.score(key, codes[:1], manifest())))
    other = [dict(r, run_tag="other") for r in codes[1]]
    check("run_tag: a row from another run refused",
          _raises(lambda: P.score(key, [codes[0], other], manifest())))
    dup = [dict(r, coder="c1") for r in codes[1]]
    check("coders: two files with one coder id refused",
          _raises(lambda: P.score(key, [codes[0], dup], manifest())))
    undecl = [dict(r, coder="zz") for r in codes[1]]
    check("coders: undeclared coder refused",
          _raises(lambda: P.score(key, [codes[0], undecl], manifest())))
    check("score: unknown id refused",
          _raises(lambda: P.score(key, [codes[0] + [{
              "id": "zzz", "run_tag": TAG, "code": "no",
              "coder": "c1"}], codes[1]], manifest())))
    bad = [dict(codes[0][0], code="maybe")] + codes[0][1:]
    check("score: code outside yes/no/unclear refused",
          _raises(lambda: P.score(key, [bad, codes[1]], manifest())))
    blank = [dict(codes[0][0], code="")] + codes[0][1:]
    check("score: blank code is incomplete, not no",
          P.score(key, [blank, codes[1]], manifest())["incomplete"] == 1)

    # ---- render
    res = S(world(split), strip_log=[{"id": key[0]["id"],
                                      "words_removed": 9}])
    out = P.render_score(res)
    check("render: original prefix hash printed with OK",
          P.ORIGINAL_SHA in out and " OK" in out)
    check("render: whole-file hash printed",
          P.predictions_status()["file_sha256"] in out)
    check("render: manifest settings printed", "temperature 1.0" in out)
    check("render: same-class coder caveat printed once",
          out.count("same model class as the authors") == 1)
    check("render: strip counts per arm printed", "strip log" in out)
    check("render: token count labelled APPROXIMATE", "APPROXIMATE" in out)
    check("render: ASCII only", all(ord(ch) < 128 for ch in out))

    # ---- cli
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = P.main(["--selftest"])
    check("cli: --selftest refused with exit 2", rc == 2
          and "test_pathways.py" in buf.getvalue())
    for args in (["--features"], ["--lengths"], ["--choices"]):
        proc = subprocess.run([sys.executable,
                               os.path.join(HERE, "pathways.py")] + args,
                              capture_output=True, text=True)
        check("cli: %s exits 0" % args[0], proc.returncode == 0)
    with tempfile.TemporaryDirectory() as d:
        bp = os.path.join(d, "run.jsonl")
        proc = subprocess.run([sys.executable,
                               os.path.join(HERE, "pathways.py"),
                               "--emit", bp, "--repeats", "3"],
                              capture_output=True, text=True)
        check("cli: --emit without --run-tag refused", proc.returncode == 2)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = P.main(["--score", bp, "--manifest", "m.json", "one.jsonl"])
        check("cli: --score with one coder file refused", rc == 2)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = P.main(["--score", bp, "a.jsonl", "b.jsonl"])
        check("cli: --score without --manifest refused", rc == 2)

    # ---- source hygiene
    src = open(os.path.join(HERE, "pathways.py"), encoding="utf-8").read()
    check("source: pathways.py ASCII only", all(ord(c) < 128 for c in src))
    check("source: no cohen_kappa definition here (imported)",
          "def cohen_kappa" not in src)


if __name__ == "__main__":
    run()
    failed = [n for n, ok in RESULTS if not ok]
    for n, ok in RESULTS:
        print("%s  %s" % ("PASS" if ok else "FAIL", n))
    print("checks: %d   failed: %d" % (len(RESULTS), len(failed)))
    sys.exit(1 if failed else 0)
