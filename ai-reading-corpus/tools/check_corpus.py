"""
check_corpus.py -- recompute every number the ledgers cite; verify the manifest.

CC0. Python >= 3.8, standard library only, no network.

Statuses (this tool's own set; not mapped onto any source vocabulary):
  PASS   the stated value or property was reproduced
  FLAG   a recorded finding (ledger/conflicts.jsonl) still stands
  FAIL   the corpus contradicts itself or a stated value did not reproduce
  NOT_TESTABLE  the check needs a sibling Simulators checkout and none was found (never PASS)

Run:
  python3 tools/check_corpus.py           # table; exit 0 = no FAIL, 1 = FAIL
  python3 tools/check_corpus.py --json    # machine-readable rows
  SIMULATORS_PATH=/path/to/Simulators python3 tools/check_corpus.py   # enables sibling checks
"""

import datetime
import os
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")  # keep sources/ byte-identical to MANIFEST
ROOT = Path(__file__).resolve().parent.parent
LAB = ROOT / "sources/scope-audit/lab/v0.5"
LAB_V01 = ROOT / "sources/scope-audit/lab/superseded/v0.1"
H0 = ROOT / "sources/habitat/H0_basis.md"
H1 = ROOT / "sources/habitat/H1_deep_research_report.md"
R4 = ROOT / "sources/scope-audit/report/R4_v0.5.md"
AOS = ROOT / "sources/aos"
DROP = AOS / "simulators-drop"
R5 = AOS / "R5_constraint_chain_report.md"
T0 = AOS / "T0_ucsd_study_summary.md"
T1 = AOS / "T1_session_transcript.md"


def simulators():
    """Sibling Simulators checkout, or None. Never cloned or fetched by this tool."""
    cands = [os.environ.get("SIMULATORS_PATH"), ROOT.parent,  # ROOT.parent: landed inside Simulators
             ROOT.parent / "Simulators", ROOT.parent / "jinnz2/simulators"]
    for c in cands:
        if c and (Path(c) / "scope-bound-shapes/scope.py").is_file():
            return Path(c)
    return None

rows = []


def row(check, status, detail):
    rows.append({"check": check, "status": status, "detail": detail})


def text(p):
    return p.read_text(encoding="utf-8")


def read_jsonl(p):
    return [json.loads(line) for line in text(p).splitlines() if line.strip()]


def lab_eval(code):
    """Run code inside the v0.5 lab directory; it must print one JSON value."""
    prelude = "import sys, json; sys.path.insert(0, '.')\n"
    out = subprocess.run([sys.executable, "-c", prelude + code], cwd=LAB,
                         env=ENV, capture_output=True, text=True, timeout=300)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip().splitlines()[-1])
    return json.loads(out.stdout)


# --- structure -------------------------------------------------------------

def check_manifest():
    m = json.loads(text(ROOT / "MANIFEST.json"))
    listed = {e["path"]: e["sha256"] for e in m["files"]}
    bad = [p for p, h in listed.items()
           if not (ROOT / p).is_file()
           or hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h]
    on_disk = {str(p.relative_to(ROOT)) for p in (ROOT / "sources").rglob("*")
               if p.is_file() and "__pycache__" not in p.parts}
    unlisted = sorted(on_disk - set(listed))
    if bad or unlisted:
        row("manifest", "FAIL", f"hash/missing: {bad[:3]}; unlisted: {unlisted[:3]}")
    else:
        row("manifest", "PASS", f"{len(listed)} files, every sha256 matches, nothing unlisted")


