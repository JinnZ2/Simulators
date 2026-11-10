"""probe.py -- submit {action, predicted_result}; get the actual back. CC0, stdlib only.

PROPOSED | co-authored (JinnZ2 + Claude).

The comparison is a record, not a judgement: `match` is True / False, or null
when no prediction was made; `offset` is actual minus predicted, or null.
A path is a start position plus an action sequence; `path_signature` is how
fix.py tells two independent paths from the same path walked twice.
"""
import hashlib
import json


def path_signature(start, actions):
    return hashlib.sha256(json.dumps([list(start), list(actions)]).encode()).hexdigest()[:12]


def compare(predicted, actual):
    if predicted is None:
        return None, None
    predicted = tuple(predicted)
    off = (actual[0] - predicted[0], actual[1] - predicted[1])
    return predicted == tuple(actual), list(off)


def probe(chamber, action, predicted=None, log=None, path_id=None, rule_hypothesis=None, note=None,
          start=None):
    actual = chamber.step(action)
    match, offset = compare(predicted, actual)
    rec = {"kind": "world", "path_id": path_id, "start": list(start) if start else None, "action": action,
           "predicted": list(predicted) if predicted is not None else None,
           "actual": list(actual), "match": match, "offset": offset,
           "rule_hypothesis": rule_hypothesis, "note": note}
    if log is not None:
        rec = log.append(**rec)
    return rec


def probe_path(chamber, actions, predictions=None, log=None, rule_hypothesis=None, note=None):
    """Walk a path; the path_id is its signature from the current reported position."""
    start = chamber.reported()
    pid = path_signature(start, actions)
    preds = predictions or [None] * len(actions)
    out = [probe(chamber, a, p, log, pid, rule_hypothesis, note, start) for a, p in zip(actions, preds)]
    return pid, start, out
