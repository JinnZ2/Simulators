#!/usr/bin/env python3
"""Reads the four delivered-to-spec checks against the order that asked
for them. Every number in CLAIM_TABLE.md is computed here. Modifies
nothing; the constructed corpora below are labelled in their own text.
Refuses --selftest (checks live in selftest_csp.py).
"""

import ast
import io
import os
import sys
import tokenize
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
import p1_deps_extract as P1  # noqa: E402
import p2_substrate_audit as P2  # noqa: E402
import p3_comprehension as P3  # noqa: E402
import p4_goal_coherence as P4  # noqa: E402
import no_severity  # noqa: E402

SHIPPED = ["p1_deps_extract.py", "p2_substrate_audit.py", "p3_comprehension.py", "p4_goal_coherence.py", "run_all.py"]
NETWORK = {"socket", "urllib", "http", "ssl", "ftplib", "smtplib", "xmlrpc", "asyncio", "select", "selectors"}
STDLIB = getattr(sys, "stdlib_module_names", None)
MORAL = ["good", "evil", "nice", "nicer", "fair", "unfair", "deserve", "deserves", "virtue", "selfish",
         "greedy", "noble", "kind", "cruel", "honest", "dishonest", "blame", "guilty"]


def constraints():
    """The order's constraints, read from the files: line count, imports,
    network modules, 3.9 parse."""
    out = {}
    for f in SHIPPED:
        src = open(os.path.join(HERE, f), encoding="utf-8").read()
        tree = ast.parse(src)
        mods = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                mods.update(a.name.split(".")[0] for a in n.names)
            elif isinstance(n, ast.ImportFrom) and n.module:
                mods.add(n.module.split(".")[0])
        local = {m for m in mods if m.startswith("p") and m[1:2].isdigit()}
        ext = mods - local
        nonstd = sorted(m for m in ext if STDLIB is not None and m not in STDLIB)
        try:
            ast.parse(src, feature_version=(3, 9))
            p39 = True
        except SyntaxError:
            p39 = False
        out[f] = {"lines": src.count("\n") + (0 if src.endswith("\n") else 1), "under_300": src.count("\n") < 300,
                  "imports": sorted(ext), "non_stdlib": nonstd, "network_modules": sorted(ext & NETWORK),
                  "stdlib_table": STDLIB is not None, "parses_3_9": p39}
    return out


def p1_fixture():
    recs, rep = P1.run(os.path.join(HERE, "fixtures"))
    a = [r for r in recs if r["result_id"] == "constructed_result_a"]
    b = [r for r in recs if r["result_id"] == "constructed_result_b"]
    rep_b_only = P1.report(b, 1)
    return {"a_records": len(a), "a_by_class": dict(Counter(r["class"] for r in a)),
            "a_argued": sum(r["verified_in_argument"] for r in a), "b_records": len(b),
            "ratio_all": rep["ratio_required_over_argued"], "ratio_b_only": rep_b_only["ratio_required_over_argued"]}


def p1_in_tree(rel="energy"):
    """The pattern set over in-tree documents that are not methods
    sections. The records are returned for hand reading; the audit's
    reading of them is declared in CLAIM_TABLE, not computed."""
    recs, rep = P1.run(os.path.join(ROOT, rel))
    return {"dir": rel, "records": len(recs), "argued": rep["dependencies_argued"],
            "ratio": rep["ratio_required_over_argued"],
            "deps": [(r["class"], r["dependency"][:50], r["source_ref"]) for r in recs]}


def p2_shipped():
    out = {}
    for f in SHIPPED[:4]:
        r = P2.audit(os.path.join(HERE, f))
        out[f] = {"callsites": r["total_callsites"], "records": r["records"], "unverified": r["unverified_contracts"],
                  "ratio": r["ratio_unverified_over_callsites"], "verified": r["records"] - r["unverified_contracts"],
                  "ast_calls": r["ast_calls"], "bytecode_calls": r["bytecode_calls"]}
    return out


def p2_proxy_limits():
    """Three constructed sources showing what the verified proxy reads."""
    srcs = {
        "try_only": "def f():\n    try:\n        x = g()\n    except Exception:\n        pass\n    return x\n",
        "checked": "def f():\n    x = g()\n    assert isinstance(x, int)\n    return x\n",
        "bare": "def f():\n    x = g()\n    return x\n",
        "comprehension": "def f(xs):\n    return [x for x in xs]\n",
    }
    out = {}
    for k, s in srcs.items():
        tree = ast.parse(s)
        recs, sites = P2.call_records(tree)
        comp = P2.compile_records(s, "<%s>" % k)
        out[k] = {"sites": sites, "verified": sum(r["verified_at_callsite"] for r in recs),
                  "bytecode_calls": sum(c["bytecode_calls"] for c in comp)}
    return out


