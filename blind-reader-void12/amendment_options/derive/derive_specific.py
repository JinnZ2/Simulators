"""derive_specific.py: derive each term's `slots_specific` from the packet's own sources by one stated rule.

RULE.  A field f is a slot of term t when
  TAG           f is defined on every instance of t and on no instance of any other term, and
  INDEPENDENCE  f is an independent input of t's record, not a function of the other slots.
"Defined" means: a declared parameter of the constructor written for t; a key present on the record (a key set to None
counts as present); or a field a source rule requires (removing it makes the constructor raise).
INDEPENDENCE: a field is dropped when it is COMPUTED FROM other candidate fields, not passed in or recorded raw.
Tested per route:
  cplay constructors   an attribute the constructor sets that is not one of its parameters is computed from them (so
                       covers_effect, typed, untyped, reason are dropped); the parameters themselves are tested for free
                       variation (every combination of two values per parameter is accepted) and any rejected combination
                       is reported, not silently ignored.
  TAF section record   each field's expression is evaluated on a corpus of exceptions; field Y is computed from field X
                       when Y is a function of X on the corpus (equal X always gives equal Y) and X is not a function of Y.
                       The corpus contains pairs that break each dependence that is not real (e.g. same message, different
                       filename), so a dependence that survives is one the corpus could not break.
  numcheck records     a candidate list is empty for every term here, so there is nothing to test; if a non-empty list
                       appears, this route has no independence test and the script says so.
(An earlier version of this file built each cplay object twice and compared; that passes for any deterministic constructor
and proves nothing about independence. It was replaced.)

Nothing here reads a key.  The derived lists are compared with the keys afterwards, in a separate step.
Where two derivation routes in the sources give different lists, the term is reported as undetermined (None) with both
routes shown; the script does not choose between them.

A derived list is only as good as the evidence it ran on.  For numcheck it is a list over the records in CORPUS: adding
records can only shrink the "defined on every instance" set and grow the "other terms" set, so an empty result is robust
and a non-empty one is an upper bound.

Run:
  FORMULA_AUDIT_DIR=<checkout whose numcheck/check.py has the packet's sha256> \
  COMPARE="p1=/path/key_p1.json,r1=/path/key_r1.json" python3 derive_specific.py
Writes derive_specific_output.txt and .json beside this file.
"""
import ast, hashlib, inspect, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, "..", ".."))                  # blind-reader-void12/
SRC = os.path.join(BASE, "reader_packet_v2", "sources")
TAF = os.path.join(SRC, "thermodynamic-accountability-framework")
FA = os.environ.get("FORMULA_AUDIT_DIR")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rd = lambda *p: open(os.path.join(*p), encoding="utf-8").read()

# ------------------------------------------------------------------------------------------------ A: numcheck
def corpus(check_all):
    U = lambda v: {"value": v, "unit": "1"}
    cases = {
        "HOLDS point exact":            {"formula": "x + y = y + x", "values": {"x": U(2), "y": U(3)}},
        "FAILS point exact":            {"formula": "x = y", "values": {"x": U(2), "y": U(3)}},
        "HOLDS point bisected":         {"formula": "x*(1-x) = x - x*x", "values": {"x": U(["0", "1"])}, "tolerance": "3/10"},
        "FAILS point bisected":         {"formula": "x*(1-x) = 1", "values": {"x": U(["0", "1"])}},
        "MIXED point bisected":         {"formula": "x = 3/2", "values": {"x": U(["1", "2"])}, "tolerance": "1/10"},
        "UNDECIDED point tol 0 (proposal)": {"formula": "x - x = 0", "values": {"x": U(["0", "1"])}},
        "UNDECIDED point tol 1e-6":     {"formula": "x - x = 0", "values": {"x": U(["0", "1"])}, "tolerance": "1/1000000"},
        "UNDECIDED intersection":       {"kind": "intersection", "formulas": [{"formula": "x*(1-x) = x - x*x"}, {"formula": "x = 1/2", "tolerance": "6/10"}], "region": {"x": ["0", "1"]}, "values": {"x": U(0)}},
        "VOID point units":             {"formula": "x = y", "values": {"x": {"value": 2, "unit": "m"}, "y": {"value": 3, "unit": "s"}}},
        "VOID point no formula":        {"values": {}},
        "VOID intersection one formula": {"kind": "intersection", "formulas": [{"formula": "x = 1"}], "region": {"x": ["0", "1"]}, "values": {"x": U(0)}},
        "BOTH_HOLD intersection":       {"kind": "intersection", "formulas": [{"formula": "x = x", "tolerance": 1}, {"formula": "x = x", "tolerance": 1}], "region": {"x": ["0", "1"]}, "values": {"x": U(0)}},
        "ONE_FAILS intersection":       {"kind": "intersection", "formulas": [{"formula": "x = 5"}, {"formula": "x = x", "tolerance": 1}], "region": {"x": ["0", "1"]}, "values": {"x": U(0)}},
    }
    return {n: check_all([c])["records"][0] for n, c in cases.items()}

