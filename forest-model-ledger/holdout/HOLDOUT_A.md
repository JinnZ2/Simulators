# Holdout, Phase A: fetch, split, seal

CC0. Data and record only. No model run, no branch, no scoring.

Status: Phase A DONE (fetch, inspect, cutoff, seal). Phase B NOT STARTED.
Co-authored, Kavik + Claude, work order of 2026-11-22. Run date (UTC):
2026-11-22. Observer slots: null.

Tags: OBSERVED = seen in this run (bytes fetched, values computed from
them); DERIVED = follows from what is stated here; PROPOSED = untested;
[co-authored] = stated in the work order, carried as stated; "chosen, no
external source" = a constant picked in the order, not taken from any
reference; NOT RECORDED = nobody in this run looked or it was not given.

Method reference, cited by hash and not copied:
`tools/density_vs_closure_sampling.md`, sha256
`40e5a753e4a9b142919bac9e987e430745200588d50b620f67c9ab355f85da45`
(Simulators PR #329, unmerged when this record was written; the file is
not on this branch).

## 1. Fetch

[OBSERVED] First attempt, 2026-11-22T18:53:06Z: zenodo.org, datadryad.org
and doi.org were all refused by the session's egress proxy (CONNECT 403).
Nothing was written. The owner asked for the three hosts to be allowed;
they were added to the environment's allowed hosts and the fetch was
re-run. Zenodo answered, so the Dryad fallback was not called.

    URL as called   https://zenodo.org/api/records/10403125/files/PSF.data.EL.open.csv/content
    UTC             2026-11-22T18:55:31Z
    HTTP            200
    file name       PSF.data.EL.open.csv
    size            1609518 bytes
    sha256          bb56ba5ac31b13be09cf3df42c1215b53255bb1eb3bb8a91838ab8cb4cb5c82c
    md5             7a0a9088362d3bf7065f1240838c3c7f  (equals the md5 Zenodo lists)

Record metadata, read from https://zenodo.org/api/records/10403125 at
2026-11-22T18:55:21Z [OBSERVED]:

    title              Dataset of global plant-soil feedback
    publication date   2023-12-18
    doi on the record  10.5061/dryad.n2z34tn35
    license            cc-zero
    files              Open_code.R (32984 bytes, not fetched)
                       PSF.data.EL.open.csv (fetched)
                       README.md (1508 bytes, fetched; sha256
                       1aeac2d8f58027687422a1336aaa4b9ca6f82cc5c357f6e92fc50db52ad2484b)

The source file itself is not committed. Only the anchor rows are
(section 4).

## 2. Schema (read only)

[OBSERVED] Encoding UTF-8, no byte-order mark, CRLF line ends, one
record per line, 28 fields on every line. 6 lines carry non-ASCII
bytes, all in the `Author` field.

    rows      5969   (order expected ~5969)
    studies    202   (order expected ~202)
    columns     28

    N  Author  Year  Species  Genus  Family  F.H  Life.form  Sp.origin
    Approach  Response  Phase1.m.ori  Phase1.m  Phase1.culti
    Experimental.setting  SoilTp  Phase2.grow  Phase2.time  Source  rr
    var  Latitude  Longitude  Latitude.abs  MAT  MAP  AI  group

`N` is in the file and is not described in the source README; its 5969
values are all distinct. What it denotes: NOT RECORDED.

How the two key fields were identified:

    study   = distinct value of `Author`. [OBSERVED] 202 distinct values,
              which matches the expected study count. The source README
              glosses the column as "Author and year". That a distinct
              `Author` string is one study is [DERIVED] from the count
              match; the file has no separate study id.
    year    = `Year`. The source README glosses it as "Year of paper".
              [OBSERVED] every value is a 4-digit integer, and every
              `Author` value maps to exactly one `Year` (0 conflicts),
              so the year is a property of the study and whole-study
              splitting is well defined.

[OBSERVED] One `Author` value does not contain its `Year` in the string:
"Kulmatiski, unpubl. Data", Year 2008. It is marked unpublished in the
source, so "publication year" does not strictly apply to it. It is kept
as the file gives it (2008, anchor side).

## 3. Year histogram, by study

[OBSERVED] Counted once per study. Rows shown beside for scale only.
"after" = studies with year greater than this row's year.

    year  studies   rows   after  after/202
    1994     1       12     201    0.995
    1999     1        4     200    0.990
    2001     2        6     198    0.980
    2002     2       62     196    0.970
    2003     2       10     194    0.960
    2004     8       57     186    0.921
    2005     5       39     181    0.896
    2006    10       59     171    0.847
    2007    10       51     161    0.797
    2008     6      410     155    0.767
    2009     1       16     154    0.762
    2010     7      135     147    0.728
    2011    10      140     137    0.678
    2012     7      104     130    0.644
    2013     9      208     121    0.599
    2014     7       37     114    0.564
    2015    13      214     101    0.500
    2016    16      439      85    0.421
    2017    14      917      71    0.351
    2018    24      787      47    0.233   <- Y
    2019    11      651      36    0.178
    2020    17      468      19    0.094
    2021    16     1079       3    0.015
    2022     3       64       0    0.000
    total  202     5969

