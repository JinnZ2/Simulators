"""Evidence for the key v2 amendment 1 options: what do the draft's rules S1 / S2 / S3 give when they are
applied mechanically to the packet's own sources?  Nothing here changes a key, the brief, the packet or a scorer.

Run:  FORMULA_AUDIT_DIR=<checkout of formula-audit whose numcheck/check.py matches the packet's> \
      python3 check_rules.py > check_rules_output.txt

Parts
  A  numcheck records (fa:UNDECIDED, fa:VOID, fa:HOLDS): which keys are exclusive to one verdict?
  B  cplay (axes.reading, tokens, closure.FieldToken): what is required per status, what is a parameter,
     what is an attribute set after construction, what is a class attribute?
  C  TAF unified_audit.py: every dict literal that carries a coverage or crash key, with line numbers.
  D  sentences quoted from the packet (glossary, brief) that the rules lean on.
"""
import ast, hashlib, inspect, json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, "..", ".."))            # blind-reader-void12/
SRC = os.path.join(BASE, "reader_packet_v2", "sources")
FA = os.environ.get("FORMULA_AUDIT_DIR")
OUT = {}

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def head(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)

# --------------------------------------------------------------------------------------------- A: numcheck
head("A. numcheck: keys that appear on records of one verdict only (S2: 'present on every record of a kind')")
pk = os.path.join(SRC, "formula-audit", "numcheck", "check.py")
if not FA or not os.path.exists(os.path.join(FA, "numcheck", "check.py")):
    print("FORMULA_AUDIT_DIR not set or has no numcheck/check.py: part A skipped"); OUT["A"] = "skipped"
else:
    same = sha(pk) == sha(os.path.join(FA, "numcheck", "check.py"))
    print("packet check.py sha256 %s ; checkout check.py sha256 %s ; identical: %s" % (sha(pk)[:16], sha(os.path.join(FA, "numcheck", "check.py"))[:16], same))
    if not same:
        print("STOP: the checkout is not the packet's file; part A not run"); OUT["A"] = "mismatch"
    else:
        sys.path.insert(0, FA)
        from numcheck.check import check_all
        U = lambda v: {"value": v, "unit": "1"}
        cases = {
            "point_HOLDS_exact":            {"formula": "x + y = y + x", "values": {"x": U(2), "y": U(3)}},
            "point_FAILS_exact":            {"formula": "x = y", "values": {"x": U(2), "y": U(3)}},
            "point_UNDECIDED_tol0_proposal": {"formula": "x*(1-x) = x - x*x", "values": {"x": U(["0", "1"])}},
            "point_MIXED_bisected":         {"formula": "x = 3/2", "values": {"x": U(["1", "2"])}, "tolerance": "1/10"},
            "point_FAILS_bisected":         {"formula": "x*(1-x) = 1", "values": {"x": U(["0", "1"])}},
            "point_HOLDS_bisected":         {"formula": "x*(1-x) = x - x*x", "values": {"x": U(["0", "1"])}, "tolerance": "3/10"},
            "point_VOID_units":             {"formula": "x = y", "values": {"x": {"value": 2, "unit": "m"}, "y": {"value": 3, "unit": "s"}}},
            "point_VOID_noformula":         {"values": {}},
            "inter_BOTH_HOLD":              {"kind": "intersection", "formulas": [{"formula": "x = x", "tolerance": 1}, {"formula": "x = x", "tolerance": 1}], "region": {"x": ["0", "1"]}, "values": {"x": U(0)}},
            "inter_UNDECIDED":              {"kind": "intersection", "formulas": [{"formula": "x*(1-x) = x - x*x"}, {"formula": "x = 1/2", "tolerance": "6/10"}], "region": {"x": ["0", "1"]}, "values": {"x": U(0)}},
            "inter_ONE_FAILS":              {"kind": "intersection", "formulas": [{"formula": "x = 5"}, {"formula": "x = x", "tolerance": 1}], "region": {"x": ["0", "1"]}, "values": {"x": U(0)}},
            "inter_VOID_one_formula":       {"kind": "intersection", "formulas": [{"formula": "x = 1"}], "region": {"x": ["0", "1"]}, "values": {"x": U(0)}},
        }
        recs = {n: check_all([c])["records"][0] for n, c in cases.items()}
        def paths(r):
            out = set()
            for k, v in r.items():
                out.add(k)
                if k in ("bisection", "proposal", "subboxes") and isinstance(v, dict):
                    for k2 in v: out.add(k + "." + k2)
            return out
        P = {n: paths(r) for n, r in recs.items()}
        for n, r in recs.items():
            print("  %-30s %-12s %-10s %2d top-level keys; proposal %-4s; bisection %s" % (
                n, r["kind"], r["verdict"], len(r), "set" if r["proposal"] else "None",
                "absent" if "bisection" not in r else ("None" if r["bisection"] is None else "set")))
        def exclusive(verdict, kinds=None):
            mine = [n for n, r in recs.items() if r["verdict"] == verdict]
            others = [n for n, r in recs.items() if r["verdict"] != verdict]
            u = set().union(*[P[n] for n in mine]) if mine else set()
            o = set().union(*[P[n] for n in others])
            return sorted(u - o), mine
        OUT["A"] = {}
        for v in ("UNDECIDED", "VOID", "HOLDS"):
            ex, mine = exclusive(v)
            OUT["A"][v] = ex
            print("\n  keys present on a %s record and on no record of another verdict (from %s):" % (v, ", ".join(mine)))
            print("    " + (", ".join(ex) if ex else "(none)"))
        prop = recs["point_UNDECIDED_tol0_proposal"]["proposal"]
        print("\n  the `proposal` record on that UNDECIDED, its own keys (%d):" % len(prop)); print("    " + ", ".join(prop))
        print("  proposal is None on every record whose verdict is not UNDECIDED here: %s" % all(
            (r["proposal"] is None) for r in recs.values() if r["verdict"] != "UNDECIDED"))
        print("  `proposal` itself is a top-level key on every record (from _blank): %s" % all("proposal" in r for r in recs.values()))
        nb = {n: sorted(set(r["bisection"]) ) for n, r in recs.items() if isinstance(r.get("bisection"), dict)}
        same_b = len({tuple(v) for v in nb.values()}) == 1
        print("  every non-None `bisection` record has the same key set whatever the verdict (%s): %s" % (", ".join(sorted(nb)), same_b))
        OUT["A"]["proposal_keys"] = sorted(prop)

