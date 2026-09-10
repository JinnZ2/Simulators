#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""ONTOLOGY PROBE -- the instrument for WORK_ORDER.md.

Three things, no model call anywhere in this file:

  declare   validate primitives.json (section 2) and constructions.jsonl
            (section 3): types, grounding, absent_by_design, class balance,
            the 30 minimum and the 40% control floor. A TARGETED construction
            must name which absent_by_design term it targets.
  prompt    render section 4 for one construction. The prompt text is
            PARSED OUT OF WORK_ORDER.md at call time, never retyped.
  score     section 5 on a JSONL run log: the four fields parsed from each
            response, the per-construction reading, the four aggregates,
            N1..N5, OP-1..OP-5, cross-family disagreement (section 7).
            `--fixture PATH` scores against a construction file admitted
            past the hand_built gate (for exercising the scorer only); the
            report says so on its second line.

Every command takes `--ontology DIR` naming a directory holding
primitives.json and constructions.jsonl; the default is this folder (the
SHAPE_SPEC reading). ontologies/substrate-primary/ is the operator's
hand-built set and carries the first real run.

TWO RUN-LOG FORMS. A RAW record carries `raw_response`, the restater's
four-field text, and the scorer parses it. A CODED record carries the
four fields already coded (`status`, `terms_used`, `terms_added`, plus
`missing_primitive` on a FAILS and a free `note`) and no restatement;
the scorer reads it as delivered, marks the leak check NOT_EVALUABLE
(there is no restatement to read), binds the ontology from `--ontology`
and checks the binding by `terms_used` being inside the primitive list.
A coded sheet is the restater's self-report passed through the operator;
the report says which form it scored.

TWO READOUTS THE ORDER DOES NOT ASK FOR, both mechanical. ABSENT-TERM
COVERAGE: for each absent_by_design term, was it EXERCISED by the run --
named by a construction's `targets`, cited by a FAILS record's
`missing_primitive`, or reached by an alias in `terms_added` -- or
UNEXERCISED, in which case the hole_rate says nothing about it. ALIAS
REIMPORT ([CHOICE 6]): an optional `aliases.json` beside primitives.json
declares, per absent term, the words that would carry it back in under
another name, each with the basis it was written on; `terms_added` is
screened against it, so a restater's "preference reimports
interior_state" note becomes a declared-list hit rather than a
self-report. A word list decides word sense there and is stepped around
by any paraphrase; the file says who wrote it and after which run, and a
hit on a run the list was written in view of is NOT blind. A second
table in the same file, `scope_required`, lists added terms that carry
no value until their scope is declared (boundary, horizon, environment
variables, what is excluded); on a sheet carrying no declaration such an
addition is SCOPE_UNDECLARED, a third state beside reimport and
unmatched -- `efficiency` is the operator's instance, and fold-matrix
registers it as a folded term. Each such entry carries an import_class:
`scope` (a ratio or objective quoted without its frame) or `morality`
(a term that could import a moral gradient -- the operator named market,
capital, monetary and value, with better/worse already an absence -- and
a morality entry must also require `graded_by`, the axis the gradient
runs on and who assigns it, or the loader refuses it as the scope class
under another label). "Any term that could import morality" is an open
class; a term not on the list is UNMATCHED, the absence of a reading.

WHAT THE ORDER LEAVES TO THE RESTATER AND WHAT THIS ADDS. `status` is
self-reported by the restater. The scorer keeps that as the order's
number and adds one mechanical cross-check beside it: the RESTATEMENT's
own content words are read against the primitive list, and a word that
is in neither the list nor `terms_added` nor a declared function-word set
is a LEAK -- an addition the restater made and did not declare. A run
whose status is COMPOSES with a non-empty leak is reported as
`status_contradicted`, counted apart, never re-labelled.

No run exists here. runs/ holds CONSTRUCTED fixtures that say so in every
record. Stdlib only. Parses under 3.9.

    python3 probe.py declare
    python3 probe.py prompt CONSTRUCTION_ID
    python3 probe.py score RUNS.jsonl [--fixture CONSTRUCTIONS.jsonl]
