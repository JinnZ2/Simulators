# Run notes: pilot-B (2026-11-18)

**Filed as a pilot, not as a counted reading.** Both pilots are fresh isolated sessions of an AI model whose family was not stated to the reader and is not known to us; it is presumed to be the same family as the first reading, so under rule 5 of `PREREG.md` it does not count toward confirming a pair.

| fact | value |
|---|---|
| brief | variant B: without the clause ", even if the second system attaches different extra fields or detail" |
| packet zip given | void12-reader-packet-B.zip, b19ec02c60c00409394743ce495190da8896b858e217e83453ec80223cf1e61c (sha256) |
| how it was run | isolated sandbox; the reader was told only to download the zip, read `READER_BRIEF.md`, follow it, work only from the packet, and return the filled JSON. It was not told what the packet is for, that a first reading exists, or how many groups to expect. |
| reader's own account of tools | file reading, shell (curl to download the zip, unzip, JSON check), file writing; no web search, page fetch or browser tool |
| raw output | `raw_output.txt`, 22934 bytes, sha256 `5a1bc4961a00481c056010b1177adfe145a5d23541ba492931a34f22292d6584`; `response.json` is the same bytes |
| validation | passed |
| blindness status by the PREREG rule | **BLIND** (q1 no, q2 no, q3 no, q4 no); q5 `yes` and q6 `no` |
| q5 `yes` | the reader says this is only because the reader label, date, model-name instruction and download URL came from outside the packet; it states none of that informed the grouping. Taken as stated; not checked. |
| declared pairs | 7 of 8 agree with the key (Clopper-Pearson 95%: 0.473 to 0.997) |
| all 105 term pairs | both join 6, reader only 0, key only 0; adjusted Rand index 1.0; 9 groups against the key's 9 |
| slots | 3 of 15 slot sets equal the key's (see `../README.md`) |

## The one declared pair that differs

`GAP_INSTRUMENT_CRASH | CRASHED` (T10 and T08): the key says MAPS, this reader says PARTIAL. **The grouping is the same**: the reader put both terms in one group and gave both the same predicate in its own words ("an attempted check raised an exception instead of delivering a measurement, recorded as missing coverage, not severity"). The tier differs only because the slot lists differ.

- T10 (TAF): key and reader agree: `kind, module, input, reason, missing_path, expiry_condition`.
- T08 (cplay `CRASHED`): key lists only the six `CoverageEntry` fields (`kind, module, input, reason, missing_path, expiry_condition`). The reader lists those six plus the seven fields of the `Reading` record that `crash()` also returns (`field, status, sigma, basis, exception, path, bound`), because the source shows both records are produced (`axes.py` 41-88, spec lines 41-55 and 335-343, as cited in its `source_lines_read`).

Both are readings of what "the term's slots" means. The key's MAPS holds only if the `CoverageEntry` alone counts.

The reader's full text is in `response.json`; the scorer's report is in `score.txt` and `score.json`.
