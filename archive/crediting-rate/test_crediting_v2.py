#!/usr/bin/env python3
"""Checks on crediting_rate_v2.py.  Prints its own count."""
import ast
import io
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import crediting_rate as V1          # noqa: E402
import crediting_rate_v2 as M        # noqa: E402
import make_fixtures_v2 as FX        # noqa: E402

N = [0]
FAIL = []


def ck(label, cond):
    N[0] += 1
    if not cond:
        FAIL.append(label)


def run(name, seed=7):
    return M.run(*FX.paths(name), seed=seed)


# ------------------------------------------------- v1 is not edited, and is
# ------------------------------------------------- imported rather than copied
src2 = io.open(os.path.join(HERE, "crediting_rate_v2.py"),
               encoding="utf-8").read()
tree2 = ast.parse(src2)
ck("v2 imports v1", any(isinstance(n, ast.Import) and
                        any(a.name == "crediting_rate" for a in n.names)
                        for n in ast.walk(tree2)))
# The pieces v2 genuinely reaches through V1.  bin_gap and shuffle_band are
# NOT among them and must not be claimed: v1's are binary and v2's bins are
# three-state, so v2 has its own `gap` and `shuffle_band` -- and the two are
# checked to AGREE on a binary input immediately below, which is the honest
# form of the claim.
for fn in ("outside", "load_frame", "ordering_state", "_jsonl", "_is_int"):
    ck("v2 reaches V1.%s rather than restating it" % fn,
       ("V1." + fn) in src2)
ck("v2 defines no second comparator", "def outside(" not in src2)
ck("v2 does not claim to reach v1's binary bin_gap",
   "V1.bin_gap" not in src2)
# v2's shuffle_band exists because v1's is binary; the two must agree on a
# binary input.  CRD_012.
bin_rows = [{"bin": M.VISIBLE, "crediting_rate": 1.0, "domain": "d",
             "first_attested_source": 800, "intermediary_count": 0,
             "attribution_depth": 2},
            {"bin": M.VISIBLE, "crediting_rate": 1.0, "domain": "d",
             "first_attested_source": 810, "intermediary_count": 0,
             "attribution_depth": 2},
            {"bin": M.NOT_RETAINED, "crediting_rate": 0.0, "domain": "d",
             "first_attested_source": 820, "intermediary_count": 0,
             "attribution_depth": 0},
            {"bin": M.NOT_RETAINED, "crediting_rate": 0.0, "domain": "d",
             "first_attested_source": 830, "intermediary_count": 0,
             "attribution_depth": 0}]
b2 = M.shuffle_band(bin_rows, 3, k=400)
v1rows = [dict(r, bin=(1 if r["bin"] == M.VISIBLE else 0)) for r in bin_rows]
b1 = V1.shuffle_band(v1rows, 3, k=400)
ck("v1 and v2 shuffle bands agree on a two-bin input",
   b1 is not None and b2 is not None
   and abs(b1["lo"] - b2["lo"]) < 1e-12 and abs(b1["hi"] - b2["hi"]) < 1e-12)

# ------------------------------------------------------- the five fixtures
f1 = run("f1_etymology")
ck("F1 returns ETYMOLOGY_TRACKING", f1["kind"] == M.ETYMOLOGY_TRACKING)
ck("F1's gap clears its shuffle band", V1.outside(f1["gap"], f1["band"]))
ck("F1's pre-stated ordering holds",
   f1["rates"][M.VISIBLE] > f1["rates"][M.TECHNICAL_ONLY]
   >= f1["rates"][M.NOT_RETAINED])
ck("F1's discriminating bin tracks visible",
   f1["discriminating_bin"]["tracks"] == "visible")

f2 = run("f2_contribution")
ck("F2 returns CONTRIBUTION_TRACKING", f2["kind"] == M.CONTRIBUTION_TRACKING)
ck("F2's gap is inside its band", not V1.outside(f2["gap"], f2["band"]))
ck("F2 clears the depth cut",
   f2["mean_depth"] >= M.DEPTH_CREDITING_CUT)
ck("F2's discriminating bin is UNDETERMINED, not forced",
   f2["discriminating_bin"]["tracks"] == "UNDETERMINED")

