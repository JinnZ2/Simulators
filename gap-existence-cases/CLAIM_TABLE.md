# CLAIM_TABLE — gap-existence-cases

`WORK_ORDER.md` is a delivered work order (verbatim, CC0), companion to
`frame-location-benchmark/`. It supplies the external key that folder's §9
open node lacked: two classes that replace an authored answer key with a
**dated external record** — CLASS-2 (a gap named in a dated archive entry,
resolved by later independent documentation) and CLASS-3 (a gap reasoned by
the model cold, resolved by material published after its training cutoff, the
model then retrieving and scoring itself). The force in both is **ordering**.

The work order's own claims are **GX-1..GX-5**, each carrying a REFUTED-IF;
they are about the benchmark's findings and **require real archive/model
runs** — CLASS-3 needs a model (STAGE 1 commit) and network retrieval
(STAGE 2), CLASS-2 needs the archive consolidation with timestamps — so they
are carried UNVERIFIED, and the runs are the operator's step.

These `GXC_0NN` claims are a different set — properties of the **built
instruments** (the hash-void commit boundary, the offline scorer, the
falsifiability gate, the admission validators), each checked on constructed
fixtures with a known answer. Nothing here is a benchmark result: no model
committed, no retrieval ran; the shipped fixtures are CONSTRUCTED.

## REFUTATION_PROTOCOL

A refuted claim is updated forward with a new id; the old id keeps its text
and gains an UPDATE paragraph. `WORK_ORDER.md` is delivered verbatim and is
not edited. `commit_specificity` is registered in `tools/known_answer.py` and
its cases are not loosened. The scorer, the hash boundary, and the validators
are null-tested in both directions so no verdict is constant. Nothing is
promoted from carried to verified without real runs.

| id | claim | status | evidence | falsifier |
|---|---|---|---|---|
| GXC_001 | **The commit hash is the structural boundary (GX-3): a commit that does not verify at STAGE 3 is VOID, not penalised.** `commit_store.write_commit` hashes the declared fields (sha256 over a canonical serialization) at STAGE 1 and the process exits; `verify` re-hashes at STAGE 3 and returns False on any change to the declaration. The enforcement is in the process boundary, not an instruction — it defends against self-deception (a later pass rewriting EXPECT to match what was read), a limit the work order states. | SUPPORTED | a clean commit verifies; a tampered commit fails `verify`; a malformed record fails without raising; the fixture `GXC-C3-05` (tampered) scores `void_hash` | a changed committed declaration passing `verify`; a hash failure scored as a hit or a miss |
| GXC_002 | **hit counts ONLY against a falsifiable EXPECT; a vague commit is VOID, never hit (the SCORING RULE).** `commit_specificity` is the fraction of EXPECT predicates that state what would contradict them; below `SPEC_GATE` the case is `void_unfalsifiable` before any hit is computed (N3). A vague commit whose ref matches "anything" scores VOID, not hit — the largest gaming surface, closed by the denominator, not by trust. `commit_specificity` is registered in `tools/known_answer.py` (all 1.0 / none 0.0 / half 0.5). | SUPPORTED | a vague commit with a matching ref scores `void_unfalsifiable`; the three known-answer cases PASS; `is_falsifiable` requires a non-empty `contradicted_if` | a non-falsifiable EXPECT scored as a hit; `commit_specificity` counting a vague predicate as falsifiable |
| GXC_003 | **The scorer classifies every outcome and B1 is enforced: a pre-cutoff ref is not resolving material.** `score_case` returns `hit` (a post-cutoff ref satisfies EXPECT), `miss_directional` (a post-cutoff ref contradicts it — reasoned gap real, located wrong), `null_retrieval` (nothing post-cutoff either way), `void_hash`, or `void_unfalsifiable`. `post_cutoff_refs` keeps only refs with `pub_date` strictly after `cutoff_date` (B1); a same-date ref is dropped. | SUPPORTED | the five fixtures fire the five branches; a pre-cutoff ref → null; a same-date ref is not strictly after cutoff | a pre-cutoff ref counted as resolving material; a contradicting ref scored as a hit |
| GXC_004 | **Arms are grouped by (cutoff_date, stage_separation) and never pooled across cutoffs (B2), and every score carries both in the same line (N5).** `score` keys arms on the cutoff and stage; `render` prints `[cutoff=... stage=...]` on every metric line. Two models with different cutoffs are different arms. An unlabelled score from this instrument is void. | SUPPORTED | the fixture arm reads `cutoff=2025-01-01 stage=staged`; every metric line carries the label | two cutoffs pooled into one arm; a score line with no cutoff/stage label |
| GXC_005 | **The full disposition is reported, never filtered (N2), and N1 fires when void_rate is high in every arm.** `render` prints every case's outcome (hit / miss / null / void), so ADJACENT/NULL-shaped results are not discarded. `null_flags` fires N1 when `void_rate ≥ VOID_HIGH` in every arm — the instrument is then measuring commit discipline, not gap-location (an instrument property, not a model finding). | SUPPORTED | the disposition lists all five fixtures; N1 fires when both arms have high void_rate and not when one is low | a case dropped from the disposition; N1 firing when an arm has low void_rate |
| GXC_006 | **CLASS-2 admits 0 cases, honestly (N4), and the rules are not relaxed.** The archive consolidation with timestamps (build order step 5) is not reachable here (egress-blocked), and the §2.4 seed set has no entry dates established, so nothing satisfies A1 (`pub_date > entry_date` strictly). `archive_cases.jsonl` is empty; `validate_cases` reports "0 admitted, report CLASS-3 alone" rather than treating it as a failure, and `check_A1_A5` fires on planted A1/A4/A5 violations. The seed set is carried as NOT-ADMITTED candidates in `archive_candidates.md`. | SUPPORTED / carried | empty archive passes with the N4 note; a well-formed case passes A1-A5; planted pub≤entry, same-month, missing-independence, missing-coding-timestamp all fire | a case admitted with `pub_date ≤ entry_date`; the admission rules relaxed to reach a sample size |
| GXC_007 | **The §3 network exception is honored in code: the commit store and the scorer touch no network; only `retrieve.py` does, and it refuses to run or fabricate here.** `commit_store.py`, `score.py`, and `validate_cases.py` import no network-capable module (asserted by an AST scan in the selftest). `retrieve.search` raises `NotRunnable` — no reachable retrieval, no model — and NEVER fabricates a dated ref (a forged `pub_date` would forge the external key); `write_refs` is the pure writer the operator's retrieval feeds. | SUPPORTED | the AST scan finds no network import in the three offline modules; `retrieve.search` raises; `write_refs` rejects an incomplete ref | a network import in `commit_store.py`/`score.py`; `retrieve` returning a fabricated ref |
| GXC_008 | **The benchmark's own claims GX-1..GX-5 are UNVERIFIED here — they require real archive/model runs — and no author/biography content appears anywhere (§7).** GX-1 (reversed-order control) and GX-2..GX-5 need model commits, network retrieval, and the archive; `entry_platform` is a provenance field, not a description of a person, and there is no author or working-style section in any file. The build order says CLASS-3 does not block on the archive — build it first — which is what this folder does (the machinery, not the run). | carried / UNVERIFIED | GX-1..GX-5 carried in `WORK_ORDER.md`; fixtures are CONSTRUCTED; no author content in any file | GX-1..GX-5 asserted as verified without runs; an author-profile section anywhere |