def paths(r):
    out = set()
    for k, v in r.items():
        out.add(k)
        if isinstance(v, dict):
            out |= {k + "." + k2 for k2 in v}
    return out

def numcheck_slots(recs):
    by = {}
    for n, r in recs.items(): by.setdefault(r["verdict"], []).append((n, paths(r)))
    res = {}
    for v, tid in (("UNDECIDED", "fa:UNDECIDED"), ("VOID", "fa:VOID"), ("HOLDS", "fa:HOLDS")):
        mine = [p for _, p in by[v]]
        others = set().union(*[p for k, l in by.items() if k != v for _, p in l])
        universal = set.intersection(*mine)
        exclusive_any = set().union(*mine) - others
        res[tid] = {"slots": sorted(universal - others), "records": [n for n, _ in by[v]],
                    "exclusive_to_term_but_not_on_every_instance": sorted(exclusive_any - universal)}
    return res

# ------------------------------------------------------------------------------------------------ B: cplay
def load_cplay():
    sys.path.insert(0, os.path.join(SRC, "Simulators", "combined-playground"))
    from cplay import tokens, axes, closure
    return tokens, axes, closure

def token_slots(T):
    nonverdict = [s for s in T.STATES if s not in T.VERDICTS]
    gen = [p for p in inspect.signature(T.Token.__init__).parameters if p != "self"]
    def required(s):
        r = set()
        for p in gen:
            if p == "state": continue
            kw = {q: "x" for q in gen}; kw["state"] = s; kw[p] = None
            try: T.Token(**kw)
            except T.TokenError: r.add(p)
        return r
    shared = {"state"} | set.intersection(*[required(s) for s in nonverdict])     # defined on every token / required on every non-verdict
    trig = lambda: T.ExpiryTrigger("k", "t", "c")
    built = {
        "cplay:UNKNOWN":             (lambda: T.unknown("r", [trig(), "note"]), list(inspect.signature(T.unknown).parameters), "UNKNOWN"),
        "cplay:ABSENT_AT_SENSITIVITY": (lambda: T.absent_at_sensitivity(limit=1, basis="LADDER", effect_size=2, conditions="c", ladder="L"),
                                        list(inspect.signature(T.absent_at_sensitivity).parameters), "ABSENT_AT_SENSITIVITY"),
        "cplay:ExpiryTrigger":       (trig, [p for p in inspect.signature(T.ExpiryTrigger.__init__).parameters if p != "self"], None),
        "cplay:VOID":                (lambda: T.Token("VOID", "r"), gen, "VOID"),
    }
    res = {}
    for tid, (mk, params, state) in built.items():
        a = mk()
        assert state is None or a.state == state, (tid, a.state)
        derived = sorted(set(vars(a)) - set(params) - {"state"})
        res[tid] = {"slots": [p for p in params if p not in shared], "parameters": params,
                    "computed_by_the_constructor_so_not_slots": derived, "free_variation": free_variation(tid, T)}
    return res, sorted(shared)

