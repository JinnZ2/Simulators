"""m01_code.py: code the filed v2 readings' slots_specific choices into M01 records.

Criteria: M01_CRITERIA.md; schema: M01_SCHEMA.json (both fixed in PREREG before this file existed).
Run from anywhere:  python3 m01_code.py        writes m01_records.json and m01_report.txt beside this file.
                    python3 m01_code.py --check  re-runs and fails if the written files would change.

Stdlib only. The packet's cplay code is imported (no bytecode written). numcheck is parsed, not run: the packet does not
ship the modules it imports.
"""
import ast, hashlib, inspect, json, os, re, sys, types, importlib.util
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                                   # blind-reader-void12/
SRC = os.path.join(BASE, "reader_packet_v2", "sources")
CP = os.path.join(SRC, "Simulators", "combined-playground", "cplay")
TAF = os.path.join(SRC, "thermodynamic-accountability-framework")
NC = os.path.join(SRC, "formula-audit", "numcheck", "check.py")
EVID = os.path.join(BASE, "amendment_options", "evidence", "check_rules_output.txt")
READINGS = {   # folder -> packet variant as filed (None: not stated)
    "2026-11-18_claude-v2-A": "A", "2026-11-19_kimi-v2-A": "A", "2026-11-19_gpt6-v2": None}
V2A_SHA = "94836e79b966a89fe9a14464e0930462d039aba052cc44377b9b092d7ca24a63"
rd = lambda *p: open(os.path.join(*p), encoding="utf-8").read()
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()

def n1(x):
    x = x.strip().lower()
    if len(x) >= 2 and x[0] == "`" and x[-1] == "`": x = x[1:-1].strip()
    if len(x) >= 2 and x[0] == "<" and x[-1] == ">": x = x[1:-1].strip()
    return x

# --------------------------------------------------------------------------------------------- the source half
def load_cplay():
    pkg = types.ModuleType("cplay_m01"); pkg.__path__ = [CP]; sys.modules["cplay_m01"] = pkg
    mods = {}
    for m in ("tokens", "axes", "closure"):
        spec = importlib.util.spec_from_file_location("cplay_m01." + m, os.path.join(CP, m + ".py"))
        mod = importlib.util.module_from_spec(spec); sys.modules["cplay_m01." + m] = mod; spec.loader.exec_module(mod)
        setattr(pkg, m, mod); mods[m] = mod
    return mods["tokens"], mods["axes"]

def raises(fn, exc=Exception):
    try: fn()
    except exc: return True
    return False

