"""
boundary.py -- the biomimicry boundary, kept visible and revisable.

CC0. Python >= 3.8, standard library only, no network.

Where does learning from nature stop: organisms, single cells, crystals, concrete,
reacting chemicals? Science has not settled it. This tool does not settle it either.
It reads boundary/boundary.json (axes, cases, candidate lines), evaluates every
line over every case in three values, and refuses to pick one line.

    Y              -> True
    N              -> False
    PARTIAL / CONTESTED / UNKNOWN -> BORDER   (Kleene logic: N wins an AND, Y wins an OR)

Membership is IN / OUT / BORDER. BORDER is a reading, never rounded to IN or OUT.

Changes are logged, not overwritten. boundary/changelog.jsonl is append-only and
hash-chained; each entry stores the sha256 of the table it leaves behind. A table
that does not match the last entry is an UNLOGGED edit.

Run:
  python3 tools/boundary.py render            # the matrix
  python3 tools/boundary.py verify            # validate table + changelog; exit 1 on a defect
  python3 tools/boundary.py log --by NAME --change "..." --reason "..."
                                              # after editing boundary.json, record the edit
  python3 tools/boundary.py --selftest
"""

import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "boundary/boundary.json"
LOG = ROOT / "boundary/changelog.jsonl"
RENDERED = ROOT / "boundary/BOUNDARY_TABLE.txt"
BORDER_VALUES = ("PARTIAL", "CONTESTED", "UNKNOWN")


# --- three-valued rules -------------------------------------------------------

def cell(value):
    if value == "Y":
        return True
    if value == "N":
        return False
    if value in BORDER_VALUES:
        return None
    raise ValueError(f"value {value!r} not in the declared set")


def parse(rule, axes):
    """'a AND NOT b OR c' -> nested tuples. OR binds loosest, NOT tightest."""
    toks = re.findall(r"\(|\)|[A-Za-z_]+", rule)
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def take():
        pos[0] += 1
        return toks[pos[0] - 1]

    def atom():
        t = take()
        if t == "NOT":
            return ("NOT", atom())
        if t == "(":
            e = expr()
            if take() != ")":
                raise ValueError(f"unbalanced rule {rule!r}")
            return e
        if t not in axes:
            raise ValueError(f"rule {rule!r} names unknown axis {t!r}")
        return ("AXIS", t)

    def conj():
        e = atom()
        while peek() == "AND":
            take()
            e = ("AND", e, atom())
        return e

    def expr():
        e = conj()
        while peek() == "OR":
            take()
            e = ("OR", e, conj())
        return e

    tree = expr()
    if peek() is not None:
        raise ValueError(f"trailing tokens in rule {rule!r}")
    return tree


def evaluate(tree, case):
    op = tree[0]
    if op == "AXIS":
        return cell(case[tree[1]])
    if op == "NOT":
        v = evaluate(tree[1], case)
        return None if v is None else not v
    a, b = evaluate(tree[1], case), evaluate(tree[2], case)
    if op == "AND":
        if a is False or b is False:
            return False
        return None if (a is None or b is None) else True
    if a is True or b is True:          # OR
        return True
    return None if (a is None or b is None) else False


def membership(v):
    return {True: "IN", False: "OUT", None: "BORDER"}[v]


# --- table -------------------------------------------------------------------

def load(path=TABLE):
    return json.loads(path.read_text(encoding="utf-8"))


def table_sha256(data):
    canon = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canon.encode()).hexdigest()


def validate(data):
    problems = []
    axes = data["axes"]
    vals = set(data["values"])
    if set(vals) != {"Y", "N"} | set(BORDER_VALUES):
        problems.append(f"value set {sorted(vals)} differs from the tool's {['N', 'Y'] + list(BORDER_VALUES)}")
    if data.get("adopted_line") is not None and data["adopted_line"] not in data["lines"]:
        problems.append(f"adopted_line {data['adopted_line']!r} is not a declared line")
    for name, line in data["lines"].items():
        try:
            parse(line["rule"], axes)
        except ValueError as exc:
            problems.append(f"{name}: {exc}")
    ids = [c["id"] for c in data["cases"]]
    problems += [f"duplicate case id {i}" for i in sorted(set(ids)) if ids.count(i) > 1]
    for c in data["cases"]:
        for a in axes:
            if a not in c:
                problems.append(f"{c['id']} has no value for axis {a}")
            elif c[a] not in vals:
                problems.append(f"{c['id']}.{a} = {c[a]!r} not in the value set")
        if any(c.get(a) in BORDER_VALUES for a in axes) and not c.get("basis"):
            problems.append(f"{c['id']} has a border value and no basis")
    return problems


