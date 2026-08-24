# study-watch — what the build turned up

`study_watch.py`, selftest PASS. Workflow at
`.github/workflows/study-watch.yml`. Suite at `tests/test_study_watch.py`,
81 tests green. Stage 1 has never executed from here.

## 1. CORRECTION — the earlier claim here was wrong

This section previously said all eight `uninstrumented.ENTRIES` WOULD MEASURE
strings return `UNDECIDABLE` **"because a WOULD MEASURE is a design and a
candidate is a claim — different grammatical kinds of thing"**.

Checked, after the operator asked what changing the noun to a verb would do:
**seven of eight carry a verb.** The `UNDECIDABLE` verdicts were mostly
extraction failures, not absent verbs:

| entry | verb present | why T1 returned UNDECIDABLE |
|---|---|---|
| 1 | `sets` | head extracted as `side`, from "each side" |
| 2 | `is` | head `correction`, not in the D3 table |
| 3 | `added` | head extracted as `one`, a pronoun |
| 4 | `name` (imperative) | no subject; imperatives have none by construction |
| 5 | `scored` | head `benchmark`, not in the D3 table |
| 6 | none | genuinely verbless — a list of probe ids |
| 7 | `sets` in the text | D0 rule 3 picked the wrong sentence entirely |
| 8 | `count` (imperative) | no subject; head extracted as `count` |

The right statement is narrower and more useful: **a WOULD MEASURE written as
an instruction is already in verb-first form.** `count caveats issued per
account type` IS the residue — verb leading, bearer dropped, operator
implied. Nothing needs transforming for those; they are recognised.

## 1a. What changing the noun to a verb buys, measured

`verbalize()` recognises an instruction and refuses everything else.

```
IMPERATIVE                1
IMPERATIVE_AFTER_MARKER   2
NOT_VERBALIZABLE         19
```

**3 of 22** watchable WOULD MEASURE strings across `ENTRIES` and `cases/`
are written as instructions: `ENTRIES[4]` (*name every input and disposal
path*), `ENTRIES[8]` (*count caveats issued per account type*), and
`016agreementasmode` (*hold the form and pressure of the correction
constant, vary only...*).

**Why the other nineteen are refused rather than transformed.** Fronting
them mechanically produced `seting tasks in its own modality`, `houring off`
and `being the product` — non-English or vacuous. A reader asked whether a
residue needs a bearer **cannot judge a residue that is not a sentence**, so
emitting one would put a malformed string in front of a reviewer and call it
a test. `verbalize()` returns `NOT_VERBALIZABLE` with the reason instead.

**So the repair is at the entry, not at the parser.** A WOULD MEASURE
written imperative is readable by this pipeline as written, and three
already are. That is a recommendation about how the field is authored — and
it is the repo's own verb-first stance (`substrate-emergence`'s verb-first
axes, `energy_english`, D6 itself) arriving in the register's own schema.

**What the reading buys is limited, and the limit is structural.** Every
verbalizable WOULD MEASURE reads `PROCESS`, because an instruction is
grammatical with no bearer supplied. That is a property of instructions, not
a discovery about these entries. At n=3 the match column does not
discriminate *between* entries, so the reading is reported with its route
attached and `matches_would_measure` stays `UNADJUDICATED` — a reviewer
still decides in the pull request.

## 1b. A defect fixed on the way: `_to_ing` had no doubling rule

`seting`, `runing`, `stoping`, `begining`, `occuring`, `refering`,
`planing`. All wrong, and all produced by
`nonidentity-census/t1_verb_first.py::_to_ing`, which is what builds the
residue a D6 judgement is made on.

Correctness, not polish: **a residue that is not English cannot be judged
for whether it needs a bearer**, so the defect silently degrades every
judgement made on a fronted irregular. Repaired with a monosyllable-CVC rule
plus a stated list for the stress-final polysyllables (`occur`, `begin`,
`admit`, ...), and sixteen known answers pinned in that module's selftest.

## 2. The null test builds, and its second arm is constructible on three nouns

Both arm constructions work and the STOP condition does not fire.

```
ARMS: assessable vs not, matched on head noun
  population  survives=ENTITY   does-not=NOT_ASSESSABLE
  allocation  survives=PROCESS  does-not=NOT_ASSESSABLE
  market      survives=PROCESS  does-not=NOT_ASSESSABLE
  arms matched on head noun: True    arms separate: True
```

The second construction — arms separating on the **reading** rather than on
assessability, still matched on head noun — is buildable for `market` and
**not** for `population` or `allocation`:

> Where T1 decides by word list, the head noun FIXES the reading. Holding the
> noun constant across arms holds the reading constant too, and the arms
> collapse.

So a reading-matched null test is constructible **only on the claim-level
nouns** — three, against a sixty-token table. That is `T1-1` arriving inside
the null test's own construction requirement, computed rather than argued.

## 3. Three entries are NOT WATCHABLE, and one of them for an interesting reason

```
024refusalfalsepositiverate   uninstrumented/cases/
attribution_and_tenure        uninstrumented/cases/
operators/D2                  notes/operators/
```

None was invented. Case `024`'s absence is the notable one: it has no WOULD
MEASURE **because it shipped one as a separate file**,
`uninstrumented/specs/SCOPED_REFUSAL.md` — the first case in the register to
do that (`UNI_164`). Linking the two here would be inventing the field, so
the case is listed unwatchable and the reason is recorded instead.

## 4. The metric guard refused this module twice, both times on the word

`assert_no_metric()` refuses a count, a percentage, a rate or trend word, a
per-interval figure. It fired twice during the build, both on legitimate
text:

1. **The run-file preamble.** The first draft said *"No count, rate or trend
   is emitted"* — refused on `rate`. The guard cannot tell a rate from the
   word for one, so the file declaring the constraint cannot state it in the
   constraint's own vocabulary. Reworded around it.
2. **A NIL RESULT line.** `ENTRIES[6]`'s query is *"practice rate during
   stable interval play"* — the entry's own term, not a computed rate.

The second refusal fixed the exemption boundary, which was previously
hand-waved as "table rows": **entry-derived query strings and retrieved
titles are data and are exempt; everything the module composes is checked.**
By line, not by section.

Left strict. Over-refusing a line this module authored is the cheap
direction, and an exemption list is the first thing a real rate would arrive
through. `tests/test_study_watch.py` pins the use/mention limit so it stays
recorded.

## 5. "Merges nothing" is a test, not a comment

The workflow's header says there is no `gh pr merge` and no `--auto`. A
naive substring check for those strings finds them **in the sentence
forbidding them** — the third use/mention catch in this folder's short
history. `tests/test_study_watch.py` strips comments before checking, so the
property is asserted against code rather than prose, along with: no standing
model approver, `gh pr create` present, and the null test ordered before the
live retrieval.

## 6. What has not run

Stage 1. Crossref, OpenAlex and arXiv are refused by the local egress gate,
which is the reason the action exists. `retrieve()` is written and has never
executed; it warns on stderr. **A first run on the runner is a first run of
untested code**, and the workflow gates it behind the selftest and the null
test for that reason.

No run file exists in `watch/`. The dry run in `samples/dry-run.md` shows the
shape with every source recorded as not queried.
