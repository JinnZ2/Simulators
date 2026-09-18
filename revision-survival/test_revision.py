# SPDX-License-Identifier: CC0-1.0
# test_revision.py -- checks for revision_survival. Stdlib only, no pytest,
# no network. Run: python3 test_revision.py
#
# Expected verdicts and counts live HERE and not in cases.py, so no record
# can agree with the instrument by construction. Constructed worlds are
# built in this file, labelled, and authored under a name that is not the
# key's.

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
import revision_survival as rs      # noqa: E402
import no_severity                  # noqa: E402

CHECKS = []


def check(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


def refuses(fn, *a, **k):
    try:
        fn(*a, **k)
    except rs.RefusedInput:
        return True
    return False


ORDER = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()

# ---------------------------------------------------------------------------
# 1. vocabularies are the order's, read out of WORK_ORDER.md at test time
# ---------------------------------------------------------------------------

m = re.search("verdict \u2208 \{([^}]*)\}", ORDER)
order_verdicts = tuple(x.strip() for x in m.group(1).replace("\n", " ").split(","))
check("VERDICTS match the order", order_verdicts == rs.VERDICTS,
      "%s" % (order_verdicts,))
m = re.search("mechanism \u2208 \{([^}]*)\}", ORDER)
order_mechs = tuple(" ".join(x.split()) for x in m.group(1).split(","))
check("MECHANISMS match the order", order_mechs == rs.MECHANISMS,
      "%s" % (order_mechs,))
sec = ORDER.split("RETURN ENUM")[1].split("KNOWN DEFECTS")[0]
order_returns = tuple(re.findall(r"^  ([A-Z_]+)\s{2,}", sec, re.M))
check("RETURNS match the order", order_returns == rs.RETURNS,
      "%s" % (order_returns,))
check("leak threshold 0.15 is the order's",
      "\u0394 < 0.15" in ORDER and rs.LEAK_THRESHOLD == 0.15)
check("overconfidence threshold 0.2 is the order's",
      "> 0.2" in sec and rs.OVERCONF_THRESHOLD == 0.2)
check("survival cut 0.8 is the order's",
      "< 0.8 survival" in ORDER and rs.SURVIVAL_CUT == 0.8)
check("Y = 2005 is the order's", "Y = 2005" in ORDER and rs.Y == 2005)
check("N >= 40 is the order's", "N\u226540" in ORDER and rs.N_FLOOR == 40)
check("SURVIVED floor 40% is the order's",
      "\u226540% SURVIVED" in ORDER and rs.SURVIVED_FLOOR == 0.40)
seedsec = ORDER.split("seed claims")[1].split("\n\n")[0]
order_seeds = [ln for ln in seedsec.split("\n")
               if ln.startswith("    ") and not ln.strip().endswith(":")]
delivered = [c for c in cases.CLAIMS if c["status"] == "DELIVERED"]
check("twelve seeds in the order, twelve DELIVERED records",
      len(order_seeds) == 12 == len(delivered), "%d / %d"
      % (len(order_seeds), len(delivered)))
check("consequence classes are the order's three",
      all(c in ORDER for c in rs.CONSEQUENCE) and len(rs.CONSEQUENCE) == 3)

# ---------------------------------------------------------------------------
# 2. intake refuses, by field
# ---------------------------------------------------------------------------

good = copy.deepcopy(cases.CLAIMS[0])
check("a well-formed claim reads", rs.read_claim(good)["id"] == "seed-01")
for k in ("id", "statement", "field_nouns", "established_as_of_Y",
          "established_basis", "outcome", "status", "author"):
    bad = copy.deepcopy(good); del bad[k]
    check("claim refused without %s" % k, refuses(rs.read_claim, bad))
for k in ("label", "mechanism", "basis", "verified", "source"):
    bad = copy.deepcopy(good); del bad["outcome"][k]
    check("claim refused without outcome.%s" % k, refuses(rs.read_claim, bad))
bad = copy.deepcopy(good); bad["outcome"]["label"] = "REFUTED"
check("claim refused on a label outside the vocabulary",
      refuses(rs.read_claim, bad))
bad = copy.deepcopy(good); bad["outcome"]["mechanism"] = "confounding"
check("claim refused on a mechanism outside the vocabulary "
      "(confounding is what seed-04 needed and the vocabulary lacks)",
      refuses(rs.read_claim, bad))
bad = copy.deepcopy(good); bad["outcome"]["verified"] = "yes"
check("claim refused on a non-bool verified", refuses(rs.read_claim, bad))
bad = copy.deepcopy(good); bad["established_as_of_Y"] = "PROBABLY"
check("claim refused on an admission reading outside YES/NO/UNCERTAIN",
      refuses(rs.read_claim, bad))

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
bad = copy.deepcopy(r0); bad["condition"] = "HALF"
check("response refused on a condition outside OPEN/BLIND",
      refuses(rs.read_response, bad))

# ---------------------------------------------------------------------------
# 3. admission on the shipped corpus
# ---------------------------------------------------------------------------

claims = [rs.read_claim(c) for c in cases.CLAIMS]
adm, exc = rs.admit(claims)
exc_d = dict(exc)
check("six seeds admitted",
      sorted(c["id"] for c in adm) == ["seed-01", "seed-05", "seed-06",
                                       "seed-07", "seed-08", "seed-09"],
      "%s" % sorted(c["id"] for c in adm))
check("five seeds read NO on established-as-of-2005",
      sorted(k for k, v in exc_d.items() if v.endswith("=NO")) ==
      ["seed-03", "seed-04", "seed-10", "seed-11", "seed-12"])
check("one seed reads UNCERTAIN", [k for k, v in exc_d.items()
                                    if v.endswith("=UNCERTAIN")] == ["seed-02"])
check("every CANDIDATE is excluded, none admitted",
      all(exc_d[c["id"]] == "status=CANDIDATE" for c in claims
          if c["status"] == "CANDIDATE") and
      not any(c["status"] == "CANDIDATE" for c in adm))
check("every excluded record carries a reason",
      all(why for _, why in exc))
check("every seed outcome is carried, none verified",
      all(c["outcome"]["verified"] is False for c in delivered))
check("every seed carries a source for its dating (D4)",
      all(c["established_basis"] for c in delivered))
check("SURVIVED share of the admitted corpus is 0 of 6",
      sum(1 for c in adm if c["outcome"]["label"] == "SURVIVED") == 0)
# D1's mirror: admitting the scorer's own SURVIVED candidates sets the rate
as_if = copy.deepcopy(claims)
for c in as_if:
    if c["status"] == "CANDIDATE":
        c["status"] = "DELIVERED"
adm2, _ = rs.admit(as_if)
share2 = sum(1 for c in adm2 if c["outcome"]["label"] == "SURVIVED") / len(adm2)
check("admitting the scorer's candidates would clear D1 by itself",
      share2 >= rs.SURVIVED_FLOOR, "%.2f of %d" % (share2, len(adm2)))

# ---------------------------------------------------------------------------
# 4. blind(): the mechanical half, and its stated limit
# ---------------------------------------------------------------------------

b = rs.blind(claims[0])
check("blind replaces every declared noun",
      "wolf" not in b["text"].lower() and "alpha" not in b["text"].lower()
      and "pack" not in b["text"].lower(), b["text"])
check("blind reports what moved per noun",
      [n for n, _, n_ in b["nouns_moved"] if n_] and b["paraphrased"] is False)
c_year = copy.deepcopy(claims[0])
c_year["statement"] = "Established in 1970 and taught in 2005: " + c_year["statement"]
by = rs.blind(c_year)
check("blind strips four-digit years", by["years_removed"] == 2
      and "1970" not in by["text"] and "2005" not in by["text"])
c_syn = copy.deepcopy(claims[0])
c_syn["statement"] = "Canid packs are led by a dominant pair."
bs = rs.blind(c_syn)
check("LIMIT: an undeclared synonym is not replaced (word list)",
      "Canid" in bs["text"] and "dominant" in bs["text"])
check("blind output says it is MECHANICAL_ONLY",
      b["blinding"] == "MECHANICAL_ONLY")

# ---------------------------------------------------------------------------
# 5. chance, above_chance, accuracy, delta
# ---------------------------------------------------------------------------

ch, u, maj = rs.chance(5, ["A", "A", "A", "B"])
check("[CHOICE 1] chance is the larger of uniform and majority",
      ch == 0.75 and u == 0.2 and maj == 0.75)
ch2, u2, maj2 = rs.chance(5, ["A", "B", "C", "D", "E"])
check("[CHOICE 1] uniform wins on a flat key", ch2 == 0.2 and maj2 == 0.2)
check("chance is None on an empty key", rs.chance(5, [])[0] is None)
check("above_chance is None on no rows", rs.above_chance(1.0, 0.2, 0) is None)
check("[CHOICE 2] one perfect row does not clear chance",
      rs.above_chance(1.0, 0.5, 1) is False)
check("[CHOICE 2] 0.8 on 50 rows clears chance 0.4",
      rs.above_chance(0.8, 0.4, 50) is True)
check("accuracy is None on nothing, never 0", rs.accuracy([]) is None)
check("accuracy counts", rs.accuracy([(1, 1), (1, 2), (3, 3), (4, 4)]) == 0.75)
check("delta: quarter", rs.delta(0.75, 0.5) == 0.25)
check("delta: None when BLIND absent", rs.delta(0.8, None) is None)
check("delta: None when OPEN absent", rs.delta(None, 0.8) is None)
check("delta: sign kept", abs(rs.delta(0.4, 0.55) + 0.15) < 1e-9)

# ---------------------------------------------------------------------------
# 6. constructed worlds -- every return reachable, under a second author
# ---------------------------------------------------------------------------

RESPONDER = "constructed responder (not the key's author)"
NON_NONE = [m for m in rs.MECHANISMS if m != "NONE_GIVEN"]


def world(n, survived_share):
    out = []
    n_surv = int(round(n * survived_share))
    for i in range(n):
        surv = i < n_surv
        label = "SURVIVED" if surv else rs.VERDICTS[1 + (i % 4)]
        mech = "NONE_GIVEN" if surv else NON_NONE[i % len(NON_NONE)]
        out.append(rs.read_claim({
            "id": "w-%02d" % i, "statement": "constructed claim %d" % i,
            "field_nouns": [], "established_as_of_Y": "YES",
            "established_basis": "constructed", "status": "DELIVERED",
            "author": "constructor (key)",
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


W = world(50, 0.4)
check("constructed world clears N and D1 floors",
      len(W) == 50 and sum(1 for c in W if c["outcome"]["label"] == "SURVIVED") == 20)


def score(open_l, open_m, blind_l, blind_m, conf=0.6, author=RESPONDER,
          blind=True):
    rs_ = respond(W, "OPEN", open_l, open_m, conf, author)
    if blind:
        rs_ += respond(W, "BLIND", blind_l, blind_m, conf, author)
    return rs.score_arm_a(W, rs_)


CAL = score(0.8, 0.8, 0.76, 0.76)
LEAK = score(0.9, 0.9, 0.4, 0.4)
LABEL = score(0.9, 0.4, 0.9, 0.4)
UNCAL = score(0.4, 0.4, 0.4, 0.4)
OVER = score(0.7, 0.8, 0.66, 0.76, conf=0.99)
NODELTA = score(0.8, 0.8, None, None, blind=False)
SAME = score(0.8, 0.8, 0.76, 0.76, author="constructor (key)")

check("CALIBRATED reachable", CAL["return"] == "CALIBRATED" and not CAL["void"],
      "%s %s" % (CAL["return"], CAL["void"]))
check("LEAK_DOMINATED reachable", LEAK["return"] == "LEAK_DOMINATED",
      "delta %s" % LEAK["delta"])
check("LABEL_ONLY reachable", LABEL["return"] == "LABEL_ONLY",
      "%s" % LABEL["return"])
check("UNCALIBRATED reachable", UNCAL["return"] == "UNCALIBRATED",
      "%s" % UNCAL["return"])
check("OVERCONFIDENT rides as a co-flag on both conditions",
      OVER["return"] == "CALIBRATED" and
      OVER["co_flags"] == ["OVERCONFIDENT(OPEN)", "OVERCONFIDENT(BLIND)"],
      "%s" % OVER["co_flags"])
check("no co-flag at honest confidence", CAL["co_flags"] == [])
check("VOID with no BLIND arm, naming the reason",
      NODELTA["return"] == "VOID" and NODELTA["delta"] is None and
      any(v.startswith("VOID_NO_DELTA") for v in NODELTA["void"]))
check("VOID when key and responses share an author",
      SAME["return"] == "VOID" and
      any(v.startswith("VOID_SAME_AUTHOR") for v in SAME["void"]))
check("a void result carries no primary member",
      NODELTA["return"] not in rs.RETURNS and SAME["return"] not in rs.RETURNS)
check("every RETURN member is produced by some world",
      {CAL["return"], LEAK["return"], LABEL["return"], UNCAL["return"]}
      | set(f.split("(")[0] for f in OVER["co_flags"]) == set(rs.RETURNS))
check("delta gates on the larger of the two [CHOICE 3]",
      LEAK["delta"] == max(LEAK["delta_label"], LEAK["delta_mech"]))
check("a leak of 0.5 in mechanism alone voids",
      score(0.8, 0.9, 0.8, 0.4)["return"] == "LEAK_DOMINATED")
check("D1 does not fire on the constructed world", 
      not any(d.startswith("D1") for d in CAL["defects"]))
check("BELOW_N_FLOOR does not fire at n = 50",
      not any(d.startswith("BELOW_N") for d in CAL["defects"]))
check("D4 fires on a carried key regardless of the rest",
      any(d.startswith("D4") for d in CAL["defects"]))

# Q_mech on SURVIVED rows is a function of Q_label
ALLS = world(30, 1.0)
r_alls = rs.score_arm_a(ALLS, respond(ALLS, "OPEN", 0.7, 0.7, 0.5)
                        + respond(ALLS, "BLIND", 0.7, 0.7, 0.5))
check("on an all-SURVIVED key the revised-row Q_mech is None (no rows)",
      r_alls["per_condition"]["OPEN"]["acc_mech_revised"] is None and
      r_alls["per_condition"]["OPEN"]["n_revised"] == 0)
check("on the 40% world the revised-row denominator is 30 of 50",
      CAL["per_condition"]["OPEN"]["n_revised"] == 30)
check("chance for mechanism on the 40% world is the NONE_GIVEN share, 0.4",
      abs(CAL["per_condition"]["OPEN"]["chance_mech"] - 0.4) < 1e-9)

# ---------------------------------------------------------------------------
# 7. the shipped run
# ---------------------------------------------------------------------------

responses = [rs.read_response(r) for r in cases.RESPONSES_OPEN]
S = rs.score_arm_a(claims, responses)
check("shipped Arm A is VOID", S["return"] == "VOID")
check("shipped Arm A voids on both reasons",
      sorted(v.split(":")[0] for v in S["void"]) ==
      ["VOID_NO_DELTA", "VOID_SAME_AUTHOR"])
check("shipped Arm A states D1, D4 and the N floor",
      {d.split(":")[0] for d in S["defects"]} == {"D1", "D4", "BELOW_N_FLOOR"})
check("shipped OPEN agreement is 6 of 6, by construction",
      S["per_condition"]["OPEN"]["acc_label"] == 1.0 and
      S["per_condition"]["OPEN"]["n"] == 6)
check("responses on excluded seeds are not scored",
      S["per_condition"]["OPEN"]["n"] == 6 and len(responses) == 12)
check("no response gives NONE_GIVEN", S["per_condition"]["OPEN"]["none_given"] == 0)

# ---------------------------------------------------------------------------
# 8. Arm B
# ---------------------------------------------------------------------------

block = rs.read_block(copy.deepcopy(cases.ARM_B_BLOCK))
rec = rs.publish_record(block)
check("shipped record hash equals the recomputed seal",
      rec["sha256"] == cases.ARM_B_RECORD["sha256"], rec["sha256"])
check("review dates are T+24mo and T+60mo [CHOICE 6]",
      rec["review"] == ["2028-09-17", "2031-09-17"] ==
      cases.ARM_B_RECORD["review"])
check("record carries k = 13", rec["k"] == 13 == len(block["claims"]))
check("record carries nothing from the block but hash, date, domain, k, review",
      set(rec) == {"sha256", "date", "domain", "review", "k"})
check("seal is deterministic", rs.seal(block) == rs.seal(copy.deepcopy(block)))
tampered = copy.deepcopy(block)
tampered["claims"][6]["p_survive"] = 0.95
check("one edited p_survive fails verify", rs.verify(tampered, rec) is False)
check("scoring a tampered block is VOID_HASH",
      rs.score_arm_b(tampered, rec, {}, "2031-09-17")["status"] == "VOID_HASH")
nd = rs.score_arm_b(block, rec, {}, "2026-09-17")
check("scoring before the first review date is NOT_DUE, naming it",
      nd["status"] == "NOT_DUE" and nd["due"] == "2028-09-17")
outcomes = {c["id"]: {"label": c["verdict"], "mechanism": c["mechanism"]}
            for c in block["claims"][:10]}
sc = rs.score_arm_b(block, rec, outcomes, "2028-09-17")
check("scoring on the review date with ten outcomes: SCORED, three unresolved",
      sc["status"] == "SCORED" and sc["n"] == 10 and
      sc["unresolved"] == ["B-11", "B-12", "B-13"])
check("a block with model UNKNOWN is refused",
      refuses(rs.read_block, dict(block, model="UNKNOWN")))
check("a block with model WITHHELD and a reason reads",
      block["model"].startswith("WITHHELD:"))
dup = copy.deepcopy(block); dup["claims"].append(dict(dup["claims"][0]))
check("a duplicate claim id is refused", refuses(rs.read_block, dup))
nop = copy.deepcopy(block); del nop["claims"][0]["p_survive"]
check("a claim without p_survive is refused [CHOICE 5]",
      refuses(rs.read_block, nop))
check("every Arm B claim carries a mechanism-if-revised and a flag",
      all(c["mechanism"] != "NONE_GIVEN" and c["flag_evidence"]
          for c in block["claims"]))
check("Arm B rates at least one claim below and one at or above the cut",
      any(c["p_survive"] < 0.8 for c in block["claims"]) and
      any(c["p_survive"] >= 0.8 for c in block["claims"]))

# ---------------------------------------------------------------------------
# 9. Arm C
# ---------------------------------------------------------------------------

C = rs.score_arm_c(cases.BRC_ROWS, block)
check("FINDING: two TERMINAL cells rest on a claim rated below 0.8",
      C["finding"] == 2 and C["terminal_low"] == ["C5", "C9"],
      "%s" % C["terminal_low"])
check("C9 rests on B-07 at 0.5", [r for r in C["per_row"] if r["id"] == "C9"][0]["low"] == ["B-07"])
check("three rows carry no substitution decision", C["not_on_record"] == ["C3", "C6", "C8"])
check("B-12 is rated and under no row", C["claims_under_no_row"] == ["B-12"])
check("nine rows, the drop's register", C["n_rows"] == 9)
check("the finding counts only the low bucket",
      C["finding"] == len(C["terminal_low"]) and
      not set(C["terminal_low"]) & set(C["terminal_unrated"]) and
      not set(C["terminal_low"]) & set(C["terminal_held"]))
rows2 = copy.deepcopy(cases.BRC_ROWS)
rows2.append({"id": "X1", "cycle": "constructed", "pathway": "NONE",
              "stock_or_flow": "FLOW", "consequence_class": "TERMINAL",
              "basis": "constructed", "rests_on": []})
rows2.append({"id": "X2", "cycle": "constructed", "pathway": "NONE",
              "stock_or_flow": "FLOW", "consequence_class": "TERMINAL",
              "basis": "constructed", "rests_on": ["B-04"]})
rows2.append({"id": "X3", "cycle": "constructed", "pathway": "PARTIAL",
              "stock_or_flow": "FLOW", "consequence_class": "UNDECLARED",
              "basis": "", "rests_on": []})
C2 = rs.score_arm_c(rows2, block)
check("TERMINAL_UNRATED reachable and kept apart",
      C2["terminal_unrated"] == ["X1"] and C2["finding"] == 2)
check("TERMINAL_RATED_HELD reachable and kept apart",
      C2["terminal_held"] == ["X2"] and C2["finding"] == 2)
check("UNDECLARED reachable and kept apart", C2["undeclared"] == ["X3"])
check("a rests_on id absent from the block is refused, not skipped",
      refuses(rs.score_arm_c, [dict(cases.BRC_ROWS[0], rests_on=["B-99"])], block))
check("a class with no basis is refused",
      refuses(rs.read_brc_row, dict(cases.BRC_ROWS[0], basis="")))
check("an UNDECLARED class needs no basis",
      rs.read_brc_row(dict(cases.BRC_ROWS[0], consequence_class="UNDECLARED",
                           basis=""))["consequence_class"] == "UNDECLARED")
check("a class outside the vocabulary is refused",
      refuses(rs.read_brc_row, dict(cases.BRC_ROWS[0], consequence_class="FATAL")))
check("every row's rests_on resolves in the block",
      all(cid in {c["id"] for c in block["claims"]}
          for r in cases.BRC_ROWS for cid in r["rests_on"]))
check("every under_brc_rows on the block resolves to a row",
      all(rid in {r["id"] for r in cases.BRC_ROWS}
          for c in block["claims"] for rid in c["under_brc_rows"]))
check("block and rows agree on who rests on whom",
      all(set(r["rests_on"]) ==
          {c["id"] for c in block["claims"] if r["id"] in c["under_brc_rows"]}
          for r in cases.BRC_ROWS))

# ---------------------------------------------------------------------------
# 10. render, screen, CLI, hygiene
# ---------------------------------------------------------------------------

text = rs.run("2026-09-17")
check("render prints the contamination block before Arm A",
      text.index("CONTAMINATION") < text.index("ARM A"))
check("render prints every [CHOICE n]",
      all("[CHOICE %d]" % k in text for k in rs.CHOICES))
check("render prints the finding", "FINDING  TERMINAL cells" in text)
check("render screens clean through no_severity, no exemption",
      no_severity.hits(text) == [], "%s" % no_severity.hits(text)[:3])
check("the screen fires on a planted word",
      no_severity.hits(text + "\nthis cell is wrong\n") != [])
p = subprocess.run([sys.executable, os.path.join(HERE, "revision_survival.py"),
                    "--selftest"], capture_output=True)
check("--selftest is refused with exit 2", p.returncode == 2)
p = subprocess.run([sys.executable, os.path.join(HERE, "revision_survival.py"),
                    "--today=2026-09-17"], capture_output=True)
check("CLI render exits 0 and matches run()", p.returncode == 0 and
      p.stdout.decode() == text)
for fn in ("revision_survival.py", "cases.py", "test_revision.py"):
    src = open(os.path.join(HERE, fn), "rb").read()
    check("%s is ASCII" % fn, all(b < 128 for b in src))
    ast.parse(src.decode("ascii"), feature_version=(3, 9))
    check("%s parses under 3.9" % fn, True)

# cases.py carries no expected verdict or count for the instrument
tree = ast.parse(open(os.path.join(HERE, "cases.py")).read())
names = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Name):
        names.add(node.id.lower())
    elif isinstance(node, ast.Constant) and isinstance(node.value, str):
        pass
check("cases.py binds no name for an expected result",
      not any(n.startswith("expected") or n.startswith("want") for n in names))

# ---------------------------------------------------------------------------

failed = [(n, d) for n, ok, d in CHECKS if not ok]
for n, ok, d in CHECKS:
    print("%s  %s%s" % ("ok  " if ok else "FAIL", n, ("  -- " + d) if (d and not ok) else ""))
print()
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