# --------------------------------------------------------------------------------------------- B: cplay
head("B. cplay: what each status requires, what is a parameter, what is set after construction")
cp = os.path.join(SRC, "Simulators", "combined-playground")
sys.path.insert(0, cp)
from cplay import tokens as T, axes as AX, closure as CL
OUT["B"] = {}
# B1: required fields per Reading status, found by running axes.reading with each optional argument removed
base_args = dict(reason="r", sigma=0.1, basis="b", exception="E", path="p", bound="bd")
fieldof = lambda s: "INSTRUMENT" if s == "CRASHED" else ("APPLICABILITY" if s == "OUTSIDE_DOMAIN" else "PHYSICAL")
req = {}
for s in AX.STATUSES:
    ok = True
    try: AX.reading(fieldof(s), s, **base_args)
    except AX.AxisError as e: ok = False; print("  note: %s with all args filled raised %s" % (s, e))
    r = set()
    for a in base_args:
        args = dict(base_args); args[a] = None
        try: AX.reading(fieldof(s), s, **args)
        except AX.AxisError: r.add(a)
    req[s] = sorted(r)
print("  Reading fields (a namedtuple, so every status has all of them):", list(AX.Reading._fields))
print("  fields whose removal makes axes.reading raise, per status (S1c 'a source rule REQUIRES'):")
for s in AX.STATUSES: print("    %-14s %s" % (s, req[s] or "-"))
OUT["B"]["required"] = req
print("\n  S2 applied to each status's S1(c) names, two ways:")
print("    literal S2, 'presence counts': a name is shared if every other status's Reading also HAS the field -> every Reading has every field")
print("    S2 on 'also requires' only:    a name is shared if every other status also REQUIRES it")
for s in ("CLOSED_WITHIN", "CRASHED", "OK"):
    lit = [a for a in req[s] if not all(a in AX.Reading._fields for _ in AX.STATUSES if _ != s)]
    alt = [a for a in req[s] if not all(a in req[o] for o in AX.STATUSES if o != s)]
    print("    %-14s S1c names %-22s literal S2 leaves %-8s requires-only S2 leaves %s" % (s, req[s], lit, alt))
