#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
build_index.py -- the generator for INSTRUMENT-INDEX.tsv (INDEX-SPEC.md).

    repos on disk --> unit rule per repo --> one row per instrument
                          |                      |
                          |          header (in-file, preferred)
                          |          override (index-overrides.json, fallback)
                          |          neither  -> UNRATED, LISTED ANYWAY
                          v                      v
                   absent repo -> NOT-SCANNED row, never silently omitted
                                                 |
                                                 v
                          TSV (13 columns, one line per instrument)
                          + build report: axis check, size check, drift,
                            refused overrides, rated share

What it does: derives what can be derived (id, repo, path, sizes, the
commit scanned), reads what was declared (header or override), and refuses
a declaration that is malformed rather than degrading it. What it does NOT
do: it does not classify an instrument from its text. A row nobody
declared reads UNRATED on every declared column. A word list deciding
input shape would be nonidentity-census T1-1 one level up.

The axis falsifier from INDEX-SPEC.md runs on every build and is printed:
more than 70% of RATED rows carrying CLAIM as their only input_shape fires
it. Rated share is printed beside it, because a HELD verdict over a small
rated denominator is a weak verdict and the reader should see the
denominator.

Choices the spec left open are numbered, printed by --choices, and cited
where taken.

CC0. Stdlib only. Parses under Python 3.9. No network.
"""

import io
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(os.path.dirname(HERE))   # parent of Simulators/

COLUMNS = ("id", "name", "repo", "path", "input_shape", "catches",
           "load_bytes", "load_tok_est", "run_cost", "run_basis", "status",
           "gate", "built_against")

INPUT_SHAPES = ("CLAIM", "FALSIFIER", "CATEGORY-SET", "NUMBER", "ABSENCE",
                "CORPUS", "DECISION", "DOCUMENT", "AGENT-OUTPUT")
RUN_COSTS = ("TRIVIAL", "LINEAR", "QUADRATIC", "CORPUS", "EXTERNAL",
             "UNRATED")
RUN_BASES = ("measured", "counted-from-source", "author-estimate")
STATUSES = ("OBSERVED", "DERIVED", "PROPOSED")
GATES = ("PASSED", "FAILED", "UNRUN")

UNRATED = "UNRATED"
NOT_SCANNED = "NOT-SCANNED"

AXIS_THRESHOLD = 0.70          # from INDEX-SPEC.md, AXIS RISK
SIZE_TARGET_BYTES = 40 * 1024  # from INDEX-SPEC.md, design constraints
ROW_TARGET = 90

CHOICES = {
    1: "UNIT OF INSTRUMENT is a per-repo rule, declared in REPO_RULES: "
       "Simulators = one row per top-level folder plus one per tools/*.py; "
       "method-layer = one row per module; chain-position-detectability = "
       "one row per work order plus the checker. A repo with no rule gets "
       "the DEFAULT rule (top-level folders + top-level .py) and the report "
       "says so.",
    2: "load_bytes for a FOLDER unit is the sum of its top-level .py and .md "
       "files; samples/, subfolders and data are excluded. An upper bound on "
       "the folder's entry documents, a lower bound on its tree.",
    3: "header WINS over override when both are present. A field where the "
       "two disagree is recorded as DRIFT in the build report and the header "
       "value is used; the override is not silently dropped.",
    4: "a MALFORMED override (unknown enum, run_cost without run_basis, "
       "unknown key) REFUSES the build (exit 1) naming the key and field. "
       "Degrading it to UNRATED would let a typo read as an honest absence.",
    5: "an absent repo produces one row: path NOT-SCANNED, every declared and "
       "derived column UNRATED or NOT-SCANNED. Present in the TSV so a reader "
       "of the file alone sees the gap; also printed in the report.",
    6: "built_against is `git rev-parse --short=12 HEAD`, with `+dirty` when "
       "tracked or untracked changes exist outside instrument-index/ itself. "
       "Fallback when not a git checkout: mtime of the newest scanned file. "
       "The hash names the commit the scan READ, which is the parent of any "
       "commit that lands the TSV.",
    7: "the generator EXCLUDES its own folder (instrument-index/) from the "
       "Simulators scan. Indexing itself would make load_bytes depend on the "
       "TSV it is writing (UNI_010's loop). The exclusion is printed.",
    8: "the axis check is computed over RATED rows only, and the rated share "
       "(rated / total) is printed beside the verdict. Under some rated floor "
       "the verdict is NOT_EVALUABLE; the floor is 1 (any rated row), because "
       "the spec sets none and a stipulated floor would be one more constant.",
    9: "name falls back to the first `# ` heading of README.md (folder) or of "
       "the file (document), then to the filename stem. Never to prose.",
}

# --- per-repo unit rules ([CHOICE 1]) ----------------------------------------

REPO_RULES = {
    "Simulators": {
        "units": [("dir", "."), ("file", "tools")],
        "exclude_dirs": {"docs", "legacy", "tests", "instrument-index",
                         ".github", ".git", "__pycache__", "samples"},
        "file_glob": ".py",
        "exclude_files": {"__init__.py"},
    },
    "method-layer": {
        "units": [("file", "."), ("file", "premise-traceability")],
        "exclude_dirs": {"tests", ".git", "__pycache__"},
        "file_glob": ".py",
        "exclude_files": {"__init__.py"},
    },
    "chain-position-detectability": {
        "units": [("file", "work-orders"), ("file", "tools")],
        "exclude_dirs": {".git", "__pycache__"},
        "file_glob": None,          # set per unit below
        "file_prefix": {"work-orders": "WO-"},
        "file_suffix": {"work-orders": ".md", "tools": ".py"},
        "exclude_files": {"README.md", "__init__.py"},
    },
}

DEFAULT_RULE = {
    "units": [("dir", "."), ("file", ".")],
    "exclude_dirs": {"tests", ".git", "__pycache__", "docs", "samples"},
    "file_glob": ".py",
    "exclude_files": {"__init__.py"},
}


class BuildRefused(Exception):
    """Raised when a declaration is malformed. [CHOICE 4]"""


# --- header parsing ----------------------------------------------------------

_HDR = re.compile(
    r"^\s*(?:#|<!--)\s*(INSTRUMENT|INPUT|CATCHES|RUN-COST|STATUS|GATE)"
    r":\s*(.*?)\s*(?:-->)?\s*$")
HEADER_SCAN_LINES = 80


def parse_header(text):
    """Read the in-file header block from the first HEADER_SCAN_LINES lines.
    Returns {} when no INSTRUMENT: line is present. The block is read as
    comment lines in .py and as `# KEY:` or `<!-- KEY: -->` lines in .md.

    The comment marker is REQUIRED. The first build had it optional and a
    work order's prose line `INSTRUMENT: the 1977 actor-observer paradigm`
    (line 69 of a delivered document) read as a header block. A header is
    a comment addressed to the generator; a sentence in the body is not."""
    found = {}
    for i, line in enumerate(text.splitlines()):
        if i >= HEADER_SCAN_LINES:
            break
        m = _HDR.match(line)
        if m:
            found.setdefault(m.group(1), m.group(2).strip())
    if "INSTRUMENT" not in found:
        return {}
    out = {"name": found["INSTRUMENT"]}
    if "INPUT" in found:
        out["input_shape"] = found["INPUT"]
    if "CATCHES" in found:
        out["catches"] = found["CATCHES"]
    if "RUN-COST" in found:
        cost, basis = split_run_cost(found["RUN-COST"])
        out["run_cost"] = cost
        if basis is not None:
            out["run_basis"] = basis
    if "STATUS" in found:
        out["status"] = found["STATUS"]
    if "GATE" in found:
        out["gate"] = found["GATE"]
    return out


def split_run_cost(value):
    """`TRIVIAL (author-estimate)` -> ("TRIVIAL", "author-estimate");
    `UNRATED` -> ("UNRATED", None); `LINEAR` -> ("LINEAR", None), which
    validate() then refuses for want of a basis."""
    m = re.match(r"^\s*([A-Z\-]+)\s*(?:\(\s*([a-z\-]+)\s*\))?\s*$", value)
    if not m:
        return value.strip(), None
    return m.group(1), m.group(2)


# --- validation ([CHOICE 4]) -------------------------------------------------

DECLARABLE = ("name", "input_shape", "catches", "run_cost", "run_basis",
              "status", "gate")
OVERRIDE_META = ("basis", "note")     # who/how the override was entered


def validate(decl, where):
    """Check a declaration dict against the enums. Raises BuildRefused
    naming the key and the field. A declaration may be partial; what it
    declares must be well-formed."""
    for k in decl:
        if k not in DECLARABLE and k not in OVERRIDE_META:
            raise BuildRefused("%s: unknown field %r" % (where, k))
    for k, v in decl.items():
        if not isinstance(v, str):
            raise BuildRefused("%s: field %r is not a string" % (where, k))
        if "\t" in v or "\n" in v:
            raise BuildRefused("%s: field %r carries a tab or newline; one "
                               "line per row is the TSV contract" % (where, k))
    shape = decl.get("input_shape")
    if shape is not None and shape != UNRATED:
        parts = shape.split("|")
        for p in parts:
            if p not in INPUT_SHAPES:
                raise BuildRefused("%s: input_shape %r not in enum" % (where, p))
        if len(set(parts)) != len(parts):
            raise BuildRefused("%s: input_shape repeats a value" % where)
    cost = decl.get("run_cost")
    if cost is not None:
        if cost not in RUN_COSTS:
            raise BuildRefused("%s: run_cost %r not in enum" % (where, cost))
        if cost != UNRATED and not decl.get("run_basis"):
            raise BuildRefused("%s: run_cost %s with no run_basis -- an "
                               "estimate wearing a number" % (where, cost))
    basis = decl.get("run_basis")
    if basis is not None and basis not in RUN_BASES:
        raise BuildRefused("%s: run_basis %r not in %r"
                           % (where, basis, RUN_BASES))
    if basis is not None and (cost is None or cost == UNRATED):
        raise BuildRefused("%s: run_basis given with run_cost %s -- a basis "
                           "for nothing" % (where, cost))
    st = decl.get("status")
    if st is not None and st not in STATUSES:
        raise BuildRefused("%s: status %r not in enum" % (where, st))
    g = decl.get("gate")
    if g is not None and g not in GATES:
        raise BuildRefused("%s: gate %r not in enum" % (where, g))
    return decl


def load_overrides(path):
    if not path or not os.path.exists(path):
        return {}
    with io.open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise BuildRefused("%s: overrides must be an object keyed by "
                           "repo/path" % path)
    for key, decl in data.items():
        if key.startswith("_"):
            continue
        if not isinstance(decl, dict):
            raise BuildRefused("%s: override %r is not an object" % (path, key))
        validate(decl, "override %s" % key)
    return {k: v for k, v in data.items() if not k.startswith("_")}


# --- unit enumeration --------------------------------------------------------

def _listdir(p):
    try:
        return sorted(os.listdir(p))
    except OSError:
        return []


def enumerate_units(repo_root, rule):
    """Yield (kind, relpath) for one repo under its rule. kind is 'dir' or
    'file'. relpath uses '/' and folders carry a trailing '/'."""
    units = []
    for kind, sub in rule["units"]:
        base = repo_root if sub == "." else os.path.join(repo_root, sub)
        if not os.path.isdir(base):
            continue
        for entry in _listdir(base):
            full = os.path.join(base, entry)
            if kind == "dir":
                if not os.path.isdir(full) or entry in rule["exclude_dirs"] \
                        or entry.startswith("."):
                    continue
                units.append(("dir", entry + "/"))
            else:
                if not os.path.isfile(full) or entry in rule["exclude_files"]:
                    continue
                suffix = rule.get("file_suffix", {}).get(sub, rule["file_glob"])
                prefix = rule.get("file_prefix", {}).get(sub, "")
                if suffix and not entry.endswith(suffix):
                    continue
                if prefix and not entry.startswith(prefix):
                    continue
                rel = entry if sub == "." else sub + "/" + entry
                units.append(("file", rel))
    return units


def slug(repo, relpath):
    """id = <repo-lower>:<path with / -> . and extension dropped>."""
    p = relpath.rstrip("/")
    p = re.sub(r"\.(py|md)$", "", p)
    p = p.replace("/", ".")
    return "%s:%s" % (repo.lower(), p)


def entry_files(repo_root, kind, relpath):
    """Files whose bytes count toward load_bytes and whose text is scanned
    for a header. [CHOICE 2]"""
    if kind == "file":
        return [os.path.join(repo_root, relpath)]
    folder = os.path.join(repo_root, relpath.rstrip("/"))
    names = _listdir(folder)
    readme = [n for n in names if n == "README.md"]
    pys = [n for n in names if n.endswith(".py")]
    mds = [n for n in names if n.endswith(".md") and n != "README.md"]
    return [os.path.join(folder, n) for n in readme + pys + mds
            if os.path.isfile(os.path.join(folder, n))]


def read_text(path):
    try:
        with io.open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def first_heading(text):
    for line in text.splitlines()[:HEADER_SCAN_LINES]:
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m and not _HDR.match(line):
            return m.group(1)
    return None


def built_against(repo_root, scanned_files):
    """[CHOICE 6]"""
    try:
        h = subprocess.run(["git", "-C", repo_root, "rev-parse",
                            "--short=12", "HEAD"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=20)
        if h.returncode == 0:
            sha = h.stdout.decode().strip()
            st = subprocess.run(["git", "-C", repo_root, "status",
                                 "--porcelain"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=20)
            dirty = any(
                ln.strip() and not ln[3:].startswith("instrument-index/")
                for ln in st.stdout.decode().splitlines())
            return sha + ("+dirty" if dirty else "")
    except (OSError, subprocess.SubprocessError):
        pass
    newest = 0
    for f in scanned_files:
        try:
            newest = max(newest, os.path.getmtime(f))
        except OSError:
            pass
    return "mtime:" + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(newest))


# --- row assembly ------------------------------------------------------------

def make_row(repo, kind, relpath, files, header, override, drift_out):
    decl = {}
    src = {}
    for k, v in (override or {}).items():
        if k in DECLARABLE:
            decl[k] = v
            src[k] = "override"
    for k, v in (header or {}).items():
        if k in decl and decl[k] != v:
            drift_out.append((slug(repo, relpath), k, v, decl[k]))   # [CHOICE 3]
        decl[k] = v
        src[k] = "header"
    validate({k: v for k, v in decl.items()}, "row %s" % slug(repo, relpath))
    size = 0
    for f in files:
        try:
            size += os.path.getsize(f)
        except OSError:
            pass
    name = decl.get("name")
    if not name:                                                   # [CHOICE 9]
        # A heading is a markdown construct. A `# ---- results ---` banner
        # in a .py file is a comment, and the first build read one as a name.
        md = [f for f in files if f.endswith(".md")]
        head_text = read_text(md[0]) if md else ""
        name = first_heading(head_text) or \
            os.path.basename(relpath.rstrip("/")).rsplit(".", 1)[0]
    row = {
        "id": slug(repo, relpath),
        "name": name,
        "repo": repo,
        "path": relpath,
        "input_shape": decl.get("input_shape", UNRATED),
        "catches": decl.get("catches", UNRATED),
        "load_bytes": str(size),
        "load_tok_est": str(size // 4),
        "run_cost": decl.get("run_cost", UNRATED),
        "run_basis": decl.get("run_basis", UNRATED),
        "status": decl.get("status", UNRATED),
        "gate": decl.get("gate", "UNRUN"),
        "built_against": "",     # filled per repo after the scan
    }
    return row, src


def not_scanned_row(repo):
    """[CHOICE 5]"""
    return {"id": "%s:%s" % (repo.lower(), NOT_SCANNED), "name": NOT_SCANNED,
            "repo": repo, "path": NOT_SCANNED, "input_shape": UNRATED,
            "catches": UNRATED, "load_bytes": UNRATED,
            "load_tok_est": UNRATED, "run_cost": UNRATED,
            "run_basis": UNRATED, "status": UNRATED, "gate": UNRATED,
            "built_against": NOT_SCANNED}


def build(root, repos, overrides):
    """Scan every named repo under root. Returns (rows, report_dict)."""
    rows = []
    report = {"repos": {}, "drift": [], "default_rule": [],
              "header_rows": 0, "override_rows": 0, "unrated_rows": 0,
              "excluded_self": False}
    for repo in repos:
        repo_root = os.path.join(root, repo)
        if not os.path.isdir(repo_root):
            rows.append(not_scanned_row(repo))
            report["repos"][repo] = {"state": NOT_SCANNED, "rows": 0}
            continue
        rule = REPO_RULES.get(repo)
        if rule is None:
            rule = DEFAULT_RULE
            report["default_rule"].append(repo)
        if repo == "Simulators":
            report["excluded_self"] = True                      # [CHOICE 7]
        repo_rows = []
        scanned = []
        for kind, rel in enumerate_units(repo_root, rule):
            files = entry_files(repo_root, kind, rel)
            scanned.extend(files)
            header = {}
            for f in files:
                header = parse_header(read_text(f))
                if header:
                    break
            if header:
                validate(header, "header in %s/%s" % (repo, rel))
            override = overrides.get("%s/%s" % (repo, rel))
            row, src = make_row(repo, kind, rel, files, header, override,
                                report["drift"])
            if any(v == "header" for v in src.values()):
                report["header_rows"] += 1
            elif src:
                report["override_rows"] += 1
            else:
                report["unrated_rows"] += 1
            repo_rows.append(row)
        ba = built_against(repo_root, scanned)
        for r in repo_rows:
            r["built_against"] = ba
        rows.extend(repo_rows)
        report["repos"][repo] = {"state": "SCANNED", "rows": len(repo_rows),
                                 "built_against": ba}
    rows.sort(key=lambda r: r["id"])
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        dup = sorted({i for i in ids if ids.count(i) > 1})
        raise BuildRefused("duplicate ids: %s" % dup)
    return rows, report


# --- the axis check ----------------------------------------------------------

def claim_only_share(shapes):
    """Fraction of RATED input_shape values that are exactly CLAIM (not
    CLAIM|something). UNRATED values are excluded from the denominator.
    None when nothing is rated -- an empty denominator is not a share of
    zero. Registered in tools/known_answer.py."""
    rated = [s for s in shapes if s and s != UNRATED]
    if not rated:
        return None
    only = sum(1 for s in rated if s == "CLAIM")
    return only / float(len(rated))


def axis_check(rows):
    """[CHOICE 8]"""
    shapes = [r["input_shape"] for r in rows if r["path"] != NOT_SCANNED]
    rated = [s for s in shapes if s != UNRATED]
    share = claim_only_share(shapes)
    dist = {}
    for s in rated:
        for p in s.split("|"):
            dist[p] = dist.get(p, 0) + 1
    if share is None:
        verdict = "NOT_EVALUABLE"
    elif share > AXIS_THRESHOLD:
        verdict = "AXIS_FALSIFIER_FIRED"
    else:
        verdict = "AXIS_HELD"
    return {"verdict": verdict, "claim_only_share": share,
            "rated": len(rated), "total": len(shapes),
            "rated_share": (len(rated) / float(len(shapes))) if shapes else None,
            "threshold": AXIS_THRESHOLD, "distribution": dist}


# --- TSV ----------------------------------------------------------------------

def to_tsv(rows):
    lines = ["\t".join(COLUMNS)]
    for r in rows:
        vals = []
        for c in COLUMNS:
            v = r[c]
            if "\t" in v or "\n" in v or "\r" in v:
                raise BuildRefused("row %s field %s carries a tab or newline"
                                   % (r["id"], c))
            vals.append(v)
        lines.append("\t".join(vals))
    return "\n".join(lines) + "\n"


def read_tsv(text):
    """Load the index whole. Refuses a row with the wrong column count
    rather than shifting fields."""
    lines = [ln for ln in text.splitlines() if ln != ""]
    if not lines or lines[0].split("\t") != list(COLUMNS):
        raise BuildRefused("TSV header does not match COLUMNS")
    out = []
    for i, ln in enumerate(lines[1:], start=2):
        parts = ln.split("\t")
        if len(parts) != len(COLUMNS):
            raise BuildRefused("TSV line %d has %d columns, expected %d"
                               % (i, len(parts), len(COLUMNS)))
        out.append(dict(zip(COLUMNS, parts)))
    return out


def size_check(tsv_text, n_rows):
    b = len(tsv_text.encode("utf-8"))
    return {"bytes": b, "rows": n_rows, "target_bytes": SIZE_TARGET_BYTES,
            "target_rows": ROW_TARGET,
            "verdict": "WITHIN" if b <= SIZE_TARGET_BYTES else "OVER",
            "bytes_per_row": (b / float(n_rows)) if n_rows else None}


# --- report -------------------------------------------------------------------

def render_report(rows, report, tsv_text, out_path):
    ax = axis_check(rows)
    sz = size_check(tsv_text, len(rows))
    L = []
    L.append("INSTRUMENT-INDEX build report")
    L.append("=" * 60)
    L.append("output: %s" % out_path)
    L.append("")
    L.append("REPOS")
    for repo, st in report["repos"].items():
        if st["state"] == NOT_SCANNED:
            L.append("  %-32s %s   (absent on disk; one NOT-SCANNED row "
                     "emitted, [CHOICE 5])" % (repo, NOT_SCANNED))
        else:
            L.append("  %-32s rows %-4d built_against %s"
                     % (repo, st["rows"], st["built_against"]))
    if report["default_rule"]:
        L.append("  DEFAULT unit rule applied to: %s  [CHOICE 1]"
                 % ", ".join(report["default_rule"]))
    if report["excluded_self"]:
        L.append("  excluded from scan: Simulators/instrument-index/  "
                 "[CHOICE 7]")
    L.append("")
    L.append("DECLARATION SOURCE")
    L.append("  rows with an in-file header: %d" % report["header_rows"])
    L.append("  rows from override only:     %d" % report["override_rows"])
    L.append("  rows UNRATED (listed anyway): %d" % report["unrated_rows"])
    L.append("  header/override DRIFT:        %d  [CHOICE 3]"
             % len(report["drift"]))
    for rid, k, hv, ov in report["drift"]:
        L.append("    %s  %s: header=%r override=%r (header used)"
                 % (rid, k, hv, ov))
    L.append("")
    L.append("AXIS CHECK (INDEX-SPEC.md, AXIS RISK)  [CHOICE 8]")
    L.append("  rows: %d   rated: %d   rated share: %s"
             % (ax["total"], ax["rated"],
                "--" if ax["rated_share"] is None
                else "%.3f" % ax["rated_share"]))
    L.append("  CLAIM-only share of rated rows: %s   threshold: > %.2f"
             % ("--" if ax["claim_only_share"] is None
                else "%.3f" % ax["claim_only_share"], ax["threshold"]))
    L.append("  verdict: %s" % ax["verdict"])
    if ax["verdict"] == "NOT_EVALUABLE":
        L.append("  (no rated rows; the axis has not been tested)")
    if ax["distribution"]:
        L.append("  input_shape distribution over rated rows "
                 "(multi-valued rows count once per value):")
        for k in sorted(ax["distribution"], key=lambda k: -ax["distribution"][k]):
            L.append("    %-13s %d" % (k, ax["distribution"][k]))
    L.append("")
    L.append("SIZE CHECK (INDEX-SPEC.md, design constraints)")
    L.append("  bytes: %d   target: <= %d   verdict: %s"
             % (sz["bytes"], sz["target_bytes"], sz["verdict"]))
    L.append("  rows: %d   spec's sizing basis: ~%d rows   bytes/row: %s"
             % (sz["rows"], sz["target_rows"],
                "--" if sz["bytes_per_row"] is None
                else "%.1f" % sz["bytes_per_row"]))
    L.append("")
    L.append("gate column: UNRUN is the default and is not FAILED. "
             "load_tok_est is bytes/4 with no tokenizer -- an ESTIMATE.")
    return "\n".join(L) + "\n"


# --- CLI ----------------------------------------------------------------------

def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "build_index.py has no --selftest. The checks are in "
            "test_index.py:\n    python3 %s\n"
            % os.path.join(HERE, "test_index.py"))
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    root = DEFAULT_ROOT
    repos = list(REPO_RULES)
    out = os.path.join(HERE, "INSTRUMENT-INDEX.tsv")
    ovr = os.path.join(HERE, "index-overrides.json")
    report_only = False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--root":
            root = argv[i + 1]; i += 1
        elif a == "--repos":
            repos = argv[i + 1].split(","); i += 1
        elif a == "--out":
            out = argv[i + 1]; i += 1
        elif a == "--overrides":
            ovr = argv[i + 1]; i += 1
        elif a == "--report-only":
            report_only = True
        else:
            sys.stderr.write("unknown argument %r\n" % a)
            return 2
        i += 1
    try:
        overrides = load_overrides(ovr)
        rows, report = build(root, repos, overrides)
        tsv = to_tsv(rows)
    except BuildRefused as ex:
        sys.stderr.write("BUILD REFUSED: %s\n" % ex)
        return 1
    if not report_only:
        with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(tsv)
    sys.stdout.write(render_report(rows, report, tsv, out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
