# Scrub rules and manifest

Applies to the public export of this memory set. CC0, like everything else here.

## What was removed

Categorically, from every exported file:

- Occupation, employer, equipment, and route identifiers
- Location at any resolution below "cold-climate continental"
- Family, partner, friends, colleagues, named third parties
- Credentials, degrees, certifications, employment history
- Health, sleep, and body data attributable to a person
- First-person voice where it marks the author — findings restated impersonally
- Repo paths and org names that resolve to an identifiable account
- Dates on personal instances (kept on published studies and citations)

## What was kept

- Every mechanism, marker, spec, gap, and falsifier
- Every measurement design, denominator problem, and queued task
- Study citations, archive shelf marks, dataset names — these are public and re-checkable
- Findings originally seeded by first-hand observation, restated as observation reports
  without the observer

## The known cost

Where a finding was grounded in a specific case, the case is now generic. The reasoning
survives; the evidentiary weight of "someone with decades in this specific position observed
this" does not. Three files carry this cost most:

- `facility-risk-index` — the whole field-observation section is now unattributed
- `refusal-false-positive-log` — instances lose their dates and their session identities
- `recent-work` — the micro-skill cases lose their relations

An observer report without a named observer is weaker evidence than one with it. That is the
tradeoff taken deliberately, not an oversight to be corrected by adding the names back.

## Tier assignment

**TIER 1 — exported unchanged (57 files).** Already written impersonally: markers,
mechanisms, case sets, simulator specs, ecosystem conventions.

**TIER 2 — scrubbed and exported (7 files).**

| file | what was lifted |
|---|---|
| sleep-duration-instrument | personal sleep pattern, attribution of the read |
| idle-shutdown-restart-accounting | specific vehicle, fleet settings, first person |
| facility-risk-index | operator identity, dates, org cross-refs |
| refusal-false-positive-log | instance dates, model names, org repo references |
| instance-log-index | corpus size, repo paths, prior-art filenames |
| work-load-ordering (was physical-work-load) | hours figure, first person |
| recent-work | family relations, repo-specific references |

**TIER 3 — held back entirely (12 files).** Not exported in any form, and not enumerated
here, because several of the filenames are themselves the personal information. By category:
an author profile, an operating-preferences file, four files on named individuals, a family
file, two personal-interest files, one site-specific build file, and two files on one person's
cognition and physical practice.

The build file is held rather than scrubbed because county, geology, permit pathway, and named
research partner are jointly identifying and the technical residue is thin. The two cognition
and practice files are held because their content is substantially about one person; scrubbed,
they would be hollow.

## Rebuild note

This export reconstructs the work, not the working relationship. Loading it into a fresh
context restores the markers, the specs, and the cross-references. It does not restore
operating preferences or calibration — those live in tier 3 and stay private.
