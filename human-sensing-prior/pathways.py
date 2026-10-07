"""pathways.py -- pathway A vs pathway B, per problem class.

CC0 1.0 Universal. Stdlib only. Python >= 3.9.

Two documents carry the same correction in two shapes:

    A   human-sensing-prior.md   (convergence, effective-N, P1-P4)
    B   PATHWAY_B.md             (cessation-as-cue, scope limits, F1-F3)

The question is not which file is better. It is, per problem class, which
one moves a model's answer in the good direction more, and whether either
beats having no document. The predictions were committed to
PREDICTIONS.md BEFORE this file existed (7f780aa); AMENDMENT 1 was
appended before any run and fixes the decision rules this file applies.
Every report prints the hash of the original 6475-byte prefix and of the
whole file, so an edit after the fact is visible.

Commands
    --features            locate, by line, the feature each prediction rests on
    --choices             decisions PREDICTIONS.md did not fix
    --lengths             chars / words / APPROXIMATE tokens for A, B, A+B
    --emit OUT.jsonl --run-tag T [--repeats K] [--salt S]
                          probe battery (arms NONE / A / B / AB / BA, opaque
                          ids) and OUT.key.jsonl, the arm key, kept apart
    --prompt BATTERY.jsonl ID
                          the exact text to send for one id
    --sheet BATTERY.jsonl OUT.jsonl
                          coding sheet: id, run_tag, class, field, probe,
                          response, code, guess, coder.  No arm.
    --strip SHEET.jsonl OUT.jsonl LOG.jsonl
                          delete verbatim 8-word runs from A or B out of each
                          response; the log goes with the key, not the coder
    --score KEY.jsonl --manifest M.json [--strip-log LOG] CODES1 CODES2 [...]
                          at least two coder files

No model is called anywhere. The operator runs each prompt cold with one
fixed model and fixed settings, pastes the response into the sheet, strips
it, and coders who do not hold the key fill `code` and `guess`.

[CHOICE n] marks a decision PREDICTIONS.md did not fix. `--choices` prints
them.
"""

import hashlib
import importlib.util
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILE_A = "human-sensing-prior.md"
FILE_B = "PATHWAY_B.md"
PREDICTIONS = "PREDICTIONS.md"

# The registered original: first 6475 bytes of PREDICTIONS.md at 7f780aa.
ORIGINAL_LEN = 6475
ORIGINAL_SHA = ("5146b5f04a96cdc1ab284e92e39f6a28"
                "cef27c4178bd57a8322b8cac46cf6baf")

ARMS = ("NONE", "A", "B", "AB", "BA")
CODES = ("yes", "no", "unclear")
GUESSES = ARMS + ("unsure",)
DOCSET = {"NONE": "NONE", "A": "A", "B": "B", "AB": "BOTH", "BA": "BOTH"}
MANIFEST_FIELDS = ("run_tag", "model", "temperature", "top_p",
                   "max_tokens", "system_prompt", "date", "coders")

# Fixed by PREDICTIONS.md amendment 1.
DELTA = 0.15          # tie band on the GOOD-rate difference
K_MIN = 3             # responses per prompt per arm, floor
K_DEFAULT = 30
MIN_PROBES = 3
KAPPA_FLOOR = 0.60
STRIP_RUN = 8         # words
CHARS_PER_TOKEN = 4   # APPROXIMATE token estimate

