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
# the seven tools of the staged build (work order 2026-11-11); each is trusted only after its gate
STAGED_SEVEN = ("multi_seed_ensemble", "ablation", "support_match", "parameter_recovery", "residual_regression",
                "equation_family_swap", "assumption_block_trace")
RUN_FIELDS = ["status", "code", "seed", "params", "results", "flags", "provenance", "feeds"]


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
    regimes = [c for c in comps if c.startswith("L5_OBS_")]   # item 3: separate rows, no shared currency
    for c in regimes:
        for d in comps[c].get("depends_on", []):
            if d in regimes:
                F(f"component {c}: depends_on {d}; observer regimes share no currency")
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
    # ---- toolkit, cards, anchors
    import hashlib
    from ledger.toolkit import coincidence_card as cc
    TOOL = ["id", "code", "diagnoses", "inputs", "outputs", "cannot_see", "other_domains_it_could_see_into",
            "used_in", "open_issues", "status", "gate", "blocked_on"]
    tools_ = {os.path.basename(p)[:-5]: miniyaml.load(p)
              for p in sorted(glob.glob(os.path.join(ROOT, "ledger", "toolkit", "*.yaml")))}
    gate_results = None
    if run_tests:
        sys.path.insert(0, HERE)
        from tests import test_toolkit
        from ledger.toolkit import gate as G_
        gate_results = {t: G_.summary(test_toolkit.run(t)) for t in test_toolkit.GATED}
    for n, t in tools_.items():
        fields("tool", n, t, TOOL)
        built = t.get("code") != "void"
        if t.get("status") == "placeholder" and built and t.get("blocked_on") == "void":
            F(f"tool {n}: placeholder with code {t.get('code')} and no blocked_on")
        if t.get("status") != "placeholder" and not built:
            F(f"tool {n}: status {t.get('status')} with code void")
        if built and not os.path.exists(os.path.join(HERE, t.get("code", "MISSING"))):
            F(f"tool {n}: code {t.get('code')} not in tree")
        # work order 2026-11-11: the brief's seven are trusted only after the gate
        if n in STAGED_SEVEN and built:
            g = t.get("gate")
            if not isinstance(g, dict) or g.get("verdict") != "PASS":
                F(f"tool {n}: built but its gate is not PASS ({g if not isinstance(g, dict) else g.get('verdict')})")
            elif gate_results is not None:
                if n not in gate_results:
                    F(f"tool {n}: gate recorded but tests/test_toolkit.py does not run it")
                elif gate_results[n]["verdict"] != "PASS":
                    F(f"tool {n}: gate re-run reads {gate_results[n]['verdict']}")
                elif gate_results[n]["known_answer"] != g.get("known_answer") or gate_results[n]["null_legs"] != g.get("null_legs"):
                    F(f"tool {n}: gate re-run differs from the recorded gate")
            for f_ in ("inputs", "outputs"):
                if t.get(f_) in ("void", [], None):
                    F(f"tool {n}: built with {f_} void")
        if not t.get("diagnoses"):
            F(f"tool {n}: lists no deviation it diagnoses")
        for r in t.get("used_in", []):
            if r not in runs:
                F(f"tool {n}: run {r} missing")
    # ---- gate rule: INCOMPLETE run <-> NEEDS_TOOL.md <-> toolkit entry
    needs_path = os.path.join(ROOT, "ledger", "NEEDS_TOOL.md")
    needs, cleared = [], []
    if os.path.exists(needs_path):
        section = "open"
        for line in open(needs_path):
            if line.startswith("## Cleared"):
                section = "cleared"
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if section == "open" and len(cells) == 5 and re.match(r"run_\d+$", cells[2]):
                needs.append(cells)
                if not all(cells):
                    F(f"NEEDS_TOOL: empty cell in row {cells}")
            elif section == "cleared" and len(cells) == 6 and re.match(r"run_\d+$", cells[2]):
                cleared.append(cells)
                if not all(cells):
                    F(f"NEEDS_TOOL cleared: empty cell in row {cells}")
    # a row leaves the open table only when the tool passed its gate AND was run on that trigger
    open_keys = {(c[0], c[1], c[2]) for c in needs}
    for tool, trig, r, _, by, _ in cleared:
        t = tools_.get(tool)
        if t is None:
            F(f"NEEDS_TOOL cleared: {tool} has no entry in ledger/toolkit/")
            continue
        if (tool, trig, r) in open_keys:
            F(f"NEEDS_TOOL cleared: {tool} / {r} is in both tables")
        g = t.get("gate")
        if not isinstance(g, dict) or g.get("verdict") != "PASS":
            F(f"NEEDS_TOOL cleared: {tool} / {r} removed but the tool's gate is not PASS")
        if t.get("status") == "placeholder":
            F(f"NEEDS_TOOL cleared: {tool} / {r} removed but the tool is a placeholder")
        if by not in runs:
            F(f"NEEDS_TOOL cleared: {tool} / {r} cleared by {by}, which is not a run")
        elif by not in t.get("used_in", []):
            F(f"NEEDS_TOOL cleared: {tool} / {r} cleared by {by}, but the tool's used_in omits {by}")
    owed_runs = []
    for tool, _, r, _, _ in needs:
        if tool not in tools_:
            F(f"NEEDS_TOOL: {tool} has no entry in ledger/toolkit/")
        elif tools_[tool].get("status") != "placeholder" and r not in tools_[tool].get("used_in", []):
            # 2026-11-11: was a FAIL. A built tool not yet run on a trigger is a state the staged build
            # passes through, not a defect; the invariant (the row cannot leave until the tool ran on it
            # and passed its gate) is enforced on the cleared table above. Counted and printed instead.
            owed_runs.append(f"{tool} built, not yet run on {r}")
        if r not in runs:
            F(f"NEEDS_TOOL: run {r} missing")
    # ---- STATUS_MAP: every status on both axes has an entry with every field
    RUN_AXIS = ("COMPLETE", "INCOMPLETE", "REPORTED")
    CARD_AXIS = ("OPEN", "PROVISIONAL", "RESOLVED", "CURIOSITY")
    MAP_FIELDS = ("means", "goal trust it", "goal explore", "goal report now", "forbidden", "exits to")
    smap, pairs_listed = {}, set()
    map_path = os.path.join(ROOT, "ledger", "STATUS_MAP.md")
    if not os.path.exists(map_path):
        F("ledger/STATUS_MAP.md missing")
    else:
        cur = None
        for line in open(map_path):
            m = re.match(r"### (RUN|CARD) (\w+)\s*$", line)
            if m:
                cur = (m.group(1), m.group(2)); smap[cur] = {}
                continue
            m = re.match(r"- ([a-z ]+): (.+)", line)
            if m and cur:
                smap[cur][m.group(1)] = m.group(2).strip()
            m = re.match(r"\| (\w+) \| (\w+) \| .+ \| .+ \|", line)
            if m and m.group(1) in RUN_AXIS:
                pairs_listed.add((m.group(1), m.group(2)))
        for key, entry in smap.items():
            for f in MAP_FIELDS:
                if not entry.get(f):
                    F(f"STATUS_MAP {key[0]} {key[1]}: field '{f}' missing")
        for r_ in RUN_AXIS:
            for c_ in CARD_AXIS:
                if (r_, c_) not in pairs_listed:
                    F(f"STATUS_MAP pair table: {r_} x {c_} missing")
        # 2026-11-11: every status on both axes needs an entry whether or not a run or card carries
        # it now. Found by the selftest: once CC_001 left PROVISIONAL, deleting that entry went silent.
        for ax, names in (("RUN", RUN_AXIS), ("CARD", CARD_AXIS)):
            for st_ in names:
                if (ax, st_) not in smap:
                    F(f"STATUS_MAP: {ax} {st_} has no entry (required for every status on the axis)")
        if ("RUN", "PROVISIONAL") in smap:
            F("STATUS_MAP: PROVISIONAL is a card status, not a run status")
    run_status = {}
    for r in sorted(runs):
        m = re.search(r"^status\s*:\s*(\w+)", open(os.path.join(ROOT, "runs", r + ".md")).read(), re.M)
        run_status[r] = m.group(1) if m else None
        if run_status[r] not in RUN_AXIS:
            F(f"{r}.md: status {run_status[r]} outside REPORTED / COMPLETE / INCOMPLETE")
        elif ("RUN", run_status[r]) not in smap:
            F(f"{r}.md: status {run_status[r]} has no entry in ledger/STATUS_MAP.md")
    owed = {c[2] for c in needs}
    for r, st in run_status.items():
        if st == "INCOMPLETE" and r not in owed:
            F(f"{r}.md: INCOMPLETE with no row in ledger/NEEDS_TOOL.md")
        if st == "COMPLETE" and r in owed:
            F(f"{r}.md: COMPLETE while ledger/NEEDS_TOOL.md still owes it a tool")
    cards = cc.load_all(ROOT)
    readings = {}
    for n, c in cards.items():
        try:
            reading, _ = cc.read(c)
        except cc.CardError as e:
            F(f"card {e}")
            continue
        readings[reading] = readings.get(reading, 0) + 1
        if ("CARD", reading) not in smap:
            F(f"card {n}: status {reading} has no entry in ledger/STATUS_MAP.md")
        if c.get("id") != n:
            F(f"card {n}: id != file name")
        if c["reading_declared"] != reading:
            F(f"card {n}: declared {c['reading_declared']}, derived {reading}")
        rw = c["recheck_when"] if isinstance(c["recheck_when"], list) else []
        for t in rw:
            if t not in tools_:
                F(f"card {n}: recheck_when names {t}, which has no entry in ledger/toolkit/")
        if rw and all(t in tools_ and tools_[t].get("status") != "placeholder" for t in rw):
            F(f"card {n}: PROVISIONAL but every tool in recheck_when is built; the re-check is due")
        if c["branch"] != "void" and c["branch"] not in branches:
            F(f"card {n}: branch {c['branch']} missing")
        for r in c["runs"]:
            if r not in runs:
                F(f"card {n}: run {r} missing")
    # ---- expiry_condition (work order 2026-11-10 item 1): count open slots with no exit; never fail on the count
    exit_counts = {"none": 0, "incomplete": 0, "complete": 0}
    no_exit = []
    for n, c in cards.items():
        try:
            for slot, st in cc.exits(c).items():
                exit_counts[st] += 1
                if st == "none":
                    no_exit.append(f"{n}.{slot}")
        except cc.CardError as e:
            F(f"card {n}: {e}")
    ex_path = os.path.join(ROOT, "ledger", "expiry.yaml")
    if not os.path.exists(ex_path):
        F("ledger/expiry.yaml missing")
    else:
        for e in miniyaml.load(ex_path)["entries"]:
            for k in ("target", "state", "expiry_condition", "note"):
                if k not in e:
                    F(f"expiry.yaml {e.get('target')}: field {k} dropped (write void)")
            if e.get("target") not in comps and e.get("target") not in cards:
                F(f"expiry.yaml: target {e.get('target')} is neither a component nor a card")
            if e.get("state") not in ("VOID", "UNKNOWN", "PROVISIONAL"):
                F(f"expiry.yaml {e.get('target')}: state {e.get('state')} outside VOID / UNKNOWN / PROVISIONAL")
            try:
                st = cc.expiry(e)
            except cc.CardError as err:
                F(f"expiry.yaml {e.get('target')}: {err}")
                continue
            exit_counts[st] += 1
            if st == "none":
                no_exit.append(e["target"])
    ANCHOR = ["id", "status", "git_tag", "git_commit", "tag_state", "run", "seed", "params", "scope", "code", "tests", "known_errors", "open_issues"]
    FOUR = ["budgets_close_within_noise_rule", "holds_across_seeds", "holds_when_each_assumption_nudged",
            "independent_budgets_close_together"]
    anchors_ = {os.path.basename(p)[:-5]: miniyaml.load(p)
                for p in sorted(glob.glob(os.path.join(ROOT, "ledger", "anchors", "*.yaml")))}
    for n, a in anchors_.items():
        for k in ANCHOR:
            if k not in a:
                F(f"anchor {n}: field {k} dropped (write void)")
        if a.get("status") not in ("candidate", "anchor", "failed"):
            F(f"anchor {n}: status {a.get('status')}")
        t4 = a.get("tests", {})
        if sorted(t4) != sorted(FOUR):
            F(f"anchor {n}: tests must be exactly the four anchor tests")
        states = [t4.get(k, {}).get("state") for k in FOUR]
        if any(s not in ("PASS", "PARTIAL", "FAIL", "NOT_RUN") for s in states):
            F(f"anchor {n}: test state outside PASS / PARTIAL / FAIL / NOT_RUN")
        if a.get("status") == "anchor" and states != ["PASS"] * 4:
            F(f"anchor {n}: status anchor with tests {states}")
        if a.get("run") not in runs:
            F(f"anchor {n}: run {a.get('run')} missing")
        for c in a.get("code", []):
            path = os.path.join(HERE, c.get("path", "MISSING"))
            if not os.path.exists(path):
                F(f"anchor {n}: code {c.get('path')} not in tree")
            elif hashlib.sha256(open(path, "rb").read()).hexdigest() != c.get("sha256"):
                F(f"anchor {n}: {c['path']} no longer matches its frozen sha256")
    rm = miniyaml.load(os.path.join(ROOT, "ledger", "regime_map.yaml"))
    for fam, row in rm["cells"].items():
        if fam not in branches or sorted(row) != sorted(rm["regimes"]):
            F(f"regime_map: row {fam}")
    count = lambda d: {s: sum(1 for x in d.values() if x.get("status") == s) for s in sorted(STATUS)}
    return fails, notes, dict(components=count(comps), branches=count(branches), blocks=len(blocks), runs=len(runs), tests=len(tests),
                              tools=len(tools_), tools_placeholder=sum(1 for t in tools_.values() if t.get("status") == "placeholder"),
                              run_status={k: sum(1 for v in run_status.values() if v == k) for k in ("REPORTED", "COMPLETE", "INCOMPLETE")},
                              needs_rows=len(needs), owed_runs=owed_runs, cleared_rows=len(cleared), cards=readings, exits=exit_counts, no_exit=no_exit,
                              anchors={n: a.get("status") for n, a in anchors_.items()})


