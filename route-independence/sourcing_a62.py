# SPDX-License-Identifier: CC0-1.0
"""WORK ORDER standing/A-6.2 (2026-09-29): the physical sourcing rule.

Landed verbatim as WORK_ORDER_A6.2_2026-09-29_physical-sourcing.md and committed ALONE at
EXPECTED_COMMIT_A62 before this module existed.  Additive: A-1..A-6.1 modules are read by
import; only standing_a61.py gains a grade on its two derived counts (item 2).

  0  rule 0: SOURCED iff url + retrieval_date + verbatim span stored + sha256 of the span.
     No reader, no grade: [CHOICE 84] reads four fields and nothing else.
  1  every MATCH row A-1..A-6.1 re-gated under rule 0, read-only; span_stored / hash per row
  2  a derived count inherits its weakest parent's grade and is printed with it
  3  identity pins (position, token, unit) per credited count, A-4, A-5, A-6, A-6.1
  4  unit/noun agreement as a second signal; proximity and agreement disagree = FLAG
  5  the single-aggregate-case condition over A-1..A-5
  6  E-A6-3 rescoped to the enumerated forms of 25 CFR 83.11(b)(1)-(2); ITEM vs COMBINATION
  7  residence coding LITERAL vs GEOGRAPHIC, both kept
  8  span intake for 83.11, and the re-evaluation that reads the store

Nothing here read a source.  The 83.11 structure is the work order's own item 6, read in
chat from the LII mirror; its span is NOT stored, so every row resting on it is unsourced.
Nothing here is legal advice or a statement of law beyond a cited text.
"""
import hashlib
import itertools
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import chains_a4 as C          # noqa: E402
import repairs_a31 as R        # noqa: E402
import standing_a61 as S61     # noqa: E402

EXPECTED_COMMIT_A62 = "0fdeda9"
ORDER_FILE = "WORK_ORDER_A6.2_2026-09-29_physical-sourcing.md"
SPAN_STORE = os.path.join(HERE, "span_store.json")

SOURCED, NOT_SOURCED = "SOURCED", "NOT_SOURCED"
UNSOURCED_PASS = "UNSOURCED_PASS"
CONSTRUCTED_PASS = S61.CONSTRUCTED_PASS
UNFALSIFIABLE_AS_RUN = S61.UNFALSIFIABLE_AS_RUN
NOT_EVALUABLE = S61.NOT_EVALUABLE
NE_BY_CONSTRUCTION = "NOT_EVALUABLE_BY_CONSTRUCTION"
NE_TRUNCATED = "NOT_EVALUABLE_TRUNCATED_RETRIEVAL"
NOT_RECORDED = S61.NOT_RECORDED
FLAG = "FLAG"
CARRIED, CONSTRUCTED, IN_REPO = "CARRIED", "CONSTRUCTED", "IN_REPO"
URL_RULE, REPO_ADDRESS = "URL_RULE", "REPO_ADDRESS"
ITEM, COMBINATION = "ITEM", "COMBINATION"
LITERAL, GEOGRAPHIC = "LITERAL", "GEOGRAPHIC"

CHOICES = {
    84: "rule 0 as a check: SOURCED iff the record's url field is an http(s) url, retrieval_date is an ISO date, "
        "span is a non-empty string, and sha256 is 64 hex equal to sha256(span utf-8); the check reads those four "
        "fields and no other, so no reader and no grade enters it",
    85: "a carried source record's text field is the carrier's description, never a verbatim span; only a field "
        "named span counts as stored, and span_stored / hash are reported per source as Y/N",
    86: "an input that is this repository's own text or code is read two ways: URL_RULE (rule 0 as worded: no "
        "http(s) url, NOT_SOURCED) and REPO_ADDRESS (repo:<commit>:<path>, the committed file as the span); the "
        "status uses URL_RULE and REPO_ADDRESS is printed beside it; the choice between them is the operator's",
    87: "the rule-0 gate over a raw MATCH: falsifier cases not enumerated, or one aggregate case -> "
        "UNFALSIFIABLE_AS_RUN; any CONSTRUCTED input -> CONSTRUCTED_PASS; any input not SOURCED under [CHOICE 84] "
        "(and every row naming no input) -> UNSOURCED_PASS; else MATCH; it replaces [CHOICE 81]",
    88: "a derived value inherits the weakest grade among its parents (NOT_RECORDED is off the order and wins); it "
        "prints as 'value [grade G via ids]'; a printed line carrying a derived label without that tag is a FAIL",
    89: "an identity pin is (position in the normalised EXPECTED block, token, unit) for every credited count; the "
        "window rule's unit is the first '(unit: X)' in its 80-character window, the A-3.1 unit for an OK token",
    90: "agreement: the words between the nearest count and its annotation, split on non-letters and singularised "
        "(ies->y, ves->f, trailing s); AGREE if one equals the unit's last word singularised, NO_NOUN if there are "
        "none; AGREE or NO_NOUN assigns, DISAGREE is a FLAG and assigns nothing",
    91: "the single-aggregate-case condition is a declared reading per row (AGGREGATE_READING): the row's "
        "falsifier ranges over one case that stands for members the run does not enumerate",
    92: "83.11(b) as item 6 states it: (b)(1) 11 forms plus an open catch-all, two or more required; (b)(2) 5 "
        "forms, one sufficient; ITEM counts the 16 enumerated forms; COMBINATION counts (b)(1) subsets of size "
        ">= 2 plus (b)(2) singletons; sets mixing (b)(1) and (b)(2) forms are supersets of a sufficient set and "
        "are not counted; the open remainder is NOT_EVALUABLE_BY_CONSTRUCTION",
    93: "residence coding: LITERAL codes the forms whose text carries the word 'reside' (word boundary, so "
        "'residence' does not match), GEOGRAPHIC the forms carrying residence|land|area; before a span is stored "
        "the coded form ids are item 7's; under COMBINATION a path presumes residence if it contains a coded form",
    94: "span intake appends one record to span_store.json, refuses a record rule 0 does not pass and a url other "
        "than the one declared for a known source id, and never overwrites; the E-A6-3 re-evaluation reads the "
        "store and, for an 83.11 span, parses the (b)(1)/(b)(2) markers and recodes residence from the span; "
        "(b) and (c) count only at a line start, (1), (2) and roman markers only between whitespace, and a span "
        "the parse cannot read is STRUCTURE_NOT_PARSED, never guessed",
}