CHOICES = {
    1: "Z = 2.0 for every interval (about 95%); no multiplicity correction "
       "across the five classes, so a single class win is read with that "
       "in mind.",
    2: "MIN_N = 10 coded (yes+no) responses per arm per class; below it a "
       "comparison is NOT_EVALUABLE.",
    3: "Difference interval is Agresti-Caffo (add one success and one "
       "failure to each arm) on the GOOD-outcome rate, so a positive "
       "difference always means the first arm did better.",
    4: "MDD is the interval half-width at p = 0.5 for the observed n: the "
       "smallest difference this n could have called, worst case.",
    5: "SUPERSEDED by amendment 1 item 4: AB and BA are separate arms.",
    6: "SUPERSEDED by amendment 1 item 2: pattern rule with TIE, "
       "LEADS_INCOMPLETE, ALL_TIE and UNRESOLVED.",
    7: "Features are located by literal substring. That is a lexical check "
       "on the document text, not a check of what a model takes from it.",
    8: "TIE is tested before a directional win: an interval inside the "
       "+-0.15 band that also excludes 0 reads TIE. The amendment states "
       "both rules and not their precedence; a tolerance that a win could "
       "override would not be a tolerance.",
    9: "Prompt template: 'Reference document N:' then the text between "
       "<<< and >>>, then 'Question: ' and the probe. No filename appears, "
       "so a response cannot echo one.",
    10: "Kappa is computed over the three-valued code (yes / no / unclear) "
        "on rows both coders coded; blank rows are left out. A class with "
        "no such rows has kappa undefined and is NOT_READABLE.",
    11: "Strip keeps the whitespace that preceded each kept word; the "
        "whitespace before a deleted run is dropped. A response with "
        "nothing deleted comes back byte-identical.",
    12: "The pooled interval treats rows as independent; probe clustering "
        "is not modelled. Between-probe SD is printed beside it.",
    13: "A kappa measured below the floor reads NOT_READABLE even when the "
        "disagreement left no consensus rows; with no jointly coded rows "
        "(kappa undefined) and no consensus data the class reads "
        "NOT_EVALUABLE. P-AB and P-CONTROL read UNTESTED when every "
        "comparison under them is NOT_EVALUABLE.",
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
        # FROZEN known defect under test, amendment 1 item 1.
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

# Cohen's kappa is imported from the repo's existing implementation, not
# copied, so the two cannot drift.
_ER_PATH = os.path.join(HERE, os.pardir, "effective-redundancy-audit",
                        "effective_redundancy.py")


def _load_kappa():
    spec = importlib.util.spec_from_file_location("effective_redundancy",
                                                  _ER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.cohen_kappa


cohen_kappa = _load_kappa()


# ---------------------------------------------------------------- io

def _read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return fh.read()


def file_sha(name):
    with open(os.path.join(HERE, name), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def predictions_status(data=None):
    """Original-prefix hash against the registered value, plus whole file."""
    if data is None:
        with open(os.path.join(HERE, PREDICTIONS), "rb") as fh:
            data = fh.read()
    prefix = hashlib.sha256(data[:ORIGINAL_LEN]).hexdigest()
    return {"prefix_sha256": prefix, "prefix_ok": prefix == ORIGINAL_SHA,
            "file_sha256": hashlib.sha256(data).hexdigest(),
            "amended": len(data) > ORIGINAL_LEN}


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
    out.append("B 'very long run of independent trials' is FROZEN as a "
               "known defect under test (PREDICTIONS.md amendment 1).")
    return "\n".join(out)


# ---------------------------------------------------------------- prompts

def context_for(arm):
    return {"NONE": [], "A": [FILE_A], "B": [FILE_B],
            "AB": [FILE_A, FILE_B], "BA": [FILE_B, FILE_A]}[arm]


def _context_block(texts):
    """[CHOICE 9] neutral headers, no filenames."""
    parts = []
    for i, t in enumerate(texts, 1):
        parts.append("Reference document %d:\n<<<\n%s\n>>>\n" % (i, t))
    return "\n".join(parts)


def assemble(row, texts=None):
    """Exact prompt for one battery row. Refuses if a file changed."""
    files = row["context_files"]
    if texts is None:
        texts = {f: _read(f) for f in files}
    for f, want in zip(files, row["context_sha256"]):
        got = hashlib.sha256(texts[f].encode("utf-8")).hexdigest()
        if got != want:
            raise ValueError("%s changed since emit (sha256 %s, battery %s)"
                             % (f, got[:12], want[:12]))
    block = _context_block([texts[f] for f in files])
    return (block + "\n" if block else "") + "Question: " + row["probe"]


def _measure(text):
    return {"chars": len(text), "words": len(text.split()),
            "tokens_approx": int(round(len(text) / float(CHARS_PER_TOKEN)))}


def lengths(texts=None):
    if texts is None:
        texts = {FILE_A: _read(FILE_A), FILE_B: _read(FILE_B)}
    return {"A": _measure(_context_block([texts[FILE_A]])),
            "B": _measure(_context_block([texts[FILE_B]])),
            "A+B": _measure(_context_block([texts[FILE_A], texts[FILE_B]]))}


def render_lengths(L):
    out = ["context length per arm (assembled block, probe excluded)",
           "tokens are APPROXIMATE: chars / %d; no tokenizer or API key here"
           % CHARS_PER_TOKEN,
           "%-5s %8s %7s %14s" % ("arm", "chars", "words", "tokens_approx")]
    for k in ("A", "B", "A+B"):
        m = L[k]
        out.append("%-5s %8d %7d %14d" % (k, m["chars"], m["words"],
                                         m["tokens_approx"]))
    out.append("B / A length ratio: %.2f   A+B / max(A, B): %.2f" % (
        L["B"]["chars"] / float(L["A"]["chars"]),
        L["A+B"]["chars"] / float(max(L["A"]["chars"], L["B"]["chars"]))))
    out.append("A vs B and the combined arms are confounded with context "
               "length; read any win against these ratios.")
    return "\n".join(out)


# ---------------------------------------------------------------- emit

def opaque_id(salt, run_tag, probe_id, arm, repeat):
    raw = "%s|%s|%s|%s|%d" % (salt, run_tag, probe_id, arm, repeat)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def emit(repeats=K_DEFAULT, salt="hsp", run_tag="run"):
    if repeats < K_MIN:
        raise ValueError("repeats must be >= %d (amendment 1 item 3)" % K_MIN)
    if not run_tag:
        raise ValueError("run_tag required")
    shas = {FILE_A: file_sha(FILE_A), FILE_B: file_sha(FILE_B)}
    battery, key = [], []
    for cls in CLASSES:
        for probe_id, text in PROBES[cls]:
            for arm in ARMS:
                for rep in range(repeats):
                    rid = opaque_id(salt, run_tag, probe_id, arm, rep)
                    ctx = context_for(arm)
                    battery.append({
                        "id": rid, "run_tag": run_tag, "class": cls,
                        "probe": text, "context_files": ctx,
                        "context_sha256": [shas[f] for f in ctx]})
                    key.append({"id": rid, "run_tag": run_tag, "class": cls,
                                "arm": arm, "probe_id": probe_id,
                                "repeat": rep})
    ids = [r["id"] for r in key]
    if len(set(ids)) != len(ids):
        raise RuntimeError("opaque id collision; change salt")
    return battery, key


def sheet(battery):
    """Coding sheet. Carries no arm and no context, by construction."""
    rows = []
    for r in battery:
        cls = r["class"]
        rows.append({"id": r["id"], "run_tag": r["run_tag"], "class": cls,
                     "field": CLASSES[cls][0], "probe": r["probe"],
                     "response": "", "code": "", "guess": "", "coder": ""})
    return rows


# ---------------------------------------------------------------- strip

def _norm(tok):
    return re.sub(r"[^a-z0-9]", "", tok.lower())


def doc_grams(texts=None, run=STRIP_RUN):
    if texts is None:
        texts = [_read(FILE_A), _read(FILE_B)]
    grams = set()
    for t in texts:
        w = [x for x in (_norm(s) for s in t.split()) if x]
        for i in range(len(w) - run + 1):
            grams.add(tuple(w[i:i + run]))
    return grams


def strip_text(text, grams, run=STRIP_RUN):
    """Delete every verbatim run of `run`+ words found in grams. Silent:
    nothing marks the deletion.  [CHOICE 11]  Returns (text, removed)."""
    parts = re.split(r"(\s+)", text)
    toks = [(i, p) for i, p in enumerate(parts) if p and not p.isspace()]
    live = [(i, _norm(p)) for i, p in toks if _norm(p)]
    kill = set()
    for j in range(len(live) - run + 1):
        if tuple(n for _, n in live[j:j + run]) in grams:
            lo, hi = live[j][0], live[j + run - 1][0]
            kill.update(i for i, _ in toks if lo <= i <= hi)
    if not kill:
        return text, 0
    out, prev_sep = [], ""
    for i, p in enumerate(parts):
        if p == "" or p.isspace():
            prev_sep = p
            continue
        if i in kill:
            prev_sep = ""
            continue
        out.append(prev_sep + p)
        prev_sep = ""
    out.append(prev_sep)
    return "".join(out), len(kill)


def strip_sheet(rows, grams=None):
    if grams is None:
        grams = doc_grams()
    out, log = [], []
    for r in rows:
        text, n = strip_text(r.get("response", ""), grams)
        nr = dict(r)
        nr["response"] = text
        out.append(nr)
        log.append({"id": r["id"], "run_tag": r.get("run_tag"),
                    "words_removed": n})
    return out, log


# ---------------------------------------------------------------- arithmetic

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


def agresti_coull_lower(x, n, z=Z):
    if n == 0:
        return None
    nt = n + z * z
    pt = (x + z * z / 2.0) / nt
    return pt - z * math.sqrt(pt * (1 - pt) / nt)


def mdd(n1, n2, z=Z):
    """[CHOICE 4] half-width at p = 0.5."""
    if n1 == 0 or n2 == 0:
        return None
    return z * math.sqrt(0.25 / (n1 + 2.0) + 0.25 / (n2 + 2.0))


def _zero():
    return {"yes": 0, "no": 0, "unclear": 0}


# ---------------------------------------------------------------- tally

def check_manifest(m):
    missing = [f for f in MANIFEST_FIELDS
               if f not in m or m[f] is None or m[f] == ""]
    if missing:
        raise ValueError("manifest missing: %s" % ", ".join(missing))
    coders = m["coders"]
    if not isinstance(coders, list) or len(coders) < 2:
        raise ValueError("manifest coders: at least 2 required")
    ids = []
    for c in coders:
        if not isinstance(c, dict) or not c.get("id") or \
                not isinstance(c.get("same_model_class"), bool):
            raise ValueError("each coder needs id and same_model_class "
                             "(true/false): %r" % (c,))
        ids.append(c["id"])
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate coder id in manifest")
    return m


def _coder_of(rows, path_label):
    names = set((r.get("coder") or "").strip() for r in rows
                if (r.get("code") or "").strip())
    if len(names) > 1:
        raise ValueError("%s: more than one coder in one file: %s"
                         % (path_label, sorted(names)))
    if "" in names:
        raise ValueError("%s: a coded row has no coder" % path_label)
    return names.pop() if names else None


def tally(key, rows):
    """counts[class][arm], probe[class][arm][probe_id]; refuses unknown ids
    and codes or guesses outside their sets. Blank code = uncoded."""
    by_id = {k["id"]: k for k in key}
    counts = {c: {a: _zero() for a in ARMS} for c in CLASSES}
    probe = {c: {a: {} for a in ARMS} for c in CLASSES}
    uncoded = 0
    for row in rows:
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
        p = probe[k["class"]][k["arm"]].setdefault(k["probe_id"], _zero())
        p[code] += 1
    return counts, probe, uncoded


def compare(cls, counts, probe, first, second):
    g1, n1 = good(cls, counts[cls][first])
    g2, n2 = good(cls, counts[cls][second])
    res = {"first": first, "second": second, "n1": n1, "n2": n2,
           "rate1": rate(g1, n1), "rate2": rate(g2, n2),
           "interval": None, "mdd": mdd(n1, n2), "winner": None,
           "reason": ""}
    elig = []
    for pid in sorted(set(probe[cls][first]) & set(probe[cls][second])):
        pg1, pn1 = good(cls, probe[cls][first][pid])
        pg2, pn2 = good(cls, probe[cls][second][pid])
        if pn1 >= K_MIN and pn2 >= K_MIN:
            elig.append(pg1 / float(pn1) - pg2 / float(pn2))
    res["probes"] = len(elig)
    if n1 < MIN_N or n2 < MIN_N:
        res["verdict"], res["reason"] = "NOT_EVALUABLE", "n below %d" % MIN_N
        return res
    if len(elig) < MIN_PROBES:
        res["verdict"] = "NOT_EVALUABLE"
        res["reason"] = "%d probes with >= %d coded per arm" % (len(elig),
                                                                 K_MIN)
        return res
    lo, hi = agresti_caffo(g1, n1, g2, n2)
    res["interval"] = (lo, hi)
    if lo >= -DELTA and hi <= DELTA:                     # [CHOICE 8]
        res["verdict"] = "TIE"
    elif lo > 0 or hi < 0:
        sign = 1 if lo > 0 else -1
        agree = sum(1 for d in elig if (d > 0 if sign > 0 else d < 0))
        if 2 * agree > len(elig):
            res["winner"] = first if sign > 0 else second
            res["verdict"] = res["winner"]
        else:
            res["verdict"] = "UNRESOLVED"
            res["reason"] = "probe majority %d of %d" % (agree, len(elig))
    else:
        res["verdict"] = "UNRESOLVED"
        res["reason"] = "interval leaves the tie band"
    return res


def spread(cls, probe):
    """Per arm: per-probe GOOD rates, between-probe SD, mean p(1-p)."""
    out = {}
    for arm in ARMS:
        rates = []
        for pid in sorted(probe[cls][arm]):
            g, n = good(cls, probe[cls][arm][pid])
            if n:
                rates.append(g / float(n))
        sd = None
        if len(rates) >= 2:
            m = sum(rates) / len(rates)
            sd = math.sqrt(sum((r - m) ** 2 for r in rates) / (len(rates) - 1))
        within = (sum(r * (1 - r) for r in rates) / len(rates)
                  if rates else None)
        out[arm] = {"probe_rates": rates, "between_sd": sd,
                    "within_var": within}
    return out


# ---------------------------------------------------------------- coders

def consensus(coder_rows):
    """Rows all coders coded identically. Returns rows, disputed, incomplete."""
    maps = [{r["id"]: (r.get("code") or "").strip().lower() for r in rows}
            for rows in coder_rows]
    ids = set()
    for m in maps:
        ids |= set(m)
    rows, disputed, incomplete = [], 0, 0
    for rid in sorted(ids):
        codes = [m.get(rid, "") for m in maps]
        if any(c == "" for c in codes):
            incomplete += 1
        elif len(set(codes)) > 1:
            disputed += 1
        else:
            rows.append({"id": rid, "code": codes[0]})
    return rows, disputed, incomplete


def agreement(key, coder_rows, names):
    """Per class: min pairwise kappa and the percent agreement of that
    pair, over rows both coded.  [CHOICE 10]"""
    by_id = {k["id"]: k for k in key}
    maps = [{r["id"]: (r.get("code") or "").strip().lower() for r in rows}
            for rows in coder_rows]
    out = {}
    for cls in CLASSES:
        pairs = []
        for i in range(len(maps)):
            for j in range(i + 1, len(maps)):
                ids = [x for x in maps[i]
                       if x in by_id and by_id[x]["class"] == cls and
                       maps[i][x] and maps[j].get(x)]
                c1 = [maps[i][x] for x in ids]
                c2 = [maps[j][x] for x in ids]
                if ids:
                    k = cohen_kappa(c1, c2)
                    pa = sum(1 for a, b in zip(c1, c2) if a == b) / len(ids)
                else:
                    k, pa = None, None
                pairs.append({"pair": (names[i], names[j]), "n": len(ids),
                              "kappa": k, "agreement": pa})
        worst = None
        for p in pairs:
            if p["kappa"] is None:
                worst = p
                break
            if worst is None or p["kappa"] < worst["kappa"]:
                worst = p
        readable = worst is not None and worst["kappa"] is not None and \
            worst["kappa"] >= KAPPA_FLOOR
        out[cls] = {"pairs": pairs, "min": worst, "readable": readable}
    return out


def leak(key, rows):
    """Guess accuracy for one coder, exact arm and document set."""
    by_id = {k["id"]: k for k in key}
    unrecorded, unsure, committed = 0, 0, []
    for r in rows:
        if not (r.get("code") or "").strip():
            continue
        g = (r.get("guess") or "").strip()
        if g == "":
            unrecorded += 1
            continue
        if g not in GUESSES:
            raise ValueError("guess %r for %s not in %s" % (g, r["id"],
                                                            GUESSES))
        if g == "unsure":
            unsure += 1
            continue
        committed.append((g, by_id[r["id"]]["arm"]))
    res = {"unrecorded": unrecorded, "unsure": unsure, "n": len(committed)}
    for grain, fn in (("exact", lambda a: a), ("docset", lambda a: DOCSET[a])):
        n = len(committed)
        x = sum(1 for g, a in committed if fn(g) == fn(a))
        shares = {}
        for _, a in committed:
            shares[fn(a)] = shares.get(fn(a), 0) + 1
        chance = max(shares.values()) / float(n) if n else None
        lo = agresti_coull_lower(x, n)
        if n < MIN_N:
            verdict = "NOT_EVALUABLE"
        else:
            verdict = "LEAK_DETECTED" if lo > chance else "NO_LEAK_DETECTED"
        res[grain] = {"accuracy": rate(x, n), "chance": chance,
                      "lower": lo, "verdict": verdict}
    return res


# ---------------------------------------------------------------- score

def _prediction(predicted, verdict):
    if verdict in ("UNRESOLVED", "NOT_EVALUABLE", "NOT_READABLE"):
        return verdict
    if predicted == "NO_DIFFERENCE":
        return "HELD" if verdict == "TIE" else "NOT_HELD"
    return "HELD" if verdict == predicted else "NOT_HELD"


def pattern(verdicts):
    """Amendment 1 item 2, over the per-class A-vs-B verdicts."""
    v = list(verdicts.values())
    a = sum(1 for x in v if x == "A")
    b = sum(1 for x in v if x == "B")
    resolved = all(x in ("A", "B", "TIE") for x in v)
    if a and b:
        return "SPLIT"
    if a:
        return "A_DOMINATES" if resolved else "A_LEADS_INCOMPLETE"
    if b:
        return "B_DOMINATES" if resolved else "B_LEADS_INCOMPLETE"
    if all(x == "TIE" for x in v):
        return "ALL_TIE"
    if all(x in ("NOT_EVALUABLE", "NOT_READABLE") for x in v):
        return "NOT_EVALUABLE"
    return "UNRESOLVED"


def _ab_verdicts(key, rows):
    counts, probe, _ = tally(key, rows)
    return {c: compare(c, counts, probe, "A", "B")["verdict"]
            for c in CLASSES}


def score(key, coder_rows, manifest, strip_log=None):
    check_manifest(manifest)
    tag = manifest["run_tag"]
    if len(coder_rows) < 2:
        raise ValueError("at least 2 coder files required")
    bad_key = [k["id"] for k in key if k.get("run_tag") != tag]
    if bad_key:
        raise ValueError("%d key rows not from run %r" % (len(bad_key), tag))
    names = []
    for i, rows in enumerate(coder_rows):
        bad = [r.get("id") for r in rows if r.get("run_tag") != tag]
        if bad:
            raise ValueError("coder file %d: %d rows not from run %r"
                             % (i + 1, len(bad), tag))
        names.append(_coder_of(rows, "coder file %d" % (i + 1))
                     or "coder-%d" % (i + 1))
    if len(set(names)) != len(names):
        raise ValueError("two coder files carry the same coder id")
    declared = {c["id"]: c for c in manifest["coders"]}
    for n in names:
        if not n.startswith("coder-") and n not in declared:
            raise ValueError("coder %r not declared in manifest" % n)
    for rows in coder_rows:
        tally(key, rows)                      # validates ids and codes

    cons, disputed, incomplete = consensus(coder_rows)
    counts, probe, _ = tally(key, cons)
    agree = agreement(key, coder_rows, names)

    per = {}
    for cls in CLASSES:
        ab = compare(cls, counts, probe, "A", "B")
        # [CHOICE 13] A kappa measured below the floor is NOT_READABLE even when the
        # disagreement emptied the consensus; with no jointly coded rows
        # (kappa undefined) and no consensus data, NOT_EVALUABLE.
        worst = agree[cls]["min"]
        verdict = ab["verdict"]
        if worst is not None and worst["kappa"] is not None and \
                worst["kappa"] < KAPPA_FLOOR:
            verdict = "NOT_READABLE"
        elif verdict != "NOT_EVALUABLE" and not agree[cls]["readable"]:
            verdict = "NOT_READABLE"
        a_none = compare(cls, counts, probe, "A", "NONE")
        b_none = compare(cls, counts, probe, "B", "NONE")
        order = compare(cls, counts, probe, "AB", "BA")
        best = None
        if ab["rate1"] is not None and ab["rate2"] is not None:
            best = "A" if ab["rate1"] >= ab["rate2"] else "B"
        combined = {}
        for arm in ("AB", "BA"):
            if best is None:
                combined[arm] = "NOT_EVALUABLE"
                continue
            r = compare(cls, counts, probe, arm, best)
            if r["verdict"] == "NOT_EVALUABLE":
                combined[arm] = "NOT_EVALUABLE"
            elif r["winner"] == best:
                combined[arm] = "INTERFERENCE"
            elif r["verdict"] == "UNRESOLVED":
                combined[arm] = "UNRESOLVED"
            else:
                combined[arm] = "NONE_DETECTED"
        vs = [a_none, b_none]
        if any(v["winner"] in ("A", "B") for v in vs):
            control = "REACHED"
        elif all(v["verdict"] == "NOT_EVALUABLE" for v in vs):
            control = "NOT_EVALUABLE"
        elif all(v["verdict"] in ("TIE", "NONE") for v in vs):
            control = "NOT_REACHED"
        else:
            control = "UNRESOLVED"
        predicted = CLASSES[cls][2]
        per[cls] = {"counts": counts[cls], "A_vs_B": ab, "verdict": verdict,
                    "A_vs_NONE": a_none, "B_vs_NONE": b_none,
                    "order": order, "best_single": best,
                    "combined": combined, "control": control,
                    "spread": spread(cls, probe),
                    "predicted": predicted,
                    "prediction": _prediction(predicted, verdict),
                    "agreement": agree[cls]}

    verdicts = {c: per[c]["verdict"] for c in CLASSES}
    pat = pattern(verdicts)

    def _all(field, good_value, bad_value):
        vals = [x for c in CLASSES for x in
                (per[c][field].values() if isinstance(per[c][field], dict)
                 else [per[c][field]])]
        if all(v == "NOT_EVALUABLE" for v in vals):
            return "UNTESTED"
        if any(v == bad_value for v in vals):
            return "NOT_HELD"
        if all(v == good_value for v in vals):
            return "HELD"
        return "UNRESOLVED"

    patterns = {
        "P-SPLIT": ("HELD" if pat == "SPLIT" else
                    "UNTESTED" if pat == "NOT_EVALUABLE" else
                    "UNRESOLVED" if pat in ("UNRESOLVED",
                                            "A_LEADS_INCOMPLETE",
                                            "B_LEADS_INCOMPLETE")
                    else "NOT_HELD"),
        "P-AB": _all("combined", "NONE_DETECTED", "INTERFERENCE"),
        "P-CONTROL": _all("control", "REACHED", "NOT_REACHED"),
    }
    per_coder = {n: _ab_verdicts(key, rows)
                 for n, rows in zip(names, coder_rows)}
    leaks = {n: leak(key, rows) for n, rows in zip(names, coder_rows)}

    stripped = None
    if strip_log is not None:
        by_id = {k["id"]: k for k in key}
        stripped = {a: {"rows": 0, "words": 0} for a in ARMS}
        for r in strip_log:
            if r["id"] in by_id:
                s = stripped[by_id[r["id"]]["arm"]]
                s["rows"] += 1 if r["words_removed"] else 0
                s["words"] += r["words_removed"]

    return {"per_class": per, "pattern": pat, "patterns": patterns,
            "per_coder": per_coder, "leak": leaks, "coders": names,
            "same_class": [n for n in names
                           if declared.get(n, {}).get("same_model_class")],
            "disputed": disputed, "incomplete": incomplete,
            "manifest": manifest, "stripped": stripped,
            "predictions": predictions_status(), "lengths": lengths()}


# ---------------------------------------------------------------- render

def _f(x):
    return "--" if x is None else "%.3f" % x


def _iv(iv):
    return "--" if iv is None else "[%+.3f, %+.3f]" % iv


def render_score(res):
    ps = res["predictions"]
    m = res["manifest"]
    out = ["pathway A vs pathway B",
           "PREDICTIONS.md original prefix (%d bytes) sha256 %s  %s"
           % (ORIGINAL_LEN, ps["prefix_sha256"],
              "OK" if ps["prefix_ok"] else "MISMATCH: ORIGINAL EDITED"),
           "PREDICTIONS.md whole file sha256 %s%s"
           % (ps["file_sha256"], "  (amended)" if ps["amended"] else ""),
           "run %s   model %s   temperature %s   top_p %s   max_tokens %s"
           % (m["run_tag"], m["model"], m["temperature"], m["top_p"],
              m["max_tokens"]),
           "date %s   system_prompt %r" % (m["date"], m["system_prompt"]),
           "z = %.1f [CHOICE 1]   min n = %d [CHOICE 2]   tie band +-%.2f   "
           "k >= %d   min probes %d   kappa floor %.2f"
           % (Z, MIN_N, DELTA, K_MIN, MIN_PROBES, KAPPA_FLOOR),
           "rates are GOOD-outcome rates on consensus rows; unclear outside n",
           "coders: %s   disputed rows: %d   incomplete rows: %d"
           % (", ".join(res["coders"]), res["disputed"], res["incomplete"])]
    if res["same_class"]:
        out.append("same model class as the authors: %s -- agreement with "
                   "such a coder bounds reliability, it does not certify it"
                   % ", ".join(res["same_class"]))
    out.append("")
    out.append("%-9s %-4s %5s %5s %5s %7s  %-22s %8s %8s" % (
        "class", "arm", "yes", "no", "uncl", "good", "per-probe good",
        "btw sd", "within"))
    for cls, p in res["per_class"].items():
        for arm in ARMS:
            c = p["counts"][arm]
            g, n = good(cls, c)
            s = p["spread"][arm]
            pr = ",".join("%.2f" % r for r in s["probe_rates"]) or "--"
            out.append("%-9s %-4s %5d %5d %5d %7s  %-22s %8s %8s" % (
                cls, arm, c["yes"], c["no"], c["unclear"], _f(rate(g, n)),
                pr, _f(s["between_sd"]), _f(s["within_var"])))
    out.append("")
    out.append("%-9s %-7s %-6s %-14s %-20s %-6s %-13s %s" % (
        "class", "kappa", "agree", "A vs B", "interval", "mdd",
        "predicted", "prediction"))
    for cls, p in res["per_class"].items():
        r, a = p["A_vs_B"], p["agreement"]["min"]
        out.append("%-9s %-7s %-6s %-14s %-20s %-6s %-13s %s%s" % (
            cls, _f(a["kappa"] if a else None),
            _f(a["agreement"] if a else None), p["verdict"],
            _iv(r["interval"]), _f(r["mdd"]), p["predicted"],
            p["prediction"], ("  (%s)" % r["reason"]) if r["reason"] else ""))
    out.append("")
    out.append("%-9s %-14s %-14s %-12s %-14s %-14s %s" % (
        "class", "A vs NONE", "B vs NONE", "control", "AB vs best",
        "BA vs best", "AB vs BA (order)"))
    for cls, p in res["per_class"].items():
        out.append("%-9s %-14s %-14s %-12s %-14s %-14s %s" % (
            cls, p["A_vs_NONE"]["verdict"], p["B_vs_NONE"]["verdict"],
            p["control"], p["combined"]["AB"], p["combined"]["BA"],
            p["order"]["verdict"]))
    out.append("order effect is reported, not predicted")
    out.append("")
    out.append("pattern: %s" % res["pattern"])
    for k in ("P-SPLIT", "P-AB", "P-CONTROL"):
        out.append("%-10s %s" % (k, res["patterns"][k]))
    out.append("")
    out.append("per-coder A vs B (not gated by kappa)")
    for n, v in res["per_coder"].items():
        out.append("  %-12s %s" % (n, "  ".join("%s=%s" % (c, v[c])
                                              for c in CLASSES)))
    out.append("")
    out.append("leakage: guessed condition vs true arm, committed guesses "
               "only; chance = largest true share")
    out.append("  %-12s %4s %6s %6s  %-34s %s" % (
        "coder", "n", "unsure", "unrec", "exact acc/chance/lower verdict",
        "docset acc/chance/lower verdict"))
    for n, L in res["leak"].items():
        e, d = L["exact"], L["docset"]
        out.append("  %-12s %4d %6d %6d  %s/%s/%s %-14s %s/%s/%s %s" % (
            n, L["n"], L["unsure"], L["unrecorded"],
            _f(e["accuracy"]), _f(e["chance"]), _f(e["lower"]), e["verdict"],
            _f(d["accuracy"]), _f(d["chance"]), _f(d["lower"]),
            d["verdict"]))
    if res["stripped"] is not None:
        out.append("")
        out.append("strip log: rows touched / words removed per arm")
        out.append("  " + "  ".join("%s %d/%d" % (a, s["rows"], s["words"])
                                    for a, s in res["stripped"].items()))
    L = res["lengths"]
    out.append("")
    out.append("context chars A %d, B %d, A+B %d; tokens APPROXIMATE "
               "(chars/%d) A %d, B %d, A+B %d; wins are confounded with "
               "length" % (L["A"]["chars"], L["B"]["chars"],
                           L["A+B"]["chars"], CHARS_PER_TOKEN,
                           L["A"]["tokens_approx"], L["B"]["tokens_approx"],
                           L["A+B"]["tokens_approx"]))
    out.append("TIE means the interval lies inside the band; UNRESOLVED is "
               "not equivalence.")
    return "\n".join(out)


# ---------------------------------------------------------------- cli

USAGE = ("usage: pathways.py --features | --choices | --lengths | "
         "--emit OUT.jsonl --run-tag T [--repeats K] [--salt S] | "
         "--prompt BATTERY.jsonl ID | --sheet BATTERY.jsonl OUT.jsonl | "
         "--strip SHEET.jsonl OUT.jsonl LOG.jsonl | "
         "--score KEY.jsonl --manifest M.json [--strip-log LOG.jsonl] "
         "CODES1.jsonl CODES2.jsonl [...]")


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
    if cmd == "--lengths":
        print(render_lengths(lengths()))
        return 0
    if cmd == "--emit" and len(argv) >= 2:
        out = argv[1]
        repeats, salt, tag = K_DEFAULT, "hsp", None
        rest = argv[2:]
        while rest:
            if rest[0] == "--repeats" and len(rest) > 1:
                repeats = int(rest[1])
            elif rest[0] == "--salt" and len(rest) > 1:
                salt = rest[1]
            elif rest[0] == "--run-tag" and len(rest) > 1:
                tag = rest[1]
            else:
                print(USAGE)
                return 2
            rest = rest[2:]
        if not tag:
            print("--emit needs --run-tag")
            return 2
        battery, key = emit(repeats, salt, tag)
        base = out[:-6] if out.endswith(".jsonl") else out
        _write_jsonl(out, battery)
        _write_jsonl(base + ".key.jsonl", key)
        print("wrote %d prompts to %s and the key to %s.key.jsonl"
              % (len(battery), out, base))
        print("keep the key away from the coders")
        return 0
    if cmd == "--prompt" and len(argv) == 3:
        rows = [r for r in _jsonl(argv[1]) if r["id"] == argv[2]]
        if not rows:
            print("id %s not in %s" % (argv[2], argv[1]))
            return 1
        print(assemble(rows[0]))
        return 0
    if cmd == "--sheet" and len(argv) == 3:
        _write_jsonl(argv[2], sheet(_jsonl(argv[1])))
        print("wrote sheet %s (no arm, no context)" % argv[2])
        return 0
    if cmd == "--strip" and len(argv) == 4:
        rows, log = strip_sheet(_jsonl(argv[1]))
        _write_jsonl(argv[2], rows)
        _write_jsonl(argv[3], log)
        print("stripped %d rows; %d touched; log %s goes with the key"
              % (len(rows), sum(1 for r in log if r["words_removed"]),
                 argv[3]))
        return 0
    if cmd == "--score" and len(argv) >= 2:
        keyp, manifest, slog, codes = argv[1], None, None, []
        rest = argv[2:]
        while rest:
            if rest[0] == "--manifest" and len(rest) > 1:
                manifest = rest[1]
                rest = rest[2:]
            elif rest[0] == "--strip-log" and len(rest) > 1:
                slog = rest[1]
                rest = rest[2:]
            else:
                codes.append(rest[0])
                rest = rest[1:]
        if manifest is None:
            print("--score needs --manifest (amendment 1 item 3)")
            return 2
        if len(codes) < 2:
            print("--score needs at least 2 coder files (amendment 1 item 7)")
            return 2
        with open(manifest, encoding="utf-8") as fh:
            m = json.load(fh)
        res = score(_jsonl(keyp), [_jsonl(c) for c in codes], m,
                    _jsonl(slog) if slog else None)
        print(render_score(res))
        return 0
    print(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
