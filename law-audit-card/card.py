"""card.py -- load and read a law audit card. CC0, stdlib only.

PROPOSED | co-authored (JinnZ2 + Claude).

The tools read; they do not decide anyone's value (READ_ME_THIS_WAY section 4).
This module checks a card's shape, derives three fields, and never writes a
disposition of its own. It only FORCES `UNRESOLVED` when `evidence` or
`cut_sensitivity` is VOID.

Every field is a dict {"tag", "value", "basis"} with tag one of
OBSERVED / DERIVED / PROPOSED / VOID. VOID means no information: value is
null, and the field is still written, never omitted.

Derived here (a card may assert them; an assertion that disagrees is refused):
  cut_sensitivity   from >= 2 declared boundaries (declared-frame `boundary`),
                    each with an evidence reading: FLIPS / HOLDS, else VOID
  circularity       enforcement.enforcer == evaluator.evaluator
                    -> CONDITIONAL(circular_eval); differ -> INDEPENDENT_AS_DECLARED;
                    either VOID -> VOID
  scope_valid       when the card carries `taf_audit`, run through TAF
                    core/regulatory_scope_audit.py (imported, not reimplemented)

Usage:
  python3 card.py CARD.json [CARD.json ...]    read cards
  (checks: python3 tests/test_card.py)
"""
import ast
import importlib.util
import io
import json
import os
import re
import sys

TAGS = ("OBSERVED", "DERIVED", "PROPOSED", "VOID")
FIELDS = ("stated_purpose", "target_outcome", "enforcement", "evidence", "cut_sensitivity",
          "scope_valid", "last_tested", "evaluator", "circularity", "anchor_date", "disposition")
DERIVED_FIELDS = ("cut_sensitivity", "circularity")
# Reader vocabulary. REVISE replaces the earlier REDO so it does not read as the
# correction notice's REBUILD (section G, which applies to parts of a report).
DISPOSITIONS = ("KEEP", "EDIT", "REVISE", "RETIRE", "UNRESOLVED")
DISPOSITION_MAP = {"REDO": "REVISE",
                   "REBUILD": "not a disposition: correction notice section G, parts of a REPORT"}
READINGS = ("SUPPORTS", "DOES_NOT_SUPPORT", "UNDETERMINED")
CIRCULAR = "CONDITIONAL(circular_eval)"
INDEPENDENT = "INDEPENDENT_AS_DECLARED"

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


class CardRefused(ValueError):
    pass


# ---------------------------------------------------------------- declared-frame
def _load_by_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def frame_boundary_field():
    """The cut is declared-frame's `boundary`; read the field name from its checker."""
    df = _load_by_path("df_check_frame", os.path.join(REPO, "declared-frame", "v2", "check_frame.py"))
    assert "boundary" in df.CORE
    return "boundary"


# ---------------------------------------------------------------- TAF pointer
def taf_path():
    p = os.environ.get("TAF_PATH")
    cands = [p] if p else []
    cands += [os.path.join(os.path.dirname(REPO), "thermodynamic-accountability-framework"),
              os.path.join(os.path.dirname(REPO), "Thermodynamic-Accountability-Framework")]
    for c in cands:
        f = c and os.path.join(c, "core", "regulatory_scope_audit.py")
        if f and os.path.isfile(f):
            return f
    return None


def taf_module():
    f = taf_path()
    return _load_by_path("taf_regulatory_scope_audit", f) if f else None


def taf_verdicts():
    """The bracketed verdict labels, read from TAF's ScopeAudit.summary() source."""
    f = taf_path()
    if not f:
        return None
    with io.open(f, encoding="utf-8") as fh:
        src = fh.read()
    return tuple(sorted(set(re.findall(r"\[(IN SCOPE|OUT OF SCOPE -- [A-Z ]+)\]", src))))


