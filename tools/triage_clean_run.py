"""Clean calibration of WO-3 site 2, the second scorer, and the PROPOSED
GA (g) variants. Stdlib only, Python >= 3.8, CC0.

Reads tools/clean_run_wo3/ (the run's files, committed verbatim before any
comparison) and tools/experiment_fruitfulness_triage.md, sections 7.8,
8.1 and 8.2. Writes nothing. The first calibration (7.1-7.6, fill pinned
at d5f5c2a) belongs to the triage scorer and is only read here, to check
it is still the committed text.

    python3 tools/triage_clean_run.py              report, then VERDICT
    python3 tools/triage_clean_run.py --selftest   checks, then VERDICT

Rubric blocks read:

    clean-run-files    sha256 and name of every file in the run directory
    clean-match-a      the stage-1 fill (fields (a)-(f)) against the 8
                       published facts of 7.3, four states
    clean-match        stages 1-2 (all seven fields) against the same
    scorer-agreement   generated here; held to what this module computes
    triage-proposed    PROPOSED GA (g) variants, not admitted
    proposed-basis     one reason per PROPOSED component
    proposed-result    generated here

The second scorer is set against the rubric's rows after the Part C delta
(tools/check_citations.py), S6 included: the reader's designed row
against the site's designed row, its (g) row against the site's (g) row.
Agreement is counted per field and per site, and every cell where the two
scorers sit more than one step apart on a three-step scale (0 against 2,
low against high) is listed. Nothing is averaged into one number.

Exit 0 every check passes; 1 a check fails; 3 the inputs cannot be read.
"""

import hashlib
import importlib.util
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RUBRIC = os.path.join(HERE, "experiment_fruitfulness_triage.md")
SCORER = os.path.join(HERE, "experiment_fruitfulness_triage.py")
AUDIT_TOOL = os.path.join(HERE, "check_citations.py")

# The run's files, committed verbatim in tools/clean_run_wo3/ (5eb76eb)
# before any comparison was written. The three reader outputs were hashed
# in the reader's own session before the next stage was sent; the
# messages are what this session sent, so the run can be repeated.
RUN_DIR = os.path.join(HERE, "clean_run_wo3")
PINNED = {
    "probe_question.txt":
        "e92f5ac27e71e01b170db9d48a495cdc77715a8117a31b5d9b1ece48d07d1e51",
    "probe_answer.txt":
        "8b8ac0db9891df53ecd45352311e72b39a248a9401ace38fc5f3e417db67f70a",
    "stage1_message.txt":
        "997d2004331d9c6ed7f460ae0a3331b4f179ab9e8092713d56693553fc77535d",
    "stage1_fill_A.txt":
        "4a98b19b13c64b68a1f07301f1e993e16c7d19d7f7de441e96aa5e7503039ddd",
    "stage2_message.txt":
        "7bc0ca020d4ba724cea171246be82ac7fb06adf34b9180bb358eaa3fa9e550bb",
    "stage2_fill_G.txt":
        "0d8851121f6b91b569c40d120cf6960c10e6413475f18683f01e964ae6d1988b",
    "stage3_message.txt":
        "16fd01ae75b8ff8e81d8c77332a17c9e8875c2098ddc4bad8365c6235e1f4269",
    "stage3_scores_C.txt":
        "ef47a893d30ee2d89ae24525cc594d6aea73af7eaa5401a9fefc06a5b9347273",
    "last_question.txt":
        "efe6d6f5817aa640b2b9704f3098d87005be401e0abcede9225dfaf41ab18495",
    "last_answer.txt":
        "b6888692711dd771f98c5541a1bdd8e124546603e204e89966fdb9d9c17ad980",
}

# The reader's twelve rows against the rubric's: designed MDE against the
# site's designed variant, (g) against the site's (g) variant. S6's
# designed MDE is S6b (audit C.5, field (c)).
PAIRS = (("S1a", "S1a"), ("S1g", "S1g"), ("S2a", "S2a"), ("S2g", "S2b"),
         ("S3a", "S3a"), ("S3g", "S3g"), ("S4a", "S4a"), ("S4g", "S4g"),
         ("S5a", "S5a"), ("S5g", "S5g"), ("S6a", "S6b"), ("S6g", "S6g"))