def p3_sample(terms=("instrument", "claim", "mechanism", "confidence"), reps=100):
    corp = P3.read_corpus(os.path.join(ROOT, "uninstrumented", "cases"))
    out = {}
    for t in terms:
        pr, _, _ = P3.observed(corp, t, 8, 2)
        obs, pairs = P3.mean_pairwise(pr)
        s = P3.summarise(P3.null_shuffle(corp, sorted(pr), t, 8, 2, reps, 0), obs)
        out[t] = {"sources": len(pr), "pairs": pairs, "observed": obs, "null_mean": s["mean"], "null_sd": s["sd"],
                  "gap_sd": s["gap_in_sd"], "frac_at_or_above": s["frac_at_or_above_observed"]}
    return out


SELF = ("cooperative-substrate/", "CLAUDE.md", "README.md")


def p3_tree(term="mass", min_count=3, reps=30):
    """Whole tree, twice: with everything, and with this folder and the
    two root index files left out -- the index describes this result in
    the term's own vocabulary, so a reading that includes it reads
    itself (the UNI_010 loop). Both are printed; the claim quotes the
    second."""
    corp_all = P3.read_corpus(ROOT, recursive=True)
    corp_ind = {k: v for k, v in corp_all.items() if not k.startswith(SELF[0]) and k not in SELF[1:]}
    out = {"term": term}
    for label, corp in (("all", corp_all), ("independent", corp_ind)):
        pr, _, _ = P3.observed(corp, term, 8, min_count)
        obs, pairs = P3.mean_pairwise(pr)
        s = P3.summarise(P3.null_shuffle(corp, sorted(pr), term, 8, min_count, reps, 0), obs)
        out[label] = {"docs": len(corp), "sources": len(pr), "pairs": pairs, "observed": obs,
                      "null_mean": s["mean"], "null_sd": s["sd"], "gap_sd": s["gap_in_sd"]}
    return out


def _constructed_corpus(same_sense):
    """CONSTRUCTED. Four sources using 'mass' either in one shared
    vocabulary (same_sense) or in four disjoint vocabularies."""
    banks = [
        "kilogram density volume weight inertia gravity newton acceleration force momentum",
        "priest altar liturgy hymn congregation cathedral sunday vestment sermon chalice",
        "crowd rally protest street banner march assembly throng gathering demonstration",
        "tumour lesion biopsy imaging scan tissue palpable growth nodule diagnosis",
    ]
    docs = {}
    for i in range(4):
        words = banks[0 if same_sense else i].split()
        toks = []
        for j in range(12):
            toks += words[j % len(words):] + ["mass"] + words[:j % len(words)]
        docs["constructed_%d" % i] = toks
    return docs


def p3_constructed(reps=100):
    out = {}
    for label, same in (("same_sense", True), ("disjoint_sense", False)):
        corp = _constructed_corpus(same)
        pr, _, _ = P3.observed(corp, "mass", 8, 2)
        obs, _ = P3.mean_pairwise(pr)
        s = P3.summarise(P3.null_shuffle(corp, sorted(pr), "mass", 8, 2, reps, 0), obs)
        out[label] = {"observed": obs, "null_mean": s["mean"], "null_sd": s["sd"], "gap_sd": s["gap_in_sd"]}
    return out


def p4_known(n=50, trials=1000, seed=0):
    ps = P4.grid("0.0:1.0:0.05")
    rows = P4.run(n, ps, trials, 10, seed)
    worst = 0.0
    for r in rows:
        q = min(1.0, max(0.0, r["exact_termination_rate"]))
        se = (q * (1 - q) / trials) ** 0.5
        worst = max(worst, abs(r["termination_rate"] - r["exact_termination_rate"]) / (se if se > 0 else 1.0))
    ex = [r["exact_termination_rate"] for r in rows]
    return {"p0_steps": rows[0]["mean_steps_to_answer"], "p0_rate": rows[0]["termination_rate"],
            "p1_rate": rows[-1]["termination_rate"], "worst_sim_vs_exact_in_se": worst,
            "monotone_nonincreasing": all(ex[i] >= ex[i + 1] - 1e-12 for i in range(len(ex) - 1)),
            "exact_at_0_5": ex[10], "exact_at_0_55": ex[11],
            "unbounded_at_0_5": P4.expected_steps_unbounded(n, 0.5),
            "growth_0_55_to_0_60": P4.expected_steps_unbounded(n, 0.6) / P4.expected_steps_unbounded(n, 0.55)}


def p4_budget_relative(n=10, p=0.6):
    """The zero is relative to the budget: same walk, two budgets."""
    small, large = P4.exact(n, p, 10 * n), P4.exact(n, p, 2000 * n)
    return {"n": n, "p": p, "rate_at_10N": small["termination_rate"], "rate_at_2000N": large["termination_rate"],
            "expected_unbounded": P4.expected_steps_unbounded(n, p)}


