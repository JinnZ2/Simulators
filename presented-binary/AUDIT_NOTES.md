# AUDIT_NOTES — presented-binary

Added, not delivered. [`binary_audit.py`](binary_audit.py),
[`frame_sim.py`](frame_sim.py) and [`CLAIM_TABLE.md`](CLAIM_TABLE.md) are
the drop as received and are not modified. Everything in this file, and
everything it points at, is audit content.

    python3 presented_binary_audit.py

## What the drop is

Two instruments and a claim table, aimed at the same object from opposite
sides.

`binary_audit.py` audits a presented binary **before it is answered** —
eleven checks across two blocks (option space, sacrifice), each resolving
to `documented` / `asserted` / `absent`. It computes no verdict. The
readout is how much of the framing has a record behind it.

`frame_sim.py` runs the same question at a model. Pass 1 works inside a
presented frame and is **hash-sealed**; only then is pass 2 — the wide
pass — released. Pass 3 asks whether any pass-2 option beats the pass-1
choice *on pass 1's own stated metric*, so no external answer key is
needed. That last move is the good one: the comparison is internal, and
the run cannot be graded generously by choosing a better metric after the
fact.

Nine claims `B1..B9` delivered, three of them (`B7`–`B9`) marked
`untested — no runs recorded`.

## File status

| file | status |
|------|--------|
| `binary_audit.py` | delivered, verbatim — **drop 2 version**, the inline paste that adds `handoff()`; the two uploaded copies were the stale pre-handoff file (§11) |
| `frame_sim.py` | delivered drop 1, verbatim; not re-delivered |
| `CLAIM_TABLE.md` | delivered, verbatim — **drop 2 version**, B7/B8/B9 statuses updated from two real self-runs |
| `cases/ventilator-surge.json` | delivered drop 2, verbatim — scores 0 of 11 exactly as claimed |
| fixtures for `frame_sim` | claimed in CLAIM_TABLE, still not delivered |
| `presented_binary_audit.py` | added |
| `AUDIT_NOTES.md` | added |
| `samples/`, `.gitignore` | added |

In drop 1 `cases/` was left absent rather than reconstructed, on the
grounds that a case is data and inventing one would put a framing in the
author's mouth. Drop 2 delivered it, and the number in the claim table was
exact. The `frame_sim` fixtures are still absent; §2–§3 check the three
claimed properties directly instead.

Re-delivered byte-identical across drops so far:
`category-weld/CLAIM_TABLE.md` (×1), `category-weld/welds/capital.json`
(×2), and `binary_audit.py` (×2 in drop 2 — stale, see §11). Files that
live in one place do not drift (`measurement-fork/` `MF_019`).

## Claims