def cplay_facts():
    T, A = load_cplay()
    f = {}
    trig = lambda: T.ExpiryTrigger("k", "t", "c")
    # T04 ExpiryTrigger
    params = [p for p in inspect.signature(T.ExpiryTrigger.__init__).parameters if p != "self"]
    stored = list(vars(trig()))
    assert params == ["kind", "target", "condition"] and sorted(stored) == sorted(params)
    for p in params:
        kw = dict(kind="k", target="t", condition="c"); kw[p] = ""
        req = raises(lambda: T.ExpiryTrigger(**kw), T.TokenError)
        assert not hasattr(T.Token("VOID", "r"), p)
        f[("T04", p)] = dict(location="tokens.py 64-72", origin="RAW_INPUT", presence_scope="ALL_EXCLUSIVE",
                             applicability_scope="ALL_EXCLUSIVE", requirement_scope="ALL_EXCLUSIVE" if req else "NONE",
                             source_basis="ran ExpiryTrigger: parameter and stored field; empty value raises TokenError: %s; "
                                          "absent from a plain Token" % req, provenance="SCRIPT_DERIVED")
    # T05 ABSENT_AT_SENSITIVITY
    params = list(inspect.signature(T.absent_at_sensitivity).parameters)
    mk = lambda **o: T.absent_at_sensitivity(**dict(dict(limit=1, basis="LADDER", effect_size=2, conditions="c", ladder="L"), **o))
    tok = mk(); stored = set(vars(tok)) - {"state", "reason"}
    computed = sorted(stored - set(params))
    assert computed == ["covers_effect"], computed
    for p in params:
        req = raises(lambda: mk(**{p: None}), T.TokenError)
        cond = p == "ladder" and not raises(lambda: mk(basis="DECLARED", ladder=None), T.TokenError)
        f[("T05", p)] = dict(location="tokens.py 92-104", origin="RAW_INPUT", presence_scope="ALL_EXCLUSIVE",
                             applicability_scope="SOME_EXCLUSIVE" if cond else "ALL_EXCLUSIVE",
                             requirement_scope="ALL_EXCLUSIVE" if (req and not cond) else "NONE",
                             source_basis="ran absent_at_sensitivity: parameter, stored; None raises: %s%s"
                                          % (req, "; required only when basis == LADDER (DECLARED with ladder=None accepted)" if cond else ""),
                             provenance="SCRIPT_DERIVED")
    f[("T05", "covers_effect")] = dict(location="tokens.py 103", origin="COMPUTED", presence_scope="ALL_EXCLUSIVE",
                                       applicability_scope="ALL_EXCLUSIVE", requirement_scope="NONE",
                                       source_basis="ran absent_at_sensitivity: stored but not a parameter (limit <= effect_size)",
                                       provenance="SCRIPT_DERIVED")
    # T12 UNKNOWN
    params = list(inspect.signature(T.unknown).parameters)
    a = T.unknown("r", [trig()]); b = T.unknown("r", [trig(), "note"])
    assert params == ["reason", "triggers"] and "triggers" not in vars(a)
    req = raises(lambda: T.unknown("r", ["note only"]), T.TokenError)
    plain = T.Token("VOID", "r")
    f[("T12", "triggers")] = dict(location="tokens.py 81-89", origin="PARAMETER_ONLY", presence_scope="NONE",
                                  applicability_scope="NONE", requirement_scope="ALL_EXCLUSIVE" if req else "NONE",
                                  source_basis="ran unknown(): parameter, not stored under that name; no typed trigger raises: %s" % req,
                                  provenance="SCRIPT_DERIVED")
    for p in ("typed", "untyped"):
        some = len(getattr(a, p)) == 0 and len(getattr(b, p)) > 0
        assert not hasattr(plain, p)
        f[("T12", p)] = dict(location="tokens.py 87-88", origin="COMPUTED", presence_scope="ALL_EXCLUSIVE",
                             applicability_scope="SOME_EXCLUSIVE" if some else "ALL_EXCLUSIVE", requirement_scope="NONE",
                             source_basis="ran unknown(): stored, split out of triggers; empty on some instances: %s" % some,
                             provenance="SCRIPT_DERIVED")
    # Reading statuses: requirement per status, for CLOSED_WITHIN (T14) and CRASHED (T08)
    full = dict(reason="r", sigma=1.0, basis="b", exception="E", path="p", bound="x")
    where = {"CRASHED": "INSTRUMENT", "OUTSIDE_DOMAIN": "APPLICABILITY"}
    req = {}
    for st in A.STATUSES:
        req[st] = set()
        for k in full:
            kw = dict(full); del kw[k]
            if raises(lambda: A.reading(where.get(st, "PHYSICAL"), st, **kw), A.AxisError): req[st].add(k)
    carried_elsewhere = A.reading("PHYSICAL", "OK", sigma=1.0, basis="b", exception="E", path="p")
    for tid, st, fields in (("T14", "CLOSED_WITHIN", ("sigma", "basis")), ("T08", "CRASHED", ("exception", "path"))):
        for p in fields:
            excl = [s for s in A.STATUSES if p in req[s]] == [st]
            assert getattr(carried_elsewhere, p) is not None       # another status can carry the value: applicability shared
            f[(tid, p)] = dict(location="axes.py 41-66", origin="RAW_INPUT", presence_scope="SHARED", applicability_scope="SHARED",
                               requirement_scope="ALL_EXCLUSIVE" if excl else "SHARED",
                               source_basis="ran reading(): a field of every Reading; OK accepts it too; required only for %s: %s" % (st, excl),
                               provenance="SCRIPT_DERIVED")
    # T08 crash() parameters, and the spec name 'call'
    cparams = list(inspect.signature(A.crash).parameters)
    assert cparams == ["exc", "path", "module", "inputs", "expiry_condition"]
    rdg, cov = A.crash(ValueError("e"), path="p", module="m", inputs="i", expiry_condition=None)
    for p in ("exc", "inputs"):
        assert not hasattr(rdg, p) and not hasattr(cov, p)
        f[("T08", p)] = dict(location="axes.py 81-88", origin="PARAMETER_ONLY", presence_scope="NONE", applicability_scope="NONE",
                             requirement_scope="SHARED",
                             source_basis="ran crash(): a parameter stored under no field of that name; crash() builds a CRASHED Reading "
                                          "AND a GAP_INSTRUMENT_CRASH CoverageEntry, so the call is shared by two terms",
                             provenance="SCRIPT_DERIVED")
    spec = rd(SRC, "Simulators", "playground-crossrun", "COMBINED_SPEC.lines_1-390.md")
    assert "CRASHED(exception, call, inputs)" in spec
    assert not any(hasattr(x, "call") for x in (rdg, cov))
    f[("T08", "call")] = dict(location="COMBINED_SPEC line 321", origin="DOCUMENTED", presence_scope="NO_INSTANCE",
                              applicability_scope="NO_INSTANCE", requirement_scope="NO_INSTANCE",
                              source_basis="named in the spec's crash-record notation; no record built by the packet's code has it",
                              provenance="SCRIPT_DERIVED")
    return f

