# Reading: GPT-6, packet v2 (2026-11-19)

**What this is.** A reading by a model of a third family (GPT), made after key v2 amendment 1 was merged (PR #318) and its hashes pinned in `PREREG.md`. Sent through the owner. Nothing in the key, scorer or packet was changed for or after it.

**Filed as received, with one caveat.** The owner pasted the JSON into a Claude Code chat (the Manus session had run out); that session wrote it to file. `raw_output.txt` and `response.json` are that transcription (sha256 `88cd9a447cc67bafb185f86eb7669d332f15890673b92afd79709d89be730c43`, 15,451 bytes), not the owner's paste byte for byte. If the owner still has the original, it should replace `raw_output.txt`; the scores do not depend on whitespace. `score.*` is under key v2, `score_a1.*` under key a1; both ran with exit 0 (validation passed).

**Packet variant: not stated.** The reader did not name the variant, and the owner's message did not either. The owner confirms A or B; the folder name carries no variant until then.

**Label.** The reader wrote `reader_label: "claude-fresh-1"` because the task told it to: the owner confirms (2026-11-19) that every reader on this round got the same task text, which is filed as received in `readings/WORK_ORDER_2026-11-19_as_received.md` (sha256 `cd766bc1321543a676aad20c882f4cb856555fe7b91b8ebf42e1733c4722037a`); its rule 4 says 'Set reader_label to "claude-fresh-1"'. That label is an earlier reading's and names another model family; it identifies nothing about this reader. Identity is `model_family`, `GPT-6`.

**Blindness (self-report, not checked).** q1 to q3 `unsure`, q4 `no`, q5 `no`, q6 `yes`. Status by the rule: `UNCERTAIN`; not counted toward confirming any pair. The reader says this was not a fresh no-memory conversation: prior-session context or memory was available, and it cannot establish whether that context held any of the material q1 to q3 ask about. Python execution was on and used only to inspect the zip and write the response; web search available, not used; no repositories connected.

## Results (from `score.txt` and `score_a1.txt`)

| | key v2 | key a1 |
|---|---|---|
| grouping, adjusted Rand index | 0.790 | 0.790 (grouping is not amended) |
| clusters, reader / key | 11 / 9 | 11 / 9 |
| `slots_specific`: declared pairs agreeing | 5 of 7 | 5 of 7 |
| `slots_specific`: slot sets equal | 9 of 14 | 8 of 14 |
| `slots_carried`: declared pairs agreeing | 5 of 7 | 5 of 7 |
| `slots_carried`: slot sets equal | 13 of 14 | 13 of 14 |

**Grouping.** Two of the key's joins are split, nothing is added: `UNDECIDED | UNRESOLVED` (T01, T06; each lists the other in `could_also_join`, confidence HIGH) and `HOLDS | CLOSED_WITHIN` (T11, T14). HOLDS is left on its own: not with CLOSED_WITHIN (key, Kimi), not with OK (both Claude v2-era readings). The two `DIFFER` pairs on each meaning are those two splits; the slot lists do not cause them.

**`slots_carried`.** 13 of 14 sets equal the key's; the only difference is T02 (`[]` against the key's `value`). This reader stopped at the term's own record everywhere, including T10, where it gives exactly the six coverage-entry keys (the key's list), unlike Claude-v2-A and Kimi, who both add `error` and `exception_type`.

