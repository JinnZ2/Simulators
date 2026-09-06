# WORK ORDER — GAP EXISTENCE CASES (external-key classes)

CC0. Public domain. No attribution requested or accepted.

Companion to `WORKORDER_frame_location_benchmark.md`. That file's §9 open
node is the weak joint: constructed cases have no external check on the
correct reframe. These two classes supply one.

Build constraints: Python 3 stdlib only. No dependencies. Single folder.
Phone-buildable. NETWORK EXCEPTION, stated rather than hidden: CLASS-3
requires a retrieval stage, so the retrieval runner touches the network.
The commit store and the scorer do not, and must run with the network
unavailable. See §3.

---

## 0. SCOPE DECISION (2026-09-05)

An earlier draft carried a second class built on dated entries from a
private archive. CUT. Stated reason: this instrument is for other people
and for AI self-assessment; a priority claim about who named a gap first
is not what it is measuring, and is not wanted in it.

What remains is self-contained. Any model can run it on itself with no
archive, no third party, and no dating of anyone's prior work.

The cut also removes the instrument's two weakest joints: the
independence problem (§8) and the archive-consolidation blocker.

## 1. THE MOVE

Replace an authored answer key with a DATED EXTERNAL RECORD. Neither the
case author nor the model under test writes the key.

```
POST-CUTOFF   gap reasoned by the model cold; the resolving
              material published AFTER its training cutoff;
              model then retrieves and scores itself
```

The force is ORDERING. The model's training cutoff is a hard date it
cannot move, and it is the only date the instrument needs.

---

## 3. CLASS-3 — POST-CUTOFF SELF-SCORING

The model's training cutoff is a hard date it cannot move. That date
does the work `entry_date` does in CLASS-2, with no archive required.

### 3.1 Staging — LOAD-BEARING

```
STAGE 1  COMMIT     no network. no retrieval tool present.
                    model receives prompt, emits:
                      POSED:   WELL | MIS
                      TARGET:  <term>
                      BASIS:   <why, <=5 lines>
                      EXPECT:  <what a resolving finding would
                                have to say, stated as a
                                predicate that can fail>
                    written to commit/<case_id>.json, hashed.
                    PROCESS EXITS.

STAGE 2  RETRIEVE   separate invocation. network available.
                    commit file NOT in context.
                    model searches, returns refs + pub_dates.

STAGE 3  SCORE      no network. no model. score.py reads the
                    hashed commit and the stage-2 refs.
```

```
WHY THE SEPARATION IS STRUCTURAL, NOT PROCEDURAL
  A model cannot distinguish reasoned-it from read-it once
  retrieval has run. Self-scoring in a single pass returns a high
  score in good faith. The stages defend against self-deception,
  not against intent — so the enforcement must be in the process
  boundary, not in an instruction.
  Hash the commit. If the hash does not verify at STAGE 3, the case
  is VOID, not penalised.
```

### 3.2 Case admission

```
B1  resolving material pub_date > model cutoff_date, verified at
    STAGE 2 from the record, not from the model's assertion.
B2  cutoff_date recorded per model, per run, in the run log. Two
    models with different cutoffs are DIFFERENT ARMS, never pooled.
B3  EXPECT must be falsifiable. If no retrievable finding could
    contradict it, the case scores VOID and is excluded from the
    denominator.
B4  Prompts must not contain post-cutoff terminology. A term the
    model has never seen leaks the date. Screen every prompt.
```

### 3.3 Scoring

```
commit_specificity   fraction of EXPECT predicates that are
                     falsifiable                      <- gate, §6 N3
hit                  EXPECT satisfied by retrieved material
miss_directional     retrieved material contradicts EXPECT
                     -> reasoned gap was real, located wrong
null_retrieval       nothing retrievable either way
void_rate            hash failures + unfalsifiable EXPECT
```

```
SCORING RULE
  hit counts ONLY against a falsifiable EXPECT.
  A vague commit that matches anything is scored VOID, never hit.
  This is the single largest gaming surface and it is closed by
  the denominator, not by trust.
```

---

## 4. WHAT THIS MEASURES

Not knowledge. The resolving material is by construction absent from the
model's corpus. What is scored is whether the model can locate a fault in
a posed problem and state, in advance, what would resolve it — then be
held to that statement by a record it did not author.

---

## 5. CLAIM TABLE

```
GX-1  A gap named before its documentation exists is evidence the
      gap was real, independent of who named it.
      REFUTED IF: match rates for dated entries do not exceed match
      rates for entries dated AFTER the resolving publication
      (run the reversed-order control — it is cheap).

GX-2  Post-cutoff self-scoring is a valid substitute for an
      authored key.
      REFUTED IF: hit rate correlates with retrieval-stage search
      quality rather than with commit content.

GX-3  Staged commit prevents post-hoc fit.
      REFUTED IF: single-pass runs and staged runs return the same
      hit rate. Then the separation is buying nothing and can be
      dropped.

GX-4  REPLICATED is as informative as CORRECTED.
      REFUTED IF: REPLICATED cases are indistinguishable from
      ADJACENT under blind re-coding by a second reader.

GX-5  Gap-location is separable from general capability.
      REFUTED IF: commit_specificity and hit track model rank with
      no residual — same refutation as FL-1 in the companion file.
```

---

## 6. NULLS

```
N1  If void_rate is high across all models, the instrument is
    measuring commit discipline, not gap-location. Report as an
    instrument property.

N2  ADJACENT and NULL outcomes are results. A case set reporting
    only CORRECTED and REPLICATED has been filtered, and the
    filtering is the finding. Publish the full disposition table
    or publish nothing.

N3  If commit_specificity is low, later numbers are void — a
    non-falsifiable EXPECT cannot be hit or missed. Gate the run
    on this before computing anything else.

N4  If CLASS-2 admits fewer than ~10 cases after A1-A5, say so and
    report CLASS-3 alone. Do not relax the admission rules to
    reach a sample size.

N5  Every score carries its cutoff_date and its stage-separation
    status in the same line. Unlabelled scores from this
    instrument are void — same rule as the harness labels in the
    companion file.
```

```
SAMPLING ABSENCE, in the body and not as a caveat:
  CLASS-2 draws from one archive. It shows what one record
  contains, not the base rate of gap-naming anywhere. CLASS-3
  draws from what is retrievable in the languages searched.
  Neither supports a frequency claim.
```

```
OUT OF SCOPE — NO EXCEPTIONS
  No section characterizing the archive's author, working style,
  or biography. Entries carry the dated text and the target.
  entry_platform is a provenance field, not a description of a
  person.
```

---

## 7. BUILD ORDER

```
1  score.py + commit hashing, hand-made fixtures      offline
2  CLASS-3, 10 cases, one model, staged               is GX-3 alive
3  single-pass control on the same 10                 GX-3
4  expand CLASS-3 across >=2 cutoff dates             GX-2, GX-5
5  archive consolidation with timestamps              BLOCKER
6  CLASS-2 admission pass under A1-A5
7  reversed-order control                             GX-1
```

CLASS-3 does not block on the archive. Build it first.

---

## 8. OPEN NODE

A4 independence cannot be fully established for anonymously posted
entries — public posting means downstream carriage is possible and
untraceable. This weakens CLASS-2 CORRECTED cases specifically: a later
paper repairing a fault may have encountered the entry.

REPLICATED cases are not weakened by this, which is a reason to weight
them. Not resolved here; state the exposure per case in `independence`
and report CORRECTED counts with and without entries that were publicly
posted before the resolving publication.