class SourcingError(ValueError):
    pass


# ---------------------------------------------------------------- 0: rule ---

_URL = re.compile(r"^https?://[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/\S*)?$")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_HEX = re.compile(r"^[0-9a-f]{64}$")
_LOCATOR = re.compile(r"\b[a-z0-9-]+(\.[a-z0-9-]+)+\.(gov|org|com|edu|us)\b|~\d{4}")


def sha256_of(span):
    return hashlib.sha256(span.encode("utf-8")).hexdigest()


def rule0(rec, reading=URL_RULE):
    """[CHOICE 84] Four fields; nothing else is read."""
    url, date, span, digest = rec.get("url"), rec.get("retrieval_date"), rec.get("span"), rec.get("sha256")
    missing = []
    url_ok = isinstance(url, str) and (_URL.match(url) is not None or
                                       (reading == REPO_ADDRESS and url.startswith("repo:")))
    if not url_ok:
        missing.append("url")
    if not (isinstance(date, str) and _DATE.match(date)):
        missing.append("retrieval_date")
    span_ok = isinstance(span, str) and span.strip() != ""
    if not span_ok:
        missing.append("span")
    hash_ok = isinstance(digest, str) and _HEX.match(digest) is not None and span_ok and digest == sha256_of(span)
    if not hash_ok:
        missing.append("sha256")
    return {"status": SOURCED if not missing else NOT_SOURCED, "missing": missing,
            "url": url_ok, "span_stored": span_ok, "hash": hash_ok}


def load_store(path=SPAN_STORE):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)["records"]


def store_record(source_id, store):
    hits = [r for r in store if r.get("source_id") == source_id]
    return sorted(hits, key=lambda r: r.get("retrieval_date") or "")[-1] if hits else None


def _carried_table():
    import gate_state_a21 as G21
    t = dict(G21.SOURCES21)
    t.update(S61.SOURCES_A61)
    return t


_GIT_CACHE = {}


def repo_record(path):
    """[CHOICE 86] REPO_ADDRESS: the committed file at its last commit is the span."""
    if path in _GIT_CACHE:
        return _GIT_CACHE[path]
    out = subprocess.run(["git", "log", "-n", "1", "--format=%h %cs", "--", path], cwd=HERE,
                         capture_output=True, text=True).stdout.split()
    if len(out) != 2:
        rec = {}
    else:
        body = subprocess.run(["git", "show", "%s:./%s" % (out[0], path)], cwd=HERE,
                              capture_output=True, text=True).stdout
        rec = {"url": "repo:%s:route-independence/%s" % (out[0], path), "retrieval_date": out[1], "span": body,
               "sha256": sha256_of(body)}
    _GIT_CACHE[path] = rec
    return rec


def source_status(source_id, kind, store=None, reading=URL_RULE):
    store = load_store() if store is None else store
    rec = store_record(source_id, store)
    if rec is None:
        if kind == IN_REPO:
            rec = repo_record(source_id)
        elif kind == CARRIED:
            rec = _carried_table().get(source_id, {})
        else:
            rec = {}
    return dict(rule0(rec, reading), source_id=source_id, kind=kind, from_store=store_record(source_id, store) is not None,
                locator_in_text=_LOCATOR.search(rec.get("text") or "") is not None)


def gate_a62(raw, inputs, enumerated=True, single_aggregate=False, store=None, reading=URL_RULE):
    """[CHOICE 87] No row reads MATCH on input rule 0 does not source."""
    if raw != "MATCH":
        return raw
    if not enumerated or single_aggregate:
        return UNFALSIFIABLE_AS_RUN
    if any(k == CONSTRUCTED for _, k in inputs):
        return CONSTRUCTED_PASS
    if not inputs or any(source_status(sid, k, store, reading)["status"] != SOURCED for sid, k in inputs):
        return UNSOURCED_PASS
    return "MATCH"


# ----------------------------------------------------- 1 and 5: the re-run ---

A31_FILES = tuple(f for a, f in R.AMENDMENTS if a in ("A-1", "A-2", "A-2.1", "A-3"))
_K = [("CONSTRUCTED rows", CONSTRUCTED)]

