#!/usr/bin/env python3
"""merge_silent_loss -- lines a merge dropped that neither parent dropped.

A three-way merge may remove a line only if at least one parent removed it
relative to the merge base. Any other removal is a decision taken at merge
time -- a conflict resolved to one side, a file both sides added resolved to
one side, a hand edit inside the merge commit -- and git records none of
those decisions anywhere. This module walks merge commits and reports every
such line, per file, with:

    side          which parent held the line (p1 = the branch merged into,
                  p2 = the branch merged in)
    category      BOTH_ADDED  file absent at base, present in both parents
                  BOTH_KEPT   file absent at base, present in both parents,
                              and the merge holds every distinct line of
                              BOTH parents while equalling neither: two
                              builds spliced into one file, nothing lost.
                              The loss test is silent on this by
                              construction (nothing was dropped); it was
                              found by tests/test_compile_gate.py, which
                              read eight such modules across four merges
                              (b57c625, 1a9c09b, e167a67, 803ffd5) on
                              2026-09-30, none of which compiled. A row
                              here carries lost 0 and is not a loss row.
                  CONFLICT    both parents changed the file
                  ONE_SIDE    only the losing side changed the file; a plain
                              git merge keeps that side's version, so the
                              a hand edit inside the merge is the only route to the loss
    still_absent  of the lost lines, how many are missing from HEAD's copy
                  of the same file
    elsewhere     of those, how many are found somewhere else in HEAD's
                  tree (a rename or a move, not a loss; sampled, see below)

WHY IT EXISTS. tools/known_answer.py was cut by merges three times in ten
days (7cf18f4, dbf4cb0, 57b9cdf), losing registered metrics each time, and
was repaired each time only because it seeds itself at test time and the
registry count came up short. The other files those merges touched have no
equivalent check. This is that check, for any file.

REFUSALS, stated because the first run of this instrument did not have them:
    BASE_UNREACHABLE  no merge base in this clone (shallow history). The
                      first sweep read an unreachable base as an empty file
                      and reported ~1,400 lost lines across three merges
                      that had lost nothing. An absent base is not an empty
                      one.
    BASE_AMBIGUOUS    more than one merge base (criss-cross history). git
                      merges against a virtual base here; this module does
                      not construct one and does not pick.

WHAT THE TEST IS. A multiset of exact line texts per file. So: a line that
moved within a file is not lost; a line changed by one character is lost
(and its replacement is present, which the still_absent column sees only if
the replacement is byte-identical to something); one copy of a line that
occurs twice masks the loss of the other copy. The `elsewhere` column is
sampled -- up to SAMPLE lines of at least MIN_LEN characters per file are
searched tree-wide -- because a git grep per lost line over a 500-line loss
costs more than it returns. A rename therefore reads as `elsewhere` on the sample
and the reader decides. Nothing here says which side to keep;
that is what the merge author did not write down.

stdlib only. Reads git objects; never writes to the tree.
CC0.
"""
from __future__ import annotations

import collections
import os
import subprocess
import sys
import tempfile

SAMPLE = 12
MIN_LEN = 30


# --- git -------------------------------------------------------------------

def _git(args, cwd=None):
    r = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True)
    if r.returncode:
        return None
    return r.stdout.decode("utf-8", "surrogateescape")


def _show(rev, path, cwd=None):
    out = _git(["show", "%s:%s" % (rev, path)], cwd)
    return None if out is None else out.splitlines()


def merge_commits(cwd=None, rev="HEAD"):
    out = _git(["rev-list", "--merges", rev], cwd) or ""
    return out.split()


def _changed(a, b, cwd):
    return (_git(["diff", "--name-only", a, b], cwd) or "").split("\n")


# --- the measurement ---------------------------------------------------------

def _elsewhere(lines, cwd, head):
    """How many of a sample of lost lines occur anywhere in HEAD's tree."""
    probe = [l for l in lines if len(l.strip()) >= MIN_LEN][:SAMPLE]
    found = 0
    for l in probe:
        hit = _git(["grep", "-l", "-F", "--", l.strip(), head], cwd)
        if hit:
            found += 1
    return len(probe), found


