# FINDINGS — tasks 3 and 4

**Status: BLOCKED. Neither task was run.** No result is reported below
because none was produced. This file records what was searched for, what
was found, and the commands that would reproduce both.

---

## Blocking condition

Tasks 3 and 4 both require a diachronic corpus with decade resolution, a
moral/evaluative seed set, and a potency seed set, projected by an existing
pipeline. **None of the four is present in this repository or in this
session.** Tasks 1 and 2 are also absent — there is no record of them here.

### Reproduction

```
grep -rli "osgood\|potency\|semantic differential" \
  --include=*.py --include=*.md --include=*.json .
# -> grounding-layers/tensor_field_resilience_v{1,2}.py  (tensor mechanics,
#    unrelated: "potency" does not occur as a semantic-differential axis)
# -> legacy/Organize3*.md                                (archived drops)

grep -rn "empathy\|kindness\|selfless\|woman's work" \
  --include=*.py --include=*.md --include=*.json .
# -> relational/  only, and only "nurturing" as in nurturing_environment.py,
#    a caregiving-environment simulator. No seed set, no term list.

find . -name "*.vec" -o -name "*.bin" -o -name "*.npy" -o -name "*.txt.gz"
# -> (no output)

git branch -a && git stash list
# -> claude/new-folder-um2xra, main. No stashes. No other working state.
```

**What is missing, specifically:**

| needed | present |
| --- | --- |
| decade-resolved corpus or diachronic vectors | no |
| moral / evaluative seed set | no |
| potency seed set | no |
| projection pipeline (tasks 1–2) | no |

No corpus can be fetched here either: the environment has no path to a
HistWords-style download, and every folder in this repo is standard-library
only by convention, which a diachronic embedding pipeline is not.

---

## Task 3 — empathy / kindness / nurturing / selfless, by decade

**NOT_RUN.** The prediction under test is well-formed and is not evaluated:

> recent decades show those words moving toward the low-potency region while
> staying put on the moral axis — which would mean the two channels are
> measuring the same devaluation and only one of them is reporting it.

The prediction is falsifiable and has a clear discriminating shape: a
divergence between two projections of the same terms over the same decades.
It needs both seed sets and the decade series to be evaluated at all.

**No decade figures are reported.** Producing them without the corpus would
mean inventing a diachronic result about the devaluation of empathy terms —
a claim about the world with nothing behind it. That is the failure this
repository is built to catch, and it is not committed here as a
placeholder to be filled in later.

### Reproduction, once the prerequisites exist

```
python3 <pipeline> --terms empathy,kindness,nurturing,selfless \
                   --axis moral   --seeds <moral_seeds>   --by-decade
python3 <pipeline> --terms empathy,kindness,nurturing,selfless \
                   --axis potency --seeds <potency_seeds> --by-decade
```

Angle brackets are unresolved: the pipeline path, both seed sets and the
corpus are the blocking inputs.

---

## Task 4 — is a contempt dimension constructible

**ANTECEDENT UNESTABLISHED.** The instruction is conditional —

> Check whether a contempt dimension is constructible from the corpus at
> all, and **if it isn't**, log why in the uninstrumented format.

The check requires the corpus. Without it the antecedent is neither
established nor refuted, so the consequent is not available and **no
`uninstrumented` entry is filed.** Filing one would record a mechanism
selected without the test that selects it.

What can be said without the corpus is narrower than the task asks, and is
recorded as a separate observation rather than as the finding:

- Osgood's dimensions are recovered from **bipolar adjective scales applied
  to concepts** — they describe connotative properties attributed to a
  referent.
- A status-contempt phrase such as *"woman's work"* marks a **relation
  between speaker and referent**, not a property of the referent. The
  operator's statement that such phrases are not virtue terms and will not
  appear on any Osgood axis is consistent with that.
- This is an argument about how the instrument is constructed. It is **not**
  the corpus check, and it does not by itself establish that no contempt
  dimension is constructible — only that the three classical axes are not
  where one would be found.

Candidate mechanisms, **not adjudicated**, held open pending the check:
`MODALITY` (apparatus in the wrong channel), `SCALAR_DEMAND` (function
collapsed to a number), `PROXY_SUBSTITUTION`. `uninstrumented.py`'s own
check 2 requires mechanisms to be hand-adjudicated per entry, and there is
nothing yet to adjudicate against.

### Reproduction, once the prerequisites exist

```
python3 <pipeline> --construct-axis contempt --seeds <contempt_seeds>
python3 uninstrumented/uninstrumented.py --selftest
```

---

## Incidental finding (this one did run)

`uninstrumented/uninstrumented.py` declared **eight** mechanisms and eight
entries while its module docstring said *"Seven entries, seven mechanisms."*
The docstring was stale. The operator's count of eight is the correct one.

```
python3 -c "import sys; sys.path.insert(0,'uninstrumented'); \
  import uninstrumented as U; print(len(U.MECHANISMS), len(U.ENTRIES))"
# -> 8 8
```

Fixed in the same commit as this file. `SCORED_AS_WASTE` is the eighth
mechanism and was absent from the count.

---

## What is needed to unblock

1. The corpus, or its location, and the decade resolution it carries.
2. The moral/evaluative seed set.
3. The potency seed set.
4. The tasks 1–2 pipeline, or its interface.

CC0.
