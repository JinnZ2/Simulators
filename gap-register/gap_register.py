#!/usr/bin/env python3
"""
gap_register -- a register of marked, unmeasured quantities.

Built to WORK_ORDER.md, which is delivered verbatim beside this file and
is the authority for every rule here. One entry is one (quantity,
excluding-method) pair. The measurand is the PRESENCE OF A MARK, not the
truth of any claim about the quantity marked (order section 1).

WHAT THIS TOOL DOES NOT DO. It does not decide whether a gap is real. It
does not rank entries. It does not read a venue, a standard or a table --
every status in the shipped register is the evaluation state recorded by
whoever ran the check, and `UNKNOWN` is a peer of every other return
rather than a soft `OPEN` (order section 1).

THREE CHECKS REST ON WORD LISTS. V2 (observable noun), V4 (accusatory
construction, name shape) and the modal screen are word lists, and a word
list deciding sense is the failure this repository records as T1-1: any
paraphrase steps around them, and an ordinary word in an unusual sense
fires. That limit is stated here at the top rather than at the bottom.
The lists are module-level constants so they can be read and disagreed
with.

V5 CARRIES AN UNDEFINED TERM. The order's V5 refuses an index term that
is "a coinage absent from index_terms of any other entry" and supplies no
test for "coinage". Two readings are available and they are not close:
under STRICT, coinage is the singleton itself, so any term no other entry
uses is refused; under LOOSE, a singleton is refused only where the entry
has no shared term at all. The checker scores both and returns
UNDETERMINED where they part, naming the terms. It does not pick.

CC0. stdlib only. Parses under Python 3.9.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTER = os.path.join(HERE, "REGISTER.jsonl")

# ---------------------------------------------------------------- schema

TYPES = ("T1", "T2", "T3", "T4")

STATUS = (
    "OPEN",
    "CLOSED_MEASURED",
    "CLOSED_INSTRUMENT_EXISTS",
    "OUT_OF_ENVELOPE",
    "UNKNOWN",
)

FIELDS = (
    "id",
    "type",
    "quantity",
    "index_terms",
    "excluding_method",
    "measured_instead",
    "venue_check",
    "closure_condition",
    "refutation",
    "status",
    "provenance",
    "confound",
    "opened",
)

# Order section 4: null is permitted in exactly these two.
NULLABLE = ("venue_check", "confound")

# Fields V4 scans. `provenance` is excluded by the rule itself: names
# appear there because they are the custody chain (order section 5).
V4_SCANNED = (
    "quantity",
    "excluding_method",
    "measured_instead",
    "venue_check",
    "closure_condition",
    "refutation",
    "confound",
)

ID_RE = re.compile(r"^[A-Z]{2}-\d{4}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# ---------------------------------------------------------------- lists

# [CHOICE 1] V2 asks for "an observable noun". The order names none, so
# this list is the checker's, not the order's, and it is short on purpose:
# a long list passes everything.
OBSERVABLE = (
    "rate", "rates", "count", "counts", "table", "tables", "column",
    "columns", "field", "fields", "log", "logs", "record", "records",
    "dataset", "datasets", "series", "figure", "figures", "number",
    "numbers", "code", "codes", "coding", "standard", "standards",
    "guideline", "guidelines", "publication", "paper", "papers",
    "study", "studies", "trial", "trials", "transcript", "transcripts",
    "sample", "samples", "survey", "surveys", "benchmark", "benchmarks",
    "instrument", "instruments", "measurement", "measurements",
    "protocol", "protocols", "timestamp", "timestamps", "version",
    "versions", "registry", "registries", "index", "audit", "audits",
    "curriculum", "curricula", "syllabus", "syllabi", "hours",
    "checklist", "checklists", "form", "forms", "score", "scores",
)

# [CHOICE 2] The modal screen. V2's own examples are "should" and
# "ought"; the rest are of the same class.
MODALS = ("should", "ought", "would", "could", "might", "may", "shall")

# [CHOICE 3] V4's accusatory constructions. Phrases, because the single
# words are ordinary: "knew" alone is not a construction, "knew and"
# in this shape is.
ACCUSATORY = (
    r"\bdeliberate(?:ly)?\b",
    r"\bintentional(?:ly)?\b",
    r"\bknowingly\b",
    r"\bwilfully\b",
    r"\bwillfully\b",
    r"\brefus(?:e|ed|es|ing)\s+to\b",
    r"\bfail(?:ed|s)?\s+to\s+disclose\b",
    r"\bconceal(?:ed|s|ing)?\b",
    r"\bsuppress(?:ed|es|ing)?\b",
    r"\bcover(?:ed)?\s+up\b",
    r"\bnegligen(?:t|ce)\b",
    r"\bat\s+fault\b",
    r"\bto\s+blame\b",
    r"\bwrongdoing\b",
    r"\bmisconduct\b",
    r"\bin\s+order\s+to\s+avoid\s+scrutiny\b",
    r"\bso\s+that\s+nobody\s+(?:would|will)\s+(?:see|know)\b",
)
_ACC = [(p, re.compile(p, re.I)) for p in ACCUSATORY]

# Order section 2: an entry needing a motive claim is OUT_OF_ENVELOPE.
MOTIVE = (
    r"\bmotive\b",
    r"\bin\s+order\s+to\s+protect\b",
    r"\bwanted\s+to\b",
    r"\bso\s+as\s+to\s+keep\b",
)
_MOT = [(p, re.compile(p, re.I)) for p in MOTIVE]

HONORIFIC = ("Dr", "Dr.", "Prof", "Prof.", "Mr", "Mr.", "Ms", "Ms.",
             "Mrs", "Mrs.", "Sir", "Judge", "Justice", "Senator")

_WORD = re.compile(r"[A-Za-z][A-Za-z'.-]*")


def name_shaped(text):
    """Spans that look like a person's name.

    [CHOICE 4] The shape is: two or more adjacent Capitalized tokens, or
    an honorific followed by one, or a token followed by "et al". An
    ALL-CAPS token is read as an acronym and never as a name, because
    method and standard names are the ordinary content of these fields
    and an acronym there is expected. That under-fires on an all-caps
    surname and it is the direction chosen: a false name hit refuses a
    legitimate entry.
    """
    out = []
    # An honorific ends in a period, and a sentence splitter that does not
    # know that severs "Dr." from the name it introduces. Found by the
    # honorific arm of the selftest, which the run-of-capitals arm would
    # otherwise have covered for.
    text = re.sub(r"\b(Dr|Prof|Mr|Mrs|Ms)\.", r"\1", text or "")
    for sentence in re.split(r"(?<=[.;:])\s+", text):
        toks = _WORD.findall(sentence)
        if not toks:
            continue
        cap = []
        for i, t in enumerate(toks):
            core = t.rstrip(".")
            is_cap = bool(core) and core[0].isupper() and not core.isupper()
            cap.append(is_cap)
        # "X et al"
        for i in range(len(toks) - 2):
            if cap[i] and toks[i + 1].lower() == "et" and \
                    toks[i + 2].lower().rstrip(".") == "al":
                out.append(" ".join(toks[i:i + 3]))
        # honorific + Capitalized
        for i in range(len(toks) - 1):
            if toks[i] in HONORIFIC and cap[i + 1]:
                out.append(" ".join(toks[i:i + 2]))
        # runs of capitalized tokens; the sentence-initial token is
        # dropped from the run because position, not naming, capitalised
        # it.
        i = 0
        while i < len(toks):
            if not cap[i]:
                i += 1
                continue
            j = i
            while j < len(toks) and cap[j]:
                j += 1
            run = list(range(i, j))
            if run and run[0] == 0:
                run = run[1:]
            if len(run) >= 2:
                out.append(" ".join(toks[run[0]:run[-1] + 1]))
            i = j
    seen = []
    for s in out:
        if s not in seen:
            seen.append(s)
    return seen


# ---------------------------------------------------------------- checks

PASS = "PASS"
FAIL = "FAIL"
UNDETERMINED = "UNDETERMINED"
NOT_EVALUABLE = "NOT_EVALUABLE"


class Check(object):
    def __init__(self, rule, verdict, detail):
        self.rule = rule
        self.verdict = verdict
        self.detail = detail

    def __repr__(self):
        return "Check(%s,%s,%s)" % (self.rule, self.verdict, self.detail)


def v1_fields(rec):
    missing = [f for f in FIELDS if f not in rec]
    if missing:
        return Check("V1", FAIL, "absent field(s): " + ", ".join(missing))
    empty = []
    for f in FIELDS:
        v = rec[f]
        if v is None:
            if f not in NULLABLE:
                empty.append(f + " (null, and null is permitted only in "
                             + ", ".join(NULLABLE) + ")")
            continue
        if isinstance(v, list):
            if not [x for x in v if str(x).strip()]:
                empty.append(f + " (empty list)")
        elif not str(v).strip():
            empty.append(f + " (empty)")
    if empty:
        return Check("V1", FAIL, "; ".join(empty))
    if not ID_RE.match(str(rec["id"])):
        return Check("V1", FAIL, "id is not XX-NNNN: " + str(rec["id"]))
    if str(rec["type"]) not in TYPES:
        return Check("V1", FAIL, "type outside " + "|".join(TYPES))
    if not DATE_RE.match(str(rec["opened"])):
        return Check("V1", FAIL, "opened is not YYYY-MM-DD")
    return Check("V1", PASS, "%d fields present" % len(FIELDS))


def v2_closure(rec):
    text = str(rec.get("closure_condition") or "")
    low = text.lower()
    nouns = [n for n in OBSERVABLE if re.search(r"\b%s\b" % n, low)]
    mods = [m for m in MODALS if re.search(r"\b%s\b" % m, low)]
    if nouns:
        return Check("V2", PASS, "observable noun: " + ", ".join(sorted(set(nouns))))
    if mods:
        return Check("V2", FAIL,
                     "no observable noun located; modal-only phrasing "
                     "(%d modal token(s))" % len(mods))
    return Check("V2", FAIL, "no observable noun located")


def _norm(s):
    return re.sub(r"[^a-z0-9 ]+", " ", str(s or "").lower()).split()


def v3_refutation(rec):
    ref = str(rec.get("refutation") or "").strip()
    clo = str(rec.get("closure_condition") or "").strip()
    if not ref:
        return Check("V3", FAIL, "refutation empty")
    if _norm(ref) == _norm(clo):
        return Check("V3", FAIL, "refutation is the closure condition restated")
    a, b = set(_norm(ref)), set(_norm(clo))
    if a and b:
        jac = len(a & b) / float(len(a | b))
        if jac >= 0.9:
            return Check("V3", FAIL,
                         "refutation overlaps closure condition at %.2f" % jac)
    return Check("V3", PASS, "distinct from closure condition")


def v4_placement(rec):
    hits = []
    for f in V4_SCANNED:
        text = str(rec.get(f) or "")
        for pat, rx in _ACC:
            if rx.search(text):
                hits.append("%s: accusatory construction %s" % (f, pat))
        for pat, rx in _MOT:
            if rx.search(text):
                hits.append("%s: motive term %s -- order section 2 routes "
                            "this entry to OUT_OF_ENVELOPE" % (f, pat))
        for n in name_shaped(text):
            hits.append("%s: name-shaped span outside provenance[]: %s"
                        % (f, n))
    if hits:
        return Check("V4", FAIL, " | ".join(hits))
    return Check("V4", PASS,
                 "no accusatory construction; no name-shaped span outside "
                 "provenance[]")


def v5_index(rec, others):
    terms = [str(t).strip().lower() for t in (rec.get("index_terms") or [])
             if str(t).strip()]
    if len(terms) < 3:
        return Check("V5", FAIL, "%d index term(s); 3 is the floor" % len(terms))
    if not others:
        return Check("V5", NOT_EVALUABLE,
                     "register of one: 'any other entry' has no referent, so "
                     "the singleton test cannot be run")
    elsewhere = set()
    for o in others:
        for t in (o.get("index_terms") or []):
            elsewhere.add(str(t).strip().lower())
    singles = [t for t in terms if t not in elsewhere]
    shared = [t for t in terms if t in elsewhere]
    strict = not singles
    loose = bool(shared)
    if strict and loose:
        return Check("V5", PASS,
                     "%d term(s), all of them used by another entry" % len(terms))
    if not strict and not loose:
        return Check("V5", FAIL,
                     "no index term is used by any other entry: " +
                     ", ".join(singles))
    return Check("V5", UNDETERMINED,
                 "STRICT refuses, LOOSE admits. term(s) no other entry "
                 "uses: " + ", ".join(singles) + " || shared: " +
                 ", ".join(shared))


def v6_status(rec):
    s = str(rec.get("status") or "")
    if s in STATUS:
        return Check("V6", PASS, s)
    return Check("V6", FAIL, "status outside the enum: " + s)


def validate_record(rec, others):
    return [
        v1_fields(rec),
        v2_closure(rec),
        v3_refutation(rec),
        v4_placement(rec),
        v5_index(rec, others),
        v6_status(rec),
    ]


def validate_all(records):
    """[(entry_id, [Check, ...]), ...] in file order."""
    out = []
    for i, rec in enumerate(records):
        others = records[:i] + records[i + 1:]
        out.append((str(rec.get("id") or "<no id>"), validate_record(rec, others)))
    return out


def tally(results):
    counts = {PASS: 0, FAIL: 0, UNDETERMINED: 0, NOT_EVALUABLE: 0}
    for _id, checks in results:
        for c in checks:
            counts[c.verdict] = counts.get(c.verdict, 0) + 1
    return counts


# ------------------------------------------------------------------ io

def load(path):
    """[record, ...]. Raises ValueError naming the line that did not parse."""
    records = []
    if not os.path.exists(path):
        raise ValueError("no such register: " + path)
    fh = open(path, "r")
    try:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                records.append(json.loads(line))
            except Exception as exc:
                raise ValueError("%s line %d does not parse: %s"
                                 % (path, lineno, exc))
    finally:
        fh.close()
    return records


def next_id(records, prefix="GR"):
    n = 0
    for r in records:
        m = re.match(r"^%s-(\d{4})$" % prefix, str(r.get("id") or ""))
        if m:
            n = max(n, int(m.group(1)))
    return "%s-%04d" % (prefix, n + 1)


# ------------------------------------------------------------ rendering

def render_checks(entry_id, checks):
    lines = []
    for c in checks:
        lines.append("  %-4s %-14s %s" % (c.rule, c.verdict, c.detail))
    return ["%s" % entry_id] + lines


def render_validate(path, results):
    counts = tally(results)
    out = ["gap_register validate -- %s" % path,
           "%d entries, %d checks" % (len(results), sum(counts.values())),
           ""]
    for entry_id, checks in results:
        out.extend(render_checks(entry_id, checks))
        out.append("")
    loud = [(e, c) for e, checks in results for c in checks
            if c.verdict in (FAIL, UNDETERMINED)]
    if loud:
        out.append("LOUD -- every check that did not return PASS")
        for e, c in loud:
            out.append("  %s %-4s %-14s %s" % (e, c.rule, c.verdict, c.detail))
        out.append("")
    out.append("PASS %d  FAIL %d  UNDETERMINED %d  NOT_EVALUABLE %d"
               % (counts[PASS], counts[FAIL], counts[UNDETERMINED],
                  counts[NOT_EVALUABLE]))
    out.append("[CHOICE 5] exit is nonzero on FAIL. UNDETERMINED exits zero "
               "and prints above: it is an unevaluated check, and under "
               "order section 1 that is a peer return rather than a "
               "negative one.")
    return "\n".join(out)


def render_export(records):
    out = ["# gap register", "", "%d entries." % len(records), ""]
    for r in records:
        out.append("## %s  (%s, %s)" % (r.get("id"), r.get("type"),
                                        r.get("status")))
        out.append("")
        out.append("- quantity: %s" % r.get("quantity"))
        out.append("- excluded by: %s" % r.get("excluding_method"))
        out.append("- measured instead: %s" % r.get("measured_instead"))
        out.append("- venue check: %s" % (r.get("venue_check") or "none"))
        out.append("- closes when: %s" % r.get("closure_condition"))
        out.append("- not a gap if: %s" % r.get("refutation"))
        out.append("- confound: %s" % (r.get("confound") or "none recorded"))
        out.append("- index terms: %s" % ", ".join(r.get("index_terms") or []))
        out.append("- provenance: %s" % "; ".join(r.get("provenance") or []))
        out.append("- opened: %s" % r.get("opened"))
        out.append("")
    return "\n".join(out)


def render_search(terms, records):
    hits = []
    low = [t.lower() for t in terms]
    for r in records:
        hay = " ".join([str(r.get("quantity") or "")] +
                       [str(t) for t in (r.get("index_terms") or [])]).lower()
        if all(t in hay for t in low):
            hits.append(r)
    out = ["gap_register search -- %s" % " ".join(terms),
           "%d of %d entries" % (len(hits), len(records)), ""]
    for r in hits:
        out.append("%s  %s  %s" % (r.get("id"), r.get("type"),
                                   r.get("quantity")))
    return "\n".join(out)


# ------------------------------------------------------------------ cli

USAGE = """gap_register.py -- register of marked, unmeasured quantities

  gap_register.py add      <json|path>  validate + append, assign the id
  gap_register.py validate [file]       schema + rule check, nonzero on FAIL
  gap_register.py search   <terms>      match on index_terms + quantity
  gap_register.py check    <id>         print the closure condition only
  gap_register.py export   --md         flat markdown, one block per entry

  --register PATH   read/write this register instead of REGISTER.jsonl

