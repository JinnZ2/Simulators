# SOURCES — what was read, what was carried, what was refused

Measured from this environment on 2026-09-27. Egress is an allowlist;
`raw.githubusercontent.com` answers and every publisher, agency and
archive host refuses CONNECT with 403. Nothing below is a statement about
whether a source is right; it records where each value came from.

## Read here (fetched, sha256 recorded, line numbers cited in the records)

| file | fetched (UTC) | bytes | sha256 |
|---|---|---|---|
| python/peps `peps/pep-0001.rst` | 2026-09-27T01:28:57Z | 41682 | `c2bc2ce666758fa82ee2592926218d710e6fdddc674d78314bd6b56c392c46f6` |
| python/peps `peps/pep-0572.rst` | 2026-09-27T01:28:57Z | 47028 | `abf5401ec523a03d59a6f3173842784f426bfd49d8b0a87a512646557bcef8b1` |
| joelparkerhenderson/architecture-decision-record `README.md` | 2026-09-27T01:28:58Z | 33165 | `ab05f4f2b3492c9c589ebe70054d84f9573cb8799b81093609563fc5f7665294` |
| rust-lang/rfcs `0000-template.md` | 2026-09-27T01:28:58Z | 5705 | `88423c4b1ad871fd97ab7a5480ae260984fa5ddcde05e05422f6ca1fc85df50f` |
| openai/model_spec `model_spec.md` | 2026-09-27T01:28:58Z | 276131 | `a52378c1ae7514b091162c17abd285365eddaf4066f70773f3ffe05453f94cab` |
| adr/madr `template/adr-template.md` | 2026-09-27T01:31:26Z | 3527 | `940d45674563e0a2…` (prefix; full digest recomputable from the URL) |

The fetched files are not checked in; the records under `demo/records/`
cite them by line. In-tree documents coded for FWO-3
(`design-basis-ai/SOURCE_DROP_V2.md`, `seam-gaps/OPEN_QUESTIONS.md`) are
cited by line at the current revision.

## Carried (named in the work order or from memory; not read here)

| item | where it is used | why not read |
|---|---|---|
| Calhoun 1973 "Death Squared", Proc R Soc Med | FWO-1 study rows | `pmc.ncbi.nlm.nih.gov` and `europepmc.org` refuse CONNECT (403, 2026-09-27T01:28:31Z) |
| Emrick; Science History Institute; Ramsden (secondary reconstructions) | FWO-1 study rows | not attempted; the primary was refused |
| IRS Topic 420; Form 1099-B; 1099-MISC threshold | FWO-2 barter row | `www.irs.gov` refuses CONNECT (403, 2026-09-27T01:28:31Z) |
| Form 1099-PATR (co-op patronage) | FWO-2 co-op row | from memory; unverified |
| IRS Notice 2014-21 (virtual currency) | FWO-2 crypto row | from memory; unverified; the order's own line is what the row carries |
| gift tax annual exclusion | FWO-2 gift row | from memory; the mutual-aid-scale obligation medium is left UNKNOWN |
| Whillans, Weidman & Dunn (time vs money, ~48%, N ~4,690) | R-1 | not attempted; publisher hosts refuse |
| Phil Trans R Soc B 376:1819, 20190677 (macaque token economy) | R-2 | `royalsocietypublishing.org` refuses CONNECT (403, 2026-09-27T01:28:32Z) |

## Refused hosts (one CONNECT each)

```
2026-09-27T01:28:31Z  403  www.irs.gov
2026-09-27T01:28:31Z  403  pmc.ncbi.nlm.nih.gov
2026-09-27T01:28:31Z  403  europepmc.org
2026-09-27T01:28:32Z  403  royalsocietypublishing.org
2026-09-27T01:28:30Z  403  github.com/<owner>/<repo>/raw/...   (the HTML host; raw.githubusercontent.com answers 200)
```

## Repository creation

`JinnZ2/route-independence` could not be created from this session:
`add_repo` reports the repository not found or not accessible, and the
GitHub integration answers `403 Resource not accessible by integration`
to the create call. The packet lands here as a promotable folder, the
`substrate-alternative/` precedent (`SA_018`). Nothing in the folder
imports across its own boundary except the FWO-2 prior-art cross-check,
which is a file-path import that reports `PRIOR_ART_NOT_IMPORTED` when
the sibling is absent.

---

## Order of 2026-09-27 (FWO-5, FWO-6, FWO-7)

