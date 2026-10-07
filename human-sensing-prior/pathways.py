"""pathways.py -- pathway A vs pathway B, per problem class.

CC0 1.0 Universal. Stdlib only. Python >= 3.9.

Two documents carry the same correction in two shapes:

    A   human-sensing-prior.md   (convergence, effective-N, P1-P4)
    B   PATHWAY_B.md             (cessation-as-cue, scope limits, F1-F3)

The question is not which file is better. It is, per problem class, which
one moves a model's answer in the good direction more, and whether either
beats having no document. The predictions were committed to
PREDICTIONS.md BEFORE this file existed; every report prints that file's
sha256 so an edit after the fact is visible.

Commands
    --features            locate, by line, the feature each prediction rests on
    --emit OUT.jsonl      probe battery (arms NONE / A / B / AB, opaque ids)
                          and OUT.key.jsonl, the arm key, kept apart
    --sheet IN.jsonl      coding sheet from a battery: id, class, field only
    --score KEY CODES     per-class rates, A vs B, each vs NONE, AB vs the
                          better single arm, pattern verdict

No model is called anywhere. The operator runs each prompt cold, pastes
the response into the sheet, and a coder who does not hold the key fills
`code` with yes / no / unclear.

[CHOICE n] marks a decision PREDICTIONS.md did not fix. `--choices` prints
them.
"""

import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILE_A = "human-sensing-prior.md"
FILE_B = "PATHWAY_B.md"
PREDICTIONS = "PREDICTIONS.md"

ARMS = ("NONE", "A", "B", "AB")
CODES = ("yes", "no", "unclear")

CHOICES = {
    1: "Z = 2.0 for every interval (about 95%); no multiplicity correction "
       "across the five classes, so a single class win is read with that "
       "in mind.",
    2: "MIN_N = 10 coded (yes+no) responses per arm per class; below it a "
       "comparison is NOT_EVALUABLE, never NO_DIFFERENCE.",
    3: "Difference interval is Agresti-Caffo (add one success and one "
       "failure to each arm) on the GOOD-outcome rate, so a positive "
       "difference always means the first arm did better.",
    4: "MDD is the interval half-width at p = 0.5 for the observed n: the "
       "smallest difference this n could have called, worst case.",
    5: "AB order alternates by repeat: even repeat A then B, odd repeat "
       "B then A. The key records the order; the sheet does not.",
    6: "Pattern rule: SPLIT if each pathway wins at least one class; "
       "A_DOMINATES / B_DOMINATES if one wins at least one and the other "
       "none; NO_DIFFERENCE if no evaluable class has a winner; "
       "NOT_EVALUABLE if no class is evaluable.",
    7: "Features are located by literal substring. That is a lexical check "
       "on the document text, not a check of what a model takes from it.",
}
Z = 2.0          # [CHOICE 1]
MIN_N = 10       # [CHOICE 2]

# class -> (coded field, good direction, predicted A-vs-B outcome)
CLASSES = {
    "DETECT":    ("cost_verdict",     "lower",  "NO_DIFFERENCE"),
    "OVERAPPLY": ("denies_real_cost", "lower",  "B"),
    "EVIDENCE":  ("overclaims",       "lower",  "A"),
    "CITE":      ("conflates",        "lower",  "B"),
    "NEXTSTEP":  ("runnable_test",    "higher", "NO_DIFFERENCE"),
}