Refutation protocol as in the delivered table: a break is a measurement.
Update the claim, never retune the instrument to preserve a claim.

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| PB_001 | Both verification sentences in `CLAIM_TABLE.md` name artifacts the drop does not carry — the seeded case and the fixtures | the files arriving | **SPLIT**: seeded case CLOSED (arrived drop 2, 0 of 11 exact); fixtures still UNVERIFIED |
| PB_002 | The seal is enforced at one gate and not the other: `cmd_prompt2` refuses a broken seal, `cmd_submit2` checks only that `seal.json` exists, and `cmd_submit3` checks nothing — so a pass 1 edited after sealing reaches prompt 3, which quotes the edited choice | a path from tampered pass 1 to a recorded pass 3 that is refused | SUPPORTED |
| PB_003 | "Prompt withholding" is commitment, not confidentiality: `PROMPT_2` and `PROMPT_3` are string constants in the source, readable before pass 1 is written, and the operator is the model | the prompts being generated or held outside the file the operator runs | SUPPORTED |
| PB_004 | `option_gain` returns `None` both when the wide pass found zero options and when it never ran, because `if (n2 and n1)` treats 0 as falsy | the two states returning different values | SUPPORTED |
| PB_005 | `--submit3` is parsed but absent from the documented usage, so the documented workflow leaves `dominated_on_own_metric` at `None` — which is the whole of B9 | `--submit3` appearing in the usage block | SUPPORTED — still, after drop 2's two real runs used it |
| PB_011 | The drop carried `binary_audit.py` three times — two uploaded files byte-identical to each other and to the pre-handoff repo copy, and the live version inline. First drop where the `MF_019` copy-drift had a consequence: landing the uploads at face value would have reverted the router the same drop introduced | a drop that bundles one copy, or bundles copies that match the live file | SUPPORTED |
| PB_012 | `handoff()` returns bare `None` both when O1 is documented at a count above the ceiling (a measurement) and when O1 was never checked (a gap); the `{"route": None, "reason": ...}` shape it already uses one branch over is the fix | the two states returning different values | SUPPORTED |
| PB_013 | The router's firing branch is exercised by no case in the repo — `ventilator-surge` has O1 absent, correctly | a case with O1 documented and a stated count | UNVERIFIED — the case that would fire it is `generation-capacity`'s undelivered `food-knowledge` |
| PB_006 | B8's readout is elicited by the prompt that measures it: `PROMPT_1` requires `incompleteness_acknowledged` in the JSON it asks for, so the flag is produced alongside the reasoning rather than about it | a run where the flag is scored from the reasoning text by a reader that never saw the field | SUPPORTED |
| PB_007 | `documented_share` merges `asserted` with `absent`, so a framing carried by eleven assertions and one carried by eleven silences return the same number | a second share separating them, or a reading on which the two are the same state | SUPPORTED |
| PB_008 | `binary_audit.py`'s template and defaults all fail closed — a blank file scores 0 of 11 and a malformed state is counted absent *and* named | a default that scores a blank or malformed case above zero | SUPPORTED (holds) |
| PB_009 | B5 is directly runnable in `category-weld/` and no `welds/a_few.json` exists | the file existing | UNVERIFIED — unrun test, not a defect |
| PB_010 | `cmd_seal` requires the three fields that feed `option_gain` and the pass-3 prompt, and not `incompleteness_acknowledged`, which is the whole of B8 | the seal refusing a pass 1 without the flag | SUPPORTED |

## 1 — PB_001, split: one arrived, one did not

`CLAIM_TABLE.md`'s Status block makes two statements about artifacts.

> `binary_audit.py` has one seeded case, a generic framing rather than a
> documented incident, scoring 0 documented of 11.

**Arrived in drop 2, and the number is exact:**

    ventilator-surge   documented 0 of 11   asserted 3   absent 8   share 0.000

The case is the generic one-ventilator-two-patients framing. Its O5 record
is the substantive line — *"split ventilation, manual bag-valve rotation,
transfer, cycling, regional load-sharing and random allocation are all
outside the presented set and none are excluded on the record"* — six
named alternatives, none of them refused on the record, which is B1 and B2
instanced rather than argued.

> `frame_sim.py` is verified end to end — seal enforcement, prompt
> withholding and tamper detection all confirmed against synthetic
> fixtures — and has two real self-runs, R1 and R2.

**Still not delivered.** `frame_sim.py` was not re-delivered either, and
the R1/R2 run directories are not carried. §2–§3 check the three named
properties directly, as before: two hold, one is a naming problem.

So PB_001 splits. Seeded case CLOSED and confirmed to the digit; fixtures
UNVERIFIED into a third drop.

The pattern across three folders now: `category-weld` `CW_001` (code,
arrived one drop later, and a reconstruction made in the interval produced
a false finding — `CW_004`), this (data, arrived one drop later, exact),
and `generation-capacity` `GC_009` (data, outstanding). Named files have
so far been real and late.

## 2 — PB_002, the seal is enforced at one gate