SITES6 = ("S1", "S2", "S3", "S4", "S5", "S6")
COMPONENTS = ("d", "u", "k", "x", "r")
RESOURCES = ("compute", "data", "lit", "time")
LEVEL_STEP = {"low": 0, "medium": 1, "high": 2}
FIELDS = COMPONENTS + RESOURCES
MATCH_STATES = ("MATCH", "PARTIAL", "NO_SLOT", "NOT_LOCATED")
FACTS = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8")
RANK_PROFILE = "lab"     # nothing BLOCKED, so the ranks compare designs

ROW_RE = re.compile(r"^(S[1-6][a-z])\s+(S[1-6])\s+([0-2])\s+([0-2])\s+"
                    r"([0-2])\s+([0-2])\s+([0-2])\s+(low|medium|high)\s+"
                    r"(low|medium|high)\s+(low|medium|high)\s+"
                    r"(low|medium|high)\s+(\S.*)$")
BASIS_RE = re.compile(r"^(S[1-6][a-z])\.([dukxr])\s+(\S.*)$")
COUNTS_RE = (r"Counts, %s: MATCH (\d+), PARTIAL (\d+), NO_SLOT (\d+), "
             r"NOT_LOCATED (\d+)\.")


class CleanRunError(Exception):
    pass


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fenced_any(doc, name):
    """Content of the one block opened by a line reading three backticks
    and `name`, each line ending in a newline."""
    lines = doc.split("\n")
    opens = [i for i, ln in enumerate(lines) if ln.rstrip() == "```" + name]
    if len(opens) != 1:
        raise CleanRunError("block %r: %d opening fences, want 1"
                            % (name, len(opens)))
    body = []
    for ln in lines[opens[0] + 1:]:
        if ln.rstrip() == "```":
            return "".join(x + "\n" for x in body)
        body.append(ln)
    raise CleanRunError("block %r is not closed" % name)


def parse_rows(text):
    """Rows in the triage format, sites S1-S6. Lines that do not open
    with "S<n><x> S<n>" are skipped (the reader's output holds its table
    between two prose blocks); an id line that does not parse raises."""
    rows, seen = [], set()
    for n, ln in enumerate(text.splitlines(), 1):
        s = ln.strip()
        if not re.match(r"^S[1-6][a-z]\s+S[1-6]\s", s):
            continue
        m = ROW_RE.match(s)
        if not m:
            raise CleanRunError("table line %d unreadable: %r" % (n, s))
        vid, site = m.group(1), m.group(2)
        if not vid.startswith(site) or vid in seen:
            raise CleanRunError("table line %d: id %r" % (n, vid))
        seen.add(vid)
        comp = dict(zip(COMPONENTS, (int(m.group(i)) for i in range(3, 8))))
        need = dict(zip(RESOURCES, (m.group(i) for i in range(8, 12))))
        rows.append({"id": vid, "site": site, "comp": comp, "need": need,
                     "design": m.group(12).strip()})
    return rows


def parse_basis(text):
    out = {}
    for ln in text.splitlines():
        m = BASIS_RE.match(ln.strip())
        if m:
            key = (m.group(1), m.group(2))
            if key in out:
                raise CleanRunError("reason repeated: %s.%s" % key)
            out[key] = m.group(3).strip()
    return out


def parse_match(text):
    rows = []
    for ln in text.splitlines():
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) != 4 or parts[1] not in MATCH_STATES:
            raise CleanRunError("match line unreadable: %r" % ln)
        rows.append({"fact": parts[0], "state": parts[1],
                     "field": parts[2], "note": parts[3]})
    return rows


def match_counts(rows):
    return {s: sum(1 for r in rows if r["state"] == s) for s in MATCH_STATES}


def field_step(row, field):
    if field in COMPONENTS:
        return row["comp"][field]
    return LEVEL_STEP[row["need"][field]]


