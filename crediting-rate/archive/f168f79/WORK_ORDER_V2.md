═══════════════════════════════════════════
DISPATCH L — crediting_rate (REVISED 2026-09-23)
TARGET: Claude Code
REPO: JinnZ2/Simulators, folder crediting-rate/
stdlib only, CC0, phone-buildable
BUILD ON CONSTRUCTED DATA. Real run NOT_RUN.
Same F/G check-first as K.
═══════════════════════════════════════════

PURPOSE
  Does attribution of an imported technique track CONTRIBUTION
  or LOANWORD VISIBILITY? Rate comparison across bins. Not an
  argument about any single case.

UNIT
  transmission event: item, source_tradition,
  receiving_tradition, first_attested_source,
  first_attested_receiving, intermediary_count, domain,
  frame_source
  ordering from published sources only; unknown →
  EXCLUDED and counted.

BINS — REVISED, three states on VISIBILITY to a general reader
  visible          etymology legible (algebra, algorithm, alkali)
  technical_only   retained but opaque (sine: jyā → jība →
                   jaib → sinus)
  not_retained     (paper, compass, inoculation, terracing)
  ambiguous        own bin, never assigned

REVISION 1 — SAMPLING FRAME (new hard gate)
  every item carries frame_source.
  visible/technical_only CAN be enumerated from language side
    (etymological dictionaries).
  not_retained CANNOT — no linguistic index exists because the
    word did not survive. Must come from TECHNIQUE side
    (transmission catalogues).
  RULE: all bins drawn from the SAME side (technique-side for
  all), or the run returns FRAME_ASYMMETRIC and stops.
  An asymmetric frame produces the predicted gap by construction.
  RULE: no item list authored by a model. A model-drafted list
  samples the training prior, which is the measurand. Item list
  field model_authored=True → CONTAMINATED_FRAME, stop.

REVISION 2 — CODING SPLIT BY JUDGMENT LOAD
  the item name carries its own bin; any coder who knows the
  etymology sees it. Blind coding as specified cannot hold.
  crediting_rate     MECHANICAL: tradition-name string match in
                     first N sentences of primary description.
                     N in data file. Leak harmless — no judgment.
  attribution_depth  0 unnamed / 1 passing / 2 origin /
                     3 origin + transmission mechanism
                     coded with item name REDACTED from entry.
                     Two files, joined after both complete.
  origination_vs_absorption  coded from attested dates only,
                     never from narrative.

SOURCE FRAME (declared parameter)
  general-reference corpora, not specialist history — the claim
  is about the popular prior, which is also the training prior.
  declare corpus, edition, date. Second frame = replication.

NULLS (all before any real fit)
  N1 shuffle bin labels across items → observed gap inside band
     → UNKNOWN_measurable
  N2 antiquity: control first_attested_source date
  N3 domain: report per domain; one-domain gap → DOMAIN_SPECIFIC
  N4 path length: control intermediary_count
  NOTE: N2/N4 likely correlate with bin (retained items cluster
  via Arabic transmission, ~8th–12th c). Report the correlation
  before fitting.

RETURN
  ETYMOLOGY_TRACKING(gap, CI)
  CONTRIBUTION_TRACKING(gap, CI)
  UNKNOWN_measurable(reason)
  DOMAIN_SPECIFIC(domain, gap, CI)
  BLOCKED(insufficient_attested_ordering)
  FRAME_ASYMMETRIC
  CONTAMINATED_FRAME

PRE-STATED PREDICTION (record in README before any run)
  crediting_rate(visible) > crediting_rate(technical_only)
    >= crediting_rate(not_retained)
  technical_only is the discriminating bin: word survived,
  reader can't see it. If it tracks not_retained, visibility
  is the variable; if it tracks visible, retention is.

CONSTRUCTED FIXTURES (planted faults must fire)
  F1 etymology-tracking world    → ETYMOLOGY_TRACKING
  F2 contribution-tracking world → CONTRIBUTION_TRACKING
  F3 mixed-side frame            → FRAME_ASYMMETRIC
  F4 model_authored item list    → CONTAMINATED_FRAME
  F5 antiquity-confounded world  → gap vanishes under N2

REAL-RUN SPEC (README, do not run)
  open item: a technique-side transmission catalogue to draw
  ALL bins from. Unidentified. This is the one piece needing a
  human with library access.

BRANCH SET
  origin: "single-origin account of scientific method"
  branches: etymology_retention_artifact /
    volume_of_record_artifact (→ archive-siting-bias) /
    genuine_contribution_difference /
    citation_convention_artifact

DELIVERY — same as K
═══════════════════════════════════════════
