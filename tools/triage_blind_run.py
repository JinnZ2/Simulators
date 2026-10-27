"""Blind calibration of the WO-3 rubric on a post-cutoff anchor (site T),
and the independent second scorer. Stdlib only, Python >= 3.8, CC0.

Reads tools/blind_run_wo3/ (the run's files: the anchor facts and every
message pinned at 58016a4 before any session was opened; the fills
committed at 95d2579 and the second scorer's file at bf0af2d, each
before any comparison) and tools/experiment_fruitfulness_triage.md,
sections 7.9 and 8.3. Writes nothing. Reuses the parsers and the
registered field_agreement of tools/triage_clean_run.py, imported by
path, so the two runs are read by one set of rules.

    python3 tools/triage_blind_run.py              report, then VERDICT
    python3 tools/triage_blind_run.py --selftest   checks, then VERDICT

Rubric blocks read:

    blind-run-files    sha256 and name of every file in the run directory
    blind-match-a      the stage-1 fill (fields (a)-(f)) against the
                       anchor's facts T1..T7, four states
    blind-match        stages 1-2 (all seven fields) against the same
    scorer2-agreement  generated here; held to what this module computes
    scorer2-readings   generated here

The second scorer scored the rubric's own 23 rows (the triage table as
Part C left it, the S6 variants, and the six PROPOSED GA rows), given
each row's design and none of its scores or reasons. Each of its cells is
set against the rubric's cell for the same row: same, one step apart, or
two steps apart (0 against 2, low against high). Nothing is averaged into
one number.

Exit 0 every check passes; 1 a check fails; 3 the inputs cannot be read.
"""

import importlib.util
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RUBRIC = os.path.join(HERE, "experiment_fruitfulness_triage.md")
SCORER = os.path.join(HERE, "experiment_fruitfulness_triage.py")
AUDIT_TOOL = os.path.join(HERE, "check_citations.py")
CLEAN_TOOL = os.path.join(HERE, "triage_clean_run.py")
RUN_DIR = os.path.join(HERE, "blind_run_wo3")

# Pinned at 58016a4, before any session was opened. A change to any of
# these after that commit would mean the run was not what was registered.
PRE_REGISTERED = {
    "anchor_facts.txt":
        "2dd5db3469acb8de405294e5c31069319b360c52c99b1702a427682bc26f843a",
    "packet_T.txt":
        "0c7e3be492c6573366f01529a5e4cbc58aa2fe47c6e3d4d2feee80ab71054006",
    "probe_question.txt":
        "d7bc5157578a45978d59586b40f16e29cb4efa638e9127f17ecffa4ce9f56181",
    "reader_q0.txt":
        "4a6b66316871165c179b544e1ee94dff9476579c7b11c92e2b85901c492b5191",
    "stage1_message.txt":
        "c7d8c53e17974e899a4a1694d79eb0bce0eb71045c5944c505a46b02e4783074",
    "stage2_message.txt":
        "723af058ef6ef8e9f12e44b699a47d00c6ae36b550d7f3c130e0d90645137fc7",
    "reader_last.txt":
        "0680875fa1f12eb29422b733addd06a7c825c65c56c13cd74a894533a0390015",
    "scorer_q0.txt":
        "23f69c53969ac64600ea09b704886fc916b737676fa65afa8191a28f33b069b5",
    "scorer_message.txt":
        "91f5feadea4ebf36f7bf073285ca605e28fc5837a0fd37227f85bea6715a6097",
    "scorer_last.txt":
        "bf28edd2e3335d380c07c557489edab058829910ea19c7dfaadb581752f0dd4e",
}
# Hashed in the reader's and the scorer's own sessions before the next
# message was sent, and recomputed here from the committed text.
SESSION_HASHED = {
    "fill_A.txt":
        "a25bb56154e3dee3f1f8876feb4d9d19f35e7d260b4b71eb9f41faa26936a23e",
    "fill_G.txt":
        "8e5e8efef186f75ceb7085c2de24626b386090318b57c2d3aeffccea48738a93",
    "scores_S.txt":
        "b3440da8fd9181242ea5798dc55f01f866fe85edd28905db9c9534f93d37515f",
}
# The sessions' answers, transcribed verbatim and hashed here, not there.
ANSWERS = {
    "probe_answer.txt":
        "612d68f28c6bb32f3a030e535db178b7462ecc11b07257c443b77e58d9b3d932",
    "reader_q0_answer.txt":
        "789e83abac11bc3b3b7bca0cd8e8c01d531d6a58a9cb782b04ca153c518732ab",
    "reader_last_answer.txt":
        "6d4c133056b636f3aa68e1196f65e1f18d965a86fe74ee304fe9ad5a089d1a07",
    "scorer_q0_answer.txt":
        "50eb96e8b1c364a8ab79bf7ce2823cf9fb542f1539e514356244d965f8b1dfdb",
    "scorer_last_answer.txt":
        "a021747d2ffdf8fc8078d3eedc231110db6252743256b9dc510d3ef805873a7c",
}
PINNED = dict(PRE_REGISTERED)
PINNED.update(SESSION_HASHED)
PINNED.update(ANSWERS)

