#!/usr/bin/env python3
"""trust_provenance.py -- WO-1 step 2: what provenance on a trust
ASSIGNMENT would have to include for the assignment to be auditable.

A specification exercise, as the order says. No vendor internals are
used or sought; every record here is CONSTRUCTED and says so in its own
`source` field. The spec is [CHOICE 1] and is printed with every render.

The order's second-order gap: return-path filtration scores the PAYLOAD;
the trust score is itself a chained artifact with its own provenance.
So an assignment record is auditable only if it carries the provenance
of the SCORER that produced it, recursively, until a DECLARED root. A
chain that runs out without a declared root is CHAIN_UNTERMINATED --
which is the horn-A relocation seen from the record side.

Three non-value states are kept apart on every field:
  PRESENT      the field carries a value
  ABSENT       the field is missing (nobody wrote it)
  UNDECLARED   the author wrote the sentinel "UNDECLARED" (looked, has nothing)
An ABSENT field and an UNDECLARED one call for different next actions.

`common_object` is the order's "no common object to audit": over N
records from N sources, the set of fields every record carries. Audit
across sources is possible iff that set covers the spec.
"""
import json
import sys

SPEC_CHOICE = 1
DEPTH_CAP = 8          # [CHOICE 2] recursion cap on scorer_provenance
UNDECLARED = "UNDECLARED"

# [CHOICE 1] the specification: field -> (sub-fields required, why)
SPEC = (
    ("subject", ("id", "digest"), "what was scored, pinned by content digest not by name"),
    ("score", ("value", "scale"), "a number with no scale is not comparable to any other"),
    ("scorer", ("id", "version_digest"), "which scorer, pinned; a name alone drifts"),
    ("inputs", (), "every artifact the scorer read; the payload alone, or the payload plus a prior score"),
    ("method", ("id",), "the rule applied, named so it can be re-run"),
    ("position", ("step_index", "chain_id"), "where in the chain the score was assigned"),
    ("t_scored", (), "when; a score with no clock cannot be ordered against the item it scores"),
    ("authorization", ("policy_id",), "the policy that admitted this scorer at this position"),
    ("scorer_provenance", (), "the assignment record for the SCORER, recursive to a declared root"),
)
REQUIRED = tuple(f for f, _, _ in SPEC)
STATES = ("AUDITABLE", "UNAUDITABLE", "DECLARED_UNAUDITABLE", "CHAIN_UNTERMINATED", "CHAIN_CYCLE", "MALFORMED")


def field_state(record, name, subs):
    """PRESENT / ABSENT / UNDECLARED for one spec field."""
    if name not in record:
        return "ABSENT"
    v = record[name]
    if v == UNDECLARED:
        return "UNDECLARED"
    if subs:
        if not isinstance(v, dict):
            return "ABSENT"
        if any(s not in v for s in subs):
            return "ABSENT"
        if any(v[s] == UNDECLARED for s in subs):
            return "UNDECLARED"
    if name == "inputs" and (not isinstance(v, list) or not v):
        return "ABSENT"
    return "PRESENT"


def audit(record, _depth=0, _seen=None):
    """One assignment record -> verdict. Recurses on scorer_provenance."""
    if not isinstance(record, dict):
        return {"state": "MALFORMED", "why": "record is not a dict", "depth": _depth}
    _seen = _seen or []
    fields = {name: field_state(record, name, subs) for name, subs, _ in SPEC}
    absent = [f for f, s in fields.items() if s == "ABSENT"]
    undeclared = [f for f, s in fields.items() if s == "UNDECLARED"]
    out = {"fields": fields, "absent": absent, "undeclared": undeclared, "depth": _depth,
           "scores_payload_only": scores_payload_only(record)}
    if absent:
        out["state"] = "UNAUDITABLE"
        return out
    if undeclared:
        out["state"] = "DECLARED_UNAUDITABLE"
        return out
    sp = record["scorer_provenance"]
    if isinstance(sp, dict) and "root" in sp and len(sp) == 1:
        out["state"] = "AUDITABLE"
        out["root"] = sp["root"]
        return out
    if _depth >= DEPTH_CAP:
        out["state"] = "CHAIN_UNTERMINATED"
        out["why"] = "depth cap %d reached without a declared root [CHOICE 2]" % DEPTH_CAP
        return out
    # Cycle check by OBJECT IDENTITY first, then by content. The first
    # version serialized the node before checking for a cycle, and a
    # genuinely cyclic chain crashed the serializer before the detector
    # written for cycles ever ran (found by running, CHP claim table).
    if id(sp) in _seen:
        out["state"] = "CHAIN_CYCLE"
        out["why"] = "provenance node is its own ancestor (object identity)"
        return out
    try:
        key = json.dumps(sp, sort_keys=True) if isinstance(sp, dict) else repr(sp)
    except ValueError:
        out["state"] = "CHAIN_CYCLE"
        out["why"] = "provenance node contains a reference loop (serializer refused)"
        return out
    if key in _seen:
        out["state"] = "CHAIN_CYCLE"
        out["why"] = "provenance node repeats an ancestor by content"
        return out
    inner = audit(sp, _depth + 1, _seen + [id(sp), key])
    out["state"] = inner["state"] if inner["state"] != "AUDITABLE" else "AUDITABLE"
    out["depth"] = inner["depth"]
    if "root" in inner:
        out["root"] = inner["root"]
    out["inner"] = inner
    return out


