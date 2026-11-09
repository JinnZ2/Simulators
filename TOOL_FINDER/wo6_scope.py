"""WO-6 scope list, read from WO6_CORPUS_AUDIT.md (landed verbatim).

Round 4 item 2: the audit is the scope list. This module parses its
repository ledger and nothing else; it infers no scope.

IN       MERGED, plus the four open CI-blocked PRs (their status cells use
         three different spellings in the audit; all four are listed in
         its "Open CI-blocked PRs" section, and that section is checked).
OUT      SKIPPED_OUT_OF_SCOPE.
UNRESOLVED  SCOPE_UNRESOLVED: no edits, excluded from IN.

Any status cell outside those spellings stops the parse (no guessing).
The header table counts (75 / 4 / 22 / 2 / 0) are checked against the
ledger rows.

  python3 wo6_scope.py               print scope and the finder repos' status
  python3 wo6_scope.py --selftest    checks, including planted faults
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(HERE, "WO6_CORPUS_AUDIT.md")

IN_STATES = {"MERGED"}
CI_BLOCKED_STATES = {"BLOCKED_CI", "PR_OPEN_BLOCKED_FAILED_CI",
                     "PR_OPEN_CI_FAILED_UNMERGED"}
OUT_STATES = {"SKIPPED_OUT_OF_SCOPE"}
UNRESOLVED_STATES = {"SCOPE_UNRESOLVED"}
HEADER = {"merged": 75, "ci_blocked": 4, "out": 22, "unresolved": 2,
          "unreachable": 0}


class ScopeError(Exception):
    pass


def parse(text):
    if "## Repository / path / commit / PR ledger" not in text:
        raise ScopeError("ledger section not found")
    sec = text.split("## Repository / path / commit / PR ledger")[1]
    sec = sec.split("\n## ")[0]
    rows = {}
    for line in sec.splitlines():
        if not line.startswith("| JinnZ2/"):
            continue
        cells = [c.strip() for c in line.split("|")]
        repo, state = cells[1], cells[2]
        known = IN_STATES | CI_BLOCKED_STATES | OUT_STATES | UNRESOLVED_STATES
        if state not in known:
            raise ScopeError("unknown status %r for %s" % (state, repo))
        if repo in rows:
            raise ScopeError("duplicate ledger row %s" % repo)
        rows[repo] = state
    ci_sec = text.split("## Open CI-blocked PRs")[1].split("\n## ")[0]
    ci_listed = {l.split("|")[1].strip() for l in ci_sec.splitlines()
                 if l.startswith("| JinnZ2/")}
    out = {
        "merged": sorted(r for r, s in rows.items() if s in IN_STATES),
        "ci_blocked": sorted(r for r, s in rows.items()
                             if s in CI_BLOCKED_STATES),
        "out": sorted(r for r, s in rows.items() if s in OUT_STATES),
        "unresolved": sorted(r for r, s in rows.items()
                             if s in UNRESOLVED_STATES),
    }
    for k in ("merged", "ci_blocked", "out", "unresolved"):
        if len(out[k]) != HEADER[k]:
            raise ScopeError("%s: ledger %d, header %d"
                             % (k, len(out[k]), HEADER[k]))
    if set(out["ci_blocked"]) != ci_listed:
        raise ScopeError("CI-blocked rows do not match the CI-blocked section")
    out["in_scope"] = sorted(out["merged"] + out["ci_blocked"])
    out["rows"] = rows
    return out


def status_of(scope, repo):
    for k in ("rows",):
        for r, s in scope[k].items():
            if r.lower() == ("jinnz2/" + repo).lower() or r.lower() == repo.lower():
                return r, s
    return None, "NOT_IN_LEDGER"


def finder_repos():
    f = json.load(open(os.path.join(HERE, "finder.json")))
    return sorted({e["repo"] for e in f["entries"]})


def main():
    scope = parse(open(AUDIT, encoding="utf-8").read())
    print("WO-6 scope list (from WO6_CORPUS_AUDIT.md)")
    print("  in scope: %d (merged %d + CI-blocked %d)"
          % (len(scope["in_scope"]), len(scope["merged"]),
             len(scope["ci_blocked"])))
    print("  excluded: out-of-scope %d, unresolved %d"
          % (len(scope["out"]), len(scope["unresolved"])))
    print("  CI-blocked: " + ", ".join(scope["ci_blocked"]))
    print("  unresolved: " + ", ".join(scope["unresolved"]))
    print("finder repos against the scope list:")
    for r in finder_repos():
        full, s = status_of(scope, r)
        print("  %-22s %s %s" % (r, s, "(" + full + ")" if full else ""))


def selftest():
    fails = []

    def check(c, m):
        if not c:
            fails.append(m)
    text = open(AUDIT, encoding="utf-8").read()
    s = parse(text)
    check(len(s["in_scope"]) == 79, "79 in scope")
    check("JinnZ2/vibe-code-audit" in s["ci_blocked"], "vibe-code-audit CI-blocked")
    check(status_of(s, "Simulators")[1] == "MERGED", "Simulators MERGED")
    check(status_of(s, "no-such-repo")[1] == "NOT_IN_LEDGER", "absent repo")
    # planted faults: each must stop the parse
    plants = [
        text.replace("| JinnZ2/AI-arena | MERGED |", "| JinnZ2/AI-arena | SKIPPED_OUT_OF_SCOPE |", 1),
        text.replace("| JinnZ2/AI-arena | MERGED |", "| JinnZ2/AI-arena | MERGED? |", 1),
        text.replace("## Repository / path / commit / PR ledger", "## Ledger", 1),
    ]
    for i, p in enumerate(plants):
        check(p != text, "plant %d applied" % i)
        try:
            parse(p)
            check(False, "plant %d not caught" % i)
        except ScopeError:
            pass
    n = 4 + 2 * len(plants)
    print("checks: %d   failed: %d" % (n, len(fails)))
    for m in fails:
        print("  FAIL " + m)
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
