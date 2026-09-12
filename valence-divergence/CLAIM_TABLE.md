# CLAIM TABLE -- valence-divergence/

`VD_*` are properties of the instrument built here. They are not the work
order's checks; those are `D1`..`D5` and live in `WORK_ORDER.md`, delivered
verbatim and not edited.

Every number below is produced by `python3 test_valence.py` or
`python3 valence_divergence.py`. Nothing here is a claim about any word,
any exchange, or any person.

| id | claim | status |
| --- | --- | --- |
| VD_001 | `decoder_attribution` declares three values and needs four | DECIDED |
| VD_002 | D5 merges the one distinction the intake section says must not be merged | RECORDED |
| VD_003 | D1's ABSENT clause is live on exactly the entries the schema should arguably refuse | MEASURED |
| VD_004 | `flagged_by` and `proceeded` are stated for case D only; D2 and D3 on A, B and C are carried by a choice made here | MEASURED |
| VD_005 | `fired` is a chain on three of five, not five independent verdicts | MEASURED |
| VD_006 | D4 never co-fires with anything, by construction | MEASURED |
| VD_007 | `term` reaches no check -- the instrument never looks at the word | MEASURED |
| VD_008 | the Open section's self-report problem is recorded and not enforced | DECIDED |
| VD_009 | case C logs clean and its empty list is distinguishable from an unrun read | HOLDS |
| VD_010 | case E and the incoherent-entry admission are one mechanism from two sides | HOLDS |
| VD_011 | no metric is registered in `tools/known_answer.py`, and why | STATED |
| VD_012 | nothing has been run against a real exchange | UNVERIFIED |
| VD_013 | every etymological claim is carried, which is what the design says it should be | CARRIED |
| VD_014 | branches are unlinked, and the cost is that nothing here can count them | DECIDED |
| VD_015 | D1 is swap-invariant; D5 is directional by design and the asymmetry is reported | MEASURED |
| VD_016 | a multi-token entry in a forbidden vocabulary is unmatchable by construction | REPAIRED |

---

## VD_001 -- `decoder_attribution` declares three values and needs four

The order calls this field the point of the instrument: *"A divergence
report that does not say whose reading is whose has thrown away the
finding."* It declares `"A" | "B" | "SPLIT"` and glosses the field as naming
*"which decoder produced the valence when only one did."*

That sentence defines `A` and `B` and **leaves `SPLIT` undefined by its own
terms** -- `SPLIT` is by definition the case where more than one did. And
neither the sentence nor the vocabulary has a cell for an entry where
**neither** decoder produced a valence, which the schema admits directly:
`reading_A.valence` `UNREAD` beside `reading_B.valence` `UNREAD`.

`[CHOICE 1]`: `SPLIT` is read as *both decoders produced a valence*,
agreeing or not; `NEITHER` is added as a fourth value. `R_both_unread`
reaches it. The alternative -- forcing a both-UNREAD entry into `A` or `B`
-- would name a decoder that returned nothing, which is the failure the
field exists to prevent one step down.

## VD_002 -- D5 merges the one distinction the intake section protects

The intake section says it in as many words:

> `UNREAD` is a valid and important value. It means the decoder assigned no
> valence, which is itself a reading and must not be recorded as NEUTRAL.
> NEUTRAL means read and found flat. UNREAD means not read.

D5's own condition is `reading_B.valence in {"NEUTRAL", "UNREAD"}`. The two
states the order separates are the two arms of one disjunction, so a D5
firing does not say whether the history was read and found flat or never
read at all -- which is the whole difference between an orphaned valence and
an unfinished lookup.

The check is **left exactly as the order writes it**. `[CHOICE 3]` carries
`d5_basis` (`NEUTRAL_AT_ORIGIN` / `UNREAD_AT_ORIGIN`) beside the fired list
instead. On the case set: 7 `NEUTRAL_AT_ORIGIN`, 1 `UNREAD_AT_ORIGIN`.

## VD_003 -- D1's ABSENT clause is live on exactly the incoherent entries

D1's guard names a valence (`UNREAD`) and a source (`ABSENT`) -- two fields
in two different vocabularies. `absent_clause_is_live()` removes the source
clause and sweeps the schema: the verdict changes on **12** shapes, and
**every one of them is an `ABSENT` source carrying a valence other than
`UNREAD`**.

