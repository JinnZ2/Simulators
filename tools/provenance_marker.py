"""provenance_marker.py -- ran before, here is the hash, here is how it works.

CC0. stdlib only. Parses under Python 3.9.

One marker per run of a tool, appended to a ledger. A marker records:

    path      the tool file the marker is about
    sha256    the tool file's hash at the run (taken before AND after; a
              tool that changes its own file during the run is refused)
    cmd       the command that was run (often the tool's own selftest, or a
              test file beside it)
    exit      that command's exit code
    last_line the last non-empty line it printed (its own check count, if
              it prints one -- read, never parsed into a number here)
    ran_at    UTC timestamp
    how       one line, stated by whoever stamps it: what the tool does
    passes    the operator's five passes (below), one state each
    prev      sha256 of the previous ledger line, so the ledger is a chain

THE FIVE PASSES (the operator's method for finding semantic manipulation;
each pass converts a claim into a grammar that forces something English
lets a writer leave out):

    P1  noun -> verb       (Ojibwe)   forces exact condition + temporal scope
    P2  animacy            (Ojibwe)   "am I in relation with this?" -- a
                                      still-coupled thing written as an
                                      inert specimen
    P3  logic puzzle       (Aristotle) entailment: hidden quantifier,
                                      missing middle term
    P4  round trip         (Ithkuil/Lojban) every predicate place filled
    P5  evidentiality      (Turkish)  witnessed / inferred / reported

Each pass carries one of four states:

    RUNS        the tool runs this pass; a basis (path:line) is required and
                must resolve to a real line
    PARTIAL     the tool runs part of it; a basis AND a note saying which
                half is missing are required
    NOT_RUN     declared not run
    UNDECLARED  nobody said -- never read as NOT_RUN and never as RUNS

The pass states are a DECLARATION by whoever stamps the marker, recorded
with `declared_by`. Nothing here infers a pass from a tool's text: deciding
whether code runs a pass is a reading, and a word list doing it would be
the failure the passes exist to catch. What IS checked mechanically: the
basis line exists, the hash matches the file, the chain is unbroken.

Commands:
    stamp PATH --how TEXT --by WHO [--cmd CMD] [--pass P1=RUNS@file:line]
          [--note P1=TEXT]      run CMD (default: python3 PATH --selftest)
                                and append a marker
    check [PATH]                latest marker per tool: CURRENT / STALE /
                                MISSING (exit 1 if any is not CURRENT)
    passes                      tool x pass table, with per-pass counts
    verify                      chain integrity (exit 1 on a break)
    --selftest
"""

import datetime
import hashlib
import json
import os
import shlex
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LEDGER = os.path.join(HERE, "provenance_markers.jsonl")

PASSES = (
    ("P1", "noun->verb", "exact condition + temporal scope"),
    ("P2", "animacy", "relation both ways; coupled thing written as inert"),
    ("P3", "logic puzzle", "entailment: quantifier, middle term"),
    ("P4", "round trip", "every predicate place filled"),
    ("P5", "evidentiality", "witnessed / inferred / reported"),
)
PASS_IDS = tuple(p[0] for p in PASSES)
STATES = ("RUNS", "PARTIAL", "NOT_RUN", "UNDECLARED")
GENESIS = "GENESIS"
TIMEOUT = 300  # [CHOICE 1] seconds per stamped run


class MarkerRefused(Exception):
    pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _line_sha(line):
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


def read_ledger(ledger):
    if not os.path.exists(ledger):
        return []
    with open(ledger, encoding="utf-8") as f:
        return [ln.rstrip("\n") for ln in f if ln.strip()]


def basis_resolves(basis, root):
    """'path:line' -> (ok, reason). The line must exist and be non-blank."""
    if not basis or ":" not in basis:
        return False, "basis is not path:line"
    p, _, n = basis.rpartition(":")
    if not n.isdigit():
        return False, "line is not a number"
    full = os.path.join(root, p)
    if not os.path.isfile(full):
        return False, "basis file not found: %s" % p
    with open(full, encoding="utf-8", errors="replace") as f:
        lines = f.read().split("\n")
    k = int(n)
    if k < 1 or k > len(lines):
        return False, "line %d out of range (file has %d)" % (k, len(lines))
    if not lines[k - 1].strip():
        return False, "line %d is blank" % k
    return True, lines[k - 1].strip()[:80]


