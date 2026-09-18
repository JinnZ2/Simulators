# SPDX-License-Identifier: CC0-1.0
# test_revision.py -- checks for revision_survival, revision 2. Stdlib only,
# no pytest, no network. Run: python3 test_revision.py
#
# Expected verdicts and counts live HERE and not in cases.py, so no record
# can agree with the instrument by construction. Constructed worlds are
# built in this file, labelled, drawn under a declared frame (D-C1), and
# authored under a name that is not the key's.
#
# D-C3: this file carries no bare float comparison against a decimal
# literal either -- `near()` states its tolerance and takes the literal
# as an argument, which is what the rule asks of the instrument.

import ast
import copy
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import cases                        # noqa: E402
import draw_frame as df             # noqa: E402
import revision_survival as rs      # noqa: E402
import no_severity                  # noqa: E402

CHECKS = []


def check(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


def refuses(fn, *a, **k):
    try:
        fn(*a, **k)
    except (rs.RefusedInput, df.RefusedFrame):
        return True
    return False


def near(a, b):
    """|a - b| < EPS, the tolerance stated once (D-C3)."""
    return a is not None and b is not None and abs(a - b) < rs.EPS


ORDER = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()
ORDER2 = open(os.path.join(HERE, "WORK_ORDER_V2.md"), encoding="utf-8").read()
README = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()


def braces(text, key):
    m = re.search(re.escape(key) + r"\s*\u2208?\s*\{([^}]*)\}", text)
    return tuple(x.strip() for x in m.group(1).replace("\n", " ").split(","))


# ---------------------------------------------------------------------------
# 1. vocabularies: v1 read out of WORK_ORDER.md, v2 out of WORK_ORDER_V2.md
# ---------------------------------------------------------------------------

check("VERDICTS match the order", braces(ORDER, "verdict") == rs.VERDICTS)
m = re.search("mechanism \u2208 \{([^}]*)\}", ORDER)
order_mechs = tuple(" ".join(x.split()) for x in m.group(1).split(","))
check("MECHANISMS match the order", order_mechs == rs.MECHANISMS)
sec = ORDER.split("RETURN ENUM")[1].split("KNOWN DEFECTS")[0]
order_returns = tuple(re.findall(r"^  ([A-Z_]+)\s{2,}", sec, re.M))
check("RETURNS_V1 match the order", order_returns == rs.RETURNS_V1,
      "%s" % (order_returns,))
sec2 = ORDER2.split("RETURN ENUM")[1].split("RUN RECORD")[0]
added = tuple(re.findall(r"^  ([A-Z_]+)\s{2,}", sec2, re.M))
check("RETURNS_V2_ADDED are the two the dispatch adds",
      added == rs.RETURNS_V2_ADDED == ("VOID_KEY_HOLDER",
                                       "INSUFFICIENT_REVISED"), "%s" % (added,))
check("RETURNS = v1 + v2, in that order",
      rs.RETURNS == rs.RETURNS_V1 + rs.RETURNS_V2_ADDED and len(rs.RETURNS) == 7)
check("established_where is the dispatch's set",
      braces(ORDER2, "established_where") == rs.ESTABLISHED_WHERE)
check("axis_1 decision_reversibility is the dispatch's set",
      braces(ORDER2, "decision_reversibility") == rs.DECISION_REVERSIBILITY)
check("axis_2 pathway_exists is the dispatch's set",
      braces(ORDER2, "pathway_exists") == rs.PATHWAY_EXISTS)
check("n_revised_min = 24 is the dispatch's",
      "n_revised_min = 24" in ORDER2 and rs.N_REVISED_MIN == 24)
check("the three D-C3 rules are quoted from the dispatch",
      "abs(delta) < 0.15 + 1e-9" in ORDER2
      and "(mean_conf - acc) > 0.20 - 1e-9" in ORDER2
      and "frac >= 0.40 - 1e-9" in ORDER2)
check("thresholds read as the order's decimals",
      repr(rs.LEAK_THRESHOLD) == "0.15" and repr(rs.OVERCONF_THRESHOLD) == "0.2"
      and repr(rs.SURVIVED_FLOOR) == "0.4" and repr(rs.SURVIVAL_CUT) == "0.8"
      and repr(rs.EPS) == "1e-09")
check("Y = 2005 and N >= 40 are the order's",
      "Y = 2005" in ORDER and rs.Y == 2005 and "N\u226540" in ORDER
      and rs.N_FLOOR == 40)
runsec = ORDER2.split("RUN RECORD")[1].split("README FRAMING")[0]
check("RUN RECORD required fields are the dispatch's, each named there",
      all(k in runsec for k in ("frame_declaration", "delta_open_blind",
                                 "acc_label", "acc_mech_revised",
                                 "n_revised", "key_holder", "respondent"))
      and "defect log" in runsec and set(rs.RUN_RECORD_REQUIRED) >= {
          "frame_declaration", "delta_open_blind", "acc_label",
          "acc_mech_revised", "n_revised", "arm_c", "defect_log",
          "key_holder", "respondent", "key_holder_respondent_differ"})
for phrase in ("do not re-populate seeds from model recall",
               "do not pool Q_mech",
               "do not rank NO_SUBSTITUTION_EXISTS",
               "do not score a self-run"):
    check("DO NOT list carries: %s" % phrase, phrase in ORDER2)

# ---------------------------------------------------------------------------
# 2. draw_frame -- the declared draw (D-C1)
# ---------------------------------------------------------------------------

FATE = "fate adjudicated after the draw by the outcome record, this rule " \
       "written before it"
F = df.draw("constructed://index", "2005 ed.", 400, 11, 6, FATE)
check("draw is deterministic on the stdlib RNG (pinned)",
      F["positions"] == [231, 238, 260, 286, 300, 399]
      and F["frame_id"].startswith("a91adae73742"), "%s %s"
      % (F["positions"], F["frame_id"][:12]))
check("same inputs, same frame_id",
      df.draw("constructed://index", "2005 ed.", 400, 11, 6, FATE) == F)
check("a different seed moves the positions and the id",
      df.draw("constructed://index", "2005 ed.", 400, 12, 6, FATE)["positions"]
      != F["positions"])
check("positions are sorted, distinct, inside the index",
      F["positions"] == sorted(set(F["positions"]))
      and all(0 <= p < 400 for p in F["positions"]))
check("frame carries every REQUIRED field",
      all(k in F for k in df.REQUIRED))
check("check_frame passes a clean frame", df.check_frame(F) is F)
t = copy.deepcopy(F); t["positions"][0] = 5
check("check_frame refuses an edited position list",
      refuses(df.check_frame, t))
t = copy.deepcopy(F); t["fate_rule"] = "rewritten after the draw"
check("check_frame refuses an edited fate rule", refuses(df.check_frame, t))
t = copy.deepcopy(F); t["frame_id"] = "0" * 64
check("check_frame refuses an edited frame_id", refuses(df.check_frame, t))
t = copy.deepcopy(F); del t["edition"]
check("check_frame refuses a frame missing a field", refuses(df.check_frame, t))
check("check_frame refuses a non-dict", refuses(df.check_frame, None))
check("draw refuses an empty source", refuses(df.draw, "", "e", 10, 1, 2, FATE))
check("draw refuses an empty edition (not Y-vintage)",
      refuses(df.draw, "s", " ", 10, 1, 2, FATE))
check("draw refuses n > index_size", refuses(df.draw, "s", "e", 10, 1, 11, FATE))
check("draw refuses a bool seed", refuses(df.draw, "s", "e", 10, True, 2, FATE))
check("draw refuses a non-int index", refuses(df.draw, "s", "e", "10", 1, 2, FATE))
check("draw refuses an empty fate rule", refuses(df.draw, "s", "e", 10, 1, 2, ""))
check("in_draw is True on a drawn position", df.in_draw(F, 231) is True)
check("in_draw is False off the draw", df.in_draw(F, 232) is False)
check("in_draw is False on None (no position is not a position)",
      df.in_draw(F, None) is False and df.in_draw(F, True) is False)
check("render prints the frame_id and the positions",
      F["frame_id"] in df.render(F) and "231 238 260" in df.render(F))
p = subprocess.run([sys.executable, os.path.join(HERE, "draw_frame.py"),
                    "--selftest"], capture_output=True)
check("draw_frame --selftest is refused with exit 2", p.returncode == 2)
p = subprocess.run([sys.executable, os.path.join(HERE, "draw_frame.py")],
                   capture_output=True)
check("draw_frame with no arguments exits 2 and says no draw is shipped",
      p.returncode == 2 and b"no draw is shipped" in p.stderr)
p = subprocess.run([sys.executable, os.path.join(HERE, "draw_frame.py"),
                    "--source=constructed://index", "--edition=2005 ed.",
                    "--index-size=400", "--seed=11", "--n=6",
                    "--fate-rule=" + FATE], capture_output=True)
check("draw_frame CLI reproduces the pinned frame",
      p.returncode == 0 and F["frame_id"].encode() in p.stdout)

# ---------------------------------------------------------------------------
# 3. intake refuses, by field
# ---------------------------------------------------------------------------

good = copy.deepcopy(cases.CLAIMS[0])
check("a well-formed claim reads", rs.read_claim(good)["id"] == "seed-01")
for k in ("id", "statement", "field_nouns", "established_as_of_Y",
          "established_basis", "outcome", "status", "author",
          "established_where"):
    bad = copy.deepcopy(good); del bad[k]
    check("claim refused without %s" % k, refuses(rs.read_claim, bad))
for k in ("label", "mechanism", "basis", "verified", "source"):
    bad = copy.deepcopy(good); del bad["outcome"][k]
    check("claim refused without outcome.%s" % k, refuses(rs.read_claim, bad))
bad = copy.deepcopy(good); bad["outcome"]["label"] = "REFUTED"
check("claim refused on a label outside the vocabulary", refuses(rs.read_claim, bad))
bad = copy.deepcopy(good); bad["outcome"]["mechanism"] = "confounding"
check("claim refused on a mechanism outside the vocabulary "
      "(confounding is what seed-04 needed and the vocabulary lacks, RS_007)",
      refuses(rs.read_claim, bad))
bad = copy.deepcopy(good); bad["established_where"] = "textbook"
check("claim refused on established_where outside the set", refuses(rs.read_claim, bad))
bad = copy.deepcopy(good); bad["draw_position"] = -1
check("claim refused on a negative draw_position", refuses(rs.read_claim, bad))
bad = copy.deepcopy(good); bad["draw_position"] = True
check("claim refused on a bool draw_position", refuses(rs.read_claim, bad))
bad = copy.deepcopy(good); bad["status"] = "RECALLED"
check("claim refused on a status outside CLAIM_STATUS", refuses(rs.read_claim, bad))
check("draw_position defaults to None when absent",
      rs.read_claim(good)["draw_position"] is None)
r0 = copy.deepcopy(cases.RESPONSES_OPEN[0])
check("a well-formed response reads", rs.read_response(r0)["claim_id"] == "seed-01")
for k in ("claim_id", "condition", "verdict", "confidence", "mechanism",
          "flag_evidence", "author"):
    bad = copy.deepcopy(r0); del bad[k]
    check("response refused without %s" % k, refuses(rs.read_response, bad))
bad = copy.deepcopy(r0); bad["confidence"] = 1.2
check("response refused on confidence > 1", refuses(rs.read_response, bad))
bad = copy.deepcopy(r0); bad["confidence"] = True
check("response refused on a bool confidence", refuses(rs.read_response, bad))

# ---------------------------------------------------------------------------
# 4. the shipped corpus under D-C1: nothing is DRAWN, nothing scores
# ---------------------------------------------------------------------------

claims = [rs.read_claim(c) for c in cases.CLAIMS]
check("no shipped frame (cases.FRAME is None)", cases.FRAME is None)
check("every shipped record is CANDIDATE: none DELIVERED, none DRAWN, "
      "none carries a draw_position (DO NOT: no seeds from recall)",
      all(c["status"] == "CANDIDATE" and c["draw_position"] is None
          for c in claims) and len(claims) == 17)
adm, exc = rs.admit(claims, None)
check("zero admitted, seventeen excluded, every reason status=CANDIDATE",
      adm == [] and len(exc) == 17
      and all(why == "status=CANDIDATE" for _, why in exc))
adm_f, exc_f = rs.admit(claims, F)
check("a frame does not admit a CANDIDATE row either", adm_f == [])
where = {c["id"]: c["established_where"] for c in claims}
check("alpha wolf and junk DNA carry established_where = popular",
      where["seed-01"] == "popular" and where["seed-09"] == "popular")
check("every other shipped record reads both",
      all(v == "both" for k, v in where.items() if k not in ("seed-01", "seed-09")))
by_date = {c["id"]: c["established_as_of_Y"] for c in claims}
check("five rev-1 seeds read NO as of 2005 and stay out (D-C1)",
      sorted(k for k, v in by_date.items() if v == "NO") ==
      ["seed-03", "seed-04", "seed-10", "seed-11", "seed-12"])
check("the dispatch's seven admissible seeds are six YES plus one UNCERTAIN "
      "(seed-02); all seven ship as CANDIDATE only (RS_017)",
      sum(1 for k, v in by_date.items() if v == "YES" and k.startswith("seed")) == 6
      and by_date["seed-02"] == "UNCERTAIN")
check("every shipped outcome is carried, none verified",
      all(c["outcome"]["verified"] is False for c in claims))

# ---------------------------------------------------------------------------
# 5. a constructed DRAWN world under a declared frame
# ---------------------------------------------------------------------------

RESPONDER = "constructed responder (not the key's author)"
KEY_AUTHOR = "constructor (key)"
NON_NONE = [m for m in rs.MECHANISMS if m != "NONE_GIVEN"]
WF = df.draw("constructed://index", "2005 ed.", 400, 11, 50, FATE)


def world(n, survived_share, frame=WF, where="both", status="DRAWN"):
    out = []
    n_surv = int(round(n * survived_share))
    for i in range(n):
        surv = i < n_surv
        label = "SURVIVED" if surv else rs.VERDICTS[1 + (i % 4)]
        mech = "NONE_GIVEN" if surv else NON_NONE[i % len(NON_NONE)]
        out.append(rs.read_claim({
            "id": "w-%02d" % i, "statement": "constructed claim %d" % i,
            "field_nouns": [], "established_as_of_Y": "YES",
            "established_basis": "constructed", "status": status,
            "established_where": where,
            "draw_position": frame["positions"][i] if frame else None,
            "author": KEY_AUTHOR,
            "outcome": {"label": label, "mechanism": mech, "basis": "built",
                        "verified": False, "source": "constructed"}}))
    return out


def respond(claims_, cond, label_acc, mech_acc, conf, author=RESPONDER):
    out = []
    n = len(claims_)
    n_l = int(round(n * label_acc))
    n_m = int(round(n * mech_acc))
    for i, c in enumerate(claims_):
        key = c["outcome"]
        v = key["label"] if i < n_l else \
            rs.VERDICTS[(rs.VERDICTS.index(key["label"]) + 1) % 5]
        mch = key["mechanism"] if i < n_m else \
            rs.MECHANISMS[(rs.MECHANISMS.index(key["mechanism"]) + 1) % 9]
        out.append(rs.read_response({
            "claim_id": c["id"], "condition": cond, "verdict": v,
            "confidence": conf, "mechanism": mch, "flag_evidence": "built",
            "author": author}))
    return out


def score(W, open_l, open_m, blind_l, blind_m, conf=0.6, author=RESPONDER,
          blind=True, frame=WF):
    rs_ = respond(W, "OPEN", open_l, open_m, conf, author)
    if blind:
        rs_ += respond(W, "BLIND", blind_l, blind_m, conf, author)
    return rs.score_arm_a(W, rs_, frame=frame)


W = world(50, 0.4)
check("constructed world: 50 drawn rows, 20 SURVIVED, 30 revised",
      len(W) == 50 and sum(1 for c in W if c["outcome"]["label"] == "SURVIVED") == 20)
adm_w, exc_w = rs.admit(W, WF)
check("the frame admits every drawn row", len(adm_w) == 50 and exc_w == [])
check("without a frame every drawn row is excluded, naming D-C1",
      rs.admit(W, None)[0] == [] and
      all(why == "no frame_declaration (D-C1)" for _, why in rs.admit(W, None)[1]))
Wpop = world(4, 0.5, where="popular")
check("a popular row is excluded with its reason",
      rs.admit(Wpop, WF)[0] == [] and
      all(why == "established_where=popular" for _, why in rs.admit(Wpop, WF)[1]))
Wsp = world(4, 0.5, where="specialist")
check("a specialist row is admitted", len(rs.admit(Wsp, WF)[0]) == 4)
Wout = world(50, 0.4)
OFF = min(set(range(400)) - set(WF["positions"]))   # a position the draw did not produce
Wout[3]["draw_position"] = OFF
check("a row entered outside the draw is excluded, naming its position",
      ("w-03", "entered_outside_draw position=%d" % OFF) in rs.admit(Wout, WF)[1])
Wno = world(4, 0.5); Wno[0]["established_as_of_Y"] = "NO"
check("a drawn row not established as of Y is excluded",
      ("w-00", "established_as_of_2005=NO") in rs.admit(Wno, WF)[1])

# the HARD GATE
CAL = score(W, 0.8, 0.8, 0.76, 0.76)
NOFRAME = score(W, 0.8, 0.8, 0.76, 0.76, frame=None)
OUT = score(Wout, 0.8, 0.8, 0.76, 0.76)
BADF = copy.deepcopy(WF); BADF["positions"][0] = 3
BAD = score(W, 0.8, 0.8, 0.76, 0.76, frame=BADF)
check("HARD GATE: no frame -> VOID_NO_FRAME, no score",
      NOFRAME["return"] == "VOID" and NOFRAME["score"] is None and
      any(v.startswith("VOID_NO_FRAME") for v in NOFRAME["void"]))
check("HARD GATE: a row outside the draw -> VOID_OUTSIDE_DRAW naming it",
      OUT["return"] == "VOID" and
      any(v.startswith("VOID_OUTSIDE_DRAW: w-03") for v in OUT["void"]))
check("HARD GATE: a frame that does not verify -> VOID_BAD_FRAME",
      BAD["return"] == "VOID" and
      any(v.startswith("VOID_BAD_FRAME") for v in BAD["void"]))
check("a void result carries its table and no score",
      NOFRAME["per_condition"]["OPEN"]["n"] == 0 and NOFRAME["score"] is None)
check("a verified frame is carried on the result", CAL["frame"] is WF)

# ---------------------------------------------------------------------------
# 6. D-C3 comparison rules and D-C4 sizing
# ---------------------------------------------------------------------------

d = rs.delta(0.4, 0.55)
check("delta(0.4, 0.55) is the float that refused the rev-1 known answer",
      repr(d) == "-0.15000000000000002")
check("LEAK_GATE passes it: abs(delta) < 0.15 + 1e-9",
      rs.passes_leak_gate(d) is True)
check("LEAK_GATE fails at 0.16", rs.passes_leak_gate(rs.delta(0.56, 0.4)) is False)
check("LEAK_GATE is None on None", rs.passes_leak_gate(None) is None)
check("OVERCONF_GATE fires at 0.6 - 0.4 (0.20000000000000004)",
      rs.overconfident(0.6, 0.4) is True)
check("OVERCONF_GATE fires at exactly 0.2 from below-float arithmetic",
      rs.overconfident(0.7, 0.5) is True)
check("OVERCONF_GATE is silent at 0.19", rs.overconfident(0.59, 0.4) is False)
check("OVERCONF_GATE is None on an absent side",
      rs.overconfident(None, 0.4) is None and rs.overconfident(0.6, None) is None)
check("SURVIVED_FLOOR passes 2 of 5", rs.passes_survived_floor(2 / 5.0) is True)
check("SURVIVED_FLOOR passes 0.4 reached by subtraction",
      rs.passes_survived_floor(1.0 - 0.6) is True)
check("SURVIVED_FLOOR fails 0.39", rs.passes_survived_floor(0.39) is False)
check("SURVIVED_FLOOR is None on None", rs.passes_survived_floor(None) is None)
check("[CHOICE 8] Arm C cut: 0.79 below, 0.8 not, 0.8 - 1e-10 not",
      rs.below_survival_cut(0.79) is True and rs.below_survival_cut(0.8) is False
      and rs.below_survival_cut(0.8 - 1e-10) is False)
check("n_required: 24 / (1 - 0.4) = 40", rs.n_required(0.4) == 40)
check("n_required: 24 / (1 - 0.6) = 60", rs.n_required(0.6) == 60)
check("n_required rounds up: 24 / (1 - 0.5) = 48, 24 / 0.45 -> 54",
      rs.n_required(0.5) == 48 and rs.n_required(0.55) == 54)
check("n_required is None at survived 1.0 (no revised rows at any N)",
      rs.n_required(1.0) is None and rs.n_required(None) is None)
check("D-C4 tension is stated in the module: D1's floor and the informative "
      "subset pull opposite ways",
      "pull opposite" in rs.__doc__ and "REVISED subset" in rs.__doc__)

# ---------------------------------------------------------------------------
# 7. Arm A on constructed worlds -- every RETURN member reachable
# ---------------------------------------------------------------------------

LEAK = score(W, 0.9, 0.9, 0.4, 0.4)
LABEL = score(W, 0.9, 0.4, 0.9, 0.4)
UNCAL = score(W, 0.4, 0.4, 0.4, 0.4)
OVER = score(W, 0.7, 0.8, 0.66, 0.76, conf=0.99)
NODELTA = score(W, 0.8, 0.8, None, None, blind=False)
SAME = score(W, 0.8, 0.8, 0.76, 0.76, author=KEY_AUTHOR)
W60 = world(50, 0.6)
INSUF = score(W60, 0.8, 0.8, 0.76, 0.76)

check("CALIBRATED reachable", CAL["return"] == "CALIBRATED" and not CAL["void"],
      "%s %s" % (CAL["return"], CAL["void"]))
check("LEAK_DOMINATED reachable", LEAK["return"] == "LEAK_DOMINATED")
check("LABEL_ONLY reachable", LABEL["return"] == "LABEL_ONLY")
check("UNCALIBRATED reachable", UNCAL["return"] == "UNCALIBRATED")
check("OVERCONFIDENT rides as a co-flag on both conditions",
      OVER["return"] == "CALIBRATED" and
      OVER["co_flags"] == ["OVERCONFIDENT(OPEN)", "OVERCONFIDENT(BLIND)"])
check("no co-flag at honest confidence", CAL["co_flags"] == [])
check("VOID with no BLIND arm, naming VOID_NO_DELTA",
      NODELTA["return"] == "VOID" and NODELTA["delta"] is None and
      any(v.startswith("VOID_NO_DELTA") for v in NODELTA["void"]))
check("VOID_KEY_HOLDER when key and responses share a party; never a score",
      SAME["return"] == "VOID_KEY_HOLDER" and SAME["score"] is None and
      SAME["key_holder_respondent_differ"] is False)
check("key_holder and respondent are reported and differ on the honest world",
      CAL["key_holder"] == [KEY_AUTHOR] and CAL["respondent"] == [RESPONDER]
      and CAL["key_holder_respondent_differ"] is True)
check("INSUFFICIENT_REVISED reachable: 20 revised of 50 at survived 0.6",
      INSUF["return"] == "INSUFFICIENT_REVISED" and
      INSUF["per_condition"]["BLIND"]["n_revised"] == 20 and
      INSUF["per_condition"]["BLIND"]["acc_mech_revised"] is None and
      INSUF["per_condition"]["BLIND"]["mech_status"] == "INSUFFICIENT_REVISED")
check("INSUFFICIENT_REVISED is a number refused, not a number",
      INSUF["delta_mech_revised"] is None and INSUF["score"] == "INSUFFICIENT_REVISED")
check("n_required prints 60 on the 0.6 world and 40 on the 0.4 world",
      INSUF["n_required"] == 60 and CAL["n_required"] == 40)
check("every RETURN member is produced by some world",
      {CAL["return"], LEAK["return"], LABEL["return"], UNCAL["return"],
       SAME["return"], INSUF["return"]}
      | set(f.split("(")[0] for f in OVER["co_flags"]) == set(rs.RETURNS))
check("VOID (no frame / no delta) is a refusal, not an enum member",
      "VOID" not in rs.RETURNS and NOFRAME["return"] == "VOID")
check("[CHOICE 3] gate delta is the larger by magnitude of those present",
      near(LEAK["delta"], max(LEAK["delta_label"], LEAK["delta_mech_revised"],
                              key=abs)))
check("[CHOICE 3] with mech delta absent the gate reads the label delta",
      INSUF["delta"] is not None and near(INSUF["delta"], INSUF["delta_label"]))
check("a leak of 0.5 in mechanism alone voids",
      score(W, 0.8, 0.9, 0.8, 0.4)["return"] == "LEAK_DOMINATED")
check("D1 does not fire on the 0.4 world",
      not any(x.startswith("D1") for x in CAL["defects"]))
check("BELOW_N_FLOOR does not fire at n = 50",
      not any(x.startswith("BELOW_N") for x in CAL["defects"]))
check("D4 fires on a carried key regardless of the rest",
      any(x.startswith("D4") for x in CAL["defects"]))
check("revised-row denominator is 30 of 50 on the 0.4 world",
      CAL["per_condition"]["OPEN"]["n_revised"] == 30)
check("chance for mechanism on revised rows is over 8 members, not the "
      "NONE_GIVEN share", near(CAL["per_condition"]["OPEN"]["chance_mech_revised"],
                              max(1 / 8.0, 4 / 30.0)))
ALLS = world(30, 1.0)
r_alls = rs.score_arm_a(ALLS, respond(ALLS, "OPEN", 0.7, 0.7, 0.5)
                        + respond(ALLS, "BLIND", 0.7, 0.7, 0.5), frame=WF)
check("on an all-SURVIVED key the revised-row Q_mech is None over 0 rows",
      r_alls["per_condition"]["OPEN"]["acc_mech_revised"] is None and
      r_alls["per_condition"]["OPEN"]["n_revised"] == 0 and
      r_alls["n_required"] is None)

# DO NOT pool Q_mech: no pooled field anywhere
SRC = open(os.path.join(HERE, "revision_survival.py")).read()
check("no pooled Q_mech: the token acc_mech never appears bare in the module",
      re.search(r"\bacc_mech\b", SRC) is None)
check("no pooled Q_mech: per-condition tables carry only the revised figure",
      all("acc_mech" not in per for per in CAL["per_condition"].values())
      and "delta_mech" not in CAL)

# ---------------------------------------------------------------------------
# 8. the shipped run
# ---------------------------------------------------------------------------

responses = [rs.read_response(r) for r in cases.RESPONSES_OPEN]
S = rs.score_arm_a(claims, responses, frame=cases.FRAME)
check("shipped Arm A returns VOID_KEY_HOLDER (the self-run outcome), score None",
      S["return"] == "VOID_KEY_HOLDER" and S["score"] is None)
check("shipped Arm A voids on all three reasons",
      sorted(v.split(":")[0] for v in S["void"]) ==
      ["VOID_KEY_HOLDER", "VOID_NO_DELTA", "VOID_NO_FRAME"])
check("shipped Arm A admits nothing and scores nothing",
      S["n_admitted"] == 0 and S["per_condition"]["OPEN"]["n"] == 0
      and S["n_required"] is None)
check("shipped Arm A states the N floor and D1 undefined",
      {x.split(":")[0] for x in S["defects"]} == {"BELOW_N_FLOOR", "D1"})
check("shipped key holder and respondent are one party",
      S["key_holder"] == S["respondent"] and S["key_holder_respondent_differ"] is False)

# ---------------------------------------------------------------------------
# 9. Arm B -- unchanged block, revised-row scoring
# ---------------------------------------------------------------------------

block = rs.read_block(copy.deepcopy(cases.ARM_B_BLOCK))
rec = rs.publish_record(block)
check("shipped record hash equals the recomputed seal",
      rec["sha256"] == cases.ARM_B_RECORD["sha256"], rec["sha256"])
check("review dates are T+24mo and T+60mo [CHOICE 6]",
      rec["review"] == ["2028-09-17", "2031-09-17"] == cases.ARM_B_RECORD["review"])
check("record carries k = 13", rec["k"] == 13 == len(block["claims"]))
tampered = copy.deepcopy(block); tampered["claims"][6]["p_survive"] = 0.95
check("one edited p_survive fails verify", rs.verify(tampered, rec) is False)
check("scoring a tampered block is VOID_HASH",
      rs.score_arm_b(tampered, rec, {}, "2031-09-17")["status"] == "VOID_HASH")
nd = rs.score_arm_b(block, rec, {}, "2026-09-18")
check("before the first review date: NOT_DUE, naming it",
      nd["status"] == "NOT_DUE" and nd["due"] == "2028-09-17")
outcomes = {c["id"]: {"label": c["verdict"], "mechanism": c["mechanism"]}
            for c in block["claims"][:10]}
sc = rs.score_arm_b(block, rec, outcomes, "2028-09-17")
check("on the review date with ten outcomes: SCORED, three unresolved",
      sc["status"] == "SCORED" and sc["n"] == 10 and
      sc["unresolved"] == ["B-11", "B-12", "B-13"])
check("Arm B reports acc_mech_revised, INSUFFICIENT below 24 revised, no pooled figure",
      sc["mech_status"] == "INSUFFICIENT_REVISED" and sc["acc_mech_revised"] is None
      and sc["n_revised"] < rs.N_REVISED_MIN and "acc_mech" not in sc)
check("a block with model UNKNOWN is refused", refuses(rs.read_block, dict(block, model="UNKNOWN")))
check("a block with model WITHHELD and a reason reads", block["model"].startswith("WITHHELD:"))
nop = copy.deepcopy(block); del nop["claims"][0]["p_survive"]
check("a claim without p_survive is refused [CHOICE 5]", refuses(rs.read_block, nop))

# ---------------------------------------------------------------------------
# 10. Arm C -- two axes, never one scale (D-C2)
# ---------------------------------------------------------------------------

C = rs.score_arm_c(cases.BRC_ROWS, block)
check("FINDING: two TERMINAL cells rest on a claim rated below the cut",
      C["finding"] == 2 and C["terminal_low"] == ["C5", "C9"])
check("NO_SUBSTITUTION_EXISTS: C3, C6, C8 (n/a, none), reported beside the finding",
      C["no_substitution_exists"] == ["C3", "C6", "C8"])
check("the finding never counts a NO_SUBSTITUTION_EXISTS row",
      not set(C["terminal_low"]) & set(C["no_substitution_exists"]))
check("every row carries both axes and a cell",
      all(r["axis_1"] in rs.DECISION_REVERSIBILITY and
          r["axis_2"] in rs.PATHWAY_EXISTS and r["cell"] for r in C["per_row"]))
check("B-12 is rated and under no row", C["claims_under_no_row"] == ["B-12"])
check("nine rows, the drop's register", C["n_rows"] == 9)
check("cell(n/a, none) is NO_SUBSTITUTION_EXISTS",
      rs.cell("n/a", "none") == rs.NO_SUBSTITUTION_EXISTS)
check("cell(n/a, partial|yes) is NOT_ON_RECORD",
      rs.cell("n/a", "partial") == rs.NOT_ON_RECORD == rs.cell("n/a", "yes"))
check("cell(terminal, none) is TERMINAL: a decision made, no pathway",
      rs.cell("terminal", "none") == "TERMINAL")
check("cell(UNDECLARED, *) is UNDECLARED", rs.cell(rs.UNDECLARED, "yes") == rs.UNDECLARED)
base = dict(cases.BRC_ROWS[0])
check("[CHOICE 9] (recoverable, none) is refused at intake",
      refuses(rs.read_brc_row, dict(base, decision_reversibility="recoverable",
                                    pathway_exists="none")))
check("[CHOICE 9] (costly, none) is refused at intake",
      refuses(rs.read_brc_row, dict(base, decision_reversibility="costly",
                                    pathway_exists="none")))
check("a class with no basis is refused", refuses(rs.read_brc_row, dict(base, basis="")))
check("an UNDECLARED class needs no basis",
      rs.read_brc_row(dict(base, decision_reversibility=rs.UNDECLARED,
                           basis=""))["decision_reversibility"] == rs.UNDECLARED)
check("an axis value outside the set is refused, both axes",
      refuses(rs.read_brc_row, dict(base, decision_reversibility="FATAL")) and
      refuses(rs.read_brc_row, dict(base, pathway_exists="maybe")))
rows2 = copy.deepcopy(cases.BRC_ROWS)
rows2.append(dict(base, id="X1", cycle="constructed", pathway_exists="none",
                  decision_reversibility="terminal", basis="c", rests_on=[]))
rows2.append(dict(base, id="X2", cycle="constructed", pathway_exists="none",
                  decision_reversibility="terminal", basis="c", rests_on=["B-04"]))
rows2.append(dict(base, id="X3", cycle="constructed", pathway_exists="partial",
                  decision_reversibility=rs.UNDECLARED, basis="", rests_on=[]))
rows2.append(dict(base, id="X4", cycle="constructed", pathway_exists="partial",
                  decision_reversibility="n/a", basis="c", rests_on=[]))
C2 = rs.score_arm_c(rows2, block)
check("TERMINAL_UNRATED reachable and kept apart", C2["terminal_unrated"] == ["X1"])
check("TERMINAL_RATED_HELD reachable and kept apart", C2["terminal_held"] == ["X2"])
check("UNDECLARED reachable and kept apart", C2["undeclared"] == ["X3"])
check("NOT_ON_RECORD reachable via (n/a, partial)", C2["not_on_record"] == ["X4"])
check("the finding is unchanged by the four added rows", C2["finding"] == 2)
check("a rests_on id absent from the block is refused, not skipped",
      refuses(rs.score_arm_c, [dict(base, rests_on=["B-99"])], block))
check("the Arm C result carries no rank, severity or ordering key",
      not any(k for k in C if "rank" in k or "sever" in k or "order" in k))
# DO NOT rank NO_SUBSTITUTION_EXISTS against TERMINAL: no ordering compare
# in the module has a cell name as an operand
tree_rs = ast.parse(SRC)
ordered = []
for node in ast.walk(tree_rs):
    if isinstance(node, ast.Compare) and any(
            isinstance(op, (ast.Lt, ast.Gt, ast.LtE, ast.GtE)) for op in node.ops):
        for c in [node.left] + node.comparators:
            if (isinstance(c, ast.Constant) and c.value in ("TERMINAL", "NO_SUBSTITUTION_EXISTS")) \
                    or (isinstance(c, ast.Name) and c.id == "NO_SUBSTITUTION_EXISTS"):
                ordered.append(node.lineno)
check("no ordering comparison in the module takes a cell name as an operand",
      ordered == [], "%s" % ordered)

# ---------------------------------------------------------------------------
# 11. D-C2 completeness assertion -- every enum registered with a derivation
# ---------------------------------------------------------------------------

NOT_ENUMS = {"RETURNS_V1", "RETURNS_V2_ADDED", "RUN_RECORD_REQUIRED"}
tuples = {}
for node in tree_rs.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 \
            and isinstance(node.targets[0], ast.Name) \
            and isinstance(node.value, ast.Tuple) and node.value.elts \
            and all(isinstance(e, ast.Constant) and isinstance(e.value, str)
                    for e in node.value.elts):
        tuples[node.targets[0].id] = tuple(e.value for e in node.value.elts)
check("every module-level string tuple is an enum in ENUMS or a declared non-enum",
      set(tuples) - NOT_ENUMS <= set(rs.ENUMS), "%s" % (set(tuples) - NOT_ENUMS - set(rs.ENUMS)))
check("RETURNS (a concatenation) is registered too", "RETURNS" in rs.ENUMS)
check("every ENUMS entry carries its members and a non-empty derivation",
      all(isinstance(v, tuple) and len(v) == 2 and v[0] == getattr(rs, k)
          and isinstance(v[1], str) and len(v[1]) > 40 for k, v in rs.ENUMS.items()))
check("the derivation for axis 1 names the fourth member as rev 1's missing cell",
      "n/a" in rs.ENUMS["DECISION_REVERSIBILITY"][1] and
      "not below terminal" in rs.ENUMS["DECISION_REVERSIBILITY"][1])
check("the derivation for RETURNS names both added members",
      "VOID_KEY_HOLDER" in rs.ENUMS["RETURNS"][1] and
      "INSUFFICIENT_REVISED" in rs.ENUMS["RETURNS"][1])
check("every declared non-enum exists and is a tuple",
      all(isinstance(getattr(rs, n), tuple) for n in NOT_ENUMS))

# ---------------------------------------------------------------------------
# 12. D-C3 repo test -- no bare float comparison against a decimal literal
# ---------------------------------------------------------------------------

def bare_float_compares(path):
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except (SyntaxError, UnicodeDecodeError, ValueError):
        return None
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for c in [node.left] + node.comparators:
                if isinstance(c, ast.Constant) and isinstance(c.value, float):
                    hits.append(node.lineno)
    return hits


SCOPED = ("revision_survival.py", "cases.py", "draw_frame.py", "test_revision.py")
for fn in SCOPED:
    h = bare_float_compares(os.path.join(HERE, fn))
    check("D-C3: %s has no bare float comparison" % fn, h == [], "lines %s" % h)
# [CHOICE 10]: the repo-wide count is recorded, not failed (RS_022)
files_hit, compares = 0, 0
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d_ for d_ in dns if not d_.startswith(".") and d_ != "__pycache__"]
    for fn in fns:
        if fn.endswith(".py"):
            h = bare_float_compares(os.path.join(dp, fn))
            if h:
                files_hit += 1
                compares += len(h)