def matrix(data):
    trees = {n: parse(l["rule"], data["axes"]) for n, l in data["lines"].items()}
    return {c["id"]: {n: membership(evaluate(t, c)) for n, t in trees.items()}
            for c in data["cases"]}


def render(data):
    m = matrix(data)
    lines = list(data["lines"])
    short = [n.split("_", 1)[0] for n in lines]
    out = ["BIOMIMICRY BOUNDARY  status " + data["status"]
           + "  adopted line: " + str(data["adopted_line"]),
           "table sha256 " + table_sha256(data)[:16],
           "",
           "LINES (candidate; none adopted)"]
    for n in lines:
        out.append(f"  {n:<20} {data['lines'][n]['rule']}")
        out.append(f"  {'':<20} reads as: {data['lines'][n]['reads_as']}")
    out += ["", "AXES (per case; Y / N / PARTIAL / CONTESTED / UNKNOWN)"]
    ax = list(data["axes"])
    abbrev = [a[:6] for a in ax]
    w = max(len(c["name"]) for c in data["cases"])
    w = min(w, 52)
    head = f"  {'id':<4} {'case':<{w}} " + " ".join(f"{a:>9}" for a in abbrev)
    out.append(head)
    for c in data["cases"]:
        mark = "*" if c["in_hb24"] else " "
        out.append(f"  {c['id']:<4}{mark}{c['name'][:w]:<{w}} "
                   + " ".join(f"{c[a]:>9}" for a in ax))
    out += ["  (* = one of the six HB-24 rows in H0 §6)", "",
            "MEMBERSHIP (IN / OUT / BORDER)"]
    out.append(f"  {'id':<4} {'case':<{w}} " + " ".join(f"{s:>7}" for s in short))
    for c in data["cases"]:
        mark = "*" if c["in_hb24"] else " "
        out.append(f"  {c['id']:<4}{mark}{c['name'][:w]:<{w}} "
                   + " ".join(f"{m[c['id']][n]:>7}" for n in lines))
    out += ["", "PER LINE                 IN  BORDER  OUT   HB-24 rows not IN"]
    for n in lines:
        col = [m[c["id"]][n] for c in data["cases"]]
        miss = [c["id"] for c in data["cases"] if c["in_hb24"] and m[c["id"]][n] != "IN"]
        out.append(f"  {n:<20} {col.count('IN'):>4} {col.count('BORDER'):>7} "
                   f"{col.count('OUT'):>4}   {', '.join(miss) or '-'}")
    stable = [c["id"] for c in data["cases"] if len(set(m[c["id"]].values())) == 1]
    out += ["", f"cases with one reading under every line: {', '.join(stable) or 'none'}",
            f"cases whose membership depends on the line: "
            f"{len(data['cases']) - len(stable)} of {len(data['cases'])}"]
    return "\n".join(out) + "\n"


# --- changelog ----------------------------------------------------------------

def entry_sha256(entry):
    body = {k: v for k, v in entry.items() if k != "entry_sha256"}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()


def read_log(path=LOG):
    if not path.is_file():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def verify_log(entries, current_sha):
    problems = []
    prev = None
    for i, e in enumerate(entries, 1):
        if e.get("seq") != i:
            problems.append(f"entry {i} has seq {e.get('seq')}")
        if e.get("prev_sha256") != prev:
            problems.append(f"entry {i} breaks the chain")
        if entry_sha256(e) != e.get("entry_sha256"):
            problems.append(f"entry {i} was edited after it was written")
        for k in ("date", "by", "change", "reason", "table_sha256"):
            if not e.get(k):
                problems.append(f"entry {i} has no {k}")
        prev = e.get("entry_sha256")
    if not entries:
        problems.append("changelog is empty")
    elif entries[-1].get("table_sha256") != current_sha:
        problems.append("UNLOGGED EDIT: boundary.json differs from the table the last "
                        "changelog entry records; run tools/boundary.py log")
    return problems


def append_log(by, change, reason, path=LOG, table=TABLE, date=None):
    data = load(table)
    problems = validate(data)
    if problems:
        raise SystemExit("refused: table invalid: " + "; ".join(problems))
    entries = read_log(path)
    entry = {"seq": len(entries) + 1,
             "date": date or datetime.date.today().isoformat(),
             "by": by, "change": change, "reason": reason,
             "table_sha256": table_sha256(data),
             "prev_sha256": entries[-1]["entry_sha256"] if entries else None}
    if entries and entries[-1]["table_sha256"] == entry["table_sha256"]:
        raise SystemExit("refused: the table did not change since the last entry")
    entry["entry_sha256"] = entry_sha256(entry)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    RENDERED.write_text(render(data), encoding="utf-8") if table == TABLE else None
    return entry


