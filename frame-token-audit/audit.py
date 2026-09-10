#!/usr/bin/env python3
"""audit.py -- runs the delivered frame_audit.py and reads what it does.
Imports the module, edits nothing. Stage 2 (USE vs MENTION, substrate swap)
is a human/model grading the delivery names and this file does NOT perform:
every density printed here is a Stage 1 count over ungraded hits.

    python3 audit.py            render
    python3 audit.py --selftest refused; see selftest_fta.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "fold-matrix"))
import frame_audit as fa  # noqa: E402
import fold_register as fr  # noqa: E402

CONSTRUCTIONS = os.path.join(ROOT, "ontology-probe", "ontologies", "substrate-primary", "constructions.jsonl")
ALIASES = os.path.join(ROOT, "ontology-probe", "ontologies", "substrate-primary", "aliases.json")
DOCS = ("SHAPE_SPEC.md", "PREAMBLE.md", "METHOD_SPEC.md")   # mention-heavy by their own subject

# Known-answer pair: same word count, one written in the frame, one outside it.
FRAME_TEXT = ("We spend time on the market because the return on capital is worth it, "
              "and we cannot afford to waste time on an asset with no value at any price.")
PLAIN_TEXT = ("We walked along the river because the light on the water was still bright, "
              "and we could not carry the heavy basket up the hill before the rain came.")


def shadowing(v):
    """A token scanned ALONE should land on the class that declares it. Where it
    lands elsewhere, an earlier class (dict order) took the span first: the
    delivered scan sorts longest-first WITHIN a class only, so a later class's
    longer phrase loses to an earlier class's prefix and can never fire."""
    L = fa.lex(v)
    out = []
    for cls, toks in L.items():
        for t in toks:
            _, h = fa.scan(t, L)
            land = [(x["cls"], x["tok"]) for x in h]
            if land != [(cls, t)]:
                out.append({"token": t, "declared": cls, "lands": land})
    return out


def overlap():
    """Tokens the v1 lexicon shares with two registers already in the tree, read
    by import: ontology-probe's scope_required / alias words and fold-matrix's
    REGISTER keys / ALIASES. A shared token is a shared word, not a shared
    reading -- each register attaches its own state to it."""
    al = json.load(open(ALIASES, encoding="utf-8"))
    scope = {e["term"] for e in al["scope_required"]}
    alias = {a["term"] for v in al["aliases"].values() for a in v}
    reg = set(fr.REGISTER) | set(fr.ALIASES)
    toks = {t for v in fa.lex("v1").values() for t in v}
    return {"lexicon_v1": len(toks),
            "ontology_probe_scope_required": sorted(toks & scope),
            "ontology_probe_aliases": sorted(toks & alias),
            "fold_matrix_register_or_alias": sorted(toks & reg),
            "in_none": sorted(toks - scope - alias - reg)}


def known_answer():
    out = {}
    for v in ("v0", "v1"):
        wf, hf = fa.scan(FRAME_TEXT, fa.lex(v))
        wp, hp = fa.scan(PLAIN_TEXT, fa.lex(v))
        out[v] = {"frame": {"words": wf, "hits": len(hf)}, "plain": {"words": wp, "hits": len(hp)}}
    we, he = fa.scan("", fa.lex("v1"))
    out["empty"] = {"words": we, "hits": len(he), "per_1000": None if not we else 0}
    _, hs = fa.scan("spend\ntime", fa.lex("v0"))
    out["line_split_phrase_hits"] = len(hs)
    return out


def constructions(v):
    """The operator's thirty hand-built constructions (ontology-probe run 1
    corpus), scanned per record; hits split by the construction's own class."""
    L = fa.lex(v)
    rows = [json.loads(l) for l in open(CONSTRUCTIONS, encoding="utf-8") if l.strip()]
    per_class = {}
    hit_ids = []
    for r in rows:
        _, h = fa.scan(r["text"], L)
        d = per_class.setdefault(r["class"], {"n": 0, "with_hit": 0, "hits": 0})
        d["n"] += 1
        d["hits"] += len(h)
        if h:
            d["with_hit"] += 1
            hit_ids.append((r["id"], r["class"], [(x["cls"], x["tok"]) for x in h]))
    return {"n": len(rows), "per_class": per_class, "hit_ids": hit_ids}


