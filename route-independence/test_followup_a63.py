# SPDX-License-Identifier: CC0-1.0
"""Checks for the operator follow-up of 2026-09-30 (followup_a63.py).

Run:  python3 route-independence/test_followup_a63.py
Prints the check count and how many of the three fixtures built to FAIL exist.  No network: the
resolver is exercised with a constructed fetch; the live attempt on file is read, not repeated.
"""
import ast
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import followup_a63 as F       # noqa: E402
import gate_state_a21 as G21   # noqa: E402
import sourcing_a62 as P       # noqa: E402
import verification_a63 as V   # noqa: E402

_checks = 0
_failed = 0
FIXTURES = {"pin": False, "scan": False, "resolve": False}


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


def fake(table):
    """Constructed fetch: url -> (status, n_bytes)."""
    def f(url):
        st, n = table.get(url, (None, None))
        return {"status": st, "n_bytes": n, "sha256": None, "failure": None if st == 200 else "constructed"}
    return f


def t_resolve():
    a = "example.org/doc.pdf"
    check(F.candidates(a) == ["https://example.org/doc.pdf", "http://example.org/doc.pdf"], "no scheme: https then http")
    check(F.candidates("http://example.org/x") == ["http://example.org/x"], "a scheme is tried as written only")
    check(F.candidates("") == [] and F.candidates(None) == [], "no address, no candidates")
    r = F.resolve("S", a, fake({}), at="T")
    check(r["resolved_url"] is None and r["address"] == a and len(r["attempts"]) == 2, "nothing returned: None, both tried")
    r = F.resolve("S", a, fake({"https://example.org/doc.pdf": (403, 120), "http://example.org/doc.pdf": (200, 9)}), at="T")
    check(r["resolved_url"] == "http://example.org/doc.pdf", "the fetch decides the scheme: http")
    check(r["address"] == a, "the address is not rewritten")
    r = F.resolve("S", a, fake({"https://example.org/doc.pdf": (200, 9), "http://example.org/doc.pdf": (200, 9)}), at="T")
    check(r["resolved_url"] == "https://example.org/doc.pdf" and len(r["attempts"]) == 1, "first success stops")
    r = F.resolve("S", a, fake({"https://example.org/doc.pdf": (200, 0), "http://example.org/doc.pdf": (403, 50)}), at="T")
    check(r["resolved_url"] is None, "an empty 200 is not bytes [CHOICE 106]")
    check(not F.returned_bytes({"status": 403, "n_bytes": 500}), "a refusal body is not source bytes")
    FIXTURES["resolve"] = r["resolved_url"] is None
    for sid in F.RESOLVE_IDS:
        src = G21.SOURCES21[sid]
        check(V.location_form(src["url"]) == "NO_SCHEME", "%s address kept as written, no scheme added" % sid)
        check("resolved_url" not in src, "%s: resolved_url is not typed into the source table" % sid)
        s = F.address_state(sid)
        check(s["resolved_url"] is None and s["status"] == V.NO_SPAN, "%s: resolved_url None, NO_SPAN" % sid)
        check(s["n_attempts_on_file"] >= 1, "%s: the live attempt is on file" % sid)
        check(all(not F.returned_bytes(t) for t in s["last"]["attempts"]), "%s: no attempt on file returned bytes" % sid)
        check([t["url"] for t in s["last"]["attempts"]] == F.candidates(src["url"]), "%s: both schemes tried" % sid)
    tree = ast.parse(open(os.path.join(HERE, "followup_a63.py"), encoding="utf-8").read())
    top = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    names = [a.name for n in top for a in n.names] + [n.module or "" for n in top if isinstance(n, ast.ImportFrom)]
    check(not [x for x in names if "urllib" in x or "http" in x or "socket" in x], "no network import at module scope")