def check_ledgers(check_names):
    claims = read_jsonl(ROOT / "ledger/claims.jsonl")
    conflicts = read_jsonl(ROOT / "ledger/conflicts.jsonl")
    gaps = read_jsonl(ROOT / "ledger/gaps.jsonl")
    ids = [x["id"] for x in claims + conflicts + gaps]
    problems = [f"duplicate id {i}" for i in set(ids) if ids.count(i) > 1]
    known = set(ids)
    for c in claims:
        for key in ("feeds", "depends_on", "conflicts"):
            problems += [f"{c['id']}.{key} -> {r}" for r in c.get(key, []) if r not in known]
        if c.get("check") and c["check"] not in check_names:
            problems.append(f"{c['id']} names unknown check {c['check']}")
        if c["bundle_status"].startswith("RECOMPUTED") and not c.get("check"):
            problems.append(f"{c['id']} says RECOMPUTED but names no check")
        if c["bundle_status"] == "FLAG" and not c.get("conflicts"):
            problems.append(f"{c['id']} is FLAG with no conflict id")
    for g in gaps:
        problems += [f"{g['id']} -> {r}" for r in g.get("claims", []) if r not in known]
    for x in conflicts:
        if x.get("check") and x["check"] not in check_names:
            problems.append(f"{x['id']} names unknown check {x['check']}")
    if problems:
        row("ledgers", "FAIL", "; ".join(problems[:5]))
    else:
        row("ledgers", "PASS", f"{len(claims)} claims, {len(conflicts)} conflicts, "
                               f"{len(gaps)} gaps; all ids unique, all references resolve")


# --- lab: stated numbers -----------------------------------------------------

def check_lab_tests():
    out = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                         cwd=LAB, env=ENV, capture_output=True, text=True, timeout=600)
    m = re.search(r"Ran (\d+) tests?", out.stderr)
    n = int(m.group(1)) if m else -1
    ok = out.returncode == 0 and n == 90
    row("lab_tests", "PASS" if ok else "FAIL", f"ran {n}, stated 90, exit {out.returncode}")


def check_maxwell():
    p = lab_eval("from scope_audit_lab import waves\n"
                 "print(json.dumps(waves.em_unification_comparison().to_dict()['payload']['comparison']))")
    r, u, z = p["residual_m_per_s"], p["prediction_uncertainty_m_per_s"], p["normalized_residual"]
    ok = round(r, 7) == -6.5e-6 and round(u, 3) == 0.032 and abs(abs(z) - 2e-4) < 1e-5
    row("maxwell_residual", "PASS" if ok else "FAIL",
        f"residual {r:.3e} m/s (stated -6.5e-6), u {u:.4f} (stated 0.032), |z| {abs(z):.2e} (stated 2e-4)")


def scan_counts(module, runner):
    return lab_eval(
        f"from scope_audit_lab import {module}\n"
        f"out = {{}}\n"
        f"for r in {module}.{runner}():\n"
        f"    p = r.to_dict()['payload']\n"
        f"    if 'candidate_regions' in p: out[p['scan_label']] = len(p['candidate_regions'])\n"
        f"print(json.dumps(out))")


def check_waves_counts():
    c = scan_counts("waves", "run_waves_demo_suite")
    got = {k.split(": ")[1].split(" (")[0]: v for k, v in c.items()}
    want = {"Malus contrast": 24, "longitudinal rotation": 0, "EM spectrum": 23,
            "sound speed vs temperature": 12}
    bad = {k: (got.get(k), v) for k, v in want.items() if got.get(k) != v}
    row("waves_counts", "FAIL" if bad else "PASS",
        f"mismatch {bad}" if bad else "Malus 24 / longitudinal 0 / spectrum 23 / sound 12")


