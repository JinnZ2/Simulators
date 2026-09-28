# FIELD LAYER SEED 01 — Roads: human-run wear vs autonomy's infrastructure bill
### First seed of the field-originated record layer. Compiled 2026-09-24.
### Provenance labels: MEASURED (independent/government/academic) / VENDOR / FORECAST / CONSTRUCTED.

---

## WP1 — HUMAN-RUN ROAD COMPARISON: unpaved vs paved vehicle wear

**Ledger entries (measured, oldest sources first — the foundational work is old and solid):**

| Claim | Value | Provenance |
|---|---|---|
| Vehicle operating costs, gravel vs paved | "often 2 or 3 times greater" on gravel (rolling resistance, traction, tire wear, dust→engine wear, oil consumption) | MEASURED — FHWA Gravel Roads Construction & Maintenance Guide, citing AASHTO |
| Tire cost per mile @ 40 mph, tangent | concrete 0.29¢ / asphalt 0.43¢ / gravel 1.07¢ — gravel ≈ **2.5–3.7×** paved | MEASURED — NCHRP Report 111 (instrumented fleet testing; dated dollars, ratio is the content) |
| Tire wear on 90° curve vs tangent | ~**1,000×** (20 mph, stop-and-go test) | MEASURED — NCHRP Report 111 |
| Gravel road maintenance frequency | ~4× paved; gravel can go excellent→failed in **under a year** | MEASURED — county records via EPA/industry review |
| Minnesota county, 2005–2009 actuals | gravel $1,887/mi/yr vs paved $13.45/mi/yr | MEASURED — county expenditure records |
| Rainfall → roughness | +970–1,100 mm/km roughness per metre of annual rainfall | MEASURED — TRRL-class field study, unpaved test sections |
| Counter-nuance | a *deteriorating bitumen* road can be worse for spares/tyres than gravel at equal roughness | MEASURED — Caribbean/Kenya TRRL studies |

**Field-layer notes (what the desk record misses, per operator review):**
- Wear on unpaved is dominated by **corrugation cycle timing**, not surface type alone:
  2 weeks ungraded corrugation ≈ 1–2% fleet tire life (from the Komatsu scaffold, V2.1).
  A graded gravel road beats a neglected paved one — the Caribbean nuance confirms it.
- **Dust is an engine-wear term** the desk tables underweight: air-filter intervals, oil
  contamination, bearing ingestion. The FHWA guide names it; the cost models mostly don't
  price it separately.
- Driver behavior on gravel (speed choice, line choice around potholes/washboard) is a
  human skill variable that halves or doubles the wear rate — unmeasured in every table
  above. UNKNOWN, flagged.

## WP2 — THE INFRASTRUCTURE BILL AUTONOMY NEEDS (the industry's own survey answers)

Source anchor: Caltrans AV industry survey (2021, 18 companies, 90% response) — these are
the autonomy industry's **own stated requirements**, not skeptics' estimates:

| Requirement | Specifics | Provenance |
|---|---|---|
| Lane markings | 150 mm wide, ≥150 mcd/lux/m² dry retroreflectivity, ≥35 wet; contrast ratio classes; **old markings fully erased**; tar lines/expansion joints confuse machine vision | INDUSTRY-STATED (EuroRAP "Roads That Cars Can Read" + Caltrans survey) |
| Marking maintenance | "monitored and maintained **more stringently** than for human-driven vehicles"; AV companies want notification when segments go non-compliant | INDUSTRY-STATED |
| Work zones | real-time digital notification, 24 h ahead minimum — **top ask, 12/18 companies** | INDUSTRY-STATED |
| Traffic signals | machine-readable phase & timing via public database | INDUSTRY-STATED |
| HD maps | <10 cm accuracy; continuous LiDAR survey fleets; Mobileye crowdsourcing ~10 kb/km/vehicle | INDUSTRY-STATED / VENDOR |
| V2X + cellular | redundant comms paths for safety-critical inputs | INDUSTRY-STATED |
| Transfer hubs (trucking) | L4 = hub-to-hub; hubs required for refuel/swap; gradual 2027–2040 | FORECAST — McKinsey |
| Mixed traffic persistence | markings/signs "will not disappear in the next 30 years" — Mercedes-Benz R&D | INDUSTRY-STATED |
| Emergency procedures | observer/roadside-assist staffing (Aurora model); pull-over on out-of-scope weather | MEASURED (from demo-corpus audit) |

## THE COLLISION (Layer 3 — where the two work packages meet)

1. **Machine vision needs *better* roads than humans do.** Human drivers read faded
   markings, tar snakes, gravel with no markings at all, and a work zone with a guy holding
   a paddle. The autonomy industry asks for 150 mm stripes at measured retroreflectivity,
   erased ghost lines, 24-hour digital work-zone notice, and sub-10 cm maps. **The
   infrastructure maintenance standard autonomy requires is higher than what rural and
   northern roads currently get for humans** — and every bit of it is doer labor: striping
   crews, sign techs, survey fleets, telecom crews.
2. **The autonomy map ends where the pavement ends.** Corridor trucking (Aurora) runs
   validated *paved interstate*. Mine AHS runs on *privatized, re-graded gravel*. Unpaved
   public roads — the network the field actually lives on — appear in no deployment plan.
   Gravel's excellent→failed-in-a-year cycle is exactly what HD maps and retroreflectivity
   standards cannot absorb: the map would expire faster than it can be re-surveyed.
3. **WP1 quantifies what WP2 would have to tame.** 2.5–3.7× tire cost, 4× maintenance
   frequency, rainfall-driven roughness growth ~1,000 mm/km per metre of rain: that is the
   physical regime autonomy has never operated in commercially. The claim "autonomy scales
   to rural freight" currently rests on **zero unpaved-miles evidence**.

## Falsifiers registered

```
RD-F1  Autonomy on unbound surfaces is confined to privatized, re-engineered sites
       Refutes if: any commercial autonomous freight operation logs >10,000 miles
       on PUBLIC unbound (gravel/dirt) roads by 2029
RD-F2  Autonomy raises the road-maintenance standard above human requirements
       Refutes if: an AV freight deployment is validated on roads certified to
       meet only current human-driver marking/maintenance standards, with the
       deficiency data published
RD-F3  Driver skill on gravel halves/doubles wear rate (operator claim, UNKNOWN)
       Refutes if: fleet data at matched surface/vehicle shows driver-to-driver
       wear variance <10% — i.e., the human skill variable is noise, not signal
```

## Open UNKNOWN cells (the to-do list, per schema)

- Fault-detection latency on unpaved: does any AV stack detect developing washboard,
  soft shoulders, frost heave — or only obstacles? (No record found.)
- Dust ingestion curves for AV sensor suites (lidar/camera fouling rates on gravel
  duty): UNMEASURED in public record.
- Cost per mile to bring one rural gravel mile to "machine-readable" standard and
  KEEP it there through one freeze-thaw year: UNMEASURED.