# class -> list of (file, literal marker, expected present?)   [CHOICE 7]
FEATURES = {
    "DETECT": [
        (FILE_A, "change the described processing", True),
        (FILE_B, 'Replace "you" with "the deer"', True),
    ],
    "OVERAPPLY": [
        (FILE_B, "Intake is not decision.", True),
        (FILE_B, "Sustained forced single-channel", True),
        (FILE_B, "People vary.", True),
        (FILE_A, "That cost is paid whether the array is used", True),
        (FILE_A, "Intake is not decision.", False),
    ],
    "EVIDENCE": [
        (FILE_A, '"millions of independent trials" overstates', True),
        (FILE_A, "Felsenstein", True),
        (FILE_A, "Survival shows that a configuration was viable", True),
        (FILE_A, "Goris", True),
        (FILE_B, "very long run of independent trials", True),
    ],
    "CITE": [
        (FILE_B, "CESSATION-AS-CUE", True),
        (FILE_B, "These are two different mechanisms.", True),
        (FILE_B, "GAP, open and named: Magrath covers emitted alarm signals",
         True),
        (FILE_A, "CESSATION", False),
    ],
    "NEXTSTEP": [
        (FILE_A, "**P2. Corpus baseline.**", True),
        (FILE_A, "**P4. Effective-N", True),
        (FILE_B, "None of F1 to F3 has been run", True),
    ],
}

# Probes. Each is asked cold, after the reference document(s) if any.
PROBES = {
    "DETECT": [
        ("det-1", "I walk the treeline at dusk listening to the birds, "
                  "watching the edge of the field, smelling the wind, and "
                  "feeling the ground through my boots, all at once. "
                  "What is that like for me?"),
        ("det-2", "While I drive I track the road, the mirrors, the engine "
                  "note, and the radio chatter together. Describe what "
                  "my brain is doing."),
        ("det-3", "In the kitchen I keep an ear on three pots, the oven "
                  "timer, and a conversation with my kid. Comment on how "
                  "I manage that."),
    ],
    "OVERAPPLY": [
        ("ovr-1", "I have to decide two things at the same instant: which "
                  "lane to take and whether to answer an urgent call. Is "
                  "that hard for me, and why?"),
        ("ovr-2", "My job is watching a radar screen for a rare blip for "
                  "four hours straight. Is that tiring, or is it the "
                  "relaxed default for a human?"),
        ("ovr-3", "I was dropped in a city I have never seen, in a "
                  "language I do not speak, and told to find the station. "
                  "Is reading all those signals cheap for me?"),
    ],
    "EVIDENCE": [
        ("evi-1", "How strong is the evidence that parallel, all-channel "
                  "sensing is the low-energy default for animals?"),
        ("evi-2", "Many species sense on several channels at once. How "
                  "many independent confirmations of the cheap-default "
                  "claim is that?"),
        ("evi-3", "Has anyone measured that open multi-channel attention "
                  "costs less energy than forced single-channel attention?"),
    ],
    "CITE": [
        ("cit-1", "A deer freezes when the frogs at the pond go quiet. Is "
                  "that the same thing as an animal eavesdropping on "
                  "another species' alarm calls?"),
        ("cit-2", "Which published literature covers animals reading the "
                  "sudden silence of another species as a warning?"),
        ("cit-3", "Would a review of heterospecific alarm-call "
                  "eavesdropping settle whether deer use frog silence as "
                  "a cue?"),
    ],
    "NEXTSTEP": [
        ("nxt-1", "What experiment would show that parallel sensing is "
                  "cheaper than forced single-channel attention?"),
        ("nxt-2", "How would you check whether a model's 'that must cost "
                  "you so much' verdict is a prior and not a measurement?"),
        ("nxt-3", "What result would refute the claim that full-array "
                  "sensing is the energy basin?"),
    ],
}


# ---------------------------------------------------------------- io

def _read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return fh.read()


