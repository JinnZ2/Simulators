"""Shared I/O and schema checks for the B4 scripts. Not a command."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
if PARENT not in sys.path:
    sys.path.insert(0, PARENT)
from runrecord import Run, DEFAULT_RUNS_DIR  # noqa: E402,F401

FORBIDDEN = ("label", "category", "interpretation")
STATES = ("true", "false", "lapsed", "partial", "unknown", "undifferentiated")
ARMS = ("hypothetical", "documented")
ITEM_FIELDS = ("item_id", "source", "text_verbatim", "branches_stated", "arm")
REQ_FIELDS = ("item_id", "reconstructor_id", "req_id", "requirement_text",
              "status", "settling_test", "layer")
MATCH_FIELDS = ("item_id", "req_a", "req_b", "matched")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class Invalid(Exception):
    """Schema or content problem: status=error."""


class Void(Exception):
    """Well-formed input that the protocol refuses: status=void."""


def read_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except ValueError as e:
                raise Invalid("%s:%d not JSON: %s" % (path, n, e))
            if not isinstance(row, dict):
                raise Invalid("%s:%d not an object" % (path, n))
            rows.append(row)
    return rows


def write_jsonl(path, rows):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")


def check_fields(row, fields, where, exact=True):
    """Return a list of problems. exact=True forbids extra keys."""
    probs = []
    for k in FORBIDDEN:
        if k in row:
            probs.append("%s: forbidden field %r" % (where, k))
    for k in fields:
        if k not in row:
            probs.append("%s: missing field %r" % (where, k))
    if exact:
        for k in row:
            if k not in fields:
                probs.append("%s: unexpected field %r" % (where, k))
    return probs


def check_id(value, where):
    if not isinstance(value, str) or not ID_RE.match(value):
        return ["%s: id %r must match %s" % (where, value, ID_RE.pattern)]
    return []


def nonempty_str(value):
    return isinstance(value, str) and value.strip() != ""


def ref(reconstructor_id, req_id):
    return "%s/%s" % (reconstructor_id, req_id)


def parse_ref(s):
    if not isinstance(s, str) or s.count("/") != 1:
        raise Invalid("requirement reference %r must be reconstructor_id/req_id" % (s,))
    a, b = s.split("/")
    return a, b


def raise_if(probs):
    if probs:
        raise Invalid("\n".join(probs))


def count_by(rows, key):
    out = {}
    for r in rows:
        k = r.get(key)
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (str(kv[0]))))


def finish(run, status, counts=None, notes=""):
    """Set the record and print one line so failed runs are visible."""
    code = run.set(status, counts, notes)
    print("%s: %s %s" % (run.script, status, notes if notes else json.dumps(counts or {})))
    return code
