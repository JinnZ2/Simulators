#!/usr/bin/env python3
"""Build packet v2 and key v2: the same 15 terms, the same sources, but "slots" is split into two questions.
  python3 make_packet_v2.py            (run from anywhere; uses the files in this folder only)
Reads:   reader_packet/ (v1, unchanged), scoring/key.json (v1, unchanged), scoring/score.py (tier rule)
Writes:  reader_packet_v2/              v1 packet with a new brief, response template and manifest
         variants/READER_BRIEF.v2.variant_B.md   v2 brief without the clause (see PREREG.md)
         scoring/key_v2.json            per term: slots_specific, slots_carried (or null), how derived
Why: in v1 one word, "slots", covered three different things (a term's own record, the shared record that carries it,
and symbols for a calculation's inputs). Readers, and the key, used different ones. v2 asks for the first two
separately and drops the third. The derivation of each key list is written beside it and checked by test_score_v2.py
against the packet's own source files (names present, cplay records by running the pinned code).
"""
import hashlib, json, os, shutil, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "scoring"))
import score as S  # noqa: E402

READING = ["field", "status", "reason", "sigma", "basis", "exception", "path", "bound"]
COVERAGE = ["kind", "module", "input", "reason", "missing_path", "expiry_condition"]
EXPIRY = ["instrument_class", "sensitivity", "protocol", "provenance"]
BLANK = ["kind", "verdict", "void_reason", "status", "deciding_tier", "precision", "rigorous", "fast", "tiers", "triage",
         "located", "proposal", "intervals", "inputs", "units", "provenance", "slots", "human_interest", "ai_interest"]
POINT = BLANK + ["formula", "bisection"]
INTERSECTION = BLANK + ["formulas", "subboxes", "subboxes_where_both_hold", "subboxes_where_one_fails",
                        "first_undecided_subbox", "first_subbox_with_no_value"]
UNION_NUM = BLANK + ["formula", "bisection", "formulas", "subboxes", "subboxes_where_both_hold",
                     "subboxes_where_one_fails", "first_undecided_subbox", "first_subbox_with_no_value"]
CRASH_ALL = READING + [x for x in COVERAGE if x not in READING]

# term_id -> (specific, carried, how derived).  None = undetermined: the sources support more than one answer.
V2 = {
 "fa:UNDECIDED": ([], UNION_NUM, "specific: UNDECIDED is a verdict value of numcheck's result record; no class, function or key list is written for it (the symbols D and t in the docstring are inputs to the decision, not slots). carried: keys of the record built by check_point (_blank + formula + bisection) and by check_intersection (_blank + formulas + the five subbox keys); the docstring says UNDECIDED can end either check. Checked by running check_point on the pinned file."),
 "taf:ABSENT_AT_SENSITIVITY": (["value"], ["value"], "the glossary and expiry_register.py write the notation ABSENT_AT_SENSITIVITY(<value>); the prose names instrument, sensitivity and protocol as what the value must state but writes no field list; no record holds the state today ('No slot holds it yet')."),
 "cplay:VOID": ([], ["state", "reason"], "specific: no constructor or key list is written for VOID; tokens.py requires a reason on every non-verdict token, a rule shared by all of them. carried: Token(state, reason), which every VOID in the sources constructs."),
 "cplay:ExpiryTrigger": (["kind", "target", "condition"], ["kind", "target", "condition"], "class ExpiryTrigger(kind, target, condition); instance fields the same."),
 "cplay:ABSENT_AT_SENSITIVITY": (["limit", "basis", "effect_size", "conditions", "ladder"], ["state", "reason", "limit", "basis", "effect_size", "conditions", "ladder", "covers_effect"], "specific: parameters of tokens.absent_at_sensitivity. carried: instance fields of the Token it returns, checked by running it."),
 "cplay:UNRESOLVED": ([], ["field", "token"], "specific: nothing is tied to UNRESOLVED alone (the guard-band inputs m, tol, U are inputs to the decision, not slots). carried: closure.FieldToken(field, token); the Token inside is a field's value and is not opened."),
 "fa:VOID": ([], UNION_NUM, "as fa:UNDECIDED: VOID is the verdict of _blank, which both check_point and check_intersection start from."),
 "cplay:CRASHED": (None, CRASH_ALL, "specific: undetermined. axes.crash(exc, *, path, module, inputs, expiry_condition) is written for CRASHED, but what it builds is the shared Reading plus a CoverageEntry, and the sources support reading 'specific' as the call's parameters or as CoverageEntry's fields. carried: fields of Reading and of CoverageEntry (reason once), checked by running crash()."),
 "taf:UNKNOWN": ([], None, "specific: the glossary defines UNKNOWN as a status of a slot and names no fields for it. carried: undetermined; the register describes the expiry_condition and expiry_source that go beside an UNKNOWN slot but names no record that is built for UNKNOWN."),
 "taf:GAP_INSTRUMENT_CRASH": (COVERAGE, COVERAGE, "unified_audit.py builds one dictionary in the branch written for this term; its six keys. Same list for both meanings."),
 "fa:HOLDS": ([], POINT, "as fa:UNDECIDED, point check only: check_intersection's own verdicts are not HOLDS (HOLDS appears there only for subboxes)."),
 "cplay:UNKNOWN": (["reason", "triggers"], ["state", "reason", "typed", "untyped"], "specific: parameters of tokens.unknown(reason, triggers). carried: instance fields of the Token it returns, checked by running it. The nested ExpiryTrigger objects held in 'typed' are not opened."),
 "cplay:OK": ([], READING, "specific: OK needs no field beyond the shared record (axes.reading). carried: Reading(field, status, reason, sigma, basis, exception, path, bound), what axes.reading returns for OK."),
 "cplay:CLOSED_WITHIN": (["sigma", "basis"], READING, "specific: axes.reading raises unless CLOSED_WITHIN has a numeric sigma >= 0 and a basis. carried: the shared Reading fields."),
 "taf:expiry_condition": (EXPIRY, EXPIRY, "expiry_register.EXPIRY_KEYS; the register rejects any other key set."),
}

