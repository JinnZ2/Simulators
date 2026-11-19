"""validate.py: structural checks for M01 and M02 records. It records; it never scores.

  python3 validate.py m01 path/to/records.json     (a JSON list, as m01_code.py writes)
  python3 validate.py m02 path/to/sessions.json    (a JSON list of M02 sessions, each with a "records" list)
  python3 validate.py --arm=rule_on m01 ...        the GPT-6 proposal's rule as an analysis arm (default --arm=rule_off)

Rules (M01_EXTENSION.md section 3; M02_CRITERIA.md section 4):
  - every enum value is checked against the schema files, so the schema and the validator cannot drift apart;
  - null is always allowed where the schema allows it, and means NOT_RECORDED; no field is defaulted;
  - a value whose provenance says NOT_RECORDED must be null, and a null value must not claim a reader stated it;
  - a reader's listing is NEVER checked against key a1's rule (TAG / INDEPENDENCE): a record in which a reader lists a
    computed or shared field is valid. Disagreeing with the key is the behaviour under study, not an error.
Stdlib only.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STUDIES = os.path.dirname(HERE)
load = lambda name: json.load(open(os.path.join(STUDIES, name), encoding="utf-8"))

def _enum(spec):
    return spec.get("enum", spec.get("items", {}).get("enum"))

ARMS = ("rule_off", "rule_on")

def tag_by(x, reading):
    """TAG as a reading of the source half: 'presence' (the key is on every instance of the term and on no other),
    'applicability' (populated on every instance of the term and on no other), or 'a1_defined' (key a1's own TAG: present OR
    required on every instance and on no other). None is chosen here."""
    src = x["source"]
    if reading == "a1_defined":
        # KEY_V2_AMENDMENT_1.md / derive_specific.py: "defined" = a declared parameter, a key present, or a field a rule
        # requires; TAG = defined on every instance of the term and on no other. Coder's mapping onto the three scopes.
        if src["origin"] == "DOCUMENTED": return "UNRESOLVED"
        return "YES" if "ALL_EXCLUSIVE" in (src["presence_scope"], src["requirement_scope"]) else "NO"
    scope = src["presence_scope" if reading == "presence" else "applicability_scope"]
    if scope in ("UNKNOWN", "NO_INSTANCE"): return "UNRESOLVED"
    return "YES" if scope == "ALL_EXCLUSIVE" else "NO"

def independence_of(x):
    o = x["source"]["origin"]
    return {"RAW_INPUT": "YES", "PARAMETER_ONLY": "YES", "COMPUTED": "NO"}.get(o, "UNRESOLVED")

def gpt_rule_errors(recs, reading="a1_defined"):
    """The GPT-6 proposal's validator rule, kept as an arm (rule_on) instead of deleted: a LISTED field must have TAG = YES and
    INDEPENDENCE = YES. TAG and INDEPENDENCE are read off the source half (the proposal asked readers for them; D0 readers
    were never asked), so under rule_on a reader is 'invalid' whenever its listing disagrees with that reading of the rule."""
    err = []
    for x in recs:
        if x["reader"]["listed"] == "LISTED":
            t, i = tag_by(x, reading), independence_of(x)
            if not (t == "YES" and i == "YES"):
                err.append("rule_on: %s %s %s listed with TAG=%s INDEPENDENCE=%s" % (x["reader_id"], x["term_id"], x["field"], t, i))
    return err

def m01_errors(recs, arm="rule_off"):
    if arm not in ARMS:
        raise ValueError("arm must be one of %r" % (ARMS,))
    base = m01_structural_errors(recs)
    return base + (gpt_rule_errors(recs) if arm == "rule_on" and not base else [])

def m01_structural_errors(recs):
    s = load("M01_SCHEMA.json")["fields"]
    sk, rk = s["source"]["keys"], s["reader"]["keys"]
    err = []
    if not isinstance(recs, list):
        return ["M01 input must be a JSON list of records"]
    for i, x in enumerate(recs):
        w = "record %d (%s %s %s): " % (i, x.get("reader_id"), x.get("term_id"), x.get("field"))
        for k in ("study_id", "reader_id", "packet", "condition", "term_id", "field", "source", "reader", "key_a1"):
            if k not in x: err.append(w + "missing " + k)
        if any(e.startswith(w + "missing") for e in err): continue
        if x["study_id"] != "M01": err.append(w + "study_id must be M01")
        if x["condition"] not in s["condition"]["enum"]: err.append(w + "condition %r" % x["condition"])
        src, rdr = x["source"], x["reader"]
        for k in ("origin", "presence_scope", "applicability_scope", "requirement_scope", "provenance"):
            if src.get(k) not in sk[k]["enum"]: err.append(w + "source.%s %r" % (k, src.get(k)))
        if not all(c in _enum(sk["cases"]) for c in src.get("cases", [])): err.append(w + "source.cases")
        for k in ("listed", "basis_kind", "basis_kind_provenance", "provenance"):
            if rdr.get(k) not in rk[k]["enum"]: err.append(w + "reader.%s %r" % (k, rdr.get(k)))
        if rdr.get("uncertainty_stated") not in (True, False, None): err.append(w + "reader.uncertainty_stated")
        # provenance coherence: NOT_RECORDED <-> null
        if rdr.get("basis_kind_provenance") == "NOT_RECORDED" and rdr.get("basis_kind") is not None:
            err.append(w + "basis_kind set but its provenance says NOT_RECORDED")
        if rdr.get("basis_kind") is not None and rdr.get("basis_quote") is None:
            err.append(w + "basis_kind set with no basis_quote to classify")
        if x["key_a1"].get("listed") not in s["key_a1"]["keys"]["listed"]["enum"]: err.append(w + "key_a1.listed")
    return err

def m02_errors(sessions):
    s = load("M02_SCHEMA.json")["levels"]
    sf, rf = s["session"]["fields"], s["record"]["fields"]
    err = []
    if not isinstance(sessions, list):
        return ["M02 input must be a JSON list of sessions"]
    for i, x in enumerate(sessions):
        w = "session %d (%s %s): " % (i, x.get("reader_id"), x.get("term_id"))
        for k in ("study_id", "reader_id", "family", "packet", "condition", "arm", "term_id", "scope_rule", "traversal_rule",
                  "rule_provenance", "records", "unmatched_names"):
            if k not in x: err.append(w + "missing " + k)
        if any(e.startswith(w + "missing") for e in err): continue
        for k in ("condition", "arm", "scope_rule", "traversal_rule", "rule_provenance", "prior_condition"):
            if x.get(k) not in sf[k]["enum"]: err.append(w + "%s %r" % (k, x.get(k)))
        if x["condition"] != "D0" and not x.get("instruction_sha256"): err.append(w + "a D1-D3 session must carry its instruction_sha256")
        if x["condition"] == "D0" and x.get("instruction_sha256") is not None: err.append(w + "a D0 session has no instruction file")
        if x["arm"] == "SEQUENTIAL" and (x.get("sequence_index") or 0) > 1 and x.get("prior_condition") is None:
            err.append(w + "a later sequential session must name its prior_condition")
        if x["arm"] == "PARALLEL" and x.get("prior_condition") is not None: err.append(w + "a parallel session has no prior condition")
        if x["rule_provenance"] == "NOT_RECORDED" and (x["scope_rule"] is not None or x["traversal_rule"] is not None):
            err.append(w + "a rule is set but rule_provenance says NOT_RECORDED")
        if x["rule_provenance"] == "READER_STATED" and not x.get("rule_quote"):
            err.append(w + "READER_STATED rule needs its verbatim rule_quote")
        ids = [r.get("record_id") for r in x["records"]]
        if len(ids) != len(set(ids)): err.append(w + "duplicate record_id")
        for r in x["records"]:
            v = w + "record %s: " % r.get("record_id")
            for k in ("relationship", "catalog_provenance", "counted", "counted_provenance"):
                if r.get(k) not in rf[k]["enum"]: err.append(v + "%s %r" % (k, r.get(k)))
            for ref in (r.get("nested_field_refs") or {}).values():
                if ref not in ids: err.append(v + "nested ref to unknown record %r" % ref)
            if r.get("opened") is not None and r.get("relationship") != "NESTED_RECORD":
                err.append(v + "opened applies to NESTED_RECORD only")
    return err

def main(argv):
    arm = "rule_off"
    if argv and argv[0].startswith("--arm="):
        arm = argv[0].split("=", 1)[1]; argv = argv[1:]
    if len(argv) != 2 or argv[0] not in ("m01", "m02") or arm not in ARMS:
        print(__doc__); return 2
    data = json.load(open(argv[1], encoding="utf-8"))
    errs = m01_errors(data, arm) if argv[0] == "m01" else m02_errors(data)
    n_rule = sum(1 for e in errs if e.startswith("rule_on:"))
    print("%s: %d item(s), %d structural error(s)%s" % (argv[0], len(data) if isinstance(data, list) else 0, len(errs) - n_rule,
          (", %d rule_on rejection(s) (analysis arm, TAG read as key a1 defines it)" % n_rule) if arm == "rule_on" else ""))
    for e in errs: print("  " + e)
    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
