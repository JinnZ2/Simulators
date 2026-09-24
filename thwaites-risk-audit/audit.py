#!/usr/bin/env python3
"""
audit.py -- checks on the delivered Thwaites x Simulators risk audit.

The delivered documents are verbatim and this module edits none of them.
Every finding is computed here; disagreements go in CLAIM_TABLE.md.

WHAT MAKES THIS FOLDER DIFFERENT FROM external-audit/ AND
deep-research-correction/: those two read a report ABOUT this repository.
This one reads a report that says it RAN this repository -- "All tools
below were actually cloned and run" -- and every tool it names is in the
tree beside it.  So the tool CLAIMS are reproducible here, and the PAPER
claims are not (allowlist egress).  The split is enforced:
`run_*` functions import the sibling module and execute it; everything
resting on a publication is CARRIED and enters no verdict.

Three renderings of one document exist:
  SOURCE_DROP.md      v1, delivered in a zip, 46767 bytes
  SOURCE_DROP_V2.md   v2, the delivered "diff test", v1 + a repair log
  AMOC/research.md    committed to main at f35e1f5 -- a byte-exact
                      PREFIX of v1, at a path that files it as AMOC
                      research.  Not touched from here.

  [CHOICE 1]  land both renderings side by side rather than superseding,
              per the repo's own convention (observer-exclusion SPEC_V2,
              failure-mode-register WORK_ORDER_V2..V4, move-set V2).
              A revision that quotes its own repairs is a copy, and
              copies drift -- OE_011 / DBK_010 / MI_011 / FMR_026.

CC0-1.0.  Stdlib only.  No network.  Parses under 3.9.
"""
import ast
import difflib
import io
import os
import re
import subprocess
import sys
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

V1 = os.path.join(HERE, "SOURCE_DROP.md")
V2 = os.path.join(HERE, "SOURCE_DROP_V2.md")
BRIEF = os.path.join(HERE, "WORKER_FIELD_BRIEF_DESIGN_LIFE.md")
DERIVED = ("OPERATIONS_REDUNDANCY_AUDIT_TEMPLATE.md",
           "WARNING_CARD_SPEC.md",
           "WORKER_FIELD_BRIEF_DESIGN_LIFE.md")

# The commit the document's own convergence note cites, by name.  Reading
# it is checking the claim's own citation, not a fixed position in
# history -- but `third_copy()` also walks the path by CONTENT, which is
# the AGA_066 discipline, so a moved commit does not silently pass.
CITED_COMMIT = "f35e1f5"
CITED_PATH = "AMOC/research.md"

_SRC = {}


def src(path):
    if path not in _SRC:
        with open(path, encoding="utf-8") as fh:
            _SRC[path] = fh.read()
    return _SRC[path]


def _sib(name):
    p = os.path.join(ROOT, name)
    if p not in sys.path:
        sys.path.insert(0, p)
    return p


def _git(args):
    try:
        r = subprocess.run(["git"] + args, cwd=ROOT, capture_output=True,
                           text=True, timeout=60)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


# ---------------------------------------------------------------- copies

def revision():
    """v1 -> v2 as a copy.  TRA_001."""
    a, b = src(V1).splitlines(), src(V2).splitlines()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    counts = {"equal": 0, "insert": 0, "delete": 0, "replace": 0}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        counts[tag] += (j2 - j1) if tag in ("insert", "replace") else (i2 - i1)
    return {"v1_lines": len(a), "v2_lines": len(b),
            "v1_bytes": len(src(V1).encode("utf-8")),
            "v2_bytes": len(src(V2).encode("utf-8")),
            "ratio": round(sm.ratio(), 4), "opcodes": counts,
            "pure_insertion": counts["delete"] == 0 and counts["replace"] == 0,
            "reading": ("a REWRITE, not a pure insertion"
                        if counts["delete"] or counts["replace"]
                        else "a pure insertion")}


def third_copy():
    """The convergence note's own citation, checked two ways.  TRA_002.

    The note reads: "Simulators/AMOC/research.md (commit f35e1f5)
    independently added Kasuya and Nian while these searches ran.  Same
    two papers, two independent routes."
    """
    out = {"cited_commit": CITED_COMMIT, "cited_path": CITED_PATH}
    blob = _git(["show", "%s:%s" % (CITED_COMMIT, CITED_PATH)])
    out["cited_object_resolves"] = blob is not None
    if blob is None:
        out["verdict"] = "NOT_RESOLVABLE_IN_THIS_CLONE"
        out["note"] = ("the named object is not fetched here.  Not a "
                       "finding about the document: run `git fetch origin "
                       "main` and re-run.")
        return out
    v1 = src(V1)
    out["blob_bytes"] = len(blob.encode("utf-8"))
    out["v1_bytes"] = len(v1.encode("utf-8"))
    out["is_prefix_of_v1"] = v1.startswith(blob)
    out["share"] = round(len(blob) / float(len(v1)), 4)
    # By content: any commit touching the path whose blob is a v1 prefix.
    log = _git(["log", "--format=%H", "--all", "--", CITED_PATH]) or ""
    by_content = []
    for sha in log.split():
        t = _git(["show", "%s:%s" % (sha, CITED_PATH)])
        if t and v1.startswith(t):
            by_content.append(sha[:7])
    out["prefix_commits_by_content"] = by_content
    for who in ("Kasuya", "Nian"):
        out["names_%s" % who.lower()] = bool(
            re.search(r"\b%s\b" % who, blob))
    out["verdict"] = (
        "REFUTED -- one document in two places, not two routes"
        if out["is_prefix_of_v1"] else
        "HOLDS -- the file is not a copy of this document")
    return out