ROW_INPUTS = (   # module, row id prefix, inputs, basis  (read from each row's own fixture sources)
    ("settlement_split", "E-A1 majority CONSTRUCTED", _K, "the coded route rows"),
    ("settlement_split", "E-A1 at least 2 of 3", _K, "the three cases' edges"),
    ("gate_state", "E-A2-1 (reading)", [("W-1", CARRIED)], "F-W1 / F-W2 cite W-1"),
    ("gate_state", "E-A2-2", [("G-1", CARRIED), ("G-2", CARRIED)], "F-G1 / F-G2"),
    ("gate_state", "E-A2-3", [("W-1", CARRIED), ("W-2", CARRIED), ("W-3", CARRIED), ("G-2", CARRIED)],
     "CO, UT, TX, England at 2026"),
    ("gate_state", "E-A2-4", [("gate_state.py", IN_REPO)], "the module's code (AST)"),
    ("gate_state_a21", "E-A2.1-1", [("W-1a", CARRIED), ("W-2a", CARRIED)], "CO, UT at 2026"),
    ("gate_state_a21", "E-A2.1-2", [("W-1a", CARRIED), ("W-2a", CARRIED), ("W-3", CARRIED), ("G-2", CARRIED)],
     "the E-A2-3 rows under A-2.1"),
    ("thermal_gates", "E-A3-1 (reading)", _K, "F-T4"),
    ("thermal_gates", "E-A3-5", _K, "T-1, T-8, C-1"),
    ("repairs_a31", "E-A3.1-1 (LITERAL_ALL)", [(f, IN_REPO) for f in A31_FILES], "the landed EXPECTED blocks"),
    ("repairs_a31", "E-A3.1-1 (DECLARED_LITERAL)", [(f, IN_REPO) for f in A31_FILES], "the landed EXPECTED blocks"),
    ("repairs_a31", "E-A3.1-2 (EVIDENCE)", _K, "63 prior rows"),
    ("repairs_a31", "E-A3.1-2 (SCHEMA_DEFAULT)", _K, "63 prior rows"),
    ("chains_a4", "E-A4-1 (transitive steps)", _K, "5 gates, 0 sourced"),
    ("termini_a5", "E-A5-1 (LAWFUL_STRICT)", _K, "11 chains"),
    ("termini_a5", "E-A5-4 (without hops)", _K, "12 FWO-5 routes"),
)
A61_INPUTS = {"E-A6.1-1": [("CS-R routes", CONSTRUCTED), ("G-T3", CONSTRUCTED)],
              "E-A6.1-3": [("CE-3", CARRIED), ("CE-3f", CARRIED)]}
NAMED_ROWS = ("E-A2-1", "E-A2-2", "E-A2-3", "E-A2.1-1", "E-A2.1-2")

AGGREGATE_READING = {   # [CHOICE 91] row prefix -> (single aggregate case?, basis)
    "E-A1 majority CONSTRUCTED": (False, "24 decided rows, each enumerated"),
    "E-A1 at least 2 of 3": (False, "three cases, each one instance"),
    "E-A2-1 (reading)": (False, "two fixture rows"),
    "E-A2-2": (False, "one England event from two rows"),
    "E-A2-3": (False, "four jurisdictions, each one rule"),
    "E-A2-4": (False, "the module's expressions"),
    "E-A2.1-1": (False, "three jurisdictions"),
    "E-A2.1-2": (False, "the E-A2-3 rows"),
    "E-A3-1 (reading)": (False, "one fixture, F-T4, enumerated"),
    "E-A3-5": (False, "one coupling, with and without"),
    "E-A3.1-1 (LITERAL_ALL)": (False, "16 registry entries"),
    "E-A3.1-1 (DECLARED_LITERAL)": (False, "16 registry entries"),
    "E-A3.1-2 (EVIDENCE)": (False, "63 rows"),
    "E-A3.1-2 (SCHEMA_DEFAULT)": (False, "63 rows"),
    "E-A4-1 (transitive steps)": (False, "5 gates over 7 steps"),
    "E-A5-1 (LAWFUL_STRICT)": (False, "11 chains"),
    "E-A5-4 (without hops)": (False, "12 routes"),
    "E-A6.1-1": (False, "3 routes, one coupling"),
    "E-A6.1-3": (True, "1 aggregate case; 0 of the 200+ village corporations enumerated"),
}


def erratum_sweep_ran_aggregate_condition():
    """Item 5: read the erratum's sweep.  The third argument of its gate call is a constant."""
    import ast
    import inspect
    tree = ast.parse(inspect.getsource(S61.prior_sweep))
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "gate_status"]
    consts = [n.args[2].value for n in calls if len(n.args) > 2 and isinstance(n.args[2], ast.Constant)]
    return {"ran": not (calls and len(consts) == len(calls) and all(c is True for c in consts)),
            "evidence": "standing_a61.prior_sweep calls gate_status(raw, grades, %s) on every row" % consts}


