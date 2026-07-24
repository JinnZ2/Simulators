# SPEC — drift mesh: entrain.py + syndrome.py + divlog.py

CC0. stdlib only. Phone-buildable. No third-party deps, no network, no config files.
Clients: clock.py (registry), echo.py, modes.py, scaffold.py, revalidate.py.

## 0. WHAT THIS IS

Three structurally different checks on the same target. Degenerate, not redundant:
each catches a failure the others cannot see. None outranks the others.

    TRACE     vertical    module reading  vs  primary reference     (metrology)
    PARITY    horizontal  module reading  vs  peer module reading   (syndrome)
    PHASE     temporal    time since each module last re-read ref   (zeitgeber)

Full mesh, 3x3: every axis self-checks, cross-checks peers, traces to primary.
A disagreement between any two cells is a SYNDROME. Syndromes are LOGGED, never
resolved. Nothing in this spec picks a winner.

## 1. HARD INVARIANTS — violate any and the build is wrong

    I1  No axis is supreme. No scoring function combines axes into one number.
    I2  Comparisons NEVER cross clock targets. claim / mode_sensitivity /
        independence are separate meshes. Cross-target comparison is the
        category error already rejected in clock.py.
    I3  PARITY reads CHECKSUMS, not content. It locates divergence without
        reading the claim. Quantum syndrome discipline; also the
        no-interior-verdicts boundary.
    I4  Missing input goes LOUD + UNDETERMINED. Never silent-default, never
        assume agreement from absence.
    I5  The log is APPEND-ONLY. No entry is ever edited or deleted. A resolved
        divergence is a NEW entry referencing the old one, not a mutation.
    I6  No auto-resolution. No entry field named `winner`, `correct`, `cause`,
        `severity`, or anything carrying a verdict or an interior state.
    I7  Every timestamp is an explicit argument. No implicit now(), no
        implicit present tense. Same rule as clock.py.
    I8  Modules keep NO private copy of the reference. They hold a
        reference VERSION and a last_entrained timestamp, and re-read.

## 2. entrain.py — the zeitgeber

Peripheral oscillators run free between pulls. They are not forced into lockstep;
they are pulled back on a schedule.

    @dataclass
    class Peripheral:
        name: str                       # "scaffold", "revalidate", "echo"
        entrain_interval_days: float    # how often it must re-read primary
        last_entrained: Optional[str]   # ISO date, None = never
        ref_version: Optional[str]      # version of primary it last read

    PERIPHERALS: Dict[str, Peripheral]
    register_peripheral(p)              # the door

    def reference_version() -> str
        # deterministic fingerprint of the CURRENT primary state:
        # sorted clock.CHANNELS keys + their targets, sorted clock.VOLATILITY
        # keys + span_days. Stable hash (hashlib.sha256, first 12 hex).
        # Changing a channel or a volatility class CHANGES this string.
        # That is the point: it makes silent registry edits visible.

    def phase(name, now) -> Phase
        # days_since_entrained, interval, and one of:
        #   ENTRAINED    within interval AND ref_version matches current
        #   FREE_RUNNING within interval BUT ref_version is stale
        #                -> the reference moved under it; pull is now DUE
        #                   regardless of schedule
        #   DRIFTED      past interval
        #   NEVER        last_entrained is None  -> LOUD, UNDETERMINED
        # never returns a number that can be averaged with another axis

    def entrain(name, now) -> Phase
        # records the pull: sets last_entrained=now, ref_version=current.
        # DOES NOT change the module's readings. Entraining is re-reading the
        # reference, not overwriting anyone's answer.

## 3. syndrome.py — parity between peers, without reading content

    @dataclass
    class Reading:
        module: str
        target: str            # MUST be one of clock target names
        subject: str           # what was read (claim id / mode name / anchor id)
        band: Optional[str]    # FRESH / DECAYING / STALE / EXPIRED / UNDETERMINED
        governing: Optional[str]   # which channel governed, or None
        inputs_digest: str     # sha256[:12] of the SORTED (key, value) pairs of
                               # the inputs used. NOT of the claim content.
        as_of: str             # when this reading was taken (explicit)

    def digest(inputs: dict) -> str
        # canonical: sorted keys, repr of values, None rendered as "None"
        # so a missing input is part of the fingerprint, not invisible

    def parity(a: Reading, b: Reading) -> Optional[Syndrome]
        # RAISE if a.target != b.target                        (I2)
        # RAISE if a.subject != b.subject
        # returns None when bands match AND digests match
        # otherwise a Syndrome with `kind`:
        #
        #   SAME_INPUTS_DIFF_BAND   digests match, bands differ
        #                           -> the two modules disagree about the SAME
        #                              facts. This is a real divergence.
        #   DIFF_INPUTS_DIFF_BAND   digests differ, bands differ
        #                           -> may just be different inputs. NOT
        #                              evidence of module disagreement. Logged
        #                              separately so it never masquerades as one.
        #   DIFF_INPUTS_SAME_BAND   digests differ, bands match
        #                           -> agreement that is not evidence of
        #                              agreement. Logged. (Homoplasy analogue:
        #                              convergent, cheap.)
        #   MISSING                 either band is UNDETERMINED -> LOUD
        #
        # NOTE: parity never opens the claim. It compares two 12-char digests
        # and two band labels. That is the whole of it.

    def trace(r: Reading, now) -> Optional[Syndrome]
        # vertical check: recompute the reading by calling clock.decay directly
        # from primary, compare to r.band. Divergence here means the module's
        # own copy of the logic has drifted from the registry.
        # kind: TRACE_DIVERGENCE

    def mesh(readings: List[Reading], now) -> List[Syndrome]
        # every pairwise parity within a target, plus trace for each,
        # plus phase for each module's home peripheral.
        # returns a flat list. no aggregation, no count-as-score.

