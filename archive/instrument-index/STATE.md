# instrument-index — state

Landed in progress. This file records what is here and what is not, so
the folder is not read as finished.

```
    INDEX-SPEC.md          DELIVERED, verbatim. The schema.
    build_index.py         RECONSTRUCTION, written against the spec
                           before the operator's generator arrived.
                           SUPERSEDED — see below. Not yet replaced.
    coverage.py            consuming side. Imports the reconstruction's
                           surface (read_tsv, INPUT_SHAPES, UNRATED,
                           NOT_SCANNED, BuildRefused).
    index-overrides.json   ~164 rows. One file at the index root, keyed
                           "<repo>/<path>".
    INSTRUMENT-INDEX.tsv   built from the reconstruction.
```

## Superseded, not yet landed

The operator delivered `build_index.py` in two versions (v2 a superset
of v1, adding `--md`). Under the repo's delivered-verbatim convention
the delivered file takes the `build_index.py` name unedited, v1 lands
beside it, and the reconstruction is renamed to an audit-side module
that imports the delivered one. That has not been done.

Three consequences of landing it, recorded now so they are not
discovered as surprises:

```
    coverage.py breaks     the delivered module exposes read_header /
                           collect / axis_check and no BuildRefused,
                           NOT_SCANNED or read_tsv. Repoint, do not
                           patch the delivered file.

    overrides move         the delivered loader reads
                           "<repo-root>/index-overrides.json", keyed by
                           path relative to THAT root. The file here is
                           one file at the index root keyed
                           "<repo>/<path>". Relocate and rekey, or
                           record the mismatch.

    row count              the delivered generator walks per FILE. The
                           spec sizes for ~90 instruments under 40 KB.
```

## Findings standing against the current build

```
    SIZE    44692 bytes at 204 rows against the spec's <= 40960 at a
            ~90-row sizing basis. 219 bytes/row. Recorded, not tuned.
    AXIS    HELD. CLAIM-only share of rated rows 0.041 against a
            falsifier at > 0.70. 171 of 204 rows rated.
```

## Not done

- `claim_only_share` is not registered in `tools/known_answer.py`.
  `python3 tools/known_answer.py` currently raises a pre-existing
  `NameError` on `_drc_count_relation` at HEAD, unrelated to this work.
- No `test_index.py`.
- No `CLAIM_TABLE.md`, no `samples/`, no `CLAUDE.md` entry.
- No pointer files in `method-layer` or `chain-position-detectability`.