def free_variation(tid, T):
    import itertools
    pools = {"limit": (1, 2), "effect_size": (1, 2), "basis": ("LADDER", "DECLARED"), "ladder": ("L", "M"), "conditions": ("c", "d"),
             "kind": ("a", "b"), "target": ("a", "b"), "condition": ("a", "b"), "reason": ("a", "b"), "state": ("VOID", "UNKNOWN")}
    mk = {"cplay:ABSENT_AT_SENSITIVITY": lambda **k: T.absent_at_sensitivity(**k),
          "cplay:ExpiryTrigger": lambda **k: T.ExpiryTrigger(**k),
          "cplay:UNKNOWN": lambda reason, triggers: T.unknown(reason, [T.ExpiryTrigger("k", "t", "c")] if triggers else []),
          "cplay:VOID": lambda reason, state: T.Token("VOID", reason)}.get(tid)
    if mk is None: return "n/a"
    names = {"cplay:ABSENT_AT_SENSITIVITY": ["limit", "basis", "effect_size", "conditions", "ladder"], "cplay:ExpiryTrigger": ["kind", "target", "condition"],
             "cplay:UNKNOWN": ["reason", "triggers"], "cplay:VOID": ["reason", "state"]}[tid]
    pool = {n: pools.get(n, (True, False)) if n != "triggers" else (True, False) for n in names}
    bad = 0; tot = 0
    for combo in itertools.product(*[pool[n] for n in names]):
        tot += 1
        try: mk(**dict(zip(names, combo)))
        except T.TokenError: bad += 1
    return "%d of %d combinations accepted" % (tot - bad, tot)

def reading_required(AX, reading=None):
    reading = reading or AX.reading
    fieldof = lambda s: "INSTRUMENT" if s == "CRASHED" else ("APPLICABILITY" if s == "OUTSIDE_DOMAIN" else "PHYSICAL")
    base = dict(reason="r", sigma=0.1, basis="b", exception="E", path="p", bound="bd")
    req = {}
    for s in AX.STATUSES:
        r = set()
        for a in base:
            kw = dict(base); kw[a] = None
            try: reading(fieldof(s), s, **kw)
            except AX.AxisError: r.add(a)
        req[s] = r
    return req

def reading_slots(AX, reading=None):
    req = reading_required(AX, reading)
    out = {}
    for s in AX.STATUSES:
        out[s] = sorted(f for f in req[s] if not any(f in req[o] for o in AX.STATUSES if o != s))
    return out, {s: sorted(v) for s, v in req.items()}

def fieldtoken_slots(T, CL):
    a = CL.FieldToken("INSTRUMENT", T.Token("UNRESOLVED", "r")); b = CL.FieldToken("INSTRUMENT", T.Token("TOLERANCE_UNRESOLVABLE", "r"))
    assert a._fields == b._fields and len(CL.FieldToken.STATES) == 2
    return {"slots": [], "why": "the two states share one class, so its fields %s are defined on both" % (list(a._fields),)}

# ------------------------------------------------------------------------------------------------ C: TAF
GAP = "GAP_INSTRUMENT_CRASH"

def exception_corpus():
    class E(Exception): pass
    def withfn(fn, msg):
        e = E(msg); e.filename = fn; return e
    return [ValueError("a"), ValueError("b"), KeyError("a"), ValueError(), ValueError(""), FileNotFoundError(2, "No such", "p1"),
            FileNotFoundError(2, "No such", "p2"), FileNotFoundError(2, "Other", "p1"), FileNotFoundError(2, "No such"), OSError(),
            withfn("p1", "x"), withfn("p2", "x"), withfn(None, "x")]

def dependence(secexpr, cand, corpus=None):
    corpus = corpus or exception_corpus()
    vals = {k: [] for k in cand}
    for e in corpus:
        for k in cand:
            vals[k].append(repr(eval(secexpr[k], {"e": e, "type": type, "getattr": getattr, "str": str, "len": len})))
    def determines(x, y):
        m = {}
        for a, b in zip(vals[x], vals[y]):
            if m.setdefault(a, b) != b: return False
        return True
    computed = {}
    for y in cand:
        for x in cand:
            if x != y and determines(x, y) and not determines(y, x): computed.setdefault(y, []).append(x)
    mutual = [(x, y) for i, x in enumerate(cand) for y in cand[i + 1:] if determines(x, y) and determines(y, x)]
    return {"computed_from": computed, "mutually_determining_pairs_kept": mutual, "corpus_size": len(corpus),
            "determines": {x + "->" + y: determines(x, y) for x in cand for y in cand if x != y}}

