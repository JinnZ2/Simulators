#!/usr/bin/env python3
"""axes.py -- axis grouping for A3. The order's key move: index by AXIS,
not by rule or by repo, because axes recur across the corpus and rule
wordings do not. An axis key is a recurring measurable noun; a falsifier
carries the axis keys whose word appears in it. A3 then looks within an
axis for records from different repos that carry different numeric
cutoffs. Heuristic and stated as such. Stdlib only.
"""

import re

# Recurring measurable axes in this corpus. Not exhaustive; extend as the
# corpus grows. [CHOICE 1] the vocabulary.
AXIS_VOCAB = frozenset("""units gap null ratio threshold frame transfer margin score count rate
boundary provenance coupling drift window exponent slope variance correlation latency budget
resolution chance baseline control kappa agreement spread sigma decade decades token tokens cell
cells record records gate collapse depth density coverage separation percentile quantile
sensitivity termination convergence""".split())

WORD = re.compile(r"[a-zA-Z][a-zA-Z_-]*")
NUMBER = re.compile(r"(?<![\w.])[-+]?\d+(?:\.\d+)?%?(?![\w])")


def axis_keys(text):
    """The AXIS_VOCAB words present in the falsifier, singular/plural
    folded so 'cells' and 'cell' share an axis."""
    keys = set()
    for w in WORD.findall(text.lower()):
        if w in AXIS_VOCAB:
            keys.add(w.rstrip("s") if w.rstrip("s") in AXIS_VOCAB or (w + "s") in AXIS_VOCAB else w)
    # fold known plurals
    folded = set()
    for k in keys:
        folded.add(k[:-1] if k.endswith("s") and k[:-1] in AXIS_VOCAB else k)
    return folded


def numbers(text):
    return sorted({m.group(0) for m in NUMBER.finditer(text)})


UP = frozenset("rise rises rising above exceeds exceed higher more greater increase increases larger longer later".split())
DOWN = frozenset("fall falls falling below under lower fewer less decrease decreases smaller shorter earlier".split())


def direction(text):
    """up / down / both / none, from direction words in the falsifier."""
    ws = set(WORD.findall(text.lower()))
    up, down = bool(ws & UP), bool(ws & DOWN)
    return "both" if up and down else "up" if up else "down" if down else "none"


def group_by_axis(records):
    """axis_key -> [records carrying it]. A record with no axis key is in
    no group (it is not indexable by axis; A3 says nothing about it)."""
    groups = {}
    for r in records:
        for k in axis_keys(r["text"]):
            groups.setdefault(k, []).append(r)
    return groups


def incompatibilities(records):
    """A3 candidates: an axis carried by records from >= 2 different
    repos, where the numeric cutoffs OR the directions conflict across
    repos. The instrument does not decide whether the difference is real
    (a scope-difference) or a stray cutoff -- both are findings."""
    out = []
    for axis, recs in sorted(group_by_axis(records).items()):
        if len({r["repo"] for r in recs}) < 2:
            continue
        # numeric conflict: >= 2 repos carry numbers on this axis and the
        # number sets are not all identical.
        with_nums = [(r, numbers(r["text"])) for r in recs if numbers(r["text"])]
        num_conflict = False
        if len({r["repo"] for r, _ in with_nums}) >= 2:
            sets = {frozenset(n) for _, n in with_nums}
            num_conflict = len(sets) >= 2
        # direction conflict: two repos carry opposite directions on this axis.
        dirs = {}
        for r in recs:
            d = direction(r["text"])
            if d in ("up", "down"):
                dirs.setdefault(d, set()).add(r["repo"])
        dir_conflict = "up" in dirs and "down" in dirs and (dirs["up"] | dirs["down"]) and dirs["up"] != dirs["down"]
        if not (num_conflict or dir_conflict):
            continue
        members = with_nums if num_conflict else [(r, numbers(r["text"])) for r in recs if direction(r["text"]) in ("up", "down")]
        out.append({"axis": axis, "kind": "numeric" if num_conflict else "direction",
                    "repos": sorted({r["repo"] for r, _ in members}),
                    "records": [{"id": r["id"], "numbers": n, "direction": direction(r["text"]), "text": r["text"]}
                                for r, n in members]})
    return out
