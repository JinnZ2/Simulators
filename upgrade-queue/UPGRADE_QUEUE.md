# UPGRADE QUEUE — falsifier / claim record format

Opened: 2026-09-05
Status of every entry below: NOT ADOPTED. This is a queue, not a spec.

Rules for this file:

```
- An entry may be listed with no test, no cost estimate, and no
  evidence. Unknown is a valid status and is stated as unknown.
  A parked idea with a blank test field is worth more than a
  polished one that was never written down.
- Adopting an entry that CHANGES an existing rule requires a branch
  entry (rule as stated / forcing case / axis / derivation /
  frame note). Adopting one that only ADDS a field does not.
- Nothing here is adopted by being written here. Moving an entry to
  ADOPTED requires its adopt-test to have run, or an explicit
  decision to adopt without one, recorded as such.
- FORCED entries came from an observed failure. CANDIDATE entries
  came from another registrar and have not been tested here.
  SPECULATIVE entries came from neither.
```

---

## TIER 1 — FORCED (an observed failure in hand)

### U-01  UNCERTAINTY ON THE CUT
```
source      CIPM / CMC entries carry an uncertainty budget;
            MEASURED_AS carries units and a cut and nothing else
what it     a cut with no uncertainty is false precision.
fixes       "integer count, threshold 3" reads as decisive; if the
            count carries +/-2 it decides nothing. The format
            currently cannot tell those apart, and after ADDENDUM 02
            every MEASURED cell is required to carry a cut — so the
            format now demands a number whose reliability it has no
            slot for.
form        MEASURED_AS gains: uncertainty, and its basis
            (stated / estimated / propagated / unknown)
            UNKNOWN is permitted and must be explicit.
cost        touches every MEASURED record. ~537 in Run 2 alone.
            Probably a lazy field: required going forward, blank
            and flagged on existing records rather than backfilled.
adopt-test  take 20 existing MEASURED cells. For how many does an
            uncertainty of plausible size flip the verdict?
            If near zero, this is bookkeeping. If not, it is a
            defect the format has been hiding.
status      NOT ADOPTED. Adopt-test not run.
```

### U-02  DISTINCTNESS LINK
```
source      three external systems (Kimi partially, Perplexity,
            DeepSeek) collapsed distinct transforms that shared
            wording. DeepSeek called all ten pairs in a five-record
            cluster mutual restatements. They are not.
what it     distinctness is being destroyed at READ time, not write
fixes       time. The format states each record but never states
            that two records are NOT the same record.
form        a record may carry: restates: <id>  (asserted identity)
                                distinct_from: <id> + why
            "why" is required on distinct_from. An unexplained
            distinctness claim is as weak as an unexplained merge.
cost        low. Only needed where a collapse has actually been
            observed or is expected.
adopt-test  re-run one blind sort with distinct_from present on the
            speedup cluster. Does the collapse stop? If it happens
            anyway, the fix is not in the record format.
status      NOT ADOPTED.
```

### U-03  SIGN vs MAGNITUDE CLASS ON A MISMATCH
```
source      ENG-3 — the proxy moves OPPOSITE to the truth (reports
            1.50x more speedup while taking 1.89x more wall clock).
            Every external reader filed it with magnitude errors.
what it     a magnitude error preserves ordering; a sign error does
fixes       not. Those have different consequences and different
            repairs, and the format gives a reader nothing to see
            the difference by.
form        on a SCOPE_TRANSFORM: direction, one of
              PRESERVES-ORDER / INVERTS-ORDER / UNORDERED / UNKNOWN
cost        low, one field, judgeable from breaks_at in most cases.
adopt-test  code the 13 distinct transforms. If INVERTS-ORDER has
            exactly one member, it is still worth having — that
            member is the one that keeps getting lost.
status      NOT ADOPTED.
```

### U-04  GRAIN / CUT HEIGHT ON ANY GROUPING
```
source      the nesting result — Kimi 4-5, DeepSeek 9, Perplexity 11,
            strictly nested, no cross-cutting. A kind count with no
            stated cut height is a cut presented as a fact.
what it     any grouping emitted by this ecosystem currently states
fixes       members and a definition but not the LEVEL it was cut
            at. That is the same defect the instrument catches in
            other people's work.
form        a grouping carries: cut_criterion (what makes two
            records the same at this level), and, if known,
            the coarser and finer groupings it nests inside/over.
cost        low for new groupings. The three existing ones are
            already reconstructable.
adopt-test  none needed; the nesting result is the demonstration.
            This one is closer to adopt-on-sight than the others.
status      NOT ADOPTED, but weakest objection of anything here.
```

---

## TIER 2 — CANDIDATE (from a registrar, untested here)

