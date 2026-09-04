# claim-refusal-gap

A delivered gap document (`GAP.md`, verbatim): claim refusal in
insurance adjudication is measured only where it is contested. Seven
gaps, five experiment designs, a standing shape. `gap_audit.py` reads
it as a structure and computes what its prose asserts from the figures
it carries.

    python3 claim-refusal-gap/gap_audit.py
    python3 claim-refusal-gap/selftest_crg.py

What comes out:

- **The anchor's +10 is a band.** The baseline carries a tilde; read as
  ±2 the held-constant residual is +4..+16. Direction holds, magnitude
  is what the tilde carries.
- **G-2 is one number for two causes**, shown as arithmetic: the
  displacement world and the non-purchase world are the same pair.
- **G-3's seam is 1.45** and decides whether 2023 is a record.
- **G-4's netted move is bounded in [2, 10].**
- **G-5's ~100x is 1/appeal_rate exactly**, and the unappealed rate is
  None until E-1 runs. The document's "no benign reading" has a second
  reading — the review standard moved — and E-1's blind reviewers are
  what separate them.
- **G-6's 0/0 is None**, not zero.
- **Two gaps have no design**; G-6 says why and G-7 does not.
- **Against the register's eight mechanisms** two fit, two partially,
  three none; G-2 is category-weld's ninth.

| file | what |
|---|---|
| `GAP.md` | delivered verbatim |
| `gap_audit.py` | the document as a structure |
| `selftest_crg.py` | known answers first, both directions |
| `CLAIM_TABLE.md` | `CRG_001..CRG_010` |
| `samples/gap_audit.sample.txt` | the pinned render |

One declared screen exemption (`error`, inside the delivered G-5 title
rendered from the parse), measured with the three-arm harness. Every
figure is carried and unchecked. Stdlib only, parses under 3.9, CC0.
