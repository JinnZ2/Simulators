"""selfmode.py -- predict your own next action or answer, then compare. CC0, stdlib only.

PROPOSED | co-authored (JinnZ2 + Claude).

Two levels, both logged: the CATEGORY (e.g. move / wait, or a caller-named
answer class) and the SPECIFIC value (e.g. N, or the answer string). Either
prediction may be left out; the comparison for it is then null, not False.
"""


def action_category(action):
    return "wait" if action == "WAIT" else "move"


def record_self(log, predicted_specific=None, predicted_category=None, actual_specific=None,
                actual_category=None, note=None):
    if actual_category is None and actual_specific in ("N", "S", "E", "W", "WAIT"):
        actual_category = action_category(actual_specific)
    cat = None if predicted_category is None else predicted_category == actual_category
    spec = None if predicted_specific is None else predicted_specific == actual_specific
    rec = {"kind": "self", "action": actual_specific,
           "predicted": {"category": predicted_category, "specific": predicted_specific},
           "actual": {"category": actual_category, "specific": actual_specific},
           "match": {"category": cat, "specific": spec}, "offset": None, "note": note}
    return log.append(**rec) if log is not None else rec
