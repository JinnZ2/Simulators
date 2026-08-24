# gaps

Each entry: the gap, what would measure it, current status.
Gaps are first-class here. Absence of a legible reason for a mechanism is not
evidence of absence of reason — default reading is that something is known in
it that has not been recovered.

---

## G-PORT — highest priority, unresolved

    GAP    : proximity as enforcement/verification mechanism
    WHY    : small mutual funds stay solvent because default is VISIBLE.
             Contributors verified at walking distance. This is not a role
             binding. It is a load-bearing input.
    ASK    : does it port to non-proximate configuration, or is the loop
             count strictly bounded by verification radius?
    MEASURE:
             - solvency / default rate vs member geographic dispersion,
               across existing ROSCAs and credit unions (S12)
             - do surviving non-proximate mutual funds exist at all
             - if yes: what substitutes for visibility
    STATUS : open. No candidate substitute identified.
    NOTE   : this is the one gap where "recoverable from documents" has NOT
             been established. Procedures are recoverable. This may not be.

## G-HORIZON — partially closed

    GAP    : whether long-horizon commitment is a mindset (unrecoverable)
             or an instrument property (recoverable)
    RESOLVED TOWARD: instrument. Christmas clubs, passbooks, payroll
             deduction, B&L share plans — deliberately illiquid, small fixed
             increment, external ratchet. Horizon was the DEFAULT, not a
             thing sustained by will.
    REMAINS: participation rate under a live credit alternative. Every
             historical case ran without easy consumer credit present. No
             observed case of these instruments competing against credit.
    MEASURE: S08, S09, S10 terms + participation; look for any post-1980
             instance
    STATUS : partial

## G-BELIEF

    GAP    : distrust of long-horizon institutions
    NOT    : a mindset defect. It is a correct reading of the instruments
             (S&L collapse, pension->market conversion, 2008).
    ASK    : is the requirement legibility rather than belief?
    MEASURE: contributor retention vs inspectability. Credit unions and
             ROSCAs as the natural experiment — they require no belief in
             anything the contributor cannot check.
    STATUS : open, testable with live data

## G-KNOWLEDGE-STATE

    GAP    : is the community-work capability latent or overwritten?
    CORRECTION LOGGED: an earlier framing here assumed the knowledge sits
             latent and needs only a transmission event. That fails. Status
             devaluation overwrote the encoding — holders cannot retrieve
             the procedure even for themselves. Nostalgia reports the state,
             not the method. Self-report goes worthless in BOTH directions.
             Transmission chain is ~2 generations skipped.
    THEREFORE: no testimony-based test. Test RESIDUE.
    MEASURE:
             - viable seed stock still being grown out
             - tool inventories
             - canner present in house AND used within N years
             - continuously worked plot
             - storage volume, outbuildings, kitchen equipment
             (residue sits where nothing was logged — see sources.json
              strip_protocol.labor_note)
    STATUS : test redesigned, not yet run

## G-SLACK

    GAP    : uncommitted hours per household as the actual middle-band metric
    WHY    : the band is uncommitted labor time attached to local knowledge,
             not a wealth bracket. Income can RISE while loop count goes to
             zero and the aggregate metric holds.
    MEASURE:
             - hours per household not sold
             - count of local functions with exactly ONE provider
             - free-entry vs priced-entry shared square footage per capita
    STATUS : open, measurable with current data

## G-THRESHOLD

    GAP    : Kaiser 2020 says loop formation is DISCONTINUOUS in fluctuation
             level. Redundancy is not proportional to expected shock.
    ASK    : does a social analogue of the threshold exist, and is there any
             observable that maps to the fluctuation parameter?
    RISK   : this is a cross-domain shape read, confidence not above ~0.4.
             Not a claim. Marker only.
    MEASURE: unknown. Needs a candidate observable before it is testable.
    STATUS : uncoalesced

## G-RATE

    GAP    : return-channel rate constant vs concentration rate
    WHY    : preferential attachment concentrates with no agent required.
             Any long-running physical network that concentrates also has a
             dissipation channel (flood plains, fire, senescence). Systems
             with no return path go single-attractor and fail on the next
             perturbation.
    ASK    : does the return channel SCALE with concentration rate or LAG it?
             Lag is the failure mode — channel exists on paper, throughput
             set for a distribution that no longer holds.
    MEASURE: redistribution throughput vs concentration rate, same units,
             same period
    STATUS : open

## G-REPAIRABILITY

    GAP    : C08 is a distinct failure class — knowledge intact, object
             refuses it. Not covered by the custody/verification cut cleanly.
    ASK    : does the criterion need a fourth cut for object-side
             serviceability, or is it a special case of custody?
    MEASURE: fraction of failure modes serviceable with hand tools +
             published manual, by model year (S04)
    STATUS : open — possible criterion revision

## G-COLLINEAR — new, from the data

    GAP    : `parallel_path` is a deterministic function of `custody` across
             all eleven cases: routed->no, mixed->partial, self->yes. It
             carries no information custody does not already carry.
    ASK    : is that a real regularity (custody and redundancy genuinely
             co-vary) or a coding artifact (the same judgement entered
             twice under two names)?
    WHY IT MATTERS: if artifact, the three-cut table is a two-cut table and
             the criterion is not omitting anything. If real, it is the
             strongest structural result in the folder and belongs in the
             claim table rather than in the schema.
    MEASURE: a case coded by someone who has not seen the custody column.
             Or: any case with routed custody and a working parallel path —
             a system where you hold no residual but function survives node
             loss. Municipal utilities and open-source infrastructure are
             the obvious candidates and neither is in the corpus.
    STATUS : open. `extract.py check` reports it on every run.
