# Floor resilience assessment: EXAMPLE: Ridgeview Machining (invented plant)

EXAMPLE: this is an invented plant. No number here describes a real site.

Tags: SITE DATA = from the site file; ASSUMED = placeholder you can change; PROPOSED = untested design choice; OBSERVED = floor observation; FOUND = checked against a published source.

## Summary

Overall: 1.2 out of 4 (weighted mean; weights PROPOSED, score cuts ASSUMED). It is an average of 12 indicators, so read it with the weakest three (4 listed because of a tie at the third-lowest score): I3 outsourcing trend = 0/4; I8 hiring channel match = 0/4; I9 attribution gap = 0/4; I10 oversight ratio = 0/4.

- I3: Whether more repairs are being sent outside each year. In-house repair share went from 86% (2021) to 51% (2025): -8.8% per year.
- I8: Whether the hiring test checks the same skill the job uses. Job is hands-on; screen is written. First-year quit rate 38%.
- I9: How often the person who fixed it is not the person whose name is on the write-up. In 14 of 24 repairs, the name on the write-up is not the person who fixed it. The records place the skill wrongly there.
- I10: Whether more inspectors and supervisors are being added per operator. Oversight per operator went from 0.31 (2021) to 0.64 (2025): +0.085 per year.

## Indicators

Score 0 to 4; 4 is healthiest. Confidence 0 to 1 shows how much of the needed data the site file had.

| id | what it checks | value | score | confidence | tag | reading |
|---|---|---|---|---|---|---|
| I1 | How much scrap a skilled operator could have caught before it happened. | 0.581 | 3/4 | 0.97 | EXAMPLE SITE DATA; cuts ASSUMED | 4604 of 7922 mapped scrap units had a cause an operator could catch; 200 units unmapped. |
| I2 | Whether safety rules come from workers speaking up or from people getting hurt. | 0.25 | 1/4 | 0.80 | EXAMPLE SITE DATA; cuts ASSUMED | 2 rules from worker reports, 6 written after incidents (3 from regulation, not counted). |
| I3 | Whether more repairs are being sent outside each year. | -0.0885 | 0/4 | 1.00 | EXAMPLE SITE DATA; cuts ASSUMED | In-house repair share went from 86% (2021) to 51% (2025): -8.8% per year. |
| I4 | Whether machines and parts are being replaced faster than they should wear out. | 1.38 | 2/4 | 0.83 | EXAMPLE SITE DATA; cuts ASSUMED | Replacing at 1.38x the rate expected from service life (5 of 6 machines recorded). |
| I5 | How many long-time operators you have, and how many stay past the next three years. | 0.231 | 1/4 | 1.00 | EXAMPLE SITE DATA; cuts ASSUMED | 5 of 13 operators have more than 5 years; 2 of them retire within 36 months. |
| I6 | How many machines or jobs only one person knows how to run or fix. | 4 | 1/4 | 0.61 | EXAMPLE SITE DATA; cuts ASSUMED | 4 known by one person only; 3 of those holders retire within 36 months (coolant mix, mill-1 spindle by ear, press-1 die change). |
| I7 | How many new hires each veteran has to teach. | 1 | 3/4 | 1.00 | EXAMPLE SITE DATA; cuts ASSUMED | 5 new hires (under 1 year) and 5 veterans. |
| I8 | Whether the hiring test checks the same skill the job uses. | 0 | 0/4 | 1.00 | EXAMPLE SITE DATA; score table PROPOSED | Job is hands-on; screen is written. First-year quit rate 38%. |
| I9 | How often the person who fixed it is not the person whose name is on the write-up. | 0.583 | 0/4 | 1.00 | EXAMPLE SITE DATA; cuts ASSUMED | In 14 of 24 repairs, the name on the write-up is not the person who fixed it. The records place the skill wrongly there. |
| I10 | Whether more inspectors and supervisors are being added per operator. | 0.0848 | 0/4 | 1.00 | EXAMPLE SITE DATA; cuts ASSUMED | Oversight per operator went from 0.31 (2021) to 0.64 (2025): +0.085 per year. |
| I11 | Whether experienced operators are part of automation projects. | 0.333 | 1/4 | 1.00 | EXAMPLE SITE DATA; cuts ASSUMED | 1 of 3 automation projects involved experienced operators. |
| I12 | What keeps running, or can be run by hand, when power or software goes down. | 0.431 | 2/4 | 0.97 | EXAMPLE SITE DATA; partly derived; cuts ASSUMED | 53% of known machine x power-state cells run or can be run by a named person; 2 cells never tested; 33% of functions hit by a software layer going down can be bridged by a person. |

## Scrap: what the log says vs what was missing

The scrap log names a machine cause on every row. Read against the code map (OBSERVED), 58% (SITE DATA) of mapped scrapped units came from causes a skilled operator could catch early.

