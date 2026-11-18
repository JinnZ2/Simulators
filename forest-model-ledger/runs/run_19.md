# run_19 -- support_match on blind cases (chat-side follow-up to PR #258, item 2)

```text
status     : COMPLETE -- no trigger fired that a missing tool would answer; the question was asked of a gated tool
code       : runs/run_19.py
seed       : none; the cases are fixed text
params     : support_match as frozen at 72244bf (HELDOUT_FREEZE.md); cases/support_blind.json sha256 c4429199...
results    : (a) blind claim records: detector fires on 0 of 3 cases (run_16, this session's records: 3 of 3)
             (b) 40 blind-labelled lines: natural recall 0.250 precision 1.000; no-second-person recall 0.000 precision --
flags      : 5 (below)
provenance : DERIVED from a separate agent's records and labels (blind: excerpts, three neutral statements and the
             schema only; no repository, no tool code, no expected verdicts) against the sha-pinned texts
feeds      : support_match ; CC_005_open_slot_filled_first_hand
l0_closure : not applicable -- no model run
```

run_16's results stay labelled: build-confirming, author-contaminated.

## (a) same tool, same texts, two coders

```text
case  blind coder       run_16 (this session)   what differs
a     MATCHES *         CONTRADICTS             blind support 434, 438 ("the common denominator ... is physics", DeepSeek's
                                                own voice); run_16 support 436 ("Your physics point"). * blind record
                                                refused by validate: 434 and 438 are not the record's own locators
b     UNDETERMINED      SILENT_ON_CLAIM         blind terms "Hex token", "hardware bus drop"; 1313 names the hex token,
                                                so the item is named and the speaker (Gemini) is not INSTRUMENT
c1    UNDETERMINED      NO_SUPPORT_CITED        blind support 1256, 1257 (the record's reading of the quote); run_16 none
```

## (b) 40 labelled credit lines (detector = CONTRADICTS, positive = CREDITS_OTHER)

```text
group             tp  fp  fn  tn   recall  precision   verdicts
natural            2   0   6  12   0.250   1.000       MATCHES 18, CONTRADICTS 2
no_second_person   0   0   8  12   0.000   --          MATCHES 20
```

## Flags

```text
1  The verdict is a function of which line the coder calls the basis. On case a both coders read
   the same turn; one picked the line where DeepSeek states the item, the other the line where
   DeepSeek credits it to its addressee. The tool scored each correctly for its input.
2  Third-person credit ("the anchor idea was Wren's", "Rook originated the ledger scheme") reads
   MATCHES, not missed-and-silent: MATCHES is the verdict that reads as support. 14 of 16
   CREDITS_OTHER lines got it. This is wider than the stated cannot_see (addressee credit
   without a listed word): credit to a named third party is outside SECOND_PERSON entirely.
3  The held-out gate (tests/test_heldout.py) passed: its sets were written by this session and
   use second-person phrasings. Blind recall is the number that measures the tool's reach; the
   held-out pass measures that the frozen word list behaves as built.
4  The blind coder flagged on its own (note fields) that DeepSeek's turn presents the physics
   point as received (425, 436). That is the CONTRADICTS reading, reached by a reader the tool
   did not see, and not entered by it as a support locator.
5  Labels in (b) are the coder's; two NEITHER items carry ambiguity notes. Nobody checked the
   labels; they are the coder's reading, not ground truth.
```
