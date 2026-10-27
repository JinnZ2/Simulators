# SPDX-License-Identifier: CC0-1.0
"""Operator follow-up of 2026-09-30, after the A-6.3 build (b10392f).

Landed verbatim as FOLLOWUP_2026-09-30.md and committed ALONE at EXPECTED_COMMIT_FU before this
module existed.  Additive: no earlier module is edited; every earlier module is read by import.
Item 2 (the Part B branch) is a git operation on another branch and is reported in the README.

  1  resolved_url: the address stays as written in the source; resolved_url is filled only when a
     fetch returns bytes, and the fetch decides the scheme.  Until then the input reads NO_SPAN.
  3  module pins: blob hashes at a NAMED commit, compared against the working file; every later
     edit is declared (blob, commit, reason).  Working-tree status is not read.
  4  caller constants: an AST scan of every call to a status gate; a literal True / False / None
     bound to a gate parameter is a FLAG, each module FLAG carries a declared disposition, and
     the consequence of the constant is computed by flipping it.
  5  sample shifts: the lines the A-6.3 item 8 move changed in two pinned samples, declared, and
     checked against the git diff between the two named commits.
"""
import ast
import datetime
import hashlib
import inspect
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import gate_state_a21 as G21     # noqa: E402
import sourcing_a62 as P         # noqa: E402
import standing_a61 as S61       # noqa: E402
import verification_a63 as V     # noqa: E402

EXPECTED_COMMIT_FU = "d2f35e7"
FOLLOWUP_FILE = "FOLLOWUP_2026-09-30.md"
RESOLVE_STORE = "resolve_store.json"

CHOICES = {
    106: "a fetch 'returns bytes' iff it completes with HTTP status 200 and a body of length > 0; a "
         "proxy refusal (403 at CONNECT) or any other status carries no source bytes, whatever body it has",
    107: "an address with no scheme is tried as https then http, first success wins; an address that "
         "carries a scheme is tried as written and nothing else",
    108: "the status gates scanned are verification_a63.MUTATION_GATES plus gate_a63; a call is "
         "resolved by the called name (bare or attribute), not by import tracking",
    109: "a FLAG in a test file is a fixture exercising the gate by construction and is reported apart; "
         "every FLAG in a module file carries a declared disposition or reads UNDISPOSED",
    110: "the pin commit is f6d385c (the A-6.2 instrument commit, the last before any A-6.3 edit); "
         "the pinned set is the ten A-1..A-6.2 modules",
}