def taf_facts():
    ua = rd(TAF, "calibration", "unified_audit.py"); reg = rd(TAF, "calibration", "expiry_register.py"); gl = rd(TAF, "docs", "glossary.md")
    f = {}
    a, b = ua.index("def _coverage_entries"), ua.index("# CODE-AUDIT DISPATCHER")
    lits = [x.split("})")[0] for x in ua[a:b].split("entries.append({")[1:]]
    kinds = [re.search(r'"kind":\s*([^,]+),', x).group(1).strip() for x in lits]
    keys = [set(re.findall(r'"(\w+)":', x)) for x in lits]
    assert kinds == ["GAP_INSTRUMENT_CRASH", '"UNKNOWN"', '"INFO"', '"UNKNOWN"'], kinds
    others = set.intersection(*keys[1:])
    d = ua.index("def _dispatch"); e = ua.index("report.sections[name] = section", d)
    raise_branch = ua[ua.index("except Exception as e:", d):e]
    section = re.findall(r'"(\w+)":', raise_branch)
    assert section == ["error", "exception_type", "missing_path"]
    assert 'f"{type(e).__name__}: {e}"' in raise_branch and '"exception_type": type(e).__name__' in raise_branch
    assert "missing_path" in keys[0] and "missing_path" not in set().union(*keys[1:])
    f[("T10", "missing_path")] = dict(location="unified_audit.py 336-343, 485-489", origin="RAW_INPUT", presence_scope="ALL_EXCLUSIVE",
                                      applicability_scope="SOME_EXCLUSIVE", requirement_scope="NONE",
                                      source_basis="parsed: on the GAP coverage literal only (not UNKNOWN / INFO); value is "
                                                   "getattr(e, 'filename', None), so None on some instances",
                                      provenance="SCRIPT_DERIVED")
    f[("T10", "error")] = dict(location="unified_audit.py 485-489", origin="RAW_INPUT", presence_scope="ALL_EXCLUSIVE",
                               applicability_scope="ALL_EXCLUSIVE", requirement_scope="NONE",
                               source_basis="parsed: section record built only in the raise handler; recorded from the exception",
                               provenance="SCRIPT_DERIVED")
    f[("T10", "exception_type")] = dict(location="unified_audit.py 485-489", origin="COMPUTED", presence_scope="ALL_EXCLUSIVE",
                                        applicability_scope="ALL_EXCLUSIVE", requirement_scope="NONE",
                                        source_basis="parsed: built in the raise handler; type(e).__name__ is the prefix of error "
                                                     "(f\"{type(e).__name__}: {e}\"), so a function of error",
                                        provenance="SCRIPT_DERIVED")
    assert "expiry_condition" in others and "expiry_condition" in keys[0]
    f[("T09", "expiry_condition")] = dict(location="glossary.md 127; unified_audit.py 336-371", origin="RAW_INPUT",
                                          presence_scope="SHARED", applicability_scope="SHARED", requirement_scope="NONE",
                                          source_basis="parsed: on every coverage literal (UNKNOWN, INFO, GAP); glossary documents it for "
                                                       "PENDING / UNKNOWN slots; value set from module constants",
                                          provenance="SCRIPT_DERIVED")
    code_mentions = [p for p in (ua, reg) if "expiry_source" in p]
    assert "`expiry_source`" in gl and not code_mentions
    f[("T09", "expiry_source")] = dict(location="glossary.md 128", origin="DOCUMENTED", presence_scope="NO_INSTANCE",
                                       applicability_scope="NO_INSTANCE", requirement_scope="NO_INSTANCE",
                                       source_basis="parsed: in the glossary only; no code in the packet builds it",
                                       provenance="SCRIPT_DERIVED")
    assert "ABSENT_AT_SENSITIVITY(<value>)" in gl and "No slot holds it yet" in gl
    f[("T02", "value")] = dict(location="glossary.md 129; expiry_register.py 228-235", origin="DOCUMENTED", presence_scope="NO_INSTANCE",
                               applicability_scope="NO_INSTANCE", requirement_scope="NO_INSTANCE",
                               source_basis="parsed: the notation's parameter; the glossary says no slot holds the state",
                               provenance="SCRIPT_DERIVED")
    m = re.search(r"EXPIRY_KEYS = \(([^)]*)\)", reg); ekeys = re.findall(r'"(\w+)"', m.group(1))
    sig = re.search(r"def E\(([^)]*)\)", reg).group(1)
    eparams = [x.split("=")[0].strip() for x in sig.split(",")]
    assert ekeys == ["instrument_class", "sensitivity", "protocol", "provenance"] and eparams == ["instrument", "protocol", "provenance", "sensitivity"]
    assert 'sorted(e) != sorted(EXPIRY_KEYS)' in reg
    for k in ekeys:
        some = k == "sensitivity"                               # may be "void" (exit incomplete)
        f[("T15", k)] = dict(location="expiry_register.py 53, 58-59, 216-225", origin="RAW_INPUT", presence_scope="ALL_EXCLUSIVE",
                             applicability_scope="SOME_EXCLUSIVE" if some else "ALL_EXCLUSIVE",
                             requirement_scope="ALL_EXCLUSIVE",
                             source_basis="parsed: EXPIRY_KEYS; exit_state() refuses any other key set%s"
                                          % ("; sensitivity may be 'void'" if some else "; refused if '' or 'void'"),
                             provenance="SCRIPT_DERIVED")
    f[("T15", "instrument")] = dict(location="expiry_register.py 58-59", origin="PARAMETER_ONLY", presence_scope="NONE",
                                    applicability_scope="NONE", requirement_scope="NONE",
                                    source_basis="parsed: a parameter of E(), stored as instrument_class",
                                    provenance="SCRIPT_DERIVED")
    return f