def field_agreement(pairs_of_steps):
    """(exact, one step apart, two steps apart) over (a, b) pairs on a
    three-step scale. Two steps apart is "more than one step"."""
    exact = one = two = 0
    for a, b in pairs_of_steps:
        for v in (a, b):
            if isinstance(v, bool) or v not in (0, 1, 2):
                raise ValueError("steps are 0, 1, 2: %r" % (v,))
        d = abs(a - b)
        if d == 0:
            exact += 1
        elif d == 1:
            one += 1
        else:
            two += 1
    return exact, one, two


def comp_rank(values):
    """Competition ranking, highest first: ties share a rank and the next
    rank skips ("1 1 3"). None (no reachable variant) gets no rank."""
    vals = [v for v in values.values() if v is not None]
    return {k: (None if v is None else
                1 + sum(1 for w in vals if w > v + 1e-12))
            for k, v in values.items()}


def best_ratio(rows, site, q, sc):
    best = None
    for r in rows:
        if r["site"] != site:
            continue
        v = sc.variant_ratio(r, q)
        if v == sc.NOT_REACHED:
            continue
        if best is None or v > best + 1e-12:
            best = v
    return best


def my_rows(sc, ca):
    """The rubric's rows as Part C left them: the triage table with the
    one Part C delta applied, plus the S6 variants."""
    adoc = ca.read_doc()
    base = sc.parse_table(sc.fenced(sc.read_doc(), "triage-table"))
    rows = ca.apply_deltas(base, ca.parse_deltas(
        ca.fenced(adoc, "partc-deltas")))
    return rows + ca.parse_variants(ca.fenced(adoc, "partc-variants"), sc)


def agreement(reader, mine, sc):
    by_r = {r["id"]: r for r in reader}
    by_m = {r["id"]: r for r in mine}
    missing = [rid for rid, _ in PAIRS if rid not in by_r]
    missing += [mid for _, mid in PAIRS if mid not in by_m]
    if missing:
        raise CleanRunError("rows missing: %s" % ", ".join(missing))
    per_field, far = {}, []
    per_site = {s: [0, 0, 0] for s in SITES6}
    for f in FIELDS:
        steps = []
        for rid, mid in PAIRS:
            a, b = field_step(by_r[rid], f), field_step(by_m[mid], f)
            steps.append((a, b))
            cell = field_agreement([(a, b)])
            for i in range(3):
                per_site[rid[:2]][i] += cell[i]
            if cell[2]:
                far.append((rid, mid, f, a, b))
        per_field[f] = field_agreement(steps)
    r_rows = [by_r[rid] for rid, _ in PAIRS]
    m_rows = [by_m[mid] for _, mid in PAIRS]
    ranks = {}
    for q in sc.QUESTIONS:
        rb = {s: best_ratio(r_rows, s, q, sc) for s in SITES6}
        mb = {s: best_ratio(m_rows, s, q, sc) for s in SITES6}
        ranks[q] = (rb, mb, comp_rank(rb), comp_rank(mb))
    return {"per_field": per_field, "per_site": per_site, "far": far,
            "ranks": ranks}


def _lv(level):
    return {"low": "L", "medium": "M", "high": "H"}[level]