check("[CHOICE 10] repo-wide bare-float count is recorded as a finding (RS_022)",
      files_hit > 0, "%d files, %d compares" % (files_hit, compares))
REPO_WIDE = (files_hit, compares)
def _scan_text(s):
    return [n.lineno for n in ast.walk(ast.parse(s)) if isinstance(n, ast.Compare)
            and any(isinstance(c, ast.Constant) and isinstance(c.value, float)
                    for c in [n.left] + n.comparators)]


check("the scan fires on a planted bare comparison and not on a BinOp comparator",
      _scan_text("x = a < 0.15") == [1] and _scan_text("x = a < T + 1e-9") == [])

# ---------------------------------------------------------------------------
# 13. run record -- required fields, refused without them
# ---------------------------------------------------------------------------

RR = rs.run_record(CAL, C, cases.DEFECT_LOG)
check("run record emits on the constructed world with every field",
      RR["emitted"] is True and RR["missing"] == [] and
      all(RR["record"][k] is not None for k in rs.RUN_RECORD_REQUIRED))
check("run record frame_declaration carries source, edition, seed, n",
      set(RR["record"]["frame_declaration"]) >= {"source", "edition", "seed", "n"})
check("run record arm_c table carries both axes per row",
      all({"axis_1", "axis_2", "cell"} <= set(r) for r in RR["record"]["arm_c"]))
