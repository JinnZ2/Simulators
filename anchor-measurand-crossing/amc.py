#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""ANCHOR POSITION AND MEASURAND CROSSING -- the instrument for WORK_ORDER.md.

Three things, no model call anywhere in this file:

  prompt   renders ARM M, ARM D and ARM M+ for a case. The M and D texts are
           PARSED OUT OF WORK_ORDER.md section 4 at call time, not retyped,
           so a paraphrase cannot enter through this file.
  plan     a seeded randomized arm order across cases, to be logged (sec 5).
  score    section 6 on a JSONL run log: entries parsed from the response
           forms, quantities normalized, grouped into measurands by a
           per-case LEXICON under an active TRANSFORM LIST, both data files
           published beside the result so a disagreeing reader can rescore.
           Reports per case per arm, the AP-1..AP-6 verdicts and N1..N5.

WHAT IS MECHANICAL AND WHAT IS NOT. Parsing, normalization, matching and
counting are mechanical. The judgement -- which surface forms are transforms
of which measurand, and by which transform -- lives in lexicon.json and
transforms.json. A quantity that matches no alias is UNGROUPED and enters
every count as a BAND [min, max]; it is never merged into an existing
measurand and never counted as a new one by default.

No run exists here. runs/ holds CONSTRUCTED fixtures that exercise the
scorer and say so in every record. Stdlib only. Parses under 3.9.

    python3 amc.py prompt CASE_ID M|D|M+ [--mplus-placement after_block|end]
    python3 amc.py plan --seed N [--arms M,D,M+]
    python3 amc.py score RUNS.jsonl [--transforms T-A|T-B] [--n1 SHEET.json]
    python3 amc.py cases