The order's prose implies that combination cannot happen -- `ABSENT` means
the history was not looked up, which implies no valence was assigned. So the
clause is dead unless the schema admits an entry the prose says is
incoherent, and live exactly where it does.

`[CHOICE 5]` admits it rather than refusing it at intake, on the ground that
refusing it would delete the only evidence the clause does anything.
`R_absent_valence` is that entry, and it reads `D4_UNCHECKED` alone, never as
a divergence.

## VD_004 -- the order fixes the two flags for case D only

Case D states `flagged_by NEITHER, proceeded True`. Cases A, B and C state
neither field, so both were chosen here (`NEITHER` / `True`), and under that
choice **eight entries fire `D3_SILENT_PASS`** -- the scored failure --
including all four of case B and both arms of case A.

`unstated_field_effect()` sweeps both fields over their full vocabularies and
splits each entry's fired codes into invariant and contingent. The result:

- A1 and all four B entries -- **invariant `D1`, `D5`**; contingent `D2`, `D3`
- A2 -- invariant `D1`; contingent `D2`, `D3`

So the order's MUST lists (*"MUST fire D1 and D5"*) hold under **every**
value of the two fields it leaves open. The requirement is a property of the
case. The `D3` beside it is a property of the choice, and the render says so
under `[CHOICE 9]` rather than leaving a reader to read a contingent scored
failure as a finding.

## VD_005 -- `fired` is a chain, not five verdicts

D2 is *D1 fired AND ...*; D3 is *D2 fired AND ...*. Three of the five checks
are nested by their own definitions, so the return is not five independent
readings. `reachable_fired_sets()` brute-forces the whole schema -- 3000
combinations of the five declared vocabularies and the two booleans, not a
sample -- and finds **9 distinct `fired` sets** out of the 32 subsets a
five-item list could express:

```
(none)  D1  D4  D5  D1,D2  D1,D5  D1,D2,D3  D1,D2,D5  D1,D2,D3,D5
```

Asserted in both directions: no reachable set carries D2 without D1 or D3
without D2.

## VD_006 -- D4 never co-fires with anything

`co_firing()` measures it over the same enumeration: `D4_UNCHECKED` appears
in no set with any other code. It is structural, not a property of the case
set -- D1 excludes an `ABSENT` source by its own guard, D5 requires a
history source, and D2 and D3 nest inside D1.

Which means the queue entry and every reading are disjoint by construction:
an entry can never be both unchecked and divergent, and a reader sorting on
`D4` is sorting a partition rather than a flag.

## VD_007 -- `term` reaches no check

The strongest available statement of *no lexicon* is not that the module
holds no dictionary but that it never looks at the word. Asserted two ways:

- from the AST -- none of the five checks, nor `attribution`, nor `d5_basis`
  names `term` or `speaker`;
- behaviourally -- the verdict is unchanged when the term is replaced by the
  empty string, by `"POSITIVE"`, by a null byte, or by 200 characters.

Same for the free text: no check reads `gloss`, `citation` or
`date_or_period`, no check calls a string method, and a gloss reading
`"POSITIVE. GOOD. NOT NEG. valence=POS"` moves nothing and comes back
unaltered.

## VD_008 -- the Open section, recorded and not enforced

> Reading_A currently requires someone to state the default reading. Self-
> reporting a default is exactly the thing that fails elsewhere in this
> ecosystem. Unresolved.

`[CHOICE 6]` adds `reading_A.demonstrated` (`IN_USE` / `ON_REQUEST` /
`UNRECORDED`, default `UNRECORDED`) and **does not enforce** the order's
provisional handling. Enforcing it -- logging reading_A only when
demonstrated in an actual utterance -- empties most real logs, and that call
belongs to whoever runs the instrument rather than to whoever built it.

The field's honest state on this case set: `UNRECORDED` 19, `IN_USE` 1,
`ON_REQUEST` 1. On constructed data the default is doing nearly all the
work, which is what the field will look like on a log nobody has been asked
to fill in.

## VD_009 -- case C logs clean

Both readings `NEUTRAL`, nothing fires, `fired == []`, grade `LOGGED`. The
order is explicit about why this matters: *"An instrument that flags every
term is a preference dressed as a method."*