"""

import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = os.path.join(HERE, "WORK_ORDER.md")
PRIMITIVES = os.path.join(HERE, "primitives.json")
CONSTRUCTIONS = os.path.join(HERE, "constructions.jsonl")

TYPES = ("quantity", "relation", "operator", "state")
GROUNDS = ("physics", "declared", "undefined")
CLASSES = ("TARGETED", "AMBIENT", "CONTROL")
STATUSES = ("COMPOSES", "FAILS", "COMPOSES_WITH_ADDITION")
MIN_SET = 30
CONTROL_FLOOR = 0.40
REPEATS = 3

# [CHOICE 1] [PRIMITIVES] is rendered one term per line as `term (type)`;
#            the order fixes no layout.
# [CHOICE 2] COMPOSES_WITH_ADDITION rows sit in every section 5 DENOMINATOR
#            (the order divides by the whole class) and in no numerator;
#            addition_rate is printed per class beside the three rates.
# [CHOICE 3] a restatement leak check is added beside the self-reported
#            status; FUNCTION_WORDS is the declared exclusion list.
# [CHOICE 4] N4 fires when function words are more than half of the
#            smuggle_set; OP-5 reads a primitive set as physics-grounded
#            when at least half its primitives ground to physics.
# [CHOICE 5] `targets` on a TARGETED construction is optional: section 3's
#            schema has no such field, so a set built to the order omits
#            it. When present it must name absent_by_design terms; when
#            absent the construction-to-absence link is read from the
#            run's `missing_primitive` citations instead.
# [CHOICE 6] an optional aliases.json beside primitives.json declares, per
#            absent term, the words that would reimport it; terms_added is
#            screened against it. Declared by whoever wrote the file, with
#            a basis per alias and the run it was written after; a word
#            list, so paraphrase steps around it.
CHOICES = {
    1: "[PRIMITIVES] rendered one `term (type)` per line",
    2: "COMPOSES_WITH_ADDITION rows in every section 5 denominator, in no numerator; addition_rate printed per class",
    3: "restatement leak check added beside the self-reported status; FUNCTION_WORDS declared",
    4: "N4 threshold 0.5 function-word share; OP-5 physics-grounded = at least half of primitives ground to physics",
    5: "`targets` optional on TARGETED (not in the order's schema); checked against absent_by_design when present",
    6: "aliases.json (optional, declared, dated) screens terms_added for reimport of an absent term; a word list, paraphrase steps around it",
}
N4_THRESHOLD = 0.5
PHYSICS_SHARE = 0.5

FUNCTION_WORDS = {
    "a", "an", "the", "of", "to", "in", "on", "at", "by", "for", "with", "from", "as", "into",
    "and", "or", "but", "not", "no", "nor", "if", "then", "than", "that", "this", "these",
    "those", "it", "its", "is", "are", "was", "were", "be", "been", "being", "has", "have",
    "had", "do", "does", "did", "which", "what", "where", "when", "while", "so", "such",
    "there", "here", "over", "under", "across", "between", "through", "each", "any", "all",
    "some", "one", "two", "both", "same", "other", "only", "also", "more", "less", "most",
    "very", "can", "cannot", "may", "will", "would", "should", "could", "s",
}


class Refused(Exception):
    pass


# ----------------------------------------------------------------- order text

def order_text():
    with open(ORDER, encoding="utf-8") as fh:
        return fh.read()


def prompt_template():
    """Section 4 block, dedented, nothing else."""
    text = order_text()
    i = text.index("For each construction, the task is RESTATEMENT, not judgment:")
    j = text.index("If a term outside the list is required", i)
    chunk = text[i:j].split("\n", 1)[1]
    lines = [ln[4:] if ln.startswith("    ") else ln for ln in chunk.split("\n")]
    t = "\n".join(lines).strip("\n")
    for ph in ("[PRIMITIVES]", "[CONSTRUCTION TEXT]"):
        if ph not in t:
            raise Refused("section 4 block lost its %s placeholder" % ph)
    return t


def render_primitives(prims):
    return "\n".join("%s (%s)" % (p["term"], p["type"]) for p in prims["primitives"])


def render_prompt(prims, construction):
    return prompt_template().replace("[PRIMITIVES]", render_primitives(prims)) \
        .replace("[CONSTRUCTION TEXT]", construction["text"])


# ----------------------------------------------------------------- declarations

def load_primitives(path=PRIMITIVES):
    with open(path, encoding="utf-8") as fh:
        p = json.load(fh)
    return validate_primitives(p)


def validate_primitives(p):
    for k in ("name", "version", "primitives", "absent_by_design"):
        if k not in p:
            raise Refused("primitives lacks %r" % k)
    if not p["primitives"]:
        raise Refused("primitives list is empty")
    seen = set()
    for e in p["primitives"]:
        for k in ("term", "type", "grounds_to"):
            if k not in e:
                raise Refused("primitive %r lacks %r" % (e.get("term"), k))
        if e["type"] not in TYPES:
            raise Refused("primitive %r type %r not in %s" % (e["term"], e["type"], TYPES))
        if e["grounds_to"] not in GROUNDS:
            raise Refused("primitive %r grounds_to %r not in %s" % (e["term"], e["grounds_to"], GROUNDS))
        t = e["term"].strip().lower()
        if t in seen:
            raise Refused("primitive %r declared twice" % e["term"])
        seen.add(t)
    if not isinstance(p["absent_by_design"], list):
        raise Refused("absent_by_design must be a list (empty is legal and is reported)")
    for a in p["absent_by_design"]:
        if not a.get("term") or not a.get("reason"):
            raise Refused("absent_by_design entry needs term and reason: %r" % a)
        if a["term"].strip().lower() in seen:
            raise Refused("%r is both a primitive and absent_by_design" % a["term"])
    return p


def primitives_report(p):
    """The section 2 readings that exist before any construction is run."""
    und = [e["term"] for e in p["primitives"] if e["grounds_to"] == "undefined"]
    phys = [e["term"] for e in p["primitives"] if e["grounds_to"] == "physics"]
    return {"name": p["name"], "version": p["version"], "n_primitives": len(p["primitives"]),
            "n_absent_by_design": len(p["absent_by_design"]),
            "claims_no_protection": len(p["absent_by_design"]) == 0,
            "undefined_candidate_holes": und,
            "physics_share": len(phys) / len(p["primitives"]),
            "grounding_class": "physics-grounded" if len(phys) / len(p["primitives"]) >= PHYSICS_SHARE else "declared-only",
            "sha": _sha(json.dumps(p["primitives"], sort_keys=True))}


def _sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def load_constructions(path=CONSTRUCTIONS, prims=None, admit_candidates=False):
    out = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                out.append(json.loads(ln))
    for c in out:
        validate_construction(c, prims)
    if not admit_candidates:
        out = [c for c in out if c.get("hand_built") is True]
    return out


def validate_construction(c, prims=None):
    for k in ("id", "text", "premise", "class", "hand_built"):
        if k not in c:
            raise Refused("construction %s lacks %r" % (c.get("id"), k))
    if c["class"] not in CLASSES:
        raise Refused("construction %s class %r not in %s" % (c["id"], c["class"], CLASSES))
    if not isinstance(c["hand_built"], bool):
        raise Refused("construction %s hand_built must be a bool" % c["id"])
    if c["class"] == "TARGETED" and c.get("targets"):
        if prims is not None:
            absent = {a["term"].strip().lower() for a in prims["absent_by_design"]}
            bad = [t for t in c["targets"] if t.strip().lower() not in absent]
            if bad:
                raise Refused("construction %s targets %s, not in absent_by_design" % (c["id"], bad))
    return c


def set_report(cons):
    n = len(cons)
    by = {k: sum(1 for c in cons if c["class"] == k) for k in CLASSES}
    flags = []
    if n < MIN_SET:
        flags.append("BELOW_MINIMUM (%d < %d)" % (n, MIN_SET))
    if n and by["CONTROL"] / n < CONTROL_FLOOR:
        flags.append("CONTROL_SHORT (%.2f < %.2f)" % (by["CONTROL"] / n, CONTROL_FLOOR))
    if n == 0:
        flags.append("EMPTY")
    return {"n": n, "by_class": by, "control_share": (by["CONTROL"] / n) if n else None, "flags": flags}


def candidates(path=CONSTRUCTIONS):
    return [c for c in load_constructions(path, None, admit_candidates=True) if not c["hand_built"]]


# ----------------------------------------------------------------- runs

REQUIRED = ("run_id", "ontology", "ontology_version", "construction_id", "model", "family",
            "repeat", "date", "raw_response", "constructed")


CODED_REQUIRED = ("run_id", "family", "repeat", "id", "class", "status", "terms_used", "terms_added")


def is_coded(rec):
    return "raw_response" not in rec and "status" in rec and "id" in rec


def adapt_coded(rec, prims):
    """A coded-sheet record into the REQUIRED shape. Nothing is invented:
    a field the sheet does not carry is a stated absence, and the
    ontology is BOUND from the primitive set the caller passed, with the
    binding checked downstream by terms_used being inside that set."""
    for k in CODED_REQUIRED:
        if k not in rec:
            raise Refused("coded record %s lacks %r" % (rec.get("id"), k))
    return {"run_id": "%s|%s" % (rec["run_id"], rec["id"]), "ontology": prims["name"],
            "ontology_version": prims["version"], "construction_id": rec["id"],
            "model": rec.get("model") or "UNKNOWN(coded sheet states family only: %s)" % rec["family"],
            "family": rec["family"], "repeat": rec["repeat"],
            "date": rec.get("date") or "UNDATED(not in coded sheet)",
            "raw_response": None, "constructed": bool(rec.get("constructed", False)),
            "coded": {"status": rec["status"], "terms_used": list(rec["terms_used"]),
                      "terms_added": list(rec["terms_added"]),
                      "missing_primitive": rec.get("missing_primitive"), "note": rec.get("note"),
                      "class": rec.get("class")}}


def load_runs(path, prims=None):
    """Returns (records, form). form is 'raw' or 'coded'; a mixed log is refused."""
    out = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                out.append(json.loads(ln))
    forms = {"coded" if is_coded(r) else "raw" for r in out}
    if len(forms) > 1:
        raise Refused("run log mixes raw and coded records; score them as two logs")
    form = forms.pop() if forms else "raw"
    if form == "coded":
        if prims is None:
            raise Refused("a coded log binds its ontology from --ontology; none given")
        out = [adapt_coded(r, prims) for r in out]
    return out, form


def validate_runs(runs, cons):
    ids = {c["id"] for c in cons}
    seen = set()
    for r in runs:
        for k in REQUIRED:
            if k not in r:
                raise Refused("run %s lacks %r" % (r.get("run_id"), k))
        if r["run_id"] in seen:
            raise Refused("duplicate run_id %s" % r["run_id"])
        seen.add(r["run_id"])
        if r["construction_id"] not in ids:
            raise Refused("run %s names construction %r which is not admitted" % (r["run_id"], r["construction_id"]))
        if not isinstance(r["constructed"], bool):
            raise Refused("run %s constructed must be a bool" % r["run_id"])
        if not isinstance(r["repeat"], int) or r["repeat"] < 1:
            raise Refused("run %s repeat must be a positive int" % r["run_id"])
        if not str(r["model"]).strip():
            raise Refused("run %s has an empty model; write UNKNOWN(reason)" % r["run_id"])
    return runs


# ----------------------------------------------------------------- parsing

_FIELD = re.compile(r"^\s*(restatement|terms_used|terms_added|status)\s*:\s*(.*)$", re.I)


def _split_terms(s):
    s = s.strip()
    if not s or s.lower() in ("none", "-", "--", "[]", "n/a"):
        return []
    return [t.strip().strip("[]'\"").lower() for t in re.split(r"[,;]", s) if t.strip().strip("[]'\"")]


def parse_response(text):
    fields, notes, extra = {}, [], 0
    for ln in text.splitlines():
        if not ln.strip():
            continue
        m = _FIELD.match(ln)
        if m:
            fields[m.group(1).lower()] = m.group(2).strip()
        else:
            extra += 1
    if extra:
        notes.append("%d line(s) outside the fields" % extra)
    missing = [k for k in ("restatement", "terms_used", "terms_added", "status") if k not in fields]
    if missing:
        notes.append("lacks %d of 4 fields" % len(missing))
    st = fields.get("status", "").strip().upper()
    status = st if st in STATUSES else ("MALFORMED" if "status" in fields else "MISSING")
    return {"restatement": fields.get("restatement", ""), "terms_used": _split_terms(fields.get("terms_used", "")),
            "terms_added": _split_terms(fields.get("terms_added", "")), "status": status,
            "malformed": status in ("MALFORMED", "MISSING") or "restatement" not in fields, "notes": notes}


def _tokens(s):
    return [t for t in re.findall(r"[a-z][a-z\-']*", s.lower())]


def leak(restatement, prims, terms_added):
    """Content words of the restatement outside the primitive list, the
    function-word set and the declared additions. Multi-word primitives
    contribute each of their words."""
    allowed = set()
    for p in prims["primitives"]:
        allowed.update(_tokens(p["term"]))
    for t in terms_added:
        allowed.update(_tokens(t))
    return sorted({t for t in _tokens(restatement) if t not in allowed and t not in FUNCTION_WORDS and len(t) > 1})


def undeclared_used(terms_used, prims, terms_added):
    prim = {p["term"].strip().lower() for p in prims["primitives"]}
    added = {t.lower() for t in terms_added}
    return sorted(t for t in terms_used if t not in prim and t not in added)


# ----------------------------------------------------------------- scoring

def reading(cls, status):
    """Section 5, per construction."""
    if status == "COMPOSES_WITH_ADDITION":
        return "ADDITION"
    if status == "FAILS":
        return {"TARGETED": "PROTECTION", "CONTROL": "NARROW", "AMBIENT": "AMBIENT_FAILS"}[cls]
    if status == "COMPOSES":
        return {"TARGETED": "HOLE", "CONTROL": "USABLE", "AMBIENT": "AMBIENT_COMPOSES"}[cls]
    return "MALFORMED"


def rates(rows):
    """Section 5 aggregates over (class, status) rows. A missing denominator
    is None, never 0. COMPOSES_WITH_ADDITION rows are counted apart."""
    def share(cls, st):
        den = [r for r in rows if r[0] == cls and r[1] in STATUSES]
        if not den:
            return None
        return sum(1 for r in den if r[1] == st) / len(den)
    def share_incl(cls):
        den = [r for r in rows if r[0] == cls and r[1] in STATUSES]
        if not den:
            return None
        return sum(1 for r in den if r[1] in ("COMPOSES", "COMPOSES_WITH_ADDITION")) / len(den)
    return {"hole_rate": share("TARGETED", "COMPOSES"),
            "narrowness": share("CONTROL", "FAILS"),
            "ambient_rate": share("AMBIENT", "COMPOSES"),
            "addition_rate": {c: share(c, "COMPOSES_WITH_ADDITION") for c in CLASSES},
            # the other reading of [CHOICE 2]: an addition counted as composing
            "hole_rate_incl_addition": share_incl("TARGETED"),
            "ambient_rate_incl_addition": share_incl("AMBIENT")}


def cite_missing(missing, prims):
    """A FAILS record may name the primitive it lacked (`missing_primitive`,
    comma-separated). Each citation lands on one of three cells: a term
    the ontology DECLARED absent (protection reporting its own boundary),
    a term that IS a primitive (the restater did not find it), or a term
    the ontology neither has nor declared absent (an UNDECLARED absence --
    the cut refused something it never said it would)."""
    prim = {e["term"].strip().lower() for e in prims["primitives"]}
    absent = {a["term"].strip().lower() for a in prims["absent_by_design"]}
    out = []
    for t in _split_terms(missing or ""):
        out.append({"term": t, "cell": "declared_absent" if t in absent else ("primitive" if t in prim else "undeclared")})
    return out


def load_aliases(odir, prims):
    """Optional aliases.json beside primitives.json ([CHOICE 6]). Returns
    None when the file is absent (the reimport check is then NOT_DECLARED,
    which is not the same as no hits). Refuses an alias file that names an
    absent term the ontology did not declare, an alias that is itself a
    primitive or an absent term, or an alias with no stated basis."""
    path = os.path.join(odir, "aliases.json")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        a = json.load(fh)
    if "aliases" not in a or not isinstance(a["aliases"], dict):
        raise Refused("aliases.json needs an `aliases` object")
    decl = a.get("_declaration") or {}
    for k in ("declared_by", "written_after"):
        if not decl.get(k):
            raise Refused("aliases.json _declaration needs %s" % k)
    prim = {e["term"].strip().lower() for e in prims["primitives"]}
    absent = {x["term"].strip().lower() for x in prims["absent_by_design"]}
    table = {}
    for term, entries in a["aliases"].items():
        t = term.strip().lower()
        if t not in absent:
            raise Refused("aliases.json names %r, not an absent_by_design term" % term)
        table[t] = {}
        for e in entries:
            if not isinstance(e, dict) or not e.get("term") or not e.get("basis"):
                raise Refused("alias entry under %r needs term and basis: %r" % (term, e))
            al = e["term"].strip().lower()
            if al in prim:
                raise Refused("alias %r under %r is a primitive" % (al, term))
            if al in absent:
                raise Refused("alias %r under %r is itself an absent term" % (al, term))
            table[t][al] = e["basis"]
    scope = {}
    for e in a.get("scope_required", []):
        if not isinstance(e, dict) or not e.get("term") or not e.get("requires") or not e.get("basis"):
            raise Refused("scope_required entry needs term, requires (non-empty) and basis: %r" % e)
        t = e["term"].strip().lower()
        if t in prim or t in absent:
            raise Refused("scope_required term %r is a primitive or an absent term" % t)
        if any(t in als for als in table.values()):
            raise Refused("scope_required term %r is also listed as an alias; one state per term" % t)
        ic = e.get("import_class")
        if ic not in IMPORT_CLASSES:
            raise Refused("scope_required term %r needs import_class in %s, got %r" % (t, sorted(IMPORT_CLASSES), ic))
        req = [str(x) for x in e["requires"]]
        if ic == "morality" and "graded_by" not in req:
            raise Refused("scope_required term %r is import_class morality and does not require graded_by; "
                          "that is the scope class under another label" % t)
        scope[t] = {"requires": req, "basis": e["basis"], "import_class": ic}
    return {"declared_by": decl["declared_by"], "written_after": decl["written_after"],
            "blind_for": decl.get("blind_for"), "table": table, "scope": scope, "path": path}


IMPORT_CLASSES = ("scope", "morality")


def scope_undeclared(terms_added, aliases, declared=None):
    """An added term on the scope_required list carries no value until the
    fields it requires are declared. `declared` is the record's own scope
    declaration (a dict of field -> value) when the run form carries one;
    a coded sheet carries none, so every hit is SCOPE_UNDECLARED with the
    missing fields named. None when no table is declared."""
    if aliases is None:
        return None
    out = []
    for t in terms_added:
        if t in aliases.get("scope", {}):
            req = aliases["scope"][t]["requires"]
            missing = [f for f in req if not (declared or {}).get(f)]
            out.append({"added": t, "requires": req, "missing": missing,
                        "state": "SCOPE_UNDECLARED" if missing else "SCOPE_DECLARED",
                        "import_class": aliases["scope"][t]["import_class"],
                        "basis": aliases["scope"][t]["basis"]})
    return out


def reimports(terms_added, aliases):
    """terms_added screened against the declared alias table. None when no
    table is declared (NOT_DECLARED), else the list of hits."""
    if aliases is None:
        return None
    hits = []
    for t in terms_added:
        for absent, als in aliases["table"].items():
            if t in als:
                hits.append({"added": t, "absent": absent, "basis": als[t]})
    return hits


def absent_coverage(scored, prims):
    """Per absent_by_design term: was it EXERCISED by this run at all --
    named in a construction's `targets`, cited by a FAILS record's
    missing_primitive, or reached by a declared alias in terms_added --
    or UNEXERCISED. hole_rate is silent about an unexercised term: no
    construction put it under load. share_exercised is None when the
    ontology declares no absent term."""
    rows = {}
    for x in prims["absent_by_design"]:
        rows[x["term"].strip().lower()] = {"targeted_by": [], "cited_by": [], "reimported_via": []}
    for s in scored:
        if s.get("malformed"):
            continue
        for t in (s.get("targets") or []):
            t = t.strip().lower()
            if t in rows and s["construction_id"] not in rows[t]["targeted_by"]:
                rows[t]["targeted_by"].append(s["construction_id"])
        for m in s.get("cited_missing") or []:
            if m["cell"] == "declared_absent" and s["run_id"] not in rows[m["term"]]["cited_by"]:
                rows[m["term"]]["cited_by"].append(s["run_id"])
        for h in (s.get("reimports") or []):
            rows[h["absent"]]["reimported_via"].append("%s:%s" % (s["construction_id"], h["added"]))
    for t, r in rows.items():
        r["state"] = "EXERCISED" if (r["targeted_by"] or r["cited_by"] or r["reimported_via"]) else "UNEXERCISED"
    n = len(rows)
    ex = sum(1 for r in rows.values() if r["state"] == "EXERCISED")
    return {"rows": rows, "n_absent": n, "exercised": ex,
            "unexercised": sorted(t for t, r in rows.items() if r["state"] == "UNEXERCISED"),
            "share_exercised": (ex / n) if n else None}


def score_runs(runs, cons, prims, fixture=False, form="raw", aliases=None):
    """fixture=True says the construction set was admitted without the
    hand_built gate, for exercising the scorer; the render banners it.
    form is 'raw' or 'coded' (see the module docstring)."""
    validate_runs(runs, cons)
    by_id = {c["id"]: c for c in cons}
    prim_terms = {e["term"].strip().lower() for e in prims["primitives"]}
    scored = []
    for r in runs:
        c = by_id[r["construction_id"]]
        if r.get("coded"):
            cd = r["coded"]
            st = str(cd["status"]).strip().upper()
            p = {"restatement": None, "terms_used": [t.strip().lower() for t in cd["terms_used"]],
                 "terms_added": [t.strip().lower() for t in cd["terms_added"]],
                 "status": st if st in STATUSES else "MALFORMED", "malformed": st not in STATUSES, "notes": []}
            lk = None  # no restatement to read
            extra = {"cited_missing": cite_missing(cd["missing_primitive"], prims), "note": cd["note"],
                     "class_agrees": (cd["class"] == c["class"]) if cd["class"] is not None else None,
                     "terms_used_in_primitives": all(t in prim_terms for t in p["terms_used"])}
        else:
            p = parse_response(r["raw_response"])
            lk = leak(p["restatement"], prims, p["terms_added"]) if not p["malformed"] else []
            extra = {"cited_missing": [], "note": None, "class_agrees": None,
                     "terms_used_in_primitives": all(t in prim_terms for t in p["terms_used"])}
        s = dict(p)
        s.update({"run_id": r["run_id"], "construction_id": c["id"], "class": c["class"], "model": r["model"],
                  "family": r["family"], "repeat": r["repeat"], "ontology": r["ontology"],
                  "constructed": r["constructed"], "reading": reading(c["class"], p["status"]),
                  "leak": lk, "undeclared_used": undeclared_used(p["terms_used"], prims, p["terms_added"]),
                  "status_contradicted": (p["status"] == "COMPOSES" and bool(lk)) if lk is not None else None,
                  "targets": c.get("targets"),
                  "reimports": reimports(p["terms_added"], aliases) if not p["malformed"] else None,
                  "scope": scope_undeclared(p["terms_added"], aliases, r.get("declared_scope")) if not p["malformed"] else None})
        s.update(extra)
        scored.append(s)
    ok = [s for s in scored if not s["malformed"]]
    agg = rates([(s["class"], s["status"]) for s in ok])
    smuggle = sorted({t for s in ok for t in s["terms_added"]})
    leaks = sorted({t for s in ok for t in (s["leak"] or [])})
    leak_evaluable = [s for s in ok if s["leak"] is not None]
    cited = [(s, m) for s in ok for m in s["cited_missing"]]
    missing_summary = {
        "citations": len(cited),
        "declared_absent": sum(1 for _, m in cited if m["cell"] == "declared_absent"),
        "primitive": sorted({m["term"] for _, m in cited if m["cell"] == "primitive"}),
        "undeclared": sorted({m["term"] for _, m in cited if m["cell"] == "undeclared"}),
        "targeted_fails_citing_declared_absence": sum(
            1 for s in ok if s["class"] == "TARGETED" and s["status"] == "FAILS"
            and any(m["cell"] == "declared_absent" for m in s["cited_missing"])),
        "targeted_fails": sum(1 for s in ok if s["class"] == "TARGETED" and s["status"] == "FAILS"),
    }
    cov = absent_coverage(scored, prims)
    rhits = [(s, h) for s in ok for h in (s["reimports"] or [])]
    reimport_summary = {
        "declared": aliases is not None,
        "declared_by": aliases["declared_by"] if aliases else None,
        "written_after": aliases["written_after"] if aliases else None,
        "n_aliases": sum(len(v) for v in aliases["table"].values()) if aliases else 0,
        "records_with_hit": len({s["run_id"] for s, _ in rhits}),
        "hits": [{"construction_id": s["construction_id"], "added": h["added"], "absent": h["absent"], "basis": h["basis"]}
                 for s, h in rhits],
        "added_terms_unmatched": sorted({t for s in ok for t in s["terms_added"]
                                         if aliases and not any(t == h["added"] for h in s["reimports"])
                                         and not any(t == h["added"] for h in s["scope"])}),
        "scope_hits": [{"construction_id": s["construction_id"], "added": h["added"], "state": h["state"],
                        "import_class": h["import_class"], "missing": h["missing"], "basis": h["basis"]}
                       for s in ok for h in (s["scope"] or [])],
        "scope_terms_unhit": sorted(t for t in aliases["scope"]
                                    if not any(t == h["added"] for s in ok for h in (s["scope"] or []))) if aliases else [],
    }
    return {"scored": scored, "aggregates": agg, "smuggle_set": smuggle, "leak_set": leaks,
            "absent_coverage": cov, "reimport_summary": reimport_summary,
            "n_runs": len(runs), "n_malformed": len(scored) - len(ok), "form": form,
            "n_leak_evaluable": len(leak_evaluable),
            "n_status_contradicted": sum(1 for s in leak_evaluable if s["status_contradicted"]),
            "missing_summary": missing_summary,
            "binding": {"terms_used_in_primitives": sum(1 for s in ok if s["terms_used_in_primitives"]),
                        "class_agrees": sum(1 for s in ok if s["class_agrees"]),
                        "class_recorded": sum(1 for s in ok if s["class_agrees"] is not None), "scored": len(ok)},
            "nulls": nulls(ok, agg, smuggle), "claims": claims(ok, agg, smuggle, prims, cons),
            "family_disagreement": family_disagreement(ok),
            "constructed_share": (sum(1 for r in runs if r["constructed"]) / len(runs)) if runs else None,
            "set": set_report(cons), "primitives": primitives_report(prims), "fixture": fixture}


def nulls(ok, agg, smuggle):
    out = {}
    if not ok:
        return {k: {"verdict": "NOT_EVALUABLE", "why": "no scored run"} for k in ("N1", "N2", "N3", "N4", "N5")}
    out["N1"] = {"fires": all(s["status"] != "FAILS" for s in ok),
                 "note": "everything composes; the cut has no protective structure. Do not adjust the primitive list."}
    out["N2"] = {"fires": all(s["status"] == "FAILS" for s in ok),
                 "note": "nothing composes, controls included; narrow rather than protective."}
    groups = {}
    for s in ok:
        groups.setdefault((s["construction_id"], s["model"]), []).append(s["status"])
    full = {k: v for k, v in groups.items() if len(v) >= REPEATS}
    if not full:
        out["N3"] = {"verdict": "NOT_EVALUABLE", "why": "no (construction, model) group carries %d repeats" % REPEATS,
                     "groups": len(groups)}
    else:
        unstable = sorted("%s|%s" % k for k, v in full.items() if len(set(v)) > 1)
        out["N3"] = {"groups_with_repeats": len(full), "unstable": len(unstable),
                     "instability": len(unstable) / len(full), "fires": bool(unstable), "which": unstable}
    if smuggle:
        fw = [t for t in smuggle if all(w in FUNCTION_WORDS for w in _tokens(t))]
        share = len(fw) / len(smuggle)
        out["N4"] = {"function_word_share": share, "fires": share > N4_THRESHOLD, "function_words": fw,
                     "threshold": N4_THRESHOLD}
    else:
        out["N4"] = {"verdict": "NOT_EVALUABLE", "why": "smuggle_set is empty"}
    h, a = agg["hole_rate"], agg["ambient_rate"]
    if h is None or a is None:
        out["N5"] = {"verdict": "NOT_EVALUABLE", "why": "one of hole_rate / ambient_rate has no denominator"}
    else:
        out["N5"] = {"fires": h == a, "hole_rate": h, "ambient_rate": a}
    return out


def claims(ok, agg, smuggle, prims, cons):
    out = {}
    h, a = agg["hole_rate"], agg["ambient_rate"]
    if h is None:
        out["OP-1"] = {"verdict": "undetermined", "why": "no scored TARGETED run"}
    else:
        out["OP-1"] = {"verdict": "REFUTED" if h == 1.0 else "not refuted", "hole_rate": h}
    n4 = None
    if smuggle:
        fw = [t for t in smuggle if all(w in FUNCTION_WORDS for w in _tokens(t))]
        n4 = len(fw) / len(smuggle) > N4_THRESHOLD
    if n4 is None:
        out["OP-2"] = {"verdict": "undetermined", "why": "no terms_added logged; the column is empty"}
    else:
        out["OP-2"] = {"verdict": "REFUTED" if n4 else "not refuted", "smuggle_set": smuggle}
    if h is None or a is None:
        out["OP-3"] = {"verdict": "undetermined", "why": "scored TARGETED and AMBIENT runs both required"}
    else:
        out["OP-3"] = {"verdict": "REFUTED" if a <= h else "not refuted", "ambient_rate": a, "hole_rate": h}
    onts = {}
    for s in ok:
        onts.setdefault(s["ontology"], set())
        if s["reading"] == "HOLE":
            onts[s["ontology"]].add(s["construction_id"])
    if len(onts) < 2:
        out["OP-4"] = {"verdict": "undetermined", "why": "runs on at least two ontologies required; have %d" % len(onts)}
    else:
        sets = list(onts.values())
        overlap = set.intersection(*sets) if all(sets) else set()
        out["OP-4"] = {"verdict": "REFUTED" if not overlap else "not refuted",
                       "holes_by_ontology": {k: sorted(v) for k, v in onts.items()}, "overlap": sorted(overlap)}
    # OP-5 needs two primitive sets of different grounding class; one is loaded here
    out["OP-5"] = {"verdict": "undetermined",
                   "why": "a physics-grounded and a declared-only primitive set scored on one construction set are both required; "
                          "this set is %s (physics share %.2f)" % (primitives_report(prims)["grounding_class"],
                                                                    primitives_report(prims)["physics_share"])}
    return out


def op5(rate_physics, rate_declared):
    """OP-5 on two hole rates. Parity refutes; physics above declared refutes too."""
    if rate_physics is None or rate_declared is None:
        return "undetermined"
    return "not refuted" if rate_physics < rate_declared else "REFUTED"


def family_disagreement(ok):
    """Section 7 RESTATER: per construction, do families return different statuses?"""
    by = {}
    for s in ok:
        by.setdefault(s["construction_id"], {}).setdefault(s["family"], set()).add(s["status"])
    rows = []
    for cid, fams in sorted(by.items()):
        if len(fams) < 2:
            continue
        stat = {f: sorted(v) for f, v in fams.items()}
        disagree = len({tuple(v) for v in stat.values()}) > 1
        rows.append({"construction_id": cid, "families": stat, "disagree": disagree})
    return {"constructions_with_two_families": len(rows), "disagreements": sum(1 for r in rows if r["disagree"]),
            "rows": rows}


# ----------------------------------------------------------------- render

def render(res):
    L = ["ontology-probe -- score report"]
    pr = res["primitives"]
    L.append("ontology: %s %s  primitives %d (sha %s)  absent_by_design %d  grounding %s (physics share %.2f)" % (
        pr["name"], pr["version"], pr["n_primitives"], pr["sha"], pr["n_absent_by_design"],
        pr["grounding_class"], pr["physics_share"]))
    if pr["claims_no_protection"]:
        L.append("absent_by_design is EMPTY: the ontology claims no protective structure (section 2)")
    if pr["undefined_candidate_holes"]:
        L.append("grounds_to undefined (candidate holes before any construction): %s" % pr["undefined_candidate_holes"])
    st = res["set"]
    if res.get("fixture"):
        L.append("construction set is a FIXTURE admitted past the hand_built gate; it is not the folder's set")
    L.append("construction set: n %d, by class %s, control share %s%s" % (
        st["n"], st["by_class"], "--" if st["control_share"] is None else "%.2f" % st["control_share"],
        ("  FLAGS: " + "; ".join(st["flags"])) if st["flags"] else ""))
    for k in sorted(CHOICES):
        L.append("[CHOICE %d] %s" % (k, CHOICES[k]))
    cs = res["constructed_share"]
    if cs is None:
        L.append("runs: none. No model has been run against this instrument here.")
    else:
        L.append("runs: %d, malformed %d, constructed share %.2f%s" % (
            res["n_runs"], res["n_malformed"], cs,
            "  -- EVERY RECORD IS CONSTRUCTED; nothing below is about any model" if cs == 1.0 else ""))
        L.append("input form: %s%s" % (res.get("form", "raw"),
                 " (statuses coded by the operator; no restatement logged, so the leak check is NOT_EVALUABLE)"
                 if res.get("form") == "coded" else " (restatements parsed here)"))
        b = res["binding"]
        L.append("ontology binding: terms_used inside the primitive list on %d of %d scored; class field agrees on %d of %d recorded" % (
            b["terms_used_in_primitives"], b["scored"], b["class_agrees"], b["class_recorded"]))
    L.append("")
    L.append("per run (section 5)")
    L.append("%-8s %-9s %-14s %-3s %-24s %-16s %-6s %s" % ("constr", "class", "family", "rep", "status", "reading", "leak", "terms_added | cited missing"))
    for s in res["scored"]:
        cited = ",".join("%s(%s)" % (m["term"], m["cell"][:4]) for m in s["cited_missing"])
        L.append("%-8s %-9s %-14s %-3d %-24s %-16s %-6s %s%s%s" % (
            s["construction_id"], s["class"], s["family"][:14], s["repeat"], s["status"], s["reading"],
            "n/a" if s["leak"] is None else str(len(s["leak"])), ",".join(s["terms_added"]) or "-",
            (" | " + cited) if cited else "",
            "  CONTRADICTED(leak %s)" % ",".join(s["leak"]) if s["status_contradicted"] else ""))
    L.append("")
    a = res["aggregates"]
    fmt = lambda v: "--" if v is None else "%.3f" % v  # noqa: E731
    L.append("aggregates: hole_rate %s  narrowness %s  ambient_rate %s  addition_rate %s" % (
        fmt(a["hole_rate"]), fmt(a["narrowness"]), fmt(a["ambient_rate"]),
        {k: fmt(v) for k, v in a["addition_rate"].items()}))
    L.append("  other reading of [CHOICE 2], an addition counted as composing: hole_rate %s  ambient_rate %s" % (
        fmt(a["hole_rate_incl_addition"]), fmt(a["ambient_rate_incl_addition"])))
    L.append("smuggle_set (%d): %s" % (len(res["smuggle_set"]), ", ".join(res["smuggle_set"]) or "-"))
    if res.get("n_leak_evaluable", 0):
        L.append("leak_set (%d, undeclared additions read from restatements): %s" % (
            len(res["leak_set"]), ", ".join(res["leak_set"]) or "-"))
        L.append("status contradicted by leak: %d of %d leak-evaluable" % (res["n_status_contradicted"], res["n_leak_evaluable"]))
    else:
        L.append("leak check: NOT_EVALUABLE on every record (no restatement logged)")
    ms = res["missing_summary"]
    if ms["citations"]:
        L.append("cited missing primitives (from FAILS records): %d citations; on the declared-absent list %d; "
                 "naming a primitive %s; UNDECLARED absences %s" % (
                     ms["citations"], ms["declared_absent"], ms["primitive"] or "-", ms["undeclared"] or "-"))
        L.append("  TARGETED FAILS citing a declared absence: %d of %d" % (
            ms["targeted_fails_citing_declared_absence"], ms["targeted_fails"]))
    cov = res["absent_coverage"]
    if cov["n_absent"]:
        L.append("absent-term coverage: EXERCISED %d of %d declared absences (targeted, cited by a FAILS, or reached by alias); "
                 "UNEXERCISED %s -- hole_rate is silent about an unexercised term" % (
                     cov["exercised"], cov["n_absent"], ", ".join(cov["unexercised"]) or "-"))
        for t, r in sorted(cov["rows"].items()):
            L.append("  %-22s %-11s targeted_by %s  cited_by %s  reimported_via %s" % (
                t, r["state"], ",".join(r["targeted_by"]) or "-", ",".join(r["cited_by"]) or "-",
                ",".join(r["reimported_via"]) or "-"))
    rs = res["reimport_summary"]
    if rs["declared"]:
        L.append("alias reimport ([CHOICE 6]; %d aliases declared by: %s; written after: %s): %d record(s) hit" % (
            rs["n_aliases"], rs["declared_by"], rs["written_after"], rs["records_with_hit"]))
        for h in rs["hits"]:
            L.append("  %-8s %s => %s   [%s]" % (h["construction_id"], h["added"], h["absent"], h["basis"]))
        for h in rs["scope_hits"]:
            L.append("  %-8s %s  %s (%s)  missing %s   [%s]" % (h["construction_id"], h["added"], h["state"],
                                                               h["import_class"], ",".join(h["missing"]) or "-", h["basis"]))
        L.append("  scope_required terms declared and not added by any record: %s" % (", ".join(rs["scope_terms_unhit"]) or "-"))
        L.append("  added terms matching no alias and no scope requirement: %s" % (", ".join(rs["added_terms_unmatched"]) or "-"))
    else:
        L.append("alias reimport ([CHOICE 6]): NOT_DECLARED (no aliases.json beside primitives.json); not a zero")
    notes = [s for s in res["scored"] if s.get("note")]
    if notes:
        L.append("restater notes carried (%d):" % len(notes))
        for s in notes:
            L.append("  %-8s %s" % (s["construction_id"], s["note"]))
    L.append("")
    L.append("nulls (section 6)")
    for k in ("N1", "N2", "N3", "N4", "N5"):
        L.append("  %s  %s" % (k, json.dumps(res["nulls"][k], sort_keys=True)))
    L.append("")
    L.append("claims (section 8)")
    for k in ("OP-1", "OP-2", "OP-3", "OP-4", "OP-5"):
        v = res["claims"][k]
        L.append("  %s  %s%s" % (k, v["verdict"], ("  -- " + v["why"]) if v.get("why") else ""))
    fd = res["family_disagreement"]
    L.append("")
    L.append("restater disagreement (section 7): %d of %d constructions seen by two families disagree" % (
        fd["disagreements"], fd["constructions_with_two_families"]))
    for r in fd["rows"]:
        if r["disagree"]:
            L.append("  " + json.dumps(r, sort_keys=True))
    L.append("")
    L.append("dual use (section 7): the smuggle_set names where premises enter; publishing lowers a search cost.")
    L.append("coverage (section 7): only constructions someone wrote enter the set; the rates are over that set.")
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------- cli

def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("probe.py refuses --selftest; the checks live in selftest_op.py\n")
        return 2
    if not argv:
        sys.stderr.write(__doc__)
        return 2
    cmd = argv[0]
    odir = HERE
    if "--ontology" in argv:
        i = argv.index("--ontology")
        if len(argv) < i + 2:
            sys.stderr.write("--ontology takes a directory\n")
            return 2
        odir = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    prim_path = os.path.join(odir, "primitives.json")
    cons_path = os.path.join(odir, "constructions.jsonl")
    prims = load_primitives(prim_path)
    if cmd == "declare":
        print(json.dumps(primitives_report(prims), indent=1, sort_keys=True))
        cons = load_constructions(cons_path, prims)
        print("admitted constructions: %s" % json.dumps(set_report(cons), sort_keys=True))
        for c in candidates(cons_path):
            print("CANDIDATE %-9s %-9s hand_built=False  %s" % (c["id"], c["class"], c["text"][:60]))
        return 0
    if cmd == "prompt":
        if len(argv) < 2:
            sys.stderr.write("usage: probe.py prompt CONSTRUCTION_ID [--ontology DIR]\n")
            return 2
        cons = {c["id"]: c for c in load_constructions(cons_path, prims)}
        if argv[1] not in cons:
            sys.stderr.write("construction %r not admitted (candidates are listed by `declare`)\n" % argv[1])
            return 2
        sys.stdout.write(render_prompt(prims, cons[argv[1]]) + "\n")
        return 0
    if cmd == "score":
        if len(argv) < 2:
            sys.stderr.write("usage: probe.py score RUNS.jsonl [--ontology DIR] [--fixture CONSTRUCTIONS.jsonl]\n")
            return 2
        fixture = "--fixture" in argv
        if fixture:
            i = argv.index("--fixture")
            if len(argv) < i + 2:
                sys.stderr.write("--fixture takes a path\n")
                return 2
            cons = load_constructions(argv[i + 1], prims, admit_candidates=True)
        else:
            cons = load_constructions(cons_path, prims)
        runs, form = load_runs(argv[1], prims)
        aliases = load_aliases(odir, prims)
        sys.stdout.write(render(score_runs(runs, cons, prims, fixture=fixture, form=form, aliases=aliases)))
        return 0
    sys.stderr.write(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
