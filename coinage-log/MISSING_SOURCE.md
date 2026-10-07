# MISSING_SOURCE -- manifest for the coinage-log STATUS split

**Source:** `/topics/coinage-log.md`, the operator's memory store. It is
outside this repository and unreachable from this session.

**Size:** ~46.9k chars. The operator stated this figure; it was not
measured here.

**Export cap:** 8000 chars per read (operator-stated). That puts the
source at 6 chunks: ceil(46.9k / 8000) = 6, the same for any value
from 40,001 to 48,000.

**Route:** the chunk route is unavailable (operator, 2026-10-07). Chunk 1
was not provided.

| chunk | char range (approx) | status         | sha256 | received |
|------:|---------------------|----------------|--------|---------:|
|     1 | 0 -- 8000           | MISSING_SOURCE | --     |        0 |
|     2 | 8000 -- 16000       | MISSING_SOURCE | --     |        0 |
|     3 | 16000 -- 24000      | MISSING_SOURCE | --     |        0 |
|     4 | 24000 -- 32000      | MISSING_SOURCE | --     |        0 |
|     5 | 32000 -- 40000      | MISSING_SOURCE | --     |        0 |
|     6 | 40000 -- ~46900     | MISSING_SOURCE | --     |        0 |

**Received:** 0 of ~46.9k chars.

## What is NOT done, deliberately

- No entry is reconstructed, summarized or inferred from memory, from
  the split order's description of the file, or from the in-repo render.
- The memory file's content is unknown, so these are all UNKNOWN, not 0:
  - the count of coined terms (File A);
  - the count of unnamed slots (File B);
  - the count of failure points (File B);
  - the count of status fields (File B).
- `[[link]]` preservation is NOT_EVALUABLE. The received text holds 0
  links because there is no received text. The seed contains none.
- Frontmatter `aliases` are MISSING_SOURCE in both files.

## What IS done

- **The split pair exists.** It has frontmatter, a pointer from each
  file to the other, and the header slot in File A.
- **One entry is seeded into File B** from the in-repo render
  `COINAGE_LOG.md`, which is a different artifact from chunk 1:
  - its provenance is stated in File B's `sources`;
  - `check_coinage.py` asserts it is byte-identical to the render.
- **`check_coinage.py` reads the split.** It asserts:
  - this table still shows 6 chunks, all MISSING_SOURCE;
  - 0 chars received;
  - File A carries 0 entries;
  - File B carries exactly the one seeded entry.
  When a chunk arrives, those checks fail on purpose and must be updated
  with it.

## How this closes

Paste or attach each chunk with its char count and a sha256. Entries move
whole into File A or File B under the split rule. Each received chunk's
row flips to RECEIVED and gets its hash. The seeded entry is then
compared against the source's version of the same referent.

CC0.
