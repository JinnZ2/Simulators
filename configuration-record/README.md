# configuration-record

CC0. Co-authored. Stdlib only, parses under Python 3.9.

This folder holds one record per observed AI configuration, time-stamped.
The record lists components, positions, channels, the authority chain,
maintenance, frame exit, bounds and design source. Roles are derived from
positions and never set by hand.

## Files

- `config_schema.json`: the schema (version 1.0, written 2026-11-13).
- `config_record.py`: the validator, role derivation, flags and the axis separation check.
- `examples/chat_model_tool_api.json`: an EXAMPLE (a chat model, a tool connector and an API channel). It is not observed data, and it carries `"example": true`.
- `samples/run.sample.txt`: the selftest and every CLI command run on the example.

## Commands

```
python3 config_record.py --selftest
python3 config_record.py validate FILE [FILE ...]
python3 config_record.py derive FILE [--decide X] [--reach Y]
python3 config_record.py flags FILE
python3 config_record.py separation FILE [FILE ...]
```

`validate` exits 1 when any record is refused.

## Value rules

- An axis is `{"value": 0.0-1.0, "basis": "..."}` or `{"value": "VOID", "reason": "..."}`.
- Text fields are non-blank text, or VOID with a reason.

The validator refuses:

- blank fields;
- VOID without a reason;
- an axis value without a basis;
- a value out of range;
- an unknown component reference;
- a component with no maintenance entry or no bounds entry;
- `roles_at_t` given by hand.

## Layers

`substrate`, `algorithm`, `model`, `system`, `channel`, `tool`, `physical`.

A `physical` component also carries `kind`, which is one of `actuator`,
`sensor`, `mechanical`, `power` or `environment`.

## Roles

A role is read from positions at a given t, never from a component's name or layer.

The rule is a [CHOICE] set on 2026-11-13. It is printed with every derivation, and the thresholds can be overridden:

- decider if `chooses_vs_executes >= 0.5`;
- else executor if `reach_on_world >= 0.1`;
- else carrier.

If an axis the rule needs is VOID, the role is VOID and carries the reason.

A record may carry `roles_at_t` only if it equals the derivation and carries `derived_by`. Otherwise the record is refused as hand-set.

## Flags

| flag | condition |
|---|---|
| `FRAGMENTED` | `whole_holders` is an empty list (whole_holder_count = 0) |
| `WHOLE_HOLDERS_UNKNOWN` | `whole_holders` is VOID; not read as 0 |
| `CLOSED-FRAME` | `frame_exit` is an empty list |
| `FRAME_EXIT_UNKNOWN` | `frame_exit` is VOID; not read as closed |
| `BOUNDS_EXCEEDED` | an authority-chain entry has `operated_within_bounds` = no |
| `EXAMPLE` | the record is marked as an example |

## Bounds

Energy and physical limits are recorded per component, and once more for the whole configuration. No layer is exempt, AI included.

## Design source

This field is PROPOSED and untested. `segmentation_origin` is one of:

- `chosen_for_task`;
- `inherited_from_corpus`;
- VOID with a reason.

## Expiry

The schema expires when either holds:

- a component no longer fits any one layer;
- an axis stops separating configurations.

On expiry, fork to a new version and keep the old records readable.

The validator reports a layer outside the set as `LAYER_UNFIT`, naming the fork rule. `separation` reports each axis across two or more records as `SEPARATES` or `EXPIRY_CANDIDATE`.

## Links

- automation-maintenance-accountability-gap (not in repo)
- `automation-gap/` (related folder in this repository)