def audit_merge(merge, cwd=None, head="HEAD"):
    p1, p2 = merge + "^1", merge + "^2"
    bases = (_git(["merge-base", "--all", p1, p2], cwd) or "").split()
    rec = {"merge": merge, "status": "OK", "base": None, "files": {}}
    if not bases:
        rec["status"] = "BASE_UNREACHABLE"
        return rec
    if len(bases) > 1:
        rec["status"] = "BASE_AMBIGUOUS(%d)" % len(bases)
        return rec
    base = bases[0]
    rec["base"] = base
    files = sorted({f for f in _changed(p1, merge, cwd) + _changed(p2, merge, cwd) if f})
    for f in files:
        b = _show(base, f, cwd)
        a1 = _show(p1, f, cwd)
        a2 = _show(p2, f, cwd)
        m = _show(merge, f, cwd) or []
        cb = collections.Counter(b or [])
        c1 = collections.Counter(a1 or [])
        c2 = collections.Counter(a2 or [])
        cm = collections.Counter(m)
        # lines a parent holds that the merge lacks, minus what the OTHER
        # parent deleted relative to base (a legitimate three-way removal)
        from_p2 = (c2 - cm) - (cb - c1)
        from_p1 = (c1 - cm) - (cb - c2)
        lost = collections.Counter(
            {k: v for k, v in (from_p1 + from_p2).items() if k.strip()})
        n_lost = sum(lost.values())
        in_base = b is not None
        if (not n_lost and not in_base and a1 is not None and a2 is not None
                and m != a1 and m != a2
                and not ((set(a1) | set(a2)) - set(m))):
            # BOTH_KEPT: every distinct line of both parents survived into a
            # file that is neither parent. Multiset would miss it (a blank
            # line two parents share is merged once); the set test is the
            # one that fires. `novel` counts merge lines from neither side.
            hl = _show(head, f, cwd)
            rec["files"][f] = {
                "lost": 0, "side": "both", "category": "BOTH_KEPT",
                "in_head_tree": hl is not None, "still_absent": 0,
                "elsewhere_probed": 0, "elsewhere_found": 0, "sample": [],
                "kept_p1": len(a1), "kept_p2": len(a2), "merge_lines": len(m),
                "novel": len(set(m) - (set(a1) | set(a2))),
                "head_is_p1": hl == a1, "head_is_p2": hl == a2,
            }
            continue
        if not n_lost:
            continue
        side = "p1" if sum(from_p1.values()) >= sum(from_p2.values()) else "p2"
        ch1 = a1 != b
        ch2 = a2 != b
        if not in_base and a1 is not None and a2 is not None:
            category = "BOTH_ADDED"
        elif ch1 and ch2:
            category = "CONFLICT"
        else:
            category = "ONE_SIDE"
        hl = _show(head, f, cwd)
        hc = collections.Counter(hl or [])
        still = collections.Counter({k: v for k, v in lost.items() if hc[k] < v})
        n_still = sum(still.values())
        probed, found = _elsewhere(list(still), cwd, head) if n_still else (0, 0)
        rec["files"][f] = {
            "lost": n_lost,
            "side": side,
            "category": category,
            "in_head_tree": hl is not None,
            "still_absent": n_still,
            "elsewhere_probed": probed,
            "elsewhere_found": found,
            "sample": list(lost)[:6],
        }
    return rec


def audit_all(cwd=None, rev="HEAD"):
    return [audit_merge(m, cwd, rev if rev != "HEAD" else "HEAD")
            for m in merge_commits(cwd, rev)]


# --- render --------------------------------------------------------------------

