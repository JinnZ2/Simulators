#!/usr/bin/env python3
"""Checks for the cooperative-substrate-proof artifact.

    python3 test_proof.py

Every module in the folder refuses --selftest and names this file. The
count is printed here and is not stored anywhere in prose.
"""

import ast
import os
import subprocess
import sys
import tempfile

import p1_records
import p2_substrate
import p3_comprehension
import p4_coherence
import p5_lag
import run_all
import scope

HERE = os.path.dirname(os.path.abspath(__file__))
MODULES = ("scope.py", "p1_records.py", "p2_substrate.py",
           "p3_comprehension.py", "p4_coherence.py", "p5_lag.py",
           "run_all.py")

PASSED = []
FAILED = []


def check(label, cond):
    (PASSED if cond else FAILED).append(label)


def raises(exc, fn, *a, **k):
    try:
        fn(*a, **k)
    except exc:
        return True
    except Exception:
        return False
    return False


# ---------------------------------------------------------------- 1 scope

def sec_scope():
    r = scope.code({"C1": True, "C2": True, "C3": True, "C4": True})
    check("scope: all four hold -> WITHIN", r["verdict"] == scope.WITHIN)
    r = scope.code({"C1": True, "C2": False, "C3": True, "C4": True})
    check("scope: one fails -> OUTSIDE", r["verdict"] == scope.OUTSIDE)
    check("scope: the failing condition is named", r["failed"] == ["C2"])
    r = scope.code({"C1": True, "C2": True, "C3": True})
    check("scope: an uncoded condition -> UNDECLARED",
          r["verdict"] == scope.UNDECLARED and r["undeclared"] == ["C4"])
    check("scope: UNDECLARED outranks OUTSIDE, so a silence is never"
          " read as a failure",
          scope.code({"C2": False, "C3": None, "C4": True,
                      "C1": True})["verdict"] == scope.UNDECLARED)
    check("scope: all three verdicts are reachable",
          len({scope.code({"C1": True, "C2": True, "C3": True,
                           "C4": True})["verdict"],
               scope.code({"C1": False, "C2": True, "C3": True,
                           "C4": True})["verdict"],
               scope.code({})["verdict"]}) == 3)
    check("scope: C1 holds at the margin",
          scope.c1_time_scoped(1.0, 1.0) is True)
    check("scope: C1 fails past the margin",
          scope.c1_time_scoped(1.01, 1.0) is False)
    check("scope: a missing window is None, not False",
          scope.c1_time_scoped(None, 1.0) is None)
    check("scope: a missing coupling time is None, not False",
          scope.c1_time_scoped(1.0, None) is None)
    check("scope: a non-positive coupling time is None, not a ratio",
          scope.c1_time_scoped(1.0, 0.0) is None)
    check("scope: two quantities in different units are None, not a ratio",
          scope.c1_time_scoped(1.0, 30.0, "day", "second") is None)
    check("scope: matching units are read",
          scope.c1_time_scoped(1.0, 30.0, "day", "day") is True)
    check("scope: an unreadable condition value raises rather than"
          " defaulting",
          raises(scope.ScopeInputError, scope.code, {"C1": "maybe"}))
    check("scope: no verdict member says one frame is preferable",
          all("better" not in v.lower() and "worse" not in v.lower()
              for v in (scope.WITHIN, scope.OUTSIDE, scope.UNDECLARED)))
    check("scope: the reading for OUTSIDE says the observation stands",
          "observation stands" in scope.reading(scope.OUTSIDE, [], ["C2"]))


# -------------------------------------------------------- 2 p3 arithmetic

def sec_p3_math():
    g = p3_comprehension.gain_from_sizes
    check("p3: gain arithmetic", abs(g(100, 100, 120) - 0.4) < 1e-12)
    check("p3: no gain is a measured 0.0, not None",
          g(100, 100, 200) == 0.0)
    check("p3: a negative gain is returned as measured",
          abs(g(100, 100, 220) + 0.1) < 1e-12)
    check("p3: an absent size is None, not 0.0", g(100, None, 120) is None)
    check("p3: a zero denominator is None, not a division",
          g(0, 0, 0) is None)
    check("p3: csize of empty is None, not 0", p3_comprehension.csize("") is None)
    check("p3: csize of text is a positive int",
          isinstance(p3_comprehension.csize("hello"), int))


# ----------------------------------------------------------- 3 p3 cipher