# What each answer must say for the status declared in 7.9 and 8.3.
ANSWER_MARKS = (
    ("probe_answer.txt", "status  : NOT RECOGNIZED"),
    ("reader_q0_answer.txt", "**Do I know the paper?** No."),
    ("reader_last_answer.txt", "1. Recognition: No."),
    ("scorer_q0_answer.txt", "**Yes, I recognise it.**"),
)

FACTS = ("T1", "T2", "T3", "T4", "T5", "T6", "T7")
SCORED_IDS = ("S1a", "S1e", "S1g", "S2a", "S2b", "S2c", "S2e", "S3a",
              "S3e", "S3g", "S4a", "S4b", "S4e", "S4g", "S5a", "S5b",
              "S5e", "S5g", "S6a", "S6b", "S6c", "S6e", "S6g")
RANK_PROFILE = "lab"     # nothing BLOCKED, so the ranks compare designs
COUNTS_RE = (r"Counts, site T, %s: MATCH (\d+), PARTIAL (\d+), "
             r"NO_SLOT (\d+), NOT_LOCATED (\d+)\.")
TABLE_RE = re.compile(r"^(S[1-6][a-z])\s+(S[1-6])\s+([0-2])\s+([0-2])\s+"
                      r"([0-2])\s+([0-2])\s+([0-2])\s+(low|medium|high)\s+"
                      r"(low|medium|high)\s+(low|medium|high)\s+"
                      r"(low|medium|high)\s*$")
REASON_RE = re.compile(r"^(S[1-6][a-z])\.(d|u|k|x|r|cost)\s+(\S.*)$")
# The one phrase the packet's word-list screen missed (7.9, K-P2). It is
# held here so that an edit to the packet that removes it is noticed:
# the record says it was there.
RECORDED_MISS = "not a fixed fact"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CR = _load(CLEAN_TOOL, "_tcr_blind")
BlindRunError = CR.CleanRunError
COMPONENTS, RESOURCES, FIELDS = CR.COMPONENTS, CR.RESOURCES, CR.FIELDS
SITES6, MATCH_STATES = CR.SITES6, CR.MATCH_STATES


def source_text(text):
    """A packet as a filler reads it: a hyphen at a line break joins the
    two halves of the word, then whitespace is normalized."""
    return CR_norm(re.sub(r"-[ \t]*\n[ \t]*", "-", text))


def CR_norm(s):
    return re.sub(r"\s+", " ", s).strip()


def quotes(block):
    out = []
    for ln in block.splitlines():
        if ln.startswith("SRC"):
            out.extend(re.findall(r'"([^"]+)"', ln))
    return out


def unsourced(block, source):
    return [q for q in quotes(block) if CR_norm(q) not in source]


def g_definition(stage2):
    """Field (g)'s definition as stage 2 gave it."""
    m = re.search(r"\(g\) EMERGENCE\s+(.*?)\n\n", stage2, re.S)
    if not m:
        raise BlindRunError("stage 2: no (g) definition")
    return m.group(1)


def strip_targets(facts_text):
    m = re.search(r"STRIP TARGETS\..*?appear in the packet the reader "
                  r"gets:\n(.*?)\n\n|STRIP TARGETS\..*?gets:\n(.*)$",
                  facts_text, re.S)
    if not m:
        raise BlindRunError("anchor_facts.txt: no STRIP TARGETS list")
    body = (m.group(1) or m.group(2)).replace("\n", " ")
    terms = [t.strip().strip(".").strip('"') for t in body.split(",")]
    return [t for t in terms if t]


