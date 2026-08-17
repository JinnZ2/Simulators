# samples

Pinned output.

| file | reproducible |
| --- | --- |
| `claims.sample.txt` | byte-identical on every run |
| `sweep_S2.sample.txt` | byte-identical on every run |
| `harness_audit.sample.txt` | byte-identical on every run |
| `run_all.sample.txt` | **one line differs** — see below |

`hypothesis_block()` stamps `time.strftime("%Y-%m-%d %H:%M")` into its header,
so `run-all` is not byte-reproducible:

```
HYPOTHESIS BLOCK -- generated 2026-08-17 11:55
```

Every other line, including the file hash, is deterministic. Worth naming
because the same block carries `file hash:` one line down — the harness pins
the artifact and then stamps the wall clock into the human-facing output, so
two runs of the same file produce two different documents. A run identifier
derived from the file hash and the parameters would carry the same
information and diff cleanly.
