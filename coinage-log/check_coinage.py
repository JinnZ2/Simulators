#!/usr/bin/env python3
# check_coinage.py -- CC0, stdlib only, parses under 3.9.
#
# Checks the COINAGE LOG structurally and adjudicates NOTHING. The log
# records naming gaps -- referents with no word, each existing term
# failing for a stated reason -- and tests whether the absence of a
# word is itself a finding. This module verifies:
#   1  the entry is well-formed: a referent, a source, and NO adopted
#      name (left unnamed rather than forced)
#   2  every rejected term carries a reason (not just a list)
#   3  candidates were raised and none adopted
#   4  the woodpecker cross-check (a second trophic level) and the
#      absence-set-on-behaviour instrument are both named
#   5  the NULL discipline is stated, not hidden: a log that only ever
#      admits naming gaps is CONSTANT_FIRES until it declines one
#   6  the STATUS split of the memory file /topics/coinage-log.md
#      (coinage-log.md = File A, coined terms; vocabulary-gap-slots.md =
#      File B, unnamed slots / failure points / status fields) is in the
#      state MISSING_SOURCE.md declares: 0 of ~46.9k chars received, every
#      chunk MISSING_SOURCE, File A empty, File B holding only the one
#      entry seeded byte-identical from COINAGE_LOG.md. These checks PIN
#      the unreceived state; a chunk arriving turns them red on purpose.
# It does not decide whether any word is genuinely missing or merely
# unsearched -- that is the log's open question, not the checker's.

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "COINAGE_LOG.md")
FILE_A = os.path.join(HERE, "coinage-log.md")
FILE_B = os.path.join(HERE, "vocabulary-gap-slots.md")
MANIFEST = os.path.join(HERE, "MISSING_SOURCE.md")
SOURCE_CHARS_APPROX = 46900      # operator-stated, not measured here
EXPORT_CAP = 8000                # operator-stated

# the five terms the entry says fail, each with the reason it gives
REJECTED = {
    "cooperation": "intent",
    "symbiosis": "paired-species",
    "mutualism": "benefit ledger",
    "aggregation": "position only",
    "facilitation": "one organism easing another",
}
CANDIDATES = ["load-sharing", "phase-locking"]


def _read():
    return io.open(LOG, encoding="utf-8").read()


def entry_wellformed():
    """A referent, a source, and NO adopted name -- the left-unnamed
    device honoured rather than an approximation filled in."""
    t = _read()
    return {
        "has_entry_heading": "## ENTRY 001 — UNNAMED" in t,
        "name_adopted_none": bool(
            re.search(r"(?mi)^\s*Name adopted:\s*NONE\b", t)),
        "referent_stated":
            "jointly producing the local conditions each then" in t,
        "aggregate_is_the_habitat": "the aggregate IS the habitat" in t,
        "no_intent_no_ledger_no_channel":
            "no intent" in t.lower()
            and "no coordination channel" in t.lower(),
        "source_kavik": bool(re.search(r"(?mi)^\s*Source:\s*Kavik", t)),
        "left_unnamed_declared":
            "left unnamed rather than forcing one" in t.lower(),
    }


def rejected_terms_carry_reasons():
    """Each of the five rejected terms appears WITH its stated reason
    -- a rejection is not a bare list, it names why the term fails."""
    t = " ".join(_read().lower().split())   # fold line-wraps
    rows = {}
    for term, reason in REJECTED.items():
        rows[term] = term in t and reason.lower() in t
    return {"per_term": rows, "all_reasoned": all(rows.values()),
            "count": len(rows)}


def candidates_none_adopted():
    t = _read()
    raised = {c: c in t for c in CANDIDATES}
    # the only 'Name adopted' line says NONE; no candidate is adopted
    adopted = re.findall(r"(?mi)^\s*Name adopted:\s*(\S+)", t)
    return {
        "candidates_raised": raised,
        "all_raised": all(raised.values()),
        "adopted_values": adopted,
        "none_adopted": adopted == ["NONE"],
    }


