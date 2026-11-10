"""Ledger checker. stdlib only.

    python3 tools/check_ledger.py            # schema + cross-references
    python3 tools/check_ledger.py --tests    # also run the tests each admitted entry cites
    python3 tools/check_ledger.py --selftest # plant one defect per rule in a copy; each must fire

exit 0 = no FAIL, 1 = FAIL.
"""
import glob, os, re, subprocess, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.environ.get("LEDGER_ROOT", HERE)
sys.path.insert(0, HERE)
from tools import miniyaml

LAYERS = {"L0", "L1", "L2", "L3", "L4", "L5"}
STATUS = {"candidate", "admitted", "rejected", "placeholder"}
PCLASS = {"OBSERVED", "DERIVED", "PROPOSED"}
COMP = ["id", "layer", "equation", "assumes", "if_assumption_fails", "scope", "provenance", "admitted_by",
        "test_results", "open_issues", "depends_on", "status"]
BRANCH = ["id", "family", "status", "components", "links", "convergence_anchors", "runs", "open_issues", "note"]
BLOCK = ["id", "statement", "if_fails", "used_by", "used_by_runs", "open_issues", "status"]
RUN_FIELDS = ["code", "seed", "params", "results", "flags", "provenance", "feeds"]


def load_dir(sub):
    out = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "ledger", sub, "*.yaml"))):
        out[os.path.basename(p)[:-5]] = miniyaml.load(p)
    return out


def check(run_tests=False):
    fails, notes = [], []
    F = fails.append
    comps, branches, blocks = load_dir("components"), load_dir("branches"), load_dir("assumption_blocks")
    tests = {t["id"] for t in miniyaml.load(os.path.join(ROOT, "ledger", "tests.yaml"))["tests"]}
    runs = {os.path.basename(p)[:-3] for p in glob.glob(os.path.join(ROOT, "runs", "run_*.md"))}

    try:                                   # optional cross-check of the subset reader
        import yaml
        for p in glob.glob(os.path.join(ROOT, "ledger", "**", "*.yaml"), recursive=True):
            if os.path.basename(p) == "SCHEMA.yaml":
                continue
            with open(p) as f:
                if yaml.safe_load(f) != miniyaml.load(p):
                    F(f"{p}: miniyaml and PyYAML disagree")
        notes.append("PyYAML cross-check: ran")
    except ImportError:
        notes.append("PyYAML cross-check: NOT_TESTABLE (PyYAML absent)")

    def fields(kind, name, d, req):
        for k in req:
            if k not in d:
                F(f"{kind} {name}: field {k} dropped (write void)")
        for k in d:
            if k not in req:
                F(f"{kind} {name}: unknown field {k}")
        if d.get("id") != name:
            F(f"{kind} {name}: id != file name")
        if "status" in d and d["status"] not in STATUS:
            F(f"{kind} {name}: status {d['status']}")

    test_results = None
    if run_tests:
        sys.path.insert(0, os.path.join(ROOT, "tests"))
        import test_l0
        test_results = test_l0.run_all()

    for n, c in comps.items():
        fields("component", n, c, COMP)
        if c.get("layer") not in LAYERS:
            F(f"component {n}: layer {c.get('layer')}")
        pv = c.get("provenance", {})
        if not isinstance(pv, dict) or pv.get("class") not in PCLASS or "source" not in pv:
            F(f"component {n}: provenance")
        ab = c.get("admitted_by")
        if (c.get("status") == "admitted") != (ab != "void"):
            F(f"component {n}: status {c.get('status')} vs admitted_by {ab}")
        if ab != "void":
            if ab not in tests:
                F(f"component {n}: admitted_by {ab} not in tests.yaml")
            elif test_results is not None and test_results.get(ab) != "PASS":
                F(f"component {n}: admitting test {ab} -> {test_results.get(ab)}")
        ids = [a.get("id") for a in c.get("assumes", [])]
        iaf = c.get("if_assumption_fails")
        if ids and (not isinstance(iaf, dict) or sorted(iaf) != sorted(ids)):
            F(f"component {n}: if_assumption_fails keys != assumes ids")
        for a in c.get("assumes", []):
            b = a.get("block", "MISSING")
            if b == "MISSING" or "text" not in a:
                F(f"component {n}: assumption {a.get('id')} missing text/block")
            elif b != "void":
                if b not in blocks:
                    F(f"component {n}: block {b} missing")
                elif n not in blocks[b].get("used_by", []):
                    F(f"block {b}: used_by omits {n}")
        for d in c.get("depends_on", []):
            if d not in comps:
                F(f"component {n}: depends_on {d} missing")
        for tr in c.get("test_results", []):
            if tr.get("test", "void") != "void" and tr["test"] not in tests:
                F(f"component {n}: test_results cites {tr['test']}")
            if tr.get("run", "void") != "void" and tr["run"] not in runs:
                F(f"component {n}: test_results cites {tr['run']}")
    for n, b in blocks.items():
        fields("block", n, b, BLOCK)
        for u in b.get("used_by", []):
            if u not in comps or n not in [a.get("block") for a in comps[u].get("assumes", [])]:
                F(f"block {n}: used_by {u} does not name it back")
        for r in b.get("used_by_runs", []):
            if r not in runs:
                F(f"block {n}: run {r} missing")
    anchors = {}
    for n, b in branches.items():
        fields("branch", n, b, BRANCH)
        for c in b.get("components", []):
            if c not in comps:
                F(f"branch {n}: component {c} missing")
        for l in b.get("links", []):
            if l not in branches:
                F(f"branch {n}: link {l} missing")
        for r in b.get("runs", []):
            if r not in runs:
                F(f"branch {n}: run {r} missing")
        for a in b.get("convergence_anchors", []):
            anchors.setdefault(a["id"], []).append((n, a))
    for aid, holders in anchors.items():
        between = holders[0][1]["between"]
        if sorted(h[0] for h in holders) != sorted(between):
            F(f"anchor {aid}: carried by {[h[0] for h in holders]}, between {between}")
        if any(h[1] != holders[0][1] for h in holders):
            F(f"anchor {aid}: copies differ")
    homeless = [c for c in comps if not any(c in b.get("components", []) for b in branches.values())]
    for c in homeless:
        F(f"component {c}: in no branch")
    for r in sorted(runs):
        text = open(os.path.join(ROOT, "runs", r + ".md")).read()
        for f_ in RUN_FIELDS:
            m = re.search(rf"^{f_}\s*:\s*(.*)$", text, re.M)
            if not m:
                F(f"{r}.md: field {f_} dropped")
            elif f_ == "code" and m.group(1).strip() != "void" and not os.path.exists(os.path.join(ROOT, m.group(1).strip())):
                F(f"{r}.md: code {m.group(1).strip()} not in tree")
    rm = miniyaml.load(os.path.join(ROOT, "ledger", "regime_map.yaml"))
    for fam, row in rm["cells"].items():
        if fam not in branches or sorted(row) != sorted(rm["regimes"]):
            F(f"regime_map: row {fam}")
    count = lambda d: {s: sum(1 for x in d.values() if x.get("status") == s) for s in sorted(STATUS)}
    return fails, notes, dict(components=count(comps), branches=count(branches), blocks=len(blocks), runs=len(runs), tests=len(tests))