def _full(ref):
    try:
        return subprocess.run(["git", "rev-parse", ref], cwd=HERE, capture_output=True, text=True,
                              timeout=30).stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def _load(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return []
    return json.load(open(p, encoding="utf-8")).get("records", [])


# ------------------------------------------------------------ 1: resolved_url ---

SCHEMES = ("https", "http")   # [CHOICE 107]
_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*://", re.I)


def candidates(address):
    """[CHOICE 107] the urls a fetch may try; the address itself is never rewritten."""
    if not isinstance(address, str) or not address:
        return []
    if _SCHEME.match(address):
        return [address]
    return ["%s://%s" % (s, address) for s in SCHEMES]


def returned_bytes(attempt):
    """[CHOICE 106]"""
    return attempt.get("status") == 200 and (attempt.get("n_bytes") or 0) > 0


def default_fetch(url, timeout=20):
    """Live fetch through the environment's proxy.  Keeps the length and sha256 of the body, not the body."""
    import ssl
    import urllib.request
    import urllib.error
    ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "route-independence"}),
                                    timeout=timeout, context=ctx) as r:
            body = r.read()
            return {"status": r.status, "n_bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                    "failure": None}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "n_bytes": None, "sha256": None, "failure": "HTTP %s" % e.code}
    except Exception as e:   # every other outcome is recorded as it came back
        return {"status": None, "n_bytes": None, "sha256": None, "failure": "%s: %s" % (type(e).__name__, e)}


def resolve(source_id, address, fetch, at=None, fetched_by="unspecified"):
    """Item 1: try the candidates in order; resolved_url is the first that returned bytes, else None."""
    attempts = []
    resolved = None
    for url in candidates(address):
        a = dict(fetch(url), url=url)
        attempts.append(a)
        if returned_bytes(a):
            resolved = url
            break
    return {"source_id": source_id, "address": address, "attempts": attempts, "resolved_url": resolved,
            "attempted_at": at or datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fetched_by": fetched_by}


def record_resolution(rec):
    p = os.path.join(HERE, RESOLVE_STORE)
    recs = _load(RESOLVE_STORE) + [rec]
    with open(p, "w", encoding="utf-8") as f:
        json.dump({"note": "resolution attempts [CHOICE 106] [CHOICE 107]; append-only; the address is copied "
                           "from the source table as written", "records": recs}, f, indent=1)
        f.write("\n")


RESOLVE_IDS = ("W-1a", "W-2a")


def address_state(source_id, store=None):
    """The address as the source table carries it, the latest resolution, and the input state."""
    store = _load(RESOLVE_STORE) if store is None else store
    address = G21.SOURCES21[source_id].get("url")
    mine = [r for r in store if r.get("source_id") == source_id and r.get("address") == address]
    last = mine[-1] if mine else None
    st = V.input_status(source_id, P.CARRIED)
    return {"source_id": source_id, "address": address, "form": V.location_form(address),
            "resolved_url": last["resolved_url"] if last else None, "n_attempts_on_file": len(mine),
            "last": last, "status": st["status"]}


# -------------------------------------------------------------- 3: module pins ---

PIN_COMMIT = "f6d385c"   # [CHOICE 110]
PINS = (   # module, blob sha1 at PIN_COMMIT (git hash-object)
    ("settlement_split.py", "6b175f9073998438e9e1090d67b3f775b37c8ea2"),
    ("gate_state.py", "c41b0a352c6be3f5552bb9888066e664343933a8"),
    ("gate_state_a21.py", "78e31bb4aa6bef3f8499a3a5d1c472010150edef"),
    ("thermal_gates.py", "03a98f4dd623ab3b6fe4239152ebf4c3e3cc1f29"),
    ("repairs_a31.py", "bd6ae2437cc2e78ed45078d2af6b3d4568f99523"),
    ("chains_a4.py", "3672486bfcd407efbc4c0b490562eb8d34416ada"),
    ("termini_a5.py", "ebaee8eaee075808028ceb950f07a9737dcbb18b"),
    ("eligibility_a6.py", "7b23bedcb28fd52d489576c4bb341a4513af53eb"),
    ("standing_a61.py", "4cb9aefe9e3df0fd3fdff911a35c86195ff87080"),
    ("sourcing_a62.py", "bc39d57af6545b7c58fe3c445b447f34da6c1a18"),
)
DECLARED_EDITS = (   # module, blob after the edit, commit, reason
    ("gate_state_a21.py", "28b7e24d7c95ab8b8a4d7af197c90175b960d098", "b10392f",
     "A-6.3 item 8: W-1a / W-2a address moved from the text into a url field"),
    ("standing_a61.py", "8c7c05c5215e9cef25ee149f399a95f6e3519c7a", "b10392f",
     "A-6.3 item 3: CE-4e status note (coding rule GEOGRAPHIC, undeclared when delivered)"),
)
PINNED, DECLARED_EDIT, UNDECLARED_EDIT, MISSING = "PINNED", "DECLARED_EDIT", "UNDECLARED_EDIT", "MISSING"
NOT_TESTABLE = "NOT_TESTABLE"


def blob_sha1(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def pin_check(pins=PINS, edits=DECLARED_EDITS, read=None):
    """Item 3: the working file's blob against the pin and the declared edits; no git status is read."""
    read = read or (lambda m: open(os.path.join(HERE, m), "rb").read() if os.path.exists(os.path.join(HERE, m))
                    else None)
    out = []
    for mod, pin in pins:
        data = read(mod)
        if data is None:
            out.append({"module": mod, "pin": pin, "live": None, "state": MISSING, "edit": None})
            continue
        live = blob_sha1(data)
        ed = [e for e in edits if e[0] == mod and e[1] == live]
        state = PINNED if live == pin else (DECLARED_EDIT if ed else UNDECLARED_EDIT)
        out.append({"module": mod, "pin": pin, "live": live, "state": state, "edit": ed[0] if ed else None})
    return out


def history_check(pins=PINS, edits=DECLARED_EDITS):
    """Each pin and each declared blob is what git holds at the named commit for that path."""
    base = _full(PIN_COMMIT)
    if base is None:
        return {"status": NOT_TESTABLE, "reason": "pin commit %s not reachable" % PIN_COMMIT, "rows": []}
    rows = []
    for mod, pin in pins:
        rows.append(("pin", mod, PIN_COMMIT, _full("%s:route-independence/%s" % (PIN_COMMIT, mod)) == pin))
    for mod, blob, commit, _ in edits:
        rows.append(("edit", mod, commit, _full("%s:route-independence/%s" % (commit, mod)) == blob))
    return {"status": "CHECKED", "rows": rows, "all_match": all(r[3] for r in rows)}


def weak_check_reads_clean(mod="gate_state_a21.py"):
    """The replaced test: git diff --quiet HEAD over a module whose edit is committed returns 0."""
    try:
        return subprocess.run(["git", "diff", "--quiet", "HEAD", "--", mod], cwd=HERE, timeout=30).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return None


def pin_fail_fixture():
    """Drop the declared gate_state_a21 edit: the pin check fires; the weak check still reads clean."""
    rows = pin_check(edits=tuple(e for e in DECLARED_EDITS if e[0] != "gate_state_a21.py"))
    st = [r["state"] for r in rows if r["module"] == "gate_state_a21.py"][0]
    return {"pin_state": st, "weak_clean": weak_check_reads_clean(), "fires": st == UNDECLARED_EDIT}


# ---------------------------------------------------------- 4: caller constants ---

def gate_table():
    """[CHOICE 108] name -> function."""
    tab = dict((name.split(".")[1], getter()) for name, getter, _ in V.MUTATION_GATES)
    tab["gate_a63"] = V.gate_a63
    return tab


def _call_name(node):
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return None


def _literal(node):
    return isinstance(node, ast.Constant) and node.value is None or \
        (isinstance(node, ast.Constant) and isinstance(node.value, bool))


def scan_source(text, fname, gates=None):
    """Every literal True / False / None bound to a parameter of a status gate at a call site."""
    gates = gate_table() if gates is None else gates
    tree = ast.parse(text)
    parents = {}
    for p in ast.walk(tree):
        for c in ast.iter_child_nodes(p):
            parents[c] = p
    flags = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        if name not in gates:
            continue
        params = [p for p in inspect.signature(gates[name]).parameters]
        bound = []
        for i, a in enumerate(node.args):
            if isinstance(a, ast.Starred):
                break
            if i < len(params):
                bound.append((params[i], a))
        for k in node.keywords:
            if k.arg is not None:
                bound.append((k.arg, k.value))
        encl = parents.get(node)
        while encl is not None and not isinstance(encl, (ast.FunctionDef, ast.Lambda)):
            encl = parents.get(encl)
        where = encl.name if isinstance(encl, ast.FunctionDef) else ("<lambda>" if encl else "<module>")
        for param, a in bound:
            if _literal(a):
                flags.append({"file": fname, "line": node.lineno, "caller": where, "gate": name,
                              "param": param, "value": a.value,
                              "kind": "TEST" if os.path.basename(fname).startswith("test_") else "MODULE"})
    return flags


def scan_folder(folder=HERE):
    out = []
    for fn in sorted(os.listdir(folder)):
        if fn.endswith(".py"):
            out += scan_source(open(os.path.join(folder, fn), encoding="utf-8").read(), fn)
    return out


DISPOSITIONS = (   # [CHOICE 109] (file, caller, gate, param, value) -> disposition; consequence key if computed
    ("verification_a63.py", "rerun_a63", "gate_core", "enumerated", True,
     "every re-gated row passes enumerated=True; the enumeration state is not read per row", "rerun_a63"),
    ("sourcing_a62.py", "rerun", "gate_a62", "enumerated", True,
     "every re-gated row passes enumerated=True; the enumeration state is not read per row", "rerun_a62"),
    ("sourcing_a62.py", "score_rescoped", "gate_a62", "enumerated", True,
     "E-A6-3 over the enumerated forms of 83.11(b)(1)-(2): enumerated by construction (RIN_147)", None),
    ("sourcing_a62.py", "score_rescoped", "gate_a62", "single_aggregate", False,
     "E-A6-3 is scored per form, not over one aggregate case", None),
    ("sourcing_a62.py", "fail_fixture", "gate_a62", "enumerated", True, "fail fixture: holds the gate's other inputs fixed", None),
    ("sourcing_a62.py", "fail_fixture", "gate_a62", "single_aggregate", False, "fail fixture: holds the gate's other inputs fixed", None),
    ("sourcing_a62.py", "fail_fixture", "gate_status", "falsifier_cases_enumerated", True, "fail fixture: holds the gate's other inputs fixed", None),
    ("standing_a61.py", "prior_sweep", "gate_status", "falsifier_cases_enumerated", True,
     "RIN_146: the erratum sweep's aggregate condition was a constant here", "prior_sweep"),
    ("standing_a61.py", "score_e_a6_3", "gate_status", "falsifier_cases_enumerated", True,
     "reached only when the caller declares the list complete (complete=True)", None),
    ("standing_a61.py", "check_expectations", "gate_status", "falsifier_cases_enumerated", False,
     "E-A6.1-3: no enumerated case can fire the falsifier (RIN_136) [CHOICE 81]", None),
    ("standing_a61.py", "check_expectations", "gate_status", "falsifier_cases_enumerated", True,
     "E-A6.1-1: the falsifier cell is reachable on the constructed row (RIN_136)", None),
    ("verification_a63.py", "placeholder_fixture", "gate_a62", "enumerated", True, "fail fixture: holds the gate's other inputs fixed", None),
    ("verification_a63.py", "placeholder_fixture", "gate_a62", "single_aggregate", False, "fail fixture: holds the gate's other inputs fixed", None),
    ("followup_a63.py", "consequence", "gate_core", "enumerated", False, "this module: the flipped constant is the measurement", None),
    ("followup_a63.py", "consequence", "gate_a62", "enumerated", False, "this module: the flipped constant is the measurement", None),
    ("followup_a63.py", "consequence", "gate_status", "falsifier_cases_enumerated", False,
     "this module: the flipped constant is the measurement", None),
)
UNDISPOSED = "UNDISPOSED"


def disposed(flags, table=DISPOSITIONS):
    out = []
    for f in flags:
        hit = [d for d in table if d[:5] == (f["file"], f["caller"], f["gate"], f["param"], f["value"])]
        if f["kind"] == "TEST":
            out.append(dict(f, disposition="fixture exercising the gate [CHOICE 109]", consequence=None))
        elif hit:
            out.append(dict(f, disposition=hit[0][5], consequence=hit[0][6]))
        else:
            out.append(dict(f, disposition=UNDISPOSED, consequence=None))
    return out


def consequence(key):
    """Flip the constant the caller passed and count the rows whose verdict moves."""
    if key == "rerun_a63":
        rows = V.rerun_a63()
        moved = [r["row"] for r in rows
                 if V.gate_core(r["raw"], [s["status"] for s in r["sources"]], False,
                                P.AGGREGATE_READING[r["row"]][0]) != r["new"]]
        return {"n_rows": len(rows), "moved": moved, "flipped_to": False}
    if key == "rerun_a62":
        rows = P.rerun()
        moved = [r["row"] for r in rows
                 if P.gate_a62(r["raw"], r["inputs"], False, P.AGGREGATE_READING[r["row"]][0]) != r["new"]]
        return {"n_rows": len(rows), "moved": moved, "flipped_to": False}
    if key == "prior_sweep":
        rows = S61.prior_sweep()["rows"]
        moved = [r["row"] for r in rows if S61.gate_status(r["raw"], r["grades"], False) != r["gated"]]
        return {"n_rows": len(rows), "moved": moved, "flipped_to": False}
    return None


PLANT = "import verification_a63 as V\n\ndef f(raw, st, e):\n    V.gate_core(raw, st, False)\n" \
        "    V.gate_core(raw, st, e)\n    V.gate_core(raw, st, enumerated=None)\n    gate_core(raw, st, True, e)\n"


def scan_null():
    f = scan_source(PLANT, "planted.py")
    return {"n": len(f), "values": [(x["line"], x["param"], x["value"]) for x in f]}


# ------------------------------------------------------------ 5: sample shifts ---

SHIFT_FROM, SHIFT_TO = "f6d385c", "b10392f"
SAMPLE_SHIFTS = (   # sample, old line numbers, new line numbers, reason
    ("samples/gate_state_a21.sample.txt", (5, 6), (5, 6),
     "A-6.3 item 8: the W-1a and W-2a text columns no longer carry the address; it moved to the url field"),
    ("samples/sourcing_a62.sample.txt", (46, 47, 48, 49), (46, 47, 48, 49),
     "A-6.3 item 8: 'locator in text' reads False on E-A2.1-1 / E-A2.1-2 for W-1a and W-2a; the address left "
     "the text; url, date, span, hash unchanged (all False)"),
)
_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def diff_lines(path, a=SHIFT_FROM, b=SHIFT_TO):
    try:
        r = subprocess.run(["git", "diff", "--unified=0", a, b, "--", "route-independence/" + path],
                           cwd=os.path.dirname(HERE),
                           capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    old, new = [], []
    for ln in r.stdout.splitlines():
        m = _HUNK.match(ln)
        if m:
            o, oc, n, nc = int(m.group(1)), int(m.group(2) or 1), int(m.group(3)), int(m.group(4) or 1)
            old += list(range(o, o + oc))
            new += list(range(n, n + nc))
    return tuple(old), tuple(new)


def shift_check():
    if _full(SHIFT_FROM) is None or _full(SHIFT_TO) is None:
        return {"status": NOT_TESTABLE, "rows": []}
    rows = []
    for path, old, new, reason in SAMPLE_SHIFTS:
        d = diff_lines(path)
        live = open(os.path.join(HERE, path), "rb").read()
        rows.append({"sample": path, "declared": (old, new), "diff": d, "match": d == (old, new),
                     "live_equals_to": blob_sha1(live) == _full("%s:route-independence/%s" % (SHIFT_TO, path)),
                     "reason": reason})
    return {"status": "CHECKED", "rows": rows}


# ------------------------------------------------------------------ render ---

def _short(failure):
    """Render-only summary of a recorded failure; the store keeps the full text."""
    if not failure:
        return ""
    m = re.search(r"Tunnel connection failed: (\d+)", failure)
    if m:
        return "proxy refused CONNECT (%s)" % m.group(1)
    return failure.split(":")[0]


def render(out=None):
    out = sys.stdout if out is None else out
    wr = out.write
    wr("Operator follow-up 2026-09-30 after A-6.3; order landed at %s; nothing edited in earlier modules\n\n"
       % EXPECTED_COMMIT_FU)
    wr("1  resolved_url [CHOICE 106] [CHOICE 107]\n")
    for sid in RESOLVE_IDS:
        a = address_state(sid)
        wr("   %s  address %r (as written, form %s)  resolved_url %s  attempts on file %d  status %s\n"
           % (sid, a["address"], a["form"], a["resolved_url"], a["n_attempts_on_file"], a["status"]))
        if a["last"]:
            wr("        last attempt %s by %s:\n" % (a["last"]["attempted_at"], a["last"]["fetched_by"]))
            for t in a["last"]["attempts"]:
                wr("          %-70s status %s  bytes %s  %s\n" % (t["url"], t["status"], t["n_bytes"],
                                                                _short(t["failure"])))
    wr("\n3  module pins at %s [CHOICE 110]\n" % PIN_COMMIT)
    for r in pin_check():
        wr("   %-20s %-16s %s\n" % (r["module"], r["state"], ("edit at %s: %s" % (r["edit"][2], r["edit"][3]))
                                   if r["edit"] else ""))
    h = history_check()
    wr("   history: %s%s\n" % (h["status"], (", every pin and declared blob matches git at its commit: %s"
                                            % h["all_match"]) if h["rows"] else ""))
    ff = pin_fail_fixture()
    wr("   fail fixture: declared edit removed -> %s; the replaced diff-against-HEAD check reads clean: %s\n"
       % (ff["pin_state"], ff["weak_clean"]))
    wr("\n4  caller constants [CHOICE 108] [CHOICE 109]\n")
    flags = disposed(scan_folder())
    mod = [f for f in flags if f["kind"] == "MODULE"]
    wr("   flags: %d in modules, %d in tests, %d undisposed\n"
       % (len(mod), len(flags) - len(mod), sum(1 for f in flags if f["disposition"] == UNDISPOSED)))
    for f in mod:
        wr("   FLAG %s:%d %s -> %s(%s=%s)\n        %s\n" % (f["file"], f["line"], f["caller"], f["gate"], f["param"],
                                                       f["value"], f["disposition"]))
    for key in ("rerun_a63", "rerun_a62", "prior_sweep"):
        c = consequence(key)
        wr("   consequence %s: flip to %s moves %d of %d rows %s\n" % (key, c["flipped_to"], len(c["moved"]),
                                                                   c["n_rows"], c["moved"]))
    n = scan_null()
    wr("   null: planted source, %d flags at %s\n" % (n["n"], n["values"]))
    wr("\n5  sample shifts %s -> %s\n" % (SHIFT_FROM, SHIFT_TO))
    s = shift_check()
    for r in s["rows"]:
        wr("   %-36s declared lines %s  diff matches %s  live sample equals %s's %s\n        %s\n"
           % (r["sample"], list(r["declared"][1]), r["match"], SHIFT_TO, r["live_equals_to"], r["reason"]))
    if not s["rows"]:
        wr("   %s\n" % s["status"])


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("followup_a63 has no selftest; run python3 test_followup_a63.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    if argv[:1] == ["resolve"]:
        for sid in RESOLVE_IDS:
            rec = resolve(sid, G21.SOURCES21[sid]["url"], default_fetch, fetched_by="followup_a63 resolve (urllib, "
                                                                                    "environment proxy)")
            record_resolution(rec)
            print(sid, rec["resolved_url"], [(t["url"], t["status"], t["failure"]) for t in rec["attempts"]])
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