def render_agreement(ag, reader, mine, sc):
    by_r = {r["id"]: r for r in reader}
    by_m = {r["id"]: r for r in mine}
    out = ["# reader row -> rubric row (after the Part C delta), 12 pairs",
           "# field     same  1 step  2 steps   (2 steps = more than one "
           "step apart)"]
    for f in FIELDS:
        e, o, t = ag["per_field"][f]
        out.append("%-8s  %5d  %6d  %7d" % (f, e, o, t))
    tot = [sum(ag["per_field"][f][i] for f in FIELDS) for i in range(3)]
    out.append("%-8s  %5d  %6d  %7d   of %d cells"
               % ("all", tot[0], tot[1], tot[2], len(FIELDS) * len(PAIRS)))
    out.append("# site      same  1 step  2 steps   (2 rows x 9 fields)")
    for s in SITES6:
        e, o, t = ag["per_site"][s]
        out.append("%-8s  %5d  %6d  %7d" % (s, e, o, t))
    out.append("# more than one step apart")
    if not ag["far"]:
        out.append("none")
    for rid, mid, f, a, b in ag["far"]:
        out.append("%s/%s  %-7s  reader %d  rubric %d" % (rid, mid, f, a, b))
    out.append("# rows   d u k x r  cost   |  rubric row  d u k x r  cost"
               "   (cost: compute data lit time, L M H)")
    for rid, mid in PAIRS:
        r, m = by_r[rid], by_m[mid]
        out.append("%s    %s  %s   |  %-4s        %s  %s" % (
            rid, " ".join(str(r["comp"][c]) for c in COMPONENTS),
            "".join(_lv(r["need"][x]) for x in RESOURCES), mid,
            " ".join(str(m["comp"][c]) for c in COMPONENTS),
            "".join(_lv(m["need"][x]) for x in RESOURCES)))
    out.append("# site rank by the better of its two paired rows, declared "
               "choices, no profile gate")
    for q in sc.QUESTIONS:
        rb, mb, rr, mr = ag["ranks"][q]
        out.append("Q-%-4s site  reader      rank  rubric      rank" % q)
        for s in SITES6:
            def val(v):
                return "NOT_REACHED" if v is None else "%-11.3f" % v

            def rk(v):
                return "-" if v is None else str(v)
            if rr[s] is None or mr[s] is None:
                flag = "" if rr[s] == mr[s] else "  reached by one only"
            else:
                flag = "  moved %d" % abs(rr[s] - mr[s]) \
                    if abs(rr[s] - mr[s]) > 1 else ""
            out.append(("       %s    %s %-4s  %s %-4s%s"
                        % (s, val(rb[s]), rk(rr[s]), val(mb[s]), rk(mr[s]),
                           flag)).rstrip())
    return out


def proposed_readout(doc, sc, mine):
    """What the PROPOSED rows would do if admitted: their ratios, and the
    first-place readings over the 64-setting sweep, with and without them,
    for every profile. The triage table is not changed."""
    prop = parse_rows(fenced_any(doc, "triage-proposed"))
    if not prop:
        raise CleanRunError("triage-proposed is empty")
    for r in prop:
        if not r["design"].startswith("(g)"):
            raise CleanRunError("%s is not a (g) row" % r["id"])
    lines = ["# PROPOSED rows; LOOP / REV at the declared choices; cost"]
    for r in prop:
        lines.append("%s  %s / %s  cost %d" % (
            r["id"], sc._fmt(sc.variant_ratio(r, "LOOP")),
            sc._fmt(sc.variant_ratio(r, "REV")), sc.variant_cost(r)))
    lines.append("# profile       question  without PROPOSED          "
                 "with PROPOSED")
    for prof in sorted(sc.PROFILES):
        have = sc.PROFILES[prof]
        for q in sc.QUESTIONS:
            lines.append("%-14s Q-%-4s    %-25s %s" % (
                prof, q, sc.sweep(mine, have, q)[1],
                sc.sweep(mine + prop, have, q)[1]))
    return prop, lines


def build(rubric=RUBRIC, run_dir=RUN_DIR):
    doc = read_text(rubric)
    sc = _load(SCORER, "_eft_clean")
    ca = _load(AUDIT_TOOL, "_cc_clean")
    files = {name: read_text(os.path.join(run_dir, name)) for name in PINNED}
    scores = files["stage3_scores_C.txt"]
    mine = my_rows(sc, ca)
    reader = parse_rows(scores)
    st = {"doc": doc, "sc": sc, "files": files, "reader": reader,
          "basis": parse_basis(scores), "mine": mine,
          "ag": agreement(reader, mine, sc),
          "match_a": parse_match(fenced_any(doc, "clean-match-a")),
          "match": parse_match(fenced_any(doc, "clean-match")),
          "listed": read_text(os.path.join(run_dir, "SHA256SUMS"))}
    st["prop"], st["prop_lines"] = proposed_readout(doc, sc, mine)
    st["prop_basis"] = parse_basis(fenced_any(doc, "proposed-basis"))
    return st


def _stated_counts(doc, label):
    m = re.search(COUNTS_RE % re.escape(label), doc)
    return None if m is None else tuple(int(x) for x in m.groups())


def _first_diff(got, want):
    for i in range(max(len(got), len(want))):
        g = got[i] if i < len(got) else "<missing>"
        w = want[i] if i < len(want) else "<missing>"
        if g != w:
            return "line %d: got %r want %r" % (i + 1, g, w)
    return ""


