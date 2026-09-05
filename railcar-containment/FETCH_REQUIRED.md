# FETCH REQUIRED — FSRI e-mobility railcar fire report

Status: BLOCKED, needs a hand-fetch
Blocked on: figshare item refuses automated retrieval
Who can clear it: operator, by hand, on a connection that works
Opened: 2026-09-04

---

## 0. WHY THIS FILE EXISTS

Every quantitative FSRI number currently in this folder comes from the
landing page and the press release, not from the report itself. Those
sources are summaries: they carry headline values without test
conditions, instrument placement, or the full matrix.

This file is the tracked, in-repo form of that gap, so the hold is
visible to anyone reading the folder — not held in a queue outside it.

---

## 1. THE HOLD MARKER

Every number sourced from the landing page or press release carries, at
the point of use:

```
[FSRI-UNVERIFIED]
```

Rules:
- The marker goes at the POINT OF USE, not only in a manifest. A reader
  who reaches the number must see the hold without leaving the line.
- Anything derived from a marked number inherits the marker.
- Removing a marker requires the report in hand and the value checked
  against it. Nothing else clears it — not a second summary, not a
  citation of the summary elsewhere.
- A cleared value records what it was before clearing, if it changed.

---

## 2. WHAT IS BLOCKED ON THIS

```
Battery capacities            not retrieved
Full test matrix              not retrieved
Test conditions behind every
  cited value                 not retrieved
Instrument placement          not retrieved
```

Claims resting on the above, currently unverified for quantitative use:

```
t_available anchors           the calibration targets for all three
                              hazard channels in tenability.py — CO
                              dose, convective heat, optical density.
                              Each coefficient was bisection-calibrated
                              to a published anchor; the anchors are
                              the marked numbers.

Subway/intercity ratio        1:58 vs 3:50, 52%. Derived from the
                              anchors, so it inherits the marker.

Everything downstream of      t_hold ranges, detection_loop outputs,
tenability.py                 P(clear) figures including RC_005.
                              These are STRUCTURE-STABLE and
                              MAGNITUDE-UNVERIFIED: the inversion
                              (detection worth a lot at station egress,
                              nearly useless in tunnel) is a shape
                              result and does not turn on the anchor
                              values. The numbers attached to it do.
```

Not blocked on this, and not marked:

```
t_required                    FSRI declared it out of scope, so there
                              is no number to verify. Its absence is
                              the finding, and the report landing will
                              not change it.

Line geometry params          params/example_lines.json is
                              illustrative and declared as such.

The two weakest links         enclosure performance is ASSUMED and
                              flagged; RC_004's usable-margin
                              assumption is bench-testable and
                              independent of the report.
```

---

## 3. WHAT CHANGES WHEN IT LANDS

```
1  Check each anchor against the report. Record the delta, including
   zero deltas — a confirmed value is a result.
2  If an anchor moves, re-run the bisection calibration. Coefficients
   are derived, not stored independently.
3  Clear the markers on values checked. Leave markers on values the
   report does not cover — the report landing does not clear the whole
   set by itself.
4  If test conditions differ from what the folder's ENVELOPE assumes,
   the ENVELOPE is what gets edited first, before any number.
5  Re-run run_all.py. Note whether RC_005 survives the new anchors;
   it is the result most worth attacking and a magnitude change is a
   real test of it.
```

---

## 4. HANDLING WHILE BLOCKED

- Do not cite the marked numbers as measured values anywhere outside
  this folder.
- Do not substitute an interpolation, a nearby published value, or a
  reconstructed estimate for a marked number. An absent value stays
  absent; a substituted one is unrecoverable later.
- Structure results may be discussed without the report. Magnitude
  results may not.
- Do not attempt automated retrieval again. It is refused, and repeated
  attempts produce no information.
