# study-watch — what the build turned up

`study_watch.py`, selftest PASS. Workflow at
`.github/workflows/study-watch.yml`. Suite at `tests/test_study_watch.py`,
81 tests green. Stage 1 has never executed from here.

## 1. The match target and the candidates are different kinds of thing

**All eight `uninstrumented.ENTRIES` WOULD MEASURE strings return
`UNDECIDABLE` under the verb-first test.** Not most — all of them.

A WOULD MEASURE is a design: *"bidirectional protocol; each side sets tasks
in its own modality"*. A candidate is a claim with a main causal claim and a
subject. The verb-first test reads claims. Applied to a design it returns
nothing, by construction.

So `matches_would_measure` cannot be filled mechanically, and it is emitted
`UNADJUDICATED` on every row with the entry's WOULD MEASURE quoted beside it.
That is a `CONSTANT_SILENT` on the match column, established **before the
first run** — which is where a null test is supposed to catch things.

What stage 2 *can* decide is assessability: a candidate whose main claim has
no frontable verb or no extractable subject returns no reading and is
recorded `NOT_ASSESSABLE` with the reason. That is its only mechanical
reject, and it is a much smaller claim than "filters on predicate structure"
sounds.

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