def numcheck_facts():
    src = rd(NC); ev = rd(EVID)
    blank = src[src.index("def _blank"):src.index("def _units")]
    inter = src[src.index("def check_intersection"):src.index("def check_all")]
    bis = src[src.index("def _bisect_point"):src.index("def _polynomial_proof")]
    for k in ("proposal", "void_reason"): assert '"%s": None' % k in blank
    for k in ("first_undecided_subbox", "first_subbox_with_no_value"): assert re.search(r'\n        rec\["%s"\] = ' % k, inter)
    for k in ("straddle_at_depth_limit", "first_straddling_piece"): assert '"%s"' % k in bis
    assert '"undecided_at_depth_limit"' in inter
    assert "proposal is None on every record whose verdict is not UNDECIDED here: True" in ev
    assert "every non-None `bisection` record has the same key set whatever the verdict" in ev
    f = {}
    def put(tid, k, loc, origin, pres, app, basis):
        f[(tid, k)] = dict(location="check.py " + loc, origin=origin, presence_scope=pres, applicability_scope=app,
                           requirement_scope="NONE", source_basis=basis, provenance="CODER_INFERRED")
    put("T01", "proposal", "112-119, 296-350, 421", "COMPUTED", "SHARED", "SOME_EXCLUSIVE",
        "presence parsed from _blank (every record); populated only on an UNDECIDED point record at tolerance 0 with nothing against "
        "it (lines 304-305, 421); check_rules_output.txt agrees on 12 records")
    put("T01", "first_undecided_subbox", "513-528, 538, 541-552", "COMPUTED", "SHARED", "SHARED",
        "presence parsed (assigned on every intersection record); populated when a subbox is undecided at the depth limit, which "
        "can also happen on a MIXED or ONE_FAILS record (verdict precedence 541-552); the 13-record derive corpus did not show that")
    put("T01", "straddle_at_depth_limit", "200, 219, 226-227", "COMPUTED", "SHARED", "SHARED",
        "a count inside the bisection record, whose key set is the same whatever the verdict (check_rules_output.txt); "
        "non-zero on a MIXED record too (227: MIXED wins when pieces hold and fail)")
    put("T01", "first_straddling_piece", "201, 220, 240", "COMPUTED", "SHARED", "SHARED",
        "inside the bisection record (same key set whatever the verdict); set whenever a piece straddles at the limit, MIXED included")
    put("T01", "undecided_at_depth_limit", "479-480, 519, 533", "COMPUTED", "SHARED", "SHARED",
        "a count inside rec['subboxes'] on every intersection record; non-zero on MIXED / ONE_FAILS too")
    put("T07", "void_reason", "112, 436-439, 545-548, 553-556, 571-574", "RAW_INPUT", "SHARED", "ALL_EXCLUSIVE",
        "presence parsed from _blank (every record, None); set on every VOID path and on no other (the reason string is recorded raw)")
    put("T07", "first_subbox_with_no_value", "516-517, 539, 541-548", "COMPUTED", "SHARED", "SHARED",
        "presence parsed (every intersection record); set when a subbox has no value at the limit, which a ONE_FAILS / MIXED record "
        "can also carry; absent from point VOID records")
    return f

def cases_of(s, routes):
    scopes = [s[k] for k in ("presence_scope", "applicability_scope", "requirement_scope")]
    c = []
    if routes >= 2: c.append("G")
    if s["origin"] == "DOCUMENTED": c.append("D")
    if s["origin"] == "PARAMETER_ONLY": c.append("E")
    if s["origin"] == "COMPUTED" and any(x in ("ALL_EXCLUSIVE", "SOME_EXCLUSIVE") for x in scopes): c.append("B")
    if s["origin"] == "RAW_INPUT" and "ALL_EXCLUSIVE" in scopes: c.append("A")
    if "ALL_EXCLUSIVE" not in scopes and "SOME_EXCLUSIVE" in scopes: c.append("F")
    if all(x in ("SHARED", "NONE") for x in scopes): c.append("C")
    return c