def render(records, cwd=None, verbose=False):
    out = []
    w = out.append
    w("merge_silent_loss -- lines a merge dropped that neither parent dropped")
    w("test: exact-line multiset per file against the single merge base")
    w("")
    n_ok = n_loss = n_kept = 0
    for r in records:
        subj = (_git(["log", "-1", "--format=%ad %s", "--date=short", r["merge"]], cwd)
                or "").strip()
        if r["status"] != "OK":
            w("%-9s %s  -- %s" % (r["merge"][:9], r["status"], subj[:70]))
            continue
        n_ok += 1
        if not r["files"]:
            if verbose:
                w("%-9s 0 files with loss  -- %s" % (r["merge"][:9], subj[:70]))
            continue
        loss_rows = {f: d for f, d in r["files"].items() if d["category"] != "BOTH_KEPT"}
        kept_rows = {f: d for f, d in r["files"].items() if d["category"] == "BOTH_KEPT"}
        n_loss += bool(loss_rows)
        n_kept += bool(kept_rows)
        w("%-9s %d file(s) with loss, %d both-kept  -- %s"
          % (r["merge"][:9], len(loss_rows), len(kept_rows), subj[:70]))
        for f, d in kept_rows.items():
            w("    %-55s BOTH_KEPT  merge %4d lines holds every distinct line of p1 (%d) and p2 (%d), lost 0, novel %d, HEAD is %s"
              % (f, d["merge_lines"], d["kept_p1"], d["kept_p2"], d["novel"],
                 "p1" if d["head_is_p1"] else "p2" if d["head_is_p2"] else
                 ("the splice" if d["in_head_tree"] else "absent")))
        for f, d in loss_rows.items():
            w("    %-55s lost %4d side=%s %-10s still_absent %4d  elsewhere %d/%d%s"
              % (f, d["lost"], d["side"], d["category"], d["still_absent"],
                 d["elsewhere_found"], d["elsewhere_probed"],
                 "" if d["in_head_tree"] else "  [file absent at HEAD]"))
    w("")
    w("merges audited %d   with loss %d   both-kept %d   refused %d"
      % (n_ok, n_loss, n_kept, len(records) - n_ok))
    w("a loss row is a decision the merge did not record; whether the dropped")
    w("side to keep is not measured here")
    return "\n".join(out)


# --- selftest: a constructed history, every state reached ------------------------

def _run(cwd, *args):
    r = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True)
    return r


def _commit(cwd, msg):
    _run(cwd, "add", "-A")
    _run(cwd, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q",
         "--allow-empty", "-m", msg)


def _write(cwd, name, lines):
    with open(os.path.join(cwd, name), "w") as fh:
        fh.write("\n".join(lines) + "\n")