NEW_SLOTS = """**Slots.** "Slots" can mean two different things, so you are asked for both, as two separate lists. Use the source's spelling, each name once.

- `slots_specific`: the named fields or parameters the source ties to this term and to no other term. Examples: a class written for the term, the parameters of a function or notation written for it, a documented key list for it, or a rule that says this status needs certain fields. Not fields that every term sharing a record has. Not names for the inputs of a calculation. If nothing is tied to this term alone, write `[]`.
- `slots_carried`: every named field of every record that the source's code or text builds, returns or documents when this term is reported. This includes a shared or wrapper record that only carries the term as a value. Give a record's own fields; if a field holds another record, name the field and do not open it. If a record's fields differ by path, give every name the source can put in it. If no record is built or documented for the term, write `[]`.

The two lists often differ and may be equal, and a name can be in one list only (a constructor's parameter is not always a field of what it returns). Do not copy one into the other for convenience. If you cannot tell which list a field belongs in, put it where you think it fits and say so in `source_lines_read`.

Each list has its own basis field, `slots_specific_basis` and `slots_carried_basis`:
- `READ_FROM_SOURCE`: the source names the fields (give file and lines in `source_lines_read`).
- `NONE_STATED`: the source names none for this meaning. Write `[]`.
- `DECLARED`: the source names none, but you are naming them yourself from the prose. Say why in one line in `source_lines_read`."""

def sha(b): return hashlib.sha256(b).hexdigest()