def cross_checks_named():
    """The two things that make the entry more than an assertion: an
    independent confirmation from a second trophic level (cheap to
    verify) and the absence-set instrument the behavioural side runs
    on."""
    t = _read()
    tl = " ".join(t.lower().split())    # fold line-wraps
    return {
        "woodpecker_second_trophic_level":
            "woodpecker" in tl and "second trophic level" in tl,
        "woodpecker_cheap_to_verify":
            "you need the woodpecker" in tl or "cheap to verify" in tl,
        "pattern_class_not_intent":
            "pattern class" in tl and "not an intent claim" in tl,
        "absence_set_on_behaviour":
            "repertoire minus what fires" in tl,
        "absence_set_links_uninstrumented":
            "absence set applied to behaviour" in tl
            or "uninstrumented/` absence set" in t,
    }


def null_discipline():
    """The honest limit stated on the page, not hidden: one entry, all
    naming gaps, so the log has not been shown to DECLINE -- the
    UNI_004 / UNI_006 CONSTANT_FIRES shape -- and 'missing' is not yet
    separated from 'unsearched'."""
    t = _read()
    tl = " ".join(t.lower().split())    # fold line-wraps
    n_entries = len(re.findall(r"(?m)^## ENTRY \d", t))
    return {
        "n_entries": n_entries,
        "constant_fires_named": "constant_fires" in tl,
        "declines_not_yet_shown":
            "has not yet been shown to decline" in tl
            or "not yet been shown to decline" in tl,
        "missing_vs_unsearched_open":
            "not yet separated from" in tl
            and "was not searched" in tl,
        "provenance_separated":
            "[Kavik]" in t and "the render's" in t,
    }


def _txt(path):
    return io.open(path, encoding="utf-8").read()