def repair_reach():
    """Did R1's citation repair reach the derived deliverables?  TRA_026."""
    rows = []
    for name in ("SOURCE_DROP.md", "SOURCE_DROP_V2.md") + DERIVED:
        t = src(os.path.join(HERE, name))
        rows.append({"file": name,
                     "bradley": len(re.findall(r"\bBradley\b", t)),
                     "williams": len(re.findall(r"\bWilliams\b", t))})
    unrepaired = [r["file"] for r in rows
                  if r["bradley"] and not r["williams"]]
    return {"rows": rows, "unrepaired": unrepaired,
            "reading": ("R1 renames Bradley et al. -> Williams et al.  "
                        "A file naming Bradley and never Williams did not "
                        "receive the repair.")}


# ------------------------------------------------------------ repair log

def _lines_with(text, needle):
    return [ln for ln in text.splitlines() if needle in ln
            and not ln.lstrip().startswith("> |")]


def _all_lines_flagged(text, needle, flag):
    ls = _lines_with(text, needle)
    return bool(ls) and all(flag in ln for ln in ls)


def _any_line_flagged(text, needle, flag):
    return any(flag in ln for ln in _lines_with(text, needle))


R_RE = re.compile(r"^>\s*\|\s*(R\d)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", re.M)


def repair_log():
    """Parse the v2 repair log and check each row against the text."""
    rows = [{"id": m.group(1), "repair": m.group(2), "status": m.group(3)}
            for m in R_RE.finditer(src(V2))]
    a, b = src(V1), src(V2)
    checks = {
        "R1": {"test": "v1 names Bradley in the section-5 heading, v2 names "
                       "Williams",
               "held": ("## 5. Bradley et al." in a
                        and "## 5. Williams et al." in b)},
        # The first version of this test read `"UNVERIFIED" in b and not
        # in a` and returned a FALSE NEGATIVE: v1 already uses the token
        # for an unrelated lead (the HAL bathymetry record), so a
        # document-wide token test cannot see a figure-level flag.  That
        # is UNI_009 / T1-1 inside a repair-log checker.  The test now
        # reads the FIGURE's own lines.
        "R2": {"test": "every line mentioning 2.6 mm/yr carries "
                       "UNVERIFIED in v2 and none does in v1",
               "held": (_all_lines_flagged(b, "2.6 mm/yr", "UNVERIFIED")
                        and not _any_line_flagged(a, "2.6 mm/yr",
                                                  "UNVERIFIED"))},
        "R3": {"test": "v2 retires THW-F1 and v1 does not",
               "held": ("RETIRED" in b and "RETIRED" not in a)},
        "R4": {"test": "v2 carries the token DEMONSTRATION and v1 does not",
               "held": ("DEMONSTRATION" in b and "DEMONSTRATION" not in a)},
        "R5": {"test": "v2 flags the DOI conflict and v1 does not",
               "held": ("CONFLICT" in b and "CONFLICT" not in a)},
        "R6": {"test": "v2 marks the kappa INVALID AS RELIABILITY and v1 "
                       "does not",
               "held": ("INVALID AS RELIABILITY" in b
                        and "INVALID AS RELIABILITY" not in a)},
    }
    for r in rows:
        c = checks.get(r["id"])
        r["mechanical_check"] = c["test"] if c else "no mechanical test"
        r["applied"] = c["held"] if c else None
    return {"rows": rows, "n": len(rows),
            "applied": sum(1 for r in rows if r["applied"]),
            "untested": sum(1 for r in rows if r["applied"] is None)}


# ------------------------------------------------------------ the inputs

STATED_INPUTS = (
    ("closure-cost case files", 2, r"closure-cost case"),
    ("declared-frame blocks", 5, r"declared-frame block"),
    ("measurement-fork spec", 1, r"measurement-fork spec"),
    ("chain driver", 1, r"chain driver"),
)


def inputs_present():
    """The method note names the input files.  None is in the delivery.

    TRA_004.  A run whose inputs are absent is a run nobody can repeat;
    what stays checkable is the TOOL's behaviour, which is what every
    `run_*` function below does.
    """
    shipped = sorted(f for f in os.listdir(HERE)
                     if not f.startswith(".") and
                     os.path.isfile(os.path.join(HERE, f)))
    data = [f for f in shipped
            if f.endswith((".json", ".jsonl", ".csv", ".txt"))]
    stated = []
    note = src(V2)
    for label, n, pat in STATED_INPUTS:
        stated.append({"input": label, "stated_count": n,
                       "named_in_method_note": bool(re.search(pat, note))})
    return {"stated": stated,
            "stated_total": sum(s["stated_count"] for s in stated),
            "data_files_in_delivery": data,
            "reproducible": len(data) > 0}


# -------------------------------------------------------- tool behaviour

S1_RE = re.compile(r"^(0\.\d+)\s+(0\.\d+)\s+(0\.\d+)\s*$", re.M)


