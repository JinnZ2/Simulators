"""Build candidate amended keys (NOT adopted) and score the filed Claude-v2-A reading under each.

Why: to show how much each open choice moves the numbers, not to pick one.  Caveat that applies to every number
this script prints: there is one v2 reading, it is the reading the amendment was written after, and it is from
one model family.  A score under a candidate key cannot show that the candidate is right.

Needs the scorer that knows rules N1 / C1 (the patch's score_v2.py).  Set SCORER_DIR to the folder holding it
(with score.py beside it) and PATCHED_KEY to the patch's key_v2_a1.json.  The repo's own scoring/ is not touched.

  SCORER_DIR=... PATCHED_KEY=... python3 build_candidates.py
"""
import copy, hashlib, json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, "..", ".."))                       # blind-reader-void12/
SCORER_DIR = os.environ.get("SCORER_DIR")
PATCHED_KEY = os.environ.get("PATCHED_KEY")
if not SCORER_DIR or not PATCHED_KEY:
    sys.exit("set SCORER_DIR and PATCHED_KEY (see the docstring)")
sys.path.insert(0, SCORER_DIR)
import score_v2 as S2                                                            # noqa: E402
if not hasattr(S2, "rules_of"):
    sys.exit("this scorer has no N1/C1 support; point SCORER_DIR at the patched score_v2.py")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
load = lambda p: json.load(open(p, encoding="utf-8"))
KEY_V2 = load(os.path.join(BASE, "scoring", "key_v2.json"))
KEY_P = load(PATCHED_KEY)
READING = os.path.join(BASE, "readings", "2026-11-18_claude-v2-A", "response.json")
RESP = load(READING)
EVID = load(os.path.join(HERE, "check_rules_output.json"))
PROPOSAL_KEYS = EVID["A"]["proposal_keys"]

def tier(same_pred, la, lb, left_label, right_label):
    if same_pred:
        if la is None or lb is None: return None
        return "MAPS" if set(la) == set(lb) else "PARTIAL"
    return "HOMONYM" if left_label == right_label else "NONE"

def retier(key):
    """Recompute key_tier_specific / key_tier_carried of every pair from the term lists (the first reader's tier rule)."""
    for p in key["pairs"]:
        a, b = key["terms"][p["left"]], key["terms"][p["right"]]
        for m in ("specific", "carried"):
            p["key_tier_" + m] = tier(p["same_predicate"], a["slots_" + m], b["slots_" + m], a["label"], b["label"])

# builder self-check: retiering a known key must reproduce its own stored tiers
for name, k in (("key_v2", KEY_V2), ("patched key_v2_a1", KEY_P)):
    c = copy.deepcopy(k); retier(c)
    bad = [(p["pair_label"], m) for p, q in zip(k["pairs"], c["pairs"]) for m in ("specific", "carried") if p["key_tier_" + m] != q["key_tier_" + m]]
    print("builder self-check, %-18s: %s" % (name, "reproduces stored pair tiers" if not bad else "MISMATCH %s" % bad))
    assert not bad

def candidate(name, why, overrides):
    k = copy.deepcopy(KEY_P)
    for tid_i, lst in overrides.items(): k["terms"][tid_i]["slots_specific"] = lst
    retier(k)
    k["meta"]["v"] = "2-a1-candidate-" + name
    k["meta"]["NOT_ADOPTED"] = "options evidence only; " + why
    k["meta"].pop("amendment_sha256", None)
    k["meta"]["based_on_patched_key_sha256"] = sha(PATCHED_KEY)
    return k

CANDS = {
 "P":          ("the patch as received: S3-out, T14 keeps [sigma, basis], nested records not opened", {}),
 "P_T14lit":   ("P, but T14 = [] (S2 read literally: sigma and basis are present on every Reading)", {"T14": []}),
 "P_open":     ("P, but T01 = the 14 fields of the proposal record (S1b applied to a nested record built only on UNDECIDED)", {"T01": list(PROPOSAL_KEYS)}),
 "P_literal":  ("P with both of the above", {"T14": [], "T01": list(PROPOSAL_KEYS)}),
 "P_S3in":     ("P, but S3-in: covers_effect added to T05, typed and untyped added to T12", {"T05": KEY_P["terms"]["T05"]["slots_specific"] + ["covers_effect"], "T12": ["triggers", "typed", "untyped"]}),
}
# check: candidate P (no overrides) must equal the patched key exactly, apart from the meta marks and retiered pairs
kP = candidate("check", "builder check", {})
assert all(kP["terms"][i] == KEY_P["terms"][i] for i in KEY_P["terms"]), "candidate P differs from the patched key"
assert all({k2: v for k2, v in p.items()} == {k2: v for k2, v in q.items()} for p, q in zip(KEY_P["pairs"], kP["pairs"])), "pair tiers differ"
print("candidate P reproduces the patched key's terms and pair tiers exactly")

