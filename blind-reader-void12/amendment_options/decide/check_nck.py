"""check_nck.py: measures criteria N-a..N-d (N1), C-a..C-c (C1) and K-a..K-c (K1) of CRITERIA.md.

Needs a tree where the received revision-1 patch's scorer is applied (it holds N1 and C1) in SCORER_TREE (default /tmp/wt_r1),
and the repo (this checkout) for the key, packet and filed readings.  It imports the patch's own functions; it does not reimplement them.
Run:  SCORER_TREE=/tmp/wt_r1 FORMULA_AUDIT_DIR=... python3 check_nck.py      Writes check_nck_output.txt beside this file.
"""
import glob, importlib.util, io, itertools, json, os, re, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
BR = os.path.abspath(os.path.join(HERE, "..", ".."))                      # blind-reader-void12
TREE = os.environ.get("SCORER_TREE", "/tmp/wt_r1")
SC = os.path.join(TREE, "blind-reader-void12", "scoring")
sys.path.insert(0, SC)
import score_v2 as SV                                                      # the patch's scorer
out = []; P = lambda s="": out.append(s); res = {}
J = lambda p: json.load(open(p, encoding="utf-8"))
key_v2 = J(os.path.join(BR, "scoring", "key_v2.json")); key_a1 = J(os.path.join(SC, "key_v2_a1.json"))
readings = sorted(glob.glob(os.path.join(BR, "readings", "*", "response.json")))
P("scorer under test: %s (functions norm_name, nset, relation, rules_of imported from the received patch)" % os.path.relpath(SC, TREE))
P("key_v2 names scoring rules: %s ; key_v2_a1 names: %s" % (SV.rules_of(key_v2), SV.rules_of(key_a1)))
P()

def lists_of(obj, where):
    for tid, t in obj["terms"].items():
        for f, v in t.items():
            if f.startswith("slots") and isinstance(v, list) and not f.endswith("basis"): yield (where, tid, f, v)

# ---------------- N1 ----------------
allists = list(itertools.chain(lists_of(key_v2, "key_v2"), lists_of(key_a1, "key_v2_a1"),
                               *[lists_of(J(r), os.path.basename(os.path.dirname(r))) for r in readings]))
plain = lambda xs: frozenset(SV.norm_name(x, False) for x in xs)
n1 = lambda xs: frozenset(SV.norm_name(x, True) for x in xs)
collisions = [(w, t, f) for (w, t, f, v) in allists if len(plain(v)) != len(n1(v))]
changed = [(w, t, f, x, SV.norm_name(x, True)) for (w, t, f, v) in allists for x in v if SV.norm_name(x, True) != SV.norm_name(x, False)]
res["N-a"] = not collisions
P("N-a lists examined: %d (keys v2 and v2-a1, and %d filed readings). Lists where N1 makes two distinct names equal: %s" % (len(allists), len(readings), collisions or "none"))
srcs = ""
for fp in glob.glob(os.path.join(BR, "reader_packet_v2", "sources", "**", "*"), recursive=True):
    if os.path.isfile(fp):
        try: srcs += open(fp, encoding="utf-8").read() + "\n"
        except Exception: pass
only_wrapper = all(SV.norm_name(x, False) in (n,) or True for (_, _, _, x, n) in changed)
def wrapper_only(x, n):
    x0 = x.strip().lower(); y = x0
    if len(y) >= 2 and y[0] == "`" and y[-1] == "`": y = y[1:-1].strip()
    if len(y) >= 2 and y[0] == "<" and y[-1] == ">": y = y[1:-1].strip()
    return y == n and (x0 != n)
