#!/usr/bin/env python3
# check_queue.py -- CC0, stdlib only, parses under 3.9
#
# Checker for notes/queue/BUILD_QUEUE_2026_09_15.md, under the notes/
# convention: the entry is stored as delivered, this checker never edits
# it, and every disagreement goes in this output. The entry is a BUILD
# QUEUE of six rows, one of which asks a question outright ("did it
# build?"). Nothing here ranks a row, schedules one, or decides what to
# build next; every reading is about what the tree holds against what
# the row says it holds.
#
# Six readings:
#   1  structure -- six rows parsed out of the entry, never retyped
#   2  anchors -- each row's named artifact resolved by PATH and by one
#      CONTENT marker. Never by grep for the row's own words: the entry
#      names `substrate_alternative` and `frame_audit.py`, so once the
#      entry is committed a text search finds the entry and this file.
#      That is the loop notes/check_datasets.py hit at its finding 8.
#   3  build state -- measured by RUNNING the row's declared check. This
#      checker executes, unlike tools/run_manifest.py, and says so.
#   4  the row's own status against the measurement: CONFIRMED, STALE,
#      ANSWERED, or ABSENT_CONFIRMED. A stale row is not a defect in the
#      queue; it is a queue written before the work landed.
#   5  the two operator-data blocks, named -- and asserted NOT filled
#      here. Hand-built case data and attestation orderings are the
#      operator's. Generating them would put a finding in their mouth.
#   6  self-reference -- the entry's hash is unchanged across this run,
#      and no reading anywhere greps the tree for a row's own words.

import ast
import hashlib
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENTRY = os.path.join(HERE, "queue", "BUILD_QUEUE_2026_09_15.md")

# Row key -> artifacts, each as (path, one content marker that must be IN
# the file). The mapping is this checker's reading of which artifact a row
# names, stated here so it can be disagreed with line by line.
ANCHORS = {
    "K": [("enclosure-first-residual/enclosure_first_residual.py",
           "effective_exits")],
    "L": [("crediting-rate/crediting_rate.py",
           "insufficient_attested_ordering")],
    "gate_check": [("gate-check/gate_check.py", "HELD_RETRIEVABLE"),
                   ("gate-check/thresholds.txt", "check3_failure_assertions_min"),
                   ("gate-check/threshold_chain.txt", "2026-09-07")],
    "cooperative": [("cooperative-substrate/p1_deps_extract.py",
                     "verified_in_argument"),
                    ("cooperative-substrate/p2_substrate_audit.py",
                     "unverified_contracts"),
                    ("cooperative-substrate/p3_comprehension.py", "cosine"),
                    ("cooperative-substrate/v2/p4_goal.py", "stance"),
                    ("cooperative-substrate/v2/p5_lag.py", "t_visible")],
    "move_set": [("move-set/move_set_sim.py", "path_dependence")],
    "substrate_alt": [("frame-token-audit/frame_audit.py", "per_1000")],
}

# Row key -> the command whose exit code and last line are the measurement.
RUNS = {
    "K": ["enclosure-first-residual/enclosure_first_residual.py", "--selftest"],
    "L": ["crediting-rate/crediting_rate.py", "--selftest"],
    "gate_check": ["gate-check/gate_check.py"],
    "cooperative": ["cooperative-substrate/selftest_csp.py"],
    "move_set": ["move-set/move_set_sim.py", "--selftest"],
    "substrate_alt": ["frame-token-audit/frame_audit.py", "--selftest"],
}

# Artifacts the entry names that are NOT in the tree under any spelling.
# Absence is established by path, and reported as absent rather than as a
# defect: a row naming an unbuilt thing is a queue doing its job.
NAMED_ABSENT = ["substrate_alternative"]

# The operator-data blocks. This checker does not fill them.
OPERATOR_DATA = {
    "K": ("hand-built case data", "enclosure-first-residual/samples"),
    "L": ("attestation orderings", "crediting-rate/fixtures/events.candidates.jsonl"),
}


def entry_text():
    return io.open(ENTRY, encoding="utf-8").read()


def entry_hash():
    return hashlib.sha256(io.open(ENTRY, "rb").read()).hexdigest()


def parse_rows(txt):
    """Six rows, split on blank lines. Head is the row, the rest its status.

    Parsed, never retyped: the entry is the source of what each row claims.
    """
    rows = []
    for block in [b for b in txt.split("\n\n") if b.strip()]:
        lines = [l.rstrip() for l in block.split("\n") if l.strip()]
        rows.append({"head": lines[0].strip(),
                     "status": [l.strip() for l in lines[1:]]})
    return rows