def t_pins():
    rows = F.pin_check()
    check(len(rows) == 10, "ten modules pinned")
    check(all(r["state"] in (F.PINNED, F.DECLARED_EDIT) for r in rows),
          "every module pinned or declared %s" % [(r["module"], r["state"]) for r in rows])
    ed = sorted(r["module"] for r in rows if r["state"] == F.DECLARED_EDIT)
    check(ed == ["gate_state_a21.py", "standing_a61.py"], "the two A-6.3 edits read as declared edits %s" % ed)
    check(F.blob_sha1(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391", "blob sha1 of empty = git's")
    h = F.history_check()
    if h["status"] == F.NOT_TESTABLE:
        sys.stderr.write("NOT_TESTABLE: %s\n" % h["reason"])
    else:
        check(h["all_match"] and len(h["rows"]) == 12, "pins and declared blobs match git at their commits")
    planted = F.pin_check(read=lambda m: open(os.path.join(HERE, m), "rb").read() + (b"#\n" if m == "chains_a4.py" else b""))
    check([r["state"] for r in planted if r["module"] == "chains_a4.py"] == [F.UNDECLARED_EDIT], "a planted edit fires")
    gone = F.pin_check(read=lambda m: None if m == "termini_a5.py" else open(os.path.join(HERE, m), "rb").read())
    check([r["state"] for r in gone if r["module"] == "termini_a5.py"] == [F.MISSING], "a missing module reads MISSING")
    ff = F.pin_fail_fixture()
    check(ff["fires"], "fail fixture: without the declaration the committed edit reads UNDECLARED_EDIT")
    if ff["weak_clean"] is not None:
        check(ff["weak_clean"] is True, "the replaced check reads the committed edit as clean (the shape reported)")
    FIXTURES["pin"] = ff["fires"]
    src = open(os.path.join(HERE, "test_sourcing_a62.py"), encoding="utf-8").read()
    check('"diff", "--quiet", "HEAD", "--"] + [m + ".py"' not in src, "the weak module check is gone")
    check("FU.pin_check()" in src, "test_sourcing_a62 reads the pins")


def t_scan():
    flags = F.disposed(F.scan_folder())
    mod = [f for f in flags if f["kind"] == "MODULE"]
    check(not [f for f in flags if f["disposition"] == F.UNDISPOSED], "no undisposed flag")
    keys = set((f["file"], f["caller"], f["gate"], f["param"], f["value"]) for f in flags)
    check(not [d for d in F.DISPOSITIONS if d[:5] not in keys], "no stale disposition")
    check(len(mod) == 19 and len(flags) - len(mod) == 9, "19 module flags, 9 test flags (%d, %d)"
          % (len(mod), len(flags) - len(mod)))
    check(("verification_a63.py", "rerun_a63", "gate_core", "enumerated", True) in keys, "rerun_a63 constant flagged")
    check(("standing_a61.py", "prior_sweep", "gate_status", "falsifier_cases_enumerated", True) in keys,
          "RIN_146's prior_sweep constant flagged")
    n = F.scan_null()
    check(n["n"] == 3 and [v[2] for v in n["values"]] == [False, None, True], "null: literal flagged, variable not")
    none = F.scan_source("def f(r, s, e, a):\n    gate_core(r, s, e, a)\n    other(r, True)\n", "x.py")
    check(none == [], "variables and non-gates are not flagged")
    FIXTURES["scan"] = n["n"] == 3
    gates = F.gate_table()
    check(sorted(gates) == ["consistent", "gate_a62", "gate_a63", "gate_core", "gate_status", "input_status"],
          "gate table %s [CHOICE 108]" % sorted(gates))
    c = F.consequence("rerun_a63")
    check(c["n_rows"] == 19 and len(c["moved"]) == 18, "flipping rerun_a63's constant moves 18 of 19")
    rows = [r["row"] for r in V.rerun_a63()]
    check([r for r in rows if r not in c["moved"]] == ["E-A6.1-3"], "the unmoved row is E-A6.1-3 (aggregate)")
    check(len(F.consequence("rerun_a62")["moved"]) == 18, "rerun_a62 constant: 18 of 19")
    p = F.consequence("prior_sweep")
    check(p["n_rows"] == 17 and len(p["moved"]) == 17, "prior_sweep constant: 17 of 17")
    check(F.consequence("nothing") is None, "unknown key: None")


def t_shifts():
    s = F.shift_check()
    if s["status"] == F.NOT_TESTABLE:
        sys.stderr.write("NOT_TESTABLE: shift commits unreachable\n")
        return
    for r in s["rows"]:
        check(r["match"], "%s: declared lines equal the diff %s" % (r["sample"], r["diff"]))
        check(r["live_equals_to"], "%s: live sample is b10392f's (no later drift)" % r["sample"])
    check(sum(len(x[2]) for x in F.SAMPLE_SHIFTS) == 6, "six sample lines declared")


def t_hygiene():
    p = subprocess.run([sys.executable, os.path.join(HERE, "followup_a63.py"), "--selftest"], capture_output=True)
    check(p.returncode == 2, "--selftest refused")
    raw = open(os.path.join(HERE, "followup_a63.py"), "rb").read()
    check(all(b < 128 for b in raw), "ASCII")
    ast.parse(raw.decode("ascii"), feature_version=(3, 8))
    txt = raw.decode("ascii")
    decl = txt[txt.index("CHOICES = {"):txt.index("}\n", txt.index("CHOICES = {"))]
    rest = txt.replace(decl, "")
    for k in F.CHOICES:
        check("[CHOICE %d]" % k in rest, "CHOICE %d cited outside its declaration" % k)
    buf = io.StringIO()
    F.render(buf)
    r = buf.getvalue()
    p = subprocess.run([sys.executable, os.path.join(HERE, "..", "sheet-structure-scan", "no_severity.py")],
                       input=r, capture_output=True, text=True)
    check("no severity or interpretation vocabulary" in p.stdout, "render screens clean %s" % p.stdout[:200])
    log = subprocess.run(["git", "show", "--name-only", "--format=", F.EXPECTED_COMMIT_FU], cwd=HERE,
                         capture_output=True, text=True)
    if log.returncode == 0:
        check(log.stdout.split() == ["route-independence/" + F.FOLLOWUP_FILE], "the follow-up was committed alone")
    check(open(os.path.join(HERE, F.FOLLOWUP_FILE), encoding="utf-8").read().count("\n1. W-1a / W-2a scheme") == 1,
          "follow-up landed")
    sample = os.path.join(HERE, "samples", "followup_a63.sample.txt")
    if os.path.exists(sample):
        check(open(sample, encoding="utf-8").read() == r, "sample matches a fresh render")
    check(P.load_store() == [], "A-6.2's span store is still empty")
    for t in ("test_verification_a63.py", "test_sourcing_a62.py", "test_gate_state_a21.py"):
        p = subprocess.run([sys.executable, os.path.join(HERE, t)], capture_output=True)
        check(p.returncode == 0, "%s still green" % t)


for fn in (t_resolve, t_pins, t_scan, t_shifts, t_hygiene):
    fn()

n = sum(1 for v in FIXTURES.values() if v)
tag = "" if n == 3 else "  NO_FAIL_FIXTURE"
print("followup-a63: %d checks, %d failed; fail fixtures present: %d of 3%s" % (_checks, _failed, n, tag))
sys.exit(1 if _failed else 0)
