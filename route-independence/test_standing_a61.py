# SPDX-License-Identifier: CC0-1.0
"""Checks for AMENDMENT A-6.1 (standing_a61.py).

Run:  python3 route-independence/test_standing_a61.py
Prints the check count and whether the fixture built to FAIL exists (key-holder rule 3);
NO_FAIL_FIXTURE in the summary line otherwise.
"""
import ast
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import eligibility_a6 as E6    # noqa: E402
import repairs_a31 as R        # noqa: E402
import standing_a61 as S       # noqa: E402

_checks = 0
_failed = 0
FAIL_FIXTURE = [False]


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


def raises(exc, fn, *a, **k):
    try:
        fn(*a, **k)
    except exc:
        return True
    return False


def render():
    buf = io.StringIO()
    S.render(buf)
    return buf.getvalue()


# ------------------------------------------------------------------ 2a ---

def t_standing():
    check(S.at_least(S.MEMBER, S.ADMITTED) == S.TRUE and S.at_least(S.ADMITTED, S.MEMBER) == S.FALSE,
          "standing order [CHOICE 66]")
    check(S.at_least(S.EXCLUDED, S.ADMITTED) == S.FALSE, "EXCLUDED below ADMITTED_NOT_MEMBER")
    check(S.at_least(S.NOT_RECORDED, S.ADMITTED) == S.NOT_RECORDED and
          S.at_least(S.MEMBER, S.NOT_RECORDED) == S.NOT_RECORDED, "NOT_RECORDED never compares TRUE or FALSE")
    check(raises(S.StandingError, S.at_least, "GUEST", S.MEMBER), "standing outside the enum refused")
    got = dict((p["profile_id"], dict(S.eligible_sets(p)["pairs"])["CS-R"]) for p in S.profiles())
    check(got == {"P-0": S.EXCLUDED, "P-1": S.MEMBER, "P-2": S.EXCLUDED, "P-3": S.EXCLUDED, "P-4": S.EXCLUDED,
                  "P-ADMITTED": S.ADMITTED, "P-NR": S.NOT_RECORDED}, "CS-R standing per profile [CHOICE 67] %s" % got)
    seen = set(s for p in S.profiles() for _, s in S.eligible_sets(p)["pairs"])
    check(seen == set(S.STANDING), "all four standings reachable: %s" % sorted(seen))
    for p in S.profiles():
        check([cs for cs, _ in S.eligible_sets(p)["pairs"]] == sorted(E6.CASE_SETS),
              "%s: a pair for every case set, none dropped" % p["profile_id"])
        check(p["constructed"] is True, "%s constructed" % p["profile_id"])
    # A-6 profiles keep their A-6 membership reading
    for p in E6.profiles():
        mine = S.get_profile(p["profile_id"])
        a6 = E6.eligible_sets(p)["eligible"]
        members = [cs for cs, st in S.eligible_sets(mine)["pairs"] if st == S.MEMBER]
        check(members == a6, "%s: MEMBER sets equal A-6's eligible sets" % p["profile_id"])
    check(E6.eligible_sets(E6.get_profile("P-0"))["eligible"] == ["CS-G"], "A-6 module untouched")


# ------------------------------------------------------------------ 2b/2c ---