def build():
    src, dst = os.path.join(HERE, "reader_packet"), os.path.join(HERE, "reader_packet_v2")
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(src, dst)
    # brief
    with open(os.path.join(src, "READER_BRIEF.md"), encoding="utf-8") as f: b = f.read()
    i, j = b.index("**Slots.**"), b.index("**Cluster.**")
    b2 = b[:i] + NEW_SLOTS + "\n\n" + b[j:]
    old = "2. **What are each term's slots?** List the named fields or parameters the term carries, as the source names them."
    assert old in b2
    b2 = b2.replace(old, "2. **What are each term's slots?** Two lists per term, defined below: the fields the source ties to this term alone, and every field of every record the source builds when this term is reported.")
    old = "| `slots` | list of slot names, or `[]` |\n| `slots_basis` | `READ_FROM_SOURCE`, `NONE_STATED` or `DECLARED` |\n"
    assert old in b2
    b2 = b2.replace(old, "| `slots_specific` | list of names, or `[]` |\n| `slots_specific_basis` | `READ_FROM_SOURCE`, `NONE_STATED` or `DECLARED` |\n| `slots_carried` | list of names, or `[]` |\n| `slots_carried_basis` | `READ_FROM_SOURCE`, `NONE_STATED` or `DECLARED` |\n")
    assert b2.count("slots_basis") == 0
    with open(os.path.join(dst, "READER_BRIEF.md"), "w", encoding="utf-8", newline="\n") as f: f.write(b2)
    clause = ", even if the second system attaches different extra fields or detail"
    assert b2.count(clause) == 1
    os.makedirs(os.path.join(HERE, "variants"), exist_ok=True)
    with open(os.path.join(HERE, "variants", "READER_BRIEF.v2.variant_B.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(b2.replace(clause, ""))
    # template
    with open(os.path.join(src, "response_template.json"), encoding="utf-8") as f: t = json.load(f)
    for k in t["terms"]:
        t["terms"][k] = {"cluster": "", "predicate": "", "slots_specific": [], "slots_specific_basis": "",
                         "slots_carried": [], "slots_carried_basis": "", "source_lines_read": "", "confidence": "",
                         "could_also_join": []}
    with open(os.path.join(dst, "response_template.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(t, f, indent=1); f.write("\n")
    # manifest
    with open(os.path.join(src, "PACKET_MANIFEST.json"), encoding="utf-8") as f: m = json.load(f)
    for ex in m.get("reviewed_leak_check_exceptions", []):
        ex["reason"] = ex["reason"].replace(", unrelated to the vocabulary mapping", "")   # v1 wording hinted at the project's purpose
    for rel in ("READER_BRIEF.md", "response_template.json"):
        with open(os.path.join(dst, rel), "rb") as f: data = f.read()
        m["files"][rel] = {"bytes": len(data), "sha256": sha(data)}
    with open(os.path.join(dst, "PACKET_MANIFEST.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(m, f, indent=1); f.write("\n")
    # key v2
    with open(os.path.join(HERE, "scoring", "key.json"), encoding="utf-8") as f: k = json.load(f)
    terms = {}
    for i, t in k["terms"].items():
        sp, ca, how = V2[t["term_id"]]
        terms[i] = {"term_id": t["term_id"], "label": t["label"], "cluster": t["cluster"], "predicate": t["predicate"],
                    "slots_specific": sp, "slots_carried": ca, "derivation": how,
                    "v1_slots_welded": t["slots"], "v1_slots_from": t["slots_from"]}
    sets = lambda i, m: terms[i][m]
    pairs = []
    for p in k["pairs"]:
        a, b = p["left"], p["right"]
        row = dict(p)
        for meaning in ("slots_specific", "slots_carried"):
            sa, sb = sets(a, meaning), sets(b, meaning)
            if p["same_predicate"] and (sa is None or sb is None):
                row["key_tier_" + meaning[6:]] = None
            else:
                row["key_tier_" + meaning[6:]] = S.tier(p["same_predicate"], sa or [], sb or [], k["terms"][a]["label"], k["terms"][b]["label"])
        pairs.append(row)
    meta = dict(k["meta"]); meta.update(v=2, key_v1_sha256=sha(open(os.path.join(HERE, "scoring", "key.json"), "rb").read()),
        note="slots_* = None means undetermined: scored as 'not determined', never as a match or a miss")
    with open(os.path.join(HERE, "scoring", "key_v2.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"meta": meta, "terms": terms, "pairs": pairs}, f, indent=1); f.write("\n")
    return pairs, terms

if __name__ == "__main__":
    pairs, terms = build()
    for p in pairs:
        print("%-46s declared %-8s specific %-8s carried %-8s" % (p["pair_label"], p["key_tier"], p["key_tier_specific"], p["key_tier_carried"]))
    print("null lists:", [(i, m) for i, t in terms.items() for m in ("slots_specific", "slots_carried") if t[m] is None])