def sec_p3_cipher():
    enc = p3_comprehension.encipher
    text = open(os.path.join(HERE, "fixtures", "corpus", "a_units.txt"),
                encoding="utf-8").read()
    c = enc(text, 3)
    check("p3: cipher preserves length exactly", len(c) == len(text))
    check("p3: cipher preserves non-letters",
          all((a == b) or (a.isalpha() and b.isalpha())
              for a, b in zip(text, c)))
    check("p3: cipher preserves case",
          all(a.isupper() == b.isupper() for a, b in zip(text, c)
              if a.isalpha()))
    ct, cc = p3_comprehension.csize(text), p3_comprehension.csize(c)
    check("p3: cipher preserves compressibility to within 2 percent,"
          " which is what makes it a control and a token rename not",
          abs(ct - cc) / float(ct) < 0.02)
    check("p3: cipher is a bijection on the alphabet",
          sorted(p3_comprehension.cipher_alphabet(0)) == list(
              p3_comprehension.ALPHABET))
    check("p3: cipher is consistent within a document",
          enc("aa bb aa", 1) == enc("aa bb aa", 1))
    check("p3: a different seed is a different cipher",
          p3_comprehension.cipher_alphabet(0)
          != p3_comprehension.cipher_alphabet(1))
    fixed = sum(1 for a, b in zip(p3_comprehension.ALPHABET,
                                  p3_comprehension.cipher_alphabet(0))
                if a == b)
    check("p3: the shipped seed has at most 3 fixed points (recorded,"
          " not forced: %d)" % fixed, fixed <= 3)


# ------------------------------------------------------------ 4 p3 verdicts

def sec_p3_verdicts():
    corpus = p3_comprehension.read_corpus(
        os.path.join(HERE, "fixtures", "corpus"))
    check("p3: only .txt enters the corpus, so the README documenting"
          " the fixtures cannot become one of them",
          [n for n, _ in corpus] == ["a_units.txt", "b_protocol.txt",
                                     "c_ciphered.txt"])
    res = p3_comprehension.check(corpus)
    by = {(r["a"], r["b"]): r for r in res["pairs"]}
    ab = by[("a_units.txt", "b_protocol.txt")]
    ac = by[("a_units.txt", "c_ciphered.txt")]
    check("p3: the shared-terms pair lands on SHARED_TERMS",
          ab["verdict"] == p3_comprehension.SHARED_TERMS)
    check("p3: the ciphered control lands on SHARED_FORM_ONLY",
          ac["verdict"] == p3_comprehension.SHARED_FORM_ONLY)
    check("p3: the control separates by at least an order of magnitude"
          " from the threshold (%.4f vs %.4f)"
          % (ab["delta"], p3_comprehension.DELTA_MIN),
          ab["delta"] > 10 * p3_comprehension.DELTA_MIN)
    check("p3: the control's delta sits below the threshold",
          ac["delta"] < p3_comprehension.DELTA_MIN)
    check("p3: both verdicts occur in one corpus, so neither branch is"
          " constant",
          len({r["verdict"] for r in res["pairs"]}) == 2)
    check("p3: fewer than two documents is NOT_EVALUABLE with a reason,"
          " not a clean pass",
          p3_comprehension.check([("x", "hello")])["verdict"]
          == p3_comprehension.NOT_EVALUABLE)
    check("p3: an empty document is NOT_EVALUABLE, not a zero gain",
          p3_comprehension.pair_reading("", "text")["verdict"]
          == p3_comprehension.NOT_EVALUABLE)
    long_a = "the same sentence repeated. " * 40
    check("p3: NO_SHARED_FORM is reachable",
          p3_comprehension.pair_reading(
              "a", long_a)["verdict"] in (p3_comprehension.NO_SHARED_FORM,
                                          p3_comprehension.SHARED_FORM_ONLY,
                                          p3_comprehension.SHARED_TERMS))
    wl = p3_comprehension.weakest_link
    check("p3: the corpus verdict is the weakest pair, not the"
          " commonest -- every link must transmit",
          wl([{"verdict": p3_comprehension.SHARED_TERMS},
              {"verdict": p3_comprehension.SHARED_TERMS},
              {"verdict": p3_comprehension.NO_SHARED_FORM}])
          == p3_comprehension.NO_SHARED_FORM)
    check("p3: a corpus whose every pair shares terms reports so",
          wl([{"verdict": p3_comprehension.SHARED_TERMS}])
          == p3_comprehension.SHARED_TERMS)
    check("p3: the shipped corpus reports SHARED_FORM_ONLY, the"
          " weakest of its three pairs",
          res["verdict"] == p3_comprehension.SHARED_FORM_ONLY)
    check("p3: a document paired with itself shows the strongest drop,"
          " which is the shape the reading depends on",
          p3_comprehension.pair_reading(long_a, long_a)["delta"]
          > ac["delta"])