OUT["B"]["T14_literal"] = [a for a in req["CLOSED_WITHIN"] if not all(a in AX.Reading._fields for _ in AX.STATUSES)]
OUT["B"]["T14_requires_only"] = [a for a in req["CLOSED_WITHIN"] if not all(a in req[o] for o in AX.STATUSES if o != "CLOSED_WITHIN")]
OUT["B"]["T08_requires_only_S1c"] = [a for a in req["CRASHED"] if not all(a in req[o] for o in AX.STATUSES if o != "CRASHED")]
# B2: tokens
print("\n  tokens.py constructors, parameters versus instance attributes:")
def params(f): return [p for p in inspect.signature(f).parameters]
trig = T.ExpiryTrigger("k", "t", "c")
unk = T.unknown("r", [trig])
abs_ = T.absent_at_sensitivity(1, "DECLARED", 2, "c")
void = T.Token("VOID", "r")
rows = [("cplay:ExpiryTrigger (T04)", params(T.ExpiryTrigger.__init__)[1:], sorted(vars(trig))),
        ("cplay:UNKNOWN via unknown() (T12)", params(T.unknown), sorted(vars(unk))),
        ("cplay:ABSENT_AT_SENSITIVITY (T05)", params(T.absent_at_sensitivity), sorted(vars(abs_))),
        ("cplay:VOID, plain Token (T03)", params(T.Token.__init__)[1:], sorted(vars(void)))]
for n, p, v in rows:
    print("    %-36s parameters %-48s vars(instance) %s" % (n, p, v))
    print("    %-36s attributes beyond the parameters: %s" % ("", sorted(set(v) - set(p)) or "-"))
OUT["B"]["tokens"] = {n: {"parameters": p, "vars": v} for n, p, v in rows}
print("\n  class attribute `is_exit` on ExpiryTrigger (T04):  in vars(class): %s ; in vars(instance): %s ; set on the UNTYPED token by untyped(): %s" % (
    "is_exit" in vars(T.ExpiryTrigger), "is_exit" in vars(trig), hasattr(T.untyped("x"), "is_exit")))
# B3: FieldToken and coverage entry
print("\n  closure.FieldToken (T06): fields %s ; STATES %s" % (list(CL.FieldToken._fields), CL.FieldToken.STATES))
ce = lambda k: AX.CoverageEntry(kind=k, module="m", input=None, reason="r", missing_path=None, expiry_condition=None)
print("  axes.CoverageEntry (cplay's form of the coverage entry): fields %s ; the same six on kind UNKNOWN, INFO and GAP_INSTRUMENT_CRASH: %s" % (
    list(AX.CoverageEntry._fields), all(ce(k)._fields == AX.CoverageEntry._fields for k in AX.COVERAGE_KINDS)))
print("  axes.crash() parameters (T08):", params(AX.crash))

# --------------------------------------------------------------------------------------------- C: TAF dict literals
head("C. TAF unified_audit.py: dict literals that carry a coverage or crash key (T09, T10)")
ua = os.path.join(SRC, "thermodynamic-accountability-framework", "calibration", "unified_audit.py")
tree = ast.parse(open(ua, encoding="utf-8").read())
keys_of = ("kind", "missing_path", "exception_type", "error", "expiry_condition")
OUT["C"] = []
for node in ast.walk(tree):
    if isinstance(node, ast.Dict):
        ks = [k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
        if set(ks) & set(keys_of):
            kind = ""
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and k.value == "kind":
                    kind = ast.unparse(v)
            OUT["C"].append({"line": node.lineno, "kind": kind, "keys": ks})
for d in sorted(OUT["C"], key=lambda d: d["line"]):
    print("  line %4d  kind=%-24s keys=%s" % (d["line"], d["kind"] or "-", d["keys"]))
cov = [d for d in OUT["C"] if d["kind"]]
allk = [set(d["keys"]) for d in cov]
print("\n  coverage-entry literals found: %d ; kinds: %s" % (len(cov), sorted({d["kind"] for d in cov})))
print("  `missing_path` appears in coverage literals of kind(s): %s" % sorted({d["kind"] for d in cov if "missing_path" in d["keys"]}))
print("  `expiry_condition` appears in coverage literals of kind(s): %s" % sorted({d["kind"] for d in cov if "expiry_condition" in d["keys"]}))
print("  `error` / `exception_type` appear in literal(s) at line(s): %s" % sorted({d["line"] for d in OUT["C"] if ({"error", "exception_type"} & set(d["keys"]))}))

# --------------------------------------------------------------------------------------------- D: quoted sentences
head("D. Sentences the rules lean on (verbatim, with file and line)")
def quote(path, a, b):
    L = open(path, encoding="utf-8").read().split("\n")
    for i in range(a, b + 1): print("  %s:%d  %s" % (os.path.relpath(path, SRC), i, L[i - 1][:260]))
quote(os.path.join(SRC, "thermodynamic-accountability-framework", "docs", "glossary.md"), 124, 129)
quote(os.path.join(SRC, "thermodynamic-accountability-framework", "calibration", "expiry_register.py"), 34, 37)
quote(os.path.join(BASE, "reader_packet_v2", "READER_BRIEF.md"), 22, 22)
print("\n(done)")
json.dump(OUT, open(os.path.join(HERE, "check_rules_output.json"), "w"), indent=1, sort_keys=True, default=str)
