# SPDX-License-Identifier: CC0-1.0
"""Checks for WORK ORDER standing/A-6.3 (verification_a63.py).

Run:  python3 route-independence/test_verification_a63.py
Prints the check count and whether the fixture built to FAIL exists; NO_FAIL_FIXTURE in the
summary line otherwise.  No network: re-verification here uses LOCAL_CHECKOUT; the committed
verification records came from REMOTE_FETCH and are read, not refetched.
"""
import ast
import io
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import gate_state_a21 as G21   # noqa: E402
import repairs_a31 as R        # noqa: E402
import sourcing_a62 as P       # noqa: E402
import standing_a61 as S61     # noqa: E402
import verification_a63 as V   # noqa: E402

_checks = 0
_failed = 0
FAIL_FIXTURE = [False]


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


def t_location():
    full = "a" * 40
    check(V.location_form("repo:%s:route-independence/x.py" % full) == "REPO", "repo form with a full commit id")
    check(V.location_form("repo:abc1234:route-independence/x.py") == "REPO_MALFORMED", "a short commit is refused")
    check(V.location_form("https://example.org/x") == "HTTP", "http form")
    check(V.location_form("content.leg.colorado.gov/x.pdf") == "NO_SCHEME", "an address without a scheme")
    check(V.location_form(None) == "NONE", "no url")
    span = "s"
    base = {"url": "repo:%s:route-independence/x.py" % full, "retrieval_date": "2026-09-30", "span": span,
            "sha256": P.sha256_of(span)}
    check(V.consistent(base)["missing"] == ["clone_url"], "the repo form requires a clone url (item 1)")
    check(V.consistent(dict(base, clone_url=V.CLONE_URL))["ok"], "repo form plus clone url is consistent")
    check(V.consistent(dict(base, clone_url="github.com/x"))["missing"] == ["clone_url"],
          "a clone url without a scheme is refused")
    recs = V._load(V.REPO_STORE)
    check(len(recs) == 5, "five repo spans on file (gate_state.py and four amendment files)")
    for r in recs:
        c = V.consistent(r)
        check(c["ok"] and c["form"] == "REPO", "%s consistent in the repo form" % r["source_id"])
        m = V._REPO.match(r["url"])
        check(m is not None and len(m.group(1)) == 40 and r["clone_url"] == V.CLONE_URL,
              "%s carries a full commit id and the clone url" % r["source_id"])
        body = subprocess.run(["git", "show", "%s:%s" % (m.group(1), m.group(2))], cwd=HERE, capture_output=True,
                              text=True).stdout
        check(P.sha256_of(body) == r["sha256"], "%s: the stored hash is the committed file's" % r["source_id"])