def rerun(store=None):
    """Item 1, read-only: every MATCH row A-1..A-6.1 under the old gate and under rule 0."""
    old = dict(((x["module"], x["row"]), x) for x in S61.prior_sweep()["rows"])
    out = []
    for mod, prefix, inputs, basis in ROW_INPUTS:
        o = old[(mod, prefix)]
        agg = AGGREGATE_READING[prefix][0]
        st = [source_status(sid, k, store) for sid, k in inputs]
        out.append({"row": prefix, "module": mod, "raw": o["raw"], "old": o["gated"],
                    "old_no_aggregate": S61.gate_status(o["raw"], o["grades"], not agg),
                    "new": gate_a62(o["raw"], inputs, True, agg, store),
                    "repo_address": gate_a62(o["raw"], inputs, True, agg, store, REPO_ADDRESS),
                    "inputs": inputs, "sources": st, "basis": basis})
    for r in S61.check_expectations():
        if r["raw"] != "MATCH":
            continue
        inputs = A61_INPUTS[r["id"]]
        agg = AGGREGATE_READING[r["id"]][0]
        out.append({"row": r["id"], "module": "standing_a61", "raw": r["raw"], "old": r["status"],
                    "old_no_aggregate": r["status"], "new": gate_a62(r["raw"], inputs, True, agg, store),
                    "repo_address": gate_a62(r["raw"], inputs, True, agg, store, REPO_ADDRESS),
                    "inputs": inputs, "sources": [source_status(s, k, store) for s, k in inputs],
                    "basis": AGGREGATE_READING[r["id"]][1]})
    return out


def order_lint():
    toks = R.count_tokens(open(os.path.join(HERE, ORDER_FILE), encoding="utf-8").read())
    return {"tokens": len(toks), "ok": [(t["token"], t["unit"], t["context"][:16]) for t in toks if t["status"] == R.OK],
            "saw_2036": any(t["token"] == "2036" for t in toks)}


def yn(sources, key):
    n = len([s for s in sources if s[key]])
    return "%s %d/%d" % ("Y" if sources and n == len(sources) else "N", n, len(sources))


# ------------------------------------------------------------ 2: derived ---

LII_ID = "LII-83.11"
PARENT_GRADES = {LII_ID: NOT_RECORDED, "CE-4": S61.SOURCES_A61["CE-4"]["grade"],
                 "CE-4e": S61.SOURCES_A61["CE-4e"]["grade"]}
DERIVED_LABELS = ("outside the retrieved text", "derived:")
_TAG = re.compile(r"\[grade [A-Z_/]+ via [^\]]+\]")


def weakest(grades):
    """[CHOICE 88]"""
    if any(g not in S61.GRADE_RANK for g in grades):
        return NOT_RECORDED
    return min(grades, key=lambda g: S61.GRADE_RANK[g])


def derived(label, value, parents):
    g = weakest([PARENT_GRADES[p] for p in parents])
    return {"label": label, "value": value, "grade": g, "via": tuple(parents),
            "text": "derived: %s %s [grade %s via %s]" % (label, value, g, ", ".join(parents))}


def derived_print_check(text, labels=DERIVED_LABELS):
    """[CHOICE 88] Every line carrying a derived label carries its grade tag; else FAIL."""
    bad = [ln for ln in text.splitlines() if any(lb in ln for lb in labels) and not _TAG.search(ln)]
    return {"status": "FAIL" if bad else "PASS", "lines": bad}


def committed_a61_sample(commit="37c8e58"):
    return subprocess.run(["git", "show", "%s:./samples/standing_a61.sample.txt" % commit], cwd=HERE,
                          capture_output=True, text=True).stdout


# ---------------------------------------------------- 3 and 4: pins / lint ---

PIN_FILES = ("AMENDMENT_A4_2026-09-28_route-chains.md", "AMENDMENT_A5_2026-09-28_terminus-diversity.md",
             "AMENDMENT_A6_2026-09-28_eligibility-recognition.md",
             "AMENDMENT_A6.1_2026-09-28_standing-scarcity-consolidation.md")
_ANN = re.compile(r"\(unit:\s*([A-Za-z ]+?)\)")
_LETTERS = re.compile(r"[A-Za-z]+")


def window_identities(text):
    """[CHOICE 89] the A-4 window rule ([CHOICE 51]) as identities."""
    toks = S61.attach_nearest(text)
    out = []
    for t in toks:
        start = text.find(t["context"])
        m = _ANN.search(text[start:start + 80])
        if t["status"] == R.OK:
            out.append((t["pos"], t["token"], t["unit"].lower()))
        elif m is not None:
            out.append((t["pos"], t["token"], m.group(1).strip().lower()))
    return out


def nearest_identities(text):
    return [(t["pos"], t["token"], (t["owns"] or t["unit"]).lower())
            for t in S61.attach_nearest(text) if t["annotated"]]


def sing(w):
    w = w.lower()
    if w.endswith("ies"):
        return w[:-3] + "y"
    if w.endswith("ves"):
        return w[:-3] + "f"
    if w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def agreement(between, unit):
    """[CHOICE 90]"""
    words = [sing(w) for w in _LETTERS.findall(between)]
    if not words:
        return "NO_NOUN"
    return "AGREE" if sing(unit.split()[-1]) in words else "DISAGREE"


