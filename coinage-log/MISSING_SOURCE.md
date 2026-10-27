# MISSING_SOURCE -- manifest for the coinage-log STATUS split

**Source:** `/topics/coinage-log.md`, the operator's memory store. It is
outside this repository.

**Status:** RECEIVED 2026-10-11. Delivered sanitized, in 7 chunks, each
carrying a stated byte count and a sha256 prefix. Every chunk was checked
against both before assembly; all 7 passed.

**Path:** `source/coinage-log.full.md` -- the byte-exact concatenation of
the 7 chunk bodies in order. No header is added inside the file, so the
hash below is the hash of the delivered content; the repo-root LICENSE
covers it.

**Bytes:** 47474.

**sha256:** 4822118f1f8bac45667f4fa2652e0c4b18bf4f2f2376ff7adf46a749d28b6757

**Sanitized:** person stripped per originator's offsite rule, 16 logged
edits. The edit list was delivered beside the chunks and is not committed
here; the count is the originator's.

**Earlier estimate, superseded:** this file had carried an operator-stated
size of ~46.9k chars at an 8000-char export cap, giving a 6-chunk
estimate, all rows MISSING_SOURCE. The delivery came as 7 chunks of 6453
to 7512 bytes and the measured size is 47474 bytes. The 6-row table is
replaced by the delivered split below. The sha256[:16] column is the
prefix stated on each chunk's START line; `check_coinage.py` recomputes it
from the landed file at the cumulative byte offsets.

| chunk | bytes | sha256[:16]      | status   | received |
|------:|------:|------------------|----------|---------:|
|     1 |  6534 | fe8e0afeca7afc96 | RECEIVED |     6534 |
|     2 |  6592 | a25ac476882bd74c | RECEIVED |     6592 |
|     3 |  6457 | 38a971638e27b9e8 | RECEIVED |     6457 |
|     4 |  7113 | 97c668656a968896 | RECEIVED |     7113 |
|     5 |  7512 | 7445f208c70e1fe6 | RECEIVED |     7512 |
|     6 |  6813 | 4335592e78e0bc25 | RECEIVED |     6813 |
|     7 |  6453 | a9d51fb0347f0ad6 | RECEIVED |     6453 |

**Received:** 47474 of 47474 bytes.

## What is NOT done, deliberately

- No entry is reconstructed, summarized, expanded, rendered or
  restructured. `source/coinage-log.full.md` is the SOURCE, not an
  instrument; verbatim is the whole job.
- Entries are NOT moved into File A (`coinage-log.md`) or File B
  (`vocabulary-gap-slots.md`). That is a separate order. Both files are
  unchanged in this landing and still describe the unreceived state:
  their `sources` / `aliases` lines, File A's header slot and its
  `STATUS: MISSING_SOURCE for chunks 1..6` line are STALE as of
  2026-10-11. The source is at the path above.
- The counts those files mark UNKNOWN (coined terms, unnamed slots,
  failure points, status fields) are still not supplied here. They are
  countable from the source now; counting them is the split order's job.
- `[[link]]` targets in the source are carried as delivered and resolved
  by nothing here.
- The source carries non-ASCII characters (em dashes, CJK) as delivered.
  The ASCII convention applies to authored text, not to this file.

## What IS done

- **The source is landed**, verified per chunk (byte count and sha256
  prefix against each START line) and whole (47474 bytes, sha256 above).
- **This manifest is updated** to the delivered 7-chunk split.
- **`check_coinage.py` section 6** now pins the RECEIVED state: 7 rows,
  all RECEIVED; received total 47474 equal to the landed file's size; the
  file's sha256 equal to the one stated here; each row's sha256[:16]
  recomputed from the file at its byte offsets. The File A / File B
  checks are unchanged, since those files did not move.

## How this closes

Entries move whole into File A or File B under the split rule, from the
landed source, in a separate order. The seeded File B entry is then
compared against the source's version of the same referent, and the
UNKNOWN counts above are replaced by measured ones.

CC0.