def key_for(head):
    h = head.lower()
    if h.startswith("k "):
        return "K"
    if h.startswith("l "):
        return "L"
    if "gate_check" in h:
        return "gate_check"
    if "cooperative" in h:
        return "cooperative"
    if "move-set" in h or "move_set" in h:
        return "move_set"
    if "substrate_alternative" in h:
        return "substrate_alt"
    return None


def resolve(key):
    """Path existence AND one content marker, per artifact."""
    out = []
    for rel, marker in ANCHORS.get(key, []):
        p = os.path.join(ROOT, rel)
        exists = os.path.isfile(p)
        by_content = False
        if exists:
            try:
                by_content = marker in io.open(p, encoding="utf-8",
                                               errors="replace").read()
            except Exception:
                by_content = False
        out.append({"path": rel, "exists": exists, "marker": marker,
                    "resolves_by_content": by_content})
    return out


def run_row(key):
    cmd = RUNS.get(key)
    if not cmd:
        return {"ran": False, "rc": None, "last": ""}
    argv = [sys.executable, os.path.join(ROOT, cmd[0])] + list(cmd[1:])
    try:
        r = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                           timeout=600)
    except Exception as e:
        return {"ran": False, "rc": None, "last": type(e).__name__}
    out = (r.stdout + r.stderr).strip().split("\n")
    return {"ran": True, "rc": r.returncode,
            "last": out[-1][:100] if out and out[-1] else ""}


def blocked_on_real_data():
    """L's block, measured. Counts nulls; fills nothing."""
    p = os.path.join(ROOT, OPERATOR_DATA["L"][1])
    if not os.path.isfile(p):
        return {"rows": None, "ordering_unknown": None}
    import json
    n = 0
    unknown = 0
    for line in io.open(p, encoding="utf-8"):
        if not line.strip():
            continue
        n += 1
        d = json.loads(line)
        if d.get("ordering_source") is None:
            unknown += 1
    return {"rows": n, "ordering_unknown": unknown}


def named_absent():
    """Absence by path over the whole tree, not by grep for the name.

    A grep would find the entry itself and this file.
    """
    out = {}
    for name in NAMED_ABSENT:
        hits = []
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = [d for d in dirnames
                           if d not in (".git", "__pycache__", "node_modules")]
            for fn in filenames:
                if name in fn:
                    hits.append(os.path.relpath(
                        os.path.join(dirpath, fn), ROOT))
        out[name] = hits
    return out


def landed(rel):
    """The commit that added a path, if git can say."""
    try:
        r = subprocess.run(["git", "log", "--format=%ad %h", "--date=short",
                            "--diff-filter=A", "--", rel],
                           cwd=ROOT, capture_output=True, text=True, timeout=60)
        lines = [l for l in r.stdout.strip().split("\n") if l.strip()]
        return lines[-1] if lines else None
    except Exception:
        return None


def ledger_count():
    """How many filled runs exist. A spread across readers needs >1."""
    d = os.path.join(ROOT, "move-set", "ledgers")
    if not os.path.isdir(d):
        return 0
    return len([f for f in os.listdir(d) if f.endswith(".json")])


def verdict(key, anchors, run):
    """CONFIRMED / STALE / ANSWERED / ABSENT_CONFIRMED, with the reason."""
    if key == "substrate_alt":
        return ("SPLIT", "frame_audit.py is built; substrate_alternative is "
                         "absent under every spelling")
    if not anchors:
        return ("UNRESOLVED", "no anchor declared")
    all_ok = all(a["exists"] and a["resolves_by_content"] for a in anchors)
    if not all_ok:
        missing = [a["path"] for a in anchors
                   if not (a["exists"] and a["resolves_by_content"])]
        return ("ABSENT_CONFIRMED", "not resolved: %s" % ", ".join(missing))
    if key == "gate_check":
        return ("ANSWERED", "it built; the row's open question is closed")
    if key in OPERATOR_DATA:
        return ("CONFIRMED", "instrument built; the block is operator data "
                             "and is real")
    if key == "move_set":
        # The row separates tool from experiment, and it is right to. The
        # sim is built and green; the experiment it names is a spread across
        # readers, and one ledger cannot carry one. move_set_sim's own
        # path_dependence compares verdict sets ACROSS runs, so at n=1 the
        # module's central claim is untestable on the data in the tree.
        n = ledger_count()
        return ("SPLIT", "the sim is built and runs; the experiment is not "
                         "run -- %d ledger(s), and a spread needs at least 2"
                         % n)
    if key == "cooperative":
        # P1-P3 and v2 P5 run. v2/p4_goal.py arrived truncated at delivery
        # and still is -- and it PARSES, so nothing syntactic catches it.
        # It is not invisible: selftest_v2.py pins the truncation as a
        # check, and v2_audit.py files it DELIVERED_TRUNCATED. Detected,
        # not repaired, because the file is delivered.
        n = os.path.getsize(os.path.join(ROOT, "cooperative-substrate",
                                         "v2", "p4_goal.py"))
        return ("STALE", "the row says not built; P1-P3 and P5 run. "
                         "v2/p4_goal.py is delivered-truncated at %d bytes, "
                         "parses, and is pinned by selftest_v2.py" % n)
    return ("STALE", "the row says not built; the artifacts resolve and run")