# --------------------------------------------------------------------------------------------- the reader half
# (reader folder, term, field) -> (verbatim quote from that reader's source_lines_read, basis_kind, uncertainty_stated)
# A quote must contain the field's name. Coded by the Claude Code session (CODER_INFERRED for basis_kind).
Q = {
 ("2026-11-18_claude-v2-A", "T01", "proposal"): ("proposal exists only for UNDECIDED at tolerance 0, so I put 'proposal' in specific", "APPLICABLE_ONLY", None),
 ("2026-11-18_claude-v2-A", "T01", "straddle_at_depth_limit"): ("straddle_at_depth_limit and undecided_at_depth_limit are keys inside nested records (bisection, subboxes). I put them in specific because they are tied to this verdict, and I am unsure that is right", "APPLICABLE_ONLY", True),
 ("2026-11-18_claude-v2-A", "T01", "undecided_at_depth_limit"): ("straddle_at_depth_limit and undecided_at_depth_limit are keys inside nested records (bisection, subboxes). I put them in specific because they are tied to this verdict, and I am unsure that is right", "APPLICABLE_ONLY", True),
 ("2026-11-18_claude-v2-A", "T01", "first_straddling_piece"): ("first_straddling_piece 240, returns None meaning UNDECIDED", "OTHER", None),
 ("2026-11-18_claude-v2-A", "T01", "first_undecided_subbox"): ("first_undecided_subbox 520/538, UNDECIDED 549-550", "OTHER", None),
 ("2026-11-18_claude-v2-A", "T02", "value"): ("The notation parameter is spelled '<value>' in the glossary", "DOCUMENTED", None),
 ("2026-11-18_claude-v2-A", "T04", "kind"): ("kind, target and condition all required", "REQUIRED", None),
 ("2026-11-18_claude-v2-A", "T04", "target"): ("kind, target and condition all required", "REQUIRED", None),
 ("2026-11-18_claude-v2-A", "T04", "condition"): ("kind, target and condition all required", "REQUIRED", None),
 ("2026-11-18_claude-v2-A", "T05", "covers_effect"): ("covers_effect is a reading added here that refuses nothing", "DERIVED_BUT_TIED", None),
 ("2026-11-18_claude-v2-A", "T05", "limit"): ("absent_at_sensitivity(limit, basis, effect_size, conditions, ladder=None) sets those attributes plus covers_effect on a Token", "PARAMETER", None),
 ("2026-11-18_claude-v2-A", "T05", "basis"): ("absent_at_sensitivity(limit, basis, effect_size, conditions, ladder=None) sets those attributes plus covers_effect on a Token", "PARAMETER", None),
 ("2026-11-18_claude-v2-A", "T05", "effect_size"): ("absent_at_sensitivity(limit, basis, effect_size, conditions, ladder=None) sets those attributes plus covers_effect on a Token", "PARAMETER", None),
 ("2026-11-18_claude-v2-A", "T05", "conditions"): ("absent_at_sensitivity(limit, basis, effect_size, conditions, ladder=None) sets those attributes plus covers_effect on a Token", "PARAMETER", None),
 ("2026-11-18_claude-v2-A", "T05", "ladder"): ("absent_at_sensitivity(limit, basis, effect_size, conditions, ladder=None) sets those attributes plus covers_effect on a Token", "PARAMETER", None),
 ("2026-11-18_claude-v2-A", "T07", "void_reason"): ("void_reason set on the VOID paths", "APPLICABLE_ONLY", None),
 ("2026-11-18_claude-v2-A", "T07", "first_subbox_with_no_value"): ("intersection VOID with first_subbox_with_no_value", "APPLICABLE_ONLY", None),
 ("2026-11-18_claude-v2-A", "T08", "exception"): ("CRASHED must be on INSTRUMENT and needs exception and path", "REQUIRED", None),
 ("2026-11-18_claude-v2-A", "T08", "path"): ("CRASHED must be on INSTRUMENT and needs exception and path", "REQUIRED", None),
 ("2026-11-18_claude-v2-A", "T08", "call"): ("'call' and 'inputs' are names in the spec prose only", "DOCUMENTED", None),
 ("2026-11-18_claude-v2-A", "T08", "inputs"): ("'call' and 'inputs' are names in the spec prose only", "DOCUMENTED", None),
 ("2026-11-18_claude-v2-A", "T09", "expiry_condition"): ("expiry_condition and expiry_source are the exits documented for it", "DOCUMENTED", None),
 ("2026-11-18_claude-v2-A", "T09", "expiry_source"): ("expiry_condition and expiry_source are the exits documented for it", "DOCUMENTED", None),
 ("2026-11-18_claude-v2-A", "T10", "error"): ("_dispatch writes the section record {error, exception_type, missing_path} only on a raise", "STORED_FIELD", None),
 ("2026-11-18_claude-v2-A", "T10", "exception_type"): ("_dispatch writes the section record {error, exception_type, missing_path} only on a raise", "STORED_FIELD", None),
 ("2026-11-18_claude-v2-A", "T10", "missing_path"): ("it is the only kind that carries missing_path", "STORED_FIELD", None),
 ("2026-11-18_claude-v2-A", "T12", "triggers"): ("unknown(reason, triggers) refuses without a typed trigger", "PARAMETER", None),
 ("2026-11-18_claude-v2-A", "T12", "typed"): ("the Token gains typed and untyped", "STORED_FIELD", None),
 ("2026-11-18_claude-v2-A", "T12", "untyped"): ("the Token gains typed and untyped", "STORED_FIELD", None),
 ("2026-11-18_claude-v2-A", "T14", "sigma"): ("CLOSED_WITHIN needs a numeric sigma and a basis", "REQUIRED", None),
 ("2026-11-18_claude-v2-A", "T14", "basis"): ("CLOSED_WITHIN needs a numeric sigma and a basis", "REQUIRED", None),
 ("2026-11-18_claude-v2-A", "T15", "instrument_class"): ("a dict with instrument_class, sensitivity, protocol, provenance", "STORED_FIELD", None),
 ("2026-11-18_claude-v2-A", "T15", "sensitivity"): ("a dict with instrument_class, sensitivity, protocol, provenance", "STORED_FIELD", None),
 ("2026-11-18_claude-v2-A", "T15", "protocol"): ("a dict with instrument_class, sensitivity, protocol, provenance", "STORED_FIELD", None),
 ("2026-11-18_claude-v2-A", "T15", "provenance"): ("a dict with instrument_class, sensitivity, protocol, provenance", "STORED_FIELD", None),
 ("2026-11-19_kimi-v2-A", "T01", "proposal"): ("proposal is generated only for qualifying UNDECIDED point checks", "APPLICABLE_ONLY", None),
 ("2026-11-19_kimi-v2-A", "T01", "first_undecided_subbox"): ("first_undecided_subbox is specific to the intersection UNDECIDED path", "APPLICABLE_ONLY", None),
 ("2026-11-19_kimi-v2-A", "T02", "value"): ("value is the parameter in the notation", "DOCUMENTED", None),
 ("2026-11-19_kimi-v2-A", "T04", "kind"): ("ExpiryTrigger requires and stores kind, target, and condition", "REQUIRED", None),
 ("2026-11-19_kimi-v2-A", "T04", "target"): ("ExpiryTrigger requires and stores kind, target, and condition", "REQUIRED", None),
 ("2026-11-19_kimi-v2-A", "T04", "condition"): ("ExpiryTrigger requires and stores kind, target, and condition", "REQUIRED", None),
 ("2026-11-19_kimi-v2-A", "T05", "covers_effect"): ("covers_effect is an additional absence-only derived attribute", "DERIVED_BUT_TIED", None),
 ("2026-11-19_kimi-v2-A", "T07", "void_reason"): ("void_reason records the VOID cause", "APPLICABLE_ONLY", None),
 ("2026-11-19_kimi-v2-A", "T07", "first_subbox_with_no_value"): ("first_subbox_with_no_value is specific to the intersection VOID path", "APPLICABLE_ONLY", None),
 ("2026-11-19_kimi-v2-A", "T08", "exception"): ("CRASHED requires exception and path", "REQUIRED", None),
 ("2026-11-19_kimi-v2-A", "T08", "path"): ("CRASHED requires exception and path", "REQUIRED", None),
 ("2026-11-19_kimi-v2-A", "T08", "exc"): ("the dedicated crash() constructor also has the crash-specific parameters exc and inputs", "PARAMETER", None),
 ("2026-11-19_kimi-v2-A", "T08", "inputs"): ("the dedicated crash() constructor also has the crash-specific parameters exc and inputs", "PARAMETER", None),
 ("2026-11-19_kimi-v2-A", "T09", "expiry_condition"): ("No field is exclusive to UNKNOWN: expiry_condition also serves PENDING and other coverage kinds", "SHARED_SO_NOT", None),
 ("2026-11-19_kimi-v2-A", "T10", "error"): ("A crash produces a section record with error, exception_type, and missing_path", "STORED_FIELD", None),
 ("2026-11-19_kimi-v2-A", "T10", "exception_type"): ("A crash produces a section record with error, exception_type, and missing_path", "STORED_FIELD", None),
 ("2026-11-19_kimi-v2-A", "T10", "missing_path"): ("Those crash-section fields and missing_path distinguish this path from UNKNOWN and INFO coverage entries", "STORED_FIELD", None),
 ("2026-11-19_kimi-v2-A", "T12", "triggers"): ("triggers is the UNKNOWN constructor's parameter", "PARAMETER", None),
 ("2026-11-19_kimi-v2-A", "T12", "typed"): ("the returned Token stores typed and untyped", "STORED_FIELD", None),
 ("2026-11-19_kimi-v2-A", "T12", "untyped"): ("the returned Token stores typed and untyped", "STORED_FIELD", None),
 ("2026-11-19_kimi-v2-A", "T14", "sigma"): ("CLOSED_WITHIN specifically requires numeric sigma and basis", "REQUIRED", None),
 ("2026-11-19_kimi-v2-A", "T14", "basis"): ("CLOSED_WITHIN specifically requires numeric sigma and basis", "REQUIRED", None),
 ("2026-11-19_kimi-v2-A", "T15", "instrument"): ("E() has the constructor parameter instrument", "PARAMETER", None),
 ("2026-11-19_kimi-v2-A", "T15", "instrument_class"): ("its returned expiry dictionary spells the corresponding key instrument_class", "STORED_FIELD", None),
 ("2026-11-19_kimi-v2-A", "T15", "sensitivity"): ("the other three keys are sensitivity, protocol, and provenance", "STORED_FIELD", None),
 ("2026-11-19_kimi-v2-A", "T15", "protocol"): ("the other three keys are sensitivity, protocol, and provenance", "STORED_FIELD", None),
 ("2026-11-19_kimi-v2-A", "T15", "provenance"): ("the other three keys are sensitivity, protocol, and provenance", "STORED_FIELD", None),
 ("2026-11-19_gpt6-v2", "T05", "covers_effect"): ("derived covers_effect on a Token", "DERIVED_BUT_TIED", None),
 ("2026-11-19_gpt6-v2", "T05", "limit"): ("implementation stores limit, basis, effect_size, conditions, ladder", "STORED_FIELD", None),
 ("2026-11-19_gpt6-v2", "T05", "basis"): ("implementation stores limit, basis, effect_size, conditions, ladder", "STORED_FIELD", None),
 ("2026-11-19_gpt6-v2", "T05", "effect_size"): ("implementation stores limit, basis, effect_size, conditions, ladder", "STORED_FIELD", None),
 ("2026-11-19_gpt6-v2", "T05", "conditions"): ("implementation stores limit, basis, effect_size, conditions, ladder", "STORED_FIELD", None),
 ("2026-11-19_gpt6-v2", "T05", "ladder"): ("implementation stores limit, basis, effect_size, conditions, ladder", "STORED_FIELD", None),
 ("2026-11-19_gpt6-v2", "T07", "void_reason"): ("Point VOID writes void_reason", "APPLICABLE_ONLY", None),
 ("2026-11-19_gpt6-v2", "T08", "exception"): ("CRASHED requires exception/path on a Reading", "REQUIRED", None),
 ("2026-11-19_gpt6-v2", "T08", "path"): ("CRASHED requires exception/path on a Reading", "REQUIRED", None),
 ("2026-11-19_gpt6-v2", "T08", "inputs"): ("The spec's crash record additionally names inputs", "DOCUMENTED", None),
 ("2026-11-19_gpt6-v2", "T12", "typed"): ("implementation stores typed and untyped trigger tuples on the Token", "STORED_FIELD", None),
 ("2026-11-19_gpt6-v2", "T12", "untyped"): ("implementation stores typed and untyped trigger tuples on the Token", "STORED_FIELD", None),
 ("2026-11-19_gpt6-v2", "T12", "triggers"): ("The constructor parameter `triggers` is not a returned field", "OTHER", None),
 ("2026-11-19_gpt6-v2", "T14", "sigma"): ("Spec requires sigma and basis", "REQUIRED", None),
 ("2026-11-19_gpt6-v2", "T14", "basis"): ("Spec requires sigma and basis", "REQUIRED", None),
}
ROUTES = {"T08": 2, "T09": 2}
KINDS = ("PARAMETER", "STORED_FIELD", "REQUIRED", "APPLICABLE_ONLY", "DOCUMENTED", "DERIVED_BUT_TIED", "SHARED_SO_NOT", "OTHER")

