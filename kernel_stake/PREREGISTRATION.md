# PREREGISTRATION -- kernel subsystem stake split

Work order D, 2026-09-30.  Committed BEFORE any measure is pulled.
The sha of this commit is the pre-registration timestamp.

STATUS: PROPOSED design, first run.  A null result is a result.  If the
predictions in section 6 do not hold, that is the finding and nothing in
this file is to be revised to accommodate it.

---

## 0. WHAT WAS READ BEFORE THIS COMMIT

Honest declaration, because "before any counts" needs a boundary:

- Reachability probes (section 7).
- `git ls-tree -r --name-only <tag> -- <path>` at v4.14, to confirm each
  candidate path exists.  This produced FILE COUNTS.  A file count is
  not one of M1..M6 and is not used as a denominator anywhere.
- The MAINTAINERS file at v4.14, in full.  The classification in
  section 3 is derived from it, which the work order requires.

No commit count, KLOC, author, organization, tenure, latency or
concentration figure has been computed at the time of this commit.

---

## 1. CLASSIFICATION RULE

Each subsystem is assigned exactly one class.

**STAKE_SPECIFIC** -- serves one firm's product line.  The benefit of the
work accrues to an identifiable company whose hardware or product the
code exists to support.  Examples named in the order: amdgpu, a specific
ARM SoC, a vendor NIC driver.

**SHARED_CORE** -- every user needs it and no firm owns the benefit.
Examples named in the order: mm, VFS, scheduler, locking.

**MIXED/UNCLEAR** -- declared, never forced.  A subsystem goes here when
the rule does not decide it, including: general-purpose code with a
single dominant corporate sponsor, hardware-facing code that serves a
standard rather than a firm, and code that serves one firm's hardware
without that firm's participation.

MIXED/UNCLEAR is a real class.  It is not a holding pen to be emptied
later, and no analysis step may collapse it into the other two.

---

## 2. RELEASES IN RANGE (fixed now)

Selection rule, stated so it cannot be adjusted after the fact: **the
longterm (LTS) release of each calendar year, 2017 through 2024.**  This
gives exactly one tag per year and involves no choice about which
release within a year.

| tag | date | sha |
|---|---|---|
| v4.14 | 2017-11-12 | e3d97e8db5c4 |
| v4.19 | 2018-10-22 | 2241b8bcf2b5 |
| v5.4  | 2019-11-24 | 6e815efe19a9 |
| v5.10 | 2020-12-13 | 3f995f8e0b54 |
| v5.15 | 2021-10-31 | dc7089468610 |
| v6.1  | 2022-12-11 | 7614896350aa |
| v6.6  | 2023-10-29 | 5260836abb70 |
| v6.12 | 2024-11-17 | 06090c9b622a |

Eight tags, seven intervals.  An interval is `(tag[i-1], tag[i]]` by
first-parent-inclusive `git log tag[i-1]..tag[i]`.

v4.14 is the FIRST release in range; the subsystem list and its
classification come from the MAINTAINERS file at v4.14.

---

## 3. SUBSYSTEM LIST, CLASSIFIED (classifier A)

Source: MAINTAINERS at v4.14.  Every path below was confirmed to exist
at v4.14 and to be covered by at least one `F:` pattern in that file.

`init/` was a candidate and is **dropped**: it has zero `F:` coverage in
MAINTAINERS at v4.14, so it is not a subsystem by this order's own
sourcing rule.  Recorded rather than silently omitted.

Classifier A is this session's judgment applying section 1.  Classifier
B (section 4) is mechanical and independent of it.

### STAKE_SPECIFIC (15)