def run_s1():
    """instrument-bias-sims S1, run.  TRA_005."""
    quoted = [(float(a), float(b), float(c))
              for a, b, c in S1_RE.findall(src(V2))]
    _sib("instrument-bias-sims")
    import s1_encounter_denominator as s1
    got = {}
    for row in s1.sweep([q[0] for q in quoted]):
        got[round(row["f"], 3)] = (round(row["true_null_share"], 4),
                                   round(row["B_null_share"], 4))
    rows = []
    for f, tn, bn in quoted:
        g = got.get(round(f, 3))
        rows.append({"f": f, "quoted": (tn, bn), "computed": g,
                     "matches": g == (tn, bn)})
    doc = s1.__doc__ or ""
    return {"rows": rows, "all_match": all(r["matches"] for r in rows),
            "thwaites_input": False,
            "module_says_by_construction":
                "by construction" in src(
                    os.path.join(ROOT, "instrument-bias-sims",
                                 "s1_encounter_denominator.py")),
            "reading": ("the quoted numbers are the module's own defaults "
                        "-- sweep(f, n_dyads=40, ticks=400, seed=11).  No "
                        "Thwaites quantity enters.  R4 relabelled two "
                        "blocks DEMONSTRATION and not this one.")}


CHAIN_RE = re.compile(
    r"^\s*(\w+)\s+([\d.]+)\s+([\d.]+)\s+BREACH\s*$", re.M)


def run_chain():
    """reservoir-chain-coupling, run.  TRA_006 / TRA_007 / TRA_008."""
    quoted = [(m.group(1), float(m.group(2)), float(m.group(3)))
              for m in CHAIN_RE.finditer(src(V2))]
    _sib("reservoir-chain-coupling")
    import chain as ch
    # render() hardcodes the boundary inflow and exports no constant, so
    # it is PARSED out of chain.py rather than retyped here (MF_019).
    m = re.search(r"^\s*inflow\s*=\s*([\d.]+)\s*$",
                  src(os.path.join(ROOT, "reservoir-chain-coupling",
                                   "chain.py")), re.M)
    inflow = float(m.group(1))
    r = ch.compare(ch.signal_chain(), inflow)
    ind = [(n, w) for n, w, br in r["run1_independent"]["trace"]]
    cou = [(n, w) for n, w, br in r["run2_coupled"]["trace"]]
    fixture = [(a[0], round(a[1], 2), round(b[1], 2))
               for a, b in zip(ind, cou)]
    rows = []
    for i, (name, mx, sm) in enumerate(quoted):
        f = fixture[i] if i < len(fixture) else None
        rows.append({"doc_label": name,
                     "doc_values": (mx, sm),
                     "fixture_node": f[0] if f else None,
                     "fixture_values": (f[1], f[2]) if f else None,
                     "numbers_identical": bool(f) and (mx, sm) == (f[1], f[2]),
                     # a+b <= 2*max(a,b) for non-negative a,b
                     "sum_le_2max": sm <= 2 * mx + 1e-9})
    nulls = {}
    for label, fn in (("high_freeboard", ch.null_high_freeboard),
                      ("no_freeboard", ch.null_no_freeboard)):
        nulls[label] = ch.compare(fn(), inflow)["verdict"].split("(")[0].strip()
    return {"rows": rows, "boundary_inflow": inflow,
            "all_numbers_identical": all(r["numbers_identical"]
                                         for r in rows),
            "rows_violating_sum_le_2max":
                [r["doc_label"] for r in rows if not r["sum_le_2max"]],
            "module_column_names": ("independent", "coupled"),
            "doc_column_names": ("max", "sum"),
            "null_fixtures": nulls,
            "detector_always_fires": all(v.startswith("LOAD-BEARING")
                                         for v in nulls.values()),
            "reading": ("the block is signal_chain()'s shipped fixture "
                        "output with four node names substituted.  Under "
                        "the module's column names there is no arithmetic "
                        "difficulty; under the document's (max / sum) every "
                        "row reads as impossible, since a+b <= 2*max(a,b).")}


def fork_arms():
    """measurement-fork: how many arms can compare.py hold?  TRA_010."""
    p = os.path.join(ROOT, "measurement-fork", "compare.py")
    tree = ast.parse(src(p))
    arms = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "arms" and \
                        isinstance(node.value, ast.Dict):
                    arms = [k.value for k in node.value.keys
                            if isinstance(k, ast.Constant)]
    pools_widen = "allp" in src(p) and "is_quantity" not in src(p)
    return {"arms": arms, "n_arms": len(arms) if arms else None,
            "fourth_arm_expressible": False if arms else None,
            "residual_pools_every_arm": pools_widen,
            "reading": ("the arm set is a hardcoded dict of three "
                        "generators.  A fourth arm is not expressible, so "
                        "'four-arm result' is not what compare.py "
                        "computed.  MF_004 stands unrepaired: the residual "
                        "loop still pools every arm, so a widen PROPOSAL "
                        "can mark a residual question COVERED.")}


def run_fork():
    """measurement-fork on the shipped spec.  TRA_009."""
    spec = os.path.join(ROOT, "measurement-fork", "systems",
                        "provisioning_calibration.json")
    cwd = os.getcwd()
    os.chdir(os.path.join(ROOT, "measurement-fork"))
    _sib("measurement-fork")
    buf = io.StringIO()
    try:
        import compare
        argv = sys.argv
        sys.argv = ["compare.py", spec]
        with redirect_stdout(buf):
            compare.main()
        sys.argv = argv
    finally:
        os.chdir(cwd)
    out = buf.getvalue()
    counts = dict((m.group(1), int(m.group(2))) for m in
                  re.finditer(r"arm (\w+)\s+(\d+) probes", out))
    const = "none -- the arms share no quantity at all."
    doc_counts = dict((m.group(1), int(m.group(2))) for m in
                      re.finditer(r"arm (\w+)\s+(\d+) probes", src(V2)))
    return {"shipped_spec_counts": counts,
            "document_counts": doc_counts,
            "counts_differ": counts != doc_counts,
            "shipped_spec_cell_empty": const in out,
            "verdict_text_is_a_module_constant": const in src(
                os.path.join(ROOT, "measurement-fork", "compare.py")),
            "covered_in_document": "[COVERED" in src(V2),
            "reading": ("the verdict sentence is compare.py's constant for "
                        "an empty cell and is what the SHIPPED spec returns "
                        "too.  The probe counts differ, so a Thwaites spec "
                        "was run; it is not in the delivery.")}