CAND_OUT = os.environ.get("CAND_OUT", "/tmp/key_v2_a1_candidates")   # candidate keys are NOT kept in the repo: they are not keys
os.makedirs(CAND_OUT, exist_ok=True)
rows = []
def run(label, key, why):
    o = S2.score(RESP, key)
    sp, ca = o["meanings"]["specific"], o["meanings"]["carried"]
    rel = sp.get("relations", {})
    t = {s["id"]: s for s in sp["slots"]}
    rows.append((label, why, o, key))
    return o

run("v2", KEY_V2, "key v2 as filed (no N1, no C1)")
for n, (why, ov) in CANDS.items():
    k = candidate(n, why, ov)
    p = os.path.join(CAND_OUT, "key_v2_a1_candidate_%s.json" % n)
    json.dump(k, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(p, "a").write("\n")
    run(n, k, why)

out = []
out.append("Claude-v2-A (status UNCERTAIN, same family as the first reader) scored under each candidate key. Specific meaning only: the candidates differ only there.")
out.append("grouping and slots_carried are identical under every key and are not repeated: ARI %s; carried %d of %d determined pairs agree; %d of %d carried slot sets equal." % (
    rows[0][2]["ari"], rows[0][2]["meanings"]["carried"]["tier_agree"], rows[0][2]["meanings"]["carried"]["n_determined"], rows[0][2]["meanings"]["carried"]["slots_equal"], rows[0][2]["meanings"]["carried"]["slots_determined"]))
out.append("")
hdr = "%-10s %-17s %-17s %-12s %-12s  %s" % ("key", "pairs agree", "sets equal", "nothing-grp", "label-only", "slot set vs key, the four terms the options move (T01 T05 T12 T14)")
out.append(hdr); out.append("-" * len(hdr))
for label, why, o, key in rows:
    sp = o["meanings"]["specific"]
    t = {s["id"]: s for s in sp["slots"]}
    mv = "  ".join("%s:%s" % (i, ("n/d" if t[i]["status"] == "n/d" else t[i]["status"] + ("(" + t[i]["relation"].replace("reader-", "") + ")" if "relation" in t[i] and t[i]["status"] == "differ" else ""))) for i in ("T01", "T05", "T12", "T14"))
    out.append("%-10s %-17s %-17s %-12s %-12s  %s" % (label, "%d of %d" % (sp["tier_agree"], sp["n_determined"]), "%d of %d" % (sp["slots_equal"], sp["slots_determined"]),
               "%d of %d" % (sp["baselines"]["singletons"], sp["n_determined"]), "%d of %d" % (sp["baselines"]["label_only"], sp["n_determined"]), mv))
out.append("")
out.append("what each candidate is:")
for label, why, o, key in rows: out.append("  %-10s %s" % (label, why))
out.append("")
out.append("per-pair tiers, specific meaning (reader / key):")
names = [p["pair_label"] for p in KEY_V2["pairs"]]
out.append("  %-48s " % "pair" + " ".join("%-13s" % r[0] for r in rows))
for i, nm in enumerate(names):
    cells = []
    for label, why, o, key in rows:
        r = o["meanings"]["specific"]["pairs"][i]
        cells.append("%-13s" % ("%s/%s" % (str(r["reader"] if "reader" in r else r.get("reader_tier")), str(r["key"] if "key" in r else r.get("key_tier")))))
    out.append("  %-48s " % nm + " ".join(cells))
out.append("")
out.append("scorer sha256 %s ; patched key sha256 %s ; reading sha256 %s" % (sha(os.path.join(SCORER_DIR, "score_v2.py"))[:16], sha(PATCHED_KEY)[:16], sha(READING)[:16]))
txt = "\n".join(out)
print(txt)
open(os.path.join(HERE, "candidate_scores.txt"), "w").write(txt + "\n")
json.dump({l: o for l, w, o, k in rows}, open(os.path.join(HERE, "candidate_scores.json"), "w"), indent=1, sort_keys=True)
