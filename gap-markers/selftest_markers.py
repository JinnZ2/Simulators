#!/usr/bin/env python3
"""Selftest for markers.py.

The parse arms are the ones that earned their place: the first version
of `fields()` returned SIX of seven, and a check asserting the parse is
non-empty passes on that. So the count is asserted, every parsed name
is asserted to appear in the delivered file, and a constructed
malformed document must not parse clean.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import markers as M  # noqa: E402


def run():
    ok, bad = [0], []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    doc = M._doc()

    # -- 1. the parse. Completeness, not just non-emptiness.
    chk("seven fields are parsed", len(M.FIELDS) == 7)
    chk("WHAT_IS_MISSING is one of them",
        "WHAT_IS_MISSING" in M.FIELDS)
    chk("every parsed field appears in the delivered file",
        all(f in doc for f in M.FIELDS))
    chk("the STATE line names exactly the parsed states",
        set(M.STATES) == set(
            x.strip() for x in
            doc.split("STATE           ")[1].split("\n")[0].split("|")))
    chk("five states", len(M.STATES) == 5)
    chk("two kinds", len(M.KINDS) == 2)
    chk("every state carries a definition",
        all(len(v) > 20 for v in M.STATES.values()))
    chk("every kind carries a definition",
        all(len(v) > 20 for v in M.KINDS.values()))
    chk("the kind names are the ones the KIND line lists",
        set(M.KINDS) == set(
            x.strip() for x in
            doc.split("KIND            ")[1].split("\n")[0].split("|")))
    # a field whose column is one space wide must still parse
    chk("a one-space column parses",
        M.FIELDS.index("WHAT_IS_MISSING") == 4)

    # -- 2. KIND x STATE, from the definitions
    c = M.cross()
    chk("ten cells", c["cells"] == 10)
    chk("KIND is free on exactly one state",
        c["states_where_kind_is_free"] == 1)
    chk("and that state is uncounted",
        next(r["state"] for r in c["rows"] if r["forced"] is None)
        == "uncounted")
    chk("the other four are forced to boundary-artifact",
        all(r["forced"] == M.BOUNDARY for r in c["rows"]
            if r["state"] != "uncounted"))
    chk("each forced state names the phrase that forces it",
        all(r["by"] for r in c["rows"] if r["forced"]))
    chk("and every such phrase is in the delivered definition",
        all(r["by"].lower() in M.STATES[r["state"]].lower()
            for r in c["rows"] if r["by"]))
    chk("boundary-artifact is open on every state",
        all(r["boundary-artifact"] for r in c["rows"]))
    # the forcing must be READ, not hardcoded: a definition with no
    # existence claim leaves both open.
    saved = M.STATES["undated"]
    try:
        M.STATES["undated"] = "currency unknown"
        chk("a definition with no existence claim frees the kind",
            M.kind_forced("undated")["forced"] is None)
    finally:
        M.STATES["undated"] = saved
    chk("and the real definition forces it again",
        M.kind_forced("undated")["forced"] == M.BOUNDARY)

    # -- 3. the delivered distribution line is derivable
    chk("the file states the distribution",
        "Most entries here are boundary-artifact" in doc)
    chk("and four of five states force it", 4 == sum(
        1 for r in c["rows"] if r["forced"] == M.BOUNDARY))

    # -- 4. no negative state
    chk("no state means nothing-is-missing-here",
        not any(k in M.STATES for k in
                ("none", "clear", "covered", "no-gap", "checked")))
    chk("all five definitions describe an absence",
        all(any(w in v.lower() for w in
                ("no ", "never", "unknown", "not "))
            for v in M.STATES.values()))

    # -- 5. ENTRY_POINT
    chk("ENTRY_POINT is conditional in the delivered text",
        "where one exists" in doc)
    chk("and no state or field records which of the two absences",
        not any("entry" in f.lower() and f != "ENTRY_POINT"
                for f in M.FIELDS))

    # -- 6. the reading rule is recorded, never inferred
    u = M.sort_record("b1")
    chk("an unsorted boundary says so", u["branch"] == "UNSORTED")
    chk("and does not read as sorted-and-neither",
        "Not the same as" in u["note"])
    s = M.sort_record("b1", "keep", "the correlation breaks off its "
                                    "calibration range")
    chk("a declared sort is recorded", s["branch"] == "keep")
    chk("with its reason", s["reason"])
    chk("and is marked declared", "declared" in s["sorted_by"])
    for bad_branch in ("neither", "maybe", "KEEP"):
        try:
            M.sort_record("b1", bad_branch, "r")
            chk("branch %r is refused" % bad_branch, False)
        except M.SchemaMismatch:
            chk("branch %r is refused" % bad_branch, True)
    try:
        M.sort_record("b1", "keep", "   ")
        chk("a sort with no reason is refused", False)
    except M.SchemaMismatch:
        chk("a sort with no reason is refused", True)
    # nothing may infer a branch from text
    src = open(os.path.join(HERE, "markers.py"), encoding="utf-8").read()
    body = src.split("def sort_record(")[1].split("\ndef ")[0]
    chk("sort_record takes the branch as an argument",
        "branch=None" in src.split("def sort_record(")[1][:60])
    chk("and does not scan for who-pays language",
        not any(w in body for w in ("liable", "jurisdiction", "budget")
                if w + '"' in body or "'" + w in body))

    # -- 6b. the investigation-sim map
    bm = M.bin_map()
    chk("the bin vocabulary is imported, not retyped",
        "BINS" in bm["source"] and "imported" in bm["source"])
    chk("and it is whatever that module currently declares",
        bm["bin_vocabulary"] == list(M._bins().BINS))
    chk("three states map to a bin", len(bm["states_with_a_bin"]) == 3)
    chk("two do not", len(bm["states_with_none"]) == 2)
    chk("three bins have no state here",
        len(bm["bins_with_none"]) == 3)
    chk("unasked now maps, and it did not when GM_005 was written",
        bm["states"]["unasked"]["bin"] == "HELD_BUT_UNASKED")
    chk("the row records that it had no bin",
        "had NO bin" in bm["states"]["unasked"]["why"])
    chk("and names the other module's claim",
        "IS_014" in bm["states"]["unasked"]["why"])
    chk("the map is not onto in either direction",
        bm["states_with_none"] and bm["bins_with_none"])
    chk("every mapping carries a reason",
        all(v["why"] for v in bm["states"].values()))
    chk("the unmapped states are the two that sit off the axis",
        set(bm["states_with_none"]) == {"uncounted", "assembly"})
    chk("and NOT_FORESEEN is one of the unmapped bins",
        "NOT_FORESEEN" in bm["bins_with_none"])
    # a mapping naming a bin the other module does not have must refuse
    saved = M.STATE_TO_BIN["undated"]
    try:
        M.STATE_TO_BIN["undated"] = ("NOT_A_BIN", "x")
        try:
            M.bin_map()
            chk("a mapping to a non-bin is refused", False)
        except M.SchemaMismatch:
            chk("a mapping to a non-bin is refused", True)
    finally:
        M.STATE_TO_BIN["undated"] = saved
    chk("and the real map passes again",
        M.bin_map()["states"]["undated"]["bin"] == "CALCULATED_UNCLOCKED")

    # -- 7. the index and the corpus
    idx = M.index()
    chk("five index entries", len(idx) == 5)
    chk("each names a gaps/ path",
        all(i["path"].startswith("gaps/") for i in idx))
    chk("none of them is here", not any(i["present"] for i in idx))
    chk("no gaps/ directory was created",
        not os.path.isdir(os.path.join(HERE, "gaps")))
    try:
        M.load_gaps()
        chk("an absent corpus is refused, not returned empty", False)
    except M.CorpusAbsent as e:
        chk("an absent corpus is refused, not returned empty", True)
        chk("and the refusal names the files", "gaps/substrate.md" in str(e))
        chk("and says they are not reconstructed",
            "not reconstructed" in str(e))

    # -- 8. four standing cautions, read from the file
    cs = M.cautions()
    chk("four standing cautions", len(cs) == 4)
    chk("the first is the uncounted-population one",
        "unbounded in both directions" in cs[0])
    chk("the last is the no-residue one", "no residue" in cs[-1].lower())

    # -- 9. the report
    out = M.render()
    chk("the report names every state", all(s in out for s in M.STATES))
    chk("it shows the corpus refusal rather than describing it",
        "load_gaps() raises" in out)
    chk("it says the gaps files are not reconstructed",
        "not reconstructed" in out)
    chk("it names the KIND-is-forced result",
        "free on 1 of 5" in out)

    # -- 10. the screen
    sys.path.insert(0, os.path.join(M.ROOT, "sheet-structure-scan"))
    import no_severity  # noqa: E402
    chk("the report carries no severity language",
        not no_severity.hits(out))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(out + "\nthis schema is broken\n")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b in bad:
        print("  FAILED", b)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