def authored_parenthetical():
    """A fence that mixes tool output with annotation.  TRA_011."""
    cp = src(os.path.join(ROOT, "measurement-fork", "compare.py"))
    marks = re.findall(r"\(unchanged with arm \d\)", src(V2))
    return {"in_document": marks,
            "in_compare_py": [m for m in marks if m in cp],
            "reading": ("compare.py prints four fixed lines for an empty "
                        "cell and prints no parenthetical, so the fence "
                        "mixes output and annotation without marking "
                        "which is which.")}


def closure_labels():
    """Are the quoted closure-cost labels the module's?  TRA_014."""
    cc = src(os.path.join(ROOT, "closure-cost", "closure.py"))
    labels = ("VARIABLE", "INFORMATION AVAILABILITY", "PROCEDURE GAP RIVAL",
              "collapsed into closure")
    return {"labels": {l: (l in cc and l in src(V2)) for l in labels},
            "all_from_the_module": all(l in cc for l in labels),
            "document_states_its_own_caveat":
                "restates an auditor-entered input" in src(V2),
            "reading": ("the render is genuine -- every quoted label is "
                        "closure.py's.  The case file is absent (TRA_004), "
                        "and the repair log's own 'still unrepaired' line "
                        "already names the verdict as a restatement of an "
                        "auditor-entered field.")}


def run_oir():
    """observable-indicator-rules, run.  TRA_017."""
    cwd = os.getcwd()
    os.chdir(os.path.join(ROOT, "observable-indicator-rules"))
    _sib("observable-indicator-rules")
    buf = io.StringIO()
    try:
        import pipeline
        with redirect_stdout(buf):
            pipeline.main() if hasattr(pipeline, "main") else None
    except SystemExit:
        pass
    finally:
        os.chdir(cwd)
    out = buf.getvalue()
    if not out:
        import subprocess as sp
        r = sp.run([sys.executable, "pipeline.py"],
                   cwd=os.path.join(ROOT, "observable-indicator-rules"),
                   capture_output=True, text=True, timeout=300)
        out = r.stdout
    rates = [(float(m.group(1)), float(m.group(2))) for m in re.finditer(
        r"false-alarm rate ([\d.]+)\s+miss rate ([\d.]+)", out)]
    return {"rates": rates,
            "document_pair": (0.5, 0.0),
            "reproduces": (0.5, 0.0) in rates,
            "document_scopes_it_down": "over-transfer" in src(V2),
            "reading": ("the pair is the module's own false_alarm_heavy "
                        "ensemble and the document presents it as OIR's "
                        "standing finding, then section 12a demotes the "
                        "transfer on the operator's critique.")}


def kappa_constant_coder():
    """A constant second coder forces kappa to exactly 0.  TRA_013."""
    import itertools
    _sib("effective-redundancy-audit")
    from effective_redundancy import cohen_kappa
    S, N = "shared", "not"
    nonzero, total = 0, 0
    for k in range(1, 6):
        for c1 in set(itertools.permutations([S] * k + [N] * (6 - k))):
            total += 1
            if abs(cohen_kappa(list(c1), [S] * 6)) > 1e-12:
                nonzero += 1
    return {"n_codings": total, "kappa_nonzero": nonzero,
            "degenerate_both_constant": round(
                cohen_kappa([S] * 6, [S] * 6), 4),
            "doc_reports_kappa_zero": "0.000" in src(V2),
            "doc_reports_neff_1": "N_eff=1" in src(V2)
                                  or "N_eff = 1" in src(V2),
            "reading": ("N_eff = 1 is every channel collapsed, i.e. the "
                        "second coder marked every channel the same way.  "
                        "Against a constant coder kappa is exactly 0 for "
                        "every non-degenerate first coding, so 0.000 is "
                        "forced by the reported N_eff and carries no "
                        "agreement information.  R6's reason (one model "
                        "coded twice) is the weaker one.")}


def stommel_grid(grids=((0.0, 0.5, 80), (0.0, 1.0, 80), (0.0, 0.4, 80),
                        (0.0, 0.5, 40), (0.0, 0.5, 160), (0.0, 0.3, 80))):
    """The spinodal moves with the grid.  TRA_018."""
    _sib("AMOC")
    import forcing
    b = forcing.StommelBox()
    rows = []
    for lo, hi, n in grids:
        r = b.hysteresis_band(lo, hi, n)
        rows.append({"range": (lo, hi), "n": n,
                     "step": round((hi - lo) / (n - 1), 5),
                     "spinodal": round(r["spinodal_collapse"], 4)})
    vals = [r["spinodal"] for r in rows]
    doc = 0.228
    return {"rows": rows, "min": min(vals), "max": max(vals),
            "spread": round(max(vals) - min(vals), 4),
            "document_value": doc,
            "document_value_reproduced_by":
                [r["range"] + (r["n"],) for r in rows
                 if abs(r["spinodal"] - doc) < 5e-4],
            "document_value_is_lowest": abs(min(vals) - doc) < 5e-4,
            "reading": ("hysteresis_band reports the last grid point at "
                        "which both states coexist, so every value is a "
                        "LOWER bound and the reported figure moves with the "
                        "grid.  Three decimals state a precision the method "
                        "does not have.")}