`[CHOICE 2]` keeps that empty list distinguishable from an entry that failed
intake, where `fired` is `None`. `[]` says five checks ran and none fired;
`None` says no check ran. Collapsing them would make the required negative
indistinguishable from a malformed record.

The second arm (`C_pos`, reading_A `POS`) fires D1, because difference is the
only condition D1 reads. That arm is what makes the NEUTRAL arm a control
rather than a shape the instrument is blind to.

## VD_010 -- case E and the admitted-incoherent entry are one mechanism

Case E requires `D4` **only** and forbids `D1`: *"An unchecked history is not
a divergence, and the instrument must not manufacture one from absence."*
What stops D1 is the `ABSENT` source clause of VD_003.

So the order's own validation case and the entry its prose implies cannot
exist are the same clause seen from two sides. Case E reaches it with
`UNREAD` beside `ABSENT`, where either half of the guard would do;
`R_absent_valence` reaches it with a valence beside `ABSENT`, where only the
source clause does.

## VD_011 -- no metric is registered, and why

`tools/known_answer.py` refuses a metric with no known-answer case, and the
repo test asserts every metric is in its manifest. Nothing here qualifies:
the five checks return booleans, `attribution` and `d5_basis` return members
of a declared vocabulary, and `read` returns a record. `reachable_fired_sets`
is an exhaustive enumeration whose known answer is the enumeration itself --
registering it would be registering a case that computes its own expectation.

Stated rather than left silent, because an absent registration and an
overlooked one look identical from outside.

## VD_012 -- UNVERIFIED

No exchange has been logged. Every entry in `cases.py` is constructed and
says so in its own `constructed_note`; no speaker is a person and no
utterance was said. Whether the five checks separate real divergences from
real agreement is untouched in both directions.

The order's own falsifier -- *"If D3 does not fire, the instrument cannot
detect the only failure mode it was built for"* -- is a property of the code
and is met.

## VD_013 -- every etymological claim is carried

`hystera` = womb, the PIE abdomen root, the 1610s mechanism, the 1939
branch, *of the woods*, *rural*, *wild animal*, the pious/superstitious
adjective, `oikonomia` = household management: all carried from
`WORK_ORDER.md` and verified against nothing in this folder. There is no
network here and no reference work in this repository.

This is not a shortfall against the design, it is the design:

> This is a WORKFLOW, not an algorithm. The instrument stores the result of
> the lookup and its source. It does not perform the lookup and must not
> pretend to.

Every `citation` field therefore says where the claim came from rather than
naming a dictionary nobody here opened. An instrument that filled that field
with a plausible reference would be performing the lookup.

## VD_014 -- branches are unlinked, and that has a cost

`[CHOICE 8]`. No entry carries a field pointing at another. Case A is two
entries and case B is four, and the only handle joining them is the `term`
string, which VD_007 establishes the instrument reads for nothing.

The order makes this the reader's job explicitly: *"Four entries, not one;
the instrument logs terms, and the observation that they share a shape is
made by the reader."* The cost is real and stated: nothing in the folder can
report how many branches a term has, or that `hysteria` has two. The
alternative -- a group id -- is one field away from a record that can be
summarised, and summarising branches is the failure the instrument exists to
prevent.

## VD_015 -- D1 is swap-invariant; D5 is directional by design

*"No field ranks the decoders. Neither is the correct one."* Measured rather
than promised: `d1_swap_invariance()` exchanges the two valences across the
full 5x5x5 space and D1 moves on **0 of 125** pairs.

D5 moves on **16 of 125**, and that is correct -- D5 is a claim about a
valence now against its absence at origin, which is a statement about
direction in time and not a ranking of decoders. Reported in the render
beside the invariance result rather than left for someone to discover.

## VD_016 -- a multi-token forbidden entry is unmatchable

Found by the plant, not by reading. `tools/authority_scan.split_identifier`
splits `citation_count` into `["citation", "count"]`, so a vocabulary entry
spelled `citation_count` can never equal any token the scanner produces --
it reads as coverage and catches nothing. The standing-vocabulary plant
returned one hit where two were expected, which is what surfaced it.

Repaired by dropping the unmatchable entry, and the rule is now asserted for
all three vocabularies here rather than left as a comment: every entry must
satisfy `split_identifier(t) == [t]`.

`citation` itself is deliberately **not** forbidden -- it is a source field
the schema requires -- and a check pins that it survives the standing scan.