Rules V1..V6 are WORK_ORDER.md section 6. The checks are in this file.
"""


def cmd_add(arg, path):
    if os.path.exists(arg):
        text = open(arg).read()
    else:
        text = arg
    try:
        rec = json.loads(text)
    except Exception as exc:
        sys.stderr.write("add: argument does not parse as JSON: %s\n" % exc)
        return 2
    records = load(path) if os.path.exists(path) else []
    if rec.get("id") and any(str(r.get("id")) == str(rec["id"])
                             for r in records):
        sys.stderr.write("add: id %s is already in the register; the tool "
                         "assigns ids\n" % rec["id"])
        return 2
    rec["id"] = next_id(records)
    ordered = {}
    for f in FIELDS:
        if f in rec:
            ordered[f] = rec[f]
    for k in rec:
        if k not in ordered:
            ordered[k] = rec[k]
    checks = validate_record(ordered, records)
    bad = [c for c in checks if c.verdict == FAIL]
    print("\n".join(render_checks(ordered["id"], checks)))
    if bad:
        sys.stderr.write("add: not appended; %d check(s) returned FAIL\n"
                         % len(bad))
        return 1
    fh = open(path, "a")
    try:
        fh.write(json.dumps(ordered, sort_keys=False) + "\n")
    finally:
        fh.close()
    print("appended %s to %s" % (ordered["id"], path))
    return 0


def cmd_validate(path):
    records = load(path)
    results = validate_all(records)
    print(render_validate(path, results))
    counts = tally(results)
    return 1 if counts[FAIL] else 0


def cmd_search(terms, path):
    print(render_search(terms, load(path)))
    return 0


def cmd_check(entry_id, path):
    for r in load(path):
        if str(r.get("id")) == entry_id:
            print(r.get("closure_condition"))
            return 0
    sys.stderr.write("check: no entry %s in %s\n" % (entry_id, path))
    return 2


def cmd_export(path):
    print(render_export(load(path)))
    return 0


def main(argv):
    args = list(argv)
    path = REGISTER
    if "--register" in args:
        i = args.index("--register")
        if i + 1 >= len(args):
            sys.stderr.write("--register wants a path\n")
            return 2
        path = args[i + 1]
        del args[i:i + 2]
    if "--selftest" in args:
        sys.stderr.write(
            "gap_register.py is the instrument. Its checks live in "
            "selftest_gr.py; run that.\n")
        return 2
    if not args:
        sys.stderr.write(USAGE)
        return 2
    cmd, rest = args[0], args[1:]
    try:
        if cmd == "add":
            if not rest:
                sys.stderr.write("add wants a JSON object or a path\n")
                return 2
            return cmd_add(rest[0], path)
        if cmd == "validate":
            return cmd_validate(rest[0] if rest else path)
        if cmd == "search":
            if not rest:
                sys.stderr.write("search wants one or more terms\n")
                return 2
            return cmd_search(rest, path)
        if cmd == "check":
            if not rest:
                sys.stderr.write("check wants an entry id\n")
                return 2
            return cmd_check(rest[0], path)
        if cmd == "export":
            if "--md" not in rest:
                sys.stderr.write("export wants --md\n")
                return 2
            return cmd_export(path)
    except ValueError as exc:
        sys.stderr.write("%s\n" % exc)
        return 2
    sys.stderr.write(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