**`slots_specific` under a1.** Narrower than the other two readers: T10 `[]` (subset), T12 `[typed, untyped]` (disjoint from the key's `[triggers]`: the reader says the parameter `triggers` "is not a returned field"), T01 `[]` (equal). Supersets where the other two readers also added: T05 `covers_effect`, T07 `void_reason`; T08 adds `inputs`.

## Across the three v2 readings (one each; observations, not findings)

```text
term  key a1 specific        Claude-v2-A           Kimi                  GPT-6
T05   5 params               + covers_effect       + covers_effect       + covers_effect
T07   []                     void_reason, +1       void_reason, +1       void_reason
T12   [triggers]             + typed, untyped      + typed, untyped      typed, untyped (no triggers)
T10   [missing_path, error]  + exception_type      + exception_type      []
T01   []                     5 names               2 names               []
T08   [exception, path]      + inputs, call        + inputs, exc         + inputs
```

- Three families add a name the a1 rule excludes on T05 (`covers_effect`), T07 (`void_reason`) and T12 (`typed`, `untyped`). Readers working from the brief do not apply the rule's INDEPENDENCE or every-instance tests. That is about the brief's wording and the definition of "slot", as `OPTIONS.md` 6.4 says; it is not a finding that the key or the readers are wrong.
- The grouping question that was open (HOLDS) now has three answers across readings: with OK (two Claude readings), with CLOSED_WITHIN (key, both v1 Claude pilots, Kimi), alone (GPT-6). T01 | T06 is split for the first time.
- On T10 `slots_carried`, two families add `error` and `exception_type` and one does not; the open carried question stays open.

## Limits

One reading per family, one run each; reader noise is not estimated. Status `UNCERTAIN`, so by PREREG rules 1 and 2 this reading confirms and contests nothing; it is filed and scored. The Clopper-Pearson interval for 5 of 7 is 0.29 to 0.96.

## Addendum: the reader's follow-up (filed as received)

`followup_as_received.txt` (sha256 `555f70024b7571ce24c7a28557fd984a814046190c43d65c55b8d3bac3885076`, 6,761 bytes) is a note the GPT-6 session wrote after its reading, passed on by the owner: a gap inventory (sections 1 to 7, 9) and a record of its own session (section 8). Transcribed from the owner's paste in a Claude Code session; characters kept as pasted, tab layout as rendered.

**What section 8 reports about the session, beside what the attestation says.** Recorded side by side; nothing is reconciled and the status is not changed.

```text
item                          response.json attestation / notes          follow-up, section 8
----------------------------  -----------------------------------------  -----------------------------------------
memory                        available (q6 yes)                         available
project context               "cannot be established" (q1-q3 unsure)     "project-related prior context was available"
repository                    "connected repositories were not           "the user supplied the repository URL";
                              connected or used"                         "repository context was subsequently supplied"
tools                         Python on, used to inspect the zip         container used to read the zip and READER_BRIEF.md;
                                                                         "code/tool isolation was not established"
packet read before output?    -                                          "initially returned a file link without
                                                                         establishing that the packet had been read";
                                                                         later acknowledged
classification                -                                          "cannot be classified as a fresh,
                                                                         memory-free reading experiment"
```

**Not known from either text** (recorded as unknown, not as absent): whether the repository URL was supplied before or after `response.json` was produced; whether the repository was opened; whether the file-link response came before the JSON that is filed here.

**Effect on the filing.** None on the scores. Status stays `UNCERTAIN` by the rule, which reads q1 to q4 as answered. The follow-up strengthens the reason for that status: a repository URL in the session and project-related prior context are exactly what the blindness questions ask about. The v2 key, packet and scorer are public in that repository, so any later GPT-family reading should be taken in a session with no URL supplied, as the owner advised for the Claude readings.

## The task this reader received

`readings/WORK_ORDER_2026-11-19_as_received.md` (sha256 `cd766bc1321543a676aad20c882f4cb856555fe7b91b8ebf42e1733c4722037a`): the owner's text, sent to every reader on this round (owner, 2026-11-19). It is a condition of the reading, like the packet. It differs from the task the Claude-v2-A reader received (recorded in that session's transcript, not filed here): that one set `reader_label` to "Claude-v2-A", named "no project instruction files" and "attached repositories", and added a rule on field names. Readings taken under different task texts are scored the same way; the difference is recorded, not corrected for.

**For the next task text** (a suggestion, the owner's to adopt or not): an unused, neutral `reader_label` (or none), so the label cannot be read as an identity or a hint; and "no repository URL" beside "no connected repositories", since this reader's follow-up reports a repository URL in its session.
