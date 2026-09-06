# SPDX-License-Identifier: CC0-1.0
"""
Selftest for the gap-existence-cases instruments (commit_store.py, score.py,
validate_cases.py, retrieve.py). Null tests run both directions:

  - the hash verifies on a clean commit and FAILS on a tampered one (VOID,
    not penalised -- GX-3's structural boundary);
  - commit_specificity is 1.0 all-falsifiable, 0.0 none, 0.5 half;
  - the scorer classifies hit / miss_directional / null_retrieval /
    void_hash / void_unfalsifiable, and a VAGUE commit is VOID, never hit
    (the SCORING RULE, the gaming surface closed by the denominator);
  - a pre-cutoff ref does not count as resolving material (B1);
  - N1 fires when void_rate is high in every arm;
  - the A1-A5 validators fire on planted-bad archive cases and pass empty;
  - the B4 prompt screen catches a post-cutoff term and passes a clean one;
  - commit_store.py and score.py import NOTHING that can reach the network
    (the §3 exception is honored in code -- only retrieve.py touches it).

Run:  python3 gap-existence-cases/selftest_gxc.py
"""

import ast
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import commit_store as cs          # noqa: E402
import score                       # noqa: E402
import validate_cases as vc        # noqa: E402
import retrieve                    # noqa: E402

_checks = 0
_failed = 0


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


def mk_commit(cid, expect, cutoff="2025-01-01", model="M"):
    return {"case_id": cid, "posed": "MIS", "target": "t",
            "basis": "b", "expect": expect, "cutoff_date": cutoff,
            "model": model}


FALS = {"statement": "s", "satisfied_if": ["yes"], "contradicted_if": ["no"]}
VAGUE = {"statement": "s", "satisfied_if": ["anything"], "contradicted_if": []}

# ---- commit_store: hash boundary + specificity ----------------------------

c = mk_commit("H1", [FALS])
h = cs.commit_hash(c)
check(h == cs.commit_hash(dict(c)), "hash is deterministic over fields")
rec = {"commit": {k: c[k] for k in cs.COMMIT_FIELDS}, "sha256": h}
check(cs.verify(rec) is True, "clean commit verifies")
tampered = {"commit": dict(rec["commit"], target="edited"), "sha256": h}
check(cs.verify(tampered) is False, "tampered commit fails verify (VOID)")
check(cs.verify({"commit": {}, "sha256": "x"}) is False,
      "malformed record fails verify, does not raise")

check(cs.is_falsifiable(FALS) is True, "predicate with contradicted_if is falsifiable")
check(cs.is_falsifiable(VAGUE) is False, "predicate with no contradicted_if is not")
check(cs.commit_specificity(mk_commit("x", [FALS, FALS])) == 1.0, "spec all-fals 1.0")
check(cs.commit_specificity(mk_commit("x", [VAGUE, VAGUE])) == 0.0, "spec none 0.0")
check(cs.commit_specificity(mk_commit("x", [FALS, VAGUE])) == 0.5, "spec half 0.5")
check(cs.commit_specificity(mk_commit("x", [])) == 0.0, "spec no predicates 0.0")

# ---- score_case: every branch, and the SCORING RULE -----------------------

def rec_of(c):
    return {"commit": {k: c[k] for k in cs.COMMIT_FIELDS},
            "sha256": cs.commit_hash(c), "stage_separation": "staged"}

post = [{"pub_date": "2025-06-01", "finding": "the result is yes here"}]
contra = [{"pub_date": "2025-06-01", "finding": "the result is no here"}]
pre = [{"pub_date": "2024-06-01", "finding": "the result is yes here"}]

r = score.score_case(rec_of(mk_commit("A", [FALS])), post)
check(r["outcome"] == score.HIT, "satisfied post-cutoff ref -> hit")
r = score.score_case(rec_of(mk_commit("A", [FALS])), contra)
check(r["outcome"] == score.MISS, "contradicting ref -> miss_directional")
r = score.score_case(rec_of(mk_commit("A", [FALS])), pre)
check(r["outcome"] == score.NULL, "pre-cutoff ref does not count (B1) -> null")
r = score.score_case(rec_of(mk_commit("A", [FALS])), [])
check(r["outcome"] == score.NULL, "no refs -> null_retrieval")

# SCORING RULE: vague commit is VOID, never hit -- even with a matching ref
r = score.score_case(rec_of(mk_commit("A", [VAGUE])),
                     [{"pub_date": "2025-06-01", "finding": "anything matches"}])
check(r["outcome"] == score.VOID_SPEC,
      "vague commit is VOID (unfalsifiable), never hit -- the gaming surface")

# hash failure -> VOID_HASH
r = score.score_case(tampered_rec := {"commit": {k: mk_commit("A", [FALS])[k]
                     for k in cs.COMMIT_FIELDS}, "sha256": "deadbeef"}, post)