check("run record acc_mech_revised is per condition and n_revised beside it",
      set(RR["record"]["acc_mech_revised"]) == set(rs.CONDITIONS) ==
      set(RR["record"]["n_revised"]))
RS_ = rs.run_record(S, C, cases.DEFECT_LOG)
check("run record is REFUSED on the shipped run, naming the frame and delta",
      RS_["emitted"] is False and RS_["record"] is None and
      "frame_declaration" in RS_["missing"] and "delta_open_blind" in RS_["missing"])
one_col = {"spec": cases.DEFECT_LOG["spec"]}
check("run record refuses a defect log with one column",
      rs.run_record(CAL, C, one_col)["emitted"] is False)
check("run record refuses a defect log that is not two columns",
      rs.run_record(CAL, C, [])["emitted"] is False)
RI = rs.run_record(INSUF, C, cases.DEFECT_LOG)
check("run record on INSUFFICIENT_REVISED is refused: acc_mech_revised is None",
      RI["emitted"] is False and any(m.startswith("acc_mech_revised") for m in RI["missing"]))
ids_spec = [e["id"] for e in cases.DEFECT_LOG["spec"]]
ids_impl = [e["id"] for e in cases.DEFECT_LOG["implementation"]]
check("defect log: spec and implementation columns are disjoint",
      not set(ids_spec) & set(ids_impl))