def verify(table=TABLE, log=LOG, rendered=RENDERED):
    data = load(table)
    problems = validate(data)
    problems += verify_log(read_log(log), table_sha256(data))
    if rendered.is_file() and rendered.read_text(encoding="utf-8") != render(data):
        problems.append("BOUNDARY_TABLE.txt is stale; rerun tools/boundary.py render --write")
    return problems


# --- selftest ------------------------------------------------------------------

def selftest():
    import tempfile
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))

    axes = {"a": "", "b": ""}
    case = lambda a, b: {"a": a, "b": b}
    ok("Y AND Y = IN", membership(evaluate(parse("a AND b", axes), case("Y", "Y"))) == "IN")
    ok("N AND border = OUT (N wins)", membership(evaluate(parse("a AND b", axes), case("N", "CONTESTED"))) == "OUT")
    ok("Y AND border = BORDER", membership(evaluate(parse("a AND b", axes), case("Y", "PARTIAL"))) == "BORDER")
    ok("Y OR border = IN (Y wins)", membership(evaluate(parse("a OR b", axes), case("Y", "UNKNOWN"))) == "IN")
    ok("NOT border = BORDER", membership(evaluate(parse("NOT a", axes), case("UNKNOWN", "Y"))) == "BORDER")
    ok("NOT N = IN", membership(evaluate(parse("NOT a", axes), case("N", "Y"))) == "IN")
    ok("precedence: a OR b AND NOT b", membership(evaluate(parse("a OR b AND NOT b", axes), case("N", "Y"))) == "OUT")
    try:
        parse("a AND c", axes)
        ok("unknown axis refused", False)
    except ValueError:
        ok("unknown axis refused", True)
    try:
        cell("MAYBE")
        ok("undeclared value refused", False)
    except ValueError:
        ok("undeclared value refused", True)

    data = load()
    ok("shipped table validates", validate(data) == [])
    ok("no line adopted", data["adopted_line"] is None and data["status"] == "UNSETTLED")
    m = matrix(data)
    ok("membership values stay in IN / OUT / BORDER",
       all(set(m[c][n] for c in m) <= {"IN", "OUT", "BORDER"} for n in data["lines"]))
    ok("BORDER occurs (the boundary is visibly unsettled)",
       any(v == "BORDER" for row_ in m.values() for v in row_.values()))

    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        t, l = d / "b.json", d / "c.jsonl"
        t.write_text(json.dumps(data), encoding="utf-8")
        ok("empty log is a defect", verify_log([], table_sha256(data)) != [])
        append_log("selftest", "initial", "fixture", path=l, table=t, date="2000-01-01")
        ok("logged table verifies", verify_log(read_log(l), table_sha256(load(t))) == [])
        edited = load(t)
        edited["cases"][0]["living"] = "CONTESTED"
        t.write_text(json.dumps(edited), encoding="utf-8")
        ok("unlogged edit detected",
           any("UNLOGGED" in p for p in verify_log(read_log(l), table_sha256(load(t)))))
        append_log("selftest", "C01.living Y -> CONTESTED", "fixture", path=l, table=t, date="2000-01-02")
        ok("logged edit verifies", verify_log(read_log(l), table_sha256(load(t))) == [])
        ents = read_log(l)
        ents[0]["reason"] = "rewritten"
        ok("rewritten history detected",
           any("edited after" in p for p in verify_log(ents, table_sha256(load(t)))))
        try:
            append_log("selftest", "nothing", "fixture", path=l, table=t)
            ok("no-op entry refused", False)
        except SystemExit:
            ok("no-op entry refused", True)

    failed = [n for n, c in checks if not c]
    for n, c in checks:
        print(("PASS " if c else "FAIL ") + n)
    print(f"checks: {len(checks)}   failed: {len(failed)}")
    return 1 if failed else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    cmd = argv[1] if len(argv) > 1 else "render"
    if cmd == "render":
        txt = render(load())
        if "--write" in argv:
            RENDERED.write_text(txt, encoding="utf-8")
        print(txt, end="")
        return 0
    if cmd == "verify":
        problems = verify()
        print("\n".join(problems) if problems else "boundary: table valid, changelog intact, render current")
        return 1 if problems else 0
    if cmd == "log":
        def arg(k):
            if k not in argv or argv.index(k) + 1 >= len(argv):
                raise SystemExit(f"log needs {k}")
            return argv[argv.index(k) + 1]
        e = append_log(arg("--by"), arg("--change"), arg("--reason"))
        print(f"logged entry {e['seq']} table {e['table_sha256'][:16]}")
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
