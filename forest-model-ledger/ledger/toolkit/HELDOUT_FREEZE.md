# Held-out gate: freeze record (2026-11-11)

Written and committed BEFORE any held-out set exists (chat-side follow-up to PR #258, item 1).
Thresholds are frozen at their values in commit 22a42e2. The held-out sets are written
after this commit, are not the tuning draws, and are run once. A tool that fails held-out
goes back to PROVISIONAL; it is not retuned against the held-out set.

tests/test_heldout.py re-hashes these files before it runs and refuses if any differs.

```text
file                                     sha256 at 22a42e2
ledger/toolkit/gate.py                   3c5e18880c50da0924db80b51657746bdd70e796eae4ad8b0a3a8c1e950f0be4
ledger/toolkit/multi_seed_ensemble.py    49bc40171462eb6e9e21f51b058b8dd65a1f777b2300011d05294bc4813e7a93
ledger/toolkit/ablation.py               56b65c2b8bd9f59b9e68f511e6f5120b9074f46bda59da791be7d7c383daba9b
ledger/toolkit/support_match.py          a16da4d9b9f86b631f048865144817cf1f3a362a73eb9f9fd9a0482c729a3004
ledger/toolkit/parameter_recovery.py     9951088f72457786fd9bf74cb4a7b10a72c471b5148668c44d5cf30c94b7d0b9
ledger/toolkit/residual_regression.py    0d9d8359f23b31d4a5f085f3f2370cf00d55511902b7769d4ac8dc8c79b953c5
ledger/toolkit/equation_family_swap.py   4c510b00cb398ac528d6ae844482d32dc937322f0035c02fb942824a1d5b5851
ledger/toolkit/assumption_block_trace.py 255d95ac98c5ad40588fae0e9dc1ec22baded50a0595accfe370423799b46a51
```

```text
tool                    frozen thresholds
multi_seed_ensemble     REL_TOL 0.05  K_MOVED 5.0  K_EQ 2.0  K_SPIKE 3.0
ablation                (uses multi_seed_ensemble's)
support_match           SECOND_PERSON word list as committed
parameter_recovery      DCHI2 9.0
residual_regression     N_PERM 500  ALPHA 0.01  MIN_DR2 0.10  COLLINEAR 0.95
equation_family_swap    K_HANDOFF 3.0  MIN_RUN 3
assumption_block_trace  ALPHA 0.001  MIN_STUDIES 8
```

Held-out rule: fresh generators (different distributions and shapes from the tuning
draws), harness seeds 100-104, PASS = every planted known answer right and FP 0 / TP 1
on every held-out leg. The held-out sets are written by the same session that tuned the
tools: they are new draws, not blind. Blind cases (support_match item 2) are separate.

## Amendments (each logged; the held-out result is unchanged by them)

```text
2026-11-11  ledger/toolkit/support_match.py
  was  79f28c50f42449851f3f2183b46bc577fa6fcb7b06a994534a2f32a0451c7e98   (frozen at 22a42e2; held-out ran on it)
  now  a16da4d9b9f86b631f048865144817cf1f3a362a73eb9f9fd9a0482c729a3004
  what the refusal string in the __main__ block only: "tests/test_toolkit.py" -> "forest-model-ledger/tests/test_toolkit.py".
       The repo's redirect contract (tools/run_manifest.py) reads a path in a refusal from the repo root, so the
       old string named a file that is not there: three UNPINNED mismatches in tools/known_red_check.py --suite,
       present since 357123c (this session's support_match commit), found 2026-11-11 after the held-out run.
  check the module AST outside `if __name__ == "__main__"` is identical before and after (ast.dump, every top-level
       node). No threshold, word list or function changed; tests/test_heldout.py re-run reads the same.
```