| missing catch | units |
|---|---|
| setup knowledge of feed and material behavior | 1769 (SITE DATA) |
| operator who notices dimension creep | 1526 (SITE DATA) |
| operator who hears or feels the change before failure | 1309 (SITE DATA) |

| machine | catchable share | mapped units (SITE DATA) |
|---|---|---|
| cnc-1 | 58% (SITE DATA) | 1684 |
| lathe-1 | 55% (SITE DATA) | 1476 |
| lathe-2 | 77% (SITE DATA) | 1529 |
| mill-1 | 52% (SITE DATA) | 1604 |
| press-1 | 49% (SITE DATA) | 1629 |

| shift | catchable share | mapped units (SITE DATA) |
|---|---|---|
| day | 60% (SITE DATA) | 3683 |
| night | 57% (SITE DATA) | 4239 |

![catchable scrap share by month](scrap_monthly.png)

Machines whose catchable share rose by 10% or more after a veteran left (window 180 days each side; thresholds ASSUMED):

| machine | veteran who left | left | before | after |
|---|---|---|---|---|
| lathe-2 | Dale R. | 2025-03-01 | 56% (SITE DATA) | 87% (SITE DATA) |

## Skill-drain projection

Starting from this site's operators (13 people, screen: written, reserve line: 0). Every model constant is ASSUMED; this is the shape of the mechanism, not a forecast. 40 seeded runs averaged.

| month (index) | scrapped parts | veterans on floor | inspectors |
|---|---|---|---|
| 1 | 848 (ASSUMED) | 4.9 (ASSUMED) | 2 (ASSUMED) |
| 12 | 892 (ASSUMED) | 4.4 (ASSUMED) | 3 (ASSUMED) |
| 24 | 931 (ASSUMED) | 3.9 (ASSUMED) | 3 (ASSUMED) |
| 36 | 952 (ASSUMED) | 3.0 (ASSUMED) | 3 (ASSUMED) |
| 48 | 925 (ASSUMED) | 3.7 (ASSUMED) | 3 (ASSUMED) |
| 60 | 902 (ASSUMED) | 3.9 (ASSUMED) | 3 (ASSUMED) |

Early warning: veterans fall 30% by month 22; scrap rises 50% by month never. The lead time is sensitive: in the default plant the expected scrap curve peaks only a few points above the 50% alarm, so the alarm month moves a lot between runs.

![skill-drain projection](drain_projection.png)

## Stress tests

### Power states

| machine | no power | intermittent / surging | minimal power |
|---|---|---|---|
| lathe-1 | STOPS; tested: never | RUNS; tested: 2024-06-11 | RUNS; tested: not recorded |
| lathe-2 | MANUAL_NO_ONE; who: no one named; tested: not recorded | MANUAL_NO_ONE; who: no one named; tested: not recorded | MANUAL_NO_ONE; who: no one named; tested: not recorded |
| mill-1 | STOPS; tested: not recorded | STOPS; re-home after dropout; tested: never | RUNS; tested: not recorded |
| cnc-1 | STOPS; tested: not recorded | UNKNOWN; tested: not recorded | STOPS; tested: not recorded |
| press-1 | MANUAL; who: Gene P.; tested: not recorded | MANUAL; who: Gene P.; tested: not recorded | RUNS; tested: not recorded |
| saw-1 | MANUAL; who: Sam W.; tested: not recorded | MANUAL; who: Sam W.; tested: not recorded | RUNS; tested: not recorded |

RUNS = keeps running. MANUAL = a named person can run it by hand. MANUAL_NO_ONE = a manual way exists but no one on site is recorded as able to do it. STOPS = no way to run it. UNKNOWN = no record.

Minimal-power plan for 60 kW (SITE DATA): keep mill-1, lathe-1, press-1, saw-1 (56 kW); shed lathe-2, cnc-1. Greedy by priority, 1 first.

### Software layer knockout

If php_portal goes down (also takes down: mes):

- machine press-1: DEGRADED (hidden chain: it does not use php_portal directly)
- function job_tickets: BRIDGED by paper job tickets (php_portal)
- function scheduling: STOPS (mes)
- function pressing: DEGRADED (machine press-1 on manual)
- function inspection_log: BRIDGED by paper check sheet (mes)

If mes goes down (also takes down: nothing else):

- machine press-1: DEGRADED
- function scheduling: STOPS (mes)
- function pressing: DEGRADED (machine press-1 on manual)
- function inspection_log: BRIDGED by paper check sheet (mes)

If hmi_win goes down (also takes down: nothing else):

- machine lathe-2: DEGRADED
- machine mill-1: STOPS
- function turning: DEGRADED (machine lathe-2 on manual)
- function milling: STOPS (machine mill-1)

If cloud_link goes down (also takes down: license_server, vendor_remote):