def build():
    key = json.load(open(os.path.join(BASE, "scoring", "key_v2_a1.json"), encoding="utf-8"))["terms"]
    resp = {r: json.load(open(os.path.join(BASE, "readings", r, "response.json"), encoding="utf-8")) for r in READINGS}
    facts = {}
    for part in (cplay_facts(), taf_facts(), numcheck_facts()):
        facts.update(part)
    # catalog: every name any coded reader or key a1 lists, after N1
    cat = {}
    for t in key:
        names = {n1(x) for x in (key[t]["slots_specific"] or [])}
        for r in resp: names |= {n1(x) for x in resp[r]["terms"][t]["slots_specific"]}
        cat[t] = sorted(names)
    missing = [(t, f) for t in cat for f in cat[t] if (t, f) not in facts]
    assert not missing, "catalog fields with no source fact: %r" % missing
    unused = [k for k in facts if k[1] not in cat.get(k[0], [])]
    assert not unused, "source facts for fields nobody names: %r" % unused
    for (r, t, f), (q, kind, unc) in Q.items():
        assert kind in KINDS, kind
        assert q in resp[r]["terms"][t]["source_lines_read"], "quote not verbatim in %s %s: %r" % (r, t, q)
        assert f.lower() in q.lower() or (f == "value" and "<value>" in q), "quote does not name %s: %r" % (f, q)
        assert f in cat[t], (r, t, f)
    recs = []
    for r, variant in READINGS.items():
        rl = {t: {n1(x) for x in resp[r]["terms"][t]["slots_specific"]} for t in key}
        for t in sorted(cat):
            for f in cat[t]:
                s = dict(facts[(t, f)]); s["routes"] = ROUTES.get(t, 1); s["cases"] = cases_of(s, s["routes"])
                q = Q.get((r, t, f))
                ks = key[t]["slots_specific"]
                recs.append({
                    "study_id": "M01", "reader_id": r,
                    "packet": {"version": "v2", "variant": variant, "sha256": V2A_SHA if variant == "A" else None},
                    "condition": "D0", "term_id": t, "term": key[t]["term_id"], "field": f, "source": s,
                    "reader": {"listed": "LISTED" if f in rl[t] else "NOT_LISTED",
                               "basis_quote": q[0] if q else None,
                               "basis_kind": q[1] if q else None,
                               "basis_kind_provenance": "CODER_INFERRED" if q else "NOT_RECORDED",
                               "uncertainty_stated": q[2] if q else None,
                               "provenance": "READER_STATED"},
                    "key_a1": {"listed": "KEY_UNDETERMINED" if ks is None else ("LISTED" if f in {n1(x) for x in ks} else "NOT_LISTED")}})
    return recs, cat