in_src = {x: (x.strip() in srcs) for (_, _, _, x, _) in changed}
nb = all(wrapper_only(x, n) for (_, _, _, x, n) in changed) and all(in_src.values())
res["N-b"] = nb
P("N-b names N1 changes: %d occurrences, distinct %s" % (len(changed), sorted({x for (_, _, _, x, _) in changed})))
for c in changed: P("      %s %s %s: %r -> %r" % c)
P("   each change removes only the wrapper: %s ; each wrapped form appears verbatim in a packet source: %s" % (all(wrapper_only(x, n) for (_, _, _, x, n) in changed), in_src))
# N-c: score claude-v2-A under key_v2 with the patched scorer; compare with the filed score
v2a = os.path.join(BR, "readings", "2026-11-18_claude-v2-A")
import tempfile; tmpj = os.path.join(tempfile.mkdtemp(), "nck_v2A.json")
cp = subprocess.run([sys.executable, "-B", os.path.join(SC, "score_v2.py"), os.path.join(v2a, "response.json"), "--key", os.path.join(BR, "scoring", "key_v2.json"), "--json", tmpj], capture_output=True, text=True)
same_txt = cp.stdout == open(os.path.join(v2a, "score.txt"), encoding="utf-8").read()
same_json = open(tmpj, encoding="utf-8").read() == open(os.path.join(v2a, "score.json"), encoding="utf-8").read()
res["N-c"] = same_txt and same_json
P("N-c patched scorer on Claude-v2-A under key_v2 (no rules named): text identical to filed score.txt: %s ; json byte-identical to filed score.json: %s" % (same_txt, same_json))
# N-d: effect on filed readings
eff = {}
for r in readings:
    rd = J(r)
    if "slots_specific" not in next(iter(rd["terms"].values())): continue
    for m in ("specific", "carried"):
        pass
rows = []
for r in readings:
    rd = J(r); name = os.path.basename(os.path.dirname(r))
    if not rd["terms"] or "slots_specific" not in next(iter(rd["terms"].values())): rows.append((name, "v1 packet reading (one 'slots' list); not scored by score_v2", None)); continue
    k0 = SV.score(rd, key_v2); k1 = SV.score(rd, {**key_v2, "meta": {**key_v2["meta"], "scoring_rules": ["N1"]}})
    eq0 = {m: k0["meanings"][m]["slots_equal"] for m in SV.MEANINGS}; eq1 = {m: k1["meanings"][m]["slots_equal"] for m in SV.MEANINGS}
    t0 = {m: k0["meanings"][m]["tier_agree"] for m in SV.MEANINGS}; t1 = {m: k1["meanings"][m]["tier_agree"] for m in SV.MEANINGS}
    rows.append((name, "slot sets equal to key, without N1 %s -> with N1 %s ; tier agreement %s -> %s" % (eq0, eq1, t0, t1), eq0 != eq1 or t0 != t1))
P("N-d effect of N1 on each filed v2 reading (key v2 lists, N1 switched on):")
for rname, text, ch in rows: P("   %-28s %s%s" % (rname, text, "" if ch is None else (" [CHANGES]" if ch else " [no change]")))
res["N-d"] = True   # reporting criterion; adopted regardless of effect size
P("   -> N1: N-a %s, N-b %s, N-c %s, N-d reported" % tuple("holds" if res[k] else "FAILS" for k in ("N-a", "N-b", "N-c")))
P()

# ---------------- C1 ----------------
U = range(5); subsets = [frozenset(c) for n in range(6) for c in itertools.combinations(U, n)]
bad = 0; counts = {k: 0 for k in SV.RELATIONS}
for r_, q_ in itertools.product(subsets, repeat=2):
    rel = SV.relation(r_, q_); counts[rel] += 1
    truth = {"equal": r_ == q_, "reader-superset": r_ > q_, "reader-subset": r_ < q_, "overlap": (r_ != q_ and not r_ <= q_ and not q_ <= r_ and bool(r_ & q_)),
             "disjoint": (not (r_ & q_)) and r_ != q_ and not r_ <= q_ and not q_ <= r_}
    # exhaustive + exclusive: exactly one of the five predicates is true and it is the one returned
    if sum(truth.values()) != 1 or not truth[rel]: bad += 1