# ------------------------------------------------------------- 5 p4 schema

def sec_p4_schema():
    rc = p4_coherence.read_chain
    check("p4: a chain with no steps is refused",
          raises(p4_coherence.ChainError, rc, {"steps": []}))
    check("p4: a step with no id is refused",
          raises(p4_coherence.ChainError, rc, {"steps": [{"does": "x"}]}))
    check("p4: a duplicate id is refused",
          raises(p4_coherence.ChainError, rc,
                 {"steps": [{"id": "a"}, {"id": "a"}]}))
    check("p4: an edge naming a step that does not exist is refused,"
          " not dropped",
          raises(p4_coherence.ChainError, rc,
                 {"steps": [{"id": "a", "accepts": ["ghost"]}]}))
    check("p4: a step accepting itself is refused",
          raises(p4_coherence.ChainError, rc,
                 {"steps": [{"id": "a", "accepts": ["a"]}]}))
    check("p4: a non-integer contest_limit is refused",
          raises(p4_coherence.ChainError, rc,
                 {"steps": [{"id": "a", "contest_limit": "one"}]}))
    check("p4: a negative contest_limit is refused",
          raises(p4_coherence.ChainError, rc,
                 {"steps": [{"id": "a", "contest_limit": -1}]}))
    check("p4: an absent contest_limit reads as unbounded, not as zero",
          rc({"steps": [{"id": "a"}]})["steps"]["a"]["contest_limit"]
          is None)


# ----------------------------------------------------------- 6 p4 verdicts

def sec_p4_verdicts():
    out = {}
    for obj in p4_coherence.CHAINS:
        c = p4_coherence.read_chain(obj)
        out[c["label"]] = p4_coherence.settle(c)
    check("p4: the cooperative chain SETTLES with no rework",
          out["cooperative"]["verdict"] == p4_coherence.SETTLES
          and out["cooperative"]["rework"] == 0)
    check("p4: the corrective chain SETTLES_WITH_REWORK -- correction"
          " costs and finishes",
          out["corrective"]["verdict"] == p4_coherence.SETTLES_WITH_REWORK
          and out["corrective"]["rework"] > 0)
    check("p4: the turf-war chain produces NO_ANSWER",
          out["turf_war"]["verdict"] == p4_coherence.NO_ANSWER)
    check("p4: the turf-war reason is structural, not budget_exhausted",
          out["turf_war"]["reason"] == "contest_loop")
    check("p4: both sabotaging steps are named",
          set(out["turf_war"]["involved"]) == {"agent_a", "agent_b"})
    check("p4: all three outcomes occur across the shipped chains,"
          " so no verdict is constant",
          len({r["verdict"] for r in out.values()}) == 3)

    unbounded = {"label": "x", "steps": [
        {"id": "p"}, {"id": "d", "accepts": ["p"]},
        {"id": "k", "accepts": ["d"], "contests": ["d"]}]}
    r = p4_coherence.settle(p4_coherence.read_chain(unbounded))
    check("p4: the SAME chain with the limit removed becomes NO_ANSWER,"
          " which is the cut the field carries",
          r["verdict"] == p4_coherence.NO_ANSWER
          and r["reason"] == "contest_loop")
    bounded = {"label": "x", "steps": [
        {"id": "p"}, {"id": "d", "accepts": ["p"]},
        {"id": "k", "accepts": ["d"], "contests": ["d"],
         "contest_limit": 1}]}
    check("p4: and with the limit restored it settles again",
          p4_coherence.settle(p4_coherence.read_chain(bounded))["verdict"]
          == p4_coherence.SETTLES_WITH_REWORK)
    cyc = {"label": "x", "steps": [
        {"id": "a", "accepts": ["b"]}, {"id": "b", "accepts": ["a"]}]}
    r = p4_coherence.settle(p4_coherence.read_chain(cyc))
    check("p4: an accepts cycle is NO_ANSWER for its own reason",
          r["verdict"] == p4_coherence.NO_ANSWER
          and r["reason"] == "accepts_cycle")
    check("p4: nothing in the settle loop reads the content of a step",
          "does" not in ast.dump(ast.parse(
              open(os.path.join(HERE, "p4_coherence.py"),
                   encoding="utf-8").read()).body[
                       [i for i, n in enumerate(ast.parse(open(
                           os.path.join(HERE, "p4_coherence.py"),
                           encoding="utf-8").read()).body)
                        if isinstance(n, ast.FunctionDef)
                        and n.name == "settle"][0]]))


