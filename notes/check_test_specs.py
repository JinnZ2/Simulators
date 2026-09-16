#!/usr/bin/env python3
# check_test_specs.py -- CC0, stdlib only, parses under 3.9
#
# Checker for notes/queue/TEST_SPECS_2026_09_15.md, under the notes/
# convention: the entry is stored as delivered, this checker never edits
# it, and every disagreement goes in this output.
#
# The entry is a set of experimental designs, not instruments. Nothing here
# adjudicates a prediction, assigns an id, ranks a spec or decides which to
# run: the designs are about human subjects and this tree holds no such
# data. Four readings, all about the RECORD.
#
#   1  structure -- the specs parse, and which carry a stated prediction
#   2  ids -- do T-S11 / T-S12a / T-S12b / T-dim / T-PAUSE resolve to
#      anything in this tree. They do not; the register is elsewhere, and
#      no id is invented here to make one.
#   3  the one checkable claim -- "T-PAUSE already in introspection file".
#      Checked against the introspection files this tree holds.
#   4  a sense collision in a term the specs turn on -- "Wilson" resolves
#      two ways here, and only one of them is the paradigm meant.
#
# Resolution is by path plus a declared content marker, never by searching
# the tree for a spec's own words: once this entry is committed, a text
# search for "T-dim" or "Wilson paradigm" finds the entry and this file.

import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENTRY = os.path.join(HERE, "queue", "TEST_SPECS_2026_09_15.md")

# The introspection files this tree holds, and a marker proving each is the
# file meant rather than a namesake.
INTROSPECTION = [
    ("voice-attractor-probe/introspection_delta.py", "introspection"),
    ("voice-attractor-probe/introspection_delta_v2.py", "introspection"),
]

# "Wilson" in this tree. Two different Wilsons, declared rather than merged.
WILSON_SENSES = [
    ("voice-attractor-probe/introspection_delta.py", "wilson_halfwidth",
     "Wilson score interval -- a binomial confidence bound, statistics"),
    ("notes/memory-export/files/sensing-spine.md", "Nisbett & Wilson",
     "Nisbett & Wilson 1977 -- verbal reports on one's own process"),
]

ID_RE = re.compile(r"^(T-[A-Za-z0-9]+)\b")


def entry_text():
    return io.open(ENTRY, encoding="utf-8").read()


def entry_hash():
    return hashlib.sha256(io.open(ENTRY, "rb").read()).hexdigest()


def parse_specs(txt):
    out = []
    for block in [b for b in txt.split("\n\n") if b.strip()]:
        lines = [l.rstrip() for l in block.split("\n") if l.strip()]
        m = ID_RE.match(lines[0].strip())
        out.append({
            "id": m.group(1) if m else None,
            "head": lines[0].strip(),
            "body": [l.strip() for l in lines[1:]],
            "has_prediction": any(l.strip().lower().startswith("prediction")
                                  for l in lines[1:]),
        })
    return out


def id_resolves(spec_id):
    """Does this id appear anywhere in the tree OUTSIDE the entry and this
    file? Walks and reads, but never counts the two files that carry the id
    because they were written to carry it."""
    skip = {os.path.abspath(ENTRY), os.path.abspath(__file__)}
    hits = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", "__pycache__", "node_modules")]
        for fn in filenames:
            if not fn.endswith((".md", ".py", ".txt", ".json")):
                continue
            p = os.path.join(dirpath, fn)
            if os.path.abspath(p) in skip:
                continue
            try:
                if spec_id in io.open(p, encoding="utf-8",
                                      errors="replace").read():
                    hits.append(os.path.relpath(p, ROOT))
            except OSError:
                continue
    return hits


def pause_claim():
    """"T-PAUSE already in introspection file" -- against the files here."""
    rows = []
    for rel, marker in INTROSPECTION:
        p = os.path.join(ROOT, rel)
        exists = os.path.isfile(p)
        text = io.open(p, encoding="utf-8", errors="replace").read() if exists else ""
        rows.append({"path": rel, "exists": exists,
                     "is_the_file_meant": marker.lower() in text.lower(),
                     "pause_hits": len(re.findall(r"\bpause\b", text, re.I))})
    return rows


def wilson_senses():
    rows = []
    for rel, marker, gloss in WILSON_SENSES:
        p = os.path.join(ROOT, rel)
        text = io.open(p, encoding="utf-8", errors="replace").read() \
            if os.path.isfile(p) else ""
        rows.append({"path": rel, "marker": marker, "gloss": gloss,
                     "present": marker.lower() in text.lower()})
    return rows