def parse_passes(specs, notes, root):
    """--pass P1=RUNS@file:line ... -> {P: {state, basis, note}}; refuses."""
    out = {}
    for spec in specs or []:
        if "=" not in spec:
            raise MarkerRefused("pass spec has no '=': %r" % spec)
        pid, _, rest = spec.partition("=")
        state, _, basis = rest.partition("@")
        if pid not in PASS_IDS:
            raise MarkerRefused("unknown pass %r (have %s)" % (pid, PASS_IDS))
        if state not in STATES:
            raise MarkerRefused("unknown state %r (have %s)" % (state, STATES))
        if pid in out:
            raise MarkerRefused("pass %s given twice" % pid)
        rec = {"state": state, "basis": basis or None, "note": None}
        if state in ("RUNS", "PARTIAL"):
            ok, why = basis_resolves(basis, root)
            if not ok:
                raise MarkerRefused("%s=%s needs a basis that resolves: %s"
                                    % (pid, state, why))
        elif basis:
            raise MarkerRefused("%s=%s carries a basis; only RUNS/PARTIAL do"
                                % (pid, state))
        out[pid] = rec
    for spec in notes or []:
        pid, _, text = spec.partition("=")
        if pid not in out:
            raise MarkerRefused("note for %s, which has no --pass" % pid)
        out[pid]["note"] = text.strip() or None
    for pid, rec in out.items():
        if rec["state"] == "PARTIAL" and not rec["note"]:
            raise MarkerRefused("%s=PARTIAL needs a note naming the missing half"
                                % pid)
    return out


def latest(rows, rel):
    for line in reversed(rows):
        r = json.loads(line)
        if r["path"] == rel:
            return r
    return None