def check_physics_counts():
    p = lab_eval(
        "from scope_audit_lab import physics_demos\n"
        "recs = [r.to_dict()['payload'] for r in physics_demos.run_physics_demo_suite()]\n"
        "out = {'scans': {}, 'sweep': None, 'null': None, 'coupling': None, 'perm_max': None, 'eit': None}\n"
        "for p in recs:\n"
        "    if 'candidate_regions' in p:\n"
        "        out['scans'][p['scan_label']] = len(p['candidate_regions'])\n"
        "        if 'stopped_light' in p['scan_label']:\n"
        "            o = [c['output_value'] for c in p['cases']]\n"
        "            out['eit'] = [[abs(b - a) / abs(a), abs(b - a)] for a, b in zip(o, o[1:])]\n"
        "    elif 'per_threshold' in p:\n"
        "        out['sweep'] = [t['candidate_region_count'] for t in p['per_threshold']]\n"
        "    elif 'recorded_summary' in p:\n"
        "        out['null'] = p['recorded_summary']\n"
        "    elif 'coincidence_record' in p:\n"
        "        out['coupling'] = p['coincidence_record']\n"
        "    elif 'scans' in p:\n"
        "        out['perm_max'] = max(a['appearance_count'] for a in p['region_appearances']\n"
        "                              if 0 in a['appears_in_scans'])\n"
        "print(json.dumps(out))")
    findings = []
    if p["sweep"] != [32, 24, 8, 0]:
        findings.append(f"sweep {p['sweep']} != [32,24,8,0]")
    rel = [x[0] for x in p["eit"]]
    absd = [x[1] for x in p["eit"]]
    if not (len(rel) == 19 and max(rel) - min(rel) < 1e-6 and round(rel[0], 4) == 0.3842):
        findings.append(f"EIT relative not constant 0.3842 over 19 ({len(rel)}, {rel[0]:.4f})")
    if not (round(min(absd), 2) == 0.03 and round(max(absd)) == 163):
        findings.append(f"EIT abs span {min(absd):.3f}-{max(absd):.1f}")
    grav = next(v for k, v in p["scans"].items() if "gravity" in k)
    n = p["null"]
    if not (grav == 18 and round(n["mean_candidate_regions"], 1) == 9.6
            and n["max_candidate_regions"] == 14 and n["replications"] == 25):
        findings.append(f"gravity {grav}, null {n}")
    cp = p["coupling"]
    split = tuple(len(cp[k]) for k in ("coincident_pairs", "factor_a_only_pairs", "factor_b_only_pairs"))
    if split != (4, 0, 0):
        findings.append(f"coupling {split} != (4, 0, 0)")
    if p["perm_max"] > 5:
        findings.append(f"doppler given-order pair max {p['perm_max']} > 5")
    row("physics_counts", "FAIL" if findings else "PASS", "; ".join(findings) or
        "sweep 32/24/8/0; EIT rel 0.3842 x19, abs 0.03-163; gravity 18 vs null "
        f"mean {n['mean_candidate_regions']} max 14; coupling 4/0/0; doppler max {p['perm_max']} of 26")


def check_v01_stream():
    stream = LAB_V01 / "demo_output.jsonl"
    out = subprocess.run([sys.executable, "-m", "scope_audit_lab", "validate", str(stream)],
                         cwd=LAB, env=ENV, capture_output=True, text=True, timeout=120)
    ok = out.returncode == 0
    row("v01_stream_validates", "PASS" if ok else "FAIL",
        f"v0.5 validator on v0.1 demo stream: exit {out.returncode}")


def check_instruments():
    results = []
    for name in ("physical_discrepancy.py", "physical_limits_suite.py"):
        out = subprocess.run([sys.executable, name, "--selftest"], cwd=ROOT / "sources/instruments",
                             env=ENV, capture_output=True, text=True, timeout=60)
        results.append((name, out.returncode == 0 and "selftest ok" in out.stdout))
    ok = all(r for _, r in results)
    row("instruments_selftest", "PASS" if ok else "FAIL", ", ".join(f"{n}: {'ok' if r else 'failed'}" for n, r in results))


# --- external anchors that need no network ----------------------------------

def check_landauer():
    e = 1.380649e-23 * 300 * math.log(2)
    row("landauer_300K", "PASS" if round(e, 23) == 2.87e-21 else "FAIL",
        f"k_B * 300 K * ln 2 = {e:.4e} J/bit (stated ~2.87e-21); experimental claims NOT_CHECKED")


# --- recorded findings (FLAG while they stand) -------------------------------