def checks(st):
    doc, sc = st["doc"], st["sc"]
    out = []

    def check(name, ok, detail=""):
        out.append((name, bool(ok), detail))

    for name, want in sorted(PINNED.items()):
        got = sha(st["files"][name])
        check("%s matches its pinned sha256" % name, got == want, got[:16])
    want_list = "".join("%s  %s\n" % (PINNED[n], n) for n in PINNED)
    check("SHA256SUMS lists every pinned file and hash",
          sorted(st["listed"].splitlines()) == sorted(want_list.splitlines()))
    check("the rubric's clean-run-files block is SHA256SUMS",
          fenced_any(doc, "clean-run-files") == st["listed"])
    ids = set(r["id"] for r in st["reader"])
    want_ids = set(r for r, _ in PAIRS)
    check("the reader's table has its twelve rows, S1a..S6g",
          ids == want_ids, ", ".join(sorted(ids ^ want_ids)))
    gaps = [(v, c) for v in sorted(want_ids) for c in COMPONENTS
            if (v, c) not in st["basis"]]
    check("every reader component has its reason (60 lines)",
          not gaps and len(st["basis"]) == 60,
          ", ".join("%s.%s" % g for g in gaps[:6]))
    hits = sc.leak_hits(st["files"]["stage1_fill_A.txt"])
    check("the stage-1 fill carries no key term of the published result",
          not hits, ", ".join(hits))
    hits = sc.leak_hits(st["files"]["stage1_message.txt"])
    check("the stage-1 message carries no key term", not hits,
          ", ".join(hits))
    for label, rows in (("stage 1", st["match_a"]),
                        ("stages 1-2", st["match"])):
        facts = tuple(r["fact"] for r in rows)
        check("comparison, %s, covers P1..P8 once each in order" % label,
              facts == FACTS, ", ".join(facts))
        cnt = match_counts(rows)
        check("the stated counts, %s, are the table's" % label,
              _stated_counts(doc, label) ==
              tuple(cnt[s] for s in MATCH_STATES),
              " ".join("%s %d" % (s, cnt[s]) for s in MATCH_STATES))
    got = fenced_any(doc, "scorer-agreement").rstrip("\n").split("\n")
    want = render_agreement(st["ag"], st["reader"], st["mine"], sc)
    check("scorer-agreement block is what this module computes",
          got == want, _first_diff(got, want))
    got = fenced_any(doc, "proposed-result").rstrip("\n").split("\n")
    check("proposed-result block is what this module computes",
          got == st["prop_lines"], _first_diff(got, st["prop_lines"]))
    pgaps = [(r["id"], c) for r in st["prop"] for c in COMPONENTS
             if (r["id"], c) not in st["prop_basis"]]
    check("every PROPOSED component has its reason", not pgaps,
          ", ".join("%s.%s" % g for g in pgaps[:6]))
    tbl = sc.parse_table(sc.fenced(doc, "triage-table"))
    check("no PROPOSED row is in the triage table",
          not set(r["id"] for r in st["prop"]) & set(r["id"] for r in tbl))
    check("the first calibration's fill is untouched (d5f5c2a pin)",
          sc.blind_fill_sha(sc.fenced(doc, "blind-fill"))
          == sc.BLIND_FILL_SHA256)
    check("section 7.8 states CONTAMINATED-BY-PRIOR",
          "CONTAMINATED-BY-PRIOR" in doc)
    return out