# ------------------------------------------------------------------- 7 p2

def sec_p2():
    uf = p2_substrate.unverified_fraction
    check("p2: no call sites is None, not 0.0 -- a file with no calls"
          " has nothing to report", uf([]) is None)
    check("p2: all unverified is 1.0",
          uf([{"status": p2_substrate.UNVERIFIED}]) == 1.0)
    check("p2: all checked is 0.0",
          uf([{"status": p2_substrate.LOCALLY_CHECKED}]) == 0.0)
    src = open(os.path.join(HERE, "p2_substrate.py"), encoding="utf-8").read()
    rows = p2_substrate.call_contracts(src)
    frac = uf(rows)
    check("p2: the share on real source is below 1.0 (%.4f), so the"
          " classifier is not CONSTANT_FIRES" % frac, frac < 1.0)
    check("p2: and above 0.9, which is the reading", frac > 0.9)
    checked = p2_substrate.call_contracts(
        "def f():\n    assert int('1') == 1\n")
    check("p2: a call inside an assert is LOCALLY_CHECKED",
          any(r["status"] == p2_substrate.LOCALLY_CHECKED for r in checked))
    branch = p2_substrate.call_contracts(
        "def f(x):\n    if len(x) > 0:\n        return 1\n")
    check("p2: a call compared in a branch test is LOCALLY_CHECKED",
          any(r["status"] == p2_substrate.LOCALLY_CHECKED for r in branch))
    plain = p2_substrate.call_contracts("def f(x):\n    return len(x)\n")
    check("p2: a plain call is UNVERIFIED",
          all(r["status"] == p2_substrate.UNVERIFIED for r in plain))
    comp = p2_substrate.call_contracts("def f(d, k):\n    return d[k]()\n")
    check("p2: a computed target is recorded as computed, not guessed",
          any(r["target"] == "<computed>" for r in comp))
    check("p2: the glossary is closed -- an unlisted token is UNMAPPED",
          p2_substrate.gloss("survival of the fittest")
          == p2_substrate.UNMAPPED)
    check("p2: a listed token maps to a mechanical requirement",
          "gradient" in p2_substrate.gloss("Adversarial Training"))
    check("p2: backprop maps to faithful layer output, the order's"
          " own example",
          "faithfully" in p2_substrate.gloss("backpropagation"))
    check("p2: an empty token is UNMAPPED rather than raising",
          p2_substrate.gloss("") == p2_substrate.UNMAPPED)
    check("p2: every layer contract carries an assumption and a"
          " failure mode",
          all(len(row) == 3 and all(row) for row in p2_substrate.LAYERS))
    check("p2: the six layers the order names are all present",
          {r[0] for r in p2_substrate.LAYERS} == {
              "allocator", "ieee754", "network_stack", "scheduler",
              "compiler", "hardware"})
    digest = p2_substrate.sha256_of(os.path.join(HERE, "p2_substrate.py"))
    check("p2: the digest is of the file that was analysed, which is"
          " what makes the proof checkable against itself",
          len(digest) == 64 and digest == p2_substrate.sha256_of(
              os.path.join(HERE, "p2_substrate.py")))


# ------------------------------------------------------------------- 8 p1

