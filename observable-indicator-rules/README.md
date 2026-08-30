# observable-indicator-rules

Notification is a dependency chain — someone upstream detects, decides,
sends, and the channel reaches in time, and every link is outside the
household's control. This spec inverts it: run the coupled chain solve
once, offline, upstream, and hand the household a **card** it evaluates
on sight —

    IF   water is over <the bridge you can see>
    THEN <your road out> closes in ~N minutes
    ACT  leave now, via the open route

`SOURCE_DROP.md` is delivered verbatim.

## Why this one runs here

The spec draws the line itself: *"Post-processing is stdlib,
phone-buildable. The router (2D unsteady solve) is the only non-phone
term."* So the **router output is an input** — `pipeline.py` consumes a
time-resolved depth field and never runs a solver — and the whole
post-processing chain (landmarks → wetting order → stability → lead
bands → route coupling → card) is what runs here.

    python3 observable-indicator-rules/pipeline.py     # the pipeline
    python3 observable-indicator-rules/audit.py        # what it surfaces
    python3 observable-indicator-rules/selftest_oir.py # the checks

**Nothing here is a claim about any real community.** The fields in
`ensembles.py` are synthetic, authored so ground truth is known.
Whether any real place has a derivable card needs the router run on real
terrain — the non-phone term, unreachable here.

## The finding: step 3 is a miss filter, blind to false alarms

The load-bearing check keeps a trigger→hazard pair only if the wetting
order is invariant across the ensemble. Its two failure modes are not
treated symmetrically:

    MISS         hazard wets, trigger dry   -- fatal, no warning
    FALSE ALARM  trigger wets, hazard dry   -- cry-wolf, erodes trust

A **miss** makes the trigger's wetting time INF while the hazard's is
finite, flipping the pair's sign — so **step 3 drops the pair on any
miss.** Good; it is strict about the fatal error.

A **false alarm** makes the hazard's wetting time INF while the
trigger's is finite, reading as *trigger-before-hazard* — **the same
sign as a true positive.** Step 3 does not drop it. Measured on a
constructed ensemble:

    trigger kept by step 3:  True
    miss rate:               0.0   (step 3 forces this)
    false-alarm rate:        0.5   (step 3 does not constrain this)

So a trigger that cries wolf half the time passes the load-bearing
check, and the spec's card carries a clean lead band with **no line for
it** — the strings *false alarm* and *miss rate* appear nowhere in the
delivered card. For a rule people act on by evacuating, the false-alarm
rate is what decides whether they obey it the tenth time. The pipeline
computes the timing and neither error rate; `reliability()` adds both,
and the card built here carries a `REL` line the spec's does not.

The ordering insight is sound. The card needs two numbers the pipeline
does not produce.

## What else building it surfaces

**The falsifiable condition fires both ways.** A flipping ensemble
returns empty output (the spec's *"empty output is a valid, honest
result"*); a stable one returns rules. A pipeline that always emitted a
rule would be `CONSTANT_FIRES`.

**The ordinal bet holds.** With the order fixed and the gaps varying 5×,
the pipeline extracts the order and reports a wide lead band, planned
against the short end (`min`/`p10`, never the median).

**The stability criterion is over-strict.** A tie drops a weak-but-valid
ordering — which loses rules rather than inventing them, the safe
direction for a life-safety card.

**No-wetting runs carry no order and are excluded** — a boundary the
spec leaves open, marked `[CHOICE]`.

**The route is coupled.** When the route closes before the house floods,
the chosen trigger is upstream of the door, not at it.

## Relation to the flood family

Third drop in the family and the output end. `columbia-chain-cascade` is
the coupled solve as a HEC-RAS build spec; `reservoir-chain-coupling` is
the operator swap that makes the coupling load-bearing; this is what the
household holds afterward. The inversion — heavy solve once upstream, the
household holds a result not a computation — is the same governance point
the siblings make from the modeling side: the coupled chain has no
single owner, so the product that survives every notification link
failing is one the household reads on sight.

## Files

| file | what |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim, not edited |
| `pipeline.py` | the spec's steps 1–6, consuming a router field; no solver |
| `ensembles.py` | synthetic router outputs, authored with known ground truth |
| `audit.py` | what building it surfaces, each demonstrated |
| `selftest_oir.py` | the checks; run it, it prints its own count |
| `CLAIM_TABLE.md` | `OIR_001..OIR_009` with REFUTATION_PROTOCOL |
| `samples/` | pinned runs |

`pipeline.py` and `audit.py` refuse `--selftest` rather than exiting 0
on an invocation that runs nothing. Two declared `no_severity`
exemptions, measured with the three-arm harness: `alarm` and `error`,
the finding's own vocabulary (the finding *is* that the card omits the
false-alarm rate and the error rates), where rewording would lose the
subject.

## Scope

No real community, drainage, road, or household appears here. The output
products the spec names (velocity bands, exposure overlay) are
extensions of the router run and are not touched. What is established is
that the pipeline extracts stable orderings, returns empty honestly,
plans against the short end, couples the route — and omits the two error
rates a person acting on the card needs.

CC0. Stdlib only, parses under 3.9, phone-buildable.