def target_hits(text, terms):
    return [t for t in terms
            if re.search(r"\b" + re.escape(t), text, re.IGNORECASE)]


def parse_scores(text, designs):
    """The second scorer's table (no design column) and its reasons. The
    design of each row is the rubric's, by id."""
    rows, seen = [], set()
    for n, ln in enumerate(text.splitlines(), 1):
        s = ln.strip()
        if not re.match(r"^S[1-6][a-z]\s+S[1-6]\s", s):
            continue
        m = TABLE_RE.match(s)
        if not m:
            raise BlindRunError("scores line %d unreadable: %r" % (n, s))
        vid, site = m.group(1), m.group(2)
        if not vid.startswith(site) or vid in seen:
            raise BlindRunError("scores line %d: id %r" % (n, vid))
        if vid not in designs:
            raise BlindRunError("scores line %d: %r is not a rubric row"
                                % (n, vid))
        seen.add(vid)
        rows.append({"id": vid, "site": site,
                     "comp": dict(zip(COMPONENTS, (int(m.group(i))
                                                   for i in range(3, 8)))),
                     "need": dict(zip(RESOURCES, (m.group(i)
                                                  for i in range(8, 12)))),
                     "design": designs[vid]})
    reasons = {}
    for ln in text.splitlines():
        m = REASON_RE.match(ln.strip())
        if m:
            key = (m.group(1), m.group(2))
            if key in reasons:
                raise BlindRunError("reason repeated: %s.%s" % key)
            reasons[key] = m.group(3)
    return rows, reasons


def agreement2(scorer, rubric, sc, prop_ids):
    by_r = {r["id"]: r for r in rubric}
    per_field, per_site, far = {}, {s: [0, 0, 0] for s in SITES6}, []
    split = {"admitted": [0, 0, 0], "proposed": [0, 0, 0]}
    for f in FIELDS:
        steps = []
        for row in scorer:
            mine = by_r[row["id"]]
            a, b = CR.field_step(row, f), CR.field_step(mine, f)
            steps.append((a, b))
            cell = CR.field_agreement([(a, b)])
            key = "proposed" if row["id"] in prop_ids else "admitted"
            for i in range(3):
                per_site[row["site"]][i] += cell[i]
                split[key][i] += cell[i]
            if cell[2]:
                far.append((row["id"], f, a, b))
        per_field[f] = CR.field_agreement(steps)
    ranks = {}
    for label, keep in (("admitted", lambda r: r["id"] not in prop_ids),
                        ("with PROPOSED", lambda r: True)):
        s_rows = [r for r in scorer if keep(r)]
        m_rows = [by_r[r["id"]] for r in s_rows]
        for q in sc.QUESTIONS:
            sb = {s: CR.best_ratio(s_rows, s, q, sc) for s in SITES6}
            mb = {s: CR.best_ratio(m_rows, s, q, sc) for s in SITES6}
            ranks[(label, q)] = (sb, mb, CR.comp_rank(sb), CR.comp_rank(mb))
    return {"per_field": per_field, "per_site": per_site, "far": far,
            "split": split, "ranks": ranks}


