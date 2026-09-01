# OPEN QUESTIONS — SEAM GAPS, SESSION 2026-08-31

Six gaps from one session, rendered per
[`../RESEARCH_RENDER.md`](../RESEARCH_RENDER.md). All are seam gaps —
the delivering order's own classification: each sits between two fields
whose instruments code it as the other's problem.

Every number here is carried from [`WORK_ORDER.md`](WORK_ORDER.md) at
the status [`SOURCES.md`](SOURCES.md) records. Nothing was verified
against a primary source; the egress gate refuses every publisher named
(measured, with timestamps, in `SOURCES.md`).

Entries 5 and 6 are the first worked instances of the DECISION entry
type. The **Placement** line on each entry is this render's call, noted
per the order and executed for none — see the README.

---

## 1. EMPIRICAL — The referent and the number travel separately (G-01)

**Gap:** A coral-chemistry record (~900 yr, Galápagos) puts eastern
equatorial Pacific ENSO *variability* ~36% above preindustrial, 16
points of that in the last ~40 years. The same week, two versions of
the number were in circulation: the stated referent — variability of a
regional index — and a drifted one, "El Niño events are 36% stronger",
which is event strength, unscoped. Per the delivered material, France24
and the Oman Observer carried the stated referent; most other outlets
did not. The producing field's instrument ends at publication, and no
downstream instrument reads which referent circulates. A citation born
in two versions on a known date, with named outlets on each side, is a
measurable propagation experiment that nobody is measuring.

**Knowledge state:** NOT_STUDIED (countable, dated, and uncounted)

**Research question:** For a result published with a stated referent
and a same-week drifted version, what share of coverage and citation
carries which referent at 1, 6 and 24 months — and does the drifted
form displace the stated one, hold level with it, or decay?

**Disciplines:** science communication, bibliometrics, climatology
(for the referent coding)

**Data sources:**
  EXISTING RECORD: news archives (GDELT, Media Cloud), the paper and
    its press release, citation databases as they populate
  YOUR OWN DATA: a coded coverage corpus — referent per item, coded
    against a two-form rubric fixed before collection
  SOMEONE'S HANDS: the outlets the delivered material already splits
    anchor the rubric's two ends; they are the calibration, not data

**Method:**
1. Operationalise the two forms before reading any coverage:
   variability-of-index (states region and index) against
   event-strength (states neither, attributes the percentage to
   El Niño events themselves).
2. Collect coverage items over 24 months from the archive.
3. Code each item to a form, blind to outlet, rubric unchanged
   mid-run.
4. Report the share per form at 1, 6 and 24 months.

**Expected deliverable:** a dated propagation curve per referent form —
the first entry in the reference class
[`../question-availability/`](../question-availability/) `QA_005` says
its correction-half-life instrument cannot be read without.

**Falsifier:** the drifted form does not out-circulate the stated form
at any horizon. Then the coverage error is noise rather than a channel
property, and the gap closes as a calibration point instead of a
mechanism.

**What it opens:** with one curve in hand, `QA_005`'s `half_life()` has
a reference class of one instead of zero; and
[`../term-drift-citation/`](../term-drift-citation/) gets a
born-divergent case where referent drift is normally only measurable
over decades.