def sec_p1():
    R = p1_records.Requirement
    check("p1: a requirement with no source is REFUSED at construction,"
          " not admitted and flagged",
          raises(p1_records.SourceMissing, R, "METHOD", "x", "", True))
    check("p1: a whitespace source is refused too",
          raises(p1_records.SourceMissing, R, "METHOD", "x", "   ", True))
    check("p1: a kind outside the closed set is refused, not filed"
          " under a nearest neighbour",
          raises(p1_records.KindError, R, "SOFTWARE", "x", "s", True))
    check("p1: absent_from_argument must be declared as a bool",
          raises(ValueError, R, "METHOD", "x", "s", "yes"))
    check("p1: an empty statement is refused",
          raises(ValueError, R, "METHOD", "", "s", True))
    check("p1: a well-formed requirement is admitted",
          R("METHOD", "x", "s", True).kind == "METHOD")
    empty = p1_records.Record("o", "CONSTRUCTED", [])
    check("p1: an empty record's unstated_fraction is None, never 0.0"
          " -- zero would read as an argument that stated everything",
          empty.unstated_fraction() is None)
    check("p1: every kind appears in preconditions, so a kind nobody"
          " looked for is a visible zero",
          set(empty.preconditions()) == set(p1_records.KINDS))
    rec = p1_records.from_json(p1_records.DEMO)
    check("p1: the shipped record is labelled CONSTRUCTED in its own"
          " provenance field", rec.provenance == "CONSTRUCTED")
    check("p1: and says so in its note", "CONSTRUCTED" in rec.note)
    check("p1: the shipped record's fraction is computed, not stated",
          abs(rec.unstated_fraction() - 5.0 / 6.0) < 1e-12)
    check("p1: an entry stated in the argument is present, so the"
          " fraction is not 1.0 by construction",
          any(not r.absent_from_argument for r in rec.requirements))
    check("p1: a bad provenance is refused",
          raises(ValueError, p1_records.Record, "o", "MEASURED", []))


# ------------------------------------------------------------------- 9 p5

def sec_p5():
    lr = p5_lag.lag_ratio
    check("p5: the ratio is a division",
          abs(lr(50.0, 5.0) - 10.0) < 1e-12)
    check("p5: an undeclared t_visible is None, never a small ratio",
          lr(None, 10.0) is None)
    check("p5: a t_visible of exactly zero is a MEASUREMENT and returns"
          " 0.0, which is why the undeclared case must not",
          lr(0.0, 10.0) == 0.0)
    check("p5: an absent t_scored is None", lr(10.0, None) is None)
    check("p5: a zero t_scored is None, not a division", lr(10.0, 0.0) is None)
    check("p5: a negative t_scored is None", lr(10.0, -1.0) is None)
    check("p5: unreadable inputs are None, not zero", lr("soon", 10.0) is None)
    check("p5: at the threshold the gate fires",
          p5_lag.classify(10.0, 1.0) == p5_lag.DECLARED_UNKNOWN)
    check("p5: below the threshold it does not",
          p5_lag.classify(9.99, 1.0) == p5_lag.TRACKED)
    check("p5: an undeclared t_visible is UNDECLARED, kept apart from"
          " DECLARED_UNKNOWN",
          p5_lag.classify(None, 1.0) == p5_lag.UNDECLARED)
    check("p5: an absent denominator is NOT_EVALUABLE, kept apart from"
          " both", p5_lag.classify(1.0, None) == p5_lag.NOT_EVALUABLE)
    rows = [p5_lag.read_action(o) for o in p5_lag.ANCHORS]
    check("p5: all four verdicts occur across the shipped anchors",
          len({r["verdict"] for r in rows}) == 4)
    check("p5: the antibiotic anchor is DECLARED_UNKNOWN",
          rows[0]["verdict"] == p5_lag.DECLARED_UNKNOWN)
    check("p5: the reachable negative is present -- a failure visible"
          " faster than the scoring interval",
          any(r["verdict"] == p5_lag.TRACKED for r in rows))
    check("p5: the gate does not block: no code path raises or exits"
          " on DECLARED_UNKNOWN",
          "raise" not in open(os.path.join(HERE, "p5_lag.py"),
                              encoding="utf-8").read().split(
                                  "def classify")[1].split("def ")[0])


# ------------------------------------------------------------- 10 framing

VALUES_TOKENS = ("rank", "ranking", "score", "scores", "better", "worse",
                 "prefer", "preferred", "superior", "inferior", "wins",
                 "beats", "merit", "virtue", "moral", "should", "best",
                 "worst", "good", "bad")


