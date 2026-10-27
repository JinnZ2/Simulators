#!/usr/bin/env python3
"""KLOC per (subsystem, tag).  The only step that needs blobs.

Sparse checkout of the 36 paths at one tag at a time, count, then move
on -- disk peak is one tag's subset, not eight.  Temp dir only.
"""
import subprocess, json, os, sys, shutil
import subsystems as S

SRC = ("/tmp/claude-0/-home-user/edb5a076-aa65-52b4-b9f8-d9089c041f39"
       "/scratchpad/ks/linux")
WT = ("/tmp/claude-0/-home-user/edb5a076-aa65-52b4-b9f8-d9089c041f39"
      "/scratchpad/ks/wt")
TEXT_SKIP = {".png", ".jpg", ".gif", ".bmp", ".ico", ".bin", ".fw",
             ".gz", ".xz", ".bz2", ".zip", ".pdf", ".ttf", ".woff"}


def sh(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                          check=True, errors="replace").stdout


def count_lines(p):
    try:
        with open(p, "rb") as f:
            return f.read().count(b"\n")
    except OSError:
        return 0


def measure(tag):
    # [D3] a --shared clone does NOT inherit the promisor remote, so a
    # blobless source leaves it unable to fetch the missing blobs.  A
    # worktree shares the object store AND the partial-clone config, so
    # lazy fetch works.  Temp dir, removed after each tag.
    if os.path.exists(WT):
        shutil.rmtree(WT, ignore_errors=True)
    subprocess.run(["git", "-C", SRC, "worktree", "prune"],
                   capture_output=True, text=True)
    sh(["git", "-C", SRC, "worktree", "add", "--no-checkout", "-f",
        "--detach", WT, tag])
    sh(["git", "sparse-checkout", "init", "--cone"], cwd=WT)
    sh(["git", "sparse-checkout", "set"] + [p.rstrip("/") for p in S.PATHS],
       cwd=WT)
    sh(["git", "checkout", "-q", tag], cwd=WT)
    out = {}
    for p in S.PATHS:
        base = os.path.join(WT, p.rstrip("/"))
        lines, files = 0, 0
        for root, _d, fns in os.walk(base):
            for fn in fns:
                if os.path.splitext(fn)[1].lower() in TEXT_SKIP:
                    continue
                lines += count_lines(os.path.join(root, fn))
                files += 1
        out[p] = {"lines": lines, "files": files}
    shutil.rmtree(WT, ignore_errors=True)
    subprocess.run(["git", "-C", SRC, "worktree", "prune"],
                   capture_output=True, text=True)
    return out


def selftest():
    n = 0
    def chk(c, name):
        nonlocal n; n += 1; assert c, name
    import tempfile
    d = tempfile.mkdtemp()
    open(os.path.join(d, "a.c"), "w").write("x\ny\nz\n")
    chk(count_lines(os.path.join(d, "a.c")) == 3, "counts newlines")
    open(os.path.join(d, "b.c"), "w").write("no trailing newline")
    chk(count_lines(os.path.join(d, "b.c")) == 0, "no newline -> 0")
    chk(count_lines(os.path.join(d, "missing.c")) == 0, "absent -> 0")
    chk(".png" in TEXT_SKIP and ".c" not in TEXT_SKIP, "binary skip list")
    shutil.rmtree(d)
    print("checks: %d  failed: 0" % n)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest(); sys.exit(0)
    res = {}
    for tag, _d in S.TAGS:
        res[tag] = measure(tag)
        tot = sum(v["lines"] for v in res[tag].values())
        print("%-6s %10d lines across 36 paths" % (tag, tot), file=sys.stderr)
        json.dump(res, open("kloc.json", "w"), indent=1, sort_keys=True)
    print("wrote kloc.json")