def render_agreement(ag, scorer, rubric, prop_ids):
    by_r = {r["id"]: r for r in rubric}
    n = len(scorer)
    out = ["# second scorer -> rubric, same row, %d rows (17 admitted, "
           "%d PROPOSED)" % (n, len(prop_ids)),
           "# field     same  1 step  2 steps   (2 steps = more than one "
           "step apart)"]
    for f in FIELDS:
        e, o, t = ag["per_field"][f]
        out.append("%-8s  %5d  %6d  %7d" % (f, e, o, t))
    tot = [sum(ag["per_field"][f][i] for f in FIELDS) for i in range(3)]
    out.append("%-8s  %5d  %6d  %7d   of %d cells"
               % ("all", tot[0], tot[1], tot[2], len(FIELDS) * n))
    for key in ("admitted", "proposed"):
        e, o, t = ag["split"][key]
        out.append("%-8s  %5d  %6d  %7d" % (key[:8], e, o, t))
    out.append("# site      same  1 step  2 steps   (rows x 9 fields)")
    for s in SITES6:
        e, o, t = ag["per_site"][s]
        out.append("%-8s  %5d  %6d  %7d" % (s, e, o, t))
    out.append("# more than one step apart")
    if not ag["far"]:
        out.append("none")
    for rid, f, a, b in ag["far"]:
        out.append("%s  %-7s  scorer %d  rubric %d" % (rid, f, a, b))
    out.append("# row   scorer d u k x r  cost  |  rubric d u k x r  cost"
               "   (cost: compute data lit time, L M H)")
    for row in scorer:
        m = by_r[row["id"]]
        out.append("%s%s  %s  %s   |  %s  %s" % (
            row["id"], "*" if row["id"] in prop_ids else " ",
            " ".join(str(row["comp"][c]) for c in COMPONENTS),
            "".join(CR._lv(row["need"][x]) for x in RESOURCES),
            " ".join(str(m["comp"][c]) for c in COMPONENTS),
            "".join(CR._lv(m["need"][x]) for x in RESOURCES)))
    out.append("# * PROPOSED row (8.2), not in the triage table")
    out.append("# site rank by the best row, declared choices, no profile "
               "gate")
    for label in ("admitted", "with PROPOSED"):
        for q in ("LOOP", "REV"):
            sb, mb, sr, mr = ag["ranks"][(label, q)]
            out.append("Q-%-4s %-13s site  scorer      rank  rubric      "
                       "rank" % (q, label))
            for s in SITES6:
                def val(v):
                    return "NOT_REACHED" if v is None else "%-11.3f" % v

                def rk(v):
                    return "-" if v is None else str(v)
                if sr[s] is None or mr[s] is None:
                    flag = "" if sr[s] == mr[s] else "  reached by one only"
                else:
                    flag = "  moved %d" % abs(sr[s] - mr[s]) \
                        if abs(sr[s] - mr[s]) > 1 else ""
                out.append(("       %-13s %s    %s %-4s  %s %-4s%s"
                            % ("", s, val(sb[s]), rk(sr[s]), val(mb[s]),
                               rk(mr[s]), flag)).rstrip())
    return out


def render_readings(scorer, rubric, sc, prop_ids):
    adm = [r for r in scorer if r["id"] not in prop_ids]
    by_r = {r["id"]: r for r in rubric}
    r_adm = [by_r[r["id"]] for r in adm]
    r_all = [by_r[r["id"]] for r in scorer]
    out = ["# first place over the 64-setting sweep (CHOICE 4, 5)",
           "# profile       question  rubric                    "
           "second scorer"]
    for prof in sorted(sc.PROFILES):
        have = sc.PROFILES[prof]
        for q in sc.QUESTIONS:
            out.append("%-14s Q-%-4s    %-25s %s" % (
                prof, q, sc.sweep(r_adm, have, q)[1],
                sc.sweep(adm, have, q)[1]))
    out.append("# the same with the six PROPOSED rows admitted")
    for prof in sorted(sc.PROFILES):
        have = sc.PROFILES[prof]
        for q in sc.QUESTIONS:
            out.append("%-14s Q-%-4s    %-25s %s" % (
                prof, q, sc.sweep(r_all, have, q)[1],
                sc.sweep(scorer, have, q)[1]))
    return out


def rubric_rows(doc, sc, ca):
    mine = CR.my_rows(sc, ca)
    prop = CR.parse_rows(CR.fenced_any(doc, "triage-proposed"))
    return mine + prop, set(r["id"] for r in prop)


def build(rubric=RUBRIC, run_dir=RUN_DIR):
    doc = CR.read_text(rubric)
    sc = _load(SCORER, "_eft_blind")
    ca = _load(AUDIT_TOOL, "_cc_blind")
    files = {name: CR.read_text(os.path.join(run_dir, name))
             for name in PINNED}
    rows, prop_ids = rubric_rows(doc, sc, ca)
    designs = {r["id"]: r["design"] for r in rows}
    scorer, reasons = parse_scores(files["scores_S.txt"], designs)
    st = {"doc": doc, "sc": sc, "files": files, "rows": rows,
          "prop_ids": prop_ids, "scorer": scorer, "reasons": reasons,
          "listed": CR.read_text(os.path.join(run_dir, "SHA256SUMS")),
          "match_a": CR.parse_match(CR.fenced_any(doc, "blind-match-a")),
          "match": CR.parse_match(CR.fenced_any(doc, "blind-match"))}
    st["ag"] = agreement2(scorer, rows, sc, prop_ids)
    st["agree_lines"] = render_agreement(st["ag"], scorer, rows, prop_ids)
    st["read_lines"] = render_readings(scorer, rows, sc, prop_ids)
    return st


