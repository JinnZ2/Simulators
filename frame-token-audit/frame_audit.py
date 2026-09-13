#!/usr/bin/env python3
"""frame_audit.py -- frame-token density + hit extraction. stdlib, CC0.
v0 = lexicon as declared last turn. v1 = v0 + declared additions.
Stage 1 mechanical (this file). Stage 2 = human/model grading of each hit:
USE vs MENTION, then substrate swap -> SURVIVES | CHANGES | COLLAPSES."""
import re, sys, os, json
V0 = {
 "time_as_money": ["spend time","save time","waste time","invest","budget time","worth it","afford"],
 "persons_as_stock": ["human capital","human resources","labor market","headcount"],
 "world_as_stock": ["natural capital","ecosystem services","resources","externality"],
 "relation_as_debt": ["owe","pay attention","pay back","invest in"],
 "relabel": ["restructuring","correction","pivot","realignment"],
}
ADD = {  # v1 additions, declared
 "cost_price": ["cost","costs","costly","price","priced","pricing","cheap","cheaper","cheapest","expensive","pay","paid","pays"],
 "capital_market": ["capital","market","markets","invest","investment","returns","profit","asset","assets"],
 "value_worth": ["value","valuable","worth","afford","affordable","budget","budgets"],
 "efficiency": ["efficient","efficiency","optimize","optimise","optimization"],
}
def lex(v):
    L = {k: list(x) for k, x in V0.items()}
    if v == "v1":
        for k, x in ADD.items(): L.setdefault(k, []).extend(x)
    return L
def scan(text, L):
    words = len(re.findall(r"[A-Za-z]+", text))
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        taken = []
        for cls, toks in L.items():
            for t in sorted(set(toks), key=len, reverse=True):
                for m in re.finditer(r"\b%s\b" % re.escape(t), low):
                    if any(a <= m.start() < b for a, b in taken): continue
                    taken.append((m.start(), m.end()))
                    hits.append({"line": i, "cls": cls, "tok": t, "ctx": line.strip()[:110]})
    return words, hits
if __name__ == "__main__":
    v = sys.argv[1]; out = {}
    for fn in sys.argv[2:]:
        txt = open(fn, encoding="utf-8").read()
        w, h = scan(txt, lex(v))
        out[os.path.basename(fn)] = {"words": w, "hits": len(h),
            "per_1000": round(1000*len(h)/w, 1) if w else None,
            "by_cls": {c: sum(1 for x in h if x["cls"]==c) for c in sorted(set(x["cls"] for x in h))},
            "hit_list": h}
    json.dump(out, open("result_%s.json" % v, "w"), indent=1)
    print("%-26s %6s %5s %8s  %s" % ("text", "words", "hits", "/1000", "by class"))
    for k, r in out.items():
        print("%-26s %6d %5d %8s  %s" % (k, r["words"], r["hits"], r["per_1000"], r["by_cls"]))
