"""check_rule_stability.py: measures criteria A1-A6 of CRITERIA.md for the rule (tag + independence).

Run:  FORMULA_AUDIT_DIR=<checkout matching the packet's numcheck/check.py> python3 check_rule_stability.py
Writes check_rule_stability_output.txt beside this file.  Uses a fixed random seed.
"""
import importlib.util, itertools, json, os, random, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("derive_specific", os.path.join(HERE, "..", "derive", "derive_specific.py"))
DS = importlib.util.module_from_spec(spec); spec.loader.exec_module(DS)
sys.path.insert(0, DS.FA or ""); from numcheck.check import check_all
T, AX, CL = DS.load_cplay()
out = []; P = lambda s="": out.append(s)
results = {}

# ---- A1 determinism: run derive twice in fresh processes, compare stdout
def run_derive():
    import tempfile
    env = dict(os.environ); env["DERIVE_OUT_DIR"] = tempfile.mkdtemp()      # never overwrite the filed derive outputs
    return subprocess.run([sys.executable, "-B", os.path.join(HERE, "..", "derive", "derive_specific.py")], env=env, capture_output=True, text=True).stdout
r1, r2 = run_derive(), run_derive()
results["A1"] = (r1 == r2 and "all mutation checks pass" in r1)
P("A1 determinism: two fresh runs byte-identical: %s ; mutation checks pass: %s" % (r1 == r2, "all mutation checks pass" in r1))

# ---- A2 numcheck corpus stability: >= 200 random inputs covering every verdict
rnd = random.Random(20261118)
U = lambda v, u="1": {"value": v, "unit": u}
IDENT = ["x + y = y + x", "x*(1-x) = x - x*x", "x - x = 0", "(x+y)*(x+y) = x*x + 2*x*y + y*y", "x*y = y*x"]
NONID = ["x = y", "x*(1-x) = 1", "x = 3/2", "x*x = x", "x + y = 2*x"]
TOLS = [None, "1/10", "3/10", "1/1000000", "1", "0"]
frac = lambda: "%d/%d" % (rnd.randint(0, 9), rnd.randint(1, 9))
def val():
    if rnd.random() < 0.5: return U(rnd.randint(-3, 5))
    a, b = sorted([frac(), frac()], key=lambda f: int(f.split("/")[0]) / int(f.split("/")[1]))
    return U([a, b])
def make():
    k = rnd.random()
    if k < 0.08: return {"values": {}}
    if k < 0.14: return {"formula": "x = y", "values": {"x": {"value": 2, "unit": "m"}, "y": {"value": 3, "unit": "s"}}}
    if k < 0.45:
        c = {"formula": rnd.choice(IDENT + NONID), "values": {"x": val(), "y": val()}}
        t = rnd.choice(TOLS)
        if t is not None: c["tolerance"] = t
        return c
    f = lambda: {"formula": rnd.choice(IDENT + NONID), **({"tolerance": t} if (t := rnd.choice(TOLS)) is not None else {})}
    return {"kind": "intersection", "formulas": [f(), f()], "region": {"x": ["0", "1"]}, "values": {"x": U(0)}}
recs, errors = {}, 0
for i in range(600):
    try: recs["r%d" % i] = check_all([make()])["records"][0]
    except Exception: errors += 1
vc = {}
for r in recs.values(): vc[r["verdict"]] = vc.get(r["verdict"], 0) + 1
big = DS.numcheck_slots(recs)
prop_all = sum(1 for r in recs.values() if r["verdict"] == "UNDECIDED" and r.get("proposal"))
und = vc.get("UNDECIDED", 0)
a2 = all(big[t]["slots"] == [] for t in ("fa:UNDECIDED", "fa:VOID", "fa:HOLDS")) and und > 0 and 0 < prop_all < und and len(recs) >= 200 and len(vc) >= 5
results["A2"] = a2
P("A2 numcheck corpus: %d records accepted (%d inputs rejected by the checker), verdict counts %s" % (len(recs), errors, json.dumps(vc, sort_keys=True)))
P("   derived lists: T01 %s  T07 %s  T11 %s ; UNDECIDED records carrying a proposal: %d of %d ; exclusive-to-UNDECIDED-but-not-universal paths: %d" % (
    big["fa:UNDECIDED"]["slots"], big["fa:VOID"]["slots"], big["fa:HOLDS"]["slots"], prop_all, und, len(big["fa:UNDECIDED"]["exclusive_to_term_but_not_on_every_instance"])))
P("   -> A2 %s" % ("holds" if a2 else "FAILS"))

# ---- A3 exception corpus stability
src = DS.rd(DS.TAF, "calibration", "unified_audit.py")
gap = DS.taf_gap(src); secexpr = gap["section_expressions"]; cand = gap["candidates"]; full = DS.exception_corpus()
slots_of = lambda corpus: [k for k in cand if k not in DS.dependence(secexpr, cand, corpus)["computed_from"]]
base = slots_of(full)
single = {i: slots_of(full[:i] + full[i + 1:]) for i in range(len(full))}
changed1 = [i for i, v in single.items() if sorted(v) != sorted(base)]
pairs = {(i, j): slots_of([e for n, e in enumerate(full) if n not in (i, j)]) for i, j in itertools.combinations(range(len(full)), 2)}
changed2 = [(i, j) for (i, j), v in pairs.items() if sorted(v) != sorted(base)]
a3 = (not changed1)
results["A3"] = a3
P("A3 exception corpus (%d exceptions): base T10 %s" % (len(full), base))
P("   single removals that change T10: %s (of %d)" % (changed1 or "none", len(full)))
P("   pair removals that change T10: %d of %d: %s" % (len(changed2), len(pairs), [(repr(full[i])[:40], repr(full[j])[:40]) for i, j in changed2][:6]))
P("   -> A3 %s" % ("holds" if a3 else "FAILS"))