def _stated_counts(doc, label):
    m = re.search(COUNTS_RE % re.escape(label), doc)
    return None if m is None else tuple(int(x) for x in m.groups())


def checks(st):
    doc, files = st["doc"], st["files"]
    out = []

    def check(name, ok, detail=""):
        out.append((name, bool(ok), detail))

    for name, want in sorted(PINNED.items()):
        got = CR.sha(files[name])
        check("%s matches its pinned sha256" % name, got == want, got[:16])
    want_list = "".join("%s  %s\n" % (PINNED[n], n) for n in sorted(PINNED))
    check("SHA256SUMS lists every pinned file and hash",
          st["listed"] == want_list)
    check("the rubric's blind-run-files block is SHA256SUMS",
          CR.fenced_any(doc, "blind-run-files") == st["listed"])
    terms = strip_targets(files["anchor_facts.txt"])
    check("anchor_facts.txt carries its strip-target list", len(terms) >= 10,
          str(len(terms)))
    for name in ("packet_T.txt", "stage1_message.txt",
                 "stage2_message.txt"):
        hits = target_hits(files[name], terms)
        check("%s carries no strip target" % name, not hits,
              ", ".join(hits))
    check("the recorded miss is in the packet (7.9, K-P2)",
          RECORDED_MISS in CR_norm(files["packet_T.txt"]))
    packet = source_text(files["packet_T.txt"])
    bad = unsourced(files["fill_A.txt"], packet)
    check("every stage-1 SRC quote is in the packet", not bad,
          " | ".join(bad))
    g_src = packet + " " + source_text(g_definition(
        files["stage2_message.txt"]))
    bad = unsourced(files["fill_G.txt"], g_src)
    check("every stage-2 SRC quote is in the packet or the (g) definition",
          not bad, " | ".join(bad))
    for name, mark in ANSWER_MARKS:
        check("%s says %r" % (name, mark), mark in files[name])
    ids = tuple(r["id"] for r in st["scorer"])
    check("the second scorer scored the 23 rows, in order",
          ids == SCORED_IDS, ", ".join(ids))
    check("the 23 rows are the rubric's admitted rows plus the PROPOSED",
          set(SCORED_IDS) == set(r["id"] for r in st["rows"]))
    gaps = [(v, c) for v in SCORED_IDS for c in COMPONENTS + ("cost",)
            if (v, c) not in st["reasons"]]
    check("every scored component and cost has its reason (138 lines)",
          not gaps and len(st["reasons"]) == 138,
          ", ".join("%s.%s" % g for g in gaps[:6]))
    for label, rows in (("stage 1", st["match_a"]),
                        ("stages 1-2", st["match"])):
        facts = tuple(r["fact"] for r in rows)
        check("comparison, %s, covers T1..T7 once each in order" % label,
              facts == FACTS, ", ".join(facts))
        cnt = CR.match_counts(rows)
        check("the stated counts, site T, %s, are the table's" % label,
              _stated_counts(doc, label) ==
              tuple(cnt[s] for s in MATCH_STATES),
              " ".join("%s %d" % (s, cnt[s]) for s in MATCH_STATES))
    got = CR.fenced_any(doc, "scorer2-agreement").rstrip("\n").split("\n")
    check("scorer2-agreement block is what this module computes",
          got == st["agree_lines"], CR._first_diff(got, st["agree_lines"]))
    got = CR.fenced_any(doc, "scorer2-readings").rstrip("\n").split("\n")
    check("scorer2-readings block is what this module computes",
          got == st["read_lines"], CR._first_diff(got, st["read_lines"]))
    check("section 7.9 states BLIND", "Status: **BLIND**, for this anchor."
          in doc)
    check("section 8.3 states CONTAMINATED-BY-PRIOR",
          "### 8.3" in doc and "CONTAMINATED-BY-PRIOR" in
          doc.split("### 8.3", 1)[1].split("\n## ", 1)[0])
    check("section 9 keeps the training-cutoff line",
          "Blindness depends on the reader's training cutoff" in doc
          and "Keep this line." in doc)
    check("the first clean run's files are untouched",
          not [n for n in CR.PINNED if CR.sha(CR.read_text(
              os.path.join(CR.RUN_DIR, n))) != CR.PINNED[n]])
    return out