def report(recs, cat):
    rdrs = list(READINGS)
    short = {"2026-11-18_claude-v2-A": "claude", "2026-11-19_kimi-v2-A": "kimi", "2026-11-19_gpt6-v2": "gpt6"}
    by = {(x["reader_id"], x["term_id"], x["field"]): x for x in recs}
    L = ["M01 coding of the filed v2 readings (descriptive; the coder had seen all three readings; see M01_CRITERIA.md section 1)",
         "readers: " + ", ".join("%s=%s" % (short[r], r) for r in rdrs) + " ; condition D0 ; one coder (Claude Code session)", "",
         "1. per field: L = listed, . = not listed ; key a1: L / . / n/d", "",
         "%-4s %-27s %-7s %-6s %-5s %-5s %-7s %s" % ("term", "field", "origin", "cases", "claude", "kimi", "gpt6", "key a1 | presence / applicability / requirement")]
    for t in sorted(cat):
        for f in cat[t]:
            x = by[(rdrs[0], t, f)]; s = x["source"]
            mark = lambda r: "L" if by[(r, t, f)]["reader"]["listed"] == "LISTED" else "."
            k = {"LISTED": "L", "NOT_LISTED": ".", "KEY_UNDETERMINED": "n/d"}[x["key_a1"]["listed"]]
            L.append("%-4s %-27s %-7s %-6s %-5s %-5s %-7s %-4s| %s / %s / %s%s" % (t, f, s["origin"][:7], "".join(s["cases"]), mark(rdrs[0]), mark(rdrs[1]), mark(rdrs[2]),
                     k, s["presence_scope"], s["applicability_scope"], s["requirement_scope"], "  [coder]" if s["provenance"] == "CODER_INFERRED" else ""))
    L += ["", "2. per case cell: fields in the cell, and how many each reader / key a1 lists (a field can sit in several cells)", ""]
    desc = {"A": "exclusive raw field", "B": "exclusive computed field", "C": "shared field", "D": "documented only",
            "E": "parameter, not a stored field", "F": "on some instances only", "G": "two routes to the instance"}
    for c in "ABCDEFG":
        cell = [(t, f) for t in sorted(cat) for f in cat[t] if c in by[(rdrs[0], t, f)]["source"]["cases"]]
        cnt = lambda r: sum(by[(r, t, f)]["reader"]["listed"] == "LISTED" for t, f in cell)
        kc = sum(by[(rdrs[0], t, f)]["key_a1"]["listed"] == "LISTED" for t, f in cell)
        kn = sum(by[(rdrs[0], t, f)]["key_a1"]["listed"] == "KEY_UNDETERMINED" for t, f in cell)
        L.append("%s %-31s n=%-3d claude %d  kimi %d  gpt6 %d  key a1 %d%s" % (c, desc[c], len(cell), cnt(rdrs[0]), cnt(rdrs[1]), cnt(rdrs[2]), kc,
                 (" (+%d n/d)" % kn) if kn else ""))
    L += ["", "3. same list, different stated reasons: fields all three readers list, with each reader's coded basis_kind", ""]
    n3 = 0
    for t in sorted(cat):
        for f in cat[t]:
            xs = [by[(r, t, f)]["reader"] for r in rdrs]
            if all(x["listed"] == "LISTED" for x in xs):
                kinds = [x["basis_kind"] or "-" for x in xs]
                stated = [k for k in kinds if k != "-"]
                flag = "DIFFER" if len(set(stated)) > 1 else ("same" if len(stated) == 3 else "partly stated")
                n3 += flag == "DIFFER"
                L.append("   %-4s %-18s %-16s %-16s %-16s %s" % (t, f, kinds[0], kinds[1], kinds[2], flag))
    L.append("   fields listed by all three with stated reasons of different kinds: %d (a lower bound: silence is not coded as a reason)" % n3)
    L += ["", "4. uncertainty the reader stated about a field", ""]
    for x in recs:
        if x["reader"]["uncertainty_stated"]:
            L.append("   %s %s %s: %r" % (short[x["reader_id"]], x["term_id"], x["field"], x["reader"]["basis_quote"]))
    L += ["", "5. readers agree with each other and not with key a1 (PREREG v2 case (a): a reason to re-read the key's derivation)", ""]
    for t in sorted(cat):
        for f in cat[t]:
            xs = {by[(r, t, f)]["reader"]["listed"] for r in rdrs}
            k = by[(rdrs[0], t, f)]["key_a1"]["listed"]
            if len(xs) == 1 and k != "KEY_UNDETERMINED" and k not in xs:
                L.append("   %-4s %-18s readers all %s, key a1 %s ; origin %s ; cases %s" % (t, f, xs.pop(), k, by[(rdrs[0], t, f)]["source"]["origin"], "".join(by[(rdrs[0], t, f)]["source"]["cases"])))
    L += ["", "inputs: key_v2_a1.json %s ; check_rules_output.txt %s ; numcheck check.py %s" % (
        sha(os.path.join(BASE, "scoring", "key_v2_a1.json"))[:16], sha(EVID)[:16], sha(NC)[:16]),
          "records: %d (%d readers x %d catalog fields)" % (len(recs), len(rdrs), sum(len(v) for v in cat.values()))]
    return "\n".join(L) + "\n"

