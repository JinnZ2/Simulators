"""Shared helpers for every build in frame-instruments. Not a command.

Scripts in b1/ b2/ b3/ b4/ bootstrap with two lines:
    import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ficommon import ...
"""
import json
import os
import re
import sys
from types import SimpleNamespace

from runrecord import Run, DEFAULT_RUNS_DIR  # noqa: F401

FORBIDDEN = ("label", "category", "type", "interpretation")
B3_ARMS = ("single", "split")
CASE_FIELDS = ("case_id", "statement", "key_posed", "key_target", "key_why")
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


def write_jsonl(path, rows, append=False):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "a" if append else "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")


def check_fields(row, fields, where, exact=True):
    """Return a list of problems, each naming the row and the field. exact forbids extras."""
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


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def is_num(v):
    return (isinstance(v, (int, float)) and not isinstance(v, bool))


def nonempty_str(value):
    return isinstance(value, str) and value.strip() != ""


def raise_if(probs):
    if probs:
        raise Invalid("\n".join(probs))


def count_by(rows, key):
    out = {}
    for r in rows:
        k = r.get(key)
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: str(kv[0])))


def mean(xs):
    xs = list(xs)
    return (sum(xs) / float(len(xs))) if xs else None


def finish(run, status, counts=None, notes=""):
    """Set the record and print the one-line summary."""
    code = run.set(status, counts, notes)
    print("%s: %s %s" % (run.script, status, notes if notes else json.dumps(counts or {}, sort_keys=True)))
    return code


def parse_argv(argv, doc, positional=(), options=(), required=(), defaults=None):
    """Hand-rolled argument parsing: positionals in order, then --name value.
    Returns a SimpleNamespace. --help prints doc and returns None. Unknown or missing
    arguments raise Invalid before any run record exists (a usage error is
    not a run)."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--help" in argv or "-h" in argv:
        print(doc)
        return None
    out = dict(defaults or {})
    for k in options:
        out.setdefault(k, None)
    pos = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--"):
            name = a[2:].replace("-", "_")
            if name not in options:
                raise Invalid("unknown option %s" % a)
            if i + 1 >= len(argv):
                raise Invalid("option %s needs a value" % a)
            out[name] = argv[i + 1]
            i += 2
        else:
            pos.append(a)
            i += 1
    if len(pos) != len(positional):
        raise Invalid("expected %d positional argument(s) %s, got %d" % (len(positional), list(positional), len(pos)))
    out.update(zip(positional, pos))
    missing = [k for k in required if out.get(k) in (None, "")]
    if missing:
        raise Invalid("missing required option(s): %s" % ", ".join("--" + m.replace("_", "-") for m in missing))
    return SimpleNamespace(**out)


def usage_exit(e):
    print("usage error: %s" % e, file=sys.stderr)
    return 2