def unit_checks():
    out = []

    def check(name, ok, detail=""):
        out.append((name, bool(ok), detail))

    check("field_agreement: identical pairs are all the same",
          field_agreement([(0, 0), (2, 2)]) == (2, 0, 0))
    check("field_agreement: 0 against 2 is two steps",
          field_agreement([(0, 2)]) == (0, 0, 1))
    check("field_agreement: low against medium is one step",
          field_agreement([(LEVEL_STEP["low"], LEVEL_STEP["medium"])])
          == (0, 1, 0))
    try:
        field_agreement([(True, 1)])
        refused = False
    except ValueError:
        refused = True
    check("field_agreement refuses a bool step", refused)
    check("comp_rank: ties share a rank and the next skips",
          comp_rank({"a": 3.0, "b": 3.0, "c": 1.0})
          == {"a": 1, "b": 1, "c": 3})
    check("comp_rank: a site with no reachable row gets no rank",
          comp_rank({"a": 1.0, "b": None}) == {"a": 1, "b": None})
    rows = parse_rows("S6x  S6  2 1 2 2 1  low low low low  (g) x\n"
                      "S6x.d reason\n")
    check("parse_rows reads an S6 row and skips a reason line",
          len(rows) == 1 and rows[0]["comp"]["u"] == 1)
    try:
        parse_rows("S6x  S6  2 1 2 2 9  low low low low  bad\n")
        bad = False
    except CleanRunError:
        bad = True
    check("parse_rows refuses a component of 9", bad)
    return out


def planted(st):
    """Each plant must turn at least one check red."""
    out = []
    doc = st["doc"]
    match = fenced_any(doc, "clean-match")
    agree = fenced_any(doc, "scorer-agreement")
    plants = (
        ("an edited stage-1 fill", None,
         ("stage1_fill_A.txt", "FOUND", "FOUNDX")),
        ("a comparison state changed without its counts",
         (match, match.replace("| NO_SLOT |", "| PARTIAL |", 1)), None),
        ("a hand-edited agreement block",
         (agree, agree.replace("  of 108 cells", "  of 109 cells", 1)),
         None),
    )
    for name, doc_edit, file_edit in plants:
        tmp = tempfile.mkdtemp(prefix="clean_run_plant_")
        try:
            rub = os.path.join(tmp, "rubric.md")
            run = os.path.join(tmp, "run")
            os.mkdir(run)
            text = doc if doc_edit is None else \
                doc.replace(doc_edit[0], doc_edit[1], 1)
            changed = text != doc
            with open(rub, "w", encoding="utf-8") as fh:
                fh.write(text)
            names = list(PINNED) + ["SHA256SUMS"]
            for n in names:
                body = st["files"].get(n, st["listed"])
                if file_edit and n == file_edit[0]:
                    new = body.replace(file_edit[1], file_edit[2], 1)
                    changed = changed or new != body
                    body = new
                with open(os.path.join(run, n), "w", encoding="utf-8") as fh:
                    fh.write(body)
            try:
                bad = any(not ok for _, ok, _ in checks(build(rub, run)))
            except (CleanRunError, KeyError, ValueError):
                bad = True
        finally:
            for root, dirs, fnames in os.walk(tmp, topdown=False):
                for f in fnames:
                    os.remove(os.path.join(root, f))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(tmp)
        out.append(("plant caught: %s" % name, changed and bad, ""))
    return out


def report(st):
    sc = st["sc"]
    L = ["CLEAN CALIBRATION, SECOND SCORER, PROPOSED GA (g)  "
         "(tools/triage_clean_run.py)"]
    for label, rows in (("stage 1", st["match_a"]),
                        ("stages 1-2", st["match"])):
        cnt = match_counts(rows)
        L.append("comparison, %-10s %s" % (label + ":", "  ".join(
            "%s %d" % (s, cnt[s]) for s in MATCH_STATES)))
    L.extend(render_agreement(st["ag"], st["reader"], st["mine"], sc))
    L.extend(st["prop_lines"])
    return L


def main(argv):
    try:
        st = build()
    except (OSError, CleanRunError, KeyError) as exc:
        print("cannot read the inputs: %s" % exc)
        print("VERDICT: CANNOT_RUN")
        return 3
    if "--selftest" in argv:
        res = unit_checks() + checks(st) + planted(st)
        for name, ok, detail in res:
            print("%s  %s%s" % ("PASS" if ok else "FAIL", name,
                                ("   " + detail) if detail and not ok
                                else ""))
    else:
        for ln in report(st):
            print(ln)
        res = checks(st)
        for name, ok, detail in res:
            if not ok:
                print("FAIL  %s   %s" % (name, detail))
    failed = sum(1 for _, ok, _ in res if not ok)
    print("VERDICT: %s   checks=%d failed=%d"
          % ("PASS" if not failed else "FAIL", len(res), failed))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
