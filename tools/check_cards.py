#!/usr/bin/env python3
"""check_cards.py -- checks tools/TOOL_CARDS.json and renders TOOL_CARDS.md.

CC0. Co-authored. Stdlib only, parses under 3.8, no network.

  python3 tools/check_cards.py              check; exit 0 no card VOID, 1 a card is VOID, 2 cannot run
  python3 tools/check_cards.py --write      also regenerate tools/TOOL_CARDS.md
  python3 tools/check_cards.py --find TEXT  the card ids whose aliases (or id) match TEXT
  python3 tools/check_cards.py --selftest   plants one defect per rule, each must fire
  python3 tools/check_cards.py --json       machine-readable result

TOOL_CARDS is a map. The code stays in the repository it was built in; a row
says where, pinned to a MERGED commit and the sha256 of the file at that
commit. Sibling checkouts are looked for at ../<dir>; override with
CARDS_<REPO>_PATH (e.g. CARDS_FORMULA_AUDIT_PATH).

Per row, by location state:
  PINNED         the commit and path resolve in a checkout and the sha256
                 matches -> OK. A mismatch, or a path that is not in that
                 commit -> the card is VOID.
  CARD_TEXT      as PINNED; the pinned file is card text, not code.
  PENDING_MERGE  allowed only with a PR number; without one -> VOID. Its
                 sha256 is the file on the unmerged branch: compared when the
                 branch commit is in a checkout, never counted as pinned.
  VOID           a declared gap (not built, or text in no repository): kept,
                 reported, and not a failure of the index. It must say why.

Per cell: every text cell of a row (trigger, inputs, output, fails_when,
measures, fits, breaks_when, warning_sign) names its source in `cell_source`:
  VERBATIM        a literal substring of the pinned text, byte for byte.
  WRAP_COLLAPSED  a substring once runs of whitespace (the card's line wraps)
                  are collapsed to one space on both sides.
  INDEX_WRITTEN   written for this index; matched against nothing, and flagged
                  in the rendered .md.
  VOID            the source carries no such field; the cell reads "VOID: ..."
                  and is kept as a gap, never filled in.
A VERBATIM or WRAP_COLLAPSED claim that does not hold against the pinned text
voids the row. A cell with no source, an unknown source, or a "VOID: ..." text
whose source is not VOID (or the reverse) voids the row.
A WRAP_COLLAPSED cell that is in fact a literal match is reported as
UPGRADE_AVAILABLE: a warning, the row stays OK and the exit code does not
change. The cell is relabelled VERBATIM by hand.

NOT_CHECKED is not OK. When the repository or the commit is not available
here, the row reads NOT_CHECKED and is counted apart; nothing is assumed to
match. Structural rules (fields present, ids unique, aliases resolve, a
PENDING_MERGE row has a PR number) are checked everywhere.

Status: PROPOSED, OBSERVED, DERIVED, or DERIVED with its basis named,
"DERIVED (basis: OBSERVED)" or "DERIVED (basis: PROPOSED)". Any other basis,
and any other status, voids the card. A gate state ("gate run, thresholds not
set") is not a status: it is carried in breaks_when and not_built.

pairs_with (optional): a list of {"id", "reason"} naming a card this one is
used with. The id must be a card, the reason must be stated, and the other
card must name this one back; a one-way or dangling pair voids the card.

Aliases: every card has at least one, an alias names exactly one card, and
--find resolves them. A row with a `finder` name must have that entry in
TOOL_FINDER/finder.json: the card points at the existing entry and does not
copy it.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CARDS = os.path.join(HERE, "TOOL_CARDS.json")
MD = os.path.join(HERE, "TOOL_CARDS.md")
FINDER = os.path.join(ROOT, "TOOL_FINDER", "finder.json")
DIRS = {"Simulators": None, "formula-audit": "formula-audit",
        "Geometric-to-Binary-Computational-Bridge": "geometric-to-binary-computational-bridge"}
FIELDS = ("id", "trigger", "inputs", "output", "fails_when", "status", "location",
          "measures", "fits", "breaks_when", "warning_sign")
EXTRA = ("kind", "cell_source", "aliases", "finder", "not_built", "evidence")
STATES = ("PINNED", "PENDING_MERGE", "CARD_TEXT", "VOID")
STATUS = ("PROPOSED", "OBSERVED", "DERIVED", "DERIVED (basis: OBSERVED)",
          "DERIVED (basis: PROPOSED)")
CELLS = ("trigger", "inputs", "output", "fails_when", "measures", "fits", "breaks_when",
         "warning_sign")
SOURCES = ("VERBATIM", "WRAP_COLLAPSED", "INDEX_WRITTEN", "VOID")
QUOTED = ("VERBATIM", "WRAP_COLLAPSED")


def repo_dir(repo):
    if repo == "Simulators":
        return ROOT
    if repo not in DIRS:
        return None
    env = os.environ.get("CARDS_%s_PATH" % repo.upper().replace("-", "_"))
    cand = env or os.path.join(os.path.dirname(ROOT), DIRS[repo])
    return cand if os.path.isdir(cand) else None


def blob(repo, commit, path):
    """(state, bytes): FOUND, NO_REPO, NO_COMMIT (not in this checkout) or NO_PATH."""
    d = repo_dir(repo)
    if d is None:
        return "NO_REPO", None
    have = subprocess.run(["git", "-C", d, "cat-file", "-e", "%s^{commit}" % commit],
                          capture_output=True)
    if have.returncode:
        return "NO_COMMIT", None
    p = subprocess.run(["git", "-C", d, "show", "%s:%s" % (commit, path)], capture_output=True)
    if p.returncode:
        return "NO_PATH", None
    return "FOUND", p.stdout


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def check_row(row, finder_names):
    """One row -> {id, state, verdict, why}. verdict: OK | NOT_CHECKED | PENDING | DECLARED_VOID | VOID."""
    out = {"id": row.get("id"), "state": None, "verdict": "VOID", "why": None, "warn": []}
    missing = [f for f in FIELDS + EXTRA if f not in row]
    if missing:
        out["why"] = "missing field: " + ", ".join(missing)
        return out
    blank = [f for f in FIELDS if f != "location" and not (isinstance(row[f], str) and row[f].strip())]
    if blank:
        out["why"] = "empty field: " + ", ".join(blank)
        return out
    if row["status"] not in STATUS:
        out["why"] = "status %r is not one of %s" % (row["status"], ", ".join(STATUS))
        return out
    if not row["aliases"] or not all(isinstance(a, str) and a.strip() for a in row["aliases"]):
        out["why"] = "no alias"
        return out
    if row["finder"] is not None and finder_names is not None and row["finder"] not in finder_names:
        out["why"] = "finder entry %r is not in TOOL_FINDER/finder.json" % row["finder"]
        return out
    src = row["cell_source"]
    if not isinstance(src, dict) or sorted(src) != sorted(CELLS):
        out["why"] = "cell_source must name exactly: " + ", ".join(CELLS)
        return out
    bad = [f for f in CELLS if src[f] not in SOURCES]
    if bad:
        out["why"] = "cell source is not one of %s: %s" % (", ".join(SOURCES), ", ".join(bad))
        return out
    bad = [f for f in CELLS if (src[f] == "VOID") != row[f].startswith("VOID:")]
    if bad:
        out["why"] = "a VOID cell reads \"VOID: ...\" and nothing else does: " + ", ".join(bad)
        return out
    loc = row["location"]
    state = loc.get("state") if isinstance(loc, dict) else None
    out["state"] = state
    if state not in STATES:
        out["why"] = "location state %r is not one of %s" % (state, ", ".join(STATES))
        return out
    if state == "VOID":
        if not loc.get("reason"):
            out["why"] = "a VOID location must say why"
            return out
        quoted = [f for f in CELLS if src[f] in QUOTED]
        if quoted:
            out["why"] = "a quoted cell with no pinned text to quote: " + ", ".join(quoted)
            return out
        out.update(verdict="DECLARED_VOID", why=loc["reason"])
        return out
    if not (isinstance(loc.get("sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", loc["sha256"])
            and loc.get("repo") and loc.get("path")):
        out["why"] = "location needs repo, path and a full sha256"
        return out
    if state == "PENDING_MERGE":
        quoted = [f for f in CELLS if src[f] in QUOTED]
        if quoted:
            out["why"] = "a quoted cell on an unmerged branch (no pinned text): " + ", ".join(quoted)
            return out
        if not (isinstance(loc.get("pr"), int) and not isinstance(loc["pr"], bool) and loc["pr"] > 0):
            out["why"] = "PENDING_MERGE without a PR number"
            return out
        if loc.get("commit"):
            out["why"] = "PENDING_MERGE with a pinned commit: re-pin it as PINNED or drop the commit"
            return out
        st, data = blob(loc["repo"], loc.get("branch_commit") or "", loc["path"])
        if st == "FOUND" and hashlib.sha256(data).hexdigest() != loc["sha256"]:
            out["why"] = "sha256 does not match the file on the unmerged branch"
            return out
        out.update(verdict="PENDING", why="PR %d, not merged; %s" % (
            loc["pr"], "branch file matches" if st == "FOUND" else "branch not in a checkout here"))
        return out
    if not (isinstance(loc.get("commit"), str) and re.fullmatch(r"[0-9a-f]{40}", loc["commit"])):
        out["why"] = "a pinned location needs a full commit id"
        return out
    st, data = blob(loc["repo"], loc["commit"], loc["path"])
    if st in ("NO_REPO", "NO_COMMIT"):
        out.update(verdict="NOT_CHECKED", why="%s: %s is not available here" % (
            st, loc["repo"] if st == "NO_REPO" else loc["commit"][:12]))
        return out
    if st == "NO_PATH":
        out["why"] = "%s is not in %s at %s" % (loc["path"], loc["repo"], loc["commit"][:12])
        return out
    if hashlib.sha256(data).hexdigest() != loc["sha256"]:
        out["why"] = "sha256 mismatch for %s at %s" % (loc["path"], loc["commit"][:12])
        return out
    raw = data.decode("utf-8", "replace")
    text = norm(raw)
    # INDEX_WRITTEN and VOID cells are not looked for; a quoted cell must be there
    bad = ["%s (%s)" % (f, src[f]) for f in CELLS
           if (src[f] == "VERBATIM" and row[f] not in raw)
           or (src[f] == "WRAP_COLLAPSED" and norm(row[f]) not in text)]
    if bad:
        out["why"] = "claimed as quoted, not in the pinned text: " + ", ".join(bad)
        return out
    out["warn"] = ["UPGRADE_AVAILABLE: %s is a literal match, labelled WRAP_COLLAPSED" % f
                   for f in CELLS if src[f] == "WRAP_COLLAPSED" and row[f] in raw]
    out.update(verdict="OK", why="%s at %s" % (loc["path"], loc["commit"][:12]))
    return out


def alias_table(rows):
    """{alias (lower): [ids]} over aliases and ids."""
    table = {}
    for r in rows:
        for a in list(r.get("aliases") or []) + [r.get("id") or ""]:
            table.setdefault(norm(a).lower(), []).append(r.get("id"))
    return table


def find(rows, text):
    q = norm(text).lower()
    hits = []
    for r in rows:
        names = [r["id"]] + list(r["aliases"])
        if any(q in norm(n).lower() for n in names):
            hits.append(r["id"])
    return hits


def finder_names():
    try:
        return {e["name"] for e in json.load(open(FINDER, encoding="utf-8"))["entries"]}
    except (OSError, ValueError, KeyError):
        return None


def check(doc):
    rows = doc.get("rows") if isinstance(doc, dict) else None
    if not isinstance(rows, list) or not rows:
        raise ValueError("no rows")
    names = finder_names()
    results = [check_row(r, names) for r in rows]
    ids = [r.get("id") for r in rows]
    for res in results:
        if ids.count(res["id"]) > 1 and res["verdict"] != "VOID":
            res.update(verdict="VOID", why="id %r is used by more than one row" % res["id"])
    shared = {a: sorted(set(v)) for a, v in alias_table(rows).items() if len(set(v)) > 1}
    for res in results:
        mine = [a for a, v in shared.items() if res["id"] in v]
        if mine and res["verdict"] != "VOID":
            res.update(verdict="VOID", why="alias %r names more than one card" % mine[0])
    pairs = {r.get("id"): r.get("pairs_with") for r in rows if "pairs_with" in r}
    for res in results:
        if res["id"] not in pairs or res["verdict"] == "VOID":
            continue
        why = pair_fault(res["id"], pairs, ids)
        if why:
            res.update(verdict="VOID", why=why)
    counts = {}
    for res in results:
        counts[res["verdict"]] = counts.get(res["verdict"], 0) + 1
    return {"rows": len(rows), "counts": counts, "results": results,
            "finder_read": names is not None,
            "warnings": [(r["id"], w) for r in results for w in r["warn"]],
            "void": [r["id"] for r in results if r["verdict"] == "VOID"]}


def pair_fault(rid, pairs, ids):
    """None, or why this card's pairs_with does not hold."""
    mine = pairs[rid]
    if not isinstance(mine, list) or not mine:
        return "pairs_with must be a non-empty list of {id, reason}"
    for p in mine:
        if not (isinstance(p, dict) and isinstance(p.get("id"), str)
                and isinstance(p.get("reason"), str) and p["reason"].strip()):
            return "a pairs_with entry needs an id and a stated reason"
        if p["id"] == rid or p["id"] not in ids:
            return "pairs_with names %r, which is not another card" % p["id"]
        back = pairs.get(p["id"])
        if not (isinstance(back, list) and any(isinstance(b, dict) and b.get("id") == rid
                                               for b in back)):
            return "pairs_with %r is one-way: that card does not name this one" % p["id"]
    return None


def cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def where(loc):
    st = loc["state"]
    if st == "VOID":
        return "VOID: " + loc["reason"]
    tail = "`%s:%s`" % (loc["repo"], loc["path"]) + (loc.get("anchor") or "")
    if st == "PENDING_MERGE":
        return "PENDING_MERGE (PR %d) %s sha256 `%s`" % (loc["pr"], tail, loc["sha256"][:12])
    return "%s @ `%s` sha256 `%s`%s" % (tail, loc["commit"][:7], loc["sha256"][:12],
                                         " (card text only; no code)" if st == "CARD_TEXT" else "")


def render(doc):
    L = ["# TOOL_CARDS", "",
         "Generated from `TOOL_CARDS.json` by `check_cards.py --write`. Edit the JSON, not this file.",
         "CC0. Co-authored. Status of every row: PROPOSED unless it says otherwise.", "",
         "A map, not a move: the code stays in the repository it was built in. Each row is pinned to a",
         "merged commit and the sha256 of the file there. A row on an unmerged branch reads PENDING_MERGE",
         "with its PR number and is re-pinned when the PR merges. `python3 tools/check_cards.py` checks",
         "every location it can reach and says NOT_CHECKED, never OK, for one it cannot.", "",
         "Find a card by a phrase: `python3 tools/check_cards.py --find \"moving goalposts\"`.",
         "For tools by need and symptom see `TOOL_FINDER/TOOL_FINDER.md`; a card with a `finder` name",
         "points at its entry there.", "",
         "Every text cell names its source. A cell marked `[iw]` in the index (INDEX_WRITTEN below) was",
         "written for this index: a summary, not a quote, matched against nothing. VERBATIM and",
         "WRAP_COLLAPSED cells are checked against the pinned text (WRAP_COLLAPSED after the card's line",
         "wraps are collapsed to one space). A VOID cell is a field the source does not carry.", "",
         "## Index", "",
         "| id | trigger | inputs | output | fails when | status | location + sha |",
         "|---|---|---|---|---|---|---|"]
    for r in doc["rows"]:
        src = r["cell_source"]

        def marked(f):
            return r[f] + (" [iw]" if src[f] == "INDEX_WRITTEN" else "")
        L.append("| %s |" % " | ".join(cell(x) for x in (
            r["id"], marked("trigger"), marked("inputs"), marked("output"), marked("fails_when"),
            r["status"], where(r["location"]))))
    L += ["", "## Cards", ""]
    for r in doc["rows"]:
        L += ["### %s" % r["id"], "",
              "- kind: %s" % r["kind"],
              "- measures [%s]: %s" % (r["cell_source"]["measures"], r["measures"]),
              "- fits [%s]: %s" % (r["cell_source"]["fits"], r["fits"]),
              "- breaks when [%s]: %s" % (r["cell_source"]["breaks_when"], r["breaks_when"]),
              "- warning sign [%s]: %s" % (r["cell_source"]["warning_sign"], r["warning_sign"]),
              "- index cells: %s" % "; ".join("%s %s" % (f, r["cell_source"][f]) for f in CELLS[:4]),
              "- aliases: %s" % "; ".join(r["aliases"]),
              "- finder: %s" % (r["finder"] or "none")]
        for n in r["not_built"]:
            L.append("- not built: %s" % n)
        for p in r.get("pairs_with") or []:
            L.append("- pairs with: %s (%s)" % (p["id"], p["reason"]))
        for e in r["evidence"]:
            L.append("- evidence: %s `%s:%s` %s (PR %s)" % (
                e["state"], e["repo"], e["path"], ", ".join(e["ids"]), e.get("pr")))
        L.append("")
    return "\n".join(L)