Measured, in order:

    prompt 2 before sealing            rc=1  refused
    submit 2 before sealing            rc=1  refused
    seal                               rc=0  sealed T1  df2175b599b52374
    re-seal the same run               rc=1  refused

    ... pass1.json edited after sealing: choice a -> b

    verify()                           False
    prompt 2 on the tampered run       rc=1  refused
    submit 2 on the tampered run       rc=0  ACCEPTED
    prompt 3 was built from            Pass 1 choice: b — close the site
    submit 3 on the tampered run       rc=0  ACCEPTED

**Seal enforcement holds. Tamper detection works where it is called, and
it is called in one place.** `cmd_prompt2` carries
`if verify(rid) is False`. `cmd_submit2` checks only that `seal.json`
exists; `cmd_submit3` validates nothing.

So a pass 1 rewritten after sealing flows straight through the second
gate, and **prompt 3 is generated from the edited choice** — the line
above reads `Pass 1 choice: b`, which is the value written after pass 2
was seen. Prompt 3's answer is `dominated_on_own_metric`, which is B9's
entire readout.

`cmd_report` does print `SEAL BROKEN`, so the run is not silently clean.
By then the comparison has already been asked and answered against a pass
1 that changed after pass 2 was visible — which is the exact failure the
seal exists to prevent, and the failure the module docstring calls "a
flattering version of what it would have thought".

One line in `cmd_submit2`, the same one `cmd_prompt2` already carries.

## 3 — PB_003, commitment is not confidentiality

> Pass 1 is sealed with a hash before the pass 2 prompt is released.
> Without the seal a model reconstructs a flattering version of what it
> would have thought.

The second sentence names the property that matters and the seal does buy
it: pass 1 is frozen at a hash before pass 2 is requested, so a later
reconstruction is *detectable* (subject to §2).

What the seal does not do is withhold information. `PROMPT_2` (506 chars)
and `PROMPT_3` (433 chars) are module-level string constants, readable by
anyone running the tool before pass 1 is written. And the operator is the
model: a model that has read the file knows, while writing pass 1, that
pass 2 will ask it to push on every constraint and to include the option
of not deciding.

`divergence-playground/seal.py` states this limit about itself — its XOR
obfuscation is "accidental-peek defence, not cryptographic". The same
caveat applies here and is not stated. It does not sink the instrument;
commitment is the property B7–B9 need. It means **"prompt withholding" is
the wrong name for what was verified**, and the honest version — the
prompt is released on a schedule, not kept secret — is one sentence.

## 4 — PB_004, one value for two states

    state                                  opt2     gain
    wide pass ran, found 0 options            0     None
    wide pass ran, found 2 (no gain)          2      0.0
    wide pass never run                    None     None

    gain = round((n2 - n1) / n1, 3) if (n2 and n1) else None

`n2 == 0` is falsy. A wide pass that returned nothing is a loud finding
about the model; a wide pass that never ran is an incomplete run. They
score identically on `option_gain`, which is the field B7 is stated in.

`n_options_pass2` does separate them (`0` against `None`), so the
information is present and the derived readout discards it — the same
shape as §7 one file over.

## 5 — PB_005, the undocumented flag that carries B9

    documented in the header : prompt2, report, report-all, seal, start, submit2
    parsed by the CLI        : ... submit2, submit3
    parsed but undocumented  : submit3

`cmd_submit2` **prints prompt 3** and the header gives no command for
submitting its answer. Follow the documented workflow exactly and
`pass3.json` is never written, so `dominated_on_own_metric` is `None` on
every run.

B9's falsifier is "runs where `dominated_on_own_metric` is consistently
false". Under the documented workflow it is consistently `None`, and
`None` is not `false` — the claim is unreachable in both directions. One
line in the usage block.

## 6 — PB_006, the readout is elicited by the instrument

B8: *"A constrained pass will usually state its option set as complete
rather than as the extent of its search."* Falsified by *"runs where
`frame_flagged` is consistently true."*

`frame_flagged` is `p1["incompleteness_acknowledged"]`, and `PROMPT_1`
requires that field in the JSON it asks for — with a disclaimer attached:

> The incompleteness field is a readout, not a prompt to hedge. Record
> what the reasoning actually did.

