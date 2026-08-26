# report-typing — CLAIM_TABLE

Claims about the delivered `MARKER.md` and `reverse_arm_score.py`.
Both are landed verbatim and modified by nothing here; every check
lives in `marker_audit.py`.

**Nothing in this table is a claim about institutions.** Whether
reports are typed by the reporter's position is an empirical
question, no transcript has been coded, and every literature pointer
in the marker is egress-blocked from this environment
(`MS_004` status). The claims below are about the artifact.

## REFUTATION_PROTOCOL

A failed check updates the claim. The delivered files are not
retuned to make a claim pass. Where a check disagrees with prose in
the marker, the disagreement is recorded in this file and the marker
is left as delivered.

| id | claim | status |
|---|---|---|
| `RT_001` | The gap closed. `report-typing` was named as the canonical shape by four folders and did not exist; it now does. | SUPPORTED |
| `RT_002` | Mention and citation are two columns, not one. The classifier splits them structurally and is graded on a constructed tree, not on this corpus. | SUPPORTED |
| `RT_003` | The marker's own back-reference list is shorter than the set citing it, and one listed name is not a folder name. | SUPPORTED |
| `RT_004` | `receiver_blind` is checked with `is False`, so the string the schema itself displays does not drop the instance. | SUPPORTED |
| `RT_005` | `d_exec_testimony` is declared with five values and read on none of them, and its stated purpose is to separate the two available readings of the genre. | SUPPORTED |
| `RT_006` | `b_time_to_action`'s measurement is a delay and no accumulator sums one. Every counter in `score()` counts occurrences; only the `NEVER` tail has one. | SUPPORTED |
| `RT_007` | The two-condition gate on `contrast` and `verdict` is prose. Both are written as the literal `UNCODED`; neither condition is checked. | SUPPORTED |
| `RT_008` | The control arm is required in `CONTROL` and enforced nowhere. A one-arm input emits a result and the missing arm is not flagged. | SUPPORTED |
| `RT_009` | `domain` is Instrument 2's sharp test, is in the schema, and is scored nowhere. Three further quantities the prose asks for have no field at all. | SUPPORTED |
| `RT_010` | The marker's `uninstrumented Q7` reference is one past the end — the highest question ordinal anywhere in that folder is Q6 — and R4 rests on it. | SUPPORTED |
| `RT_011` | The marker's CROSS-REFS open three new named-and-absent artifacts while closing one. | SUPPORTED |
| `RT_012` | Nothing here has been run on a transcript. The one instrument the marker calls runnable now has no data and no coder. | UNVERIFIED |

---

## RT_001 — the arrival

Four folders name this shape in prose: `criterion-symmetry`,
`question-availability`, `conversation-type`, `blame-attribution`.
Three of the four wrote a claim whose status was *blocked on
`report-typing`, absent* — `QA_007` counted its mentions against its
non-existence and made that the finding; `conversation-type`
`CT_006` recorded it as *"named by three markers and still does not
exist"*; `blame-attribution`'s `CELLS.md` opens *"Shape match:
report-typing"*.

**Falsifier:** none. The folder is here.

What the arrival does *not* close: the marker's own CROSS-REFS open
three more (`RT_011`), so the count of named-and-absent artifacts in
this drop family went from one to three in the same commit that
removed one.

## RT_002 — two columns

`observer-exclusion` contains the string `report-typing` and does
not cite it. Its two occurrences are entries in a list of names
`archival_bias.py` resolves, plus that checker's own pinned output.
It is *checking whether this folder exists*, which is the opposite
operation from naming it as a shape.

Pooling the two would be `question-availability` `QA_007` — mention
and existence are different columns — failing inside a checker
written about `QA_007`.

The split is structural and is not a judgement about what a folder
meant: a name in a `.md` is a prose mention, a name only in a `.py`
is a code-only occurrence. It is graded on a **constructed tree**
(`_column_null_test`), three folders written for the purpose — one
prose mention, one code-only target list, one silent — because a
classifier whose known answer lives in the corpus under test is a
regression test on that corpus wearing a known-answer's clothes
(`self-scan` `SS_030`).