| path | firm |
|---|---|
| `drivers/gpu/drm/amd/` | AMD |
| `drivers/gpu/drm/radeon/` | AMD |
| `drivers/gpu/drm/i915/` | Intel |
| `drivers/net/ethernet/mellanox/mlx5/` | Mellanox |
| `drivers/net/ethernet/broadcom/bnxt/` | Broadcom |
| `drivers/net/ethernet/intel/i40e/` | Intel |
| `drivers/net/ethernet/intel/ixgbe/` | Intel |
| `drivers/net/ethernet/chelsio/` | Chelsio |
| `drivers/net/ethernet/hisilicon/hns3/` | HiSilicon |
| `drivers/net/wireless/ath/ath10k/` | Qualcomm Atheros |
| `drivers/soc/qcom/` | Qualcomm |
| `drivers/scsi/lpfc/` | Emulex / Broadcom |
| `drivers/scsi/qla2xxx/` | QLogic / Marvell |
| `drivers/infiniband/hw/hfi1/` | Intel |
| `arch/arm/mach-rockchip/` | Rockchip |

### SHARED_CORE (12)

`mm/`, `kernel/sched/`, `kernel/locking/`, `kernel/rcu/`,
`kernel/time/`, `kernel/irq/`, `kernel/cgroup/`, `kernel/trace/`,
`kernel/printk/`, `block/`, `lib/`, `net/core/`

### MIXED/UNCLEAR (9)

| path | why it does not decide |
|---|---|
| `drivers/gpu/drm/nouveau/` | serves NVIDIA hardware; NVIDIA does not fund it |
| `fs/btrfs/` | general-purpose fs, concentrated corporate sponsorship |
| `fs/xfs/` | general-purpose fs, SGI/Red Hat/Oracle lineage |
| `fs/ext4/` | general-purpose fs, dominant single maintainer employer |
| `fs/f2fs/` | Samsung-originated, general-purpose, flash-oriented |
| `drivers/usb/core/` | core infrastructure, hardware-facing |
| `net/ipv4/` | core protocol, heavy vendor participation |
| `drivers/nvme/` | serves a standard, not a firm; many vendors |
| `security/selinux/` | general-purpose, concentrated origin |

**Total: 36.**

### Selection limitation, declared now

This list is a **convenience sample**, hand-selected from MAINTAINERS to
span the three classes at comparable scales.  It is not a random draw
and it is not exhaustive.  Selection bias is therefore a live threat to
every between-class comparison in the output, and the second classifier
in section 4 does not address it -- it addresses classification bias
only.  Any result must be read with this limit attached.

---

## 4. SECOND CLASSIFIER (B), specified before it is run

Rule-based, over MAINTAINERS text only.  It does not see classifier A
and it does not look at path names.

For each subsystem, take the MAINTAINERS section(s) whose `F:` patterns
cover the path at v4.14.  Collect the `M:` lines' email domains.  A
domain is GENERIC if it is in this fixed list, else CORPORATE:

    kernel.org, gmail.com, googlemail.com, hotmail.com, yahoo.com,
    outlook.com, zeniv.linux.org.uk, infradead.org, linux.ie,
    free.fr, gnu.org, fb.com is NOT generic, protonmail.com,
    web.de, posteo.de, riseup.net, users.sourceforge.net

Then:

- **B -> STAKE_SPECIFIC** if there is at least one CORPORATE domain and
  all CORPORATE maintainers share exactly one domain and the section
  has at most 2 `M:` lines.
- **B -> SHARED_CORE** if there are at least 3 distinct CORPORATE
  domains among `M:` lines, or the covering section lists
  `linux-kernel@vger.kernel.org` on an `L:` line.
- **B -> MIXED/UNCLEAR** otherwise.

**The disagreement rate between A and B is published and the two are
NOT reconciled.**  Neither is treated as ground truth.

Independence limit, declared: B is mechanical, but its rule was authored
in the same session, by the same party, after A existed.  The
independence is therefore partial and the disagreement rate is a lower
bound on what two genuinely separate classifiers would produce.

---

## 5. MEASURES, per (subsystem, release)

**M1 -- commits per KLOC.**  Numerator: commits in the interval
`tag[i-1]..tag[i]` that touch at least one file under the subsystem's
path.  Merge commits excluded (`--no-merges`), because a merge touches
paths it did not author.  Denominator: KLOC at `tag[i]`, being the total
line count of all tracked files under the path divided by 1000.