def calibration():
    """0.50 Sv is the calibration's own anchor.  TRA_019 / TRA_020."""
    _sib("AMOC")
    from sitespec import ForcingCalibration
    c = ForcingCalibration()
    doc_F = 0.228
    cluster = re.search(r"cluster ~([\d.]+)-([\d.]+) Sv", c.__doc__ or "")
    lo, hi = (float(cluster.group(1)), float(cluster.group(2))) if cluster \
        else (None, None)
    added = c.sv_at_spinodal - c.sv_at_F0
    return {"sv_at_F0": c.sv_at_F0, "sv_at_spinodal": c.sv_at_spinodal,
            "spinodal_F_hardcoded": c.spinodal_F,
            "F_to_sv_of_document_F": round(c.F_to_sv(doc_F), 4),
            "document_states": 0.50,
            "anchor_is_the_document_value": c.sv_at_spinodal == 0.50,
            "added_flux_at_anchor": round(added, 4),
            "literature_cluster_added_Sv": (lo, hi),
            "anchor_inside_cluster": (lo is not None and lo <= added <= hi),
            "reading": ("sv_at_spinodal = 0.50 is a DECLARED anchor, so "
                        "'F = 0.228 (= 0.50 Sv)' is the anchor read back "
                        "out.  Converting the document's own F through the "
                        "calibration gives %.3f Sv, because the calibration "
                        "hardcodes spinodal_F = %.3f.  The docstring hands "
                        "the document a published BAND for the added-flux "
                        "threshold and the document uses the single anchor "
                        "-- against its own opening rule, 'report the band, "
                        "plan against the short end'."
                        % (c.F_to_sv(doc_F), c.spinodal_F))}


OCEAN_AREA_M2 = 3.61e14        # [CHOICE 2] standard ocean-area figure
SEC_PER_YEAR = 365.2425 * 24 * 3600
GT_PER_MM_SLE = 361.8          # [CHOICE 3] 1 mm SLE = 361.8 Gt
RHO_ICE, RHO_SEAWATER = 917.0, 1027.0   # [CHOICE 4]


def sle_to_sv(mm_per_year):
    """mm/yr of global mean sea-level equivalent -> sverdrups."""
    if mm_per_year is None:
        return None
    return mm_per_year * 1e-3 * OCEAN_AREA_M2 / SEC_PER_YEAR / 1e6


def flux_arithmetic():
    """TRA_021 / TRA_022."""
    sv = sle_to_sv(2.6)
    grounded = (50 / GT_PER_MM_SLE, 60 / GT_PER_MM_SLE)
    fl = 1.0 - RHO_ICE / RHO_SEAWATER
    floating = (grounded[0] * fl, grounded[1] * fl)
    return {"sle_2p6_mm_per_yr_Sv": round(sv, 5),
            "document_states_Sv": 0.030,
            "sv_matches": abs(sv - 0.030) < 5e-4,
            "gt_50_60_as_grounded_mm": (round(grounded[0], 4),
                                        round(grounded[1], 4)),
            "document_states_mm": 0.15,
            "mm_matches_as_grounded": grounded[0] <= 0.15 <= grounded[1],
            "floating_displacement_factor": round(fl, 4),
            "gt_50_60_as_floating_mm": (round(floating[0], 4),
                                        round(floating[1], 4)),
            "overstatement_factor": round(1.0 / fl, 1),
            "quantity_named_by_document": "basal melt",
            "reading": ("both conversions are exact AS WRITTEN.  The "
                        "quantity named is ice-shelf BASAL melt -- melt at "
                        "the base of FLOATING ice, per the document's own "
                        "mechanism paragraph (CDW 'under the ice shelves') "
                        "-- whose direct sea-level contribution is the "
                        "displacement residual, about %.1fx smaller.  The "
                        "sea-level consequence of shelf melt is the "
                        "downstream dynamic response of grounded ice, a "
                        "different quantity with a lag.  This is the one "
                        "arithmetic step in the document that runs toward "
                        "overstating." % (1.0 / fl))}


