# WORK ORDER — Floor Resilience Toolkit

Issued: 2026-10-23 · Authors: Kavik + Claude · License: CC0
Tags used throughout: OBSERVED = floor observation · FOUND = verified source ·
PROPOSED = untested design choice · ASSUMED = placeholder number, must be overridable

## 0. Purpose

Build a Python toolkit that measures what standard site selection and plant audits
miss: tacit floor skill, where it lives, how fast it drains, and what keeps running
when power, software or vendors fail. Output is a scored site assessment plus
stress-test reports a plant manager, grant reviewer or co-op can read.

Core claim the toolkit operationalizes (OBSERVED): plants record symptoms, not
skill. Scrap gets logged as equipment cause, repairs done by untitled operators get
written up by titled mechanics, and hiring screens on read/write channels. The
records therefore misplace capability. The toolkit must measure around the records.

## 1. Repo layout

```
floor-resilience/
  README.md                 # plain-language; what each module answers
  LICENSE                   # CC0
  pyproject.toml            # python >=3.11; deps: numpy, pydantic, pyyaml, matplotlib
  floor_resilience/
    schema.py               # pydantic models for every input (section 2)
    indicators.py           # indicator definitions + scoring (section 3)
    scrap.py                # scrap-code reclassification (section 4)
    drain_sim.py            # skill-drain simulation (section 5)
    stress/
      power.py              # power-state test (section 6a)
      software.py           # software-layer knockout (section 6b)
      vendor.py             # vendor/license dependency map (section 6c)
    reserve.py              # skilled-operator reserve line spec + costing (section 7)
    eld.py                  # fleet paper-log readiness (section 8)
    report.py               # markdown + HTML report renderer
    cli.py                  # `floorres assess site.yaml`, `floorres sim`, `floorres stress`
  examples/
    example_site.yaml       # clearly marked EXAMPLE, invented plant
  tests/
```

## 2. Inputs (schema.py)

One YAML per site. Every field optional; missing data lowers a confidence score, it
never crashes. Every numeric default is tagged ASSUMED in a comment.

- workforce: operators[] with tenure_months, role, titled (bool), reserve (bool),
  retiring_within_months (optional), sole_knower_of[] (machines/processes)
- hiring: screen_type (written | interview | hands_on_trial | working_shift),
  first_year_quit_rate
- maintenance: repairs_inhouse, repairs_outsourced (per year, multi-year series)
- repair_attribution: sample of repairs with who_diagnosed, who_fixed, who_wrote_up
- scrap: rows of {date, machine, logged_cause_code, units}
- machines: id, controller, software_layers[], vendor, license_check (bool),
  manual_mode (none | partial | full), power_draw_kw
- oversight: inspectors, supervisors, direct_operators (multi-year series)
- safety: rules[] with origin (incident_driven | worker_reported | regulation)
- automation: projects[] with experienced_operators_involved (bool)

## 3. Indicators (indicators.py)

Each indicator returns {value, score 0–4, confidence 0–1, tag, explanation}.
Weights live in a YAML config, default equal, tagged PROPOSED.

| id | indicator | signal |
|----|-----------|--------|
| I1 | operator-catchable scrap share | section 4 output |
| I2 | safety direction | share of rules from worker reports vs after incidents |
| I3 | outsourcing trend | in-house repair share, slope over years |
| I4 | machine/part turnover | replacement rate vs expected service life |
| I5 | veteran depth | operators with tenure > 5 yrs; retirements in 36 mo |
| I6 | sole-knower count | machines/processes known by exactly one person |
| I7 | mentoring load | new hires per veteran |
| I8 | hiring channel match | screen_type vs job channel (floor role + written screen = mismatch) |
| I9 | attribution gap | share of repairs where who_fixed != who_wrote_up |
| I10 | oversight ratio | (inspectors + supervisors) / direct operators, trend |
| I11 | automation ordering | automation projects with experienced operators involved |
| I12 | fallback readiness | from section 6 results |

Overall score = weighted mean, reported with the lowest three indicators named.
Never output a single number without its weakest components.

## 4. Scrap reclassification (scrap.py)

Map logged equipment codes to the human catch that was missing (OBSERVED mapping,
editable YAML):

- calibration_drift → operator who notices dimension creep
- belt_drive_failure → operator who hears/feels the change before failure
- material_jam → setup knowledge of feed and material behavior
- true_failure codes (sudden fracture, power event) → not catchable

Output: catchable share, by machine and by shift, trended monthly. Flag machines
whose catchable share rose after a named veteran left (join on workforce dates).

## 5. Skill-drain simulation (drain_sim.py)

Port the published JS model (artifact "Skill Drain Simulator") to numpy, same
mechanics so results match within Monte Carlo noise:

