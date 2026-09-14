# EXIT_CONTRACT.md — what an exit code means in this tree

License: CC0.

Two independent runners swept this tree and disagreed on two classifications. The
disagreement was not about the code's behaviour. It was about what a nonzero exit with
no verdict means. This file fixes that, because until it is fixed, every automated
sweep produces numbers that cannot be compared to any other sweep's.

---

## 1. THE CONTRACT

```
EXIT  MEANING                              IS IT A VERDICT?
0     checks ran; all passed               YES — pass
1     checks ran; at least one FAILED      YES — fail. This is a RESULT.
2     wrong entry point; redirect emitted   NO  — you called the wrong door
3     could not run                         NO  — missing input, bad env, crash
```

Any other nonzero code is undefined and must be filed as state 3.

**A verdict is a statement in the output. An exit code is a statement to the caller.
They must agree.** Three tools in this tree currently violate that (see KNOWN_RED §3),
and the violation is invisible to a human reading the output and fatal to a runner
reading the status.

---

## 2. THE THIRD STATE IS NOT OPTIONAL

```
NONZERO_EXIT_NO_VERDICT
```

An instrument that exits nonzero and prints no verdict did not report. It did not pass
and it did not fail.

Collapsing this into either bucket destroys information:

```
filed as PASS   a broken instrument is counted as working
filed as FAIL   a working instrument is counted as broken, and the real failures
                are buried in noise
```

The census currently carries 110 rows in this state. That is not 110 failures. It is
110 instruments whose status is unknown, which is a different and more actionable
finding.

RULE: any sweep reporting pass/fail totals must also report the no-verdict count. A
report of "79 pass, 5 fail" with no third number is incomplete.

---

## 3. REQUIRED OUTPUT SHAPE

Every runnable entry point should end with a line a runner can parse without heuristics:

```
VERDICT: PASS   checks=33 failed=0
VERDICT: FAIL   checks=33 failed=1
VERDICT: SKIP   reason=<short reason>
```

Then exit with the matching code. The verdict line is the authority; the exit code
mirrors it.

Redirect stubs emit instead:

```
REDIRECT: run selftest_csp.py
```
and exit 2. A redirect is not a skip: a skip means the check was declined, a redirect
means the caller used the wrong path and the check is still available.

---

## 4. MINIMAL REPAIRS, ORDERED BY LEVERAGE

```
R-1  Fix the three exit-code/verdict mismatches.
     failure-mode-register, internal-reference-boundary, tools/sourced.py
     Each one silently corrupts every future sweep, including sweeps by people who
     will never read this file. Highest leverage in the repository.

R-2  Add the VERDICT line to every entry point that lacks one.
     Mechanical. Converts 110 unknown rows into characterised ones, or proves they
     genuinely cannot report, which is also a result.

R-3  Repair D-4 (columbia-chain-cascade/selftest_kill.py).
     One filename. The test references UNDERGRADUATE_RESEARCH_GAPS.md; the folder
     supersedes to _V2. Unambiguously the test's defect, so the repair carries no
     judgement call. Do it first among the drifts to demonstrate the repair-and-record
     cycle on the easy case.

R-4  Resolve D-1, D-2, D-5 — but determine direction before editing.
     Each is "test expects artifact, artifact absent." Restoring the artifact and
     relaxing the test produce the same green and mean opposite things. Record which
     you concluded and why, in KNOWN_RED, before changing either side.

R-5  D-3 (evaluation-frame masking) last, and separately.
     It is the only behavioural failure in the set. Treat it as an instrument result,
     not a maintenance task: something fires unmasked that the design says should not,
     and the answer may be that the design statement is wrong.
```

---

## 5. WHY THIS FILE EXISTS RATHER THAN A CONVENTION IN SOMEONE'S HEAD

A format rule stated in prose does not propagate to material written after the rule.
That has been measured in this line of work, at n=1: a formatting rule was stated, and
the next table written carried the defect the rule prohibits.

So this contract needs a mechanical check, not a paragraph. The check is:

```
for each entry point in run-manifest.jsonl:
    run it
    parse the VERDICT line
    compare to the exit code
    mismatch -> report
```

That check does not exist yet. Until it does, this file is a rule with no enforcement,
and should be read as a statement of intent rather than a property of the tree.