def check_esa_60_days():
    d = datetime.date(2026, 7, 14) + datetime.timedelta(days=60)
    h1 = "September 14, 2026** (60 days post-publication)" in text(H1)
    row("esa_60_days", "FLAG" if h1 and d.isoformat() == "2026-09-12" else "PASS",
        f"2026-07-14 + 60 d = {d}; H1 states Sept 14 as 60 days; R4 states Sept 12 (X-01)")


def check_r4_fr_url():
    stale = "federalregister.gov/documents/2025/04/17/2025-06746" in text(R4)
    row("r4_fr_url", "FLAG" if stale else "PASS",
        "R4 cites a 2025-04-17 FR URL for the 2026-07-14 final rule (X-02)" if stale else "link fixed")


def check_h1_gap_count():
    t = text(H1)
    sec = t.split("## 9. Open Gaps", 1)[1].split("\n---", 1)[0]
    items = len(re.findall(r"^\d+\. \*\*", sec, flags=re.M))
    says_eighth = "add an eighth" in sec
    row("h1_gap_count", "FLAG" if says_eighth and items == 7 else "PASS",
        f"H1 §9 lists {items} items while saying 'add an eighth' (X-05)")


def check_lab_readme_stale():
    t = text(LAB / "README.md")
    hits = [s for s in ("## Not implemented in 0.3", "`stopped_light`") if s in t]
    row("lab_readme_stale", "FLAG" if hits else "PASS", f"v0.5 README still carries {hits} (X-07)")


def check_missing_instruments():
    names = ("gating_diagnostic.py", "physical_bounds.py", "limit_detection.py")
    present = {p.name for p in (ROOT / "sources").rglob("*.py")}
    missing = [n for n in names if n not in present and n in text(R4)]
    row("missing_instruments", "FLAG" if missing else "PASS",
        f"named in R4 §1, absent from bundle: {missing} (X-08)")

# --- AOS chain (sources/aos) -------------------------------------------------

MU0 = 4e-7 * math.pi
KT300 = 1.380649e-23 * 300


def kaplan_period(n, ms=0.9e6, keff=0.5e6, aex=15e-12):
    t = 0.6e-9 * n
    d0 = 4 * math.sqrt(aex * keff) / (MU0 * ms ** 2 / 2)
    return t * math.exp(math.pi * d0 / (2 * t) + math.log(math.pi) - 0.5 - math.log(2))


def check_aos_kaplan():
    stated = {3: 0.25, 5: 224e-6, 7: 12.5e-6, 9: 2.7e-6, 10: 1.6e-6, 12: 0.75e-6}
    got = {n: kaplan_period(n) for n in stated}
    bad = {n: f"{got[n]:.3g}" for n, v in stated.items() if abs(got[n] / v - 1) > 0.05}
    t0 = "~2.7 mm (N=1) to ~0.9 μm (N=9)" in text(T0)
    if bad:
        row("aos_kaplan", "FAIL", f"R5 table not reproduced at N={bad}")
    else:
        row("aos_kaplan", "FLAG" if t0 else "PASS",
            f"R5 table N=3..12 reproduces within 5 pct (N=9 {got[9] * 1e6:.2f} um); T0's '2.7 mm (N=1) / "
            f"0.9 um (N=9)' does not come from these parameters, N=1 gives {kaplan_period(1):.1e} m (X-09)")


def check_aos_delta():
    l60 = lambda k, t: math.sqrt(60 * KT300 / (k * t)) * 1e9
    vals = [l60(0.5e6, 12e-9), l60(0.5e6, 5.4e-9), l60(0.3e6, 5.4e-9),
            math.sqrt(60 * KT300 / (5e6 * 10e-9) / (math.pi / 4)) * 1e9]
    want = [6.4, 9.6, 12.4, 2.5]
    at30 = [0.3e6 * (30e-9) ** 2 * 5.4e-9 / KT300, 0.5e6 * (30e-9) ** 2 * 12e-9 / KT300]
    dep = 0.95 * 1.602177e-19 / KT300
    ok = (all(abs(v - w) < 0.06 * w for v, w in zip(vals, want))
          and abs(at30[0] - 350) < 10 and abs(at30[1] - 1300) < 20 and abs(dep - 38) <= 8)
    row("aos_delta", "PASS" if ok else "FAIL",
        "Delta=60 at %s nm (stated 6.4/9.6/12.4/2.5); Delta@30nm %.0f-%.0f (stated 350-1300); "
        "0.95 eV -> Delta %.1f (stated 38+/-8)" % ("/".join("%.2f" % v for v in vals), at30[0], at30[1], dep))