def selftest():
    import copy
    doc = json.load(open(CARDS, encoding="utf-8"))
    names = finder_names()
    by = {r["id"]: r for r in doc["rows"]}
    ok = tot = 0

    def expect(label, got, want):
        nonlocal ok, tot
        tot += 1
        good = got == want
        ok += good
        print(("PASS  " if good else "FAIL  ") + label + ("" if good else "   got %r" % (got,)))

    def verdict(row):
        return check_row(row, names)["verdict"]

    def bent(card_id, change):
        row = copy.deepcopy(by[card_id])
        change(row)
        return row

    pinned = "source_swap"                       # a Simulators row: its commit is checked when present
    base = verdict(by[pinned])
    expect("a pinned card text row checks or says NOT_CHECKED", base in ("OK", "NOT_CHECKED"), True)
    if base == "OK":
        expect("a wrong sha256 voids the card",
               verdict(bent(pinned, lambda r: r["location"].update(sha256="0" * 64))), "VOID")
        expect("a path that is not in the commit voids the card",
               verdict(bent(pinned, lambda r: r["location"].update(path="reasoning-toolkit/NOPE.md"))),
               "VOID")
        expect("a VERBATIM cell that is not in the card text voids the row",
               verdict(bent(pinned, lambda r: r.update(measures="something the card does not say"))),
               "VOID")
        expect("a paraphrase claimed VERBATIM voids the row",
               verdict(bent(pinned, lambda r: r.update(
                   warning_sign="the same reasoning seen as insight from one author"))), "VOID")

        def set_cell(f, text, source):
            def change(r):
                r[f] = text
                r["cell_source"][f] = source
            return change
        expect("a field declared VOID is kept as a gap, not looked for",
               verdict(bent(pinned, set_cell("fits", "VOID: the card carries no such field", "VOID"))),
               "OK")
        expect("an INDEX_WRITTEN cell is exempt from matching",
               verdict(bent(pinned, set_cell("measures", "a summary the card does not say",
                                             "INDEX_WRITTEN"))), "OK")
        wrapped = "gate_regeneration"            # carries WRAP_COLLAPSED cells
        f = [c for c in CELLS if by[wrapped]["cell_source"][c] == "WRAP_COLLAPSED"][0]
        expect("a WRAP_COLLAPSED cell matches once the wraps are collapsed", verdict(by[wrapped]), "OK")
        up = check_row(bent(pinned, lambda r: r["cell_source"].update(measures="WRAP_COLLAPSED")),
                       names)
        expect("a literal match labelled WRAP_COLLAPSED is a warning, the row stays OK",
               (up["verdict"], up["warn"]),
               ("OK", ["UPGRADE_AVAILABLE: measures is a literal match, labelled WRAP_COLLAPSED"]))
        expect("the shipped index has no UPGRADE_AVAILABLE warning", check(doc)["warnings"], [])
        expect("the same cell claimed VERBATIM voids the row",
               verdict(bent(wrapped, lambda r: r["cell_source"].update({f: "VERBATIM"}))), "VOID")
        expect("a WRAP_COLLAPSED cell that is not in the card text voids the row",
               verdict(bent(wrapped, lambda r: r.update({f: "something the card does not say"}))),
               "VOID")
    expect("VOID text under a source that is not VOID voids the row",
           verdict(bent(pinned, lambda r: r.update(fits="VOID: the card carries no such field"))),
           "VOID")
    expect("a VOID source on a cell that has text voids the row",
           verdict(bent(pinned, lambda r: r["cell_source"].update(fits="VOID"))), "VOID")
    expect("an unknown cell source voids the row",
           verdict(bent(pinned, lambda r: r["cell_source"].update(fits="QUOTED"))), "VOID")
    expect("a cell with no source voids the row",
           verdict(bent(pinned, lambda r: r["cell_source"].pop("trigger"))), "VOID")
    expect("a row with no cell_source voids", verdict(bent(pinned, lambda r: r.pop("cell_source"))),
           "VOID")
    expect("row-level fields_source is gone from every row",
           [r["id"] for r in doc["rows"] if "fields_source" in r], [])
    expect("every reasoning card: inputs and output VOID, trigger INDEX_WRITTEN",
           [r["id"] for r in doc["rows"] if r["kind"] == "reasoning_card" and
            (r["cell_source"]["inputs"], r["cell_source"]["output"], r["cell_source"]["trigger"])
            != ("VOID", "VOID", "INDEX_WRITTEN")], [])
    expect("every code-tool row: no cell is VOID, and a quoted cell is checked like any other",
           [r["id"] for r in doc["rows"] if r["kind"] == "tool" and
            "VOID" in r["cell_source"].values()], [])
    expect("the rendered .md flags an INDEX_WRITTEN cell and no other",
           (by["frame_edge"]["trigger"] + " [iw] |" in render(doc),
            by[pinned]["fails_when"] + " [iw]" in render(doc)), (True, False))
    expect("an unavailable commit is NOT_CHECKED, never OK",
           verdict(bent(pinned, lambda r: r["location"].update(commit="f" * 40))), "NOT_CHECKED")
    expect("a short commit id is refused",
           verdict(bent(pinned, lambda r: r["location"].update(commit="2d902a1"))), "VOID")
    # a constructed PENDING_MERGE row: the live index may hold none once its PRs merge
    pend = "_selftest_pending"
    by[pend] = copy.deepcopy(by["exact_tier"])
    by[pend]["id"] = pend
    by[pend]["location"] = {"repo": by["exact_tier"]["location"]["repo"],
                            "state": "PENDING_MERGE", "pr": 1, "branch": "a-branch",
                            "branch_commit": None, "commit": None,
                            "path": by["exact_tier"]["location"]["path"], "sha256": "0" * 64}
    expect("a PENDING_MERGE row with its PR number is PENDING", verdict(by[pend]), "PENDING")
    expect("PENDING_MERGE without a PR number voids the card",
           verdict(bent(pend, lambda r: r["location"].pop("pr"))), "VOID")
    expect("PENDING_MERGE cannot also claim a pinned commit",
           verdict(bent(pend, lambda r: r["location"].update(commit="a" * 40))), "VOID")
    # a constructed declared gap: the live index may hold none once every tool is built
    gap = "_selftest_gap"
    by[gap] = copy.deepcopy(by["exact_tier"])
    by[gap]["id"] = gap
    by[gap]["location"] = {"repo": None, "state": "VOID", "path": None, "commit": None,
                           "sha256": None, "reason": "not built"}
    expect("a declared gap is DECLARED_VOID, not a failure", verdict(by[gap]), "DECLARED_VOID")
    expect("a quoted cell on a row with no pinned text voids the row",
           verdict(bent(gap, lambda r: r["cell_source"].update(measures="VERBATIM"))), "VOID")
    expect("a VOID location must say why",
           verdict(bent(gap, lambda r: r["location"].pop("reason"))), "VOID")
    expect("a missing field voids the card",
           verdict(bent(pend, lambda r: r.pop("warning_sign"))), "VOID")
    expect("an empty field voids the card", verdict(bent(pend, lambda r: r.update(fits=" "))), "VOID")
    expect("a card with no alias voids", verdict(bent(pend, lambda r: r.update(aliases=[]))), "VOID")
    expect("an unknown status voids", verdict(bent(pend, lambda r: r.update(status="VALIDATED"))),
           "VOID")
    expect("status DERIVED is accepted", verdict(bent(pend, lambda r: r.update(status="DERIVED"))),
           "PENDING")
    expect("status DERIVED with a named basis is accepted",
           [verdict(bent(pend, lambda r, b=b: r.update(status="DERIVED (basis: %s)" % b)))
            for b in ("OBSERVED", "PROPOSED")], ["PENDING", "PENDING"])
    expect("DERIVED with any other basis voids",
           [verdict(bent(pend, lambda r, s=s: r.update(status=s)))
            for s in ("DERIVED (basis: VALIDATED)", "DERIVED (basis: )", "DERIVED (OBSERVED)")],
           ["VOID", "VOID", "VOID"])
    one_way = copy.deepcopy(doc)
    one_way["rows"][0]["pairs_with"] = [{"id": one_way["rows"][1]["id"], "reason": "planted"}]
    one_way["rows"][1].pop("pairs_with", None)
    expect("a one-way pairs_with voids the card",
           one_way["rows"][0]["id"] in check(one_way)["void"], True)
    dangling = copy.deepcopy(doc)
    dangling["rows"][0]["pairs_with"] = [{"id": "card-not-there", "reason": "planted"}]
    expect("pairs_with naming no card voids the card",
           dangling["rows"][0]["id"] in check(dangling)["void"], True)
    if names is not None:
        expect("a finder name with no entry voids the card",
               verdict(bent(pinned, lambda r: r.update(finder="card-not-there"))), "VOID")
    twin = copy.deepcopy(doc)
    twin["rows"][0]["aliases"].append(twin["rows"][1]["aliases"][0])
    expect("an alias naming two cards voids both",
           sorted(check(twin)["void"]) == sorted([twin["rows"][0]["id"], twin["rows"][1]["id"]]), True)
    dup = copy.deepcopy(doc)
    dup["rows"].append(copy.deepcopy(dup["rows"][0]))
    expect("a duplicate id is caught", dup["rows"][0]["id"] in check(dup)["void"], True)
    expect("every card id resolves from each of its aliases",
           all(r["id"] in find(doc["rows"], a) for r in doc["rows"] for a in r["aliases"]), True)
    expect("--find on a phrase", find(doc["rows"], "moving goalposts"), ["gate_regeneration"])
    real = check(doc)
    expect("the shipped index has no VOID card", real["void"], [])
    expect("TOOL_CARDS.md is what --write renders",
           open(MD, encoding="utf-8").read() == render(doc) + "\n", True)
    print("checks: %d   failed: %d" % (tot, tot - ok))
    return 0 if ok == tot else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    try:
        doc = json.load(open(CARDS, encoding="utf-8"))
        res = check(doc)
    except (OSError, ValueError) as exc:
        print("cannot run: %s" % exc, file=sys.stderr)
        return 2
    if "--find" in argv:
        hits = find(doc["rows"], argv[argv.index("--find") + 1])
        print("\n".join(hits) if hits else "NO_CARD")
        return 0 if hits else 1
    if "--write" in argv:
        open(MD, "w", encoding="utf-8").write(render(doc) + "\n")
    if "--json" in argv:
        print(json.dumps(res, indent=1))
    else:
        for r in res["results"]:
            print("%-13s %-26s %s" % (r["verdict"], r["id"], r["why"]))
        for rid, w in res["warnings"]:
            print("WARNING       %-26s %s" % (rid, w))
        print("rows %d: %s" % (res["rows"], ", ".join("%s %d" % kv for kv in sorted(res["counts"].items()))))
        print("warnings: %d" % len(res["warnings"]))
        if not res["finder_read"]:
            print("NOTE: TOOL_FINDER/finder.json was not read; finder names NOT_CHECKED")
    return 1 if res["void"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