check("defect log: the four dispatch defects are in the spec column",
      {"D-C1", "D-C2", "D-C3", "D-C4"} <= set(ids_spec))
check("defect log: every entry carries id, defect, found_by, patched",
      all({"id", "defect", "found_by", "patched"} <= set(e)
          for col in cases.DEFECT_LOG.values() for e in col))

# ---------------------------------------------------------------------------
# 14. README framing at the top; render, screen, CLI, hygiene
# ---------------------------------------------------------------------------

framing = README.find("no calibration number")
check("README framing paragraph sits at the top, before SHAPE",
      0 < framing < README.find("## SHAPE") and framing < 1200
      and "four spec defects" in README[:framing + 600]
      and "not" in README[:framing + 900] and "failed attempt" in README[:framing + 900])
text = rs.run("2026-09-18")
check("render says revision 2 and prints the contamination block before Arm A",
      "revision 2" in text and text.index("CONTAMINATION") < text.index("ARM A"))
check("render states the missing frame and the refused run record",
      "NONE DECLARED" in text and "REFUSED   missing:" in text)
check("render prints Q_mech on revised rows only and never a pooled row",
      "revised rows ONLY" in text and "acc_mech " not in text)
check("render reports NO_SUBSTITUTION_EXISTS beside TERMINAL, not ranked",
      "not ranked against it (D-C2)" in text)
