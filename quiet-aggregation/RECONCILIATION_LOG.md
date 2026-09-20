# WO-2 validated reconciliation log

**Prepared by:** Manus AI

**Validation date:** 19 September 2026

## Final disposition

Independent case-level validation changed the first reconciliation from **five supporting and three indeterminate cases** to **one supporting and seven indeterminate cases**. No case was classified `does_not_support` because the official reports did not affirmatively negate the earlier pattern elements; most uncertainty concentrated in the strict requirement that `join_assigned = no` be established from the report.

The [first reconciliation](initial-reconciliation-log.md) and [first synthesis](initial-pilot-analysis.md) are retained as superseded artifacts. They must not be cited as the final result.

## Why the first reconciliation changed

The initial reconciliation sometimes combined evidence from different hazard pathways within one case. For example, it used the Dow nitrogen-inerting signal and date with work-light inventory and vessel-closure evidence to satisfy the holder and join fields. It also treated weak controls, absent procedures, or ineffective performance as affirmative evidence that no responsible-and-authorized integration function had been assigned.

Independent validators applied two clarifications symmetrically to all eight cases. First, every field supporting a case result must belong to one official-report-identified hazard pathway. Second, `join_assigned = no` requires affirmative evidence of missing responsibility and authority; poor performance, missing procedure, or silence about organization design is insufficient. A separate suddenness clarification excludes alarm labels and generic physical-rate adverbs unless the report uses them to characterize the event, relevant failure, or warning pattern. These clarifications were post hoc and are documented in the [codebook](codebook.md).

## Validated case matrix

| Rank | Case | Signal | Reported | Holder minimum | Join assigned | First signal | Lead time | Sudden label | Final result | Validation |
| ---: | --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| 1 | [Shell Polymers](validation/shell-polymers.md) | Yes | Yes | 3 | Unclear | 2023 | 521–885 days | Unclear | **Indeterminate** | Corrected suddenness only |
| 2 | [U.S. Steel Clairton](validation/us-steel-clairton.md) | Yes | Yes | 2 | Unclear | At least 3 years before event | ≥1,096 days | Yes | **Indeterminate** | Corrected pathway, date, join, and result |
| 3 | [Bio-Lab Conyers](validation/bio-lab-conyers.md) | Yes | Yes | 3 | Unclear | 2019-12-30 | 1,735 days | No | **Indeterminate** | First reconciliation validated |
| 4 | [Givaudan Sense Colour](validation/givaudan-sense-colour.md) | Yes | Yes | 2 | No | 2012-10-15 | 4,411 days | Yes | **Supports** | First reconciliation validated |
| 5 | [Dow Louisiana Operations](validation/dow-louisiana-operations.md) | Yes | Yes | 1 | Unclear | 2020-11-20 | 966 days | Unclear | **Indeterminate** | Corrected pathway, holders, join, and result |
| 6 | [PEMEX Deer Park](validation/pemex-deer-park.md) | Yes | Yes | 2 | Unclear | 2024-10-08 | 1–2 days | Unclear | **Indeterminate** | Corrected pathway, date, join, and result |
| 7 | [Cuisine Solutions](validation/cuisine-solutions.md) | Unclear | Unclear | Not established | Unclear | Unknown | Unquantifiable | Unclear | **Indeterminate** | Corrected suddenness only |
| 8 | [TS USA](validation/ts-usa.md) | Yes | Yes | 2 | Unclear | Unknown | Unquantifiable | Unclear | **Indeterminate** | Corrected date, join, suddenness, and result |

## Case-level reconciliation

### Shell Polymers

The 2023 process hazard analysis, incident-day process-control engineer recognition, console alarm, and two-motor-operated-valve reverse-flow mechanism form one coherent pathway. The report supports three distinct role-level holders but does not establish or negate a responsible-and-authorized cross-holder integrator. The phrase “unexpected state” is an alarm label rather than a narrative characterization of the event or warning pattern. The final result remains **indeterminate**.[1]

### U.S. Steel Clairton

The 2003 facility-siting recommendation belongs to a severity pathway, while the missing-planning evidence belongs to the water-washing and valve-overpressure pathway. The final record retains only the latter. Water washing had been practiced for at least three years and was known to workers and management, but missing procedures, training, permits, and hazard analysis do not by themselves prove that no cross-holder integration function was assigned. The result changes from **supports** to **indeterminate**.[2]

### Bio-Lab Conyers