Built in a second session, later the same day, whose shell was blocked
for the whole conversation. No host was probed and no fetch was made;
there is no refused-host table for this order because nothing was
attempted. Everything READ came through the GitHub API from this
repository:

| item | read through | used for |
|---|---|---|
| `route-independence/*` at `177d885` on `claude/coupling-check-disaster-twiklx` | contents API | FWO-2 reuse; carried items 2 and 3 (the eight `demo/records`) |
| commit `57b9cdf` per-file stats; `tools/known_answer.py` at `57b9cdf` and `2fa8648` | commits / contents API | carried item 1 (RIN_030); line content of the two `run_manifest.py` lines not read |
| `Noise-as-Information-Sensor/tools/CLAIM_TABLE.md` | code-search fragments only (repository outside session scope) | carried item 4 (RIN_033), partial |

Carried, not read, in this order's files: property tax in dollars (case
(a)); IRS Notice 2014-21 (case (c); already carried above); the generic
open-access dependency structure (case (b)), whose named instance
(Kalai, Nachum, Vempala & Zhang, Nature 653, 2026) was not read,
`www.nature.com` being outside the allowlist; every entry of
`conversion_register.json`, each marked CARRIED or UNKNOWN in place;
the El Salvador legal-tender line in the bitcoin entry (from memory).

Run record, same session, later turn: a shell became available; still
no fetch and no host probed. `test_dependency_chain.py` and `test_route.py`
were run once each on this branch (counts printed by the files, recorded
in `CLAIM_TABLE.md` RIN_038), and `dependency_chain_audit.py` was
rendered to `samples/dependency_chain.sample.txt`. Carried item 1 was
re-read from the local clone (`git diff 57b9cdf^1 57b9cdf --
tools/run_manifest.py`), the one item that moved from CARRIED to READ.

## Order of 2026-09-27b

Nothing fetched. No publisher, standards-body, regulator, statistical-agency,
treasury or central-bank host is on the egress allowlist; the same measured
refusals as the sections above apply and no new host was probed, since a
refused CONNECT on one more host is not new information. What each item
carries instead:

- FWO-8: FWO-5's three cases (CONSTRUCTED / CARRIED, above); every
  `edge_class` and `coupling_side` is this session's reading with its basis in
  the table. The taxonomy itself is CARRIED from the order, which carries it
  from a pasted third-party model output.
- FWO-9: declarations, this session's; the fifth class OBSERVED, carried.
- FWO-10: six standards named from memory (CARRIED_FROM_MEMORY), none read;
  prior-art entries from memory, none read.
- FWO-11: six seed cases from the order's list; every date UNSOURCED —
  recalled, and the order's "verify, do not assume" was not done because no
  source could be reached.
- FWO-12: the Linux figures CARRIED from the order (its own note: web search
  2026-09-27, citations in the authoring session).
- FWO-13: rows 1–2 CARRIED from the order's table (OBSERVED there); row 3
  PROPOSED there, not verified; the fringe-benefit rules from memory.
- FWO-14: twelve candidate rows from memory, CANDIDATE_UNSOURCED.

Carried question 5 was answered from this clone's own history after
`git fetch --unshallow origin` (236 → 894 commits), which is the one fetch
made: the losing-parent blobs at `8d9b6c9^2`, `2c68758^1` and `83bb7d9^1`.

## Amendment A-1 of 2026-09-28

Nothing fetched. Inputs are FWO-5's three cases (CONSTRUCTED / CARRIED, above)
and the amendment's own fixtures, each labelled CONSTRUCTED in its source
field. The case-(b) token chain (citation → credential → funding) is CARRIED
from the amendment's own text and is a declaration, not an observation of any
conversion. The symmetry argument is arithmetic on the premise as the
amendment states it and rests on no source.

## Amendment A-2 of 2026-09-28

Nothing fetched. The amendment's section 2 carries six sources at its author's
grades (G-1 P; G-2 P/S; G-3 K; W-1, W-2, W-3 S) and three items marked NOT
SOURCED. Every fixture row and every event in `gate_state.py` names one of the
six by id and is CARRIED at that grade; this session read none of the texts
behind them (statute, case-report and Wikisource hosts are off the egress
allowlist; no CONNECT was attempted). Grade K (G-3) is stored and flagged and
enters no hold. The HB 16-1005 effective date (2016-08-10) is carried as
delivered, verification NOT_RUN. The G-2 court conflict is recorded in
`SOURCES["G-2"]["conflict"]` with Common Pleas carried and `resolved: False`.
The constructed all-OPEN fail fixture is labelled CONSTRUCTED_UNSOURCED in its
source field and its tag.