def taf_gap(src):
    tree = ast.parse(src)
    lits = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Dict):
            ks = [k.value for k in n.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            if "kind" in ks and "module" in ks:
                kind = ast.unparse(n.values[[k.value if isinstance(k, ast.Constant) else None for k in n.keys].index("kind")])
                lits.append((n.lineno, kind, ks))
    gap = [set(k) for _, kind, k in lits if kind == GAP]
    other = [set(k) for _, kind, k in lits if kind != GAP]
    cov_excl = sorted(set.intersection(*gap) - set().union(*other))
    is_gap = lambda v: isinstance(v, ast.Name) and v.id == GAP
    handlers = [h for h in ast.walk(tree) if isinstance(h, ast.ExceptHandler) and any(isinstance(n, ast.Assign) and is_gap(n.value) for n in ast.walk(h))]
    inside = set(id(n) for h in handlers for n in ast.walk(h))
    outside = [n.lineno for n in ast.walk(tree) if ((isinstance(n, ast.Assign) or isinstance(n, ast.Return)) and is_gap(n.value)) and id(n) not in inside]
    sec = None; secexpr = {}
    if len(handlers) == 1:
        for n in ast.walk(handlers[0]):
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict) and isinstance(n.targets[0], ast.Subscript):
                sec = [k.value for k in n.value.keys if isinstance(k, ast.Constant)]
                secexpr = {k.value: ast.unparse(v) for k, v in zip(n.value.keys, n.value.values) if isinstance(k, ast.Constant)}
    info = {"coverage_literals": [(l, k, ks) for l, k, ks in sorted(lits)], "exclusive_to_GAP_coverage_entries": cov_excl,
            "handlers_that_assign_the_GAP_status": len(handlers), "GAP_assigned_or_returned_outside_the_handler_at_lines": outside,
            "section_record_keys_built_in_that_handler": sec}
    if len(handlers) == 1 and not outside and sec:
        cand = cov_excl + [k for k in sec if k not in cov_excl]
        dep = dependence(secexpr, cand)
        info["candidates"] = cand; info["section_expressions"] = secexpr; info["dependence"] = dep
        info["slots"] = [k for k in cand if k not in dep["computed_from"]]
        info["why"] = ("the section record exists exactly when the GAP status is assigned (one assignment, in the handler that builds it); "
                       "missing_path is also the one coverage key no other kind carries; fields computed from another candidate field are dropped: " + (json.dumps(dep["computed_from"]) if dep["computed_from"] else "none"))
    else:
        info["slots"] = cov_excl
        info["why"] = "FLAG: the GAP status is also set or returned elsewhere, so the section record is not tied to it; only the coverage-entry key counts"
    return info

