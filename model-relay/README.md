# model-relay

A running log of how different models use this repository's toolboxes:
which model produced each drop, whether it built on an earlier drop or
rebuilt it, and where its claims touch the outside world. A map, not a
score. CC0, stdlib only.

    python3 relay.py             # check RELAY_LOG.md, one state per row
    python3 relay.py --selftest  # prints its own check count

## Intake, same for every drop

```
drop arrives (zip / text / screenshot / voice note)
  1. land verbatim in its folder, hash it       (nothing edited)
  2. append a row to RELAY_LOG.md               (model, date, artifact, sha12)
  3. relay: did it call or extend an existing tool, or rebuild one?
  4. boundary: trace its outside claims; count what does not trace
  5. audit findings go in the folder's own claim table; the row names them
```

Rows are never edited. A correction is a new row whose `parent` is the
row it corrects.

## The map so far

```
 GPT  ->  Kimi  ->  Perplexity / DeepSeek  ->  Claude
 spec     extend    sort / find              audit, repair, log
```

| model | holds when | breaks when | gate before use |
|---|---|---|---|
| GPT | writing a spec or a minimal schema | describing an architecture it has not built (SAL_017); it does not see later drops | run it on a real case; check its tests probe content, not shape (SAL_016) |
| Kimi (OK Computer) | extending code it is handed (SAL_015) | stating outside facts: wrong document, future dates, unlocated papers (SAL_001..010) | trace every date, citation and figure |
| Perplexity | finding sources; blind grouping (DS_013 membership) | counting groups (DS_013 count) | open each link; read its group count as one grain |
| DeepSeek | repair-based sorting (DS_014) | not yet assessed here | |
| Claude | rerunning and recomputing | checking its own work (e.g. SAL_018, a dropped qualifier) | a second reader or an instrument it did not write |

Published figures on these families (research report, 2026-10-27, not
re-checked here; per the GPT spec's section 5 each stays source-reported
until inspected): the high fabrication figure is for Kimi Code (K2.5), not
OK Computer, and no independent audit of OK Computer exists.

## Not here

- No ranking of models. The counts at the end of `relay.py` are counts.
- Rows R005 and R006 carry `unrecorded` landing dates; the shallow clone
  did not have their history.