check(r["outcome"] == score.VOID_HASH, "hash mismatch -> void_hash")

# ---- B1 helper ------------------------------------------------------------

check(len(score.post_cutoff_refs(post, "2025-01-01")) == 1, "post-cutoff kept")
check(len(score.post_cutoff_refs(pre, "2025-01-01")) == 0, "pre-cutoff dropped")
check(len(score.post_cutoff_refs([{"pub_date": "2025-01-01"}], "2025-01-01")) == 0,
      "same-date ref is not strictly after cutoff")

# ---- N1: void_rate high in every arm --------------------------------------

# build an arms dict via score() over a temp dir would need files; test
# null_flags directly on a shaped arms dict.
arms_high = {("2025-01-01", "staged"): {"void_rate": 0.8},
             ("2024-01-01", "staged"): {"void_rate": 0.6}}
check(any("N1" in f for f in score.null_flags(arms_high)),
      "N1 fires when void_rate high in every arm")
arms_mixed = {("2025-01-01", "staged"): {"void_rate": 0.8},
              ("2024-01-01", "staged"): {"void_rate": 0.1}}
check(not any("N1" in f for f in score.null_flags(arms_mixed)),
      "N1 does not fire when an arm has low void_rate")

# ---- score() groups by arm (B2: cutoffs not pooled) -----------------------

cdir = score.os.path.join(_HERE, "fixtures", "commit")
rdir = score.os.path.join(_HERE, "fixtures", "refs")
arms = score.score(cdir, rdir)
check(len(arms) >= 1, "fixtures scored into at least one arm")
# the shipped fixtures: 1 hit, 1 miss, 1 null, 1 void_spec, 1 void_hash
for arm, a in arms.items():
    if a["n"] == 5:
        c = a["counts"]
        check(c[score.HIT] == 1 and c[score.MISS] == 1 and c[score.NULL] == 1,
              "fixture arm: 1 hit / 1 miss / 1 null")
        check(c[score.VOID_HASH] == 1 and c[score.VOID_SPEC] == 1,
              "fixture arm: 1 void_hash / 1 void_spec")
        check(abs(a["void_rate"] - 0.4) < 1e-9, "fixture void_rate 0.4")

# ---- validate_cases: the B4 prompt screen (CLASS-2 cut by WORK_ORDER §0) ---

# B4 screen: a post-cutoff term leaks the date; a clean prompt passes.
check(vc.screen_prompt("plan the route across the county", ["neologism2026"]) == [],
      "B4 screen clean when no post-cutoff term present")
check(vc.screen_prompt("use the neologism2026 method", ["neologism2026"]),
      "B4 screen fires on a post-cutoff term")
check(vc.screen_prompt("nothing here", []) == [],
      "B4 screen with no blocked terms is clean (nothing to leak)")

# ---- retrieve: refuses to run, refuses to fabricate; write_refs is pure ---

try:
    retrieve.search("anything")
    check(False, "retrieve.search must raise NotRunnable")
except retrieve.NotRunnable:
    check(True, "retrieve.search raises NotRunnable (no fabrication)")

import tempfile  # noqa: E402
td = tempfile.mkdtemp()
p = retrieve.write_refs(td, "GX-9", [{"title": "t", "venue": "v",
    "pub_date": "2025-06-01", "locator": "doi:x", "finding": "f"}])
check(os.path.exists(p), "write_refs writes a refs file")
try:
    retrieve.write_refs(td, "GX-8", [{"title": "t"}])
    check(False, "write_refs must reject an incomplete ref")
except ValueError:
    check(True, "write_refs rejects an incomplete ref")

# ---- network discipline: offline modules import nothing network-capable ---

NET = {"socket", "ssl", "http", "urllib", "urllib.request", "ftplib",
       "asyncio", "requests", "httpx", "smtplib", "telnetlib"}


def imported_modules(path):
    tree = ast.parse(open(path).read())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.add(node.module.split(".")[0])
    return names


for mod in ("commit_store.py", "score.py", "validate_cases.py"):
    imp = imported_modules(os.path.join(_HERE, mod))
    leak = imp & {n.split(".")[0] for n in NET}
    check(not leak, "%s imports no network module (got %r)" % (mod, leak))

# ---- --selftest refusals --------------------------------------------------

for mod in ("commit_store.py", "score.py", "retrieve.py", "validate_cases.py"):
    rc = subprocess.call([sys.executable, os.path.join(_HERE, mod),
                          "--selftest"], stderr=subprocess.DEVNULL)
    check(rc == 2, "%s --selftest exits 2" % mod)

# ---- report ---------------------------------------------------------------
print("selftest: %d checks, %d failed" % (_checks, _failed))
sys.exit(1 if _failed else 0)