def derive_scope(card):
    """Run a card's taf_audit block through TAF; return (tag, value, basis) or a NOT_TESTABLE note."""
    block = card.get("taf_audit")
    if not block:
        return None
    mod = taf_module()
    if mod is None:
        return ("NOT_TESTABLE", None, "TAF checkout not found (set TAF_PATH)")
    sp = card["stated_purpose"]
    if sp["tag"] == "VOID":
        return ("VOID", None, "taf_audit needs stated_purpose as first_principle_intent; it is VOID")
    r = block["regulation"]
    reg = mod.Regulation(id=r["id"], title=r.get("title", ""), jurisdiction=r.get("jurisdiction", ""),
                         year_enacted=r.get("year_enacted", 0), first_principle_intent=sp["value"],
                         scope=[mod.ScopeVar(v["name"], tuple(v["valid_range"]), v.get("units", ""))
                                for v in r.get("scope", [])])
    sit = mod.Situation(id=block.get("situation_id", "s"), location=block.get("location", ""),
                        description="", conditions=block["conditions"])
    intent = block.get("intent_still_applicable")
    if not reg.in_scope(sit.conditions) and intent is None:
        # TAF defaults an absent intent check to True; the card does not take that default.
        return ("VOID", None, "out of scope and intent_still_applicable undeclared")
    a = mod.audit(reg, sit, None if intent is None else (lambda _r, _s: bool(intent)))
    label = re.match(r"\[([^\]]+)\]", a.summary()).group(1)
    return ("DERIVED", label, "TAF core/regulatory_scope_audit.py audit(); exits=%s" % a.scope_exits)


# ---------------------------------------------------------------- derivations
def derive_cut(field):
    bs = field.get("boundaries") or []
    key = frame_boundary_field()
    for b in bs:
        if not b.get(key):
            raise CardRefused("cut_sensitivity boundary without a declared-frame %r" % key)
        if b.get("evidence_reading") not in READINGS:
            raise CardRefused("cut_sensitivity reading %r not in %s" % (b.get("evidence_reading"), READINGS))
    read = [b["evidence_reading"] for b in bs if b["evidence_reading"] != "UNDETERMINED"]
    if len(read) < 2:
        return ("VOID", None, "%d boundaries with a determined reading; 2 needed" % len(read))
    return ("DERIVED", "FLIPS" if len(set(read)) > 1 else "HOLDS",
            "%d declared boundaries: %s" % (len(read), ", ".join(read)))


def derive_circularity(card):
    enf, ev = card["enforcement"], card["evaluator"]
    a = enf["value"].get("enforcer") if isinstance(enf.get("value"), dict) else None
    b = ev["value"].get("evaluator") if isinstance(ev.get("value"), dict) else None
    if enf["tag"] == "VOID" or ev["tag"] == "VOID" or not a or not b:
        return ("VOID", None, "enforcer or evaluator not declared")
    if a.strip().lower() == b.strip().lower():
        return ("DERIVED", CIRCULAR, "enforcer and evaluator are both %r" % a)
    return ("DERIVED", INDEPENDENT, "enforcer %r, evaluator %r (as declared, not checked)" % (a, b))


# ---------------------------------------------------------------- shape
def check_field(name, f):
    if not isinstance(f, dict) or "tag" not in f or "value" not in f:
        raise CardRefused("%s: needs tag and value (VOID is written, not omitted)" % name)
    if f["tag"] not in TAGS:
        raise CardRefused("%s: tag %r not in %s" % (name, f["tag"], TAGS))
    if (f["tag"] == "VOID") != (f["value"] is None):
        raise CardRefused("%s: VOID iff value is null" % name)
    if f["tag"] in ("OBSERVED", "PROPOSED") and not f.get("basis"):
        raise CardRefused("%s: %s needs a basis" % (name, f["tag"]))
    if name == "last_tested" and f["value"] is not None:
        if not (f["value"].get("date") and f["value"].get("tester")):
            raise CardRefused("last_tested: needs date and tester, else VOID")
    if name == "disposition" and f["value"] is not None:
        if f["value"].get("value") not in DISPOSITIONS:
            raise CardRefused("disposition: %r not in %s" % (f["value"].get("value"), DISPOSITIONS))
        if not (f["value"].get("reader") and f["value"].get("date")):
            raise CardRefused("disposition: READER-ASSIGNED, needs reader id and date")


