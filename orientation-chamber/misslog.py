"""misslog.py -- append-only JSONL log of predictions and outcomes. CC0, stdlib only.

PROPOSED | co-authored (JinnZ2 + Claude).

Every record carries the same fields. A field the agent did not fill is null
(void: no information), never dropped and never a zero. A field whose name
looks like a score, grade or penalty is refused at write time, so one cannot
be added by accident. The first line of a new log is a header record carrying
the principle verbatim. Each record carries `prev`, the sha256 of the line
before it, so a rewritten history is visible to `verify()`.
"""
import hashlib
import io
import json
import os

from common import PRINCIPLE, SCORE_KEYS

FIELDS = ("t", "kind", "path_id", "start", "action", "predicted", "actual", "match", "offset",
          "rule_hypothesis", "note")


class LogFieldRefused(ValueError):
    pass


def _sha(line):
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


class MissLog:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            with io.open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"_header": PRINCIPLE, "status": "PROPOSED",
                                     "fields": list(FIELDS)}, sort_keys=True) + "\n")

    def _last(self):
        with io.open(self.path, encoding="utf-8") as fh:
            lines = [l.rstrip("\n") for l in fh if l.strip()]
        return lines[-1], len(lines) - 1

    def append(self, **kw):
        for k in kw:
            if SCORE_KEYS.search(k):
                raise LogFieldRefused("field %r reads as a score; misslog carries none" % k)
            if k not in FIELDS:
                raise LogFieldRefused("field %r is not a misslog field %s" % (k, FIELDS))
        last, n = self._last()
        rec = dict((f, kw.get(f)) for f in FIELDS)
        if rec["t"] is None:
            rec["t"] = n
        rec["prev"] = _sha(last)
        with io.open(self.path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
        return rec

    def records(self):
        with io.open(self.path, encoding="utf-8") as fh:
            rows = [json.loads(l) for l in fh if l.strip()]
        return [r for r in rows if "_header" not in r]

    def verify(self):
        """True when every record's prev matches the line before it."""
        with io.open(self.path, encoding="utf-8") as fh:
            lines = [l.rstrip("\n") for l in fh if l.strip()]
        return all(json.loads(lines[i]).get("prev") == _sha(lines[i - 1]) for i in range(1, len(lines)))