res["C-a"] = bad == 0 and (r_ := None) is None
P("C-a all %d ordered pairs of subsets of a 5-name universe: relation returned is the one true predicate in %d cases, in %d it is not (exhaustive and exclusive: %s). counts %s" % (len(subsets) ** 2, len(subsets) ** 2 - bad, bad, bad == 0, counts))
# empty-vs-empty and empty-vs-nonempty cases deserve a look
P("   edge cases: relation(empty, empty) = %s ; relation(empty, {a}) = %s ; relation({a}, empty) = %s" % (SV.relation(frozenset(), frozenset()), SV.relation(frozenset(), frozenset("a")), SV.relation(frozenset("a"), frozenset())))
# C-b: Claude-v2-A under key_v2 with C1 named
kc1 = {**key_v2, "meta": {**key_v2["meta"], "scoring_rules": ["C1"]}}
rd = J(os.path.join(v2a, "response.json")); base = SV.score(rd, key_v2); new = SV.score(rd, kc1)
def strip_c1(o):
    o = json.loads(json.dumps(o)); o.pop("key_version", None); o.pop("scoring_rules", None)
    for m in o["meanings"].values():
        m.pop("relations", None)
        for s in m["slots"]: s.pop("relation", None)
    return o
unchanged = json.dumps(strip_c1(new), sort_keys=True) == json.dumps(base, sort_keys=True)   # both through JSON: tuples and lists compare alike
consistent = all((s["relation"] == "equal") == (s["status"] == "equal") for m in new["meanings"].values() for s in m["slots"] if s["status"] != "n/d")
res["C-b"] = unchanged and consistent
P("C-b Claude-v2-A under key_v2 with C1 switched on: every existing number unchanged once the C1 fields are removed: %s ; relation == 'equal' iff status == 'equal' on every determined row: %s" % (unchanged, consistent))
for m in SV.MEANINGS: P("      %s: relations %s" % (m, new["meanings"][m]["relations"]))
# C-c: nothing combined, nothing removed
def keys_of(o, pre=""):
    ks = set()
    if isinstance(o, dict):
        for k, v in o.items(): ks.add(pre + k); ks |= keys_of(v, pre + k + ".")
    elif isinstance(o, list) and o and isinstance(o[0], dict): ks |= keys_of(o[0], pre + "[].")
    return ks
removed = keys_of(base) - keys_of(new); added = keys_of(new) - keys_of(base)
res["C-c"] = not removed and all(("relation" in a or a.endswith("relations") or a in ("key_version", "scoring_rules")) for a in added)
P("C-c output keys removed by C1: %s ; added: %s" % (sorted(removed) or "none", sorted(added)))
P("   -> C1: C-a %s, C-b %s, C-c %s" % tuple("holds" if res[k] else "FAILS" for k in ("C-a", "C-b", "C-c")))
P()

# ---------------- K1 ----------------
spec = importlib.util.spec_from_file_location("derive_specific", os.path.join(HERE, "..", "derive", "derive_specific.py"))
DS = importlib.util.module_from_spec(spec); spec.loader.exec_module(DS)
T, AX, CL = DS.load_cplay()
inst = {
    "T03": ("cplay:VOID", lambda: T.Token("VOID", "r")),
    "T04": ("cplay:ExpiryTrigger", lambda: T.ExpiryTrigger("k", "t", "c")),
    "T05": ("cplay:ABSENT_AT_SENSITIVITY", lambda: T.absent_at_sensitivity(1, "DECLARED", 2, "c")),
    "T12": ("cplay:UNKNOWN", lambda: T.unknown("r", [T.ExpiryTrigger("k", "t", "c")])),
}
def fields_by_running(tid):
    if tid in inst: return list(vars(inst[tid][1]()).keys())
    if tid in ("T13", "T14"): return list(AX.Reading._fields)      # OK and CLOSED_WITHIN are statuses of a Reading
    if tid == "T06": return list(CL.FieldToken._fields)               # UNRESOLVED is carried in closure.FieldToken
    if tid == "T08":
        rd, cov = AX.crash(OSError("x"), path="p", module="m", inputs="i", expiry_condition="void")
        return list(dict.fromkeys(list(rd._fields) + list(cov._fields)))
# can vars(instance) be applied to each term's record at all?
def vars_works(obj):
    try: vars(obj); return True
    except TypeError: return False
