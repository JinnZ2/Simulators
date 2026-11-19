# Excerpt of P3/docs/glossary.md, original line numbers kept (lines 122-142 of 142). Lines not shown are omitted, not empty.

  122| ## Open-slot statuses and their exits
  123| 
  124| | Term | Role | Defined in |
  125| |---|---|---|
  126| | `PENDING` / `UNKNOWN` | A slot whose value is not yet known. Never read as zero or as absent. | per module; listed in `docs/expiry_register.json` |
  127| | `expiry_condition` | Instrument class, sensitivity or protocol whose null result would downgrade a PENDING / UNKNOWN slot. Filled only from the slot's own text; otherwise `VOID -- no exit defined`. | `docs/expiry_register.json` |
  128| | `expiry_source` | `file:line` or citation where that exit is already stated; `VOID` when none is. | `docs/expiry_register.json` |
  129| | `ABSENT_AT_SENSITIVITY(<value>)` | Scoped absence: looked for with a stated instrument / sensitivity / protocol and not found at that sensitivity. Never written as bare "absent". No slot holds it yet. | `docs/expiry_register.json` |
  130| 
  131| ## Audit coverage terms (`calibration/unified_audit.py`)
  132| 
  133| One name, `GAP_INSTRUMENT`, was used in two senses on two branches. Both
  134| senses are kept under split names (2026-11-11). The bare name is retired.
  135| 
  136| | Term | Meaning | Defined in |
  137| |---|---|---|
  138| | `GAP_INSTRUMENT_CRASH` | A module raised; nothing was measured. Coverage, not severity (#82 sense) | `calibration/unified_audit.py` |
  139| | `GAP_INSTRUMENT_UNRECOGNIZED_LABEL` | A module returned a status outside `_STATUS_RANK`; it emitted no severity that can be ranked (#84 sense) | `calibration/unified_audit.py` |
  140| | `ALL_MODULES_GAP_INSTRUMENT_CRASH` | `not_determinable_reason`: every non-measured status is a crash | `calibration/unified_audit.py` |
  141| | `ALL_MODULES_GAP_INSTRUMENT_UNRECOGNIZED_LABEL` | `not_determinable_reason`: every non-measured status is an unrecognized label | `calibration/unified_audit.py` |
  142| | `MIXED_UNKNOWN_AND_GAP_INSTRUMENT` | `not_determinable_reason`: UNKNOWN and gap-instrument statuses both present | `calibration/unified_audit.py` |