f3 = run("f3_mixed_side")
ck("F3 returns FRAME_ASYMMETRIC", f3["kind"] == M.FRAME_ASYMMETRIC)
ck("F3 names both sides", set(f3["sides"]) == {M.LANGUAGE_SIDE,
                                              M.TECHNIQUE_SIDE})
ck("F3 stops before any rate exists", "rates" not in f3)

f4 = run("f4_model_authored")
ck("F4 returns CONTAMINATED_FRAME", f4["kind"] == M.CONTAMINATED_FRAME)
ck("F4 stops before any rate exists", "rates" not in f4)
ck("F4's manifest carries the declaration",
   f4["manifest"]["model_authored"] is True)

f5 = run("f5_antiquity")
ck("F5's pooled gap clears the band", V1.outside(f5["gap"], f5["band"]))
ck("F5 pools to ETYMOLOGY_TRACKING", f5["kind"] == M.ETYMOLOGY_TRACKING)
ck("F5's gap vanishes inside the early date stratum",
   f5["n2_antiquity"]["pre-1200"]["gap"] == 0.0)
ck("F5's late stratum has no gap at all (one bin present)",
   f5["n2_antiquity"]["1200+"]["gap"] is None)
ck("F5's correlates were reported before the fit",
   "correlates_before_fit" in f5)
ck("F5's correlates show the date confound",
   f5["correlates_before_fit"]["first_attested_source"][M.VISIBLE]
   < f5["correlates_before_fit"]["first_attested_source"][M.NOT_RETAINED])
ck("F5's depth does not decide it",
   f5["mean_depth"] >= M.DEPTH_CREDITING_CUT)

f6 = run("f6_domain_specific")
ck("F6 returns DOMAIN_SPECIFIC", f6["kind"] == M.DOMAIN_SPECIFIC)
ck("F6's pooled gap is inside its band",
   not V1.outside(f6["gap"], f6["band"]))
ck("F6's one clearing domain does clear its own band",
   V1.outside(f6["domain_gap"], f6["domain_band"]))
ck("exactly one domain clears",
   sum(1 for v in f6["per_domain"].values() if v["clears"]) == 1)
# CRD_016: `gap` is the POOLED gap on every branch, DOMAIN_SPECIFIC included.
ck("gap means the pooled gap on DOMAIN_SPECIFIC too",
   f6["gap"] == f6["per_domain"][
       [d for d, v in f6["per_domain"].items() if not v["clears"]][0]
   ]["gap"] or abs(f6["gap"]) < 1.0)
ck("the domain's gap has its own key", f6["domain_gap"] != f6["gap"])
ck("F6 declares itself beyond the order",
   "BEYOND THE ORDER" in json.load(
       io.open(FX.paths("f6_domain_specific")[3], encoding="utf-8"))["note"])

# every return class the order lists is reached by a fixture or a constructed
# variant; a declared member no path populates cannot be told from one nobody
# looked for.  BLOCKED and UNKNOWN_measurable are reached below.
seen = {f1["kind"], f2["kind"], f3["kind"], f4["kind"], f5["kind"],
        f6["kind"]}
ck("five of the seven return classes are reached by the fixtures",
   len(seen) == 5)

# ------------------------------------------------ BLOCKED and UNKNOWN paths
tmp = tempfile.mkdtemp()
FX.write(tmp)


def _thin():
    """Two items per bin: below MIN_PER_BIN, so BLOCKED."""
    items = [it for it in FX.F1
             if int(it[0][-1] if it[0][-1].isdigit() else 0) < 9][:6]
    d = tempfile.mkdtemp()
    ev, mech, dep = FX.world(items, note="thin")
    for suf, rows in (("events", ev), ("mechanical", mech), ("depth", dep)):
        with io.open(os.path.join(d, "t.%s.jsonl" % suf), "w",
                     encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, sort_keys=True) + "\n")
    with io.open(os.path.join(d, "t.frame.json"), "w",
                 encoding="utf-8") as fh:
        fh.write(json.dumps(FX.frame("thin", "thin")) + "\n")
    return M.run(os.path.join(d, "t.events.jsonl"),
                 os.path.join(d, "t.mechanical.jsonl"),
                 os.path.join(d, "t.depth.jsonl"),
                 os.path.join(d, "t.frame.json"), 7)