def t_routes():
    check(raises(S.StandingError, S.route, "x", "CS-R", S.EXCLUDED, S.TRUE, ""), "min_standing EXCLUDED refused")
    check(raises(S.StandingError, S.route, "x", "CS-R", S.MEMBER, "YES", ""), "allocation_limited enum")
    check(raises(S.StandingError, S.coupling, "G-NOPE", "CS-R:fuel_allotment", S.MEMBER), "unknown gate refused")
    check(raises(S.StandingError, S.coupling, "G-T3", "CS-R:water", S.MEMBER), "target not limited refused")
    check(raises(S.StandingError, S.coupling, "G-T3", "CS-R:fuel_allotment", S.EXCLUDED), "raises_to enum")
    check(raises(S.StandingError, S.coupling, "G-T3", "CS-R:nope", S.MEMBER), "unknown target refused")
    saved = dict(S.F.LAYER_OF)
    try:
        S.F.LAYER_OF["G-INT"] = ("TRIBAL", "constructed internal gate")
        check(raises(S.StandingError, S.coupling, "G-INT", "CS-R:fuel_allotment", S.MEMBER),
              "a TRIBAL-layer source is refused as internal [CHOICE 70]")
    finally:
        S.F.LAYER_OF.clear()
        S.F.LAYER_OF.update(saved)
    c = S.coupling("G-LAND", "CS-R:housing_assignment", S.MEMBER)
    check(c["flags"] == ["LAYER_NOT_RECORDED"], "NOT_RECORDED layer accepted and flagged")
    cp = S.seed_couplings()
    check(len(cp) == 1 and cp[0]["layer"] == "STATE" and cp[0]["provenance"] == "CONSTRUCTED_UNSOURCED",
          "one constructed coupling, state layer")
    fl = dict(S.scarcity_flags())
    check(fl["CS-R:housing_assignment"] == S.SCARCITY_UNATTRIBUTED, "RULE 2c: limited with no row is flagged")
    check(fl["CS-R:fuel_allotment"].startswith(S.IMPOSED_SCARCITY), "limited with a row is attributed")
    check(not any(v == S.SCARCITY_UNATTRIBUTED for v in dict(S.scarcity_flags(couplings=[
        S.coupling("G-T3", "CS-R:fuel_allotment", S.MEMBER),
        S.coupling("G-T3", "CS-R:housing_assignment", S.MEMBER)])).values()), "flag clears when attributed")
    r = [x for x in S.seed_routes() if x["route_id"] == "CS-R:fuel_allotment"][0]
    check(S.effective_min(r, cp) == S.MEMBER and S.effective_min(r, []) == S.ADMITTED, "raise [CHOICE 69]")
    h = [x for x in S.seed_routes() if x["route_id"] == "CS-R:housing_assignment"][0]
    check(S.effective_min(h, [S.coupling("G-T3", h["route_id"], S.MEMBER)]) == "AT_LEAST:MEMBER",
          "a raise over a NOT_RECORDED minimum is a floor, not a value")
    check(all(x["grade"] == "K" and x["source"] == "CONSTRUCTED_UNSOURCED" for x in S.seed_routes()),
          "routes K, constructed [CHOICE 71]")


def t_gap():
    pa = S.get_profile("P-ADMITTED")
    g = S.standing_gap(pa, "CS-R")
    check((g["gap"], g["gap_routes"], g["band"]) == (1, ["CS-R:fuel_allotment"], (1, 2)), "P-ADMITTED gap %s" % g)
    check(g["reachable_routes"] == ["CS-R:water"], "reachable_routes applies 2b [CHOICE 72]")
    g0 = S.standing_gap(pa, "CS-R", couplings=[])
    check((g0["gap"], g0["band"]) == (0, (0, 1)), "without the coupling: gap 0, band [0, 1]")
    nr = S.standing_gap(S.get_profile("P-NR"), "CS-R")
    check((nr["gap"], nr["band"], len(nr["undetermined"])) == (0, (0, 3), 3),
          "NOT_RECORDED standing: band [0, 3], never gap 0 alone [CHOICE 68]")
    m = S.standing_gap(S.get_profile("P-1"), "CS-R")
    check(m["gap"] == 0 and m["undetermined"] == ["CS-R:housing_assignment"], "MEMBER: gap 0, housing undetermined")
    check(S.standing_gap(pa, "CS-G")["band"] == (0, 0), "no routes declared in CS-G: band [0, 0]")
    check(g["unit"] == "routes", "unit carried")


# ------------------------------------------------------------------ 2d / 3 ---