def build_fixture(root):
    """Five merges: clean, conflict-resolved-to-p1, both-added-resolved-to-p1,
    one-side loss by `-s ours`, both-added-with-both-kept. Returns (repo, {name: sha})."""
    repo = os.path.join(root, "repo")
    os.makedirs(repo)
    _run(repo, "init", "-q", "-b", "main")
    _write(repo, "a.txt", ["line one", "line two", "line three", "line four"])
    _commit(repo, "base")
    shas = {}
    # 1. clean: A edits top, B edits bottom
    _run(repo, "checkout", "-q", "-b", "cleanA")
    _write(repo, "a.txt", ["line one CHANGED BY A", "line two", "line three", "line four"])
    _commit(repo, "A top")
    _run(repo, "checkout", "-q", "main")
    _write(repo, "a.txt", ["line one", "line two", "line three", "line four CHANGED BY B"])
    _commit(repo, "B bottom")
    _run(repo, "-c", "user.name=t", "-c", "user.email=t@t", "merge", "-q", "--no-edit", "cleanA")
    shas["clean"] = _run(repo, "rev-parse", "HEAD").stdout.strip()
    # 2. conflict: both add a different block after line two; resolve to main's
    _run(repo, "checkout", "-q", "-b", "confA")
    cur = open(os.path.join(repo, "a.txt")).read().splitlines()
    _write(repo, "a.txt", cur[:2] + ["ADDED BY A: a registration that seeds nothing else"] + cur[2:])
    _commit(repo, "A adds block")
    _run(repo, "checkout", "-q", "main")
    _write(repo, "a.txt", cur[:2] + ["ADDED BY MAIN: a different block in the same place"] + cur[2:])
    _commit(repo, "main adds block")
    r = _run(repo, "merge", "--no-commit", "confA")
    assert r.returncode != 0, "fixture: expected a conflict"
    _run(repo, "checkout", "--ours", "a.txt")
    _run(repo, "add", "a.txt")
    _run(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "merge confA, ours")
    shas["conflict"] = _run(repo, "rev-parse", "HEAD").stdout.strip()
    # 3. both added: a new file on each side, resolved to main's
    _run(repo, "checkout", "-q", "-b", "addA")
    _write(repo, "new.py", ["def build_one():", "    return 'branch build with its own selftest'"])
    _commit(repo, "A adds new.py")
    _run(repo, "checkout", "-q", "main")
    _write(repo, "new.py", ["def build_two():", "    return 'main build with a different test file'"])
    _commit(repo, "main adds new.py")
    r = _run(repo, "merge", "--no-commit", "addA")
    assert r.returncode != 0, "fixture: expected an add/add conflict"
    _run(repo, "checkout", "--ours", "new.py")
    _run(repo, "add", "new.py")
    _run(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "merge addA, ours")
    shas["both_added"] = _run(repo, "rev-parse", "HEAD").stdout.strip()
    # 4. one side: only the branch touches z.txt, merged with -s ours
    _run(repo, "checkout", "-q", "-b", "oneB")
    _write(repo, "z.txt", ["only the branch wrote this, and only git would have kept it"])
    _commit(repo, "B adds z.txt")
    _run(repo, "checkout", "-q", "main")
    _run(repo, "-c", "user.name=t", "-c", "user.email=t@t", "merge", "-q", "-s", "ours", "--no-edit", "oneB")
    shas["one_side"] = _run(repo, "rev-parse", "HEAD").stdout.strip()
    # 5. both kept: a new file on each side, resolved by keeping both wholes
    a_lines = ["# build A", "def build_a():", "    return 'A'"]
    m_lines = ["# build MAIN", "def build_main():", "    return 'MAIN'"]
    _run(repo, "checkout", "-q", "-b", "keepA")
    _write(repo, "two.py", a_lines)
    _commit(repo, "A adds two.py")
    _run(repo, "checkout", "-q", "main")
    _write(repo, "two.py", m_lines)
    _commit(repo, "main adds two.py")
    r = _run(repo, "merge", "--no-commit", "keepA")
    assert r.returncode != 0, "fixture: expected an add/add conflict"
    _write(repo, "two.py", m_lines[:1] + a_lines + m_lines[1:])
    _run(repo, "add", "two.py")
    _run(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "merge keepA, both kept")
    shas["both_kept"] = _run(repo, "rev-parse", "HEAD").stdout.strip()
    return repo, shas