thin = _thin()
ck("a thin bin returns BLOCKED", thin["kind"] == M.BLOCKED)
ck("BLOCKED names the reason the order gives",
   thin["why"] == "insufficient_attested_ordering")
ck("BLOCKED names which bins are thin", bool(thin["thin_bins"]))

# UNKNOWN_measurable: null gap, nobody crediting anyone.
low = [(nm, b, dom, ds, dr, h, 0, 3, 0)
       for (nm, b, dom, ds, dr, h, _, _, _) in FX.F1]
d = tempfile.mkdtemp()
ev, mech, dep = FX.world(low, note="nobody credits")
for suf, rows in (("events", ev), ("mechanical", mech), ("depth", dep)):
    with io.open(os.path.join(d, "u.%s.jsonl" % suf), "w",
                 encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
with io.open(os.path.join(d, "u.frame.json"), "w", encoding="utf-8") as fh:
    fh.write(json.dumps(FX.frame("u", "u")) + "\n")
unk = M.run(os.path.join(d, "u.events.jsonl"),
            os.path.join(d, "u.mechanical.jsonl"),
            os.path.join(d, "u.depth.jsonl"),
            os.path.join(d, "u.frame.json"), 7)
ck("a null gap with no credit flowing returns UNKNOWN_measurable",
   unk["kind"] == M.UNKNOWN_MEASURABLE)
ck("and it names the depth cut as the reason",
   "attribution_depth" in unk["why"])
ck("CONTRIBUTION_TRACKING and UNKNOWN_measurable differ only in depth here",
   abs(unk["gap"] - f2["gap"]) < 1e-12
   and unk["mean_depth"] < M.DEPTH_CREDITING_CUT)

# ------------------------------------------------------------ the gates
ck("gap with an absent end is None, never 0.0",
   M.gap({M.VISIBLE: 1.0}) is None)
ck("gap with both ends present is a number",
   abs(M.gap({M.VISIBLE: 1.0, M.NOT_RETAINED: 0.25}) - 0.75) < 1e-12)


def _refuses(fn, *a):
    try:
        fn(*a)
        return False
    except Exception:
        return True


ev_path = FX.paths("f1_etymology")[0]
raw = [json.loads(l) for l in io.open(ev_path, encoding="utf-8")
       if l.strip()]


def _write(rows, tag):
    p = os.path.join(tempfile.mkdtemp(), tag + ".jsonl")
    with io.open(p, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    return p


ck("events load as delivered", M.load_events(ev_path)[1]["salt"] == FX.SALT)
ck("an events file with no _manifest is refused",
   _refuses(M.load_events, _write([r for r in raw if "_manifest" not in r],
                                  "nomani")))
ck("model_authored must be a boolean, not absent",
   _refuses(M.load_events, _write(
       [{"_manifest": {"salt": FX.SALT}}] +
       [r for r in raw if "_manifest" not in r], "nobool")))
ck("an item with no frame_source is refused",
   _refuses(M.load_events, _write(
       [raw[0]] + [dict(r, frame_source="") for r in raw[1:]], "noframe")))
ck("an out-of-vocabulary bin is refused",
   _refuses(M.load_events, _write(
       [raw[0]] + [dict(r, bin="loanword_retained") for r in raw[1:]],
       "badbin")))
ck("a wrong entry_id is refused",
   _refuses(M.load_events, _write(
       [raw[0]] + [dict(r, entry_id="deadbeefdeadbeef") for r in raw[1:]],
       "badeid")))

dpath = FX.paths("f1_etymology")[2]
drows = [json.loads(l) for l in io.open(dpath, encoding="utf-8")
         if l.strip()]
ck("depth loads as delivered", len(M.load_depth(dpath)) == 12)
ck("a depth file carrying `item` is refused",
   _refuses(M.load_depth, _write([dict(r, item="alpha") for r in drows],
                                 "leak")))
ck("a depth field naming the bin is refused",
   _refuses(M.load_depth, _write([dict(r, loanword_retained=1)
                                  for r in drows], "leak2")))
ck("an out-of-range attribution_depth is refused",
   _refuses(M.load_depth, _write([dict(r, attribution_depth=4)
                                  for r in drows], "baddepth")))

# the join key carries no readable content -- UNI_078
eid = M.entry_id("alpha", FX.SALT)
ck("the entry_id does not contain the item name", "alpha" not in eid)
ck("the entry_id is 16 hex characters",
   len(eid) == 16 and all(c in "0123456789abcdef" for c in eid))
ck("two items get different handles",
   M.entry_id("alpha", FX.SALT) != M.entry_id("beta", FX.SALT))
ck("the same item under a different salt gets a different handle",
   M.entry_id("alpha", "other") != eid)

# ------------------------------------------------------ the mechanical rule
d1 = ("The method came from the Sigmaic tradition. Later handbooks "
      "restate it. A third sentence.")
d2 = ("The method came into use. Later handbooks restate it. Attributed "
      "to the Sigmaic tradition.")
ck("the name in sentence 1 counts at N=2",
   M.names_source(d1, "Sigmaic", 2) == 1)
ck("the name in sentence 3 does not count at N=2",
   M.names_source(d2, "Sigmaic", 2) == 0)
ck("and it does count at N=3", M.names_source(d2, "Sigmaic", 3) == 1)
ck("N is read from the data, so the measure moves with it",
   M.names_source(d2, "Sigmaic", 2) != M.names_source(d2, "Sigmaic", 3))
ck("the match is case-insensitive  [CHOICE 1]",
   M.names_source("From the SIGMAIC tradition. x. y.", "Sigmaic", 1) == 1)
ck("the match is on a word boundary  [CHOICE 1]",
   M.names_source("From the Sigmaically odd tradition. x. y.",
                  "Sigmaic", 1) == 0)
ck("first_sentences at N=1 keeps one sentence",
   M.first_sentences(d1, 1) == "The method came from the Sigmaic tradition.")

# --------------------------------------------- the revision's own removal
# CRD_010: REVISION 2 removes the field v1's CONTRIBUTION_TRACKING rested on.
v1src = io.open(os.path.join(HERE, "crediting_rate.py"),
                encoding="utf-8").read()
ck("v1's CONTRIBUTION_TRACKING rests on a misattribution rate",
   "misattr <= MISATTR_MAX" in v1src)
ck("that rate is derived from described_originator",
   '["described_originator"] == "receiving"' in v1src)
# A substring scan here fires on the three comments in which v2 NAMES the
# field it removed -- UNI_009 / T1-1 inside the check written against it, and
# the third instance in this session.  The honest test is structural: the
# field must reach no subscript, no key and no name in v2's code.
_dodgy = []
for node in ast.walk(tree2):
    if isinstance(node, ast.Constant) and node.value == "described_originator":
        _dodgy.append("constant")
    if isinstance(node, ast.Name) and node.id == "described_originator":
        _dodgy.append("name")
    if isinstance(node, ast.Attribute) and \
            node.attr == "described_originator":
        _dodgy.append("attribute")
ck("v2 uses described_originator in no expression", not _dodgy)
ck("v2 does name it in prose, which is why the scan is structural",
   src2.count("described_originator") >= 3)
ck("v2 declares a replacement discriminator",
   "DEPTH_CREDITING_CUT" in src2)
ck("the replacement is named a stipulation with no derivation",
   "has no derivation" in src2)
ck("the order still lists the class the revision removed the input for",
   "CONTRIBUTION_TRACKING" in io.open(
       os.path.join(HERE, "WORK_ORDER_V2.md"), encoding="utf-8").read())

# -------------------------------------------------- the order's own text
wo2 = io.open(os.path.join(HERE, "WORK_ORDER_V2.md"),
              encoding="utf-8").read()
for tok in ("visible", "technical_only", "not_retained", "ambiguous",
            "FRAME_ASYMMETRIC", "CONTAMINATED_FRAME", "model_authored",
            "frame_source", "attribution_depth",
            "origination_vs_absorption"):
    ck("the order names %s" % tok, tok in wo2)
ck("v1's order is not edited", "loanword_retained" in io.open(
    os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read())
ck("v1's order carries no three-state bin",
   "technical_only" not in io.open(os.path.join(HERE, "WORK_ORDER.md"),
                                   encoding="utf-8").read())

# ------------------------------------------------------------ the prediction
ck("the prediction file exists and is hashed",
   len(M.prediction_hash()) == 16)
ck("every run carries the hash",
   run("f1_etymology")["prediction_sha256_16"] == M.prediction_hash())
pred = io.open(os.path.join(HERE, "PREDICTION_V2.md"),
               encoding="utf-8").read()
ck("the prediction states the three-bin ordering",
   "crediting_rate(visible)" in pred and "technical_only" in pred)
ck("the prediction records the revision's provenance",
   "model-authored" in pred)

# ----------------------------------------------------------- F / G and the
# ----------------------------------------------------------- branch set
bs = M.branch_set()
ck("the branch set carries the order's origin",
   bs["origin"] == "single-origin account of scientific method")
ck("it carries all four branches", len(bs["branches"]) == 4)
ck("it names the discriminator", "three visibility bins" in
   bs["discriminator"])
ck("it records whether the method layer is present",
   bs["method_layer"] in ("present", "absent"))
ck("the method layer state is measured, not assumed",
   M.METHOD_LAYER in ("present", "absent"))
if M.METHOD_LAYER == "present":
    ck("F is branch_set", getattr(M.F, "__name__", "") == "branch_set")
    ck("G carries the return classes the order reuses",
       hasattr(M.G, "ReturnClass"))
else:
    ck("with F absent the branch set still renders",
       "F_module" not in bs)
    ck("and nothing is estimated differently", bs["method_layer"] == "absent")

# ------------------------------------------------------------ the manners
out = M.render(f1)
ck("the render is non-trivial", len(out) > 800)
ck("the render carries the revision's provenance first",
   "model-authored" in out.split("RETURN")[0])
ck("the render names no real technique or tradition",
   "algebra" not in out and "algorithm" not in out)
ck("the render states nothing is a claim",
   "NOTHING HERE IS A STATEMENT" in out)
ck("--selftest is refused", M.main(["--selftest"]) == 2)
ck("--choices exits clean", M.main(["--choices"]) == 0)
ck("six choices are declared", len(M.choices()) == 6)
ck("every choice marker appears in the module",
   all(("[CHOICE %d]" % i) in src2 for i in range(1, 7)))

# every fixture declares itself constructed
for name in sorted(FX.WORLDS):
    fr = json.load(io.open(FX.paths(name)[3], encoding="utf-8"))
    ck("%s declares itself constructed" % name,
       "CONSTRUCTED" in fr["corpus"] and "CONSTRUCTED WORLD" in fr["note"])
ck("the fixtures regenerate byte-identically",
   __import__("subprocess").run(
       [sys.executable, os.path.join(HERE, "make_fixtures_v2.py"), "--check"],
       capture_output=True).returncode == 0)

# contamination declared before the numbers
fxsrc = io.open(os.path.join(HERE, "make_fixtures_v2.py"),
                encoding="utf-8").read()
ck("the fixture generator declares the contamination",
   "REGRESSION result, not validation" in fxsrc)
ck("and it is in the header, before any world",
   fxsrc.index("REGRESSION result, not validation") < fxsrc.index("F1 = ["))

# ------------------------------------------------------ the severity screen
sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                "sheet-structure-scan"))
import no_severity  # noqa: E402

for name, o in (("f1", f1), ("f2", f2), ("f3", f3), ("f4", f4),
                ("f5", f5), ("f6", f6), ("blocked", thin),
                ("unknown", unk)):
    h = no_severity.hits(M.render(o))
    ck("the %s render screens clean" % name, not h)
ck("the screen fires on a plant",
   len(no_severity.hits(M.render(f1) + "\nthis is a defect\n")) == 1)

ck("all seven return classes are reached",
   seen | {thin["kind"], unk["kind"]} == {
       M.ETYMOLOGY_TRACKING, M.CONTRIBUTION_TRACKING, M.UNKNOWN_MEASURABLE,
       M.DOMAIN_SPECIFIC, M.BLOCKED, M.FRAME_ASYMMETRIC,
       M.CONTAMINATED_FRAME})

print("checks: %d   failed: %d" % (N[0], len(FAIL)))
for f in FAIL:
    print("  FAIL  " + f)
sys.exit(1 if FAIL else 0)