def t_consolidation():
    evs = S.consolidation_events()
    check([e["event_id"] for e in evs] == ["CE-1", "CE-3"], "two consolidation events")
    check(all(e["peoples_in"] == S.NOT_RECORDED and e["prior_mode_of_peoples_in"] == S.NOT_RECORDED for e in evs),
          "peoples_in and prior mode NOT_RECORDED: no source names them")
    check(raises(S.StandingError, S.consolidation_event, "x", "i", "d", "S", S.NOT_RECORDED, "u", "EXPULSION",
                 S.NOT_RECORDED, "s"), "mechanism enum")
    check(raises(S.StandingError, S.consolidation_event, "x", "i", "d", "S", S.NOT_RECORDED, "u", "REMOVAL",
                 "NOMADIC", "s"), "prior-mode enum")
    check(raises(S.StandingError, S.consolidation_event, "x", "i", "d", "S", "several", "u", "REMOVAL",
                 S.NOT_RECORDED, "s"), "peoples_in is a list or NOT_RECORDED")
    a, b = S.ce1_figures()
    check(a["scope"] != b["scope"], "CE-1 figures carry distinct scopes")
    check(raises(S.ScopePooled, S.pool_figures, a, b), "CE-1 figures never pooled (section 6)")
    check(raises(S.ScopePooled, S.pool_figures, a, a), "no pooling rule even within one scope")
    check(b["grade"] == S.NOT_RECORDED and a["grade"] == "S", "NPS grade not borrowed [CHOICE 75]")
    w = S.worcester_split()
    check(w["lawful_reach"] == S.FALSE and w["diverge"], "CE-2: lawful reach and outcome diverge")
    ac = S.alaska_cases()
    check([c["control"] for c in ac] == [False, True] and ac[1]["mechanism"] is None, "Metlakatla control [CHOICE 76]")
    o = S.ce3_other_mechanism()
    check((o["count"], o["over"]) == (0, 1), "E-A6.1-3: 0 of 1 non-control cases")
    check(S.SOURCES_A61["CE-3k"]["grade"] == "K" and S.SOURCES_A61["CE-3k"]["input"] is False,
          "pipeline link K, not an input")
    rp = S.residence_presuming_paths()
    check((rp["count"], rp["total_paths"], rp["list"]) == (1, S.NOT_RECORDED, "TRUNCATED"),
          "E-A6-3 revised: 1 path, lower bound [CHOICE 74]")
    check("understood flexibly" in rp["flexibility_clause"] and "not a requirement" in rp["sufficiency"],
          "flexibility clause recorded beside the paths")
    check(E6.residence_presuming_criteria()["status"] == S.NOT_EVALUABLE, "A-6's criteria reading kept, unedited")
    cc = S.chain_count()
    check((cc["literal_links_only"], cc["admitted"], cc["band"]) == (1, 0, (0, 1)), "chain band [CHOICE 73]")
    ch = S.presumption_chains()[0]
    check(ch["join"] == S.NOT_RECORDED and "S-2" in ch["missing"], "the missing join is named")
    joined = [dict(ch, join=S.TRUE)]
    check(S.chain_count(joined)["band"] == (1, 1), "a sourced join admits the chain")


# ------------------------------------------------------------ expectations ---

def t_expected():
    rows = S.check_expectations()
    st = dict((r["id"], r["status"]) for r in rows)
    check(rows[0]["id"] == "E-A6.1-2" and rows[0]["status"] == S.NOT_EVALUABLE, "the row not holding is first")
    check(st == {"E-A6.1-1": "MATCH", "E-A6.1-2": S.NOT_EVALUABLE, "E-A6.1-3": "MATCH", "E-A6-3 REVISED": "MATCH"},
          "statuses %s" % st)
    check(S._v("E-A6.1-2", 1) == "MATCH" and S._v("E-A6.1-2", 0) == "MISMATCH",
          "E-A6.1-2 literal and absent readings both reachable")
    comp = dict((x["id"], R.complement(x)["status"]) for x in S.registry())
    check(comp["E-A6.1-1"] == "COMPLEMENT" and comp["E-A6.1-3"] == "COMPLEMENT", "two complements")
    check(comp["E-A6.1-2"] == "GAP", "E-A6.1-2 GAP at NOT_EVALUABLE")
    check(comp["E-A6-3 REVISED"] != "COMPLEMENT", "E-A6-3 revised: no falsifier sentence (%s)" % comp["E-A6-3 REVISED"])
    q = S.C.quotes_present(S.registry(), S.AMENDMENT_FILE)
    check(all(x[2] for x in q) and len(q) == 7, "7 quotes found verbatim")
    lt = S.C.lint_two_ways(S.AMENDMENT_FILE)
    check((lt["fail_a31_list"], lt["fail_with_annotation"], len(lt["tokens"])) == (8, 4, 8), "A-6.1 lint 8, then 4")
    ff = S.fail_fixture()
    FAIL_FIXTURE[0] = (ff["a6_P-0"] == ff["a6_P-ADMITTED"] and ff["a61_P-0"] != ff["a61_P-ADMITTED"])
    check(FAIL_FIXTURE[0], "A-6's boolean reads P-0 and P-ADMITTED identically; 2a separates them")