The corpus counts are printed and **not asserted**. What is asserted
is the relation: the columns are disjoint, both are non-empty, and
the marker's list is shorter than the citing set.

**Falsifier:** a folder citing this shape in prose whose only
occurrence is a checker's target list, or the reverse.

## RT_003 — the back-reference list

    the marker says:  criterion-symmetry, question-availability,
                      blame-attribution-by-role
    citing in prose:  criterion-symmetry, question-availability,
                      conversation-type, blame-attribution

`conversation-type` cites it and is not listed. `blame-attribution`
is listed under `blame-attribution-by-role`, which is not a folder
name — the folder is `blame-attribution` and the string in its own
`CELLS.md` is `report-typing`, so the drift is in this direction
only.

Neither is consequential; both are recorded because a back-reference
list is a claim about the tree and is checkable against it.

**Falsifier:** the list matching the citing set.

## RT_004 — the blindness check

`receiver_blind` is the design. The reverse arm's whole warrant is
that the assessor does not know who they are dismissing, and the
confound block says a receiver who suspects the setup breaks
blindness: *"Code it, drop the instance."*

The drop is `if i.get("receiver_blind") is False: continue`.

    receiver_blind=False            instances counted: 0
    receiver_blind='False'          instances counted: 1
    receiver_blind='false'          instances counted: 1
    receiver_blind=None             instances counted: 1
    receiver_blind=<field absent>   instances counted: 1

The schema displays the field as the **string**
`"True | False -- if False, DROP the instance"`. A coder reading the
schema and filling it in writes `"False"`, and `"False" is False` is
`False`, so the instance stays. A missing field does not drop
either.

This is the one branch in `score()` whose failure runs *toward* the
finding: an instance where blindness lapsed and which stays in the
sample is one where the receiver may have known, and those are exactly
the ones that would show the disguised executive listened to.

The suspicion confound is otherwise **carried**, not missing —
`receiver_blind=False` is precisely the switch it asks for, and it
is the one value the check reads correctly.

**Falsifier:** the check reading a string, or the schema declaring a
boolean.

## RT_005 — a field declared and never read

    a_prior_filing     reads 1 of 4 values
    b_time_to_action   reads 1 of 3
    c_attribution      reads 2 of 4
    d_exec_testimony   reads 0 of 5

`d_exec_testimony`'s own `why` is *"distinguishes the two available
readings of the whole genre"* — `LEARNED_ABOUT_OPERATION` is the
forward, confounded reading and `SAID_IT_AND_IT_WENT_NOWHERE` is the
reverse reading the marker calls the finding. Neither reaches an
accumulator. A coder can fill the field correctly on every instance
and `score()` returns the same numbers.

The values are read out of the source rather than retyped, so a new
branch cannot go unnoticed here.

**Falsifier:** a branch reading it.

## RT_006 — the delay has no accumulator

`b_time_to_action`'s `why`: *"the discount is a delay, not always a
refusal. Refusal is the tail of the distribution, not the
measurement."*

Its declared values are `integer beats | NEVER | NOT_STATED`, and
`score()` reads `== "NEVER"`. Every accumulator in the function is
`+= 1` — five of them, all counting occurrences, none summing a
value — so an integer beat count is not summed, averaged or binned
anywhere. The quantity the field's own note calls the measurement
has no place to go; only its tail is counted.

Sharper than "reads only one value": the other three fields could be
scored by adding branches, and this one takes a different kind of
accumulator.

**Falsifier:** a sum, mean, or histogram over the beats.

## RT_007 — the gate is prose

    contrast_literal         True
    verdict_literal          True
    both_arms_checked        False
    double_coding_checked    False

The returned `note` states two conditions: both arms have instances,
and a second coder has passed the same transcripts blind. Both
`contrast` and `verdict` are written as the module-level literal
`UNCODED`, so they are `None` on every input — including one with
both arms present.

That default is **safe** and it is not a check: nothing distinguishes
*not yet earned* from *earned and computed*. The refusal is a
constant, and a constant refusal cannot report that a condition was
met.