def t_verify():
    recs, vrecs = V._load(V.REPO_STORE), V._load(V.VERIFY_STORE)
    check(len(vrecs) == 5 and all(v["method"] == V.REMOTE_FETCH for v in vrecs),
          "five verification records, all REMOTE_FETCH")
    for v in vrecs:
        check(v["matches_stored"] and set(v) >= {"fetched_by", "date", "hash_obtained", "location"},
              "%s: record names who/what fetched, the date and the hash obtained" % v["source_id"])
        check("proxy" not in json.dumps(v) and "@" not in v["location"], "%s: no remote address written"
              % v["source_id"])
    for r in recs:
        st = V.input_status(r["source_id"], P.IN_REPO)
        check(st["status"] == V.VERIFIED, "%s reads VERIFIED" % r["source_id"])
    # independent re-verification without network
    lv = V.verify(recs[0], V.LOCAL_CHECKOUT)
    check(lv is not None and lv["hash_obtained"] == recs[0]["sha256"] and lv["method"] == V.LOCAL_CHECKOUT,
          "a local checkout at the commit returns the stored hash")
    # states
    r0 = dict(recs[0])
    check(V.input_status(r0["source_id"], P.IN_REPO, [r0], [])["status"] == V.STORED_UNVERIFIED,
          "no verification record -> STORED_UNVERIFIED")
    bad = dict(vrecs[0], source_id=r0["source_id"], location=r0["url"], hash_obtained="0" * 64)
    check(V.input_status(r0["source_id"], P.IN_REPO, [r0], [bad])["status"] == V.VERIFICATION_MISMATCH,
          "a verification whose hash differs -> VERIFICATION_MISMATCH")
    same = dict(bad, hash_obtained=r0["sha256"], method=V.LOCAL_OBJECT_STORE)
    check(V.input_status(r0["source_id"], P.IN_REPO, [r0], [same])["status"] == V.STORED_UNVERIFIED,
          "a verification by the storing method is not independent [CHOICE 97]")
    other = dict(bad, hash_obtained=r0["sha256"], location="repo:%s:x" % ("b" * 40))
    check(V.input_status(r0["source_id"], P.IN_REPO, [r0], [other])["status"] == V.STORED_UNVERIFIED,
          "a verification of another location does not count")
    drift = dict(r0, span=r0["span"] + " ", sha256=P.sha256_of(r0["span"] + " "))
    check(V.input_status(r0["source_id"], P.IN_REPO, [drift], [])["status"] == V.WORKTREE_DRIFT,
          "stored span differing from the working tree -> WORKTREE_DRIFT [CHOICE 98]")
    broken = dict(r0, sha256="0" * 64)
    check(V.input_status(r0["source_id"], P.IN_REPO, [broken], [])["status"] == V.INCONSISTENT,
          "a record on file whose hash does not match its span -> INCONSISTENT")
    check(V.input_status("nothing", P.CARRIED, [], [])["status"] == V.NO_SPAN, "no record -> NO_SPAN")
    check(V.input_status("K", V.CONSTRUCTED, [], [])["status"] == V.CONSTRUCTED, "constructed input")


def t_gate():
    g = V.gate_core
    check(g("MATCH", [V.VERIFIED]) == "MATCH", "all VERIFIED -> MATCH")
    check(g("MATCH", [V.STORED_UNVERIFIED]) == V.UNVERIFIED_PASS, "STORED_UNVERIFIED never reads MATCH")
    check(g("MATCH", [V.VERIFIED, V.STORED_UNVERIFIED]) == V.UNVERIFIED_PASS, "one unverified input suffices")
    check(g("MATCH", [V.CONSTRUCTED, V.VERIFIED]) == V.CONSTRUCTED_PASS, "CONSTRUCTED stays first (item 1)")
    check(g("MATCH", [V.CONSTRUCTED, V.NO_SPAN]) == V.CONSTRUCTED_PASS, "CONSTRUCTED before NO_SPAN")
    check(g("MATCH", []) == V.UNSOURCED_PASS and g("MATCH", [V.NO_SPAN]) == V.UNSOURCED_PASS, "no span")
    check(g("MATCH", [V.VERIFICATION_MISMATCH]) == V.VERIFICATION_FAILED, "mismatch")
    check(g("MATCH", [V.VERIFIED], False) == V.UNFALSIFIABLE_AS_RUN, "not enumerated")
    check(g("MATCH", [V.VERIFIED], True, True) == V.UNFALSIFIABLE_AS_RUN, "one aggregate case")
    check(g("UNMET_UNFALSIFIED", [V.VERIFIED]) == "UNMET_UNFALSIFIED", "a non-MATCH passes through")
    fx = V.placeholder_fixture()
    check(fx["a62"] == "MATCH", "RIN_150 placeholder read MATCH under the A-6.2 gate")
    check(fx["status"] == V.STORED_UNVERIFIED and fx["a63"] == V.UNVERIFIED_PASS,
          "RIN_150 placeholder now reads STORED_UNVERIFIED, gate UNVERIFIED_PASS (item 2)")
    check(fx["verify"] is None, "a web location is not fetched here")
    FAIL_FIXTURE[0] = V.fail_fixture()["fires"]
    check(FAIL_FIXTURE[0], "the fail fixture fires: A-6.2 MATCH, A-6.3 not")


