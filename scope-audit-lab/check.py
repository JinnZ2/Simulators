#!/usr/bin/env python3
"""Checks on the delivered Scope Audit Lab drop (Kimi / OKComputer).

Reads the landed files. Never edits them. Recomputes what the two
continuation reports say about their own code and demo outputs, and
prints the search-depth status of the external anchors.

    python3 check.py              render the report
    python3 check.py --selftest   run the checks

What it does NOT do: run the lab, verify any external claim, or judge the
ETH result. External statuses below are carried from search-result text
(see SOURCES.md), not from primary documents.
"""
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE / "CONTINUATION_REPORT_V1.md"
V2 = HERE / "CONTINUATION_REPORT_V2.md"
LAB3 = HERE / "lab_0_3"
LAB2 = HERE / "lab_0_2"

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def delivered_files():
    out = [V1, V2]
    for root in (LAB2, LAB3):
        out += sorted(p for p in root.rglob("*") if p.is_file())
    return out


def manifest_digest():
    """One digest over every delivered file, path + bytes."""
    h = hashlib.sha256()
    for p in delivered_files():
        h.update(str(p.relative_to(HERE)).encode())
        h.update(p.read_bytes())
    return h.hexdigest()


# Digest over every delivered file (path + bytes) as landed. A change means a
# delivered file was edited, which the repo convention forbids.
MANIFEST_SHA256 = "1a1de4c7933a709a4cdc372e313d9415919aa42a3397c9d6649f25424082949e"


# ---------------------------------------------------------------- 1. revision

def revision():
    a = V1.read_text(encoding="utf-8").splitlines()
    b = V2.read_text(encoding="utf-8").splitlines()
    ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
           if o[0] != "equal"]
    kinds = {}
    for o in ops:
        kinds[o[0]] = kinds.get(o[0], 0) + 1
    return len(a), len(b), kinds


# ---------------------------------------------------------------- 2. test counts

def test_count(lab):
    return sum(len(re.findall(r"^\s+def test_", p.read_text(encoding="utf-8"), re.M))
               for p in (lab / "tests").glob("test_*.py"))


def stated_counts():
    t = V2.read_text(encoding="utf-8")
    v02 = re.search(r"\((\d+) total, all passing\)", t)
    v03 = re.search(r"at (\d+) tests passing", t)
    return int(v02.group(1)), int(v03.group(1))


# ---------------------------------------------------------------- 3. demo stream