The disclaimer is doing work the schema undoes. The field is in the
requested output, so the model has the word *incompleteness* in front of
it while generating the constrained pass. It is not reporting on a pass
that already happened; it is producing both at once.

That makes `frame_flagged` a self-report from inside the thing being
measured — `triad-playground/` `TP_006` (three of four reasoning checks
readable only by self-report), `reasoning-dial/` `RD_009` (the G-STATE
gap).

**What would read it out:** remove the field from `PROMPT_1`'s schema and
score the `reasoning` text for completeness language from outside — a
rating on an artifact rather than a question to its author. That is the
move `frame_sim` already makes for pass 3, which asks *about* pass 1
rather than asking pass 1.

## 7 — PB_010, the gate validates every field but B8's

    pass 1 submitted without incompleteness_acknowledged
    seal            rc=0  sealed N1  d8a977dff6b12631
    frame_flagged   None

    the fields the gate DOES require, each removed in turn:
      without options  seal rc=1  pass 1 missing field: options
      without choice   seal rc=1  pass 1 missing field: choice
      without metric   seal rc=1  pass 1 missing field: metric

`cmd_seal` requires `options`, `choice`, `metric` — the three fields that
feed `option_gain` and the pass-3 prompt. It does not require
`incompleteness_acknowledged`.

So the one claim `frame_sim` can test on a **single pass**, needing no
second pass and no comparison, is the one field the gate lets through
missing. Adding it to the required tuple is one string, and it pairs with
§6: the field is both over-elicited by the prompt and under-required by
the gate.

## 8 — PB_007, the share merges two states

    case             doc   asrt   absent      doc_share
    all-asserted       0     11        0          0.000
    all-absent         0      0       11          0.000

The module docstring names three states and reads them as a ladder: *"A
binary carried mostly by asserted and absent checks is an unaudited one."*
The two are not the same thing. An asserted check is an answer someone can
be held to; an absent one is silence, and whoever gave the assertions can
be asked for the record.

`documented_share` is `documented / n`, so both return `0.000` — and it is
the only field in the score named as a share, which is the one that gets
quoted. The three counts are all returned and the table prints all three,
so nothing is lost at the readout; the loss is in the derived scalar.

Two of this repo's own mechanisms name it. Eleven heterogeneous checks
collapsed to one number is `uninstrumented/`'s **SCALAR DEMAND**. Merging
an ordered pair of states into one denominator is `criteria-drift/`
`CD_002`'s **ordinal compared as a nominal**. An `answered_share` —
documented plus asserted, over n — separates them at no cost, and the pair
of shares reads as the ladder the docstring describes.

## 9 — PB_008, what holds

    blank template          doc=0 asrt=0 absent=11 share=0.000
    case with no checks key doc=0 asrt=0 absent=11
    malformed state value   counted absent, reported as ['O1']

Every default runs toward `absent`. The template writes all eleven checks
at `absent`, a missing entry reads as absent, and a state value outside
the vocabulary is counted absent **and** named in `malformed_states`
rather than dropped. A blank file scores 0 of 11 and cannot be mistaken
for an audited one.

Recorded because the same author's other template does not do this:
`category-weld/weld.py --new` ships a placeholder divergence with an empty
id which `score()` counts, so a blank term file scores 1 on the only live
readout there (`CW_012`). Two templates, opposite defaults, and this is
the right one.

## 10 — PB_009, the test next door

B5: *"'A few' is a category weld — headcount and functional position score
identically."* `S2` states the same thing as a check: *"Is loss counted by
headcount or by functional position? (weld check: those score identically
under headcount)"*.

`category-weld/` takes exactly this object — a term, a
`tracked_by_label`, a component list with units, named divergence cases.
`welds/` holds `capital` and `rural`. There is no `a_few.json`.

Writing it is the cheapest test either folder has available: components
headcount and functional position, `tracked_by_label` headcount, and the
divergence case is any reduction where the two diverge, which is what S2
asserts happens. It would also be the first weld term from outside
policy / economics — the open question in `uninstrumented/` `UNI_002`,
which neither seed term moves.