def docs(v):
    L = fa.lex(v)
    out = {}
    for name in DOCS:
        p = os.path.join(ROOT, name)
        if not os.path.exists(p):
            out[name] = "ABSENT"
            continue
        w, h = fa.scan(open(p, encoding="utf-8").read(), L)
        by = {}
        for x in h:
            by[x["cls"]] = by.get(x["cls"], 0) + 1
        out[name] = {"words": w, "hits": len(h), "per_1000": round(1000 * len(h) / w, 1) if w else None, "by_cls": by}
    return out


def render():
    L = []
    L.append("FRAME-TOKEN AUDIT -- Stage 1 counts over the delivered lexicon; Stage 2 (USE vs MENTION,")
    L.append("substrate swap) NOT performed here. No density below is a graded reading.")
    L.append("")
    L.append("lexicon: v0 %d tokens in %d classes; v1 %d tokens in %d classes" % (
        sum(len(v) for v in fa.lex("v0").values()), len(fa.lex("v0")),
        sum(len(v) for v in fa.lex("v1").values()), len(fa.lex("v1"))))
    L.append("")
    L.append("shadowed tokens (scanned alone, land on a different class -- can never fire as declared):")
    for v in ("v0", "v1"):
        for s in shadowing(v):
            L.append("  %s  %-12r declared %-17s lands %s" % (v, s["token"], s["declared"], s["lands"]))
    L.append("")
    ov = overlap()
    L.append("overlap of the v1 lexicon (%d tokens) with registers already in the tree, by import:" % ov["lexicon_v1"])
    for k in ("ontology_probe_scope_required", "ontology_probe_aliases", "fold_matrix_register_or_alias"):
        L.append("  %-32s %d  %s" % (k, len(ov[k]), ", ".join(ov[k])))
    L.append("  %-32s %d" % ("in none of the three", len(ov["in_none"])))
    L.append("")
    ka = known_answer()
    L.append("known answer (constructed pair, matched word count):")
    for v in ("v0", "v1"):
        L.append("  %s  frame %d hits / %d words   plain %d hits / %d words" % (
            v, ka[v]["frame"]["hits"], ka[v]["frame"]["words"], ka[v]["plain"]["hits"], ka[v]["plain"]["words"]))
    L.append("  empty text: words %d, per_1000 %s (None, not 0)" % (ka["empty"]["words"], ka["empty"]["per_1000"]))
    L.append("  a phrase split across a line break ('spend\\ntime'): %d hits (the scan is per line)" % ka["line_split_phrase_hits"])
    L.append("")
    for v in ("v0", "v1"):
        c = constructions(v)
        L.append("ontology-probe run-1 constructions (%d, hand-built by the operator) under %s:" % (c["n"], v))
        for cls in ("TARGETED", "CONTROL", "AMBIENT"):
            d = c["per_class"].get(cls, {"n": 0, "with_hit": 0, "hits": 0})
            L.append("  %-9s n %2d  with a hit %2d  hits %2d" % (cls, d["n"], d["with_hit"], d["hits"]))
        for cid, cls, hs in c["hit_ids"]:
            L.append("    %s %-9s %s" % (cid, cls, hs))
    L.append("")
    L.append("root documents whose SUBJECT is this vocabulary (mention-heavy by construction; DF_010):")
    for v in ("v0", "v1"):
        for name, d in docs(v).items():
            if d == "ABSENT":
                L.append("  %s %-16s ABSENT" % (v, name))
            else:
                L.append("  %s %-16s %6d words %4d hits %6s /1000  %s" % (v, name, d["words"], d["hits"], d["per_1000"], d["by_cls"]))
    L.append("")
    L.append("note: frame_audit.py writes result_<v>.json into the working directory with every hit's")
    L.append("context line, so a rescan of a directory holding a prior result reads its own output (UNI_010).")
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("audit.py: run python3 selftest_fta.py")
        sys.exit(2)
    print(render())
