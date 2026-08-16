# uninstrumented

CC0-1.0. Public domain.

Cases where a quantity exists and the instrument's constitution
prevents it from appearing.

Not a gap log. A gap is an oversight. These are exclusions built
into the apparatus before the first reading is taken.

Every entry is a QUESTION until something measures it. Nothing
here is a position under defense. Test fit, extend it, or report
where it breaks.

## Entry structure

    QUANTITY       what would be measured
    EXCLUDED BY    what in the instrument's constitution
                   prevents it
    VISIBLE AS     how the absence currently reads
    WOULD MEASURE  the design, if one exists yet
    CONFIDENCE     gradient, stated separately from the shape

## Exclusion mechanisms

    MODALITY             apparatus in the wrong channel
    STORAGE              medium cannot hold the shape
    SCALAR DEMAND        function collapsed to a number
    BUDGET BOUNDARY      closed budget compared to open
    AUTHORED REFERENCE   reference produced by the measured party
    PROXY SUBSTITUTION   enforceable measure displaces the target
    AUDIT ASYMMETRY      guard fires on one side only
    SCORED AS WASTE      component read as cost by the
                         instrument's own accounting

Sort by mechanism, not by field. That is what lets a case from
evolutionary biology sit next to one from survey methodology and
be recognizably the same failure.

## scan.py

Searches text for the signature of an exclusion, not for topics.

    python3 scan.py docs/
    python3 scan.py --mech "SCORED AS WASTE" docs/
    python3 scan.py --asym transcripts/
    python3 scan.py --jsonl hits.jsonl docs/

Highest-yield sources: limitations sections, standards documents,
regulatory text, abstracts. Limitations sections are the richest,
because authors state the exclusion themselves and then proceed.

Most hits are noise. That is the design. Triage is the human step.

## Added, not delivered

    python3 uninstrumented.py   the register as code, three checks on it
    python3 scan_audit.py       grades scan.py + patterns.json

See [`AUDIT_NOTES.md`](AUDIT_NOTES.md) and
[`CLAIM_TABLE.md`](CLAIM_TABLE.md).

## Note on the prior literatures

Each mechanism has a partial literature -- Goodhart and Campbell
for proxy substitution, Polanyi for storage, STS for undeclared
frames, symptom-dismissal work in medicine for affect routing.
None of them cite each other. The cross-domain shape is not
visible from inside any one of them.

Some things are absent because they are wrong. The filter is not
only removing signal. That is why the entries stay questions.
