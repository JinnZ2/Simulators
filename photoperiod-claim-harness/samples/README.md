# samples

Pinned output.

| file | reproducible |
| --- | --- |
| `claims.sample.txt` | byte-identical on every run |
| `sweep_S2.sample.txt` | byte-identical on every run |
| `harness_audit.sample.txt` | byte-identical on every run |
| `run_all.sample.txt` | byte-identical on every run |

All four are reproducible. `run-all` was not, until the repair:
`hypothesis_block()` stamped `time.strftime("%Y-%m-%d %H:%M")` into its
header, one line above the `file hash:` it printed for provenance — so the
harness pinned the artifact and then stamped the wall clock into the
human-facing output, and two runs of the same file produced two different
documents.

It now prints a deterministic `run id` (file hash + claim statuses), which
moves when either does and not otherwise. The clock stays in the JSONL log,
where every record already carries one.