def selftest():
    """Plant one defect per rule in a copy; each must produce a FAIL naming it."""
    import shutil, tempfile
    plants = [
        ("dropped field", "ledger/components/L1_LEACHING.yaml", "scope:", "#scope:", "field scope dropped"),
        ("admitted without test", "ledger/components/L1_LEACHING.yaml", "status: candidate", "status: admitted", "vs admitted_by"),
        ("dangling dependency", "ledger/components/L1_LEACHING.yaml", "  - L0_N_BUDGET", "  - L0_NOPE", "depends_on L0_NOPE"),
        ("one-way block link", "ledger/assumption_blocks/AB_WELL_MIXED.yaml", "  - L1_UPTAKE_MM\n", "", "used_by omits L1_UPTAKE_MM"),
        ("anchor on one branch only", "ledger/branches/BR_FIRE_MEANFIELD.yaml", "drought >= 0.5", "drought >= 0.4", "anchor CA_1: copies differ"),
        ("card none_of_above against derivation", "ledger/toolkit/cards/CC_001_n_misclosure_seed_invariance.yaml",
         'none_of_above:\n    state: ruled_out', 'none_of_above:\n    state: supported', "none_of_above declared supported"),
        ("candidate promoted with tests unpassed", "ledger/anchors/ANCHOR_run9.yaml", "status: candidate", "status: anchor", "status anchor with tests"),
        ("frozen code hash drift", "ledger/anchors/ANCHOR_run9.yaml", "sha256: ebb656bb", "sha256: 0bb656bb", "no longer matches its frozen sha256"),
        ("tool with no diagnoses", "ledger/toolkit/coincidence_card.yaml", "diagnoses:", "diagnoses: []\nwas:", None),
        ("incomplete run marked complete", "runs/run_11.md", "status     : INCOMPLETE", "status     : COMPLETE", "COMPLETE while ledger/NEEDS_TOOL.md still owes"),
        ("needed tool with no toolkit entry", "ledger/NEEDS_TOOL.md", "| ablation | same shape across three families (card CC_004)", "| ablation_v2 | same shape across three families (card CC_004)", "NEEDS_TOOL: ablation_v2 has no entry"),
        ("provisional card waiting on an unknown tool", "ledger/toolkit/cards/CC_001_n_misclosure_seed_invariance.yaml",
         "recheck_when: void", "recheck_when:\n  - multi_seed_ensemble_v2", "recheck_when names multi_seed_ensemble_v2"),
        ("card kept PROVISIONAL after its tools are built", "ledger/toolkit/cards/CC_001_n_misclosure_seed_invariance.yaml",
         "recheck_when: void", "recheck_when:\n  - multi_seed_ensemble\n  - ablation", "the re-check is due"),
        ("provisional card declared resolved", "ledger/toolkit/cards/CC_001_n_misclosure_seed_invariance.yaml",
         "recheck_when: void", "recheck_when:\n  - support_match", "declared RESOLVED, derived PROVISIONAL"),
        ("cleared row whose tool's gate is not PASS", "ledger/toolkit/ablation.yaml", "  verdict: PASS", "  verdict: FAIL", "ablation / run_10 removed but the tool's gate is not PASS"),
        ("cleared row whose clearing run is not in used_in", "ledger/toolkit/ablation.yaml", "used_in:\n  - run_14\n  - run_15", "used_in:\n  - run_15", "used_in omits run_14"),
        ("row in both open and cleared tables", "ledger/NEEDS_TOOL.md", "| ablation | same shape across three families (card CC_004)", "| ablation | N misclosure near-identical across seeds (card CC_001) | run_10 | 2026-11-10 | x |\n| ablation | same shape across three families (card CC_004)", "is in both tables"),
        ("card status with no STATUS_MAP entry", "ledger/STATUS_MAP.md", "### CARD PROVISIONAL", "### CARD PROVISIONAL_X", "CARD PROVISIONAL has no entry"),
        ("run status with no STATUS_MAP entry", "ledger/STATUS_MAP.md", "### RUN REPORTED", "### RUN REPORTED_X", "status REPORTED has no entry"),
        ("STATUS_MAP entry missing a field", "ledger/STATUS_MAP.md", "- forbidden: treating PROVISIONAL as RESOLVED", "- forbiden: treating PROVISIONAL as RESOLVED", "CARD PROVISIONAL: field 'forbidden' missing"),
        ("STATUS_MAP pair row missing", "ledger/STATUS_MAP.md", "| INCOMPLETE | PROVISIONAL |", "| INCOMPLETE | PROVISIONAL_X |", "INCOMPLETE x PROVISIONAL missing"),
        ("run field dropped", "runs/run_3.md", "seed       :", "sead       :", "field seed dropped"),
        ("card slot expiry_condition dropped", "ledger/toolkit/cards/CC_002_grid_onto_ode_convergence.yaml",
         "    expiry_condition: void\n", "", "expiry_condition dropped"),
        ("bare absent state", "ledger/toolkit/cards/CC_003_nudges_that_move_nothing.yaml",
         "local_normal_form:\n    state: void", "local_normal_form:\n    state: ABSENT_AT_SENSITIVITY", "not void / supported / ruled_out"),
        ("observer regimes linked", "ledger/components/L5_OBS_STRATEGY.yaml", "depends_on: []", "depends_on:\n  - L5_OBS_REACTIVITY", "observer regimes share no currency"),
        ("built brief tool with no passing gate", "ledger/toolkit/multi_seed_ensemble.yaml", "  verdict: PASS", "  verdict: FAIL", "multi_seed_ensemble: built but its gate is not PASS"),
        ("placeholder with code and no blocked_on", "ledger/toolkit/assumption_block_trace.yaml", "blocked_on: \"real data", "blocked_on: void\nwas: \"real data", "placeholder with code"),
        ("expiry target unknown", "ledger/expiry.yaml", "target: L0_P_BUDGET", "target: L0_Q_BUDGET", "L0_Q_BUDGET is neither"),
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
    print(f"runs {summ['run_status']}  NEEDS_TOOL rows {summ['needs_rows']} open, {summ['cleared_rows']} cleared  placeholder tools {summ['tools_placeholder']}")
    print(f"toolkit {summ['tools']} tools  cards {summ['cards']}  anchors {summ['anchors']}")
    ex = summ["exits"]
    print(f"open slots by exit: no exit defined {ex['none']}  exit incomplete (sensitivity void) {ex['incomplete']}  exit complete {ex['complete']}  (counted, not failed)")
    for t in summ["owed_runs"]:
        print("  owed:", t)
    for t in summ["no_exit"]:
        print("  no exit defined:", t)
    for n in notes:
        print("note:", n)
    for f in fails:
        print("FAIL", f)
    print("FAIL" if fails else "OK", f"({len(fails)} failures)")
    sys.exit(1 if fails else 0)
