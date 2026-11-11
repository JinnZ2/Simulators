Status: implemented experimental, offline publication-to-claim capture-binding audit with constructed controls and adapted preserved-specimen challenges. It does not authenticate publishers, establish semantic fidelity, or enforce a mandatory gate in the parent `assess.py`.

# Publication-to-claim provenance audit

The question is bounded: does this claim, rendered in this declared way, bind
to this selected passage in this hash-bound material under the supplied
publication and material-access declarations? The report keeps known
differences alongside unresolved fields, rather than converting either into
a verdict about the paper, model, or user.

## Contract and separate outcomes

- **Identity declarations:** compare identifier, title, authors, and version.
  Outcomes are `CONSISTENT_DECLARATIONS`, `DECLARATIONS_DIFFER`, and
  `UNRESOLVED`, with each field retained. A known difference survives alongside
  unknown author or version fields. Literal differences are not proof of
  different real publications; abbreviations, spelling variants, author
  order, and aliases require review rather than automatic reconciliation.
- **Material integrity:** compare the supplied SHA-256 with explicit local
  bytes, then decode strict UTF-8. A missing file, unknown expected hash,
  changed bytes, or unreadable text remains separately identifiable.
- **Material access:** compare the selected capture with explicit
  `materials_held` IDs. An empty list means no captures declared held;
  `UNDECLARED` means access is unknown. A reviewer possessing a file does not
  establish that the original assessor possessed it.
- **Location:** select a nonempty, in-bounds `[start, end)` span of Unicode
  codepoints in that same hash-bound file. A human-readable label records the
  locator's intended role; its semantic accuracy is not automatically tested.
- **Rendering:** an explicit `QUOTATION` requires exact text at that span,
  including punctuation, case, spacing and Unicode. A declared `PARAPHRASE`
  remains in need of semantic review even if the text happens to match.
  Missing rendering is not silently assumed to mean quotation.
- **Other-capture hints:** an exact occurrence in another supplied, hash-bound
  capture is recorded as a possible lead, without changing the selected
  source, location, identity, or original assessment.

Each claim derives one narrow binding state while retaining all component
outcomes:

| State | Meaning within this audit |
|---|---|
| `BOUND_TO_DECLARED_CAPTURE` | All implemented checks agree for the supplied declarations and selected passage |
| `INCONSISTENT_BINDING` | At least one known declaration, access, hash, span, or quotation difference; unknowns remain alongside it |
| `UNRESOLVED_BINDING` | No known difference established, but at least one prerequisite is unresolved |

`BOUND_TO_DECLARED_CAPTURE` is not `SUPPORTED`, publication authentication,
semantic equivalence, author endorsement, physical adequacy, or permission to
act. A common method described in a paper can still appear in quoted prior
work, a reference list, or a criticism; the exact-match check cannot resolve
those roles. Numerical equality and correct citation syntax do not remove
these limits.

## Inputs

The input schema is `study-aperture/publication-claim-bundle/1`. Supply:

- `publication`: expected `identifier`, `title`, `authors` and `version`.
  Missing values remain unresolved; author names may be an ordered string
  list or an explicitly declared string. No author expansion or identifier
  normalization is invented.
- `captures`: uniquely identified local files, each with its declared
  publication metadata, relative `path` and expected lowercase `sha256`.
  Additional source URL, material kind, acquisition and selection metadata
  are retained. A hash and URL are not publisher authentication.
- `materials_held`: explicit capture IDs, an empty list, or `UNDECLARED`.
  This describes the assessment being audited, not the reviewer's current
  filesystem access.
- `claims`: unique IDs, `text`, `rendering`, selected `capture_id` and a
  `location` object containing integer `start`, `end`, and a nonempty `label`.
  Missing text, rendering, capture or location remains unresolved.
- `provenance`: selection decision, conditions and remaining uncertainty.
  Omitted condition fields are explicitly listed as undeclared. Original
  records, support labels and decisions can be retained as data, never run
  as instructions or used to authorize a result.

Only declared paths within the explicit bundle directory are read.
Absolute paths, parent-directory escapes, and escaping symlinks are rejected.
Duplicate IDs, duplicate JSON keys, boolean offsets, nonfinite values and
unsupported schemas are input errors, not scientific findings.

## Run and inspect

From the repository root:

