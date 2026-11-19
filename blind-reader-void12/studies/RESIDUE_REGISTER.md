# Residue register (sidecar): records kept on purpose that a tidy-minded reader might "fix"

Status: **DRAFT, 2026-11-19.** Requested by the owner (message of 2026-11-19, item 4) after the Grok reader's repository read proposed inline `INTENTIONAL_RESIDUE:` markers (`as_received/grok_repo_read_2026-11-19.md`, E3). The owner chose a sidecar file over inline markers: **no marker is written into a specimen or a hashed file.** Every row points at its file from outside it.

The `kind` vocabulary is `READ_ME_THIS_WAY.md` section 1: mis-bin, dead end, correction specimen, model-chosen name, workaround, duplicate. A row that fits none says `other:` and names the kind. A row records why the residue is kept and where that is stated. It does not judge the residue. Scope: `blind-reader-void12/` only; no other folder has been surveyed.

| id | path | kind | reason kept | source |
|---|---|---|---|---|
| RR01 | `KEY_V2_AMENDMENT_1.md` line 3 ("Status: proposed, on a branch, not merged.") | correction specimen | The file is hashed. The line is stale (amendment 1 is in force), and the correction sits outside the file. | `PREREG.md`, "Status note on amendment 1" |
| RR02 | `amendment_options/as_received/KEY_V2_AMENDMENT_1_r1.patch` | dead end | Superseded by amendment 1 (a1) and never adopted. Kept so the `decide/` re-run instruction can be followed. | `amendment_options/README.md` line 10 |
| RR03 | `amendment_options/as_received/KEY_V2_AMENDMENT_1.patch`, `KEY_V2_AMENDMENT_1_DRAFT.md` | dead end | Received drafts, replaced by the a1 text; nothing in them is adopted unless it appears in a1. | `KEY_V2_AMENDMENT_1.md` line 3 |
| RR04 | `readings/2026-11-19_kimi-v2-A/response.json`, `reader_label: "claude-fresh-1"` | other: label set by the task text | The task text's rule 4 set this label for every reader that round. It is not the reader's identity, and editing it would change a filed reading. | `readings/2026-11-19_kimi-v2-A/RUN_NOTES.md` line 51; `readings/WORK_ORDER_2026-11-19_as_received.md` |
| RR05 | `readings/2026-11-19_kimi-v2-A/RUN_NOTES.md`, the "Label" paragraph (line 7) | correction specimen | It guessed the label was a typo, which was wrong. Kept as written; a later section supersedes its last two sentences. | same file, line 51 |
| RR06 | `readings/2026-11-19_kimi-v2-A/followup_as_received.md`, three `￼` placeholders under the section headings | workaround | Tables lost in a phone copy-paste. The owner then sent the tables as text, filed below the placeholders. | the file's lines 2-8; owner's messages of 2026-11-19 |
| RR07 | `studies/as_received/gpt6_g01_g02_instrumentation.patch`, the names G01 / G02 | model-chosen name | The study names stay as chosen in the as-received file. In `studies/` they are M01 / M02 because G01 / G02 clashed with the same reader's gap inventory G01-G33. | `studies/GLOSSARY.md`, id families, last row |
| RR08 | `studies/confusion/2026-11-19_kimi_m01-m02.md`, the reader's own ids C01-C12 | duplicate | They collide with the same reader's earlier branch inventory C01-C15. Kept beside the filed ids KC01-KC13. | `studies/GLOSSARY.md`, row KC01-KC13 |
| RR09 | `studies/packets/grok_2026-11-19/` (packet v1) | correction specimen | Sent with defects P1-P6. Kept byte-reproducible, with the v2 draft beside it; the reader's rows refer to v1. | `studies/packets/grok_2026-11-19_v2/MANIFEST_PRIVATE.json`, `diff_from_v1`; `studies/confusion/2026-11-19_grok_m01-m02.md` |
| RR10 | `studies/confusion/2026-11-19_grok_m01-m02.md`, the owner's summary as quoted in the dated sections | correction specimen | The summary placed GR04, GR07 and GR09 differently from the filed rows. The correction is a dated section, and the summary is not rewritten. | that file's dated sections; `studies/GAPS.md`, dated note |

## Rules for adding a row

- One row per residue. The path names the exact file, and the line where one applies.
- `source` is where the reason is already stated. A reason stated only in this register gets `source: this register`, which marks it as unrecorded elsewhere.
- No row is removed. If a residue is later repaired by an owner decision, its row gains a dated note saying so.
