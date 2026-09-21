# WO-2 pilot codebook

## Purpose

This codebook operationalizes the five variables named in WO-2 for a bounded pilot over public accident-investigation reports. The pilot is descriptive. It does not estimate a population base rate or establish that the proposed four-part structure applies across domains.[1]

## Sampling rule fixed before coding

The sample consists of the **eight most recently published U.S. Chemical Safety and Hazard Investigation Board final incident-investigation reports** that can be identified from the agency’s official completed-investigation materials as of **19 September 2026**.

A record is eligible when it concerns a specific incident, has a publicly accessible final investigation report, and contains enough pre-event chronology to apply the codebook. General studies, safety videos, interim products, duplicate incident pages, and records without a final report are excluded. If an otherwise eligible report is inaccessible, the source manifest must record the exclusion and replace it with the next report under the same ordering rule.

The discovery phase determines the sample without reference to whether a case supports the WO-2 decomposition. Coders receive the resulting manifest and do not select cases.

## Unit of analysis

The unit is one investigated incident and its official final report. A **signal** is a pre-event observation, measurement, alarm, defect, deviation, inspection result, near miss, complaint, or other documented state that is directionally related to the hazard mechanism identified in the final report.

Routine background knowledge is not a case-specific signal unless the report connects it to the incident equipment, process, site, or operating condition before the event.

## Coding variables

| Variable | Allowed values | Operational rule |
| --- | --- | --- |
| `signal_present` | `yes`, `no`, `unclear` | `yes` requires at least one documented pre-event signal related to the incident hazard. `no` requires an affirmative basis that no such signal existed in the available record. Missing evidence is `unclear`, not `no`. |
| `signal_reported` | `yes`, `no`, `unclear`, `not_applicable` | `yes` requires evidence that a holder communicated or recorded the signal beyond private awareness before the event. A maintenance entry, alarm visible to another role, inspection finding, shift handoff, email, meeting, or formal report qualifies. Use `not_applicable` only when `signal_present = no`. |
| `holder_count_min` | non-negative integer or `null` | Conservative lower bound on distinct people, roles, teams, contractors, or organizational units documented as holding a relevant fragment before the event. Count a role once unless the report establishes distinct holders. Use `null` when the source cannot support a lower bound. |
| `join_assigned` | `yes`, `no`, `unclear`, `not_applicable` | `yes` requires a named role or function with both responsibility and authority to aggregate the relevant cross-holder signals before the event. Ownership of one inspection, alarm, maintenance task, or risk category does not by itself qualify. `no` requires affirmative evidence that fragments were distributed without such an integration point. Missing role information is `unclear`. |
| `first_signal_date` | ISO date, year-month, year, relative interval, or `unknown` | Earliest pre-event signal supported by the report. Preserve the source’s precision rather than inventing a date. |
| `event_date` | ISO date | Date of the investigated event. |
| `lead_time_days_min` | non-negative number or `null` | Minimum defensible days from the earliest documented signal to the event. |
| `lead_time_days_max` | non-negative number or `null` | Maximum defensible days where the source gives a bounded range. Equal to the minimum for an exact interval. `null` indicates an open or unquantifiable upper bound. |
| `sudden_label` | `yes`, `no`, `unclear` | Whether official material characterizes the event, failure, or warning pattern as sudden, unexpected, unforeseen, without warning, or a close equivalent. A coder must quote the language. |
| `pattern_result` | `supports`, `does_not_support`, `indeterminate` | `supports` requires `signal_present = yes`, `signal_reported = yes`, `holder_count_min >= 2`, and `join_assigned = no`. `does_not_support` requires evidence that at least one necessary element is false. Any unresolved necessary element yields `indeterminate`. |

## Evidence rules

Every non-`unclear` value must be supported by an exact quotation or a tightly located paraphrase from an official final report or its official investigation page. Page numbers refer to printed report pages where available; PDF page numbers may also be recorded. Secondary reporting can identify a source but cannot determine a coded value.

A report’s causal finding controls over a coder’s engineering intuition. Coders must not infer that a warning was meaningful merely because it preceded the event. The source must connect the warning to the hazard mechanism or failure sequence.

## Independent coding and reconciliation

Two coders apply this codebook independently to every case. They do not see each other’s outputs during the first pass. A separate reconciliation pass compares values and evidence. Agreement is reported by variable. Disagreements are not silently averaged: the reconciled record states which value was retained, why, and whether the case remains indeterminate.

Because the coders are AI research agents operating from the same task design, their agreement is not equivalent to human inter-rater reliability. The duplicate pass is a consistency and ambiguity check, not a validated psychometric measure.

## Interpretation limits

The sample is bounded to one investigating agency and one report genre. Eight cases are sufficient to test whether the instrument can be applied and falsified, but not to estimate prevalence. Selection by publication recency avoids hand-picking for the target pattern, yet agency case selection and report availability remain upstream filters.

A finding that several cases support the pattern would show recurrence within this pilot. It would not prove that the aggregation step was unownable, that every event called sudden was signalled, or that the same rate applies in aviation, transport, medicine, intelligence, or structural engineering.

## References

[1]: https://github.com/JinnZ2/chain-position-detectability/blob/main/work-orders/WO-2-quiet-failure-missing-aggregation.md "WO-2 — Quiet failure as a missing aggregation function"
