# label-position-test

A work order, delivered verbatim in `WORK_ORDER.md`: do valence labels
on a probing move (*cheat* | *innovation*) track the move, or the
actor's position and the outcome after the fact? One stdlib file
computes what the order's procedure asks for from a flat CSV in its
schema — Cramér's V by hand, a leak test, overlap against chance, the
within-document control — and nothing else.

**No data ships here.** The seed case is not reachable from the
environment this was built in, so the within-document control has
nothing to run on and the unfilled render says so. The rows under
`samples/` are constructed, carry a `constructed://` URL scheme, and
are counted apart from public rows in every render.

    python3 label-position-test/label_position_test.py                       # unfilled
    python3 label-position-test/label_position_test.py --csv ROWS.csv        # the numbers
    python3 label-position-test/label_position_test.py --csv ROWS.csv --relabel SHEET.json
    python3 label-position-test/selftest_lpt.py                              # the checks

| step | function | reads |
|---|---|---|
| P2 leak test | `leak_test` | in-sample (upper bound) and leave-one-out against the majority baseline; tuple space 72 cells |
| P4 cross-tabs | `cross_tabs` | V for `label_valence ×` position / move / outcome / actor; None where undefined |
| P5 overlap | `overlap_rates` | per label_source class, strict and half, against a chance computed from the class's marginals |
| seed control | `within_document_control` | URLs with ≥ 2 rows, actor and position held, move varying |
| P3 relabel | `relabel_agreement` | pairwise agreement and Fleiss' kappa by hand over a labeler sheet |
| OUTPUT | `output_table` | the order's row shape, one row per term plus ALL |

Three choices the order leaves open are marked `[CHOICE]` in the code
and printed on every render.

**The revision.** `WORK_ORDER_V2.md` adds one bullet, the N2 CONTROL —
the missing control from `zero-sum-curriculum-null/`, specified with
three measurables and filed in this order. `revision_audit.py` shows
the copy is a pure insertion with the changelog unmoved, that `N2` and
`the null` have no referent inside this order, that one of the three
measurables is exact on the sibling sheet and two are partial, and that
the bullet's *persists* outcome names the template where the null
construction's own table routes to N3. The verdict lines apply the order's own
FALSIFICATION rule to the computed numbers and print `undetermined`
where a number it needs is None.

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `WORK_ORDER_V2.md` | the revision, verbatim beside v1: one added bullet, the N2 CONTROL |
| `revision_audit.py` | v2 as a copy (pure insertion, changelog) and as a claim (referent, measurables, outcomes) |
| `label_position_test.py` | the instrument, one stdlib file |
| `selftest_lpt.py` | known answers first, both directions of every guard; writes the samples |
| `CLAIM_TABLE.md` | `LPT_001..LPT_014` |
| `samples/` | constructed rows and relabel sheet, the pinned renders |

The instrument refuses `--selftest`. Renders screen clean through the
repo's `no_severity` with no exemption. No author section. Stdlib
only, parses under 3.9, runs on a phone, CC0.
