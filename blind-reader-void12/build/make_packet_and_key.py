#!/usr/bin/env python3
"""Build the blind-reader packet and the scoring key for VOID-12 (vocabulary mapping rows).

Reads the first reader's declarations from combined-playground/cplay/vocab_branches.py (the "key") and writes:
  reader_packet/terms.json            15 terms, neutral ids, fixed shuffled order, definition + source location ONLY
  reader_packet/response_template.json
  reader_packet/sources/...           the pinned source files, byte-exact as at their pinned commits
                                      (COMBINED_SPEC.md is cut before section 9c; the cut is recorded)
  reader_packet/PACKET_MANIFEST.json  sha256 of every packet file
  scoring/key.json                    the first reader's predicates, slots, clusters and tiers, per neutral id
It then checks that the packet contains none of the first reader's predicate strings, tier names or branch names.

Run (paths are clones of the four repositories; each needs the pinned commit in its history):
  SIM_DIR=Simulators TAF_DIR=thermodynamic-accountability-framework FA_DIR=formula-audit python3 make_packet_and_key.py
Reproducible: the shuffle is seeded (SEED below) and the output is deterministic for a given first-reader module.
"""
import hashlib, json, os, random, re, subprocess, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the blind-reader-void12 folder
SIM = os.environ.get("SIM_DIR", "Simulators")
TAF = os.environ.get("TAF_DIR", "thermodynamic-accountability-framework")
FA = os.environ.get("FA_DIR", "formula-audit")
SEED = 20261118
SPEC_PATH = "playground-crossrun/COMBINED_SPEC.md"
SPEC_CUT_BEFORE = "### 9c."          # first heading that is withheld from the reader
REPO_DIR = {"thermodynamic-accountability-framework": TAF, "Simulators": SIM, "formula-audit": FA}
# files a reader may need: every pinned definition source, plus the code the first reader says it read slots from
EXTRA_SOURCES = [
    ("thermodynamic-accountability-framework", "calibration/unified_audit.py"),
    ("thermodynamic-accountability-framework", "calibration/expiry_register.py"),
    ("Simulators", "combined-playground/cplay/tokens.py"),
    ("Simulators", "combined-playground/cplay/axes.py"),
    ("Simulators", "combined-playground/cplay/closure.py"),
]

sys.path.insert(0, os.path.join(SIM, "combined-playground"))
from cplay import vocab_branches as V  # noqa: E402


