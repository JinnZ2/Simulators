#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
validate.py -- every check the registry is held to, and the selftest that
plants a defect for each check and shows the check fires.

    pins        bundle/MANIFEST.sha256, bundle_pins.json, source/PINS.json:
                every pinned input re-hashed on every run
    manifest    registry/MANIFEST.json: a registry file edited by hand fails
    schema      every object against schema/registry.schema.json ($defs per
                type), every edge against $defs/EDGE
    claims      every claim value against its vocabulary list or type; an
                unlisted claim field is an error
    endpoints   every edge's (from type, to type) against x-edge-endpoints
    refs        every id a field names resolves to an object
    ledger      every EV-<row> verification equals the ledger's derived state
    statements  every corrected statement's needle occurs exactly once in its
                pinned file, at the line recorded
    configuration  every CHANGE names an NCR that lists it; every recode left
                a history entry carrying its CHANGE id; every audit NCR is
                flagged single-failure
    gaps        gaps are nodes: unlocated inputs, frames not loaded and
                unsearched disclosure records are UNREACHABLE, never blank;
                every graded case has a disclosure-record CONFLICT node
    rebuild     tools/build.py rebuilt in memory equals registry/ byte for
                byte (this also re-derives every grade and every statement
                value through tools/stats.py)
    report      REVISED_REPORT.md equals its template rendered from stats,
                and the template carries no bare count outside a {key}
    tools       symmetry, chain, gaps, who, reversals: each tool's checks()

Usage
    python3 tools/validate.py              all checks; exit 1 on any error
    python3 tools/validate.py --selftest   planted defects first (each check
                                           must fire), then all checks