def t_rerun():
    rows = V.rerun_a63()
    by = dict((r["row"], r) for r in rows)
    check(len(rows) == 19, "19 rows re-gated")
    want_match = {"E-A2-4", "E-A3.1-1 (LITERAL_ALL)", "E-A3.1-1 (DECLARED_LITERAL)"}
    check(set(r["row"] for r in rows if r["new"] == "MATCH") == want_match,
          "MATCH exactly on the three in-repo rows (item 1)")
    check(V.match_on_unverified(rows) == [], "no row reads MATCH on a non-VERIFIED input")
    for r in rows:
        if any(s["status"] == V.CONSTRUCTED for s in r["sources"]):
            check(r["new"] != "MATCH", "%s: constructed input, not MATCH" % r["row"])
    for rid in ("E-A2.1-1", "E-A2.1-2"):
        st = dict((s["source_id"], s) for s in by[rid]["sources"])
        check(st["W-1a"]["status"] == V.NO_SPAN and st["W-2a"]["status"] == V.NO_SPAN,
              "%s: W-1a, W-2a NO_SPAN (item 8's STORED_UNVERIFIED does not hold)" % rid)
        check(by[rid]["new"] == V.UNSOURCED_PASS, "%s stays UNSOURCED_PASS" % rid)
    c = V.counts(rows)
    check(c["references"] == {V.VERIFIED: 9, V.STORED_UNVERIFIED: 0, V.NO_SPAN: 15, V.CONSTRUCTED: 11,
                              V.INCONSISTENT: 0, V.VERIFICATION_MISMATCH: 0, V.WORKTREE_DRIFT: 0},
          "counts by reference %s" % c["references"])
    check(c["distinct"][V.VERIFIED] == 5 and c["distinct"][V.NO_SPAN] == 9 and c["distinct"][V.CONSTRUCTED] == 3,
          "counts by distinct source %s" % c["distinct"])
    check(c["n_refs"] == sum(c["references"].values()) == 35, "35 references")
    a62 = dict((r["row"], r["new"]) for r in P.rerun())
    for r in rows:
        if r["row"] not in want_match:
            check(r["new"] == a62[r["row"]], "%s unmoved from A-6.2" % r["row"])


def t_item8():
    w1, w2 = G21.SOURCES21["W-1a"], G21.SOURCES21["W-2a"]
    check(w1["url"] == "content.leg.colorado.gov/sites/default/files/2016a_1005_signed.pdf", "W-1a url moved")
    check(w2["url"] == "le.utah.gov/~2010", "W-2a url moved")
    check(P._LOCATOR.search(w1["text"]) is None and P._LOCATOR.search(w2["text"]) is None,
          "no address left in either text")
    check(V.location_form(w1["url"]) == V.location_form(w2["url"]) == "NO_SCHEME", "no scheme was added")
    old = subprocess.run(["git", "show", "f6d385c:./gate_state_a21.py"], cwd=HERE, capture_output=True,
                         text=True).stdout
    check("content.leg.colorado.gov/sites/default/files/" in old and "le.utah.gov/~2010" in old,
          "both addresses were in the text before the move")


def t_ce4e():
    n = S61.SOURCES_A61["CE-4e"].get("status_note", "")
    check("coding rule = GEOGRAPHIC, undeclared at issue" in n, "CE-4e names its coding rule (item 3)")
    check("chat handover (Claude), not the agent" in n, "CE-4e names the origin of the undeclared rule")
    check(S61.SOURCES_A61["CE-4e"]["grade"] == P.NOT_RECORDED, "CE-4e grade unchanged")


