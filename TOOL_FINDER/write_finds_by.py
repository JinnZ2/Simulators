#!/usr/bin/env python3
"""write_finds_by.py -- append a Finds-by section per tool to its README.

CC0. Stdlib only. Co-authored (JinnZ2 + Claude), 2026-11-09. Work order
TOOL FINDER part 1. Additive only: appends to the end of a README, never edits
existing text; creates a README only where the tool's directory has none, and
says so in the created file. Idempotent: a section already present for that
tool is not written twice.

  python3 TOOL_FINDER/write_finds_by.py --dry-run [REPO ...]
  python3 TOOL_FINDER/write_finds_by.py [REPO ...]     REPO in entries.py keys

Target README:
  tool is a directory            -> <dir>/README.md
  tool is a file in a directory  -> README.md of that directory if one exists,
                                    else of the repo root (method-layer), else
                                    created in the file's directory
Shared READMEs get the tool name in the heading so several sections coexist.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import entries as EN  # noqa: E402
from build_finder import repo_dir  # noqa: E402

DATE = "2026-11-09"
TARGET = {  # file tools whose README lives somewhere specific
    ("method-layer", "frame_probe.py"): "README.md",
    ("method-layer", "observer_position_control.py"): "README.md",
    ("method-layer", "rank_detector.py"): "README.md",
    ("method-layer", "premise-traceability/register_map.py"): "premise-traceability/README.md",
}


def target(e):
    d = repo_dir(e["repo"])
    if (e["repo"], e["path"]) in TARGET:
        return d, TARGET[(e["repo"], e["path"])]
    if e["path"].endswith("/"):
        return d, e["path"] + "README.md"
    return d, os.path.join(os.path.dirname(e["path"]), "README.md")


def section(e, shared):
    head = "## Finds-by (ALIAS_PROPOSED, %s)" % DATE
    if shared:
        head += ": %s" % e["name"]
    L = ["", head, "Note %s: added by WORK ORDER TOOL FINDER part 1; aliases derived from this" % DATE,
         "tool's stated scope only. Index: Simulators `TOOL_FINDER/TOOL_FINDER.md`.", ""]
    L += ["- %s" % a for a in e["aliases"]]
    L.append("- avoided term: %s" % e["avoided"])
    L.append("- measures: \"%s\"" % e["measures"])
    if e["breaks_when"] == EN.NB:
        L.append("- breaks when: NO_STATED_LIMITS")
    else:
        L.append("- breaks when: \"%s\"" % e["breaks_when"])
    return "\n".join(L) + "\n"


def plan(repos):
    by_file = {}
    for e in EN.E:
        if repos and e["repo"] not in repos:
            continue
        d, rel = target(e)
        if d is None:
            continue
        by_file.setdefault((d, rel), []).append(e)
    out = []
    for (d, rel), es in sorted(by_file.items()):
        p = os.path.join(d, rel)
        exists = os.path.isfile(p)
        text = open(p, encoding="utf-8").read() if exists else ""
        shared = not (len(es) == 1 and es[0]["path"].endswith("/"))
        todo = []
        for e in es:
            marker = "## Finds-by (ALIAS_PROPOSED, %s)%s" % (DATE, (": %s" % e["name"]) if shared else "")
            if marker in text:
                continue
            todo.append(section(e, shared))
        if todo:
            out.append((p, exists, todo))
    return out


def main(argv):
    repos = [a for a in argv if not a.startswith("--")]
    dry = "--dry-run" in argv
    n = 0
    for p, exists, todo in plan(repos):
        n += len(todo)
        print("%s %s (+%d section%s)" % ("APPEND" if exists else "CREATE", p, len(todo), "" if len(todo) == 1 else "s"))
        if dry:
            continue
        with open(p, "a", encoding="utf-8") as f:
            if not exists:
                f.write("# %s\n\nNote %s: README created by WORK ORDER TOOL FINDER part 1 because this\n"
                        "directory had none. It holds only the Finds-by section(s) below; the tool's own\n"
                        "text is in the files beside it.\n" % (os.path.basename(os.path.dirname(p)), DATE))
            f.write("".join(todo))
    print("%s %d section(s)" % ("would add" if dry else "added", n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