Stdlib only.
"""

import copy
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reglib  # noqa: E402

CLAIM_VOCAB = {
    "direction": "direction", "action_direction": "direction",
    "outcome_direction": "direction", "direction_verb": "direction_verb",
    "direction_rel_bearer": "direction_rel_bearer",
    "cost_bearer": "cost_bearer", "cost_bearer_L": "cost_bearer",
    "cost_bearer_S": "cost_bearer", "cost_bearer_detail": "cost_bearer",
    "cost_group": "cost_group", "cost_group_L": "cost_group",
    "cost_group_S": "cost_group", "uncertainty": "uncertainty",
    "evidence_class": "evidence_class", "U_grade": "rus_U",
    "forcing_kind": "forcing_kind", "r1": "r1_flag", "r1_scope": "r1_scope",
    "r6_justification": "r6_justification", "mirror": "yes_no",
    "source_verified_flag": "source_verified_flag", "statute_compelled": "flag01",
}
CLAIM_LIST = ("evidence_class",)
CLAIM_NULLABLE = ("r6_justification",)
CLAIM_TYPES = {
    "forced_action": (bool,), "forced_outcome": (bool,), "r5": (bool,),
    "r6_blocking": (bool,), "r6b_loosening": (bool,),
    "r6_cycles": (int, type(None)), "us_score": (int,),
    "comparator_score": (int,), "divergence": (int,), "pair": (str,),
    "decision_type": (str,), "notice": (str,),
}
REPORT = os.path.join(reglib.FOLDER, "REVISED_REPORT.md")
TEMPLATE = os.path.join(reglib.FOLDER, "REVISED_REPORT.template.md")
TOOL_MODULES = ("symmetry", "chain", "gaps", "who", "reversals")


def schema_type(obj):
    return "case" if obj["type"] in ("DECISION", "NON_DECISION") else obj["type"]


# ---------------------------------------------------------------- checks

def c_pins(reg):
    bad = reglib.check_pins()
    return reglib.pinned_count(), ["pin %s: want %s got %s" % (p, w[:12], (g or "MISSING")[:12])
                                   for p, w, g in bad]


def c_manifest(reg):
    man = reglib.load_json(reglib.MANIFEST)
    return len(man["files"]), ["manifest %s" % x for x in reglib.check_manifest()]


def c_schema(reg):
    v = reglib.schema_validator()
    errs = []
    for oid in sorted(reg.objects):
        o = reg.objects[oid]
        for e in v.errors(o, {"$ref": "#/$defs/" + schema_type(o)}):
            errs.append("%s: %s" % (oid, e))
    for i, e in enumerate(reg.edges):
        for x in v.errors(e, {"$ref": "#/$defs/EDGE"}):
            errs.append("edge %d: %s" % (i, x))
    return len(reg.objects) + len(reg.edges), errs


def c_claims(reg):
    vocab = reglib.vocabulary()
    errs, n = [], 0
    for o in reg.cases():
        for field, c in sorted(o["claims"].items()):
            n += 1
            v = c["value"]
            if field in CLAIM_VOCAB:
                allowed = vocab[CLAIM_VOCAB[field]]["values"]
                vals = v if field in CLAIM_LIST else [v]
                if field in CLAIM_LIST and not isinstance(v, list):
                    errs.append("%s.%s: not a list" % (o["id"], field))
                    continue
                for x in vals:
                    if x is None and field in CLAIM_NULLABLE:
                        continue
                    if x not in allowed:
                        errs.append("%s.%s: %r not in %s" % (o["id"], field, x,
                                                            CLAIM_VOCAB[field]))
            elif field in CLAIM_TYPES:
                ts = CLAIM_TYPES[field]
                if type(v) not in ts:  # bool is not an int here
                    errs.append("%s.%s: %r is not %s" % (o["id"], field, v,
                                                        "/".join(t.__name__ for t in ts)))
            else:
                errs.append("%s.%s: claim field not listed in validate.py" % (o["id"], field))
            for h in c.get("history", []):
                n += 1
                if field in CLAIM_VOCAB:
                    allowed = vocab[CLAIM_VOCAB[field]]["values"]
                    if h["value"] not in allowed and not isinstance(h["value"], bool):
                        errs.append("%s.%s history: %r not in %s" % (
                            o["id"], field, h["value"], CLAIM_VOCAB[field]))
    return n, errs


def c_endpoints(reg):
    schema = reglib.load_json(reglib.SCHEMA)
    ends = schema["x-edge-endpoints"]
    errs = []
    for e in reg.edges:
        a, b = reg.objects.get(e["from"]), reg.objects.get(e["to"])
        if a is None or b is None:
            errs.append("edge %s %s -> %s: unknown end" % (e["type"], e["from"], e["to"]))
            continue
        if [a["type"], b["type"]] not in ends.get(e["type"], []):
            errs.append("edge %s %s(%s) -> %s(%s): pair not allowed" % (
                e["type"], e["from"], a["type"], e["to"], b["type"]))
    return len(reg.edges), errs


REF_FIELDS = {
    "EVIDENCE": ("sources",), "SOURCE": (), "ACTOR": ("basis",),
    "CONFLICT": ("actor_id", "decision", "basis"), "OUTCOME": ("basis", "case"),
    "REVERSAL": ("from_case", "to_case", "initiator", "date_basis"),
    "ENDPOINT_ABSENCE": ("substance", "endpoint", "basis", "decisions"),
    "NCR": ("evidence", "statements", "changes"), "CHANGE": ("ncr",),
}


def c_refs(reg):
    errs, n = [], 0
    def chk(oid, field, val):
        vals = val if isinstance(val, list) else [val]
        for x in vals:
            if x is None:
                continue
            if x not in reg.objects:
                errs.append("%s.%s: %s unresolved" % (oid, field, x))
    for o in reg.objects.values():
        for f in REF_FIELDS.get(o["type"], ()):
            if f in o:
                n += 1
                chk(o["id"], f, o[f])
        if o["type"] == "REVERSAL":
            n += 1
            chk(o["id"], "harm_at_reversal.basis", o["harm_at_reversal"]["basis"])
        if o["type"] in ("DECISION", "NON_DECISION"):
            n += 1
            chk(o["id"], "authority_chain", o["authority_chain"])
            for f, c in o["claims"].items():
                if c.get("basis"):
                    chk(o["id"], f + ".basis", c["basis"])
                if c.get("source"):
                    chk(o["id"], f + ".source", c["source"])
                for h in c.get("history", []):
                    if h.get("change"):
                        chk(o["id"], f + ".history", h["change"])
    return n, errs


def c_ledger(reg):
    import ledger
    led = ledger.ledger()
    errs = []
    for rid, row in sorted(led.items()):
        o = reg.objects.get("EV-" + rid)
        if o is None:
            errs.append("ledger row %s has no evidence node" % rid)
            continue
        want = ledger.verification_of(row)
        if o["verification"] != want:
            errs.append("EV-%s: verification %s, ledger derives %s"
                        % (rid, o["verification"]["state"], want["state"]))
        if want["state"] != reglib.citation_state(row["reached"], row["queries"],
                                                  row["exists"], row["says"]):
            errs.append("EV-%s: state not the four-state rule's" % rid)
    return len(led), errs


def c_statements(reg):
    errs, n = [], 0
    for o in reg.of("EVIDENCE"):
        if o["kind"] != "statement":
            continue
        n += 1
        path = os.path.join(reglib.FOLDER, o["located"]["path"])
        text = open(path, "r", encoding="utf-8").read()
        k = text.count(o["statement"])
        if k != 1:
            errs.append("%s: needle occurs %d times" % (o["id"], k))
            continue
        line = text[:text.index(o["statement"])].count("\n") + 1
        if line != o["located"]["line"]:
            errs.append("%s: needle at line %d, recorded %d" % (o["id"], line, o["located"]["line"]))
        if "{" in o["registry_value"]:
            errs.append("%s: unfilled placeholder" % o["id"])
    return n, errs


def c_configuration(reg):
    errs, n = [], 0
    ncrs = {o["id"]: o for o in reg.of("NCR")}
    for ch in reg.of("CHANGE"):
        n += 1
        if ch["ncr"] and ch["id"] not in ncrs[ch["ncr"]]["changes"]:
            errs.append("%s names %s, which does not list it" % (ch["id"], ch["ncr"]))
        if ch["kind"] == "recode" and ch["field"] != "id":
            o = reg.objects[ch["object"]]
            hist = o["claims"][ch["field"]].get("history", [])
            if not any(h.get("change") == ch["id"] for h in hist):
                errs.append("%s: no history entry on %s.%s" % (ch["id"], ch["object"], ch["field"]))
    changes = {o["id"] for o in reg.of("CHANGE")}
    for nid, nc in sorted(ncrs.items()):
        n += 1
        for c in nc["changes"]:
            if c not in changes:
                errs.append("%s lists %s, not in the change log" % (nid, c))
        if not nc["reason"].strip():
            errs.append("%s: disposition without a reason" % nid)
        if nc["origin"] == "AUDIT_WO-REG-1" and not nc["single_failure"]:
            errs.append("%s: audit NCR not flagged single-failure" % nid)
    seqs = sorted(c["seq"] for c in reg.of("CHANGE"))
    if seqs != list(range(1, len(seqs) + 1)):
        errs.append("CHANGE seq not contiguous")
    return n, errs


def c_gaps(reg):
    errs, n = [], 0
    for o in reg.of("EVIDENCE"):
        if o["kind"] in ("unlocated_input", "gap") or o["id"].startswith("EV-U"):
            n += 1
            if o["verification"]["state"] != "UNREACHABLE":
                errs.append("%s: gap node is %s" % (o["id"], o["verification"]["state"]))
    graded = [o for o in reg.cases() if o["frame"] in ("A", "B", "C", "D", "E", "R8")]
    with_rec = {c["decision"] for c in reg.of("CONFLICT") if c["conflict_type"] == "disclosure_record"}
    for o in graded:
        n += 1
        if o["id"] not in with_rec:
            errs.append("%s: no disclosure-record CONFLICT node" % o["id"])
    for c in reg.of("CONFLICT"):
        if c["record_state"] == "UNREACHABLE" and c["basis"] and any(
                reg.objects[b]["verification"]["state"] in ("VERIFIED", "CORRECTED")
                for b in c["basis"]):
            errs.append("%s: UNREACHABLE with a located basis" % c["id"])
    for o in reg.of("SUBSTANCE", "ENDPOINT"):
        n += 1
        if o["id_state"] == "LOCAL_ONLY" and not o.get("gap"):
            errs.append("%s: LOCAL_ONLY id with no gap stated" % o["id"])
    return n, errs


def c_rebuild(reg):
    import build
    files = build.Builder().run()
    diffs = build.check(files)
    return len(files), ["rebuild differs: %s" % d for d in diffs]


# ---------------------------------------------------------------- report

PLACEHOLDER = re.compile(r"\{[a-z][A-Za-z0-9_.+\-]*\}")
ALLOWED_NUMBER = re.compile(  # specific forms first: alternation is leftmost-first
    r"(?:RUS-0\.\d+|NQA-1|RG \d+\.\d+|\bAB \d+\b|\b\d+ FR \d+|Pub\. L\. \d+-\d+|\d+ U\.S\.C\. \d+|\d+ CFR [\d.]+"
    r"|\d+ F\.4th \d+|\bv\d\b|section \d+|\u00a7\s?\d+|\b\d+(?:st|nd|rd|th)\b"
    r"|\b(?:1[89]|20)\d\d(?:-\d\d){0,2}\b"             # years and dates
    r"|[A-Z][A-Za-z_]*-?\d+[a-z]?(?:-\d+)*(?:\.\d+)?)")  # ids: A10, NCR-R6, CHG-N04-01, G036, U3, D5, M7, RG 1.28


def report_lint(text):
    """Digits in the template outside a {key} and outside an allowed pattern
    (ids, dates, legal citations) are bare numbers: an error."""
    errs = []
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("<!--"):
            continue
        s = re.sub(r"^#{1,6} \d+\.", "", line)          # section numbers in headings
        s = PLACEHOLDER.sub("", s)
        s = ALLOWED_NUMBER.sub("", s)
        for m in re.finditer(r"\d+(?:\.\d+)?", s):
            errs.append("template line %d: bare number %s" % (i, m.group()))
    return errs


def c_report(reg):
    if not os.path.exists(TEMPLATE):
        return 0, []
    import report
    tmpl = open(TEMPLATE, "r", encoding="utf-8").read()
    errs = report_lint(tmpl)
    for path, want in ((report.REPORT, report.render(reg, tmpl)),
                       (report.CHANGELOG, report.render_changelog(reg)),
                       (report.QA, report.render_qa(reg))):
        got = open(path, "r", encoding="utf-8").read() if os.path.exists(path) else None
        if got != want:
            errs.append("%s is not what tools/report.py renders from the registry"
                        % reglib.rel(path))
    return len(tmpl.splitlines()), errs


def c_tools(reg):
    errs, n = [], 0
    for name in TOOL_MODULES:
        path = os.path.join(HERE, name + ".py")
        if not os.path.exists(path):
            errs.append("tool %s.py missing" % name)
            continue
        mod = __import__(name)
        k, e = mod.checks(reg)
        n += k
        errs.extend("%s: %s" % (name, x) for x in e)
    return n, errs


CHECKS = [("pins", c_pins), ("manifest", c_manifest), ("schema", c_schema),
          ("claims", c_claims), ("endpoints", c_endpoints), ("refs", c_refs),
          ("ledger", c_ledger), ("statements", c_statements),
          ("configuration", c_configuration), ("gaps", c_gaps),
          ("rebuild", c_rebuild), ("report", c_report), ("tools", c_tools)]


def run_checks(only=None, quiet=False):
    try:
        reg = reglib.Registry()
    except reglib.RegistryError as e:
        print("registry  LOAD FAILED: %s" % e)
        return {"load": ["%s" % e]}
    results = {}
    for name, fn in CHECKS:
        if only and name not in only:
            continue
        try:
            n, errs = fn(reg)
        except Exception as e:  # a check that cannot run is a failure
            n, errs = 0, ["%s raised %s: %s" % (name, type(e).__name__, e)]
        results[name] = errs
        if not quiet:
            print("%-14s %5d checked  %s" % (name, n, "OK" if not errs else
                                              "%d ERROR(S)" % len(errs)))
            for e in errs[:8]:
                print("    " + e)
            if len(errs) > 8:
                print("    ... %d more" % (len(errs) - 8))
    return results


# ---------------------------------------------------------------- selftest

def _copy_folder():
    tmp = tempfile.mkdtemp(prefix="regsel-")
    dst = os.path.join(tmp, os.path.basename(reglib.FOLDER))
    shutil.copytree(reglib.FOLDER, dst, ignore=shutil.ignore_patterns("__pycache__"))
    # check_citations / effective_redundancy are imported from the repo
    for sib in ("tools", "effective-redundancy-audit"):
        src = os.path.join(reglib.REPO, sib)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(tmp, sib),
                            ignore=shutil.ignore_patterns("__pycache__"))
    return tmp, dst


def _run(folder, only):
    p = subprocess.run([sys.executable, "-I", os.path.join(folder, "tools", "validate.py"),
                        "--only", ",".join(only)],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       universal_newlines=True, timeout=900)
    return p.returncode, p.stdout


def _edit_json(path, fn):
    data = reglib.load_json(path)
    fn(data)
    reglib.dump_json(data, path)


def _edit_text(path, old, new):
    s = open(path, "r", encoding="utf-8").read()
    if s.count(old) < 1:
        raise RuntimeError("selftest anchor not found in %s: %r" % (path, old[:40]))
    open(path, "w", encoding="utf-8").write(s.replace(old, new, 1))


def _first(data, oid):
    return next(o for o in data if o["id"] == oid)


PLANTS = [
    # (name, check that must fire, function(folder))
    ("bundle byte changed", "pins",
     lambda d: open(os.path.join(d, "bundle", "source", "current", "epa_frame_2022.csv"), "a").write("\n")),
    ("registry file edited by hand", "manifest",
     lambda d: _edit_json(os.path.join(d, "registry", "outcomes.json"),
                          lambda x: x[0].update(date="1999"))),
    ("object missing a required field", "schema",
     lambda d: _edit_json(os.path.join(d, "registry", "reversals.json"),
                          lambda x: x[0].pop("mechanism"))),
    ("claim value outside its vocabulary", "claims",
     lambda d: _edit_json(os.path.join(d, "registry", "cases.json"),
                          lambda x: _first(x, "A01")["claims"]["direction"].update(value="sideways"))),
    ("edge with a disallowed type pair", "endpoints",
     lambda d: _edit_json(os.path.join(d, "registry", "edges.json"),
                          lambda x: x.append({"from": "A01", "to": "A02", "type": "cites",
                                              "status": "PROPOSED"}))),
    ("dangling reference", "refs",
     lambda d: _edit_json(os.path.join(d, "registry", "conflicts.json"),
                          lambda x: x[0].update(basis=["EV-NOPE"]))),
    ("evidence state not the ledger's", "ledger",
     lambda d: _edit_json(os.path.join(d, "registry", "evidence.json"),
                          lambda x: _first(x, "EV-G036")["verification"].update(state="UNREACHABLE"))),
    ("statement line moved", "statements",
     lambda d: _edit_json(os.path.join(d, "registry", "evidence.json"),
                          lambda x: _first(x, "ST-01")["located"].update(line=1))),
    ("CHANGE not listed by its NCR", "configuration",
     lambda d: _edit_json(os.path.join(d, "registry", "ncr.json"),
                          lambda x: _first(x, "NCR-R6").update(changes=[]))),
    ("gap node read as located", "gaps",
     lambda d: _edit_json(os.path.join(d, "registry", "evidence.json"),
                          lambda x: _first(x, "EV-U01")["verification"].update(state="VERIFIED"))),
    ("CHANGE whose from-value the source does not carry", "rebuild",
     lambda d: _edit_text(os.path.join(d, "tools", "curation_ncr.py"),
                          '("CHG-N03-01", "recode", "B06", "statute_compelled", "1", "0",',
                          '("CHG-N03-01", "recode", "B06", "statute_compelled", "0", "1",')),
    ("ledger result edited, registry not rebuilt", "rebuild",
     lambda d: _edit_text(os.path.join(d, "verification", "results_g2.txt"),
                          "G036 | Y", "G036 | N")),
]


def selftest():
    print("== selftest: planted defects (each named check must fire)")
    fired = 0
    tmp, base = _copy_folder()
    try:
        # the clean copy must pass first, or a plant proves nothing
        code, out = _run(base, [c for c, _ in CHECKS if c not in ("report", "tools")])
        clean = code == 0
        print("%-52s %s" % ("clean copy passes", "OK" if clean else "FAIL"))
        if not clean:
            print(out)
        for name, check, plant in PLANTS:
            t2 = tempfile.mkdtemp(prefix="regsel-")
            for sib in os.listdir(tmp):
                shutil.copytree(os.path.join(tmp, sib), os.path.join(t2, sib))
            d = os.path.join(t2, os.path.basename(base))
            plant(d)
            code, out = _run(d, [check])
            ok = code != 0 and re.search(r"^%s\s+\d+ checked\s+\d+ ERROR" % re.escape(check),
                                         out, re.M) is not None
            fired += ok
            print("%-52s %-14s %s" % (name, check, "FIRED" if ok else "SILENT"))
            if not ok:
                print(out[-2000:])
            shutil.rmtree(t2, ignore_errors=True)
        lint = report_lint("12 of 33 rows; {n} cases; A10 in 2016 under 81 FR 53767")
        lint_ok = len(lint) == 2
        print("%-52s %-14s %s" % ("bare counts in a report template", "report",
                                  "FIRED" if lint_ok else "SILENT %s" % lint))
        fired += lint_ok
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    total = len(PLANTS) + 1
    print("planted %d   fired %d   clean copy %s" % (total, fired, "passes" if clean else "FAILS"))
    return fired == total and clean


def main(argv):
    only = None
    if "--only" in argv:
        only = argv[argv.index("--only") + 1].split(",")
    ok = True
    if "--selftest" in argv:
        ok = selftest()
        print("== real checks")
    res = run_checks(only)
    n_err = sum(len(e) for e in res.values())
    print("checks %d   errors %d" % (len(res), n_err))
    return 0 if ok and n_err == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