def selftest(verbose=True):
    checks = []

    def ck(cond, label):
        checks.append((bool(cond), label))
        if verbose:
            print(("  ok   " if cond else "  FAIL ") + label)

    with tempfile.TemporaryDirectory() as root:
        repo, shas = build_fixture(root)
        clean = audit_merge(shas["clean"], repo)
        ck(clean["status"] == "OK" and clean["files"] == {},
           "a clean three-way merge reads zero loss (not CONSTANT_FIRES)")
        conf = audit_merge(shas["conflict"], repo)
        d = conf["files"].get("a.txt")
        ck(d is not None and d["lost"] == 1 and d["side"] == "p2" and d["category"] == "CONFLICT",
           "a conflict resolved to p1 reports p2's added line as CONFLICT loss")
        ck(d is not None and d["still_absent"] == 1 and d["elsewhere_found"] == 0,
           "the lost line is still absent at HEAD and found nowhere else")
        ba = audit_merge(shas["both_added"], repo)
        d = ba["files"].get("new.py")
        ck(d is not None and d["category"] == "BOTH_ADDED" and d["lost"] == 2 and d["side"] == "p2",
           "a file both sides added, resolved to one, reads BOTH_ADDED with the other build lost")
        bk = audit_merge(shas["both_kept"], repo)
        d = bk["files"].get("two.py")
        ck(d is not None and d["category"] == "BOTH_KEPT" and d["lost"] == 0
           and d["kept_p1"] == 3 and d["kept_p2"] == 3 and d["merge_lines"] == 6
           and d["novel"] == 0,
           "a file both sides added, resolved by keeping both, reads BOTH_KEPT with lost 0 (the loss test alone is silent here)")
        ck(bk["files"]["two.py"]["head_is_p1"] is False and bk["files"]["two.py"]["head_is_p2"] is False,
           "HEAD still holds the splice, neither parent")
        one = audit_merge(shas["one_side"], repo)
        d = one["files"].get("z.txt")
        ck(d is not None and d["category"] == "ONE_SIDE" and d["side"] == "p2" and not d["in_head_tree"],
           "a -s ours merge reads ONE_SIDE loss with the file absent at HEAD")
        # a moved line is not a loss: move a line and merge cleanly
        _run(repo, "checkout", "-q", "-b", "mover")
        cur = open(os.path.join(repo, "a.txt")).read().splitlines()
        _write(repo, "a.txt", cur[1:] + cur[:1])
        _commit(repo, "move first line to the end")
        _run(repo, "checkout", "-q", "main")
        _write(repo, "z2.txt", ["unrelated"])
        _commit(repo, "main unrelated")
        _run(repo, "-c", "user.name=t", "-c", "user.email=t@t", "merge", "-q", "--no-edit", "mover")
        mv = audit_merge(_run(repo, "rev-parse", "HEAD").stdout.strip(), repo)
        ck(mv["status"] == "OK" and mv["files"] == {},
           "a line moved within a file is not a loss (multiset test)")
        # elsewhere: the lost both-added line copied to another file at HEAD reads elsewhere 1
        _write(repo, "copy.py", ["    return 'branch build with its own selftest'"])
        _commit(repo, "copy the lost line elsewhere")
        ba2 = audit_merge(shas["both_added"], repo)
        d = ba2["files"]["new.py"]
        ck(d["still_absent"] == 2 and d["elsewhere_found"] == 1,
           "a lost line present elsewhere at HEAD reads still_absent AND elsewhere (a move, for the reader)")
        # shallow clone: the base is unreachable and the instrument refuses
        shallow = os.path.join(root, "shallow")
        r = _run(root, "clone", "-q", "--depth", "1", "--no-local", "file://" + repo, shallow)
        if r.returncode == 0:
            head = _run(shallow, "rev-parse", "HEAD").stdout.strip()
            sh = audit_merge(head, shallow)
            ck(sh["status"] == "BASE_UNREACHABLE" and sh["files"] == {},
               "a merge whose base is not in the clone is refused, not read against an empty file")
        else:
            ck(False, "shallow clone fixture could not be built: " + r.stderr.strip()[:80])
        ck(all(m in [x["merge"] for x in audit_all(repo)] for m in shas.values()),
           "audit_all walks every merge reachable from HEAD")
        text = render([clean, conf, ba, one, bk], repo)
        ck("CONFLICT" in text and "BOTH_ADDED" in text and "ONE_SIDE" in text
           and "BOTH_KEPT" in text
           and "merges audited 5   with loss 3   both-kept 1" in text,
           "render carries every category and keeps the both-kept count apart from the loss count")
    failed = [l for ok, l in checks if not ok]
    print("merge_silent_loss selftest: %d checks, %d failed" % (len(checks), len(failed)))
    return 0 if not failed else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    verbose = "-v" in argv
    args = [a for a in argv if not a.startswith("-")]
    cwd = os.getcwd()
    if "--all" in argv or not args:
        recs = audit_all(cwd)
    else:
        recs = [audit_merge(a, cwd) for a in args]
    print(render(recs, cwd, verbose))
    return 1 if any(r["status"] == "OK" and r["files"] for r in recs) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