# ---------------------------------------------------------------- hygiene ---

def t_hygiene():
    r = render()
    sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
    try:
        import no_severity
        ok, h = no_severity.check(r)
        check(ok, "render screens clean (%s)" % [x[1] for x in h][:5])
    except ImportError:
        pass
    src = os.path.join(HERE, "standing_a61.py")
    for seed in ("1", "2"):
        p = subprocess.run([sys.executable, src], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONHASHSEED=seed))
        check(p.stdout == r, "render identical under PYTHONHASHSEED=%s" % seed)
    p = subprocess.run([sys.executable, src, "--selftest"], capture_output=True, text=True)
    check(p.returncode == 2, "refuses --selftest")
    p = subprocess.run([sys.executable, src, "--choices"], capture_output=True, text=True)
    check(len([l for l in p.stdout.splitlines() if l.startswith("[CHOICE")]) == len(S.CHOICES), "--choices")
    check(sorted(S.CHOICES) == list(range(66, 78)), "choices numbered 66..77")
    text = open(src).read()
    body = text.split('"""', 2)[2]
    start = body.index("CHOICES = {")
    end = body.index("\n}\n", start)
    rest = body[:start] + body[end:]
    for k in S.CHOICES:
        check(("[CHOICE %d]" % k) in rest, "[CHOICE %d] cited outside its declaration" % k)
    raw = open(src, "rb").read()
    check(all(b < 128 for b in raw), "ASCII")
    tree = ast.parse(raw.decode("ascii"), feature_version=(3, 8))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) in ("sum",):
            check(False, "no sum() anywhere: figures and gaps are never totalled")
    log = subprocess.run(["git", "log", "--format=%h", "-n", "1", "--", S.AMENDMENT_FILE], cwd=HERE,
                         capture_output=True, text=True).stdout.strip()
    if log:
        check(log == S.EXPECTED_COMMIT_A61, "the amendment's last commit is the EXPECTED commit (%s)" % log)
    amend = open(os.path.join(HERE, S.AMENDMENT_FILE), encoding="utf-8").read()
    check(amend.startswith("# FWO AMENDMENT A-6.1") and "&gt;" not in amend and "&amp;" not in amend,
          "amendment landed with entities decoded")
    sample = os.path.join(HERE, "samples", "standing_a61.sample.txt")
    if os.path.exists(sample):
        check(open(sample, encoding="utf-8").read() == r, "sample matches a fresh render")
    p = subprocess.run([sys.executable, os.path.join(HERE, "test_chains_a456.py")], capture_output=True)
    check(p.returncode == 0, "test_chains_a456.py still green")


for fn in (t_standing, t_routes, t_gap, t_consolidation, t_expected, t_hygiene):
    fn()

n = 1 if FAIL_FIXTURE[0] else 0
tag = "" if n else "  NO_FAIL_FIXTURE"
print("standing-a61: %d checks, %d failed; fail fixtures present: %d of 1%s" % (_checks, _failed, n, tag))
sys.exit(1 if _failed else 0)
