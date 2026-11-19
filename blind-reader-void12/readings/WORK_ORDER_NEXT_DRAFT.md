# Next task text: DRAFT, not sent, not adopted

Status: a draft for the owner. It takes effect only when the owner sends it to a reader; the text actually sent is then filed as received beside that reading, as `WORK_ORDER_2026-11-19_as_received.md` was. Changes from that task text, each from a filed finding:

```text
change                                                     from
---------------------------------------------------------  ---------------------------------------------------------
rule 4: a fresh neutral label, not "claude-fresh-1"         every reader on the 2026-11-19 round copied that label
setup: "no repository URL" beside "no connected repos"      the GPT-6 session had a repository URL (its follow-up)
a companion confusion inventory with every reading          Kimi's proposal (studies/as_received/), the template
```

---

You are being asked to do one reading task and return two things.

**Setup.** Use a new conversation with no memory, no project knowledge, no connected repositories and no repository link or URL, and web search and code tools off if you can turn them off. Attached are the files of a small packet: READER_BRIEF.md, terms.json, response_template.json, PACKET_MANIFEST.json, and a folder sources/ with eight source files. If your app cannot open a zip, use the unzipped files.

**Task.** Open READER_BRIEF.md and follow it exactly. It tells you how to group the 15 terms in terms.json, what to write for each, and how to fill response_template.json. Read the source files, not only the definitions.

**Rules.**
1. Work only from the packet. If you use anything else (including anything you recall about these projects), say so in attestation.notes.
2. Answer the six attestation questions honestly. "unsure" is an acceptable answer and is recorded as such. Do not answer "no" for something you cannot tell.
3. Nobody will tell you how many groups to expect, and you should not guess a number to aim for. If it seems to you that the packet implies one, say so in attestation.notes.
4. Set reader_label to "<NEW-NEUTRAL-LABEL>", model_family to the exact model name your app shows (or "unknown AI model"), and date_utc to today's UTC date.
5. If you are unsure of something, use the confidence field and say why; do not leave a field blank.

**Return.**
1. The completed response_template.json as a single JSON object.
2. After it, separately, a confusion inventory: one row for every point where you were unsure, guessed, stopped, or needed evidence not in the packet.

```text
id | term or passage | what was missing | what you did | source path | resolves with
```

- "What you did" is required: include every guess or interpretation, even if later evidence showed it was right.
- Leave a cell void when you do not know; do not omit the row. One row per point; do not merge.
- If you find no confusion, write "none found" and list everything you read.
- The inventory accompanies the response; it does not change the response or how it is scored.

In attestation.notes also say which tools were on, and whether memory or project knowledge was on.

## Later (2026-11-19): header form

The owner's message of 2026-11-19 (`studies/as_received/mode_and_authority_2026-11-19.md`, item 7) puts the mode, read set, exclusions and output contract at the top. The draft above is kept as written. Sent in header form, the next blind reading opens with the BLIND header in `studies/REQUEST_HEADERS.md`, filled for packet v2:

```text
MODE: BLIND (blind reading)
READ: only the attached packet: reader_packet_v2/ (variant A or B, as sent)
DO NOT USE: the repository, web, prior readings, keys, scores, or earlier sessions
SESSION: new conversation; memory off; no project knowledge; no connected repositories; no repository URL
CODE EXECUTION: not allowed (turn code tools off if the app allows)
RETURN:
1. The completed response_template.json, reader_label "<NEW-NEUTRAL-LABEL>".
2. A separate confusion inventory using the row format in Return item 2 above, with the reader attestation block at its head.
Record guesses even if you later believe they were correct. Do not merge rows. Use void for unknown cells.
If no confusion is found, say "none found" and list what you read.
```

The attestation block's wording for a packet is in `studies/packets/build_packet.py` (`ATTEST`), where the packet leak scan checks it. The pinned `reader_packet_v2/response_template.json` is not changed. The block goes in the confusion inventory, which the reader writes outside the template.