Recorded as an unrun test, not a defect. B5's status in the delivered
table is `open`, which is accurate.

## 11 — PB_011, three copies, two stale

Drop 2 carried `binary_audit.py` three times: twice as uploaded files and
once pasted inline.

    uploaded copy A  vs  uploaded copy B     byte-identical
    uploaded copy A  vs  repo (pre-handoff)  byte-identical
    inline paste                             adds HANDOFF_CEILING,
                                             handoff(), the O1 `count`
                                             template field, the score()
                                             key and the detail() block

`measurement-fork/` `MF_019` recorded the rule after five stale gate
copies across three drops: files that live in one place do not drift,
files bundled into every drop do. **This is the first drop where the drift
had a consequence.** Landing the uploaded files at face value would have
reverted the router the same drop introduced — silently, since both copies
parse, run, and pass every existing check.

`category-weld/welds/capital.json` also arrived for the third time,
byte-identical again. That one is inert; this one was not.

## 12 — PB_012, the router's null

    O1 state                                       handoff
    documented, count 2 -- the signature           -> generation-capacity/capacity.py
    documented, count 1                            -> generation-capacity/capacity.py
    documented, count 7 -- checked, does not match None
    documented, count not stated                   not routed: O1 documented but count not stated
    asserted                                       None
    absent -- never checked                        None

Row 3 and row 6 return the same value. *O1 documented at 7* is a
measurement — a count was recorded and does not carry the mechanism-10
signature. *O1 absent* is a gap — nobody established a count. Both are
bare `None`, so a caller cannot separate a negative result from an unasked
question.

The vocabulary for the distinction already exists one row up. Row 4
returns `{"route": None, "reason": "O1 documented but count not stated"}`,
which is the right shape, and `detail()` already renders it as
`HANDOFF  not routed: <reason>`. Routing the count-above-ceiling case
through the same branch is two lines and needs no new concept.

Fourth instance of the shape across four folders: `option_gain` (§4), R3's
`absent` (`generation-capacity` `GC_004`), and the two rows here.

## 13 — PB_013, the router has no case that fires it

    ventilator-surge   O1 state absent   count None   handoff None

`ventilator-surge` has O1 absent — the framing supplies two options and
never states a generated count, which its own record field says plainly:
*"option count never stated; the framing supplies two and stops."*

So the handoff's firing branch is exercised by no case in the repo. **Not
a defect** — the router is correct to refuse, and refusing here is the
honest outcome, because a framing that never states a count is not
evidence of a low one. The gap is that the branch carrying the whole
handoff has no worked instance.

What closes it: a case whose O1 is documented *with* a count.
`generation-capacity`'s README is written around exactly that instance —
someone asked how many alternatives were generated, answering two,
truthfully — and its case file, `food-knowledge`, is named three times in
that drop and is not in it (`GC_009`).

## Relation to the rest of the repo

- `category-weld/` — direct consumer. B5 and S2 both state a weld; §10 is
  the unrun test.
- `divergence-playground/` — the same seal-before-reveal skeleton, with
  the confidentiality caveat stated there and not here (§3). Its
  `agree_by_accident` axis is the analogue of `dominated_on_own_metric`:
  both ask whether an agreement or an improvement survives being scored on
  someone else's stated criterion.
- `reasoning-gate/` — `G-CTRL` is `S3` ("was a no-sacrifice comparison
  case specified in advance?") as a precondition rather than an audit
  question; `G-PRE` is `S5`.
- `uninstrumented/` — §8 is SCALAR DEMAND on the drop's own headline
  number.
- `triad-playground/` / `reasoning-dial/` — §6 is `TP_006` and `RD_009`
  arriving in a third instrument.
- `null-harness/` — `option_gain` (§4) and `dominated_on_own_metric` (§5)
  are both readouts whose null branch is currently unreachable.