def check_aos_pulse_arithmetic():
    dwell = 1.0 / 5.0            # 1 um spot at 5 um/s
    hi = 2.0 / 1.0               # 2 um spot at 1 um/s
    ok = round(dwell * 1000) == 200 and round(hi * 1000) == 2000
    row("aos_pulse_arithmetic", "PASS" if ok else "FAIL",
        "1 kHz x (1 um / 5 um/s) = %d pulses; x (2 um / 1 um/s) = %d (stated 200-2,000)" % (dwell * 1000, hi * 1000))


def check_aos_energy():
    area = lambda d_um: math.pi * (d_um / 2 * 1e-4) ** 2
    ucsd = 7.6e-6 * area(0.76) * 1e3 * 1e12
    hds = 4e-3 * area(0.76) * 100 * 1e12
    tb = 3.7e-3 * area(0.053) * 100 * 1e12
    toggle = 6 * (40e-7 * 40e-7 * 20e-7) * 1e18
    stated = "~12 pJ per bit" in text(R5) and "~640 pJ" in text(R5) and "~120 aJ" in text(R5)
    row("aos_energy", "FLAG" if stated else "PASS",
        "R5 states 12 pJ / 640 pJ / 4.9 pJ / 120 aJ; stated inputs give %.1f pJ / %.0f pJ / %.1f pJ / %.0f aJ; "
        "12 and 640 equal fluence x (0.4 um)^2 x pulses without pi (X-10)" % (ucsd, hds, tb, toggle))


def check_aos_latency():
    t = text(R5)
    claim = "even the multi-pulse AO-HDS protocols" in t and "~2.7 ns" in t
    row("aos_latency", "FLAG" if claim else "PASS",
        "8 pulses @3 GHz = %.2f ns is the dual-pulse record; AO-HDS 100 pulses = %.0f ns; "
        "same-protocol kHz gap = %.1f orders, R5 says ~9 (X-11)" % (8 / 3e9 * 1e9, 100 / 3e9 * 1e9,
                                                                   math.log10(1 / (1000 / 3e9))))


def check_aos_crpt_carried():
    carriers = []
    for name in ("granular-reptation.json", "ife-amplifier-scaling.json"):
        case = json.loads(text(DROP / "constraint-assembly/cases" / name))
        if any("CrPt" in o and "coherent nonthermal IFE switching" in o and "simulation" not in o
               for o in case.get("open", [])):
            carriers.append(name)
    voided = "simulation" in text(R5) and "2104.11820" in text(R5)
    row("aos_crpt_carried", "FLAG" if carriers and voided else "PASS",
        f"R5 voids arXiv:2104.11820 as a simulation; still carried as shown in {carriers} (X-12)")


def check_aos_ez_contradiction():
    zero = "E_z(0)=0 by symmetry" in text(T0)
    case = json.loads(text(DROP / "constraint-assembly/cases/aos-vector-beam.json"))
    zero_case = any("Ez(0)=0" in c["name"] for c in case["components"])
    strong = "strong longitudinal E_z component" in text(R5)
    row("aos_ez_contradiction", "FLAG" if (zero or zero_case) and strong else "PASS",
        "T0 and the case file: Ez(0)=0 at focus; R5 §1.1: 'strong longitudinal E_z ... is what confines' (X-17)")


