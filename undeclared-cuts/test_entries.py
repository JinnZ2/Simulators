#!/usr/bin/env python3
"""Checks on check_entries.py. Prints the check count; nothing stores it.

Every check that asserts the checker STAYS SILENT is paired with one that
plants the condition and asserts it FIRES. A validator nobody has seen
refuse is not known to discriminate.

    python3 test_entries.py
"""

import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_entries as CE

COUNT = [0]
FAILED = []


def check(name, cond):
    COUNT[0] += 1
    if not cond:
        FAILED.append(name)


HEADER = "\n".join("%s: v%d" % (k, i) for i, k in enumerate(CE.REQUIRED))
GOOD = (HEADER
        .replace("status: v2", "status: NOT_MEASURED")
        .replace("term_status: v3", "term_status: UNNAMED")
        .replace("decay_class: v11", "decay_class: UNSET")
        + "\n\nbody line\nid: not-a-header\n")


def write(tmp, name, text):
    path = os.path.join(tmp, name)
    with open(path, "w") as fh:
        fh.write(text)
    return path


def section_parser(tmp):
    p = write(tmp, "GOOD.md", GOOD)
    rep = CE.read_header(p)
    check("good entry is complete", rep.complete)
    check("good entry has 12 keys", len(rep.header) == 12)
    check("body not read as header", rep.header["id"] == "v0")
    check("malformed is None", rep.malformed is None)

    # absent key
    lines = [l for l in GOOD.split("\n") if not l.startswith("owner:")]
    p = write(tmp, "NOOWNER.md", "\n".join(lines))
    rep = CE.read_header(p)
    check("absent key caught", rep.missing == ["owner"])
    check("absent key is not empty-key", rep.empty == [])
    check("absent key -> incomplete", not rep.complete)

    # present and empty
    p = write(tmp, "EMPTY.md", GOOD.replace("owner: v10", "owner:"))
    rep = CE.read_header(p)
    check("empty key caught", [k for k, _ in rep.empty] == ["owner"])
    check("empty key is not missing", rep.missing == [])
    check("empty key carries a line number", rep.empty[0][1] == 11)

    # sentinels are valid
    sent = (GOOD.replace("reinspect: v9", "reinspect: UNSET")
                .replace("owner: v10", "owner: UNOWNED")
                .replace("control: v5", "control: NONE_KNOWN"))
    p = write(tmp, "SENT.md", sent)
    check("sentinels pass", CE.read_header(p).complete)

    # vocabulary
    p = write(tmp, "OFFVOCAB.md", GOOD.replace("status: NOT_MEASURED",
                                               "status: MEASURED"))
    rep = CE.read_header(p)
    check("off-vocabulary caught", [k for k, _, _ in rep.off_vocab] == ["status"])
    check("off-vocabulary carries the value",
          rep.off_vocab[0][2] == "MEASURED")
    for value in CE.VOCAB["status"]:
        p = write(tmp, "V.md", GOOD.replace("status: NOT_MEASURED",
                                            "status: " + value))
        check("vocabulary member %s passes" % value,
              CE.read_header(p).complete)

    # any status x term_status combination is legal
    for s in CE.VOCAB["status"]:
        for t in CE.VOCAB["term_status"]:
            p = write(tmp, "C.md", GOOD
                      .replace("status: NOT_MEASURED", "status: " + s)
                      .replace("term_status: UNNAMED", "term_status: " + t))
            check("combination %s/%s legal" % (s, t),
                  CE.read_header(p).complete)

    # duplicate
    p = write(tmp, "DUP.md", GOOD.replace("owner: v10", "owner: v10\nowner: v10"))
    rep = CE.read_header(p)
    check("duplicate caught", [k for k, _ in rep.duplicate] == ["owner"])
    check("duplicate keeps first value", rep.header["owner"] == "v10")

    # malformed
    p = write(tmp, "BAD.md", GOOD.replace("owner: v10", "owner v10"))
    rep = CE.read_header(p)
    check("malformed caught", rep.malformed is not None)
    check("malformed line number", rep.malformed[0] == 11)
    check("malformed infers nothing", rep.missing == [] and rep.empty == [])
    check("malformed -> incomplete", not rep.complete)

    # leading blank lines skipped
    p = write(tmp, "LEAD.md", "\n\n" + GOOD)
    check("leading blanks skipped", CE.read_header(p).complete)

    # value containing a colon survives
    p = write(tmp, "COLON.md", GOOD.replace("title: v1", "title: a: b: c"))
    check("colon in value kept", CE.read_header(p).header["title"] == "a: b: c")


def section_registry(tmp):
    d = os.path.join(tmp, "entries")
    os.mkdir(d)
    write(d, "B.md", GOOD.replace("id: v0", "id: B-2")
          .replace("title: v1", "title: second"))
    write(d, "A.md", GOOD.replace("id: v0", "id: A-1")
          .replace("title: v1", "title: first")
          .replace("owner: v10", "owner: UNOWNED"))
    reports = CE.check_all(d)
    check("both entries read", len(reports) == 2)
    text = CE.registry_text(reports)
    check("registry sorted by id", text.index("A-1") < text.index("B-2"))
    check("registry carries title", "first" in text and "second" in text)
    check("registry carries status", "NOT_MEASURED" in text)
    check("registry carries owner", "UNOWNED" in text)
    check("registry counts entries", "2 entries." in text)
    check("registry marks itself generated", "do not hand-edit" in text)
    check("registry has no score column",
          "score" not in text.lower() and "rank" not in text.lower())

    check("missing dir returns None", CE.check_all(os.path.join(tmp, "nope")) is None)

    rendered = CE.render(reports, d)
    check("render marks OK", "OK " in rendered)
    check("render states sentinel rule", "never whether it was filled" in rendered)

    write(d, "C.md", GOOD.replace("owner: v10", "owner:"))
    reports = CE.check_all(d)
    rendered = CE.render(reports, d)
    check("render marks INCOMPLETE", "INCOMPLETE" in rendered)
    check("render gives file:line", "C.md:11" in rendered)
    check("incomplete entry still reaches registry",
          "(no owner)" in CE.registry_text(reports))


def section_cli(tmp):
    rc = CE.main(["--selftest"])
    check("refuses --selftest", rc == 2)
    rc = CE.main(["--dir", os.path.join(tmp, "absent"), "--no-write"])
    check("absent dir -> rc 3", rc == 3)


def section_real():
    here = os.path.dirname(os.path.abspath(__file__))
    d = os.path.join(here, "entries")
    reports = CE.check_all(d)
    check("real entries found", reports is not None and len(reports) > 0)
    check("every real entry complete", all(r.complete for r in reports))
    ids = [r.get("id") for r in reports]
    check("real ids unique", len(ids) == len(set(ids)))
    check("real ids match filenames",
          all(r.get("id") + ".md" == os.path.basename(r.path) for r in reports))
    check("every real entry declares a sentinel or a value on reinspect",
          all(r.get("reinspect") != "" for r in reports))
    check("no real entry body is empty",
          all(os.path.getsize(r.path) > len("\n".join(
              "%s:" % k for k in CE.REQUIRED)) for r in reports))


def main():
    tmp = tempfile.mkdtemp(prefix="undeclared-cuts-")
    try:
        section_parser(tmp)
        section_registry(tmp)
        section_cli(tmp)
        section_real()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("checks: %d   failed: %d" % (COUNT[0], len(FAILED)))
    for name in FAILED:
        print("  FAILED  %s" % name)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
