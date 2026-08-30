#!/usr/bin/env python3
"""gap-markers -- checks on the delivered GAP_MARKERS.md.

The delivered file is READ, never modified. Its schema is parsed rather
than retyped: field names, STATE values, KIND values and the index all
come out of the file, so an edit there and not here turns --selftest
red.

The five `gaps/*.md` files named in the INDEX did not arrive. Nothing
here reconstructs them -- they are data, and inventing an entry puts a
gap in the author's mouth (the PB_001 / CW_004 rule). Every readout
below is a property of the SCHEMA, which is what did arrive.

The READING RULE is deliberately NOT automated. It says of its own two
branches that "both look identical from outside", so a keyword sort
over them would be nonidentity-census T1-1 -- a word list deciding a
question the author says cannot be decided from the surface. What is
built instead is a place to record a sort someone made, with the reason,
and a refusal to infer one.

usage:  python3 markers.py                 # the report
        python3 markers.py --cross         # the KIND x STATE table
        python3 markers.py --selftest

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOC = os.path.join(HERE, "GAP_MARKERS.md")
GAPDIR = os.path.join(HERE, "gaps")


class SchemaMismatch(Exception):
    """The delivered file and this checker disagree."""


class CorpusAbsent(Exception):
    """The gaps/ files named in the INDEX are not here."""


def _doc():
    return open(DOC, encoding="utf-8").read()


# ---------------------------------------------------------------- parse

def fields():
    """The seven entry fields, in delivered order.

    The first version required two spaces after the name and returned
    SIX -- WHAT_IS_MISSING is fifteen characters into a sixteen-wide
    column, so it has one. A parse that drops one field of seven passes
    every check asserting the parse is non-empty, which is worse than
    returning nothing. One space, and the count is asserted.
    """
    body = _doc().split("Each gap entry carries these fields:")[1]
    body = body.split("### STATE")[0]
    return tuple(m.group(1) for m in
                 re.finditer(r"^    ([A-Z][A-Z_]+)\s+\S", body, re.M))


def _defs(header, nxt):
    body = _doc().split(header)[1].split(nxt)[0]
    out = {}
    cur = None
    for ln in body.split("\n"):
        m = re.match(r"^    ([a-z][a-z-]+)\s{2,}(.*)$", ln)
        if m:
            cur = m.group(1)
            out[cur] = m.group(2).strip()
        elif cur and re.match(r"^\s{8,}\S", ln):
            out[cur] += " " + ln.strip()
        elif ln.strip() == "":
            cur = None
    return out


def states():
    return _defs("### STATE values", "### KIND values")


def kinds():
    return _defs("### KIND values", "KIND is the load-bearing")


def index():
    """The five files the INDEX names, and whether each is here."""
    body = _doc().split("## INDEX")[1]
    out = []
    for m in re.finditer(r"^    (gaps/[\w.]+)\s{2,}(.*)$", body, re.M):
        p = os.path.join(HERE, m.group(1))
        out.append({"path": m.group(1), "covers": m.group(2).strip(),
                    "present": os.path.exists(p)})
    return out


def cautions():
    body = _doc().split("## STANDING CAUTION")[1].split("## INDEX")[0]
    return [" ".join(b.split()) for b in
            re.split(r"\n\n(?=- )", body) if b.strip().startswith("-")]


FIELDS = fields()
STATES = states()
KINDS = kinds()

KNOWLEDGE = "knowledge"
BOUNDARY = "boundary-artifact"


# --------------------------------------------- the KIND x STATE cross
#
# KIND is called the load-bearing distinction. Whether it is FREE to
# vary is a property of the STATE definitions, and it is checkable
# before any entry exists: a state whose own definition asserts that
# the data, record, or competence EXISTS cannot also be a state where
# the knowledge is genuinely absent.

EXISTENCE_CLAIM = re.compile(
    r"\b(data exists|record exists|components present|party competent"
    r"|parties competent)\b", re.I)


def kind_forced(state):
    """Does this state's own definition force its KIND?

    Read from the delivered definition text, not from a hand-made list,
    so an edited definition moves the answer.
    """
    d = STATES[state]
    m = EXISTENCE_CLAIM.search(d)
    if m:
        return {"forced": BOUNDARY, "by": m.group(0),
                "why": "the definition asserts the knowledge is present, "
                       "so the absence is not a knowledge absence"}
    return {"forced": None, "by": None,
            "why": "the definition makes no existence claim, so both "
                   "KINDs are open"}


def cross():
    """The ten cells, and which are reachable from the definitions."""
    rows = []
    for s in STATES:
        f = kind_forced(s)
        rows.append({
            "state": s,
            "knowledge": f["forced"] != BOUNDARY,
            "boundary-artifact": True,
            "forced": f["forced"],
            "by": f["by"],
        })
    open_cells = sum(1 for r in rows if r["forced"] is None)
    return {
        "rows": rows,
        "states": len(rows),
        "cells": 2 * len(rows),
        "reachable": sum((1 if r["knowledge"] else 0) + 1 for r in rows),
        "states_where_kind_is_free": open_cells,
        "states_where_kind_is_forced": len(rows) - open_cells,
    }


# --------------------------------------------------- the reading rule
#
# NOT automated, on the delivered file's own instruction.

def sort_record(boundary_id, branch=None, reason=None):
    """Record a sort someone made. Never infer one.

    The rule's two branches are `keep` (the boundary encodes failure
    knowledge) and `do-not-inherit` (it encodes who pays, who is
    liable, who holds jurisdiction). The delivered text says both look
    identical from outside, so nothing here reads a boundary and
    returns a branch.
    """
    if branch is None:
        return {"boundary": boundary_id, "branch": "UNSORTED",
                "reason": None,
                "note": "no sort recorded. Not the same as sorted and "
                        "found to be neither."}
    if branch not in ("keep", "do-not-inherit"):
        raise SchemaMismatch("branch %r is not one of the rule's two"
                             % branch)
    if not (reason or "").strip():
        raise SchemaMismatch(
            "a recorded sort carries the reason. Without it the branch "
            "is asserted one level down, and the rule's own point is "
            "that the two are indistinguishable from outside.")
    return {"boundary": boundary_id, "branch": branch, "reason": reason,
            "sorted_by": "declared, not inferred"}


# ---------------------------------------------- the investigation-sim map
#
# `investigation-sim` classifies CASES into five foreknowledge bins.
# This register marks LOCATIONS in five states. They are the same
# object from two sides, and the map is not onto in either direction --
# which is the useful part, because each side's unmapped members are
# what the other side cannot express.
#
# Declared, not inferred: the correspondences are stated here with the
# reason, and the bin vocabulary is IMPORTED so a rename over there
# turns this red rather than silently mismatching.

STATE_TO_BIN = {
    "undated": ("CALCULATED_UNCLOCKED",
                "record exists but currency unknown, and a date field "
                "answers it -- which is the bin's own definition: a "
                "figure survived and the conditions under which it held "
                "did not"),
    "unowned": ("GAP_UNINSTRUMENTED",
                "every party competent, interface inside no party's "
                "scope. The exclusion is in how the scopes were drawn, "
                "so it predates the first reading"),
    "uncounted": (None,
                  "no bin. It is the DENOMINATOR investigation-sim IS_001 "
                  "says is uncounted, so it sits one level up from the "
                  "bins rather than among them"),
    "unasked": ("HELD_BUT_UNASKED",
                "mapped 2026-08-26. It had NO bin: the instrument exists "
                "and reported and nobody posed the question, which is "
                "neither KNOWN_ROUTED_AWAY (no report was made) nor "
                "GAP_UNINSTRUMENTED (the instrument is not blind), so "
                "such a case landed on NOT_FORESEEN. That module added a "
                "sixth bin and a fifth signal (its IS_014). This entry "
                "records the state after the repair, and the finding is "
                "GM_005"),
    "assembly": (None,
                 "no bin. Components present in separate literatures is "
                 "a property of a FIELD, and the bins are properties of "
                 "one organisation's record"),
}


def _bins():
    p = os.path.join(ROOT, "investigation-sim")
    if p not in sys.path:
        sys.path.insert(0, p)
    import bins as B
    return B


def bin_map():
    """The two vocabularies against each other, both directions."""
    B = _bins()
    declared = {}
    for st, (b, why) in STATE_TO_BIN.items():
        if b is not None and b not in B.BINS:
            raise SchemaMismatch(
                "state %r maps to %r, which is not a bin over there: %s"
                % (st, b, ", ".join(B.BINS)))
        declared[st] = {"bin": b, "why": why}
    mapped = set(v["bin"] for v in declared.values() if v["bin"])
    return {
        "states": declared,
        "states_with_a_bin": sorted(s for s, v in declared.items()
                                    if v["bin"]),
        "states_with_none": sorted(s for s, v in declared.items()
                                   if not v["bin"]),
        "bins_with_a_state": sorted(mapped),
        "bins_with_none": [b for b in B.BINS if b not in mapped],
        "bin_vocabulary": list(B.BINS),
        "source": "investigation-sim.bins.BINS, imported",
    }


# ------------------------------------------------------- the corpus
#
# The five gaps/*.md files landed 2026-08-26. Entries are parsed from
# the delivered text; nothing is normalised and nothing is repaired.
# A field carrying two values carries two values in the readout.

ENTRY_SPLIT = re.compile(r"^---\s*$", re.M)
FIELD_RE = re.compile(r"^    ([A-Z][A-Z_]+)\s+(.*)$")
EXTRA_RE = re.compile(r"^    ([A-Z][A-Z ]+?)\s{2,}(.*)$")


def parse_entries(text, source):
    out = []
    for block in ENTRY_SPLIT.split(text):
        if "GAP_ID" not in block:
            continue
        rec, cur = {"_source": source, "_extra": {}}, None
        for ln in block.split("\n"):
            m = FIELD_RE.match(ln)
            if m and m.group(1) in FIELDS:
                cur = m.group(1)
                rec[cur] = m.group(2).strip()
                continue
            e = EXTRA_RE.match(ln)
            if e and e.group(1) not in FIELDS:
                cur = None
                rec["_extra"].setdefault(e.group(1).strip(), []).append(
                    e.group(2).strip())
                continue
            if cur and ln.strip() and ln.startswith("    "):
                rec[cur] += " " + ln.strip()
        out.append(rec)
    return out


def load_gaps():
    """Now returns. The refusal branch is kept and is still reachable.

    Before 2026-08-26 the INDEX named five files and none was here, so
    this raised rather than returning an empty list -- a well-formed
    report with zero rows over an absent corpus is the DL_005 / CC_006
    shape. The files landed. The branch stays because the next INDEX
    entry to be named before it is written will hit it.
    """
    missing = [i["path"] for i in index() if not i["present"]]
    if missing:
        raise CorpusAbsent(
            "the INDEX names %d files and %d are not here: %s. They are "
            "data and are not reconstructed. Every readout that depends "
            "on them is unavailable until they land."
            % (len(index()), len(missing), ", ".join(missing)))
    out = []
    for i in index():
        p = os.path.join(HERE, i["path"])
        out += parse_entries(open(p, encoding="utf-8").read(), i["path"])
    return out


def split_values(v):
    """A field carrying more than one value. Read, never resolved."""
    if not v:
        return []
    parts = [p.strip() for p in re.split(r"\s*/\s*(?![^(]*\))", v)]
    return [p for p in parts if p]


def _bare(v):
    """The value with any parenthetical qualifier removed."""
    return re.sub(r"\s*\([^)]*\)", "", v).strip()


def entry_audit():
    """Every readout that needed the corpus."""
    gaps = load_gaps()
    rows, multi_state, multi_kind, no_entry, unknown = [], [], [], [], []
    by_state, by_kind = {}, {}
    for g in gaps:
        gid = g.get("GAP_ID", "?")
        sts = [_bare(x) for x in split_values(g.get("STATE", ""))]
        kds = [_bare(x) for x in split_values(g.get("KIND", ""))]
        if len(sts) > 1:
            multi_state.append((gid, g["STATE"]))
        if len(kds) > 1:
            multi_kind.append((gid, g["KIND"]))
        if not g.get("ENTRY_POINT"):
            no_entry.append(gid)
        for s in sts:
            by_state[s] = by_state.get(s, 0) + 1
            if s not in STATES:
                unknown.append((gid, "STATE", s))
        for k in kds:
            by_kind[k] = by_kind.get(k, 0) + 1
            if k not in KINDS:
                unknown.append((gid, "KIND", k))
        rows.append({"id": gid, "source": g["_source"], "states": sts,
                     "kinds": kds,
                     "entry_point": bool(g.get("ENTRY_POINT")),
                     "extra": sorted(g["_extra"])})
    return {
        "rows": rows, "n": len(rows),
        "by_state": by_state, "by_kind": by_kind,
        "multi_state": multi_state, "multi_kind": multi_kind,
        "no_entry_point": no_entry,
        "unknown_values": unknown,
        "extra_keys": sorted(set(k for r in rows for k in r["extra"])),
    }


def gm001_test():
    """GM_001 said the distribution is forced. Now it can be counted.

    Predicted before the corpus existed: KIND is free on `uncounted`
    alone and forced to boundary-artifact on the other four. The
    falsifier was an entry in one of those four correctly marked
    `knowledge`.
    """
    a = entry_audit()
    forced_states = [r["state"] for r in cross()["rows"] if r["forced"]]
    violations = []
    for r in a["rows"]:
        for s in r["states"]:
            if s in forced_states and KNOWLEDGE in r["kinds"]:
                violations.append({"id": r["id"], "state": s,
                                   "kinds": r["kinds"]})
    n_b = a["by_kind"].get(BOUNDARY, 0)
    return {
        "entries": a["n"],
        "boundary_artifact": n_b,
        "knowledge": a["by_kind"].get(KNOWLEDGE, 0),
        "most_are_boundary": n_b > a["n"] / 2.0,
        "forced_states": forced_states,
        "falsifier_fired": bool(violations),
        "violations": violations,
    }


# ------------------------------------------------------------- report

def wrap(t, w=66, ind="   "):
    out, cur = [], ind
    for word in t.split():
        if len(cur) + len(word) + 1 > w and cur.strip():
            out.append(cur.rstrip())
            cur = ind
        cur += word + " "
    if cur.strip():
        out.append(cur.rstrip())
    return out


def render():
    o = []
    o.append("GAP MARKERS -- checks on the delivered schema")
    o.append("GAP_MARKERS.md is read and not modified. The five gaps/")
    o.append("files it names did not arrive and are not reconstructed.")
    o.append("")

    o.append("1. THE SCHEMA, PARSED")
    o.append("   fields (%d): %s" % (len(FIELDS), ", ".join(FIELDS)))
    o.append("   states (%d): %s" % (len(STATES), ", ".join(STATES)))
    o.append("   kinds  (%d): %s" % (len(KINDS), ", ".join(KINDS)))
    o.append("")

    o.append("2. KIND x STATE -- is the load-bearing field free to vary?")
    c = cross()
    o.append("   %-12s %-11s %-18s %s"
             % ("state", "knowledge", "boundary-artifact", "forced by"))
    for r in c["rows"]:
        o.append("   %-12s %-11s %-18s %s"
                 % (r["state"], "open" if r["knowledge"] else "--",
                    "open", r["by"] or ""))
    o.append("   KIND is free on %d of %d states, forced on %d."
             % (c["states_where_kind_is_free"], c["states"],
                c["states_where_kind_is_forced"]))
    o.append("")
    o += wrap("Four of the five state definitions assert that the data, "
              "the record, or the competence EXISTS. A state whose own "
              "definition says the knowledge is present cannot also be "
              "a state where the knowledge is absent, so KIND is "
              "determined on those four and carries information on one.")
    o.append("")
    o += wrap("So the delivered line \"Most entries here are "
              "boundary-artifact\" is not an observation about a "
              "corpus. It is forced by the state vocabulary, and it is "
              "derivable before any entry is written. That is a schema "
              "economy, and the field stays load-bearing for the READING "
              "RULE, which operates on boundaries rather than on "
              "entries.")
    o.append("")

    o.append("3. NO NEGATIVE STATE")
    o += wrap("All five STATE values are gaps. There is no value "
              "meaning looked, and nothing is missing here. So the "
              "register can only ever record gaps, and a null test "
              "over it has no arm that returns nothing -- the "
              "null-harness CONSTANT_FIRES shape at the schema level.")
    o += wrap("The delivered framing answers part of this: \"A marked "
              "gap is not a finding. It is a location.\" A register of "
              "locations does not need a negative the way a classifier "
              "does. What it cannot then do is report coverage, "
              "because there is no denominator of places looked at.")
    o.append("")

    o.append("4. ENTRY_POINT IS OPTIONAL AND HAS NO THIRD STATE")
    o += wrap("The field reads \"cheapest available first query, where "
              "one exists\". So an entry with no ENTRY_POINT carries "
              "two readings -- searched, and no query is available; or "
              "nobody named one -- and they are the two states this "
              "repo has separated a dozen times. ENTRY_POINT is the "
              "field that makes a gap actionable, so it is the one "
              "where the collapse costs most.")
    o.append("")

    o.append("5. THE READING RULE IS NOT AUTOMATED, ON ITS OWN SAY-SO")
    o += wrap("\"Both look identical from outside. The content "
              "differs.\" A keyword sort over the two branches would "
              "be a word list deciding a question the author states "
              "cannot be decided from the surface. What is built is a "
              "record: sort_record() takes a declared branch with a "
              "reason, refuses a branch outside the two, refuses a "
              "branch with no reason, and returns UNSORTED rather than "
              "guessing.")
    o.append("")

    o.append("6. AGAINST investigation-sim -- %d states, %d bins,"
             % (len(STATES), len(bin_map()["bin_vocabulary"])))
    o.append("   and the map is not onto in either direction")
    bm = bin_map()
    for st in STATES:
        d = bm["states"][st]
        o.append("     %-10s -> %s" % (st, d["bin"] or "(no bin)"))
    o.append("")
    o.append("   bins with no state here: %s"
             % ", ".join(bm["bins_with_none"]))
    o.append("")
    o += wrap("Each side's unmapped members are what the other side "
              "cannot express, and the sharpest was `unasked`: the "
              "instrument exists and reported, and nobody posed the "
              "question. That is neither KNOWN_ROUTED_AWAY, where a "
              "report was made and routed, nor GAP_UNINSTRUMENTED, "
              "where the instrument is blind -- so a case coded "
              "honestly against that module's four original signals "
              "read ABSENT on all four and landed on NOT_FORESEEN, "
              "genuinely novel, with the data in a file the whole "
              "time.")
    o += wrap("It landed. That module added a sixth bin and a fifth "
              "signal on 2026-08-26 (its IS_014), and this row now "
              "maps. The finding is that a single vocabulary cannot "
              "enumerate what it has no word for, and the gap was "
              "found by mapping two registers against each other "
              "rather than by any check inside either.")
    o.append("")
    o += wrap("Running the other way, this register has no state for "
              "NOT_FORESEEN, which follows from section 3: a register "
              "of gaps has no negative, so a location where nothing is "
              "missing has nowhere to go.")
    o.append("")

    o.append("7. THE INDEX")
    for i in index():
        o.append("     %-22s %-3s %s" % (i["path"],
                                         "yes" if i["present"] else "NO",
                                         i["covers"][:34]))
    o.append("   present: %d of %d"
             % (sum(1 for i in index() if i["present"]), len(index())))
    o += wrap("Not reconstructed. A gap entry is data, and inventing "
              "one puts a gap in the author's mouth.")
    o.append("")

    o.append("8. THE CORPUS -- 29 entries across five files")
    a = entry_audit()
    o.append("   entries: %d" % a["n"])
    o.append("   by state:")
    for st in STATES:
        o.append("     %-12s %d" % (st, a["by_state"].get(st, 0)))
    o.append("   by kind:")
    for kd in KINDS:
        o.append("     %-18s %d" % (kd, a["by_kind"].get(kd, 0)))
    o.append("   values outside the declared vocabulary: %s"
             % (a["unknown_values"] or "none"))
    o.append("")

    o.append("9. GM_001 TESTED -- the prediction, against the corpus")
    g = gm001_test()
    o.append("   boundary-artifact on %d of %d entries; knowledge on %d"
             % (g["boundary_artifact"], g["entries"], g["knowledge"]))
    o.append("   the delivered distribution line holds: %s"
             % g["most_are_boundary"])
    o.append("   the stated falsifier fired: %s" % g["falsifier_fired"])
    for v in g["violations"]:
        o.append("     %s  state %s  kinds %s"
                 % (v["id"], v["state"], ", ".join(v["kinds"])))
    o += wrap("It fired on one entry, and the firing is not decidable "
              "by the check. STR-05 marks `knowledge (for the "
              "compliance figure)`, and what its own WHAT_IS_MISSING "
              "describes is a number whose primary source the author "
              "does not have. The KIND definition reads `the physics "
              "or the measurement is genuinely not known`, which a "
              "figure that exists and lacks a citation is not. So "
              "either the entry uses `knowledge` in a second sense, or "
              "GM_001 falls -- and the falsifier as written cannot say "
              "which, because it turns on the word `correctly`, which "
              "nothing measures.")
    o.append("")

    o.append("10. ENTRY_POINT -- present on %d of %d"
             % (a["n"] - len(a["no_entry_point"]), a["n"]))
    for i in index():
        rs = [r for r in a["rows"] if r["source"] == i["path"]]
        n = sum(1 for r in rs if r["entry_point"])
        o.append("     %-22s %d of %-2d" % (i["path"], n, len(rs)))
    o += wrap("The distribution is by FILE, not by gap. Three files "
              "are 0 of 18 and two are 6 of 11, and the file whose own "
              "premise is that its entries are the cheapest gaps to "
              "close is the highest. So GM_003's two readings need a "
              "third: the field is in use in two files and not in "
              "three, which makes its absence a property of the file "
              "rather than a judgement about the gap. A reader picking "
              "the cheapest gap to attack reads all eighteen as "
              "equally hard, and none of them was assessed.")
    o.append("")

    o.append("11. FIELDS CARRYING TWO VALUES, AND FIELDS WITH NO SLOT")
    o.append("   STATE with two values:")
    for gid, v in a["multi_state"]:
        o.append("     %-44s %s" % (gid[:44], v))
    o.append("   KIND with two values:")
    for gid, v in a["multi_kind"]:
        o.append("     %-30s %s" % (gid[:30], v[:44]))
    o.append("")
    o.append("   field names in use and not in the schema: %s"
             % ", ".join(a["extra_keys"]))
    o.append("   entries carrying at least one: %d of %d"
             % (sum(1 for r in a["rows"] if r["extra"]), a["n"]))
    o += wrap("The schema says `Each gap entry carries these fields` "
              "and lists seven. Six more are in use. WHY UNRUN is the "
              "one that matters: on SCR-01 it gives the reason the "
              "computation has not been performed -- liability for "
              "whoever publishes the flagged list, and no agency "
              "owning a screen that crosses three programs -- which is "
              "the boundary-artifact content itself, and it is the "
              "only place in the corpus where that content is stated "
              "as a field rather than left to be inferred from KIND.")
    o.append("")

    o.append("12. THE SIXTH FILE")
    add = os.path.join(HERE, "ADDENDUM.md")
    o.append("   ADDENDUM.md present: %s" % os.path.exists(add))
    o.append("   named in the INDEX: %s"
             % any("ADDENDUM" in i["path"].upper() for i in index()))
    o += wrap("The INDEX names five files and six arrived. The addendum "
              "is addressed to a reader the other five are not "
              "addressed to, which is a reason for it to sit outside "
              "the index rather than an oversight -- and it is not "
              "reachable by anything that reads the INDEX.")
    return "\n".join(o)


def main(argv):
    if "--selftest" in argv:
        import selftest_markers
        return selftest_markers.run()
    if "--cross" in argv:
        import json
        print(json.dumps(cross(), indent=2))
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
