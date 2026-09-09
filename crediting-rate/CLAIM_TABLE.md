# CLAIM TABLE — CREDITING RATE (WORK ORDER L)

Prefix `CRD_` (`CR_` is taken by `claim-record/`). Statuses: SUPPORTED /
REFUTED / UNVERIFIED / OPEN, with the falsifier stated per claim.

---

**CRD_001.** The instrument returns different G values on two constructed
worlds that differ only in whether crediting follows the loanword bin
(`ETYMOLOGY_TRACKING` at gap 0.6; `CONTRIBUTION_TRACKING` at gap 0.0), so
the return is not constant.

*Falsifier:* a pair of worlds with different crediting-by-bin that return the
same value. *Status:* SUPPORTED on the fixtures (`--selftest`).

---

**CRD_002.** Unknown ordering is excluded and counted, never estimated: the
ten items the order names carry `null` attestation years and the run returns
`BLOCKED(insufficient_attested_ordering)` with `ordering_unknown = 10`.

*Falsifier:* any code path that fills a missing year or admits an item
without `ordering_source`. *Status:* SUPPORTED; pinned.

---

**CRD_003.** The blind is structural: a codings file carrying any field
whose name contains `loanword` is refused at load, and the bin meets the
coding only in `join()`.

*Falsifier:* a codings row reaching `join()` with the bin on it. *Status:*
SUPPORTED; pinned. Limit: the blind is a file rule, not a person rule — a
coder who has read `events.jsonl` is not blind, and nothing here can tell.

---

**CRD_004.** The N1 band brackets zero on the constructed worlds and the
`equal` known-answer case sits inside it; the band is a percentile of 2000
seeded label shuffles and the run is deterministic under a fixed seed.

*Falsifier:* a band that excludes zero on a world with equal rates.
*Status:* SUPPORTED on fixtures.

---

**CRD_005.** The pre-stated prediction (retained credited more) is a
DIRECTION only; the script refuses to run without `PREDICTION.md` and
prints its hash, so a change to the prediction after the fact changes the
hash every report carries.

*Falsifier:* a run with no prediction file. *Status:* SUPPORTED; pinned.

---

**CRD_006.** The method layer the order consumes (F branch set, G return
enum) is not in this repository; nothing in the tree carries `branch_set` or
a G enum. G is implemented locally as the five listed values plus one added
BLOCKED reason (`frame_undeclared`); F is emitted as `branch_set.json` in the
order's shape. `archive-siting-bias`, which the branch set links, is also
absent.

*Falsifier:* the layer landing; then this folder imports it and this claim
closes. *Status:* OPEN — named-and-absent, the shape this tree records.

---

**CRD_007.** `CONTRIBUTION_TRACKING` is decided by a stipulated cut
(`MISATTR_MAX = 0.2`) on the misattribution rate, and `MIN_PER_BIN = 3` is
stipulated too. Both are `[CHOICE]` constants printed in the report, with no
basis beyond being stated.

*Falsifier:* a basis for either number. *Status:* OPEN.

---

**CRD_008.** Nothing here is a statement about algebra, paper, printing,
or any tradition. Every real cell is unmeasured: no attestation ordering was
consulted, no corpus declared, no coding done. The instrument is built and
its return is shown to move on constructed data only.

*Falsifier:* a real run. *Status:* UNVERIFIED, and stays so until an operator
supplies the three inputs.
