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
    chk("all five landed 2026-08-26", all(i["present"] for i in idx))
    # the refusal branch stays reachable, on a constructed absence
    saved = M.index
    try:
        M.index = lambda: [{"path": "gaps/nothere.md", "covers": "x",
                            "present": False}]
        try:
            M.load_gaps()
            chk("an absent corpus is still refused", False)
        except M.CorpusAbsent as e:
            chk("an absent corpus is still refused", True)
            chk("and the refusal names the file", "nothere" in str(e))
            chk("and says they are not reconstructed",
                "not reconstructed" in str(e))
    finally:
        M.index = saved

    # -- 7b. the corpus
    a = M.entry_audit()
    chk("29 entries parse", a["n"] == 29)
    chk("every entry has an id",
        all(r["id"] and r["id"] != "?" for r in a["rows"]))
    chk("every entry has at least one state and one kind",
        all(r["states"] and r["kinds"] for r in a["rows"]))
    chk("no value falls outside the declared vocabulary",
        a["unknown_values"] == [])
    chk("every declared state is used at least once",
        all(a["by_state"].get(s, 0) > 0 for s in M.STATES))
    chk("unasked is the largest state",
        max(a["by_state"], key=a["by_state"].get) == "unasked")

    # -- 7c. GM_001, now testable
    g = M.gm001_test()
    chk("boundary-artifact is on every entry",
        g["boundary_artifact"] == g["entries"])
    chk("the delivered distribution line holds", g["most_are_boundary"])
    chk("knowledge appears exactly once", g["knowledge"] == 1)
    chk("the stated falsifier fired", g["falsifier_fired"])
    chk("on exactly one entry", len(g["violations"]) == 1)
    chk("and that entry is STR-05",
        g["violations"][0]["id"].startswith("STR-05"))
    chk("its state is one GM_001 called forced",
        g["violations"][0]["state"] in g["forced_states"])
    chk("it carries BOTH kinds, not knowledge alone",
        set(g["violations"][0]["kinds"]) == {M.KNOWLEDGE, M.BOUNDARY})
    chk("the KIND definition names physics or measurement",
        "physics" in M.KINDS[M.KNOWLEDGE]
        and "measurement" in M.KINDS[M.KNOWLEDGE])
    # the check cannot adjudicate, and must not pretend to
    chk("gm001_test reports the firing and no verdict on it",
        "falsifier_fired" in g and "verdict" not in g)

    # -- 7d. ENTRY_POINT, GM_003 with a magnitude
    chk("23 of 29 carry no entry point", len(a["no_entry_point"]) == 23)
    per_file = {}
    for i in idx:
        rs = [r for r in a["rows"] if r["source"] == i["path"]]
        per_file[i["path"]] = (sum(1 for r in rs if r["entry_point"]),
                               len(rs))
    chk("three files are zero of eighteen",
        sum(t for n, t in per_file.values() if n == 0) == 18)
    chk("and two files carry all six",
        sum(n for n, _ in per_file.values()) == 6)
    chk("screens.md is one of the two",
        per_file["gaps/screens.md"][0] > 0)
    chk("screens.md states its entries are the cheapest to close",
        "cheapest gaps to close" in " ".join(
            open(os.path.join(HERE, "gaps", "screens.md"),
                 encoding="utf-8").read().split()))

    # -- 7e. composite fields, GM_010's question answered
    chk("one entry carries two states", len(a["multi_state"]) == 1)
    chk("and it is SCR-03", a["multi_state"][0][0].startswith("SCR-03"))
    chk("one entry carries two kinds", len(a["multi_kind"]) == 1)
    chk("and it is a different entry",
        a["multi_state"][0][0] != a["multi_kind"][0][0])
    chk("split_values reads them and does not resolve them",
        M.split_values("undated / unasked") == ["undated", "unasked"])
    chk("and a parenthetical qualifier does not split",
        len(M.split_values("knowledge (for the compliance figure) / "
                           "boundary-artifact (for the scope)")) == 2)

    # -- 7f. fields in use with no schema slot
    chk("six undeclared field names are in use",
        len(a["extra_keys"]) == 6)
    chk("WHY UNRUN is one", "WHY UNRUN" in a["extra_keys"])
    chk("none of them is a declared field",
        not any(k in M.FIELDS for k in a["extra_keys"]))
    chk("17 of 29 entries carry at least one",
        sum(1 for r in a["rows"] if r["extra"]) == 17)

    # -- 7g. the sixth file
    add = os.path.join(HERE, "ADDENDUM.md")
    chk("the addendum is here", os.path.exists(add))
    chk("and is not named in the INDEX",
        not any("ADDENDUM" in i["path"].upper() for i in idx))
    chk("it addresses a reader the other five do not",
        "Directed at any system" in open(add, encoding="utf-8").read())

    # -- 8. four standing cautions, read from the file
    cs = M.cautions()
    chk("four standing cautions", len(cs) == 4)
    chk("the first is the uncounted-population one",
        "unbounded in both directions" in cs[0])
    chk("the last is the no-residue one", "no residue" in cs[-1].lower())

    # -- 9. the report
    out = M.render()
    chk("the report names every state", all(s in out for s in M.STATES))
    chk("it reports the corpus now that it landed",
        "29 entries across five files" in out)
    chk("and the GM_001 test is shown, not described",
        "the stated falsifier fired: True" in out)
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
