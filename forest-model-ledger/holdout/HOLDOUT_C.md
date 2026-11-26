# Holdout, Phase C: reveal and score

CC0. Seal verification and mechanical scoring only. No refit, no new
branch, no rescue.

Status: REVEALED and SCORED. Every holdout direction read INDETERMINATE,
so no model direction was scored as hit or miss.
Co-authored, Kavik + Claude, work order of 2026-11-22. Run date (UTC):
2026-11-22. Observer slots: null.

Tags: OBSERVED = seen in this run (hashes checked, numbers printed by
`holdout/phase_c.py`); DERIVED = a reading that follows from what is
stated here; PROPOSED = untested; NOT RECORDED = nobody in this run
looked or it was not given. Hits and misses are OBSERVED and scoped to
this holdout; interpretations are DERIVED.

Every number in the indented blocks below was printed by
`python3 holdout/phase_c.py SOURCE_CSV NONCE_A NONCE_B` and pasted by
script. None was typed.

"Holdout validation can only confirm branches someone later reached; it
 cannot score true unavailability. (inherited weld 4)"

"Predictions were computed by code from anchor studies; the proposing
 model's training may contain the holdout literature."

## 1. Seal verification

[OBSERVED] Source refetched for the reveal:

    URL as called   https://zenodo.org/api/records/10403125/files/PSF.data.EL.open.csv/content
    UTC             2026-11-22T20:11:22Z      HTTP 200
    sha256          bb56ba5ac31b13be09cf3df42c1215b53255bb1eb3bb8a91838ab8cb4cb5c82c

Revealed nonces (both were held by the owner until this order):

    nonce_A   32fd3e42714d19086fe6b71b9faae1302abf2eb5361c37a669fc25f2f237bf7f
    nonce_B   118e00ab83f2a96435aa40e54b79add04848a245b8c090a1bf21d3990205affd

    STEP 1 seals
      a source sha256                      PASS   1609518 bytes
      b holdout rebuilt                    PASS   601888 bytes, 2262 rows
      c sha256(nonce_A || holdout)         PASS   ce54a50ecc4eba87d9df5ce99db93eddcbf3c1f3243765481d21cb2340c76713
      d predictions.json sha256 + bytes    PASS   33257 bytes
      d sha256(nonce_B || predictions)     PASS   f5dcc443d5afb4144ea0836015d0694c6796b723aa6d3c34e0bb00d7f7bcc65d
      holdout: 2262 rows, 47 studies ; anchor: 3707 rows, 155 studies
      same-code check: refit on anchor vs sealed, largest difference 0.0e+00  PASS

`phase_b.py --seal` was not run. The holdout rows are still not in this
tree; `phase_c.py` rebuilds them from the source file and refuses to
score unless every line above reads PASS.

The same-code check is the guard on "no new choices": the fit function
imported from `phase_b.py`, run on the anchor rows, returns every sealed
estimate and interval bound exactly.

## 2. Exposure audit

Owner decisions, recorded as given in the Phase C order:

- "Phase B read root CLAUDE.md (harness-loaded) and SHAPE_SPEC.md lines
   1-12 outside its read set. Neither holds holdout data. Holdout
   exposure: none. Logged as PROCEDURAL DEVIATION, not EXPOSED. The
   Phase B order's 'any other read = EXPOSED' rule was broader than its
   purpose (guarding holdout contact); the fault is in the order."
- "Crowding for B1-B4 stays sealed as NOT RECORDED. Probes, if run
   later, go in a separate dated record."
- "Phase B model: [WITHHELD], training cutoff June 2026 as stated
   to that session; declared in its report, withheld from its artifact
   by a harness rule."

The third decision is recorded with one substitution: the model
identifier the owner wrote is replaced by [WITHHELD], because the same
rule that kept it out of `HOLDOUT_B.md` binds this file. The owner's
order and the Phase B report carry the identifier.

[OBSERVED] `HOLDOUT_B.md` was read in full for this audit. Its run header
lists "EXPOSED reads: none" and names the two out-of-set reads above. No
other EXPOSED or STOP flag appears in it. No branch is excluded from
scoring for holdout exposure.

[OBSERVED] Exposure on the scoring side: this run was the Phase A
session. It had read the holdout rows during the split. Both seals were
fixed before that mattered: the predictions were made by a different
session and are checked byte for byte above, and nothing in the scoring
is chosen here.

## 3. Scores

Sealed intervals are cluster-bootstrap intervals of the anchor estimate,
not widened for holdout sampling error, so interval_hit is strict;
overlap is the looser companion.

