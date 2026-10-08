"""test_pathways.py -- checks for pathways.py. CC0. Stdlib only.

Run: python3 test_pathways.py

Every world below is CONSTRUCTED. A world returning the verdict it was
built to return shows the verdict is reachable; it is no evidence about
either pathway.
"""

import hashlib
import io
import json
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
         "date": "2026-10-07", "phase": "main",
         "pilot_run_tag": "p1", "pilot_result": "PILOT_PASS",
         "coders": [{"id": "c1", "same_model_class": False},
                    {"id": "c2", "same_model_class": True}]}
    m.update(over)
    return m


def world(spec, repeats=30, flip=None, guess=None, keep=None, tag=TAG):
    """spec(cls, arm, probe_id) -> GOOD fraction. Two coders.
    flip(cls) -> True: coder 2 inverts yes/no in that class.
    guess(arm, i) -> guessed condition string.
    keep(cls, arm, probe_id) -> False: rows left uncoded."""
    _, key = P.emit(repeats=repeats, run_tag=tag)
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
        c1.append({"id": k["id"], "run_tag": tag, "code": code,
                   "guess": g, "coder": "c1"})
        code2 = code
        if flip and flip(cls):
            code2 = {"yes": "no", "no": "yes"}[code]
        c2.append({"id": k["id"], "run_tag": tag, "code": code2,
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
    check("predictions: six registered layers, all OK",
          len(ps["layers"]) == 6 and ps["all_ok"])
    a1 = data[:8000] + b"X" + data[8001:]
    st = P.predictions_status(a1)
    check("predictions: an edit inside amendment 1 trips that layer only",
          st["layers"][0]["ok"] and not st["layers"][1]["ok"] and
          not any(st["layers"][i]["ok"] for i in (2, 3, 4, 5)))
    check("predictions: text after amendment 4 is flagged past the last layer",
          P.predictions_status(data + b"\nmore\n")["past_last_layer"] and
          P.predictions_status(data + b"\nmore\n")["all_ok"])
    check("predictions: amendment 2 declares AF and the pilot",
          "Length-matched control arm AF" in text and "PILOT_PASS" in text)
    check("predictions: note 1 records the filler sha matching filler(1190)",
          hashlib.sha256(P.filler(1190).encode("utf-8")).hexdigest() in text
          and P.filler_words(P.load_docs()) == 1190)
    check("predictions: note 1 records the P4 split",
          "P4 was split, not removed" in " ".join(text.split()))

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
    check("emit: default k = 30, six arms",
          len(battery) == n_probes * 6 * 30 == len(key))
    check("emit: ids unique", len(set(r["id"] for r in key)) == len(key))
    check("emit: k below 3 refused",
          _raises(lambda: P.emit(repeats=2, run_tag=TAG)))
    check("emit: run_tag required", _raises(lambda: P.emit(run_tag="")))
    check("emit: every row carries the run_tag",
          all(r["run_tag"] == TAG for r in battery + key))
    arms = {k["arm"] for k in key}
    check("emit: arms NONE/A/AF/B/AB/BA", arms == set(P.ARMS) and
          len(arms) == 6)
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
          pab.index(P.load_docs()[P.FILE_A][:200]) <
          pab.index(P._read(P.FILE_B)[:200]))
    check("prompt: no filename in any header",
          "PATHWAY_B" not in pab and ".md" not in
          "\n".join(l for l in pab.splitlines()
                    if l.startswith("Reference document")))
    changed = {P.FILE_A: "edited", P.FILE_B: P._read(P.FILE_B)}
    check("prompt: a changed file is refused",
          _raises(lambda: P.assemble(ab, changed)))

    # ---- AF arm (amendment 2 item 1)
    af = next(r for r in battery if by[r["id"]] == "AF")
    paf = P.assemble(af)
    a_row = next(r for r in battery if by[r["id"]] == "A")
    b_row = next(r for r in battery if by[r["id"]] == "B")
    blk = lambda t: t[:t.index("\nQuestion: ")]
    check("AF: filler words recorded on AF rows only",
          af["filler_words"] > 0 and
          all(r["filler_words"] == 0 for r in battery if by[r["id"]] != "AF"))
    check("AF: one neutral header, A's text then placeholder words",
          paf.count("Reference document") == 1 and
          P.load_docs()[P.FILE_A] + "\n\nlorem ipsum dolor" in paf)
    gap = len(blk(P.assemble(b_row))) - len(blk(paf))
    nxt = len(P.LOREM[af["filler_words"] % len(P.LOREM)]) + 1
    check("AF: block not longer than B's, within one word",
          0 <= gap < nxt)
    check("AF: same probe text as A and B", paf.endswith(a_row["probe"]))
    check("AF: filler deterministic",
          P.filler(5) == "lorem ipsum dolor sit amet" and
          P.filler(len(P.LOREM) + 1).split()[-1] == "lorem")
    texts = P.load_docs()
    short_b = {P.FILE_A: texts[P.FILE_A], P.FILE_B: "tiny"}
    check("AF: B shorter than A gives no filler",
          P.filler_words(short_b) == 0 and P.af_text("x", 0) == "x")

    # ---- pins (amendment 2 item 4)
    edited = dict(texts)
    edited[P.FILE_A] = texts[P.FILE_A] + "\nrevised\n"
    check("pins: emit refuses an A off the registered sha",
          _raises(lambda: P.emit(repeats=3, run_tag=TAG, texts=edited)))
    edited_b = dict(texts)
    edited_b[P.FILE_B] = texts[P.FILE_B].replace("People vary.", "People.")
    check("pins: emit refuses a B off the registered sha",
          _raises(lambda: P.emit(repeats=3, run_tag=TAG, texts=edited_b)))
    check("pins: default A (registered copy) and B match the pins",
          P.check_pins(texts) is texts)
    check("pins: default A is the registered copy, not the working copy",
          P.load_docs()[P.FILE_A] == P._read(P.REGISTERED_A))
    live = {P.FILE_A: P._read(P.FILE_A), P.FILE_B: texts[P.FILE_B]}
    st = P.live_status()
    check("pins: live A reported; refused at emit iff off the pin",
          st["is_registered"] ==
          (not _raises(lambda: P.emit(repeats=3, run_tag=TAG, texts=live))))
    check("pins: live A line printed in features, lengths and score",
          "LIVE" in P.render_features(P.locate_features()) and
          "LIVE" in P.render_lengths(P.lengths()))
    with tempfile.TemporaryDirectory() as d:
        good_a = os.path.join(d, "a.md")
        bad_a = os.path.join(d, "a2.md")
        with open(good_a, "w", encoding="utf-8", newline="") as fh:
            fh.write(texts[P.FILE_A])
        with open(bad_a, "w", encoding="utf-8", newline="") as fh:
            fh.write(edited[P.FILE_A])
        check("pins: --a-file with the registered bytes loads",
              P.load_docs(good_a)[P.FILE_A] == texts[P.FILE_A])
        bp = os.path.join(d, "run.jsonl")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = P.main(["--emit", bp, "--run-tag", "x", "--repeats", "3",
                         "--a-file", bad_a])
        check("pins: cli --emit with a revised --a-file refused, exit 1",
              rc == 1 and "registered" in buf.getvalue() and
              not os.path.exists(bp))
        with redirect_stdout(io.StringIO()):
            rc = P.main(["--emit", bp, "--run-tag", "x", "--repeats", "3",
                         "--a-file", good_a])
        check("pins: cli --emit with the registered --a-file writes",
              rc == 0 and os.path.exists(bp))
        rid = P._jsonl(bp)[0]["id"]
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = P.main(["--prompt", bp, rid, "--a-file", good_a])
        check("pins: cli --prompt accepts --a-file", rc == 0 and
              "Question: " in buf.getvalue())
    sh = P.sheet(battery)
    check("sheet: keys fixed",
          all(set(r) == {"id", "run_tag", "class", "field", "probe",
                         "response", "code", "guess", "coder"} for r in sh))
    check("sheet: no field value is an arm name",
          not any(str(v) in P.ARMS for r in sh for v in r.values()))

    # ---- lengths
    L = P.lengths()
    check("lengths: A, AF, B, A+B measured",
          all(L[k]["chars"] > 0 for k in ("A", "AF", "B", "A+B")))
    check("lengths: AF within one word of B, A shorter",
          L["A"]["chars"] < L["AF"]["chars"] <= L["B"]["chars"] and
          L["B"]["chars"] - L["AF"]["chars"] <= max(len(w) for w in P.LOREM))
    check("lengths: A+B at least A + B chars",
          L["A+B"]["chars"] >= L["A"]["chars"] + L["B"]["chars"])
    check("lengths: render labels tokens APPROXIMATE",
          "APPROXIMATE" in P.render_lengths(L))

    # ---- strip
    g = P.doc_grams()
    words = P.load_docs()[P.FILE_A].split()
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
    lor = P.filler(40).split()[3:13]
    check("strip: a 10-word filler run is removed",
          P.strip_text("x " + " ".join(lor) + " y", g)[1] == 10)
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

    # ---- attribution (amendment 2 item 1)
    at = P.attribution
    check("attribution: all five states from the table",
          at("A", "AF") == "STRUCTURE_SURVIVES" and
          at("B", "B") == "STRUCTURE_SURVIVES" and
          at("A", "TIE") == "NOT_SEPARABLE_FROM_VOLUME" and
          at("A", "B") == "NOT_SEPARABLE_FROM_VOLUME" and
          at("B", "AF") == "NOT_SEPARABLE_FROM_VOLUME" and
          at("TIE", "TIE") == "TIE_SURVIVES" and
          at("TIE", "AF") == "TIE_NOT_SURVIVING" and
          at("A", "UNRESOLVED") == "UNRESOLVED" and
          at("NOT_READABLE", "TIE") == "UNRESOLVED" and
          at("TIE", "NOT_EVALUABLE") == "UNRESOLVED")
    struct = lambda c, a, p: {"NONE": 0.2, "A": 0.9, "AF": 0.9,
                              "B": 0.2}.get(a, 0.9)
    res = S(world(struct))
    d = res["per_class"]["DETECT"]
    check("world AF = A: A wins, AF wins, STRUCTURE_SURVIVES, A vs AF TIE",
          d["verdict"] == "A" and d["AF_vs_B_verdict"] == "AF" and
          d["attribution"] == "STRUCTURE_SURVIVES" and
          d["A_vs_AF_verdict"] == "TIE")
    vol = lambda c, a, p: {"NONE": 0.2, "A": 0.9, "AF": 0.2,
                           "B": 0.2}.get(a, 0.9)
    d = S(world(vol))["per_class"]["DETECT"]
    check("world AF = B: A wins, AF vs B TIE, NOT_SEPARABLE_FROM_VOLUME",
          d["verdict"] == "A" and d["AF_vs_B_verdict"] == "TIE" and
          d["attribution"] == "NOT_SEPARABLE_FROM_VOLUME" and
          d["A_vs_AF_verdict"] == "A")
    tie_ns = lambda c, a, p: {"AF": 0.9}.get(a, 0.5)
    d = S(world(tie_ns))["per_class"]["DETECT"]
    check("world A = B, AF differs: TIE_NOT_SURVIVING",
          d["verdict"] == "TIE" and d["attribution"] == "TIE_NOT_SURVIVING")
    d = S(world(lambda c, a, p: 0.5))["per_class"]["DETECT"]
    check("world flat: TIE_SURVIVES", d["attribution"] == "TIE_SURVIVES")

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
        return {"NONE": 0.2, "A": 0.9, "AF": 0.9, "B": 0.5, "AB": 0.1,
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
    check("leak: chance exact 1/6, docset 1/3 (AF counts as A)",
          abs(L1["exact"]["chance"] - 1 / 6.0) < 1e-9 and
          abs(L1["docset"]["chance"] - 1 / 3.0) < 1e-9)
    res = S(world(split, guess=lambda arm, i: "A" if arm == "AF" else arm))
    L1 = res["leak"]["c1"]
    check("leak: guessing A for AF misses exact, hits docset",
          L1["exact"]["accuracy"] < 1.0 and
          abs(L1["docset"]["accuracy"] - 1.0) < 1e-9)
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
    check("manifest: phase outside pilot/main refused",
          _raises(lambda: P.score(key, codes, manifest(phase="trial"))))
    nopilot = manifest()
    del nopilot["pilot_run_tag"]
    check("manifest: main without pilot_run_tag refused",
          _raises(lambda: P.score(key, codes, nopilot)))
    check("manifest: main with pilot_run_tag == run_tag refused",
          _raises(lambda: P.score(key, codes, manifest(pilot_run_tag=TAG))))
    check("manifest: main after PILOT_FAIL refused",
          _raises(lambda: P.score(key, codes,
                                  manifest(pilot_result="PILOT_FAIL"))))
    blank = [dict(codes[0][0], code="")] + codes[0][1:]
    check("score: blank code is incomplete, not no",
          P.score(key, [blank, codes[1]], manifest())["incomplete"] == 1)

    # ---- pilot (amendment 2 item 2)
    pm = lambda: manifest(run_tag="p1", phase="pilot")
    pk, pc3 = world(lambda c, a, p: 0.5, repeats=3, tag="p1")
    pr = P.score(pk, pc3, pm())
    check("pilot: perfect agreement, no leak -> PILOT_PASS",
          pr["pilot_result"] == "PILOT_PASS" and not pr["pilot_reasons"])
    check("pilot: no verdict, prediction or pattern computed",
          "per_class" not in pr and "pattern" not in pr)
    check("pilot: ~54 rows per class at k = 3 over all arms",
          pr["agreement"]["DETECT"]["min"]["n"] == 3 * 6 * 3)
    check("pilot: all-unsure coders named as leak-unchecked [CHOICE 15]",
          set(pr["leak_unchecked"]) == {"c1", "c2"})
    out = P.render_score(pr)
    check("pilot render: gate printed, no pattern or prediction",
          "gate: PILOT_PASS" in out and "pattern:" not in out and
          "predicted" not in out and "interval" not in out and
          "PILOT" in out.splitlines()[0])
    pk, pc3 = world(lambda c, a, p: 0.5, repeats=3, tag="p1",
                    flip=lambda c: c == "CITE")
    pr = P.score(pk, pc3, pm())
    check("pilot: kappa below floor in one class -> PILOT_FAIL naming it",
          pr["pilot_result"] == "PILOT_FAIL" and
          any(r.startswith("CITE:") for r in pr["pilot_reasons"]))
    pk, pc3 = world(lambda c, a, p: 0.5, repeats=3, tag="p1",
                    guess=lambda arm, i: arm)
    pr = P.score(pk, pc3, pm())
    check("pilot: a leaking coder -> PILOT_FAIL naming the coder",
          pr["pilot_result"] == "PILOT_FAIL" and
          any("c1: LEAK_DETECTED" in r for r in pr["pilot_reasons"]))
    pk, pc3 = world(lambda c, a, p: 0.5, repeats=4, tag="p1")
    check("pilot: a key with k != 3 refused",
          _raises(lambda: P.score(pk, pc3, pm())))
    pk, pc3 = world(lambda c, a, p: 0.5, repeats=3, tag="p1")
    sub_k = [k for k in pk if k["arm"] != "AF"]
    ids = set(k["id"] for k in sub_k)
    check("pilot: a key missing an arm refused",
          _raises(lambda: P.score(sub_k, [[r for r in c if r["id"] in ids]
                                         for c in pc3], pm())))
    check("pilot: its rows refused by a main score (run_tag)",
          _raises(lambda: P.score(pk, pc3, manifest())))

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
    check("render: every registered layer printed",
          out.count("registered ") >= 3 and "amendment 2" in out)
    check("render: length control and attribution printed",
          "AF vs B" in out and "attribution of A vs B" in out)
    check("render: pilot run named, excluded",
          "pilot run p1: PILOT_PASS" in out)
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

    # ---- runner job (amendment 3)
    runner_checks()

    # ---- source hygiene
    src = open(os.path.join(HERE, "pathways.py"), encoding="utf-8").read()
    check("source: pathways.py ASCII only", all(ord(c) < 128 for c in src))
    check("source: no cohen_kappa definition here (imported)",
          "def cohen_kappa" not in src)


def dispatch_prompt(job, item):
    """The dispatch's assembly, written here from its text, not imported."""
    docs = item["docs"]
    if docs:
        docs_text = job["doc_separator"].join(job["documents"][k]
                                              for k in docs)
    else:
        docs_text = job["no_doc_text"]
    out = job["template"].replace("{DOCUMENTS}", docs_text)
    return out.replace("{QUESTION}", item["question"])


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fake_results(job, plan):
    """plan(item) -> (status, text) or None for no row."""
    rows = []
    for i, it in enumerate(job["items"]):
        p = plan(it)
        if p is None:
            continue
        st, text = p
        rows.append({"index": i, "item_id": it["id"], "arm": it["arm"],
                     "class": it["class"], "probe": it["probe"],
                     "repeat": it["repeat"], "status": st, "text": text,
                     "truncated": False, "model_tier_applied": "default",
                     "prompt_sha256": it["prompt_sha256"],
                     "started_at": "2026-10-08T10:00:00Z",
                     "finished_at": "2026-10-08T10:00:05Z"})
    return rows


def runner_checks():
    tag = "pilot-test"
    job = json.loads(json.dumps(P.emit_job(tag, "pilot")))   # round trip
    items = job["items"]
    check("job: format, run_tag, phase, tier, template fields",
          job["format"] == "pathways-run/1" and job["run_tag"] == tag and
          job["phase"] == "pilot" and job["model_tier"] == "default" and
          job["template"] == "{DOCUMENTS}Question: {QUESTION}" and
          job["doc_separator"] == "" and job["no_doc_text"] == "" and
          "seed" not in job)
    check("job: pilot has 5 classes x 3 probes x 6 arms x 3 = 270 items",
          len(items) == 270 and
          set(it["arm"] for it in items) == set(P.ARMS) and
          set(it["repeat"] for it in items) == {1, 2, 3})
    check("job: every item hashes to its prompt_sha256 under the "
          "dispatch's assembly",
          all(sha(dispatch_prompt(job, it)) == it["prompt_sha256"]
              for it in items))
    battery, key = P.emit(3, "hsp", tag)
    by = {r["id"]: r for r in battery}
    check("job: ids equal --emit's for the same salt and run_tag",
          set(it["id"] for it in items) == set(by))
    check("job: every prompt is byte-identical to the harness's assemble",
          all(dispatch_prompt(job, it) == P.assemble(by[it["id"]])
              for it in items))
    check("job: key from the job equals --emit's key",
          sorted(P.job_key(job), key=lambda k: k["id"]) ==
          sorted(key, key=lambda k: k["id"]))
    head = job["documents_source"]["wrap_head"]
    tail = job["documents_source"]["wrap_tail"]
    raw = {k: v[len(head):-len(tail)] for k, v in job["documents"].items()}
    check("job: A and B unwrap to their pins",
          sha(raw["A"]) == P.PINNED[P.FILE_A] and
          sha(raw["B"]) == P.PINNED[P.FILE_B] and
          all(v.startswith(head) and v.endswith(tail)
              for v in job["documents"].values()))
    check("job: AF unwraps to the af_text recorded in amendment 2 note 1",
          sha(raw["AF"]) == "e570b26d5659dba21c6feb791fc310c53f9d8a699035e7"
                            "120485167a1179a745" and
          job["documents_source"]["AF"]["filler_words"] == 1190)
    check("job: no document label carries a number or a filename",
          all("Reference document:" in v and "Reference document 1" not in v
              and "PATHWAY_B" not in v[:60] for v in job["documents"].values()))
    none = next(it for it in items if it["arm"] == "NONE")
    check("job: NONE prompt is 'Question: ' + the probe",
          dispatch_prompt(job, none) == "Question: " + none["question"])
    ab = next(it for it in items if it["arm"] == "AB")
    ba = next(it for it in items if it["arm"] == "BA")
    check("job: AB and BA list the documents in opposite order",
          ab["docs"] == ["A", "B"] and ba["docs"] == ["B", "A"])
    ids = [it["id"] for it in items]
    check("job: items ordered by opaque id, not grouped by arm",
          ids == sorted(ids) and
          [it["arm"] for it in items[:6]] != list(P.ARMS))
    check("job: a pilot with k != 3 is refused",
          _raises(lambda: P.emit_job(tag, "pilot", repeats=4)))
    check("job: an unknown phase is refused",
          _raises(lambda: P.emit_job(tag, "warmup")))
    check("job: a non-integer seed is refused",
          _raises(lambda: P.emit_job(tag, "pilot", seed="7")))
    check("job: an integer seed is recorded",
          P.emit_job(tag, "pilot", seed=7)["seed"] == 7)
    check("job: a main job at k = 3 is allowed",
          len(P.emit_job("main-test", "main", repeats=3)["items"]) == 270)
    texts = P.load_docs()
    bad = {P.FILE_A: texts[P.FILE_A] + " {QUESTION}",
           P.FILE_B: texts[P.FILE_B]}
    pins = {f: P._sha_text(v) for f, v in bad.items()}
    check("job: a document holding a placeholder is refused",
          _raises(lambda: P.emit_job(tag, "pilot", texts=bad, pins=pins)))
    check("job: --emit-job refuses an A off the pin",
          _raises(lambda: P.emit_job(tag, "pilot", texts={
              P.FILE_A: texts[P.FILE_A] + "x", P.FILE_B: texts[P.FILE_B]})))
    tamper = json.loads(json.dumps(job))
    tamper["documents"]["B"] = tamper["documents"]["B"].replace("e", "E", 1)
    check("job: check_job refuses a job whose documents changed",
          _raises(lambda: P.check_job(tamper)))
    check("job: check_job passes the job as written", P.check_job(job))
    tamper2 = json.loads(json.dumps(job))
    tamper2["no_doc_text"] = "(no documents)"
    n_none = sum(1 for it in items if it["arm"] == "NONE")
    check("job: a runner default for an empty no_doc_text breaks exactly "
          "the NONE hashes",
          sum(1 for it in items if sha(dispatch_prompt(tamper2, it)) !=
              it["prompt_sha256"]) == n_none == 45)

    # ---- import
    arms_seen = {}

    def plan(it):
        n = arms_seen.get(it["arm"], 0)
        arms_seen[it["arm"]] = n + 1
        if it["arm"] == "AB" and n == 0:
            return ("prompt_too_large", "")
        if it["arm"] == "BA" and n == 0:
            return None
        if it["arm"] == "A" and n == 0:
            return ("error", "")
        if it["arm"] == "B" and n == 0:
            return ("hash_mismatch", "")
        if it["arm"] == "NONE" and n == 0:
            return ("refused", "I can't help with that.")
        if it["arm"] == "AF" and n == 0:
            return ("empty", "")
        return ("answered", "response to %s" % it["id"])

    res = fake_results(job, plan)
    jsha = hashlib.sha256(json.dumps(job).encode("utf-8")).hexdigest()
    sheet_rows, k2, rep = P.import_runner(job, res, jsha)
    check("import: 4 NOT_DELIVERED (error, hash_mismatch, too large, "
          "no row), 266 delivered, 264 on the sheet (refused and empty off)",
          rep["not_delivered"] == 4 and rep["delivered"] == 266 and
          len(sheet_rows) == 264 and rep["on_sheet"] == 264 and
          rep["per_arm"]["AB"]["prompt_too_large"] == 1 and
          rep["per_arm"]["BA"]["no_row"] == 1 and
          rep["per_arm"]["A"]["error"] == 1 and
          rep["per_arm"]["B"]["hash_mismatch"] == 1)
    st = {r["runner_status"] for r in sheet_rows}
    kst = {}
    for k in k2:
        kst[k["runner_status"]] = kst.get(k["runner_status"], 0) + 1
    check("import: refused and empty are off the sheet; the key carries "
          "every status (amendment 4 item 4)",
          st == {"answered"} and kst == {
              "answered": 264, "refused": 1, "empty": 1, "error": 1,
              "hash_mismatch": 1, "prompt_too_large": 1, "no_row": 1} and
          all(k["job_sha256"] == jsha for k in k2))
    check("import: refused rows with text are counted",
          rep["fixed_with_text"]["NONE"] == 1 and
          sum(rep["fixed_with_text"].values()) == 1)
    check("import: sheet carries no arm and no context",
          all("arm" not in r and "docs" not in r and "context_files" not in r
              for r in sheet_rows))
    check("import: sheet ordered by opaque id",
          [r["id"] for r in sheet_rows] ==
          sorted(r["id"] for r in sheet_rows))
    check("import: key covers every job item",
          len(k2) == 270 and {k["id"] for k in k2} == set(ids))
    check("import: tier counts over delivered items",
          rep["model_tier_applied_counts"] == {"default": 266})
    check("import: render names NOT_DELIVERED",
          "NOT_DELIVERED 4" in P.render_import(rep))

    def mutate(fn):
        rows = json.loads(json.dumps(res))
        fn(rows)
        return lambda: P.import_runner(job, rows)

    ok = [r for r in res if r["status"] == "answered"]
    i0 = res.index(ok[0])
    check("import refuses: arm disagrees with the job",
          _raises(mutate(lambda r: r[i0].update(arm="NONE" if
                  r[i0]["arm"] != "NONE" else "A"))))
    check("import refuses: duplicate item_id",
          _raises(mutate(lambda r: r.append(dict(r[i0])))))
    check("import refuses: unknown status",
          _raises(mutate(lambda r: r[i0].update(status="timeout"))))
    check("import refuses: answered with blank text",
          _raises(mutate(lambda r: r[i0].update(text="  "))))
    check("import refuses: empty with text",
          _raises(mutate(lambda r: [x.update(text="hi") for x in r
                                    if x["status"] == "empty"])))
    check("import refuses: delivered under another prompt_sha256",
          _raises(mutate(lambda r: r[i0].update(prompt_sha256="0" * 64))))
    check("import refuses: item not in the job",
          _raises(mutate(lambda r: r[i0].update(item_id="zzzzzzzzzzzz"))))
    check("import refuses: a missing field",
          _raises(mutate(lambda r: r[i0].pop("truncated"))))
    check("import refuses: a job that fails its own hashes",
          _raises(lambda: P.import_runner(tamper, res)))

    # ---- runner manifest
    stub = P.manifest_stub(rep)
    check("manifest stub: runner strings, tier fields, date from results",
          stub["model"] == P.RUNNER_MODEL and
          stub["temperature"] == "PLATFORM_DEFAULT_NOT_SETTABLE" and
          stub["system_prompt"] == "PLATFORM_FRAMING_NOT_VISIBLE" and
          stub["model_tier_requested"] == "default" and
          stub["date"] == "2026-10-08")
    check("manifest stub: refused until coders are filled",
          _raises(lambda: P.check_manifest(stub)))
    check("manifest stub: job sha256 and blind from the job (default "
          "salt -> COMPROMISED), size_check empty",
          stub["job_sha256"] == jsha and stub["blind"] == "COMPROMISED" and
          stub["size_check"] == {})
    sc = P.size_check(job, 200000, 4096, "constructed for the test", jsha)
    full = dict(stub, coders=[{"id": "c1", "same_model_class": True},
                              {"id": "c2", "same_model_class": False}],
                size_check=sc)
    check("runner manifest: accepted with coders and a PASS size check",
          P.check_manifest(full))
    check("runner manifest: missing job_sha256 refused",
          _raises(lambda: P.check_manifest(dict(full, job_sha256=""))))
    check("runner manifest: blind outside SEALED/COMPROMISED refused",
          _raises(lambda: P.check_manifest(dict(full, blind="PARTIAL"))))
    check("runner manifest: no size check refused",
          _raises(lambda: P.check_manifest(dict(full, size_check={}))))
    check("runner manifest: a REFUSED size check refused",
          _raises(lambda: P.check_manifest(dict(
              full, size_check=P.size_check(job, 20000, 0, "t", jsha)))))
    check("runner manifest: a size check for another job refused",
          _raises(lambda: P.check_manifest(dict(
              full, size_check=dict(sc, job_sha256="0" * 64)))))
    check("runner manifest: main run on a COMPROMISED job refused",
          _raises(lambda: P.check_manifest(dict(
              full, phase="main", pilot_run_tag="p0",
              pilot_result="PILOT_PASS"))))
    check("runner manifest: main run on a SEALED job accepted",
          P.check_manifest(dict(full, phase="main", pilot_run_tag="p0",
                                pilot_result="PILOT_PASS", blind="SEALED")))
    check("runner manifest: two applied tiers refused",
          _raises(lambda: P.check_manifest(dict(
              full, model_tier_applied_counts={"default": 200,
                                               "other": 66}))))
    check("runner manifest: applied tier other than requested refused",
          _raises(lambda: P.check_manifest(dict(
              full, model_tier_applied_counts={"other": 266}))))
    check("runner manifest: sentinel settings without tier fields refused",
          _raises(lambda: P.check_manifest(dict(
              manifest(), temperature="PLATFORM_DEFAULT_NOT_SETTABLE"))))
    check("runner manifest: zero count refused",
          _raises(lambda: P.check_manifest(dict(
              full, model_tier_applied_counts={"default": 0}))))
    check("non-runner manifest unchanged: numbers still accepted",
          P.check_manifest(manifest()))
    coded = []
    for name in ("c1", "c2"):
        coded.append([dict(r, code="yes", guess="unsure", coder=name)
                      for r in sheet_rows])
    pres = P.score(k2, coded, full)
    out = P.render_pilot(pres)
    check("end to end: imported sheet scores as a pilot under the runner "
          "manifest",
          "runner: model tier requested 'default'" in out and
          "single platform" in out)
    check("pilot on a COMPROMISED job cannot pass, and says why",
          pres["pilot_result"] == "PILOT_FAIL" and
          any("blind COMPROMISED" in r for r in pres["pilot_reasons"]) and
          "delivery per class per arm" in out)
    sres = P.score(k2, coded, dict(full, blind="SEALED"))
    check("the same pilot on a SEALED job carries no blind reason",
          not any("blind" in r for r in sres["pilot_reasons"]))
    for bad_status in ("refused", "empty", "error"):
        rid = [k["id"] for k in k2 if k["runner_status"] == bad_status][0]
        bad = [rows + [{"id": rid, "run_tag": tag, "code": "no",
                        "guess": "", "coder": rows[0]["coder"]}]
               for rows in coded]
        check("score refuses a coder code on a %s row" % bad_status,
              _raises(lambda: P.score(k2, bad, full)))
    other = [dict(k, job_sha256="1" * 64) for k in k2]
    check("score refuses a key from another job",
          _raises(lambda: P.score(other, coded, full)))
    dl = P.delivery(k2)
    check("delivery: per class per arm counts sum to the job",
          sum(dl[c][a][f] for c in P.CLASSES for a in P.ARMS
              for f in ("delivered", "not_delivered")) == 270 and
          sum(dl[c][a]["fixed"] for c in P.CLASSES for a in P.ARMS) == 2)
    check("delivery: None for a key not from the runner",
          P.delivery([{k2[0]["id"]: 1, "class": "DETECT", "arm": "A"}])
          is None)
    zero = {"delivered": 9, "not_delivered": 0, "fixed": 0}
    dlx = {c: {a: dict(zero) for a in P.ARMS} for c in P.CLASSES}
    dlx["CITE"]["AB"] = {"delivered": 8, "not_delivered": 1, "fixed": 0}
    dlx["CITE"]["A"] = {"delivered": 9, "not_delivered": 0, "fixed": 2}
    check("flags: loss differs by one -> LOSS_DIFFERENTIAL",
          P.contrast_flags(dlx, "CITE", "AB", "BA") == ["LOSS_DIFFERENTIAL"])
    check("flags: fixed codes differ -> OUTCOME_DIFFERENTIAL",
          P.contrast_flags(dlx, "CITE", "A", "B") ==
          ["OUTCOME_DIFFERENTIAL"])
    check("flags: equal arms carry none; another class carries none",
          P.contrast_flags(dlx, "CITE", "B", "BA") == [] and
          P.contrast_flags(dlx, "DETECT", "AB", "A") == [] and
          P.contrast_flags(None, "CITE", "AB", "BA") == [])
    mm = dict(full, phase="main", pilot_run_tag="p0",
              pilot_result="PILOT_PASS", blind="SEALED")
    mres = P.score(k2, coded, mm)
    fixed_ids = {k["id"]: k for k in k2
                 if k["runner_status"] in P.FIXED_STATUSES}
    ok = True
    for k in fixed_ids.values():
        c = mres["per_class"][k["class"]]["counts"][k["arm"]]
        if c["no"] < 1:
            ok = False
    check("main score: refused and empty enter the counts as 'no'", ok)
    ok = True
    for cls, p in mres["per_class"].items():
        for r in (p["A_vs_B"], p["A_vs_AF"], p["AF_vs_B"], p["A_vs_NONE"],
                  p["B_vs_NONE"], p["order"]):
            if r["flags"] != P.contrast_flags(dl, cls, r["first"],
                                              r["second"]):
                ok = False
    check("main score: every contrast carries its delivery flags", ok)
    check("main score: a sensitivity verdict excludes fixed rows",
          all(p["A_vs_B_excl_fixed"] is not None
              for p in mres["per_class"].values()))
    mout = P.render_score(mres)
    check("main render: delivery table, sensitivity and blind line",
          "delivery per class per arm" in mout and
          "sensitivity (amendment 4 item 4)" in mout and
          "blind SEALED" in mout and "size check PASS" in mout)

    # ---- size check
    und = P.size_check(job)
    check("size check: no declared limit -> REFUSED_UNDECLARED",
          und["verdict"] == "REFUSED_UNDECLARED" and
          set(und["undeclared"]) == {"context_limit", "reserve_output",
                                     "limit_source"})
    check("size check: per-arm maximum bytes; AB and BA are the longest",
          sc["per_arm"]["AB"]["max_bytes"] == sc["per_arm"]["BA"]["max_bytes"]
          == sc["max_item_bytes"] and
          sc["per_arm"]["NONE"]["max_bytes"] < sc["per_arm"]["A"]["max_bytes"]
          < sc["per_arm"]["B"]["max_bytes"] < sc["max_item_bytes"])
    tight = P.size_check(job, 20000, 0, "t", jsha)
    check("size check: a limit between B and AB refuses exactly AB and BA",
          tight["verdict"] == "REFUSED_ITEM_EXCEEDS" and
          {e["arm"] for e in tight["exceeding"]} == {"AB", "BA"} and
          len(tight["exceeding"]) == 90)
    edge = P.size_check(job, sc["max_item_bytes"] + 10, 10, "t", jsha)
    check("size check: reserve counts against the limit (exact fit passes, "
          "one byte less refuses)",
          edge["verdict"] == "PASS" and
          P.size_check(job, sc["max_item_bytes"] + 9, 10, "t",
                       jsha)["verdict"] == "REFUSED_ITEM_EXCEEDS")
    check("size check: a non-integer limit is refused",
          _raises(lambda: P.size_check(job, "200k", 0, "t", jsha)))
    check("size check: render names the verdict",
          "REFUSED_UNDECLARED" in P.render_size_check(und) and
          "verdict PASS" in P.render_size_check(sc))

    # ---- blind
    check("blind: default salt -> COMPROMISED",
          P.blind_default(job) == "COMPROMISED")
    gen = P.emit_job(tag, "pilot", salt="f" * 32, salt_source="generated")
    check("blind: generated salt -> SEALED; ids differ from the public salt",
          P.blind_default(gen) == "SEALED" and
          not ({it["id"] for it in gen["items"]} & set(ids)))
    old = json.loads(json.dumps(job))
    old["harness"].pop("salt_source")
    check("blind: a job with no salt_source (e.g. 2026-10-08a) -> "
          "COMPROMISED", P.blind_default(old) == "COMPROMISED")
    check("blind: a generated label on the public salt is COMPROMISED",
          P.blind_default(P.emit_job(tag, "pilot",
                                     salt_source="generated"))
          == "COMPROMISED")
    gi = os.path.join(HERE, "runs", ".gitignore")
    check("runs/.gitignore ignores everything but itself",
          os.path.exists(gi) and
          open(gi).read().split() == ["*", "!.gitignore"])

    with tempfile.TemporaryDirectory() as d:
        jp = os.path.join(d, "job.json")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = P.main(["--emit-job", jp, "--run-tag", "cli-pilot"])
        cj = json.load(open(jp, encoding="utf-8"))
        check("cli: --emit-job writes a pilot job", rc == 0 and
              len(cj["items"]) == 270 and cj["run_tag"] == "cli-pilot")
        check("cli: --emit-job generates a salt by default (SEALED) and "
              "prints the job sha256",
              cj["harness"]["salt_source"] == "generated" and
              cj["harness"]["salt"] != "hsp" and
              len(cj["harness"]["salt"]) == 32 and
              P.job_bytes_sha(jp) in buf.getvalue() and
              "Do not commit this file" in buf.getvalue())
        jp2 = os.path.join(d, "job2.json")
        with redirect_stdout(io.StringIO()):
            P.main(["--emit-job", jp2, "--run-tag", "cli-pilot"])
        check("cli: two default emissions do not share ids",
              not ({it["id"] for it in cj["items"]} &
                   {it["id"] for it in json.load(open(jp2))["items"]}))
        recp = os.path.join(d, "size.json")
        with redirect_stdout(io.StringIO()):
            rc_u = P.main(["--size-check", jp])
            rc_p = P.main(["--size-check", jp, "--context-limit", "200000",
                           "--reserve-output", "4096", "--limit-source",
                           "test", "--out", recp])
        rec = json.load(open(recp))
        check("cli: --size-check rc 1 undeclared, rc 0 PASS with --out",
              rc_u == 1 and rc_p == 0 and rec["verdict"] == "PASS" and
              rec["job_sha256"] == P.job_bytes_sha(jp))
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc_v = P.main(["--reveal", jp, "--expect", P.job_bytes_sha(jp)])
            rc_m = P.main(["--reveal", jp, "--expect", "0" * 64])
        check("cli: --reveal VERIFIED rc 0, MISMATCH rc 1",
              rc_v == 0 and rc_m == 1 and "VERIFIED" in buf.getvalue() and
              "MISMATCH" in buf.getvalue())
        rp = os.path.join(d, "res.jsonl")
        P._write_jsonl(rp, fake_results(
            cj, lambda it: ("answered", "r %s" % it["id"])))
        sp, kp, mp = (os.path.join(d, x) for x in
                      ("sheet.jsonl", "key.jsonl", "m.json"))
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = P.main(["--import-runner", rp, "--job", jp, "--sheet", sp,
                         "--key", kp, "--manifest-stub", mp])
        st_ = json.load(open(mp))
        check("cli: --import-runner writes sheet, key and stub; stub carries "
              "the job file's sha256 and SEALED",
              rc == 0 and len(P._jsonl(sp)) == 270 and
              st_["model_tier_applied_counts"] == {"default": 270} and
              st_["job_sha256"] == P.job_bytes_sha(jp) and
              st_["blind"] == "SEALED")
        # A flag passed where a path belongs is refused and never becomes a
        # file name. Run from inside d so a stray "--out" would land here.
        cwd = os.getcwd()
        bad_calls = [
            ["--import-runner", rp, "--job", jp, "--sheet", "--out",
             "--key", kp],
            ["--import-runner", rp, "--job", jp, "--sheet=--out",
             "--key", kp],
            ["--import-runner", rp, "--job", jp, "--sheet", sp,
             "--key", kp, "--manifest-stub", "--out"],
            ["--import-runner", rp, "--job", jp, sp, kp, "--out", mp],
            ["--import-runner", rp, "--job", jp, "--sheet", sp,
             "--key", sp],
        ]
        rcs = []
        try:
            os.chdir(d)
            for call in bad_calls:
                with redirect_stdout(io.StringIO()):
                    rcs.append(P.main(call))
        finally:
            os.chdir(cwd)
        check("cli: --import-runner refuses a path starting with '--' "
              "(rc 2 on every form, no file named --out)",
              rcs == [2] * len(bad_calls) and
              not os.path.exists(os.path.join(d, "--out")) and
              not os.path.exists(os.path.join(cwd, "--out")))
        check("cli: --import-runner refuses the old positional SHEET KEY form",
              rcs[3] == 2)
        ok = True
        try:
            P._import_runner_args([rp, "--job", jp, "--sheet=--out",
                                   "--key", kp])
            ok = False
        except ValueError:
            pass
        check("cli: _import_runner_args raises ValueError on '--' path", ok)
        with redirect_stdout(io.StringIO()):
            rc = P.main(["--emit-job", jp])
        check("cli: --emit-job without --run-tag refused", rc == 2)


if __name__ == "__main__":
    run()
    failed = [n for n, ok in RESULTS if not ok]
    for n, ok in RESULTS:
        print("%s  %s" % ("PASS" if ok else "FAIL", n))
    print("checks: %d   failed: %d" % (len(RESULTS), len(failed)))
    sys.exit(1 if failed else 0)