def stamp(rel, how, by, cmd=None, pass_specs=None, notes=None,
          ledger=LEDGER, root=ROOT, now=None):
    if not how or not how.strip():
        raise MarkerRefused("how is empty: a marker says how the tool works")
    if not by or not by.strip():
        raise MarkerRefused("declared_by is empty")
    full = os.path.join(root, rel)
    if not os.path.isfile(full):
        raise MarkerRefused("tool not found: %s" % rel)
    passes = parse_passes(pass_specs, notes, root)
    rows = read_ledger(ledger)
    prev_marker = latest(rows, rel)
    for pid in PASS_IDS:
        if pid in passes:
            passes[pid]["inherited"] = False
        elif prev_marker and pid in prev_marker["passes"]:
            r = dict(prev_marker["passes"][pid])
            r["inherited"] = True
            passes[pid] = r
        else:
            passes[pid] = {"state": "UNDECLARED", "basis": None, "note": None,
                           "inherited": False}
    cmd = cmd or "python3 %s --selftest" % rel
    before = sha256_file(full)
    try:
        p = subprocess.run(shlex.split(cmd), cwd=root, capture_output=True,
                           text=True, timeout=TIMEOUT)
        code, text = p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        code, text = None, "TIMEOUT after %ds" % TIMEOUT
    after = sha256_file(full)
    if before != after:
        raise MarkerRefused("tool file changed during its own run; no marker")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    rec = {
        "path": rel,
        "sha256": before,
        "cmd": cmd,
        "exit": code,
        "last_line": lines[-1].strip()[:200] if lines else None,
        "ran_at": now or datetime.datetime.now(datetime.timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "how": how.strip(),
        "declared_by": by.strip(),
        "passes": passes,
        "prev": _line_sha(rows[-1]) if rows else GENESIS,
    }
    with open(ledger, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec


def verify(ledger=LEDGER):
    """[(index, problem)] for every break in the chain; [] if intact."""
    rows = read_ledger(ledger)
    bad = []
    for i, line in enumerate(rows):
        r = json.loads(line)
        want = _line_sha(rows[i - 1]) if i else GENESIS
        if r.get("prev") != want:
            bad.append((i, "prev does not match line %d" % (i - 1)))
    return bad


def check(ledger=LEDGER, root=ROOT, only=None):
    """{path: (status, marker)} for the latest marker of each tool."""
    rows = read_ledger(ledger)
    out = {}
    for line in rows:
        r = json.loads(line)
        out[r["path"]] = r
    res = {}
    for rel, r in sorted(out.items()):
        if only and rel != only:
            continue
        full = os.path.join(root, rel)
        if not os.path.isfile(full):
            res[rel] = ("MISSING", r)
        elif sha256_file(full) == r["sha256"]:
            res[rel] = ("CURRENT", r)
        else:
            res[rel] = ("STALE", r)
    if only and only not in res:
        res[only] = ("NEVER_STAMPED", None)
    return res


SYM = {"RUNS": "R", "PARTIAL": "p", "NOT_RUN": ".", "UNDECLARED": "?"}


def render_passes(ledger=LEDGER, root=ROOT):
    res = check(ledger, root)
    out = ["passes per tool, latest marker (R runs, p partial, . not run, "
           "? undeclared)", ""]
    for pid, name, forces in PASSES:
        out.append("  %s  %-14s %s" % (pid, name, forces))
    out.append("")
    out.append("  %-44s %s  %s" % ("tool", " ".join(PASS_IDS), "marker"))
    counts = {pid: {s: 0 for s in STATES} for pid in PASS_IDS}
    for rel, (status, r) in res.items():
        cells = []
        for pid in PASS_IDS:
            s = r["passes"][pid]["state"]
            counts[pid][s] += 1
            cells.append(" %s" % SYM[s] + " ")
        out.append("  %-44s %s  %s" % (rel, " ".join(cells), status))
    out.append("")
    for pid, name, _ in PASSES:
        c = counts[pid]
        out.append("  %s %-14s RUNS %d  PARTIAL %d  NOT_RUN %d  UNDECLARED %d"
                   % (pid, name, c["RUNS"], c["PARTIAL"], c["NOT_RUN"],
                      c["UNDECLARED"]))
        if res and c["RUNS"] == 0 and c["PARTIAL"] == 0:
            out.append("     -> no stamped tool runs %s, even in part" % pid)
    out.append("")
    out.append("  pass states are declarations (declared_by in each marker); "
               "only basis lines, hashes and the chain are checked here")
    return "\n".join(out)


def render_check(res):
    out = []
    for rel, (status, r) in res.items():
        if r is None:
            out.append("%-13s %s" % (status, rel))
            continue
        out.append("%-13s %s  sha %s  ran %s  exit %s" % (
            status, rel, r["sha256"][:12], r["ran_at"], r["exit"]))
        out.append("              how: %s" % r["how"])
        out.append("              cmd: %s   -> %s" % (r["cmd"], r["last_line"]))
        for pid in PASS_IDS:
            p = r["passes"][pid]
            if p["state"] in ("RUNS", "PARTIAL"):
                out.append("              %s %s @ %s%s" % (
                    pid, p["state"], p["basis"],
                    ("  (%s)" % p["note"]) if p.get("note") else ""))
    return "\n".join(out)


# ---------------------------------------------------------------- selftest

def selftest():
    fails = []
    n = [0]

    def ok(cond, label):
        n[0] += 1
        if not cond:
            fails.append(label)

    def refused(fn, label):
        try:
            fn()
        except MarkerRefused:
            ok(True, label)
            return
        ok(False, label + " (not refused)")

    with tempfile.TemporaryDirectory() as d:
        tool = os.path.join(d, "t.py")
        with open(tool, "w") as f:
            f.write("import sys\n# P5 lives here\nprint('checks: 3   failed: 0')\n")
        led = os.path.join(d, "ledger.jsonl")
        kw = dict(ledger=led, root=d, now="2026-01-01T00:00:00Z")

        refused(lambda: stamp("t.py", "", "me", **kw), "empty how refused")
        refused(lambda: stamp("t.py", "x", "", **kw), "empty by refused")
        refused(lambda: stamp("nope.py", "x", "me", **kw), "missing tool refused")
        refused(lambda: stamp("t.py", "x", "me", pass_specs=["P5=RUNS"], **kw),
                "RUNS without basis refused")
        refused(lambda: stamp("t.py", "x", "me",
                              pass_specs=["P5=RUNS@t.py:99"], **kw),
                "out-of-range basis refused")
        refused(lambda: stamp("t.py", "x", "me",
                              pass_specs=["P5=RUNS@t.py:4"], **kw),
                "blank-line basis refused")
        refused(lambda: stamp("t.py", "x", "me", pass_specs=["P9=RUNS@t.py:2"],
                              **kw), "unknown pass refused")
        refused(lambda: stamp("t.py", "x", "me", pass_specs=["P1=MAYBE"], **kw),
                "unknown state refused")
        refused(lambda: stamp("t.py", "x", "me",
                              pass_specs=["P1=PARTIAL@t.py:2"], **kw),
                "PARTIAL without note refused")
        refused(lambda: stamp("t.py", "x", "me",
                              pass_specs=["P1=NOT_RUN@t.py:2"], **kw),
                "NOT_RUN with basis refused")
        ok(read_ledger(led) == [], "no refused stamp wrote a line")

        r = stamp("t.py", "prints a count", "me",
                  pass_specs=["P5=RUNS@t.py:2", "P3=NOT_RUN"], **kw)
        ok(r["exit"] == 0, "exit recorded")
        ok(r["last_line"] == "checks: 3   failed: 0", "last line recorded")
        ok(r["prev"] == GENESIS, "first marker chains to GENESIS")
        ok(r["passes"]["P2"]["state"] == "UNDECLARED",
           "unspecified pass is UNDECLARED, not NOT_RUN")
        ok(r["passes"]["P3"]["state"] == "NOT_RUN", "declared NOT_RUN kept")
        ok(check(led, d)["t.py"][0] == "CURRENT", "unchanged file CURRENT")

        r2 = stamp("t.py", "prints a count", "me", **kw)
        ok(r2["passes"]["P5"]["state"] == "RUNS" and
           r2["passes"]["P5"]["inherited"], "declaration inherited, marked so")
        ok(r2["prev"] == _line_sha(read_ledger(led)[0]), "second marker chains")
        ok(verify(led) == [], "intact chain verifies")

        with open(tool, "a") as f:
            f.write("# edit\n")
        ok(check(led, d)["t.py"][0] == "STALE", "edited file STALE")
        ok(check(led, d, only="other.py")["other.py"][0] == "NEVER_STAMPED",
           "unknown tool NEVER_STAMPED")
        os.remove(tool)
        ok(check(led, d)["t.py"][0] == "MISSING", "removed file MISSING")

        rows = read_ledger(led)
        bad = json.loads(rows[0])
        bad["how"] = "tampered"
        with open(led, "w") as f:
            f.write(json.dumps(bad, sort_keys=True) + "\n" + rows[1] + "\n")
        ok(verify(led) != [], "tampered earlier line breaks the chain")

        selfmod = os.path.join(d, "m.py")
        with open(selfmod, "w") as f:
            f.write("open(__file__,'a').write('#x\\n')\n")
        led2 = os.path.join(d, "l2.jsonl")
        refused(lambda: stamp("m.py", "x", "me", ledger=led2, root=d),
                "tool that edits itself during its run refused")
        ok(read_ledger(led2) == [], "self-editing run wrote no marker")

        txt = render_passes(led2, d)
        ok("RUNS 0" in txt, "empty ledger renders zero counts")

    print("checks: %d   failed: %d" % (n[0], len(fails)))
    for f in fails:
        print("  FAIL", f)
    return 0 if not fails else 1


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--selftest":
        return selftest()
    cmd, rest = argv[0], argv[1:]
    if cmd == "stamp":
        if not rest:
            print("stamp needs PATH", file=sys.stderr)
            return 2
        rel, opts = rest[0], {"how": None, "by": None, "cmd": None}
        specs, notes, i = [], [], 1
        while i < len(rest):
            a = rest[i]
            if a in ("--how", "--by", "--cmd") and i + 1 < len(rest):
                opts[a[2:]] = rest[i + 1]
                i += 2
            elif a == "--pass" and i + 1 < len(rest):
                specs.append(rest[i + 1])
                i += 2
            elif a == "--note" and i + 1 < len(rest):
                notes.append(rest[i + 1])
                i += 2
            else:
                print("unknown or incomplete argument: %s" % a, file=sys.stderr)
                return 2
        try:
            r = stamp(rel, opts["how"], opts["by"], opts["cmd"], specs, notes)
        except MarkerRefused as e:
            print("REFUSED: %s" % e, file=sys.stderr)
            return 1
        print(render_check({rel: ("CURRENT", r)}))
        return 0
    if cmd == "check":
        res = check(only=rest[0] if rest else None)
        print(render_check(res))
        return 0 if all(s == "CURRENT" for s, _ in res.values()) else 1
    if cmd == "passes":
        print(render_passes())
        return 0
    if cmd == "verify":
        bad = verify()
        for i, why in bad:
            print("BREAK at line %d: %s" % (i, why))
        print("chain %s (%d lines)" % ("BROKEN" if bad else "intact",
                                       len(read_ledger(LEDGER))))
        return 1 if bad else 0
    print("unknown command: %s" % cmd, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