Rule: a holdout direction is read only if the holdout 80% interval
excludes zero. Otherwise INDETERMINATE, neither hit nor miss.

    STEP 3 holdout estimates
      id      holdout est   holdout 80% interval     studies  rows  dropped  direction
      B1 AI     +0.0407   [ -0.0091,  +0.0820]      47   2262      0    INDETERMINATE
      B1 MAP    +0.0373   [ -0.0053,  +0.0569]      47   2262      0    INDETERMINATE
      B2        -0.0006   [ -0.0068,  +0.0027]      47   2262      0    INDETERMINATE
      B3        -0.0379   [ -0.1307,  +0.0152]      47   2262      0    INDETERMINATE
      B4        +0.0738   [ -0.0036,  +0.1397]      47   2262      0    INDETERMINATE
      R5        -0.1385   [ -0.3174,  +0.0155]      47   2262      0    INDETERMINATE

MODEL column (tests run_9 mechanisms). Kept apart from the FIT column.

    MODEL column
      id      sealed model dir   holdout dir     result          counted  tag
      B1 AI   negative           INDETERMINATE   INDETERMINATE   no
      B1 MAP  negative           INDETERMINATE   INDETERMINATE   no
      B2      positive           INDETERMINATE   INDETERMINATE   no
      B3      positive           INDETERMINATE   INDETERMINATE   no
      B4      positive           INDETERMINATE   INDETERMINATE   no       direction by construction, not scored
      R5      void               INDETERMINATE   void            no       no model run

FIT column (tests whether the anchor relation replicates; no model).

    FIT column
      id      sealed fit est  sealed 80% interval      sealed dir  dir result      interval_hit  overlap
      B1 AI     -0.2378       [ -0.3342,  -0.1271]   negative    INDETERMINATE   no            no
      B1 MAP    -0.1164       [ -0.2236,  -0.0118]   negative    INDETERMINATE   no            no
      B2        +0.0019       [ -0.0040,  +0.0076]   positive    INDETERMINATE   yes           yes
      B3        -0.0104       [ -0.1289,  +0.1155]   negative    INDETERMINATE   yes           yes
      B4        +0.1000       [ +0.0202,  +0.1815]   positive    INDETERMINATE   yes           yes
      R5        +0.1375       [ +0.0438,  +0.2389]   positive    INDETERMINATE   no            no

[OBSERVED] Read of the two tables, scoped to this holdout:

    model directions scored        0 of 4 (B1 AI, B1 MAP, B2, B3 all INDETERMINATE)
    B4                             INDETERMINATE as well; by construction, not counted either way
    fit directions scored          0 of 6
    interval_hit yes               B2, B3, B4
    interval_hit no, overlap no    B1 AI, B1 MAP, R5

[DERIVED] The holdout does not confirm and does not refute any sealed
direction. What it does show is on the FIT side: for B1 (both columns)
and for R5 the holdout estimate falls outside the sealed anchor interval
and the two intervals do not overlap. The anchor relation did not carry
over at its anchor size in those three. In all three the holdout point
estimate has the opposite sign to the anchor estimate, with an interval
that includes zero.

## 4. Baselines

    STEP 4 baseline (chance 0.5 per scored model direction)
      scored 0: no baseline computable
      scored ids: none

[OBSERVED] With zero scored model directions there is no hit count and
no binomial probability to report. This is not a result of 0 hits; it is
no scored trials.

R5, the dense reference, beside B1-B4 in the FIT column: direction
INDETERMINATE, interval_hit no, overlap no. The reference with no run_9
mechanism failed to replicate at anchor size in the same way B1 did.

n is tiny (at most four countable directions, 47 holdout studies).
volume: thin on any aggregate claim.

## 5. Reading the misses

No refit and no rescue. There is no direction miss to read, because no
direction was scored. The three interval misses with no overlap (B1 AI,
B1 MAP, R5) are read here as FIT-column misses.

B1, read against A1 first. Declared assumptions, from predictions.json:

    A1  fertility E maps onto aridity / water limitation: E = min(AI, 1); MAP is read as a second monotone proxy of E
        breaks -> model and fit disagree in sign on AI, or AI and MAP fits disagree with each other
    A2  the benefit term is linear in E and changes sign inside 0..1 (written into the equation; run_1 flag: partly circular)
        breaks -> holdout rr vs AI is flat or curved with no sign change inside the sampled AI range
    A3  aff is set so that b at E = 0 equals run_9's b
        breaks -> direction holds but the magnitude is off by a constant factor
    A4  E changes only b; precipitation, deposition and decay stay at run_9 values
        breaks -> an aridity effect appears in sterilised-soil growth as well (not a coupling effect)
    M1  mapping
        breaks -> Self-Other rows and Self-Sterilized rows give opposite moderator directions; M2 (self vs other-conditioned soil) is carried beside M1 for that reading

    A1   signature = a sign disagreement. NOT met under the scoring rule:
         the holdout direction is INDETERMINATE on AI and on MAP. The two
         columns do not disagree with each other (both point estimates
         positive, both intervals include zero). [OBSERVED]
    A2   signature = holdout rr vs AI flat. This is the one the result
         points to: the holdout slope interval includes zero. [DERIVED]
    A3   not reached: it presumes the direction held.
    A4   NOT RECORDED: it needs sterilised-soil growth read against
         aridity, which no fit in Phase B or C computes.
    M1   NOT RECORDED: it needs the fit split by Approach, a fit Phase B
         did not define. Not run here (it would be a new choice).

    So A1 is neither supported nor broken by this holdout. The flat
    reading matches A2's stated signature. [DERIVED]