def taf_unknown(src, glossary):
    tree = ast.parse(src)
    lits = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Dict):
            ks = [k.value for k in n.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            if "kind" in ks and "module" in ks:
                kind = ast.unparse(n.values[[k.value if isinstance(k, ast.Constant) else None for k in n.keys].index("kind")])
                lits.append((kind, set(ks)))
    mine = [k for kind, k in lits if kind == "'UNKNOWN'"]; other = [k for kind, k in lits if kind != "'UNKNOWN'"]
    code = sorted(set.intersection(*mine) - set().union(*other))
    rows = [l for l in glossary.splitlines() if l.startswith("| `")]
    text = []
    for l in rows:
        cells = [c.strip() for c in l.strip("|").split("|")]
        name = re.match(r"`([^`]+)`", cells[0])
        if "UNKNOWN" in cells[1] and not cells[0].startswith("`PENDING`") and name: text.append(name.group(1))
    return {"routes": {"code: coverage entries of kind UNKNOWN, keys no other kind carries": code,
                       "glossary: terms whose row text names an UNKNOWN slot": sorted(text)}}

def derive_all(check_all=None, T=None, AX=None, CL=None):
    out = {}
    if check_all is not None:
        out.update(numcheck_slots(corpus(check_all)))
    tk, shared = token_slots(T)
    for tid, v in tk.items(): out[tid] = v
    rs, req = reading_slots(AX)
    out["cplay:OK"] = {"slots": rs["OK"]}
    out["cplay:CLOSED_WITHIN"] = {"slots": rs["CLOSED_WITHIN"], "required_per_status": req}
    out["cplay:UNRESOLVED"] = fieldtoken_slots(T, CL)
    crash_routes = {"Reading fields a rule requires for CRASHED": rs["CRASHED"],
                    "parameters of crash()": [p for p in inspect.signature(AX.crash).parameters]}
    out["cplay:CRASHED"] = {"routes": crash_routes}
    ua, gl = rd(TAF, "calibration", "unified_audit.py"), rd(TAF, "docs", "glossary.md")
    out["taf:GAP_INSTRUMENT_CRASH"] = taf_gap(ua)
    out["taf:UNKNOWN"] = taf_unknown(ua, gl)
    ER = rd(TAF, "calibration", "expiry_register.py")
    m = re.search(r"^EXPIRY_KEYS\s*=\s*(\(.*?\))", ER, re.M)
    out["taf:expiry_condition"] = {"slots": list(ast.literal_eval(m.group(1)))}
    nota = set(re.findall(r"ABSENT_AT_SENSITIVITY\(<(\w+)>\)", gl + ER))
    out["taf:ABSENT_AT_SENSITIVITY"] = {"slots": sorted(nota), "why": "the notation's one parameter, in the glossary and in expiry_register.py"}
    for tid, v in out.items():
        if "routes" in v:
            sets = {tuple(sorted(x)) for x in v["routes"].values()}
            v["slots"] = sorted(next(iter(sets))) if len(sets) == 1 else None      # None = undetermined: routes disagree
    return out

# ------------------------------------------------------------------------------------------------ main
def main():
    lines = []; P = lambda s="": lines.append(s)
    for f in ("numcheck/check.py",):
        pk = os.path.join(SRC, "formula-audit", f)
        if not FA or not os.path.exists(os.path.join(FA, f)) or sha(pk) != sha(os.path.join(FA, f)):
            sys.exit("FORMULA_AUDIT_DIR must hold a numcheck/check.py with the packet's sha256 (%s)" % sha(pk)[:16])
    sys.path.insert(0, FA)
    from numcheck.check import check_all
    T, AX, CL = load_cplay()
    D = derive_all(check_all, T, AX, CL)
    keys = {"v2": json.load(open(os.path.join(BASE, "scoring", "key_v2.json")))}
    for kv in filter(None, os.environ.get("COMPARE", "").split(",")):
        n, p = kv.split("=", 1); keys[n] = json.load(open(p))
    byid = {t["term_id"]: i for i, t in keys["v2"]["terms"].items()}
    P("derive_specific: slots_specific derived from the packet's sources; the rule is in the docstring of derive_specific.py")
    P("sources: numcheck/check.py sha256 %s ; unified_audit.py %s ; expiry_register.py %s ; glossary.md %s" % (
        sha(os.path.join(SRC, "formula-audit", "numcheck", "check.py"))[:16], sha(os.path.join(TAF, "calibration", "unified_audit.py"))[:16],
        sha(os.path.join(TAF, "calibration", "expiry_register.py"))[:16], sha(os.path.join(TAF, "docs", "glossary.md"))[:16]))
    P("keys compared: " + ", ".join("%s (sha256 %s)" % (n, hashlib.sha256(json.dumps(k, sort_keys=True).encode()).hexdigest()[:12]) for n, k in keys.items()))
    P()
    hdr = "%-4s %-28s %-48s" % ("id", "term", "derived") + "".join(" %-12s" % n for n in keys)
    P(hdr); P("-" * len(hdr))
    summary = {n: [0, 0, 0] for n in keys}                           # same, differ, undetermined-on-one-side
    rows = {}
    for tid in sorted(byid, key=lambda t: byid[t]):
        d = D[tid]["slots"]
        cells = []
        for n, k in keys.items():
            kl = k["terms"][byid[tid]]["slots_specific"]
            if d is None and kl is None: c = "n/d = n/d"; summary[n][0] += 1
            elif d is None or kl is None: c = "n/d vs list" if d is None else "list vs n/d"; summary[n][2] += 1
            elif set(d) == set(kl): c = "same"; summary[n][0] += 1
            else: c = "DIFFERS"; summary[n][1] += 1
            cells.append(c)
        rows[tid] = {"derived": d, "vs": dict(zip(keys, cells))}
        P("%-4s %-28s %-48s" % (byid[tid], tid, ("n/d (routes disagree)" if d is None else str(d))[:48]) + "".join(" %-12s" % c for c in cells))
    P()
    for n, (s, df, u) in summary.items(): P("against key %-3s: same %d, differs %d, undetermined on one side only %d (of 15)" % (n, s, df, u))
    P(); P("detail where a term was not read off a single source")
    for tid in sorted(byid, key=lambda t: byid[t]):
        v = D[tid]
        if "routes" in v:
            P("  %s %s: routes %s" % (byid[tid], tid, json.dumps(v["routes"])))
        if tid in ("fa:UNDECIDED", "fa:VOID", "fa:HOLDS"):
            P("  %s %s: from %d records; exclusive to the term but not on every instance of it: %s" % (byid[tid], tid, len(v["records"]), v["exclusive_to_term_but_not_on_every_instance"] or "-"))
        if tid.startswith("cplay:") and "computed_by_the_constructor_so_not_slots" in v:
            P("  %s %s: parameters %s ; computed by the constructor (not slots): %s ; free variation: %s" % (byid[tid], tid, v["parameters"], v["computed_by_the_constructor_so_not_slots"] or "-", v["free_variation"]))
        if tid == "cplay:CLOSED_WITHIN":
            P("  %s %s: fields whose removal makes reading() raise, per status: %s" % (byid[tid], tid, json.dumps(v["required_per_status"])))
        if tid == "taf:GAP_INSTRUMENT_CRASH":
            P("  %s %s: %s" % (byid[tid], tid, v["why"]))
            if "dependence" in v:
                P("      independence on %d exceptions: computed from another candidate field: %s ; determines: %s" % (v["dependence"]["corpus_size"], json.dumps(v["dependence"]["computed_from"]), json.dumps({k: x for k, x in v["dependence"]["determines"].items() if x})))
            P("      coverage literals (line, kind): %s ; GAP assigned or returned outside the handler at lines: %s ; section keys: %s" % (
                [(l, k) for l, k, _ in v["coverage_literals"]], v["GAP_assigned_or_returned_outside_the_handler_at_lines"] or "none", v["section_record_keys_built_in_that_handler"]))
    # ---- mutation checks: the rule must change its answer when the evidence changes
    P(); P("mutation checks (the rule must move when the evidence moves)")
    ok = True
    def chk(name, got, want):
        nonlocal ok
        good = got == want; ok &= good
        P("  %-4s %s: got %s ; expected %s" % ("PASS" if good else "FAIL", name, got, want))
    recs = corpus(check_all)
    only_prop = {n: r for n, r in recs.items() if r["verdict"] != "UNDECIDED" or n == "UNDECIDED point tol 0 (proposal)"}
    m1 = numcheck_slots(only_prop)["fa:UNDECIDED"]["slots"]
    chk("M1 corpus whose only UNDECIDED record carries a proposal: T01 has the proposal fields", ("proposal.lhs" in m1, len(m1) >= 14), (True, True))
    src = rd(TAF, "calibration", "unified_audit.py")
    m2 = taf_gap(src + "\ndef _x():\n    return GAP_INSTRUMENT_CRASH\n")
    chk("M2 GAP status also returned outside the handler: T10 falls back to the coverage-entry key", (m2["slots"], bool(m2["GAP_assigned_or_returned_outside_the_handler_at_lines"])), (["missing_path"], True))
    def stub(field, status, **kw):                                  # FAILED additionally requires sigma
        if status == "FAILED" and kw.get("sigma") is None: raise AX.AxisError("stub")
        return AX.reading(field, status, **kw)
    m3, _ = reading_slots(AX, stub)
    chk("M3 a second status also requires sigma: T14 drops sigma", m3["CLOSED_WITHIN"], ["basis"])
    m4 = taf_gap(src.replace('"exception_type": type(e).__name__,', '"exception_type": len(e.args),'))
    chk("M4 exception_type made an independent input (len(e.args)): T10 gets it back", m4["slots"], ["missing_path", "error", "exception_type"])
    m5 = taf_gap(src.replace('"exception_type": type(e).__name__,', '"exception_type": e.__class__.__name__ + "!",'))
    chk("M5 exception_type still computed from error by another route: dropped", m5["slots"], ["missing_path", "error"])
    P(); P("all mutation checks pass" if ok else "A MUTATION CHECK FAILED")
    txt = "\n".join(lines)
    print(txt)
    open(os.path.join(HERE, "derive_specific_output.txt"), "w").write(txt + "\n")
    json.dump({"derived": {t: {k: v for k, v in d.items() if k in ("slots", "routes", "parameters")} for t, d in D.items()}, "comparison": rows},
              open(os.path.join(HERE, "derive_specific_output.json"), "w"), indent=1, sort_keys=True)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