def identifiers(source):
    """Every identifier, attribute, argument, function name and
    dict-literal key in a module. An AST walk and not a substring scan,
    because these modules have to be able to NAME what they refuse and a
    substring scan fires on the sentence saying so.

    This scan is a COPY of the operation in tools/authority_scan.py and
    not an import: the order addresses a separate repository, so this
    folder imports nothing across its own boundary. The cost is stated
    rather than hidden -- two copies of one operation can drift, and
    nothing here would notice.
    """
    out = set()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            out.add(node.id)
        elif isinstance(node, ast.Attribute):
            out.add(node.attr)
        elif isinstance(node, ast.arg):
            out.add(node.arg)
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            out.add(node.name)
        elif isinstance(node, ast.keyword) and node.arg:
            out.add(node.arg)
        elif isinstance(node, ast.Dict):
            for k in node.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    out.add(k.value)
    split = set()
    for name in out:
        for piece in name.replace("-", "_").split("_"):
            if piece:
                split.add(piece.lower())
    return split


def sec_framing():
    order = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()
    framing = open(os.path.join(HERE, "FRAMING.md"), encoding="utf-8").read()
    for line in run_all.FRAMING_LINES:
        check("framing: the order's line %r is in FRAMING.md"
              % line[:38], line in framing)
        check("framing: and is the order's own words", line in order)
    ok, why = run_all.framing_present()
    check("framing: run_all reports it present (%s)" % why, ok)

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                     encoding="utf-8") as fh:
        fh.write("nothing\n")
        stripped = fh.name
    real = run_all.FRAMING
    try:
        run_all.FRAMING = stripped
        ok2, why2 = run_all.framing_present()
        check("framing: a stripped framing is DETECTED, so the check"
              " is not constant", ok2 is False and "stripped" in why2)
    finally:
        run_all.FRAMING = real
        os.unlink(stripped)

    hits = {}
    for name in MODULES:
        src = open(os.path.join(HERE, name), encoding="utf-8").read()
        found = identifiers(src) & set(VALUES_TOKENS)
        if found:
            hits[name] = sorted(found)
    check("framing: no module carries a ranking or values identifier"
          " (%s)" % (hits or "clean"), not hits)
    planted = identifiers("def rank_frames(a, b):\n    return a\n")
    check("framing: the scan FIRES on a planted violation, so its"
          " silence means something",
          bool(planted & set(VALUES_TOKENS)))
    check("framing: the scan does not fire on a comment naming the"
          " tokens it refuses",
          not (identifiers("# rank, score, better\nx = 1\n")
               & set(VALUES_TOKENS)))


# --------------------------------------------------------- 11 conventions

def sec_conventions():
    for name in MODULES + ("test_proof.py",):
        path = os.path.join(HERE, name)
        raw = open(path, "rb").read()
        try:
            raw.decode("ascii")
            ok = True
        except UnicodeDecodeError:
            ok = False
        check("conventions: %s is ASCII" % name, ok)
        try:
            ast.parse(raw.decode("utf-8"))
            parsed = True
        except SyntaxError:
            parsed = False
        check("conventions: %s parses" % name, parsed)

    for name in MODULES:
        p = subprocess.run([sys.executable, os.path.join(HERE, name),
                            "--selftest"], capture_output=True, cwd=HERE)
        check("conventions: %s refuses --selftest with exit 2" % name,
              p.returncode == 2)
        check("conventions: %s names this file in its refusal" % name,
              b"test_proof.py" in p.stderr)

    # p3 is the one module whose bare invocation is a REFUSAL rather
    # than a render: it reads a corpus and will not fall back to its own
    # source, which would measure the instrument. That refusal is
    # asserted on its own below, so it is excluded here rather than
    # weakening this check for every module.
    for name in MODULES:
        if name == "p3_comprehension.py":
            continue
        p = subprocess.run([sys.executable, os.path.join(HERE, name)],
                           capture_output=True, cwd=HERE)
        check("conventions: %s renders on a bare invocation" % name,
              p.returncode == 0 and len(p.stdout) > 100)

    p = subprocess.run([sys.executable, os.path.join(HERE, "p3_comprehension.py"),
                        "--corpus", os.path.join(HERE, "fixtures", "corpus")],
                       capture_output=True, cwd=HERE)
    check("conventions: p3_comprehension.py renders when given the"
          " input it requires",
          p.returncode == 0 and len(p.stdout) > 100)

    for name in ("scope.py", "p1_records.py", "p2_substrate.py",
                 "p3_comprehension.py", "p4_coherence.py", "p5_lag.py"):
        p = subprocess.run([sys.executable, os.path.join(HERE, name),
                            "--choices"], capture_output=True, cwd=HERE)
        check("conventions: %s answers --choices" % name,
              p.returncode == 0 and len(p.stdout) > 10)

    for name, n in (("scope.py", 1), ("p3_comprehension.py", 3),
                    ("p4_coherence.py", 1), ("p5_lag.py", 1)):
        src = open(os.path.join(HERE, name), encoding="utf-8").read()
        for i in range(1, n + 1):
            marker = "[CHOICE %d]" % i
            check("conventions: %s %s is cited more than once, so the"
                  " choice appears where it takes effect and not only"
                  " where it is declared" % (name, marker),
                  src.count(marker) >= 2)

    p = subprocess.run([sys.executable, os.path.join(HERE, "p3_comprehension.py")],
                       capture_output=True, cwd=HERE)
    check("conventions: p3 with no corpus reports NOT_RUN and does not"
          " fall back to its own source",
          p.returncode == 2 and b"NOT_RUN" in p.stderr)

    p = subprocess.run([sys.executable, os.path.join(HERE, "run_all.py")],
                       capture_output=True, cwd=HERE)
    out = p.stdout.decode("utf-8")
    check("run_all: exits 0 with the framing present", p.returncode == 0)
    check("run_all: reports one ABSENT row and names its reason",
          out.count("ABSENT") == 1 and "methods sections" in out)
    check("run_all: reports five PASS rows", out.count("PASS") == 5)
    check("run_all: every part is listed", all(
        ("P%d " % i) in out or ("P%d*" % i) in out for i in range(1, 6)))

    check("conventions: LICENSE is present and is CC0",
          "CC0" in open(os.path.join(HERE, "LICENSE"), encoding="utf-8").read())
    for name in MODULES:
        src = open(os.path.join(HERE, name), encoding="utf-8").read()
        check("conventions: %s imports only the standard library and"
              " this folder" % name,
              all(m.split(".")[0] in (
                  "ast", "hashlib", "json", "os", "random", "re",
                  "subprocess", "sys", "tempfile", "zlib",
                  "scope", "p1_records", "p2_substrate",
                  "p3_comprehension", "p4_coherence", "p5_lag",
                  "run_all")
                  for m in _imports(src)))