def selftest():
    """Plant one defect per rule in a copy; each must produce a FAIL naming it."""
    import shutil, tempfile
    plants = [
        ("dropped field", "ledger/components/L1_LEACHING.yaml", "scope:", "#scope:", "field scope dropped"),
        ("admitted without test", "ledger/components/L1_LEACHING.yaml", "status: candidate", "status: admitted", "vs admitted_by"),
        ("dangling dependency", "ledger/components/L1_LEACHING.yaml", "  - L0_N_BUDGET", "  - L0_NOPE", "depends_on L0_NOPE"),
        ("one-way block link", "ledger/assumption_blocks/AB_WELL_MIXED.yaml", "  - L1_UPTAKE_MM\n", "", "used_by omits L1_UPTAKE_MM"),
        ("anchor on one branch only", "ledger/branches/BR_FIRE_MEANFIELD.yaml", "drought >= 0.5", "drought >= 0.4", "anchor CA_1: copies differ"),
        ("run field dropped", "runs/run_3.md", "seed       :", "sead       :", "field seed dropped"),
    ]
    bad = 0
    for name, rel, old, new, expect in plants:
        tmp = tempfile.mkdtemp()
        try:
            for d in ("ledger", "runs"):
                shutil.copytree(os.path.join(HERE, d), os.path.join(tmp, d))
            path = os.path.join(tmp, rel)
            text = open(path).read()
            assert old in text, (name, "plant site missing")
            open(path, "w").write(text.replace(old, new, 1))
            env = dict(os.environ, LEDGER_ROOT=tmp)
            out = subprocess.run([sys.executable, os.path.abspath(__file__)], env=env, capture_output=True, text=True)
            fired = out.returncode != 0 and (expect is None or expect in out.stdout + out.stderr)
        finally:
            shutil.rmtree(tmp)
        print(("FIRED " if fired else "SILENT"), name)
        bad += not fired
    print(f"selftest: {len(plants)} planted, {bad} silent")
    return bad


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(1 if selftest() else 0)
    fails, notes, summ = check("--tests" in sys.argv)
    print("components", summ["components"])
    print("branches  ", summ["branches"])
    print(f"blocks {summ['blocks']}  runs {summ['runs']}  tests {summ['tests']}")
    for n in notes:
        print("note:", n)
    for f in fails:
        print("FAIL", f)
    print("FAIL" if fails else "OK", f"({len(fails)} failures)")
    sys.exit(1 if fails else 0)