def gap_blocks():
    """THW-01..05 against the gap-markers schema.  TRA_023 / TRA_024."""
    _sib("gap-markers")
    import markers
    text = src(V2)
    # As delivered: the register's own reader, unmodified, on the
    # document's own bytes.
    as_delivered = [r for r in markers.parse_entries(text, "SOURCE_DROP_V2.md")
                    if r.get("GAP_ID")]
    # markers.FIELD_RE requires exactly four leading spaces; the
    # delivered blocks sit unindented inside fences.  [CHOICE 6] re-indent
    # an IN-MEMORY copy so field-level conformance can be read apart from
    # block-form conformance.  The delivered file is not touched.
    fenced = [b for b in re.findall(r"```\n([\s\S]*?)```", text)
              if "GAP_ID" in b]
    fence = []
    for blk in fenced:
        cur = []
        for ln in blk.splitlines():
            if ln.startswith("GAP_ID") and cur:
                fence.append("\n".join(cur))
                cur = []
            cur.append(ln)
        if cur:
            fence.append("\n".join(cur))
    fence = [b for b in fence if b.lstrip().startswith("GAP_ID")]
    reindented = "\n---\n".join(
        "\n".join("    " + ln if ln.strip() else ln
                   for ln in blk.splitlines()) for blk in fence)
    recs = [r for r in markers.parse_entries(reindented, "reindented")
            if r.get("GAP_ID")]
    rows = []
    for r in recs:
        gid = r.get("GAP_ID", "?")
        missing = [f for f in markers.FIELDS if f not in r]
        state = r.get("STATE", "")
        kind_raw = r.get("KIND", "")
        kind_vals = [markers._bare(v)
                     for v in re.split(r"\s+\+\s+|\s*/\s*", kind_raw) if v]
        rows.append({
            "id": gid,
            "fields_present": len(markers.FIELDS) - len(missing),
            "fields_total": len(markers.FIELDS),
            "missing": missing,
            "state": state,
            "state_in_vocabulary": state in markers.STATES,
            "kind_raw": kind_raw,
            "kind_values": kind_vals,
            "kind_count": len(kind_vals),
            "kinds_in_vocabulary": [k in markers.KINDS for k in kind_vals],
            "kind_forced_by_state": (markers.kind_forced(state)["forced"]
                                     if state in markers.STATES else None),
        })
    composite = [r["id"] for r in rows if r["kind_count"] > 1]
    contradicted = []
    for r in rows:
        f = r["kind_forced_by_state"]
        if f and any(k != f for k in r["kind_values"]):
            contradicted.append({"id": r["id"], "forced": f,
                                 "declared": r["kind_values"]})
    return {"rows": rows, "n_blocks": len(rows),
            "records_the_register_reader_sees_as_delivered":
                len(as_delivered),
            "fenced_blocks_found": len(fence),
            "schema_fields": list(markers.FIELDS),
            "composite_kind": composite,
            "state_contradicts_kind": contradicted,
            "thw05_is_a_block": any(r["id"].startswith("THW-05")
                                    for r in rows),
            "reading": ("the blocks carry the right FIELD NAMES and not "
                        "the register's block FORM: markers.FIELD_RE wants "
                        "four leading spaces and the fenced blocks have "
                        "none, so the register's own reader ingests %d of "
                        "them.  THW-05 is prose and is not a block at all, "
                        "so 'schema-conformant' covers four of five.  A "
                        "composite KIND is GM_010's shape reached by an "
                        "author who has not read the register."
                        % len(as_delivered))}


