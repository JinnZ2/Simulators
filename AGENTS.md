# AGENTS.md — read this before surveying this repository

License: CC0.

If you are an AI agent, a reviewer, or anyone about to describe this repository:
**this tree is executable, and reading it is not the same measurement as running it.**

A survey of this repository that does not run it measures the repository AS DOCUMENTED.
That is a legitimate result, but it must be labelled as such, because the checks below
find drift that no amount of careful reading can find.

---

## 1. RUN THIS FIRST

```
python3 tools/run_manifest.py            # enumerate every entry point, no execution
python3 tools/known_answer.py            # the calibration gate. EXPECT 2 RED. See §3.
python3 -m unittest discover tests       # ~105 tests
python3 gate-check/gate_check.py         # artifact retrievability over the tree
python3 self-scan/census.py              # whole-tree runner, independent implementation
```

`run_manifest.py` is a lister, not a runner. It emits `run-manifest.jsonl`, one record
per entry point, so you can execute the surface without discovering it by guesswork.
Run it first even if you intend to run nothing else: the manifest alone tells you what
you are choosing not to measure.

---

## 2. THE HOUSE RULE ON FAILURE

**A failing self-test in this repository is a RESULT, not an embarrassment.**

Report failures verbatim. Do not soften them into a severity rating, do not omit them
to be polite, and do not treat a red row as a reason to lower your assessment of the
folder. A test layer that never fails is a test layer nobody has checked.

Corollary: do not silently fix a failure you find. Record it, then fix it in a separate
change, so the failure and the repair are both in the record.

---

## 3. EXPECTED RED — do not report these as new findings

Two metrics in `tools/known_answer.py` are **pinned red by design**. They are calibration
anchors: a registry seeded only with metrics that pass is a registry nobody has tested.

```
null-harness          verdict-string collision      PINNED RED
nonidentity-census    marginal-majority bug         PINNED RED
```

A run reporting 24/24 registered metrics complete, 84 case verdicts PASS and 2 FAIL is
the **gate holding**, not the gate failing.

For currently-known drifts that are real but already recorded, see `KNOWN_RED.md`. Check
your failure set against that file before writing anything up. Failures already listed
there are confirmations; failures not listed there are new and are the interesting ones.

---

## 4. ENTRY-POINT REDIRECTS — exit 2 is not a failure

Some scripts deliberately refuse to run and name their folder's real entry point
instead:

```
$ python3 <folder>/some_module.py --selftest
has no selftest; run selftest_csp.py
$ echo $?
2
```

**Exit 2 with a redirect message means: you called the wrong door.** Follow the redirect
and run the named script. A naive sweep counts these as failures on first pass; they are
not. `run_manifest.py` marks them `redirect` so this does not happen twice.

---

## 5. EXIT-CODE CONTRACT

Read `EXIT_CONTRACT.md` before interpreting any exit code. Summary:

```
0   checks ran, all passed
1   checks ran, at least one FAILED          <- a result
2   wrong entry point, redirect emitted      <- not a result
3   could not run (missing input, bad env)   <- NOT a verdict
```

A nonzero exit with no verdict in the output is `NONZERO_EXIT_NO_VERDICT` and must not
be filed as a failure. It means the instrument did not report. That is a third state,
and collapsing it into pass or fail destroys information.

---

## 6. IF YOU ARE WRITING A REVIEW

State explicitly which of these you did:

```
[ ] surveyed the tree (documented)
[ ] ran the manifest (surface enumerated)
[ ] ran the checks (as-run)
[ ] executed CLAIM_TABLE falsifiers as stated (as-falsified)
```

The fourth is the one nobody has done yet. It is the open measurement.

Also state your verification method for external citations. Fetching a source and
reading a search snippet about a source are different methods with different error
rates, and a report that does not distinguish them is claiming a status it has not
earned.

---

## 7. WHAT THIS REPO IS

Instruments for epistemic hygiene: claim tables with falsifiers, gap registers, work
orders, and simulators. Stdlib-only, no network, no build step. Every claim is meant to
carry the conditions under which it would be wrong.

The format exists so that a claim can be knocked out. If you knock one out, that is the
format working. Say so plainly.
