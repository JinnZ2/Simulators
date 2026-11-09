#!/usr/bin/env python3
"""check_landing.py -- confirm the landed ICSC files carry the PDF's text unedited. CC0, stdlib + pdftotext.

Note 2026-11-09: the markdown source arrived after the PDF. It is SPEC_AUDIT_v0.1.md; the earlier
pdftotext stand-in moved to SPEC_AUDIT_v0.1.pdftotext.md. Check 4 compares the two word sequences
after stripping markdown and box-drawing characters.

python3 ICSC/check_landing.py      prints checks: N failed: M; NOT_RUN if pdftotext is absent.
"""
import hashlib, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PDF, MD = os.path.join(HERE, "SPEC_AUDIT_v0.1.pdf"), os.path.join(HERE, "SPEC_AUDIT_v0.1.pdftotext.md")
SRC = os.path.join(HERE, "SPEC_AUDIT_v0.1.md")
def words(t):
    return re.sub(r"[`#\-\u2500\u2502\u251c\u2514]+", " ", t).split()
SHA = "b0a1d4f2e2f2703e629fc7edab8a2db7b18e3bf3014bc79f2d2e712cc8dfc111"
ok = total = 0
def check(c, lab):
    global ok, total
    total += 1; ok += bool(c)
    if not c: print("FAIL:", lab)
check(hashlib.sha256(open(PDF, "rb").read()).hexdigest() == SHA, "PDF bytes match the delivered sha256")
md = open(MD, encoding="utf-8").read()
check(SHA in md and "STATUS: PROPOSED" in md, "header carries sha256 and PROPOSED status")
if shutil.which("pdftotext") is None:
    print("NOT_RUN: pdftotext absent; text identity not checked")
else:
    lay = subprocess.run(["pdftotext", "-layout", PDF, "-"], capture_output=True, text=True).stdout
    body = md.split("```text\n", 1)[1].rsplit("```", 1)[0]
    check(body == lay, "fenced text equals a fresh pdftotext -layout extraction")
    src = open(SRC, encoding="utf-8").read()
    check(words(src) == words(lay), "markdown source has the same word sequence as the PDF")
print("checks: %d   failed: %d" % (total, total - ok))
sys.exit(0 if ok == total else 1)