def declared_frame_surface():
    """What does check_frame.py emit for ONE block?  TRA_015 / TRA_016."""
    p = os.path.join(ROOT, "declared-frame", "v2", "check_frame.py")
    t = src(p)
    tree = ast.parse(t)
    strings = [n.value for n in ast.walk(tree)
               if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    emits_flag = any("flag" in s.lower() for s in strings)
    core = re.search(r"CORE\s*=\s*\[([^\]]*)\]", t)
    never_compared = [f for f in ("sign_source", "observer_access")
                      if core and f not in core.group(1)]
    doc_flags = sorted(set(re.findall(r"frame flag: `?(\w+)`?", src(V2))))
    return {"module": "declared-frame/v2/check_frame.py",
            "emits_the_word_flag": emits_flag,
            "core_fields_line": core.group(1).strip() if core else None,
            "recorded_never_compared": never_compared,
            "flags_asserted_in_document": doc_flags,
            "reading": ("on a single block the checker prints 'all six "
                        "fields declared' plus any unknowns.  It emits no "
                        "frame flag, so the per-paper flags are authored "
                        "in a sentence whose first clause is the tool's.  "
                        "And observer_access -- the field section 14 ranks "
                        "the corpus by -- is one of the two DF_001 records "
                        "but never compares.")}


def climate_modeling_state():
    """Is the 7/7 FAIL block reproducible here?  TRA_025."""
    missing = []
    for mod in ("numpy", "scipy"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    return {"required": ["numpy", "scipy"], "missing": missing,
            "state": "NOT_RUN" if missing else "RUNNABLE",
            "reason": ("absent in this environment: " + ", ".join(missing)
                       if missing else ""),
            "document_relabelled_it": "DEMONSTRATION" in src(V2),
            "reading": ("NOT_RUN is a measured state here, not an "
                        "assumption.  The document's own R4 already "
                        "relabels the block a DEMONSTRATION.")}


def carried():
    """Everything resting on a publication.  TRA_027."""
    dois = sorted(set(re.findall(r"10\.\d{4,9}/[^\s,;)\]]+", src(V2))))
    return {"dois_named": len(dois),
            "verified_here": 0,
            "reason": ("allowlist egress: only github.com answers.  No "
                       "publisher, DOI resolver or agency host is "
                       "reachable, so every paper, date, figure and the R5 "
                       "DOI conflict is CARRIED and enters no verdict."),
            "sample": dois[:5]}


# ------------------------------------------------------------ the render

def _w(lines, text, ind="  ", width=74):
    import textwrap
    for ln in textwrap.wrap(text, width, initial_indent=ind,
                            subsequent_indent=ind):
        lines.append(ln)


def render():
    L = []
    a = L.append
    a("=" * 74)
    a("CHECKS ON THE DELIVERED THWAITES x SIMULATORS AUDIT")
    a("=" * 74)
    a("")
    _w(L, "The document says its tools were cloned and run from this "
          "repository.  Every tool it names is in the tree, so the TOOL "
          "claims are reproducible here and the PAPER claims are not.  "
          "Nothing below is a statement about Thwaites Glacier.", "")
    a("")

    r = revision()
    a("1. THE TWO RENDERINGS  [TRA_001]")
    a("   v1 %d lines / %d bytes   v2 %d lines / %d bytes   ratio %.4f"
      % (r["v1_lines"], r["v1_bytes"], r["v2_lines"], r["v2_bytes"],
         r["ratio"]))
    a("   opcodes %s" % r["opcodes"])
    a("   %s" % r["reading"])
    a("")

    t = third_copy()
    a("2. THE THIRD COPY  [TRA_002]")
    a("   cited: %s:%s   resolves %s"
      % (t["cited_commit"], t["cited_path"], t["cited_object_resolves"]))
    if t["cited_object_resolves"]:
        a("   blob %d bytes of v1's %d  (%.1f%%)   prefix of v1: %s"
          % (t["blob_bytes"], t["v1_bytes"], 100 * t["share"],
             t["is_prefix_of_v1"]))
        a("   names Kasuya %s   names Nian %s"
          % (t["names_kasuya"], t["names_nian"]))
        a("   prefix commits found by content: %s"
          % (", ".join(t["prefix_commits_by_content"]) or "none"))
    a("   VERDICT  %s" % t["verdict"])
    if not t["cited_object_resolves"]:
        _w(L, t["note"], "   ")
    a("")

    rl = repair_log()
    a("3. R1..R6, THE DOCUMENT'S OWN SIX-ROW TABLE  [TRA_003]")
    a("   %d rows, %d mechanically confirmed applied, %d untested"
      % (rl["n"], rl["applied"], rl["untested"]))
    for row in rl["rows"]:
        a("   %-3s %-8s %s" % (row["id"], str(row["applied"]),
                               row["mechanical_check"]))
    a("")

    rr = repair_reach()
    a("4. DID R1 REACH THE DERIVED DOCUMENTS?  [TRA_026]")
    for row in rr["rows"]:
        a("   %-42s Bradley %d  Williams %d"
          % (row["file"], row["bradley"], row["williams"]))
    a("   UNREPAIRED: %s" % (", ".join(rr["unrepaired"]) or "none"))
    a("")

    ip = inputs_present()
    a("5. THE INPUTS THE RUNS USED  [TRA_004]")
    for s in ip["stated"]:
        a("   %-26s stated %d   named in method note %s"
          % (s["input"], s["stated_count"], s["named_in_method_note"]))
    a("   data files in the delivery: %s"
      % (", ".join(ip["data_files_in_delivery"]) or "none"))
    a("   reproducible from the delivery: %s" % ip["reproducible"])
    a("")

    s = run_s1()
    a("6. instrument-bias-sims S1, RUN  [TRA_005]")
    for row in s["rows"]:
        a("   f=%-7s quoted %s   computed %s   match %s"
          % (row["f"], row["quoted"], row["computed"], row["matches"]))
    a("   all quoted numbers reproduce: %s" % s["all_match"])
    _w(L, s["reading"], "   ")
    a("")

    c = run_chain()
    a("7. reservoir-chain-coupling, RUN  [TRA_006 / TRA_007 / TRA_008]")
    a("   %-26s %-14s %-16s %s"
      % ("document label", "doc (max,sum)", "fixture node", "identical"))
    for row in c["rows"]:
        a("   %-26s %-14s %-16s %s"
          % (row["doc_label"], row["doc_values"], row["fixture_node"],
             row["numbers_identical"]))
    a("   every number identical to the shipped fixture: %s"
      % c["all_numbers_identical"])
    a("   module column names %s   document column names %s"
      % (c["module_column_names"], c["doc_column_names"]))
    a("   rows where sum > 2*max (impossible for two non-negatives): %s"
      % (", ".join(c["rows_violating_sum_le_2max"]) or "none"))
    a("   null fixtures: %s" % c["null_fixtures"])
    a("   detector always fires: %s" % c["detector_always_fires"])
    _w(L, c["reading"], "   ")
    a("")

    fa = fork_arms()
    f = run_fork()
    a("8. measurement-fork  [TRA_009 / TRA_010 / TRA_012]")
    a("   compare.py arms: %s  (n=%s)" % (fa["arms"], fa["n_arms"]))
    a("   a fourth arm is expressible: %s" % fa["fourth_arm_expressible"])
    a("   shipped spec probe counts   %s" % f["shipped_spec_counts"])
    a("   document probe counts       %s" % f["document_counts"])
    a("   shipped spec's SAME QUANTITY cell empty too: %s"
      % f["shipped_spec_cell_empty"])
    a("   the verdict sentence is a module constant: %s"
      % f["verdict_text_is_a_module_constant"])
    a("   residual loop pools every arm (MF_004 unrepaired): %s"
      % fa["residual_pools_every_arm"])
    _w(L, f["reading"], "   ")
    _w(L, fa["reading"], "   ")
    a("")

    k = kappa_constant_coder()
    a("9. effective-redundancy-audit, the kappa  [TRA_013]")
    a("   non-degenerate codings against a constant coder: %d"
      % k["n_codings"])
    a("   of those, kappa != 0: %d" % k["kappa_nonzero"])
    a("   both coders constant and equal -> kappa %s"
      % k["degenerate_both_constant"])
    _w(L, k["reading"], "   ")
    a("")

    g = stommel_grid()
    cal = calibration()
    a("10. AMOC StommelBox  [TRA_018 / TRA_019 / TRA_020]")
    for row in g["rows"]:
        a("   range %-12s n=%-4d step %.5f -> spinodal %.4f"
          % (str(row["range"]), row["n"], row["step"], row["spinodal"]))
    a("   spread over ordinary grids: %.4f  (min %.4f, max %.4f)"
      % (g["spread"], g["min"], g["max"]))
    a("   the document's %.3f is the lowest of these: %s"
      % (g["document_value"], g["document_value_is_lowest"]))
    _w(L, g["reading"], "   ")
    a("   sv_at_F0 %.2f   sv_at_spinodal %.2f   spinodal_F %.3f"
      % (cal["sv_at_F0"], cal["sv_at_spinodal"],
         cal["spinodal_F_hardcoded"]))
    a("   F_to_sv(0.228) = %.4f Sv   the document states %.2f Sv"
      % (cal["F_to_sv_of_document_F"], cal["document_states"]))
    a("   added flux at the anchor %.2f Sv   literature cluster %s Sv"
      % (cal["added_flux_at_anchor"], cal["literature_cluster_added_Sv"]))
    _w(L, cal["reading"], "   ")
    a("")

    fx = flux_arithmetic()
    a("11. THE FLUX AND SEA-LEVEL ARITHMETIC  [TRA_021 / TRA_022]")
    a("   2.6 mm/yr SLE -> %.5f Sv   document %.3f   match %s"
      % (fx["sle_2p6_mm_per_yr_Sv"], fx["document_states_Sv"],
         fx["sv_matches"]))
    a("   50-60 Gt as GROUNDED ice -> %s mm   document ~%.2f   match %s"
      % (str(fx["gt_50_60_as_grounded_mm"]), fx["document_states_mm"],
         fx["mm_matches_as_grounded"]))
    a("   50-60 Gt as FLOATING shelf melt -> %s mm  (%.1fx smaller)"
      % (str(fx["gt_50_60_as_floating_mm"]), fx["overstatement_factor"]))
    _w(L, fx["reading"], "   ")
    a("")

    gb = gap_blocks()
    a("12. THE GAP-MARKERS BLOCKS  [TRA_023 / TRA_024]")
    for row in gb["rows"]:
        a("   %-8s fields %d/%d  state %-10s in-vocab %s  kinds %d %s"
          % (row["id"], row["fields_present"], row["fields_total"],
             row["state"], row["state_in_vocabulary"], row["kind_count"],
             row["kind_values"]))
    a("   composite KIND: %s" % (", ".join(gb["composite_kind"]) or "none"))
    for cc in gb["state_contradicts_kind"]:
        a("   %s: STATE forces KIND %s, entry declares %s"
          % (cc["id"], cc["forced"], cc["declared"]))
    a("   fenced GAP_ID blocks in the document: %d" %
      gb["fenced_blocks_found"])
    a("   records the register's own reader sees AS DELIVERED: %d"
      % gb["records_the_register_reader_sees_as_delivered"])
    a("   THW-05 parsed as a block: %s" % gb["thw05_is_a_block"])
    _w(L, gb["reading"], "   ")
    a("")

    df = declared_frame_surface()
    a("13. declared-frame  [TRA_015 / TRA_016]")
    a("   the checker emits the word 'flag': %s" % df["emits_the_word_flag"])
    a("   CORE (the only compared fields): %s" % df["core_fields_line"])
    a("   recorded but never compared: %s" % df["recorded_never_compared"])
    a("   flags asserted in the document: %s"
      % (", ".join(df["flags_asserted_in_document"]) or "none"))
    _w(L, df["reading"], "   ")
    a("")

    ap = authored_parenthetical()
    cl = closure_labels()
    oi = run_oir()
    a("14. THREE SMALLER READS  [TRA_011 / TRA_014 / TRA_017]")
    a("   fence annotations in the document: %s   present in compare.py: %s"
      % (ap["in_document"] or "none", ap["in_compare_py"] or "none"))
    a("   closure-cost labels all from the module: %s   the document "
      "states its own caveat: %s"
      % (cl["all_from_the_module"], cl["document_states_its_own_caveat"]))
    a("   OIR rates measured here: %s   reproduces the document's %s: %s"
      % (oi["rates"], oi["document_pair"], oi["reproduces"]))
    a("")

    cm = climate_modeling_state()
    a("15. climate-modeling  [TRA_025]")
    a("   state %s   %s" % (cm["state"], cm["reason"]))
    _w(L, cm["reading"], "   ")
    a("")

    ca = carried()
    a("16. WHAT IS CARRIED  [TRA_027 / TRA_028]")
    a("   DOIs named in the document: %d   verified here: %d"
      % (ca["dois_named"], ca["verified_here"]))
    _w(L, ca["reason"], "   ")
    a("")

    a("CHOICES IN FORCE")
    for ln in choices():
        a("   " + ln)
    a("")
    a("=" * 74)
    return "\n".join(L)


def choices():
    return [
        "[CHOICE 1] both renderings land side by side; neither supersedes.",
        "[CHOICE 2] ocean area 3.61e14 m^2 for the SLE -> Sv conversion.",
        "[CHOICE 3] 1 mm global mean SLE = 361.8 Gt.",
        "[CHOICE 4] rho_ice 917, rho_seawater 1027 for the floating-ice "
        "displacement residual.",
        "[CHOICE 5] the StommelBox grid list is six ordinary (range, n) "
        "choices, not a convergence study.",
        "[CHOICE 6] the gap blocks are re-indented IN MEMORY so the "
        "register's reader can see their fields; the delivered file is not "
        "touched, and the as-delivered count is reported beside it.",
    ]


def main(argv):
    if "--selftest" in argv:
        print("audit.py is the instrument, not the suite.")
        print("run: python3 thwaites-risk-audit/test_audit.py")
        return 2
    if "--choices" in argv:
        for ln in choices():
            print(ln)
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