check("render prints key_holder, respondent and whether they differ",
      "key_holder" in text and "respondent" in text and "differ      NO" in text)
check("render prints every [CHOICE n]", all("[CHOICE %d]" % k in text for k in rs.CHOICES))
check("render screens clean through no_severity, no exemption",
      no_severity.hits(text) == [], "%s" % no_severity.hits(text)[:3])
check("the screen fires on a planted word", no_severity.hits(text + "\nthis cell is wrong\n") != [])
p = subprocess.run([sys.executable, os.path.join(HERE, "revision_survival.py"), "--selftest"],
                   capture_output=True)
check("revision_survival --selftest is refused with exit 2", p.returncode == 2)
p = subprocess.run([sys.executable, os.path.join(HERE, "revision_survival.py"),
                    "--today=2026-09-18"], capture_output=True)
check("CLI render exits 0 and matches run()", p.returncode == 0 and p.stdout.decode() == text)
p = subprocess.run([sys.executable, os.path.join(HERE, "revision_survival.py"), "--choices"],
                   capture_output=True)
check("--choices prints ten choices", p.stdout.decode().count("[CHOICE") == 10)
for fn in SCOPED:
    src = open(os.path.join(HERE, fn), "rb").read()
    check("%s is ASCII" % fn, all(b < 128 for b in src))
    ast.parse(src.decode("ascii"), feature_version=(3, 9))
    check("%s parses under 3.9" % fn, True)
tree = ast.parse(open(os.path.join(HERE, "cases.py")).read())
names = {n.id.lower() for n in ast.walk(tree) if isinstance(n, ast.Name)}
check("cases.py binds no name for an expected result",
      not any(n.startswith("expected") or n.startswith("want") for n in names))

# ---------------------------------------------------------------------------

failed = [(n, d_) for n, ok, d_ in CHECKS if not ok]
for n, ok, d_ in CHECKS:
    print("%s  %s%s" % ("ok  " if ok else "FAIL", n, ("  -- " + d_) if (d_ and not ok) else ""))
print()
print("repo-wide bare float comparisons (RS_022, recorded): %d files, %d compares"
      % REPO_WIDE)
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