def scores_payload_only(record):
    """True when the scorer read the payload and nothing else -- the
    return-path-filtration shape the order describes. A property, not a
    fault. None when it cannot be read."""
    if not isinstance(record, dict):
        return None
    subj = record.get("subject")
    inputs = record.get("inputs")
    if not isinstance(subj, dict) or not isinstance(inputs, list) or not inputs:
        return None
    digests = [i.get("digest") for i in inputs if isinstance(i, dict)]
    if len(digests) != len(inputs):
        return None
    return digests == [subj.get("digest")]


def common_object(records):
    """Fields PRESENT in every record. Audit across sources needs the
    intersection to cover the spec."""
    if not records:
        return {"state": "EMPTY", "common": [], "missing": list(REQUIRED)}
    present = []
    for r in records:
        if not isinstance(r, dict):
            present.append(set())
            continue
        present.append({name for name, subs, _ in SPEC if field_state(r, name, subs) == "PRESENT"})
    common = set.intersection(*present)
    missing = [f for f in REQUIRED if f not in common]
    return {"state": "COMMON_OBJECT" if not missing else "NO_COMMON_OBJECT",
            "n_records": len(records), "common": [f for f in REQUIRED if f in common], "missing": missing}


def full_record(step=2, chain="CONSTRUCTED-chain", root="declared root: operator policy P0"):
    return {
        "source": "CONSTRUCTED",
        "subject": {"id": "payload-1", "digest": "d1"},
        "score": {"value": 0.8, "scale": "[0,1] trust"},
        "scorer": {"id": "scorer-A", "version_digest": "sA"},
        "inputs": [{"id": "payload-1", "digest": "d1"}],
        "method": {"id": "rule-7"},
        "position": {"step_index": step, "chain_id": chain},
        "t_scored": "2026-09-19T00:00:00Z",
        "authorization": {"policy_id": "P0"},
        "scorer_provenance": {"root": root},
    }


def constructed_set():
    """Three CONSTRUCTED records from three unnamed sources."""
    a = full_record()
    b = {"source": "CONSTRUCTED", "score": {"value": 3, "scale": "1-5"}, "method": {"id": "m"}}
    c = full_record()
    del c["scorer_provenance"]
    return [a, b, c]


def render(records=None):
    records = records if records is not None else constructed_set()
    lines = ["trust_provenance -- WO-1 step 2, provenance of a trust ASSIGNMENT",
             "  spec is [CHOICE %d]; depth cap %d is [CHOICE 2]; every record CONSTRUCTED" % (SPEC_CHOICE, DEPTH_CAP),
             "  spec fields:"]
    for name, subs, why in SPEC:
        lines.append("    %-19s %-28s %s" % (name, ",".join(subs) or "-", why))
    lines.append("  records:")
    for i, r in enumerate(records):
        a = audit(r)
        lines.append("    #%d  %-22s absent=%s undeclared=%s depth=%s payload_only=%s" % (
            i, a["state"], a.get("absent", []), a.get("undeclared", []), a.get("depth"), a.get("scores_payload_only")))
    co = common_object(records)
    lines.append("  common object across %d records: %s  common=%s missing=%s" % (
        co.get("n_records", 0), co["state"], co["common"], co["missing"]))
    lines.append("  reading: the order's 'no common object to audit' is a property of the intersection,")
    lines.append("           and the intersection is measured here on constructed records only")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        print("trust_provenance.py refuses --selftest; run: python3 selftest.py")
        return 2
    if "--records" in argv:
        path = argv[argv.index("--records") + 1]
        with open(path) as f:
            recs = [json.loads(l) for l in f if l.strip()]
        print(render(recs))
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