def _imports(source):
    out = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            out += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            out.append(node.module)
    return out


# --------------------------------------------------------------- 12 scope
#                                                        coded into P1-P5

def sec_scope_in_parts():
    for name, mod, attr in (
            ("p1_records.py", p1_records, "DEMO"),
            ("p2_substrate.py", p2_substrate, "ANALYSIS_SCOPE"),
            ("p3_comprehension.py", p3_comprehension, "CORPUS_SCOPE"),
            ("p5_lag.py", p5_lag, "ANCHOR_SCOPE")):
        src = open(os.path.join(HERE, name), encoding="utf-8").read()
        check("scope in parts: %s imports scope" % name,
              "scope" in _imports(src))
        check("scope in parts: %s calls scope.code" % name,
              "scope.code(" in src)
    check("scope in parts: p4 codes every shipped chain",
          all(obj.get("scope") for obj in p4_coherence.CHAINS))
    check("scope in parts: the turf-war chain is the one coded WITHIN"
          " the competitive frame",
          [obj["label"] for obj in p4_coherence.CHAINS
           if scope.code(obj["scope"])["verdict"] == scope.WITHIN]
          == ["turf_war"])
    check("scope in parts: both the WITHIN and the OUTSIDE verdict"
          " occur across the parts, so the coding pass is not constant",
          len({scope.code(p2_substrate.ANALYSIS_SCOPE)["verdict"],
               scope.code(p5_lag.ANCHOR_SCOPE)["verdict"]}) == 2)
    check("scope in parts: the templates ship the four conditions"
          " undeclared rather than pre-answered",
          set(p1_records.TEMPLATE["scope"]) == set(scope.CONDITIONS)
          and all(v is None for v in p1_records.TEMPLATE["scope"].values()))
    check("scope in parts: and so does p4's",
          all(v is None for v in p4_coherence.TEMPLATE["scope"].values()))


def main():
    for fn in (sec_scope, sec_p3_math, sec_p3_cipher, sec_p3_verdicts,
               sec_p4_schema, sec_p4_verdicts, sec_p2, sec_p1, sec_p5,
               sec_framing, sec_conventions, sec_scope_in_parts):
        fn()
    for label in FAILED:
        sys.stdout.write("FAIL  %s\n" % label)
    sys.stdout.write("checks: %d   failed: %d\n"
                     % (len(PASSED) + len(FAILED), len(FAILED)))
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