def _frontmatter(t):
    m = re.match(r"---\n(.*?)\n---\n", t, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def _entry_001(t):
    # anchored at line start: a bare find() matched File B's prose MENTION
    # of the heading before the heading itself (found by running; README)
    hit = re.search(r"(?m)^## ENTRY 001", t)
    if hit is None:
        return None
    a = hit.start()
    b = t.find("\n---\n", a)
    b2 = t.find("\n## Remaining entries", a)
    ends = [x for x in (b, b2) if x >= 0]
    return t[a:min(ends)].rstrip("\n") if ends else t[a:].rstrip("\n")


def split_state():
    """The STATUS split as MISSING_SOURCE.md declares it. Reads three
    files, writes none. Absent counts are UNKNOWN in the files, never 0;
    this checks the files SAY so, it does not supply the count."""
    present = {k: os.path.exists(v) for k, v in
               (("file_a", FILE_A), ("file_b", FILE_B),
                ("manifest", MANIFEST))}
    if not all(present.values()):
        return {"present": present}
    a, b, m = _txt(FILE_A), _txt(FILE_B), _txt(MANIFEST)
    fa, fb = _frontmatter(a), _frontmatter(b)
    keys = ("name", "description", "sources", "aliases")
    rows = re.findall(r"(?m)^\|\s*(\d+)\s*\|[^|]*\|\s*(\S+)\s*\|"
                      r"[^|]*\|\s*(\d+)\s*\|", m)
    expected_chunks = -(-SOURCE_CHARS_APPROX // EXPORT_CAP)
    seed_b, seed_log = _entry_001(b), _entry_001(_read())
    return {
        "present": present,
        "a_frontmatter_complete": all(fa.get(k) for k in keys),
        "b_frontmatter_complete": all(fb.get(k) for k in keys),
        "a_name": fa.get("name"),
        "b_name": fb.get("name"),
        "a_points_to_b": "vocabulary-gap-slots.md" in a,
        "b_points_to_a": "(coinage-log.md)" in b,
        "a_header_slot_missing_source":
            "## PURPOSE / USE / Format" in a and "MISSING_SOURCE" in a,
        "a_entries": len(re.findall(r"(?m)^## ENTRY \d", a)),
        "b_entries": len(re.findall(r"(?m)^## ENTRY \d", b)),
        "a_count_unknown_not_zero":
            "UNKNOWN" in a and "not 0" in a.lower(),
        "seed_identical_to_render":
            seed_b is not None and seed_b == seed_log,
        "seed_provenance_not_chunk1":
            "NOT chunk 1" in fb.get("sources", ""),
        "chunk_rows": len(rows),
        "expected_chunks": expected_chunks,
        "all_rows_missing":
            bool(rows) and all(st == "MISSING_SOURCE" for _, st, _ in rows),
        "received_total": sum(int(r) for _, _, r in rows),
        "received_line_zero": "**Received:** 0 of" in m,
        "no_reconstruction_declared":
            "No entry is reconstructed" in m,
    }


def render():
    L = []
    w = L.append
    w("COINAGE LOG -- STRUCTURAL CHECK")
    w("(the log is edited by nothing here; it records naming gaps and")
    w(" tests whether the absence of a word is itself a finding --")
    w(" this module computes structure and adjudicates no coinage)")
    w("")
    e = entry_wellformed()
    w("1  ENTRY WELL-FORMED (referent + source + NO adopted name)")
    for k in ("has_entry_heading", "name_adopted_none",
              "referent_stated", "aggregate_is_the_habitat",
              "no_intent_no_ledger_no_channel", "source_kavik",
              "left_unnamed_declared"):
        w("   %-34s %s" % (k, e[k]))
    w("")
    r = rejected_terms_carry_reasons()
    w("2  EACH REJECTED TERM CARRIES A REASON (%d terms)" % r["count"])
    for term, ok in r["per_term"].items():
        w("   %-14s reasoned: %s" % (term, ok))
    w("   all reasoned: %s" % r["all_reasoned"])
    w("")
    c = candidates_none_adopted()
    w("3  CANDIDATES RAISED, NONE ADOPTED")
    for cand, ok in c["candidates_raised"].items():
        w("   %-14s raised: %s" % (cand, ok))
    w("   adopted values: %s; none adopted: %s"
      % (c["adopted_values"], c["none_adopted"]))
    w("")
    x = cross_checks_named()
    w("4  CROSS-CHECKS NAMED")
    for k in ("woodpecker_second_trophic_level",
              "woodpecker_cheap_to_verify", "pattern_class_not_intent",
              "absence_set_on_behaviour",
              "absence_set_links_uninstrumented"):
        w("   %-38s %s" % (k, x[k]))
    w("")
    nd = null_discipline()
    w("5  NULL DISCIPLINE STATED, NOT HIDDEN")
    w("   entries: %d; CONSTANT_FIRES named: %s; declines not yet"
      % (nd["n_entries"], nd["constant_fires_named"]))
    w("   shown: %s; missing-vs-unsearched still open: %s;"
      % (nd["declines_not_yet_shown"], nd["missing_vs_unsearched_open"]))
    w("   provenance separated: %s" % nd["provenance_separated"])
    w("")
    sp = split_state()
    w("6  STATUS SPLIT OF /topics/coinage-log.md (see MISSING_SOURCE.md)")
    if not all(sp["present"].values()):
        w("   files present: %s" % sp["present"])
    else:
        w("   File A %s: frontmatter %s, entries %d, count UNKNOWN-not-0 %s"
          % (sp["a_name"], sp["a_frontmatter_complete"], sp["a_entries"],
             sp["a_count_unknown_not_zero"]))
        w("   File B %s: frontmatter %s, entries %d (seeded)"
          % (sp["b_name"], sp["b_frontmatter_complete"], sp["b_entries"]))
        w("   pointers A->B %s, B->A %s; seed identical to render %s;"
          % (sp["a_points_to_b"], sp["b_points_to_a"],
             sp["seed_identical_to_render"]))
        w("   seed provenance says NOT chunk 1: %s"
          % sp["seed_provenance_not_chunk1"])
        w("   chunks: %d rows (expected %d), all MISSING_SOURCE %s,"
          % (sp["chunk_rows"], sp["expected_chunks"],
             sp["all_rows_missing"]))
        w("   received %d chars; no reconstruction declared %s"
          % (sp["received_total"], sp["no_reconstruction_declared"]))
    w("")
    w("This module computes; it does not conclude, and it adjudicates")
    w("no coinage. Whether the word is missing or merely unsearched is")
    w("the log's open question -- see the STATE section.")
    return "\n".join(L)


def selftest():
    n = [0]

    def chk(name, ok):
        n[0] += 1
        if not ok:
            sys.stderr.write("FAIL %s\n" % name)
            sys.exit(1)

    import hashlib
    before = hashlib.sha256(io.open(LOG, "rb").read()).hexdigest()

    e = entry_wellformed()
    for k, v in e.items():
        chk("entry:" + k, v)

    r = rejected_terms_carry_reasons()
    chk("five rejected terms", r["count"] == 5)
    chk("every rejected term carries a reason", r["all_reasoned"])

    c = candidates_none_adopted()
    chk("both candidates raised", c["all_raised"])
    chk("no candidate adopted", c["none_adopted"])

    x = cross_checks_named()
    for k, v in x.items():
        chk("crosscheck:" + k, v)

    nd = null_discipline()
    chk("one entry", nd["n_entries"] == 1)
    chk("CONSTANT_FIRES null named", nd["constant_fires_named"])
    chk("declines not yet shown", nd["declines_not_yet_shown"])
    chk("missing-vs-unsearched open", nd["missing_vs_unsearched_open"])
    chk("provenance separated", nd["provenance_separated"])

    split_paths = (FILE_A, FILE_B, MANIFEST)
    split_before = [hashlib.sha256(io.open(p, "rb").read()).hexdigest()
                    for p in split_paths]
    sp = split_state()
    for k, v in sp["present"].items():
        chk("split:present:" + k, v)
    chk("split: File A frontmatter complete", sp["a_frontmatter_complete"])
    chk("split: File B frontmatter complete", sp["b_frontmatter_complete"])
    chk("split: File A name", sp["a_name"] == "coinage-log")
    chk("split: File B name", sp["b_name"] == "vocabulary-gap-slots")
    chk("split: A points to B", sp["a_points_to_b"])
    chk("split: B points to A", sp["b_points_to_a"])
    chk("split: header slot in A is MISSING_SOURCE",
        sp["a_header_slot_missing_source"])
    chk("split: File A holds 0 entries (none received)",
        sp["a_entries"] == 0)
    chk("split: File A states its count UNKNOWN, not 0",
        sp["a_count_unknown_not_zero"])
    chk("split: File B holds exactly the 1 seeded entry",
        sp["b_entries"] == 1)
    chk("split: seed byte-identical to COINAGE_LOG.md ENTRY 001",
        sp["seed_identical_to_render"])
    chk("split: seed provenance says NOT chunk 1",
        sp["seed_provenance_not_chunk1"])
    chk("split: manifest rows == ceil(46.9k/8000)",
        sp["chunk_rows"] == sp["expected_chunks"] == 6)
    chk("split: every chunk MISSING_SOURCE", sp["all_rows_missing"])
    chk("split: 0 chars received (table)", sp["received_total"] == 0)
    chk("split: 0 chars received (line)", sp["received_line_zero"])
    chk("split: no reconstruction declared",
        sp["no_reconstruction_declared"])

    # the seed check must be able to fail: a one-character drift reads False
    drifted = _entry_001(_txt(FILE_B)).replace("NONE", "NONE.", 1)
    chk("split: seed check detects a drifted copy",
        drifted != _entry_001(_read()))
    # and must not read a mention as the heading
    chk("split: a mention of the heading is not the heading",
        _entry_001("see the `## ENTRY 001` section\n## ENTRY 001 -- X\n")
        == "## ENTRY 001 -- X")

    render()
    after = hashlib.sha256(io.open(LOG, "rb").read()).hexdigest()
    chk("log untouched by the checker", before == after)
    chk("split files untouched by the checker",
        split_before == [hashlib.sha256(io.open(p, "rb").read()).hexdigest()
                         for p in split_paths])

    print("check_coinage selftest: %d/%d checks pass" % (n[0], n[0]))


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        selftest()
    else:
        print(render())