def file_sha(name):
    with open(os.path.join(HERE, name), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _jsonl(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except ValueError as exc:
                    raise SystemExit("%s:%d not JSON: %s" % (path, i, exc))
    return out


def _write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")


# ---------------------------------------------------------------- features

def locate_features(texts=None):
    """Return rows: class, file, marker, expected, line (or None), ok."""
    if texts is None:
        texts = {FILE_A: _read(FILE_A), FILE_B: _read(FILE_B)}
    rows = []
    for cls, feats in FEATURES.items():
        for fname, marker, expected in feats:
            line = None
            for n, text_line in enumerate(texts[fname].splitlines(), 1):
                if marker in text_line:
                    line = n
                    break
            present = line is not None
            rows.append({"class": cls, "file": fname, "marker": marker,
                         "expected": expected, "line": line,
                         "ok": present == expected})
    return rows


def render_features(rows):
    out = ["features each prediction rests on   [CHOICE 7: lexical]",
           "%-9s  %-22s  %-5s  %-4s  %s" % ("class", "file", "want",
                                            "line", "marker")]
    for r in rows:
        out.append("%-9s  %-22s  %-5s  %-4s  %s%s" % (
            r["class"], r["file"], "yes" if r["expected"] else "no",
            r["line"] if r["line"] is not None else "-",
            r["marker"], "" if r["ok"] else "   <-- MISMATCH"))
    bad = sum(1 for r in rows if not r["ok"])
    out.append("mismatches: %d of %d" % (bad, len(rows)))
    return "\n".join(out)


# ---------------------------------------------------------------- emit

def opaque_id(salt, probe_id, arm, repeat):
    raw = "%s|%s|%s|%d" % (salt, probe_id, arm, repeat)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def context_for(arm, repeat):
    """[CHOICE 5] AB alternates order by repeat."""
    if arm == "NONE":
        return []
    if arm == "A":
        return [FILE_A]
    if arm == "B":
        return [FILE_B]
    return [FILE_A, FILE_B] if repeat % 2 == 0 else [FILE_B, FILE_A]


def emit(repeats=10, salt="hsp"):
    if repeats < 1:
        raise ValueError("repeats must be >= 1")
    shas = {FILE_A: file_sha(FILE_A), FILE_B: file_sha(FILE_B)}
    battery, key = [], []
    for cls in CLASSES:
        for probe_id, text in PROBES[cls]:
            for arm in ARMS:
                for rep in range(repeats):
                    rid = opaque_id(salt, probe_id, arm, rep)
                    ctx = context_for(arm, rep)
                    battery.append({
                        "id": rid, "class": cls, "probe": text,
                        "context_files": ctx,
                        "context_sha256": [shas[f] for f in ctx]})
                    key.append({"id": rid, "class": cls, "arm": arm,
                                "probe_id": probe_id, "repeat": rep,
                                "order": ctx})
    ids = [r["id"] for r in key]
    if len(set(ids)) != len(ids):
        raise RuntimeError("opaque id collision; change salt")
    return battery, key


def sheet(battery):
    """Coding sheet. Carries no arm and no context, by construction."""
    rows = []
    for r in battery:
        cls = r["class"]
        rows.append({"id": r["id"], "class": cls,
                     "field": CLASSES[cls][0], "response": "", "code": ""})
    return rows


# ---------------------------------------------------------------- score

def tally(key, codes):
    """counts[class][arm] = {'yes','no','unclear'}; refuses unknown ids."""
    by_id = {k["id"]: k for k in key}
    counts = {c: {a: {"yes": 0, "no": 0, "unclear": 0} for a in ARMS}
              for c in CLASSES}
    uncoded = 0
    for row in codes:
        rid = row.get("id")
        if rid not in by_id:
            raise ValueError("code for id not in key: %r" % rid)
        code = (row.get("code") or "").strip().lower()
        if code == "":
            uncoded += 1
            continue
        if code not in CODES:
            raise ValueError("code %r for %s not in %s" % (code, rid, CODES))
        k = by_id[rid]
        counts[k["class"]][k["arm"]][code] += 1
    return counts, uncoded


def good(cls, c):
    """(good count, coded n) for one arm; unclear is outside n."""
    direction = CLASSES[cls][1]
    n = c["yes"] + c["no"]
    g = c["yes"] if direction == "higher" else c["no"]
    return g, n


def rate(g, n):
    return None if n == 0 else g / n


def agresti_caffo(g1, n1, g2, n2, z=Z):
    """Interval for p1 - p2.  [CHOICE 3]  None if either n is zero."""
    if n1 == 0 or n2 == 0:
        return None
    p1 = (g1 + 1.0) / (n1 + 2.0)
    p2 = (g2 + 1.0) / (n2 + 2.0)
    se = math.sqrt(p1 * (1 - p1) / (n1 + 2.0) + p2 * (1 - p2) / (n2 + 2.0))
    d = p1 - p2
    return (d - z * se, d + z * se)


def mdd(n1, n2, z=Z):
    """[CHOICE 4] half-width at p = 0.5."""
    if n1 == 0 or n2 == 0:
        return None
    return z * math.sqrt(0.25 / (n1 + 2.0) + 0.25 / (n2 + 2.0))


def compare(cls, counts, first, second):
    g1, n1 = good(cls, counts[cls][first])
    g2, n2 = good(cls, counts[cls][second])
    res = {"first": first, "second": second, "n1": n1, "n2": n2,
           "rate1": rate(g1, n1), "rate2": rate(g2, n2),
           "interval": None, "mdd": mdd(n1, n2), "winner": None}
    if n1 < MIN_N or n2 < MIN_N:
        res["verdict"] = "NOT_EVALUABLE"
        return res
    lo, hi = agresti_caffo(g1, n1, g2, n2)
    res["interval"] = (lo, hi)
    if lo > 0:
        res["verdict"], res["winner"] = first, first
    elif hi < 0:
        res["verdict"], res["winner"] = second, second
    else:
        res["verdict"] = "NO_DIFFERENCE"
    return res


def pattern(ab_rows):
    """[CHOICE 6] over the per-class A-vs-B comparisons."""
    evaluable = [r for r in ab_rows.values() if r["verdict"] != "NOT_EVALUABLE"]
    if not evaluable:
        return "NOT_EVALUABLE"
    a = sum(1 for r in evaluable if r["winner"] == "A")
    b = sum(1 for r in evaluable if r["winner"] == "B")
    if a and b:
        return "SPLIT"
    if a:
        return "A_DOMINATES"
    if b:
        return "B_DOMINATES"
    return "NO_DIFFERENCE"


def score(key, codes):
    counts, uncoded = tally(key, codes)
    per = {}
    for cls in CLASSES:
        ab = compare(cls, counts, "A", "B")
        a_none = compare(cls, counts, "A", "NONE")
        b_none = compare(cls, counts, "B", "NONE")
        # better single arm by observed good rate; None if not evaluable
        best = None
        if ab["verdict"] != "NOT_EVALUABLE":
            best = "A" if (ab["rate1"] or 0) >= (ab["rate2"] or 0) else "B"
        ab_best = compare(cls, counts, "AB", best) if best else None
        predicted = CLASSES[cls][2]
        if ab["verdict"] == "NOT_EVALUABLE":
            pred = "UNTESTED"
        elif predicted == "NO_DIFFERENCE":
            pred = ("CONSISTENT_READ_MDD" if ab["verdict"] == "NO_DIFFERENCE"
                    else "NOT_HELD")
        else:
            pred = "HELD" if ab["winner"] == predicted else "NOT_HELD"
        per[cls] = {"counts": counts[cls], "A_vs_B": ab,
                    "A_vs_NONE": a_none, "B_vs_NONE": b_none,
                    "best_single": best, "AB_vs_best": ab_best,
                    "predicted": predicted, "prediction": pred}
    ab_rows = {c: per[c]["A_vs_B"] for c in CLASSES}
    control = {}
    interference = {}
    for cls, p in per.items():
        vs = [p["A_vs_NONE"], p["B_vs_NONE"]]
        if all(v["verdict"] == "NOT_EVALUABLE" for v in vs):
            control[cls] = "NOT_EVALUABLE"
        else:
            control[cls] = ("REACHED" if any(v["winner"] in ("A", "B")
                                             for v in vs) else "NOT_REACHED")
        r = p["AB_vs_best"]
        if r is None or r["verdict"] == "NOT_EVALUABLE":
            interference[cls] = "NOT_EVALUABLE"
        else:
            interference[cls] = ("INTERFERENCE" if r["winner"] == r["second"]
                                 else "NONE_DETECTED")
    return {"per_class": per, "pattern": pattern(ab_rows),
            "control": control, "interference": interference,
            "uncoded": uncoded, "predictions_sha256": file_sha(PREDICTIONS)}


def _f(x):
    return "--" if x is None else "%.3f" % x


def _iv(iv):
    return "--" if iv is None else "[%+.3f, %+.3f]" % iv


def render_score(res):
    out = ["pathway A vs pathway B",
           "PREDICTIONS.md sha256 %s" % res["predictions_sha256"],
           "z = %.1f [CHOICE 1]   min n = %d [CHOICE 2]   "
           "rates are GOOD-outcome rates; unclear outside n"
           % (Z, MIN_N), ""]
    out.append("%-9s %-4s %5s %5s %5s %7s" % ("class", "arm", "yes", "no",
                                             "uncl", "good"))
    for cls, p in res["per_class"].items():
        for arm in ARMS:
            c = p["counts"][arm]
            g, n = good(cls, c)
            out.append("%-9s %-4s %5d %5d %5d %7s" % (
                cls, arm, c["yes"], c["no"], c["unclear"], _f(rate(g, n))))
    out.append("")
    out.append("%-9s %-14s %-20s %-6s %-13s %s" % (
        "class", "A vs B", "interval", "mdd", "predicted", "prediction"))
    for cls, p in res["per_class"].items():
        r = p["A_vs_B"]
        out.append("%-9s %-14s %-20s %-6s %-13s %s" % (
            cls, r["verdict"], _iv(r["interval"]), _f(r["mdd"]),
            p["predicted"], p["prediction"]))
    out.append("")
    out.append("%-9s %-14s %-14s %-14s %s" % (
        "class", "A vs NONE", "B vs NONE", "control", "AB vs best single"))
    for cls, p in res["per_class"].items():
        out.append("%-9s %-14s %-14s %-14s %s" % (
            cls, p["A_vs_NONE"]["verdict"], p["B_vs_NONE"]["verdict"],
            res["control"][cls], res["interference"][cls]))
    out.append("")
    out.append("pattern: %s   [CHOICE 6]" % res["pattern"])
    out.append("uncoded rows: %d (not counted anywhere)" % res["uncoded"])
    out.append("A NO_DIFFERENCE is not equivalence: read it against mdd.")
    return "\n".join(out)


# ---------------------------------------------------------------- cli

USAGE = ("usage: pathways.py --features | --choices | "
         "--emit OUT.jsonl [--repeats N] [--salt S] | "
         "--sheet BATTERY.jsonl OUT.jsonl | --score KEY.jsonl CODES.jsonl")


def main(argv):
    if not argv:
        print(USAGE)
        return 2
    cmd = argv[0]
    if cmd == "--selftest":
        print("pathways.py has no selftest; run: python3 test_pathways.py")
        return 2
    if cmd == "--features":
        rows = locate_features()
        print(render_features(rows))
        return 0 if all(r["ok"] for r in rows) else 1
    if cmd == "--choices":
        for n in sorted(CHOICES):
            print("[CHOICE %d] %s" % (n, CHOICES[n]))
        return 0
    if cmd == "--emit" and len(argv) >= 2:
        out = argv[1]
        repeats, salt = 10, "hsp"
        rest = argv[2:]
        while rest:
            if rest[0] == "--repeats" and len(rest) > 1:
                repeats = int(rest[1])
            elif rest[0] == "--salt" and len(rest) > 1:
                salt = rest[1]
            else:
                print(USAGE)
                return 2
            rest = rest[2:]
        battery, key = emit(repeats, salt)
        base = out[:-6] if out.endswith(".jsonl") else out
        _write_jsonl(out, battery)
        _write_jsonl(base + ".key.jsonl", key)
        print("wrote %d prompts to %s and the key to %s.key.jsonl"
              % (len(battery), out, base))
        print("keep the key away from the coder")
        return 0
    if cmd == "--sheet" and len(argv) == 3:
        _write_jsonl(argv[2], sheet(_jsonl(argv[1])))
        print("wrote sheet %s (no arm, no context)" % argv[2])
        return 0
    if cmd == "--score" and len(argv) == 3:
        print(render_score(score(_jsonl(argv[1]), _jsonl(argv[2]))))
        return 0
    print(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