def t_lint():
    for text, tok, kind, credited in V.LINT_FIXTURES:
        f = V.lint_fixture(text, tok)
        check(f["kind"] == kind and f["credited"] == credited, "%r: %s credited %s (%s)" % (text, kind, credited, f))
    check(V.lint_fixture("2036 paths", "2036")["a31_credited"] is False, "[CHOICE 30] dropped 2036 unseen")
    check(V.lint_fixture("rule 0 these rows", "0")["a31_credited"] is True, "A-3.1 credited rule 0")
    for text, tok in (("in 1980 there were", "1980"), ("by 2031", "2031"), ("March 2026", "2026"),
                      ("1971 - 1973 era", "1971"), ("1971 \u2013 1973", "1973"), ("1971 to 1973", "1971")):
        check(V.lint_fixture(text, tok)["kind"] == V.YEAR, "%r: YEAR" % text)
    hy = V.count_tokens_a63("1971-1973 era")
    check(hy["counted"] == [] and hy["dropped"] == [],
          "a hyphen-joined range is outside the count pattern (R._DIGITS), neither counted nor a year")
    for text, tok in (("1535 paths", "1535"), ("2041 paths total", "2041")):
        f = V.lint_fixture(text, tok)
        check(f["credited"] and f["flag"] == V.YEAR_SHAPED, "%r: counted, flagged YEAR_SHAPED" % text)
    for text in ("item 6 rows", "step 3 gates", "[CHOICE 30] rows", "section 4 rows", "Rule 2 cells"):
        check(V.count_tokens_a63(text)["counted"] == [], "%r: label, nothing counted" % text)
    for pfx in ("A-", "RIN_", "P-", "E-A", "CE-", "FWO-"):
        check(V.count_tokens_a63("%s4 rows" % pfx)["counted"] == [], "%s4 is outside the count pattern" % pfx)
    check(len(V.LABEL_IDENTIFIERS) == len(set(i for i, _, _ in V.LABEL_IDENTIFIERS)),
          "identifier list declared once per identifier")
    src = open(V.__file__, encoding="utf-8").read()
    fn = ast.parse(src)
    body = [n for n in fn.body if isinstance(n, ast.FunctionDef) and n.name == "classify_number"][0]
    consts = [n.value for n in ast.walk(body) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    check(not any(c in ("rule", "item", "step", "choice") for c in consts),
          "no identifier inline in classify_number; the list is data")
    # equivalence with A-3.1 where no label or year-shaped token sits
    for f in P.PIN_FILES:
        t = V.C.expected_block(f)
        a31 = [(x["token"], x["status"]) for x in R.count_tokens(t)]
        new = V.count_tokens_a63(t)
        a63 = [(x["token"], x["status"]) for x in new["counted"]]
        check(new["dropped"] == [] and not any(x["flag"] for x in new["counted"]) and a31 == a63,
              "%s: no label or year token, A-6.3 counts equal A-3.1's" % f[:22])
    ol = V.order_lint()
    check(ol["labels"] == 3 and ol["years"] == ["1000", "2999", "1971"] and ol["year_shaped_counted"] == ["2036"],
          "the order under items 4-5: 3 labels, 1000-2999 read as a year range, 2036 counted %s" % ol)
    check(ol["a31_ok"] and not ol["a63_ok"], "A-3.1's one OK on the order was the label 'rule 0'")


def t_pins_alias():
    moves = {}
    for f in P.PIN_FILES:
        p = V.pins_a63(f)
        moves[f] = p["moved"]
    a6 = V.pins_a63(P.PIN_FILES[2])
    check(len(a6["a62_agree"]) == 2 and len(a6["a63"]) == 3 and a6["flags"] == [],
          "A-6 returns to 3 once P-* is declared (item 6)")
    check(moves[P.PIN_FILES[2]] == ([], [(136, "1", "profiles")]), "the one move is A-6 position 136")
    check(all(moves[f] == ([], []) for f in P.PIN_FILES if f != P.PIN_FILES[2]),
          "A-4, A-5, A-6.1: no identity change")
    none = V.pins_a63(P.PIN_FILES[2], aliases=())
    check(len(none["a63"]) == 2 and len(none["flags"]) == 1, "without the map the row stays a FLAG")
    check(V.dealias("1 of Q-0..Q-4 for") == "1 of Q-0..Q-4 for", "an undeclared prefix is not aliased")
    check("profiles" in V.dealias("of P-0..P-4 for") and "profiles" in V.dealias("of P-3 for"), "range and single")
    check(V.ID_ALIASES == (("P-", "profiles"),), "one declared line per prefix")


def t_mutation():
    res = V.mutation_all()
    for m in res:
        check(m["verdict"] == "PASS", "%s: output moves over its grid" % m["gate"])
        check(not [k for k, v in m["per_arg"].items() if v["dead"]], "%s: no dead argument" % m["gate"])
    cg = V.mutation(V.CONSTANT_GATE_FIXTURE[1](), V.CONSTANT_GATE_FIXTURE[2]())
    check(cg["verdict"] == "FAIL", "a constant gate FAILs")
    named = set(V.gate_functions_named())
    cov = set(n for n, _, _ in V.MUTATION_GATES) | set(n for n, _ in V.NOT_MUTATED)
    check(named <= cov, "every gate/status function is mutated or excluded with a reason %s" % (named - cov))
    g = list(V._grid_gate_a62())
    g[1] = ("inputs", g[1][1][:4])
    no_repo = V.mutation(P.gate_a62, g)
    check(no_repo["per_arg"]["reading"]["dead"], "without an IN_REPO input, 'reading' reads dead: a grid gap")


def t_hygiene():
    src = V.__file__
    txt = open(src, encoding="utf-8").read()
    check(txt.startswith("# SPDX-License-Identifier: CC0-1.0"), "SPDX header")
    p = subprocess.run([sys.executable, src, "--selftest"], capture_output=True, text=True)
    check(p.returncode == 2 and "test_verification_a63.py" in p.stderr, "refuses --selftest")
    decl = txt.split("CHOICES = {")[1].split("\n}\n")[0]
    rest = txt.replace(decl, "")
    check(sorted(V.CHOICES) == list(range(95, 106)), "choices 95..105")
    for k in V.CHOICES:
        check(("[CHOICE %d]" % k) in rest, "[CHOICE %d] cited outside its declaration" % k)
    raw = open(src, "rb").read()
    check(all(b < 128 for b in raw), "ASCII")
    ast.parse(raw.decode("ascii"), feature_version=(3, 8))
    buf = io.StringIO()
    V.render(buf)
    r = buf.getvalue()
    p = subprocess.run([sys.executable, os.path.join(HERE, "..", "sheet-structure-scan", "no_severity.py")],
                       input=r, capture_output=True, text=True)
    check("no severity or interpretation vocabulary" in p.stdout, "render screens clean %s" % p.stdout[:200])
    log = subprocess.run(["git", "log", "--format=%h", "-n", "1", "--", V.ORDER_FILE], cwd=HERE,
                         capture_output=True, text=True).stdout.strip()
    if log:
        check(log == V.EXPECTED_COMMIT_A63, "the order's last commit is its registration commit (%s)" % log)
    order = open(os.path.join(HERE, V.ORDER_FILE), encoding="utf-8").read()
    check(order.startswith("WORK ORDER \u2014 standing/A-6.3 : verification split"), "order landed as delivered")
    check(P.load_store() == [], "A-6.2's span store is still empty [CHOICE 95]")
    sample = os.path.join(HERE, "samples", "verification_a63.sample.txt")
    if os.path.exists(sample):
        check(open(sample, encoding="utf-8").read() == r, "sample matches a fresh render")
    for t in ("test_sourcing_a62.py", "test_standing_a61.py", "test_gate_state_a21.py"):
        p = subprocess.run([sys.executable, os.path.join(HERE, t)], capture_output=True)
        check(p.returncode == 0, "%s still green" % t)


for fn in (t_location, t_verify, t_gate, t_rerun, t_item8, t_ce4e, t_lint, t_pins_alias, t_mutation, t_hygiene):
    fn()

n = 1 if FAIL_FIXTURE[0] else 0
tag = "" if n else "  NO_FAIL_FIXTURE"
print("verification-a63: %d checks, %d failed; fail fixtures present: %d of 1%s" % (_checks, _failed, n, tag))
sys.exit(1 if _failed else 0)