def demo_records():
    return [json.loads(l) for l in
            (LAB3 / "experiments_demo.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]


def payload(r):
    return r.get("payload", r)


IDS = ("record_id", "created_utc", "linked_record_ids", "subject_record_ids")


def strip_ids(x):
    if isinstance(x, dict):
        return {k: strip_ids(v) for k, v in x.items() if k not in IDS}
    if isinstance(x, list):
        return [strip_ids(v) for v in x]
    return x


def stream_runs():
    """How many copies of the five-record demo the stream holds, and whether
    the copies are identical once record ids and timestamps are removed."""
    r = demo_records()
    n = len(r) // 5
    copies = [[strip_ids(payload(x)) for x in r[i * 5:(i + 1) * 5]] for i in range(n)]
    return len(r), n, all(c == copies[0] for c in copies)


# ---------------------------------------------------------------- 4. null baseline

def null_summary():
    p = payload(demo_records()[0])
    s = p["recorded_summary"]
    g = p["generator"]["parameters"]
    th = p["scan_config"]["threshold"]
    n = s["cases_per_replication"]
    w = g["high"] - g["low"]
    # P(|U1 - U2| > th) for two independent uniforms on an interval of width w
    analytic = (n - 1) * (1 - th / w) ** 2
    return s["min_candidate_regions"], s["max_candidate_regions"], s["mean_candidate_regions"], analytic


# ---------------------------------------------------------------- 5. planted steps

def planted_outputs():
    src = (LAB3 / "scope_audit_lab" / "__main__.py").read_text(encoding="utf-8")
    m = re.search(r"enumerate\(\[([0-9., ]+)\]\)", src)
    return [float(x) for x in m.group(1).split(",")]


def big_crossings(outputs, at_least=20.0):
    return [(f"step_{i}", f"step_{i+1}", outputs[i + 1] - outputs[i])
            for i in range(len(outputs) - 1) if abs(outputs[i + 1] - outputs[i]) >= at_least]


def permutation_counts():
    p = payload(demo_records()[2])
    return {tuple(a["between_pair_unordered"]): a["appearance_count"] for a in p["region_appearances"]}


# ---------------------------------------------------------------- 6. v0.2 demo

def transition_demo():
    r = [json.loads(l) for l in
         (LAB3 / "transitions_demo.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    s = payload(r[0])
    regions = [(tuple(c["between"]), c["metric_value"]) for c in s["candidate_regions"]]
    cases = s["cases"]
    zero_left = [i for i in range(len(cases) - 1) if cases[i]["output_value"] == 0.0]
    right_missing = [i for i in zero_left if cases[i + 1]["output_value"] is None]
    return regions, zero_left, right_missing


# ---------------------------------------------------------------- 7. ESA citation

def esa_row():
    for line in V2.read_text(encoding="utf-8").splitlines():
        if line.startswith("| 2026 ESA rule"):
            m = re.search(r"federalregister\.gov/documents/(\d{4}/\d\d/\d\d)/([0-9-]+)/", line)
            return line, m.group(1), m.group(2)
    return None, None, None


# ---------------------------------------------------------------- 8. external anchors

# Search-result depth, 2026-10-27. Carried; no primary document read.
ANCHORS = [
    ("OpenAI ETH announcement, Oct 26 2026, Impagliazzo/Paturi/Williams review", "FOUND_IN_SEARCH"),
    ("Navier-Stokes lost in translation, arXiv 2610.08144 (Bastounis, Circelli, Hansen)", "FOUND_IN_SEARCH"),
    ("Palomar registry opened 2026-08-18, Tao among maintainers", "FOUND_IN_SEARCH"),
    ("IEA data-centre demand +17% in 2025, ~950 TWh by 2030", "FOUND_IN_SEARCH"),
    ("IEA 485 TWh 2025 baseline", "SECONDARY_ONLY"),
    ("Anthropic-attributed #3-SAT preprint, hexagonmath 2610.00577", "NOT_LOCATED"),
    ("ESA harm rescission final rule, July 14 2026", "FOUND_IN_SEARCH (FR 2026-14195; see habitat-lag-dependency/)"),
]


# ---------------------------------------------------------------- render

def render():
    out = ["scope-audit-lab / check.py", "=" * 64]
    out.append(f"delivered-file digest {manifest_digest()[:16]}...  pinned: {manifest_digest() == MANIFEST_SHA256}")
    la, lb, kinds = revision()
    out += ["", "1. REPORT V1 -> V2 (Deep Research Continuation -> Creative Scope Audit)",
            f"   lines {la} -> {lb}; non-equal blocks {kinds}",
            "   -> a revision, not a pure insertion: v1 lines are rewritten, not only added to"]
    s02, s03 = stated_counts()
    out += ["", "2. TEST COUNTS (static count of def test_*)",
            f"   lab 0.2: counted {test_count(LAB2)}, report states {s02}",
            f"   lab 0.3: counted {test_count(LAB3)}, report states {s03}"]
    n, runs, same = stream_runs()
    out += ["", "3. experiments_demo.jsonl",
            f"   {n} records = {runs} copies of the five-record demo; copies identical (ids removed): {same}",
            "   -> the report describes a five-record stream; the shipped file is the demo appended twice"]
    lo, hi, mean, an = null_summary()
    out += ["", "4. NULL BASELINE",
            f"   recorded per-replication regions: min {lo}, max {hi}, mean {mean}",
            f"   analytic (n-1)(1 - threshold/width)^2 = {an:.2f}",
            "   -> the 'copious' null count is fixed by uniform[0,100] against threshold 10;",
            "      it measures the generator's width/threshold ratio, computable without a run"]
    outs = planted_outputs()
    bc = big_crossings(outs)
    pc = permutation_counts()
    out += ["", "5. 'PLANTED STEPS' IN THE v0.3 DEMO",
            f"   series {outs}",
            "   crossings with |delta| >= 20: " + ", ".join(f"{a}-{b} {d:+.0f}" for a, b, d in bc),
            "   permutation appearances of those pairs: "
            + ", ".join(f"{a}-{b} {pc.get((a, b), 0)}/26" for a, b, _ in bc),
            "   report, sweep paragraph: two planted steps of ~26 and ~51 (pairs 2-3, 6-7)",
            "   report, permutation paragraph: planted pairs appear 9 and 8 times (pairs 2-3, 4-5)",
            "   -> the two paragraphs name different pairs as 'planted'; the ~51 step appears 4/26"]
    regions, zl, rm = transition_demo()
    out += ["", "6. v0.2 TRANSITION DEMO",
            "   regions: " + ", ".join(f"{a}->{b} {v:g}" for (a, b), v in regions) + "  (report: 27, 61)",
            f"   pairs with a zero left output: {len(zl)}; of those, right side missing: {len(rm)}",
            "   -> the demo's labelled zero-output case is never a computed pair; the tests cover it"]
    line, date, doc = esa_row()
    out += ["", "7. ESA ROW OF THE FACT-CHECK TABLE",
            "   row says: final rule published July 14, 2026",
            f"   Federal Register link it cites: {date}  document {doc}",
            "   -> the cited document is dated April 2025 (the proposed rule), not the July 2026 final rule"]
    out += ["", "8. EXTERNAL ANCHORS (search-result depth, carried)"]
    for name, st in ANCHORS:
        out.append(f"   {st:<16} {name}")
    out += ["", "Nothing above is a verdict on ETH, on any lab, or on the lab's design."]
    return "\n".join(out)


def selftest():
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))

    ok("delivered files unedited (digest pinned)", manifest_digest() == MANIFEST_SHA256)
    la, lb, kinds = revision()
    ok("v2 is longer than v1", lb > la)
    ok("v2 rewrites v1 lines (replace blocks present)", kinds.get("replace", 0) > 0)
    s02, s03 = stated_counts()
    ok("lab 0.2 static test count == stated 31", test_count(LAB2) == s02 == 31)
    ok("lab 0.3 static test count == stated 56", test_count(LAB3) == s03 == 56)
    n, runs, same = stream_runs()
    ok("demo stream holds two identical copies of five records", n == 10 and runs == 2 and same)
    lo, hi, mean, an = null_summary()
    ok("null range 7..11 as reported", (lo, hi) == (7, 11))
    ok("null mean within 0.1 of analytic 8.91", abs(mean - an) < 0.1 and abs(an - 8.91) < 0.01)
    bc = big_crossings(planted_outputs())
    ok("demo series has three crossings >= 20, not two", len(bc) == 3)
    pc = permutation_counts()
    ok("pairs appearing 9 and 8 times are 2-3 and 4-5",
       pc[("step_2", "step_3")] == 9 and pc[("step_4", "step_5")] == 8)
    ok("the ~51 step (6-7) appears 4 of 26", pc[("step_6", "step_7")] == 4)
    regions, zl, rm = transition_demo()
    ok("v0.2 demo deltas are 27 and 61", [v for _, v in regions] == [27.0, 61.0])
    ok("only zero-left pair has a missing right side", len(zl) == 1 and zl == rm)
    line, date, doc = esa_row()
    ok("ESA row cites a 2025 FR document", date is not None and date.startswith("2025"))
    ok("anchor list keeps NOT_LOCATED apart from FOUND",
       {st.split()[0] for _, st in ANCHORS} >= {"NOT_LOCATED", "FOUND_IN_SEARCH"})
    failed = [n for n, c in checks if not c]
    for n_, c in checks:
        print(("PASS " if c else "FAIL ") + n_)
    print(f"checks: {len(checks)}   failed: {len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    print(render())
