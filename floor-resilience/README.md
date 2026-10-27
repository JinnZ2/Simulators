# Floor Resilience Toolkit

Plants record symptoms, not skill. Scrap gets logged as an equipment cause.
Repairs done by untitled operators get written up by titled mechanics.
Hiring screens on reading and writing. So the records put the plant's
capability in the wrong place. This toolkit measures around the records:
where tacit floor skill lives, how fast it drains, and what keeps running
when power, software or a vendor fails.

You get a scored site assessment plus stress-test reports that a plant
manager, grant reviewer or co-op can read.

Built to `WORK_ORDER.md` (issued 2026-10-23, Kavik + Claude). CC0.

**Provenance.** The work order came with an upload,
`OKComputer_Dyslexia_Spatial_Gap.zip`. OKComputer is Kimi, an open-source
model. That material is a diagnosis and a set of notes from work done with
Kimi. It is read as notes to check, not as findings, and nothing in the zip
was used as a measured input.

## Quick start

```
pip install -e .            # needs python 3.11+, numpy, pydantic, pyyaml, matplotlib
floorres assess examples/example_site.yaml --out my-report
floorres sim                # skill-drain model, default plant
floorres sim --rng js       # replays the published model's exact numbers
floorres stress examples/example_site.yaml
```

`assess` writes `report.md`, `report.html` (opens on its own, charts
embedded) and the chart PNGs. Nothing makes a network call.

To fill in a site without typing YAML, open
`floor_resilience/intake/intake.html` in any browser, phone included. It has big
buttons, every question can be skipped, and voice memos and photos are saved
as file names. Press Save to get `site.yaml`.

## Tags on every number

| tag | means |
|---|---|
| SITE DATA | computed from your site file |
| ASSUMED | a placeholder. Change it in `data/config.yaml` or with a flag |
| PROPOSED | an untested design choice (indicator weights, the I8 score table) |
| OBSERVED | a floor observation (the scrap-code map) |
| FOUND | checked against a published source |
| EXAMPLE | invented, for illustration only |

## What each indicator answers

Score 0 to 4, where 4 is healthiest. Every indicator also reports a
confidence from 0 to 1, which is how much of the needed data your file had.
With no data the score is left blank. A blank is never counted as good or bad.

| id | in one sentence |
|---|---|
| I1 | How much scrap a skilled operator could have caught before it happened. |
| I2 | Whether safety rules come from workers speaking up or from people getting hurt. |
| I3 | Whether more repairs are being sent outside each year. |
| I4 | Whether machines and parts are being replaced faster than they should wear out. |
| I5 | How many long-time operators you have, and how many stay past the next three years. |
| I6 | How many machines or jobs only one person knows how to run or fix. |
| I7 | How many new hires each veteran has to teach. |
| I8 | Whether the hiring test checks the same skill the job uses. |
| I9 | How often the person who fixed it is not the person whose name is on the write-up. |
| I10 | Whether more inspectors and supervisors are being added per operator. |
| I11 | Whether experienced operators are part of automation projects. |
| I12 | What keeps running, or can be run by hand, when power or software goes down. |

The overall score is a weighted average. The report always prints the three
weakest indicators beside it. If several indicators tie for third-lowest, all
of them are listed, so a tie can't hide a weak spot.

## What each module answers

| module | question |
|---|---|
| `schema.py` | What can a site file hold? Every field is optional. A bad row is dropped and listed, never a crash. |
| `scrap.py` | How much logged "equipment" scrap was a missed human catch? Did a machine get worse after a named veteran left? |
| `drain_sim.py` | How does scrap climb as veterans leave? How much warning does a veteran count give before the scrap alarm? |
| `stress/power.py` | With no power, surging power or a generator budget: what runs, what can be run by hand, and by whom? |
| `stress/software.py` | Take one software layer down: what stops, what degrades, and what can a person bridge? Hidden chains are flagged. |
| `stress/vendor.py` | Which vendor's outage would stop more than 30 % of output? |
| `reserve.py` | A small skilled reserve line, costed as insurance: premium against expected avoided loss. |
| `eld.py` | Can the fleet's drivers fall back to paper logs if the electronic log fails? |
| `report.py` | Writes it all out in plain words, with tags. |

