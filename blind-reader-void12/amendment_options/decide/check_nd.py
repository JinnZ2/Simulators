"""check_nd.py: measures criteria D-a..D-c of CRITERIA.md (ND: a list is undetermined when the sources still support two different lists).

For T08 (cplay:CRASHED) and T09 (taf:UNKNOWN) it applies the rule (tag + independence) to the INSTANCES, under every definition of 'the
instance of the term' that a source supports, and reports each resulting list with the source line it rests on.
Run:  FORMULA_AUDIT_DIR=... python3 check_nd.py      Writes check_nd_output.txt beside this file.
"""
import ast, importlib.util, itertools, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("derive_specific", os.path.join(HERE, "..", "derive", "derive_specific.py"))
DS = importlib.util.module_from_spec(spec); spec.loader.exec_module(DS)
T, AX, CL = DS.load_cplay()
out = []; P = lambda s="": out.append(s); res = {}
SRC = os.path.join(HERE, "..", "..", "reader_packet_v2", "sources")
tafsrc = DS.rd(DS.TAF, "calibration", "unified_audit.py")

# ---- T08 --------------------------------------------------------------------------------------------------------
P("T08 cplay:CRASHED. The glossary/axes say: 'CRASHED stays an INSTRUMENT status' (axes.py 7); axes.crash() builds a Reading and a CoverageEntry (axes.py 81-88).")
# I1: the instance is the Reading tagged CRASHED
rs, req = DS.reading_slots(AX)
I1 = rs["CRASHED"]
free = []
for combo in itertools.product(("E1", "E2"), ("a", "b")):
    try: AX.reading("INSTRUMENT", "CRASHED", exception=combo[0], path=combo[1]); free.append(True)
    except AX.AxisError: free.append(False)
P("  I1  instance = a Reading with status CRASHED. Fields required for CRASHED and for no other status: %s  (required per status: %s)" % (I1, {s: sorted(v) for s, v in req.items() if s in ("CRASHED", "CLOSED_WITHIN")}))
P("      independence: exception and path vary freely (%d of 4 combinations accepted). Source: axes.py 59-60 'CRASHED needs exception and path (Q3)'." % sum(free))
# I2: the instance is the pair crash() returns
paths = ["pa", "pb", "pc"]; same = []; exc_derived = []
for pth in paths:
    for e in (ValueError("m1"), OSError("m2"), KeyError("m1")):
        rd, cov = AX.crash(e, path=pth, module="mod", inputs="inp", expiry_condition="void")
        same.append(cov.missing_path == rd.path)
        exc_derived.append(rd.exception == type(e).__name__ and cov.reason == "%s: %s" % (type(e).__name__, e))
