# report-typing

**Reports get typed by the reporter's position, not by content.**
The operation runs on routing, not on evidence — it never has to
claim anything about the report, it only assigns it to a channel
where reading is optional.

`MARKER.md` and `reverse_arm_score.py` are **delivered verbatim** and
modified by nothing here. All audit content is in
`marker_audit.py`, `CLAIM_TABLE.md` and this file.

This folder is the first named-and-absent artifact in its drop family
to arrive. Four folders had named it as their canonical shape while
it did not exist:

    criterion-symmetry      criterion applied downward, never upward
    question-availability   Q2, unaskable — the cost channel
    conversation-type       no channel typed to receive it
    blame-attribution       attribution tracks actor position

`question-availability` `QA_007` made the absence its own finding and
counted the mentions.

## What is here

| file | |
|---|---|
| `MARKER.md` | delivered. Mechanism, three instruments, an R-register of six work orders, falsifiers, cross-refs. |
| `reverse_arm_score.py` | delivered. The R1 instrument: a coding schema and a scorer for reverse-arm report instances. |
| `marker_audit.py` | the audit. Imports the scorer, reads the marker, modifies neither. 66 checks. |
| `CLAIM_TABLE.md` | `RT_001..RT_012` under a REFUTATION_PROTOCOL. |
| `samples/` | pinned audit output. |

    python3 marker_audit.py             # the report
    python3 marker_audit.py --selftest  # 66 checks
    python3 reverse_arm_score.py --schema

## The three instruments

**1 — credential correction.** Hold the claim constant, correct the
stated objection, measure whether the assessment updates. No update: the stated reason was produced after a discount
already applied. Run inadvertently twice in the literature; never as a
designed experiment.

**2 — the seat change.** Within-subject, the strongest design
available, because content, competence and credential are held
constant and only the seat moves. The prediction is that the
discount arrives *with the seat* and applies to reports inside the
person's prior domain.

**3 — the reverse arm (R1).** Reality television built the
experiment and never scored it. A disguised executive reports
upward; the supervisor doing the dismissing does not know who they
are dismissing, so the assessor is blind and no strategic behaviour
is available to them. This is the one the marker calls runnable now,
and `reverse_arm_score.py` is its coding instrument.

## What the audit found

The scorer's design is right and its refusals are declared. What is
checked is whether the code enforces what the prose promises, and in
six places it does not.

- **`RT_004`** — `receiver_blind` is checked with `is False`, and the
  schema displays the field as a **string**. A coder following the
  schema writes `"False"`, which does not drop the instance; nor
  does a missing field, nor `None`. The one branch whose failure
  runs *toward* the finding.
- **`RT_005`** — `d_exec_testimony` is declared with five values and
  read on none. Its stated purpose is to separate the two available
  readings of the whole genre.
- **`RT_006`** — `b_time_to_action`'s `why` says the discount is a
  **delay** and refusal is the tail. Every accumulator in `score()`
  is a `+= 1` occurrence counter, so the beats are never summed,
  averaged or binned, and only the tail is counted.
- **`RT_007`** — `contrast` and `verdict` are written as the literal
  `UNCODED`. The two-condition gate in the returned note — both arms
  present, second coder passed — is checked nowhere, so the refusal
  is a constant rather than a check.
- **`RT_008`** — the control arm is required in `CONTROL` and
  enforced nowhere. A one-arm input emits a well-formed result.
- **`RT_009`** — `domain` is Instrument 2's *sharp test*, is in the
  schema, and reaches no accumulator. Three quantities the prose
  asks for have no field at all, one of them named inside the
  control's own expected-result sentence.

Two about the marker rather than the scorer:

- **`RT_010`** — the `uninstrumented Q7` cross-ref is one past the
  end. The highest question ordinal anywhere in that folder is Q6,
  and R4 rests on the identification.
- **`RT_003`** — the back-reference list is shorter than the citing
  set, and one listed name is not a folder name.

## Two columns, and why

`observer-exclusion` contains the string `report-typing` and does not
cite it — its occurrences are entries in a cross-link checker's
target list. Counting that as a citation would be `QA_007`'s own
finding, that mention and existence are different columns, failing
inside a checker written about `QA_007`.

The classifier splits prose mentions from code-only occurrences and
is graded on a **constructed tree** rather than on this corpus. Corpus
counts are printed; what is asserted is the relation between them.
A known-answer check whose known answer lives in the data under test
is a regression test on that corpus wearing a known-answer's clothes
(`self-scan` `SS_030`).

## Scope

**Nothing here tests the mechanism.** No transcript has been coded,
no second coder exists, and every literature pointer in the marker —
Rafferty, the BC deskilling study, Araki/OECD, StatCan, arXiv
2602.21369, the Belzer/Viscelli pair, the Dangote figures, the
Nielsen demographic claim — is carried and unchecked at `ANC_010` /
`MS_004` status, the publisher hosts being refused by this
environment's egress allowlist. No claim in `RT_001..RT_011` rests
on any of them.

The marker states its own limits in the same terms: the one-observer
report is *"an observation of the pattern, not a scored count"*, and
the viewer-wording sample is *"direction not rate, provenance stated
so it can be discounted appropriately."*

## Siblings

`criterion-symmetry` (a criterion applied downward only),
`question-availability` (Q2, the cost of posing),
`blame-attribution` (attribution by role),
`conversation-type`, `observer-exclusion` (no intake path),
`uninstrumented` (the exclusion register).

CC0. Stdlib only. Parses under Python 3.9. Phone-buildable.