def validate(recs):
    schema = json.load(open(os.path.join(HERE, "M01_SCHEMA.json"), encoding="utf-8"))["fields"]
    sk = schema["source"]["keys"]; rk = schema["reader"]["keys"]
    for x in recs:
        for k in ("origin", "presence_scope", "applicability_scope", "requirement_scope", "provenance"):
            assert x["source"][k] in sk[k]["enum"], (k, x["source"][k])
        assert all(c in sk["cases"]["items"]["enum"] for c in x["source"]["cases"])
        for k in ("listed", "basis_kind", "basis_kind_provenance", "provenance"):
            assert x["reader"][k] in rk[k]["enum"], (k, x["reader"][k])
        assert x["reader"]["uncertainty_stated"] in (True, None)
        assert x["condition"] in schema["condition"]["enum"]

def main():
    recs, cat = build()
    validate(recs)
    out = {"records": json.dumps(recs, indent=1, ensure_ascii=False) + "\n", "report": report(recs, cat)}
    paths = {"records": os.path.join(HERE, "m01_records.json"), "report": os.path.join(HERE, "m01_report.txt")}
    if "--check" in sys.argv:
        bad = [k for k in out if not os.path.exists(paths[k]) or open(paths[k], encoding="utf-8").read() != out[k]]
        print("m01 --check: " + ("identical" if not bad else "WOULD CHANGE: " + ", ".join(bad)))
        sys.exit(1 if bad else 0)
    for k in out:
        with open(paths[k], "w", encoding="utf-8") as fh: fh.write(out[k])
    print(out["report"])

if __name__ == "__main__":
    main()
