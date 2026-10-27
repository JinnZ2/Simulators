# WORK ORDER (delivered verbatim, 2026-10-08)

The dispatch as delivered, both parts. PART 1 concerns PR #126 and was
carried out on that branch. PART 2 is this folder. The text is not edited.

```text
DISPATCH — #126 follow-up + MOVING-MEAN TRACKER build

PART 1 — PR #126 (pathways runner)
Context: another session (session_01U4mRsf…) pushed the runner
build at 14:06; this session's parallel build was NOT pushed —
correct, a second AMENDMENT 3 would break the hash chain.
1. Discard the duplicate-build patches in scratchpad. Do not push.
2. Fix --import-runner arg parsing: use argparse; sheet/key as
   named options; refuse any path that starts with "--". Add a
   test: passing "--out" as a path → error, no file named --out.
3. Chat side loaded the job into the runner (no CC action):
   job file sha256 5e55685f8f8922186a843782c773456e5d72394550626114c123528382b86457
   (raw bytes @5a9642e); all 270 prompt hashes recomputed under the
   runner rule: 0 mismatches. Order seed 1114932034, recorded at
   load before any call. Record both in HOLDS footnote for the pilot.
4. Then apply the standing PR rule to #126 (failures == pins by id,
   no conflicts, paths within declared allowed_paths → merge).

PART 2 — MOVING-MEAN TRACKER (new build; HOLDS row first,
declare allowed_paths before starting)
Repo: JinnZ2/Simulators, folder moving-mean-tracker/ · stdlib only · CC0
Purpose: a mean anchored to moving targets (GDP, wealth gap,
skills/literacy) drifts with them; any norm, filter or loss tied to
the mean inherits the drift. Track it per segment, with provenance,
on a fixed schedule. Status: PROPOSED instrument, no data yet.

SCHEDULE  interval declared in config (default quarterly); every run
          appended to a run log, never overwritten.
SEGMENTS  declared in config before run 1 (e.g. income/wealth band,
          region, connectivity tier, desk vs hands-on occupation,
          AI-tool access). Definitions frozen; any change = new dated
          version, and cross-version comparisons are flagged.
PROVIDER  dumb interface: provider returns records + provenance only.
          No interpretation, scoring or conclusions in the provider.
          Ship a fixture provider (synthetic data) — live sources are
          added later; network may be unavailable, so no live fetch
          is required for this build.
PER RECORD provenance: source, pull_date, query, filters_applied,
          dropped (bool) + drop_rule if dropped.
PER RUN, PER SEGMENT: n, mean, median, p10, p90, mean_minus_median;
          sample_share vs population_share (population reference
          named + dated, else UNRATED).
GAUGES (series across runs):
  G1 mean − median gap          → tail pull on the reference
  G2 sample share − pop share   → access-gate loop running
  G3 dropped-as-noise share per segment → cleaning as class filter
  G4 metric in physical units vs dollars (when a physical unit is
     declared for the metric) → token drift vs real change
RULES: segments + metrics declared before run 1 · every dropped
  record logged with its rule · undeclared population reference →
  G2 UNRATED, never 0 · fewer than declared min_n in a segment →
  INSUFFICIENT_SAMPLE for that segment, not a value.
TESTS (fixtures): tail added to top segment only → G1 widens while
  median unchanged; segment dropped by a filter → G3 rises for that
  segment only; segment definition changed between runs → flagged,
  no silent comparison; missing population reference → UNRATED.
  Tests and module share an author → mark SELF-GRADED in README.

End report with PR + compare links.
```