def framing_scan():
    """no_severity plus a moral-token list over comments and strings of
    the shipped files. Lexical: a paraphrase steps around it."""
    out = {}
    moral = [(w, __import__("re").compile(r"\b%s\b" % w, __import__("re").I)) for w in MORAL]
    for f in SHIPPED:
        src = open(os.path.join(HERE, f), encoding="utf-8").read()
        parts = [t.string for t in tokenize.generate_tokens(io.StringIO(src).readline)
                 if t.type in (tokenize.COMMENT, tokenize.STRING)]
        text = "\n".join(parts)
        out[f] = {"severity_hits": sorted({w for _, w, _ in no_severity.hits(text)}),
                  "moral_hits": sorted({w for w, p in moral if p.search(text)})}
    return out


def readme_checks():
    rd = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
    wo = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()
    frame = wo.split("```\n")[1]
    note = [b for b in wo.split("```\n") if b.startswith("Multiagent")][0]
    heads = [l for l in rd.splitlines() if l.startswith("#")]
    return {"framing_verbatim": frame in rd, "note_verbatim": note in rd,
            "falsification_rows": sum(1 for l in rd.split("## Falsification table")[1].split("## ")[0].splitlines()
                                      if l.startswith("| P")),
            "author_or_provenance_heading": any(w in h.lower() for h in heads for w in ("author", "provenance", "working style"))}


def render():
    L = ["cooperative-substrate order audit"]
    L.append("constraints:")
    for f, c in constraints().items():
        L.append("  %-22s lines %3d under_300 %s non_stdlib %s network %s parses_3.9 %s" % (
            f, c["lines"], c["under_300"], c["non_stdlib"], c["network_modules"], c["parses_3_9"]))
    fx = p1_fixture()
    L.append("P1 fixture: a %d records %s argued %d; b %d records; ratio(all) %s ratio(b only) %s" % (
        fx["a_records"], fx["a_by_class"], fx["a_argued"], fx["b_records"], fx["ratio_all"], fx["ratio_b_only"]))
    it = p1_in_tree()
    L.append("P1 in-tree (%s): %d records, %d argued, ratio %s" % (it["dir"], it["records"], it["argued"], it["ratio"]))
    for c, d, s in it["deps"]:
        L.append("    %-18s %-50s %s" % (c, d, s))
    L.append("P2 shipped:")
    for f, r in p2_shipped().items():
        L.append("  %-22s sites %3d records %3d unverified %3d verified %2d ratio %.3f ast %d bytecode %d" % (
            f, r["callsites"], r["records"], r["unverified"], r["verified"], r["ratio"], r["ast_calls"], r["bytecode_calls"]))
    L.append("P2 proxy on constructed sources: %s" % p2_proxy_limits())
    L.append("P3 on uninstrumented/cases (min_count 2, window 8, 100 reps):")
    for t, r in p3_sample().items():
        L.append("  %-12s sources %2d pairs %3d observed %.4f null %.4f sd %.4f gap %5.1f sd  frac>= %.2f" % (
            t, r["sources"], r["pairs"], r["observed"], r["null_mean"], r["null_sd"], r["gap_sd"], r["frac_at_or_above"]))
    tr = p3_tree()
    for label in ("all", "independent"):
        t = tr[label]
        L.append("P3 whole tree %-11s (%d docs) term %r min_count 3: sources %d pairs %d observed %.4f null %.4f sd %.4f gap %.1f sd" % (
            label, t["docs"], tr["term"], t["sources"], t["pairs"], t["observed"], t["null_mean"], t["null_sd"], t["gap_sd"]))
    for k, r in p3_constructed().items():
        L.append("P3 constructed %-14s observed %.4f null %.4f sd %.4f gap %s" % (
            k, r["observed"], r["null_mean"], r["null_sd"], "%.1f" % r["gap_sd"] if r["gap_sd"] is not None else "undefined"))
    k4 = p4_known()
    L.append("P4 known answers: p=0 steps %.1f rate %.3f; p=1 rate %.3f; largest |sim-exact| %.2f se; monotone %s; "
             "exact 0.5 %.3f 0.55 %.2e; unbounded E at 0.5 %.0f; growth 0.55->0.60 %.0fx" % (
                 k4["p0_steps"], k4["p0_rate"], k4["p1_rate"], k4["worst_sim_vs_exact_in_se"], k4["monotone_nonincreasing"],
                 k4["exact_at_0_5"], k4["exact_at_0_55"], k4["unbounded_at_0_5"], k4["growth_0_55_to_0_60"]))
    b = p4_budget_relative()
    L.append("P4 budget-relative: N=%d p=%.2f rate at 10N %.3f, at 2000N %.3f (E unbounded %.0f)" % (
        b["n"], b["p"], b["rate_at_10N"], b["rate_at_2000N"], b["expected_unbounded"]))
    L.append("framing scan (comments and strings): %s" % framing_scan())
    L.append("README: %s" % readme_checks())
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("order_audit has no selftest; run selftest_csp.py", file=sys.stderr)
        sys.exit(2)
    print(render())