rd_ok = AX.reading("INSTRUMENT", "OK"); ft = CL.FieldToken("INSTRUMENT", T.Token("UNRESOLVED", "r")); cv = AX.CoverageEntry(kind="UNKNOWN", module="m", input="i", reason="r", missing_path=None, expiry_condition="void")
vw = {"Reading (T13, T14, T08)": vars_works(rd_ok), "closure.FieldToken (T06)": vars_works(ft), "CoverageEntry (T08)": vars_works(cv),
      "Token (T03, T05, T12)": vars_works(T.Token("VOID", "r")), "ExpiryTrigger (T04)": vars_works(T.ExpiryTrigger("k", "t", "c"))}
P("K-0 does vars(instance) work on the record each term's carried list comes from?  %s" % json.dumps(vw))
kmis = []
for tid in ("T03", "T04", "T05", "T06", "T08", "T12", "T13", "T14"):
    got = fields_by_running(tid); kc = key_v2["terms"][tid]["slots_carried"]
    same = (sorted(got) == sorted(kc)); P("K-a %s %-26s key carried %s == fields by running %s" % (tid, key_v2["terms"][tid]["term_id"], same, "" if same else "| key %s | running %s" % (kc, got)))
    if not same: kmis.append(tid)
res["K-a"] = not kmis
res["K-0"] = all(vw.values())   # extra, reported: K1's literal wording "vars(instance)" must be applicable
trig = T.ExpiryTrigger("k", "t", "c")
kb = ("is_exit" not in vars(trig)) and hasattr(T.ExpiryTrigger, "is_exit") and ("is_exit" not in key_v2["terms"]["T04"]["slots_carried"])
res["K-b"] = kb
P("K-b ExpiryTrigger.is_exit is a class attribute (in vars of the class, not of an instance): %s ; not in T04 carried: %s" % (("is_exit" not in vars(trig)) and hasattr(T.ExpiryTrigger, "is_exit"), "is_exit" not in key_v2["terms"]["T04"]["slots_carried"]))
ut = T.untyped("note")
P("   note: tokens.untyped() DOES set is_exit on the instance: 'is_exit' in vars(untyped('note')) = %s (an UNTYPED Token; no term in the packet is UNTYPED, and T12's `untyped` holds such tokens, unopened)" % ("is_exit" in vars(ut)))
# K-c: where does the phrase occur
phrase = "instance fields"
places = {}
for name, p in (("reader_packet_v2/READER_BRIEF.md", os.path.join(BR, "reader_packet_v2", "READER_BRIEF.md")), ("reader_packet/READER_BRIEF.md", os.path.join(BR, "reader_packet", "READER_BRIEF.md")),
                ("PREREG.md", os.path.join(BR, "PREREG.md")), ("PROTOCOL.md", os.path.join(BR, "PROTOCOL.md")), ("scoring/key_v2.json (derivation notes)", os.path.join(BR, "scoring", "key_v2.json"))):
    try: places[name] = phrase in open(p, encoding="utf-8").read()
    except OSError: places[name] = None
res["K-c"] = places["reader_packet_v2/READER_BRIEF.md"] is True
P("K-c the phrase 'instance fields' occurs in: %s" % json.dumps(places))
P("   brief wording for slots_carried (what the readers were given): 'every named field of every record that the source's code or text builds, returns or documents ...'")
P("   -> K-c %s: the criterion assumed the phrase is the brief's own; it is in the key's derivation notes only" % ("holds" if res["K-c"] else "FAILS"))
P("   -> K1: K-a %s, K-b %s, K-c %s ; K-0 (not a pre-registered criterion; found while running K-a) %s" % tuple(["holds" if res[k] else "FAILS" for k in ("K-a", "K-b", "K-c")] + ["holds" if res["K-0"] else "FAILS: vars() raises on namedtuple records"]))
P()
P("summary: " + ", ".join("%s %s" % (k, "holds" if v else "FAILS") for k, v in sorted(res.items())))
txt = "\n".join(out); print(txt)
open(os.path.join(HERE, "check_nck_output.txt"), "w").write(txt + "\n")