- machine mill-1: STOPS (hidden chain: it does not use cloud_link directly)
- machine cnc-1: STOPS (hidden chain: it does not use cloud_link directly)
- function milling: STOPS (machine mill-1; machine cnc-1)

If license_server goes down (also takes down: nothing else):

- machine mill-1: STOPS
- machine cnc-1: STOPS
- function milling: STOPS (machine mill-1; machine cnc-1)

If vendor_remote goes down (also takes down: nothing else):

- machine cnc-1: STOPS
- function milling: STOPS (machine cnc-1)

### Worked example: PHP layer down (PHP2Shell)

PHP2Shell (CVE-2026-109618, CVE-2026-109619; CVSS v4 9.2, no login needed). Patches released 2026-10-21 for PHP 8.2.35, 8.3.36, 8.4.27, 8.5.12; nothing from the PHP project for branches below 8.2. (FOUND at search-result depth only; the PHP advisory itself was not opened. Check php.net before acting.)

- layer php_portal: PHP 8.1.31: no patch from the PHP project for this branch; needs a vendor backport or a move to 8.2+. Plan for this layer staying down.
- functions that stop: scheduling
- functions a person keeps going: job_tickets (by paper job tickets), inspection_log (by paper check sheet)
- hidden chains: press-1

### Vendor dependency

| vendor | machines | license checks (SITE DATA) | repair knowledge (in-house / vendor / unknown) | share of line | output stopped if vendor down | flag |
|---|---|---|---|---|---|---|
| Vendor X (EXAMPLE) | mill-1, cnc-1 | 2 | 0 / 2 / 0 | 45% (SITE DATA) | 45% (SITE DATA) | over 30% (ASSUMED) |
| Lathe Works (EXAMPLE) | lathe-1, lathe-2 | 0 | 2 / 0 / 0 | 30% (SITE DATA) | 0% (SITE DATA) |  |
| Press Co (EXAMPLE) | press-1 | 0 | 1 / 0 / 0 | 15% (SITE DATA) | 0% (SITE DATA) |  |
| Saw Co (EXAMPLE) | saw-1 | 0 | 0 / 0 / 1 | 10% (ASSUMED) | 0% (ASSUMED) |  |

## Reserve line

- Runs live daily production, not drills.
- Operators see automation data and fault logs, and their fixes feed back into the maintenance record under their own names.
- Sized to keep the plant's critical output going by hand if the automated line or its software is down.

| item | value |
|---|---|
| wage cost per year | 204,000 (SITE DATA) |
| output value of the reserve line per year | 150,000 (SITE DATA) |
| premium (net yearly cost) | 54,000 (SITE DATA) |
| expected avoided outage loss per year | 67,500 (ASSUMED) |
| avoided loss per unit of premium | 1.25 (ASSUMED) |

Assumed: share_of_outage_avoided = 1.0 (ASSUMED).

PROPOSED: a policy frame like a strategic reserve (compare the Defense Production Act) could fund such lines. This is an analogy, not an existing program.

## Fleet: paper-log fallback

3 of 5 drivers can fall back to paper logs; 1 cannot; 1 not recorded. Share able among known: 75% (SITE DATA).

Started after the ELD compliance date (2017-12-18) with no paper drill on record: truck-3, truck-5.

What the rule asks, as found at search-result depth on 2026-10-23 (status: NOT_VERIFIED_AGAINST_PRIMARY_TEXT; verify against 49 CFR 395.34 before relying on it):

- Driver notes the malfunction and gives the carrier written notice within 24 hours. [395.34(a)]
- Driver reconstructs records of duty status for the current 24-hour period and the previous 7 consecutive days on graph-grid paper, unless they are already in hand or retrievable from the ELD. [395.34(a)]
- Driver keeps paper logs until the ELD is serviced and back in compliance. [395.34(a)]
- Carrier corrects, repairs, replaces or services the ELD within 8 days of discovering it or of the driver's notice, whichever comes first. [395.34(c)]
- Carrier may request an extension within 5 days after the driver's notice, to the FMCSA Division Administrator for the state of its principal place of business. [395.34(d) per FMCSA FAQ (cite letter not confirmed)]

## Field measures (research gap 5)

Raw counts only, for the open question of how floor skill shows up outside reading tests. Not scored.

| group | repairs (SITE DATA) | median fault-detection lead (SITE DATA) | first-time fixes (SITE DATA) | called after a titled mechanic failed (SITE DATA) |
|---|---|---|---|---|
| titled fixer | 8 | 5.4 h (n=6) | 3/6 | 0 |
| untitled fixer | 16 | 20.8 h (n=13) | 10/13 | 4 |

9 repair records carry a voice memo and 0 a photo (file references only).

## Data gaps

- scrap codes not in the map (left out of the share): operator_error (200 units)
- machine output shares missing for some machines; equal shares assumed (ASSUMED)
