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
CHOICES = {
    1: "[PRIMITIVES] rendered one `term (type)` per line",
    2: "COMPOSES_WITH_ADDITION rows in every section 5 denominator, in no numerator; addition_rate printed per class",
    3: "restatement leak check added beside the self-reported status; FUNCTION_WORDS declared",
    4: "N4 threshold 0.5 function-word share; OP-5 physics-grounded = at least half of primitives ground to physics",
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
    if c["class"] == "TARGETED":
        if not c.get("targets"):
            raise Refused("TARGETED construction %s must name the absent_by_design term(s) it targets" % c["id"])
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


def load_runs(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                out.append(json.loads(ln))
    return out


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
    return {"hole_rate": share("TARGETED", "COMPOSES"),
            "narrowness": share("CONTROL", "FAILS"),
            "ambient_rate": share("AMBIENT", "COMPOSES"),
            "addition_rate": {c: share(c, "COMPOSES_WITH_ADDITION") for c in CLASSES}}


def score_runs(runs, cons, prims, fixture=False):
    """fixture=True says the construction set was admitted without the
    hand_built gate, for exercising the scorer; the render banners it."""
    validate_runs(runs, cons)
    by_id = {c["id"]: c for c in cons}
    scored = []
    for r in runs:
        p = parse_response(r["raw_response"])
        c = by_id[r["construction_id"]]
        lk = leak(p["restatement"], prims, p["terms_added"]) if not p["malformed"] else []
        s = dict(p)
        s.update({"run_id": r["run_id"], "construction_id": c["id"], "class": c["class"], "model": r["model"],
                  "family": r["family"], "repeat": r["repeat"], "ontology": r["ontology"],
                  "constructed": r["constructed"], "reading": reading(c["class"], p["status"]),
                  "leak": lk, "undeclared_used": undeclared_used(p["terms_used"], prims, p["terms_added"]),
                  "status_contradicted": (p["status"] == "COMPOSES" and bool(lk))})
        scored.append(s)
    ok = [s for s in scored if not s["malformed"]]
    agg = rates([(s["class"], s["status"]) for s in ok])
    smuggle = sorted({t for s in ok for t in s["terms_added"]})
    leaks = sorted({t for s in ok for t in s["leak"]})
    return {"scored": scored, "aggregates": agg, "smuggle_set": smuggle, "leak_set": leaks,
            "n_runs": len(runs), "n_malformed": len(scored) - len(ok),
            "n_status_contradicted": sum(1 for s in ok if s["status_contradicted"]),
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
    L.append("")
    L.append("per run (section 5)")
    L.append("%-8s %-9s %-14s %-3s %-24s %-16s %-6s %s" % ("constr", "class", "model", "rep", "status", "reading", "leak", "terms_added"))
    for s in res["scored"]:
        L.append("%-8s %-9s %-14s %-3d %-24s %-16s %-6d %s%s" % (
            s["construction_id"], s["class"], s["model"][:14], s["repeat"], s["status"], s["reading"],
            len(s["leak"]), ",".join(s["terms_added"]) or "-",
            "  CONTRADICTED(leak %s)" % ",".join(s["leak"]) if s["status_contradicted"] else ""))
    L.append("")
    a = res["aggregates"]
    fmt = lambda v: "--" if v is None else "%.3f" % v  # noqa: E731
    L.append("aggregates: hole_rate %s  narrowness %s  ambient_rate %s  addition_rate %s" % (
        fmt(a["hole_rate"]), fmt(a["narrowness"]), fmt(a["ambient_rate"]),
        {k: fmt(v) for k, v in a["addition_rate"].items()}))
    L.append("smuggle_set (%d): %s" % (len(res["smuggle_set"]), ", ".join(res["smuggle_set"]) or "-"))
    L.append("leak_set (%d, undeclared additions read from restatements): %s" % (
        len(res["leak_set"]), ", ".join(res["leak_set"]) or "-"))
    L.append("status contradicted by leak: %d of %d scored" % (res["n_status_contradicted"], res["n_runs"] - res["n_malformed"]))
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
    prims = load_primitives()
    if cmd == "declare":
        print(json.dumps(primitives_report(prims), indent=1, sort_keys=True))
        cons = load_constructions(CONSTRUCTIONS, prims)
        print("admitted constructions: %s" % json.dumps(set_report(cons), sort_keys=True))
        for c in candidates():
            print("CANDIDATE %-9s %-9s hand_built=False  %s" % (c["id"], c["class"], c["text"][:60]))
        return 0
    if cmd == "prompt":
        if len(argv) < 2:
            sys.stderr.write("usage: probe.py prompt CONSTRUCTION_ID\n")
            return 2
        cons = {c["id"]: c for c in load_constructions(CONSTRUCTIONS, prims)}
        if argv[1] not in cons:
            sys.stderr.write("construction %r not admitted (candidates are listed by `declare`)\n" % argv[1])
            return 2
        sys.stdout.write(render_prompt(prims, cons[argv[1]]) + "\n")
        return 0
    if cmd == "score":
        if len(argv) < 2:
            sys.stderr.write("usage: probe.py score RUNS.jsonl [--fixture CONSTRUCTIONS.jsonl]\n")
            return 2
        fixture = "--fixture" in argv
        if fixture:
            i = argv.index("--fixture")
            if len(argv) < i + 2:
                sys.stderr.write("--fixture needs a path\n")
                return 2
            cons = load_constructions(argv[i + 1], prims, admit_candidates=True)
        else:
            cons = load_constructions(CONSTRUCTIONS, prims)
        sys.stdout.write(render(score_runs(load_runs(argv[1]), cons, prims, fixture=fixture)))
        return 0
    sys.stderr.write(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