- skill s in [0,1]; s += (1 - s)/tau_eff monthly; tau_eff = tau / (0.3 + 0.7*mentor_factor)
- mentor_factor = min(1, veterans / max(1, newbies/3)); veteran = s >= 0.7
- drift events Poisson(3)/machine/month, caught with prob s; miss = 40 scrapped parts
- true failures Poisson(0.3)/machine/month, uncatchable
- written screen: new hire s0 ~ 0.02–0.06, first-year quit x2;
  hands-on: s0 ~ 0.22–0.32, normal quit
- reserve line: k veterans exempt from quitting, always mentor, hand off at s=0.5
- in-house repair share = min(1, veterans/4); inspectors = 2 + ceil(excess scrap/400)

All constants ASSUMED and exposed as parameters. Add: initialize from a site YAML
instead of the default 12-veteran plant. Output: monthly series + early-warning
lead time (veterans down 30% vs scrap up 50%). Seeded and reproducible.
Acceptance: default run reproduces Plant A ≈ +48% scrap at month 60, Plant B ≈ +7%,
lead time ≈ 14 months (±20%).

## 6. Stress tests (stress/)

### 6a. Power states
For each machine and each state {none, intermittent/surging, minimal (generator or
small solar, kW budget)}: runs? needs re-homing after dropouts? manual alternative?
who on site can run it (names from workforce)? last time tested (date or "never").
Minimal state: greedy load-shed plan by priority within the kW budget.

### 6b. Software-layer knockout
Build a dependency graph: function → machine → software layers (PHP web portal,
Java/Windows HMI, license server, cloud link, vendor remote support, MES/scheduler).
Remove one layer at a time; report which functions stop, which degrade, and whether
a person can bridge it (paper job tickets, local panel, manual mode).
Include a worked example using PHP2Shell (CVE-2026-109618/109619, disclosed
2026-10-20, patches only for PHP 8.2–8.5) as the "PHP layer down" scenario. FOUND.
Flag hidden chains: a locally fine machine that stops because it calls a down layer.

### 6c. Vendor dependency
Per vendor: machines covered, license checks, whether repair knowledge is in-house
or vendor-held, single-vendor share of the line. Flag any vendor whose outage stops
more than 30% of output (threshold ASSUMED).

## 7. Reserve line (reserve.py)

Spec + cost model for a small skilled-operator reserve line:
- runs live daily production, not drills
- operators see automation data and fault logs; their fixes feed back
- size, wage cost, output value, and avoided cost of a fleet-wide outage
  (outage days x daily output value x probability, all user inputs)
Report it as resilience insurance: premium vs expected avoided loss.
Note the policy frame (strategic-reserve / Defense Production Act analogy) as
PROPOSED, not an existing program.

## 8. ELD / paper-log readiness (eld.py)

Fleet input: drivers[] with start_year, has_kept_paper_logs_in_cab (bool),
completed_week_long_paper_drill (bool). Outputs: share of drivers able to fall back
to paper; flag drivers who started after the ELD mandate with no in-cab drill.
Note: FMCSA malfunction rules (paper logs, reconstruct prior 7 days, 8 days to
repair) must be verified against current 49 CFR 395.34 before shipping; do not
hardcode from memory.

## 9. Report (report.py)

Markdown and self-contained HTML. Sections: summary with weakest three indicators,
indicator table with tags and confidence, scrap reclassification chart, drain-sim
projection, stress-test matrix (machine x state), reserve-line costing, data gaps.
Writing rules: plain words, no jargon the floor wouldn't use, every number shows its
tag, every invented example labeled EXAMPLE.

## 10. Accessibility of input (records channel)

The tool must not repeat the hiring-screen error. Provide:
- a large-format, big-touch-target HTML intake form (no small text fields required)
- voice-memo and photo fields per repair record (store file refs; transcription optional)
- every field skippable

## 11. Acceptance criteria

- `pytest` passes; coverage on indicators, scrap, drain_sim, stress >= 85%
- `floorres assess examples/example_site.yaml` produces report.md + report.html
- drain_sim matches section 5 targets
- no indicator returns a score without confidence and tag
- missing inputs never crash; they lower confidence and appear under "data gaps"
- README explains each indicator in one plain sentence

## 12. Out of scope / do not

- No scraping or collecting data about named private individuals beyond what the
  site owner supplies.
- No network calls at runtime.
- Do not present ASSUMED numbers as findings.
- Do not add a single headline score without the weakest components beside it.

## 13. Open research gaps (for a separate pass, not code)

- Dyslexia × mechanical aptitude: see "Gap Handoff v4.1" (Kimmy). Gap 5 (in-situ
  field measure) is the one this toolkit could collect data for: fault-detection
  lead time, first-fix rate, who gets called when titled mechanics fail.
- Germany/Japan floor-credential share over time (FOUND-pending).