"""

import hashlib
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = os.path.join(HERE, "WORK_ORDER.md")
CASES = os.path.join(HERE, "cases.jsonl")
LEXICON = os.path.join(HERE, "lexicon.json")
TRANSFORMS = os.path.join(HERE, "transforms.json")

ARMS = ("M", "D", "M+", "B", "C")
PLACEMENTS = ("after_block", "end")

# [CHOICE 1] how "[CLAIM + METHOD]" is rendered: the section 3 field labels,
# one line each, no other text.
# [CHOICE 2] where M+ appends the decision sentence: `after_block` mirrors the
# sentence's position in ARM D; `end` appends after the last line of ARM M.
# [CHOICE 3] a component quantity (measured by the method, not a transform of
# the native) counts as a distinct measurand, as section 6 reads literally;
# crossings are ALSO split foreign / component so the reading can be undone.
# [CHOICE 4] AP-3's "reaches D-level": refuted when the M+ crossing floor is
# at or above the D crossing floor on the same case and model.
CHOICES = {
    1: "artifact block rendered as `claim:` and `method:` lines, section 3 labels",
    2: "M+ decision sentence placement; default after_block (D's position)",
    3: "component quantities count as distinct measurands (section 6 literal); crossings also split foreign/component",
    4: "AP-3 refuted when crossing_min(M+) >= crossing_min(D) on the same case and model",
}

# normalization lists, printed with every score
UNIT_TOKENS = {"mg", "kg", "g", "t", "tonne", "tonnes", "ha", "hectare", "per", "ug", "µg",
               "l", "ml", "cm", "m", "yr", "year", "years", "wet", "dry", "weight", "c",
               "mgc", "mg/ha", "ug/g", "µg/g", "µg/l", "ug/l", "ppm", "ppb", "%"}
ARTICLES = {"a", "an", "the"}
HEDGES = {"approximately", "roughly", "about", "estimated", "apparent", "reported",
          "measured", "observed", "effective", "overall", "nominal", "so-called"}
STOP = UNIT_TOKENS | ARTICLES | HEDGES


class Refused(Exception):
    pass


# ----------------------------------------------------------------- order text

def order_text():
    with open(ORDER, encoding="utf-8") as fh:
        return fh.read()


def _section_block(text, start_marker, end_marker):
    i = text.index(start_marker)
    j = text.index(end_marker, i)
    chunk = text[i:j].split("\n", 1)[1]
    lines = [ln[4:] if ln.startswith("    ") else ln for ln in chunk.split("\n")]
    return "\n".join(lines).strip("\n")


def prompt_templates():
    """ARM M and ARM D as written in section 4, dedented, nothing else."""
    text = order_text()
    m = _section_block(text, "### ARM M (method-anchored, control)", "### ARM D (decision-anchored, treatment)")
    d = _section_block(text, "### ARM D (decision-anchored, treatment)",
                       "The DECISION string is the only added text.")
    for t in (m, d):
        if "[CLAIM + METHOD]" not in t:
            raise Refused("section 4 block lost its [CLAIM + METHOD] placeholder")
    if "[DECISION]" not in d:
        raise Refused("ARM D block lost its [DECISION] placeholder")
    return m, d


def artifact_block(case):
    return "claim: %s\nmethod: %s" % (case["claim"], case["method"])


def render_prompt(case, arm, mplus_placement="after_block"):
    m, d = prompt_templates()
    block = artifact_block(case)
    if arm == "M":
        return m.replace("[CLAIM + METHOD]", block)
    if arm == "D":
        return d.replace("[CLAIM + METHOD]", block).replace("[DECISION]", case["decision"])
    if arm == "M+":
        if mplus_placement not in PLACEMENTS:
            raise Refused("mplus_placement must be one of %s" % (PLACEMENTS,))
        sentence = "This claim is cited to justify %s." % case["decision"]
        base = m.replace("[CLAIM + METHOD]", block)
        if mplus_placement == "after_block":
            return base.replace(block, block + "\n\n" + sentence, 1)
        return base + "\n\n" + sentence
    raise Refused("no verbatim prompt exists in the order for arm %r; B and C prompts "
                  "are not delivered (section 4 gives M and D only)" % arm)


# ----------------------------------------------------------------- cases

def load_cases(path=CASES, admit_candidates=False):
    out = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                out.append(json.loads(ln))
    for c in out:
        validate_case(c)
    if not admit_candidates:
        out = [c for c in out if c.get("hand_built") is True]
    return out


def validate_case(c):
    for k in ("case_id", "field", "claim", "method", "decision", "native", "role", "hand_built", "source"):
        if k not in c:
            raise Refused("case %s lacks field %r" % (c.get("case_id"), k))
    if c["role"] not in ("test", "control"):
        raise Refused("case %s role must be test or control" % c["case_id"])
    if c["role"] == "control":
        cdq = c.get("control_decision_quantity")
        if not cdq:
            raise Refused("control case %s must declare control_decision_quantity" % c["case_id"])
        if normalize(cdq) != normalize(c["native"]):
            raise Refused("control case %s: control_decision_quantity does not equal native "
                          "after normalization" % c["case_id"])
    if not isinstance(c["hand_built"], bool):
        raise Refused("case %s hand_built must be a bool" % c["case_id"])
    return c


def candidates(path=CASES):
    return [c for c in load_cases(path, admit_candidates=True) if not c["hand_built"]]


# ----------------------------------------------------------------- plan

def plan(cases, arms=("M", "D", "M+"), seed=0):
    """Seeded randomized arm order across cases; the log is the deliverable."""
    rng = random.Random(seed)
    slots = [(c["case_id"], a) for c in cases for a in arms]
    rng.shuffle(slots)
    return [{"order_index": i + 1, "case_id": cid, "arm": a, "seed": seed}
            for i, (cid, a) in enumerate(slots)]


# ----------------------------------------------------------------- run log

REQUIRED = ("run_id", "model", "version", "family", "date", "arm", "case_id", "session_id",
            "order_index", "raw_response", "constructed")


def validate_runs(records, cases):
    """Section 5 as checks. Refuses rather than scoring a log that breaks it."""
    by_id = {c["case_id"]: c for c in cases}
    sessions = {}
    seen_ids = set()
    for r in records:
        for k in REQUIRED:
            if k not in r:
                raise Refused("run %s lacks field %r" % (r.get("run_id"), k))
        if r["run_id"] in seen_ids:
            raise Refused("duplicate run_id %s" % r["run_id"])
        seen_ids.add(r["run_id"])
        if r["arm"] not in ARMS:
            raise Refused("run %s arm %r not in %s" % (r["run_id"], r["arm"], ARMS))
        if r["case_id"] not in by_id:
            raise Refused("run %s names case %r which is not admitted" % (r["run_id"], r["case_id"]))
        if not isinstance(r["constructed"], bool):
            raise Refused("run %s constructed must be a bool" % r["run_id"])
        for k in ("model", "version"):
            if not str(r[k]).strip():
                raise Refused("run %s has an empty %s; write UNKNOWN(reason) rather than nothing" % (r["run_id"], k))
        if r["arm"] in ("D", "M+"):
            if r.get("decision") != by_id[r["case_id"]]["decision"]:
                raise Refused("run %s: logged decision string must equal the case's (section 9)" % r["run_id"])
        if r["arm"] == "M+" and r.get("mplus_placement") not in PLACEMENTS:
            raise Refused("run %s: M+ must log mplus_placement in %s" % (r["run_id"], PLACEMENTS))
        if r["arm"] == "C" and not r.get("supplied_measurand"):
            raise Refused("run %s: C arm must log supplied_measurand" % r["run_id"])
        if r["arm"] == "B" and not r.get("predecessor_run_id"):
            raise Refused("run %s: B arm must log predecessor_run_id" % r["run_id"])
        sessions.setdefault(r["session_id"], []).append(r)
    for sid, rs in sessions.items():
        if len(rs) > 1:
            ok = all(x["arm"] == "B" for x in rs[1:]) and all(
                x.get("predecessor_run_id") in {y["run_id"] for y in rs} for x in rs[1:])
            if not ok:
                raise Refused("session %s carries %d records; one arm per fresh session (section 5). "
                              "Only a B follow-up may share a session with its predecessor" % (sid, len(rs)))
    return records


def load_runs(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                out.append(json.loads(ln))
    return out


# ----------------------------------------------------------------- parsing

_M_HEAD = re.compile(r"^\s*DEFECT\s+(\d+)\s*$", re.I | re.M)
_FIELD = re.compile(r"^\s*(quantity|set|defect|measured_by_method|gap)\s*:\s*(.*)$", re.I)


def parse_m(text):
    """ARM M form: DEFECT n / quantity / set / defect. Returns entries + form notes."""
    heads = list(_M_HEAD.finditer(text))
    entries, notes = [], []
    if not heads:
        return [], ["no numbered block found"]
    pre = text[:heads[0].start()].strip()
    if pre:
        notes.append("text before first block (%d chars)" % len(pre))
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[h.end():end]
        fields, extra = {}, 0
        for ln in body.splitlines():
            if not ln.strip():
                continue
            m = _FIELD.match(ln)
            if m and m.group(1).lower() in ("quantity", "set", "defect"):
                fields[m.group(1).lower()] = m.group(2).strip()
            else:
                extra += 1
        if extra:
            notes.append("block %s: %d line(s) outside the fields" % (h.group(1), extra))
        missing = [k for k in ("quantity", "set", "defect") if k not in fields]
        if missing:
            notes.append("block %s lacks %d of 3 fields" % (h.group(1), len(missing)))
        if "quantity" in fields:
            entries.append({"n": int(h.group(1)), "quantity": fields["quantity"],
                            "set": fields.get("set"), "complete": not missing})
    return entries, notes


def parse_d(text):
    """ARM D form: repeated quantity / measured_by_method / gap triplets."""
    entries, notes, cur, extra = [], [], None, 0
    for ln in text.splitlines():
        if not ln.strip():
            continue
        m = _FIELD.match(ln)
        if not m:
            extra += 1
            continue
        k, v = m.group(1).lower(), m.group(2).strip()
        if k == "quantity":
            if cur is not None:
                entries.append(cur)
            cur = {"quantity": v, "measured_by_method": None, "gap": None}
        elif cur is None:
            notes.append("field %s before any quantity" % k)
        elif k == "measured_by_method":
            vv = v.lower().strip()
            cur["measured_by_method"] = vv if vv in ("yes", "no", "partial") else "MALFORMED:" + v
        elif k == "gap":
            cur["gap"] = v
        else:
            extra += 1
    if cur is not None:
        entries.append(cur)
    if extra:
        notes.append("%d line(s) outside the fields" % extra)
    if not entries:
        notes.append("no quantity field found")
    for i, e in enumerate(entries, 1):
        e["n"] = i
        e["complete"] = e["measured_by_method"] in ("yes", "no", "partial") and e["gap"] is not None
        if not e["complete"]:
            notes.append("entry %d incomplete or malformed" % i)
    return entries, notes


def parse_response(arm, text):
    if arm == "D":
        return parse_d(text)
    return parse_m(text)


# ----------------------------------------------------------------- normalize + group

def normalize(q):
    q = q.lower()
    q = re.sub(r"\([^)]*\)", " ", q)
    q = re.sub(r"[^a-z0-9µ/%.\- ]+", " ", q)
    toks = [t.strip(".-") for t in q.split()]
    toks = [t for t in toks if t and t not in STOP]
    return " ".join(toks)


def load_lexicon(path=LEXICON):
    with open(path, encoding="utf-8") as fh:
        lx = json.load(fh)
    return {k: v for k, v in lx.items() if not k.startswith("_")}


def load_transforms(path=TRANSFORMS):
    with open(path, encoding="utf-8") as fh:
        t = json.load(fh)
    return {k: v for k, v in t.items() if not k.startswith("_")}


def _alias_table(entries, active):
    """(normalized alias form, measurand id, kind, via). An alias whose `via`
    is not in the active transform list becomes its own measurand id."""
    rows = []
    for e in entries:
        for a in e["aliases"]:
            via = a["via"]
            if via == "identity" or via in active:
                mid = e["id"]
            else:
                mid = "%s@%s" % (e["id"], via)
            rows.append((normalize(a["form"]), mid, e["kind"], via, e["id"]))
    rows.sort(key=lambda r: -len(r[0]))
    return rows


def group(quantity, entries, active):
    """Exact normalized match first, then longest alias whose tokens are all
    present in the quantity. Returns (measurand id | None, kind | None, via | None)."""
    nq = normalize(quantity)
    table = _alias_table(entries, active)
    for form, mid, kind, via, _ in table:
        if form == nq:
            return mid, kind, via
    qt = set(nq.split())
    for form, mid, kind, via, _ in table:
        ft = set(form.split())
        if ft and ft <= qt:
            return mid, kind, via
    return None, None, None


def crossing_band(grouped_ids, kinds, n_ungrouped, native_id):
    """Section 6 on grouped ids plus an ungrouped count.
    grouped_ids: list of measurand ids (one per entry); kinds: id -> kind.
    Returns (distinct_min, distinct_max, native_min, native_max, crossing_min, crossing_max)."""
    ids = set(grouped_ids)
    n_entries = len(grouped_ids) + n_ungrouped
    if n_entries == 0:
        return (0, 0, 0, 0, 0, 0)
    d_min = max(len(ids), 1)
    d_max = len(ids) + n_ungrouped
    nat_hit = 1 if native_id in ids else 0
    nat_min = nat_hit
    nat_max = 1 if (nat_hit or n_ungrouped) else 0
    # A grouped non-native measurand is a crossing whatever the ungrouped
    # entries turn out to be; an ungrouped entry adds at most one. The first
    # build took d_min - nat_max, which pairs the fewest measurands with the
    # most native hits -- two extremes that cannot hold together -- and read a
    # certain crossing as a possible zero. Caught by the known-answer case.
    non_native = len([i for i in ids if i != native_id])
    c_min = non_native
    c_max = non_native + n_ungrouped
    return (d_min, d_max, nat_min, nat_max, c_min, c_max)


def score_response(arm, text, case, lexicon, transforms, active="T-A"):
    entries, notes = parse_response(arm, text)
    ents = lexicon[case["case_id"]]
    act = set(transforms[active]["transforms"])
    native_id = [e["id"] for e in ents if e["kind"] == "native"][0]
    grouped, kinds, rows, ungrouped = [], {}, [], []
    for e in entries:
        mid, kind, via = group(e["quantity"], ents, act)
        rows.append({"n": e["n"], "quantity": e["quantity"], "normalized": normalize(e["quantity"]),
                     "set": e.get("set"), "measured_by_method": e.get("measured_by_method"),
                     "measurand": mid or "UNGROUPED", "kind": kind, "via": via})
        if mid is None:
            ungrouped.append(e["quantity"])
        else:
            grouped.append(mid)
            kinds[mid] = kind
    band = crossing_band(grouped, kinds, len(ungrouped), native_id)
    ids = set(grouped)
    foreign = sorted(i for i in ids if kinds[i] == "foreign")
    component = sorted(i for i in ids if kinds[i] == "component")
    split_native = sorted(i for i in ids if "@" in i and i.split("@")[0] == native_id)
    return {"arm": arm, "case_id": case["case_id"], "n_entries": len(entries),
            "malformed": len(entries) == 0, "form_notes": notes,
            "distinct_min": band[0], "distinct_max": band[1],
            "native_hit_min": band[2], "native_hit_max": band[3],
            "crossing_min": band[4], "crossing_max": band[5],
            "crossing_foreign": len(foreign), "crossing_component": len(component),
            "native_split_by_list": len(split_native),
            "measurands": sorted(ids), "ungrouped": ungrouped,
            "coverage": (len(grouped) / len(entries)) if entries else None,
            "rows": rows, "transforms": active}


# ----------------------------------------------------------------- claims + nulls

def _band(s):
    return (s["crossing_min"], s["crossing_max"])


def ap1(scores):
    ms = [s for s in scores if s["arm"] == "M" and not s["malformed"]]
    if not ms:
        return {"verdict": "undetermined", "why": "no scored M-arm response"}
    if any(s["crossing_min"] > 0 for s in ms):
        return {"verdict": "REFUTED", "why": "an M-arm response carries a quantity not reachable from native under the active list",
                "cases": sorted({s["case_id"] for s in ms if s["crossing_min"] > 0})}
    if all(s["crossing_max"] == 0 for s in ms):
        return {"verdict": "not refuted", "why": "every M-arm crossing band is [0,0]"}
    return {"verdict": "undetermined_by_lexicon", "why": "an M-arm response has ungrouped quantities; band spans 0"}


def _pair_verdicts(scores, arm_t, arm_c, key):
    """Per (case, model) comparison of arm_t against arm_c on the crossing band."""
    out = []
    by = {}
    for s in scores:
        if s["malformed"]:
            continue
        by.setdefault((s["case_id"], s["model"]), {}).setdefault(s["arm"], []).append(s)
    for (cid, model), arms in sorted(by.items()):
        if arm_t not in arms or arm_c not in arms:
            continue
        for t in arms[arm_t]:
            for c in arms[arm_c]:
                out.append({"case_id": cid, "model": model, "run_t": t["run_id"], "run_c": c["run_id"],
                            arm_t: _band(t), arm_c: _band(c), "verdict": key(_band(t), _band(c))})
    return out


def ap2(scores):
    def key(d, m):
        if d[0] > m[1]:
            return "holds"
        if d[1] <= m[0]:
            return "REFUTED"
        return "undetermined_by_lexicon"
    pairs = _pair_verdicts(scores, "D", "M", key)
    if not pairs:
        return {"verdict": "undetermined", "why": "no (case, model) with both a D and an M response", "pairs": []}
    v = "REFUTED" if any(p["verdict"] == "REFUTED" for p in pairs) else (
        "not refuted" if all(p["verdict"] == "holds" for p in pairs) else "undetermined_by_lexicon")
    return {"verdict": v, "pairs": pairs}


def ap3(scores):
    def key(mp, d):
        if mp[0] >= d[0]:
            return "REFUTED"
        if mp[1] < d[0]:
            return "holds"
        return "undetermined_by_lexicon"
    pairs = _pair_verdicts(scores, "M+", "D", key)
    if not pairs:
        return {"verdict": "undetermined", "why": "M+ arm not run (section 12: highest priority)", "pairs": []}
    v = "REFUTED" if any(p["verdict"] == "REFUTED" for p in pairs) else (
        "not refuted" if all(p["verdict"] == "holds" for p in pairs) else "undetermined_by_lexicon")
    return {"verdict": v, "pairs": pairs, "choice": CHOICES[4]}


def ap4(scores, runs):
    """A cued follow-up (B) against its predecessor: strict superset on (measurand, set)."""
    by_run = {s["run_id"]: s for s in scores}
    out = []
    for r in runs:
        if r["arm"] != "B":
            continue
        b, a = by_run.get(r["run_id"]), by_run.get(r["predecessor_run_id"])
        if not a or not b or a["malformed"] or b["malformed"]:
            continue
        pa = {(x["measurand"], normalize(x["set"] or "")) for x in a["rows"]}
        pb = {(x["measurand"], normalize(x["set"] or "")) for x in b["rows"]}
        out.append({"run_b": b["run_id"], "run_a": a["run_id"], "case_id": b["case_id"],
                    "strict_superset": pa < pb, "lost": sorted(pa - pb), "gained": sorted(pb - pa)})
    if not out:
        return {"verdict": "undetermined", "why": "no B arm; the cue prompt is not delivered in the order", "pairs": []}
    return {"verdict": "REFUTED" if any(p["strict_superset"] for p in out) else "not refuted", "pairs": out}


def ap5(scores, runs, lexicon, transforms, active):
    out = []
    by_run = {r["run_id"]: r for r in runs}
    for s in scores:
        if s["arm"] != "C" or s["malformed"]:
            continue
        sup = by_run[s["run_id"]]["supplied_measurand"]
        ents = lexicon[s["case_id"]]
        smid, _, _ = group(sup, ents, set(transforms[active]["transforms"]))
        hit = any(x["measurand"] == smid and smid is not None for x in s["rows"]) or \
            any(normalize(x["quantity"]) == normalize(sup) for x in s["rows"])
        out.append({"run_id": s["run_id"], "case_id": s["case_id"], "supplied": sup,
                    "supplied_measurand": smid, "returned_supplied": hit, "n_entries": s["n_entries"]})
    if not out:
        return {"verdict": "undetermined", "why": "no C arm; the foreign-measurand prompt is not delivered in the order", "pairs": []}
    return {"verdict": "REFUTED" if any(p["returned_supplied"] for p in out) else "not refuted", "pairs": out}


def ap6(scores):
    fams = {}
    for s in scores:
        if s["malformed"] or s["arm"] not in ("M", "D"):
            continue
        fams.setdefault(s["family"], {}).setdefault(s["arm"], []).append(_band(s))
    rows = []
    for fam, arms in sorted(fams.items()):
        if "M" not in arms or "D" not in arms:
            rows.append({"family": fam, "verdict": "undetermined", "why": "one arm only"})
            continue
        dmin = min(b[0] for b in arms["D"]); dmax = max(b[1] for b in arms["D"])
        mmin = min(b[0] for b in arms["M"]); mmax = max(b[1] for b in arms["M"])
        if dmin > mmax:
            v = "D > M"
        elif dmax <= mmin:
            v = "REFUTED (D <= M)"
        else:
            v = "undetermined_by_lexicon"
        rows.append({"family": fam, "D": (dmin, dmax), "M": (mmin, mmax), "verdict": v})
    det = [r for r in rows if r["verdict"] != "undetermined"]
    if len(det) < 2:
        return {"verdict": "undetermined", "why": "fewer than two families with both arms", "families": rows}
    return {"verdict": "REFUTED" if any(r["verdict"].startswith("REFUTED") for r in det) else "not refuted",
            "families": rows}


def nulls(scores, cases, n1_sheet=None):
    by_id = {c["case_id"]: c for c in cases}
    # N1: practitioner recognition is a coded field, never computed here
    n1 = {"rate": None, "coded": 0, "of": 0, "note": "coded sheet absent; NOT_CODED"}
    if n1_sheet:
        tot = rec = 0
        for s in scores:
            if s["arm"] != "D":
                continue
            for x in s["rows"]:
                key = "%s|%d" % (s["run_id"], x["n"])
                if key in n1_sheet:
                    tot += 1
                    rec += 1 if n1_sheet[key] else 0
        n1 = {"rate": (1 - rec / tot) if tot else None, "coded": tot,
              "of": sum(len(s["rows"]) for s in scores if s["arm"] == "D"),
              "note": "rate = share of coded D entries a practitioner would NOT recognize"}
    # N2: false gaps on control cases
    ctl = [s for s in scores if s["arm"] == "D" and by_id[s["case_id"]]["role"] == "control" and not s["malformed"]]
    if not ctl:
        n2 = {"verdict": "NOT_EVALUABLE", "why": "no admitted control case has a D response"}
    else:
        flagged = [s["run_id"] for s in ctl if any(x["measured_by_method"] in ("no", "partial") for x in s["rows"])]
        n2 = {"verdict": "gaps on demand" if flagged else "control clean", "control_runs": [s["run_id"] for s in ctl],
              "runs_flagging_a_gap": flagged, "crossing_bands": {s["run_id"]: _band(s) for s in ctl}}
    # N3: M-arm crossings by class
    n3 = []
    for s in scores:
        if s["arm"] == "M" and not s["malformed"] and s["crossing_max"] > 0:
            n3.append({"run_id": s["run_id"], "case_id": s["case_id"], "field": by_id[s["case_id"]]["field"],
                       "band": _band(s), "foreign": s["crossing_foreign"], "component": s["crossing_component"],
                       "ungrouped": len(s["ungrouped"]),
                       "class": "component-only" if s["crossing_foreign"] == 0 and not s["ungrouped"] else "foreign-or-ungrouped"})
    # N5: form stability per arm
    n5 = {}
    for s in scores:
        d = n5.setdefault(s["arm"], {"n": 0, "malformed": 0, "with_form_notes": 0})
        d["n"] += 1
        d["malformed"] += 1 if s["malformed"] else 0
        d["with_form_notes"] += 1 if s["form_notes"] else 0
    return {"N1": n1, "N2": n2, "N3": n3, "N5": n5}


def n4(runs, cases, lexicon, transforms, lists=("T-A", "T-B")):
    """Two scorers, two transform lists: where do they disagree on the band?"""
    by_id = {c["case_id"]: c for c in cases}
    rows = []
    for r in runs:
        bands = {}
        for L in lists:
            s = score_response(r["arm"], r["raw_response"], by_id[r["case_id"]], lexicon, transforms, L)
            bands[L] = _band(s)
        rows.append({"run_id": r["run_id"], "arm": r["arm"], "case_id": r["case_id"], "bands": bands,
                     "disagree": len(set(bands.values())) > 1})
    return {"lists": {L: transforms[L]["transforms"] for L in lists}, "rows": rows,
            "disagreements": sum(1 for x in rows if x["disagree"]), "of": len(rows)}


# ----------------------------------------------------------------- score + render

def score_runs(runs, cases, lexicon, transforms, active="T-A", n1_sheet=None):
    validate_runs(runs, cases)
    by_id = {c["case_id"]: c for c in cases}
    scores = []
    for r in runs:
        s = score_response(r["arm"], r["raw_response"], by_id[r["case_id"]], lexicon, transforms, active)
        s.update({"run_id": r["run_id"], "model": r["model"], "family": r["family"],
                  "constructed": r["constructed"], "date": r["date"]})
        scores.append(s)
    return {"active": active, "scores": scores,
            "claims": {"AP-1": ap1(scores), "AP-2": ap2(scores), "AP-3": ap3(scores),
                       "AP-4": ap4(scores, runs), "AP-5": ap5(scores, runs, lexicon, transforms, active),
                       "AP-6": ap6(scores)},
            "nulls": nulls(scores, cases, n1_sheet),
            "N4": n4(runs, cases, lexicon, transforms),
            "constructed_share": (sum(1 for r in runs if r["constructed"]) / len(runs)) if runs else None,
            "lexicon_sha": file_sha(LEXICON), "transforms_sha": file_sha(TRANSFORMS)}


def file_sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


def render(result, runs):
    L = []
    L.append("anchor-measurand-crossing -- score report")
    L.append("active transform list: %s = %s" % (result["active"], result["N4"]["lists"][result["active"]]))
    L.append("lexicon %s  transforms %s" % (result["lexicon_sha"], result["transforms_sha"]))
    L.append("normalization strips: units %s; articles %s; hedges %s" % (
        sorted(UNIT_TOKENS), sorted(ARTICLES), sorted(HEDGES)))
    for k in sorted(CHOICES):
        L.append("[CHOICE %d] %s" % (k, CHOICES[k]))
    cs = result["constructed_share"]
    if cs is None:
        L.append("runs: none. No model has been run against this instrument here.")
    else:
        L.append("runs: %d, constructed share %.2f%s" % (
            len(runs), cs, "  -- EVERY RECORD IS CONSTRUCTED; nothing below is about any model" if cs == 1.0 else ""))
    L.append("")
    L.append("per case per arm (section 6)")
    L.append("%-8s %-3s %-16s %-4s %-10s %-9s %-10s %-4s %-4s %-6s %s" % (
        "case", "arm", "run", "n", "distinct", "native", "crossing", "for", "cmp", "ungrp", "coverage"))
    for s in result["scores"]:
        if s["malformed"]:
            L.append("%-8s %-3s %-16s MALFORMED: %s" % (s["case_id"], s["arm"], s["run_id"], "; ".join(s["form_notes"])))
            continue
        L.append("%-8s %-3s %-16s %-4d [%d,%d]      [%d,%d]     [%d,%d]      %-4d %-4d %-6d %.2f" % (
            s["case_id"], s["arm"], s["run_id"], s["n_entries"], s["distinct_min"], s["distinct_max"],
            s["native_hit_min"], s["native_hit_max"], s["crossing_min"], s["crossing_max"],
            s["crossing_foreign"], s["crossing_component"], len(s["ungrouped"]), s["coverage"]))
        for x in s["rows"]:
            L.append("    %2d  %-34s -> %s%s" % (x["n"], x["quantity"][:34], x["measurand"],
                                                 ("  via " + x["via"]) if x["via"] and x["via"] != "identity" else ""))
        if s["form_notes"]:
            L.append("    form: " + "; ".join(s["form_notes"]))
    L.append("")
    L.append("claims (section 7)")
    for k, v in result["claims"].items():
        L.append("  %s  %s%s" % (k, v["verdict"], ("  -- " + v["why"]) if v.get("why") else ""))
        for p in v.get("pairs", []):
            L.append("      " + json.dumps(p, sort_keys=True))
        for p in v.get("families", []):
            L.append("      " + json.dumps(p, sort_keys=True))
    L.append("")
    L.append("nulls (section 8)")
    n = result["nulls"]
    L.append("  N1  practitioner recognition: %s" % json.dumps(n["N1"], sort_keys=True))
    L.append("  N2  control case: %s" % json.dumps(n["N2"], sort_keys=True))
    L.append("  N3  M-arm crossings: %d run(s)" % len(n["N3"]))
    for x in n["N3"]:
        L.append("      " + json.dumps(x, sort_keys=True))
    n4r = result["N4"]
    L.append("  N4  two transform lists disagree on %d of %d bands" % (n4r["disagreements"], n4r["of"]))
    for x in n4r["rows"]:
        if x["disagree"]:
            L.append("      %s %s %s" % (x["run_id"], x["arm"], json.dumps(x["bands"], sort_keys=True)))
    L.append("  N5  form stability: %s" % json.dumps(n["N5"], sort_keys=True))
    L.append("")
    L.append("selection of artifact, field and decision string is operator input (section 9); "
             "nothing above bears on it.")
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------- cli

def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("amc.py refuses --selftest; the checks live in selftest_amc.py\n")
        return 2
    if not argv:
        sys.stderr.write(__doc__)
        return 2
    cmd = argv[0]
    if cmd == "cases":
        for c in load_cases(admit_candidates=True):
            print("%-7s %-8s hand_built=%-5s %s" % (c["case_id"], c["role"], c["hand_built"], c["field"]))
        return 0
    if cmd == "prompt":
        if len(argv) < 3:
            sys.stderr.write("usage: amc.py prompt CASE_ID M|D|M+ [--mplus-placement P]\n")
            return 2
        cases = {c["case_id"]: c for c in load_cases()}
        if argv[1] not in cases:
            sys.stderr.write("case %r not admitted (candidates are listed by `cases`)\n" % argv[1])
            return 2
        pl = argv[argv.index("--mplus-placement") + 1] if "--mplus-placement" in argv else "after_block"
        sys.stdout.write(render_prompt(cases[argv[1]], argv[2], pl) + "\n")
        return 0
    if cmd == "plan":
        seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else 0
        arms = tuple(argv[argv.index("--arms") + 1].split(",")) if "--arms" in argv else ("M", "D", "M+")
        for row in plan(load_cases(), arms, seed):
            print(json.dumps(row))
        return 0
    if cmd == "score":
        if len(argv) < 2:
            sys.stderr.write("usage: amc.py score RUNS.jsonl [--transforms T-A|T-B] [--n1 SHEET.json]\n")
            return 2
        active = argv[argv.index("--transforms") + 1] if "--transforms" in argv else "T-A"
        sheet = None
        if "--n1" in argv:
            with open(argv[argv.index("--n1") + 1], encoding="utf-8") as fh:
                sheet = json.load(fh)
        runs = load_runs(argv[1])
        res = score_runs(runs, load_cases(), load_lexicon(), load_transforms(), active, sheet)
        sys.stdout.write(render(res, runs))
        return 0
    sys.stderr.write(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