R5. Declared assumptions:

    A1  no mechanism; a moderator fit on anchor studies only
        breaks -> not applicable

    none of the above -> curiosity branch placeholder:
    CB_R5_ORIGIN (placeholder, not built): the non-native minus native
    difference was positive with an interval excluding zero in studies
    through 2018 and is not distinguishable from zero, with a negative
    point estimate, in studies after 2018. No run_9 mechanism speaks to
    it. Status: open. [PROPOSED]

Method mix, anchor vs holdout, row counts (the Phase2.time bins are for
this table only; no score uses them):

    STEP 5 method mix (row counts)
      Experimental.setting   Greenhouse   anchor  3559 (0.960)   holdout  1802 (0.797)
      Experimental.setting   Field        anchor   148 (0.040)   holdout   460 (0.203)
      Approach               Self-Other   anchor  3198 (0.863)   holdout  2105 (0.931)
      Approach               Self-Sterilized anchor   509 (0.137)   holdout   157 (0.069)
      Phase2.time            <= 3 mo      anchor  2707 (0.730)   holdout   846 (0.374)
      Phase2.time            3-6 mo       anchor   708 (0.191)   holdout   642 (0.284)
      Phase2.time            6-12 mo      anchor   184 (0.050)   holdout   389 (0.172)
      Phase2.time            > 12 mo      anchor   102 (0.028)   holdout   385 (0.170)
      Phase2.time            NA           anchor     6 (0.002)   holdout     0 (0.000)

[OBSERVED] The method mix moved between the two sides: field rows went
from 0.040 to 0.203 of rows, Self-Sterilized from 0.137 to 0.069, and
experiments longer than 6 months from 0.077 to 0.342.

[DERIVED] Per id, does a miss or a shift line up with that drift?

    B1 AI, B1 MAP   interval miss. Lines up in time with the drift: yes.
                    Cause: NOT RECORDED. Separating aridity from setting
                    and duration needs a fit with those as covariates,
                    which is a refit and is not done here.
    B2              no miss. Its own moderator (Phase2.time) is one of the
                    drifting columns: the holdout samples long durations
                    about four times as often as the anchor set.
    B3              no miss. Its own moderator (Experimental.setting) is
                    the other drifting column: 148 anchor field rows
                    against 460 holdout field rows.
    B4              no miss. Lines up with drift: NOT RECORDED (Life.form
                    mix by side was not in the order's table).
    R5              interval miss. Lines up in time with the drift: yes.
                    Cause: NOT RECORDED, same reason as B1.

B3 and B4: toolbox owed (gate rule); cannot read as holds. This applies
regardless of score. Both matched toolbox triggers in Phase B (B3: the
change moves nearly nothing; B4: the direction holds by construction)
and the full toolbox has not been run on either. Their interval_hit
"yes" is a statement about the anchor fit replicating, not about the
run_9 mechanism.

## 6. What this does and does not establish

    does       both seals verify; the scoring used the sealed code path;
               three of six anchor relations sit inside their sealed
               interval on the holdout, three do not
    does not   score any run_9 mechanism: every direction is
               INDETERMINATE at the holdout's size
    does not   say the indeterminate directions are absent: 47 studies
               give wide intervals, and a wider holdout could read them
    does not   score crowding: sealed as NOT RECORDED for B1-B4

## Provenance

Co-authored, Kavik + Claude, Phase C work order of 2026-11-22 (order
text sha256 93f486d4b898fea66ddc1e1c9769ac3dc1bd46596c1436966366ccc7cbc56055,
END marker present). Base branch: claude/forest-holdout-phase-b (PR
#331). Code: `holdout/phase_c.py`, which imports `fit` and `dummy` from
the committed `holdout/phase_b.py` and changes neither. Source data:
Zenodo record 10403125, not committed. The sealed predictions were made
by a separate session from anchor studies only; this run verified their
bytes and scored them. The readings in section 5 are this run's and are
tagged DERIVED or PROPOSED.
