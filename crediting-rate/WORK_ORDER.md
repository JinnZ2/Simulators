=====================================================
WORK ORDER L — crediting_rate.py
target: Fable / Claude Code
repo:   sims repo
        (consumes method-layer:
         F branch_set, G return enum)
        stdlib only, phone-buildable, CC0
=====================================================

PURPOSE
  Test whether attribution of an
  imported technique tracks
  CONTRIBUTION or tracks whether the
  loanword survived into the
  receiving language.

  Not an argument about any single
  case. A rate comparison across
  bins.

=====================================================
UNIT
=====================================================
  technique-transmission event
    (item, source_tradition,
     receiving_tradition,
     first_attested_source,
     first_attested_receiving)

  REQUIRE first_attested ordering
  from published sources only.
  Ordering unknown → EXCLUDED and
  counted, not estimated.

=====================================================
BINS (independent variable)
=====================================================
  loanword_retained      0/1
      receiving-language term
      still carries the source
      etymology
      (algebra, algorithm, zero,
       alcohol, alkali — retained)
      (paper, printing, compass,
       inoculation, terracing —
       not retained)

  ambiguous → own bin, not
  assigned

=====================================================
DEPENDENT MEASURES
=====================================================
  crediting_rate
      fraction of general-reference
      sources naming the source
      tradition in the item's
      primary description

  attribution_depth
      0 = unnamed
      1 = named in passing
      2 = named as origin
      3 = named with mechanism of
          transmission

  origination_vs_absorption
      as CODED FROM the attested
      ordering, not from the
      narrative
      → flags cases where the
        receiving tradition is
        described as originator
        while ordering says
        otherwise

=====================================================
SOURCE FRAME (must be declared)
=====================================================
  code crediting from general-
  reference corpora, NOT specialist
  history of science
    rationale: specialists credit
    correctly; the claim is about
    the POPULAR prior, which is
    also the training prior
  declare corpus, edition, date
  → the frame is a parameter, and
    running a second frame is the
    replication

=====================================================
NULLS (all four, before any real run)
=====================================================
  N1  MAIN — shuffle
      loanword_retained across
      items, recompute crediting
      rate. Observed gap inside
      null band → UNKNOWN_measurable

  N2  antiquity — older items may
      be credited less regardless
      of loanword. Control on
      first_attested_source date.

  N3  domain — mathematics vs
      materials vs medicine may
      differ in citation
      convention. Report per
      domain; a gap present in
      only one domain is a domain
      result, not the claim.

  N4  transmission-path length —
      items passing through more
      intermediaries may lose
      credit for path reasons.
      Code intermediary count.

=====================================================
BLIND CODING (required)
=====================================================
  crediting/attribution coded
  WITHOUT the coder seeing the
  loanword bin
  → two files, joined only after
    both are complete
  → this is the substitute for a
    neutral coder; neither author
    is one

=====================================================
RETURN TYPE (G enum)
=====================================================
  ETYMOLOGY_TRACKING(gap, CI)
  CONTRIBUTION_TRACKING(gap, CI)
  UNKNOWN_measurable(reason)
  BLOCKED(insufficient_attested_ordering)
  DOMAIN_SPECIFIC(domain, gap, CI)

=====================================================
PRE-STATED PREDICTION (record before run)
=====================================================
  crediting_rate(retained) >
  crediting_rate(not_retained)
  → i.e. credit tracks the
    surviving word, not the
    contribution

  stated now so it cannot be
  fitted afterward

=====================================================
BRANCH SET (emit to F)
=====================================================
  origin_pattern:
    "single-origin account of
     scientific method"
  branches:
    etymology_retention_artifact
    volume_of_record_artifact
      (→ [[archive-siting-bias]],
         same signed-bias structure)
    genuine_contribution_difference
    citation_convention_artifact
  discriminator: crediting rate
    across loanword bins with
    ordering held
  cost: low — published reference
    sources only
  predicts_elsewhere:
    proxy archive siting
    (different domain, same
     preservation-weighting
     mechanism)