def _assert_matches(name, f, tag, value):
    if f["tag"] != "VOID" and f["value"] != value:
        raise CardRefused("%s: card asserts %r, derivation gives %r" % (name, f["value"], value))


def read(card):
    """Return the card with derived fields filled and the disposition forced if it must be."""
    missing = [n for n in FIELDS if n not in card]
    if missing:
        raise CardRefused("missing fields %s (VOID is written, not omitted)" % missing)
    for n in FIELDS:
        check_field(n, card[n])
    out = json.loads(json.dumps(card))
    notes = []
    t, v, b = derive_cut(card["cut_sensitivity"])
    _assert_matches("cut_sensitivity", card["cut_sensitivity"], t, v)
    out["cut_sensitivity"].update(tag=t, value=v, basis=b)
    t, v, b = derive_circularity(card)
    _assert_matches("circularity", card["circularity"], t, v)
    out["circularity"].update(tag=t, value=v, basis=b)
    s = derive_scope(card)
    if s:
        if s[0] == "NOT_TESTABLE":
            notes.append("scope_valid: NOT_TESTABLE, " + s[2])
        else:
            _assert_matches("scope_valid", card["scope_valid"], s[0], s[1])
            out["scope_valid"].update(tag=s[0], value=s[1], basis=s[2])
    elif card["scope_valid"]["tag"] != "VOID":
        tv = taf_verdicts()
        if tv is None:
            notes.append("scope_valid: label unchecked, TAF checkout not found")
        elif card["scope_valid"]["value"] not in tv:
            raise CardRefused("scope_valid: %r not a TAF verdict %s" % (card["scope_valid"]["value"], tv))
    void = [n for n in ("evidence", "cut_sensitivity") if out[n]["tag"] == "VOID"]
    if void:
        prior = card["disposition"]["value"]
        out["disposition"] = {"tag": "DERIVED", "value": {"value": "UNRESOLVED", "reader": None, "date": None},
                              "basis": "forced: %s VOID" % " and ".join(void),
                              "reader_assigned": prior}
    out["_notes"] = notes
    return out


def render(card):
    r = read(card)
    L = ["# law-audit-card | PROPOSED | %s" % card.get("id", "?"),
         "# the tool reads; the disposition is the reader's (READ_ME_THIS_WAY section 4)"]
    for n in FIELDS:
        f = r[n]
        L.append("  %-16s %-9s %s" % (n, f["tag"], json.dumps(f["value"])))
    L += ["  note: " + x for x in r["_notes"]]
    return "\n".join(L)


def load(path):
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def tool_writes_no_disposition(src=None):
    """AST check: no reader disposition literal outside the DISPOSITIONS tuple, its map,
    and this checker's own body (which has to name what it looks for)."""
    if src is None:
        with io.open(os.path.abspath(__file__), encoding="utf-8") as fh:
            src = fh.read()
    tree = ast.parse(src)
    allowed = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") in ("DISPOSITIONS", "DISPOSITION_MAP")
                                                for t in node.targets):
            allowed |= {id(c) for c in ast.walk(node.value)}
        if isinstance(node, ast.FunctionDef) and node.name == "tool_writes_no_disposition":
            allowed |= {id(c) for c in ast.walk(node)}
    return [c.value for c in ast.walk(tree)
            if isinstance(c, ast.Constant) and c.value in ("KEEP", "EDIT", "REVISE", "RETIRE")
            and id(c) not in allowed]


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or any(a.startswith("-") for a in args):
        print("usage: python3 card.py CARD.json [...]   (checks: python3 tests/test_card.py)")
        sys.exit(2)
    for p in args:
        print(render(load(p)))
        print()