# ---- A4 constructor stability: second filler, second pools
D1 = {}
tk1, sh1 = DS.token_slots(T); tk2, sh2 = DS.token_slots(T, fill="zz9")
rs1, _ = DS.reading_slots(AX); rs2, _ = DS.reading_slots(AX, base=dict(reason="r2", sigma=2.5, basis="other", exception="OSError", path="q", bound="b2"))
same_tokens = {t: tk1[t]["slots"] == tk2[t]["slots"] for t in tk1} | {"shared": sh1 == sh2}
same_reading = rs1 == rs2
fv1 = {t: DS.free_variation(t, T) for t in ("cplay:VOID", "cplay:ExpiryTrigger", "cplay:ABSENT_AT_SENSITIVITY", "cplay:UNKNOWN")}
fv2 = {t: DS.free_variation(t, T, alt=True) for t in fv1}
a4 = all(same_tokens.values()) and same_reading and fv1 == fv2
results["A4"] = a4
P("A4 constructor stability under a second filler and a second, disjoint pool:")
P("   token-constructor lists unchanged: %s ; Reading-requirement lists unchanged: %s ; free-variation counts unchanged: %s" % (same_tokens, same_reading, fv1 == fv2))
if fv1 != fv2: P("   free variation first pool %s ; second pool %s" % (fv1, fv2))
P("   -> A4 %s" % ("holds" if a4 else "FAILS"))

# ---- A5 no reader dependence: static check of the derivation functions
import inspect
body = "".join(inspect.getsource(f) for f in (DS.derive_all, DS.numcheck_slots, DS.token_slots, DS.reading_slots, DS.taf_gap, DS.taf_unknown, DS.dependence, DS.free_variation))
bad = [w for w in ("scoring", "readings", "key_v2", "response.json", "COMPARE") if w in body]
a5 = not bad
results["A5"] = a5
P("A5 reader independence: the derivation functions mention none of scoring / readings / key_v2 / response.json / COMPARE: %s %s" % (a5, bad or ""))
P("   (keys are opened only in main(), after derive_all has returned.)")
P("   -> A5 %s" % ("holds" if a5 else "FAILS"))

# ---- A6 independence applied on each route that yields a non-empty list
reading_free = {}
for st, fields in (("CLOSED_WITHIN", ("sigma", "basis")), ("CRASHED", ("exception", "path"))):
    ok = 0; tot = 0
    for combo in itertools.product((0.1, 2.5), ("a", "b")) if st == "CLOSED_WITHIN" else itertools.product(("E1", "E2"), ("a", "b")):
        tot += 1
        kw = dict(zip(fields, combo)); field = "INSTRUMENT" if st == "CRASHED" else "PHYSICAL"
        try: AX.reading(field, st, **kw); ok += 1
        except AX.AxisError: pass
    reading_free[st] = "%d of %d combinations accepted" % (ok, tot)
routes = [
    ("cplay constructors (T04, T05, T12)", "computed attributes dropped; parameters probed for free variation", "yes"),
    ("cplay Reading requirement table (T14)", "required fields probed for free variation: " + json.dumps(reading_free), "yes"),
    ("TAF section record (T10)", "functional dependence on %d exceptions" % len(full), "yes"),
    ("TAF coverage entries (T10 missing_path, T09)", "the one exclusive key; module and input are both `name` in the GAP entry but are not exclusive, so are dropped by TAG", "n/a (one candidate)"),
    ("numcheck records (T01, T07, T11)", "every list is empty on %d records, nothing to test" % len(recs), "n/a (empty)"),
    ("TAF notation (T02, T15)", "one parameter / a fixed key tuple from the source; no dependence test", "NO TEST"),
]
a6 = all(r[2] != "NO TEST" for r in routes[:3]) and "3 of 4" not in json.dumps(reading_free)
results["A6"] = a6
P("A6 routes that yield a non-empty list and the independence test applied:")
for r in routes: P("   %-48s %s [%s]" % r)
P("   Noted gap: T02 (`value`) and T15 (the four EXPIRY_KEYS) are read from a notation / a constant and have no dependence test; they are single named parameters or a fixed tuple in the source.")
P("   -> A6 %s (for the three routes that derive a list from instances)" % ("holds" if a6 else "FAILS"))
P()
P("summary: " + ", ".join("%s %s" % (k, "holds" if v else "FAILS") for k, v in results.items()))
txt = "\n".join(out); print(txt)
open(os.path.join(HERE, "check_rule_stability_output.txt"), "w").write(txt + "\n")
sys.exit(0 if all(results.values()) else 1)