def attach_agree(text):
    """[CHOICE 90] proximity ([CHOICE 78]) and agreement; a disagreement is a FLAG, never an owner."""
    toks = R.count_tokens(text)
    pos = S61._positions(text, toks)
    owner, flags = {}, []
    for m in _ANN.finditer(text):
        unit = m.group(1).strip().lower()
        prev = [i for i, q in enumerate(pos) if q + len(toks[i]["token"]) <= m.start()
                and m.start() - (q + len(toks[i]["token"])) <= 80]
        if not prev:
            continue
        near = prev[-1]
        sig = agreement(text[pos[near] + len(toks[near]["token"]):m.start()], unit)
        if sig in ("AGREE", "NO_NOUN"):
            owner[near] = unit
        else:
            cand = [toks[i]["token"] for i in prev[:-1]
                    if agreement(text[pos[i] + len(toks[i]["token"]):m.start()], unit) == "AGREE"]
            flags.append({"unit": unit, "nearest": toks[near]["token"], "nearest_pos": pos[near],
                          "agreeing": cand, "context": text[pos[near]:m.end()]})
    ann = [dict(t, pos=pos[i], owns=owner.get(i), annotated=(t["status"] == R.OK or i in owner))
           for i, t in enumerate(toks)]
    return {"tokens": ann, "flags": flags,
            "identities": [(t["pos"], t["token"], (t["owns"] or t["unit"]).lower()) for t in ann if t["annotated"]]}


def pins(fname):
    text = C.expected_block(fname)
    w, n, a = window_identities(text), nearest_identities(text), attach_agree(text)
    return {"file": fname, "window": w, "nearest": n, "agree": a["identities"], "flags": a["flags"],
            "window_to_nearest": (sorted(set(w) - set(n)), sorted(set(n) - set(w))),
            "nearest_to_agree": (sorted(set(n) - set(a["identities"])), sorted(set(a["identities"]) - set(n)))}


NON_NEAREST_FIXTURE = "3 routes via 2 chains (unit: routes)"


def non_nearest_fixture():
    text = "Expected: %s." % NON_NEAREST_FIXTURE
    near = S61.attach_nearest(text)
    agr = attach_agree(text)
    return {"nearest_owner": [t["token"] for t in near if t["owns"]],
            "agree_owner": [t["token"] for t in agr["tokens"] if t["owns"]], "flags": agr["flags"]}


# ----------------------------------------------------- 6 and 7: 83.11(b) ---

ROMAN = ("i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi")
STRUCTURE_83_11 = {"b1": 11, "b2": 5, "b1_min": 2, "b2_min": 1, "b1_open_catch_all": True,
                   "b2_also_satisfies": "(c)",
                   "cross_links": ("(b)(1)(xi)", "(b)(2)(v)", "(c)(1)(iv)", "(c)(2)(ii)"),
                   "source": LII_ID, "read": "in chat 2026-09-29 (work order item 6); span NOT stored"}
LII_URL = "https://www.law.cornell.edu/cfr/text/25/83.11"
DECLARED_URLS = {LII_ID: LII_URL}
RESIDENCE_FORMS = {LITERAL: ("(b)(2)(i)",), GEOGRAPHIC: ("(b)(2)(i)", "(b)(1)(ix)", "(b)(1)(x)")}   # item 7
RESIDENCE_PATTERN = {LITERAL: re.compile(r"\breside\b", re.I),
                     GEOGRAPHIC: re.compile(r"\b(residence|land|area)\b", re.I)}
RIN_139_TARGET = ("complete 25 CFR 83.11(b)(2) path list", "enumerated forms, 83.11(b)(1)-(2)")


def forms(structure=STRUCTURE_83_11):
    return (["(b)(1)(%s)" % r for r in ROMAN[:structure["b1"]]],
            ["(b)(2)(%s)" % r for r in ROMAN[:structure["b2"]]])


def paths(definition, structure=STRUCTURE_83_11):
    """[CHOICE 92] each path is a tuple of form ids."""
    b1, b2 = forms(structure)
    if definition == ITEM:
        return [(f,) for f in b1 + b2]
    if definition == COMBINATION:
        out = [c for k in range(structure["b1_min"], len(b1) + 1) for c in itertools.combinations(b1, k)]
        return out + [(f,) for f in b2]
    raise SourcingError("definition is ITEM or COMBINATION; got %r" % definition)


def residence_count(definition, coding, coded=None, structure=STRUCTURE_83_11):
    """[CHOICE 93]"""
    coded = RESIDENCE_FORMS[coding] if coded is None else coded
    ps = paths(definition, structure)
    return {"definition": definition, "coding": coding, "paths": len(ps),
            "residence": len([p for p in ps if any(f in coded for f in p)]), "coded": tuple(coded)}


def score_rescoped(store=None, structure=STRUCTURE_83_11, coded_by=None):
    """E-A6-3 over the enumerated forms, 2 definitions x 2 codings x 2 thresholds."""
    inputs = [(LII_ID, CARRIED)]
    rows = []
    for d in (ITEM, COMBINATION):
        for cd in (LITERAL, GEOGRAPHIC):
            rc = residence_count(d, cd, None if coded_by is None else coded_by[cd], structure)
            for eid in ("E-A6-3 REVISED", "E-A6-3 ERRATUM"):
                raw = S61._v(eid, rc["residence"])
                rows.append(dict(rc, row=eid, raw=raw, status=gate_a62(raw, inputs, True, False, store)))
    rows.append({"row": "E-A6-3 open remainder", "definition": "ANY", "coding": "ANY", "raw": NE_BY_CONSTRUCTION,
                 "status": NE_BY_CONSTRUCTION, "paths": None, "residence": None, "coded": (),
                 "reason": "(b)(1) closes on 'or by other evidence'; no complete path list can exist"})
    return rows


# ----------------------------------------------------------- 8: intake ---

