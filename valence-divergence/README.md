# valence-divergence

Logs a term used by two parties, records the valence each decoder assigned
and where each reading came from, and flags divergence.

**It does not determine valence.** There is no dictionary here and no model
of what words mean. Both readings are supplied. That is what makes the
instrument buildable at all: a valence dictionary would be one decoder
claiming to be the answer, and the instrument would then be reporting its
own reading as the finding.

The scored failure is not disagreement. Disagreement is visible and gets
handled. The scored failure is **agreement reached over an unflagged
mismatch** -- both parties proceed, neither marks the term, and the
divergence never surfaces.

```
python3 valence_divergence.py     # render the case set
python3 test_valence.py           # the checks
```

Stdlib only. No network. Parses under Python 3.9. ASCII only.
Phone-buildable. CC0.

## Files

| file | what it is |
| --- | --- |
| `WORK_ORDER.md` | the delivered order, verbatim, not edited |
| `valence_divergence.py` | the instrument |
| `cases.py` | the entries. Every one CONSTRUCTED |
| `test_valence.py` | the checks. Every expected verdict lives here |
| `CLAIM_TABLE.md` | `VD_001..VD_016` |
| `samples/` | one pinned run of each |

## The five checks

```
D1_DIVERGENT          the two valences differ, neither UNREAD, B not ABSENT
D2_UNFLAGGED          D1 and nobody marked the term at the time of use
D3_SILENT_PASS        D2 and the exchange continued -- the scored failure
D4_UNCHECKED          the history was not looked up; a queue entry, not a
                      failure
D5_ORPHAN_CANDIDATE   valence now, none at origin
```

D2 and D3 nest inside D1 by their own definitions, so `fired` is a chain on
three of the five rather than five independent verdicts -- **9** distinct
sets are reachable out of the 32 a five-item list could express, brute-forced
over the whole schema rather than sampled (`VD_005`). `D4_UNCHECKED` never
co-fires with anything, which is structural and not a property of the case
set (`VD_006`).

## What the instrument does not hold

- **No lexicon, no valence model, no sentiment scoring.** `term` is carried
  and read by nothing -- asserted from the AST and behaviourally, which is
  the strongest available form of the constraint: the instrument never looks
  at the word (`VD_007`).
- **No field for intent, motive, or what either party meant.** Three
  identifier vocabularies scanned through `tools/authority_scan`, each with
  a planted violation beside it so a clean result means something.
- **No ranking of the decoders.** D1 is swap-invariant over the full valence
  space, measured at 0 of 125 pairs. D5 is directional by design -- a claim
  about now against origin -- and that asymmetry is reported rather than
  hidden (`VD_015`).
- **Nothing averaged, no dominant sense, no single valence.** The return has
  no top-level valence field at all, both readings come back byte-for-byte,
  and no valence is ever changed, merged or invented anywhere in the schema.
  Branches of one term are separate entries with nothing linking them
  (`VD_014`).

## Where the order leaves a decision open

Nine places, all in `CHOICES`, all printed in the header of every render,
none silent. The three that carry the most:

- `[CHOICE 1]` **`decoder_attribution` declares three values and needs
  four.** The order calls the field the point of the instrument and glosses
  it as naming the decoder that produced the valence *when only one did* --
  which defines `A` and `B`, leaves `SPLIT` undefined by its own sentence,
  and has no cell for the both-`UNREAD` entry the schema admits directly.
  `NEITHER` is added (`VD_001`).
- `[CHOICE 3]` **D5 merges `NEUTRAL` and `UNREAD`**, which is the one
  distinction the intake section says in as many words must not be merged.
  The check is left exactly as written and `d5_basis` is carried beside it
  (`VD_002`).
- `[CHOICE 9]` **the order fixes `flagged_by` and `proceeded` for case D
  only.** Under the values chosen here, eight entries fire the scored
  failure. `unstated_field_effect()` splits every entry's codes into
  invariant and contingent, and the order's own MUST lists for A and B come
  back **invariant** -- so the requirement is a property of the case and the
  `D3` beside it is a property of the choice (`VD_004`).

## The findings worth reading first

`VD_003` -- D1's guard names a valence (`UNREAD`) and a source (`ABSENT`),
and the source clause changes a verdict on exactly **12** shapes, every one
of them an `ABSENT` source carrying a valence, which the order's prose
implies cannot happen. Refusing that combination at intake would make the
clause dead; admitting it is `[CHOICE 5]`.

`VD_010` -- the order's case E (*an unchecked history is not a divergence*)
and that admitted-incoherent entry are the same clause seen from two sides.

`VD_013` -- every etymological claim here is **carried** from the work order
and verified against nothing, which is what the design says it should be:
*the instrument stores the result of the lookup and its source. It does not
perform the lookup and must not pretend to.* Each `citation` field says
where the claim came from rather than naming a reference work nobody here
opened.

`VD_016` -- found by a plant and not by reading: a two-token entry in a
forbidden-identifier vocabulary can never match, because the scanner splits
identifiers into single tokens. It reads as coverage and catches nothing.
Repaired, and the rule is now asserted for all three vocabularies.

## State

**UNVERIFIED** (`VD_012`). No exchange has been logged, no speaker is a
person, no utterance here was said. Every entry is constructed and says so
in its own record. Whether these five checks separate real divergences from
real agreement is untouched in both directions. What is established is that
the falsifier the order names is met: case D fires `D1`, `D2` and `D3`, and
case C -- the required negative -- logs clean.

No metric is registered in `tools/known_answer.py`, and `VD_011` says why
rather than leaving an absence that looks like an oversight.

The check count is printed by `python3 test_valence.py` and is not stored
here.
