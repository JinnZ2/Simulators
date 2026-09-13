# demo -- two entries that do not validate

Order section 8: *"Ship a `demo/` with two entries that FAIL validate --
one tripping V4, one tripping V2 -- and assert nonzero exit. A demo that
only passes proves nothing."*

Both entries in `fails.jsonl` are CONSTRUCTED. The practice, the intake
form, the appointment record and the name in `GX-0001` are authored for
this file and are not a record of anything. They are ids `GX-`, not
`GR-`, so they cannot be read back as register entries.

```
python3 gap_register.py validate demo/fails.jsonl   # exits 1
python3 gap_register.py validate                    # exits 0
```

- `GX-0001` trips **V4** three ways in one field: an accusatory adverb, a
  construction that assigns purpose, and a name-shaped span outside
  `provenance[]`. It passes V1, V2, V3, V5 and V6, so the refusal is
  attributable to one rule.
- `GX-0002` trips **V2**: its closure condition is two modals and no
  observable noun. It passes the other five.

The two share one index vocabulary, which is what exercises the V5 PASS
branch -- the branch the shipped register does not reach.

`selftest_gr.py` runs `validate demo/fails.jsonl` as a subprocess and
asserts both the nonzero exit and that the set of refused checks is
exactly `{(GX-0001, V4), (GX-0002, V2)}`. A demo that failed for some
other reason would pass a bare nonzero-exit check.