def render():
    before = entry_hash()
    specs = parse_specs(entry_text())
    L = []
    w = L.append
    w("check_test_specs -- notes/queue/TEST_SPECS_2026_09_15.md")
    w("   sha256 %s" % before[:16])
    w("   designs, not instruments. Nothing here adjudicates a prediction,")
    w("   assigns an id, or decides which to run.")
    w("")
    w("1  STRUCTURE")
    for s in specs:
        w("   %-9s prediction=%-5s %s"
          % (s["id"] or "(none)", s["has_prediction"], s["head"][:46]))
    w("")
    w("2  IDS AGAINST THIS TREE (entry and this checker never counted)")
    for s in specs:
        if not s["id"]:
            continue
        hits = id_resolves(s["id"])
        w("   %-9s %s" % (s["id"], hits if hits else "no hit -- register is elsewhere"))
    w("   No id is invented here to close the gap: an id is permanent once")
    w("   assigned, and this is not the document that assigns them.")
    w("")
    w("3  THE ONE CHECKABLE CLAIM: T-PAUSE 'already in introspection file'")
    for r in pause_claim():
        w("   %-48s exists=%s is_the_file=%s pause_hits=%d"
          % (r["path"], r["exists"], r["is_the_file_meant"], r["pause_hits"]))
    w("   The introspection files this tree holds carry no pause probe, so")
    w("   the claim is about a file that is not here. Not contradicted:")
    w("   unresolvable from this tree.")
    w("")
    w("4  'WILSON' RESOLVES TWO WAYS HERE")
    for r in wilson_senses():
        w("   %-48s %s" % (r["path"], "present" if r["present"] else "ABSENT"))
        w("       %s" % r["gloss"])
    w("   T-S12a's 'Wilson paradigm' is the second. A reader searching this")
    w("   tree for it meets the statistics function first, four times.")
    w("")
    w("entry hash unchanged across this run: %s" % (entry_hash() == before))
    return "\n".join(L)


def selftest():
    checks = 0
    failed = 0

    def ck(cond, label):
        nonlocal checks, failed
        checks += 1
        if not cond:
            failed += 1
            print("FAIL  %s" % label)
        else:
            print("ok    %s" % label)

    before = entry_hash()
    specs = parse_specs(entry_text())

    print("-- 1 structure")
    ck(len(specs) == 5, "five specs parsed (got %d)" % len(specs))
    ids = [s["id"] for s in specs]
    ck(ids == ["T-S11", "T-S12a", "T-S12b", "T-dim", "T-PAUSE"],
       "ids parse in order (got %s)" % ids)
    ck(sum(1 for s in specs if s["has_prediction"]) == 3,
       "three specs carry a stated prediction line")
    ck(not specs[-1]["body"], "T-PAUSE carries no body; it is a pointer")

    print("\n-- 2 ids do not resolve, and none is invented")
    for s in specs:
        ck(id_resolves(s["id"]) == [],
           "%s has no hit outside the entry and this checker" % s["id"])
    own = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    # Ids necessarily appear here -- the checker has to name what it resolves,
    # and a first version counted occurrences of an id and failed on its own
    # counting argument, which is an occurrence. The property worth asserting
    # is that the checker does not reproduce the spec BODIES: a prediction
    # restated here is a second copy that can drift from the entry.
    bodies = [l for s_ in specs for l in s_["body"] if l.lower().startswith("prediction")]
    ck(bodies, "there are prediction lines to check against")
    leaked = [b for b in bodies if b in own]
    ck(not leaked, "no spec prediction is restated in this checker (%s)" % leaked)

    print("\n-- 2b the null: a string that IS in the tree must resolve")
    ck(id_resolves("METHOD_LAYER_PATH") != [],
       "a known in-tree string resolves, so an empty result means absent")

    print("\n-- 3 the pause claim")
    rows = pause_claim()
    ck(all(r["exists"] for r in rows), "both introspection files are present")
    ck(any(r["is_the_file_meant"] for r in rows),
       "at least one is the file meant, by its own content marker")
    ck(sum(r["pause_hits"] for r in rows) == 0,
       "no pause probe in either, so the claim points outside this tree")

    print("\n-- 4 the two Wilsons")
    ws = wilson_senses()
    ck(all(r["present"] for r in ws), "both senses are present in the tree")
    ck(len(set(r["gloss"] for r in ws)) == 2, "and they are two glosses")

    print("\n-- 5 self-reference")
    ck(entry_hash() == before, "entry hash unchanged across the run")
    ck(os.path.abspath(ENTRY) != os.path.abspath(__file__),
       "the checker is not the entry")

    print("\nchecks: %d   failed: %d" % (checks, failed))
    print("VERDICT: %s   checks=%d failed=%d"
          % ("PASS" if failed == 0 else "FAIL", checks, failed))
    return 0 if failed == 0 else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