def intake(source_id, url, retrieval_date, span, store_path=SPAN_STORE):
    """[CHOICE 94] Append one record; refuse what rule 0 does not pass; never overwrite."""
    if source_id in DECLARED_URLS and url != DECLARED_URLS[source_id]:
        raise SourcingError("%s is declared at %s; got %r" % (source_id, DECLARED_URLS[source_id], url))
    rec = {"source_id": source_id, "url": url, "retrieval_date": retrieval_date, "span": span,
           "sha256": sha256_of(span) if isinstance(span, str) else None}
    r = rule0(rec)
    if r["status"] != SOURCED:
        raise SourcingError("rule 0 not met: missing %s" % r["missing"])
    data = {"records": load_store(store_path)}
    if any(x.get("source_id") == source_id and x.get("sha256") == rec["sha256"] for x in data["records"]):
        return rec
    data["records"].append(rec)
    data["note"] = "append-only span store, rule 0 [CHOICE 94]; nothing is edited or removed"
    with open(store_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return rec


def _seek(text, marker, start, end, line_start=False):
    """[CHOICE 94] A paragraph marker preceded by whitespace (or at a line start) and followed by
    whitespace; '(c)(1)(iv)' and 'toward (c)(2)' are cross-references, not markers."""
    lead = r"(^[ \t]*)" if line_start else r"(^|\s)"
    m = re.compile(lead + re.escape(marker) + r"(?=\s)", re.M).search(text, start, end)
    return -1 if m is None else m.start() + len(m.group(1))


def parse_83_11(span):
    """[CHOICE 94] (b)(1) and (b)(2) form texts in order; None when the markers are not found."""
    b = _seek(span, "(b)", 0, len(span), line_start=True)
    if b < 0:
        return None
    c = _seek(span, "(c)", b, len(span), line_start=True)
    c = len(span) if c < 0 else c
    p1 = _seek(span, "(1)", b, c)
    p2 = _seek(span, "(2)", p1 + 1, c) if p1 >= 0 else -1
    if p1 < 0 or p2 < 0:
        return None
    out = {}
    for key, lo, hi in (("b1", p1, p2), ("b2", p2, c)):
        cur, items = lo, []
        for r in ROMAN:
            q = _seek(span, "(%s)" % r, cur, hi)
            if q < 0:
                break
            items.append(q)
            cur = q + 1
        out[key] = [span[q:(items[i + 1] if i + 1 < len(items) else hi)] for i, q in enumerate(items)]
    out["b1_open_catch_all"] = re.search(r"other evidence", span[p1:p2], re.I) is not None
    return out


def reevaluate_e_a6_3(store=None):
    """Item 8: under rule 0, from the store."""
    store = load_store() if store is None else store
    rec = store_record(LII_ID, store)
    if rec is None:
        return {"state": "NO_SPAN_STORED", "rows": score_rescoped(store)}
    parsed = parse_83_11(rec["span"])
    if parsed is None:
        return {"state": "STRUCTURE_NOT_PARSED", "rows": []}
    got = {"b1": len(parsed["b1"]), "b2": len(parsed["b2"]), "b1_open_catch_all": parsed["b1_open_catch_all"]}
    want = dict((k, STRUCTURE_83_11[k]) for k in got)
    if got != want:
        return {"state": "STRUCTURE_MISMATCH", "parsed": got, "declared": want, "rows": []}
    b1, b2 = forms()
    texts = dict(zip(b1 + b2, parsed["b1"] + parsed["b2"]))
    coded = dict((cd, tuple(f for f in b1 + b2 if RESIDENCE_PATTERN[cd].search(texts[f]))) for cd in (LITERAL,
                                                                                                        GEOGRAPHIC))
    return {"state": "SPAN_STORED", "coded_from_span": coded,
            "coding_agrees_with_item_7": dict((cd, set(coded[cd]) == set(RESIDENCE_FORMS[cd])) for cd in coded),
            "rows": score_rescoped(store, coded_by=coded)}


OPEN_TARGETS_A62 = (
    {"target": "LII span of 25 CFR 83.11, stored (url, date, span, sha256)", "blocks": "E-A6-3 rescoped (item 8)",
     "now": "no record in span_store.json"},
    {"target": "official edition check: govinfo annual CFR, 25 CFR 83.11", "blocks": "LII read as the regulation",
     "now": "unsourced; LII is not the official edition"},
    {"target": RIN_139_TARGET[1], "blocks": "E-A6-3 (was: %s)" % RIN_139_TARGET[0], "now": "structure from chat"},
    {"target": "a stored span for every carried source (W-*, G-*, CE-*)", "blocks": "every row item 1 re-gated",
     "now": "0 records"},
    {"target": "operator decision: does a repo:<commit>:<path> address meet rule 0's url",
     "blocks": "E-A2-4, E-A3.1-1 x2", "now": "URL_RULE applied; REPO_ADDRESS printed beside"},
)


def fail_fixture():
    """The erratum's gate reads MATCH on a row resting on carried grades with no stored span;
    rule 0 does not."""
    return {"old": S61.gate_status("MATCH", ["S"], True),
            "rule0": gate_a62("MATCH", [("G-2", CARRIED)], True, False, store=[])}


# ---------------------------------------------------------------- render ---

def render(out=None, store=None):
    wr = (out or sys.stdout).write
    store = load_store() if store is None else store
    rows = rerun(store)
    wr("sourcing_a62 -- WORK ORDER standing/A-6.2: the physical sourcing rule over A-1..A-6.1\n")
    wr("order registered at %s; span store records: %d; nothing read here\n\n" % (EXPECTED_COMMIT_A62, len(store)))
    wr("-- what did not hold, first\n")
    kept = [r for r in rows if r["old"] == "MATCH"]
    wr("   the erratum's sweep kept %d rows at MATCH on carried grades; under rule 0 %d of them read MATCH\n"
       % (len(kept), len([r for r in kept if r["new"] == "MATCH"])))
    full = [r for r in rows if r["sources"] and all(x["span_stored"] and x["hash"] for x in r["sources"])]
    wr("   rows whose every input has a span and a matching hash: %d of %d, all %s; none has a url; the other %d "
       "rest on carried or constructed inputs with no span stored (span store records: %d) [CHOICE 84] "
       "[CHOICE 85]\n" % (len(full), len(rows), "this repository's own files" if all(
           k == IN_REPO for r in full for _, k in r["inputs"]) else "mixed", len(rows) - len(full), len(store)))
    rp = [r for r in rows if r["repo_address"] == "MATCH"]
    wr("   rule 0's 'url' has no slot for this repository's own text: %d rows read MATCH under REPO_ADDRESS and "
       "UNSOURCED_PASS under URL_RULE; status uses URL_RULE [CHOICE 86]\n" % len(rp))
    dc = derived_print_check(committed_a61_sample())
    wr("   the A-6.1 render at 37c8e58 printed %d derived counts without a grade: %s [CHOICE 88]\n"
       % (len(dc["lines"]), dc["status"]))
    flips = [(p["file"], f) for p in [pins(f) for f in PIN_FILES] for f in p["flags"]]
    wr("   agreement flags %d count(s) the nearest rule credits: %s [CHOICE 90]\n"
       % (len(flips), ["%s: %r" % (f[:10], x["context"]) for f, x in flips]))
    wr("   under LITERAL coding E-A6-3 (erratum, >= 3) reads %s on both path definitions\n"
       % sorted(set(r["raw"] for r in score_rescoped(store) if r["coding"] == LITERAL and r["row"] ==
                    "E-A6-3 ERRATUM")))
    wr("   rule 0 checks reproducibility, not authenticity: a constructed span with the declared url passes it "
       "(test_sourcing_a62.py, a temp store)\n")
    lo = order_lint()
    wr("   A-3.1 lint on the order: %d count tokens, %d OK; 2036 seen: %s ([CHOICE 30] drops a four-digit token in "
       "1000..2999); OK tokens %s\n" % (lo["tokens"], len(lo["ok"]), lo["saw_2036"], lo["ok"]))
    wr("\n-- item 0: rule 0 [CHOICE 84]; the gate [CHOICE 87] replaces [CHOICE 81]\n")
    wr("   fields read: url, retrieval_date, span, sha256; reader: not a field; grade: not a field\n")
    wr("\n-- item 1: every MATCH row A-1..A-6.1, read-only (old = [CHOICE 81], new = rule 0)\n")
    wr("   %-30s %-6s %-17s %-20s %-6s %-6s %-6s %s\n" % ("row", "raw", "old", "new", "url", "span", "hash",
                                                         "repo_address"))
    for r in rows:
        mark = " <- named in item 1" if any(r["row"].startswith(n + " ") or r["row"] == n for n in NAMED_ROWS) else ""
        wr("   %-30s %-6s %-17s %-20s %-6s %-6s %-6s %s%s\n"
           % (r["row"][:30], r["raw"], r["old"][:17], r["new"], yn(r["sources"], "url"),
              yn(r["sources"], "span_stored"), yn(r["sources"], "hash"), r["repo_address"], mark))
    wr("   an IN_REPO span is the committed file at its last commit, its hash computed here, not stored [CHOICE 86]\n")
    for n in NAMED_ROWS:
        r = [x for x in rows if x["row"] == n or x["row"].startswith(n + " ")][0]
        for s in r["sources"]:
            wr("   %-9s %-6s url %-5s date %-5s span %-5s hash %-5s locator in text %-5s missing %s\n"
               % (n, s["source_id"], s["url"], "retrieval_date" not in s["missing"], s["span_stored"], s["hash"],
                  s["locator_in_text"], s["missing"]))
    wr("   rows reading MATCH under rule 0: %d\n" % len([r for r in rows if r["new"] == "MATCH"]))
    wr("\n-- item 2: derived counts carry their parent's grade [CHOICE 88]\n")
    for d in derived_values():
        wr("   %s\n" % d["text"])
    wr("   check on the A-6.1 render at 37c8e58: %s (%d lines); on the current A-6.1 render: %s\n"
       % (dc["status"], len(dc["lines"]), derived_print_check(_a61_render())["status"]))
    wr("\n-- item 3: identity pins (position, token, unit) [CHOICE 89]\n")
    for f in PIN_FILES:
        p = pins(f)
        wr("   %-62s credited window %d, nearest %d, agree %d\n" % (f, len(p["window"]), len(p["nearest"]),
                                                                    len(p["agree"])))
        for tag, (gone, new) in (("window -> nearest", p["window_to_nearest"]),
                                 ("nearest -> agree", p["nearest_to_agree"])):
            for x in gone:
                wr("      %-17s - %r\n" % (tag, x))
            for x in new:
                wr("      %-17s + %r\n" % (tag, x))
    wr("\n-- item 4: non-nearest fixture %r [CHOICE 90]\n" % NON_NEAREST_FIXTURE)
    nf = non_nearest_fixture()
    wr("   nearest rule assigns to %s; agreement rule assigns to %s; flags %s\n"
       % (nf["nearest_owner"], nf["agree_owner"], [(x["nearest"], x["agreeing"], x["unit"]) for x in nf["flags"]]))
    wr("\n-- item 5: the single-aggregate-case condition [CHOICE 91]\n")
    ea = erratum_sweep_ran_aggregate_condition()
    wr("   run in the erratum's sweep: %s (%s)\n" % (ea["ran"], ea["evidence"]))
    cp = [r for r in rows if r["old"] == CONSTRUCTED_PASS and r["module"] != "standing_a61"]
    ch = [r for r in cp if r["old_no_aggregate"] != r["old"]]
    wr("   of the %d prior rows A-1..A-5 at CONSTRUCTED_PASS, %d change label under the condition: %s; of all %d rows "
       "only E-A6.1-3 is a single aggregate case, and it already read UNFALSIFIABLE_AS_RUN\n"
       % (len(cp), len(ch), [r["row"] for r in ch], len(rows)))
    for r in rows:
        agg, basis = AGGREGATE_READING[r["row"]]
        wr("   %-30s single aggregate %-5s %s\n" % (r["row"][:30], agg, basis))
    wr("\n-- items 6 and 7: E-A6-3 rescoped to %r [CHOICE 92] [CHOICE 93]\n" % RIN_139_TARGET[1])
    wr("   structure (%s, %s): (b)(1) %d forms + open catch-all, >= %d required; (b)(2) %d forms, %d sufficient, "
       "also satisfies %s; cross-links %s\n"
       % (STRUCTURE_83_11["source"], STRUCTURE_83_11["read"], STRUCTURE_83_11["b1"], STRUCTURE_83_11["b1_min"],
          STRUCTURE_83_11["b2"], STRUCTURE_83_11["b2_min"], STRUCTURE_83_11["b2_also_satisfies"],
          ", ".join(STRUCTURE_83_11["cross_links"])))
    for r in score_rescoped(store):
        if r["paths"] is None:
            wr("   %-22s %s: %s\n" % (r["row"], r["status"], r["reason"]))
            continue
        wr("   %-15s [path=%s coding=%s] %s; raw %-17s status %s\n"
           % (r["row"], r["definition"], r["coding"],
              derived("residence-presuming of", "%d of %d" % (r["residence"], r["paths"]), [LII_ID])["text"],
              r["raw"], r["status"]))
    wr("   previous reason (erratum, retrieved (b)(2)(i)..(iv)): %s; this reason: %s\n"
       % (NE_TRUNCATED, NE_BY_CONSTRUCTION))
    wr("\n-- item 8: span intake [CHOICE 94]\n")
    ev = reevaluate_e_a6_3(store)
    wr("   %s at %s: %s\n" % (LII_ID, LII_URL, ev["state"]))
    wr("   run: python3 route-independence/sourcing_a62.py intake %s <retrieval_date> <span_file>\n" % LII_ID)
    wr("\n-- open sourcing targets\n")
    for t in OPEN_TARGETS_A62:
        wr("   %-66s blocks %-30s now %s\n" % (t["target"][:66], t["blocks"][:30], t["now"]))
    ff = fail_fixture()
    wr("\nfail fixture: the erratum's gate reads %s on a carried-S row with no stored span; rule 0 reads %s\n"
       % (ff["old"], ff["rule0"]))
    wr("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))
    wr("execution note: test_sourcing_a62.py prints the check count; samples/sourcing_a62.sample.txt is one "
       "recorded render, compare before quoting\n")


def derived_values():
    rp = S61.residence_presuming_paths()
    b1, b2 = forms()
    retrieved = ["(b)(2)(%s)" % r for r in ROMAN[:rp["retrieved"]]]
    return [
        derived("unread paths outside the retrieved text (erratum bound)",
                rp["outside_retrieved_text"]["total"], ["CE-4e", "CE-4"]),
        derived("residence-presuming outside the retrieved text (erratum bound)",
                rp["outside_retrieved_text"]["residence_presuming"], ["CE-4e", "CE-4"]),
        derived("enumerated forms outside the retrieved text (ITEM)", len(b1 + b2) - len(retrieved),
                [LII_ID, "CE-4"]),
    ] + [derived("residence-presuming enumerated forms outside the retrieved text (%s)" % cd,
                 len([f for f in RESIDENCE_FORMS[cd] if f not in retrieved]), [LII_ID, "CE-4"])
         for cd in (LITERAL, GEOGRAPHIC)] + [
        derived("COMBINATION paths from (b)(1) alone", len(paths(COMBINATION)) - len(b2), [LII_ID]),
    ]


def _a61_render():
    import io
    buf = io.StringIO()
    S61.render(buf)
    return buf.getvalue()


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_sourcing_a62.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    if argv[:1] == ["intake"]:
        if len(argv) != 4:
            sys.stderr.write("usage: sourcing_a62.py intake <source_id> <retrieval_date> <span_file>\n")
            return 2
        with open(argv[3], encoding="utf-8") as fh:
            span = fh.read()
        rec = intake(argv[1], DECLARED_URLS.get(argv[1], ""), argv[2], span)
        print("stored %s sha256 %s" % (rec["source_id"], rec["sha256"]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