**Falsifier:** a run where the conditions hold and the fields move.

## RT_008 — the control is required and not enforced

`CONTROL` states the requirement and the reason: without the
floor-worker rate in the same setting, a dismissal rate is
uninterpretable. `score()` returns `by_seat` for whatever seats it
was handed, so a single-arm input emits a well-formed result and
nothing in the output says the denominator is missing.

Same shape as `null-harness`'s known-truth-first invariant read as a
precondition rather than a measurement.

**Falsifier:** a one-arm input refusing, or flagging.

## RT_009 — stated in prose, no field or no branch

Carried in the schema and never branched on:
`content_summary`, `domain`, `episode_id`, `receiver_role`,
`timestamp`.

`domain` is the sharp one. Instrument 2's prediction is that the
discount applies to reports **in the person's original domain** —
*"the sharp test, because content sits squarely inside prior
expertise and routing ignores it."* It is codable, it is in the
schema, and it reaches no accumulator, so the instrument's own
sharpest prediction is the one thing the scorer cannot report on.

Asked for in prose with no field at all:

- **episode air order** and **network** — `CONFOUNDS["editing"]`
  says to code both *"so it can be checked rather than assumed"*.
- **known-exec seat** — `CONTROL["expected_if_marker_holds"]` is
  that disguised-exec instances score like floor-worker instances
  and *not* like **known-exec** instances elsewhere in the same
  organisation. `reporter_seat` declares two values and that is not
  one of them, so the comparison the control's expected result rests
  on is not expressible in the schema.

Seventh instance in this drop family of the stated-rule-with-no-field
shape (`MF_017`, `CW_015`, `DL_004`, `GC_012`, `UNI_013`, `SSS_050`),
and the first where the missing field is named inside the control's
own expected-result sentence.

**Falsifier:** the fields existing, or the prose not asking for them.

## RT_010 — Q7 is one past the end

The CROSS-REFS block cites *"uninstrumented — Q7 and the exclusion
mechanisms. R4 is a direct instance of Q7."*

`uninstrumented` resolves. Its highest question ordinal anywhere —
every `.md` and `.py` under the folder, cases included — is **Q6**,
in case 016. There is no Q7.

R4 (non-event output: prevention produces the absence of an output,
no counter increments) rests on the identification entirely. The
claim may well be right about some entry in that register; it does
not currently point at one.

**Falsifier:** a Q7 landing, or the reference naming an existing
ordinal.

## RT_011 — the cross-refs open three

    merit-anchoring            NO
    median-case-calibration    NO
    sensing-spine              NO
    uninstrumented             yes
    criterion-symmetry         yes
    question-availability      yes
    blame-attribution          yes

`merit-anchoring` was already named by `criterion-symmetry` and
carries what the marker calls the labour-market half of the same
engine. The other two are new.

So the arrival of this folder took the drop family's named-and-absent
count from one to three. A marker naming what it does not have is
the register's own discipline, and this is the
same pattern `QA_007` measured: the count is a property of how the
markers cross-reference, not of how much is missing.

**Falsifier:** any of the three landing.

## RT_012 — nothing has been run

R1 is the instrument the marker calls *"the one that is runnable
now"*. There is no `episodes.json` in this folder, no transcript has
been coded, no second coder exists, and the CLI with no argument
prints the schema.

The eight findings above are properties of a schema and a scoring
function. None of them is evidence for or against the mechanism, and
the marker's own status line already says so: *"That is an
observation of the pattern, not a scored count."*

Every literature pointer in the marker — Rafferty, the BC deskilling
study, Araki/OECD, StatCan, arXiv 2602.21369, the Belzer/Viscelli
pair, the Dangote figures, the Nielsen demographic claim — is
carried and unchecked, at `ANC_010` / `MS_004` status: the sources
are behind an egress allowlist that refuses every publisher host
from this environment. Nothing in `RT_001..RT_011` rests on any of
them.

**Falsifier:** run it. Code the reverse arm on transcripts, with the
control arm, with a second coder, and the four repairs above applied
— or report that the repairs change no number, which is also a
result.
