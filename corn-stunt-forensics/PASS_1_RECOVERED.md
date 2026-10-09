# PASS 1 — recovered, verbatim

**Provenance.** This is the output of PASS 1, produced in session on
2026-10-08 and lost when the session hit its context limit. It was
**supplied by the operator** from the chat transcript after
`PASS_2.md` and `FRAME_CYCLE.md` had already landed. It is **not** a
reconstruction: no part of it was rebuilt by the model from memory of a
label, which is what `CSF_007` refused and what would have made
`COMPARISON.md` worthless.

Landed **verbatim**, including its formatting damage: the DISSONANCE
table arrived collapsed onto one line in transit, and the frame-cycle
table arrived intact. Nothing is reflowed, corrected or completed.
The parsed rows are in `COMPARISON.md`.

The closing line is the model's own question from the lost session and
is left as delivered.

Originally model-authored under the operator's method. Every figure in it
is `[CARRIED]` from news and extension sources; none is checked.

---

ARGENTINA 2023/24                                   US 2024 -> 2026
mild winter, few frosts                             leafhopper reaches KS/OK/TX
  -> leafhopper (vector) survives, found early      2024 yield loss 10-55% in KS/OK
  -> sowings staggered Aug..Jan                     NY: vector found for the first time
  -> 5+ generations Nov-May, ~480 eggs/female       2025: TX first detection in Feb (earlier)
  -> Mar 2024: outbreak                                   185 counties, 16 states
  -> forecast cut 6.5 Mt; 40-50% loss in north      2026: detections in Oklahoma again


On the last row: maize and this leafhopper come from the same Mexican origin. A calendar with a hard season break builds in the "sanitary gap" INTA is now prescribing as a remedy. That reading is a hypothesis from the frame-cycle, not a sourced finding.
DISSONANCE (the richest bin, as you said)
#	where the faces won't line up	what it exposes D1	One Reuters article blames the spread first on "hot and dry," then on "humid and warm" conditions	The press layer welded two weather stories into one. Weather may not be the right axis at all D2	Argentina blames local persistence plus host continuity; the US blames wind import	Same vector, opposite causal frames. Each continent reads only one face D3	INTA's remedy is a sanitary gap in the planting calendar; the US 2025 write-up describes Texas leafhoppers moving from maturing corn to younger second-season corn, and calls it migration	The US describes its own host ladder and doesn't name it as a precursor D4	Only 3.8% of trapped leafhoppers carried the disease, yet 33% of submitted leaves were positive	Counting leafhoppers measures the wrong thing. Infectivity is the sensor D5	Kansas/Oklahoma losses ranged 10–55% with no explanation	The spread itself is information, probably infection timing against growth stage. Nobody has partitioned it
What the scan surfaced that the write-ups missed: D3. It only appears when Argentina's write-ups and the US write-ups are put side by side. The US frame is "it blew in," and that frame hides a precursor the US is running itself: second-season and irrigated corn are the same bridge INTA blames. That's a candidate, not a finding. Six articles is a small pile.
GAPS (where to build)
	•	G1. Overwintering up north is presumed, not measured. Cornell says the presumption may be wrong, and Argentina already saw the vector survive farther from the equator than recorded. An unmeasured presumption reads exactly like a measured "no."
	•	G2. No write-up joins the planting-date spread to outbreak severity in the US.
	•	G3. Action thresholds are set on counts, not infectivity.
	•	G4. The misdiagnosis rate is unmeasured. Drought years hide the disease.
	•	G5. The 10–55% loss range has not been broken down by when plants were infected.
EXPERIMENT
	•	Cage adult leafhoppers over winter on volunteer corn and grass in Kansas. That closes G1 in one season.
	•	County by county, correlate planting-date spread against detection and loss. The data already exists in USDA crop-progress reports and the extension dashboards, so it's desk work.
	•	Sentinel corn plots sown at staggered dates, to time when infection happens.
BUILDABLE NOW
	•	Yellow sticky traps plus the free PCR testing extension services offer, reported as infectivity rate, not counts.
	•	prearm.py ports directly. Feed it weekly counts of infective leafhoppers per trap and trigger on the rate of rise, not the level. The same code, with a threshold declared from a breathing log of normal seasons.
	•	Remove volunteer corn and grass weeds.
	•	Compress the planting window across neighbours. This is a commons problem: one late field bridges everyone's fields, so individual action alone can't close it.
NEEDS TO BE SAVED
	•	INTA's four-zone sowing logic. It reasons from where the vector can survive winter, not from where outbreaks happened.
	•	The 6-week lag arithmetic.
	•	D3: the US host ladder hiding inside the import story.
Grading the test. The method did one thing a single read wouldn't: D3 only exists across the two continents' faces. Everything above is from news and extension sources, not peer-reviewed papers. Counts are carried, not checked. The calendar frame and D3 are hypotheses. Want it landed as a folder in the repo with a claim table, so the next pass can test D3?
Sources:
	•	Argentina corn harvest faces more deep cuts from stunt disease spread (Reuters via Canadian Cattlemen)
	•	CropLife: Is increased corn leafhopper migration creating corn stunt outbreaks?
	•	Cornell: Corn stunt, a new disease and a new insect vector for New York
	•	Bichos de Campo: INTA advice on the leafhopper
	•	Bichos de Campo: INTA's staggered-sowing strategy and four zones
	•	K-State steps up corn leafhopper monitoring after detections in Oklahoma (Sunflower State Radio)

PRECURSORS (what shows up before the event)
	•	Winter severity. Few, weak frosts let adult leafhoppers carry over to the next season.
	•	The vector shows up early in the season, and at higher latitudes than ever recorded.
	•	Host continuity, meaning living corn in the field all year. Staggered sowings from August to January, volunteer corn and grass weeds meant there was always corn at a susceptible stage.
	•	Reproduction is exponential: five or more generations a season at about 480 eggs each. That is the runaway glyph, and it has to be read early.
MEASUREMENTS (what the event leaves, and when)
	•	There is a lag: about 20 days before a leafhopper becomes infective, then about 3 more weeks before symptoms show. So the visible signal arrives about 6 weeks after the act.
	•	Symptoms are a lagging sensor. INTA says symptoms appear too late to act on. Same shape as the battery: heat arrives too late, gas comes early. Here the early signal is infective vectors, and plant symptoms come late.
	•	The symptoms also mimic drought, soil compaction and phosphorus deficiency, so in a dry year the sensor is masked.
ANGLE OF REGARD (how it came in)
	•	Argentina reads the cause as local persistence: the vector overwintered and the host ladder carried it through the season.
	•	The US reads the cause as import: wind and storm tracks brought it north, and "leafhoppers don't overwinter here."
WHERE IT WAS LOOKING (the target)
	•	Young corn at the right growth stage, all the time. From the vector's side, a staggered planting calendar is a highway.
FRAME-CYCLE

frame        what counts as a signal               what that frame can't see
farmer/econ  stagger to spread labour and risk;    builds the vector's ladder
             double-crop for land use
vector       continuous green host + mild winter   nothing; this is its optimum
pathogen     vector infectivity, the 20-day lag    -
weather      frost count, storm tracks             host continuity (not weather)
lab/diag     symptom + PCR on submitted samples    the samples nobody submits
seasonal     a hard dry or cold season empties     modern irrigation and double
calendar     the host every year                   cropping removed that break


