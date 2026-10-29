#!/usr/bin/env python3
"""SAL-WO2: the confound_record type, beside the delivered lab, not inside it.

The continuation report's top recommendation (sec. 6.2, sec. 7): one record
per alternative explanation, with the test applied, its result, a status and
a version stamp, under the lab's no-verdict rule. Thread B's ten confounds
are seeded as UNTESTED.

The delivered lab (lab_0_3/) is not edited. Its validator accepts a closed
list of five record types, so a new type cannot validate there without an
edit, against the report's own "new record types may be added". Two
encodings are therefore provided and both are tested:

    native        record_type "confound_record", validated by validate() here
    lab-encoded   record_type "audit_event", event_kind "confound_record",
                  which the lab's own validate_record accepts unchanged

States are kept apart; none of them is a verdict:

    UNTESTED            no test has been run          (not "absent")
    RAN_NO_SIGNAL       a stated test ran; it showed nothing
    RAN_SIGNAL          a stated test ran; it showed something
    NOT_TESTABLE        no test is available; the reason is required

Append-only: a status change is a new record that names the one it
supersedes. Nothing is edited in place, and no function combines the
statuses into a "confounded / clean" call.

    python3 confound_record.py     the seeded ledger for thread B
The module refuses --selftest; checks live in test_confound_record.py.
"""
import json
import sys
import uuid
from datetime import datetime, timezone

SCHEMA_VERSION = "0.2"
STATES = ("UNTESTED", "RAN_NO_SIGNAL", "RAN_SIGNAL", "NOT_TESTABLE")
MODEL_ID_STATES = ("STATED", "WITHHELD", "NO_BUILD_STRING")

# Thread B's ten confounds, as the continuation report lists them (sec. 6.2).
THREAD_B = (
    ("C01", "corpus prior"),
    ("C02", "framing pull"),
    ("C03", "trained reflex"),
    ("C04", "narration-not-causal"),
    ("C05", "context contamination"),
    ("C06", "sampling variance"),
    ("C07", "version drift"),
    ("C08", "evaluator sharing"),
    ("C09", "term freight"),
    ("C10", "observer effect"),
)


class ConfoundRecordError(ValueError):
    pass


def _now():
    return datetime.now(timezone.utc).isoformat()


def version_stamp(model_id_state, model_id=None, reason=None, date=None):
    """Confound 7 (version drift) is why every non-UNTESTED record carries
    one. A missing model id is a state with a reason, never a blank."""
    if model_id_state not in MODEL_ID_STATES:
        raise ConfoundRecordError(f"model_id_state must be one of {MODEL_ID_STATES}")
    if model_id_state == "STATED" and not model_id:
        raise ConfoundRecordError("STATED needs a model_id")
    if model_id_state != "STATED" and not reason:
        raise ConfoundRecordError(f"{model_id_state} needs a reason")
    return {"model_id_state": model_id_state, "model_id": model_id,
            "reason": reason, "date": date or _now()[:10]}


def make(confound_id, name, status, *, subject_record_ids=(), test_applied=None,
         result=None, evidence=(), reason=None, stamp=None, supersedes=None,
         record_id=None):
    """Return a native confound_record dict, or raise. The rules:
      UNTESTED      test_applied and result must be absent
      RAN_*         test_applied, result and a version stamp are required
      NOT_TESTABLE  a reason is required"""
    if status not in STATES:
        raise ConfoundRecordError(f"status must be one of {STATES}")
    if status == "UNTESTED" and (test_applied or result):
        raise ConfoundRecordError("UNTESTED cannot carry a test or result")
    if status.startswith("RAN_"):
        if not test_applied or not result:
            raise ConfoundRecordError(f"{status} needs test_applied and result")
        if stamp is None:
            raise ConfoundRecordError(f"{status} needs a version stamp (confound 7)")
    if status == "NOT_TESTABLE" and not reason:
        raise ConfoundRecordError("NOT_TESTABLE needs a reason")
    return {
        "schema_version": SCHEMA_VERSION,
        "record_type": "confound_record",
        "record_id": record_id or f"confound_record_{uuid.uuid4().hex[:12]}",
        "created_utc": _now(),
        "payload": {
            "confound_id": confound_id,
            "name": name,
            "status": status,
            "subject_record_ids": list(subject_record_ids),
            "test_applied": test_applied,
            "result": result,
            "evidence": list(evidence),
            "reason": reason,
            "version_stamp": stamp,
            "supersedes": supersedes,
            "interpretation": "unassigned",
        },
    }


