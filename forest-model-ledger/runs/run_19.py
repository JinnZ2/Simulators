"""run_19: support_match on blind cases (chat-side follow-up to PR #258, item 2). stdlib only.

Blind coder: a separate agent given only the excerpt lines (cases/support_blind_excerpts.txt),
three neutral attribution statements and the claim-record schema; no repository, no tool code,
no expected verdicts. Its output is cases/support_blind.json, landed verbatim (sha256 below).

(a) task_a: the coder's own claim records for cases a, b, c1, read by support_match against the
    pinned texts, beside run_16's records (written by the session that built the tool).
(b) task_b: 40 short credit exchanges the coder wrote and labelled (CREDITS_OTHER / OWN /
    NEITHER; 20 "natural", 20 with no second-person words). support_match is asked
    "does this line, spoken by its speaker, give the item away to someone else?" (CONTRADICTS).
    recall and precision against the coder's CREDITS_OTHER label, per group.

run_16's results stay labelled build-confirming, author-contaminated.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from ledger.toolkit import support_match as S
from ledger.toolkit import attribution_directionality as ad

BLIND = os.path.join(HERE, "ledger", "toolkit", "cases", "support_blind.json")
SHA = "c442919999a303fa9fe8f58275411cda131829348892aabc7dcea3880dc31d50"
IDS = dict(A1="a_kimi_provenance_map", A2="b_gemini_hex_token", A3="c1_chatgpt_denial_frame")


def load():
    raw = open(BLIND, "rb").read()
    if hashlib.sha256(raw).hexdigest() != SHA:
        raise SystemExit("refused: support_blind.json differs from the landed copy")
    return json.loads(raw)


def task_a(blind):
    texts = S._texts()
    recs = {r["id"]: r for r in ad.load_cases(ad.CASES_FIRST)}
    mine = {c["id"]: c for c in S.load_claims()}
    rows = []
    for b in blind["task_a"]:
        rid = IDS[b["id"]]
        rec = recs[rid]
        claim = dict(id=rid, claim=b["claim"], credited_to=b["credited_to"], item_terms=b["item_terms"],
                     support=b["support"], support_basis=b["support_basis"])
        try:
            S.validate(claim, rec, texts)
            valid = "valid"
        except S.ClaimError as e:
            valid = f"refused by validate: {e}"
        rows.append(dict(id=rid, blind=S.verdict(rec, claim, texts), mine=S.verdict(rec, mine[rid], texts), valid=valid,
                         blind_support=[x["line"] for x in b["support"]], mine_support=[x["line"] for x in mine[rid]["support"]],
                         blind_terms=b["item_terms"], mine_terms=mine[rid]["item_terms"], note=b.get("note", "")))
    return rows


def task_b(blind):
    rec = dict(id="blind", first_attribution="OTHER_SYSTEM", fits_question="IN_SCOPE")
    out = {}
    for it in blind["task_b"]:
        w = {"b.txt": ([f"{it['speaker']}:", it["line"]], None)}
        c = dict(credited_to=it["credited_to_in_claim"], item_terms=[it["item"]], support=[dict(file="b.txt", line="2")])
        v = S.verdict(rec, c, w)
        g = out.setdefault(it["group"], dict(tp=0, fp=0, fn=0, tn=0, missed=[], false=[], verdicts={}))
        hit, pos = v == "CONTRADICTS", it["label"] == "CREDITS_OTHER"
        g["verdicts"][v] = g["verdicts"].get(v, 0) + 1
        if hit and pos:
            g["tp"] += 1
        elif hit:
            g["fp"] += 1; g["false"].append(it["line"])
        elif pos:
            g["fn"] += 1; g["missed"].append(it["line"])
        else:
            g["tn"] += 1
    for g in out.values():
        g["recall"] = g["tp"] / (g["tp"] + g["fn"]) if g["tp"] + g["fn"] else None
        g["precision"] = g["tp"] / (g["tp"] + g["fp"]) if g["tp"] + g["fp"] else None
    return out


def fmt(x):
    return "--" if x is None else f"{x:.3f}"


if __name__ == "__main__":
    b = load()
    print(f"blind coder: {b['coder']}   file sha256 {SHA[:16]}")
    print("\n(a) claim records, blind coder vs this session (run_16), same tool, same pinned texts")
    for r in task_a(b):
        print(f"  {r['id']:26s} blind {r['blind']:18s} run_16 {r['mine']:18s} [{r['valid']}]")
        print(f"  {'':26s} support blind {r['blind_support']} terms {r['blind_terms']}; run_16 {r['mine_support']} terms {r['mine_terms']}")
    print("\n(b) 40 labelled credit lines; detector = CONTRADICTS; positive = coder label CREDITS_OTHER")
    res = task_b(b)
    for grp in ("natural", "no_second_person"):
        g = res[grp]
        print(f"  {grp:18s} tp {g['tp']} fp {g['fp']} fn {g['fn']} tn {g['tn']}   recall {fmt(g['recall'])}  precision {fmt(g['precision'])}   verdicts {g['verdicts']}")
        for l in g["missed"]:
            print(f"      missed: {l}")
        for l in g["false"]:
            print(f"      false : {l}")
