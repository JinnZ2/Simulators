# zero-sum-curriculum-null

A delivered null construction (`NULL_CONSTRUCTION.md`, verbatim,
including its trailing `g4`): five conditions under which a zero-sum
curriculum could NOT have affected the incident's outcomes, each with
requires / test / status, and a RESULT. `null_construction.py` parses
the delivered text and computes what its prose asserts.

    python3 zero-sum-curriculum-null/null_construction.py
    python3 zero-sum-curriculum-null/selftest_nc.py

What comes out:

- **The header and the RESULT use different logic.** *"Each is a
  requirement"* is a conjunction and empties the set at N1; *"survives
  on the two branches"* is a disjunction and gives {N2, N4}. N1
  (absent) and N2 (present) cannot both hold, so only the second reading
  is coherent.
- **The branches lean on N3.** N2 and N5 each leave the behaviour to be
  accounted for without the curriculum, which is N3's job. With those
  edges applied the null survives on N4 alone; N2 carries only if N3's
  residual closes.
- **N2's control is buildable now** in `hf-incident-extract`'s schema
  (imported, not copied): two arms, every cell UNMEASURED, `None`
  propagating. Its outcome table shows neither result carries the null
  by itself.
- **N5's named artifacts are absent** from this tree by content, and
  the sibling records the transcripts N5 reads as `NOT_RELEASED`. The
  repo's own index entry for this folder then carried the names and
  tripped the check; hits are now split into an index column and an
  independent column, and absence is read on the second (`ZSN_008`).

| file | what |
|---|---|
| `NULL_CONSTRUCTION.md` | delivered verbatim |
| `null_construction.py` | parse + logic + the N2 arms |
| `selftest_nc.py` | both directions of every result |
| `CLAIM_TABLE.md` | `ZSN_001..ZSN_008` |
| `samples/render.sample.txt` | the pinned render |

Nothing here holds a value from the report, the transcripts, or any
corpus. The module refuses `--selftest`. Render screens clean through
the repo's `no_severity` with no exemption. Stdlib only, parses under
3.9, CC0.