def check_aos_weld_encoding():
    spreads = {}
    for name in ("optical_switching_speed.json", "deterministic_switching.json"):
        w = json.loads(text(DROP / "category-weld/welds" / name))
        per_case = []
        for case in w["divergences"]:  # same rule as weld.py case_spread: needs >= 2 paired components
            rel = [r["after"] / r["before"] for r in case.get("readings", {}).values()
                   if r.get("before") and r.get("after") is not None]
            if len(rel) > 1:
                per_case.append(max(rel) / min(rel))
        spreads[name] = max(per_case) if per_case else None
    row("aos_weld_encoding", "FLAG",
        f"spreads {spreads} come from low/high range ends stored as before/after, not from a "
        f"field movement (X-15)")


def stage(sim, tmp):
    for d in ("category-weld", "constraint-assembly", "presented-binary"):
        shutil.copytree(sim / d, tmp / d, ignore=shutil.ignore_patterns("__pycache__"))
    for p in DROP.rglob("*.json"):
        if "superseded" in p.parts:
            continue
        rel = p.relative_to(DROP)
        shutil.copy2(p, tmp / rel)


def check_aos_sim_instruments(sim):
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        stage(sim, tmp)
        run = lambda d, *a: subprocess.run([sys.executable, *a], cwd=tmp / d, env=ENV,
                                           capture_output=True, text=True, timeout=120)
        w = run("category-weld", "weld.py")
        a = run("constraint-assembly", "assemble.py")
        b = run("presented-binary", "binary_audit.py", "--case", "aos-thickness-ceiling")
    weld_ok = w.returncode == 0 and "optical switching" in w.stdout and "deterministic swit" in w.stdout
    asm_ok = a.returncode == 0 and all(k in a.stdout for k in
                                       ("aos-vector-beam", "granular-reptation", "ife-amplifier-scaling"))
    pb_ok = b.returncode == 0 and "documented=5 asserted=3 absent=3 share=0.46" in b.stdout
    ok = weld_ok and asm_ok and pb_ok
    row("aos_sim_instruments", "PASS" if ok else "FAIL",
        f"against {sim.name}: weld.py {'ok' if weld_ok else 'fail'}, assemble.py {'ok' if asm_ok else 'fail'}, "
        f"binary_audit 5/3/3 share 0.46 {'ok' if pb_ok else 'fail'}")


def check_aos_scope_verdict(sim):
    out = subprocess.run([sys.executable, str(DROP / "scope-bound-shapes/aos_topology_scope.py")],
                         cwd=sim / "scope-bound-shapes", env=dict(ENV, PYTHONPATH="."),
                         capture_output=True, text=True, timeout=60)
    verdict = re.search(r"^COMPARE (\S+)", out.stdout, re.M)
    v = verdict.group(1) if verdict else "none"
    refused = "REFUSED_BY_CONSTRAINT" in out.stdout
    claims = "corroborating with zero declared collisions" in text(T1)
    if out.returncode != 0 or not refused:
        row("aos_scope_verdict", "FAIL", f"exit {out.returncode}, verdict {v}, refusal {refused}")
    else:
        row("aos_scope_verdict", "FLAG" if claims and v != "CORROBORATE" else "PASS",
            f"tool verdict {v}, corroborate None, infer_frozen REFUSED_BY_CONSTRAINT; T1 reports "
            f"'corroborating' (X-16)")


def check_aos_case_number(sim):
    drop = DROP / "uninstrumented/cases/024aoswritelatency.md"
    h = hashlib.sha256(drop.read_bytes()).hexdigest()
    cases = sim / "uninstrumented/cases"
    landed = sorted(p.name for p in cases.glob("*.md")
                    if hashlib.sha256(p.read_bytes()).hexdigest() == h)
    taken = sorted(p.name for p in cases.glob("024*") if p.name not in landed)
    if landed and not any(n.startswith("024") for n in landed):
        row("aos_case_number", "PASS",
            f"landed as {landed}; 024 held by {taken}; the file's own header and aos-vector-beam "
            f"open[1] still say 024 (delivered text, X-20)")
    else:
        row("aos_case_number", "FLAG",
            f"Simulators uninstrumented/cases holds {taken}; drop file 024aoswritelatency.md "
            f"landed as {landed or 'nothing'} (X-20)")