def git_show(repo, commit, path):
    out = subprocess.run(["git", "-C", REPO_DIR[repo], "show", "%s:%s" % (commit, path)], capture_output=True)
    if out.returncode:
        raise SystemExit("cannot read %s@%s:%s : %s" % (repo, commit[:7], path, out.stderr.decode()[:200]))
    return out.stdout


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    terms = list(V.TERMS)
    pairs = [(x, y) for x, y in V.PAIRS]
    # fixed shuffle; re-draw (deterministically) until no key pair is adjacent in the list
    rng = random.Random(SEED)
    order = list(range(len(terms)))
    while True:
        rng.shuffle(order)
        pos = {terms[i].term_id: n for n, i in enumerate(order)}
        if all(abs(pos[a] - pos[b]) > 1 for a, b in pairs):
            break
    ids = {terms[i].term_id: "T%02d" % (n + 1) for n, i in enumerate(order)}

    # sources
    served, want = {}, {}
    for t in terms:
        want[(t.pin.repo, t.pin.commit, t.pin.path)] = t.pin.sha256
    for repo, path in EXTRA_SOURCES:
        commit = next(t.pin.commit for t in terms if t.pin.repo == repo)
        want.setdefault((repo, commit, path), None)
    pdir = os.path.join(HERE, "reader_packet")
    sdir = os.path.join(pdir, "sources")
    os.makedirs(sdir, exist_ok=True)
    src_manifest = []
    for (repo, commit, path), pinned in sorted(want.items()):
        raw = git_show(repo, commit, path)
        if pinned and sha(raw) != pinned:
            raise SystemExit("pin sha mismatch for %s:%s" % (repo, path))
        body, note, name = raw, "complete file", path
        if path == SPEC_PATH:
            text = raw.decode("utf-8")
            i = text.index(SPEC_CUT_BEFORE)
            body = text[:i].encode("utf-8")
            kept = text[:i].count("\n")
            note = "cut before the heading %r: lines 1-%d of %d; line numbers are those of the full file" % (
                SPEC_CUT_BEFORE, kept, text.count("\n"))
            name = path.replace(".md", ".lines_1-%d.md" % kept)
        dest = os.path.join(sdir, repo, name)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "wb").write(body)
        served[(repo, path)] = os.path.relpath(dest, pdir).replace(os.sep, "/")
        src_manifest.append({"served_as": served[(repo, path)], "repo": repo, "commit": commit, "path": path,
                             "sha256_of_full_file_at_commit": sha(raw), "bytes_served": len(body), "note": note})

    out_terms = []
    for n, i in enumerate(order):
        t = terms[i]
        out_terms.append({"id": "T%02d" % (n + 1), "label": t.label, "definition": t.definition,
                          "source": {"repo": t.pin.repo, "commit": t.pin.commit, "path": t.pin.path,
                                     "served_as": served[(t.pin.repo, t.pin.path)], "anchor": t.pin.anchor}})
    json.dump({"note": "Fifteen terms from three projects. Order is fixed and carries no meaning.", "terms": out_terms},
              open(os.path.join(pdir, "terms.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    tmpl = {"reader_label": "", "model_family": "", "date_utc": "",
            "terms": {x["id"]: {"cluster": "", "predicate": "", "slots": [], "slots_basis": "", "source_lines_read": "",
                                "confidence": "", "could_also_join": []} for x in out_terms},
            "attestation": {"q1_seen_pair_table_with_verdicts": "", "q2_seen_predicate_sentence_by_someone_else": "",
                            "q3_seen_vocabulary_mapping_or_second_reader_report": "", "q4_told_how_many_clusters_or_pairs": "",
                            "q5_used_anything_outside_packet": "", "q6_prior_sessions_about_this_project": "", "notes": ""}}
    json.dump(tmpl, open(os.path.join(pdir, "response_template.json"), "w", encoding="utf-8"), indent=1)

    # key
    cl = {}
    for t in terms:
        cl.setdefault(t.predicate, len(cl) + 1)
    key_terms = {ids[t.term_id]: {"term_id": t.term_id, "label": t.label, "predicate": t.predicate, "slots": list(t.slots),
                                  "slots_from": t.slots_from, "cluster": cl[t.predicate]} for t in terms}
    key_pairs = []
    for a, b in pairs:
        ta, tb = V.term(a), V.term(b)
        rel = V.relation(ta, tb)
        same_p = ta.predicate == tb.predicate
        set_eq = sorted(map(str.lower, ta.slots)) == sorted(map(str.lower, tb.slots))
        if same_p:
            assert set_eq == (tuple(ta.slots) == tuple(tb.slots)), "set vs ordered slot equality differ for %s | %s" % (a, b)
        key_pairs.append({"left": ids[a], "right": ids[b], "pair_label": "%s | %s" % (ta.label, tb.label), "key_tier": rel,
                          "same_predicate": same_p, "slots_equal": set_eq, "same_label": ta.label == tb.label})
    meta = {"first_reader_module": "combined-playground/cplay/vocab_branches.py",
            "first_reader_module_sha256": sha(open(os.path.join(SIM, "combined-playground/cplay/vocab_branches.py"), "rb").read()),
            "simulators_head": subprocess.run(["git", "-C", SIM, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
            "shuffle_seed": SEED, "n_terms": len(terms), "n_pairs": len(pairs), "n_predicate_clusters": len(cl)}
    json.dump({"meta": meta, "terms": key_terms, "pairs": key_pairs}, open(os.path.join(HERE, "scoring", "key.json"), "w",
              encoding="utf-8"), indent=1, ensure_ascii=False)

    # leak check over everything the reader will receive
    forbidden_cs = ["MAPS", "PARTIAL", "HOMONYM", "SPLIT", "V-A", "V-B", "V-C"]
    forbidden_ci = [t.predicate for t in terms] + ["vocab_branches", "second reader", "second-reader", "VOID-12", "blind"]
    # reviewed exceptions: (file, word) -> reason. "SPLIT" in closure.py names that file's own table of verdict
    # branches A-G; it has nothing to do with the vocabulary mapping. The file is a pinned source and is served unchanged.
    allowed = {("sources/Simulators/combined-playground/cplay/closure.py", "SPLIT"):
               "closure.py's own branch table (verdict branches A-G), unrelated to the vocabulary mapping"}
    hits, waived = [], []
    for d, _, fs in os.walk(pdir):
        for f in fs:
            if f == "PACKET_MANIFEST.json":
                continue
            p = os.path.join(d, f)
            txt = open(p, encoding="utf-8", errors="replace").read()
            for w in forbidden_cs:
                if re.search(r"\b%s\b" % re.escape(w), txt):
                    hits.append((os.path.relpath(p, pdir), w))
            for w in forbidden_ci:
                if w.lower() in txt.lower():
                    hits.append((os.path.relpath(p, pdir), w))
    waived = [dict(file=k[0], word=k[1], reason=v) for k, v in allowed.items() if (k[0], k[1]) in hits]
    hits = [h for h in hits if h not in allowed]
    man = {"reviewed_leak_check_exceptions": waived, "files": {}}
    for d, _, fs in os.walk(pdir):
        for f in sorted(fs):
            if f == "PACKET_MANIFEST.json":
                continue
            p = os.path.join(d, f)
            b = open(p, "rb").read()
            man["files"][os.path.relpath(p, pdir).replace(os.sep, "/")] = {"bytes": len(b), "sha256": sha(b)}
    man["sources"] = src_manifest
    json.dump(man, open(os.path.join(pdir, "PACKET_MANIFEST.json"), "w"), indent=1)
    print("terms %d, pairs %d, predicate clusters %d, files in packet %d" % (len(terms), len(pairs), len(cl), len(man["files"])))
    print("leak check hits:", hits if hits else "none")
    if hits:
        sys.exit(1)


if __name__ == "__main__":
    main()
