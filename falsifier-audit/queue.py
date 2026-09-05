#!/usr/bin/env python3
"""queue.py -- the research queue. Every entry is a QUESTION with status
OPEN (the only machine-set value). No rank, no score. Ids are stable:
re-running on an unchanged tree emits the same ids, so entries can be
closed by hand in a separate file and survive the next run. A coverage
line reports falsifiers found / analysed and files skipped and why, so
an unscanned file does not read as a clean one. Stdlib only.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract as E  # noqa: E402
import checks as C  # noqa: E402


def entries(records=None, empty=0):
    if records is None:
        records, empty = E.records()
    out = []
    for h in C.per_record(records):
        out.append({"qid": "%s/%s" % (h["check"], h["falsifier_id"]),
                    "check": h["check"], "falsifier_id": h["falsifier_id"],
                    "text": h["text"], "question": h["question"], "detail": h.get("detail", ""),
                    "status": "OPEN"})
    out.sort(key=lambda e: e["qid"])
    return out


def coverage(roots=None, exclude=E.SELF_EXCLUDE):
    roots = roots or [E.DEFAULT_ROOT]
    scanned = skipped_binary = skipped_excluded = 0
    skipped_ext = 0
    for root in roots:
        root = os.path.abspath(root)
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d not in E.SKIP_DIRS]
            for fn in fns:
                ap = os.path.join(dp, fn)
                rel = os.path.relpath(ap, root)
                if not fn.endswith((".md", ".py")):
                    skipped_ext += 1
                    continue
                if any(x in rel for x in exclude):
                    skipped_excluded += 1
                    continue
                if not E.is_text(ap):
                    skipped_binary += 1
                    continue
                scanned += 1
    return {"scanned_md_py": scanned, "skipped_non_md_py": skipped_ext,
            "skipped_binary_or_nontext": skipped_binary,
            "skipped_self_excluded": skipped_excluded,
            "skip_dirs": sorted(E.SKIP_DIRS)}


def render(roots=None):
    records, empty = E.records(roots)
    ent = entries(records, empty)
    cov = coverage(roots)
    from collections import Counter
    by_check = Counter(e["check"] for e in ent)
    by_status = Counter(r["attach_status"] for r in records)
    L = ["falsifier research queue -- questions, not repairs; status OPEN; unranked"]
    L.append("COVERAGE: %d falsifiers found (%d LOCATED, %d NOT-FOUND, %d empty cells skipped); "
             "%d entries by A1-A4 %s" % (len(records), by_status.get("LOCATED", 0), by_status.get("NOT-FOUND", 0),
                                         empty, len(ent), dict(by_check)))
    L.append("COVERAGE: scanned %d .md/.py files; skipped %d non-.md/.py, %d binary/non-text, %d self-excluded "
             "(the tool's own queue, samples, and authored docs); skip dirs %s" % (
                 cov["scanned_md_py"], cov["skipped_non_md_py"], cov["skipped_binary_or_nontext"],
                 cov["skipped_self_excluded"], cov["skip_dirs"]))
    L.append("NOTE A3 (cross-repo incompatibility) emitted %d entries: on this corpus the numeric-bearing "
             "falsifiers on any shared axis are folder-local, so no two folders quantify one axis "
             "incompatibly -- the same unquantified property A1 flags. Not silent: the null test fires." % by_check.get("A3", 0))
    L.append("")
    for e in ent:
        L.append("[%s] %s   status:%s" % (e["check"], e["qid"], e["status"]))
        L.append("  falsifier: %s" % e["text"][:200])
        L.append("  question:  %s" % e["question"])
        if e["detail"]:
            L.append("  detail:    %s" % e["detail"][:200])
    return "\n".join(L)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        print("queue has no selftest; run selftest_fa.py", file=sys.stderr)
        return 2
    roots = [a for a in argv if not a.startswith("-")] or None
    out = render(roots)
    if "--write" in argv:
        with open(os.path.join(HERE, "QUEUE.md"), "w", encoding="utf-8") as fh:
            fh.write("# QUEUE — falsifier audit\n\n")
            fh.write("Emitted by `run_all.py`; human-editable and hand-closable. Every entry is\n")
            fh.write("a research question with status OPEN. Ids are stable across runs on an\n")
            fh.write("unchanged tree; close an entry by recording its qid elsewhere.\n\n```\n")
            fh.write(out + "\n```\n")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