## Findings from building it

**The published lead time is one draw, not the model's value.** The
skill-drain model ships with Plant A +48 % scrap, Plant B +7 % and a 14-month
warning lead. `floorres sim --rng js` replays the JS model's random generator
and reproduces those three numbers exactly, which is the work order's
acceptance check. But at 40 runs the JS model's own seed-to-seed spread is
A ± 6 points, B ± 4 points and lead ± 6 months (30 seed bases, run in node).
Over 2000 runs (three seed bases) it settles at A +47 %, B +6 %, with
veterans down 30 % by month 13 in all three, but scrap first passes +50 % in
month 32, 28 and 28: a lead of **15 to 19 months**, not 14. The
lead swings because Plant A's expected scrap curve peaks at about +53 % around
month 35, then falls back to about +47 % by month 60. The +50 % alarm sits
only a few points under that peak, so noise decides when it trips. The numpy
port is tested against the converged values, and the exact replay against the
published draw.

**In the example plant, the manual knowledge for lathe-2 left with Dale R.**
The power stress test reads lathe-2 as MANUAL_NO_ONE, meaning a manual mode
exists but nobody left on site is recorded as able to use it. The same
departure shows in scrap: lathe-2's catchable share went from 56 % to 87 % in
the six months after he left. Everything about that plant is EXAMPLE data,
planted to exercise the modules.

## Verification status of outside facts

| fact | where | status |
|---|---|---|
| PHP2Shell: CVE-2026-109618 and CVE-2026-109619, CVSS v4 9.2, fixed in 8.2.35, 8.3.36, 8.4.27 and 8.5.12, nothing upstream below 8.2 | `data/php2shell.yaml` | Search-result text only. The php.net advisory was not opened. The work order says "disclosed 2026-10-20". Sources say claims and an advance notice came out 10-20 and patches shipped 10-21. Both dates are kept. |
| 49 CFR 395.34: 24-hour notice, 7 prior days rebuilt on paper, 8 days to repair, 5 days to ask for an extension | `data/fmcsa_395_34.yaml` | Search-result text only. ecfr.gov and law.cornell.edu did not resolve from the build sandbox. Marked `NOT_VERIFIED_AGAINST_PRIMARY_TEXT`. Check the regulation before shipping, as the work order says. No logic depends on these numbers. |
| ELD compliance date 2017-12-18, AOBRD grandfathering until 2019-12-16 | `data/fmcsa_395_34.yaml` | FMCSA brochure, seen through search results. |

## Research gaps (separate pass, not code)

`research/` holds the dyslexia × spatial/mechanical gap handoffs v2 through
v4.1, unchanged from delivery. Gap 5 asks for an in-situ field measure of
the skill. The toolkit collects the three measures that gap names on each
repair record, all optional: `detection_lead_hours`, `first_fix` and
`called_after_titled_failed`. The report shows them as raw counts by titled
vs untitled fixer, and does not score them.

## Limits

- Every model constant is ASSUMED. The projection shows the shape of the
  mechanism, not a forecast for any plant.
- Score cuts are ASSUMED and weights PROPOSED. Override both with
  `--config`.
- When a site file has no machine output shares, vendor shares are split
  equally (ASSUMED), and those cells say so.
- A machine whose software goes down with `manual_mode` missing is read as
  having no bypass. That reading is pessimistic on purpose.
- No data about named people is collected beyond what the site owner puts in
  the file.

## Tests

```
pytest --cov=floor_resilience
```

The work order asks for at least 85 % coverage on indicators, scrap,
drain_sim and stress; at this commit each is at 100 %. The intake form is driven in headless Chromium
when node and Playwright are installed. Otherwise that one test is skipped.