```sh
python3 -m experimental.publication_provenance.audit \
  --bundle /path/to/bundle.json \
  --output-dir /tmp/publication-binding-new

python3 -m experimental.publication_provenance.demo \
  --output-dir /tmp/publication-binding-demo-new

python3 -m unittest discover -s tests -p 'test_publication_provenance.py' -v
./run_checks.sh
```

The demo generates 22 constructed control reports and four explicitly adapted
C1 challenges from the preserved assessment specimens. It writes each full
bundle, original selected record, capture declarations, content hashes,
source locations, differences, unknowns and unchanged supplied annotations
inside the JSON report. The markdown report exposes the separate outcomes
and selected declarations. Output directories must be fresh; earlier runs
are not overwritten.

Reports identify the procedure version, audit-module source SHA-256 and Python
version. These selected-source fingerprints are not runtime integrity or full
environment attestation; they do not detect arbitrary in-memory monkeypatches.

Each case directory also contains a portable `bundle.json` and its explicitly
declared source files; the single-bundle CLI can replay it without relying on
the original scratch directory. `evidence.json` retains every full report,
while `index.md` and `index.json` summarize the cases without calling their
status labels test results.

Exit 0 means the report was written, including reports of inconsistent or
unresolved bindings. Exit 2 means invalid input or I/O failure. Neither a
zero exit nor the demo's report count is a test result; test assertions and
their independent expected matrix supply the diagnostic regression evidence.

## Preserved specimens and excerpts

The originals in
`audits/gemini-assessment-records-2026-11-11/` remain unchanged. The adapter
checks their recorded byte hashes, extracts the supplied C1 wording, retains
the entire source record, and records its own explicit selection map.
Abbreviated author attributions in the originals are retained without expansion.
Captured author lists, original versions, and per-capture access are not invented.

Four selected, reviewer-transcribed passages are pinned separately. They are
not raw HTTP captures, full-paper snapshots, or evidence of the original
assessor's access:

| File | Selected source location |
|---|---|
| `examples/review-excerpts/bias.txt` | The “We provide that audit” sentence in the [demographic-bias abstract](https://arxiv.org/abs/2611.00496) |
| `examples/review-excerpts/agency.txt` | The host/sandbox UDS sentence in [Agency §4.1](https://arxiv.org/html/2611.12122v1) |
| `examples/review-excerpts/rl.txt` | The opening sentence of the [RL-misalignment abstract](https://arxiv.org/abs/2611.12865) |
| `examples/review-excerpts/stopping.txt` | The correct-intermediate-answer sentence in [early stopping §6](https://arxiv.org/html/2611.00166v1) |

The adapted comparisons test those selected spans, not absence of a claim
throughout an entire publication. In particular, a quotation difference does
not establish that the underlying proposition is wrong: the source review
already retains substantiated Agency details and the substantive
early-stopping finding.
([Preserved source review](https://github.com/JinnZ2/study-aperture/pull/25))
The constructed positive controls independently demonstrate usable exact
bindings; the four adapted cases are not an estimate of model reliability.

## This does not

- **Authenticate a publisher or model session:** supplied identity metadata,
  URLs, capture receipts and matching hashes can all be consistently wrong.
- **Judge meaning or scientific support:** paraphrase fidelity, author
  endorsement, measurand scope, causal validity and physical adequacy require
  additional inspection.
- **Authorize diagnostics or action:** every result explicitly leaves claim
  support and physical adequacy `NOT_ASSESSED`, and design checks,
  independence and deployment `NOT_AUTHORIZED`.
- **Repair an original record:** possible donor matches remain hints; the
  original identity, quotation, support and decision stay inspectable.
- **Change parent enforcement:** this is an explicit audit API and CLI, not
  an automatic import, new parent support state, or mandatory `assess.py`
  ingestion rule. A parent assessment that never calls this audit is not
  retroactively source-verified. No source-authentication guarantee is added
  to the equation library or its diagnostic certificates.
- **Guarantee atomic recovery from disk failure:** existing directories are
  refused; a low-level write failure can leave a partial new directory.
  Preserve it as a failed attempt and use a fresh directory for a retry.

The library remains stdlib-only and offline. It follows explicit declarations
and preserves the conditions under which this particular binding was tested,
without forcing mathematical descriptions or studies into a universal rank.