### U-05  WHEN-IT-FIRES
```
source      the fixture-vs-format distinction. CT.gov fires at
            submission and is enforced; a proof assistant fires
            continuously; nanopublications fire never.
what it     a claim record says what would falsify it and never
fixes       says WHEN anyone would check. A falsifier nobody
            executes and a falsifier executed on every commit are
            recorded identically.
form        fires: never / on-demand / at-review / on-commit /
                   continuous
            enforced_by: nobody / author / reviewer / a script /
                   an external body
cost        low. Mostly already implicit in whether a script exists.
adopt-test  count the distribution across one repo. If almost
            everything is "never", that is a finding about the
            ecosystem, not a defect in the field.
status      NOT ADOPTED. Untested.
```

### U-06  STATED-BEFORE-OR-AFTER
```
source      preregistration (CT.gov, OSF)
what it     whether a falsifier was written before or after the
fixes       result it judges. This is the single cheapest
            discriminator any registrar has and the format lacks
            it entirely.
form        stated_relative_to_data: before / after / unknown
            "unknown" will be the honest answer for most existing
            records and should be the default, not "before".
cost        very low going forward. Unrecoverable retroactively for
            most records — which is itself worth recording.
adopt-test  none obvious. The value is not in doubt; the question
            is only whether the field can be filled honestly.
status      NOT ADOPTED.
```

### U-07  TRACEABILITY CHAIN
```
source      CMC entries; and the ecosystem already does this
            informally — coefficients "bisection-calibrated to a
            published anchor" (tenability.py) is a one-link chain
            written in prose.
what it     how_obtained is a string. A chain would be a linked
fixes       path back to a reference, so that when an anchor moves,
            everything downstream is findable.
            The FSRI hold marker is a hand-built instance of
            exactly this, for one report.
form        how_obtained gains: anchors: [ {id, source, value} ]
            and derived records inherit the anchor list.
cost        moderate. Real value only if something actually moves.
adopt-test  when the FSRI report lands, check whether the anchor
            list would have found everything the manual marker
            search found. That is a free test on work already
            queued.
status      NOT ADOPTED. Test is scheduled by another task.
```

### U-08  MECHANICAL-CHECK FLAG
```
source      proof assistants — the check is total and machine-run
what it     distinguishes a falsifier a script can execute from one
fixes       requiring human judgement from one requiring an
            experiment nobody has run.
form        checkable_by: script / human / experiment-not-run /
                          undecidable
cost        low.
note        overlaps U-05. Possibly one field, not two — fires
            (when) and checkable_by (by what) may collapse.
            Do not merge them without checking whether a case
            exists where they differ.
status      NOT ADOPTED.
```

### U-09  PROVENANCE AS STRUCTURE
```
source      nanopublications — provenance is a first-class graph
what it     source_file is a string. Where a claim came from,
fixes       through what transformations, is not represented.
cost        high, and this is the entry most likely to turn into a
            format rewrite. Lowest priority of Tier 2 for that
            reason.
open        does anything downstream actually need it, or is
question    file+line sufficient given the repos are the record?
status      NOT ADOPTED. Cost may exceed value.
```

---

## TIER 3 — SPECULATIVE (no source, no test, parked deliberately)

### U-10  LAG DECLARATION PER CLAIM
```
t_visible / t_scored on a claim record — shortest interval at which
this claim's failure could become observable, over the interval at
which anyone checks. Already specced as P5 in the cooperative-
substrate work order; not yet a field on a claim.
Unknown whether it belongs on a claim or only on an action.
```

### U-11  REVERSE-GAP FIELD
```
a record states where its own instrument is WEAKER than a named
alternative. Would make the section-4 discipline of the merge-path
order structural rather than a one-off instruction.
Unknown whether anyone would ever fill it honestly.
```

### U-12  STALENESS / REVALIDATION TRIGGER
```
the railcar folder's ENVELOPE has one (valid for / not valid for /
degradation mode / revalidation trigger). Generalizing it to every
claim record is obvious and might be too heavy.
Unknown. Parked.
```

### U-13  N AND SATURATION ON A KIND
```
a kind or grouping carries the N it was derived from, and whether
adding records has stopped changing it. K4 has N=4, single-run,
single-folder, and did not replicate — the format had no place to
say that at the time it was proposed.
Unknown whether this is a record field or a report field.
```

---

## NOT ON THIS LIST, AND WHY

```
a confidence score per claim   scores compress the thing the
                               format exists to keep uncompressed.
                               A record already carries a falsifier;
                               a number beside it invites reading
                               the number instead.
a severity or priority rank    ranking is a judgement made once and
                               then inherited unexamined. Nothing
                               in this ecosystem ranks.
a verdict field on a branch    already decided against. Repair type
  entry                        is judged per case; the derivation
                               is what gets recorded.
```