## Amendment A-2.1 of 2026-09-28

Nothing fetched. Two sources are upgraded to P by the amendment's author and
CARRIED here at P unread: W-1a (the signed HB 16-1005 text at
content.leg.colorado.gov, effective 2016-08-10 conditional on sine die
2016-05-11, the condition confirmed by the CO Division of Real Estate 2016
Annual Report) and W-2a (UT SB 32 (2010) enacting Utah Code 73-3-1.5 at year
precision, plus the 2022 codification's container rule). Two sources are
recorded at S with `input: False` and refused as any row's gate_source until
read: UT 73-2-27 and UT 73-1-1. The 2009 Colorado bill and the Texas
agency/attorney-general statement are named as NOT sourced; the rows that
would rest on them read UNKNOWN.

## Amendment A-3 of 2026-09-28

Nothing fetched. Section 3 names nine sources, T-1..T-9, and none has landed:
each is stored in `SOURCES_A3` at grade K with status NOT_LANDED, so every
fixture row resting on one is hold-ineligible (rule 2). The TOKEN_PURCHASE
gates in F-T4 and the constructed rows used by the fail fixtures carry no
source and are tagged CONSTRUCTED_UNSOURCED. Every jurisdiction is a
constructed placeholder (US city X, county X, state A, state B, state X) and
every gate_state is a constructed reading of an unread source. Grants Pass v.
Johnson (2024) is named in the amendment and was not read here; its year is
the order's.

## Amendment A-3.1 of 2026-09-28

Nothing fetched. The one added source id is `A31-6`, the amendment's own
section-6 sentence instructing a clothing RETAIN fixture row, stored at grade K
with status STATED_BY_AMENDMENT; the row resting on it is hold-ineligible. The
EVIDENCE migration rule reads OPEN_ENDED on a t field only where a source text
records it, and the only such text in the tree is W-2a's "current text (Justia
2022 codification)", carried from A-2.1 and read by that amendment's author,
not by this session.

## Amendments A-4, A-5, A-6 of 2026-09-28

Egress probe at 2026-09-28T13:14:37Z: ecfr.gov, leg.colorado.gov and
law.cornell.edu refused CONNECT (curl exit 56); github.com connected as the
control. Nothing named in the three amendments was read by this session.

```
C-1      P, FRAGMENT   Colorado 37-96.5-103 as quoted in A-4; read in part by the
                       amendment's author; not hold-eligible until read in full
C-2      S             named by A-4; not an input to any computed reading
T-10..13 NOT_SOURCED   gates named by A-4; carried as K rows
A4-1     K             A-4's own statement (STATED_BY_AMENDMENT)
CS-R     unread        3 sources named by A-5 (enrollment-based set)
CS-A     unread        4 sources named by A-5 (admission-based set)
RA-1..5  K NOT_LANDED  25 CFR 83.11, the other-tribe criterion, one
                       Termination-era act and its restoration act, one nation's
                       enrollment criteria, one ethnographic conversion figure
A6-4     K             A-6's own fixture text (STATED_BY_AMENDMENT)
```

E-A6-3 is not filled from memory, per the amendment. The recognition events on
CS-R4 (1954 TERMINATED, 1973 RESTORED) are RA-3's structure as the order
states it, grade K, flagged.

## Amendment A-6.1 of 2026-09-28

Nothing was fetched. The amendment text was recovered from the chat transcript with
entities decoded, not re-typed, and the user's re-paste matched it. Every CE line is
CARRIED at the amendment author's grade and was read by nobody in this session. The
egress record from A-4..A-6 stands.

```
CE-1a  P             Indian Removal Act, 4 Stat. 411 (citation)
CE-1b  S             history.state.gov scope: ~70 treaties, nearly 50,000 by end of Jackson's presidency
CE-1c  NOT_RECORDED  NPS scope: about 100,000 across five nations (the amendment states no grade)
CE-2   S             Worcester v. Georgia (1832)
CE-3   S             ANCSA, PL 92-203 (several); CE-3f Kodiak ANCSA history PDF, S
CE-3k  K             Prudhoe Bay / pipeline link (Grokipedia only); not an input
CE-4   P             25 CFR 83.11(b), retrieved TRUNCATED; total evidence paths NOT_RECORDED
CE-5   S             1994 rule 83.7(f) and 83.1; retention in the current rule NOT_RECORDED
S-1..S-5             still to source
```

The one IMPOSED_SCARCITY row is constructed. Its source gate, G-T3, is A-3's T-3:
grade K, NOT_LANDED.
