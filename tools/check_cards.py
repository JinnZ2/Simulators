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
  CARD_TEXT      as PINNED, and the four card fields (measures, fits, breaks
                 when, warning sign) are literal substrings of the card text
                 (whitespace-normalised). A field that is not -> VOID. A field
                 the card does not carry is written "VOID: ..." and is kept
                 as a gap, never filled in.
  PENDING_MERGE  allowed only with a PR number; without one -> VOID. Its
                 sha256 is the file on the unmerged branch: compared when the
                 branch commit is in a checkout, never counted as pinned.
  VOID           a declared gap (not built, or text in no repository): kept,
                 reported, and not a failure of the index. It must say why.

NOT_CHECKED is not OK. When the repository or the commit is not available
here, the row reads NOT_CHECKED and is counted apart; nothing is assumed to
match. Structural rules (fields present, ids unique, aliases resolve, a
PENDING_MERGE row has a PR number) are checked everywhere.

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
EXTRA = ("kind", "fields_source", "aliases", "finder", "not_built", "evidence")
STATES = ("PINNED", "PENDING_MERGE", "CARD_TEXT", "VOID")
STATUS = ("PROPOSED", "OBSERVED")
CARD_FIELDS = ("measures", "fits", "breaks_when", "warning_sign")


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
    out = {"id": row.get("id"), "state": None, "verdict": "VOID", "why": None}
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
        out.update(verdict="DECLARED_VOID", why=loc["reason"])
        return out
    if not (isinstance(loc.get("sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", loc["sha256"])
            and loc.get("repo") and loc.get("path")):
        out["why"] = "location needs repo, path and a full sha256"
        return out
    if state == "PENDING_MERGE":
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
    if state == "CARD_TEXT":
        text = norm(data.decode("utf-8", "replace"))
        # a field the card does not carry is declared "VOID: ..." and is not looked for
        bad = [f for f in CARD_FIELDS
               if not row[f].startswith("VOID:") and norm(row[f]) not in text]
        if bad:
            out["why"] = "not a literal substring of the card text: " + ", ".join(bad)
            return out
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
    counts = {}
    for res in results:
        counts[res["verdict"]] = counts.get(res["verdict"], 0) + 1
    return {"rows": len(rows), "counts": counts, "results": results,
            "finder_read": names is not None,
            "void": [r["id"] for r in results if r["verdict"] == "VOID"]}


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
         "## Index", "",
         "| id | trigger | inputs | output | fails when | status | location + sha |",
         "|---|---|---|---|---|---|---|"]
    for r in doc["rows"]:
        L.append("| %s |" % " | ".join(cell(x) for x in (
            r["id"], r["trigger"], r["inputs"], r["output"], r["fails_when"], r["status"],
            where(r["location"]))))
    L += ["", "## Cards", ""]
    for r in doc["rows"]:
        L += ["### %s" % r["id"], "",
              "- kind: %s" % r["kind"],
              "- measures: %s" % r["measures"], "- fits: %s" % r["fits"],
              "- breaks when: %s" % r["breaks_when"], "- warning sign: %s" % r["warning_sign"],
              "- fields: %s" % r["fields_source"],
              "- aliases: %s" % "; ".join(r["aliases"]),
              "- finder: %s" % (r["finder"] or "none")]
        for n in r["not_built"]:
            L.append("- not built: %s" % n)
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
        expect("a card field that is not in the card text voids the card",
               verdict(bent(pinned, lambda r: r.update(measures="something the card does not say"))),
               "VOID")
    if base == "OK":
        expect("a field declared VOID is kept as a gap, not looked for",
               verdict(bent(pinned, lambda r: r.update(fits="VOID: the card carries no such field"))),
               "OK")
        expect("a paraphrase of a card field voids the card",
               verdict(bent(pinned, lambda r: r.update(
                   warning_sign="the same reasoning seen as insight from one author"))), "VOID")
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
    expect("a declared gap is DECLARED_VOID, not a failure", verdict(by["snapshot_class"]),
           "DECLARED_VOID")
    expect("a VOID location must say why",
           verdict(bent("snapshot_class", lambda r: r["location"].pop("reason"))), "VOID")
    expect("a missing field voids the card",
           verdict(bent(pend, lambda r: r.pop("warning_sign"))), "VOID")
    expect("an empty field voids the card", verdict(bent(pend, lambda r: r.update(fits=" "))), "VOID")
    expect("a card with no alias voids", verdict(bent(pend, lambda r: r.update(aliases=[]))), "VOID")
    expect("an unknown status voids", verdict(bent(pend, lambda r: r.update(status="VALIDATED"))),
           "VOID")
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
        print("rows %d: %s" % (res["rows"], ", ".join("%s %d" % kv for kv in sorted(res["counts"].items()))))
        if not res["finder_read"]:
            print("NOTE: TOOL_FINDER/finder.json was not read; finder names NOT_CHECKED")
    return 1 if res["void"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