def validate(rec):
    """Problems with one native record; [] if none."""
    p = rec.get("payload", {})
    out = []
    if rec.get("record_type") != "confound_record":
        out.append("record_type is not confound_record")
    try:
        make(p.get("confound_id"), p.get("name"), p.get("status"),
             test_applied=p.get("test_applied"), result=p.get("result"),
             reason=p.get("reason"), stamp=p.get("version_stamp"))
    except ConfoundRecordError as e:
        out.append(str(e))
    if p.get("interpretation") != "unassigned":
        out.append("interpretation must stay unassigned")
    return out


def validate_stream(records):
    """Append-only checks over a stream: unique ids, and every `supersedes`
    points to an EARLIER record for the SAME confound."""
    out, seen = [], {}
    for i, r in enumerate(records):
        rid = r["record_id"]
        if rid in seen:
            out.append(f"{rid}: id repeated (edit in place?)")
        sup = r["payload"].get("supersedes")
        if sup is not None:
            if sup not in seen:
                out.append(f"{rid}: supersedes {sup}, which is not earlier in the stream")
            elif seen[sup] != r["payload"]["confound_id"]:
                out.append(f"{rid}: supersedes a record for a different confound")
        seen[rid] = r["payload"]["confound_id"]
        out += [f"{rid}: {m}" for m in validate(r)]
    return out


def current(records):
    """Latest record per confound (the head of each supersedes chain).
    Returns {confound_id: status}. No combination of statuses is returned."""
    superseded = {r["payload"]["supersedes"] for r in records if r["payload"]["supersedes"]}
    heads = {}
    for r in records:
        if r["record_id"] not in superseded:
            heads[r["payload"]["confound_id"]] = r["payload"]["status"]
    return heads


def counts(records):
    c = {s: 0 for s in STATES}
    for s in current(records).values():
        c[s] += 1
    return c


def to_lab_audit_event(rec):
    """The lab-compatible encoding: an audit_event the delivered lab's own
    validate_record accepts. The confound fields ride in the payload."""
    p = dict(rec["payload"])
    return {
        "schema_version": rec["schema_version"],
        "record_type": "audit_event",
        "record_id": rec["record_id"].replace("confound_record_", "audit_event_"),
        "created_utc": rec["created_utc"],
        "payload": {
            "subject_record_ids": p["subject_record_ids"],
            "event_kind": "confound_record",
            "description": f"{p['confound_id']} {p['name']}: {p['status']}",
            "evidence": p["evidence"],
            "unresolved_questions": [] if p["status"] != "UNTESTED"
            else [f"{p['name']} has not been tested"],
            "proposed_next_tests": [],
            "verdict": None,
            "confound": p,
        },
    }


def seed_thread_b(subject_record_ids=()):
    """All ten of thread B's confounds as UNTESTED: the honest starting state."""
    return [make(cid, name, "UNTESTED", subject_record_ids=subject_record_ids)
            for cid, name in THREAD_B]


def render():
    recs = seed_thread_b()
    lines = ["scope-audit-lab / confound_record.py", "=" * 60,
             "thread B seeded (sec. 6.2 of the continuation report):"]
    for r in recs:
        p = r["payload"]
        lines.append(f"   {p['confound_id']}  {p['status']:<13} {p['name']}")
    c = counts(recs)
    lines += ["", "current status counts: " + ", ".join(f"{k} {v}" for k, v in c.items()),
              "no combined call is produced; UNTESTED is not 'absent'"]
    return "\n".join(lines)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("confound_record.py is a library; run: python3 test_confound_record.py")
        sys.exit(2)
    if "--jsonl" in sys.argv[1:]:
        for r in seed_thread_b():
            print(json.dumps(r, sort_keys=True))
    else:
        print(render())