## 4. divlog.py — the append-only divergence log

This is the piece that turns a list of problems into a baseline.

    @dataclass(frozen=True)
    class Entry:
        observed_at: str            # explicit now
        target: str                 # claim / mode_sensitivity / independence
        subject: str
        axis_a: str                 # module or axis name
        axis_b: str                 # peer, or "PRIMARY" for a trace check
        kind: str                   # the Syndrome kind, verbatim
        band_a: Optional[str]
        band_b: Optional[str]
        digest_a: str
        digest_b: str
        governing_a: Optional[str]  # which channel drove each side
        governing_b: Optional[str]
        ref_version: str            # what primary was at the time
        phase_a: Optional[str]      # ENTRAINED/FREE_RUNNING/DRIFTED/NEVER
        phase_b: Optional[str]
        supersedes: Optional[str]   # id of a prior entry this one revisits
        note: str = ""              # operator field. free text. never parsed.

        # id = sha256[:12] of all fields except note.
        # NO verdict fields. See I6.

    STORAGE: newline-delimited JSON, one Entry per line, file path passed in.
             Never rewritten. Append with open(path, "a").

    def append(path, entry) -> str            # returns id
    def load(path) -> List[Entry]
    def history(path, target, subject, axis_a, axis_b) -> List[Entry]
        # the same pair, same subject, time-ordered. THE baseline query.

    def residual(entries: List[Entry]) -> Residual
        # classify the SHAPE of the disagreement history. Not its severity.
        #
        #   NEW           len < 2                 -> no baseline yet
        #   FLAT          same kind, same band pair, across all entries
        #                 -> stable offset. calibration, not signal.
        #   WALKING       band pair changes monotonically across entries
        #                 (FRESH->DECAYING->STALE...)  -> real drift
        #   INTERMITTENT  appears, clears, reappears  -> neither; log more
        #   WIDENING      count of distinct governing channels grows
        #                 -> divergence is spreading to new mechanisms
        #
        # Residual carries the classification AND the entry ids it read.
        # It NEVER says which side is right.

## 5. TEST CASES — build is not done until these pass

    T1  parity() raises on cross-target comparison                        (I2)
    T2  two modules, identical inputs_digest, different band
        -> SAME_INPUTS_DIFF_BAND, logged, no winner field anywhere
    T3  two modules, different digest, different band
        -> DIFF_INPUTS_DIFF_BAND, NOT classified as module disagreement
    T4  agreement with different digests -> DIFF_INPUTS_SAME_BAND is LOGGED,
        not silently dropped
    T5  peripheral never entrained -> phase NEVER, LOUD, UNDETERMINED       (I4)
    T6  register a new clock channel -> reference_version() changes ->
        every peripheral inside its interval flips to FREE_RUNNING          (I8)
    T7  same pair logged 3x with identical bands -> residual FLAT
    T8  same pair logged 3x with FRESH/DECAYING/STALE -> residual WALKING
    T9  one prior entry -> residual NEW (no baseline claim from n=1)
    T10 append never mutates: load() after two appends returns both, in order
    T11 grep the source: no field or return key named winner/correct/cause/
        severity/score/rank                                                (I6)
    T12 no implicit now(): grep for datetime.now / date.today -> zero hits  (I7)

## 6. BUILD ORDER

    1. divlog.py     (no deps beyond stdlib; testable alone)
    2. entrain.py    (imports clock)
    3. syndrome.py   (imports clock, entrain, divlog)
    4. THEN: make scaffold.py and revalidate.py peripherals — register them,
       strip their private clock assumptions, have them emit Reading objects.
       This is open-queue item 5 and it is the reason this spec exists.

## 7. DO NOT BUILD

    - a dashboard, a score, a health percentage
    - any function that resolves a syndrome
    - any default value for a missing input
    - rows, tables, or field content of any kind — that is operator input
    - a fourth band NOT_APPLICABLE: still open, decide before it is assumed
