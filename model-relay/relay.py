"""Check RELAY_LOG.md: one row per model drop. CC0, stdlib only.

States per row:
  OK          every check passes
  STALE       the artifact's sha256 no longer starts with sha12
  MISSING     the artifact path is not in the tree
  MALFORMED   a field is empty, out of vocabulary, or a parent is unknown
A row is never dropped from the report.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOG = os.path.join(HERE, "RELAY_LOG.md")
COLS = ["id", "landed", "model", "product", "artifact", "sha12", "parent",
        "relay", "relay_basis", "boundary", "audit"]
RELAY = {"SPEC_ONLY", "EXTENDED", "CALLED", "REBUILT", "INDEPENDENT",
         "UNASSESSED"}
NEEDS_PARENT = {"EXTENDED", "CALLED", "REBUILT"}


def parse(text):
    rows = []
    for line in text.splitlines():
        if not line.startswith("| R"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(dict(zip(COLS, cells)) if len(cells) == len(COLS)
                    else {"id": cells[0], "_ncols": len(cells)})
    return rows


def check(rows, root=ROOT):
    seen, out = set(), []
    for r in rows:
        why = []
        if "_ncols" in r:
            why.append("has %d columns, want %d" % (r["_ncols"], len(COLS)))
        else:
            empty = [c for c in COLS if not r[c]]
            if empty:
                why.append("empty: " + ",".join(empty))
            if r["relay"] not in RELAY:
                why.append("relay not in vocabulary: " + r["relay"])
            if r["parent"] != "-" and r["parent"] not in seen:
                why.append("parent not an earlier row: " + r["parent"])
            if r["relay"] in NEEDS_PARENT and r["parent"] == "-":
                why.append(r["relay"] + " needs a parent")
        if why:
            out.append((r["id"], "MALFORMED", "; ".join(why)))
        else:
            p = os.path.join(root, r["artifact"])
            if not os.path.isfile(p):
                out.append((r["id"], "MISSING", r["artifact"]))
            else:
                h = hashlib.sha256(open(p, "rb").read()).hexdigest()
                st = "OK" if h.startswith(r["sha12"]) else "STALE"
                out.append((r["id"], st, h[:12] if st == "STALE" else ""))
        seen.add(r["id"])
    return out


def render(rows, res):
    lines = ["model-relay: %d rows" % len(rows)]
    for rid, st, note in res:
        lines.append("  %-5s %-9s %s" % (rid, st, note))
    by = {}
    for r in rows:
        if "relay" in r:
            by.setdefault(r["model"], []).append(r["relay"])
    lines.append("relay by model (counts, no ranking):")
    for m in sorted(by):
        c = {}
        for x in by[m]:
            c[x] = c.get(x, 0) + 1
        lines.append("  %-10s %s" % (m, ", ".join(
            "%s %d" % kv for kv in sorted(c.items()))))
    return "\n".join(lines)


def selftest():
    import tempfile
    n = [0]

    def ok(cond, msg):
        n[0] += 1
        if not cond:
            raise SystemExit("FAIL: " + msg)
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "a.txt"), "w").write("x")
        h = hashlib.sha256(b"x").hexdigest()[:12]
        good = "| R1 | d | M | P | a.txt | %s | - | INDEPENDENT | b | none | - |" % h
        res = check(parse(good), d)
        ok(res == [("R1", "OK", "")], "good row reads OK")
        res = check(parse(good.replace(h, "0" * 12)), d)
        ok(res[0][1] == "STALE", "changed hash reads STALE")
        res = check(parse(good.replace("a.txt", "b.txt")), d)
        ok(res[0][1] == "MISSING", "absent file reads MISSING")
        res = check(parse(good.replace("INDEPENDENT", "BORROWED")), d)
        ok(res[0][1] == "MALFORMED", "out-of-vocabulary relay refused")
        res = check(parse(good.replace("| - | INDEPENDENT", "| - | EXTENDED")), d)
        ok(res[0][1] == "MALFORMED", "EXTENDED with no parent refused")
        res = check(parse(good.replace("| - | INDEPENDENT", "| R9 | INDEPENDENT")), d)
        ok(res[0][1] == "MALFORMED", "unknown parent refused")
        res = check(parse(good.replace("| b |", "|  |")), d)
        ok(res[0][1] == "MALFORMED", "empty field refused")
        res = check(parse(good + "\n| R2 | short |"), d)
        ok(len(res) == 2 and res[1][1] == "MALFORMED", "short row kept, not dropped")
    real = parse(open(LOG).read())
    ok(len(real) >= 6, "log parses")
    print("selftest: %d checks, 0 failed" % n[0])


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        rows = parse(open(LOG).read())
        res = check(rows)
        print(render(rows, res))
        sys.exit(0 if all(s == "OK" for _, s, _ in res) else 1)