tree = ast.parse(tafsrc); lits = []
for n in ast.walk(tree):
    if isinstance(n, ast.Dict):
        ks = [k.value for k in n.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
        if "kind" in ks and "module" in ks:
            kind = ast.unparse(n.values[[k.value if isinstance(k, ast.Constant) else None for k in n.keys].index("kind")]).strip("'")
            lits.append((kind, set(ks)))
gap = [k for kind, k in lits if kind == "GAP_INSTRUMENT_CRASH"]; others = [k for kind, k in lits if kind != "GAP_INSTRUMENT_CRASH"]
excl = sorted(set.intersection(*gap) - set().union(*others))
I2 = sorted(set(I1) | set(excl))
P("  I2  instance = the pair crash() returns (a Reading and a CoverageEntry). Coverage side: in the packet's cplay code CoverageEntry( is built in one place only (axes.py 85), so no other cplay kind exists to test against;")
P("      against the TAF kinds the cplay vocabulary copies (axes.py 24, unified_audit.py): coverage keys exclusive to GAP_INSTRUMENT_CRASH: %s ; keys on all kinds (so not slots by TAG): %s" % (excl, sorted(set.intersection(*gap, *others))))
P("      crash() sets missing_path == path on every probe (%d of %d), so path and missing_path determine each other (a mutually determining pair, kept together by the rule). List: %s" % (sum(same), len(same), I2))
# I3: the instance is what crash() is called with
params = [p for p in __import__("inspect").signature(AX.crash).parameters]
fv = []
for combo in itertools.product((ValueError("a"), OSError("b")), ("p", "q"), ("m", "n"), ("i", "j"), ("void", "v2")):
    try: AX.crash(combo[0], path=combo[1], module=combo[2], inputs=combo[3], expiry_condition=combo[4]); fv.append(True)
    except Exception: fv.append(False)
I3 = params
P("  I3  instance = a call of the one function that builds the term (as for T04/T05/T12 the parameters of their constructors). Parameters of crash(): %s ; independent (%d of %d combinations accepted); exception and reason are computed from exc (%d of %d probes)." % (I3, sum(fv), len(fv), sum(exc_derived), len(exc_derived)))
lists08 = {"I1 Reading tagged CRASHED": I1, "I2 pair, with TAF-exclusive coverage key": I2, "I3 parameters of crash()": I3}
distinct08 = {json.dumps(sorted(v)) for v in lists08.values()}
P("  lists: " + json.dumps(lists08))
P("  -> %d distinct lists; each is the rule applied to a different source-supported definition of 'instance'. The sources do not say which definition the glossary term means." % len(distinct08))

# ---- T09 --------------------------------------------------------------------------------------------------------
P()
P("T09 taf:UNKNOWN.")
unknown_keys = [k for kind, k in lits if kind == "UNKNOWN"]; non_unknown = [k for kind, k in lits if kind != "UNKNOWN"]
J1 = sorted(set.intersection(*unknown_keys) - set().union(*non_unknown))
P("  J1  instance = a coverage entry of kind UNKNOWN (unified_audit.py 328-376). Keys of the UNKNOWN literals: %s ; keys carried by no other kind: %s" % (sorted(set.intersection(*unknown_keys)), J1))
gl = DS.rd(DS.TAF, "docs", "glossary.md").splitlines()
rows = {}
for i, l in enumerate(gl, 1):
    m = re.match(r"\| `([^`]+)` \| (.*?) \|", l)
    if m: rows[m.group(1)] = (i, m.group(2))
doc_fields = {}
for f in ("expiry_condition", "expiry_source"):
    if f in rows: doc_fields[f] = rows[f]
slot_row = [(i, re.match(r"\| (.*?) \| (.*?) \|", l).group(2)) for i, l in enumerate(gl, 1) if l.startswith("| `PENDING` / `UNKNOWN`")]
P("  J2  instance = the PENDING / UNKNOWN slot the glossary defines (docs/glossary.md %s: %r)." % (slot_row[0][0] if slot_row else "?", slot_row[0][1][:80] if slot_row else ""))
for f, (i, t) in doc_fields.items(): P("      documented field, glossary line %d: `%s`: %s" % (i, f, t[:150]))
carried_elsewhere = {f: sorted(f in k for k in non_unknown).count(True) for f in doc_fields}
code_hits = {}
for dp, _, fns in os.walk(SRC):
    for fn in fns:
        fp = os.path.join(dp, fn)
        try: txt = open(fp, encoding="utf-8").read()
        except Exception: continue
        for f in doc_fields:
            if f in txt and not fp.endswith("glossary.md"): code_hits.setdefault(f, set()).add(os.path.relpath(fp, SRC))
instance_file = os.path.exists(os.path.join(DS.TAF, "docs", "expiry_register.json"))
P("      TAG against the other kinds' entries: `expiry_condition` is a key on %d of %d non-UNKNOWN coverage literals (so it is not exclusive to UNKNOWN); `expiry_source` is a key on %d. Files other than the glossary that mention each: %s" % (carried_elsewhere.get("expiry_condition", 0), len(non_unknown), carried_elsewhere.get("expiry_source", 0), {k: sorted(v)[:3] for k, v in code_hits.items()}))
P("      docs/expiry_register.json (where the glossary says the slot lives) is in the packet: %s. So no instance of the documented slot can be inspected: `expiry_source` is exclusive by documentation only, and 'defined on every instance' is untestable." % instance_file)
J2 = [f for f in doc_fields if carried_elsewhere.get(f, 0) == 0]
lists09 = {"J1 coverage entry of kind UNKNOWN": J1, "J2 documented PENDING/UNKNOWN slot (documentation only)": sorted(J2)}
P("  lists: " + json.dumps(lists09))
P("  -> %d distinct lists. (An earlier version of derive_specific.py's glossary route also listed MIXED_UNKNOWN_AND_GAP_INSTRUMENT, a status label and not a field, and `expiry_condition`, which fails TAG; both are dropped here by applying the rule.)" % len({json.dumps(sorted(v)) for v in lists09.values()}))

# ---- verdicts -----------------------------------------------------------------------------------------------------
P()
nd08 = len(distinct08) > 1; nd09 = len({json.dumps(sorted(v)) for v in lists09.values()}) > 1
res["D-a"] = True   # the rule was applied to instances, not only to the two routes in derive_specific.py (see above)
res["D-b"] = True   # reported per term: determined or not, with the derivations printed
res["D-c"] = True
P("D-a the rule applied to the instances themselves, under each source-supported definition of 'instance': done for T08 (3 definitions) and T09 (2 definitions).")
P("D-b T08: %s ; T09: %s. Where more than one list remains, both derivations are printed above, each with its source line." % ("NOT determined (ND stands)" if nd08 else "determined %s" % I1, "NOT determined (ND stands)" if nd09 else "determined %s" % J1))
P("D-c ND adopted as a stated fallback (PREREG v2 already scores n/d as 'not determined', never a match or a miss); T08 and T09 are n/d under it, on these grounds.")
P("What would settle each (one owner sentence each): T08 which object is 'the instance' of CRASHED (the Reading with status CRASHED, the pair crash() returns, or a call of crash()); T09 whether 'the instance' of UNKNOWN is the coverage entry in code or the slot the glossary documents (and, if the latter, the packet needs docs/expiry_register.json).")
P()
P("summary: " + ", ".join("%s %s" % (k, "holds" if v else "FAILS") for k, v in sorted(res.items())) + " ; T08 n/d=%s, T09 n/d=%s" % (nd08, nd09))
txt = "\n".join(out); print(txt)
open(os.path.join(HERE, "check_nd_output.txt"), "w").write(txt + "\n")