def unit_checks():
    out = []

    def check(name, ok, detail=""):
        out.append((name, bool(ok), detail))

    check("source_text joins a word split by a line-break hyphen",
          source_text("bidirectional-\npass-through") ==
          "bidirectional-pass-through")
    check("source_text leaves an ordinary hyphen alone",
          source_text("a two-step test") == "a two-step test")
    terms = strip_targets("x\n\nSTRIP TARGETS. None of these may appear in "
                          "the packet the reader gets:\nrole, \"not fixed\""
                          ", 15.\n")
    check("strip_targets reads a comma list, quotes and stop removed",
          terms == ["role", "not fixed", "15"], repr(terms))
    check("target_hits: 'role' does not fire inside 'control'",
          target_hits("a control arm", ["role"]) == [])
    check("target_hits: a listed stem fires on its word",
          target_hits("units removed", ["remov"]) == ["remov"])
    check("unsourced: a quote absent from the source is returned",
          unsourced('SRC    "abc" | "xyz"', "abc def") == ["xyz"])
    designs = {"S1a": "design"}
    rows, reasons = parse_scores(
        "S1a   S1    2 1 2 2 1  low low low low\nS1a.d why\n"
        "S1a.cost cheap\n", designs)
    check("parse_scores reads a row without a design and its reasons",
          rows[0]["comp"]["d"] == 2 and rows[0]["design"] == "design"
          and ("S1a", "cost") in reasons)
    try:
        parse_scores("S1b   S1    2 1 2 2 1  low low low low\n", designs)
        refused = False
    except BlindRunError:
        refused = True
    check("parse_scores refuses an id that is not a rubric row", refused)
    return out


def planted(st):
    """Each plant must turn at least one check red."""
    out = []
    doc = st["doc"]
    match = CR.fenced_any(doc, "blind-match")
    agree = CR.fenced_any(doc, "scorer2-agreement")
    plants = (
        ("an edited stage-1 fill", None, ("fill_A.txt", "FOUND", "FOUNDX")),
        ("a strip target added to the packet", None,
         ("packet_T.txt", "temporal pattern?", "temporal pattern and role?")),
        ("a comparison state changed without its counts",
         (match, match.replace("| NO_SLOT |", "| PARTIAL |", 1)), None),
        ("a hand-edited agreement block",
         (agree, agree.replace(" of 207 cells", " of 208 cells", 1)), None),
    )
    for name, doc_edit, file_edit in plants:
        tmp = tempfile.mkdtemp(prefix="blind_run_plant_")
        try:
            rub = os.path.join(tmp, "rubric.md")
            run = os.path.join(tmp, "run")
            os.mkdir(run)
            text = doc if doc_edit is None else \
                doc.replace(doc_edit[0], doc_edit[1], 1)
            changed = text != doc
            with open(rub, "w", encoding="utf-8") as fh:
                fh.write(text)
            for n in list(PINNED) + ["SHA256SUMS"]:
                body = st["files"].get(n, st["listed"])
                if file_edit and n == file_edit[0]:
                    new = body.replace(file_edit[1], file_edit[2], 1)
                    changed = changed or new != body
                    body = new
                with open(os.path.join(run, n), "w", encoding="utf-8") as fh:
                    fh.write(body)
            try:
                bad = any(not ok for _, ok, _ in checks(build(rub, run)))
            except (BlindRunError, KeyError, ValueError):
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
    L = ["BLIND CALIBRATION ON SITE T, INDEPENDENT SECOND SCORER  "
         "(tools/triage_blind_run.py)"]
    for label, rows in (("stage 1", st["match_a"]),
                        ("stages 1-2", st["match"])):
        cnt = CR.match_counts(rows)
        L.append("comparison, %-10s %s" % (label + ":", "  ".join(
            "%s %d" % (s, cnt[s]) for s in MATCH_STATES)))
    L.extend(st["agree_lines"])
    L.extend(st["read_lines"])
    return L


def main(argv):
    try:
        st = build()
    except (OSError, BlindRunError, KeyError) as exc:
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
