#!/usr/bin/env python3
"""selftest_fta.py -- checks for frame-token-audit/. Prints its count."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import frame_audit as fa  # noqa: E402
import audit  # noqa: E402

_n = [0]


def check(cond, msg):
    _n[0] += 1
    if not cond:
        raise AssertionError("check %d: %s" % (_n[0], msg))


def main():
    # delivered file is verbatim: its lexicon is what the audit reads
    v0, v1 = fa.lex("v0"), fa.lex("v1")
    check(len(v0) == 5 and len(v1) == 9, "class counts")
    check(sum(len(v) for v in v1.values()) == 57 and len({t for v in v1.values() for t in v}) == 55,
          "FTA_001: two tokens (invest, afford) are declared in both V0 and ADD -- 57 declared, 55 distinct")
    # FTA_001 shadowing: the later declaration can never fire; 'invest in' never fires at all
    s0 = {(x["token"], x["declared"]) for x in audit.shadowing("v0")}
    s1 = {(x["token"], x["declared"]) for x in audit.shadowing("v1")}
    check(s0 == {("invest in", "relation_as_debt")}, "v0: 'invest in' is shadowed by time_as_money's 'invest'")
    check(s1 == {("invest in", "relation_as_debt"), ("invest", "capital_market"), ("afford", "value_worth")},
          "v1: three declared tokens land on time_as_money")
    _, h = fa.scan("we invest in people", v1)
    check([(x["cls"], x["tok"]) for x in h] == [("time_as_money", "invest")],
          "the longer phrase in a later class loses to an earlier class's prefix")
    # not CONSTANT_FIRES / CONSTANT_SILENT: the constructed pair separates
    ka = audit.known_answer()
    check(ka["v1"]["frame"]["hits"] == 9 and ka["v1"]["plain"]["hits"] == 0, "known-answer pair separates under v1")
    check(ka["v0"]["frame"]["hits"] == 4 and ka["v0"]["plain"]["hits"] == 0, "known-answer pair separates under v0")
    check(abs(ka["v1"]["frame"]["words"] - ka["v1"]["plain"]["words"]) <= 1, "pair is matched on words")
    check(ka["empty"]["per_1000"] is None, "empty text is None, not 0 (the delivered per_1000 rule)")
    check(ka["line_split_phrase_hits"] == 0, "FTA_003: a phrase across a line break is missed (per-line scan)")
    # FTA_002 overlap by import
    ov = audit.overlap()
    check(ov["ontology_probe_scope_required"] == ["capital", "efficiency", "market", "optimization", "optimize", "value"],
          "six v1 tokens are ontology-probe scope_required terms")
    check("resources" in ov["fold_matrix_register_or_alias"] and "cost" in ov["fold_matrix_register_or_alias"],
          "fold-matrix register overlap")
    check(ov["ontology_probe_aliases"] == [], "no v1 token is an ontology-probe absent-term alias")
    # FTA_004 constructions: v0 silent on all thirty, v1 fires on 3 and 0 of them TARGETED
    c0, c1 = audit.constructions("v0"), audit.constructions("v1")
    check(c0["n"] == 30 and c0["hit_ids"] == [], "v0 fires on none of the thirty constructions")
    check([i for i, _, _ in c1["hit_ids"]] == ["c-012", "c-024", "c-025"], "v1 fires on c-012, c-024, c-025")
    check(c1["per_class"]["TARGETED"]["hits"] == 0, "no TARGETED construction carries a v1 token")
    # FTA_005 the verb sense of `returns` fires (T1-1)
    _, h = fa.scan("the function returns a null", v1)
    check([(x["cls"], x["tok"]) for x in h] == [("capital_market", "returns")], "`returns` (verb) fires as capital_market")
    d = audit.docs("v1")
    check(d["SHAPE_SPEC.md"]["hits"] == 6 and d["SHAPE_SPEC.md"]["by_cls"].get("cost_price") == 5,
          "SHAPE_SPEC section 9, which argues against cost, carries 5 cost_price hits (mention)")
    check(all(v["hits"] == 0 for v in audit.docs("v0").values()), "v0 is silent on all three root documents")
    # the audit refuses --selftest; the render carries the Stage 2 disclaimer
    r = audit.render()
    check("NOT performed here" in r and "UNI_010" in r, "render states Stage 2 undone and the self-read loop")
    print("selftest_fta: %d checks passed" % _n[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