**M2 -- distinct contributing organizations.**  Requires a published
employer mapping.  See section 7: none is reachable from this
environment.  M2 is therefore reported as **UNKNOWN** for every cell.
A count of distinct email domains is NOT M2 and will not be presented as
M2; if reported at all it is labelled a separate, weaker quantity.

**M3 -- maintainer count and tenure.**  Count: number of `M:` lines in
the covering section(s) at `tag[i]`.  Tenure: for each such maintainer,
years between their first commit anywhere in the tree and the tag date;
reported as the median across maintainers.  Identity is canonicalised
through the tree's own `.mailmap` at `tag[i]`.  A maintainer with no
commit in the tree has tenure UNKNOWN and is excluded from the median,
with the exclusion counted.

**M4 -- review latency (posted -> merged).**  Requires lore.kernel.org.
Unreachable (section 7).  **NOT_RUN.**  Not estimated, not proxied, and
no substitute measure is introduced in its place.

**M5 -- unpaid/volunteer share.**  Requires the volunteer marking in a
published employer mapping.  Unreachable.  **NOT_RUN.**

**M6 -- bus factor.**  Share of the interval's non-merge commits
contributed by the top 1 and by the top 3 **individual** authors, after
`.mailmap` canonicalisation.  Organization-level M6 requires the
employer mapping and is **BLOCKED**, reported as UNKNOWN, kept separate
from the individual-level figure.

Employer rule, as the order states it: **an email domain is not an
employer.**  Where the mapping cannot resolve a name, the cell is
UNKNOWN.  Nothing is guessed.

---

## 6. CONFOUND COLUMN (required)

**Subsystem age at each release**: years between the first commit
touching the subsystem's path anywhere in tree history and the tag date.

M1 is the measure maturity most plausibly explains away -- an old,
settled subsystem changes less per KLOC regardless of who pays for it.
**M3, M4 and M6 are reported separately from M1** for that reason:
maintainer count, tenure and concentration are not straightforwardly
predicted by age alone.

---

## 7. PREDICTIONS (Corbet's claim), registered now

The claim under test: shared infrastructure is under-resourced relative
to work that serves a firm's product line.

- **M1**: SHARED_CORE **lower** than STAKE_SPECIFIC.
- **M2**: SHARED_CORE **lower** than STAKE_SPECIFIC.  (Not testable this
  run.)
- **M3**: SHARED_CORE **lower** maintainer count than STAKE_SPECIFIC.
- **M4**: SHARED_CORE **worse** (longer latency).  (Not testable.)
- **M6**: SHARED_CORE **worse** (higher top-1 and top-3 concentration).

Direction over time is reported per class; no prediction is registered
for the trend, because the order registers none.

MIXED/UNCLEAR gets no prediction.  It is reported alongside and is not
pooled with either class.

---

## 8. FEASIBILITY, per read path tried

Recorded per the convention that "unreachable" must name the read path.

| source | read path tried | result |
|---|---|---|
| Linux kernel tree | anonymous git, git.kernel.org | CONNECT tunnel failed, 403 |
| Linux kernel tree | anonymous git, github.com/torvalds/linux | **REACHED** |
| lore.kernel.org | anonymous https | no response (000) |
| gitdm employer map | anonymous https, git.lwn.net | no response (000) |
| gitdm employer map | anonymous git, 8 candidate GitHub mirrors | all 404 / unauthorized |

Clone plan actually used: `--filter=blob:none --no-checkout`, full
history and tags, into a temp directory outside any live checkout.
2.0 GB.  No full clone, no checkout of the working tree; blobs are
fetched lazily and only for the 36 subsystem paths at the 8 tags.

---

## 9. SCOPE LIMITS -- printed with every result

- Author email is not who directed the work.
- Volunteer share is self-declared, where it is available at all.
- One project.  Nothing here generalises to other ecosystems.
- Activity, not code quality.  None of M1..M6 measures whether the code
  is good, needed, or correct.
- The subsystem list is a convenience sample (section 3).
- Three of six measures are not run or not resolvable in this
  environment (section 5).
