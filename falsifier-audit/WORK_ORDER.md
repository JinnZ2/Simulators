# WORK ORDER — falsifier audit

TARGET EXECUTOR: Claude Code
LICENSE: CC0
LANGUAGE: Python 3, standard library only
CONSTRAINTS: phone-buildable, no network at run time, operates on a local
             checkout of one or more repos
DELIVERABLE: an extractor + analyser that emits a RESEARCH QUEUE

---

## 0. WHAT THIS IS AND IS NOT

```
IS NOT   a linter. It does not grade falsifiers as good or bad,
         and it emits no fixes.

IS       an instrument that locates where a falsifier's SCOPE is
         implicit, and turns each such place into a research
         question.
```

The premise: a falsifier is itself a claim, and it is frame-bound. Where a
falsifier's scope is unstated, a frame is being inherited silently. Those
sites are where the corpus has more information in it than the corpus
states. The output is therefore ADDITIVE — questions the repos do not
already ask — not corrective.

Pairs with the branch record instrument: an audit hit is a candidate
forcing case, and any adjustment made downstream gets a branch entry
(rule as stated / forcing case / axis / derivation / frame note).

---

## 1. EXTRACTION

Walk a repo tree. Pull every falsifier and its attachment context.

```
INPUT     one or more local repo roots (argv), default cwd
SCAN      .md and .py; skip .git, vendor dirs, binaries
MATCH     line- and block-level falsifier markers as they actually
          appear in the corpus. DO NOT assume one format — the repos
          were written over time and the markers vary.
          FIRST TASK for the executor: scan the tree and emit an
          inventory of the marker forms actually present, before
          building the extractor around any of them.
```

Each extracted record:

```
FALSIFIER RECORD
  id            repo + path + line
  text          the falsifier as written, verbatim, unedited
  attached_to   the claim/rule it tests, verbatim, if locatable
  attach_status LOCATED | NOT-FOUND
  repo          source repo
```

`attach_status: NOT-FOUND` is a result in its own right — a falsifier with
no locatable claim is already a finding. Emit it, do not drop it.

---

## 2. ANALYSIS — four checks, each emitting a research question

Run each check independently. A falsifier may hit several. Do not
aggregate into a score.

### A1  UNFALSIFIABLE-AS-WRITTEN
```
TEST     does the falsifier state a threshold, a quantity, or a
         discrete outcome that could be observed to occur?
HIT      no units, no threshold, no observable outcome
MEANING  it cannot fail, so it is not doing the work its position
         claims. The claim it guards is currently unguarded.
EMITS    what quantity, in what units, would make this fail?
```

### A2  CLAIM-TEST DRIFT
```
TEST     do the load-bearing terms of the falsifier appear in the
         claim it is attached to?
HIT      falsifier terms absent from the claim, or vice versa
MEANING  the test may be testing something adjacent to the claim.
         Common where either side was edited without the other.
EMITS    which of the two moved, and is the claim or the test the
         thing that drifted?
NOTE     term matching will be noisy. Emit hits with the matched
         and unmatched terms shown, so a human can dismiss cheaply.
         A noisy check that is cheap to dismiss is acceptable;
         a silent one is not.
```

### A3  CROSS-REPO INCOMPATIBILITY   <- highest expected yield
```
TEST     do two or more falsifiers in different repos test the same
         axis with different thresholds, units, or directions?
HIT      same axis, incompatible cutoffs
MEANING  either the substrates genuinely differ (a scope-difference
         worth recording) or one of them is miscalibrated. Both are
         findings and the instrument does not decide which.
EMITS    what distinguishes the two contexts, and is that difference
         real or is one cutoff inherited?
GROUPING index by AXIS, not by rule or by repo. Axes recur across
         the corpus; rule wordings do not. This is what makes the
         check possible at all.
```

### A4  FIXED-REFERENCE-BODY
```
TEST     does the falsifier presuppose a fixed frame, observer,
         baseline, or reference body that is not itself declared?
HIT      an undeclared reference term
MEANING  the geocentric shape — the falsifier can PASS while testing
         the wrong thing, because the frame supplied the reference
         and the falsifier inherited it silently.
EMITS    what is the reference body here, and what happens to this
         falsifier if it moves?
NOTE     these are RESCOPE candidates, not narrow candidates.
         Narrowing a rule when the strain is in the frame looks like
         a fix, stops the complaint, and re-strains later from a
         different direction.
```

---

## 3. OUTPUT — a research queue, not a repair list

```
QUEUE ENTRY
  check          A1 | A2 | A3 | A4
  falsifier_id   repo + path + line
  text           verbatim
  question       the emitted research question
  status         OPEN   <- default and only machine-set value
```

Rules:
- Every entry is a QUESTION. Never a suggested edit, never a rewrite.
- Do not rank or score entries. Ranking imports a priority the
  instrument has no basis for.
- Emit a coverage line: falsifiers found, falsifiers analysed,
  files skipped and why. An unscanned file must not read as a clean one.
- Queue is append-stable: re-running on an unchanged tree emits the
  same ids, so entries can be closed by hand in a separate file and
  survive the next run.

---

## 4. FORM

```
falsifier_audit/
  README.md      what this is, what each check means, how to run
  inventory.py   marker-form inventory (run first, before extraction)
  extract.py     tree walk + falsifier records
  checks.py      A1-A4, each independent
  axes.py        axis grouping for A3
  queue.py       research queue emit, coverage line, stable ids
  run_all.py     inventory -> extract -> checks -> queue, to stdout
  QUEUE.md       emitted queue, human-editable, hand-closable
```

Plain text. Stdlib only. Must run on a phone against a local checkout.

---

## 5. NON-GOALS

- No fixes, no rewrites, no suggested wording. Questions only.
- No quality score, no ranking, no "confidence" number on a hit.
- Do not skip a falsifier because it looks fine. A1-A4 are structural
  checks, not judgement calls, and a clean pass is information.
- Do not infer intent behind a falsifier's wording, or why it was
  written as it was.
- STRIP ON SIGHT: any section describing or characterising the author,
  her working style, or her circumstances. No author profile, no
  working-conditions note, no acknowledgements. No exceptions.
