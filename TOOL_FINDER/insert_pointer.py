#!/usr/bin/env python3
"""insert_pointer.py -- add the TOOL_FINDER pointer to a repo README (Amendment A3).

CC0. Stdlib only. Co-authored (JinnZ2 + Claude), 2026-11-09.

  python3 TOOL_FINDER/insert_pointer.py --dry-run REPO_DIR ...
  python3 TOOL_FINDER/insert_pointer.py REPO_DIR ...
  python3 TOOL_FINDER/insert_pointer.py --selftest

Rule (A3 item 2): the READ_ME_THIS_WAY preamble stays first, byte for byte; the
pointer goes immediately after it (line 3 when the preamble is the usual two
lines). The preamble is the run of leading '>' lines that mentions
READ_ME_THIS_WAY. A README with no such preamble is SKIPPED_NO_PREAMBLE, not
edited: placing the pointer "after the preamble" is undefined there. A README
that already carries the pointer is ALREADY_PRESENT. After writing, the file is
re-read and every original byte is checked to be where it was: the preamble
unchanged at the top and the rest unchanged after the inserted lines.
"""
import os, sys

LINK = "https://github.com/JinnZ2/Simulators/blob/main/TOOL_FINDER/TOOL_FINDER.md"
POINTER = ["> Looking for a tool by what's going wrong?\n", "> See TOOL_FINDER: %s\n" % LINK]


def plan(text):
    lines = text.splitlines(keepends=True)
    if any(POINTER[0].strip() in l for l in lines[:12]):
        return "ALREADY_PRESENT", None
    k = 0
    while k < len(lines) and lines[k].startswith(">"):
        k += 1
    if k == 0 or not any("READ_ME_THIS_WAY" in l for l in lines[:k]):
        return "SKIPPED_NO_PREAMBLE", None
    return "INSERT", k


def apply(text):
    state, k = plan(text)
    if state != "INSERT":
        return state, text, None
    lines = text.splitlines(keepends=True)
    new = "".join(lines[:k] + POINTER + lines[k:])
    head, tail = "".join(lines[:k]), "".join(lines[k:])
    assert new.startswith(head) and new.endswith(tail) and len(new) == len(text) + len("".join(POINTER))
    return "INSERTED", new, k + 1


def selftest():
    ok = tot = 0
    def check(c, lab):
        nonlocal ok, tot
        tot += 1; ok += bool(c)
        if not c: print("FAIL:", lab)
    pre = "> Before reading or editing anything here, read READ_ME_THIS_WAY.md.\n> Mismatches kept.\n\n# Title\nbody\n"
    st, new, line = apply(pre)
    check(st == "INSERTED" and line == 3, "pointer lands on line 3 after a two-line preamble")
    check(new.splitlines()[2] == POINTER[0].rstrip("\n"), "line 3 is the pointer")
    check(new.startswith(pre.split("\n\n")[0]), "preamble bytes unchanged")
    check(apply(new)[0] == "ALREADY_PRESENT", "idempotent")
    check(apply("WHY THIS REPO EXISTS\n\nletter\n")[0] == "SKIPPED_NO_PREAMBLE", "no preamble -> skipped")
    check(apply("> a quote unrelated\n\n# T\n")[0] == "SKIPPED_NO_PREAMBLE", "blockquote without READ_ME_THIS_WAY -> skipped")
    print("checks: %d   failed: %d" % (tot, tot - ok))
    return 0 if ok == tot else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    dry = "--dry-run" in argv
    for d in [a for a in argv if not a.startswith("--")]:
        p = os.path.join(d, "README.md")
        if not os.path.isfile(p):
            print("%-14s %s" % ("NO_README", d)); continue
        text = open(p, encoding="utf-8").read()
        st, new, line = apply(text)
        if st == "INSERTED" and not dry:
            open(p, "w", encoding="utf-8").write(new)
            back = open(p, encoding="utf-8").read()
            assert back == new
        print("%-14s %s%s" % (st if not dry or st != "INSERTED" else "WOULD_INSERT", d, (" (line %d)" % line) if line else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
