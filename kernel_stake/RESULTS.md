# RESULTS -- kernel subsystem stake split

Pre-registration: `4147046ea67300a37129f40e09c4eb2860678932`
(committed and pushed before any measure was computed).

**All three testable predictions are REFUTED, in the same direction.**
A null result is a result; nothing in PREREGISTRATION.md has been
revised to accommodate this.

| prediction (Corbet's claim) | registered | measured | verdict |
|---|---|---|---|
| M1 SHARED_CORE **lower** | lower | **higher, 2x-8x, every interval** | REFUTED |
| M2 SHARED_CORE lower | lower | -- | NOT TESTABLE |
| M3 SHARED_CORE **lower** maintainers | lower | **higher, every tag** | REFUTED |
| M4 SHARED_CORE worse latency | worse | -- | NOT TESTABLE |
| M6 SHARED_CORE **worse** concentration | worse | **no separation** | REFUTED (null) |

The maturity confound runs AGAINST the refutation rather than for it:
SHARED_CORE is the OLDER class (17.4y median path age vs 11.4y), and
older code should change less per KLOC, not more.  See the caveat on
path age below -- the true gap is wider still.

==========================================================================
M1  commits per KLOC  (median across subsystems in class)
==========================================================================
interval           STAKE      CORE     MIXED
v4.14..v4.19       2.879     6.677     4.921
v4.19..v5.4        3.212      7.05     3.948
v5.4..v5.10        1.939     6.613     5.575
v5.10..v5.15       1.389      5.58     3.381
v5.15..v6.1        1.505     5.908     4.754
v6.1..v6.6           1.0     5.059     2.916
v6.6..v6.12        0.761     6.101      4.41

==========================================================================
M6  bus factor  (median top-1 share / top-3 share, individuals)
==========================================================================
interval                     STAKE                CORE               MIXED
v4.14..v4.19         0.258 / 0.508       0.221 / 0.413       0.229 / 0.429
v4.19..v5.4          0.142 / 0.372       0.144 / 0.398       0.233 / 0.486
v5.4..v5.10          0.204 / 0.429       0.215 / 0.415       0.194 / 0.443
v5.10..v5.15          0.165 / 0.37        0.25 / 0.447       0.213 / 0.462
v5.15..v6.1          0.181 / 0.333       0.167 / 0.333       0.224 / 0.473
v6.1..v6.6            0.19 / 0.422       0.202 / 0.411       0.263 / 0.542
v6.6..v6.12          0.218 / 0.434       0.269 / 0.469       0.285 / 0.537

==========================================================================
M3  maintainer count (median) / tenure years (median of medians)
==========================================================================
tag                    STAKE                CORE               MIXED
v4.14               3 / 4.67        5.5 / 10.595            4 / 5.82
v4.19               4 / 6.34        6.0 / 11.015            4 / 6.72
v5.4               4 / 6.845        7.5 / 10.725            4 / 8.12
v5.10               4 / 7.06        8.0 / 11.465            4 / 9.17
v5.15               4 / 7.94         8.0 / 11.65            4 / 9.75
v6.1                6 / 8.91        9.0 / 10.115            4 / 10.0
v6.6                6 / 9.44         9.0 / 11.44           5 / 10.49
v6.12              7 / 10.85        10.5 / 11.57           5 / 11.54

==========================================================================
CONFOUND  path age in years at v6.12 (median)
==========================================================================
  STAKE_SPECIFIC     11.4 y   (n=15)
  SHARED_CORE        17.4 y   (n=12)
  MIXED/UNCLEAR      18.1 y   (n=9)

==========================================================================
UNKNOWN / NOT_RUN share
==========================================================================
  M1 undefined (no lines)      0 / 252
  M2 organizations             288 / 288   UNKNOWN (no employer map)
  M3 tenure unresolvable       1 / 288 cells; 37 maintainer-slots
  M4 review latency            252 / 252   NOT_RUN (lore unreachable)
  M5 volunteer share           288 / 288   NOT_RUN (no employer map)
  M6 no commits in interval    2 / 252
  M6 organization-level        252 / 252   BLOCKED

SCOPE LIMITS (printed with every result)
  author email is not who directed the work
  volunteer share is self-declared -- and is NOT_RUN here
  one project; nothing generalises
  activity, not code quality
  the 36-subsystem list is a convenience sample, not a random draw
  M2 UNKNOWN, M4 NOT_RUN, M5 NOT_RUN, M6-org BLOCKED (no employer map)
  classifier disagreement is 0.50-0.53; class membership is unstable

## Robustness -- both checks ADDED, neither is in the order

R-0  as pre-registered: classifier A, KLOC denominator
interval           STAKE      CORE     MIXED
v4.14..v4.19       2.879     6.677     4.921
v4.19..v5.4        3.212      7.05     3.948
v5.4..v5.10        1.939     6.613     5.575
v5.10..v5.15       1.389      5.58     3.381
v5.15..v6.1        1.505     5.908     4.754
v6.1..v6.6           1.0     5.059     2.916
v6.6..v6.12        0.761     6.101      4.41
  unit: commits per 1000 lines
  intervals where STAKE >= CORE: 0 of 7

R-A  classifier A, FILES denominator (generated-header check)
interval           STAKE      CORE     MIXED
v4.14..v4.19    4015.213  4697.479  3953.488
v4.19..v5.4       3500.0  5427.261  3909.091
v5.4..v5.10     2737.192  5715.054  3884.058
v5.10..v5.15    2459.459  4215.625  2772.059
v5.15..v6.1     2628.399  5690.731    4000.0
v6.1..v6.6      1439.945  4282.051  2297.101
v6.6..v6.12     1062.016  5483.333  4036.232
  unit: commits per 1000 files
  intervals where STAKE >= CORE: 0 of 7

R-B  classifier B (repaired/core_first), KLOC denominator
interval           STAKE      CORE     MIXED
v4.14..v4.19       4.931     4.959     4.229
v4.19..v5.4        5.069     6.053     6.527
v5.4..v5.10        5.006     5.032      5.74
v5.10..v5.15       2.843     4.044     3.335
v5.15..v6.1        2.769     3.687     4.234
v6.1..v6.6          1.82     3.072     3.787
v6.6..v6.12        3.614      4.31     3.221
  unit: commits per 1000 lines
  intervals where STAKE >= CORE: 0 of 7

R-AB classifier B, FILES denominator
interval           STAKE      CORE     MIXED
v4.14..v4.19    4226.891  4637.066  4022.199
v4.19..v5.4     3696.429  5020.656  4460.101
v5.4..v5.10     3347.619  4662.617  3865.088
v5.10..v5.15    2713.063  3228.104  3122.908
v5.15..v6.1     3290.745  3486.438  3246.018
v6.1..v6.6      2245.968  2361.871  1916.991
v6.6..v6.12     3049.534  2667.857   1972.33
  unit: commits per 1000 files
  intervals where STAKE >= CORE: 1 of 7


## Findings

**F1 -- M1 refuted, and robust to both obvious attacks.**  STAKE_SPECIFIC
is lower than SHARED_CORE on commits/KLOC in 7 of 7 intervals.  Swapping
the denominator to files (generated register headers inflate driver
KLOC: `drivers/gpu/drm/amd/` alone is 5.8M of the STAKE class's 7.3M
lines) keeps the direction in 7 of 7.  Swapping to classifier B's class
assignment keeps it in 7 of 7, at a much smaller effect size.  Across
all four variants the direction holds in 27 of 28 interval-cells.

**F2 -- the maturity confound has a defect that understates the case.**
Path age is measured as the first commit touching the path, which is
PATH age, not SUBSYSTEM age.  `kernel/sched/` reads 2011, `kernel/rcu/`
and `kernel/locking/` 2013, `kernel/cgroup/` 2016 -- those are the dates
the directories were split out, not the dates the code was written.  The
scheduler is older than git.  So SHARED_CORE's real age is understated,
its measured 17.4y is a floor, and the confound argues harder against
the prediction than the table shows.  Not repaired: repairing it means
tracing code movement, which is a different instrument.

**F3 -- M6 is a clean null.**  Median top-1 share 0.14-0.27 and top-3
0.33-0.51 with no consistent separation between classes in any interval.
The prediction was that SHARED_CORE would be worse.  It is not.

**F4 -- classifier disagreement is 0.50-0.53 and is not uniform.**  A and
B agree on the core (10 of 12) and come apart on the stake side (4 of
15): vendor driver sections routinely list lkml, which B reads as
shared.  Class membership on the STAKE side is unstable, and that is
why R-B exists.  The two are not reconciled and neither is ground truth.

**F5 -- three of six measures did not run** and are not proxied.  M2 and
M5 need a published employer mapping; M4 needs lore.kernel.org.  Every
read path tried is named in PREREGISTRATION.md section 8.