The 2019 same-site corrosion failure, later inspection and insurer communications, and 2024 sprinkler failure remain on one corrosion and water-contact pathway. The report documents observed warning signs and a run-to-failure approach, but it does not resolve whether a role held both responsibility and authority to aggregate all relevant fragments. The first reconciliation remains **indeterminate**.[3]

### Givaudan Sense Colour

This is the sole supporting case. A 15 October 2012 reactivity test documented a self-sustained temperature rise and gas-driven pressure rise, and D.D. Williamson sent the results to an outside consultant. The CSB expressly found that no employee had been adequately assigned and trained to own process-safety-policy implementation, including oversight of hazard assessment, and directly linked that absence to the Reactor 5/6 team’s lack of the 2012 information. All required elements remain on the sugar-decomposition and relief-system-design pathway. The result is **supports**.[4]

### Dow Louisiana Operations

The first reconciliation combined the 2020 inerting-pressure signal with the separate work-light and vessel-closure pathway. On the coherent inerting pathway, the transmitter recording establishes reporting and the worker group establishes one holder, but a second organizational holder and affirmative absence of an assigned integration function are not established. The result changes from **supports** to **indeterminate**.[5]

### PEMEX Deer Park

The dated job aids and Blind 407 tag condition, their transfer from a PEMEX operator to a Repcon foreman, and the wrong-equipment opening form one coherent equipment-identification pathway. They establish a two-holder minimum and a one-to-two-day lead-time range. Separate permit hold-point, active-unit handoff, and simultaneous-operations deficiencies cannot establish an absent join for this pathway. The result changes from **supports** to **indeterminate**.[6]

### Cuisine Solutions

The CSB could not connect the same-day chilled-water-pump and temperature evidence to the unidentified initiating process upset. Signal, reporting, holders, and timing therefore remain unresolved. “Sudden pressure drop” describes a possible downstream liquid-carryover mechanism after a relief valve opened, not the event, initiating failure, or warning pattern. The result remains **indeterminate**, with suddenness corrected to unclear.[7]

### TS USA

The 2018 Mexico incident, cross-company reporting, corporate risk analysis, and 2024 event belong to the same water-in-cavity and salt-bath-overpressure pathway. However, the undated risk analysis prevents an exact earliest-signal date, and the report’s finding of ineffective knowledge management does not affirmatively establish that no responsible-and-authorized join had been assigned. “Rapidly expanded” describes reaction speed rather than an official suddenness characterization. The result changes from **supports** to **indeterminate**.[8]

## Raw coding consistency

The two original coder records agreed on **59 of 87 structured-field comparisons (67.8%)** under the initial comparison scheme. That denominator includes helper fields used to represent whether numeric bounds and counts were known. It is a transparency statistic, not a validated inter-rater reliability measure. Both coders were AI research agents working under the same task design.

More importantly, agreement did not guarantee validity. Both coders agreed on the Givaudan result, while several disagreements exposed ambiguity in join assignment, date precision, and suddenness. Independent validation then found that four of five initial supporting classifications did not satisfy the stricter pathway and affirmative-evidence rules.

## References

[1]: https://www.csb.gov/file.aspx?DocumentId=6343 "Furnace Explosion and Fire at Shell Polymers"

[2]: https://www.csb.gov/file.aspx?DocumentId=6340 "Fatal Coke Oven Gas Explosion at U.S. Steel Clairton Coke Works"

[3]: https://www.csb.gov/file.aspx?DocumentId=6339 "Chemical Decomposition, Fires, and Toxic Gas Release at KIK Consumer Products / Bio-Lab Conyers Facility"

[4]: https://www.csb.gov/file.aspx?DocumentId=6324 "Fatal Runaway Reaction and Explosion at Givaudan Sense Colour / D.D. Williamson"

[5]: https://www.csb.gov/file.aspx?DocumentId=6316 "Explosions, Fires, and Toxic Ethylene Oxide Release at Dow Louisiana Operations"

[6]: https://www.csb.gov/file.aspx?DocumentId=6315 "Fatal Hydrogen Sulfide Release at PEMEX Deer Park Refinery"

[7]: https://www.csb.gov/file.aspx?DocumentId=6304 "Hazardous Ammonia Release at Cuisine Solutions, Inc. Facility"

[8]: https://www.csb.gov/file.aspx?DocumentId=6296 "Explosion, Molten Salt Eruption, and Fatal Injury at TS USA Liquid Nitriding Facility"
