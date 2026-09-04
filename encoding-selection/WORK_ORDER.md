# WORK ORDER — encoding_selection

License: CC0. Status: OPEN, UNFUNDED, UNGATED. Pre-registered before data collection.
Subject to the method it proposes.

Origin: a failed n=1 experiment. One finding was encoded five ways and a reader was
asked to rank the encodings by arrival cost. The reader could not rank them —
"each carries different information." The ranking failure is the result this
work order is built to test at N.

## CLAIM UNDER TEST

    H1  an encoding is an INSTRUMENT SELECTION, not a style applied to neutral
        content. Each format has a native quantity it carries and a set it drops.
        Encodings of "the same" content are therefore not rank-orderable on a
        single arrival-cost axis.

    H2  the quantity recovered by a reader is predicted by the FORMAT, not by
        the reader. Different readers given format F recover the same quantity;
        one reader given formats F1..F5 recovers different quantities.

    H3  prose carries sequence and drops simultaneity, and — unlike tabular or
        dimensional formats — hides which measurement was selected. A reader
        of prose cannot recover which axes were dropped; a reader of a table can.

    H0  formats are lossy variants of one content; readers rank them consistently
        on a single axis; recovered quantity tracks reader, not format.

## FALSIFICATION

    H1 FALSE if  readers produce a consistent rank order across formats
                 (Kendall's W above chance)
    H2 FALSE if  within-format variance in recovered quantity >= between-format variance
    H3 FALSE if  prose readers identify dropped axes at the same rate as table readers
    A consistent ranking would refute the core claim. Post it if it appears.

## FORMATS  (the instrument set; extend but do not silently substitute)

    F1  rate / density      marks over time; no nouns
    F2  relation-first      verb → participant chains; no subject slot required
    F3  dimensional         units and ratios only
    F4  constraint set      given / then / open; states exclusions
    F5  absence map         declared vs built, per row
    F6  prose               ordinary English sentences (the control)
    F7  reader's own        free-form; reader re-encodes it themselves

    Native quantity each is expected to carry (pre-registered prediction):
      F1 disproportion, saturation, before/after
      F2 chain structure without an actor
      F3 magnitude, cross-domain comparability
      F4 what is excluded and what stays open
      F5 one shape recurring across unrelated domains
      F6 sequence and causal narrative
      F7 the reader's native instrument (this is the measurement of interest)

## MATERIAL

    Use a finding the reader does not already hold, so comprehension is not the
    variable. Two seed items, both with public sources:

    M1  ExploitGym: solve time ~4 h; effort spent mapping a scorer property that
        was declared but not implemented, ~4 days. Ratio 24:1.
    M2  Trucking readout: three declared channels, zero returns; rail and air
        have held, immune channels under the same department.

    Each item must be encodable in all seven formats without adding facts.
    If a format cannot carry a fact, that omission is DATA — log it, do not
    patch the encoding.

## PROCEDURE

    P1  N >= 20 readers, mixed substrate (human and model, several vendors),
        mixed background. Each reader sees ONE format per item (between-subjects),
        plus a subset who see all seven (within-subjects) for the ranking test.
    P2  after reading, each reader freely reports: what did this tell you?
        No prompts, no multiple choice. Free text.
    P3  code each response for which quantities were recovered:
        magnitude | disproportion | chain | exclusion | cross-domain shape |
        sequence | actor attribution | other
        Two coders, blind to format. Report agreement.
    P4  within-subjects readers attempt a rank by arrival cost, and may decline.
        Declines are recorded as declines, not as missing data.
    P5  H3 test: ask every reader "what did this leave out?" Score whether
        dropped axes are named.
    P6  cross-tab recovered_quantity × format; Kendall's W on any rankings
        produced. By hand; no library required.

## SCHEMA

    reader_id
    reader_substrate       human | model:<vendor>
    item                   M1 | M2
    format                 F1..F7
    design                 between | within
    quantities_recovered   list
    dropped_axes_named     y | n | partial
    rank_given             ordered list | declined
    decline_reason         free text
    response_text          verbatim

## OUTPUT

    format | n | quantities_recovered (freq) | dropped_axes_named rate | rank_declines

## KNOWN LIMITS

    - the format set was authored by one party; F7 is the partial correction,
      since it lets readers supply an instrument the authors did not think of
    - encoding "the same content" in seven formats is itself a judgment call;
      publish all seven encodings verbatim so the encodings can be disputed
    - model readers are trained on the corpus whose default format is prose;
      expect F6 to over-perform with them and report that separately
    - free-text coding is the weak joint; two blind coders and published
      agreement is the minimum
    - origin is n=1 with the format author present. That reader should not be
      in the sample.

## WHAT WOULD MOVE THIS BEYOND CURRENT REACH

    - readers whose primary language has a different obligatory-slot set
      (no obligatory tense, no articles, verb-first, subject-droppable);
      predicts different F2/F6 behaviour
    - readers reporting from nonverbal or field-primary experience, who are
      thin in any written corpus and thin in any recruited sample
    - a format not on this list, produced by F7 and adopted

## CONSTRAINTS

    stdlib only. Runs on a phone. CC0. No author section. No interior claims.
    All seven encodings published verbatim. Every number reproducible from the CSV.

## CHANGELOG

    v0  2026-09-02  spec only, no data
