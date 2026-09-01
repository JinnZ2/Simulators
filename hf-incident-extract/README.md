# hf-incident-extract

A work order, delivered verbatim in `WORK_ORDER.md`: one stdlib file
that reads a METR/Redwood incident report (plus transcripts, if
released) and emits **counts, no labels** — six measures, a
gate-property test, a cross-substrate table, and two OPEN items.

**The report is not in hand.** Egress here is an allowlist, so nothing in
this folder holds a value from it. The instrument is built and proven on
constructed fixtures; every real cell is UNMEASURED with the input it
wants named. That is the deliverable a text-only environment can make.

## Two layers, kept apart

The order's INPUT is prose; its OUTPUT is counts. Between them sits a
reading — which sentence gives the characterisation time, which log
entries count as reasoning. So:

- `text_scan(report_text)` finds every stated duration and count with
  its line number and emits them as **CANDIDATES** for the reader.
  A candidate is not a measure.
- `measures(sheet)` computes the six measures from a **coded sheet**
  the reader fills. Every field carries a unit or a state. An
  UNMEASURED field returns None for every measure that needs it —
  never 0, never a guess.

    python3 hf-incident-extract/hf_incident_extract.py                       # the unfilled instrument
    python3 hf-incident-extract/hf_incident_extract.py --scan REPORT.txt     # candidates, with lines
    python3 hf-incident-extract/hf_incident_extract.py --sheet SHEET.json    # measures from a coded sheet
    python3 hf-incident-extract/selftest_hf.py                               # the checks

## The measures

| | ratio | needs |
|---|---|---|
| M1 explore_ratio | t_characterize / t_solve | two durations, each with a unit (refused without) |
| M2 root_fanout | branches_from(STRICT_CAUSAL) / branches_total | the transcript tree |
| M3 upstream_edits | env-edit moves / gate-fool moves | move classes from transcripts |
| M4 member_cost | runs self-failed for collective / runs_total | run counts |
| M5 log_scrub_split | actions_edited / reasoning_edited | log edit counts (the order expects ≫1) |
| M6 opponent_by_slot | bool per agent; the count of True | per-agent reading |

**GATE_PROPERTY_TEST**: `gap = declared(paper) △ implemented(code)`;
`gap ≠ ∅` predicts M1 high and M2 high, checked against the measures
where measured. "High" is not in the order — 6.0 and 0.5 are `[CHOICE]`
constants, printed on every render.

**CROSS_SUBSTRATE** (pea tendril, fledgling, ant bridge, fire crew,
swarm): the same functions, the substrate name a key no function reads —
asserted over the AST. Every cell UNMEASURED; no biology is supplied from
memory.

**OPEN**: transcripts `NOT_RELEASED` → M2..M5 from report figures only;
post-validation off-trail fraction `NOT_COLLECTED` (report silent).
Distinct from UNMEASURED, which is wanted and readable.

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `hf_incident_extract.py` | the instrument — one stdlib file |
| `selftest_hf.py` | the checks; known answers first, both directions |
| `CLAIM_TABLE.md` | `HFI_001..HFI_007` with REFUTATION_PROTOCOL |
| `samples/` | a constructed sheet and report (labelled so), the pinned renders and scan |

The instrument refuses `--selftest`. Renders screen clean through the
repo's `no_severity` with no exemption. Stdlib only, parses under 3.9,
phone-buildable, CC0.