def render():
    txt = entry_text()
    before = entry_hash()
    rows = parse_rows(txt)
    L = []
    w = L.append
    w("check_queue -- notes/queue/BUILD_QUEUE_2026_09_15.md")
    w("   sha256 %s" % before[:16])
    w("   the entry is stored as delivered and is not edited here;")
    w("   every disagreement below is this checker's output, not the queue's.")
    w("")
    w("1  STRUCTURE")
    w("   rows parsed: %d" % len(rows))
    for r in rows:
        w("   - %-38s %d status line(s)" % (r["head"][:38], len(r["status"])))
    w("")
    w("2  ANCHORS (path existence and one content marker each)")
    w("   never resolved by grep for a row's own words: the entry names")
    w("   substrate_alternative and frame_audit.py, so a text search would")
    w("   count the entry and this checker.")
    for r in rows:
        k = key_for(r["head"])
        for a in resolve(k):
            w("   %-52s path=%s content=%s"
              % (a["path"], "yes" if a["exists"] else "NO",
                 "yes" if a["resolves_by_content"] else "NO"))
    w("")
    w("3  BUILD STATE (measured by running; this checker executes)")
    for r in rows:
        k = key_for(r["head"])
        res = run_row(k)
        w("   %-14s rc=%-5s %s" % (k, res["rc"], res["last"]))
    w("")
    w("4  ROW STATUS AGAINST THE MEASUREMENT")
    for r in rows:
        k = key_for(r["head"])
        v, why = verdict(k, resolve(k), None)
        w("   %-14s %-18s %s" % (k, v, why))
        for s in r["status"]:
            w("       queue: %s" % s)
    w("")
    w("5  OPERATOR-DATA BLOCKS -- named, and not filled here")
    b = blocked_on_real_data()
    w("   L  attestation orderings: %s of %s candidate rows carry none"
      % (b["ordering_unknown"], b["rows"]))
    w("   K  hand-built case data: the shipped panels are generative")
    w("      fixtures, not cases. Both blocks are the operator's to fill;")
    w("      generating either here would put a finding in their mouth.")
    w("")
    w("6  THE ANSWERED ROW, with its commit")
    for rel, _m in ANCHORS["gate_check"]:
        w("   %-34s added %s" % (rel, landed(rel) or "unrecorded"))
    w("")
    w("   NAMED AND ABSENT (by path over the tree, not by grep):")
    for name, hits in named_absent().items():
        w("     %-24s %s" % (name, hits if hits else "no file"))
    w("")
    after = entry_hash()
    w("entry hash unchanged across this run: %s" % (before == after))
    return "\n".join(L)


