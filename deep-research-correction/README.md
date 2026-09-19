# deep-research-correction

An external deep-research report about `JinnZ2/Simulators`, the correction
notice issued against it, and a checker that recomputes the notice's
mechanical items. The `external-audit/` pattern: the outside documents are
landed **verbatim** and edited by nothing here; the folder's work is a
read-only recomputation.

## The two documents

- **`Simulators_Last_5_Folders_Deep_Research.md`** — the target. A
  deep-research report produced by Kimi (external model, deep-research
  mode), self-dated 2026-09-19, covering the five most recently updated
  content folders of the repository on `main` (`substrate-alternative`,
  `revision-survival`, `ledger`, `move-set`, `notes`). Landed byte-exact.
- **`CORRECTION_NOTICE.md`** — the notice. Issued 2026-09-18 by Claude
  (Opus 5), single session, no independent clone. It covers only what is
  checkable without a clone: internal consistency of the target, its
  external citations, and its measurand assignments. It does **not** audit
  the repository and does **not** confirm or dispute any test-suite result
  the target reports. Landed byte-exact.

## The checker

`check.py` reads the landed target read-only and recomputes the subset of
the notice that is mechanical. It **inherits the notice's scope**: document
integrity and measurand assignment only — nothing here audits the
repository's instruments or the target's suite results.

```
C-1  forward-dated execution   doc research/re-exec date vs notice issue date
C-2  check counts (157 vs 220) doc-internal arithmetic (count_relation)
C-3  dead citation URL          a future-year URL segment (jul-3026) in the doc
C-4  commit author read as      (a) the doc's own figures reconcile, so the
     contribution share             fault is the measurand not arithmetic;
     (LOAD-BEARING)             (b) a local git recompute differs from the
                                    doc's main-branch figures;
                                (c) the STRUCTURAL verdict UNPARTITIONED,
                                    imported from measurand-partition
C-5  operator characterization  the two clauses present in the doc
C-6  preference attribution      the clause present in the doc
C-7  sibling repository count    doc vs operator figure; true count egress-blocked
U-1  same-author void scope      live: undeclared in this repo
```

Verdicts are one closed set — `CONFIRMED_FROM_DOC`, `CONFIRMED_HERE`,
`CARRIED`, `NOT_EVALUABLE` — plus C-4's structural half, which returns the
measurand verdict `UNPARTITIONED` computed by `common.attribution` rather
than restating it.

## C-4 is the load-bearing one, and it is the repository's own thesis

The notice's C-4: the target reads the git commit-author field as a share
of contribution ("roughly 65% authored by Claude"). The commit-author field
records **which identity ran `git commit`**, not who originated the
specification, the claim set, the falsifier choice, or the decision to
build. In an agent-executed workflow the two come apart completely.

That is exactly `measurand-partition/`'s instrument fault — an observation
made in one setting (which identity executed the commit) scored against an
outcome produced by many unmeasured variables (the contribution), with the
whole residual assigned to the observed thing. So the checker does not
restate the point; it **imports `common.attribution`** and lets it return
`UNPARTITIONED`. The local git recompute shows the count is not even a
stable quantity: the target read `main` (853 commits, Claude 550), this is
a working branch (a different total), and both are properties of who ran
the tool.

## Running it

```
python3 check.py            # render the recomputation
python3 check.py --choices  # the [CHOICE n] markers
python3 test_check.py       # the checks; prints their count
```

`check.py` refuses `--selftest` (exit 2). The render screens clean through
`sheet-structure-scan/no_severity` with no exemption. `count_relation` (the
C-2 classifier) is registered in `tools/known_answer.py`.

## Charts

The target's zip carried three chart PNGs. This repository is text-only, so
they are not checked in; `CHARTS.md` records their filenames, sizes and
sha256 so a re-obtained copy is checkable against the hash.

## What is carried, not verified

Every external-source item is `UNVERIFIED` here — the egress gate refuses
publisher hosts. That covers C-7's true sibling count and the notice's own
V-1..V-3 citation checks (the Kalai *Nature* DOI, AbstentionBench, Kadavath),
which are the notice's OBSERVED and are recorded, not re-checked. The
target's suite results are the notice's U-2 and are unchecked here; the
`ledger` folder the target names is absent from this branch, so even the
folder set differs. Permanent-id findings in `CLAIM_TABLE.md` (`DRC_`).
Stdlib only, parses under 3.9, phone-buildable, CC0.