**Placement (this render's call):** `question-availability/` — its
`QA_005` is the consumer. Alternative: `term-drift-citation/`, if the
reading is that the drift itself is the subject rather than the
propagation.

---

## 2. METHODOLOGICAL — A null below its own floor reads as a finding (G-02)

**Gap:** Per the delivered material, a 29-year moth series puts the
minimum record length for detecting a true insect trend at 15 years,
while a continental weather-radar study reports no decline over a
10-year window. Ten is below fifteen: the radar null is `SILENT` — a
statement about the instrument's reach, not about the insects — and it
enters the literature as a finding beside −76% flying-insect biomass
over 27 years (German Malaise traps) and ~−9% per decade (global
synthesis). The seam: entomology derives detection floors per taxon
and does not police remote sensing; radar aeroecology publishes
windows and does not derive floors. Nothing requires a trend study to
print its own floor next to its window, so results on both sides of
the floor are compared as if they were the same kind of result.

**Knowledge state:** NOT_STUDIED (one floor stated; per-method floors not)

**Research question:** For each major monitoring method — Malaise
trap, light trap, transect, weather radar — what is the minimum series
length at which a trend the size of the reported declines clears that
method's own interannual variance, and what fraction of published
insect-trend nulls sit below their own method's floor?

**Disciplines:** biostatistics, entomology, radar aeroecology

**Data sources:**
  EXISTING RECORD: the 29-yr moth series (the one derived floor), the
    long Malaise series, the radar study's variance structure,
    published trend studies with their windows stated
  YOUR OWN DATA: power curves per method, computed from each method's
    own published interannual variance

**Method:**
1. Extract interannual variance per method from the longest available
   series of each kind.
2. Compute the minimum window for a −9%/decade trend at stated power,
   per method.
3. Classify published trend results by their window-to-floor ratio;
   a null below 1 reads `SILENT`, a null above it stands as `OFF`.
4. Report the two populations separately; do not average them.

**Expected deliverable:** a per-method floor table, and the published
null record split into can-see and cannot-see — the number the
funding-not-technology argument ("ecological dark matter") currently
makes in prose.

**Falsifier:** the radar method's interannual variance is low enough
that 10 years clears its floor for a −9%/decade trend. Then its null
is a real `OFF`, the disagreement with the trap series is substantive,
and this gap closes into a harder one.

**What it opens:** the meta-analysis under an Editorial Expression of
Concern (per the delivered material) gets a variance-first re-read;
and the exposure side of the same monitoring hole — US seed-applied
insecticides absent from national estimates since 2014 — is a
[`../criteria-drift/`](../criteria-drift/) case standing ready for
whoever ends up at this node.

**Placement (this render's call):**
`instrument-epistemology/` — a detection floor per instrument is that
folder's subject, and the radar null's shape is `nonidentity-census`
`T2-5`'s `CANNOT_HAVE_SEEN_IT` at field scale.

---

## 3. EMPIRICAL — Substitution reads as stability (G-03)

**Gap:** Per the biomass census the order carries (PNAS 2018), wild
mammal biomass is down ~6× from the pre-human baseline while TOTAL
mammal biomass is up ~4× (0.04 → 0.17 Gt C): livestock 0.10, humans
0.06, wild 0.007. Substitution, not depletion — the aggregate grows
while its composition inverts. The seam: conservation's instruments
read the wild component, agriculture's read the livestock component,
and the aggregate "mammal biomass" belongs to neither, so a reader of
the total sees stability where the components crossed. The census is
two time points; the substitution has no series — no rate, no
inflection, and no test of whether the total carries any information
its largest component does not.

**Knowledge state:** UNKNOWN_ATM (endpoints measured; series unassembled)

**Research question:** What is the time series of the wild / livestock
/ human partition of mammal biomass — at what rate has domestic
biomass substituted for wild, and does the aggregate carry any
information the livestock component does not?

**Disciplines:** macroecology, agricultural statistics, demography

**Data sources:**
  EXISTING RECORD: the census supplement (endpoint partition), FAO
    livestock counts (annual), UN population series (annual), wild
    mammal population indices as a relative series
  YOUR OWN DATA: the assembled partition series, with stated error per
    component

**Method:**
1. Fix the two endpoint partitions from the census.
2. Build the livestock and human components as annual series from
   their own records; convert count to biomass with stated per-head
   masses and their error.
3. Scale the wild component against the relative population index,
   with the band widened to say that is what was done.
4. Test whether the total's trajectory is distinguishable from the
   livestock series plus a constant.

**Expected deliverable:** the partition as a series, and a
[`../category-weld/`](../category-weld/) `welds/` entry for "mammal
biomass" — components under opposite drivers, divergence quantified.

**Falsifier:** the total does not track the livestock component — the
components move independently enough that the aggregate carries its
own information. Then the weld reading is refuted for this term, and
"mammal biomass" is a legitimate quantity rather than a costume.

**What it opens:** `category-weld/`'s register gets its first
candidate weld from outside policy and economics — the cross-field
case `uninstrumented/` `UNI_002` has held open since the ninth
mechanism landed — and the same partition question is immediately
posable for birds, where the census puts domestic poultry above all
wild birds combined.

**Placement (this render's call):** `category-weld/` — the deliverable
is literally a `welds/` entry with quantified divergence cases.

---

## 4. INSTRUMENTAL — The count is not the function (G-04)

**Gap:** Per the delivered material: a UK four-decade analysis over
4,424 species finds net declines in pollination, pest control and
cultural value while decomposition and carbon sequestration hold —
with function weighting done at higher-taxon level by choice, because
per-species contribution is context-dependent. An FAO case has bee
species count INCREASING while common species decline — "probably
bodes poorly for pollination" — and function was never measured.
Functional identity and diversity predict measured function better
than species-based indices (3 crops, 3 countries). The trait route to
function carries the field's own stated trade-off: easy-to-measure
traits have weak functional evidence, hard-to-measure traits carry the
robust link, the validation that would bridge them does not exist, and
the trait data itself is geographically and taxonomically biased. The
seam: monitoring counts species because counting is what its
instrument does; services need function; the bridge is nobody's
instrument.

**Knowledge state:** NOT_STUDIED (the field's own review says so)

**Research question:** On datasets where pollination function was
measured, does an index built from hard-to-measure traits predict
function where richness does not — and can the easy traits be
calibrated against the hard ones once, so that routine monitoring runs
on cheap traits with a stated error instead of an assumed link?

**Disciplines:** pollination ecology, functional ecology,
biostatistics

**Data sources:**
  EXISTING RECORD: the 3-crop / 3-country function dataset, the UK
    species-function classification, trait databases with their bias
    stated
  YOUR OWN DATA: paired cheap-and-expensive trait measurements on one
    regional bee assemblage — the calibration set the review calls for
  SOMEONE'S HANDS: groups already measuring pollination service in
    the field

**Method:**
1. On the function-measured datasets, fit three indices: richness,
   easy-trait, hard-trait.
2. Report the predictive gaps between the three, per crop and
   country.
3. Regress easy traits on hard traits in the paired set; the residual
   is the error a cheap monitoring index must carry — stated, not
   assumed.
4. Re-read the FAO count-up case through the calibrated index.

**Expected deliverable:** a validated-or-refuted cheap-trait
monitoring index with stated error, and the FAO case converted from a
warning in prose to a number.

**Falsifier:** the easy-trait index predicts measured function no
better than richness in every tested system. Then trait-based
monitoring at scale is not currently buildable, and the field's call
for validation has its answer, in the negative.

**What it opens:**
[`../proxy-investigation-lab/`](../proxy-investigation-lab/) gets a
live decision-use proxy chain to grade — richness → traits → function,
fidelity multiplicative through the assumed link, exactly the shape
its catalog batch already ranks.

**Placement (this render's call):** `proxy-investigation-lab/`.

---

## 5. DECISION — Which record is the preindustrial ENSO baseline (G-05)

**Fork:** "ENSO variability is now X% above preindustrial" is
baseline-relative, and two instruments hold candidate baselines: an
1,100-year annual index reconstructed from North American tree rings
(the canonical public series), and ~900 years of Galápagos coral
chemistry (the record behind the 36% figure). They are not the same
quantity — one reads ENSO through a continental drought
teleconnection, the other reads eastern equatorial Pacific water
properties in-basin — and the field's own stated motivation for both
is that the instrumental record is too short to characterize natural
variability.

**Options:**
  A. The tree-ring index is the reference — continuous, annual, long
     instrumental overlap. What follows: every variability statement
     inherits the teleconnection transfer function, and if the drought
     response to ENSO is itself nonstationary, the baseline moves
     with it.
  B. The coral record is the reference — in-basin, direct chemistry.
     What follows: variability statements are regional to the eastern
     equatorial Pacific, and the archive's splicing across coral
     colonies carries a variance structure that has to be priced
     before a 36% change is read against it.

**Winning condition:** one record's variance structure transfers to
the instrumental target over the overlap period with stationary
calibration where the other's does not — or the two agree on the
variability trend within stated error, in which case the fork closes
as a non-fork at this precision.

**Discriminator:** run both records against the instrumental record
and against each other over their common centuries — in particular,
does the recent-decades variability rise (16 of 36 points in ~40
years, per the delivered material) reproduce in the tree-ring index
over the same window? Both series are public in principle; the
comparison is a running-variance analysis, not new fieldwork.

**Blocked by:** access — this environment's egress refuses both
archives (measured; `SOURCES.md`), and the coral series' availability
rests on the paper's data deposit.

**Who could run it:** anyone with both series downloaded and a
statistics course — a student with the public archive and the paper's
supplement. No lab, no boat.

**If you run it:** the baseline fork closes for the variability claim;
entry 1's propagation question gets a firmer referent to code against;
and the 40-year acceleration is either corroborated across instruments
or isolated as a single-record reading.

**Placement (this render's call):** `climate-modeling/` — its
`StationarityAudit` is the instrumental-window-too-short failure as
runnable code, and this fork is that audit's subject arriving as a
real case.

---

## 6. DECISION — Pre-1630, which channel is in error (G-06)

**Fork:** Per the delivered material, ice core and tree ring agree
back to ~1630 and the documentary record does not match well before
that — published as such (Michaelsen 1992), an honest `OFF`. Elsewhere
the documentary channel earns calibration standing: Chinese records
used to correct a tree-ring precipitation series; ships' logbooks
reconstructing ENSO; a NE India speleothem in "striking synchrony"
with famine accounts across the past millennium; Arabic chronicles
carrying precipitation, temperature, hail, flood and river levels from
AD 680; Kyoto cherry flowering since the 9th century; Jesuit typhoon
records from 1566. So the pre-1630 mismatch is a fork, not a verdict
on the channel.

**Options:**
  A. The documentary channel degrades before ~1630 — compilation loss,
     dating drift, survivorship deepening with time. What follows:
     documentary series before ~1600 need external anchoring per
     region before use, and reconstructions built on them alone carry
     an undated floor.
  B. The physical-proxy pair is the side with the problem there — two
     proxies agreeing is shared variance, not ground truth; ice core
     and tree ring can share a regional driver the documents do not,
     and the documents record local weather impacts where the proxies
     record regional integrals, so the comparison object may shift
     before 1630 rather than either channel erring. What follows: the
     documentary record is the one vote with a different failure mode,
     and discarding it selects for whatever bias the proxies share.

**Winning condition:** the pre-1630 divergence is attributed — a third
channel with an independent failure mode repeatedly sides one way in a
region where both records exist — rather than the mismatch being
restated.

**Discriminator:** an annually-resolved speleothem run against BOTH
channels in a region whose literary tradition reaches well before
1630. The design is proven at millennium depth in one region (the
India speleothem-and-famine-records case, per the delivered material);
the Arabic corpus (AD 680 onward) and the Chinese corpus reach deeper
than the divergence.

**Blocked by:** the archives — the field's own stated limit is that
documentary evidence is confined to regions with long literary
traditions, the deep Arabic corpus is still being assembled (the named
DFG project), and the discriminator also needs a speleothem in the
same region as the documents, which is a geological fact nobody can
schedule.

**Who could run it:** the historical-climatology groups already
holding a deep documentary corpus with a regional speleothem in range
— the Arabic-sources project is the named position, and the India team
has already run the shape once.

**If you run it:** the fork closes per region — and may close
differently in different regions, which would itself be the finding.
Either way the pre-1630 documentary record converts from
does-not-match-well into a bounded instrument, and entry 5's baseline
question inherits whatever record survives.

**Placement (this render's call):** `instrument-epistemology/` — the
fork is a triangulation-order question, and that folder's declared
strength order (traceability → inter-instrument triangulation →
forward simulation → intervention) is the frame the discriminator
runs in.

---

CC0.
