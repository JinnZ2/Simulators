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