def sibling(fn, name):
    def run():
        sim = simulators()
        if sim is None:
            row(name, "NOT_TESTABLE", "no Simulators checkout (set SIMULATORS_PATH)")
        else:
            fn(sim)
    return run


# --- biomimicry boundary -------------------------------------------------------

def _boundary():
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(ROOT / "tools"))
    import boundary
    return boundary


def check_boundary_log():
    b = _boundary()
    problems = b.verify()
    data = b.load()
    if problems:
        row("boundary_log", "FAIL", "; ".join(problems[:3]))
    else:
        n = len(b.read_log())
        row("boundary_log", "PASS", f"table {b.table_sha256(data)[:12]} matches changelog entry {n}; "
                                    f"chain intact; render current; adopted_line {data['adopted_line']}")


def check_boundary_hb24():
    """X-22: a HB-24 row that is IN under no candidate line."""
    b = _boundary()
    data = b.load()
    m = b.matrix(data)
    hb = [c for c in data["cases"] if c["in_hb24"]]
    h0 = text(H0)
    missing = [c["id"] for c in hb if c["name"].split()[0].lower() not in h0.lower()]
    if len(hb) != 6 or missing:
        row("boundary_hb24", "FAIL", f"{len(hb)} HB-24 rows; not found in H0: {missing}")
        return
    nowhere = [c["id"] for c in hb if "IN" not in m[c["id"]].values()]
    if nowhere:
        row("boundary_hb24", "FLAG", f"HB-24 rows IN under no candidate line: {nowhere} (X-22)")
    else:
        row("boundary_hb24", "PASS", "every HB-24 row is IN under at least one line")


CHECKS = {
    "manifest": check_manifest,
    "lab_tests": check_lab_tests,
    "maxwell_residual": check_maxwell,
    "waves_counts": check_waves_counts,
    "physics_counts": check_physics_counts,
    "v01_stream_validates": check_v01_stream,
    "instruments_selftest": check_instruments,
    "landauer_300K": check_landauer,
    "esa_60_days": check_esa_60_days,
    "r4_fr_url": check_r4_fr_url,
    "h1_gap_count": check_h1_gap_count,
    "lab_readme_stale": check_lab_readme_stale,
    "missing_instruments": check_missing_instruments,
    "aos_kaplan": check_aos_kaplan,
    "aos_delta": check_aos_delta,
    "aos_pulse_arithmetic": check_aos_pulse_arithmetic,
    "aos_energy": check_aos_energy,
    "aos_latency": check_aos_latency,
    "aos_crpt_carried": check_aos_crpt_carried,
    "aos_ez_contradiction": check_aos_ez_contradiction,
    "aos_weld_encoding": check_aos_weld_encoding,
    "aos_sim_instruments": sibling(check_aos_sim_instruments, "aos_sim_instruments"),
    "aos_scope_verdict": sibling(check_aos_scope_verdict, "aos_scope_verdict"),
    "aos_case_number": sibling(check_aos_case_number, "aos_case_number"),
    "boundary_log": check_boundary_log,
    "boundary_hb24": check_boundary_hb24,
}


def main():
    check_ledgers(set(CHECKS))
    for name, fn in CHECKS.items():
        try:
            fn()
        except Exception as exc:  # a check that cannot run is a FAIL, never a PASS
            row(name, "FAIL", f"could not run: {exc}")
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=1))
    else:
        w = max(len(r["check"]) for r in rows)
        for r in rows:
            print(f"{r['status']:<12} {r['check']:<{w}}  {r['detail']}")
        counts = {s: sum(r["status"] == s for r in rows) for s in ("PASS", "FLAG", "NOT_TESTABLE", "FAIL")}
        print(f"\n{len(rows)} checks: {counts}")
    sys.exit(1 if any(r["status"] == "FAIL" for r in rows) else 0)


if __name__ == "__main__":
    main()
