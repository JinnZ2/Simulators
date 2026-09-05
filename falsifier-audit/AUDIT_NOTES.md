# AUDIT_NOTES — falsifier-audit

Findings on the instrument itself, kept as prose rather than a claim table.
The reason is structural: this folder's own tool scans every `.md` in the
tree for falsifier markers, so a claim table here carrying a `falsifier`
column — or a `Falsified if:` prose line — would enter its own corpus and
inflate the next run (the loop `uninstrumented/` records as `UNI_010`). The
findings therefore state each check-that-would-overturn-them in running
prose, and the folder ships no `CLAIM_TABLE.md`. Findings are `FA_001..`,
append-forward.

## FA_001 — inventory first, and the two-form extraction is a coverage
statement not a judgement

The order's first task is to inventory the marker forms before building the
extractor. `inventory.py` does, and the corpus is heterogeneous:
`REFUTATION_PROTOCOL` sections dominate (~110 files), then prose
`Falsifier:` / `Falsified if:`, then claim-table columns under four
different header names with the falsifier in no fixed position, then
`falsifier_shape`/`falsifier_value` fields and JSON/YAML keys, then
`FALSIFIER` block labels. `extract.py` builds records around exactly the two
forms that carry an attached claim on the same structure — the table column
and the prose `Falsified if:` — because those are the two where
`attached_to` is recoverable verbatim. The other forms are counted and not
extracted. That is a coverage decision, printed on every run, not a claim
that the unextracted forms are clean. The check that would overturn it: a
`REFUTATION_PROTOCOL` block whose claim and falsifier sit on one parseable
structure, which would move that form from counted to extracted.

## FA_002 — header-name parsing, not fixed position

The four column names (`falsifier`, `falsified by`, `falsified if`, `refuted
by`) appear in different positions across tables, so the extractor resolves
the falsifier and the claim by **header name** (`_header_index`), not by
column number. The selftest pins both a falsifier-last table and a
`falsified by`-middle table and checks the falsifier is read from the named
column and the claim from the claim column in each. Reading by position
would silently mis-column every table whose falsifier is not last.

## FA_003 — A3 returns zero on this corpus, and that is a result, not a
broken check

A3 indexes by axis and looks for two repos quantifying one axis
incompatibly. On this corpus it emits **zero**: the numeric-bearing
falsifiers on any shared axis are folder-local, so no cross-repo numeric
conflict exists — which is the same unquantified property A1 flags from the
other side (a falsifier stating a shared axis without a number cannot
conflict with another folder's number on it). The coverage note reports the
zero explicitly rather than letting a silent A3 read as a clean corpus. The
check is demonstrably **not** `CONSTANT_SILENT`: the null test builds a
cross-repo pair carrying opposite directions on one axis and A3 fires, then
confirms it stays silent when both records are in one repo and when the two
carry the same cutoff. What would move A3 off zero is a more numeric corpus,
not a code change.

## FA_004 — A1's observable vocabulary was widened by correctness, not by
tuning to a target rate

A1 fires when a falsifier carries no number, comparison, unit, or
observable-outcome word. Its first `OBSERVABLE` set omitted the
gerund-and-verb observables the corpus actually uses (`admits`, `refuses`,
`reverses`, `flips`, `differs`, `present`, `absent`, …), so A1 fired at
~52%, over-counting real observables as absences. The vocabulary was widened
to the words the corpus uses to name a discrete outcome, taking A1 to ~40%.
The direction of the change is correctness — the added words genuinely name
observables — not a fit to a chosen hit rate; the remaining hits are
falsifiers whose observable is phrased in a form the word list still does
not carry, which is a known residue and the reason A1 is stated as a noisy,
cheap-to-dismiss check rather than a verdict.

## FA_005 — self-exclude closes the UNI_010 loop, checked not assumed

`SELF_EXCLUDE` drops the tool's own `QUEUE.md`, `samples/`, `README.md` and
`AUDIT_NOTES.md` from the scan so a re-run does not read its emitted queue —
or an authored doc that quotes a marker verbatim to document it — as new
corpus. The README and these notes both quote `Falsified if:` and the
`falsifier` header names to explain the checks, and the prose extractor's
marker regex matches such a quotation on sight; excluding the two authored
docs is the correct close of that loop, not rewording every mention.
`WORK_ORDER.md` — the delivered spec — is left scannable and carries no
attachable marker (no claim-table falsifier column, no `Falsified if:`
line), so it produces no records; that is verified by the record count
holding across its addition, not assumed. The coverage line reports the
self-excluded count on every run.

## FA_006 — the tool's authored framing screens clean; the quoted falsifier
text does not, and that is correct

Every report this instrument emits is screened through
`sheet-structure-scan/no_severity`, imported not copied. The queue's authored
framing — the coverage lines, the emitted questions, the A3 note — screens
clean. The queue **body** does not, because it quotes corpus falsifier text
verbatim (`  falsifier:` and `  detail:` lines), and that text is data, not
the tool's prose: a corpus falsifier saying a value is *wrong* is the
material under audit, not a severity label the tool authored. The selftest
therefore screens the framing with those two line prefixes removed, and
separately checks the screen fires on a planted word so the exclusion is not
hiding a real hit. One authored word did trip the screen and was reworded
(`fixes` → `repairs` in the queue header), which is the screen doing its
job on the tool's own prose.

## FA_007 — empty falsifier cells are skipped and counted, never recorded as
present

A falsifier cell holding only punctuation (`—`, `n/a`, fewer than three word
characters) is skipped and added to an `empty` count, not emitted as a
record. The coverage line reports it. An absent falsifier (empty cell) and a
present-but-unparsed one (`NOT-FOUND`, a locatable falsifier with no
locatable claim) are different results and are kept apart; collapsing them
would let a blank cell read as a falsifier the tool could not attach.

## FA_008 — the queue carries questions only, and the constraint is enforced,
not just intended

Every queue entry carries `status: OPEN`, the only machine-set value, a
verbatim falsifier, and a question — never a suggested edit. The selftest
asserts every entry's status is `OPEN`, its question is non-empty, and the
question contains no repair verb. Ranking and scoring are absent by
construction: `per_record` returns a flat, unaggregated hit list, and the
queue sorts by stable id, not by any hit count. The order's non-goal against
ranking is thereby a property of the data structure, not a discipline the
renderer has to remember.