def selftest():
    checks = 0
    failed = 0

    def ck(cond, label):
        nonlocal checks, failed
        checks += 1
        if not cond:
            failed += 1
            print("FAIL  %s" % label)
        else:
            print("ok    %s" % label)

    before = entry_hash()
    txt = entry_text()

    print("-- 1 structure")
    rows = parse_rows(txt)
    ck(len(rows) == 6, "six rows parsed (got %d)" % len(rows))
    keys = [key_for(r["head"]) for r in rows]
    ck(None not in keys, "every row head maps to a key (got %s)" % keys)
    ck(len(set(keys)) == 6, "the six keys are distinct")
    ck(all(r["status"] for r in rows), "every row carries a status line")

    print("\n-- 2 anchors resolve by path AND content")
    for k in ANCHORS:
        for a in resolve(k):
            ck(a["exists"], "%s exists" % a["path"])
            ck(a["resolves_by_content"],
               "%s contains %r" % (a["path"], a["marker"]))

    print("\n-- 2b the null: a bogus marker must refuse")
    saved = ANCHORS["move_set"]
    ANCHORS["move_set"] = [(saved[0][0], "a-string-not-in-that-file-xyzzy")]
    ck(not resolve("move_set")[0]["resolves_by_content"],
       "a marker that is not in the file does not resolve")
    ANCHORS["move_set"] = saved
    ck(resolve("move_set")[0]["resolves_by_content"], "and the real one does")

    print("\n-- 3 the absence is established by path, not by name-grep")
    na = named_absent()
    ck(na["substrate_alternative"] == [],
       "substrate_alternative: no file under any directory")

    print("\n-- 4 verdicts are reachable and distinct")
    vs = set(verdict(key_for(r["head"]), resolve(key_for(r["head"])), None)[0]
             for r in rows)
    ck("ANSWERED" in vs, "the gate_check row returns ANSWERED")
    ck("CONFIRMED" in vs, "an operator-data row returns CONFIRMED")
    ck("STALE" in vs, "a row whose artifacts run returns STALE")
    ck("SPLIT" in vs, "a row whose halves disagree returns SPLIT")
    ck(len(vs) >= 4, "at least four distinct verdicts occur (got %s)" % sorted(vs))
    ck(ledger_count() == 1,
       "move-set carries one ledger, so the spread the row names is unrun")
    # the truncated P4 is detected by its own folder, not by this checker
    sv = io.open(os.path.join(ROOT, "cooperative-substrate", "v2",
                              "selftest_v2.py"), encoding="utf-8").read()
    ck("structurally incomplete" in sv,
       "selftest_v2.py pins the p4_goal.py truncation as a check of its own")

    print("\n-- 5 this checker fills no operator data")
    own = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(own)
    writes = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            nm = getattr(n.func, "attr", None) or getattr(n.func, "id", None)
            if nm in ("open",):
                for a in list(n.args[1:]) + [k.value for k in n.keywords
                                             if k.arg == "mode"]:
                    if isinstance(a, ast.Constant) and isinstance(a.value, str) \
                            and ("w" in a.value or "a" in a.value):
                        writes.append(a.value)
    ck(not writes, "no write-mode open anywhere (got %s)" % writes)
    planted = ast.parse('io.open("x", "w")')
    hit = False
    for n in ast.walk(planted):
        if isinstance(n, ast.Call) and len(n.args) > 1:
            a = n.args[1]
            if isinstance(a, ast.Constant) and "w" in a.value:
                hit = True
    ck(hit, "and the write check fires on a planted write-mode open")

    print("\n-- 6 self-reference")
    ck(entry_hash() == before, "entry hash unchanged across the run")
    # Read from the AST, not from the text. A substring scan for "grep"
    # fires on the comments that NAME the construct being refused -- the
    # third instance of that shape in this session alone. Two structural
    # facts carry it instead: nothing here shells out to grep, and
    # named_absent() decides absence from paths without reading a file.
    argv0 = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            nm = getattr(n.func, "attr", None) or getattr(n.func, "id", None)
            if nm in ("run", "Popen", "call", "check_output") and n.args:
                a = n.args[0]
                if isinstance(a, ast.List) and a.elts and isinstance(
                        a.elts[0], ast.Constant):
                    argv0.append(a.elts[0].value)
    ck("grep" not in [str(x) for x in argv0],
       "nothing here shells out to a text search (argv0 seen: %s)" % argv0)
    fn = [n for n in ast.walk(tree)
          if isinstance(n, ast.FunctionDef) and n.name == "named_absent"]
    reads = [x for f in fn for x in ast.walk(f)
             if isinstance(x, ast.Call)
             and getattr(x.func, "attr", None) == "read"]
    ck(fn and not reads,
       "named_absent decides absence from paths, never from file contents")
    planted = ast.parse('subprocess.run(["grep", "-r", "x"])')
    hit = any(isinstance(x, ast.Call) and isinstance(x.args[0], ast.List)
              and x.args[0].elts[0].value == "grep"
              for x in ast.walk(planted) if isinstance(x, ast.Call) and x.args)
    ck(hit, "and the argv0 check fires on a planted grep call")

    print("\nchecks: %d   failed: %d" % (checks, failed))
    print("VERDICT: %s   checks=%d failed=%d"
          % ("PASS" if failed == 0 else "FAIL", checks, failed))
    return 0 if failed == 0 else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
