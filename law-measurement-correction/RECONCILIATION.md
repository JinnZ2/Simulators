# RECONCILIATION — two passes of one dispatch

The 2026-10-03 dispatch was run twice, by two Claude Code sessions that did
not coordinate. Found at push time, when this branch name already existed on
the remote:

    pass 1  folder law-as-unvalidated-measurement/   commit 60152f7
            branch claude/law-measurement-correction  2026-10-04T02:17Z
            HAD the report zip (sha256 recorded) and the ledger rows
            (delivered in chat 2026-10-02)
    pass 2  folder law-measurement-correction/        this folder
            branch claude/law-measurement-correction-xcheck
            had NEITHER: the dispatch text only

Pass 2 did not overwrite pass 1. Both folders now carry a copy of sections
A-G, which is two authorities for one notice. Which folder merges is the
repository owner's decision; nothing here makes it.

Neither pass edits the other. No row in pass 2's records was changed after
pass 1 was read: `VERIFICATION_2026-10-04.md` stands as run, and this file
records the differences beside it.

## CC-3, row by row

| item | pass 1 | pass 2 | re-query from pass 2 after reading pass 1 |
|---|---|---|---|
| CJEU Alsen C-137/23 | VERIFIED | VERIFIED | agree |
| OR-Bench Hard-1K 39.8% illegal | VERIFIED | NOT_FOUND | reproduces: the query `OR-Bench-Hard-1K category breakdown "39.8%" illegal arxiv 2405.20947` returns "the 'illegal' category comprises 39.8% of the dataset" (arXiv 2405.20947). Pass 2's NOT_FOUND was bounded by its queries. |
| Claude-2.1 73.7% | CONTRADICTED (the ~73% is Claude-2.1's overall OR-Bench-80K rate, not a class rate) | NOT_FOUND | not re-run; pass 1 had the report's sentence, which is what decides whether 73.7% was claimed as a class rate. Pass 2 could not read it. |
| XSTest model size | CONTRADICTED | CONTRADICTED | agree |
| RegData 1,126,959 / +175.2% | NOT_FOUND (2025 total); VERIFIED 1970 base 409,520; arithmetic 1,126,959 / 409,520 = 2.752 | NOT_FOUND | agree on the total |
| OECD "9 of 38 reach 2/4" | VERIFIED (Government at a Glance 2025, ex post evaluation page) | NOT_FOUND | reproduces: "Only 9 out of the 38 countries with data available, and the EU, achieved a score of 2 or more." Pass 2 searched the Regulatory Policy Outlook 2025, the wrong publication. Its NOT_FOUND was bounded by its queries. |
| IRS publishes no aggregate dye-enforcement stats | NOT_FOUND (queries aimed at the IRS Data Book and IRM) | CONTRADICTED | reproduces from pass 2: the exact-phrase query `"120,000 fuel inspections" IRS dyed diesel "$4.6 million" penalties` returns the 2005-04-14 Senate Finance statement of Kevin M. Brown (https://www.finance.senate.gov/imo/media/doc/kbtest041405.pdf): "During FY 2004, the IRS Fuel Compliance Officers conducted more than 120,000 fuel inspections and assessed over $4.6 million in penalties for misuse of dyed diesel fuel." Pass 1's NOT_FOUND was bounded by its queries. A second, broader query from pass 2 did not surface the sentence. |
| DEA "no longer fits Schedule I" | VERIFIED (post-hearing brief, Aug 2026) | VERIFIED | agree |

Agreement on 4 of 8 rows. Every one of the 4 disagreements is a NOT_FOUND on
one side and a located source on the other, and in the 3 that pass 2 could
re-run, the located source reproduces. All rows on both sides rest on the
search index; both passes record the egress gate refusing every primary host.

## CC-4

    column A   both SETTLED to the same value and unit. Pass 1 adds 11.13 mg/L
               and a mass-ppm conversion, and reads the ledger's own figures
               against the settled unit.
    column B   both NOT_EVALUABLE. Pass 1 read the ledger row ("~12,000 ag
               sites") and lists order-of-magnitude candidates; pass 2 had no
               row and lists candidates without magnitudes.
    E / F      pass 1 split them from the rows; pass 2 NOT_EVALUABLE for want
               of the rows.

## CC-2 and CC-5

    CC-2       both record why-recovery and split-ledger / parks as
               NAMED-AND-ABSENT. Pass 1 also records the two memory notes and
               RECOVER-THE-LAW.
    CC-5       both write a design note with the same measurand, arms and
               coding cells, and neither builds a harness.

## What this pair shows, stated flat

At search-index depth a NOT_FOUND is a property of the queries, not of the
source. Two passes with the same search tool and no shared queries disagreed
on half the rows, always as found against not-found. Neither pass recorded
its queries' coverage in a form that would have told a reader which of its
NOT_FOUND rows were weak.