Years 1995-1998 and 2000 have no study.

## 4. Cutoff and split

[co-authored] Rule: the latest year Y such that studies with year > Y
are at least 20% of all studies AND at least 30 studies. Both constants
(20%, 30) are chosen, no external source.

[OBSERVED] Y = 2018. After 2018: 47 studies, 47/202 = 0.233. The next
year fails the first condition: after 2019 there are 36 studies,
36/202 = 0.178.

Whole studies are split, never rows. No study has rows on both sides.

    side      years       studies   rows   file
    anchor    <= 2018       155     3707   anchor_studies.csv (committed, plain)
    holdout   >  2018        47     2262   not committed in plain form
    total                   202     5969

[DERIVED] The holdout is 23% of studies and 38% of rows (2262/5969):
late studies carry more rows each. Anything in Phase B that weights by
row will lean on the holdout side harder than the study share suggests.

`anchor_studies.csv`: the source header line, then the anchor rows in
source order, each line byte-for-byte as fetched (CRLF kept, the `N`
values kept, 4 lines with non-ASCII bytes in `Author`).

    size     1007858 bytes
    sha256   e2ea825c7bb1372dc2b9a2d1c46f1c2a14f78b466f0a7f382bacb0c129a29438

## 5. Seal

[OBSERVED] `holdout_commitment.json` holds the study count, the row
count, and one hash:

    sha256( nonce || holdout file bytes )
      = ce54a50ecc4eba87d9df5ce99db93eddcbf3c1f3243765481d21cb2340c76713

    nonce                32 random bytes, placed first. NOT committed.
                         Reported once to the owner, who holds it until
                         the Phase B reveal.
    holdout file bytes   the source header line, then every row with
                         Year > 2018 in source order, each line
                         byte-for-byte as fetched, every line ended by
                         CRLF including the last. 601888 bytes.

To check at reveal: fetch the source file (sha256 in section 1), keep
the header and the rows with Year > 2018 as above, prepend the 32 nonce
bytes, hash. The salt is there because an unsalted hash of a file that
anyone can rebuild from a public source can be guessed by rebuilding it.

What the seal does and does not do [DERIVED]:

    does       fix which bytes are the holdout before any branch exists;
               keep the holdout rows out of this tree
    does not   hide the holdout from anyone who fetches the public
               source and applies section 4. The source is public and
               Y is stated here. Secrecy rests on Phase B not reading
               the source file, which this record cannot enforce.

## 6. What has seen the holdout

- "Holdout validation can only confirm branches someone later
   reached; it cannot score true unavailability. (inherited weld 4)"
- "No branch, crowding probe or model run has seen the holdout."

[OBSERVED] What did read it: the fetch-and-split run that produced this
record read every row in order to split. Its inspection output listed up
to four arbitrary distinct values per column across the whole file,
without regard to side, and the per-year row counts in section 3. No
effect size (`rr`, `var`) was summarised, on either side.

[DERIVED] The Phase B explorer should therefore not be the session that
ran Phase A, or should be told nothing beyond this record and
`anchor_studies.csv`.

Whether run_9 or any earlier ledger run used studies from this dataset:
NOT RECORDED here. `ledger/data_sources.yaml` lists this source as
`not_retrieved` with `used_by: []`; that file was not edited by this
order.

Dated note 2026-11-22: superseded by the follow-up order on this PR
(commits 4bcca3a, 2c02eaa); data_sources.yaml now lists DS_JIANG_PSF
as retrieved. The text above is kept as true at Phase A time.

## Network state (2026-11-22)

zenodo.org, datadryad.org, doi.org were added to the environment's
allowed hosts for Phase A and remain allowed. Any later session can
fetch the full source including the holdout. Phase B must not call
these hosts; a call marks that run exposed and unscored.

## Provenance

Co-authored, Kavik + Claude, work order of 2026-11-22; the decisions on
source set, cutoff rule and staging are the order's and are carried as
stated. Everything tagged OBSERVED was computed in this run from the
fetched bytes whose hashes are in section 1. The dataset is Jiang et
al., "Dataset of global plant-soil feedback", Zenodo record 10403125
(doi:10.5061/dryad.n2z34tn35), licensed cc-zero on the record; the paper
that accompanies it was not read in this run. The method note is cited
by hash only. No row was reconstructed or synthesised.
