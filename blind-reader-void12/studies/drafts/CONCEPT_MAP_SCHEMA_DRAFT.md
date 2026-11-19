# Draft: per-folder fields for `concept_map.json` (not merged)

Status: **DRAFT, 2026-11-19.** Nothing here is written into `concept_map.json`, `CONCEPT_MAP.md` or `check_concept_map.py`. Requested by the owner (message of 2026-11-19, item 3) after the Grok reader's repository read proposed a root `AI_ENTRY` manifest (`../as_received/grok_repo_read_2026-11-19.md`, E1). The owner asked for the fields to go into the existing map instead: "No new root manifest file."

## Where they would go

`concept_map.json` today has `as_of` and `rows`. Each row is a **concept** with several homes, not a folder. The new fields are per **folder**, so they cannot be row fields. The draft adds one top-level key beside `rows`:

```text
concept_map.json
  as_of      (existing)
  rows       (existing, unchanged)
  folders    (NEW)   { "<top-level folder name>": { the fields below } }
```

`check_concept_map.py` reads only `as_of`, `rows` and `conditions`, so an added `folders` key would not break it. It would not check the key either. A check would be a separate change.

## Fields

Unfilled = `null`, meaning not recorded. No field has a default.

| field | type | meaning | who fills it |
|---|---|---|---|
| `purpose` | string or null | one line | a reader of the folder (judgment) |
| `read_first` | list of paths, or null | files to read before the folder, in order (the root docs first) | a reader (judgment) |
| `deps` | `"stdlib"` or list of module names | non-stdlib imports | script (`folder_fields_draft.py`) |
| `claim_table` | `"yes"` / `"no"` / `"void"` | whether the folder carries a claim table | script for yes / no; `void` is the owner's to define (see below) |
| `refutation_protocol` | `"yes"` / `"no"` / null | whether the folder states one | script (a mention only) |
| `selftest` | `"yes"` / `"no"` / null | whether a `.py` file handles or refuses `--selftest` | script (a mention only; nothing run) |
| `first_file` | path or null | the file to open first | a reader (judgment) |
| `residue_register_ref` | path or null | the folder's residue register, if it has one | whoever writes the register |
| `provenance` | object | per field: `SCRIPT_DERIVED`, `CODER_INFERRED`, `READER_STATED` or null | set with each value |

## What the script fills, and its limits

`folder_fields_draft.py` writes `folder_fields.draft.json` (all 232 top-level folders). `--check` fails if a rebuild would change it. Each rule is stored in the output's `rules`. The limits:

- **`deps` mixes two kinds.** It lists third-party packages and also modules imported but defined nowhere in this tree. Examples: `numcheck` in the packet sources of `blind-reader-void12`; `preference_free_rank` in `crediting-rate`. The script cannot separate the two without a package list, and an import inside try/except still counts.
- **Three fields count mentions.** `claim_table`, `refutation_protocol` and `selftest` record that a token or filename is present. They do not show that a claim table is current, that the protocol is followed, or that a selftest passes.
- **`void` is not assigned.** The owner's list allows it, and no file defines it. Possible readings: a folder with no claims by design (an archive, a field guide), or a claim table declared not applicable. Unfilled until the owner defines it.
- **The draft's own folder is not scanned.** It names the tokens it counts, so scanning it would count itself; one run did, moving `refutation_protocol` from 95 to 96.

Counts on 2026-11-19 (script output):

```text
folders 232 | non-stdlib 24 | claim_table yes 139 | refutation_protocol yes 95 | selftest yes 152
```

**Later (2026-11-19).** The file committed at `3b963e7` was stale: `GROK_REPO_READ_CHECK.md` was written after the last run, and it quotes the token REFUTATION_PROTOCOL as evidence for F7, so `--check` would have failed on that commit. Re-run, the count is **96**: `blind-reader-void12` now reads `refutation_protocol: yes` because a check file names the token. The folder has no refutation protocol. This is the mention-only limit above, set off by this session's own audit text. The value is kept as the rule gives it, not overridden.

`purpose`, `read_first` and `first_file` are null for all 232. `residue_register_ref` is set for one folder (`blind-reader-void12`, CODER_INFERRED).

## Open for the owner

1. Adopt the `folders` key, or keep the fields in the draft file only.
2. The meaning of `claim_table: "void"`.
3. Who fills `purpose`, `read_first` and `first_file`, and whether a filled value needs a source line.
4. Whether `check_concept_map.py` should check the `folders` key (for example, that every folder exists and every path resolves).
